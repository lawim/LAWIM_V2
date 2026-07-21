from __future__ import annotations

from typing import Any

from ..state.state import ResponsePlan, ConversationTurnDecision, ConversationState
from .dialogue_plan import DialoguePlan
from .internal_engine import LawimInternalResponseEngine
from .language_policy import LawimLanguagePolicy
from .persona import LawimConversationPersona, get_lawim_persona
from .validator import LawimConversationPolicyValidator


class LawimConversationPolicy:
    def __init__(
        self,
        persona: LawimConversationPersona | None = None,
        language_policy: LawimLanguagePolicy | None = None,
        validator: LawimConversationPolicyValidator | None = None,
        internal_engine: LawimInternalResponseEngine | None = None,
    ) -> None:
        self.persona = persona or get_lawim_persona()
        self.language_policy = language_policy or LawimLanguagePolicy()
        self.validator = validator or LawimConversationPolicyValidator()
        self.internal_engine = internal_engine or LawimInternalResponseEngine()

    def build_dialogue_plan(
        self,
        state: ConversationState,
        decision: ConversationTurnDecision | None = None,
        response_plan: ResponsePlan | None = None,
        actor: dict[str, Any] | None = None,
        channel: str = "",
        message: str = "",
    ) -> DialoguePlan:
        language = state.language or "fr"

        dialogue_act = self._detect_dialogue_act(
            state, decision, response_plan, message,
        )

        plan = DialoguePlan(
            speaker="LAWIM AI",
            language=language,
            dialogue_act=dialogue_act,
            facts_to_confirm=dict(self._get_facts_to_confirm(state, dialogue_act, response_plan)),
            next_question_key=state.last_question_key or "",
            maximum_questions=self.persona.maximum_questions,
            maximum_sentences=self.persona.maximum_sentences,
            maximum_characters=self.persona.maximum_characters,
            tone=list(self.persona.tone),
            footer_required=True,
            generated_by_ai=False,
        )

        if response_plan and response_plan.next_question_text:
            plan.rendered_next_question = response_plan.next_question_text

        # Apply persona forbidden lists
        plan.forbidden_phrases = list(self.persona.prohibited_claims)
        plan.forbidden_topics = list(self.persona.prohibited_referrals)

        return plan

    def _detect_dialogue_act(
        self,
        state: ConversationState,
        decision: ConversationTurnDecision | None = None,
        response_plan: ResponsePlan | None = None,
        message: str = "",
    ) -> str:
        missing = state.missing_slots or []

        if response_plan and response_plan.response_type == "HANDOVER_ACK":
            return "HANDOVER"

        if response_plan and response_plan.response_type == "REPHRASE":
            return "REPHRASE_LAST_QUESTION"

        if response_plan and response_plan.response_type == "CLARIFICATION":
            return "CLARIFY_CURRENT_SLOT"

        if response_plan and response_plan.response_type == "QUALIFICATION_COMPLETE":
            return "SEARCH_READY"

        if response_plan and response_plan.response_type == "GREETING":
            return "WELCOME"

        if state.current_intent is None and not state.known_slots:
            return "WELCOME"

        if response_plan and response_plan.response_type == "QUESTION":
            return "ACKNOWLEDGE_AND_ASK"

        if response_plan and response_plan.updated_slots:
            if any(
                key in (response_plan.updated_slots or {})
                for key in ("confirmation", "consent")
            ):
                return "SUMMARIZE_AND_CONFIRM"

        if state.current_intent and missing:
            return "ACKNOWLEDGE_AND_ASK"

        if state.current_intent and not missing:
            return "SEARCH_READY"

        return "ACKNOWLEDGE_AND_ASK"

    def _get_facts_to_confirm(
        self,
        state: ConversationState,
        dialogue_act: str,
        response_plan: ResponsePlan | None = None,
    ) -> dict[str, Any]:
        if dialogue_act == "WELCOME":
            return {}
        if dialogue_act == "REPHRASE_LAST_QUESTION":
            return {}
        if dialogue_act == "HANDOVER":
            return {}
        if response_plan and response_plan.updated_slots:
            return dict(response_plan.updated_slots)
        if response_plan and response_plan.acknowledgement_facts:
            return dict(response_plan.acknowledgement_facts)
        return dict(state.known_slots)
