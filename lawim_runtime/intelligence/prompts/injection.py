from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


PROMPT_INJECTION_PATTERNS: list[tuple[str, str]] = [
    (r"ignore\s+(.*\s+)?instructions", "instruction_override"),
    (r"reveal\s+(the\s+)?(system\s+)?prompt", "system_prompt_reveal"),
    (r"reveal\s+(the\s+)?(secret|key|token)", "secret_extraction"),
    (r"show\s+(your\s+)?(environment|env|instructions)", "env_disclosure"),
    (r"print\s+(your\s+)?(system|developer)\s+prompt", "prompt_extraction"),
    (r"exfiltrat", "exfiltration"),
    (r"mark\s+(my\s+)?(dossier|file|case|project|profile)\s+as\s+(valid|approved|qualified|complete|verified)", "business_status_override"),
    (r"(consid[eè]re|marque|d[eé]clare|passe)\s+(mon|le)\s+(projet|dossier)\s+comme\s+(qualifi[ée]|valid[ée]|compl[eè]te|approuv[ée])", "business_status_override_fr"),
    (r"d[eé]clenche\s+(un\s+)?paiement", "payment_trigger"),
    (r"(call\s+this\s+tool|use\s+this\s+tool|appelle\s+cet\s+outil)", "tool_call_request"),
    (r"agis\s+comme\s+(un\s+)?administrateur", "admin_impersonation"),
    (r"ignore\s+.*instructions\s+(pr[eé]c[eé]dentes|avant)", "instruction_override_fr"),
    (r"n\u2019?oublie\s+pas\s+(les|que)", "instruction_override_fr"),
]


@dataclass
class InjectionDetectionResult:
    is_injection: bool = False
    matched_patterns: list[str] = field(default_factory=list)
    matched_categories: list[str] = field(default_factory=list)
    risk_level: str = "none"


class PromptInjectionDetector:
    def __init__(self, patterns: list[tuple[str, str]] | None = None) -> None:
        self._patterns = patterns or PROMPT_INJECTION_PATTERNS

    def detect(self, text: str) -> InjectionDetectionResult:
        result = InjectionDetectionResult()
        text_lower = text.lower()

        for pattern, category in self._patterns:
            if re.search(pattern, text_lower):
                result.is_injection = True
                result.matched_patterns.append(pattern)
                result.matched_categories.append(category)

        if result.is_injection:
            risk_categories = {"payment_trigger", "business_status_override", "business_status_override_fr", "admin_impersonation"}
            matched_set = set(result.matched_categories)
            if matched_set & risk_categories:
                result.risk_level = "high"
            else:
                result.risk_level = "medium"

        return result

    def sanitize(self, text: str) -> str:
        return text
