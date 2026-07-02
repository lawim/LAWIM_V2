from __future__ import annotations

EVENT_TYPES: frozenset[str] = frozenset(
    {
        "generic",
        "metric_recorded",
        "kpi_computed",
        "dashboard_viewed",
        "report_generated",
        "export_completed",
        "anomaly_detected",
        "insight_generated",
        "score_updated",
        "aggregation_completed",
    }
)

METRIC_CATEGORIES: frozenset[str] = frozenset(
    {
        "general",
        "crm",
        "marketplace",
        "workflow",
        "rei",
        "communication",
        "security",
        "cognition",
        "knowledge",
        "assistant",
        "ecosystem",
        "infrastructure",
        "performance",
        "quality",
        "users",
        "activity",
        "commercial",
        "financial",
    }
)

KPI_CATEGORIES: frozenset[str] = frozenset(
    {
        "crm",
        "marketplace",
        "workflow",
        "rei",
        "communication",
        "security",
        "cognition",
        "knowledge",
        "assistant",
        "ecosystem",
        "performance",
        "infrastructure",
        "quality",
        "users",
        "activity",
        "commercial",
        "financial",
        "executive",
    }
)

DASHBOARD_TYPES: frozenset[str] = frozenset(
    {
        "executive",
        "administrator",
        "crm",
        "marketplace",
        "workflow",
        "rei",
        "security",
        "communication",
        "ai",
        "rag",
        "global",
        "realtime",
        "custom",
    }
)

REPORT_FORMATS: frozenset[str] = frozenset({"json", "csv", "html", "pdf", "excel", "xml"})

EXPORT_FORMATS: frozenset[str] = frozenset({"json", "csv", "html", "pdf", "excel", "xml"})

REPORT_STATUSES: frozenset[str] = frozenset(
    {"draft", "pending", "running", "completed", "failed", "cancelled", "archived"}
)

AGGREGATION_TYPES: frozenset[str] = frozenset(
    {"sum", "avg", "min", "max", "count", "median", "percentile", "rate"}
)

TREND_TYPES: frozenset[str] = frozenset(
    {"linear", "exponential", "seasonal", "moving_average", "regression"}
)

SCORE_TYPES: frozenset[str] = frozenset(
    {
        "customer",
        "partner",
        "provider",
        "property",
        "workflow",
        "communication",
        "security",
        "knowledge",
        "ai_confidence",
        "platform_health",
    }
)

DATA_MART_TYPES: frozenset[str] = frozenset(
    {
        "crm",
        "marketplace",
        "workflow",
        "communication",
        "security",
        "knowledge",
        "rei",
        "assistant",
        "global",
    }
)

INSIGHT_TYPES: frozenset[str] = frozenset(
    {
        "trend",
        "anomaly",
        "recommendation",
        "forecast",
        "segmentation",
        "prioritization",
        "summary",
        "explanation",
    }
)

PROGRAM_CODES: frozenset[str] = frozenset(
    {
        "intelligent_core",
        "ecosystem",
        "cognition",
        "assistant",
        "knowledge",
        "workflow",
        "rei",
        "crm",
        "marketplace",
        "security",
        "communication",
        "observability",
        "global",
    }
)

ANALYTIC_SOURCES: tuple[tuple[str, str, str], ...] = (
    ("crm_metrics", "crm", "metrics"),
    ("marketplace_metrics", "marketplace", "metrics"),
    ("communication_metrics", "communication", "metrics"),
    ("security_metrics", "security", "metrics"),
    ("workflow_metrics", "workflow", "metrics"),
    ("rei_metrics", "rei", "metrics"),
    ("knowledge_metrics", "knowledge", "metrics"),
    ("assistant_metrics", "assistant", "metrics"),
    ("cognition_metrics", "cognition", "metrics"),
    ("ecosystem_metrics", "ecosystem", "metrics"),
    ("observability_metrics", "observability", "metrics"),
    ("audit_events", "security", "events"),
    ("notification_events", "communication", "events"),
    ("workflow_events", "workflow", "events"),
    ("marketplace_events", "marketplace", "events"),
    ("crm_events", "crm", "events"),
    ("security_events", "security", "events"),
    ("communication_events", "communication", "events"),
)

DEFAULT_KPI_DEFINITIONS: tuple[tuple[str, str, str, str], ...] = (
    ("kpi-crm-leads", "CRM Leads", "crm", "crm"),
    ("kpi-crm-conversion", "CRM Conversion Rate", "crm", "crm"),
    ("kpi-marketplace-requests", "Marketplace Requests", "marketplace", "marketplace"),
    ("kpi-workflow-success", "Workflow Success Rate", "workflow", "workflow"),
    ("kpi-rei-properties", "REI Properties", "rei", "rei"),
    ("kpi-communication-delivery", "Communication Delivery Rate", "communication", "communication"),
    ("kpi-security-incidents", "Security Incidents", "security", "security"),
    ("kpi-knowledge-queries", "Knowledge Queries", "knowledge", "knowledge"),
    ("kpi-assistant-sessions", "Assistant Sessions", "assistant", "assistant"),
    ("kpi-ecosystem-partners", "Ecosystem Partners", "ecosystem", "ecosystem"),
    ("kpi-platform-health", "Platform Health Score", "executive", "global"),
    ("kpi-user-activity", "User Activity", "users", "global"),
)

DEFAULT_DASHBOARDS: tuple[tuple[str, str, str], ...] = (
    ("dashboard-executive", "Executive Dashboard", "executive"),
    ("dashboard-admin", "Administrator Dashboard", "administrator"),
    ("dashboard-crm", "CRM Dashboard", "crm"),
    ("dashboard-marketplace", "Marketplace Dashboard", "marketplace"),
    ("dashboard-workflow", "Workflow Dashboard", "workflow"),
    ("dashboard-rei", "REI Dashboard", "rei"),
    ("dashboard-security", "Security Dashboard", "security"),
    ("dashboard-communication", "Communication Dashboard", "communication"),
    ("dashboard-ai", "AI Dashboard", "ai"),
    ("dashboard-rag", "RAG Dashboard", "rag"),
    ("dashboard-global", "Global Dashboard", "global"),
    ("dashboard-realtime", "Real-Time Dashboard", "realtime"),
)

DEFAULT_DATA_MARTS: tuple[tuple[str, str, str], ...] = (
    ("mart-crm", "CRM Analytics", "crm"),
    ("mart-marketplace", "Marketplace Analytics", "marketplace"),
    ("mart-workflow", "Workflow Analytics", "workflow"),
    ("mart-communication", "Communication Analytics", "communication"),
    ("mart-security", "Security Analytics", "security"),
    ("mart-knowledge", "Knowledge Analytics", "knowledge"),
    ("mart-rei", "REI Analytics", "rei"),
    ("mart-assistant", "Assistant Analytics", "assistant"),
    ("mart-global", "Global Analytics", "global"),
)

DEFAULT_SCORE_DEFINITIONS: tuple[tuple[str, str, str, str], ...] = (
    ("score-customer", "Customer Score", "customer", "crm"),
    ("score-partner", "Partner Score", "partner", "marketplace"),
    ("score-provider", "Provider Score", "provider", "marketplace"),
    ("score-property", "Property Score", "property", "rei"),
    ("score-workflow", "Workflow Score", "workflow", "workflow"),
    ("score-communication", "Communication Score", "communication", "communication"),
    ("score-security", "Security Score", "security", "security"),
    ("score-knowledge", "Knowledge Score", "knowledge", "knowledge"),
    ("score-ai-confidence", "AI Confidence Score", "ai_confidence", "assistant"),
    ("score-platform-health", "Platform Health Score", "platform_health", "global"),
)
