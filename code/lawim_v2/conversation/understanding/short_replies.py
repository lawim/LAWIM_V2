from __future__ import annotations

from typing import Any

AFFIRMATIVE_SHORT = {"ok", "oui", "d'accord", "dac", "okay", "yes", "si", "da", "vas-y", "yep", "yep", "kk", "dacc"}
NEGATIVE_SHORT = {"non", "no", "nan", "pas", "non merci", "merci non", "non pas"}
AMBIGUOUS_SELECTION = {"ok", "oui", "d'accord", "dac", "vas-y", "yep"}


def classify_short_reply(text: str) -> dict[str, Any]:
    cleaned = text.strip().lower().rstrip("!.,?")
    return {
        "is_short": True,
        "is_affirmative": cleaned in AFFIRMATIVE_SHORT,
        "is_negative": cleaned in NEGATIVE_SHORT,
        "is_ambiguous_selection": cleaned in AMBIGUOUS_SELECTION,
        "raw_value": cleaned,
    }


def is_project_selection_ambiguity(text: str) -> bool:
    return classify_short_reply(text)["is_ambiguous_selection"]
