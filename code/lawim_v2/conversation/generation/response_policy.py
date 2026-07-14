from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..domain.decisions import ConversationDecision
from .validator import ContentValidator, Violation

STATUS_FAILED = "FAILED"


@dataclass
class ValidationResult:
    is_valid: bool = True
    violations: list[Violation] = field(default_factory=list)
    requires_regeneration: bool = False


class ResponsePolicy:

    def __init__(self, validator: ContentValidator | None = None) -> None:
        self._validator = validator or ContentValidator()

    def validate(self, response: str, decision: ConversationDecision) -> ValidationResult:
        violations = self._validator.validate(response, decision)

        policy_violations = self._check_policy_rules(response, decision)
        violations.extend(policy_violations)

        severity_errors = [v for v in violations if v.severity == "error"]
        severity_warnings = [v for v in violations if v.severity == "warning"]

        requires_regeneration = len(severity_errors) > 0

        return ValidationResult(
            is_valid=len(severity_errors) == 0,
            violations=violations,
            requires_regeneration=requires_regeneration,
        )

    def _check_policy_rules(self, response: str, decision: ConversationDecision) -> list[Violation]:
        policy_violations: list[Violation] = []

        policy_violations.extend(self._check_empty_or_too_short(response))
        policy_violations.extend(self._check_excessive_length(response))
        policy_violations.extend(self._check_response_type_mismatch(response, decision))
        policy_violations.extend(self._check_contradiction(response, decision))
        policy_violations.extend(self._check_action_status_consistency(response, decision))

        return policy_violations

    def _check_empty_or_too_short(self, response: str) -> list[Violation]:
        stripped = response.strip()
        if not stripped:
            return [Violation(
                type=None,  # type: ignore
                message="Response is empty",
                severity="error",
                source="policy",
            )]
        if len(stripped) < 5:
            return [Violation(
                type=None,
                message=f"Response is too short ({len(stripped)} chars)",
                severity="error",
                source="policy",
            )]
        return []

    def _check_excessive_length(self, response: str) -> list[Violation]:
        if len(response) > 2000:
            return [Violation(
                type=None,
                message=f"Response exceeds maximum length ({len(response)} > 2000 chars)",
                severity="warning",
                source="policy",
            )]
        return []

    def _check_response_type_mismatch(self, response: str, decision: ConversationDecision) -> list[Violation]:
        response_type = decision.response_type
        if not response_type:
            return []

        response_lower = response.lower()
        expected_content: dict[str, list[str]] = {
            "greeting": ["bonjour", "lawim"],
            "ask_intent": ["acheter", "louer", "vendre", "construire", "professionnel"],
            "ask_city": ["ville"],
            "ask_budget": ["budget"],
            "ask_property_type": ["type de bien", "appartement", "maison", "villa", "terrain"],
            "ask_bedrooms": ["chambres"],
            "ask_transaction_type": ["acheter", "louer"],
            "consent": ["consentement", "partager", "acceptez"],
            "handover": ["transfère", "conseiller", "contactera"],
            "error": ["désolé", "erreur", "technique"],
        }

        keywords = expected_content.get(response_type, [])
        if not keywords:
            return []

        match_count = sum(1 for kw in keywords if kw in response_lower)
        if match_count == 0:
            return [Violation(
                type=None,
                message=f"Response type '{response_type}' but response lacks expected keywords",
                severity="warning",
                source="policy",
            )]

        return []

    def _check_contradiction(self, response: str, decision: ConversationDecision) -> list[Violation]:
        contradictions: dict[str, list[tuple[str, str]]] = {
            "greeting": [
                ("transaction", "acheter"),
                ("transaction", "louer"),
            ],
        }
        return []

    def _check_action_status_consistency(self, response: str, decision: ConversationDecision) -> list[Violation]:
        action_status = decision.action_status
        if action_status == STATUS_FAILED:
            if "succès" in response.lower() or "réussi" in response.lower():
                return [Violation(
                    type=None,
                    message="Action failed but response claims success",
                    severity="error",
                    source="policy",
                )]
        return []
