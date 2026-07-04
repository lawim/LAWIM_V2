-- LAWIM_V2 schema v18 initial migration (generated from code/lawim_v2/schema_ddl.py; aligned with persistence manifest)

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
        );

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
        );

CREATE TABLE IF NOT EXISTS rei_listing_publications (
            id SERIAL PRIMARY KEY,
            listing_id INTEGER NOT NULL REFERENCES rei_listings(id) ON DELETE CASCADE,
            channel TEXT NOT NULL DEFAULT 'lawim',
            status TEXT NOT NULL DEFAULT 'published',
            published_at TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS rei_listing_scores (
            id SERIAL PRIMARY KEY,
            listing_id INTEGER NOT NULL REFERENCES rei_listings(id) ON DELETE CASCADE,
            score_type TEXT NOT NULL DEFAULT 'visibility',
            score INTEGER NOT NULL DEFAULT 0,
            factors_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (listing_id, score_type)
        );

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
        );

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
        );

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
        );

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
        );

CREATE TABLE IF NOT EXISTS rei_verification_scores (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL UNIQUE REFERENCES properties(id) ON DELETE CASCADE,
            trust_score INTEGER NOT NULL DEFAULT 0,
            consistency_score INTEGER NOT NULL DEFAULT 0,
            details_json TEXT NOT NULL DEFAULT '{}',
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS rei_matching_sessions (
            id SERIAL PRIMARY KEY,
            session_key TEXT NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
            criteria_json TEXT NOT NULL DEFAULT '{}',
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS rei_matching_results (
            id SERIAL PRIMARY KEY,
            session_id INTEGER NOT NULL REFERENCES rei_matching_sessions(id) ON DELETE CASCADE,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            score INTEGER NOT NULL DEFAULT 0,
            reasons_json TEXT NOT NULL DEFAULT '[]',
            rank_position INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );

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
        );

CREATE TABLE IF NOT EXISTS rei_visit_reports (
            id SERIAL PRIMARY KEY,
            visit_id INTEGER NOT NULL UNIQUE REFERENCES rei_visits(id) ON DELETE CASCADE,
            summary TEXT NOT NULL DEFAULT '',
            rating INTEGER NOT NULL DEFAULT 3,
            signed INTEGER NOT NULL DEFAULT 0,
            report_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

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
        );

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
        );

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
        );

CREATE TABLE IF NOT EXISTS rei_reservations (
            id SERIAL PRIMARY KEY,
            reservation_key TEXT NOT NULL UNIQUE,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            reserved_until TEXT NOT NULL,
            amount INTEGER,
            created_at TEXT NOT NULL
        );

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
        );

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
        );

CREATE TABLE IF NOT EXISTS rei_intelligence_scores (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            score_key TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 0,
            factors_json TEXT NOT NULL DEFAULT '{}',
            computed_at TEXT NOT NULL,
            UNIQUE (property_id, score_key)
        );

CREATE TABLE IF NOT EXISTS rei_analytics_snapshots (
            id SERIAL PRIMARY KEY,
            snapshot_key TEXT NOT NULL UNIQUE,
            scope TEXT NOT NULL DEFAULT 'global',
            metrics_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS rei_search_index (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL UNIQUE REFERENCES properties(id) ON DELETE CASCADE,
            index_text TEXT NOT NULL DEFAULT '',
            geo_hash TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS rei_nearby_properties (
            id SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            nearby_property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            distance_km REAL NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            UNIQUE (property_id, nearby_property_id)
        );

CREATE TABLE IF NOT EXISTS rei_property_reports (
            id SERIAL PRIMARY KEY,
            report_key TEXT NOT NULL UNIQUE,
            property_id INTEGER NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
            report_type TEXT NOT NULL DEFAULT 'summary',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE INDEX IF NOT EXISTS idx_rei_listings_property ON rei_listings(property_id, status);

CREATE INDEX IF NOT EXISTS idx_rei_visits_property ON rei_visits(property_id, scheduled_at);

CREATE INDEX IF NOT EXISTS idx_rei_transactions_property ON rei_transactions(property_id, status);

CREATE INDEX IF NOT EXISTS idx_rei_matching_results_session ON rei_matching_results(session_id, score);

CREATE INDEX IF NOT EXISTS idx_rei_recommendations_user ON rei_recommendations(user_id, recommendation_type);

CREATE INDEX IF NOT EXISTS idx_rei_intelligence_scores_property ON rei_intelligence_scores(property_id, score_key);

CREATE INDEX IF NOT EXISTS idx_rei_search_index_text ON rei_search_index(index_text);

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
        );

CREATE TABLE IF NOT EXISTS crm_contact_tags (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            tag TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE (contact_id, tag)
        );

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
        );

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
        );

CREATE INDEX IF NOT EXISTS idx_crm_lead_sources_reference_code ON crm_lead_sources(reference_code);

CREATE INDEX IF NOT EXISTS idx_crm_lead_sources_status ON crm_lead_sources(status, created_at);

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
        );

CREATE TABLE IF NOT EXISTS crm_customers (
            id SERIAL PRIMARY KEY,
            customer_key TEXT NOT NULL UNIQUE,
            contact_id INTEGER NOT NULL UNIQUE REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            status TEXT NOT NULL DEFAULT 'active',
            lifetime_value INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS crm_customer_roles (
            id SERIAL PRIMARY KEY,
            customer_id INTEGER NOT NULL REFERENCES crm_customers(id) ON DELETE CASCADE,
            role TEXT NOT NULL DEFAULT 'buyer',
            assigned_at TEXT NOT NULL,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (customer_id, role)
        );

CREATE TABLE IF NOT EXISTS crm_pipelines (
            id SERIAL PRIMARY KEY,
            pipeline_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            is_default INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS crm_pipeline_stages (
            id SERIAL PRIMARY KEY,
            pipeline_id INTEGER NOT NULL REFERENCES crm_pipelines(id) ON DELETE CASCADE,
            stage_key TEXT NOT NULL,
            label TEXT NOT NULL,
            position INTEGER NOT NULL DEFAULT 0,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (pipeline_id, stage_key)
        );

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
        );

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
        );

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
        );

CREATE TABLE IF NOT EXISTS crm_timeline_entries (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            entry_type TEXT NOT NULL,
            summary TEXT NOT NULL DEFAULT '',
            reference_type TEXT,
            reference_id INTEGER,
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

CREATE TABLE IF NOT EXISTS crm_campaign_targets (
            id SERIAL PRIMARY KEY,
            campaign_id INTEGER NOT NULL REFERENCES crm_campaigns(id) ON DELETE CASCADE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            status TEXT NOT NULL DEFAULT 'pending',
            sent_at TEXT,
            response_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            UNIQUE (campaign_id, contact_id)
        );

CREATE TABLE IF NOT EXISTS crm_segments (
            id SERIAL PRIMARY KEY,
            segment_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            criteria_json TEXT NOT NULL DEFAULT '{}',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS crm_segment_members (
            id SERIAL PRIMARY KEY,
            segment_id INTEGER NOT NULL REFERENCES crm_segments(id) ON DELETE CASCADE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            added_at TEXT NOT NULL,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            UNIQUE (segment_id, contact_id)
        );

CREATE TABLE IF NOT EXISTS crm_customer_scores (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            score_key TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 0,
            factors_json TEXT NOT NULL DEFAULT '{}',
            computed_at TEXT NOT NULL,
            UNIQUE (contact_id, score_key)
        );

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
        );

CREATE TABLE IF NOT EXISTS crm_satisfaction_responses (
            id SERIAL PRIMARY KEY,
            survey_id INTEGER NOT NULL REFERENCES crm_satisfaction_surveys(id) ON DELETE CASCADE,
            contact_id INTEGER NOT NULL REFERENCES crm_contact_profiles(id) ON DELETE CASCADE,
            rating INTEGER NOT NULL DEFAULT 3,
            answers_json TEXT NOT NULL DEFAULT '{}',
            submitted_at TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

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
        );

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
        );

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
        );

CREATE TABLE IF NOT EXISTS crm_analytics_snapshots (
            id SERIAL PRIMARY KEY,
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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

CREATE TABLE IF NOT EXISTS marketplace_review_moderation (
            id SERIAL PRIMARY KEY,
            review_id INTEGER NOT NULL UNIQUE REFERENCES marketplace_reviews(id) ON DELETE CASCADE,
            moderator_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            action TEXT NOT NULL DEFAULT 'pending',
            reason TEXT NOT NULL DEFAULT '',
            notes TEXT NOT NULL DEFAULT '',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS marketplace_reputation_snapshots (
            id SERIAL PRIMARY KEY,
            provider_profile_id INTEGER NOT NULL,
            score_key TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 0,
            factors_json TEXT NOT NULL DEFAULT '{}',
            computed_at TEXT NOT NULL,
            UNIQUE (provider_profile_id, score_key)
        );

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
        );

CREATE TABLE IF NOT EXISTS marketplace_dispute_messages (
            id SERIAL PRIMARY KEY,
            dispute_id INTEGER NOT NULL REFERENCES marketplace_disputes(id) ON DELETE CASCADE,
            author_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            message TEXT NOT NULL,
            visibility TEXT NOT NULL DEFAULT 'parties',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

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
        );

CREATE TABLE IF NOT EXISTS marketplace_analytics_snapshots (
            id SERIAL PRIMARY KEY,
            snapshot_key TEXT NOT NULL UNIQUE,
            scope TEXT NOT NULL DEFAULT 'global',
            metrics_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

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

CREATE TABLE IF NOT EXISTS iam_roles (
            id SERIAL PRIMARY KEY,
            role_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS iam_permissions (
            id SERIAL PRIMARY KEY,
            permission_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            resource TEXT NOT NULL DEFAULT '*',
            action TEXT NOT NULL DEFAULT 'read',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS iam_role_permissions (
            id SERIAL PRIMARY KEY,
            role_id INTEGER NOT NULL REFERENCES iam_roles(id) ON DELETE CASCADE,
            permission_id INTEGER NOT NULL REFERENCES iam_permissions(id) ON DELETE CASCADE,
            granted_at TEXT NOT NULL,
            UNIQUE (role_id, permission_id)
        );

CREATE TABLE IF NOT EXISTS iam_user_roles (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role_id INTEGER NOT NULL REFERENCES iam_roles(id) ON DELETE CASCADE,
            assigned_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
            assigned_at TEXT NOT NULL,
            expires_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            UNIQUE (user_id, role_id)
        );

CREATE TABLE IF NOT EXISTS iam_groups (
            id SERIAL PRIMARY KEY,
            group_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL,
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS iam_group_members (
            id SERIAL PRIMARY KEY,
            group_id INTEGER NOT NULL REFERENCES iam_groups(id) ON DELETE CASCADE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role_in_group TEXT NOT NULL DEFAULT 'member',
            joined_at TEXT NOT NULL,
            UNIQUE (group_id, user_id)
        );

CREATE TABLE IF NOT EXISTS iam_teams (
            id SERIAL PRIMARY KEY,
            team_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL,
            leader_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS iam_team_members (
            id SERIAL PRIMARY KEY,
            team_id INTEGER NOT NULL REFERENCES iam_teams(id) ON DELETE CASCADE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role_in_team TEXT NOT NULL DEFAULT 'member',
            joined_at TEXT NOT NULL,
            UNIQUE (team_id, user_id)
        );

CREATE TABLE IF NOT EXISTS iam_access_policies (
            id SERIAL PRIMARY KEY,
            policy_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            policy_type TEXT NOT NULL DEFAULT 'rbac',
            rules_json TEXT NOT NULL DEFAULT '[]',
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS iam_policy_bindings (
            id SERIAL PRIMARY KEY,
            policy_id INTEGER NOT NULL REFERENCES iam_access_policies(id) ON DELETE CASCADE,
            binding_type TEXT NOT NULL DEFAULT 'role',
            binding_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE (policy_id, binding_type, binding_id)
        );

CREATE TABLE IF NOT EXISTS access_devices (
            id SERIAL PRIMARY KEY,
            device_key TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            device_type TEXT NOT NULL DEFAULT 'browser',
            device_name TEXT NOT NULL DEFAULT '',
            fingerprint TEXT NOT NULL DEFAULT '',
            trust_level TEXT NOT NULL DEFAULT 'unknown',
            last_seen_at TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS access_api_keys (
            id SERIAL PRIMARY KEY,
            api_key_key TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL,
            name TEXT NOT NULL,
            key_prefix TEXT NOT NULL DEFAULT '',
            key_hash TEXT NOT NULL DEFAULT '',
            scopes_json TEXT NOT NULL DEFAULT '[]',
            status TEXT NOT NULL DEFAULT 'active',
            expires_at TEXT,
            last_used_at TEXT,
            created_at TEXT NOT NULL,
            revoked_at TEXT
        );

CREATE TABLE IF NOT EXISTS access_session_records (
            id SERIAL PRIMARY KEY,
            session_key TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            session_token TEXT REFERENCES sessions(token) ON DELETE SET NULL,
            device_id INTEGER REFERENCES access_devices(id) ON DELETE SET NULL,
            ip_address TEXT NOT NULL DEFAULT '',
            user_agent TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'active',
            started_at TEXT NOT NULL,
            expires_at TEXT,
            revoked_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}'
        );

CREATE TABLE IF NOT EXISTS access_route_policies (
            id SERIAL PRIMARY KEY,
            route_key TEXT NOT NULL UNIQUE,
            path_pattern TEXT NOT NULL,
            methods_json TEXT NOT NULL DEFAULT '["GET"]',
            required_roles_json TEXT NOT NULL DEFAULT '[]',
            required_permissions_json TEXT NOT NULL DEFAULT '[]',
            policy_type TEXT NOT NULL DEFAULT 'rbac',
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS access_mfa_enrollments (
            id SERIAL PRIMARY KEY,
            enrollment_key TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            mfa_type TEXT NOT NULL DEFAULT 'totp',
            secret_ref TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            enrolled_at TEXT,
            last_used_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}'
        );

CREATE TABLE IF NOT EXISTS access_token_rotations (
            id SERIAL PRIMARY KEY,
            rotation_key TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            token_type TEXT NOT NULL DEFAULT 'session',
            old_token_ref TEXT NOT NULL DEFAULT '',
            new_token_ref TEXT NOT NULL DEFAULT '',
            rotated_at TEXT NOT NULL,
            reason TEXT NOT NULL DEFAULT '',
            metadata_json TEXT NOT NULL DEFAULT '{}'
        );

CREATE TABLE IF NOT EXISTS audit_trail_entries (
            id SERIAL PRIMARY KEY,
            entry_key TEXT NOT NULL UNIQUE,
            event_type TEXT NOT NULL DEFAULT 'system',
            actor_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            resource_type TEXT NOT NULL DEFAULT '',
            resource_id INTEGER,
            action TEXT NOT NULL DEFAULT '',
            severity TEXT NOT NULL DEFAULT 'info',
            payload_json TEXT NOT NULL DEFAULT '{}',
            checksum TEXT NOT NULL DEFAULT '',
            previous_checksum TEXT NOT NULL DEFAULT '',
            ip_address TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS audit_system_events (
            id SERIAL PRIMARY KEY,
            event_key TEXT NOT NULL UNIQUE,
            trail_entry_id INTEGER REFERENCES audit_trail_entries(id) ON DELETE SET NULL,
            component TEXT NOT NULL DEFAULT 'platform',
            message TEXT NOT NULL DEFAULT '',
            severity TEXT NOT NULL DEFAULT 'info',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS audit_user_events (
            id SERIAL PRIMARY KEY,
            event_key TEXT NOT NULL UNIQUE,
            trail_entry_id INTEGER REFERENCES audit_trail_entries(id) ON DELETE SET NULL,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            action TEXT NOT NULL DEFAULT '',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS audit_admin_events (
            id SERIAL PRIMARY KEY,
            event_key TEXT NOT NULL UNIQUE,
            trail_entry_id INTEGER REFERENCES audit_trail_entries(id) ON DELETE SET NULL,
            admin_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            action TEXT NOT NULL DEFAULT '',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS audit_ai_events (
            id SERIAL PRIMARY KEY,
            event_key TEXT NOT NULL UNIQUE,
            trail_entry_id INTEGER REFERENCES audit_trail_entries(id) ON DELETE SET NULL,
            assistant_session_id INTEGER REFERENCES assistant_sessions(id) ON DELETE SET NULL,
            action TEXT NOT NULL DEFAULT '',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS compliance_policies (
            id SERIAL PRIMARY KEY,
            policy_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            framework TEXT NOT NULL DEFAULT 'internal',
            rules_json TEXT NOT NULL DEFAULT '[]',
            status TEXT NOT NULL DEFAULT 'active',
            effective_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS compliance_consents (
            id SERIAL PRIMARY KEY,
            consent_key TEXT NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL,
            consent_type TEXT NOT NULL DEFAULT 'terms',
            status TEXT NOT NULL DEFAULT 'pending',
            granted_at TEXT,
            revoked_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS compliance_retention_rules (
            id SERIAL PRIMARY KEY,
            rule_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            resource_type TEXT NOT NULL DEFAULT 'audit',
            retention_days INTEGER NOT NULL DEFAULT 365,
            action_on_expiry TEXT NOT NULL DEFAULT 'archive',
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS compliance_deletion_requests (
            id SERIAL PRIMARY KEY,
            request_key TEXT NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL,
            deletion_type TEXT NOT NULL DEFAULT 'soft_delete',
            status TEXT NOT NULL DEFAULT 'pending',
            requested_at TEXT NOT NULL,
            completed_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}'
        );

CREATE TABLE IF NOT EXISTS privacy_data_exports (
            id SERIAL PRIMARY KEY,
            export_key TEXT NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL,
            format TEXT NOT NULL DEFAULT 'json',
            scope_json TEXT NOT NULL DEFAULT '{}',
            status TEXT NOT NULL DEFAULT 'pending',
            storage_ref TEXT NOT NULL DEFAULT '',
            requested_at TEXT NOT NULL,
            completed_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}'
        );

CREATE TABLE IF NOT EXISTS privacy_erasure_requests (
            id SERIAL PRIMARY KEY,
            request_key TEXT NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL,
            scope_json TEXT NOT NULL DEFAULT '{}',
            status TEXT NOT NULL DEFAULT 'pending',
            requested_at TEXT NOT NULL,
            completed_at TEXT,
            validation_json TEXT NOT NULL DEFAULT '{}',
            metadata_json TEXT NOT NULL DEFAULT '{}'
        );

CREATE TABLE IF NOT EXISTS risk_signals (
            id SERIAL PRIMARY KEY,
            signal_key TEXT NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            signal_type TEXT NOT NULL DEFAULT 'login_anomaly',
            severity TEXT NOT NULL DEFAULT 'medium',
            score_delta INTEGER NOT NULL DEFAULT 10,
            source TEXT NOT NULL DEFAULT 'platform',
            payload_json TEXT NOT NULL DEFAULT '{}',
            detected_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            metadata_json TEXT NOT NULL DEFAULT '{}'
        );

CREATE TABLE IF NOT EXISTS risk_scores (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            score_key TEXT NOT NULL DEFAULT 'overall',
            score INTEGER NOT NULL DEFAULT 0,
            level TEXT NOT NULL DEFAULT 'low',
            factors_json TEXT NOT NULL DEFAULT '{}',
            computed_at TEXT NOT NULL,
            UNIQUE (user_id, score_key)
        );

CREATE TABLE IF NOT EXISTS risk_alerts (
            id SERIAL PRIMARY KEY,
            alert_key TEXT NOT NULL UNIQUE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            signal_id INTEGER REFERENCES risk_signals(id) ON DELETE SET NULL,
            level TEXT NOT NULL DEFAULT 'medium',
            title TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'open',
            acknowledged_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
            created_at TEXT NOT NULL,
            resolved_at TEXT
        );

CREATE TABLE IF NOT EXISTS security_incidents (
            id SERIAL PRIMARY KEY,
            incident_key TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            severity TEXT NOT NULL DEFAULT 'medium',
            status TEXT NOT NULL DEFAULT 'open',
            reported_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
            assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
            description TEXT NOT NULL DEFAULT '',
            resolution TEXT NOT NULL DEFAULT '',
            opened_at TEXT NOT NULL,
            resolved_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

CREATE TABLE IF NOT EXISTS security_analytics_snapshots (
            id SERIAL PRIMARY KEY,
            snapshot_key TEXT NOT NULL UNIQUE,
            scope TEXT NOT NULL DEFAULT 'global',
            metrics_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

CREATE INDEX IF NOT EXISTS idx_iam_user_roles_user ON iam_user_roles(user_id, role_id);

CREATE INDEX IF NOT EXISTS idx_iam_role_permissions_role ON iam_role_permissions(role_id);

CREATE INDEX IF NOT EXISTS idx_access_devices_user ON access_devices(user_id, status);

CREATE INDEX IF NOT EXISTS idx_access_api_keys_user ON access_api_keys(user_id, status);

CREATE INDEX IF NOT EXISTS idx_access_session_records_user ON access_session_records(user_id, status);

CREATE INDEX IF NOT EXISTS idx_audit_trail_created ON audit_trail_entries(created_at, event_type);

CREATE INDEX IF NOT EXISTS idx_compliance_consents_user ON compliance_consents(user_id, consent_type);

CREATE INDEX IF NOT EXISTS idx_risk_signals_user ON risk_signals(user_id, status);

CREATE INDEX IF NOT EXISTS idx_risk_scores_user ON risk_scores(user_id, score_key);

CREATE INDEX IF NOT EXISTS idx_security_incidents_status ON security_incidents(status, opened_at);

CREATE TABLE IF NOT EXISTS communication_messages (
    id SERIAL PRIMARY KEY,
    message_key TEXT NOT NULL UNIQUE,
    thread_id INTEGER,
    channel_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    direction TEXT NOT NULL DEFAULT 'outbound',
    priority TEXT NOT NULL DEFAULT 'normal',
    status TEXT NOT NULL DEFAULT 'draft',
    sender_user_id INTEGER,
    recipient_user_id INTEGER,
    contact_id INTEGER,
    organization_id INTEGER,
    subject TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    scheduled_at TEXT,
    sent_at TEXT,
    expires_at TEXT,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    thread_id INTEGER REFERENCES communication_threads(id) ON DELETE SET NULL,
    channel_id INTEGER REFERENCES communication_channels(id) ON DELETE SET NULL,
    sender_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    recipient_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_messages_status ON communication_messages(status, created_at);

CREATE INDEX IF NOT EXISTS idx_communication_messages_channel ON communication_messages(channel_type, status);

CREATE TABLE IF NOT EXISTS communication_threads (
    id SERIAL PRIMARY KEY,
    thread_key TEXT NOT NULL UNIQUE,
    channel_id INTEGER,
    subject TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'open',
    organization_id INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    channel_id INTEGER REFERENCES communication_channels(id) ON DELETE SET NULL,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_threads_status ON communication_threads(status, created_at);

CREATE TABLE IF NOT EXISTS communication_channels (
    id SERIAL PRIMARY KEY,
    channel_key TEXT NOT NULL UNIQUE,
    channel_type TEXT NOT NULL DEFAULT 'email',
    name TEXT NOT NULL,
    provider TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    config_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_channels_status ON communication_channels(status, created_at);

CREATE TABLE IF NOT EXISTS communication_recipients (
    id SERIAL PRIMARY KEY,
    recipient_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    recipient_type TEXT NOT NULL DEFAULT 'user',
    user_id INTEGER,
    contact_id INTEGER,
    address TEXT NOT NULL DEFAULT '',
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_recipients_status ON communication_recipients(status, created_at);

CREATE TABLE IF NOT EXISTS communication_groups (
    id SERIAL PRIMARY KEY,
    group_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    organization_id INTEGER,
    updated_at TEXT NOT NULL,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_groups_status ON communication_groups(status, created_at);

CREATE TABLE IF NOT EXISTS communication_events (
    id SERIAL PRIMARY KEY,
    event_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    event_kind TEXT NOT NULL DEFAULT 'system',
    source_program TEXT NOT NULL DEFAULT 'platform',
    payload_json TEXT NOT NULL DEFAULT '{}',
    message_id INTEGER,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_events_status ON communication_events(status, created_at);

CREATE TABLE IF NOT EXISTS communication_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    message_id INTEGER,
    level TEXT NOT NULL DEFAULT 'info',
    message TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_logs_status ON communication_logs(status, created_at);

CREATE TABLE IF NOT EXISTS communication_history (
    id SERIAL PRIMARY KEY,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    message_id INTEGER,
    action TEXT NOT NULL DEFAULT '',
    actor_user_id INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{}',
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE CASCADE,
    actor_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_history_status ON communication_history(status, created_at);

CREATE TABLE IF NOT EXISTS communication_archives (
    id SERIAL PRIMARY KEY,
    archive_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    message_id INTEGER,
    archived_at TEXT NOT NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_communication_archives_status ON communication_archives(status, created_at);

CREATE TABLE IF NOT EXISTS communication_metadata (
    id SERIAL PRIMARY KEY,
    metadata_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    resource_type TEXT NOT NULL DEFAULT 'message',
    resource_id INTEGER NOT NULL DEFAULT 0,
    meta_key TEXT NOT NULL DEFAULT '',
    meta_value_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_metadata_status ON communication_metadata(status, created_at);

CREATE TABLE IF NOT EXISTS notification_events (
    id SERIAL PRIMARY KEY,
    event_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_type TEXT NOT NULL DEFAULT 'system',
    user_id INTEGER,
    contact_id INTEGER,
    title TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    priority TEXT NOT NULL DEFAULT 'normal',
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_notification_events_status ON notification_events(status, created_at);

CREATE TABLE IF NOT EXISTS notification_rules (
    id SERIAL PRIMARY KEY,
    rule_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    event_kind TEXT NOT NULL DEFAULT 'system',
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    rules_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_notification_rules_status ON notification_rules(status, created_at);

CREATE TABLE IF NOT EXISTS notification_templates (
    id SERIAL PRIMARY KEY,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    subject TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_notification_templates_status ON notification_templates(status, created_at);

CREATE TABLE IF NOT EXISTS notification_preferences (
    id SERIAL PRIMARY KEY,
    preference_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    enabled INTEGER NOT NULL DEFAULT 1,
    settings_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_notification_preferences_status ON notification_preferences(status, created_at);

CREATE TABLE IF NOT EXISTS notification_deliveries (
    id SERIAL PRIMARY KEY,
    delivery_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'in_app',
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    delivered_at TEXT,
    notification_event_id INTEGER REFERENCES notification_events(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_notification_deliveries_status ON notification_deliveries(status, created_at);

CREATE TABLE IF NOT EXISTS notification_batches (
    id SERIAL PRIMARY KEY,
    batch_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    batch_status TEXT NOT NULL DEFAULT 'pending',
    scheduled_at TEXT,
    completed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_notification_batches_status ON notification_batches(status, created_at);

CREATE TABLE IF NOT EXISTS notification_acknowledgements (
    id SERIAL PRIMARY KEY,
    ack_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    user_id INTEGER,
    acknowledged_at TEXT NOT NULL,
    notification_event_id INTEGER REFERENCES notification_events(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_notification_acknowledgements_status ON notification_acknowledgements(status, created_at);

CREATE TABLE IF NOT EXISTS notification_failures (
    id SERIAL PRIMARY KEY,
    failure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    error_code TEXT NOT NULL DEFAULT '',
    error_message TEXT NOT NULL DEFAULT '',
    failed_at TEXT NOT NULL,
    notification_event_id INTEGER REFERENCES notification_events(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_notification_failures_status ON notification_failures(status, created_at);

CREATE TABLE IF NOT EXISTS notification_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_notification_statistics_status ON notification_statistics(status, created_at);

CREATE TABLE IF NOT EXISTS notification_queue (
    id SERIAL PRIMARY KEY,
    queue_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_event_id INTEGER,
    priority TEXT NOT NULL DEFAULT 'normal',
    queue_status TEXT NOT NULL DEFAULT 'pending',
    scheduled_at TEXT,
    notification_event_id INTEGER REFERENCES notification_events(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_notification_queue_status ON notification_queue(status, created_at);

CREATE TABLE IF NOT EXISTS email_accounts (
    id SERIAL PRIMARY KEY,
    account_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    organization_id INTEGER,
    email_address TEXT NOT NULL DEFAULT '',
    display_name TEXT NOT NULL DEFAULT '',
    provider TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_email_accounts_status ON email_accounts(status, created_at);

CREATE TABLE IF NOT EXISTS email_templates (
    id SERIAL PRIMARY KEY,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    subject TEXT NOT NULL DEFAULT '',
    body_html TEXT NOT NULL DEFAULT '',
    body_text TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_email_templates_status ON email_templates(status, created_at);

CREATE TABLE IF NOT EXISTS email_messages (
    id SERIAL PRIMARY KEY,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    account_id INTEGER,
    message_id INTEGER,
    to_email TEXT NOT NULL DEFAULT '',
    from_email TEXT NOT NULL DEFAULT '',
    subject TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    email_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    account_id INTEGER REFERENCES email_accounts(id) ON DELETE SET NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_email_messages_status ON email_messages(status, created_at);

CREATE TABLE IF NOT EXISTS email_attachments (
    id SERIAL PRIMARY KEY,
    attachment_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    filename TEXT NOT NULL DEFAULT '',
    content_type TEXT NOT NULL DEFAULT 'application/octet-stream',
    size_bytes INTEGER NOT NULL DEFAULT 0,
    storage_ref TEXT NOT NULL DEFAULT '',
    email_message_id INTEGER REFERENCES email_messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_email_attachments_status ON email_attachments(status, created_at);

CREATE TABLE IF NOT EXISTS email_threads (
    id SERIAL PRIMARY KEY,
    thread_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    subject TEXT NOT NULL DEFAULT '',
    thread_status TEXT NOT NULL DEFAULT 'open',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_email_threads_status ON email_threads(status, created_at);

CREATE TABLE IF NOT EXISTS email_delivery_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    email_message_id INTEGER REFERENCES email_messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_email_delivery_logs_status ON email_delivery_logs(status, created_at);

CREATE TABLE IF NOT EXISTS email_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_email_statistics_status ON email_statistics(status, created_at);

CREATE TABLE IF NOT EXISTS email_bounces (
    id SERIAL PRIMARY KEY,
    bounce_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    bounce_type TEXT NOT NULL DEFAULT 'hard',
    reason TEXT NOT NULL DEFAULT '',
    bounced_at TEXT NOT NULL,
    email_message_id INTEGER REFERENCES email_messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_email_bounces_status ON email_bounces(status, created_at);

CREATE TABLE IF NOT EXISTS email_click_tracking (
    id SERIAL PRIMARY KEY,
    click_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    link_url TEXT NOT NULL DEFAULT '',
    clicked_at TEXT NOT NULL,
    email_message_id INTEGER REFERENCES email_messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_email_click_tracking_status ON email_click_tracking(status, created_at);

CREATE TABLE IF NOT EXISTS email_open_tracking (
    id SERIAL PRIMARY KEY,
    open_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    email_message_id INTEGER,
    opened_at TEXT NOT NULL,
    email_message_id INTEGER REFERENCES email_messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_email_open_tracking_status ON email_open_tracking(status, created_at);

CREATE TABLE IF NOT EXISTS sms_templates (
    id SERIAL PRIMARY KEY,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sms_templates_status ON sms_templates(status, created_at);

CREATE TABLE IF NOT EXISTS sms_messages (
    id SERIAL PRIMARY KEY,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    provider_id INTEGER,
    message_id INTEGER,
    to_number TEXT NOT NULL DEFAULT '',
    from_number TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    sms_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    provider_id INTEGER REFERENCES sms_providers(id) ON DELETE SET NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_sms_messages_status ON sms_messages(status, created_at);

CREATE TABLE IF NOT EXISTS sms_delivery_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    sms_message_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    sms_message_id INTEGER REFERENCES sms_messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sms_delivery_logs_status ON sms_delivery_logs(status, created_at);

CREATE TABLE IF NOT EXISTS sms_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sms_statistics_status ON sms_statistics(status, created_at);

CREATE TABLE IF NOT EXISTS sms_providers (
    id SERIAL PRIMARY KEY,
    provider_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    provider_type TEXT NOT NULL DEFAULT 'twilio',
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sms_providers_status ON sms_providers(status, created_at);

CREATE TABLE IF NOT EXISTS sms_queue (
    id SERIAL PRIMARY KEY,
    queue_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    sms_message_id INTEGER,
    priority TEXT NOT NULL DEFAULT 'normal',
    queue_status TEXT NOT NULL DEFAULT 'pending',
    scheduled_at TEXT,
    sms_message_id INTEGER REFERENCES sms_messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sms_queue_status ON sms_queue(status, created_at);

CREATE TABLE IF NOT EXISTS whatsapp_accounts (
    id SERIAL PRIMARY KEY,
    account_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    handle TEXT NOT NULL DEFAULT '@lawimofficial',
    phone_e164 TEXT NOT NULL DEFAULT '',
    provider TEXT NOT NULL DEFAULT 'meta_cloud',
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_accounts_status ON whatsapp_accounts(status, created_at);

CREATE TABLE IF NOT EXISTS whatsapp_templates (
    id SERIAL PRIMARY KEY,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    template_name TEXT NOT NULL DEFAULT '',
    language TEXT NOT NULL DEFAULT 'fr',
    body TEXT NOT NULL DEFAULT '',
    variables_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_templates_status ON whatsapp_templates(status, created_at);

CREATE TABLE IF NOT EXISTS whatsapp_messages (
    id SERIAL PRIMARY KEY,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    account_id INTEGER,
    message_id INTEGER,
    to_number TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    whatsapp_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    account_id INTEGER REFERENCES whatsapp_accounts(id) ON DELETE SET NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_messages_status ON whatsapp_messages(status, created_at);

CREATE TABLE IF NOT EXISTS whatsapp_media (
    id SERIAL PRIMARY KEY,
    media_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    whatsapp_message_id INTEGER,
    media_type TEXT NOT NULL DEFAULT 'document',
    filename TEXT NOT NULL DEFAULT '',
    storage_ref TEXT NOT NULL DEFAULT '',
    whatsapp_message_id INTEGER REFERENCES whatsapp_messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_media_status ON whatsapp_media(status, created_at);

CREATE TABLE IF NOT EXISTS whatsapp_sessions (
    id SERIAL PRIMARY KEY,
    session_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    contact_id INTEGER,
    session_status TEXT NOT NULL DEFAULT 'open',
    opened_at TEXT NOT NULL,
    closed_at TEXT,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_sessions_status ON whatsapp_sessions(status, created_at);

CREATE TABLE IF NOT EXISTS whatsapp_delivery_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    whatsapp_message_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    whatsapp_message_id INTEGER REFERENCES whatsapp_messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_delivery_logs_status ON whatsapp_delivery_logs(status, created_at);

CREATE TABLE IF NOT EXISTS whatsapp_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_statistics_status ON whatsapp_statistics(status, created_at);

CREATE TABLE IF NOT EXISTS telegram_bots (
    id SERIAL PRIMARY KEY,
    bot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    bot_handle TEXT NOT NULL DEFAULT '@lawim_assistant_bot',
    bot_token_ref TEXT NOT NULL DEFAULT '',
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_telegram_bots_status ON telegram_bots(status, created_at);

CREATE TABLE IF NOT EXISTS telegram_messages (
    id SERIAL PRIMARY KEY,
    message_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    bot_id INTEGER,
    message_id INTEGER,
    chat_id TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    telegram_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    bot_id INTEGER REFERENCES telegram_bots(id) ON DELETE SET NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_telegram_messages_status ON telegram_messages(status, created_at);

CREATE TABLE IF NOT EXISTS telegram_updates (
    id SERIAL PRIMARY KEY,
    update_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    bot_id INTEGER,
    update_type TEXT NOT NULL DEFAULT 'message',
    payload_json TEXT NOT NULL DEFAULT '{}',
    received_at TEXT NOT NULL,
    bot_id INTEGER REFERENCES telegram_bots(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_telegram_updates_status ON telegram_updates(status, created_at);

CREATE TABLE IF NOT EXISTS telegram_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_telegram_statistics_status ON telegram_statistics(status, created_at);

CREATE TABLE IF NOT EXISTS push_devices (
    id SERIAL PRIMARY KEY,
    device_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    platform TEXT NOT NULL DEFAULT 'web',
    device_token TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_push_devices_status ON push_devices(status, created_at);

CREATE TABLE IF NOT EXISTS push_notifications (
    id SERIAL PRIMARY KEY,
    notification_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    device_id INTEGER,
    message_id INTEGER,
    title TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    push_status TEXT NOT NULL DEFAULT 'draft',
    sent_at TEXT,
    device_id INTEGER REFERENCES push_devices(id) ON DELETE SET NULL,
    message_id INTEGER REFERENCES communication_messages(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_push_notifications_status ON push_notifications(status, created_at);

CREATE TABLE IF NOT EXISTS push_delivery_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    push_notification_id INTEGER,
    delivery_status TEXT NOT NULL DEFAULT 'pending',
    provider_response TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    push_notification_id INTEGER REFERENCES push_notifications(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_push_delivery_logs_status ON push_delivery_logs(status, created_at);

CREATE TABLE IF NOT EXISTS push_subscriptions (
    id SERIAL PRIMARY KEY,
    subscription_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    topic TEXT NOT NULL DEFAULT '',
    subscription_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_push_subscriptions_status ON push_subscriptions(status, created_at);

CREATE TABLE IF NOT EXISTS push_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_push_statistics_status ON push_statistics(status, created_at);

CREATE TABLE IF NOT EXISTS inapp_notifications (
    id SERIAL PRIMARY KEY,
    notification_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    category_id INTEGER,
    title TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    action_json TEXT NOT NULL DEFAULT '{}',
    read_at TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES inapp_categories(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_inapp_notifications_status ON inapp_notifications(status, created_at);

CREATE TABLE IF NOT EXISTS inapp_categories (
    id SERIAL PRIMARY KEY,
    category_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    slug TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_inapp_categories_status ON inapp_categories(status, created_at);

CREATE TABLE IF NOT EXISTS inapp_read_status (
    id SERIAL PRIMARY KEY,
    read_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    notification_id INTEGER,
    user_id INTEGER,
    read_at TEXT NOT NULL,
    notification_id INTEGER REFERENCES inapp_notifications(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_inapp_read_status_status ON inapp_read_status(status, created_at);

CREATE TABLE IF NOT EXISTS inapp_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_inapp_statistics_status ON inapp_statistics(status, created_at);

CREATE TABLE IF NOT EXISTS campaigns (
    id SERIAL PRIMARY KEY,
    campaign_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    campaign_type TEXT NOT NULL DEFAULT 'multichannel',
    organization_id INTEGER,
    campaign_status TEXT NOT NULL DEFAULT 'draft',
    scheduled_at TEXT,
    started_at TEXT,
    completed_at TEXT,
    updated_at TEXT NOT NULL,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status, created_at);

CREATE TABLE IF NOT EXISTS campaign_channels (
    id SERIAL PRIMARY KEY,
    channel_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    config_json TEXT NOT NULL DEFAULT '{}',
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_campaign_channels_status ON campaign_channels(status, created_at);

CREATE TABLE IF NOT EXISTS campaign_audiences (
    id SERIAL PRIMARY KEY,
    audience_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    name TEXT NOT NULL DEFAULT '',
    audience_json TEXT NOT NULL DEFAULT '{}',
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_campaign_audiences_status ON campaign_audiences(status, created_at);

CREATE TABLE IF NOT EXISTS campaign_segments (
    id SERIAL PRIMARY KEY,
    segment_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    name TEXT NOT NULL DEFAULT '',
    criteria_json TEXT NOT NULL DEFAULT '{}',
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_campaign_segments_status ON campaign_segments(status, created_at);

CREATE TABLE IF NOT EXISTS campaign_executions (
    id SERIAL PRIMARY KEY,
    execution_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    execution_status TEXT NOT NULL DEFAULT 'pending',
    started_at TEXT,
    completed_at TEXT,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_campaign_executions_status ON campaign_executions(status, created_at);

CREATE TABLE IF NOT EXISTS campaign_statistics (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_campaign_statistics_status ON campaign_statistics(status, created_at);

CREATE TABLE IF NOT EXISTS campaign_results (
    id SERIAL PRIMARY KEY,
    result_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    result_type TEXT NOT NULL DEFAULT 'summary',
    result_json TEXT NOT NULL DEFAULT '{}',
    recorded_at TEXT NOT NULL,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_campaign_results_status ON campaign_results(status, created_at);

CREATE TABLE IF NOT EXISTS campaign_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    campaign_id INTEGER,
    level TEXT NOT NULL DEFAULT 'info',
    message TEXT NOT NULL DEFAULT '',
    logged_at TEXT NOT NULL,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_campaign_logs_status ON campaign_logs(status, created_at);

CREATE TABLE IF NOT EXISTS queue_jobs (
    id SERIAL PRIMARY KEY,
    job_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    job_type TEXT NOT NULL DEFAULT 'send_message',
    channel_type TEXT NOT NULL DEFAULT 'email',
    priority TEXT NOT NULL DEFAULT 'normal',
    job_status TEXT NOT NULL DEFAULT 'pending',
    payload_json TEXT NOT NULL DEFAULT '{}',
    scheduled_at TEXT,
    started_at TEXT,
    completed_at TEXT,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 3
);

CREATE INDEX IF NOT EXISTS idx_queue_jobs_status ON queue_jobs(status, created_at);

CREATE TABLE IF NOT EXISTS queue_workers (
    id SERIAL PRIMARY KEY,
    worker_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    worker_name TEXT NOT NULL DEFAULT '',
    worker_status TEXT NOT NULL DEFAULT 'idle',
    last_heartbeat_at TEXT,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_queue_workers_status ON queue_workers(status, created_at);

CREATE TABLE IF NOT EXISTS queue_failures (
    id SERIAL PRIMARY KEY,
    failure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    job_id INTEGER,
    error_code TEXT NOT NULL DEFAULT '',
    error_message TEXT NOT NULL DEFAULT '',
    failed_at TEXT NOT NULL,
    job_id INTEGER REFERENCES queue_jobs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_queue_failures_status ON queue_failures(status, created_at);

CREATE TABLE IF NOT EXISTS queue_retry_history (
    id SERIAL PRIMARY KEY,
    retry_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    job_id INTEGER,
    attempt_number INTEGER NOT NULL DEFAULT 1,
    retry_at TEXT NOT NULL,
    result TEXT NOT NULL DEFAULT '',
    job_id INTEGER REFERENCES queue_jobs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_queue_retry_history_status ON queue_retry_history(status, created_at);

CREATE TABLE IF NOT EXISTS queue_batches (
    id SERIAL PRIMARY KEY,
    batch_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    batch_status TEXT NOT NULL DEFAULT 'pending',
    job_count INTEGER NOT NULL DEFAULT 0,
    completed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_queue_batches_status ON queue_batches(status, created_at);

CREATE TABLE IF NOT EXISTS template_categories (
    id SERIAL PRIMARY KEY,
    category_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    slug TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_template_categories_status ON template_categories(status, created_at);

CREATE TABLE IF NOT EXISTS template_versions (
    id SERIAL PRIMARY KEY,
    version_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    category_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    version_number INTEGER NOT NULL DEFAULT 1,
    content_json TEXT NOT NULL DEFAULT '{}',
    published_at TEXT,
    category_id INTEGER REFERENCES template_categories(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_template_versions_status ON template_versions(status, created_at);

CREATE TABLE IF NOT EXISTS template_variables (
    id SERIAL PRIMARY KEY,
    variable_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    template_version_id INTEGER,
    variable_name TEXT NOT NULL DEFAULT '',
    default_value TEXT NOT NULL DEFAULT '',
    template_version_id INTEGER REFERENCES template_versions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_template_variables_status ON template_variables(status, created_at);

CREATE TABLE IF NOT EXISTS template_translations (
    id SERIAL PRIMARY KEY,
    translation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    template_version_id INTEGER,
    locale TEXT NOT NULL DEFAULT 'fr',
    content_json TEXT NOT NULL DEFAULT '{}',
    template_version_id INTEGER REFERENCES template_versions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_template_translations_status ON template_translations(status, created_at);

CREATE TABLE IF NOT EXISTS communication_preferences (
    id SERIAL PRIMARY KEY,
    preference_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    channel_type TEXT NOT NULL DEFAULT 'email',
    enabled INTEGER NOT NULL DEFAULT 1,
    settings_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_communication_preferences_status ON communication_preferences(status, created_at);

CREATE TABLE IF NOT EXISTS communication_consent_history (
    id SERIAL PRIMARY KEY,
    consent_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    consent_type TEXT NOT NULL DEFAULT 'marketing',
    consent_status TEXT NOT NULL DEFAULT 'granted',
    recorded_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_consent_history_status ON communication_consent_history(status, created_at);

CREATE TABLE IF NOT EXISTS communication_blacklists (
    id SERIAL PRIMARY KEY,
    blacklist_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    channel_type TEXT NOT NULL DEFAULT 'email',
    address TEXT NOT NULL DEFAULT '',
    reason TEXT NOT NULL DEFAULT '',
    blocked_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_blacklists_status ON communication_blacklists(status, created_at);

CREATE TABLE IF NOT EXISTS communication_whitelists (
    id SERIAL PRIMARY KEY,
    whitelist_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    channel_type TEXT NOT NULL DEFAULT 'email',
    address TEXT NOT NULL DEFAULT '',
    reason TEXT NOT NULL DEFAULT '',
    allowed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_whitelists_status ON communication_whitelists(status, created_at);

CREATE TABLE IF NOT EXISTS communication_quiet_hours (
    id SERIAL PRIMARY KEY,
    quiet_hours_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    timezone TEXT NOT NULL DEFAULT 'Africa/Douala',
    start_time TEXT NOT NULL DEFAULT '22:00',
    end_time TEXT NOT NULL DEFAULT '07:00',
    days_json TEXT NOT NULL DEFAULT '[]',
    updated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_communication_quiet_hours_status ON communication_quiet_hours(status, created_at);

CREATE TABLE IF NOT EXISTS communication_dashboard_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    snapshot_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_dashboard_snapshots_status ON communication_dashboard_snapshots(status, created_at);

CREATE TABLE IF NOT EXISTS communication_analytics (
    id SERIAL PRIMARY KEY,
    analytics_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global',
    period TEXT NOT NULL DEFAULT 'daily',
    metrics_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_analytics_status ON communication_analytics(status, created_at);

CREATE TABLE IF NOT EXISTS communication_ai_recommendations (
    id SERIAL PRIMARY KEY,
    recommendation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    user_id INTEGER,
    contact_id INTEGER,
    recommendation_type TEXT NOT NULL DEFAULT 'followup',
    recommendation_json TEXT NOT NULL DEFAULT '{}',
    score REAL NOT NULL DEFAULT 0,
    generated_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    contact_id INTEGER REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_communication_ai_recommendations_status ON communication_ai_recommendations(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_events (
    id SERIAL PRIMARY KEY,
    event_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    event_type TEXT NOT NULL DEFAULT 'generic', source_program TEXT NOT NULL DEFAULT 'global', payload_json TEXT NOT NULL DEFAULT '{}', occurred_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_events_status ON analytics_events(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_event_sources (
    id SERIAL PRIMARY KEY,
    source_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    program_code TEXT NOT NULL DEFAULT 'global', source_type TEXT NOT NULL DEFAULT 'metrics', config_json TEXT NOT NULL DEFAULT '{}', enabled INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_analytics_event_sources_status ON analytics_event_sources(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_metrics (
    id SERIAL PRIMARY KEY,
    metric_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', category TEXT NOT NULL DEFAULT 'general', unit TEXT NOT NULL DEFAULT 'count', source_program TEXT NOT NULL DEFAULT 'global', definition_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_metrics_status ON analytics_metrics(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_metric_values (
    id SERIAL PRIMARY KEY,
    value_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metric_id INTEGER, value REAL NOT NULL DEFAULT 0, dimensions_json TEXT NOT NULL DEFAULT '{}', recorded_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_metric_values_status ON analytics_metric_values(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_metric_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global', metrics_json TEXT NOT NULL DEFAULT '{}', snapshot_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_metric_snapshots_status ON analytics_metric_snapshots(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_aggregations (
    id SERIAL PRIMARY KEY,
    aggregation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', aggregation_type TEXT NOT NULL DEFAULT 'sum', config_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_aggregations_status ON analytics_aggregations(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_aggregation_results (
    id SERIAL PRIMARY KEY,
    result_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    aggregation_id INTEGER, result_json TEXT NOT NULL DEFAULT '{}', computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_aggregation_results_status ON analytics_aggregation_results(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_dimensions (
    id SERIAL PRIMARY KEY,
    dimension_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', dimension_type TEXT NOT NULL DEFAULT 'string', config_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_dimensions_status ON analytics_dimensions(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_measures (
    id SERIAL PRIMARY KEY,
    measure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', measure_type TEXT NOT NULL DEFAULT 'count', expression TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_analytics_measures_status ON analytics_measures(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_filters (
    id SERIAL PRIMARY KEY,
    filter_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', filter_type TEXT NOT NULL DEFAULT 'equals', expression_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_filters_status ON analytics_filters(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_queries (
    id SERIAL PRIMARY KEY,
    query_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', query_type TEXT NOT NULL DEFAULT 'aggregate', query_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_queries_status ON analytics_queries(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_query_results (
    id SERIAL PRIMARY KEY,
    result_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    query_id INTEGER, result_json TEXT NOT NULL DEFAULT '{}', executed_at TEXT NOT NULL, duration_ms REAL NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_analytics_query_results_status ON analytics_query_results(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_kpi_definitions (
    id SERIAL PRIMARY KEY,
    kpi_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', category TEXT NOT NULL DEFAULT 'general', formula_json TEXT NOT NULL DEFAULT '{}', source_program TEXT NOT NULL DEFAULT 'global'
);

CREATE INDEX IF NOT EXISTS idx_analytics_kpi_definitions_status ON analytics_kpi_definitions(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_kpi_values (
    id SERIAL PRIMARY KEY,
    value_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, value REAL NOT NULL DEFAULT 0, period TEXT NOT NULL DEFAULT 'daily', computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_kpi_values_status ON analytics_kpi_values(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_kpi_targets (
    id SERIAL PRIMARY KEY,
    target_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, target_value REAL NOT NULL DEFAULT 0, period TEXT NOT NULL DEFAULT 'monthly', effective_from TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_kpi_targets_status ON analytics_kpi_targets(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_kpi_thresholds (
    id SERIAL PRIMARY KEY,
    threshold_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, threshold_type TEXT NOT NULL DEFAULT 'warning', min_value REAL, max_value REAL, config_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_kpi_thresholds_status ON analytics_kpi_thresholds(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_kpi_alerts (
    id SERIAL PRIMARY KEY,
    alert_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, alert_type TEXT NOT NULL DEFAULT 'threshold', severity TEXT NOT NULL DEFAULT 'warning', message TEXT NOT NULL DEFAULT '', triggered_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_kpi_alerts_status ON analytics_kpi_alerts(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_kpi_history (
    id SERIAL PRIMARY KEY,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, value REAL NOT NULL DEFAULT 0, period TEXT NOT NULL DEFAULT 'daily', recorded_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_kpi_history_status ON analytics_kpi_history(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_kpi_categories (
    id SERIAL PRIMARY KEY,
    category_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', description TEXT NOT NULL DEFAULT '', parent_key TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_analytics_kpi_categories_status ON analytics_kpi_categories(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_dashboards (
    id SERIAL PRIMARY KEY,
    dashboard_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', dashboard_type TEXT NOT NULL DEFAULT 'custom', layout_json TEXT NOT NULL DEFAULT '{}', owner_user_id INTEGER,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_dashboards_status ON analytics_dashboards(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_dashboard_widgets (
    id SERIAL PRIMARY KEY,
    widget_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, widget_type TEXT NOT NULL DEFAULT 'metric', config_json TEXT NOT NULL DEFAULT '{}', position_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_widgets_status ON analytics_dashboard_widgets(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_dashboard_layouts (
    id SERIAL PRIMARY KEY,
    layout_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, layout_json TEXT NOT NULL DEFAULT '{}', version INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_layouts_status ON analytics_dashboard_layouts(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_dashboard_filters (
    id SERIAL PRIMARY KEY,
    filter_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, filter_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_filters_status ON analytics_dashboard_filters(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_dashboard_permissions (
    id SERIAL PRIMARY KEY,
    permission_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, user_id INTEGER, role TEXT NOT NULL DEFAULT 'viewer', granted_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_permissions_status ON analytics_dashboard_permissions(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_dashboard_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, snapshot_json TEXT NOT NULL DEFAULT '{}', snapshot_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_snapshots_status ON analytics_dashboard_snapshots(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_dashboard_exports (
    id SERIAL PRIMARY KEY,
    export_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, format TEXT NOT NULL DEFAULT 'json', file_path TEXT NOT NULL DEFAULT '', exported_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_exports_status ON analytics_dashboard_exports(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_reports (
    id SERIAL PRIMARY KEY,
    report_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', report_type TEXT NOT NULL DEFAULT 'standard', config_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_reports_status ON analytics_reports(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_report_templates (
    id SERIAL PRIMARY KEY,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', format TEXT NOT NULL DEFAULT 'html', template_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_report_templates_status ON analytics_report_templates(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_report_sections (
    id SERIAL PRIMARY KEY,
    section_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, section_type TEXT NOT NULL DEFAULT 'summary', content_json TEXT NOT NULL DEFAULT '{}', sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_analytics_report_sections_status ON analytics_report_sections(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_report_runs (
    id SERIAL PRIMARY KEY,
    run_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, run_status TEXT NOT NULL DEFAULT 'pending', started_at TEXT NOT NULL, completed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_analytics_report_runs_status ON analytics_report_runs(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_report_outputs (
    id SERIAL PRIMARY KEY,
    output_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    run_id INTEGER, format TEXT NOT NULL DEFAULT 'json', output_json TEXT NOT NULL DEFAULT '{}', generated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_report_outputs_status ON analytics_report_outputs(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_report_schedules (
    id SERIAL PRIMARY KEY,
    schedule_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, cron_expression TEXT NOT NULL DEFAULT '0 0 * * *', next_run_at TEXT, enabled INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_analytics_report_schedules_status ON analytics_report_schedules(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_report_recipients (
    id SERIAL PRIMARY KEY,
    recipient_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    schedule_id INTEGER, user_id INTEGER, email TEXT NOT NULL DEFAULT '', delivery_format TEXT NOT NULL DEFAULT 'json',
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_report_recipients_status ON analytics_report_recipients(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_report_history (
    id SERIAL PRIMARY KEY,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, run_id INTEGER, summary_json TEXT NOT NULL DEFAULT '{}', recorded_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_report_history_status ON analytics_report_history(status, created_at);

CREATE TABLE IF NOT EXISTS bi_dimensions (
    id SERIAL PRIMARY KEY,
    dimension_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', hierarchy_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_bi_dimensions_status ON bi_dimensions(status, created_at);

CREATE TABLE IF NOT EXISTS bi_measures (
    id SERIAL PRIMARY KEY,
    measure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', aggregation TEXT NOT NULL DEFAULT 'sum', expression TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_bi_measures_status ON bi_measures(status, created_at);

CREATE TABLE IF NOT EXISTS bi_cubes (
    id SERIAL PRIMARY KEY,
    cube_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', config_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_bi_cubes_status ON bi_cubes(status, created_at);

CREATE TABLE IF NOT EXISTS bi_cube_dimensions (
    id SERIAL PRIMARY KEY,
    link_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    cube_id INTEGER, dimension_id INTEGER, sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_bi_cube_dimensions_status ON bi_cube_dimensions(status, created_at);

CREATE TABLE IF NOT EXISTS bi_cube_measures (
    id SERIAL PRIMARY KEY,
    link_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    cube_id INTEGER, measure_id INTEGER, sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_bi_cube_measures_status ON bi_cube_measures(status, created_at);

CREATE TABLE IF NOT EXISTS bi_segments (
    id SERIAL PRIMARY KEY,
    segment_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', filter_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_bi_segments_status ON bi_segments(status, created_at);

CREATE TABLE IF NOT EXISTS bi_segment_members (
    id SERIAL PRIMARY KEY,
    member_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    segment_id INTEGER, entity_type TEXT NOT NULL DEFAULT 'user', entity_id INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_bi_segment_members_status ON bi_segment_members(status, created_at);

CREATE TABLE IF NOT EXISTS bi_benchmarks (
    id SERIAL PRIMARY KEY,
    benchmark_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', benchmark_type TEXT NOT NULL DEFAULT 'industry', value REAL NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_bi_benchmarks_status ON bi_benchmarks(status, created_at);

CREATE TABLE IF NOT EXISTS bi_drill_paths (
    id SERIAL PRIMARY KEY,
    path_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    cube_id INTEGER, path_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_bi_drill_paths_status ON bi_drill_paths(status, created_at);

CREATE TABLE IF NOT EXISTS bi_comparisons (
    id SERIAL PRIMARY KEY,
    comparison_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', comparison_type TEXT NOT NULL DEFAULT 'period', config_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_bi_comparisons_status ON bi_comparisons(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_data_marts (
    id SERIAL PRIMARY KEY,
    mart_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', mart_type TEXT NOT NULL DEFAULT 'crm', config_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_data_marts_status ON analytics_data_marts(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_data_mart_sources (
    id SERIAL PRIMARY KEY,
    source_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, source_program TEXT NOT NULL DEFAULT 'crm', source_table TEXT NOT NULL DEFAULT '', mapping_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_sources_status ON analytics_data_mart_sources(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_data_mart_fields (
    id SERIAL PRIMARY KEY,
    field_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, field_name TEXT NOT NULL DEFAULT '', field_type TEXT NOT NULL DEFAULT 'string', expression TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_fields_status ON analytics_data_mart_fields(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_data_mart_views (
    id SERIAL PRIMARY KEY,
    view_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, view_json TEXT NOT NULL DEFAULT '{}', refreshed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_views_status ON analytics_data_mart_views(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_data_mart_refreshes (
    id SERIAL PRIMARY KEY,
    refresh_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, refresh_status TEXT NOT NULL DEFAULT 'completed', started_at TEXT NOT NULL, completed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_refreshes_status ON analytics_data_mart_refreshes(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_data_mart_permissions (
    id SERIAL PRIMARY KEY,
    permission_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, user_id INTEGER, role TEXT NOT NULL DEFAULT 'viewer', granted_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_permissions_status ON analytics_data_mart_permissions(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_trends (
    id SERIAL PRIMARY KEY,
    trend_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', metric_key TEXT NOT NULL DEFAULT '', trend_type TEXT NOT NULL DEFAULT 'linear', config_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_trends_status ON analytics_trends(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_trend_points (
    id SERIAL PRIMARY KEY,
    point_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, value REAL NOT NULL DEFAULT 0, recorded_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_trend_points_status ON analytics_trend_points(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_anomalies (
    id SERIAL PRIMARY KEY,
    anomaly_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, anomaly_type TEXT NOT NULL DEFAULT 'spike', severity TEXT NOT NULL DEFAULT 'warning', detected_at TEXT NOT NULL, details_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_anomalies_status ON analytics_anomalies(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_forecasts (
    id SERIAL PRIMARY KEY,
    forecast_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, horizon_days INTEGER NOT NULL DEFAULT 30, model TEXT NOT NULL DEFAULT 'simple', config_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_forecasts_status ON analytics_forecasts(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_forecast_points (
    id SERIAL PRIMARY KEY,
    point_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    forecast_id INTEGER, value REAL NOT NULL DEFAULT 0, forecast_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_forecast_points_status ON analytics_forecast_points(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_seasonality_profiles (
    id SERIAL PRIMARY KEY,
    profile_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, profile_json TEXT NOT NULL DEFAULT '{}', computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_seasonality_profiles_status ON analytics_seasonality_profiles(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_score_definitions (
    id SERIAL PRIMARY KEY,
    score_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', score_type TEXT NOT NULL DEFAULT 'customer', formula_json TEXT NOT NULL DEFAULT '{}', source_program TEXT NOT NULL DEFAULT 'global'
);

CREATE INDEX IF NOT EXISTS idx_analytics_score_definitions_status ON analytics_score_definitions(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_score_values (
    id SERIAL PRIMARY KEY,
    value_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, entity_type TEXT NOT NULL DEFAULT 'contact', entity_id INTEGER NOT NULL DEFAULT 0, value REAL NOT NULL DEFAULT 0, computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_score_values_status ON analytics_score_values(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_score_components (
    id SERIAL PRIMARY KEY,
    component_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, component_name TEXT NOT NULL DEFAULT '', weight REAL NOT NULL DEFAULT 1, value REAL NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_analytics_score_components_status ON analytics_score_components(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_score_history (
    id SERIAL PRIMARY KEY,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, entity_id INTEGER NOT NULL DEFAULT 0, value REAL NOT NULL DEFAULT 0, recorded_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_score_history_status ON analytics_score_history(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_score_rules (
    id SERIAL PRIMARY KEY,
    rule_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, rule_type TEXT NOT NULL DEFAULT 'threshold', rule_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_analytics_score_rules_status ON analytics_score_rules(status, created_at);

CREATE TABLE IF NOT EXISTS executive_dashboard_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global', snapshot_json TEXT NOT NULL DEFAULT '{}', snapshot_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_executive_dashboard_snapshots_status ON executive_dashboard_snapshots(status, created_at);

CREATE TABLE IF NOT EXISTS executive_dashboard_kpis (
    id SERIAL PRIMARY KEY,
    kpi_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, display_name TEXT NOT NULL DEFAULT '', value REAL NOT NULL DEFAULT 0, trend TEXT NOT NULL DEFAULT 'stable'
);

CREATE INDEX IF NOT EXISTS idx_executive_dashboard_kpis_status ON executive_dashboard_kpis(status, created_at);

CREATE TABLE IF NOT EXISTS executive_dashboard_alerts (
    id SERIAL PRIMARY KEY,
    alert_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    alert_type TEXT NOT NULL DEFAULT 'info', severity TEXT NOT NULL DEFAULT 'info', message TEXT NOT NULL DEFAULT '', triggered_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_executive_dashboard_alerts_status ON executive_dashboard_alerts(status, created_at);

CREATE TABLE IF NOT EXISTS executive_dashboard_sections (
    id SERIAL PRIMARY KEY,
    section_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', section_type TEXT NOT NULL DEFAULT 'overview', content_json TEXT NOT NULL DEFAULT '{}', sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_executive_dashboard_sections_status ON executive_dashboard_sections(status, created_at);

CREATE TABLE IF NOT EXISTS realtime_event_streams (
    id SERIAL PRIMARY KEY,
    stream_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', source_program TEXT NOT NULL DEFAULT 'global', config_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_realtime_event_streams_status ON realtime_event_streams(status, created_at);

CREATE TABLE IF NOT EXISTS realtime_counters (
    id SERIAL PRIMARY KEY,
    counter_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, counter_name TEXT NOT NULL DEFAULT '', value INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_realtime_counters_status ON realtime_counters(status, created_at);

CREATE TABLE IF NOT EXISTS realtime_activity_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, activity_type TEXT NOT NULL DEFAULT 'event', payload_json TEXT NOT NULL DEFAULT '{}', logged_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_realtime_activity_logs_status ON realtime_activity_logs(status, created_at);

CREATE TABLE IF NOT EXISTS realtime_alerts (
    id SERIAL PRIMARY KEY,
    alert_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, alert_type TEXT NOT NULL DEFAULT 'threshold', severity TEXT NOT NULL DEFAULT 'warning', message TEXT NOT NULL DEFAULT '', triggered_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_realtime_alerts_status ON realtime_alerts(status, created_at);

CREATE TABLE IF NOT EXISTS realtime_sessions (
    id SERIAL PRIMARY KEY,
    session_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    user_id INTEGER, started_at TEXT NOT NULL, last_activity_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_realtime_sessions_status ON realtime_sessions(status, created_at);

CREATE TABLE IF NOT EXISTS realtime_processing_stats (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, events_processed INTEGER NOT NULL DEFAULT 0, avg_latency_ms REAL NOT NULL DEFAULT 0, recorded_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_realtime_processing_stats_status ON realtime_processing_stats(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_exports (
    id SERIAL PRIMARY KEY,
    export_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', export_type TEXT NOT NULL DEFAULT 'csv', config_json TEXT NOT NULL DEFAULT '{}', requested_by INTEGER,
    requested_by INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_exports_status ON analytics_exports(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_export_files (
    id SERIAL PRIMARY KEY,
    file_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, format TEXT NOT NULL DEFAULT 'csv', file_path TEXT NOT NULL DEFAULT '', size_bytes INTEGER NOT NULL DEFAULT 0, created_at_file TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_export_files_status ON analytics_export_files(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_export_jobs (
    id SERIAL PRIMARY KEY,
    job_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, job_status TEXT NOT NULL DEFAULT 'pending', started_at TEXT NOT NULL, completed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_analytics_export_jobs_status ON analytics_export_jobs(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_export_permissions (
    id SERIAL PRIMARY KEY,
    permission_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, user_id INTEGER, role TEXT NOT NULL DEFAULT 'viewer', granted_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_export_permissions_status ON analytics_export_permissions(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_export_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, action TEXT NOT NULL DEFAULT 'create', details_json TEXT NOT NULL DEFAULT '{}', logged_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_export_logs_status ON analytics_export_logs(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_ai_insights (
    id SERIAL PRIMARY KEY,
    insight_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    insight_type TEXT NOT NULL DEFAULT 'trend', title TEXT NOT NULL DEFAULT '', content_json TEXT NOT NULL DEFAULT '{}', confidence REAL NOT NULL DEFAULT 0, generated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_ai_insights_status ON analytics_ai_insights(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_ai_recommendations (
    id SERIAL PRIMARY KEY,
    recommendation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    recommendation_type TEXT NOT NULL DEFAULT 'action', title TEXT NOT NULL DEFAULT '', content_json TEXT NOT NULL DEFAULT '{}', score REAL NOT NULL DEFAULT 0, generated_at TEXT NOT NULL, user_id INTEGER,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_ai_recommendations_status ON analytics_ai_recommendations(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_ai_anomaly_reviews (
    id SERIAL PRIMARY KEY,
    review_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    anomaly_id INTEGER, review_status TEXT NOT NULL DEFAULT 'pending', reviewer_user_id INTEGER, notes TEXT NOT NULL DEFAULT '', reviewed_at TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_ai_anomaly_reviews_status ON analytics_ai_anomaly_reviews(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_ai_forecasts (
    id SERIAL PRIMARY KEY,
    forecast_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metric_key TEXT NOT NULL DEFAULT '', horizon_days INTEGER NOT NULL DEFAULT 30, forecast_json TEXT NOT NULL DEFAULT '{}', generated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_ai_forecasts_status ON analytics_ai_forecasts(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_ai_explanations (
    id SERIAL PRIMARY KEY,
    explanation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, explanation_text TEXT NOT NULL DEFAULT '', generated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_ai_explanations_status ON analytics_ai_explanations(status, created_at);

CREATE TABLE IF NOT EXISTS analytics_ai_feedback (
    id SERIAL PRIMARY KEY,
    feedback_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    insight_id INTEGER, user_id INTEGER, rating INTEGER NOT NULL DEFAULT 0, comment TEXT NOT NULL DEFAULT '', submitted_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_analytics_ai_feedback_status ON analytics_ai_feedback(status, created_at);

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
    );

CREATE INDEX IF NOT EXISTS idx_source_intelligence_contexts_source ON source_intelligence_source_contexts(source_id, updated_at);

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
    );

CREATE INDEX IF NOT EXISTS idx_source_intelligence_imports_source ON source_intelligence_imports(source_id, imported_at);

CREATE INDEX IF NOT EXISTS idx_source_intelligence_imports_status ON source_intelligence_imports(import_status, imported_at);

CREATE TABLE IF NOT EXISTS operations (
    id SERIAL PRIMARY KEY,
    record_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL DEFAULT '',
    kind TEXT NOT NULL DEFAULT '',
    scope TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    parent_id INTEGER,
    reference_id INTEGER,
    secondary_id INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_operations_status ON operations(status, created_at);

CREATE INDEX IF NOT EXISTS idx_operations_record_key ON operations(record_key);

CREATE TABLE IF NOT EXISTS deployment (
    id SERIAL PRIMARY KEY,
    record_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL DEFAULT '',
    kind TEXT NOT NULL DEFAULT '',
    scope TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    parent_id INTEGER,
    reference_id INTEGER,
    secondary_id INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_deployment_status ON deployment(status, created_at);

CREATE INDEX IF NOT EXISTS idx_deployment_record_key ON deployment(record_key);

CREATE TABLE IF NOT EXISTS backup (
    id SERIAL PRIMARY KEY,
    record_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL DEFAULT '',
    kind TEXT NOT NULL DEFAULT '',
    scope TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    parent_id INTEGER,
    reference_id INTEGER,
    secondary_id INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_backup_status ON backup(status, created_at);

CREATE INDEX IF NOT EXISTS idx_backup_record_key ON backup(record_key);

CREATE TABLE IF NOT EXISTS installer (
    id SERIAL PRIMARY KEY,
    record_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL DEFAULT '',
    kind TEXT NOT NULL DEFAULT '',
    scope TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    parent_id INTEGER,
    reference_id INTEGER,
    secondary_id INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_installer_status ON installer(status, created_at);

CREATE INDEX IF NOT EXISTS idx_installer_record_key ON installer(record_key);

CREATE TABLE IF NOT EXISTS releases (
    id SERIAL PRIMARY KEY,
    record_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL DEFAULT '',
    kind TEXT NOT NULL DEFAULT '',
    scope TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    parent_id INTEGER,
    reference_id INTEGER,
    secondary_id INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_releases_status ON releases(status, created_at);

CREATE INDEX IF NOT EXISTS idx_releases_record_key ON releases(record_key);
