"""Schema v14 DDL — CRM platform (RELEASE PROGRAM H)."""

V14_TABLE_NAMES: tuple[str, ...] = (
    "crm_contact_profiles",
    "crm_contact_tags",
    "crm_contact_consents",
    "crm_leads",
    "crm_lead_sources",
    "crm_customers",
    "crm_customer_roles",
    "crm_opportunities",
    "crm_pipelines",
    "crm_pipeline_stages",
    "crm_pipeline_items",
    "crm_journey_events",
    "crm_timeline_entries",
    "crm_communications",
    "crm_whatsapp_messages",
    "crm_telegram_messages",
    "crm_email_messages",
    "crm_sms_messages",
    "crm_reminders",
    "crm_followups",
    "crm_campaigns",
    "crm_campaign_targets",
    "crm_segments",
    "crm_segment_members",
    "crm_customer_scores",
    "crm_satisfaction_surveys",
    "crm_satisfaction_responses",
    "crm_notes",
    "crm_documents",
    "crm_ai_suggestions",
    "crm_analytics_snapshots",
)

SQLITE_V14_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS crm_contact_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_key TEXT NOT NULL UNIQUE,
    contact_type TEXT NOT NULL DEFAULT 'individual',
    full_name TEXT NOT NULL,
    email TEXT NOT NULL DEFAULT '',
    phone TEXT NOT NULL DEFAULT '',
    whatsapp TEXT NOT NULL DEFAULT '',
    telegram TEXT NOT NULL DEFAULT '',
    company TEXT NOT NULL DEFAULT '',
    country TEXT NOT NULL DEFAULT 'Cameroon',
    user_id INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS crm_contact_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
    UNIQUE (contact_id, tag)
);

CREATE TABLE IF NOT EXISTS crm_contact_consents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    consent_type TEXT NOT NULL DEFAULT 'marketing',
    granted INTEGER NOT NULL DEFAULT 0,
    granted_at TEXT,
    revoked_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
    UNIQUE (contact_id, consent_type)
);

CREATE TABLE IF NOT EXISTS crm_lead_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_key TEXT NOT NULL UNIQUE,
    reference_code TEXT NOT NULL DEFAULT '' UNIQUE,
    name TEXT NOT NULL,
    channel TEXT NOT NULL DEFAULT 'web',
    target TEXT NOT NULL DEFAULT 'acquisition',
    status TEXT NOT NULL DEFAULT 'active',
    created_by INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_crm_lead_sources_reference_code ON crm_lead_sources(reference_code);
CREATE INDEX IF NOT EXISTS idx_crm_lead_sources_status ON crm_lead_sources(status, created_at);

CREATE TABLE IF NOT EXISTS crm_leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_key TEXT NOT NULL UNIQUE,
    contact_id INTEGER NOT NULL,
    source_id INTEGER,
    status TEXT NOT NULL DEFAULT 'new',
    score INTEGER NOT NULL DEFAULT 0,
    title TEXT NOT NULL DEFAULT '',
    notes TEXT NOT NULL DEFAULT '',
    assigned_user_id INTEGER,
    converted_customer_id INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES crm_lead_sources(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS crm_customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_key TEXT NOT NULL UNIQUE,
    contact_id INTEGER NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    lifetime_value INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crm_customer_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    role TEXT NOT NULL DEFAULT 'buyer',
    assigned_at TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES crm_customers(id) ON DELETE CASCADE,
    UNIQUE (customer_id, role)
);

CREATE TABLE IF NOT EXISTS crm_pipelines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    is_default INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_pipeline_stages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_id INTEGER NOT NULL,
    stage_key TEXT NOT NULL,
    label TEXT NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (pipeline_id) REFERENCES crm_pipelines(id) ON DELETE CASCADE,
    UNIQUE (pipeline_id, stage_key)
);

CREATE TABLE IF NOT EXISTS crm_pipeline_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_id INTEGER NOT NULL,
    stage_id INTEGER NOT NULL,
    entity_type TEXT NOT NULL DEFAULT 'lead',
    entity_id INTEGER NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    entered_at TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (pipeline_id) REFERENCES crm_pipelines(id) ON DELETE CASCADE,
    FOREIGN KEY (stage_id) REFERENCES crm_pipeline_stages(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crm_opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_key TEXT NOT NULL UNIQUE,
    customer_id INTEGER,
    contact_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    amount INTEGER,
    currency TEXT NOT NULL DEFAULT 'XAF',
    probability INTEGER NOT NULL DEFAULT 50,
    pipeline_item_id INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    closed_at TEXT,
    FOREIGN KEY (customer_id) REFERENCES crm_customers(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (pipeline_item_id) REFERENCES crm_pipeline_items(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS crm_journey_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    event_key TEXT NOT NULL,
    summary TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    actor_id INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (contact_id, event_key)
);

CREATE TABLE IF NOT EXISTS crm_timeline_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    entry_type TEXT NOT NULL,
    summary TEXT NOT NULL DEFAULT '',
    reference_type TEXT,
    reference_id INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crm_communications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    communication_key TEXT NOT NULL UNIQUE,
    contact_id INTEGER NOT NULL,
    channel TEXT NOT NULL DEFAULT 'email',
    direction TEXT NOT NULL DEFAULT 'outbound',
    status TEXT NOT NULL DEFAULT 'pending',
    subject TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    sender_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    sent_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crm_whatsapp_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    communication_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    from_number TEXT NOT NULL DEFAULT '',
    to_number TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    lawim_sender_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    sent_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (communication_id) REFERENCES crm_communications(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crm_telegram_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    communication_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    from_handle TEXT NOT NULL DEFAULT '',
    to_handle TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    lawim_sender_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    sent_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (communication_id) REFERENCES crm_communications(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crm_email_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    communication_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    from_email TEXT NOT NULL DEFAULT '',
    to_email TEXT NOT NULL DEFAULT '',
    subject TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    lawim_sender_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    sent_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (communication_id) REFERENCES crm_communications(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crm_sms_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    communication_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    from_number TEXT NOT NULL DEFAULT '',
    to_number TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    lawim_sender_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    sent_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (communication_id) REFERENCES crm_communications(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crm_reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reminder_key TEXT NOT NULL UNIQUE,
    contact_id INTEGER NOT NULL,
    assigned_user_id INTEGER,
    title TEXT NOT NULL,
    due_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    completed_at TEXT,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS crm_followups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    followup_key TEXT NOT NULL UNIQUE,
    contact_id INTEGER NOT NULL,
    lead_id INTEGER,
    opportunity_id INTEGER,
    channel TEXT NOT NULL DEFAULT 'whatsapp',
    scheduled_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled',
    notes TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    completed_at TEXT,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (lead_id) REFERENCES crm_leads(id) ON DELETE SET NULL,
    FOREIGN KEY (opportunity_id) REFERENCES crm_opportunities(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS crm_campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    channel TEXT NOT NULL DEFAULT 'email',
    status TEXT NOT NULL DEFAULT 'draft',
    audience_json TEXT NOT NULL DEFAULT '{}',
    content_json TEXT NOT NULL DEFAULT '{}',
    scheduled_at TEXT,
    started_at TEXT,
    completed_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_campaign_targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    sent_at TEXT,
    response_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (campaign_id) REFERENCES crm_campaigns(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
    UNIQUE (campaign_id, contact_id)
);

CREATE TABLE IF NOT EXISTS crm_segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    segment_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    criteria_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_segment_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    segment_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    added_at TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (segment_id) REFERENCES crm_segments(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
    UNIQUE (segment_id, contact_id)
);

CREATE TABLE IF NOT EXISTS crm_customer_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    score_key TEXT NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    factors_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
    UNIQUE (contact_id, score_key)
);

CREATE TABLE IF NOT EXISTS crm_satisfaction_surveys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    survey_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    survey_type TEXT NOT NULL DEFAULT 'csat',
    questions_json TEXT NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'draft',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_satisfaction_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    survey_id INTEGER NOT NULL,
    contact_id INTEGER NOT NULL,
    rating INTEGER NOT NULL DEFAULT 3,
    answers_json TEXT NOT NULL DEFAULT '{}',
    submitted_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (survey_id) REFERENCES crm_satisfaction_surveys(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crm_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_key TEXT NOT NULL UNIQUE,
    contact_id INTEGER NOT NULL,
    author_id INTEGER,
    content TEXT NOT NULL,
    visibility TEXT NOT NULL DEFAULT 'internal',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS crm_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_key TEXT NOT NULL UNIQUE,
    contact_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    document_type TEXT NOT NULL DEFAULT 'other',
    storage_ref TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crm_ai_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    suggestion_key TEXT NOT NULL UNIQUE,
    contact_id INTEGER,
    suggestion_type TEXT NOT NULL DEFAULT 'followup',
    title TEXT NOT NULL,
    rationale TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'pending',
    sources_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS crm_analytics_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_key TEXT NOT NULL UNIQUE,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_crm_leads_status ON crm_leads(status, score);
CREATE INDEX IF NOT EXISTS idx_crm_leads_contact ON crm_leads(contact_id);
CREATE INDEX IF NOT EXISTS idx_crm_customers_status ON crm_customers(status);
CREATE INDEX IF NOT EXISTS idx_crm_opportunities_status ON crm_opportunities(status, amount);
CREATE INDEX IF NOT EXISTS idx_crm_pipeline_items_stage ON crm_pipeline_items(stage_id, position);
CREATE INDEX IF NOT EXISTS idx_crm_communications_contact ON crm_communications(contact_id, channel);
CREATE INDEX IF NOT EXISTS idx_crm_timeline_contact ON crm_timeline_entries(contact_id, created_at);
CREATE INDEX IF NOT EXISTS idx_crm_journey_contact ON crm_journey_events(contact_id, created_at);
CREATE INDEX IF NOT EXISTS idx_crm_campaign_targets_campaign ON crm_campaign_targets(campaign_id, status);
CREATE INDEX IF NOT EXISTS idx_crm_customer_scores_contact ON crm_customer_scores(contact_id, score_key);
CREATE INDEX IF NOT EXISTS idx_crm_followups_scheduled ON crm_followups(scheduled_at, status);
"""

POSTGRESQL_V14_STATEMENTS: tuple[str, ...] = tuple(
    stmt.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
    for stmt in (
        """
        CREATE TABLE IF NOT EXISTS crm_contact_profiles (
            id SERIAL PRIMARY KEY,
            contact_key TEXT NOT NULL UNIQUE,
            contact_type TEXT NOT NULL DEFAULT 'individual',
            full_name TEXT NOT NULL,
            email TEXT NOT NULL DEFAULT '',
            phone TEXT NOT NULL DEFAULT '',
            whatsapp TEXT NOT NULL DEFAULT '',
            telegram TEXT NOT NULL DEFAULT '',
            company TEXT NOT NULL DEFAULT '',
            country TEXT NOT NULL DEFAULT 'Cameroon',
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_contact_tags (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            tag TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE (contact_id, tag)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_contact_consents (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            consent_type TEXT NOT NULL DEFAULT 'marketing',
            granted INTEGER NOT NULL DEFAULT 0,
            granted_at TEXT,
            revoked_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (contact_id, consent_type)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_lead_sources (
            id SERIAL PRIMARY KEY,
            source_key TEXT NOT NULL UNIQUE,
            reference_code TEXT NOT NULL DEFAULT '' UNIQUE,
            name TEXT NOT NULL,
            channel TEXT NOT NULL DEFAULT 'web',
            target TEXT NOT NULL DEFAULT 'acquisition',
            status TEXT NOT NULL DEFAULT 'active',
            created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        "CREATE INDEX IF NOT EXISTS idx_crm_lead_sources_reference_code ON crm_lead_sources(reference_code)",
        "CREATE INDEX IF NOT EXISTS idx_crm_lead_sources_status ON crm_lead_sources(status, created_at)",
        """
        CREATE TABLE IF NOT EXISTS crm_leads (
            id SERIAL PRIMARY KEY,
            lead_key TEXT NOT NULL UNIQUE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            source_id INTEGER REFERENCES crm_lead_sources(id) ON DELETE SET NULL,
            status TEXT NOT NULL DEFAULT 'new',
            score INTEGER NOT NULL DEFAULT 0,
            title TEXT NOT NULL DEFAULT '',
            notes TEXT NOT NULL DEFAULT '',
            assigned_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            converted_customer_id INTEGER,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_customers (
            id SERIAL PRIMARY KEY,
            customer_key TEXT NOT NULL UNIQUE,
            contact_id INTEGER NOT NULL UNIQUE REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            status TEXT NOT NULL DEFAULT 'active',
            lifetime_value INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_customer_roles (
            id SERIAL PRIMARY KEY,
            customer_id INTEGER NOT NULL REFERENCES crm_customers(id) ON DELETE CASCADE,
            role TEXT NOT NULL DEFAULT 'buyer',
            assigned_at TEXT NOT NULL,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (customer_id, role)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_pipelines (
            id SERIAL PRIMARY KEY,
            pipeline_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            is_default INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_pipeline_stages (
            id SERIAL PRIMARY KEY,
            pipeline_id INTEGER NOT NULL REFERENCES crm_pipelines(id) ON DELETE CASCADE,
            stage_key TEXT NOT NULL,
            label TEXT NOT NULL,
            position INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (pipeline_id, stage_key)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_pipeline_items (
            id SERIAL PRIMARY KEY,
            pipeline_id INTEGER NOT NULL REFERENCES crm_pipelines(id) ON DELETE CASCADE,
            stage_id INTEGER NOT NULL REFERENCES crm_pipeline_stages(id) ON DELETE CASCADE,
            entity_type TEXT NOT NULL DEFAULT 'lead',
            entity_id INTEGER NOT NULL,
            position INTEGER NOT NULL DEFAULT 0,
            entered_at TEXT NOT NULL,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_opportunities (
            id SERIAL PRIMARY KEY,
            opportunity_key TEXT NOT NULL UNIQUE,
            customer_id INTEGER REFERENCES crm_customers(id) ON DELETE SET NULL,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            amount INTEGER,
            currency TEXT NOT NULL DEFAULT 'XAF',
            probability INTEGER NOT NULL DEFAULT 50,
            pipeline_item_id INTEGER REFERENCES crm_pipeline_items(id) ON DELETE SET NULL,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            closed_at TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_journey_events (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            event_type TEXT NOT NULL,
            event_key TEXT NOT NULL,
            summary TEXT NOT NULL DEFAULT '',
            payload_json TEXT NOT NULL DEFAULT '{}',
            actor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            created_at TEXT NOT NULL,
            UNIQUE (contact_id, event_key)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_timeline_entries (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            entry_type TEXT NOT NULL,
            summary TEXT NOT NULL DEFAULT '',
            reference_type TEXT,
            reference_id INTEGER,
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_communications (
            id SERIAL PRIMARY KEY,
            communication_key TEXT NOT NULL UNIQUE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            channel TEXT NOT NULL DEFAULT 'email',
            direction TEXT NOT NULL DEFAULT 'outbound',
            status TEXT NOT NULL DEFAULT 'pending',
            subject TEXT NOT NULL DEFAULT '',
            body TEXT NOT NULL DEFAULT '',
            sender_json TEXT NOT NULL DEFAULT '{}',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            sent_at TEXT,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_whatsapp_messages (
            id SERIAL PRIMARY KEY,
            communication_id INTEGER NOT NULL REFERENCES crm_communications(id) ON DELETE CASCADE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            from_number TEXT NOT NULL DEFAULT '',
            to_number TEXT NOT NULL DEFAULT '',
            body TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            lawim_sender_json TEXT NOT NULL DEFAULT '{}',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            sent_at TEXT,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_telegram_messages (
            id SERIAL PRIMARY KEY,
            communication_id INTEGER NOT NULL REFERENCES crm_communications(id) ON DELETE CASCADE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            from_handle TEXT NOT NULL DEFAULT '',
            to_handle TEXT NOT NULL DEFAULT '',
            body TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            lawim_sender_json TEXT NOT NULL DEFAULT '{}',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            sent_at TEXT,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_email_messages (
            id SERIAL PRIMARY KEY,
            communication_id INTEGER NOT NULL REFERENCES crm_communications(id) ON DELETE CASCADE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            from_email TEXT NOT NULL DEFAULT '',
            to_email TEXT NOT NULL DEFAULT '',
            subject TEXT NOT NULL DEFAULT '',
            body TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            lawim_sender_json TEXT NOT NULL DEFAULT '{}',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            sent_at TEXT,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_sms_messages (
            id SERIAL PRIMARY KEY,
            communication_id INTEGER NOT NULL REFERENCES crm_communications(id) ON DELETE CASCADE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            from_number TEXT NOT NULL DEFAULT '',
            to_number TEXT NOT NULL DEFAULT '',
            body TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            lawim_sender_json TEXT NOT NULL DEFAULT '{}',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            sent_at TEXT,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_reminders (
            id SERIAL PRIMARY KEY,
            reminder_key TEXT NOT NULL UNIQUE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            assigned_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            title TEXT NOT NULL,
            due_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_followups (
            id SERIAL PRIMARY KEY,
            followup_key TEXT NOT NULL UNIQUE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            lead_id INTEGER REFERENCES crm_leads(id) ON DELETE SET NULL,
            opportunity_id INTEGER REFERENCES crm_opportunities(id) ON DELETE SET NULL,
            channel TEXT NOT NULL DEFAULT 'whatsapp',
            scheduled_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'scheduled',
            notes TEXT NOT NULL DEFAULT '',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_campaigns (
            id SERIAL PRIMARY KEY,
            campaign_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            channel TEXT NOT NULL DEFAULT 'email',
            status TEXT NOT NULL DEFAULT 'draft',
            audience_json TEXT NOT NULL DEFAULT '{}',
            content_json TEXT NOT NULL DEFAULT '{}',
            scheduled_at TEXT,
            started_at TEXT,
            completed_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_campaign_targets (
            id SERIAL PRIMARY KEY,
            campaign_id INTEGER NOT NULL REFERENCES crm_campaigns(id) ON DELETE CASCADE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            status TEXT NOT NULL DEFAULT 'pending',
            sent_at TEXT,
            response_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (campaign_id, contact_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_segments (
            id SERIAL PRIMARY KEY,
            segment_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            criteria_json TEXT NOT NULL DEFAULT '{}',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_segment_members (
            id SERIAL PRIMARY KEY,
            segment_id INTEGER NOT NULL REFERENCES crm_segments(id) ON DELETE CASCADE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            added_at TEXT NOT NULL,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            UNIQUE (segment_id, contact_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_customer_scores (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            score_key TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 0,
            factors_json TEXT NOT NULL DEFAULT '{}',
            computed_at TEXT NOT NULL,
            UNIQUE (contact_id, score_key)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_satisfaction_surveys (
            id SERIAL PRIMARY KEY,
            survey_key TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            survey_type TEXT NOT NULL DEFAULT 'csat',
            questions_json TEXT NOT NULL DEFAULT '[]',
            status TEXT NOT NULL DEFAULT 'draft',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_satisfaction_responses (
            id SERIAL PRIMARY KEY,
            survey_id INTEGER NOT NULL REFERENCES crm_satisfaction_surveys(id) ON DELETE CASCADE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            rating INTEGER NOT NULL DEFAULT 3,
            answers_json TEXT NOT NULL DEFAULT '{}',
            submitted_at TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_notes (
            id SERIAL PRIMARY KEY,
            note_key TEXT NOT NULL UNIQUE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            author_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            content TEXT NOT NULL,
            visibility TEXT NOT NULL DEFAULT 'internal',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_documents (
            id SERIAL PRIMARY KEY,
            document_key TEXT NOT NULL UNIQUE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            document_type TEXT NOT NULL DEFAULT 'other',
            storage_ref TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_ai_suggestions (
            id SERIAL PRIMARY KEY,
            suggestion_key TEXT NOT NULL UNIQUE,
            contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL,
            suggestion_type TEXT NOT NULL DEFAULT 'followup',
            title TEXT NOT NULL,
            rationale TEXT NOT NULL DEFAULT '',
            payload_json TEXT NOT NULL DEFAULT '{}',
            status TEXT NOT NULL DEFAULT 'pending',
            sources_json TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crm_analytics_snapshots (
            id SERIAL PRIMARY KEY,
            snapshot_key TEXT NOT NULL UNIQUE,
            scope TEXT NOT NULL DEFAULT 'global',
            metrics_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        "CREATE INDEX IF NOT EXISTS idx_crm_leads_status ON crm_leads(status, score)",
        "CREATE INDEX IF NOT EXISTS idx_crm_leads_contact ON crm_leads(contact_id)",
        "CREATE INDEX IF NOT EXISTS idx_crm_customers_status ON crm_customers(status)",
        "CREATE INDEX IF NOT EXISTS idx_crm_opportunities_status ON crm_opportunities(status, amount)",
        "CREATE INDEX IF NOT EXISTS idx_crm_pipeline_items_stage ON crm_pipeline_items(stage_id, position)",
        "CREATE INDEX IF NOT EXISTS idx_crm_communications_contact ON crm_communications(contact_id, channel)",
        "CREATE INDEX IF NOT EXISTS idx_crm_timeline_contact ON crm_timeline_entries(contact_id, created_at)",
        "CREATE INDEX IF NOT EXISTS idx_crm_journey_contact ON crm_journey_events(contact_id, created_at)",
        "CREATE INDEX IF NOT EXISTS idx_crm_campaign_targets_campaign ON crm_campaign_targets(campaign_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_crm_customer_scores_contact ON crm_customer_scores(contact_id, score_key)",
        "CREATE INDEX IF NOT EXISTS idx_crm_followups_scheduled ON crm_followups(scheduled_at, status)",
    )
)
