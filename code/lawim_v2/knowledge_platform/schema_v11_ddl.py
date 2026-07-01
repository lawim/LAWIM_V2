"""Schema v11 DDL — expert knowledge platform (RELEASE PROGRAM E)."""

V11_TABLE_NAMES: tuple[str, ...] = (
    "expert_knowledge_collections",
    "expert_knowledge_sources",
    "expert_knowledge_categories",
    "expert_knowledge_tags",
    "expert_knowledge_documents",
    "expert_knowledge_versions",
    "expert_knowledge_articles",
    "expert_knowledge_sections",
    "expert_knowledge_paragraphs",
    "expert_knowledge_chunks",
    "expert_knowledge_citations",
    "expert_knowledge_attachments",
    "expert_knowledge_references",
    "expert_knowledge_embeddings",
    "expert_knowledge_indexes",
    "expert_knowledge_relationships",
    "expert_knowledge_feedback",
    "expert_knowledge_reviews",
    "expert_knowledge_approvals",
    "expert_knowledge_publications",
    "expert_knowledge_imports",
    "expert_knowledge_exports",
    "expert_knowledge_snapshots",
)

# Shared column blocks abbreviated — PostgreSQL first, then SQLite script.

POSTGRESQL_V11_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_collections (
        id SERIAL PRIMARY KEY,
        collection_key TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        domain TEXT NOT NULL,
        description TEXT NOT NULL DEFAULT '',
        status TEXT NOT NULL DEFAULT 'active',
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_sources (
        id SERIAL PRIMARY KEY,
        source_key TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        source_type TEXT NOT NULL,
        url TEXT,
        publisher TEXT,
        trust_score INTEGER NOT NULL DEFAULT 70,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_categories (
        id SERIAL PRIMARY KEY,
        category_key TEXT NOT NULL UNIQUE,
        domain TEXT NOT NULL,
        title TEXT NOT NULL,
        parent_key TEXT,
        description TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_tags (
        id SERIAL PRIMARY KEY,
        tag_key TEXT NOT NULL UNIQUE,
        label TEXT NOT NULL,
        domain TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_documents (
        id SERIAL PRIMARY KEY,
        collection_id INTEGER NOT NULL REFERENCES expert_knowledge_collections(id) ON DELETE CASCADE,
        source_id INTEGER REFERENCES expert_knowledge_sources(id) ON DELETE SET NULL,
        document_key TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        format TEXT NOT NULL DEFAULT 'markdown',
        status TEXT NOT NULL DEFAULT 'draft',
        author TEXT,
        current_version_id INTEGER,
        category_key TEXT,
        tags_json TEXT NOT NULL DEFAULT '[]',
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_versions (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        version_key TEXT NOT NULL,
        version_number INTEGER NOT NULL DEFAULT 1,
        content_hash TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'draft',
        change_note TEXT,
        content_text TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE (document_id, version_number)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_articles (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        article_key TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        slug TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'draft',
        summary TEXT NOT NULL DEFAULT '',
        body_format TEXT NOT NULL DEFAULT 'markdown',
        published_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_sections (
        id SERIAL PRIMARY KEY,
        article_id INTEGER NOT NULL REFERENCES expert_knowledge_articles(id) ON DELETE CASCADE,
        section_key TEXT NOT NULL,
        title TEXT NOT NULL,
        position INTEGER NOT NULL DEFAULT 0,
        content TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL,
        UNIQUE (article_id, section_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_paragraphs (
        id SERIAL PRIMARY KEY,
        section_id INTEGER NOT NULL REFERENCES expert_knowledge_sections(id) ON DELETE CASCADE,
        paragraph_key TEXT NOT NULL,
        position INTEGER NOT NULL DEFAULT 0,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE (section_id, paragraph_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_chunks (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        article_id INTEGER REFERENCES expert_knowledge_articles(id) ON DELETE SET NULL,
        chunk_key TEXT NOT NULL UNIQUE,
        content TEXT NOT NULL,
        token_estimate INTEGER NOT NULL DEFAULT 0,
        index_lexical TEXT NOT NULL DEFAULT '',
        metadata_json TEXT NOT NULL DEFAULT '{}',
        freshness_score INTEGER NOT NULL DEFAULT 80,
        confidence_score INTEGER NOT NULL DEFAULT 75,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_citations (
        id SERIAL PRIMARY KEY,
        chunk_id INTEGER NOT NULL REFERENCES expert_knowledge_chunks(id) ON DELETE CASCADE,
        citation_key TEXT NOT NULL,
        label TEXT NOT NULL,
        source_ref TEXT,
        page TEXT,
        quote TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL,
        UNIQUE (chunk_id, citation_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_attachments (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        attachment_key TEXT NOT NULL,
        filename TEXT NOT NULL,
        mime_type TEXT NOT NULL,
        size_bytes INTEGER NOT NULL DEFAULT 0,
        storage_path TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL,
        UNIQUE (document_id, attachment_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_references (
        id SERIAL PRIMARY KEY,
        from_document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        to_document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        reference_type TEXT NOT NULL DEFAULT 'references',
        label TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_embeddings (
        id SERIAL PRIMARY KEY,
        chunk_id INTEGER NOT NULL REFERENCES expert_knowledge_chunks(id) ON DELETE CASCADE,
        model_key TEXT NOT NULL DEFAULT 'lawim-deterministic-v1',
        vector_json TEXT NOT NULL DEFAULT '[]',
        dimensions INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        UNIQUE (chunk_id, model_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_indexes (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        index_key TEXT NOT NULL,
        index_type TEXT NOT NULL DEFAULT 'lexical',
        status TEXT NOT NULL DEFAULT 'active',
        token_count INTEGER NOT NULL DEFAULT 0,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (document_id, index_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_relationships (
        id SERIAL PRIMARY KEY,
        subject_type TEXT NOT NULL,
        subject_id INTEGER NOT NULL,
        object_type TEXT NOT NULL,
        object_id INTEGER NOT NULL,
        relation_type TEXT NOT NULL,
        confidence INTEGER NOT NULL DEFAULT 50,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_feedback (
        id SERIAL PRIMARY KEY,
        article_id INTEGER NOT NULL REFERENCES expert_knowledge_articles(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        rating INTEGER NOT NULL DEFAULT 3,
        comment TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_reviews (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        reviewer_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        note TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_approvals (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        approver_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        note TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_publications (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        publication_key TEXT NOT NULL UNIQUE,
        status TEXT NOT NULL DEFAULT 'draft',
        published_at TEXT,
        unpublished_at TEXT,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_imports (
        id SERIAL PRIMARY KEY,
        import_key TEXT NOT NULL UNIQUE,
        format TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'completed',
        source_filename TEXT,
        records_count INTEGER NOT NULL DEFAULT 0,
        error_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_exports (
        id SERIAL PRIMARY KEY,
        export_key TEXT NOT NULL UNIQUE,
        format TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'completed',
        destination TEXT NOT NULL DEFAULT '',
        records_count INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS expert_knowledge_snapshots (
        id SERIAL PRIMARY KEY,
        snapshot_key TEXT NOT NULL UNIQUE,
        scope TEXT NOT NULL DEFAULT 'global',
        payload_json TEXT NOT NULL DEFAULT '{}',
        record_count INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_expert_knowledge_documents_collection ON expert_knowledge_documents(collection_id, status)",
    "CREATE INDEX IF NOT EXISTS idx_expert_knowledge_articles_document ON expert_knowledge_articles(document_id, status)",
    "CREATE INDEX IF NOT EXISTS idx_expert_knowledge_chunks_document ON expert_knowledge_chunks(document_id)",
    "CREATE INDEX IF NOT EXISTS idx_expert_knowledge_chunks_lexical ON expert_knowledge_chunks(index_lexical)",
    "CREATE INDEX IF NOT EXISTS idx_expert_knowledge_categories_domain ON expert_knowledge_categories(domain, category_key)",
)

SQLITE_V11_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS expert_knowledge_collections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    collection_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    domain TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    source_type TEXT NOT NULL,
    url TEXT,
    publisher TEXT,
    trust_score INTEGER NOT NULL DEFAULT 70,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_key TEXT NOT NULL UNIQUE,
    domain TEXT NOT NULL,
    title TEXT NOT NULL,
    parent_key TEXT,
    description TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_key TEXT NOT NULL UNIQUE,
    label TEXT NOT NULL,
    domain TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    collection_id INTEGER NOT NULL,
    source_id INTEGER,
    document_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    format TEXT NOT NULL DEFAULT 'markdown',
    status TEXT NOT NULL DEFAULT 'draft',
    author TEXT,
    current_version_id INTEGER,
    category_key TEXT,
    tags_json TEXT NOT NULL DEFAULT '[]',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (collection_id) REFERENCES expert_knowledge_collections(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES expert_knowledge_sources(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    version_key TEXT NOT NULL,
    version_number INTEGER NOT NULL DEFAULT 1,
    content_hash TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    change_note TEXT,
    content_text TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
    UNIQUE (document_id, version_number)
);

CREATE TABLE IF NOT EXISTS expert_knowledge_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    article_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    slug TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    summary TEXT NOT NULL DEFAULT '',
    body_format TEXT NOT NULL DEFAULT 'markdown',
    published_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS expert_knowledge_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    section_key TEXT NOT NULL,
    title TEXT NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    content TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    FOREIGN KEY (article_id) REFERENCES expert_knowledge_articles(id) ON DELETE CASCADE,
    UNIQUE (article_id, section_key)
);

CREATE TABLE IF NOT EXISTS expert_knowledge_paragraphs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER NOT NULL,
    paragraph_key TEXT NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (section_id) REFERENCES expert_knowledge_sections(id) ON DELETE CASCADE,
    UNIQUE (section_id, paragraph_key)
);

CREATE TABLE IF NOT EXISTS expert_knowledge_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    article_id INTEGER,
    chunk_key TEXT NOT NULL UNIQUE,
    content TEXT NOT NULL,
    token_estimate INTEGER NOT NULL DEFAULT 0,
    index_lexical TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    freshness_score INTEGER NOT NULL DEFAULT 80,
    confidence_score INTEGER NOT NULL DEFAULT 75,
    created_at TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES expert_knowledge_articles(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_citations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chunk_id INTEGER NOT NULL,
    citation_key TEXT NOT NULL,
    label TEXT NOT NULL,
    source_ref TEXT,
    page TEXT,
    quote TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    FOREIGN KEY (chunk_id) REFERENCES expert_knowledge_chunks(id) ON DELETE CASCADE,
    UNIQUE (chunk_id, citation_key)
);

CREATE TABLE IF NOT EXISTS expert_knowledge_attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    attachment_key TEXT NOT NULL,
    filename TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    size_bytes INTEGER NOT NULL DEFAULT 0,
    storage_path TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
    UNIQUE (document_id, attachment_key)
);

CREATE TABLE IF NOT EXISTS expert_knowledge_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_document_id INTEGER NOT NULL,
    to_document_id INTEGER NOT NULL,
    reference_type TEXT NOT NULL DEFAULT 'references',
    label TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    FOREIGN KEY (from_document_id) REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
    FOREIGN KEY (to_document_id) REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS expert_knowledge_embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chunk_id INTEGER NOT NULL,
    model_key TEXT NOT NULL DEFAULT 'lawim-deterministic-v1',
    vector_json TEXT NOT NULL DEFAULT '[]',
    dimensions INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (chunk_id) REFERENCES expert_knowledge_chunks(id) ON DELETE CASCADE,
    UNIQUE (chunk_id, model_key)
);

CREATE TABLE IF NOT EXISTS expert_knowledge_indexes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    index_key TEXT NOT NULL,
    index_type TEXT NOT NULL DEFAULT 'lexical',
    status TEXT NOT NULL DEFAULT 'active',
    token_count INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
    UNIQUE (document_id, index_key)
);

CREATE TABLE IF NOT EXISTS expert_knowledge_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_type TEXT NOT NULL,
    subject_id INTEGER NOT NULL,
    object_type TEXT NOT NULL,
    object_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL,
    confidence INTEGER NOT NULL DEFAULT 50,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    user_id INTEGER,
    rating INTEGER NOT NULL DEFAULT 3,
    comment TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    FOREIGN KEY (article_id) REFERENCES expert_knowledge_articles(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    reviewer_id INTEGER,
    status TEXT NOT NULL DEFAULT 'pending',
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    approver_id INTEGER,
    status TEXT NOT NULL DEFAULT 'pending',
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
    FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    publication_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'draft',
    published_at TEXT,
    unpublished_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS expert_knowledge_imports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    import_key TEXT NOT NULL UNIQUE,
    format TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'completed',
    source_filename TEXT,
    records_count INTEGER NOT NULL DEFAULT 0,
    error_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_exports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    export_key TEXT NOT NULL UNIQUE,
    format TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'completed',
    destination TEXT NOT NULL DEFAULT '',
    records_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expert_knowledge_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_key TEXT NOT NULL UNIQUE,
    scope TEXT NOT NULL DEFAULT 'global',
    payload_json TEXT NOT NULL DEFAULT '{}',
    record_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_expert_knowledge_documents_collection ON expert_knowledge_documents(collection_id, status);
CREATE INDEX IF NOT EXISTS idx_expert_knowledge_articles_document ON expert_knowledge_articles(document_id, status);
CREATE INDEX IF NOT EXISTS idx_expert_knowledge_chunks_document ON expert_knowledge_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_expert_knowledge_chunks_lexical ON expert_knowledge_chunks(index_lexical);
CREATE INDEX IF NOT EXISTS idx_expert_knowledge_categories_domain ON expert_knowledge_categories(domain, category_key);
"""
