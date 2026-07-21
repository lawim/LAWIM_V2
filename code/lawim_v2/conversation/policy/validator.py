from __future__ import annotations

from .dialogue_plan import DialoguePlan


class LawimConversationPolicyValidator:
    FORBIDDEN_PHRASES: list[str] = [
        "assistant neutre", "neutral assistant",
        "je ne peux pas prendre de d\u00e9cisions commerciales",
        "I cannot make business decisions",
        "How can I help you today",
        "French for", "in English", "in French",
        "the correct spelling", "the correct phrasing",
        "provide more context", "clarify your request",
        "Jumia", "SeLoger", "Leboncoin", "Lamudi",
    ]

    def validate(self, response: str, plan: DialoguePlan) -> tuple[str, str]:
        if not response or not response.strip():
            return response, "BLOCK"

        lower = response.lower()

        for phrase in self.FORBIDDEN_PHRASES:
            if phrase.lower() in lower:
                if phrase.lower() == "how can i help you today":
                    if plan.dialogue_act == "WELCOME":
                        continue
                return response, "REPAIR"

        if plan.maximum_questions > -1:
            q_count = response.count("?")
            if q_count > plan.maximum_questions:
                return plan.rendered_next_question or response, "REPAIR"

        return response, "PASS"
