from __future__ import annotations

AUTOMATION_DOMAINS: dict[str, tuple[str, ...]] = {
    "immobilier": ("achat", "vente", "location", "visite", "verification", "publication", "signature"),
    "juridique": ("contrats", "conformite", "validation_documentaire", "contentieux", "archivage"),
    "financement": ("demande", "etude", "scoring", "validation", "decaissement"),
    "administration": ("creation_comptes", "moderation", "support", "incidents", "reclamations"),
    "ia": ("analyse", "recommandations", "decisions_assistees", "enrichissement", "assistant"),
}

WORKFLOW_STATUSES: frozenset[str] = frozenset({"draft", "active", "paused", "archived"})
EXECUTION_STATUSES: frozenset[str] = frozenset({"pending", "running", "waiting", "completed", "failed", "cancelled"})
TASK_STATUSES: frozenset[str] = frozenset({"pending", "assigned", "in_progress", "completed", "failed", "escalated"})
APPROVAL_STATUSES: frozenset[str] = frozenset({"pending", "approved", "rejected", "escalated"})
QUEUE_PRIORITIES: frozenset[str] = frozenset({"low", "normal", "high", "critical"})
RULE_OPERATORS: frozenset[str] = frozenset({"eq", "neq", "gt", "gte", "lt", "lte", "contains", "in"})
AI_HOOK_TYPES: frozenset[str] = frozenset(
    {"assistant_chat", "knowledge_rag", "cognition_decision", "expert_search", "enrichment", "recommendation"}
)

DEFAULT_RETRY_MAX = 3
DEFAULT_SLA_HOURS = 48
DEFAULT_QUEUE_CAPACITY = 500
