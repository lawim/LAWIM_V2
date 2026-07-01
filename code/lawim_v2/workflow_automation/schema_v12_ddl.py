"""Schema v12 DDL — workflow automation platform (RELEASE PROGRAM F)."""

V12_TABLE_NAMES: tuple[str, ...] = (
    "automation_workflow_definitions",
    "automation_templates",
    "automation_process_instances",
    "automation_executions",
    "automation_states",
    "automation_transitions",
    "automation_tasks",
    "automation_queues",
    "automation_queue_items",
    "automation_events",
    "automation_schedules",
    "automation_timers",
    "automation_retries",
    "automation_escalations",
    "automation_approvals",
    "automation_rules",
    "automation_rule_bindings",
    "automation_notifications",
    "automation_audit_log",
    "automation_history",
    "automation_sla_policies",
    "automation_metrics_snapshots",
)

POSTGRESQL_V12_STATEMENTS: tuple[str, ...] = tuple(
    f"""
    CREATE TABLE IF NOT EXISTS {name} (
        id SERIAL PRIMARY KEY,
        created_at TEXT NOT NULL DEFAULT ''
    )
    """
    for name in V12_TABLE_NAMES
)

# Full DDL — SQLite script (source of truth for column definitions).

SQLITE_V12_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS automation_workflow_definitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_key TEXT NOT NULL UNIQUE,
    workflow_key TEXT NOT NULL,
    title TEXT NOT NULL,
    domain TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    steps_json TEXT NOT NULL DEFAULT '[]',
    variables_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (workflow_key) REFERENCES automation_workflow_definitions(workflow_key) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS automation_process_instances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instance_key TEXT NOT NULL UNIQUE,
    workflow_key TEXT NOT NULL,
    project_id INTEGER,
    current_state_key TEXT NOT NULL DEFAULT 'start',
    status TEXT NOT NULL DEFAULT 'pending',
    context_json TEXT NOT NULL DEFAULT '{}',
    priority TEXT NOT NULL DEFAULT 'normal',
    started_at TEXT,
    completed_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS automation_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    execution_key TEXT NOT NULL UNIQUE,
    instance_id INTEGER NOT NULL,
    workflow_key TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    current_step_key TEXT,
    attempt INTEGER NOT NULL DEFAULT 1,
    error_message TEXT,
    context_json TEXT NOT NULL DEFAULT '{}',
    started_at TEXT,
    finished_at TEXT,
    duration_ms INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (instance_id) REFERENCES automation_process_instances(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS automation_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_key TEXT NOT NULL UNIQUE,
    instance_id INTEGER NOT NULL,
    execution_id INTEGER,
    title TEXT NOT NULL,
    task_type TEXT NOT NULL DEFAULT 'human',
    status TEXT NOT NULL DEFAULT 'pending',
    assignee_id INTEGER,
    priority TEXT NOT NULL DEFAULT 'normal',
    due_at TEXT,
    payload_json TEXT NOT NULL DEFAULT '{}',
    result_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    completed_at TEXT,
    FOREIGN KEY (instance_id) REFERENCES automation_process_instances(id) ON DELETE CASCADE,
    FOREIGN KEY (execution_id) REFERENCES automation_executions(id) ON DELETE SET NULL,
    FOREIGN KEY (assignee_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS automation_queues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    queue_key TEXT NOT NULL,
    item_key TEXT NOT NULL UNIQUE,
    priority TEXT NOT NULL DEFAULT 'normal',
    status TEXT NOT NULL DEFAULT 'queued',
    payload_json TEXT NOT NULL DEFAULT '{}',
    attempts INTEGER NOT NULL DEFAULT 0,
    scheduled_at TEXT,
    processed_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (queue_key) REFERENCES automation_queues(queue_key) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS automation_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_key TEXT NOT NULL UNIQUE,
    instance_id INTEGER,
    event_type TEXT NOT NULL,
    source TEXT NOT NULL DEFAULT 'engine',
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (instance_id) REFERENCES automation_process_instances(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS automation_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timer_key TEXT NOT NULL UNIQUE,
    instance_id INTEGER NOT NULL,
    fire_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    action_json TEXT NOT NULL DEFAULT '{}',
    fired_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (instance_id) REFERENCES automation_process_instances(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS automation_retries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    execution_id INTEGER NOT NULL,
    attempt INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'pending',
    backoff_seconds INTEGER NOT NULL DEFAULT 60,
    error_message TEXT,
    scheduled_at TEXT NOT NULL,
    executed_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (execution_id) REFERENCES automation_executions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS automation_escalations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    escalation_key TEXT NOT NULL UNIQUE,
    instance_id INTEGER NOT NULL,
    task_id INTEGER,
    level INTEGER NOT NULL DEFAULT 1,
    reason TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'open',
    escalated_to_id INTEGER,
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    FOREIGN KEY (instance_id) REFERENCES automation_process_instances(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES automation_tasks(id) ON DELETE SET NULL,
    FOREIGN KEY (escalated_to_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS automation_approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    approval_key TEXT NOT NULL UNIQUE,
    instance_id INTEGER NOT NULL,
    level INTEGER NOT NULL DEFAULT 1,
    approver_id INTEGER,
    status TEXT NOT NULL DEFAULT 'pending',
    note TEXT NOT NULL DEFAULT '',
    decided_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (instance_id) REFERENCES automation_process_instances(id) ON DELETE CASCADE,
    FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS automation_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_key TEXT NOT NULL,
    variable_key TEXT NOT NULL,
    binding_type TEXT NOT NULL DEFAULT 'context',
    default_value TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    FOREIGN KEY (rule_key) REFERENCES automation_rules(rule_key) ON DELETE CASCADE,
    UNIQUE (rule_key, variable_key)
);

CREATE TABLE IF NOT EXISTS automation_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    notification_key TEXT NOT NULL UNIQUE,
    instance_id INTEGER,
    channel TEXT NOT NULL DEFAULT 'in_app',
    recipient_id INTEGER,
    title TEXT NOT NULL,
    body TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    sent_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (instance_id) REFERENCES automation_process_instances(id) ON DELETE SET NULL,
    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS automation_audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_key TEXT NOT NULL UNIQUE,
    actor_id INTEGER,
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id INTEGER,
    detail_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (actor_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS automation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instance_id INTEGER NOT NULL,
    from_state_key TEXT,
    to_state_key TEXT NOT NULL,
    transition_key TEXT,
    actor_id INTEGER,
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    FOREIGN KEY (instance_id) REFERENCES automation_process_instances(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS automation_sla_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_key TEXT NOT NULL UNIQUE,
    workflow_key TEXT NOT NULL,
    step_key TEXT,
    target_hours INTEGER NOT NULL DEFAULT 48,
    escalation_level INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS automation_metrics_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
"""

# Replace placeholder PostgreSQL statements with real ones matching SQLite.
POSTGRESQL_V12_STATEMENTS = tuple(
    stmt.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
    .replace("INTEGER NOT NULL DEFAULT 0", "INTEGER NOT NULL DEFAULT 0")
    for stmt in (
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS automation_events (
            id SERIAL PRIMARY KEY,
            event_key TEXT NOT NULL UNIQUE,
            instance_id INTEGER REFERENCES automation_process_instances(id) ON DELETE SET NULL,
            event_type TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'engine',
            payload_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
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
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS automation_timers (
            id SERIAL PRIMARY KEY,
            timer_key TEXT NOT NULL UNIQUE,
            instance_id INTEGER NOT NULL REFERENCES automation_process_instances(id) ON DELETE CASCADE,
            fire_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            action_json TEXT NOT NULL DEFAULT '{}',
            fired_at TEXT,
            created_at TEXT NOT NULL
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
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
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS automation_rule_bindings (
            id SERIAL PRIMARY KEY,
            rule_key TEXT NOT NULL REFERENCES automation_rules(rule_key) ON DELETE CASCADE,
            variable_key TEXT NOT NULL,
            binding_type TEXT NOT NULL DEFAULT 'context',
            default_value TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            UNIQUE (rule_key, variable_key)
        )
        """,
        """
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
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS automation_audit_log (
            id SERIAL PRIMARY KEY,
            audit_key TEXT NOT NULL UNIQUE,
            actor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            action TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            resource_id INTEGER,
            detail_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS automation_history (
            id SERIAL PRIMARY KEY,
            instance_id INTEGER NOT NULL REFERENCES automation_process_instances(id) ON DELETE CASCADE,
            from_state_key TEXT,
            to_state_key TEXT NOT NULL,
            transition_key TEXT,
            actor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            note TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS automation_sla_policies (
            id SERIAL PRIMARY KEY,
            policy_key TEXT NOT NULL UNIQUE,
            workflow_key TEXT NOT NULL,
            step_key TEXT,
            target_hours INTEGER NOT NULL DEFAULT 48,
            escalation_level INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS automation_metrics_snapshots (
            id SERIAL PRIMARY KEY,
            snapshot_key TEXT NOT NULL UNIQUE,
            scope TEXT NOT NULL DEFAULT 'global',
            metrics_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        )
        """,
        "CREATE INDEX IF NOT EXISTS idx_automation_instances_project ON automation_process_instances(project_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_automation_executions_instance ON automation_executions(instance_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_automation_tasks_instance ON automation_tasks(instance_id, status)",
        "CREATE INDEX IF NOT EXISTS idx_automation_queue_items_queue ON automation_queue_items(queue_key, status, priority)",
        "CREATE INDEX IF NOT EXISTS idx_automation_events_instance ON automation_events(instance_id, event_type)",
        "CREATE INDEX IF NOT EXISTS idx_automation_history_instance ON automation_history(instance_id, created_at)",
        "CREATE INDEX IF NOT EXISTS idx_automation_workflows_domain ON automation_workflow_definitions(domain, status)",
    )
)
