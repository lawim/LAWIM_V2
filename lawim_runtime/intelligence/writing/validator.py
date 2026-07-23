from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from ...interaction.response_plan import InteractionResponsePlan, ResponseType
from ..safety.validation import ResponseValidationResult, FORBIDDEN_CLAIMS


@dataclass
class PlanComplianceResult:
    compliant: bool = True
    violations: list[str] = field(default_factory=list)


class WriterValidator:
    def validate(self, text: str, plan: InteractionResponsePlan | None = None) -> ResponseValidationResult:
        result = ResponseValidationResult()
        text_lower = text.lower()
        for pattern in FORBIDDEN_CLAIMS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                result.has_forbidden_claims = True
                result.forbidden_claims_found.append(pattern)
                result.errors.append(f"forbidden claim: {pattern}")
                result.valid = False
        return result


class PlanComplianceValidator:
    def validate(self, text: str, plan: InteractionResponsePlan) -> PlanComplianceResult:
        result = PlanComplianceResult()
        rtype = plan.response_type
        text_lower = text.lower()

        forbidding_map = {
            ResponseType.PRESENT_RESULTS: [r"invent", r"fictif", r"imagin"],
            ResponseType.HANDOVER: [r"votre\s+dossier\s+est\s+valid"],
            ResponseType.ERROR: [r"r[eé]ussi", r"confirm[ée]"],
        }

        patterns = forbidding_map.get(rtype, [])
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                result.violations.append(f"plan type {rtype.value} violated: found '{pattern}'")
                result.compliant = False
        return result
