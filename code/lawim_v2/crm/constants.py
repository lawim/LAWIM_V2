from __future__ import annotations

LEAD_STATUSES: frozenset[str] = frozenset(
    {"new", "contacted", "qualified", "proposal", "negotiation", "won", "lost", "nurturing", "archived"}
)

CONTACT_TYPES: frozenset[str] = frozenset(
    {"individual", "company", "prospect", "lead", "customer", "partner", "vendor", "agent"}
)

CUSTOMER_ROLES: frozenset[str] = frozenset(
    {"buyer", "seller", "tenant", "landlord", "investor", "broker", "developer", "partner"}
)

OPPORTUNITY_STATUSES: frozenset[str] = frozenset(
    {"open", "qualified", "proposal", "negotiation", "won", "lost", "on_hold", "closed"}
)

PIPELINE_STAGES: tuple[str, ...] = (
    "prospection",
    "qualification",
    "proposition",
    "negociation",
    "cloture",
)

COMMUNICATION_CHANNELS: frozenset[str] = frozenset({"whatsapp", "telegram", "email", "sms", "in_app"})

CAMPAIGN_STATUSES: frozenset[str] = frozenset({"draft", "scheduled", "running", "paused", "completed", "cancelled"})

SCORE_KEYS: tuple[str, ...] = (
    "engagement",
    "intent",
    "fit",
    "recency",
    "value",
    "loyalty",
    "risk",
)

SATISFACTION_TYPES: frozenset[str] = frozenset({"nps", "csat", "ces", "post_visit", "post_transaction", "general"})

CONSENT_TYPES: frozenset[str] = frozenset({"marketing", "whatsapp", "telegram", "email", "sms", "data_processing", "analytics"})

LEAD_SCORING_SIGNAL_BONUSES: tuple[tuple[str, int], ...] = (
    (r"\b(douala|yaounde|yaoundé|buea|bafoussam|kribi|bastos|akwa|makepe|molyko)\b", 10),
    (r"\b(budget|budget max|max budget|prix|price)\b.*\b\d", 10),
    (r"\b(urgent|tout de suite|immédiatement|now|quick)\b", 20),
    (r"\b(visite|visit|voir le bien|viewing)\b", 20),
    (r"\b(diaspora|france|belgique|suisse|canada|usa|uk|allemagne|italie|espagne)\b", 15),
    (r"\b(roi|cashflow|rentable|investissement|investment|rental income)\b", 15),
    (r"\b(cash|compte|bank|prêt|financement|loan)\b", 15),
    (r"\b(ce mois|semaine|1 mois|2 mois|rapide|quick)\b", 15),
)
