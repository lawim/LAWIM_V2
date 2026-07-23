from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class NormalizationResult:
    result_id: str = field(default_factory=lambda: uuid4().hex[:16])
    normalized_content: str = ""
    is_empty: bool = False
    is_duplicate_content: bool = False
    warnings: list[str] = field(default_factory=list)


class MessageNormalizer:
    def normalize(self, raw_content: str, channel: str = "") -> NormalizationResult:
        if not raw_content or not raw_content.strip():
            return NormalizationResult(normalized_content="", is_empty=True)

        content = raw_content
        warnings: list[str] = []

        content = content.strip()
        content = re.sub(r'\s+', ' ', content)

        content = self._normalize_whitespace(content)

        if channel == "telegram":
            content = content.replace(r'\@', '@')

        if channel == "whatsapp":
            content = content.replace('\n', ' ').strip()

        return NormalizationResult(
            normalized_content=content,
            is_empty=False,
            warnings=warnings,
        )

    def _normalize_whitespace(self, text: str) -> str:
        text = re.sub(r'[\u200b\u200c\u200d\u2060\uFEFF]', '', text)
        text = re.sub(r'\u00a0', ' ', text)
        return text.strip()

    def is_empty_or_noise(self, content: str) -> bool:
        if not content or not content.strip():
            return True
        cleaned = re.sub(r'[\s.,!?;:\'\"-]+', '', content)
        return len(cleaned) == 0
