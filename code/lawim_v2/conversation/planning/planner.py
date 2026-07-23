from __future__ import annotations

from typing import Any

from ..domain.actions import Action, ActionType
from ..domain.conversation import Conversation
from ..domain.decisions import ConversationDecision
from ..domain.message import NormalizedMessage
from ..domain.states import ConversationState
from .anti_loop import (
    LoopDetectionResult,
    clear_field_repeat,
    detect_loop,
    update_conversation_loop_state,
)
from .dossier_selector import DossierSelectionResult, resolve_dossier_selection
from .next_action_policy import determine_next_action, list_missing_fields
from .project_selector import ProjectSelectionResult, resolve_project_selection
from .transition_policy import can_transition, resolve_transition


class Planner:
    def __init__(self) -> None:
        self._loop_tracking: dict[str, int] = {}
        self._reformulation_count: dict[str, int] = {}

    def plan(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        *,
        active_projects: list[dict[str, Any]] | None = None,
        active_dossiers: list[dict[str, Any]] | None = None,
        intent_candidates: list[dict[str, Any]] | None = None,
        known_facts: dict[str, Any] | None = None,
    ) -> ConversationDecision:
        active_projects = active_projects or []
        active_dossiers = active_dossiers or []
        intent_candidates = intent_candidates or []
        known_facts = known_facts or {}

        decision = ConversationDecision(
            conversation_id=conversation.conversation_id,
            user_id=conversation.user_id,
            channel_identity_id=conversation.channel_identity_id,
            channel=conversation.channel,
            project_id=conversation.project_id,
            dossier_id=conversation.dossier_id,
            raw_message=message.raw_text,
            normalized_message=message.normalized_text,
            state_before=conversation.state,
            state_after=conversation.state,
            known_facts=known_facts,
            intent_candidates=intent_candidates,
        )

        if conversation.state == ConversationState.NEW:
            return self._handle_new(message, conversation, decision)

        if not can_transition(conversation.state, "message_received"):
            if not can_receive_state(conversation.state):
                from uuid import uuid4
                decision.action = ActionType.HANDOVER_TO_HUMAN.value
                decision.requires_human = True
                decision.action_parameters = {
                    "handover_id": str(uuid4()),
                    "reason": "state_not_receiving",
                    "target_team": "support",
                }
                return decision

        handover_decision = self._check_handover(message, conversation, decision)
        if handover_decision:
            return handover_decision

        greeting_decision = self._check_greeting(message, conversation, decision, active_projects)
        if greeting_decision:
            return greeting_decision

        loop_result = detect_loop(
            conversation,
            message.normalized_text,
            current_field=conversation.last_question_field,
            expected_input=conversation.expected_input,
        )
        update_conversation_loop_state(conversation, loop_result)
        decision.loop_detected = loop_result.loop_detected
        decision.loop_score = loop_result.loop_score

        if loop_result.action == "handover":
            from uuid import uuid4
            decision.action = ActionType.HANDOVER_TO_HUMAN.value
            decision.requires_human = True
            decision.action_parameters = {
                "handover_id": str(uuid4()),
                "reason": "loop_exceeded",
                "target_team": "support",
            }
            decision.state_after = ConversationState.HUMAN_HANDOVER
            conversation.apply_transition("loop_exceeded")
            return decision

        if loop_result.action == "offer_options":
            decision.requires_clarification = True
            decision.response_type = "offer_options"
            decision.action = ActionType.REQUEST_CLARIFICATION.value
            return decision

        state = conversation.state

        if state == ConversationState.AWAITING_PROJECT_SELECTION:
            return self._handle_project_selection(
                message, conversation, decision, active_projects, intent_candidates,
            )

        if state == ConversationState.AWAITING_INTENT:
            return self._handle_intent(message, conversation, decision, intent_candidates)

        if state == ConversationState.QUALIFYING:
            return self._handle_qualifying(message, conversation, decision)

        if state == ConversationState.AWAITING_CLARIFICATION:
            return self._handle_clarification(message, conversation, decision)

        if state == ConversationState.READY_FOR_SEARCH:
            return self._handle_ready_for_search(message, conversation, decision)

        if state == ConversationState.SEARCHING:
            decision.action = ActionType.RUN_MATCHING.value
            return decision

        if state == ConversationState.RESULTS_AVAILABLE:
            decision.action = ActionType.PRESENT_RESULTS.value
            return decision

        if state == ConversationState.AWAITING_RESULT_SELECTION:
            return self._handle_result_selection(message, conversation, decision)

        if state == ConversationState.AWAITING_RELATIONSHIP_CONSENT:
            return self._handle_consent(message, conversation, decision)

        if state == ConversationState.RELATIONSHIP_PROPOSED:
            return self._handle_relationship_proposal(message, conversation, decision)

        if state == ConversationState.RELATIONSHIP_ACTIVE:
            decision.action = ActionType.PRESENT_PARTICIPANTS.value
            return decision

        if state == ConversationState.VISIT_PENDING:
            decision.action = ActionType.REQUEST_VISIT.value
            selected_property = getattr(conversation, 'selected_property_id', None) or conversation.facts.get_latest_confirmed("selected_property_id")
            if not selected_property:
                decision.action = ActionType.UPDATE_FACT.value
                decision.response_type = "visit_without_property"
                decision.next_question_text = (
                    "Aucun logement précis n'a encore été sélectionné. Je vais d'abord rechercher les biens "
                    "correspondant à vos critères, puis vous pourrez choisir celui que vous souhaitez visiter."
                    if state.language == "fr" else
                    "No specific property has been selected yet. I will first search for properties "
                    "matching your criteria, then you can choose which one to visit."
                )
            return decision

        if state == ConversationState.VISIT_CONFIRMED:
            decision.action = ActionType.PROVIDE_INFORMATION.value
            return decision

        if state == ConversationState.VISIT_COMPLETED:
            return self._handle_visit_completed(message, conversation, decision)

        if state == ConversationState.FOLLOW_UP:
            decision.action = ActionType.PROVIDE_INFORMATION.value
            return decision

        if state == ConversationState.HUMAN_HANDOVER:
            from uuid import uuid4
            decision.action = ActionType.HANDOVER_TO_HUMAN.value
            decision.requires_human = True
            decision.action_parameters = {
                "handover_id": str(uuid4()),
                "reason": "state_human_handover",
                "target_team": "support",
            }
            return decision

        next_action = determine_next_action(conversation)
        decision.action = next_action["action"].value
        decision.action_parameters = {
            "field": next_action.get("field"),
            "reason": next_action.get("reason"),
        }
        decision.expected_input = next_action.get("field")

        if next_action["action"] == ActionType.UPDATE_FACT:
            decision.response_type = "ask_field"
            decision.expected_input = next_action.get("field")

        return decision

    def _check_handover(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
    ) -> ConversationDecision | None:
        if message.is_handover_request():
            from uuid import uuid4
            decision.action = ActionType.HANDOVER_TO_HUMAN.value
            decision.requires_human = True
            decision.action_parameters = {
                "handover_id": str(uuid4()),
                "reason": "user_requested_human",
                "target_team": "support",
            }
            conversation.apply_transition("handover_requested")
            decision.state_after = conversation.state
            return decision
        return None

    def _check_greeting(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
        active_projects: list[dict[str, Any]],
    ) -> ConversationDecision | None:
        if message.is_greeting() and conversation.state in {
            ConversationState.NEW,
            ConversationState.AWAITING_PROJECT_SELECTION,
            ConversationState.AWAITING_INTENT,
        }:
            decision.action = ActionType.GREETING.value
            decision.response_type = "greeting"
            if conversation.state == ConversationState.NEW:
                conversation.apply_transition("message_received")

            if active_projects:
                conversation.apply_transition("user_identified")
                decision.state_after = conversation.state
            else:
                conversation.apply_transition("message_received")
                decision.state_after = conversation.state
            return decision
        return None

    def _handle_new(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
    ) -> ConversationDecision:
        conversation.apply_transition("message_received")
        decision.state_after = conversation.state
        decision.action = ActionType.GREETING.value
        decision.response_type = "greeting"
        return decision

    def _handle_project_selection(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
        active_projects: list[dict[str, Any]],
        intent_candidates: list[dict[str, Any]],
    ) -> ConversationDecision:
        result: ProjectSelectionResult = resolve_project_selection(
            message.normalized_text,
            active_projects,
            user_id=conversation.user_id,
            conversation_project_id=conversation.project_id,
        )

        decision.action_parameters = {"project_selection": result.action}

        if result.action == "select_existing":
            if result.requires_confirmation:
                decision.requires_clarification = True
                decision.response_type = "confirm_project"
                decision.action = ActionType.SELECT_PROJECT.value
                decision.project_id = result.project_id
                return decision

            decision.project_id = result.project_id
            conversation.project_id = result.project_id
            conversation.apply_transition("project_selected")
            decision.state_after = conversation.state
            decision.action = ActionType.SELECT_PROJECT.value
            decision.action_parameters["project_id"] = result.project_id
            decision.selected_intent = self._pick_best_intent(intent_candidates)

            if conversation.state == ConversationState.AWAITING_INTENT and intent_candidates:
                best = self._pick_best_intent_candidate(intent_candidates)
                if best and best["intent"]:
                    decision.selected_intent = best["intent"]
                    decision.intent_confidence = best.get("confidence", 0.0)
                    conversation.apply_transition("intent_identified")
                    decision.state_after = conversation.state

            return decision

        if result.action == "request_new":
            decision.action = ActionType.CREATE_PROJECT.value
            decision.response_type = "create_project"
            conversation.apply_transition("new_project_requested")
            decision.state_after = conversation.state
            return decision

        if result.action in ("list_projects", "ambiguous", "none"):
            decision.requires_clarification = True
            decision.response_type = "list_projects" if result.action == "list_projects" else "clarification"
            decision.action = ActionType.REQUEST_CLARIFICATION.value
            if result.alternatives:
                decision.action_parameters["alternatives"] = result.alternatives
            conversation.apply_transition("ambiguity_detected")
            decision.state_after = conversation.state
            return decision

        return decision

    def _handle_intent(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
        intent_candidates: list[dict[str, Any]],
    ) -> ConversationDecision:
        best = self._pick_best_intent_candidate(intent_candidates)

        if best and best.get("intent"):
            confidence = best.get("confidence", 0.0)
            decision.selected_intent = best["intent"]
            decision.intent_confidence = confidence
            decision.transaction_type = self._intent_to_transaction_type(best["intent"])

            if confidence >= 0.6:
                conversation.apply_transition("intent_identified")
                decision.state_after = conversation.state
                decision.action = ActionType.UPDATE_FACT.value
                decision.action_parameters = {
                    "field": "intent",
                    "value": best["intent"],
                    "confidence": confidence,
                }
                return decision

            decision.requires_clarification = True
            decision.response_type = "clarify_intent"
            decision.action = ActionType.REQUEST_CLARIFICATION.value
            decision.action_parameters = {
                "candidates": intent_candidates,
                "reason": "low_confidence",
            }
            return decision

        conversation.apply_transition("ambiguity_detected")
        decision.state_after = conversation.state
        decision.requires_clarification = True
        decision.response_type = "clarify_intent"
        decision.action = ActionType.REQUEST_CLARIFICATION.value
        return decision

    def _handle_qualifying(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
    ) -> ConversationDecision:
        missing = list_missing_fields(conversation)

        if not missing:
            ambiguous = conversation.facts.get_ambiguous()
            if not ambiguous:
                conversation.apply_transition("minimum_readiness")
                decision.state_after = conversation.state
                decision.action = ActionType.CREATE_DOSSIER.value
                decision.action_parameters = {"auto_create": True}
                return decision

            decision.requires_clarification = True
            decision.response_type = "clarify_ambiguous"
            decision.action = ActionType.REQUEST_CLARIFICATION.value
            decision.action_parameters = {
                "field": ambiguous[0].field,
                "ambiguous_value": ambiguous[0].raw_value,
            }
            return decision

        next_field = missing[0]
        clear_field_repeat(next_field)
        decision.action = ActionType.UPDATE_FACT.value
        decision.response_type = "ask_field"
        decision.expected_input = next_field
        decision.action_parameters = {
            "field": next_field,
            "reason": f"missing_required_field:{next_field}",
        }
        return decision

    def _handle_clarification(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
    ) -> ConversationDecision:
        conversation.apply_transition("clarification_provided")
        decision.state_after = conversation.state
        decision.action = ActionType.UPDATE_FACT.value
        decision.response_type = "clarification_received"
        return decision

    def _handle_ready_for_search(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
    ) -> ConversationDecision:
        conversation.apply_transition("search_requested")
        decision.state_after = conversation.state
        decision.action = ActionType.START_SEARCH.value
        return decision

    def _handle_result_selection(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
    ) -> ConversationDecision:
        cleaned = message.normalized_text.strip().lower()
        if cleaned in {"oui", "yes", "vas-y", "d'accord", "ok", "ce"}:
            conversation.apply_transition("result_selected")
            decision.state_after = conversation.state
            decision.action = ActionType.CREATE_RELATIONSHIP_PROPOSAL.value
            return decision

        if cleaned in {"non", "no", "pas celui-ci", "autre"}:
            conversation.apply_transition("result_dismissed")
            decision.state_after = conversation.state
            decision.action = ActionType.UPDATE_FACT.value
            decision.action_parameters = {"action": "widen_criteria"}
            return decision

        decision.requires_clarification = True
        decision.response_type = "clarify_result_selection"
        decision.action = ActionType.REQUEST_CLARIFICATION.value
        return decision

    def _handle_consent(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
    ) -> ConversationDecision:
        cleaned = message.normalized_text.strip().lower()
        if cleaned in {"oui", "yes", "j'accepte", "je suis d'accord", "d'accord", "ok"}:
            conversation.apply_transition("consent_granted")
            decision.state_after = conversation.state
            decision.action = ActionType.CREATE_RELATIONSHIP_PROPOSAL.value
            return decision

        if cleaned in {"non", "no", "je refuse", "pas maintenant", "non merci"}:
            conversation.apply_transition("consent_denied")
            decision.state_after = conversation.state
            decision.action = ActionType.RECORD_CONSENT.value
            decision.action_parameters = {"consent": False}
            return decision

        decision.requires_clarification = True
        decision.response_type = "clarify_consent"
        decision.action = ActionType.REQUEST_CLARIFICATION.value
        return decision

    def _handle_relationship_proposal(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
    ) -> ConversationDecision:
        cleaned = message.normalized_text.strip().lower()
        if cleaned in {"oui", "yes", "j'accepte", "je suis d'accord", "d'accord", "ok"}:
            conversation.apply_transition("proposal_accepted")
            decision.state_after = conversation.state
            decision.action = ActionType.CREATE_RELATIONSHIP.value
            return decision

        if cleaned in {"non", "no", "je refuse", "pas maintenant", "non merci"}:
            conversation.apply_transition("proposal_rejected")
            decision.state_after = conversation.state
            decision.action = ActionType.UPDATE_FACT.value
            decision.action_parameters = {"relationship": "rejected"}
            return decision

        decision.requires_clarification = True
        decision.response_type = "clarify_proposal"
        decision.action = ActionType.REQUEST_CLARIFICATION.value
        return decision

    def _handle_visit_completed(
        self,
        message: NormalizedMessage,
        conversation: Conversation,
        decision: ConversationDecision,
    ) -> ConversationDecision:
        conversation.apply_transition("follow_up_needed")
        decision.state_after = conversation.state
        decision.action = ActionType.PROVIDE_INFORMATION.value
        decision.response_type = "visit_feedback"
        return decision

    def _pick_best_intent(self, candidates: list[dict[str, Any]]) -> str | None:
        best = self._pick_best_intent_candidate(candidates)
        return best["intent"] if best else None

    def _pick_best_intent_candidate(self, candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
        if not candidates:
            return None
        return max(candidates, key=lambda c: c.get("confidence", 0.0))

    def _intent_to_transaction_type(self, intent: str) -> str | None:
        if intent.startswith("rent_"):
            return "rent"
        if intent.startswith("buy_"):
            return "buy"
        if intent.startswith("sell_"):
            return "sell"
        if intent == "rent_out":
            return "rent"
        if intent in {"construct", "renovate", "invest"}:
            return intent
        if intent.startswith("find_"):
            return "find_professional"
        return None


def can_receive_state(state: ConversationState) -> bool:
    non_receiving = {
        ConversationState.CLOSED,
        ConversationState.ERROR,
    }
    return state not in non_receiving
