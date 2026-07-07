"""Unified DDL for SQLite and PostgreSQL runtimes (persistence manifest v7)."""

from __future__ import annotations

import hashlib
import re

from .persistence import APPLICATION_SCHEMA_VERSION
from .intelligent.schema_v7_ddl import POSTGRESQL_V7_STATEMENTS, SQLITE_V7_TABLES_SCRIPT
from .ecosystem.schema_v8_ddl import POSTGRESQL_V8_STATEMENTS, SQLITE_V8_TABLES_SCRIPT
from .cognition.schema_v9_ddl import POSTGRESQL_V9_STATEMENTS, SQLITE_V9_TABLES_SCRIPT
from .assistant.schema_v10_ddl import POSTGRESQL_V10_STATEMENTS, SQLITE_V10_TABLES_SCRIPT
from .knowledge_platform.schema_v11_ddl import POSTGRESQL_V11_STATEMENTS, SQLITE_V11_TABLES_SCRIPT
from .workflow_automation.schema_v12_ddl import POSTGRESQL_V12_STATEMENTS, SQLITE_V12_TABLES_SCRIPT
from .real_estate_intelligence.schema_v13_ddl import POSTGRESQL_V13_STATEMENTS, SQLITE_V13_TABLES_SCRIPT
from .crm.schema_v14_ddl import POSTGRESQL_V14_STATEMENTS, SQLITE_V14_TABLES_SCRIPT
from .marketplace.schema_v15_ddl import POSTGRESQL_V15_STATEMENTS, SQLITE_V15_TABLES_SCRIPT
from .security.schema_v16_ddl import POSTGRESQL_V16_STATEMENTS, SQLITE_V16_TABLES_SCRIPT
from .communication.schema_v17_ddl import POSTGRESQL_V17_STATEMENTS, SQLITE_V17_TABLES_SCRIPT
from .analytics.schema_v18_ddl import POSTGRESQL_V18_STATEMENTS, SQLITE_V18_TABLES_SCRIPT
from .source_intelligence.schema_ddl import POSTGRESQL_SIE_STATEMENTS, SQLITE_SIE_TABLES_SCRIPT
from .program_m_support import build_postgresql_statements, build_sqlite_tables_script
from .user_roles import USER_ROLE_VALUES

USER_ROLE_VALUES_SQL = ", ".join(f"'{role}'" for role in USER_ROLE_VALUES)

POSTGRESQL_INIT_STATEMENTS: tuple[str, ...] = (
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
        role TEXT NOT NULL CHECK (role IN (__USER_ROLE_VALUES__)),
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
        provider_name TEXT NOT NULL DEFAULT 'local',
        provider_media_id TEXT,
        provider_public_id TEXT,
        provider_resource_type TEXT DEFAULT 'image',
        provider_storage_key TEXT,
        provider_object_id TEXT,
        mime_type TEXT,
        size_bytes INTEGER,
        thumbnail_url TEXT,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        position INTEGER NOT NULL DEFAULT 0,
        lifecycle_state TEXT NOT NULL DEFAULT 'active',
        backup_state TEXT NOT NULL DEFAULT 'available',
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
        organization_id INTEGER REFERENCES organizations(id),
        subject TEXT NOT NULL,
        status TEXT NOT NULL,
        negotiation_stage TEXT NOT NULL DEFAULT 'inquiry',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
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
    CREATE TABLE IF NOT EXISTS notifications (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        kind TEXT NOT NULL,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        payload_json TEXT NOT NULL DEFAULT '{}',
        read_at TEXT,
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
    "CREATE INDEX IF NOT EXISTS idx_properties_created_at ON properties(created_at, id)",
    "CREATE INDEX IF NOT EXISTS idx_media_property_position ON media(property_id, position)",
    "CREATE INDEX IF NOT EXISTS idx_media_created_at ON media(created_at, id)",
    "CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_conversations_user_updated ON conversations(user_id, updated_at)",
    "CREATE INDEX IF NOT EXISTS idx_conversations_updated_at ON conversations(updated_at, id)",
    "CREATE INDEX IF NOT EXISTS idx_conversations_organization_updated ON conversations(organization_id, updated_at, id)",
    "CREATE INDEX IF NOT EXISTS idx_conversations_property_updated ON conversations(property_id, updated_at, id)",
    "CREATE INDEX IF NOT EXISTS idx_notifications_user_read ON notifications(user_id, read_at, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_organizations_created_at ON organizations(created_at, id)",
    "CREATE INDEX IF NOT EXISTS idx_users_organization ON users(organization_id, id)",
    "CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at, id)",
    "CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at, id)",
    "CREATE INDEX IF NOT EXISTS idx_events_kind_created ON events(kind, created_at, id)",
    "CREATE INDEX IF NOT EXISTS idx_sessions_user_expires ON sessions(user_id, expires_at)",
    "CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at)",
    "CREATE INDEX IF NOT EXISTS idx_properties_owner_status ON properties(owner_organization_id, status, deleted_at)",
    """
    CREATE TABLE IF NOT EXISTS projects (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        organization_id INTEGER REFERENCES organizations(id),
        title TEXT NOT NULL,
        project_type TEXT NOT NULL,
        objective TEXT NOT NULL,
        budget_min INTEGER,
        budget_max INTEGER,
        currency TEXT NOT NULL DEFAULT 'XAF',
        location_city TEXT,
        location_region TEXT,
        location_country TEXT DEFAULT 'Cameroon',
        location_latitude DOUBLE PRECISION,
        location_longitude DOUBLE PRECISION,
        timeline_horizon TEXT,
        status TEXT NOT NULL DEFAULT 'draft',
        priority TEXT NOT NULL DEFAULT 'normal',
        progress_percent INTEGER NOT NULL DEFAULT 0,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        primary_goal_key TEXT,
        intelligence_json TEXT NOT NULL DEFAULT '{}',
        archived_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS project_steps (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
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
        UNIQUE (project_id, step_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS project_checklist_items (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        step_id INTEGER REFERENCES project_steps(id) ON DELETE CASCADE,
        label TEXT NOT NULL,
        checked INTEGER NOT NULL DEFAULT 0,
        position INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS project_step_history (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        step_id INTEGER NOT NULL REFERENCES project_steps(id) ON DELETE CASCADE,
        from_status TEXT,
        to_status TEXT NOT NULL,
        note TEXT,
        created_at TEXT NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_projects_user_status ON projects(user_id, status, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_projects_organization_status ON projects(organization_id, status, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_projects_created_at ON projects(created_at, id)",
    "CREATE INDEX IF NOT EXISTS idx_project_steps_project_position ON project_steps(project_id, position)",
    "CREATE INDEX IF NOT EXISTS idx_project_checklist_project ON project_checklist_items(project_id, step_id, position)",
    "CREATE INDEX IF NOT EXISTS idx_project_step_history_project ON project_step_history(project_id, created_at, id)",
)

SQLITE_INIT_SCRIPT = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    kind TEXT NOT NULL DEFAULT 'agency' CHECK (kind IN ('agency', 'partner', 'owner')),
    city TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN (__USER_ROLE_VALUES__)),
    organization_id INTEGER,
    password_salt TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_code TEXT UNIQUE,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    address_line TEXT,
    city TEXT NOT NULL,
    region TEXT,
    postal_code TEXT,
    country TEXT NOT NULL,
    search_key TEXT,
    latitude REAL,
    longitude REAL,
    price_min INTEGER CHECK (price_min IS NULL OR price_min >= 0),
    price_max INTEGER CHECK (price_max IS NULL OR price_max >= 0),
    currency TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('draft', 'open', 'closed', 'published', 'archived')),
    availability TEXT NOT NULL DEFAULT 'available' CHECK (availability IN ('available', 'reserved', 'sold', 'rented', 'unavailable')),
    property_type TEXT NOT NULL,
    owner_organization_id INTEGER,
    bedrooms INTEGER NOT NULL DEFAULT 0 CHECK (bedrooms >= 0),
    bathrooms INTEGER NOT NULL DEFAULT 0 CHECK (bathrooms >= 0),
    area_sqm REAL NOT NULL DEFAULT 0 CHECK (area_sqm >= 0),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    version INTEGER NOT NULL DEFAULT 1 CHECK (version >= 1),
    published_at TEXT,
    deleted_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (owner_organization_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    kind TEXT NOT NULL CHECK (kind <> ''),
    url TEXT NOT NULL CHECK (url <> ''),
    caption TEXT NOT NULL CHECK (caption <> ''),
    storage_path TEXT,
    provider_name TEXT NOT NULL DEFAULT 'local' CHECK (provider_name <> ''),
    provider_media_id TEXT,
    provider_public_id TEXT,
    provider_resource_type TEXT DEFAULT 'image',
    provider_storage_key TEXT,
    provider_object_id TEXT,
    mime_type TEXT,
    size_bytes INTEGER CHECK (size_bytes IS NULL OR size_bytes >= 0),
    thumbnail_url TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    position INTEGER NOT NULL DEFAULT 0 CHECK (position >= 0),
    lifecycle_state TEXT NOT NULL DEFAULT 'active' CHECK (lifecycle_state IN ('active', 'deleted', 'archived', 'pending')),
    backup_state TEXT NOT NULL DEFAULT 'available' CHECK (backup_state IN ('available', 'archived', 'restored', 'missing')),
    version INTEGER NOT NULL DEFAULT 1 CHECK (version >= 1),
    deleted_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER,
    user_id INTEGER NOT NULL,
    organization_id INTEGER,
    subject TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('open', 'closed', 'archived')),
    negotiation_stage TEXT NOT NULL DEFAULT 'inquiry' CHECK (negotiation_stage IN ('inquiry', 'offer', 'counter', 'accepted', 'declined', 'closed')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    sender_user_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);

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

CREATE TABLE IF NOT EXISTS schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_properties_status_city ON properties(status, city);
CREATE INDEX IF NOT EXISTS idx_properties_search_key ON properties(search_key);
CREATE INDEX IF NOT EXISTS idx_properties_deleted_at ON properties(deleted_at);
CREATE INDEX IF NOT EXISTS idx_properties_created_at ON properties(created_at, id);
CREATE INDEX IF NOT EXISTS idx_media_property_position ON media(property_id, position);
CREATE INDEX IF NOT EXISTS idx_media_created_at ON media(created_at, id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id, created_at);
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

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    organization_id INTEGER,
    title TEXT NOT NULL,
    project_type TEXT NOT NULL CHECK (project_type IN ('buy', 'rent', 'sell', 'invest', 'build', 'other')),
    objective TEXT NOT NULL,
    budget_min INTEGER CHECK (budget_min IS NULL OR budget_min >= 0),
    budget_max INTEGER CHECK (budget_max IS NULL OR budget_max >= 0),
    currency TEXT NOT NULL DEFAULT 'XAF',
    location_city TEXT,
    location_region TEXT,
    location_country TEXT DEFAULT 'Cameroon',
    location_latitude REAL,
    location_longitude REAL,
    timeline_horizon TEXT,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'paused', 'completed', 'archived')),
    priority TEXT NOT NULL DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high')),
    progress_percent INTEGER NOT NULL DEFAULT 0 CHECK (progress_percent >= 0 AND progress_percent <= 100),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    primary_goal_key TEXT,
    intelligence_json TEXT NOT NULL DEFAULT '{}',
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
    position INTEGER NOT NULL DEFAULT 0 CHECK (position >= 0),
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'skipped', 'blocked')),
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
    checked INTEGER NOT NULL DEFAULT 0 CHECK (checked IN (0, 1)),
    position INTEGER NOT NULL DEFAULT 0 CHECK (position >= 0),
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
""" + SQLITE_V7_TABLES_SCRIPT + SQLITE_V8_TABLES_SCRIPT + SQLITE_V9_TABLES_SCRIPT + SQLITE_V10_TABLES_SCRIPT + SQLITE_V11_TABLES_SCRIPT + SQLITE_V12_TABLES_SCRIPT + SQLITE_V13_TABLES_SCRIPT + SQLITE_V14_TABLES_SCRIPT + SQLITE_V15_TABLES_SCRIPT + SQLITE_V16_TABLES_SCRIPT + SQLITE_V17_TABLES_SCRIPT + SQLITE_V18_TABLES_SCRIPT + SQLITE_SIE_TABLES_SCRIPT + build_sqlite_tables_script(("operations", "deployment", "backup", "installer", "releases"))

SQLITE_INIT_SCRIPT = SQLITE_INIT_SCRIPT.replace("__USER_ROLE_VALUES__", USER_ROLE_VALUES_SQL)

POSTGRESQL_INIT_STATEMENTS = POSTGRESQL_INIT_STATEMENTS + tuple(
    statement for statement in POSTGRESQL_V7_STATEMENTS if "ALTER TABLE" not in statement
) + POSTGRESQL_V8_STATEMENTS + POSTGRESQL_V9_STATEMENTS + POSTGRESQL_V10_STATEMENTS + POSTGRESQL_V11_STATEMENTS + POSTGRESQL_V12_STATEMENTS + POSTGRESQL_V13_STATEMENTS + POSTGRESQL_V14_STATEMENTS + POSTGRESQL_V15_STATEMENTS + POSTGRESQL_V16_STATEMENTS + POSTGRESQL_V17_STATEMENTS + POSTGRESQL_V18_STATEMENTS + POSTGRESQL_SIE_STATEMENTS + build_postgresql_statements(("operations", "deployment", "backup", "installer", "releases"))

POSTGRESQL_INIT_STATEMENTS = tuple(statement.replace("__USER_ROLE_VALUES__", USER_ROLE_VALUES_SQL) for statement in POSTGRESQL_INIT_STATEMENTS)


def manifest_table_names() -> tuple[str, ...]:
    from .persistence import APPLICATION_SCHEMA

    return tuple(table.name for table in APPLICATION_SCHEMA.tables)


def ddl_table_names(script: str) -> set[str]:
    return set(re.findall(r"CREATE TABLE IF NOT EXISTS (\w+)", script, flags=re.IGNORECASE))


def sqlite_table_names() -> set[str]:
    return ddl_table_names(SQLITE_INIT_SCRIPT)


def postgresql_table_names() -> set[str]:
    names: set[str] = set()
    for statement in POSTGRESQL_INIT_STATEMENTS:
        names.update(ddl_table_names(statement))
    return names


def validate_manifest_table_alignment() -> list[str]:
    expected = set(manifest_table_names())
    errors: list[str] = []
    for engine, names in (("sqlite", sqlite_table_names()), ("postgresql", postgresql_table_names())):
        missing = expected - names
        extra = names - expected
        if missing:
            errors.append(f"{engine} DDL missing tables: {sorted(missing)}")
        if extra:
            errors.append(f"{engine} DDL has unexpected tables: {sorted(extra)}")
    return errors


def normalize_sql_statement(statement: str) -> str:
    return " ".join(statement.strip().rstrip(";").split())


def normalized_ddl_fingerprint(statements: tuple[str, ...] | None = None) -> str:
    payload = statements if statements is not None else POSTGRESQL_INIT_STATEMENTS
    canonical = "|".join(normalize_sql_statement(stmt) for stmt in payload)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def extract_sql_statements(text: str) -> tuple[str, ...]:
    without_comments = re.sub(r"--[^\n]*", "", text)
    parts = [part.strip() for part in without_comments.split(";") if part.strip()]
    return tuple(parts)


def postgresql_migration_sql(*, header: str | None = None) -> str:
    lines: list[str] = []
    if header is not None:
        lines.append(header.rstrip())
        lines.append("")
    for statement in POSTGRESQL_INIT_STATEMENTS:
        normalized = statement.strip()
        if not normalized.endswith(";"):
            normalized = f"{normalized};"
        lines.append(normalized)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def migration_header() -> str:
    return (
        f"-- LAWIM_V2 schema v{APPLICATION_SCHEMA_VERSION} initial migration "
        f"(generated from code/lawim_v2/schema_ddl.py; aligned with persistence manifest)"
    )
