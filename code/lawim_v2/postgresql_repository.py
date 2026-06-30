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


def _adapt_sql(sql: str) -> str:
    adapted = sql.replace("INSERT OR REPLACE INTO schema_meta", "INSERT INTO schema_meta")
    if "INSERT INTO schema_meta" in adapted and "ON CONFLICT" not in adapted:
        adapted = adapted.replace(
            "VALUES (?, ?)",
            "VALUES ($1, $2) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
        )

    counter = 0

    def replace_placeholder(_match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        return f"${counter}"

    return re.sub(r"\?", replace_placeholder, adapted)


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
        add_returning = (
            adapted.strip().upper().startswith("INSERT INTO")
            and "RETURNING" not in adapted.upper()
            and "schema_meta" not in adapted.lower()
        )
        if add_returning:
            adapted = adapted.rstrip().rstrip(";") + " RETURNING id"
        run_kwargs = {f"__p{i}": value for i, value in enumerate(params)}
        try:
            rows = list(self._conn.run(adapted, **run_kwargs) or [])
        except Exception as exc:
            if add_returning:
                adapted = _adapt_sql(sql)
                try:
                    rows = list(self._conn.run(adapted, **run_kwargs) or [])
                except Exception as retry_exc:
                    raise _map_pg_exception(retry_exc) from retry_exc
            else:
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
            WHERE table_schema = 'public' AND table_name = %s
            """,
            (table,),
        ).fetchall()
        return {str(row["column_name"]) for row in rows}

    def _apply_migrations(self, conn: Any) -> None:
        return
