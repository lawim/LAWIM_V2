from __future__ import annotations

import re
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .db import DemoSeed, LawimRepository, SCHEMA_VERSION
from .persistence import build_postgresql_profile, build_schema_fingerprint, build_application_schema_manifest
from .schema_ddl import POSTGRESQL_INIT_STATEMENTS


_POSTGRESQL_REPLACE_CONFLICT_TARGETS: dict[str, tuple[str, ...]] = {
    "reasoning_traces": ("project_id", "trace_key"),
    "knowledge_inferences": ("project_id", "inference_key"),
    "next_best_actions": ("project_id", "action_key"),
    "intelligence_snapshots": ("project_id", "snapshot_key"),
    "knowledge_snapshots": ("project_id", "snapshot_key"),
    "expert_knowledge_indexes": ("document_id", "index_key"),
    "expert_knowledge_publications": ("publication_key",),
    "crm_contact_consents": ("contact_id", "consent_type"),
    "crm_customer_scores": ("contact_id", "score_key"),
    "iam_user_roles": ("user_id", "role_id"),
    "rei_verification_checks": ("property_id", "check_key"),
    "rei_verification_scores": ("property_id",),
    "rei_visit_reports": ("visit_id",),
    "rei_intelligence_scores": ("property_id", "score_key"),
    "rei_search_index": ("property_id",),
}


def _extract_postgresql_id_returning_tables() -> frozenset[str]:
    tables: set[str] = set()
    table_pattern = re.compile(r"^\s*CREATE TABLE IF NOT EXISTS\s+([A-Za-z_][A-Za-z0-9_]*)", re.IGNORECASE | re.DOTALL)
    id_pattern = re.compile(r"^\s*id\s+(?:SERIAL|BIGSERIAL|SMALLSERIAL|INTEGER|INT|BIGINT)\b", re.IGNORECASE | re.MULTILINE)
    for statement in POSTGRESQL_INIT_STATEMENTS:
        match = table_pattern.match(statement)
        if match and id_pattern.search(statement):
            tables.add(match.group(1))
    return frozenset(tables)


_POSTGRESQL_ID_RETURNING_TABLES = _extract_postgresql_id_returning_tables()


def _should_return_postgresql_id(sql: str) -> bool:
    if "RETURNING" in sql.upper():
        return False
    match = re.match(r"^\s*INSERT\s+INTO\s+([A-Za-z_][A-Za-z0-9_]*)\b", sql, re.IGNORECASE)
    if not match:
        return False
    table = match.group(1)
    if table == "schema_meta":
        return False
    return table in _POSTGRESQL_ID_RETURNING_TABLES


def _adapt_sql(sql: str) -> str:
    adapted = _normalize_postgresql_create_table(sql)
    adapted = adapted.replace("INSERT OR REPLACE INTO schema_meta", "INSERT INTO schema_meta")
    if "INSERT INTO schema_meta" in adapted and "ON CONFLICT" not in adapted:
        adapted = adapted.replace(
            "VALUES (?, ?)",
            "VALUES ($1, $2) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
        )
    adapted = _rewrite_postgresql_insert_conflicts(adapted)

    counter = 0

    def replace_placeholder(_match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        return f"${counter}"

    return re.sub(r"\?", replace_placeholder, adapted)


def _rewrite_postgresql_insert_conflicts(sql: str) -> str:
    stripped = sql.lstrip()
    if not stripped.upper().startswith("INSERT OR "):
        return sql

    ignore_match = re.match(r"^\s*INSERT OR IGNORE INTO\s+", sql, re.IGNORECASE)
    if ignore_match:
        return re.sub(r"^\s*INSERT OR IGNORE INTO\s+", "INSERT INTO ", sql, count=1, flags=re.IGNORECASE).rstrip() + " ON CONFLICT DO NOTHING"

    replace_match = re.match(
        r"^\s*INSERT OR REPLACE INTO\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:\((.*?)\))?\s*(VALUES\b.*|SELECT\b.*)$",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if not replace_match:
        return sql

    table = replace_match.group(1)
    columns_block = replace_match.group(2)
    tail = replace_match.group(3).rstrip()
    if table == "schema_meta":
        return sql

    conflict_target = _POSTGRESQL_REPLACE_CONFLICT_TARGETS.get(table)
    if not conflict_target:
        return re.sub(r"^\s*INSERT OR REPLACE INTO\s+", "INSERT INTO ", sql, count=1, flags=re.IGNORECASE).rstrip() + " ON CONFLICT DO NOTHING"
    if not columns_block:
        return re.sub(r"^\s*INSERT OR REPLACE INTO\s+", "INSERT INTO ", sql, count=1, flags=re.IGNORECASE).rstrip() + " ON CONFLICT DO NOTHING"

    columns = [column.strip() for column in columns_block.split(",") if column.strip()]
    update_columns = [column for column in columns if column not in conflict_target]
    if not update_columns:
        return re.sub(r"^\s*INSERT OR REPLACE INTO\s+", "INSERT INTO ", sql, count=1, flags=re.IGNORECASE).rstrip() + " ON CONFLICT DO NOTHING"

    assignments = ", ".join(f"{column} = EXCLUDED.{column}" for column in update_columns)
    conflict_clause = ", ".join(conflict_target)
    return f"INSERT INTO {table} ({columns_block}) {tail} ON CONFLICT ({conflict_clause}) DO UPDATE SET {assignments}"


def _normalize_postgresql_create_table(sql: str) -> str:
    stripped = sql.lstrip()
    if not stripped.upper().startswith("CREATE TABLE"):
        return sql

    output: list[str] = []
    seen_columns: set[str] = set()
    inside_table = False

    def trim_trailing_comma() -> None:
        for index in range(len(output) - 1, -1, -1):
            candidate = output[index]
            if candidate.strip():
                output[index] = candidate.rstrip().rstrip(",")
                return

    def expand_line_fragments(line: str) -> list[str]:
        stripped_line = line.strip()
        if not inside_table:
            return [line]
        if not stripped_line:
            return [line]
        if stripped_line.startswith(("FOREIGN KEY", "PRIMARY KEY", "UNIQUE", "CHECK", "CONSTRAINT", ")")):
            return [line]
        if "," not in line:
            return [line]

        parts = [part.strip() for part in line.split(",") if part.strip()]
        if len(parts) <= 1:
            return [line]

        indent = re.match(r"^\s*", line).group(0)
        ends_with_comma = line.rstrip().endswith(",")
        fragments: list[str] = []
        for index, part in enumerate(parts):
            suffix = "," if ends_with_comma or index < len(parts) - 1 else ""
            fragments.append(f"{indent}{part}{suffix}")
        return fragments

    for line in sql.splitlines():
        if not inside_table:
            output.append(line)
            if "(" in line:
                inside_table = True
            continue

        for fragment in expand_line_fragments(line):
            stripped_line = fragment.strip()
            upper_line = stripped_line.upper()

            if not stripped_line:
                output.append(fragment)
                continue

            if upper_line.startswith(")"):
                trim_trailing_comma()
                output.append(fragment)
                inside_table = False
                break

            if upper_line.startswith(("FOREIGN KEY", "PRIMARY KEY", "UNIQUE", "CHECK", "CONSTRAINT")):
                output.append(fragment)
                continue

            match = re.match(r"^(\s*)([A-Za-z_][A-Za-z0-9_]*)\b(.*)$", fragment)
            if not match:
                output.append(fragment)
                continue

            indent, column_name, _ = match.groups()
            if column_name not in seen_columns:
                seen_columns.add(column_name)
                output.append(fragment)
                continue

            # Drop duplicated PostgreSQL column declarations emitted by the generated
            # runtime DDL. The first plain column definition is kept and the
            # duplicate line is discarded to preserve creation order.

    return "\n".join(output)


def _map_pg_exception(exc: Exception) -> Exception:
    if exc.__class__.__name__ != "DatabaseError":
        return exc
    payload = exc.args[0] if exc.args else None
    if isinstance(payload, dict) and payload.get("C") == "23505":
        return sqlite3.IntegrityError("duplicate key")
    return exc


class _PgCursor:
    def __init__(self, columns: list[str], rows: list[tuple[Any, ...]], last_row_id: int | None = None) -> None:
        self._columns = columns
        self._rows = rows
        self._index = 0
        self.lastrowid = last_row_id

    def fetchone(self) -> dict[str, Any] | None:
        if self._index >= len(self._rows):
            return None
        row = self._rows[self._index]
        self._index += 1
        return dict(zip(self._columns, row, strict=False))

    def fetchall(self) -> list[dict[str, Any]]:
        remaining = self._rows[self._index :]
        self._index = len(self._rows)
        return [dict(zip(self._columns, row, strict=False)) for row in remaining]


class _PgConnection:
    def __init__(self, native_connection: Any) -> None:
        self._conn = native_connection
        self._in_transaction = False

    def execute(self, sql: str, params: tuple[object, ...] = ()) -> _PgCursor:
        adapted = _adapt_sql(sql)
        add_returning = _should_return_postgresql_id(adapted)
        if add_returning:
            adapted = adapted.rstrip().rstrip(";") + " RETURNING id"
        run_kwargs = {f"__p{i}": value for i, value in enumerate(params)}
        try:
            rows = list(self._conn.run(adapted, **run_kwargs) or [])
        except Exception as exc:
            raise _map_pg_exception(exc) from exc
        columns_meta = self._conn.columns or []
        columns = [col["name"] if isinstance(col, dict) else str(col) for col in columns_meta]
        last_id = None
        if rows and columns and "id" in columns:
            last_id = rows[0][columns.index("id")]
        return _PgCursor(columns, rows, last_id)

    def executescript(self, script: str) -> None:
        for statement in script.split(";"):
            cleaned = statement.strip()
            if cleaned:
                self.execute(cleaned)

    def begin(self) -> None:
        self._conn.run("BEGIN")

    def commit(self) -> None:
        self._conn.run("COMMIT")

    def rollback(self) -> None:
        self._conn.run("ROLLBACK")

    def __enter__(self) -> "_PgConnection":
        self.begin()
        self._in_transaction = True
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self._in_transaction = False


def parse_postgres_dsn(dsn: str) -> dict[str, Any]:
    parsed = urlparse(dsn)
    if parsed.scheme not in {"postgresql", "postgres"}:
        raise ValueError("LAWIM_DATABASE_URL must use postgresql:// scheme")
    database = parsed.path.lstrip("/") or "lawim_v2"
    return {
        "user": parsed.username or "lawim",
        "password": parsed.password or "lawim",
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 5432,
        "database": database,
    }


def postgres_available() -> bool:
    try:
        import pg8000.native  # noqa: F401

        return True
    except ImportError:
        return False


def check_postgres_connection(dsn: str) -> bool:
    if not postgres_available():
        return False
    import pg8000.native

    params = parse_postgres_dsn(dsn)
    try:
        connection = pg8000.native.Connection(**params)
        connection.run("SELECT 1")
        connection.close()
        return True
    except Exception:
        return False


class PostgreSQLLawimRepository(LawimRepository):
    driver = "postgresql"

    def __init__(self, dsn: str, seed: DemoSeed | None = None) -> None:
        import pg8000.native

        self.dsn = dsn
        self.db_path = Path("postgresql")
        params = parse_postgres_dsn(dsn)
        native = pg8000.native.Connection(**params)
        self.connection = _PgConnection(native)
        self.lock = threading.RLock()
        self.seed = seed or DemoSeed()

    def _configure_connection(self) -> None:
        return

    def close(self) -> None:
        with self.lock:
            self.connection._conn.close()

    @contextmanager
    def _transaction(self):
        with self.lock:
            with self.connection as conn:
                yield conn

    def initialize(self, seed_demo_data: bool = True) -> None:
        import json

        with self._transaction() as conn:
            for statement in POSTGRESQL_INIT_STATEMENTS:
                if statement == "CREATE INDEX IF NOT EXISTS idx_crm_lead_sources_reference_code ON crm_lead_sources(reference_code)":
                    conn.execute(
                        "ALTER TABLE crm_lead_sources ADD COLUMN IF NOT EXISTS reference_code TEXT NOT NULL DEFAULT ''"
                    )
                    conn.execute(
                        "ALTER TABLE crm_lead_sources ADD COLUMN IF NOT EXISTS channel TEXT NOT NULL DEFAULT 'web'"
                    )
                    conn.execute(
                        "ALTER TABLE crm_lead_sources ADD COLUMN IF NOT EXISTS target TEXT NOT NULL DEFAULT 'acquisition'"
                    )
                    conn.execute(
                        "ALTER TABLE crm_lead_sources ADD COLUMN IF NOT EXISTS status TEXT NOT NULL DEFAULT 'active'"
                    )
                    conn.execute(
                        "ALTER TABLE crm_lead_sources ADD COLUMN IF NOT EXISTS created_by INTEGER"
                    )
                    conn.execute(
                        "ALTER TABLE crm_lead_sources ADD COLUMN IF NOT EXISTS metadata_json TEXT NOT NULL DEFAULT '{}'"
                    )
                    conn.execute(
                        "ALTER TABLE crm_lead_sources ADD COLUMN IF NOT EXISTS updated_at TEXT NOT NULL DEFAULT ''"
                    )
                conn.execute(statement)
            metadata = {
                "schema_version": str(SCHEMA_VERSION),
                "schema_manifest": json.dumps(build_application_schema_manifest(), ensure_ascii=False, sort_keys=True),
                "schema_fingerprint": build_schema_fingerprint(build_application_schema_manifest()),
            }
            for key, value in metadata.items():
                conn.execute(
                    "INSERT INTO schema_meta (key, value) VALUES (?, ?) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
                    (key, value),
                )
        if seed_demo_data:
            self.seed_demo_data()

    def backend_profile(self) -> dict[str, object]:
        profile = build_postgresql_profile(self.dsn, self.schema_version())
        profile["adapter"] = "postgresql-repository"
        profile["status"] = "active"
        return profile

    def one(self, sql: str, params: tuple[object, ...] = ()) -> dict[str, object] | None:
        with self.lock:
            cursor = self.connection.execute(sql, params)
            row = cursor.fetchone()
        return row

    def all(self, sql: str, params: tuple[object, ...] = ()) -> list[dict[str, object]]:
        with self.lock:
            cursor = self.connection.execute(sql, params)
            rows = cursor.fetchall()
        return rows

    def _table_columns(self, conn: Any, table: str) -> set[str]:
        rows = conn.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = ?
            """,
            (table,),
        ).fetchall()
        return {str(row["column_name"]) for row in rows}

    def _apply_migrations(self, conn: Any) -> None:
        return
