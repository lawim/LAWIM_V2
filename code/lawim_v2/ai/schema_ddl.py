from __future__ import annotations

AI_TABLE_NAMES: tuple[str, ...] = (
    "ai_providers",
    "ai_provider_credentials_metadata",
    "ai_provider_health",
    "ai_requests",
    "ai_responses",
    "ai_usage_daily",
    "ai_usage_monthly",
    "ai_alerts",
    "ai_circuit_breakers",
    "ai_routing_decisions",
    "ai_fallback_entries",
    "ai_fallback_usage",
    "ai_learning_candidates",
    "ai_learning_reviews",
    "ai_knowledge_versions",
    "ai_feedback",
    "ai_cost_estimates",
)

AI_TABLE_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS ai_providers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider_key TEXT NOT NULL UNIQUE,
        provider_name TEXT NOT NULL,
        credential_alias TEXT NOT NULL,
        secret_reference TEXT NOT NULL,
        enabled INTEGER NOT NULL DEFAULT 0,
        priority INTEGER NOT NULL DEFAULT 0,
        model TEXT NOT NULL DEFAULT '',
        base_url TEXT NOT NULL DEFAULT '',
        provider_role TEXT NOT NULL DEFAULT 'primary',
        status TEXT NOT NULL DEFAULT 'inactive',
        notes TEXT NOT NULL DEFAULT '',
        last_validated_at TEXT,
        last_success_at TEXT,
        last_failure_at TEXT,
        consecutive_failures INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_provider_credentials_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider_key TEXT NOT NULL UNIQUE,
        credential_alias TEXT NOT NULL,
        secret_reference TEXT NOT NULL,
        enabled INTEGER NOT NULL DEFAULT 0,
        priority INTEGER NOT NULL DEFAULT 0,
        model TEXT NOT NULL DEFAULT '',
        base_url TEXT NOT NULL DEFAULT '',
        last_validated_at TEXT,
        last_success_at TEXT,
        last_failure_at TEXT,
        status TEXT NOT NULL DEFAULT 'inactive',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_provider_health (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider_key TEXT NOT NULL UNIQUE,
        credential_alias TEXT NOT NULL,
        model TEXT NOT NULL DEFAULT '',
        state TEXT NOT NULL DEFAULT 'UNKNOWN',
        available INTEGER NOT NULL DEFAULT 0,
        checked_at TEXT NOT NULL,
        latency_ms INTEGER NOT NULL DEFAULT 0,
        error_type TEXT,
        error_code TEXT,
        credit_remaining REAL,
        credit_limit REAL,
        quota_status TEXT,
        last_success_at TEXT,
        last_failure_at TEXT,
        consecutive_failures INTEGER NOT NULL DEFAULT 0,
        details_json TEXT NOT NULL DEFAULT '{}',
        updated_at TEXT NOT NULL DEFAULT ''
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_key TEXT NOT NULL UNIQUE,
        conversation_key TEXT NOT NULL,
        channel TEXT NOT NULL,
        external_chat_id TEXT NOT NULL DEFAULT '',
        external_user_id TEXT NOT NULL DEFAULT '',
        message_id TEXT NOT NULL DEFAULT '',
        language TEXT NOT NULL DEFAULT 'fr',
        complexity TEXT NOT NULL DEFAULT 'simple',
        prompt_text TEXT NOT NULL DEFAULT '',
        sanitized_text TEXT NOT NULL DEFAULT '',
        context_json TEXT NOT NULL DEFAULT '[]',
        metadata_json TEXT NOT NULL DEFAULT '{}',
        provider_chain_json TEXT NOT NULL DEFAULT '[]',
        status TEXT NOT NULL DEFAULT 'pending',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_key TEXT NOT NULL,
        provider_key TEXT NOT NULL,
        model TEXT NOT NULL DEFAULT '',
        success INTEGER NOT NULL DEFAULT 0,
        content TEXT NOT NULL DEFAULT '',
        latency_ms INTEGER NOT NULL DEFAULT 0,
        input_tokens INTEGER NOT NULL DEFAULT 0,
        output_tokens INTEGER NOT NULL DEFAULT 0,
        estimated_cost REAL NOT NULL DEFAULT 0.0,
        finish_reason TEXT,
        error_type TEXT,
        error_code TEXT,
        retryable INTEGER NOT NULL DEFAULT 0,
        fallback_required INTEGER NOT NULL DEFAULT 0,
        provider_request_id TEXT,
        valid INTEGER NOT NULL DEFAULT 0,
        complete INTEGER NOT NULL DEFAULT 0,
        relevant INTEGER NOT NULL DEFAULT 0,
        safe INTEGER NOT NULL DEFAULT 0,
        well_formed INTEGER NOT NULL DEFAULT 0,
        confidence_score REAL NOT NULL DEFAULT 0.0,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_usage_daily (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider_key TEXT NOT NULL,
        period_day TEXT NOT NULL,
        requests_total INTEGER NOT NULL DEFAULT 0,
        requests_success INTEGER NOT NULL DEFAULT 0,
        requests_failed INTEGER NOT NULL DEFAULT 0,
        fallbacks_triggered INTEGER NOT NULL DEFAULT 0,
        input_tokens INTEGER NOT NULL DEFAULT 0,
        output_tokens INTEGER NOT NULL DEFAULT 0,
        estimated_cost REAL NOT NULL DEFAULT 0.0,
        rate_limit_errors INTEGER NOT NULL DEFAULT 0,
        authentication_errors INTEGER NOT NULL DEFAULT 0,
        timeouts INTEGER NOT NULL DEFAULT 0,
        empty_responses INTEGER NOT NULL DEFAULT 0,
        invalid_responses INTEGER NOT NULL DEFAULT 0,
        circuit_open_count INTEGER NOT NULL DEFAULT 0,
        last_success_at TEXT,
        last_failure_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE(provider_key, period_day)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_usage_monthly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider_key TEXT NOT NULL,
        period_month TEXT NOT NULL,
        requests_total INTEGER NOT NULL DEFAULT 0,
        requests_success INTEGER NOT NULL DEFAULT 0,
        requests_failed INTEGER NOT NULL DEFAULT 0,
        fallbacks_triggered INTEGER NOT NULL DEFAULT 0,
        input_tokens INTEGER NOT NULL DEFAULT 0,
        output_tokens INTEGER NOT NULL DEFAULT 0,
        estimated_cost REAL NOT NULL DEFAULT 0.0,
        rate_limit_errors INTEGER NOT NULL DEFAULT 0,
        authentication_errors INTEGER NOT NULL DEFAULT 0,
        timeouts INTEGER NOT NULL DEFAULT 0,
        empty_responses INTEGER NOT NULL DEFAULT 0,
        invalid_responses INTEGER NOT NULL DEFAULT 0,
        circuit_open_count INTEGER NOT NULL DEFAULT 0,
        last_success_at TEXT,
        last_failure_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE(provider_key, period_month)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_key TEXT NOT NULL UNIQUE,
        provider_key TEXT NOT NULL,
        severity TEXT NOT NULL DEFAULT 'info',
        alert_type TEXT NOT NULL DEFAULT 'general',
        message TEXT NOT NULL DEFAULT '',
        payload_json TEXT NOT NULL DEFAULT '{}',
        status TEXT NOT NULL DEFAULT 'open',
        created_at TEXT NOT NULL,
        acknowledged_at TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_circuit_breakers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider_key TEXT NOT NULL UNIQUE,
        credential_alias TEXT NOT NULL DEFAULT '',
        state TEXT NOT NULL DEFAULT 'CLOSED',
        failure_count INTEGER NOT NULL DEFAULT 0,
        success_count INTEGER NOT NULL DEFAULT 0,
        window_started_at TEXT,
        opened_at TEXT,
        closed_at TEXT,
        half_open_requests INTEGER NOT NULL DEFAULT 0,
        last_failure_at TEXT,
        last_success_at TEXT,
        last_checked_at TEXT,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        updated_at TEXT NOT NULL DEFAULT ''
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_routing_decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        routing_key TEXT NOT NULL UNIQUE,
        request_key TEXT NOT NULL,
        conversation_key TEXT NOT NULL,
        complexity TEXT NOT NULL DEFAULT 'simple',
        selected_provider TEXT NOT NULL DEFAULT '',
        fallback_used INTEGER NOT NULL DEFAULT 0,
        chain_json TEXT NOT NULL DEFAULT '[]',
        rationale_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_fallback_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fallback_key TEXT NOT NULL UNIQUE,
        intent TEXT NOT NULL,
        question TEXT NOT NULL DEFAULT '',
        variants_json TEXT NOT NULL DEFAULT '[]',
        keywords_json TEXT NOT NULL DEFAULT '[]',
        category TEXT NOT NULL DEFAULT 'general',
        language TEXT NOT NULL DEFAULT 'fr',
        channel TEXT NOT NULL DEFAULT 'all',
        response_text TEXT NOT NULL DEFAULT '',
        confidence REAL NOT NULL DEFAULT 0.0,
        validated_at TEXT,
        validated_by TEXT,
        version_number INTEGER NOT NULL DEFAULT 1,
        status TEXT NOT NULL DEFAULT 'published',
        expires_at TEXT,
        usage_count INTEGER NOT NULL DEFAULT 0,
        satisfaction_rate REAL NOT NULL DEFAULT 0.0,
        risk_level TEXT NOT NULL DEFAULT 'low',
        source_type TEXT NOT NULL DEFAULT 'manual',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_fallback_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usage_key TEXT NOT NULL UNIQUE,
        request_key TEXT NOT NULL,
        fallback_key TEXT,
        used_generic INTEGER NOT NULL DEFAULT 0,
        response_text TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_learning_candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_key TEXT NOT NULL UNIQUE,
        intent TEXT NOT NULL,
        question_examples_json TEXT NOT NULL DEFAULT '[]',
        proposed_answer TEXT NOT NULL DEFAULT '',
        source_count INTEGER NOT NULL DEFAULT 0,
        confidence REAL NOT NULL DEFAULT 0.0,
        risk_level TEXT NOT NULL DEFAULT 'low',
        language TEXT NOT NULL DEFAULT 'fr',
        recommended_action TEXT NOT NULL DEFAULT 'review_required',
        supporting_conversation_ids_json TEXT NOT NULL DEFAULT '[]',
        status TEXT NOT NULL DEFAULT 'candidate',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        published_at TEXT,
        deprecated_at TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_learning_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review_key TEXT NOT NULL UNIQUE,
        candidate_key TEXT NOT NULL,
        reviewer_user_id INTEGER,
        decision TEXT NOT NULL DEFAULT 'review_required',
        notes TEXT NOT NULL DEFAULT '',
        reviewed_at TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_knowledge_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        version_key TEXT NOT NULL UNIQUE,
        version_number INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'draft',
        summary TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL,
        published_at TEXT,
        rolled_back_at TEXT,
        rolled_back_to_version_id INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feedback_key TEXT NOT NULL UNIQUE,
        request_key TEXT NOT NULL,
        conversation_key TEXT NOT NULL DEFAULT '',
        rating INTEGER NOT NULL DEFAULT 0,
        satisfaction INTEGER NOT NULL DEFAULT 0,
        outcome TEXT NOT NULL DEFAULT '',
        notes TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ai_cost_estimates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estimate_key TEXT NOT NULL UNIQUE,
        request_key TEXT NOT NULL,
        provider_key TEXT NOT NULL,
        model TEXT NOT NULL DEFAULT '',
        input_tokens INTEGER NOT NULL DEFAULT 0,
        output_tokens INTEGER NOT NULL DEFAULT 0,
        estimated_cost REAL NOT NULL DEFAULT 0.0,
        created_at TEXT NOT NULL
    )
    """,
)

SQLITE_AI_TABLES_SCRIPT = ";\n".join(statement.strip() for statement in AI_TABLE_STATEMENTS) + ";"
POSTGRESQL_AI_STATEMENTS: tuple[str, ...] = AI_TABLE_STATEMENTS
