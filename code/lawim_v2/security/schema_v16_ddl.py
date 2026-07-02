"""Schema v16 DDL — Security platform (RELEASE PROGRAM J)."""

V16_TABLE_NAMES: tuple[str, ...] = (
    "iam_roles",
    "iam_permissions",
    "iam_role_permissions",
    "iam_user_roles",
    "iam_groups",
    "iam_group_members",
    "iam_teams",
    "iam_team_members",
    "iam_access_policies",
    "iam_policy_bindings",
    "access_devices",
    "access_api_keys",
    "access_session_records",
    "access_route_policies",
    "access_mfa_enrollments",
    "access_token_rotations",
    "audit_trail_entries",
    "audit_system_events",
    "audit_user_events",
    "audit_admin_events",
    "audit_ai_events",
    "compliance_policies",
    "compliance_consents",
    "compliance_retention_rules",
    "compliance_deletion_requests",
    "privacy_data_exports",
    "privacy_erasure_requests",
    "risk_signals",
    "risk_scores",
    "risk_alerts",
    "security_incidents",
    "security_analytics_snapshots",
)

SQLITE_V16_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS iam_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS iam_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    resource TEXT NOT NULL DEFAULT '*',
    action TEXT NOT NULL DEFAULT 'read',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS iam_role_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    granted_at TEXT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES iam_roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES iam_permissions(id) ON DELETE CASCADE,
    UNIQUE (role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS iam_user_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    assigned_by INTEGER,
    assigned_at TEXT NOT NULL,
    expires_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES iam_roles(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS iam_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    organization_id INTEGER,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS iam_group_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role_in_group TEXT NOT NULL DEFAULT 'member',
    joined_at TEXT NOT NULL,
    FOREIGN KEY (group_id) REFERENCES iam_groups(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (group_id, user_id)
);

CREATE TABLE IF NOT EXISTS iam_teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    organization_id INTEGER,
    leader_user_id INTEGER,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE SET NULL,
    FOREIGN KEY (leader_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS iam_team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role_in_team TEXT NOT NULL DEFAULT 'member',
    joined_at TEXT NOT NULL,
    FOREIGN KEY (team_id) REFERENCES iam_teams(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (team_id, user_id)
);

CREATE TABLE IF NOT EXISTS iam_access_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_id INTEGER NOT NULL,
    binding_type TEXT NOT NULL DEFAULT 'role',
    binding_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (policy_id) REFERENCES iam_access_policies(id) ON DELETE CASCADE,
    UNIQUE (policy_id, binding_type, binding_id)
);

CREATE TABLE IF NOT EXISTS access_devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_key TEXT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    device_type TEXT NOT NULL DEFAULT 'browser',
    device_name TEXT NOT NULL DEFAULT '',
    fingerprint TEXT NOT NULL DEFAULT '',
    trust_level TEXT NOT NULL DEFAULT 'unknown',
    last_seen_at TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS access_api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_key_key TEXT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    organization_id INTEGER,
    name TEXT NOT NULL,
    key_prefix TEXT NOT NULL DEFAULT '',
    key_hash TEXT NOT NULL DEFAULT '',
    scopes_json TEXT NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'active',
    expires_at TEXT,
    last_used_at TEXT,
    created_at TEXT NOT NULL,
    revoked_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS access_session_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_key TEXT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    session_token TEXT,
    device_id INTEGER,
    ip_address TEXT NOT NULL DEFAULT '',
    user_agent TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    started_at TEXT NOT NULL,
    expires_at TEXT,
    revoked_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (session_token) REFERENCES sessions(token) ON DELETE SET NULL,
    FOREIGN KEY (device_id) REFERENCES access_devices(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS access_route_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_key TEXT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    mfa_type TEXT NOT NULL DEFAULT 'totp',
    secret_ref TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    enrolled_at TEXT,
    last_used_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS access_token_rotations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rotation_key TEXT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    token_type TEXT NOT NULL DEFAULT 'session',
    old_token_ref TEXT NOT NULL DEFAULT '',
    new_token_ref TEXT NOT NULL DEFAULT '',
    rotated_at TEXT NOT NULL,
    reason TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS audit_trail_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_key TEXT NOT NULL UNIQUE,
    event_type TEXT NOT NULL DEFAULT 'system',
    actor_user_id INTEGER,
    resource_type TEXT NOT NULL DEFAULT '',
    resource_id INTEGER,
    action TEXT NOT NULL DEFAULT '',
    severity TEXT NOT NULL DEFAULT 'info',
    payload_json TEXT NOT NULL DEFAULT '{}',
    checksum TEXT NOT NULL DEFAULT '',
    previous_checksum TEXT NOT NULL DEFAULT '',
    ip_address TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    FOREIGN KEY (actor_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS audit_system_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_key TEXT NOT NULL UNIQUE,
    trail_entry_id INTEGER,
    component TEXT NOT NULL DEFAULT 'platform',
    message TEXT NOT NULL DEFAULT '',
    severity TEXT NOT NULL DEFAULT 'info',
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (trail_entry_id) REFERENCES audit_trail_entries(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS audit_user_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_key TEXT NOT NULL UNIQUE,
    trail_entry_id INTEGER,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (trail_entry_id) REFERENCES audit_trail_entries(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS audit_admin_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_key TEXT NOT NULL UNIQUE,
    trail_entry_id INTEGER,
    admin_user_id INTEGER NOT NULL,
    action TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (trail_entry_id) REFERENCES audit_trail_entries(id) ON DELETE SET NULL,
    FOREIGN KEY (admin_user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS audit_ai_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_key TEXT NOT NULL UNIQUE,
    trail_entry_id INTEGER,
    assistant_session_id INTEGER,
    action TEXT NOT NULL DEFAULT '',
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (trail_entry_id) REFERENCES audit_trail_entries(id) ON DELETE SET NULL,
    FOREIGN KEY (assistant_session_id) REFERENCES assistant_sessions(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS compliance_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consent_key TEXT NOT NULL UNIQUE,
    user_id INTEGER,
    contact_id INTEGER,
    consent_type TEXT NOT NULL DEFAULT 'terms',
    status TEXT NOT NULL DEFAULT 'pending',
    granted_at TEXT,
    revoked_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS compliance_retention_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_key TEXT NOT NULL UNIQUE,
    user_id INTEGER,
    contact_id INTEGER,
    deletion_type TEXT NOT NULL DEFAULT 'soft_delete',
    status TEXT NOT NULL DEFAULT 'pending',
    requested_at TEXT NOT NULL,
    completed_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS privacy_data_exports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    export_key TEXT NOT NULL UNIQUE,
    user_id INTEGER,
    contact_id INTEGER,
    format TEXT NOT NULL DEFAULT 'json',
    scope_json TEXT NOT NULL DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'pending',
    storage_ref TEXT NOT NULL DEFAULT '',
    requested_at TEXT NOT NULL,
    completed_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS privacy_erasure_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_key TEXT NOT NULL UNIQUE,
    user_id INTEGER,
    contact_id INTEGER,
    scope_json TEXT NOT NULL DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'pending',
    requested_at TEXT NOT NULL,
    completed_at TEXT,
    validation_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (contact_id) REFERENCES crm_contact_profiles(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS risk_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_key TEXT NOT NULL UNIQUE,
    user_id INTEGER,
    signal_type TEXT NOT NULL DEFAULT 'login_anomaly',
    severity TEXT NOT NULL DEFAULT 'medium',
    score_delta INTEGER NOT NULL DEFAULT 10,
    source TEXT NOT NULL DEFAULT 'platform',
    payload_json TEXT NOT NULL DEFAULT '{}',
    detected_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS risk_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    score_key TEXT NOT NULL DEFAULT 'overall',
    score INTEGER NOT NULL DEFAULT 0,
    level TEXT NOT NULL DEFAULT 'low',
    factors_json TEXT NOT NULL DEFAULT '{}',
    computed_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (user_id, score_key)
);

CREATE TABLE IF NOT EXISTS risk_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_key TEXT NOT NULL UNIQUE,
    user_id INTEGER,
    signal_id INTEGER,
    level TEXT NOT NULL DEFAULT 'medium',
    title TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'open',
    acknowledged_by INTEGER,
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (signal_id) REFERENCES risk_signals(id) ON DELETE SET NULL,
    FOREIGN KEY (acknowledged_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS security_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'medium',
    status TEXT NOT NULL DEFAULT 'open',
    reported_by INTEGER,
    assigned_to INTEGER,
    description TEXT NOT NULL DEFAULT '',
    resolution TEXT NOT NULL DEFAULT '',
    opened_at TEXT NOT NULL,
    resolved_at TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (reported_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS security_analytics_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
"""

POSTGRESQL_V16_STATEMENTS: tuple[str, ...] = tuple(
    stmt.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
    for stmt in (
        """
        CREATE TABLE IF NOT EXISTS iam_roles (
            id SERIAL PRIMARY KEY,
            role_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'active',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS iam_permissions (
            id SERIAL PRIMARY KEY,
            permission_key TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            resource TEXT NOT NULL DEFAULT '*',
            action TEXT NOT NULL DEFAULT 'read',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS iam_role_permissions (
            id SERIAL PRIMARY KEY,
            role_id INTEGER NOT NULL REFERENCES iam_roles(id) ON DELETE CASCADE,
            permission_id INTEGER NOT NULL REFERENCES iam_permissions(id) ON DELETE CASCADE,
            granted_at TEXT NOT NULL,
            UNIQUE (role_id, permission_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS iam_user_roles (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role_id INTEGER NOT NULL REFERENCES iam_roles(id) ON DELETE CASCADE,
            assigned_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
            assigned_at TEXT NOT NULL,
            expires_at TEXT,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            UNIQUE (user_id, role_id)
        )
        """,
        """
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
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS iam_group_members (
            id SERIAL PRIMARY KEY,
            group_id INTEGER NOT NULL REFERENCES iam_groups(id) ON DELETE CASCADE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role_in_group TEXT NOT NULL DEFAULT 'member',
            joined_at TEXT NOT NULL,
            UNIQUE (group_id, user_id)
        )
        """,
        """
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
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS iam_team_members (
            id SERIAL PRIMARY KEY,
            team_id INTEGER NOT NULL REFERENCES iam_teams(id) ON DELETE CASCADE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role_in_team TEXT NOT NULL DEFAULT 'member',
            joined_at TEXT NOT NULL,
            UNIQUE (team_id, user_id)
        )
        """,
        """
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
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS iam_policy_bindings (
            id SERIAL PRIMARY KEY,
            policy_id INTEGER NOT NULL REFERENCES iam_access_policies(id) ON DELETE CASCADE,
            binding_type TEXT NOT NULL DEFAULT 'role',
            binding_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE (policy_id, binding_type, binding_id)
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS audit_system_events (
            id SERIAL PRIMARY KEY,
            event_key TEXT NOT NULL UNIQUE,
            trail_entry_id INTEGER REFERENCES audit_trail_entries(id) ON DELETE SET NULL,
            component TEXT NOT NULL DEFAULT 'platform',
            message TEXT NOT NULL DEFAULT '',
            severity TEXT NOT NULL DEFAULT 'info',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS audit_user_events (
            id SERIAL PRIMARY KEY,
            event_key TEXT NOT NULL UNIQUE,
            trail_entry_id INTEGER REFERENCES audit_trail_entries(id) ON DELETE SET NULL,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            action TEXT NOT NULL DEFAULT '',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS audit_admin_events (
            id SERIAL PRIMARY KEY,
            event_key TEXT NOT NULL UNIQUE,
            trail_entry_id INTEGER REFERENCES audit_trail_entries(id) ON DELETE SET NULL,
            admin_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            action TEXT NOT NULL DEFAULT '',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS audit_ai_events (
            id SERIAL PRIMARY KEY,
            event_key TEXT NOT NULL UNIQUE,
            trail_entry_id INTEGER REFERENCES audit_trail_entries(id) ON DELETE SET NULL,
            assistant_session_id INTEGER REFERENCES assistant_sessions(id) ON DELETE SET NULL,
            action TEXT NOT NULL DEFAULT '',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS risk_scores (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            score_key TEXT NOT NULL DEFAULT 'overall',
            score INTEGER NOT NULL DEFAULT 0,
            level TEXT NOT NULL DEFAULT 'low',
            factors_json TEXT NOT NULL DEFAULT '{}',
            computed_at TEXT NOT NULL,
            UNIQUE (user_id, score_key)
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS security_analytics_snapshots (
            id SERIAL PRIMARY KEY,
            snapshot_key TEXT NOT NULL UNIQUE,
            scope TEXT NOT NULL DEFAULT 'global',
            metrics_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        "CREATE INDEX IF NOT EXISTS idx_iam_user_roles_user ON iam_user_roles(user_id, role_id)",
        "CREATE INDEX IF NOT EXISTS idx_iam_role_permissions_role ON iam_role_permissions(role_id)",
        "CREATE INDEX IF NOT EXISTS idx_access_devices_user ON access_devices(user_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_access_api_keys_user ON access_api_keys(user_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_access_session_records_user ON access_session_records(user_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_audit_trail_created ON audit_trail_entries(created_at, event_type)",
        "CREATE INDEX IF NOT EXISTS idx_compliance_consents_user ON compliance_consents(user_id, consent_type)",
        "CREATE INDEX IF NOT EXISTS idx_risk_signals_user ON risk_signals(user_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_risk_scores_user ON risk_scores(user_id, score_key)",
        "CREATE INDEX IF NOT EXISTS idx_security_incidents_status ON security_incidents(status, opened_at)",
    )
)
