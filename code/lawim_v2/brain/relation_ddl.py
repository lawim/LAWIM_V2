from __future__ import annotations

RELATION_TABLE_NAMES: tuple[str, ...] = (
    "brain_relation_proposals",
    "brain_relations",
)

PROPOSAL_STATUSES = (
    "detected", "proposed", "consulted", "accepted", "rejected",
    "deferred", "consent_pending", "relation_established",
    "contact_made", "appointment_scheduled", "in_progress",
    "completed", "no_follow_up", "expired", "cancelled",
)
PROPOSAL_STATUSES_SQL = ", ".join(f"'{s}'" for s in PROPOSAL_STATUSES)

RELATION_TYPES = (
    "person_to_property", "person_to_person", "person_to_partner",
    "project_to_project", "property_to_partner", "partner_to_partner",
)
RELATION_TYPES_SQL = ", ".join(f"'{t}'" for t in RELATION_TYPES)

POSTGRESQL_RELATION_STATEMENTS: tuple[str, ...] = (
    f"""
    CREATE TABLE IF NOT EXISTS brain_relation_proposals (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        relation_type TEXT NOT NULL CHECK (relation_type IN ({RELATION_TYPES_SQL})),
        target_type TEXT NOT NULL,
        target_id INTEGER NOT NULL,
        score INTEGER NOT NULL DEFAULT 50,
        justification TEXT NOT NULL,
        metadata_json TEXT NOT NULL DEFAULT '{{}}',
        status TEXT NOT NULL DEFAULT 'detected' CHECK (status IN ({PROPOSAL_STATUSES_SQL})),
        proposed_at TEXT,
        accepted_at TEXT,
        rejected_at TEXT,
        consent_requested_at TEXT,
        consent_granted_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS brain_relations (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        relation_type TEXT NOT NULL CHECK (relation_type IN ({RELATION_TYPES_SQL})),
        source_type TEXT NOT NULL,
        source_id INTEGER,
        target_type TEXT NOT NULL,
        target_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'established',
        metadata_json TEXT NOT NULL DEFAULT '{{}}',
        established_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_brain_proposals_project ON brain_relation_proposals(project_id, status)",
    "CREATE INDEX IF NOT EXISTS idx_brain_proposals_target ON brain_relation_proposals(target_type, target_id)",
    "CREATE INDEX IF NOT EXISTS idx_brain_relations_project ON brain_relations(project_id, relation_type)",
)

SQLITE_RELATION_TABLES_SCRIPT = f"""
CREATE TABLE IF NOT EXISTS brain_relation_proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL CHECK (relation_type IN ({RELATION_TYPES_SQL})),
    target_type TEXT NOT NULL,
    target_id INTEGER NOT NULL,
    score INTEGER NOT NULL DEFAULT 50,
    justification TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{{}}',
    status TEXT NOT NULL DEFAULT 'detected' CHECK (status IN ({PROPOSAL_STATUSES_SQL})),
    proposed_at TEXT,
    accepted_at TEXT,
    rejected_at TEXT,
    consent_requested_at TEXT,
    consent_granted_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS brain_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL CHECK (relation_type IN ({RELATION_TYPES_SQL})),
    source_type TEXT NOT NULL,
    source_id INTEGER,
    target_type TEXT NOT NULL,
    target_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'established',
    metadata_json TEXT NOT NULL DEFAULT '{{}}',
    established_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_brain_proposals_project ON brain_relation_proposals(project_id, status);
CREATE INDEX IF NOT EXISTS idx_brain_proposals_target ON brain_relation_proposals(target_type, target_id);
CREATE INDEX IF NOT EXISTS idx_brain_relations_project ON brain_relations(project_id, relation_type);
"""
