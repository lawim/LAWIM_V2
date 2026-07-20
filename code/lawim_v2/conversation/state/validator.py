from __future__ import annotations

from typing import Any

from .state import ResponsePlan


_FORBIDDEN_PHRASES = [
    "assistant neutre",
    "neutral assistant",
    "i cannot make business decisions",
    "je ne peux pas prendre de décisions commerciales",
    "provide more context for your request",
]

_REFERRAL_PLATFORMS = [
    "jumia",
    "seloger",
    "leboncoin",
    "facebook",
    "lamudi",
]

_TRANSLATION_PATTERNS = [
    "french for",
    "in english",
    "français signifie",
    "in french",
]

_GRAMMAR_PATTERNS = [
    "correct spelling is",
    "the correct phrasing",
    "you wrote",
    "vous avez écrit",
    "l'orthographe correcte",
    "la bonne orthographe",
]


class ConversationResponseValidator:
    @staticmethod
    def detect_forbidden_content(response: str) -> str | None:
        lower = response.lower()

        for phrase in _FORBIDDEN_PHRASES:
            if phrase in lower:
                return "REPAIR"

        for platform in _REFERRAL_PLATFORMS:
            if platform in lower:
                return "REPAIR"

        for pattern in _TRANSLATION_PATTERNS:
            if pattern in lower:
                return "REPAIR"

        for pattern in _GRAMMAR_PATTERNS:
            if pattern in lower:
                return "REPAIR"

        return None

    def validate(self, response: str, plan: ResponsePlan) -> tuple[str, str]:
        forbidden_status = self.detect_forbidden_content(response)
        if forbidden_status:
            return response, forbidden_status

        q_count = response.count("?")
        if plan.maximum_questions > 0 and q_count > plan.maximum_questions:
            replacement = plan.next_question_text or response
            return replacement, "REPAIR"
        return response, "PASS"
