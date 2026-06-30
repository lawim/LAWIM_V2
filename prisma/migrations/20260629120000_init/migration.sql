-- LAWIM_V2 schema v6 initial migration (generated from code/lawim_v2/schema_ddl.py; aligned with persistence manifest)

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
