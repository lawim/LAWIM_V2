from __future__ import annotations

import re
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .db import DemoSeed, LawimRepository, SCHEMA_VERSION
from .persistence import build_postgresql_profile, build_schema_fingerprint, build_application_schema_manifest


POSTGRESQL_INIT_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS organizations (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        slug TEXT NOT NULL UNIQUE,
        kind TEXT NOT NULL DEFAULT 'agency',
        city TEXT,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        organization_id INTEGER REFERENCES organizations(id),
        password_salt TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS properties (
        id SERIAL PRIMARY KEY,
        listing_code TEXT UNIQUE,
        title TEXT NOT NULL,
        summary TEXT NOT NULL,
        address_line TEXT,
        city TEXT NOT NULL,
        region TEXT,
        postal_code TEXT,
        country TEXT NOT NULL,
        search_key TEXT,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        price_min INTEGER,
        price_max INTEGER,
        currency TEXT NOT NULL,
        status TEXT NOT NULL,
        availability TEXT NOT NULL DEFAULT 'available',
        property_type TEXT NOT NULL,
        owner_organization_id INTEGER REFERENCES organizations(id),
        bedrooms INTEGER NOT NULL DEFAULT 0,
        bathrooms INTEGER NOT NULL DEFAULT 0,
        area_sqm DOUBLE PRECISION NOT NULL DEFAULT 0,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        version INTEGER NOT NULL DEFAULT 1,
        published_at TEXT,
        deleted_at TEXT,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS media (
        id SERIAL PRIMARY KEY,
        property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
        kind TEXT NOT NULL,
        url TEXT NOT NULL,
        caption TEXT NOT NULL,
        storage_path TEXT,
        mime_type TEXT,
        size_bytes INTEGER,
        thumbnail_url TEXT,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        position INTEGER NOT NULL DEFAULT 0,
        version INTEGER NOT NULL DEFAULT 1,
        deleted_at TEXT,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS conversations (
        id SERIAL PRIMARY KEY,
        property_id INTEGER REFERENCES properties(id),
        user_id INTEGER NOT NULL REFERENCES users(id),
        subject TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
        sender_user_id INTEGER NOT NULL REFERENCES users(id),
        body TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        kind TEXT NOT NULL,
        payload TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS schema_meta (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_properties_status_city ON properties(status, city)",
    "CREATE INDEX IF NOT EXISTS idx_properties_search_key ON properties(search_key)",
    "CREATE INDEX IF NOT EXISTS idx_properties_deleted_at ON properties(deleted_at)",
    "CREATE INDEX IF NOT EXISTS idx_media_property_position ON media(property_id, position)",
    "CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token)",
    "CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id, created_at)",
)


def _adapt_sql(sql: str) -> str:
    adapted = sql.replace("INSERT OR REPLACE INTO schema_meta", "INSERT INTO schema_meta")
    if "INSERT INTO schema_meta" in adapted and "ON CONFLICT" not in adapted:
        adapted = adapted.replace(
            "VALUES (?, ?)",
            "VALUES (%s, %s) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
        )
    return adapted.replace("?", "%s")


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
        add_returning = adapted.strip().upper().startswith("INSERT INTO") and "RETURNING" not in adapted.upper()
        if add_returning:
            adapted = adapted.rstrip().rstrip(";") + " RETURNING id"
        try:
            result = self._conn.run(adapted, params)
        except Exception:
            if add_returning:
                adapted = _adapt_sql(sql)
                result = self._conn.run(adapted, params)
            else:
                raise
        columns = [col["name"] if isinstance(col, dict) else str(col) for col in getattr(result, "columns", [])]
        rows = list(getattr(result, "rows", []) or [])
        last_id = None
        if rows and columns and columns[0] == "id":
            last_id = rows[0][0]
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
