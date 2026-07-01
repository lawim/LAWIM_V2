from __future__ import annotations

PROPERTY_TYPES: frozenset[str] = frozenset(
    {
        "house",
        "apartment",
        "building",
        "land",
        "office",
        "retail",
        "industrial",
        "hotel",
        "residence",
        "investment_building",
    }
)

LISTING_STATUSES: frozenset[str] = frozenset({"draft", "published", "suspended", "expired", "archived"})
VERIFICATION_STATUSES: frozenset[str] = frozenset({"pending", "verified", "failed", "review"})
VISIT_STATUSES: frozenset[str] = frozenset({"scheduled", "confirmed", "completed", "cancelled", "no_show"})
NEGOTIATION_STATUSES: frozenset[str] = frozenset({"open", "offer", "counter", "accepted", "rejected", "closed"})
OFFER_STATUSES: frozenset[str] = frozenset({"draft", "submitted", "countered", "accepted", "rejected", "withdrawn"})
TRANSACTION_STATUSES: frozenset[str] = frozenset({"pending", "reserved", "promised", "signed", "closed", "cancelled"})
TRANSACTION_TYPES: frozenset[str] = frozenset({"sale", "rent", "reservation", "lease"})

INTELLIGENCE_SCORE_KEYS: tuple[str, ...] = (
    "quality",
    "legal",
    "investment",
    "market",
    "profitability",
    "liquidity",
    "risk",
)

RECOMMENDATION_TYPES: frozenset[str] = frozenset(
    {"property", "investment", "similar", "opportunity", "alert", "risk"}
)

DOCUMENT_TYPES: frozenset[str] = frozenset({"title", "diagnostic", "contract", "photo", "plan", "other"})
