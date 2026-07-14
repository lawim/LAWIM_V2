from __future__ import annotations

import logging
from typing import Any

from ..domain.decisions import ConversationDecision
from .llm_adapter import LLMAdapter, ProviderType
from .response_policy import ResponsePolicy, ValidationResult
from .templates import get_template, has_template

ACTION_GREETING = "GREETING"
ACTION_HANDOVER_TO_HUMAN = "HANDOVER_TO_HUMAN"
ACTION_CREATE_RELATIONSHIP = "CREATE_RELATIONSHIP"
ACTION_RECORD_CONSENT = "RECORD_CONSENT"
ACTION_CREATE_PROJECT = "CREATE_PROJECT"
ACTION_START_SEARCH = "START_SEARCH"
ACTION_CLOSE_PROJECT = "CLOSE_PROJECT"
ACTION_REQUEST_CLARIFICATION = "REQUEST_CLARIFICATION"

logger = logging.getLogger(__name__)

MAX_REGENERATION_ATTEMPTS = 3


class GenerativeComposer:

    def __init__(
        self,
        llm_adapter: LLMAdapter | None = None,
        policy: ResponsePolicy | None = None,
    ) -> None:
        self._llm = llm_adapter or LLMAdapter()
        self._policy = policy or ResponsePolicy()

    def compose(self, decision: ConversationDecision) -> str:
        response = self._generate(decision)

        for attempt in range(MAX_REGENERATION_ATTEMPTS):
            result: ValidationResult = self._policy.validate(response, decision)
            if result.is_valid:
                return response

            logger.warning(
                "Validation failed (attempt %d/%d): %s",
                attempt + 1,
                MAX_REGENERATION_ATTEMPTS,
                [str(v.type) if v.type else v.message for v in result.violations],
            )

            response = self._regenerate(response, decision, result)

        logger.error(
            "All %d regeneration attempts exhausted. Returning last response.",
            MAX_REGENERATION_ATTEMPTS,
        )
        return response

    def _generate(self, decision: ConversationDecision) -> str:
        response_type = decision.response_type
        action = decision.action

        if response_type:
            response = self._render_response_type(response_type, decision)
            if response:
                return self._maybe_rephrase(response, decision)

        if action:
            response = self._render_action(action, decision)
            if response:
                return self._maybe_rephrase(response, decision)

        return self._render_fallback(decision)

    def _regenerate(
        self,
        previous: str,
        decision: ConversationDecision,
        result: ValidationResult,
    ) -> str:
        is_llm_fallback = self._llm.last_provider_used == ProviderType.LLM

        if is_llm_fallback:
            return self._generate_stripped(decision)

        forced = self._generate_forced(decision, result)
        if forced:
            return forced

        return self._generate(decision)

    def _render_response_type(self, response_type: str, decision: ConversationDecision) -> str | None:
        template_name = self._map_response_type_to_template(response_type, decision)
        if not template_name:
            return None

        params = self._build_template_params(template_name, decision)
        return get_template(template_name, **params)

    def _map_response_type_to_template(self, response_type: str, decision: ConversationDecision) -> str | None:
        mapping: dict[str, str] = {
            "greeting": "greeting",
            "ask_intent": "ask_intent",
            "ask_city": "ask_city",
            "ask_budget": "ask_budget",
            "ask_property_type": "ask_property_type",
            "ask_bedrooms": "ask_bedrooms",
            "ask_transaction_type": "ask_transaction_type",
            "ask_consent": "ask_consent",
            "search": "await_search",
            "consent": "ask_consent",
            "handover": "handover",
            "error": "error",
            "offer_options": "clarification_options",
        }

        if response_type in mapping:
            return mapping[response_type]

        if response_type == "greeting_returning":
            return "greeting_returning"

        if response_type in ("ask_field",):
            field = decision.expected_input or ""
            field_to_template: dict[str, str] = {
                "intent": "ask_intent",
                "city": "ask_city",
                "budget": "ask_budget",
                "budget_max": "ask_budget",
                "budget_min": "ask_budget",
                "property_type": "ask_property_type",
                "bedrooms": "ask_bedrooms",
                "rooms_min": "ask_bedrooms",
                "transaction_type": "ask_transaction_type",
                "location": "ask_city",
                "surface": "ask_budget",
                "surface_min": "ask_budget",
                "surface_max": "ask_budget",
            }
            return field_to_template.get(field)

        if response_type in ("list_projects",):
            return "project_list"

        if response_type in ("create_project",):
            return None

        if response_type in (
            "clarify_intent",
            "clarify_ambiguous",
            "clarify_result_selection",
            "clarify_consent",
            "clarify_proposal",
            "confirm_project",
        ):
            params = decision.action_parameters or {}
            if "ambiguous_value" in params or "raw_value" in params:
                return "ask_clarification_amount"
            if "alternatives" in params:
                return "clarify_selection"
            return "clarify_selection"

        if response_type == "clarification_received":
            return None

        if response_type == "visit_feedback":
            return None

        return None

    def _render_action(self, action: str, decision: ConversationDecision) -> str | None:
        if decision.loop_detected and action == ACTION_HANDOVER_TO_HUMAN:
            params = self._build_template_params("loop_handover", decision)
            return get_template("loop_handover", **params)

        action_to_template: dict[str, str] = {
            ACTION_GREETING: "greeting",
            ACTION_HANDOVER_TO_HUMAN: "handover",
            ACTION_CREATE_RELATIONSHIP: "relationship_created",
            ACTION_RECORD_CONSENT: "consent_granted",
            ACTION_CREATE_PROJECT: "no_project",
            ACTION_START_SEARCH: "await_search",
            "PRESENT_RESULTS": "results_available",
            ACTION_CLOSE_PROJECT: None,
        }

        template_name = action_to_template.get(action)
        if template_name is None:
            return None

        params = self._build_template_params(template_name, decision)
        return get_template(template_name, **params)

    def _render_fallback(self, decision: ConversationDecision) -> str:
        if decision.requires_clarification:
            return get_template("clarification_repeat", **{}) or "Pourriez-vous reformuler votre réponse ?"
        if decision.loop_detected:
            return get_template("clarification_repeat", **{}) or "Pourriez-vous reformuler votre réponse ?"
        if decision.requires_human:
            return get_template("handover", **{}) or "Je transfère votre demande à un conseiller LAWIM."
        return get_template("clarification_repeat", **{}) or "Pourriez-vous reformuler votre réponse ?"

    def _generate_stripped(self, decision: ConversationDecision) -> str:
        response = self._generate(decision)
        lines = [l for l in response.split("\n") if l.strip()]
        if len(lines) > 2:
            lines = lines[:2]
        return "\n".join(lines)

    def _generate_forced(
        self,
        decision: ConversationDecision,
        result: ValidationResult,
    ) -> str | None:
        action = decision.action

        if action == ACTION_GREETING:
            return get_template("greeting", **{})

        if action == ACTION_REQUEST_CLARIFICATION:
            return get_template("clarification_repeat", **{})

        if action == ACTION_HANDOVER_TO_HUMAN:
            return get_template("handover", **{})

        return None

    def _maybe_rephrase(self, response: str, decision: ConversationDecision) -> str:
        can_rephrase = (
            not decision.requires_clarification
            and not decision.loop_detected
            and decision.response_type not in (
                "handover", "error", "offer_options", "clarification_repeat",
            )
        )
        if not can_rephrase:
            return response

        context: dict[str, Any] = {
            "response_type": decision.response_type,
            "action": decision.action,
            "state_before": decision.state_before.value if decision.state_before else None,
            "state_after": decision.state_after.value if decision.state_after else None,
            "has_projects": bool(decision.project_id),
        }

        rephrased = self._llm.rephrase(response, context)
        if rephrased and rephrased != response:
            return rephrased
        return response

    def _build_template_params(self, template_name: str, decision: ConversationDecision) -> dict[str, Any]:
        params: dict[str, Any] = {}
        action_params = decision.action_parameters or {}
        known_facts = decision.known_facts or {}

        if template_name == "greeting_returning":
            project_summary = known_facts.get("project_summary") or action_params.get("project_summary")
            if not project_summary:
                intent = known_facts.get("intent") or action_params.get("intent", "un projet")
                city = known_facts.get("city") or action_params.get("city", "")
                if city:
                    project_summary = f"{intent} à {city}"
                else:
                    project_summary = str(intent)
            params["project_summary"] = project_summary

        elif template_name == "ask_clarification_amount":
            params["raw_value"] = (
                action_params.get("raw_value")
                or action_params.get("ambiguous_value")
                or ""
            )
            option1 = action_params.get("option1", "")
            option2 = action_params.get("option2", "")
            if not option1:
                option1 = known_facts.get("budget", "")
            if not option2:
                option2 = known_facts.get("budget_alt", "")
            params["option1"] = str(option1)
            params["option2"] = str(option2)

        elif template_name == "project_list":
            alternatives = action_params.get("alternatives", [])
            projects = action_params.get("projects", alternatives)
            if isinstance(projects, list):
                formatted = "\n".join(
                    f"- {p.get('name', p.get('id', str(p)))}"
                    for p in projects
                )
                params["projects"] = formatted
                params["count"] = len(projects)
            else:
                params["projects"] = str(projects)
                params["count"] = str(projects).count("\n") + 1

        elif template_name == "results_available":
            count = action_params.get("count", action_params.get("result_count", 0))
            if decision.dossier_id and not count:
                count = 1
            params["count"] = count

        elif template_name == "ask_consent":
            partner_name = action_params.get("partner_name") or known_facts.get("partner_name", "le professionnel")
            params["partner_name"] = str(partner_name)
            data_fields = action_params.get("data_fields") or known_facts.get("data_fields", "vos informations")
            if isinstance(data_fields, list):
                data_str = ", ".join(str(d) for d in data_fields)
            else:
                data_str = str(data_fields)
            params["data"] = data_str

        elif template_name == "consent_granted":
            pass

        elif template_name == "relationship_created":
            partner_name = action_params.get("partner_name") or known_facts.get("partner_name", "le professionnel")
            params["partner_name"] = str(partner_name)

        elif template_name == "clarification_options":
            options = action_params.get("options") or action_params.get("candidates", [])
            if isinstance(options, list):
                formatted = "\n".join(f"- {o}" for o in options)
            else:
                formatted = str(options)
            params["options"] = formatted

        return params
