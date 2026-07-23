from __future__ import annotations

import argparse
import logging
import os
import sqlite3
import sys

logger = logging.getLogger(__name__)

MIGRATIONS: list[tuple[str, str]] = [
    ("001_initial_sessions", """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            channel TEXT NOT NULL DEFAULT '',
            conversation_id TEXT DEFAULT '',
            active_project_id TEXT DEFAULT '',
            started_at TEXT NOT NULL,
            last_activity_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'ACTIVE',
            locale TEXT DEFAULT 'fr',
            metadata TEXT DEFAULT '{}'
        );
        CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
    """),
    ("002_initial_profiles", """
        CREATE TABLE IF NOT EXISTS profiles (
            profile_id TEXT PRIMARY KEY,
            project_id TEXT NOT NULL,
            profile_type TEXT NOT NULL DEFAULT '',
            fields_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            version INTEGER DEFAULT 1
        );
        CREATE INDEX IF NOT EXISTS idx_profiles_project ON profiles(project_id);
    """),
    ("003_initial_deliveries", """
        CREATE TABLE IF NOT EXISTS deliveries (
            delivery_id TEXT PRIMARY KEY,
            channel TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'CREATED',
            provider_message_id TEXT DEFAULT '',
            correlation_id TEXT DEFAULT '',
            error TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_deliveries_correlation ON deliveries(correlation_id);
    """),
    ("004_initial_events", """
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            event_type TEXT NOT NULL,
            project_id TEXT DEFAULT '',
            correlation_id TEXT DEFAULT '',
            actor TEXT DEFAULT '',
            source TEXT DEFAULT '',
            payload TEXT DEFAULT '{}',
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_events_correlation ON events(correlation_id);
        CREATE INDEX IF NOT EXISTS idx_events_project ON events(project_id);
    """),
]


ROLLBACK_MIGRATIONS: list[tuple[str, str]] = [
    ("004_initial_events", "DROP TABLE IF EXISTS events;"),
    ("003_initial_deliveries", "DROP TABLE IF EXISTS deliveries;"),
    ("002_initial_profiles", "DROP TABLE IF EXISTS profiles;"),
    ("001_initial_sessions", "DROP TABLE IF EXISTS sessions;"),
]


def get_db_path() -> str:
    return os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")


def run_migrations(db_path: str | None = None, rollback: bool = False) -> None:
    path = db_path or get_db_path()
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            name TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    applied = set(row[0] for row in conn.execute("SELECT name FROM _migrations").fetchall())

    if rollback:
        migrations_to_run = [(n, sql) for n, sql in ROLLBACK_MIGRATIONS if n in applied]
        for name, sql in migrations_to_run:
            logger.info("rollback migration: %s", name)
            conn.executescript(sql)
            conn.execute("DELETE FROM _migrations WHERE name = ?", (name,))
            conn.commit()
        logger.info("rollback complete: %d migrations reverted", len(migrations_to_run))
    else:
        migrations_to_run = [(n, sql) for n, sql in MIGRATIONS if n not in applied]
        for name, sql in migrations_to_run:
            logger.info("applying migration: %s", name)
            conn.executescript(sql)
            conn.execute("INSERT OR IGNORE INTO _migrations (name) VALUES (?)", (name,))
            conn.commit()
        logger.info("migrations complete: %d applied, %d already applied", len(migrations_to_run), len(applied))

    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="LAWIM database migrations")
    parser.add_argument("--rollback", action="store_true", help="Rollback migrations")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    run_migrations(rollback=args.rollback)


if __name__ == "__main__":
    main()
