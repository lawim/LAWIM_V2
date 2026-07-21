from __future__ import annotations

import json
import re
from typing import Any

from .business import BusinessValidator
from .conversation import ConversationValidator
from .structural import StructuralValidator


class RepairHandler:
    """Attempts a SINGLE repair of an invalid response."""

    def __init__(
        self,
        structural: StructuralValidator,
        business: BusinessValidator,
        conversation: ConversationValidator,
    ) -> None:
        self._structural = structural
        self._business = business
        self._conversation = conversation

    def repair(
        self,
        response_text: str,
        request,
        dialogue_plan=None,
    ) -> tuple[str | None, bool]:
        is_valid_struct, struct_errors = self._structural.validate(
            response_text, request,
        )

        if not is_valid_struct:
            repaired = self._repair_structural(response_text, request, struct_errors)
            if repaired is not None:
                response_text = repaired
            else:
                return None, False

        try:
            data = json.loads(response_text)
        except (json.JSONDecodeError, ValueError):
            return None, False

        content = data.get("content", "")

        is_valid_conv, conv_errors = self._conversation.validate(content, request)
        if not is_valid_conv:
            cleaned = self._strip_forbidden_content(content)
            if cleaned != content:
                data["content"] = cleaned
                response_text = json.dumps(data, ensure_ascii=False)
            else:
                return None, False

        is_valid_biz, biz_errors = self._business.validate(
            data, request, dialogue_plan,
        )
        if not is_valid_biz:
            return None, False

        return response_text, True

    def _repair_structural(
        self,
        response_text: str,
        request,
        errors: list[str],
    ) -> str | None:
        error_set = set(errors)

        if any("Invalid JSON" in e for e in error_set):
            content = self._extract_content_from_non_json(response_text)
            if content is None:
                return None
            return self._build_json_response(content, request)

        return None

    def _extract_content_from_non_json(self, text: str) -> str | None:
        cleaned = text.strip().strip("`").strip()
        if cleaned.startswith("{") or cleaned.startswith("["):
            return None
        if len(cleaned) < 2:
            return None
        return cleaned

    def _build_json_response(
        self,
        content: str,
        request,
    ) -> str:
        lang = "fr"
        if request is not None:
            lang = getattr(request, "language", "fr")

        data = {
            "content": content,
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "language": lang,
            "question_count": content.count("?"),
        }
        return json.dumps(data, ensure_ascii=False)

    def _strip_forbidden_content(self, content: str) -> str:
        lower = content.lower()
        all_patterns: list[tuple[str, str]] = []
        for category, patterns in ConversationValidator.FORBIDDEN_PATTERNS.items():
            for p in patterns:
                all_patterns.append((p, category))

        sentences = re.split(r'(?<=[.!?])\s+', content)
        cleaned_sentences: list[str] = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            is_forbidden = False
            for pattern, _ in all_patterns:
                if pattern in sentence_lower:
                    is_forbidden = True
                    break
            if not is_forbidden:
                cleaned_sentences.append(sentence)

        result = " ".join(cleaned_sentences).strip()
        return result
