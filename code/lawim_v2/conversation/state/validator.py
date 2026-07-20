from __future__ import annotations

from typing import Any

from .state import ResponsePlan


class ConversationResponseValidator:
    def validate(self, response: str, plan: ResponsePlan) -> tuple[str, str]:
        q_count = response.count("?")
        if plan.maximum_questions > 0 and q_count > plan.maximum_questions:
            replacement = plan.next_question_text or response
            return replacement, "REPAIR"
        return response, "PASS"
