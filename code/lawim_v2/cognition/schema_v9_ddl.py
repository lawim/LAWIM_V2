"""Schema v9 DDL extensions for knowledge, decision and reasoning platform."""

V9_TABLE_NAMES: tuple[str, ...] = (
    "knowledge_nodes",
    "knowledge_edges",
    "knowledge_relations",
    "knowledge_snapshots",
    "knowledge_inferences",
    "knowledge_history",
    "cognition_decisions",
    "decision_evidences",
    "decision_histories",
    "simulation_runs",
    "reasoning_traces",
    "next_best_actions",
    "risk_intelligence_scores",
    "opportunity_intelligence_scores",
    "intelligence_snapshots",
)

POSTGRESQL_V9_STATEMENTS: tuple[str, ...] = (
    """
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
    )
    """,
    """
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
    )
    """,
    """
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
    )
    """,
    """
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
    )
    """,
    """
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
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS knowledge_history (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        node_id INTEGER REFERENCES knowledge_nodes(id) ON DELETE SET NULL,
        change_type TEXT NOT NULL,
        before_json TEXT NOT NULL DEFAULT '{}',
        after_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    )
    """,
    """
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
    )
    """,
    """
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
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS decision_histories (
        id SERIAL PRIMARY KEY,
        decision_id INTEGER NOT NULL REFERENCES cognition_decisions(id) ON DELETE CASCADE,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        from_status TEXT,
        to_status TEXT NOT NULL,
        note TEXT,
        created_at TEXT NOT NULL
    )
    """,
    """
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
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS reasoning_traces (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        trace_key TEXT NOT NULL,
        rules_fired_json TEXT NOT NULL DEFAULT '[]',
        conclusions_json TEXT NOT NULL DEFAULT '[]',
        merged_priority_json TEXT NOT NULL DEFAULT '[]',
        created_at TEXT NOT NULL,
        UNIQUE (project_id, trace_key)
    )
    """,
    """
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
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS risk_intelligence_scores (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        risk_key TEXT NOT NULL,
        severity TEXT NOT NULL DEFAULT 'medium',
        likelihood TEXT NOT NULL DEFAULT 'medium',
        score INTEGER NOT NULL DEFAULT 50,
        mitigation_json TEXT NOT NULL DEFAULT '[]',
        computed_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS opportunity_intelligence_scores (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        opportunity_key TEXT NOT NULL,
        value_score INTEGER NOT NULL DEFAULT 50,
        opportunity_score INTEGER NOT NULL DEFAULT 50,
        description TEXT NOT NULL,
        computed_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS intelligence_snapshots (
        id SERIAL PRIMARY KEY,
        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        snapshot_key TEXT NOT NULL,
        payload_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        UNIQUE (project_id, snapshot_key)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_knowledge_nodes_project ON knowledge_nodes(project_id, node_type)",
    "CREATE INDEX IF NOT EXISTS idx_knowledge_edges_project ON knowledge_edges(project_id, edge_type)",
    "CREATE INDEX IF NOT EXISTS idx_cognition_decisions_project ON cognition_decisions(project_id, status)",
    "CREATE INDEX IF NOT EXISTS idx_next_best_actions_project ON next_best_actions(project_id, status, score)",
    "CREATE INDEX IF NOT EXISTS idx_simulation_runs_project ON simulation_runs(project_id, scenario_key)",
    "CREATE INDEX IF NOT EXISTS idx_reasoning_traces_project ON reasoning_traces(project_id, created_at)",
)

SQLITE_V9_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS knowledge_nodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    node_key TEXT NOT NULL,
    node_type TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id INTEGER,
    title TEXT NOT NULL,
    content_json TEXT NOT NULL DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, node_key)
);

CREATE TABLE IF NOT EXISTS knowledge_edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    source_node_id INTEGER NOT NULL,
    target_node_id INTEGER NOT NULL,
    edge_type TEXT NOT NULL,
    weight INTEGER NOT NULL DEFAULT 50,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (source_node_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
    FOREIGN KEY (target_node_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
    UNIQUE (project_id, source_node_id, target_node_id, edge_type)
);

CREATE TABLE IF NOT EXISTS knowledge_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    relation_key TEXT NOT NULL,
    subject_node_id INTEGER NOT NULL,
    object_node_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL,
    confidence INTEGER NOT NULL DEFAULT 50,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_node_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
    FOREIGN KEY (object_node_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
    UNIQUE (project_id, relation_key)
);

CREATE TABLE IF NOT EXISTS knowledge_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    snapshot_key TEXT NOT NULL,
    graph_json TEXT NOT NULL DEFAULT '{}',
    node_count INTEGER NOT NULL DEFAULT 0,
    edge_count INTEGER NOT NULL DEFAULT 0,
    relation_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, snapshot_key)
);

CREATE TABLE IF NOT EXISTS knowledge_inferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    inference_key TEXT NOT NULL,
    premise_json TEXT NOT NULL DEFAULT '[]',
    conclusion TEXT NOT NULL,
    confidence INTEGER NOT NULL DEFAULT 50,
    rule_key TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, inference_key)
);

CREATE TABLE IF NOT EXISTS knowledge_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    node_id INTEGER,
    change_type TEXT NOT NULL,
    before_json TEXT NOT NULL DEFAULT '{}',
    after_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (node_id) REFERENCES knowledge_nodes(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS cognition_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
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
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, decision_key)
);

CREATE TABLE IF NOT EXISTS decision_evidences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    evidence_key TEXT NOT NULL,
    label TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_id INTEGER,
    weight INTEGER NOT NULL DEFAULT 50,
    content_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (decision_id) REFERENCES cognition_decisions(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS decision_histories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    from_status TEXT,
    to_status TEXT NOT NULL,
    note TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (decision_id) REFERENCES cognition_decisions(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS simulation_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    scenario_key TEXT NOT NULL,
    title TEXT NOT NULL,
    input_json TEXT NOT NULL DEFAULT '{}',
    output_json TEXT NOT NULL DEFAULT '{}',
    impacts_json TEXT NOT NULL DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'completed',
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reasoning_traces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    trace_key TEXT NOT NULL,
    rules_fired_json TEXT NOT NULL DEFAULT '[]',
    conclusions_json TEXT NOT NULL DEFAULT '[]',
    merged_priority_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, trace_key)
);

CREATE TABLE IF NOT EXISTS next_best_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
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
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, action_key)
);

CREATE TABLE IF NOT EXISTS risk_intelligence_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    risk_key TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'medium',
    likelihood TEXT NOT NULL DEFAULT 'medium',
    score INTEGER NOT NULL DEFAULT 50,
    mitigation_json TEXT NOT NULL DEFAULT '[]',
    computed_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS opportunity_intelligence_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    opportunity_key TEXT NOT NULL,
    value_score INTEGER NOT NULL DEFAULT 50,
    opportunity_score INTEGER NOT NULL DEFAULT 50,
    description TEXT NOT NULL,
    computed_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS intelligence_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    snapshot_key TEXT NOT NULL,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE (project_id, snapshot_key)
);

CREATE INDEX IF NOT EXISTS idx_knowledge_nodes_project ON knowledge_nodes(project_id, node_type);
CREATE INDEX IF NOT EXISTS idx_knowledge_edges_project ON knowledge_edges(project_id, edge_type);
CREATE INDEX IF NOT EXISTS idx_cognition_decisions_project ON cognition_decisions(project_id, status);
CREATE INDEX IF NOT EXISTS idx_next_best_actions_project ON next_best_actions(project_id, status, score);
CREATE INDEX IF NOT EXISTS idx_simulation_runs_project ON simulation_runs(project_id, scenario_key);
CREATE INDEX IF NOT EXISTS idx_reasoning_traces_project ON reasoning_traces(project_id, created_at);
"""

SQLITE_V9_SCRIPT = SQLITE_V9_TABLES_SCRIPT
