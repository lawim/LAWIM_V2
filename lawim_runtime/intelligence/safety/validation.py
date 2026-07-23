from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from lawim_runtime.interaction.response_plan import InteractionResponsePlan, ResponseType


FORBIDDEN_CLAIMS = [
    r"votre\s+paiement\s+(a\s+)?r[eé]ussi",
    r"votre\s+transaction\s+(a\s+)?r[eé]ussi",
    r"paiement\s+(confirm[ée]|valid[ée]|effectu[ée])",
    r"transaction\s+(confirm[ée]e|valid[ée]e|effectu[ée]e)",
    r"visite\s+(confirm[ée]e|programm[ée]e|planifi[ée]e)\s+(sans|automatiquement)",
    r"bien\s+(trouv[ée]|disponible|r[eé]serv[ée])",
    r"votre\s+profil\s+(a\s+)?\u00e9t[ée]\s+(qualifi[ée]|valid[ée]|approuv[ée])",
    r"votre\s+projet\s+(a\s+)?\u00e9t[ée]\s+(qualifi[ée]|valid[ée]|approuv[ée])",
    r"ce\s+titre\s+foncier\s+est\s+valide",
    r"cette\s+propri[eé]t[ée]\s+est\s+(l[ée]gitime|l[ée]gale)",
]


@dataclass
class ResponseValidationResult:
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    has_forbidden_claims: bool = False
    forbidden_claims_found: list[str] = field(default_factory=list)
    plan_compliant: bool = True
    plan_violations: list[str] = field(default_factory=list)


class ResponseValidator:
    def validate(self, text: str, plan: InteractionResponsePlan | None = None) -> ResponseValidationResult:
        result = ResponseValidationResult()
        text_lower = text.lower()
        for pattern in FORBIDDEN_CLAIMS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                result.has_forbidden_claims = True
                result.forbidden_claims_found.append(pattern)
                result.errors.append(f"forbidden claim detected: {pattern}")
                result.valid = False
        return result


class ClaimValidator:
    def validate_claim(self, claim: str, source: str | None = None) -> bool:
        return True


class ForbiddenClaimDetector:
    def __init__(self, patterns: list[str] | None = None) -> None:
        self._patterns = patterns or FORBIDDEN_CLAIMS

    def detect(self, text: str) -> list[str]:
        matches: list[str] = []
        text_lower = text.lower()
        for pattern in self._patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                matches.append(pattern)
        return matches
