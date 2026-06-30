from __future__ import annotations

GOAL_KEYS = frozenset({
    "buy",
    "rent",
    "sell",
    "build",
    "invest",
    "secure_patrimony",
    "prepare_retirement",
    "house_family",
    "diaspora",
    "other",
})

LIFE_EVENT_TYPES = frozenset({
    "marriage",
    "birth",
    "relocation",
    "retirement",
    "investment",
    "succession",
    "business_creation",
    "job_change",
    "education",
    "other",
})

DECISION_STATUSES = frozenset({"proposed", "accepted", "rejected", "deferred", "superseded"})
RECOMMENDATION_STATUSES = frozenset({"active", "dismissed", "completed", "expired"})
ACTION_STATUSES = frozenset({"pending", "in_progress", "completed", "cancelled", "blocked"})
TASK_STATUSES = frozenset({"todo", "doing", "done", "cancelled"})
JOURNEY_STATUSES = frozenset({"draft", "active", "blocked", "replanned", "completed", "cancelled"})
RISK_SEVERITIES = frozenset({"low", "medium", "high", "critical"})
TIMELINE_ENTRY_TYPES = frozenset({"event", "milestone", "action", "projection", "history", "planning"})
KNOWLEDGE_CATEGORIES = frozenset({
    "market",
    "neighborhood",
    "procedure",
    "legal",
    "finance",
    "checklist",
    "faq",
    "general",
})

GOAL_JOURNEY_INFLUENCE: dict[str, tuple[str, ...]] = {
    "buy": ("qualification", "search", "visit", "negotiation", "closing"),
    "rent": ("qualification", "search", "visit", "negotiation", "closing"),
    "sell": ("qualification", "preparation", "promotion", "negotiation", "closing"),
    "invest": ("qualification", "analysis", "search", "due_diligence", "closing"),
    "build": ("qualification", "land", "design", "construction", "closing"),
    "secure_patrimony": ("qualification", "planning", "execution", "review", "closing"),
    "prepare_retirement": ("qualification", "planning", "execution", "review", "closing"),
    "house_family": ("qualification", "search", "visit", "negotiation", "closing"),
    "diaspora": ("qualification", "planning", "execution", "review", "closing"),
    "other": ("qualification", "planning", "execution", "review", "closing"),
}

LIFE_EVENT_GOAL_SHIFT: dict[str, tuple[str, ...]] = {
    "marriage": ("house_family", "buy"),
    "birth": ("house_family", "buy", "rent"),
    "relocation": ("buy", "rent"),
    "retirement": ("prepare_retirement", "secure_patrimony", "sell"),
    "investment": ("invest", "secure_patrimony"),
    "succession": ("secure_patrimony", "sell"),
    "business_creation": ("invest", "build"),
    "job_change": ("rent", "buy", "relocation"),
}
