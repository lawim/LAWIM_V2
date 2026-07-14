from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ..domain.decisions import ConversationDecision

ACTION_REQUEST_CLARIFICATION = "REQUEST_CLARIFICATION"
ACTION_PRESENT_RESULTS = "PRESENT_RESULTS"
ACTION_CREATE_RELATIONSHIP = "CREATE_RELATIONSHIP"
ACTION_RUN_MATCHING = "RUN_MATCHING"
ACTION_START_SEARCH = "START_SEARCH"
ACTION_RECORD_CONSENT = "RECORD_CONSENT"
ACTION_CREATE_PROJECT = "CREATE_PROJECT"
ACTION_CLOSE_PROJECT = "CLOSE_PROJECT"
ACTION_REQUEST_CONSENT = "REQUEST_CONSENT"

STATUS_EXECUTED = "EXECUTED"
STATUS_COMPLETED = "COMPLETED"


class ViolationType(str, Enum):
    EXTERNAL_PLATFORM_RECOMMENDATION = "external_platform_recommendation"
    CONFIRMED_FACT_REPEAT = "confirmed_fact_repeat"
    INVENTED_DATA = "invented_data"
    UNEXECUTED_ACTION_ANNOUNCEMENT = "unexecuted_action_announcement"
    PRIVATE_CONTACT_INFO_SHARED = "private_contact_info_shared"
    REQUIRED_CLARIFICATION_OMITTED = "required_clarification_omitted"
    UNAUTHORIZED_STATE_CHANGE = "unauthorized_state_change"


@dataclass
class Violation:
    type: ViolationType
    message: str
    severity: str = "error"
    source: str | None = None


EXTERNAL_PLATFORMS: list[str] = [
    "airbnb",
    "booking.com",
    "booking",
    "jumia house",
    "jumiahouse",
    "facebook marketplace",
    "facebook",
    "leboncoin",
    "seloger",
    "logic-immo",
    "paruvendu",
    "entreparticuliers",
    "pap",
    "bienici",
    "ouestfrance-immo",
]


CONFIRMED_FACT_QUESTIONS: dict[str, list[str]] = {
    "city": ["quelle ville", "dans quelle ville", "quelle localisation", "où"],
    "budget": ["quel budget", "combien", "prix", "budget"],
    "property_type": ["quel type", "quel bien", "type de bien"],
    "bedrooms": ["combien de chambres", "nombre de chambres", "chambres"],
    "intent": ["que voulez-vous", "souhaitez-vous", "votre projet", "intention"],
    "surface": ["quelle surface", "surface"],
}


class ContentValidator:

    def validate(self, response: str, decision: ConversationDecision) -> list[Violation]:
        violations: list[Violation] = []

        violations.extend(self._check_external_platforms(response))
        violations.extend(self._check_confirmed_fact_repeat(response, decision))
        violations.extend(self._check_invented_data(response, decision))
        violations.extend(self._check_unexecuted_action(response, decision))
        violations.extend(self._check_private_contact_info(response, decision))
        violations.extend(self._check_clarification_omitted(response, decision))
        violations.extend(self._check_unauthorized_state_change(response, decision))

        return violations

    def _check_external_platforms(self, response: str) -> list[Violation]:
        response_lower = response.lower()
        found: list[Violation] = []
        for platform in EXTERNAL_PLATFORMS:
            if platform in response_lower:
                found.append(Violation(
                    type=ViolationType.EXTERNAL_PLATFORM_RECOMMENDATION,
                    message=f"Response recommends or references external platform: {platform}",
                    severity="error",
                ))
        return found

    def _check_confirmed_fact_repeat(self, response: str, decision: ConversationDecision) -> list[Violation]:
        if not decision.requires_clarification:
            return []
        if decision.action != ACTION_REQUEST_CLARIFICATION:
            return []

        response_lower = response.lower()
        known_facts = decision.known_facts or {}
        found: list[Violation] = []

        for field, patterns in CONFIRMED_FACT_QUESTIONS.items():
            if field not in known_facts:
                continue
            for pattern in patterns:
                if pattern in response_lower:
                    found.append(Violation(
                        type=ViolationType.CONFIRMED_FACT_REPEAT,
                        message=f"Response re-asks about already confirmed fact '{field}' with pattern '{pattern}'",
                        severity="warning",
                    ))
                    break

        return found

    def _check_invented_data(self, response: str, decision: ConversationDecision) -> list[Violation]:
        response_lower = response.lower()
        found: list[Violation] = []

        action = decision.action
        action_status = decision.action_status
        action_params = decision.action_parameters or {}

        if action in (ACTION_PRESENT_RESULTS,) and action_status not in (STATUS_EXECUTED, STATUS_COMPLETED, None, "", "PENDING"):
            if "j'ai trouvé" in response_lower or "voici" in response_lower:
                found.append(Violation(
                    type=ViolationType.INVENTED_DATA,
                    message="Response presents results before search has been executed",
                    severity="error",
                ))

        if action == ACTION_CREATE_RELATIONSHIP and action_status not in (STATUS_EXECUTED, STATUS_COMPLETED, None, "", "PENDING"):
            name_patterns = [
                kw for kw in decision.known_facts.values()
                if isinstance(kw, str) and kw.strip()
            ]
            if "mis en relation" in response_lower or "relation créée" in response_lower:
                found.append(Violation(
                    type=ViolationType.INVENTED_DATA,
                    message="Response announces relationship creation before action is executed",
                    severity="error",
                ))

        if decision.action_status not in (STATUS_EXECUTED, STATUS_COMPLETED, None, "", "PENDING"):
            if "j'ai trouvé" in response_lower and "résultat" in response_lower:
                if action not in (ACTION_PRESENT_RESULTS, ACTION_RUN_MATCHING):
                    found.append(Violation(
                        type=ViolationType.INVENTED_DATA,
                        message="Response invents search results without matching action",
                        severity="error",
                    ))

        return found

    def _check_unexecuted_action(self, response: str, decision: ConversationDecision) -> list[Violation]:
        if decision.action_status in (STATUS_EXECUTED, STATUS_COMPLETED, None, "", "PENDING"):
            return []
        if decision.action is None:
            return []

        response_lower = response.lower()
        found: list[Violation] = []

        action_announcements: dict[str, list[str]] = {
            ACTION_CREATE_RELATIONSHIP: [
                "vient d'être créée", "a été créée", "est créée",
                "relation établie", "mis en relation",
            ],
            ACTION_START_SEARCH: [
                "recherche a été lancée", "recherche est terminée",
            ],
            ACTION_RECORD_CONSENT: [
                "consentement a été enregistré", "consentement enregistré",
            ],
            ACTION_CREATE_PROJECT: [
                "projet a été créé", "projet créé",
            ],
            ACTION_CLOSE_PROJECT: [
                "projet a été fermé", "projet fermé", "projet clôturé",
            ],
        }

        announcements = action_announcements.get(decision.action, [])
        for phrase in announcements:
            if phrase in response_lower:
                found.append(Violation(
                    type=ViolationType.UNEXECUTED_ACTION_ANNOUNCEMENT,
                    message=f"Response announces action '{decision.action}' as completed but it has not been executed",
                    severity="error",
                ))
                break

        return found

    def _check_private_contact_info(self, response: str, decision: ConversationDecision) -> list[Violation]:
        action_params = decision.action_parameters or {}
        action = decision.action

        if action == ACTION_REQUEST_CONSENT:
            return []

        if action == ACTION_CREATE_RELATIONSHIP and decision.action_status in (STATUS_EXECUTED, STATUS_COMPLETED):
            return []

        response_lower = response.lower()
        contact_indicators = [
            "téléphone", "numéro", "+225", "+221", "+237", "+233",
            "email", "adresse mail", "contactez-le", "contactez-la",
            "whatsapp", "joignable",
        ]
        found: list[Violation] = []
        for indicator in contact_indicators:
            if indicator in response_lower:
                consent_given = action_params.get("consent") or decision.known_facts.get("consent_given")
                if not consent_given:
                    found.append(Violation(
                        type=ViolationType.PRIVATE_CONTACT_INFO_SHARED,
                        message=f"Response shares contact information ('{indicator}') without recorded consent",
                        severity="error",
                    ))
                    break

        return found

    def _check_clarification_omitted(self, response: str, decision: ConversationDecision) -> list[Violation]:
        if not decision.requires_clarification:
            return []
        if decision.action != ACTION_REQUEST_CLARIFICATION:
            return []

        response_lower = response.lower()
        clarification_indicators = [
            "pouvez-vous", "pourriez-vous", "merci de", "veuillez",
            "choisir", "préciser", "clarifier", "voulez-vous",
            "souhaitez-vous", "options", "choix",
            "?",  # questions typically indicate clarification
        ]

        has_question_mark = "?" in response
        has_indicator = any(ind in response_lower for ind in clarification_indicators)

        if not has_question_mark and not has_indicator:
            return [Violation(
                type=ViolationType.REQUIRED_CLARIFICATION_OMITTED,
                message="Response does not ask for clarification when required",
                severity="error",
            )]

        return []

    def _check_unauthorized_state_change(self, response: str, decision: ConversationDecision) -> list[Violation]:
        action = decision.action
        state_before = decision.state_before
        state_after = decision.state_after

        if state_before is None or state_after is None:
            return []
        if state_before == state_after:
            return []

        state_announcement_map: dict[str, list[str]] = {
            "HUMAN_HANDOVER": [
                "je transfère", "transfert", "un conseiller va vous",
                "va vous contacter",
            ],
            "CLOSED": [
                "projet est fermé", "conversation terminée", "au revoir",
            ],
        }

        transition_str = f"{state_before.value} -> {state_after.value}"
        announcements = state_announcement_map.get(state_after.value, [])
        if not announcements:
            return []

        response_lower = response.lower()
        for phrase in announcements:
            if phrase in response_lower:
                return [Violation(
                    type=ViolationType.UNAUTHORIZED_STATE_CHANGE,
                    message=f"Response announces state change {transition_str} without authorization",
                    severity="error",
                )]

        return []
