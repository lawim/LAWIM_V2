-- LAWIM_V2 schema v12 initial migration (generated from code/lawim_v2/schema_ddl.py; aligned with persistence manifest)

CREATE TABLE IF NOT EXISTS organizations (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        slug TEXT NOT NULL UNIQUE,
        kind TEXT NOT NULL DEFAULT 'agency',
        city TEXT,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        organization_id INTEGER REFERENCES organizations(id),
        password_salt TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL
    );

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
    );

CREATE TABLE IF NOT EXISTS media (
        id SERIAL PRIMARY KEY,
        property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
        kind TEXT NOT NULL,
        url TEXT NOT NULL,
        caption TEXT NOT NULL,
        storage_path TEXT,
        mime_type TEXT,
        size_bytes INTEGER,
        thumbnail_url TEXT,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        position INTEGER NOT NULL DEFAULT 0,
        version INTEGER NOT NULL DEFAULT 1,
        deleted_at TEXT,
        created_at TEXT NOT NULL
    );

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
    );

CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
        sender_user_id INTEGER NOT NULL REFERENCES users(id),
        body TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        kind TEXT NOT NULL,
        payload TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS notifications (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        kind TEXT NOT NULL,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        payload_json TEXT NOT NULL DEFAULT '{}',
        read_at TEXT,
        created_at TEXT NOT NULL
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
    );

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
    );

CREATE TABLE IF NOT EXISTS project_checklist_items (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        step_id INTEGER REFERENCES project_steps(id) ON DELETE CASCADE,
        label TEXT NOT NULL,
        checked INTEGER NOT NULL DEFAULT 0,
        position INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_step_history (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        step_id INTEGER NOT NULL REFERENCES project_steps(id) ON DELETE CASCADE,
        from_status TEXT,
        to_status TEXT NOT NULL,
        note TEXT,
        created_at TEXT NOT NULL
    );

CREATE INDEX IF NOT EXISTS idx_projects_user_status ON projects(user_id, status, created_at);

CREATE INDEX IF NOT EXISTS idx_projects_organization_status ON projects(organization_id, status, created_at);

CREATE INDEX IF NOT EXISTS idx_projects_created_at ON projects(created_at, id);

CREATE INDEX IF NOT EXISTS idx_project_steps_project_position ON project_steps(project_id, position);

CREATE INDEX IF NOT EXISTS idx_project_checklist_project ON project_checklist_items(project_id, step_id, position);

CREATE INDEX IF NOT EXISTS idx_project_step_history_project ON project_step_history(project_id, created_at, id);

CREATE TABLE IF NOT EXISTS journeys (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        journey_key TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'draft',
        replan_count INTEGER NOT NULL DEFAULT 0,
        started_at TEXT,
        completed_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (project_id, journey_key)
    );

CREATE TABLE IF NOT EXISTS project_goals (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        goal_key TEXT NOT NULL,
        title TEXT NOT NULL,
        priority TEXT NOT NULL DEFAULT 'normal',
        status TEXT NOT NULL DEFAULT 'active',
        influence_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_needs (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        need_key TEXT NOT NULL,
        description TEXT NOT NULL,
        priority TEXT NOT NULL DEFAULT 'normal',
        status TEXT NOT NULL DEFAULT 'open',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_constraints (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        constraint_type TEXT NOT NULL,
        description TEXT NOT NULL,
        severity TEXT NOT NULL DEFAULT 'medium',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_preferences (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        preference_key TEXT NOT NULL,
        value_json TEXT NOT NULL DEFAULT '{}',
        weight INTEGER NOT NULL DEFAULT 50,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_funding (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        source_type TEXT NOT NULL,
        amount INTEGER,
        currency TEXT NOT NULL DEFAULT 'XAF',
        status TEXT NOT NULL DEFAULT 'planned',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_life_events (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        event_type TEXT NOT NULL,
        title TEXT NOT NULL,
        impact_json TEXT NOT NULL DEFAULT '{}',
        occurred_at TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_risks (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        risk_key TEXT NOT NULL,
        severity TEXT NOT NULL DEFAULT 'medium',
        likelihood TEXT NOT NULL DEFAULT 'medium',
        description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'open',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_opportunities (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        opportunity_key TEXT NOT NULL,
        value_score INTEGER NOT NULL DEFAULT 50,
        description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'open',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_decisions (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        decision_key TEXT NOT NULL,
        title TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'proposed',
        reason TEXT NOT NULL,
        confidence INTEGER NOT NULL DEFAULT 50,
        alternatives_json TEXT NOT NULL DEFAULT '[]',
        tradeoffs_json TEXT NOT NULL DEFAULT '[]',
        next_action TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_recommendations (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        recommendation_key TEXT NOT NULL,
        title TEXT NOT NULL,
        priority TEXT NOT NULL DEFAULT 'normal',
        confidence INTEGER NOT NULL DEFAULT 50,
        score INTEGER NOT NULL DEFAULT 50,
        reasons_json TEXT NOT NULL DEFAULT '[]',
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_actions (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        action_key TEXT NOT NULL,
        title TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        priority TEXT NOT NULL DEFAULT 'normal',
        due_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_tasks (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        action_id INTEGER REFERENCES project_actions(id) ON DELETE SET NULL,
        title TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'todo',
        assignee_user_id INTEGER REFERENCES users(id),
        due_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_milestones (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        step_id INTEGER REFERENCES project_steps(id) ON DELETE SET NULL,
        title TEXT NOT NULL,
        target_at TEXT,
        achieved_at TEXT,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS knowledge_facts (
        id SERIAL PRIMARY KEY,
        project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        category TEXT NOT NULL,
        fact_key TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        source TEXT NOT NULL DEFAULT 'system',
        confidence INTEGER NOT NULL DEFAULT 70,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS user_contexts (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        context_json TEXT NOT NULL DEFAULT '{}',
        version INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_contexts (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        context_json TEXT NOT NULL DEFAULT '{}',
        version INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS partner_suggestions (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        partner_kind TEXT NOT NULL,
        title TEXT NOT NULL,
        rationale TEXT NOT NULL,
        priority TEXT NOT NULL DEFAULT 'normal',
        confidence INTEGER NOT NULL DEFAULT 50,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS service_suggestions (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        service_key TEXT NOT NULL,
        title TEXT NOT NULL,
        rationale TEXT NOT NULL,
        priority TEXT NOT NULL DEFAULT 'normal',
        confidence INTEGER NOT NULL DEFAULT 50,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS trust_scores (
        id SERIAL PRIMARY KEY,
        subject_type TEXT NOT NULL,
        subject_id INTEGER NOT NULL,
        score INTEGER NOT NULL DEFAULT 50,
        factors_json TEXT NOT NULL DEFAULT '[]',
        computed_at TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS timeline_entries (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        entry_type TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'planned',
        scheduled_at TEXT,
        occurred_at TEXT,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS progress_snapshots (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        progress_percent INTEGER NOT NULL DEFAULT 0,
        metrics_json TEXT NOT NULL DEFAULT '{}',
        captured_at TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS project_resources (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        resource_type TEXT NOT NULL,
        resource_id INTEGER NOT NULL,
        role TEXT NOT NULL DEFAULT 'linked',
        created_at TEXT NOT NULL,
        UNIQUE (project_id, resource_type, resource_id)
    );

CREATE INDEX IF NOT EXISTS idx_journeys_project ON journeys(project_id, status);

CREATE INDEX IF NOT EXISTS idx_project_goals_project ON project_goals(project_id, status);

CREATE INDEX IF NOT EXISTS idx_project_decisions_project ON project_decisions(project_id, status);

CREATE INDEX IF NOT EXISTS idx_project_recommendations_project ON project_recommendations(project_id, status);

CREATE INDEX IF NOT EXISTS idx_project_actions_project ON project_actions(project_id, status);

CREATE INDEX IF NOT EXISTS idx_knowledge_facts_project ON knowledge_facts(project_id, category);

CREATE INDEX IF NOT EXISTS idx_timeline_entries_project ON timeline_entries(project_id, scheduled_at, id);

CREATE INDEX IF NOT EXISTS idx_trust_scores_subject ON trust_scores(subject_type, subject_id);

CREATE INDEX IF NOT EXISTS idx_project_resources_project ON project_resources(project_id, resource_type);

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
    );

CREATE TABLE IF NOT EXISTS partner_zones (
        id SERIAL PRIMARY KEY,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        city TEXT,
        region TEXT,
        country TEXT NOT NULL DEFAULT 'Cameroon',
        radius_km REAL,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS partner_skills (
        id SERIAL PRIMARY KEY,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        skill_key TEXT NOT NULL,
        level TEXT NOT NULL DEFAULT 'standard',
        created_at TEXT NOT NULL,
        UNIQUE (partner_profile_id, skill_key)
    );

CREATE TABLE IF NOT EXISTS partner_certifications (
        id SERIAL PRIMARY KEY,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        certification_key TEXT NOT NULL,
        title TEXT NOT NULL,
        valid_until TEXT,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS partner_availability (
        id SERIAL PRIMARY KEY,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        status TEXT NOT NULL DEFAULT 'available',
        schedule_json TEXT NOT NULL DEFAULT '{}',
        updated_at TEXT NOT NULL,
        UNIQUE (partner_profile_id)
    );

CREATE TABLE IF NOT EXISTS partner_sla (
        id SERIAL PRIMARY KEY,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        response_hours REAL NOT NULL DEFAULT 24,
        completion_days INTEGER NOT NULL DEFAULT 14,
        uptime_percent REAL NOT NULL DEFAULT 95,
        created_at TEXT NOT NULL,
        UNIQUE (partner_profile_id)
    );

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
    );

CREATE TABLE IF NOT EXISTS service_catalog_partners (
        id SERIAL PRIMARY KEY,
        service_catalog_id INTEGER NOT NULL REFERENCES service_catalog(id) ON DELETE CASCADE,
        partner_profile_id INTEGER NOT NULL REFERENCES partner_profiles(id) ON DELETE CASCADE,
        priority INTEGER NOT NULL DEFAULT 50,
        created_at TEXT NOT NULL,
        UNIQUE (service_catalog_id, partner_profile_id)
    );

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
    );

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
    );

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
    );

CREATE TABLE IF NOT EXISTS workflows (
        id SERIAL PRIMARY KEY,
        workflow_key TEXT NOT NULL UNIQUE,
        workflow_type TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

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
    );

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
    );

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
    );

CREATE TABLE IF NOT EXISTS ecosystem_events (
        id SERIAL PRIMARY KEY,
        project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        event_type TEXT NOT NULL,
        title TEXT NOT NULL,
        payload_json TEXT NOT NULL DEFAULT '{}',
        occurred_at TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

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
    );

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
    );

CREATE TABLE IF NOT EXISTS project_ecosystem_state (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        orchestration_json TEXT NOT NULL DEFAULT '{}',
        last_matched_at TEXT,
        updated_at TEXT NOT NULL,
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

CREATE TABLE IF NOT EXISTS knowledge_nodes (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        node_key TEXT NOT NULL,
        node_type TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        entity_id INTEGER,
        title TEXT NOT NULL,
        content_json TEXT NOT NULL DEFAULT '{}',
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (project_id, node_key)
    );

CREATE TABLE IF NOT EXISTS knowledge_edges (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        source_node_id INTEGER NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
        target_node_id INTEGER NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
        edge_type TEXT NOT NULL,
        weight INTEGER NOT NULL DEFAULT 50,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        UNIQUE (project_id, source_node_id, target_node_id, edge_type)
    );

CREATE TABLE IF NOT EXISTS knowledge_relations (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        relation_key TEXT NOT NULL,
        subject_node_id INTEGER NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
        object_node_id INTEGER NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
        relation_type TEXT NOT NULL,
        confidence INTEGER NOT NULL DEFAULT 50,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        UNIQUE (project_id, relation_key)
    );

CREATE TABLE IF NOT EXISTS knowledge_snapshots (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        snapshot_key TEXT NOT NULL,
        graph_json TEXT NOT NULL DEFAULT '{}',
        node_count INTEGER NOT NULL DEFAULT 0,
        edge_count INTEGER NOT NULL DEFAULT 0,
        relation_count INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        UNIQUE (project_id, snapshot_key)
    );

CREATE TABLE IF NOT EXISTS knowledge_inferences (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        inference_key TEXT NOT NULL,
        premise_json TEXT NOT NULL DEFAULT '[]',
        conclusion TEXT NOT NULL,
        confidence INTEGER NOT NULL DEFAULT 50,
        rule_key TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE (project_id, inference_key)
    );

CREATE TABLE IF NOT EXISTS knowledge_history (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        node_id INTEGER REFERENCES knowledge_nodes(id) ON DELETE SET NULL,
        change_type TEXT NOT NULL,
        before_json TEXT NOT NULL DEFAULT '{}',
        after_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS cognition_decisions (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        decision_key TEXT NOT NULL,
        title TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'proposed',
        reason TEXT NOT NULL,
        confidence INTEGER NOT NULL DEFAULT 50,
        priority TEXT NOT NULL DEFAULT 'normal',
        alternatives_json TEXT NOT NULL DEFAULT '[]',
        tradeoffs_json TEXT NOT NULL DEFAULT '[]',
        explainability_json TEXT NOT NULL DEFAULT '{}',
        next_action TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (project_id, decision_key)
    );

CREATE TABLE IF NOT EXISTS decision_evidences (
        id SERIAL PRIMARY KEY,
        decision_id INTEGER NOT NULL REFERENCES cognition_decisions(id) ON DELETE CASCADE,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        evidence_key TEXT NOT NULL,
        label TEXT NOT NULL,
        source_type TEXT NOT NULL,
        source_id INTEGER,
        weight INTEGER NOT NULL DEFAULT 50,
        content_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS decision_histories (
        id SERIAL PRIMARY KEY,
        decision_id INTEGER NOT NULL REFERENCES cognition_decisions(id) ON DELETE CASCADE,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        from_status TEXT,
        to_status TEXT NOT NULL,
        note TEXT,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS simulation_runs (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        scenario_key TEXT NOT NULL,
        title TEXT NOT NULL,
        input_json TEXT NOT NULL DEFAULT '{}',
        output_json TEXT NOT NULL DEFAULT '{}',
        impacts_json TEXT NOT NULL DEFAULT '{}',
        status TEXT NOT NULL DEFAULT 'completed',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS reasoning_traces (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        trace_key TEXT NOT NULL,
        rules_fired_json TEXT NOT NULL DEFAULT '[]',
        conclusions_json TEXT NOT NULL DEFAULT '[]',
        merged_priority_json TEXT NOT NULL DEFAULT '[]',
        created_at TEXT NOT NULL,
        UNIQUE (project_id, trace_key)
    );

CREATE TABLE IF NOT EXISTS next_best_actions (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        action_key TEXT NOT NULL,
        title TEXT NOT NULL,
        score INTEGER NOT NULL DEFAULT 50,
        confidence INTEGER NOT NULL DEFAULT 50,
        justification TEXT NOT NULL,
        explanation_json TEXT NOT NULL DEFAULT '{}',
        factors_json TEXT NOT NULL DEFAULT '[]',
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE (project_id, action_key)
    );

CREATE TABLE IF NOT EXISTS risk_intelligence_scores (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        risk_key TEXT NOT NULL,
        severity TEXT NOT NULL DEFAULT 'medium',
        likelihood TEXT NOT NULL DEFAULT 'medium',
        score INTEGER NOT NULL DEFAULT 50,
        mitigation_json TEXT NOT NULL DEFAULT '[]',
        computed_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS opportunity_intelligence_scores (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        opportunity_key TEXT NOT NULL,
        value_score INTEGER NOT NULL DEFAULT 50,
        opportunity_score INTEGER NOT NULL DEFAULT 50,
        description TEXT NOT NULL,
        computed_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS intelligence_snapshots (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        snapshot_key TEXT NOT NULL,
        payload_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        UNIQUE (project_id, snapshot_key)
    );

CREATE INDEX IF NOT EXISTS idx_knowledge_nodes_project ON knowledge_nodes(project_id, node_type);

CREATE INDEX IF NOT EXISTS idx_knowledge_edges_project ON knowledge_edges(project_id, edge_type);

CREATE INDEX IF NOT EXISTS idx_cognition_decisions_project ON cognition_decisions(project_id, status);

CREATE INDEX IF NOT EXISTS idx_next_best_actions_project ON next_best_actions(project_id, status, score);

CREATE INDEX IF NOT EXISTS idx_simulation_runs_project ON simulation_runs(project_id, scenario_key);

CREATE INDEX IF NOT EXISTS idx_reasoning_traces_project ON reasoning_traces(project_id, created_at);

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
    );

CREATE TABLE IF NOT EXISTS assistant_prompt_versions (
        id SERIAL PRIMARY KEY,
        prompt_key TEXT NOT NULL,
        version TEXT NOT NULL,
        content TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        UNIQUE (prompt_key, version)
    );

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
    );

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
    );

CREATE TABLE IF NOT EXISTS assistant_context_snapshots (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        session_id INTEGER REFERENCES assistant_sessions(id) ON DELETE SET NULL,
        snapshot_key TEXT NOT NULL,
        context_json TEXT NOT NULL DEFAULT '{}',
        sources_json TEXT NOT NULL DEFAULT '[]',
        created_at TEXT NOT NULL,
        UNIQUE (project_id, snapshot_key)
    );

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
    );

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
    );

CREATE TABLE IF NOT EXISTS assistant_rag_retrievals (
        id SERIAL PRIMARY KEY,
        session_id INTEGER REFERENCES assistant_sessions(id) ON DELETE SET NULL,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        query_text TEXT NOT NULL,
        chunks_json TEXT NOT NULL DEFAULT '[]',
        score INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    );

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
    );

CREATE TABLE IF NOT EXISTS assistant_memory_summaries (
        id SERIAL PRIMARY KEY,
        session_id INTEGER NOT NULL REFERENCES assistant_sessions(id) ON DELETE CASCADE,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        summary_text TEXT NOT NULL,
        message_count INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS assistant_agent_assignments (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        session_id INTEGER REFERENCES assistant_sessions(id) ON DELETE SET NULL,
        agent_key TEXT NOT NULL,
        assigned_at TEXT NOT NULL,
        UNIQUE (project_id, session_id, agent_key)
    );

CREATE INDEX IF NOT EXISTS idx_assistant_sessions_project ON assistant_sessions(project_id, user_id, status);

CREATE INDEX IF NOT EXISTS idx_assistant_messages_session ON assistant_messages(session_id, created_at);

CREATE INDEX IF NOT EXISTS idx_assistant_rag_documents_project ON assistant_rag_documents(project_id, source_type);

CREATE INDEX IF NOT EXISTS idx_assistant_rag_chunks_project ON assistant_rag_chunks(project_id, document_id);

CREATE INDEX IF NOT EXISTS idx_assistant_turns_session ON assistant_turns(session_id, created_at);

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
    );

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
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_categories (
        id SERIAL PRIMARY KEY,
        category_key TEXT NOT NULL UNIQUE,
        domain TEXT NOT NULL,
        title TEXT NOT NULL,
        parent_key TEXT,
        description TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_tags (
        id SERIAL PRIMARY KEY,
        tag_key TEXT NOT NULL UNIQUE,
        label TEXT NOT NULL,
        domain TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

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
    );

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
    );

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
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_sections (
        id SERIAL PRIMARY KEY,
        article_id INTEGER NOT NULL REFERENCES expert_knowledge_articles(id) ON DELETE CASCADE,
        section_key TEXT NOT NULL,
        title TEXT NOT NULL,
        position INTEGER NOT NULL DEFAULT 0,
        content TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL,
        UNIQUE (article_id, section_key)
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_paragraphs (
        id SERIAL PRIMARY KEY,
        section_id INTEGER NOT NULL REFERENCES expert_knowledge_sections(id) ON DELETE CASCADE,
        paragraph_key TEXT NOT NULL,
        position INTEGER NOT NULL DEFAULT 0,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE (section_id, paragraph_key)
    );

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
    );

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
    );

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
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_references (
        id SERIAL PRIMARY KEY,
        from_document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        to_document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        reference_type TEXT NOT NULL DEFAULT 'references',
        label TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_embeddings (
        id SERIAL PRIMARY KEY,
        chunk_id INTEGER NOT NULL REFERENCES expert_knowledge_chunks(id) ON DELETE CASCADE,
        model_key TEXT NOT NULL DEFAULT 'lawim-deterministic-v1',
        vector_json TEXT NOT NULL DEFAULT '[]',
        dimensions INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        UNIQUE (chunk_id, model_key)
    );

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
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_relationships (
        id SERIAL PRIMARY KEY,
        subject_type TEXT NOT NULL,
        subject_id INTEGER NOT NULL,
        object_type TEXT NOT NULL,
        object_id INTEGER NOT NULL,
        relation_type TEXT NOT NULL,
        confidence INTEGER NOT NULL DEFAULT 50,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_feedback (
        id SERIAL PRIMARY KEY,
        article_id INTEGER NOT NULL REFERENCES expert_knowledge_articles(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        rating INTEGER NOT NULL DEFAULT 3,
        comment TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_reviews (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        reviewer_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        note TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_approvals (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        approver_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        note TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_publications (
        id SERIAL PRIMARY KEY,
        document_id INTEGER NOT NULL REFERENCES expert_knowledge_documents(id) ON DELETE CASCADE,
        publication_key TEXT NOT NULL UNIQUE,
        status TEXT NOT NULL DEFAULT 'draft',
        published_at TEXT,
        unpublished_at TEXT,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_imports (
        id SERIAL PRIMARY KEY,
        import_key TEXT NOT NULL UNIQUE,
        format TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'completed',
        source_filename TEXT,
        records_count INTEGER NOT NULL DEFAULT 0,
        error_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_exports (
        id SERIAL PRIMARY KEY,
        export_key TEXT NOT NULL UNIQUE,
        format TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'completed',
        destination TEXT NOT NULL DEFAULT '',
        records_count INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS expert_knowledge_snapshots (
        id SERIAL PRIMARY KEY,
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

CREATE TABLE IF NOT EXISTS automation_workflow_definitions (
            id SERIAL PRIMARY KEY,
            workflow_key TEXT NOT NULL UNIQUE,
            domain TEXT NOT NULL,
            process_key TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            version INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'draft',
            definition_json TEXT NOT NULL DEFAULT '{}',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_templates (
            id SERIAL PRIMARY KEY,
            template_key TEXT NOT NULL UNIQUE,
            workflow_key TEXT NOT NULL,
            title TEXT NOT NULL,
            domain TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            steps_json TEXT NOT NULL DEFAULT '[]',
            variables_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_process_instances (
            id SERIAL PRIMARY KEY,
            instance_key TEXT NOT NULL UNIQUE,
            workflow_key TEXT NOT NULL,
            project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
            current_state_key TEXT NOT NULL DEFAULT 'start',
            status TEXT NOT NULL DEFAULT 'pending',
            context_json TEXT NOT NULL DEFAULT '{}',
            priority TEXT NOT NULL DEFAULT 'normal',
            started_at TEXT,
            completed_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_executions (
            id SERIAL PRIMARY KEY,
            execution_key TEXT NOT NULL UNIQUE,
            instance_id INTEGER NOT NULL REFERENCES automation_process_instances(id) ON DELETE CASCADE,
            workflow_key TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            current_step_key TEXT,
            attempt INTEGER NOT NULL DEFAULT 1,
            error_message TEXT,
            context_json TEXT NOT NULL DEFAULT '{}',
            started_at TEXT,
            finished_at TEXT,
            duration_ms INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_states (
            id SERIAL PRIMARY KEY,
            workflow_key TEXT NOT NULL,
            state_key TEXT NOT NULL,
            title TEXT NOT NULL,
            state_type TEXT NOT NULL DEFAULT 'task',
            is_terminal INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (workflow_key, state_key)
        );

CREATE TABLE IF NOT EXISTS automation_transitions (
            id SERIAL PRIMARY KEY,
            workflow_key TEXT NOT NULL,
            transition_key TEXT NOT NULL,
            from_state_key TEXT NOT NULL,
            to_state_key TEXT NOT NULL,
            condition_json TEXT NOT NULL DEFAULT '{}',
            priority INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            UNIQUE (workflow_key, transition_key)
        );

CREATE TABLE IF NOT EXISTS automation_tasks (
            id SERIAL PRIMARY KEY,
            task_key TEXT NOT NULL UNIQUE,
            instance_id INTEGER NOT NULL REFERENCES automation_process_instances(id) ON DELETE CASCADE,
            execution_id INTEGER REFERENCES automation_executions(id) ON DELETE SET NULL,
            title TEXT NOT NULL,
            task_type TEXT NOT NULL DEFAULT 'human',
            status TEXT NOT NULL DEFAULT 'pending',
            assignee_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            priority TEXT NOT NULL DEFAULT 'normal',
            due_at TEXT,
            payload_json TEXT NOT NULL DEFAULT '{}',
            result_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            completed_at TEXT
        );

CREATE TABLE IF NOT EXISTS automation_queues (
            id SERIAL PRIMARY KEY,
            queue_key TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            domain TEXT NOT NULL DEFAULT 'general',
            status TEXT NOT NULL DEFAULT 'active',
            capacity INTEGER NOT NULL DEFAULT 500,
            depth INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_queue_items (
            id SERIAL PRIMARY KEY,
            queue_key TEXT NOT NULL REFERENCES automation_queues(queue_key) ON DELETE CASCADE,
            item_key TEXT NOT NULL UNIQUE,
            priority TEXT NOT NULL DEFAULT 'normal',
            status TEXT NOT NULL DEFAULT 'queued',
            payload_json TEXT NOT NULL DEFAULT '{}',
            attempts INTEGER NOT NULL DEFAULT 0,
            scheduled_at TEXT,
            processed_at TEXT,
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_events (
            id SERIAL PRIMARY KEY,
            event_key TEXT NOT NULL UNIQUE,
            instance_id INTEGER REFERENCES automation_process_instances(id) ON DELETE SET NULL,
            event_type TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'engine',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_schedules (
            id SERIAL PRIMARY KEY,
            schedule_key TEXT NOT NULL UNIQUE,
            workflow_key TEXT NOT NULL,
            cron_expr TEXT NOT NULL DEFAULT '@daily',
            status TEXT NOT NULL DEFAULT 'active',
            next_run_at TEXT,
            last_run_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_timers (
            id SERIAL PRIMARY KEY,
            timer_key TEXT NOT NULL UNIQUE,
            instance_id INTEGER NOT NULL REFERENCES automation_process_instances(id) ON DELETE CASCADE,
            fire_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            action_json TEXT NOT NULL DEFAULT '{}',
            fired_at TEXT,
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_retries (
            id SERIAL PRIMARY KEY,
            execution_id INTEGER NOT NULL REFERENCES automation_executions(id) ON DELETE CASCADE,
            attempt INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'pending',
            backoff_seconds INTEGER NOT NULL DEFAULT 60,
            error_message TEXT,
            scheduled_at TEXT NOT NULL,
            executed_at TEXT,
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_escalations (
            id SERIAL PRIMARY KEY,
            escalation_key TEXT NOT NULL UNIQUE,
            instance_id INTEGER NOT NULL REFERENCES automation_process_instances(id) ON DELETE CASCADE,
            task_id INTEGER REFERENCES automation_tasks(id) ON DELETE SET NULL,
            level INTEGER NOT NULL DEFAULT 1,
            reason TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'open',
            escalated_to_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            created_at TEXT NOT NULL,
            resolved_at TEXT
        );

CREATE TABLE IF NOT EXISTS automation_approvals (
            id SERIAL PRIMARY KEY,
            approval_key TEXT NOT NULL UNIQUE,
            instance_id INTEGER NOT NULL REFERENCES automation_process_instances(id) ON DELETE CASCADE,
            level INTEGER NOT NULL DEFAULT 1,
            approver_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            note TEXT NOT NULL DEFAULT '',
            decided_at TEXT,
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_rules (
            id SERIAL PRIMARY KEY,
            rule_key TEXT NOT NULL UNIQUE,
            workflow_key TEXT,
            title TEXT NOT NULL,
            domain TEXT NOT NULL DEFAULT 'general',
            expression TEXT NOT NULL DEFAULT '',
            action_json TEXT NOT NULL DEFAULT '{}',
            priority INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_rule_bindings (
            id SERIAL PRIMARY KEY,
            rule_key TEXT NOT NULL REFERENCES automation_rules(rule_key) ON DELETE CASCADE,
            variable_key TEXT NOT NULL,
            binding_type TEXT NOT NULL DEFAULT 'context',
            default_value TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            UNIQUE (rule_key, variable_key)
        );

CREATE TABLE IF NOT EXISTS automation_notifications (
            id SERIAL PRIMARY KEY,
            notification_key TEXT NOT NULL UNIQUE,
            instance_id INTEGER REFERENCES automation_process_instances(id) ON DELETE SET NULL,
            channel TEXT NOT NULL DEFAULT 'in_app',
            recipient_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            sent_at TEXT,
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_audit_log (
            id SERIAL PRIMARY KEY,
            audit_key TEXT NOT NULL UNIQUE,
            actor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            action TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            resource_id INTEGER,
            detail_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_history (
            id SERIAL PRIMARY KEY,
            instance_id INTEGER NOT NULL REFERENCES automation_process_instances(id) ON DELETE CASCADE,
            from_state_key TEXT,
            to_state_key TEXT NOT NULL,
            transition_key TEXT,
            actor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            note TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_sla_policies (
            id SERIAL PRIMARY KEY,
            policy_key TEXT NOT NULL UNIQUE,
            workflow_key TEXT NOT NULL,
            step_key TEXT,
            target_hours INTEGER NOT NULL DEFAULT 48,
            escalation_level INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS automation_metrics_snapshots (
            id SERIAL PRIMARY KEY,
            snapshot_key TEXT NOT NULL UNIQUE,
            scope TEXT NOT NULL DEFAULT 'global',
            metrics_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE INDEX IF NOT EXISTS idx_automation_instances_project ON automation_process_instances(project_id, status);

CREATE INDEX IF NOT EXISTS idx_automation_executions_instance ON automation_executions(instance_id, status);

CREATE INDEX IF NOT EXISTS idx_automation_tasks_instance ON automation_tasks(instance_id, status);

CREATE INDEX IF NOT EXISTS idx_automation_queue_items_queue ON automation_queue_items(queue_key, status, priority);

CREATE INDEX IF NOT EXISTS idx_automation_events_instance ON automation_events(instance_id, event_type);

CREATE INDEX IF NOT EXISTS idx_automation_history_instance ON automation_history(instance_id, created_at);

CREATE INDEX IF NOT EXISTS idx_automation_workflows_domain ON automation_workflow_definitions(domain, status);
