from __future__ import annotations

from typing import Any


class ConversationValidator:
    """Validates against conversation policies."""

    FORBIDDEN_PATTERNS: dict[str, list[str]] = {
        "neutral_assistant": [
            "assistant neutre",
            "neutral assistant",
            "i cannot make business decisions",
            "je ne peux pas prendre de décisions commerciales",
            "provide more context for your request",
        ],
        "external_referral": [
            "jumia",
            "seloger",
            "leboncoin",
            "facebook",
            "lamudi",
        ],
        "translation": [
            "french for",
            "in english",
            "français signifie",
            "in french",
        ],
        "grammar": [
            "correct spelling is",
            "the correct phrasing",
            "you wrote",
            "vous avez écrit",
            "l'orthographe correcte",
            "la bonne orthographe",
        ],
    }

    def validate(self, content: str, request) -> tuple[bool, list[str]]:
        errors: list[str] = []
        lower = content.lower()

        for category, patterns in self.FORBIDDEN_PATTERNS.items():
            for pattern in patterns:
                if pattern in lower:
                    errors.append(f"Forbidden content ({category}): '{pattern}' found")

        if not errors:
            pass

        return len(errors) == 0, errors
