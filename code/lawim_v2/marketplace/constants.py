from __future__ import annotations

PARTNER_REGISTRATION_STATUSES: frozenset[str] = frozenset(
    {"draft", "submitted", "under_review", "approved", "rejected", "suspended", "archived"}
)

PROVIDER_TYPES: frozenset[str] = frozenset(
    {"individual", "company", "agency", "freelancer", "enterprise", "collective"}
)

SERVICE_CATEGORIES: frozenset[str] = frozenset(
    {
        "property_management",
        "legal_notary",
        "financing",
        "insurance",
        "renovation",
        "moving",
        "cleaning",
        "inspection",
        "valuation",
        "architecture",
        "interior_design",
        "photography",
        "marketing",
        "maintenance",
        "security",
        "utilities",
        "consulting",
        "other",
    }
)

REQUEST_STATUSES: frozenset[str] = frozenset(
    {"draft", "submitted", "matching", "quoted", "contracted", "in_progress", "completed", "cancelled", "expired"}
)

QUOTE_STATUSES: frozenset[str] = frozenset(
    {"draft", "sent", "viewed", "accepted", "rejected", "expired", "superseded", "withdrawn"}
)

CONTRACT_STATUSES: frozenset[str] = frozenset(
    {"draft", "pending_signature", "active", "completed", "terminated", "disputed", "cancelled"}
)

MISSION_STATUSES: frozenset[str] = frozenset(
    {"planned", "scheduled", "in_progress", "blocked", "delivered", "accepted", "closed", "cancelled"}
)

REVIEW_STATUSES: frozenset[str] = frozenset(
    {"pending", "published", "hidden", "flagged", "removed"}
)

DISPUTE_STATUSES: frozenset[str] = frozenset(
    {"open", "under_review", "mediation", "resolved", "closed", "escalated"}
)

SUBSCRIPTION_STATUSES: frozenset[str] = frozenset(
    {"trial", "active", "past_due", "paused", "cancelled", "expired"}
)

COMMISSION_TYPES: frozenset[str] = frozenset(
    {"flat", "percentage", "tiered", "referral", "subscription", "performance"}
)

REPUTATION_SCORE_KEYS: tuple[str, ...] = (
    "quality",
    "responsiveness",
    "reliability",
    "value",
    "communication",
    "completion",
    "satisfaction",
)

PAYMENT_METHODS: frozenset[str] = frozenset(
    {"mobile_money", "orange_money", "mtn_momo", "card", "bank_transfer", "stripe", "paypal"}
)
