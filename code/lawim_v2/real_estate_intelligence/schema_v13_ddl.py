"""Schema v13 DDL — real estate intelligence platform (RELEASE PROGRAM G)."""

V13_TABLE_NAMES: tuple[str, ...] = (
    "rei_property_profiles",
    "rei_listings",
    "rei_listing_publications",
    "rei_listing_scores",
    "rei_property_owners",
    "rei_property_documents",
    "rei_property_valuations",
    "rei_verification_checks",
    "rei_verification_scores",
    "rei_matching_sessions",
    "rei_matching_results",
    "rei_visits",
    "rei_visit_reports",
    "rei_negotiations",
    "rei_offers",
    "rei_transactions",
    "rei_reservations",
    "rei_property_history",
    "rei_recommendations",
    "rei_intelligence_scores",
    "rei_analytics_snapshots",
    "rei_search_index",
    "rei_nearby_properties",
    "rei_property_reports",
)

SQLITE_V13_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS rei_property_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL UNIQUE,
    property_type TEXT NOT NULL DEFAULT 'apartment',
    subtype TEXT,
    characteristics_json TEXT NOT NULL DEFAULT '{}',
    provenance TEXT NOT NULL DEFAULT 'internal',
    availability_status TEXT NOT NULL DEFAULT 'available',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rei_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_key TEXT NOT NULL UNIQUE,
    property_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    visibility TEXT NOT NULL DEFAULT 'public',
    ai_score INTEGER NOT NULL DEFAULT 0,
    diffusion_json TEXT NOT NULL DEFAULT '[]',
    expires_at TEXT,
    published_at TEXT,
    archived_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rei_listing_publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    channel TEXT NOT NULL DEFAULT 'lawim',
    status TEXT NOT NULL DEFAULT 'published',
    published_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (listing_id) REFERENCES rei_listings(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rei_listing_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    score_type TEXT NOT NULL DEFAULT 'visibility',
    score INTEGER NOT NULL DEFAULT 0,
    factors_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (listing_id) REFERENCES rei_listings(id) ON DELETE CASCADE,
    UNIQUE (listing_id, score_type)
);

CREATE TABLE IF NOT EXISTS rei_property_owners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    owner_type TEXT NOT NULL DEFAULT 'individual',
    owner_name TEXT NOT NULL,
    owner_contact TEXT NOT NULL DEFAULT '',
    ownership_share REAL NOT NULL DEFAULT 100.0,
    verified INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rei_property_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    document_key TEXT NOT NULL,
    document_type TEXT NOT NULL DEFAULT 'other',
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    storage_ref TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    UNIQUE (property_id, document_key)
);

CREATE TABLE IF NOT EXISTS rei_property_valuations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    valuation_key TEXT NOT NULL UNIQUE,
    amount INTEGER NOT NULL,
    currency TEXT NOT NULL DEFAULT 'XAF',
    method TEXT NOT NULL DEFAULT 'comparative',
    confidence INTEGER NOT NULL DEFAULT 70,
    factors_json TEXT NOT NULL DEFAULT '{}',
    valued_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rei_verification_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    check_key TEXT NOT NULL,
    check_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    result_json TEXT NOT NULL DEFAULT '{}',
    anomaly_flags_json TEXT NOT NULL DEFAULT '[]',
    checked_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    UNIQUE (property_id, check_key)
);

CREATE TABLE IF NOT EXISTS rei_verification_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL UNIQUE,
    trust_score INTEGER NOT NULL DEFAULT 0,
    consistency_score INTEGER NOT NULL DEFAULT 0,
    details_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rei_matching_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_key TEXT NOT NULL UNIQUE,
    user_id INTEGER,
    project_id INTEGER,
    criteria_json TEXT NOT NULL DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS rei_matching_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    property_id INTEGER NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    reasons_json TEXT NOT NULL DEFAULT '[]',
    rank_position INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES rei_matching_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rei_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_key TEXT NOT NULL UNIQUE,
    property_id INTEGER NOT NULL,
    user_id INTEGER,
    scheduled_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled',
    confirmed_at TEXT,
    cancelled_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS rei_visit_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visit_id INTEGER NOT NULL UNIQUE,
    summary TEXT NOT NULL DEFAULT '',
    rating INTEGER NOT NULL DEFAULT 3,
    signed INTEGER NOT NULL DEFAULT 0,
    report_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (visit_id) REFERENCES rei_visits(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rei_negotiations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    negotiation_key TEXT NOT NULL UNIQUE,
    property_id INTEGER NOT NULL,
    buyer_id INTEGER,
    status TEXT NOT NULL DEFAULT 'open',
    current_offer_id INTEGER,
    workflow_instance_id INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (buyer_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS rei_offers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    offer_key TEXT NOT NULL UNIQUE,
    negotiation_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    currency TEXT NOT NULL DEFAULT 'XAF',
    status TEXT NOT NULL DEFAULT 'submitted',
    offer_type TEXT NOT NULL DEFAULT 'purchase',
    terms_json TEXT NOT NULL DEFAULT '{}',
    submitted_at TEXT NOT NULL,
    decided_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (negotiation_id) REFERENCES rei_negotiations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rei_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_key TEXT NOT NULL UNIQUE,
    property_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL DEFAULT 'sale',
    status TEXT NOT NULL DEFAULT 'pending',
    amount INTEGER,
    currency TEXT NOT NULL DEFAULT 'XAF',
    buyer_id INTEGER,
    seller_id INTEGER,
    workflow_instance_id INTEGER,
    closed_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rei_reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_key TEXT NOT NULL UNIQUE,
    property_id INTEGER NOT NULL,
    user_id INTEGER,
    status TEXT NOT NULL DEFAULT 'pending',
    reserved_until TEXT NOT NULL,
    amount INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS rei_property_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    event_key TEXT NOT NULL,
    summary TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    actor_id INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (property_id, event_key)
);

CREATE TABLE IF NOT EXISTS rei_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recommendation_key TEXT NOT NULL UNIQUE,
    user_id INTEGER,
    project_id INTEGER,
    property_id INTEGER,
    recommendation_type TEXT NOT NULL DEFAULT 'property',
    score INTEGER NOT NULL DEFAULT 0,
    title TEXT NOT NULL,
    rationale TEXT NOT NULL DEFAULT '',
    sources_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS rei_intelligence_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    score_key TEXT NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    factors_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    UNIQUE (property_id, score_key)
);

CREATE TABLE IF NOT EXISTS rei_analytics_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_key TEXT NOT NULL UNIQUE,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rei_search_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL UNIQUE,
    index_text TEXT NOT NULL DEFAULT '',
    geo_hash TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rei_nearby_properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    nearby_property_id INTEGER NOT NULL,
    distance_km REAL NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (nearby_property_id) REFERENCES properties(id) ON DELETE CASCADE,
    UNIQUE (property_id, nearby_property_id)
);

CREATE TABLE IF NOT EXISTS rei_property_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_key TEXT NOT NULL UNIQUE,
    property_id INTEGER NOT NULL,
    report_type TEXT NOT NULL DEFAULT 'summary',
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_rei_listings_property ON rei_listings(property_id, status);
CREATE INDEX IF NOT EXISTS idx_rei_visits_property ON rei_visits(property_id, scheduled_at);
CREATE INDEX IF NOT EXISTS idx_rei_transactions_property ON rei_transactions(property_id, status);
CREATE INDEX IF NOT EXISTS idx_rei_matching_results_session ON rei_matching_results(session_id, score);
CREATE INDEX IF NOT EXISTS idx_rei_recommendations_user ON rei_recommendations(user_id, recommendation_type);
CREATE INDEX IF NOT EXISTS idx_rei_intelligence_scores_property ON rei_intelligence_scores(property_id, score_key);
CREATE INDEX IF NOT EXISTS idx_rei_search_index_text ON rei_search_index(index_text);
"""

POSTGRESQL_V13_STATEMENTS: tuple[str, ...] = tuple(
    stmt.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
    for stmt in (
        """
        CREATE TABLE IF NOT EXISTS rei_property_profiles (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL UNIQUE REFERENCES properties(id) ON DELETE CASCADE,
            property_type TEXT NOT NULL DEFAULT 'apartment',
            subtype TEXT,
            characteristics_json TEXT NOT NULL DEFAULT '{}',
            provenance TEXT NOT NULL DEFAULT 'internal',
            availability_status TEXT NOT NULL DEFAULT 'available',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_listings (
            id SERIAL PRIMARY KEY,
            listing_key TEXT NOT NULL UNIQUE,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'draft',
            visibility TEXT NOT NULL DEFAULT 'public',
            ai_score INTEGER NOT NULL DEFAULT 0,
            diffusion_json TEXT NOT NULL DEFAULT '[]',
            expires_at TEXT,
            published_at TEXT,
            archived_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_listing_publications (
            id SERIAL PRIMARY KEY,
            listing_id INTEGER NOT NULL REFERENCES rei_listings(id) ON DELETE CASCADE,
            channel TEXT NOT NULL DEFAULT 'lawim',
            status TEXT NOT NULL DEFAULT 'published',
            published_at TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_listing_scores (
            id SERIAL PRIMARY KEY,
            listing_id INTEGER NOT NULL REFERENCES rei_listings(id) ON DELETE CASCADE,
            score_type TEXT NOT NULL DEFAULT 'visibility',
            score INTEGER NOT NULL DEFAULT 0,
            factors_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (listing_id, score_type)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_property_owners (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            owner_type TEXT NOT NULL DEFAULT 'individual',
            owner_name TEXT NOT NULL,
            owner_contact TEXT NOT NULL DEFAULT '',
            ownership_share REAL NOT NULL DEFAULT 100.0,
            verified INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_property_documents (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            document_key TEXT NOT NULL,
            document_type TEXT NOT NULL DEFAULT 'other',
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            storage_ref TEXT NOT NULL DEFAULT '',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (property_id, document_key)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_property_valuations (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            valuation_key TEXT NOT NULL UNIQUE,
            amount INTEGER NOT NULL,
            currency TEXT NOT NULL DEFAULT 'XAF',
            method TEXT NOT NULL DEFAULT 'comparative',
            confidence INTEGER NOT NULL DEFAULT 70,
            factors_json TEXT NOT NULL DEFAULT '{}',
            valued_at TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_verification_checks (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            check_key TEXT NOT NULL,
            check_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            result_json TEXT NOT NULL DEFAULT '{}',
            anomaly_flags_json TEXT NOT NULL DEFAULT '[]',
            checked_at TEXT,
            created_at TEXT NOT NULL,
            UNIQUE (property_id, check_key)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_verification_scores (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL UNIQUE REFERENCES properties(id) ON DELETE CASCADE,
            trust_score INTEGER NOT NULL DEFAULT 0,
            consistency_score INTEGER NOT NULL DEFAULT 0,
            details_json TEXT NOT NULL DEFAULT '{}',
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_matching_sessions (
            id SERIAL PRIMARY KEY,
            session_key TEXT NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
            criteria_json TEXT NOT NULL DEFAULT '{}',
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_matching_results (
            id SERIAL PRIMARY KEY,
            session_id INTEGER NOT NULL REFERENCES rei_matching_sessions(id) ON DELETE CASCADE,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            score INTEGER NOT NULL DEFAULT 0,
            reasons_json TEXT NOT NULL DEFAULT '[]',
            rank_position INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_visits (
            id SERIAL PRIMARY KEY,
            visit_key TEXT NOT NULL UNIQUE,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            scheduled_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'scheduled',
            confirmed_at TEXT,
            cancelled_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_visit_reports (
            id SERIAL PRIMARY KEY,
            visit_id INTEGER NOT NULL UNIQUE REFERENCES rei_visits(id) ON DELETE CASCADE,
            summary TEXT NOT NULL DEFAULT '',
            rating INTEGER NOT NULL DEFAULT 3,
            signed INTEGER NOT NULL DEFAULT 0,
            report_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_negotiations (
            id SERIAL PRIMARY KEY,
            negotiation_key TEXT NOT NULL UNIQUE,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            buyer_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            status TEXT NOT NULL DEFAULT 'open',
            current_offer_id INTEGER,
            workflow_instance_id INTEGER,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_offers (
            id SERIAL PRIMARY KEY,
            offer_key TEXT NOT NULL UNIQUE,
            negotiation_id INTEGER NOT NULL REFERENCES rei_negotiations(id) ON DELETE CASCADE,
            amount INTEGER NOT NULL,
            currency TEXT NOT NULL DEFAULT 'XAF',
            status TEXT NOT NULL DEFAULT 'submitted',
            offer_type TEXT NOT NULL DEFAULT 'purchase',
            terms_json TEXT NOT NULL DEFAULT '{}',
            submitted_at TEXT NOT NULL,
            decided_at TEXT,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_transactions (
            id SERIAL PRIMARY KEY,
            transaction_key TEXT NOT NULL UNIQUE,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            transaction_type TEXT NOT NULL DEFAULT 'sale',
            status TEXT NOT NULL DEFAULT 'pending',
            amount INTEGER,
            currency TEXT NOT NULL DEFAULT 'XAF',
            buyer_id INTEGER,
            seller_id INTEGER,
            workflow_instance_id INTEGER,
            closed_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_reservations (
            id SERIAL PRIMARY KEY,
            reservation_key TEXT NOT NULL UNIQUE,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            reserved_until TEXT NOT NULL,
            amount INTEGER,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_property_history (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            event_type TEXT NOT NULL,
            event_key TEXT NOT NULL,
            summary TEXT NOT NULL DEFAULT '',
            payload_json TEXT NOT NULL DEFAULT '{}',
            actor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            created_at TEXT NOT NULL,
            UNIQUE (property_id, event_key)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_recommendations (
            id SERIAL PRIMARY KEY,
            recommendation_key TEXT NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
            property_id INTEGER REFERENCES properties(id) ON DELETE SET NULL,
            recommendation_type TEXT NOT NULL DEFAULT 'property',
            score INTEGER NOT NULL DEFAULT 0,
            title TEXT NOT NULL,
            rationale TEXT NOT NULL DEFAULT '',
            sources_json TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_intelligence_scores (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            score_key TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 0,
            factors_json TEXT NOT NULL DEFAULT '{}',
            computed_at TEXT NOT NULL,
            UNIQUE (property_id, score_key)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_analytics_snapshots (
            id SERIAL PRIMARY KEY,
            snapshot_key TEXT NOT NULL UNIQUE,
            scope TEXT NOT NULL DEFAULT 'global',
            metrics_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_search_index (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL UNIQUE REFERENCES properties(id) ON DELETE CASCADE,
            index_text TEXT NOT NULL DEFAULT '',
            geo_hash TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_nearby_properties (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            nearby_property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            distance_km REAL NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            UNIQUE (property_id, nearby_property_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rei_property_reports (
            id SERIAL PRIMARY KEY,
            report_key TEXT NOT NULL UNIQUE,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            report_type TEXT NOT NULL DEFAULT 'summary',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        "CREATE INDEX IF NOT EXISTS idx_rei_listings_property ON rei_listings(property_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_rei_visits_property ON rei_visits(property_id, scheduled_at)",
        "CREATE INDEX IF NOT EXISTS idx_rei_transactions_property ON rei_transactions(property_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_rei_matching_results_session ON rei_matching_results(session_id, score)",
        "CREATE INDEX IF NOT EXISTS idx_rei_recommendations_user ON rei_recommendations(user_id, recommendation_type)",
        "CREATE INDEX IF NOT EXISTS idx_rei_intelligence_scores_property ON rei_intelligence_scores(property_id, score_key)",
        "CREATE INDEX IF NOT EXISTS idx_rei_search_index_text ON rei_search_index(index_text)",
    )
)
