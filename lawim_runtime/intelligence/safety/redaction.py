from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

REDACTION_PATTERNS: dict[str, str] = {
    r"sk-[A-Za-z0-9]{20,}": "[REDACTED_API_KEY]",
    r"AIza[0-9A-Za-z_-]{20,}": "[REDACTED_API_KEY]",
    r"Bearer [A-Za-z0-9._-]{20,}": "[REDACTED_TOKEN]",
    r"[0-9]{6,}@(c\.us|s\.whatsapp\.net)": "[REDACTED_WHATSAPP_ID]",
    r"[\w.+-]+@[\w-]+(\.[\w-]+)+": "[REDACTED_EMAIL]",
    r"\+(?:\d{1,3})?\d{6,14}": "[REDACTED_PHONE]",
    r"\b\d{14,16}\b": "[REDACTED_CARD]",
}


@dataclass
class RedactionPolicy:
    patterns: dict[str, str] = field(default_factory=lambda: dict(REDACTION_PATTERNS))
    enabled: bool = True

    def redact(self, text: str) -> str:
        if not self.enabled or not text:
            return text
        result = text
        for pattern, replacement in self.patterns.items():
            result = re.sub(pattern, replacement, result)
        return result


_default_policy = RedactionPolicy()


def redact_sensitive_text(text: str) -> str:
    return _default_policy.redact(text)
