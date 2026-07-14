from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AmbiguityResult:
    field: str = ""
    raw_value: str = ""
    ambiguity_type: str = ""  # "unit", "intent", "selection", "location"
    possible_interpretations: list[dict[str, Any]] = field(default_factory=list)
    clarification_question: str = ""
    confidence_threshold: float = 0.6


def is_likely_ambiguous_amount(text: str) -> bool:
    import re
    patterns = [
        re.compile(r"\d+\s*mil\s*$", re.IGNORECASE),
        re.compile(r"\d+\s*m\s*$", re.IGNORECASE),
        re.compile(r"(?:environ|vers|presque|~)\s*\d+", re.IGNORECASE),
    ]
    return any(p.search(text) for p in patterns)


def is_likely_correction(text: str) -> bool:
    indicators = [
        "finalement", "en fait", "en realite", "plutot", "non je",
        "je voulais dire", "je rectifie", "correction", "desole",
        "désolé", "non c'est", "c'est pas", "ce n'est pas",
    ]
    lower = text.lower()
    return any(ind in lower for ind in indicators)


def needs_clarification(field: str, value: Any, context: dict[str, Any]) -> bool:
    if field == "budget" and isinstance(value, dict) and value.get("ambiguity"):
        return True
    if field in ("property_type", "transaction_type") and value is None:
        return True
    if field == "project_selection" and isinstance(value, str) and value.lower() in {"ok", "oui", "d'accord", "vas-y"}:
        return True
    return False
