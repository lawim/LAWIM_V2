from __future__ import annotations

import json
from typing import Any

from ..conversation.state.state import ResponsePlan

_SUPPORTED_LANGUAGES = {"fr", "en", "pcm"}
_VALID_DIALOGUE_ACTS = {
    "WELCOME", "HANDOVER", "REPHRASE_LAST_QUESTION",
    "ACKNOWLEDGE_AND_ASK", "CONFIRM_CORRECTION_AND_ASK",
    "CLARIFY_CURRENT_SLOT", "SEARCH_READY", "PUBLICATION_READY",
    "VISIT_READY", "TRANSACTION_READY", "SUMMARIZE_AND_CONFIRM",
    "CONTROLLED_ERROR",
}


class StructuralValidator:
    """Validates the structural integrity of a provider response."""

    def validate(self, response_text: str, request) -> tuple[bool, list[str]]:
        errors: list[str] = []

        is_valid, data, parse_error = self._check_valid_json(response_text)
        if not is_valid:
            return False, [f"Invalid JSON: {parse_error}"]

        errors.extend(self._check_required_fields(data))
        errors.extend(self._check_types(data))
        errors.extend(self._check_non_empty(data))
        errors.extend(self._check_language(data, request))
        errors.extend(self._check_dialogue_act(data))
        errors.extend(self._check_question_count(data))
        errors.extend(self._check_max_size(data, request))

        return len(errors) == 0, errors

    def _check_valid_json(self, text: str) -> tuple[bool, dict | None, str]:
        try:
            data = json.loads(text)
            if not isinstance(data, dict):
                return False, None, "Response is not a JSON object"
            return True, data, ""
        except json.JSONDecodeError as e:
            return False, None, str(e)

    def _check_required_fields(self, data: dict) -> list[str]:
        errors: list[str] = []
        required = {"content", "dialogue_act", "language"}
        for field in required:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        return errors

    def _check_types(self, data: dict) -> list[str]:
        errors: list[str] = []
        if "content" in data and not isinstance(data["content"], str):
            errors.append("Field 'content' must be a string")
        if "dialogue_act" in data and not isinstance(data["dialogue_act"], str):
            errors.append("Field 'dialogue_act' must be a string")
        if "language" in data and not isinstance(data["language"], str):
            errors.append("Field 'language' must be a string")
        if "question_count" in data and not isinstance(data["question_count"], int):
            errors.append("Field 'question_count' must be an integer")
        return errors

    def _check_non_empty(self, data: dict) -> list[str]:
        errors: list[str] = []
        content = data.get("content", "")
        if not content or not content.strip():
            errors.append("Response content is empty")
        return errors

    def _check_language(self, data: dict, request) -> list[str]:
        errors: list[str] = []
        lang = data.get("language", "")
        if lang not in _SUPPORTED_LANGUAGES:
            errors.append(f"Unsupported language: {lang}. Supported: {_SUPPORTED_LANGUAGES}")
        return errors

    def _check_dialogue_act(self, data: dict) -> list[str]:
        errors: list[str] = []
        act = data.get("dialogue_act", "")
        if act not in _VALID_DIALOGUE_ACTS:
            errors.append(f"Invalid dialogue_act: {act}. Valid: {_VALID_DIALOGUE_ACTS}")
        return errors

    def _check_question_count(self, data: dict) -> list[str]:
        errors: list[str] = []
        q_count = data.get("question_count", 0)
        max_q = data.get("maximum_questions", 1)
        if q_count > max_q:
            errors.append(f"question_count {q_count} exceeds maximum {max_q}")
        return errors

    def _check_max_size(self, data: dict, request) -> list[str]:
        errors: list[str] = []
        content = data.get("content", "")
        max_len = getattr(request, "maximum_length", 500) if request is not None else 500
        if len(content) > max_len:
            errors.append(f"Response length {len(content)} exceeds maximum {max_len}")
        return errors
