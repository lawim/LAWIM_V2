"""Incremental SQLite migrations and production migration strategy metadata."""

from __future__ import annotations

import sqlite3
from typing import Protocol

from .persistence import APPLICATION_SCHEMA_VERSION

# Production PostgreSQL: apply prisma/migrations via `prisma migrate deploy`.
# Development SQLite: runtime init (schema_ddl.SQLITE_INIT_SCRIPT) + legacy steps below.
PRODUCTION_MIGRATION_TOOL = "prisma"
SQLITE_RUNTIME_INIT = "schema_ddl.SQLITE_INIT_SCRIPT"
MIGRATION_STRATEGY_NOTES = (
    "Fresh installs use schema_ddl init scripts aligned with persistence manifest v15.",
    "SQLite legacy databases receive idempotent ALTER/backfill steps in apply_sqlite_legacy_migrations().",
    "PostgreSQL production deployments should prefer prisma migrate deploy over runtime DDL init.",
    "Future schema versions must add a Prisma migration and optional SQLite legacy steps.",
)


class _ColumnMigrationConnection(Protocol):
    def execute(self, sql: str, params: tuple[object, ...] = ()) -> object: ...
    def executescript(self, sql: str) -> object: ...


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {str(row[1]) for row in rows}


def _ensure_column(conn: sqlite3.Connection, table: str, column: str, definition: str) -> None:
    if column not in _table_columns(conn, table):
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def apply_sqlite_legacy_migrations(conn: sqlite3.Connection) -> None:
    """Idempotent upgrades for databases created before schema v5."""
    property_columns = {
        "listing_code": "TEXT",
        "address_line": "TEXT",
        "region": "TEXT",
        "postal_code": "TEXT",
        "search_key": "TEXT",
        "availability": "TEXT NOT NULL DEFAULT 'available'",
        "metadata_json": "TEXT NOT NULL DEFAULT '{}'",
        "version": "INTEGER NOT NULL DEFAULT 1",
        "published_at": "TEXT",
        "deleted_at": "TEXT",
    }
    for column, definition in property_columns.items():
        _ensure_column(conn, "properties", column, definition)

    media_columns = {
        "storage_path": "TEXT",
        "mime_type": "TEXT",
        "size_bytes": "INTEGER",
        "thumbnail_url": "TEXT",
        "metadata_json": "TEXT NOT NULL DEFAULT '{}'",
        "position": "INTEGER NOT NULL DEFAULT 0",
        "version": "INTEGER NOT NULL DEFAULT 1",
        "deleted_at": "TEXT",
    }
    for column, definition in media_columns.items():
        _ensure_column(conn, "media", column, definition)

    conn.execute(
        """
        UPDATE properties
        SET availability = 'available'
        WHERE availability IS NULL OR TRIM(availability) = ''
        """
    )
    conn.execute(
        """
        UPDATE properties
        SET metadata_json = '{}'
        WHERE metadata_json IS NULL OR TRIM(metadata_json) = ''
        """
    )
    conn.execute(
        """
        UPDATE properties
        SET version = 1
        WHERE version IS NULL OR version < 1
        """
    )
    conn.execute(
        """
        UPDATE media
        SET metadata_json = '{}'
        WHERE metadata_json IS NULL OR TRIM(metadata_json) = ''
        """
    )
    conn.execute(
        """
        UPDATE media
        SET version = 1
        WHERE version IS NULL OR version < 1
        """
    )
    conn.execute(
        """
        UPDATE media
        SET position = 0
        WHERE position IS NULL OR position < 0
        """
    )
    conn.execute(
        """
        UPDATE properties
        SET search_key = LOWER(city || '|' || COALESCE(region, '') || '|' || country)
        WHERE search_key IS NULL OR TRIM(search_key) = ''
        """
    )
    conn.execute(
        """
        UPDATE properties
        SET published_at = created_at
        WHERE status = 'published' AND (published_at IS NULL OR TRIM(published_at) = '')
        """
    )
    conn.execute(
        """
        UPDATE properties
        SET listing_code = 'lawim-' || id
        WHERE listing_code IS NULL OR TRIM(listing_code) = ''
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_properties_search_key ON properties(search_key)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_properties_deleted_at ON properties(deleted_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_properties_created_at ON properties(created_at, id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_media_property_position ON media(property_id, position)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_media_created_at ON media(created_at, id)")

    conversation_columns = {
        "organization_id": "INTEGER",
        "negotiation_stage": "TEXT NOT NULL DEFAULT 'inquiry'",
        "updated_at": "TEXT",
    }
    for column, definition in conversation_columns.items():
        _ensure_column(conn, "conversations", column, definition)
    conn.execute(
        """
        UPDATE conversations
        SET negotiation_stage = 'inquiry'
        WHERE negotiation_stage IS NULL OR TRIM(negotiation_stage) = ''
        """
    )
    conn.execute(
        """
        UPDATE conversations
        SET updated_at = created_at
        WHERE updated_at IS NULL OR TRIM(updated_at) = ''
        """
    )
    conn.execute(
        """
        UPDATE conversations
        SET organization_id = (
            SELECT owner_organization_id FROM properties WHERE properties.id = conversations.property_id
        )
        WHERE organization_id IS NULL AND property_id IS NOT NULL
        """
    )
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            kind TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            payload_json TEXT NOT NULL DEFAULT '{}',
            read_at TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_conversations_user_updated ON conversations(user_id, updated_at);
        CREATE INDEX IF NOT EXISTS idx_conversations_updated_at ON conversations(updated_at, id);
        CREATE INDEX IF NOT EXISTS idx_conversations_organization_updated ON conversations(organization_id, updated_at, id);
        CREATE INDEX IF NOT EXISTS idx_conversations_property_updated ON conversations(property_id, updated_at, id);
        CREATE INDEX IF NOT EXISTS idx_notifications_user_read ON notifications(user_id, read_at, created_at);
        CREATE INDEX IF NOT EXISTS idx_organizations_created_at ON organizations(created_at, id);
        CREATE INDEX IF NOT EXISTS idx_users_organization ON users(organization_id, id);
        CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at, id);
        CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at, id);
        CREATE INDEX IF NOT EXISTS idx_events_kind_created ON events(kind, created_at, id);
        CREATE INDEX IF NOT EXISTS idx_sessions_user_expires ON sessions(user_id, expires_at);
        CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);
        CREATE INDEX IF NOT EXISTS idx_properties_owner_status ON properties(owner_organization_id, status, deleted_at);
        """
    )
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            organization_id INTEGER,
            title TEXT NOT NULL,
            project_type TEXT NOT NULL,
            objective TEXT NOT NULL,
            budget_min INTEGER,
            budget_max INTEGER,
            currency TEXT NOT NULL DEFAULT 'XAF',
            location_city TEXT,
            location_region TEXT,
            location_country TEXT DEFAULT 'Cameroon',
            location_latitude REAL,
            location_longitude REAL,
            timeline_horizon TEXT,
            status TEXT NOT NULL DEFAULT 'draft',
            priority TEXT NOT NULL DEFAULT 'normal',
            progress_percent INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            archived_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (organization_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS project_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            step_key TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            position INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'pending',
            milestone TEXT,
            next_action TEXT,
            completed_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
            UNIQUE (project_id, step_key)
        );
        CREATE TABLE IF NOT EXISTS project_checklist_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            step_id INTEGER,
            label TEXT NOT NULL,
            checked INTEGER NOT NULL DEFAULT 0,
            position INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
            FOREIGN KEY (step_id) REFERENCES project_steps(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS project_step_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            step_id INTEGER NOT NULL,
            from_status TEXT,
            to_status TEXT NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
            FOREIGN KEY (step_id) REFERENCES project_steps(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_projects_user_status ON projects(user_id, status, created_at);
        CREATE INDEX IF NOT EXISTS idx_projects_organization_status ON projects(organization_id, status, created_at);
        CREATE INDEX IF NOT EXISTS idx_projects_created_at ON projects(created_at, id);
        CREATE INDEX IF NOT EXISTS idx_project_steps_project_position ON project_steps(project_id, position);
        CREATE INDEX IF NOT EXISTS idx_project_checklist_project ON project_checklist_items(project_id, step_id, position);
        CREATE INDEX IF NOT EXISTS idx_project_step_history_project ON project_step_history(project_id, created_at, id);
        """
    )
    _ensure_column(conn, "projects", "primary_goal_key", "TEXT")
    _ensure_column(conn, "projects", "intelligence_json", "TEXT NOT NULL DEFAULT '{}'")
    from .intelligent.schema_v7_ddl import SQLITE_V7_TABLES_SCRIPT

    conn.executescript(SQLITE_V7_TABLES_SCRIPT)
    from .ecosystem.schema_v8_ddl import SQLITE_V8_TABLES_SCRIPT

    conn.executescript(SQLITE_V8_TABLES_SCRIPT)
    from .cognition.schema_v9_ddl import SQLITE_V9_TABLES_SCRIPT

    conn.executescript(SQLITE_V9_TABLES_SCRIPT)
    from .assistant.schema_v10_ddl import SQLITE_V10_TABLES_SCRIPT

    conn.executescript(SQLITE_V10_TABLES_SCRIPT)
    from .knowledge_platform.schema_v11_ddl import SQLITE_V11_TABLES_SCRIPT

    conn.executescript(SQLITE_V11_TABLES_SCRIPT)
    from .workflow_automation.schema_v12_ddl import SQLITE_V12_TABLES_SCRIPT

    conn.executescript(SQLITE_V12_TABLES_SCRIPT)
    from .real_estate_intelligence.schema_v13_ddl import SQLITE_V13_TABLES_SCRIPT

    conn.executescript(SQLITE_V13_TABLES_SCRIPT)
    from .crm.schema_v14_ddl import SQLITE_V14_TABLES_SCRIPT

    conn.executescript(SQLITE_V14_TABLES_SCRIPT)
    from .marketplace.schema_v15_ddl import SQLITE_V15_TABLES_SCRIPT

    conn.executescript(SQLITE_V15_TABLES_SCRIPT)


def migration_strategy_profile() -> dict[str, object]:
    return {
        "schema_version": APPLICATION_SCHEMA_VERSION,
        "production_tool": PRODUCTION_MIGRATION_TOOL,
        "sqlite_runtime_init": SQLITE_RUNTIME_INIT,
        "notes": list(MIGRATION_STRATEGY_NOTES),
    }
