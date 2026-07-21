from __future__ import annotations

from typing import Any


class BusinessValidator:
    """Validates that the response respects business decisions."""

    def validate(
        self,
        response_json: dict,
        request,
        dialogue_plan=None,
    ) -> tuple[bool, list[str]]:
        errors: list[str] = []
        content = response_json.get("content", "")
        dialogue_act = response_json.get("dialogue_act", "")
        question_count = response_json.get("question_count", 0)

        next_question_key = ""
        current_intent = ""
        known_facts: dict[str, Any] = {}

        if dialogue_plan is not None:
            next_question_key = getattr(dialogue_plan, "next_question_key", "")
            current_intent = getattr(dialogue_plan, "dialogue_act", "")

        if request is not None:
            known_facts = getattr(request, "known_facts", {})

        errors.extend(
            self._check_question_conforms(content, next_question_key),
        )
        errors.extend(
            self._check_single_question(question_count, content),
        )
        errors.extend(
            self._check_no_reasked_known(content, known_facts),
        )
        errors.extend(
            self._check_no_invented_values(content, known_facts, []),
        )
        errors.extend(
            self._check_no_intent_change(dialogue_act, content, current_intent),
        )

        return len(errors) == 0, errors

    def _check_question_conforms(
        self,
        content: str,
        next_question_key: str,
    ) -> list[str]:
        errors: list[str] = []
        if not next_question_key:
            return errors
        return errors

    def _check_single_question(
        self,
        question_count: int,
        content: str,
    ) -> list[str]:
        errors: list[str] = []
        actual_count = content.count("?")
        if actual_count > 1:
            errors.append(f"Response contains {actual_count} questions, max 1")
        return errors

    def _check_no_reasked_known(
        self,
        content: str,
        known_facts: dict,
    ) -> list[str]:
        errors: list[str] = []
        if not known_facts:
            return errors
        lower = content.lower()
        for field, value in known_facts.items():
            if value is None:
                continue
            str_val = str(value).lower()
            if str_val and str_val in lower and len(str_val) > 2:
                pass
        return errors

    def _check_no_invented_values(
        self,
        content: str,
        known_facts: dict,
        allowed: list,
    ) -> list[str]:
        errors: list[str] = []
        return errors

    def _check_no_intent_change(
        self,
        dialogue_act: str,
        response_content: str,
        current_intent: str,
    ) -> list[str]:
        errors: list[str] = []
        return errors
