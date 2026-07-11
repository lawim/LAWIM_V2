from __future__ import annotations

from .relation_ddl import RELATION_TABLE_NAMES, POSTGRESQL_RELATION_STATEMENTS, SQLITE_RELATION_TABLES_SCRIPT

BRAIN_TABLE_NAMES: tuple[str, ...] = (
    "brain_intents",
    "brain_memory_items",
    "brain_progression_state",
    "brain_suggestions",
) + RELATION_TABLE_NAMES

POSTGRESQL_BRAIN_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS brain_intents (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        session_id INTEGER REFERENCES assistant_sessions(id) ON DELETE SET NULL,
        source_message_id INTEGER REFERENCES assistant_messages(id) ON DELETE SET NULL,
        intent_type TEXT NOT NULL,
        entities_json TEXT NOT NULL DEFAULT '{}',
        language TEXT NOT NULL DEFAULT 'fr',
        confidence INTEGER NOT NULL DEFAULT 50,
        status TEXT NOT NULL DEFAULT 'hypothesis' CHECK (status IN ('hypothesis', 'confirmed', 'rejected')),
        engine_version TEXT NOT NULL DEFAULT '1.0.0',
        origin TEXT NOT NULL DEFAULT 'conversation',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS brain_memory_items (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        memory_key TEXT NOT NULL,
        kind TEXT NOT NULL CHECK (kind IN ('confirmed_fact', 'preference', 'constraint', 'decision', 'hypothesis', 'temporary')),
        label TEXT NOT NULL,
        value TEXT NOT NULL,
        source_table TEXT,
        source_id INTEGER,
        confidence INTEGER NOT NULL DEFAULT 50,
        status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'pending_confirmation', 'expired', 'superseded')),
        is_global INTEGER NOT NULL DEFAULT 0,
        field_key TEXT,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (project_id, memory_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS brain_progression_state (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        intent_type TEXT NOT NULL,
        current_step INTEGER NOT NULL DEFAULT 0,
        total_steps INTEGER NOT NULL DEFAULT 0,
        asked_questions_json TEXT NOT NULL DEFAULT '[]',
        answers_json TEXT NOT NULL DEFAULT '{}',
        missing_fields_json TEXT NOT NULL DEFAULT '[]',
        next_question TEXT,
        next_question_key TEXT,
        status TEXT NOT NULL DEFAULT 'in_progress' CHECK (status IN ('not_started', 'in_progress', 'complete', 'stuck')),
        schema_version TEXT NOT NULL DEFAULT '1.0.0',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (project_id, intent_type)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS brain_suggestions (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        suggestion_type TEXT NOT NULL,
        content TEXT NOT NULL,
        justification TEXT NOT NULL DEFAULT '',
        priority TEXT NOT NULL DEFAULT 'medium' CHECK (priority IN ('high', 'medium', 'low')),
        status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'accepted', 'rejected', 'ignored', 'deferred')),
        target_action TEXT,
        target_partner TEXT,
        language TEXT NOT NULL DEFAULT 'fr',
        expires_at TEXT,
        accepted_at TEXT,
        rejected_at TEXT,
        created_at TEXT NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_brain_intents_project ON brain_intents(project_id, intent_type, status)",
    "CREATE INDEX IF NOT EXISTS idx_brain_intents_session ON brain_intents(session_id, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_brain_memory_project ON brain_memory_items(project_id, kind, status)",
    "CREATE INDEX IF NOT EXISTS idx_brain_progression_project ON brain_progression_state(project_id, intent_type)",
    "CREATE INDEX IF NOT EXISTS idx_brain_suggestions_project ON brain_suggestions(project_id, status, priority)",
) + POSTGRESQL_RELATION_STATEMENTS

SQLITE_BRAIN_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS brain_intents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    session_id INTEGER,
    source_message_id INTEGER,
    intent_type TEXT NOT NULL,
    entities_json TEXT NOT NULL DEFAULT '{}',
    language TEXT NOT NULL DEFAULT 'fr',
    confidence INTEGER NOT NULL DEFAULT 50,
    status TEXT NOT NULL DEFAULT 'hypothesis' CHECK (status IN ('hypothesis', 'confirmed', 'rejected')),
    engine_version TEXT NOT NULL DEFAULT '1.0.0',
    origin TEXT NOT NULL DEFAULT 'conversation',
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES assistant_sessions(id) ON DELETE SET NULL,
    FOREIGN KEY (source_message_id) REFERENCES assistant_messages(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS brain_memory_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    memory_key TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('confirmed_fact', 'preference', 'constraint', 'decision', 'hypothesis', 'temporary')),
    label TEXT NOT NULL,
    value TEXT NOT NULL,
    source_table TEXT,
    source_id INTEGER,
    confidence INTEGER NOT NULL DEFAULT 50,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'pending_confirmation', 'expired', 'superseded')),
    is_global INTEGER NOT NULL DEFAULT 0,
    field_key TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, memory_key)
);

CREATE TABLE IF NOT EXISTS brain_progression_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    intent_type TEXT NOT NULL,
    current_step INTEGER NOT NULL DEFAULT 0,
    total_steps INTEGER NOT NULL DEFAULT 0,
    asked_questions_json TEXT NOT NULL DEFAULT '[]',
    answers_json TEXT NOT NULL DEFAULT '{}',
    missing_fields_json TEXT NOT NULL DEFAULT '[]',
    next_question TEXT,
    next_question_key TEXT,
    status TEXT NOT NULL DEFAULT 'in_progress' CHECK (status IN ('not_started', 'in_progress', 'complete', 'stuck')),
    schema_version TEXT NOT NULL DEFAULT '1.0.0',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, intent_type)
);

CREATE TABLE IF NOT EXISTS brain_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    suggestion_type TEXT NOT NULL,
    content TEXT NOT NULL,
    justification TEXT NOT NULL DEFAULT '',
    priority TEXT NOT NULL DEFAULT 'medium' CHECK (priority IN ('high', 'medium', 'low')),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'accepted', 'rejected', 'ignored', 'deferred')),
    target_action TEXT,
    target_partner TEXT,
    language TEXT NOT NULL DEFAULT 'fr',
    expires_at TEXT,
    accepted_at TEXT,
    rejected_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_brain_intents_project ON brain_intents(project_id, intent_type, status);
CREATE INDEX IF NOT EXISTS idx_brain_intents_session ON brain_intents(session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_brain_memory_project ON brain_memory_items(project_id, kind, status);
CREATE INDEX IF NOT EXISTS idx_brain_progression_project ON brain_progression_state(project_id, intent_type);
CREATE INDEX IF NOT EXISTS idx_brain_suggestions_project ON brain_suggestions(project_id, status, priority);
""" + SQLITE_RELATION_TABLES_SCRIPT
