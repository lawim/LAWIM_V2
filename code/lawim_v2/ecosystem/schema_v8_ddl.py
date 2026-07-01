"""Schema v8 DDL extensions for intelligent ecosystem platform."""

V8_TABLE_NAMES: tuple[str, ...] = (
    "partner_profiles",
    "partner_zones",
    "partner_skills",
    "partner_certifications",
    "partner_availability",
    "partner_sla",
    "service_catalog",
    "service_catalog_partners",
    "project_match_results",
    "service_orders",
    "project_interventions",
    "workflows",
    "workflow_steps",
    "workflow_instances",
    "workflow_instance_steps",
    "ecosystem_events",
    "ecosystem_notifications",
    "reputation_metrics",
    "project_ecosystem_state",
)

POSTGRESQL_V8_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS partner_profiles (
        id SERIAL PRIMARY KEY,
        organization_id INTEGER NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
        partner_type TEXT NOT NULL,
        display_name TEXT NOT NULL,
        legal_name TEXT,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'active',
        quality_score INTEGER NOT NULL DEFAULT 70,
        trust_score INTEGER NOT NULL DEFAULT 70,
        completion_rate REAL NOT NULL DEFAULT 0.85,
        reliability_score INTEGER NOT NULL DEFAULT 75,
        response_time_hours REAL NOT NULL DEFAULT 24,
        satisfaction_score INTEGER NOT NULL DEFAULT 80,
        incident_count INTEGER NOT NULL DEFAULT 0,
        specialties_json TEXT NOT NULL DEFAULT '[]',
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (organization_id, partner_type)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS partner_zones (
        id SERIAL PRIMARY KEY,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        city TEXT,
        region TEXT,
        country TEXT NOT NULL DEFAULT 'Cameroon',
        radius_km REAL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS partner_skills (
        id SERIAL PRIMARY KEY,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        skill_key TEXT NOT NULL,
        level TEXT NOT NULL DEFAULT 'standard',
        created_at TEXT NOT NULL,
        UNIQUE (partner_profile_id, skill_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS partner_certifications (
        id SERIAL PRIMARY KEY,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        certification_key TEXT NOT NULL,
        title TEXT NOT NULL,
        valid_until TEXT,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS partner_availability (
        id SERIAL PRIMARY KEY,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        status TEXT NOT NULL DEFAULT 'available',
        schedule_json TEXT NOT NULL DEFAULT '{}',
        updated_at TEXT NOT NULL,
        UNIQUE (partner_profile_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS partner_sla (
        id SERIAL PRIMARY KEY,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        response_hours REAL NOT NULL DEFAULT 24,
        completion_days INTEGER NOT NULL DEFAULT 14,
        uptime_percent REAL NOT NULL DEFAULT 95,
        created_at TEXT NOT NULL,
        UNIQUE (partner_profile_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS service_catalog (
        id SERIAL PRIMARY KEY,
        service_key TEXT NOT NULL UNIQUE,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        conditions TEXT,
        indicative_price_min INTEGER,
        indicative_price_max INTEGER,
        currency TEXT NOT NULL DEFAULT 'XAF',
        estimated_duration_days INTEGER NOT NULL DEFAULT 7,
        documents_json TEXT NOT NULL DEFAULT '[]',
        prerequisites_json TEXT NOT NULL DEFAULT '[]',
        deliverables_json TEXT NOT NULL DEFAULT '[]',
        status TEXT NOT NULL DEFAULT 'active',
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS service_catalog_partners (
        id SERIAL PRIMARY KEY,
        service_catalog_id INTEGER NOT NULL REFERENCES service_catalog(id) ON DELETE CASCADE,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        priority INTEGER NOT NULL DEFAULT 50,
        created_at TEXT NOT NULL,
        UNIQUE (service_catalog_id, partner_profile_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS project_match_results (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        match_type TEXT NOT NULL,
        partner_profile_id INTEGER REFERENCES partner_profiles(id) ON DELETE SET NULL,
        service_catalog_id INTEGER REFERENCES service_catalog(id) ON DELETE SET NULL,
        score INTEGER NOT NULL DEFAULT 50,
        confidence INTEGER NOT NULL DEFAULT 50,
        priority INTEGER NOT NULL DEFAULT 50,
        rationale_json TEXT NOT NULL DEFAULT '[]',
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS service_orders (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        service_catalog_id INTEGER NOT NULL REFERENCES service_catalog(id) ON DELETE RESTRICT,
        partner_profile_id INTEGER REFERENCES partner_profiles(id) ON DELETE SET NULL,
        status TEXT NOT NULL DEFAULT 'requested',
        cost_estimate INTEGER,
        currency TEXT NOT NULL DEFAULT 'XAF',
        scheduled_at TEXT,
        completed_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS project_interventions (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        partner_profile_id INTEGER REFERENCES partner_profiles(id) ON DELETE SET NULL,
        service_order_id INTEGER REFERENCES service_orders(id) ON DELETE SET NULL,
        intervention_type TEXT NOT NULL DEFAULT 'service',
        title TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'planned',
        scheduled_at TEXT,
        completed_at TEXT,
        cost_actual INTEGER,
        currency TEXT NOT NULL DEFAULT 'XAF',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS workflows (
        id SERIAL PRIMARY KEY,
        workflow_key TEXT NOT NULL UNIQUE,
        workflow_type TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS workflow_steps (
        id SERIAL PRIMARY KEY,
        workflow_id INTEGER NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
        step_key TEXT NOT NULL,
        title TEXT NOT NULL,
        position INTEGER NOT NULL DEFAULT 0,
        partner_type TEXT,
        service_key TEXT,
        depends_on_json TEXT NOT NULL DEFAULT '[]',
        validation_rules_json TEXT NOT NULL DEFAULT '[]',
        created_at TEXT NOT NULL,
        UNIQUE (workflow_id, step_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS workflow_instances (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        workflow_id INTEGER NOT NULL REFERENCES workflows(id) ON DELETE RESTRICT,
        status TEXT NOT NULL DEFAULT 'active',
        current_step_key TEXT,
        started_at TEXT NOT NULL,
        completed_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (project_id, workflow_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS workflow_instance_steps (
        id SERIAL PRIMARY KEY,
        workflow_instance_id INTEGER NOT NULL REFERENCES workflow_instances(id) ON DELETE CASCADE,
        step_key TEXT NOT NULL,
        title TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        partner_profile_id INTEGER REFERENCES partner_profiles(id) ON DELETE SET NULL,
        due_at TEXT,
        completed_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (workflow_instance_id, step_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ecosystem_events (
        id SERIAL PRIMARY KEY,
        project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        event_type TEXT NOT NULL,
        title TEXT NOT NULL,
        payload_json TEXT NOT NULL DEFAULT '{}',
        occurred_at TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ecosystem_notifications (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
        event_id INTEGER REFERENCES ecosystem_events(id) ON DELETE SET NULL,
        kind TEXT NOT NULL,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        channel TEXT NOT NULL DEFAULT 'in_app',
        status TEXT NOT NULL DEFAULT 'pending',
        scheduled_at TEXT,
        delivered_at TEXT,
        payload_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS reputation_metrics (
        id SERIAL PRIMARY KEY,
        subject_type TEXT NOT NULL,
        subject_id INTEGER NOT NULL,
        trust_score INTEGER NOT NULL DEFAULT 70,
        quality_score INTEGER NOT NULL DEFAULT 70,
        completion_rate REAL NOT NULL DEFAULT 0.85,
        reliability INTEGER NOT NULL DEFAULT 75,
        avg_response_hours REAL NOT NULL DEFAULT 24,
        satisfaction INTEGER NOT NULL DEFAULT 80,
        incident_count INTEGER NOT NULL DEFAULT 0,
        history_json TEXT NOT NULL DEFAULT '[]',
        computed_at TEXT NOT NULL,
        UNIQUE (subject_type, subject_id, computed_at)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS project_ecosystem_state (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        orchestration_json TEXT NOT NULL DEFAULT '{}',
        last_matched_at TEXT,
        updated_at TEXT NOT NULL,
        UNIQUE (project_id)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_partner_profiles_type ON partner_profiles(partner_type, status)",
    "CREATE INDEX IF NOT EXISTS idx_partner_zones_geo ON partner_zones(city, region, country)",
    "CREATE INDEX IF NOT EXISTS idx_service_catalog_category ON service_catalog(category, status)",
    "CREATE INDEX IF NOT EXISTS idx_project_match_results_project ON project_match_results(project_id, match_type, status)",
    "CREATE INDEX IF NOT EXISTS idx_service_orders_project ON service_orders(project_id, status)",
    "CREATE INDEX IF NOT EXISTS idx_project_interventions_project ON project_interventions(project_id, status)",
    "CREATE INDEX IF NOT EXISTS idx_workflow_instances_project ON workflow_instances(project_id, status)",
    "CREATE INDEX IF NOT EXISTS idx_ecosystem_events_project ON ecosystem_events(project_id, occurred_at, id)",
    "CREATE INDEX IF NOT EXISTS idx_ecosystem_notifications_user ON ecosystem_notifications(user_id, status, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_reputation_metrics_subject ON reputation_metrics(subject_type, subject_id, computed_at)",
)

SQLITE_V8_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS partner_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER NOT NULL,
    partner_type TEXT NOT NULL,
    display_name TEXT NOT NULL,
    legal_name TEXT,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    quality_score INTEGER NOT NULL DEFAULT 70,
    trust_score INTEGER NOT NULL DEFAULT 70,
    completion_rate REAL NOT NULL DEFAULT 0.85,
    reliability_score INTEGER NOT NULL DEFAULT 75,
    response_time_hours REAL NOT NULL DEFAULT 24,
    satisfaction_score INTEGER NOT NULL DEFAULT 80,
    incident_count INTEGER NOT NULL DEFAULT 0,
    specialties_json TEXT NOT NULL DEFAULT '[]',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    UNIQUE (organization_id, partner_type)
);

CREATE TABLE IF NOT EXISTS partner_zones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partner_profile_id INTEGER NOT NULL,
    city TEXT,
    region TEXT,
    country TEXT NOT NULL DEFAULT 'Cameroon',
    radius_km REAL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS partner_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partner_profile_id INTEGER NOT NULL,
    skill_key TEXT NOT NULL,
    level TEXT NOT NULL DEFAULT 'standard',
    created_at TEXT NOT NULL,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE CASCADE,
    UNIQUE (partner_profile_id, skill_key)
);

CREATE TABLE IF NOT EXISTS partner_certifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partner_profile_id INTEGER NOT NULL,
    certification_key TEXT NOT NULL,
    title TEXT NOT NULL,
    valid_until TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS partner_availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partner_profile_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'available',
    schedule_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE CASCADE,
    UNIQUE (partner_profile_id)
);

CREATE TABLE IF NOT EXISTS partner_sla (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partner_profile_id INTEGER NOT NULL,
    response_hours REAL NOT NULL DEFAULT 24,
    completion_days INTEGER NOT NULL DEFAULT 14,
    uptime_percent REAL NOT NULL DEFAULT 95,
    created_at TEXT NOT NULL,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE CASCADE,
    UNIQUE (partner_profile_id)
);

CREATE TABLE IF NOT EXISTS service_catalog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_key TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    conditions TEXT,
    indicative_price_min INTEGER,
    indicative_price_max INTEGER,
    currency TEXT NOT NULL DEFAULT 'XAF',
    estimated_duration_days INTEGER NOT NULL DEFAULT 7,
    documents_json TEXT NOT NULL DEFAULT '[]',
    prerequisites_json TEXT NOT NULL DEFAULT '[]',
    deliverables_json TEXT NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS service_catalog_partners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_catalog_id INTEGER NOT NULL,
    partner_profile_id INTEGER NOT NULL,
    priority INTEGER NOT NULL DEFAULT 50,
    created_at TEXT NOT NULL,
    FOREIGN KEY (service_catalog_id) REFERENCES service_catalog(id) ON DELETE CASCADE,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE CASCADE,
    UNIQUE (service_catalog_id, partner_profile_id)
);

CREATE TABLE IF NOT EXISTS project_match_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    match_type TEXT NOT NULL,
    partner_profile_id INTEGER,
    service_catalog_id INTEGER,
    score INTEGER NOT NULL DEFAULT 50,
    confidence INTEGER NOT NULL DEFAULT 50,
    priority INTEGER NOT NULL DEFAULT 50,
    rationale_json TEXT NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE SET NULL,
    FOREIGN KEY (service_catalog_id) REFERENCES service_catalog(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS service_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    service_catalog_id INTEGER NOT NULL,
    partner_profile_id INTEGER,
    status TEXT NOT NULL DEFAULT 'requested',
    cost_estimate INTEGER,
    currency TEXT NOT NULL DEFAULT 'XAF',
    scheduled_at TEXT,
    completed_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (service_catalog_id) REFERENCES service_catalog(id) ON DELETE RESTRICT,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS project_interventions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    partner_profile_id INTEGER,
    service_order_id INTEGER,
    intervention_type TEXT NOT NULL DEFAULT 'service',
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'planned',
    scheduled_at TEXT,
    completed_at TEXT,
    cost_actual INTEGER,
    currency TEXT NOT NULL DEFAULT 'XAF',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE SET NULL,
    FOREIGN KEY (service_order_id) REFERENCES service_orders(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS workflows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_key TEXT NOT NULL UNIQUE,
    workflow_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS workflow_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_id INTEGER NOT NULL,
    step_key TEXT NOT NULL,
    title TEXT NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    partner_type TEXT,
    service_key TEXT,
    depends_on_json TEXT NOT NULL DEFAULT '[]',
    validation_rules_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL,
    FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE CASCADE,
    UNIQUE (workflow_id, step_key)
);

CREATE TABLE IF NOT EXISTS workflow_instances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    workflow_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    current_step_key TEXT,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE RESTRICT,
    UNIQUE (project_id, workflow_id)
);

CREATE TABLE IF NOT EXISTS workflow_instance_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_instance_id INTEGER NOT NULL,
    step_key TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    partner_profile_id INTEGER,
    due_at TEXT,
    completed_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (workflow_instance_id) REFERENCES workflow_instances(id) ON DELETE CASCADE,
    FOREIGN KEY (partner_profile_id) REFERENCES partner_profiles(id) ON DELETE SET NULL,
    UNIQUE (workflow_instance_id, step_key)
);

CREATE TABLE IF NOT EXISTS ecosystem_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    user_id INTEGER,
    event_type TEXT NOT NULL,
    title TEXT NOT NULL,
    payload_json TEXT NOT NULL DEFAULT '{}',
    occurred_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ecosystem_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    project_id INTEGER,
    event_id INTEGER,
    kind TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    channel TEXT NOT NULL DEFAULT 'in_app',
    status TEXT NOT NULL DEFAULT 'pending',
    scheduled_at TEXT,
    delivered_at TEXT,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES ecosystem_events(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS reputation_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_type TEXT NOT NULL,
    subject_id INTEGER NOT NULL,
    trust_score INTEGER NOT NULL DEFAULT 70,
    quality_score INTEGER NOT NULL DEFAULT 70,
    completion_rate REAL NOT NULL DEFAULT 0.85,
    reliability INTEGER NOT NULL DEFAULT 75,
    avg_response_hours REAL NOT NULL DEFAULT 24,
    satisfaction INTEGER NOT NULL DEFAULT 80,
    incident_count INTEGER NOT NULL DEFAULT 0,
    history_json TEXT NOT NULL DEFAULT '[]',
    computed_at TEXT NOT NULL,
    UNIQUE (subject_type, subject_id, computed_at)
);

CREATE TABLE IF NOT EXISTS project_ecosystem_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    orchestration_json TEXT NOT NULL DEFAULT '{}',
    last_matched_at TEXT,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id)
);

CREATE INDEX IF NOT EXISTS idx_partner_profiles_type ON partner_profiles(partner_type, status);
CREATE INDEX IF NOT EXISTS idx_partner_zones_geo ON partner_zones(city, region, country);
CREATE INDEX IF NOT EXISTS idx_service_catalog_category ON service_catalog(category, status);
CREATE INDEX IF NOT EXISTS idx_project_match_results_project ON project_match_results(project_id, match_type, status);
CREATE INDEX IF NOT EXISTS idx_service_orders_project ON service_orders(project_id, status);
CREATE INDEX IF NOT EXISTS idx_project_interventions_project ON project_interventions(project_id, status);
CREATE INDEX IF NOT EXISTS idx_workflow_instances_project ON workflow_instances(project_id, status);
CREATE INDEX IF NOT EXISTS idx_ecosystem_events_project ON ecosystem_events(project_id, occurred_at, id);
CREATE INDEX IF NOT EXISTS idx_ecosystem_notifications_user ON ecosystem_notifications(user_id, status, created_at);
CREATE INDEX IF NOT EXISTS idx_reputation_metrics_subject ON reputation_metrics(subject_type, subject_id, computed_at);
"""

SQLITE_V8_SCRIPT = SQLITE_V8_TABLES_SCRIPT
