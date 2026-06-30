-- LAWIM_V2 schema v5 initial migration (generated from code/lawim_v2/schema_ddl.py; aligned with persistence manifest)

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
