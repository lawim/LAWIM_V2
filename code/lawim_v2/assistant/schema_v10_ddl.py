"""Schema v10 DDL extensions for AI assistant platform."""

V10_TABLE_NAMES: tuple[str, ...] = (
    "assistant_agents",
    "assistant_prompt_versions",
    "assistant_sessions",
    "assistant_messages",
    "assistant_context_snapshots",
    "assistant_rag_documents",
    "assistant_rag_chunks",
    "assistant_rag_retrievals",
    "assistant_turns",
    "assistant_memory_summaries",
    "assistant_agent_assignments",
)

POSTGRESQL_V10_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS assistant_agents (
        id SERIAL PRIMARY KEY,
        agent_key TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        description TEXT NOT NULL DEFAULT '',
        capabilities_json TEXT NOT NULL DEFAULT '[]',
        prompt_key TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS assistant_prompt_versions (
        id SERIAL PRIMARY KEY,
        prompt_key TEXT NOT NULL,
        version TEXT NOT NULL,
        content TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        UNIQUE (prompt_key, version)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS assistant_sessions (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        session_key TEXT NOT NULL,
        agent_key TEXT NOT NULL DEFAULT 'project_advisor',
        status TEXT NOT NULL DEFAULT 'active',
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (project_id, session_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS assistant_messages (
        id SERIAL PRIMARY KEY,
        session_id INTEGER NOT NULL REFERENCES assistant_sessions(id) ON DELETE CASCADE,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        message_key TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        UNIQUE (session_id, message_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS assistant_context_snapshots (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        session_id INTEGER REFERENCES assistant_sessions(id) ON DELETE SET NULL,
        snapshot_key TEXT NOT NULL,
        context_json TEXT NOT NULL DEFAULT '{}',
        sources_json TEXT NOT NULL DEFAULT '[]',
        created_at TEXT NOT NULL,
        UNIQUE (project_id, snapshot_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS assistant_rag_documents (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        document_key TEXT NOT NULL,
        source_type TEXT NOT NULL,
        title TEXT NOT NULL,
        content_text TEXT NOT NULL,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (project_id, document_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS assistant_rag_chunks (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES assistant_rag_documents(id) ON DELETE CASCADE,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        chunk_key TEXT NOT NULL,
        content TEXT NOT NULL,
        token_estimate INTEGER NOT NULL DEFAULT 0,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        UNIQUE (project_id, chunk_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS assistant_rag_retrievals (
        id SERIAL PRIMARY KEY,
        session_id INTEGER REFERENCES assistant_sessions(id) ON DELETE SET NULL,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        query_text TEXT NOT NULL,
        chunks_json TEXT NOT NULL DEFAULT '[]',
        score INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS assistant_turns (
        id SERIAL PRIMARY KEY,
        session_id INTEGER NOT NULL REFERENCES assistant_sessions(id) ON DELETE CASCADE,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        user_message_id INTEGER REFERENCES assistant_messages(id) ON DELETE SET NULL,
        assistant_message_id INTEGER REFERENCES assistant_messages(id) ON DELETE SET NULL,
        agent_key TEXT NOT NULL,
        mode TEXT NOT NULL DEFAULT 'deterministic',
        provider TEXT NOT NULL DEFAULT 'deterministic',
        fallback_used INTEGER NOT NULL DEFAULT 1,
        routing_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS assistant_memory_summaries (
        id SERIAL PRIMARY KEY,
        session_id INTEGER NOT NULL REFERENCES assistant_sessions(id) ON DELETE CASCADE,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        summary_text TEXT NOT NULL,
        message_count INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS assistant_agent_assignments (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        session_id INTEGER REFERENCES assistant_sessions(id) ON DELETE SET NULL,
        agent_key TEXT NOT NULL,
        assigned_at TEXT NOT NULL,
        UNIQUE (project_id, session_id, agent_key)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_assistant_sessions_project ON assistant_sessions(project_id, user_id, status)",
    "CREATE INDEX IF NOT EXISTS idx_assistant_messages_session ON assistant_messages(session_id, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_assistant_rag_documents_project ON assistant_rag_documents(project_id, source_type)",
    "CREATE INDEX IF NOT EXISTS idx_assistant_rag_chunks_project ON assistant_rag_chunks(project_id, document_id)",
    "CREATE INDEX IF NOT EXISTS idx_assistant_turns_session ON assistant_turns(session_id, created_at)",
)

SQLITE_V10_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS assistant_agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    capabilities_json TEXT NOT NULL DEFAULT '[]',
    prompt_key TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assistant_prompt_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_key TEXT NOT NULL,
    version TEXT NOT NULL,
    content TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    UNIQUE (prompt_key, version)
);

CREATE TABLE IF NOT EXISTS assistant_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    session_key TEXT NOT NULL,
    agent_key TEXT NOT NULL DEFAULT 'project_advisor',
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (project_id, session_key)
);

CREATE TABLE IF NOT EXISTS assistant_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    message_key TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES assistant_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (session_id, message_key)
);

CREATE TABLE IF NOT EXISTS assistant_context_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    session_id INTEGER,
    snapshot_key TEXT NOT NULL,
    context_json TEXT NOT NULL DEFAULT '{}',
    sources_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES assistant_sessions(id) ON DELETE SET NULL,
    UNIQUE (project_id, snapshot_key)
);

CREATE TABLE IF NOT EXISTS assistant_rag_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    document_key TEXT NOT NULL,
    source_type TEXT NOT NULL,
    title TEXT NOT NULL,
    content_text TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, document_key)
);

CREATE TABLE IF NOT EXISTS assistant_rag_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    chunk_key TEXT NOT NULL,
    content TEXT NOT NULL,
    token_estimate INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES assistant_rag_documents(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, chunk_key)
);

CREATE TABLE IF NOT EXISTS assistant_rag_retrievals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    project_id INTEGER NOT NULL,
    query_text TEXT NOT NULL,
    chunks_json TEXT NOT NULL DEFAULT '[]',
    score INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES assistant_sessions(id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS assistant_turns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    user_message_id INTEGER,
    assistant_message_id INTEGER,
    agent_key TEXT NOT NULL,
    mode TEXT NOT NULL DEFAULT 'deterministic',
    provider TEXT NOT NULL DEFAULT 'deterministic',
    fallback_used INTEGER NOT NULL DEFAULT 1,
    routing_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES assistant_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_message_id) REFERENCES assistant_messages(id) ON DELETE SET NULL,
    FOREIGN KEY (assistant_message_id) REFERENCES assistant_messages(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS assistant_memory_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    summary_text TEXT NOT NULL,
    message_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES assistant_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS assistant_agent_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    session_id INTEGER,
    agent_key TEXT NOT NULL,
    assigned_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES assistant_sessions(id) ON DELETE SET NULL,
    UNIQUE (project_id, session_id, agent_key)
);

CREATE INDEX IF NOT EXISTS idx_assistant_sessions_project ON assistant_sessions(project_id, user_id, status);
CREATE INDEX IF NOT EXISTS idx_assistant_messages_session ON assistant_messages(session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_assistant_rag_documents_project ON assistant_rag_documents(project_id, source_type);
CREATE INDEX IF NOT EXISTS idx_assistant_rag_chunks_project ON assistant_rag_chunks(project_id, document_id);
CREATE INDEX IF NOT EXISTS idx_assistant_turns_session ON assistant_turns(session_id, created_at);
"""
