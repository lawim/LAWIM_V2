"""Schema v15 DDL — Marketplace platform (RELEASE PROGRAM I)."""

V15_TABLE_NAMES: tuple[str, ...] = (
    "marketplace_partner_registrations",
    "marketplace_provider_profiles",
    "marketplace_provider_certifications",
    "marketplace_catalog_categories",
    "marketplace_catalog_items",
    "marketplace_service_requests",
    "marketplace_request_documents",
    "marketplace_quotes",
    "marketplace_quote_lines",
    "marketplace_contracts",
    "marketplace_contract_documents",
    "marketplace_missions",
    "marketplace_mission_milestones",
    "marketplace_mission_deliverables",
    "marketplace_availability",
    "marketplace_reviews",
    "marketplace_review_moderation",
    "marketplace_reputation_snapshots",
    "marketplace_disputes",
    "marketplace_dispute_messages",
    "marketplace_subscription_plans",
    "marketplace_subscriptions",
    "marketplace_commission_rules",
    "marketplace_commissions",
    "marketplace_payment_preparations",
    "marketplace_matching_sessions",
    "marketplace_matching_results",
    "marketplace_portfolio_items",
    "marketplace_analytics_snapshots",
    "marketplace_ai_recommendations",
)

SQLITE_V15_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS marketplace_partner_registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_key TEXT NOT NULL UNIQUE,
    partner_profile_id INTEGER,
    organization_id INTEGER,
    applicant_name TEXT NOT NULL,
    applicant_email TEXT NOT NULL DEFAULT '',
    applicant_phone TEXT NOT NULL DEFAULT '',
    provider_type TEXT NOT NULL DEFAULT 'company',
    status TEXT NOT NULL DEFAULT 'draft',
    service_categories_json TEXT NOT NULL DEFAULT '[]',
    documents_json TEXT NOT NULL DEFAULT '[]',
    notes TEXT NOT NULL DEFAULT '',
    reviewed_by INTEGER,
    reviewed_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE SET NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE SET NULL,
    FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marketplace_provider_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_key TEXT NOT NULL UNIQUE,
    partner_profile_id INTEGER NOT NULL UNIQUE,
    provider_type TEXT NOT NULL DEFAULT 'company',
    headline TEXT NOT NULL DEFAULT '',
    bio TEXT NOT NULL DEFAULT '',
    service_radius_km INTEGER NOT NULL DEFAULT 50,
    languages_json TEXT NOT NULL DEFAULT '["fr"]',
    status TEXT NOT NULL DEFAULT 'active',
    featured INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace_provider_certifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_profile_id INTEGER NOT NULL,
    certification_key TEXT NOT NULL,
    title TEXT NOT NULL,
    issuer TEXT NOT NULL DEFAULT '',
    issued_at TEXT,
    expires_at TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (provider_profile_id) REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE,
    UNIQUE (provider_profile_id, certification_key)
);

CREATE TABLE IF NOT EXISTS marketplace_catalog_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    parent_id INTEGER,
    position INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES marketplace_catalog_categories(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marketplace_catalog_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_key TEXT NOT NULL UNIQUE,
    category_id INTEGER NOT NULL,
    service_catalog_id INTEGER,
    provider_profile_id INTEGER,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT 'other',
    price_min INTEGER,
    price_max INTEGER,
    currency TEXT NOT NULL DEFAULT 'XAF',
    duration_days INTEGER,
    status TEXT NOT NULL DEFAULT 'draft',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES marketplace_catalog_categories(id) ON DELETE CASCADE,
    FOREIGN KEY (service_catalog_id) REFERENCES service_catalog(id) ON DELETE SET NULL,
    FOREIGN KEY (provider_profile_id) REFERENCES marketplace_provider_profiles(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marketplace_service_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_key TEXT NOT NULL UNIQUE,
    user_id INTEGER,
    contact_id INTEGER,
    project_id INTEGER,
    property_id INTEGER,
    catalog_item_id INTEGER,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT 'other',
    city TEXT NOT NULL DEFAULT '',
    region TEXT NOT NULL DEFAULT '',
    country TEXT NOT NULL DEFAULT 'Cameroon',
    budget_min INTEGER,
    budget_max INTEGER,
    currency TEXT NOT NULL DEFAULT 'XAF',
    status TEXT NOT NULL DEFAULT 'draft',
    urgency TEXT NOT NULL DEFAULT 'normal',
    criteria_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    submitted_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET NULL,
    FOREIGN KEY (catalog_item_id) REFERENCES marketplace_catalog_items(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marketplace_request_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    document_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    document_type TEXT NOT NULL DEFAULT 'other',
    storage_ref TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (request_id) REFERENCES marketplace_service_requests(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace_quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote_key TEXT NOT NULL UNIQUE,
    request_id INTEGER NOT NULL,
    provider_profile_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    amount INTEGER NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'XAF',
    valid_until TEXT,
    notes TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    sent_at TEXT,
    accepted_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (request_id) REFERENCES marketplace_service_requests(id) ON DELETE CASCADE,
    FOREIGN KEY (provider_profile_id) REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace_quote_lines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote_id INTEGER NOT NULL,
    line_key TEXT NOT NULL,
    description TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price INTEGER NOT NULL DEFAULT 0,
    amount INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (quote_id) REFERENCES marketplace_quotes(id) ON DELETE CASCADE,
    UNIQUE (quote_id, line_key)
);

CREATE TABLE IF NOT EXISTS marketplace_contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_key TEXT NOT NULL UNIQUE,
    request_id INTEGER NOT NULL,
    quote_id INTEGER NOT NULL,
    provider_profile_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    amount INTEGER NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'XAF',
    terms_json TEXT NOT NULL DEFAULT '{}',
    signed_at TEXT,
    starts_at TEXT,
    ends_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (request_id) REFERENCES marketplace_service_requests(id) ON DELETE CASCADE,
    FOREIGN KEY (quote_id) REFERENCES marketplace_quotes(id) ON DELETE CASCADE,
    FOREIGN KEY (provider_profile_id) REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace_contract_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id INTEGER NOT NULL,
    document_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    document_type TEXT NOT NULL DEFAULT 'contract',
    storage_ref TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (contract_id) REFERENCES marketplace_contracts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace_missions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mission_key TEXT NOT NULL UNIQUE,
    contract_id INTEGER NOT NULL,
    provider_profile_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'planned',
    scheduled_start TEXT,
    scheduled_end TEXT,
    actual_start TEXT,
    actual_end TEXT,
    progress_percent INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (contract_id) REFERENCES marketplace_contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (provider_profile_id) REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace_mission_milestones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mission_id INTEGER NOT NULL,
    milestone_key TEXT NOT NULL,
    title TEXT NOT NULL,
    due_at TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    position INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    completed_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (mission_id) REFERENCES marketplace_missions(id) ON DELETE CASCADE,
    UNIQUE (mission_id, milestone_key)
);

CREATE TABLE IF NOT EXISTS marketplace_mission_deliverables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mission_id INTEGER NOT NULL,
    deliverable_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    storage_ref TEXT NOT NULL DEFAULT '',
    submitted_at TEXT,
    accepted_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (mission_id) REFERENCES marketplace_missions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace_availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_profile_id INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL DEFAULT 1,
    start_time TEXT NOT NULL DEFAULT '08:00',
    end_time TEXT NOT NULL DEFAULT '18:00',
    timezone TEXT NOT NULL DEFAULT 'Africa/Douala',
    status TEXT NOT NULL DEFAULT 'available',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (provider_profile_id) REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_key TEXT NOT NULL UNIQUE,
    provider_profile_id INTEGER NOT NULL,
    mission_id INTEGER,
    user_id INTEGER,
    rating INTEGER NOT NULL DEFAULT 5,
    title TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    published_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (provider_profile_id) REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (mission_id) REFERENCES marketplace_missions(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marketplace_review_moderation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id INTEGER NOT NULL UNIQUE,
    moderator_id INTEGER,
    action TEXT NOT NULL DEFAULT 'pending',
    reason TEXT NOT NULL DEFAULT '',
    notes TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (review_id) REFERENCES marketplace_reviews(id) ON DELETE CASCADE,
    FOREIGN KEY (moderator_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marketplace_reputation_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_profile_id INTEGER NOT NULL,
    score_key TEXT NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    factors_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL,
    UNIQUE (provider_profile_id, score_key)
);

CREATE TABLE IF NOT EXISTS marketplace_disputes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dispute_key TEXT NOT NULL UNIQUE,
    contract_id INTEGER NOT NULL,
    mission_id INTEGER,
    opened_by_user_id INTEGER,
    status TEXT NOT NULL DEFAULT 'open',
    reason TEXT NOT NULL DEFAULT '',
    resolution TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    opened_at TEXT NOT NULL,
    resolved_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (contract_id) REFERENCES marketplace_contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (mission_id) REFERENCES marketplace_missions(id) ON DELETE SET NULL,
    FOREIGN KEY (opened_by_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marketplace_dispute_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dispute_id INTEGER NOT NULL,
    author_user_id INTEGER,
    message TEXT NOT NULL,
    visibility TEXT NOT NULL DEFAULT 'parties',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (dispute_id) REFERENCES marketplace_disputes(id) ON DELETE CASCADE,
    FOREIGN KEY (author_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marketplace_subscription_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    price INTEGER NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'XAF',
    billing_period TEXT NOT NULL DEFAULT 'monthly',
    features_json TEXT NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS marketplace_subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subscription_key TEXT NOT NULL UNIQUE,
    plan_id INTEGER NOT NULL,
    provider_profile_id INTEGER,
    user_id INTEGER,
    status TEXT NOT NULL DEFAULT 'trial',
    started_at TEXT NOT NULL,
    ends_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (plan_id) REFERENCES marketplace_subscription_plans(id) ON DELETE CASCADE,
    FOREIGN KEY (provider_profile_id) REFERENCES marketplace_provider_profiles(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marketplace_commission_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    commission_type TEXT NOT NULL DEFAULT 'percentage',
    rate_percent REAL NOT NULL DEFAULT 10.0,
    flat_amount INTEGER NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'XAF',
    category TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS marketplace_commissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    commission_key TEXT NOT NULL UNIQUE,
    contract_id INTEGER NOT NULL,
    rule_id INTEGER,
    commission_type TEXT NOT NULL DEFAULT 'percentage',
    amount INTEGER NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'XAF',
    status TEXT NOT NULL DEFAULT 'pending',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL,
    paid_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (contract_id) REFERENCES marketplace_contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (rule_id) REFERENCES marketplace_commission_rules(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marketplace_payment_preparations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    preparation_key TEXT NOT NULL UNIQUE,
    contract_id INTEGER,
    subscription_id INTEGER,
    payment_method TEXT NOT NULL DEFAULT 'mobile_money',
    amount INTEGER NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'XAF',
    status TEXT NOT NULL DEFAULT 'prepared',
    payer_reference TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    prepared_at TEXT NOT NULL,
    expires_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (contract_id) REFERENCES marketplace_contracts(id) ON DELETE SET NULL,
    FOREIGN KEY (subscription_id) REFERENCES marketplace_subscriptions(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marketplace_matching_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_key TEXT NOT NULL UNIQUE,
    request_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    criteria_json TEXT NOT NULL DEFAULT '{}',
    result_count INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    started_at TEXT NOT NULL,
    completed_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (request_id) REFERENCES marketplace_service_requests(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace_matching_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    provider_profile_id INTEGER NOT NULL,
    partner_profile_id INTEGER NOT NULL,
    score REAL NOT NULL DEFAULT 0,
    rank INTEGER NOT NULL DEFAULT 0,
    reasons_json TEXT NOT NULL DEFAULT '[]',
    breakdown_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES marketplace_matching_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (provider_profile_id) REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace_portfolio_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_key TEXT NOT NULL UNIQUE,
    provider_profile_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT 'other',
    media_ref TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'published',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (provider_profile_id) REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marketplace_analytics_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_key TEXT NOT NULL UNIQUE,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS marketplace_ai_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recommendation_key TEXT NOT NULL UNIQUE,
    user_id INTEGER,
    request_id INTEGER,
    provider_profile_id INTEGER,
    recommendation_type TEXT NOT NULL DEFAULT 'provider',
    title TEXT NOT NULL,
    rationale TEXT NOT NULL DEFAULT '',
    score REAL NOT NULL DEFAULT 0,
    sources_json TEXT NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'pending',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (request_id) REFERENCES marketplace_service_requests(id) ON DELETE SET NULL,
    FOREIGN KEY (provider_profile_id) REFERENCES marketplace_provider_profiles(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_marketplace_registrations_status ON marketplace_partner_registrations(status, created_at);
CREATE INDEX IF NOT EXISTS idx_marketplace_providers_partner ON marketplace_provider_profiles(partner_profile_id, status);
CREATE INDEX IF NOT EXISTS idx_marketplace_catalog_items_category ON marketplace_catalog_items(category_id, status);
CREATE INDEX IF NOT EXISTS idx_marketplace_requests_status ON marketplace_service_requests(status, created_at);
CREATE INDEX IF NOT EXISTS idx_marketplace_quotes_request ON marketplace_quotes(request_id, status);
CREATE INDEX IF NOT EXISTS idx_marketplace_contracts_status ON marketplace_contracts(status, created_at);
CREATE INDEX IF NOT EXISTS idx_marketplace_missions_status ON marketplace_missions(status, scheduled_start);
CREATE INDEX IF NOT EXISTS idx_marketplace_reviews_provider ON marketplace_reviews(provider_profile_id, status);
CREATE INDEX IF NOT EXISTS idx_marketplace_disputes_status ON marketplace_disputes(status, opened_at);
CREATE INDEX IF NOT EXISTS idx_marketplace_matching_session ON marketplace_matching_results(session_id, rank);
CREATE INDEX IF NOT EXISTS idx_marketplace_subscriptions_status ON marketplace_subscriptions(status, ends_at);
"""

POSTGRESQL_V15_STATEMENTS: tuple[str, ...] = tuple(
    stmt.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
    for stmt in (
        """
        CREATE TABLE IF NOT EXISTS marketplace_partner_registrations (
            id SERIAL PRIMARY KEY,
            registration_key TEXT NOT NULL UNIQUE,
            partner_profile_id INTEGER REFERENCES partner_profiles(id) ON DELETE SET NULL,
            organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL,
            applicant_name TEXT NOT NULL,
            applicant_email TEXT NOT NULL DEFAULT '',
            applicant_phone TEXT NOT NULL DEFAULT '',
            provider_type TEXT NOT NULL DEFAULT 'company',
            status TEXT NOT NULL DEFAULT 'draft',
            service_categories_json TEXT NOT NULL DEFAULT '[]',
            documents_json TEXT NOT NULL DEFAULT '[]',
            notes TEXT NOT NULL DEFAULT '',
            reviewed_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
            reviewed_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_provider_profiles (
            id SERIAL PRIMARY KEY,
            provider_key TEXT NOT NULL UNIQUE,
            partner_profile_id INTEGER NOT NULL UNIQUE REFERENCES partner_profiles(id) ON DELETE CASCADE,
            provider_type TEXT NOT NULL DEFAULT 'company',
            headline TEXT NOT NULL DEFAULT '',
            bio TEXT NOT NULL DEFAULT '',
            service_radius_km INTEGER NOT NULL DEFAULT 50,
            languages_json TEXT NOT NULL DEFAULT '["fr"]',
            status TEXT NOT NULL DEFAULT 'active',
            featured INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_provider_certifications (
            id SERIAL PRIMARY KEY,
            provider_profile_id INTEGER NOT NULL REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE,
            certification_key TEXT NOT NULL,
            title TEXT NOT NULL,
            issuer TEXT NOT NULL DEFAULT '',
            issued_at TEXT,
            expires_at TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (provider_profile_id, certification_key)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_catalog_categories (
            id SERIAL PRIMARY KEY,
            category_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            parent_id INTEGER REFERENCES marketplace_catalog_categories(id) ON DELETE SET NULL,
            position INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_catalog_items (
            id SERIAL PRIMARY KEY,
            item_key TEXT NOT NULL UNIQUE,
            category_id INTEGER NOT NULL REFERENCES marketplace_catalog_categories(id) ON DELETE CASCADE,
            service_catalog_id INTEGER REFERENCES service_catalog(id) ON DELETE SET NULL,
            provider_profile_id INTEGER REFERENCES marketplace_provider_profiles(id) ON DELETE SET NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            category TEXT NOT NULL DEFAULT 'other',
            price_min INTEGER,
            price_max INTEGER,
            currency TEXT NOT NULL DEFAULT 'XAF',
            duration_days INTEGER,
            status TEXT NOT NULL DEFAULT 'draft',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_service_requests (
            id SERIAL PRIMARY KEY,
            request_key TEXT NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL,
            project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
            property_id INTEGER REFERENCES properties(id) ON DELETE SET NULL,
            catalog_item_id INTEGER REFERENCES marketplace_catalog_items(id) ON DELETE SET NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            category TEXT NOT NULL DEFAULT 'other',
            city TEXT NOT NULL DEFAULT '',
            region TEXT NOT NULL DEFAULT '',
            country TEXT NOT NULL DEFAULT 'Cameroon',
            budget_min INTEGER,
            budget_max INTEGER,
            currency TEXT NOT NULL DEFAULT 'XAF',
            status TEXT NOT NULL DEFAULT 'draft',
            urgency TEXT NOT NULL DEFAULT 'normal',
            criteria_json TEXT NOT NULL DEFAULT '{}',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            submitted_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_request_documents (
            id SERIAL PRIMARY KEY,
            request_id INTEGER NOT NULL REFERENCES marketplace_service_requests(id) ON DELETE CASCADE,
            document_key TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            document_type TEXT NOT NULL DEFAULT 'other',
            storage_ref TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_quotes (
            id SERIAL PRIMARY KEY,
            quote_key TEXT NOT NULL UNIQUE,
            request_id INTEGER NOT NULL REFERENCES marketplace_service_requests(id) ON DELETE CASCADE,
            provider_profile_id INTEGER NOT NULL REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE,
            status TEXT NOT NULL DEFAULT 'draft',
            amount INTEGER NOT NULL DEFAULT 0,
            currency TEXT NOT NULL DEFAULT 'XAF',
            valid_until TEXT,
            notes TEXT NOT NULL DEFAULT '',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            sent_at TEXT,
            accepted_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_quote_lines (
            id SERIAL PRIMARY KEY,
            quote_id INTEGER NOT NULL REFERENCES marketplace_quotes(id) ON DELETE CASCADE,
            line_key TEXT NOT NULL,
            description TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            unit_price INTEGER NOT NULL DEFAULT 0,
            amount INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (quote_id, line_key)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_contracts (
            id SERIAL PRIMARY KEY,
            contract_key TEXT NOT NULL UNIQUE,
            request_id INTEGER NOT NULL REFERENCES marketplace_service_requests(id) ON DELETE CASCADE,
            quote_id INTEGER NOT NULL REFERENCES marketplace_quotes(id) ON DELETE CASCADE,
            provider_profile_id INTEGER NOT NULL REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE,
            status TEXT NOT NULL DEFAULT 'draft',
            amount INTEGER NOT NULL DEFAULT 0,
            currency TEXT NOT NULL DEFAULT 'XAF',
            terms_json TEXT NOT NULL DEFAULT '{}',
            signed_at TEXT,
            starts_at TEXT,
            ends_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_contract_documents (
            id SERIAL PRIMARY KEY,
            contract_id INTEGER NOT NULL REFERENCES marketplace_contracts(id) ON DELETE CASCADE,
            document_key TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            document_type TEXT NOT NULL DEFAULT 'contract',
            storage_ref TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_missions (
            id SERIAL PRIMARY KEY,
            mission_key TEXT NOT NULL UNIQUE,
            contract_id INTEGER NOT NULL REFERENCES marketplace_contracts(id) ON DELETE CASCADE,
            provider_profile_id INTEGER NOT NULL REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'planned',
            scheduled_start TEXT,
            scheduled_end TEXT,
            actual_start TEXT,
            actual_end TEXT,
            progress_percent INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_mission_milestones (
            id SERIAL PRIMARY KEY,
            mission_id INTEGER NOT NULL REFERENCES marketplace_missions(id) ON DELETE CASCADE,
            milestone_key TEXT NOT NULL,
            title TEXT NOT NULL,
            due_at TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            position INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            completed_at TEXT,
            created_at TEXT NOT NULL,
            UNIQUE (mission_id, milestone_key)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_mission_deliverables (
            id SERIAL PRIMARY KEY,
            mission_id INTEGER NOT NULL REFERENCES marketplace_missions(id) ON DELETE CASCADE,
            deliverable_key TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            storage_ref TEXT NOT NULL DEFAULT '',
            submitted_at TEXT,
            accepted_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_availability (
            id SERIAL PRIMARY KEY,
            provider_profile_id INTEGER NOT NULL REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE,
            day_of_week INTEGER NOT NULL DEFAULT 1,
            start_time TEXT NOT NULL DEFAULT '08:00',
            end_time TEXT NOT NULL DEFAULT '18:00',
            timezone TEXT NOT NULL DEFAULT 'Africa/Douala',
            status TEXT NOT NULL DEFAULT 'available',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_reviews (
            id SERIAL PRIMARY KEY,
            review_key TEXT NOT NULL UNIQUE,
            provider_profile_id INTEGER NOT NULL REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE,
            mission_id INTEGER REFERENCES marketplace_missions(id) ON DELETE SET NULL,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            rating INTEGER NOT NULL DEFAULT 5,
            title TEXT NOT NULL DEFAULT '',
            body TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            published_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_review_moderation (
            id SERIAL PRIMARY KEY,
            review_id INTEGER NOT NULL UNIQUE REFERENCES marketplace_reviews(id) ON DELETE CASCADE,
            moderator_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            action TEXT NOT NULL DEFAULT 'pending',
            reason TEXT NOT NULL DEFAULT '',
            notes TEXT NOT NULL DEFAULT '',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_reputation_snapshots (
            id SERIAL PRIMARY KEY,
            provider_profile_id INTEGER NOT NULL,
            score_key TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 0,
            factors_json TEXT NOT NULL DEFAULT '{}',
            computed_at TEXT NOT NULL,
            UNIQUE (provider_profile_id, score_key)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_disputes (
            id SERIAL PRIMARY KEY,
            dispute_key TEXT NOT NULL UNIQUE,
            contract_id INTEGER NOT NULL REFERENCES marketplace_contracts(id) ON DELETE CASCADE,
            mission_id INTEGER REFERENCES marketplace_missions(id) ON DELETE SET NULL,
            opened_by_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            status TEXT NOT NULL DEFAULT 'open',
            reason TEXT NOT NULL DEFAULT '',
            resolution TEXT NOT NULL DEFAULT '',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            opened_at TEXT NOT NULL,
            resolved_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_dispute_messages (
            id SERIAL PRIMARY KEY,
            dispute_id INTEGER NOT NULL REFERENCES marketplace_disputes(id) ON DELETE CASCADE,
            author_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            message TEXT NOT NULL,
            visibility TEXT NOT NULL DEFAULT 'parties',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_subscription_plans (
            id SERIAL PRIMARY KEY,
            plan_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            price INTEGER NOT NULL DEFAULT 0,
            currency TEXT NOT NULL DEFAULT 'XAF',
            billing_period TEXT NOT NULL DEFAULT 'monthly',
            features_json TEXT NOT NULL DEFAULT '[]',
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_subscriptions (
            id SERIAL PRIMARY KEY,
            subscription_key TEXT NOT NULL UNIQUE,
            plan_id INTEGER NOT NULL REFERENCES marketplace_subscription_plans(id) ON DELETE CASCADE,
            provider_profile_id INTEGER REFERENCES marketplace_provider_profiles(id) ON DELETE SET NULL,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            status TEXT NOT NULL DEFAULT 'trial',
            started_at TEXT NOT NULL,
            ends_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_commission_rules (
            id SERIAL PRIMARY KEY,
            rule_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            commission_type TEXT NOT NULL DEFAULT 'percentage',
            rate_percent REAL NOT NULL DEFAULT 10.0,
            flat_amount INTEGER NOT NULL DEFAULT 0,
            currency TEXT NOT NULL DEFAULT 'XAF',
            category TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_commissions (
            id SERIAL PRIMARY KEY,
            commission_key TEXT NOT NULL UNIQUE,
            contract_id INTEGER NOT NULL REFERENCES marketplace_contracts(id) ON DELETE CASCADE,
            rule_id INTEGER REFERENCES marketplace_commission_rules(id) ON DELETE SET NULL,
            commission_type TEXT NOT NULL DEFAULT 'percentage',
            amount INTEGER NOT NULL DEFAULT 0,
            currency TEXT NOT NULL DEFAULT 'XAF',
            status TEXT NOT NULL DEFAULT 'pending',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            computed_at TEXT NOT NULL,
            paid_at TEXT,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_payment_preparations (
            id SERIAL PRIMARY KEY,
            preparation_key TEXT NOT NULL UNIQUE,
            contract_id INTEGER REFERENCES marketplace_contracts(id) ON DELETE SET NULL,
            subscription_id INTEGER REFERENCES marketplace_subscriptions(id) ON DELETE SET NULL,
            payment_method TEXT NOT NULL DEFAULT 'mobile_money',
            amount INTEGER NOT NULL DEFAULT 0,
            currency TEXT NOT NULL DEFAULT 'XAF',
            status TEXT NOT NULL DEFAULT 'prepared',
            payer_reference TEXT NOT NULL DEFAULT '',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            prepared_at TEXT NOT NULL,
            expires_at TEXT,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_matching_sessions (
            id SERIAL PRIMARY KEY,
            session_key TEXT NOT NULL UNIQUE,
            request_id INTEGER NOT NULL REFERENCES marketplace_service_requests(id) ON DELETE CASCADE,
            status TEXT NOT NULL DEFAULT 'pending',
            criteria_json TEXT NOT NULL DEFAULT '{}',
            result_count INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            started_at TEXT NOT NULL,
            completed_at TEXT,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_matching_results (
            id SERIAL PRIMARY KEY,
            session_id INTEGER NOT NULL REFERENCES marketplace_matching_sessions(id) ON DELETE CASCADE,
            provider_profile_id INTEGER NOT NULL REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE,
            partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
            score REAL NOT NULL DEFAULT 0,
            rank INTEGER NOT NULL DEFAULT 0,
            reasons_json TEXT NOT NULL DEFAULT '[]',
            breakdown_json TEXT NOT NULL DEFAULT '{}',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_portfolio_items (
            id SERIAL PRIMARY KEY,
            portfolio_key TEXT NOT NULL UNIQUE,
            provider_profile_id INTEGER NOT NULL REFERENCES marketplace_provider_profiles(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            category TEXT NOT NULL DEFAULT 'other',
            media_ref TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'published',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_analytics_snapshots (
            id SERIAL PRIMARY KEY,
            snapshot_key TEXT NOT NULL UNIQUE,
            scope TEXT NOT NULL DEFAULT 'global',
            metrics_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS marketplace_ai_recommendations (
            id SERIAL PRIMARY KEY,
            recommendation_key TEXT NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            request_id INTEGER REFERENCES marketplace_service_requests(id) ON DELETE SET NULL,
            provider_profile_id INTEGER REFERENCES marketplace_provider_profiles(id) ON DELETE SET NULL,
            recommendation_type TEXT NOT NULL DEFAULT 'provider',
            title TEXT NOT NULL,
            rationale TEXT NOT NULL DEFAULT '',
            score REAL NOT NULL DEFAULT 0,
            sources_json TEXT NOT NULL DEFAULT '[]',
            status TEXT NOT NULL DEFAULT 'pending',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        "CREATE INDEX IF NOT EXISTS idx_marketplace_registrations_status ON marketplace_partner_registrations(status, created_at)",
        "CREATE INDEX IF NOT EXISTS idx_marketplace_providers_partner ON marketplace_provider_profiles(partner_profile_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_marketplace_catalog_items_category ON marketplace_catalog_items(category_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_marketplace_requests_status ON marketplace_service_requests(status, created_at)",
        "CREATE INDEX IF NOT EXISTS idx_marketplace_quotes_request ON marketplace_quotes(request_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_marketplace_contracts_status ON marketplace_contracts(status, created_at)",
        "CREATE INDEX IF NOT EXISTS idx_marketplace_missions_status ON marketplace_missions(status, scheduled_start)",
        "CREATE INDEX IF NOT EXISTS idx_marketplace_reviews_provider ON marketplace_reviews(provider_profile_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_marketplace_disputes_status ON marketplace_disputes(status, opened_at)",
        "CREATE INDEX IF NOT EXISTS idx_marketplace_matching_session ON marketplace_matching_results(session_id, rank)",
        "CREATE INDEX IF NOT EXISTS idx_marketplace_subscriptions_status ON marketplace_subscriptions(status, ends_at)",
    )
)
