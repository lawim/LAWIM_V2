from __future__ import annotations

SIE_TABLE_NAMES: tuple[str, ...] = (
    "source_intelligence_source_contexts",
    "source_intelligence_imports",
)

SQLITE_SIE_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS source_intelligence_source_contexts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL UNIQUE,
    network TEXT NOT NULL DEFAULT '',
    publication_url TEXT NOT NULL DEFAULT '',
    publication_title TEXT NOT NULL DEFAULT '',
    publication_text TEXT NOT NULL DEFAULT '',
    publication_author TEXT NOT NULL DEFAULT '',
    campaign TEXT NOT NULL DEFAULT '',
    city TEXT NOT NULL DEFAULT '',
    district TEXT NOT NULL DEFAULT '',
    property_type TEXT NOT NULL DEFAULT '',
    target_audience TEXT NOT NULL DEFAULT '',
    format TEXT NOT NULL DEFAULT '',
    language TEXT NOT NULL DEFAULT '',
    tags_json TEXT NOT NULL DEFAULT '[]',
    ai_classification TEXT NOT NULL DEFAULT '',
    ai_confidence REAL NOT NULL DEFAULT 0,
    analysis_json TEXT NOT NULL DEFAULT '{}',
    notes TEXT NOT NULL DEFAULT '',
    whatsapp_link TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (source_id) REFERENCES crm_lead_sources(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_source_intelligence_contexts_source ON source_intelligence_source_contexts(source_id, updated_at);
CREATE TABLE IF NOT EXISTS source_intelligence_imports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    import_key TEXT NOT NULL UNIQUE,
    source_id INTEGER NOT NULL,
    source_url TEXT NOT NULL DEFAULT '',
    import_status TEXT NOT NULL DEFAULT 'pending',
    source_channel TEXT NOT NULL DEFAULT '',
    imported_at TEXT NOT NULL,
    analyzed_at TEXT,
    payload_json TEXT NOT NULL DEFAULT '{}',
    result_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (source_id) REFERENCES crm_lead_sources(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_source_intelligence_imports_source ON source_intelligence_imports(source_id, imported_at);
CREATE INDEX IF NOT EXISTS idx_source_intelligence_imports_status ON source_intelligence_imports(import_status, imported_at);
"""

POSTGRESQL_SIE_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS source_intelligence_source_contexts (
        id SERIAL PRIMARY KEY,
        source_id INTEGER NOT NULL UNIQUE REFERENCES crm_lead_sources(id) ON DELETE CASCADE,
        network TEXT NOT NULL DEFAULT '',
        publication_url TEXT NOT NULL DEFAULT '',
        publication_title TEXT NOT NULL DEFAULT '',
        publication_text TEXT NOT NULL DEFAULT '',
        publication_author TEXT NOT NULL DEFAULT '',
        campaign TEXT NOT NULL DEFAULT '',
        city TEXT NOT NULL DEFAULT '',
        district TEXT NOT NULL DEFAULT '',
        property_type TEXT NOT NULL DEFAULT '',
        target_audience TEXT NOT NULL DEFAULT '',
        format TEXT NOT NULL DEFAULT '',
        language TEXT NOT NULL DEFAULT '',
        tags_json TEXT NOT NULL DEFAULT '[]',
        ai_classification TEXT NOT NULL DEFAULT '',
        ai_confidence DOUBLE PRECISION NOT NULL DEFAULT 0,
        analysis_json TEXT NOT NULL DEFAULT '{}',
        notes TEXT NOT NULL DEFAULT '',
        whatsapp_link TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_source_intelligence_contexts_source ON source_intelligence_source_contexts(source_id, updated_at)",
    """
    CREATE TABLE IF NOT EXISTS source_intelligence_imports (
        id SERIAL PRIMARY KEY,
        import_key TEXT NOT NULL UNIQUE,
        source_id INTEGER NOT NULL REFERENCES crm_lead_sources(id) ON DELETE CASCADE,
        source_url TEXT NOT NULL DEFAULT '',
        import_status TEXT NOT NULL DEFAULT 'pending',
        source_channel TEXT NOT NULL DEFAULT '',
        imported_at TEXT NOT NULL,
        analyzed_at TEXT,
        payload_json TEXT NOT NULL DEFAULT '{}',
        result_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_source_intelligence_imports_source ON source_intelligence_imports(source_id, imported_at)",
    "CREATE INDEX IF NOT EXISTS idx_source_intelligence_imports_status ON source_intelligence_imports(import_status, imported_at)",
)
