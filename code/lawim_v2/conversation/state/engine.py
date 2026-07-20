from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from ..understanding.extractor import extract_all
from ...knowledge_runtime.engine.wizard import ProgressiveWizard
from .resolver import ConversationResolver
from .repository import ConversationStateRepository
from .state import ConversationState, ConversationStateUpdate, ResponsePlan


_GREETING_WORDS = {"bonjour", "bonsoir", "salut", "hello", "hi", "slt", "bjr", "cc", "coucou", "hey", "yo"}
_HANDOVER_PHRASES = [
    "parler a une personne", "parler a un conseiller", "agent lawim",
    "conseiller lawim", "humain", "personne reelle", "parler a quelqu'un",
    "operateur", "assistance", "parler à une personne", "parler à un conseiller",
]
_GREETING_RESPONSES: dict[str, str] = {
    "fr": "Bonjour et bienvenue sur LAWIM.\n\nJe peux vous accompagner pour rechercher, publier, louer, acheter ou vendre un bien immobilier. Que souhaitez-vous faire ?",
    "en": "Hello and welcome to LAWIM.\n\nI can help you search for, list, rent, buy or sell a property. What would you like to do?",
    "pcm": "Welcome for LAWIM.\n\nI fit help you find, post, rent, buy or sell property. Wetin you want do?",
}


class ConversationStateEngine:
    def __init__(
        self,
        repository: ConversationStateRepository,
        resolver: ConversationResolver,
        wizard: ProgressiveWizard | None = None,
    ) -> None:
        self._repository = repository
        self._resolver = resolver
        self._wizard = wizard

    def process_turn(
        self,
        actor_id: int | str | None,
        channel: str,
        external_conversation_id: str,
        message: str,
        language: str = "fr",
    ) -> dict[str, Any]:
        channel_session_id, _ = self._resolver.resolve(channel, external_conversation_id, actor_id)

        state = self._resolve_or_create_state(channel, channel_session_id, language)
        state.actor_id = actor_id or state.actor_id
        state.last_user_message = message
        state.updated_at = datetime.now(timezone.utc).isoformat()

        normalized_lower = message.strip().lower().rstrip("!.,? ")
        first_word = normalized_lower.split()[0] if normalized_lower.split() else ""

        is_greeting = first_word in _GREETING_WORDS or normalized_lower in _GREETING_WORDS
        is_handover = any(phrase in normalized_lower for phrase in _HANDOVER_PHRASES)

        if is_handover:
            plan = self._build_handover_plan(state)
            response_text = self._generate_response(plan, state)
            state.last_lawim_message = response_text
            state.last_action = "handover_requested"
            self._repository.save(state)
            return {
                "state": state,
                "response": response_text,
                "response_plan": plan,
                "handover_required": True,
                "wizard_completed": False,
                "actions": [{"action": "handover_requested", "status": "executed"}],
            }

        if is_greeting:
            plan = self._build_greeting_plan(state)
            response_text = self._generate_response(plan, state)
            state.last_lawim_message = response_text
            state.last_action = "greeting"
            self._repository.save(state)
            return {
                "state": state,
                "response": response_text,
                "response_plan": plan,
                "handover_required": False,
                "wizard_completed": False,
                "actions": [],
            }

        extracted = extract_all(message)
        update = self._extracted_to_update(extracted, message)
        state = self._merge_update(state, update)

        wizard_result = None
        wizard_completed = False
        next_question_key = ""
        next_question_text = ""

        if self._wizard is not None and state.qualification_status != "completed":
            wizard_result = self._run_wizard(state, update.new_slots, channel)
            if wizard_result:
                next_question_key = wizard_result["next_question_key"]
                next_question_text = wizard_result["next_question_text"]
                wizard_completed = wizard_result.get("completed", False)
                if wizard_completed:
                    state.qualification_status = "completed"

        plan = self._build_response_plan(state, wizard_result)
        response_text = self._generate_response(plan, state)

        state.last_lawim_message = response_text
        state.last_question_key = next_question_key
        state.last_action = plan.next_action or "respond"
        self._repository.save(state)

        return {
            "state": state,
            "response": response_text,
            "response_plan": plan,
            "handover_required": plan.handover_required,
            "wizard_completed": wizard_completed,
            "actions": [],
        }

    def _resolve_or_create_state(
        self,
        channel: str,
        channel_session_id: str,
        language: str,
    ) -> ConversationState:
        existing = self._repository.load(channel, channel_session_id)
        if existing is not None:
            return existing
        now = datetime.now(timezone.utc).isoformat()
        return ConversationState(
            channel=channel,
            channel_session_id=channel_session_id,
            language=language,
            qualification_status="unqualified",
            created_at=now,
            updated_at=now,
        )

    def _extracted_to_update(
        self,
        extracted: dict[str, Any],
        raw_message: str,
    ) -> ConversationStateUpdate:
        new_slots: dict[str, Any] = {}
        for fact in extracted.get("facts", []):
            field = fact.get("field")
            value = fact.get("normalized_value") or fact.get("raw_value")
            if field and value is not None:
                new_slots[field] = value

        intent = None
        for fact in extracted.get("facts", []):
            if fact.get("field") == "transaction_type":
                intent = fact.get("normalized_value") or fact.get("raw_value")
                break
        if not intent:
            for fact in extracted.get("facts", []):
                if fact.get("field") == "property_type":
                    intent = fact.get("normalized_value") or fact.get("raw_value")
                    break

        return ConversationStateUpdate(
            new_intent=intent,
            new_slots=new_slots,
        )

    def _merge_update(
        self,
        state: ConversationState,
        update: ConversationStateUpdate,
    ) -> ConversationState:
        if update.new_intent:
            state.previous_intent = state.current_intent
            state.current_intent = update.new_intent
            state.intent_confidence = 1.0

        for key, value in update.new_slots.items():
            if value is not None:
                state.known_slots[key] = value

        state.missing_slots = []
        state.updated_at = datetime.now(timezone.utc).isoformat()
        return state

    def _run_wizard(
        self,
        state: ConversationState,
        new_slots: dict[str, Any],
        channel: str,
    ) -> dict[str, Any] | None:
        if self._wizard is None:
            return None

        session_id = state.wizard_session_id
        if not session_id:
            session_id = str(uuid4())
            state.wizard_session_id = session_id
            self._wizard.create_session(session_id, channel=channel)

        session = self._wizard.get_session(session_id)
        if session is None:
            session = self._wizard.create_session(session_id, channel=channel)

        if session.completed:
            state.qualification_status = "completed"
            return {
                "completed": True,
                "next_question_key": "",
                "next_question_text": "",
            }

        for field, value in new_slots.items():
            result = self._wizard.submit_answer(session_id, field, value)
            if isinstance(result, dict) and result.get("error"):
                continue

        current_info = self._wizard.get_current_step_info(session_id)
        if isinstance(current_info, dict) and current_info.get("error"):
            state.qualification_status = "unqualified"
            return None

        completed = current_info.get("completed", False)
        if completed:
            state.qualification_status = "completed"

        next_q = current_info.get("next_question", {}) or {}
        next_question_key = next_q.get("field") or ""
        next_question_text = self._get_question_text(next_question_key, state.language)

        return {
            "completed": completed,
            "next_question_key": next_question_key,
            "next_question_text": next_question_text,
            "current_step": current_info.get("step"),
            "step_name": current_info.get("name", ""),
            "known_fields": current_info.get("known_fields", {}),
        }

    def _get_question_text(self, field: str, language: str) -> str:
        QUESTIONS: dict[str, dict[str, str]] = {
            "intent": {"fr": "Que recherchez-vous ?", "en": "What are you looking for?", "pcm": "Wetin you dey find?"},
            "transaction_type": {"fr": "Souhaitez-vous acheter, louer ou vendre ?", "en": "Do you want to buy, rent or sell?", "pcm": "You want buy, rent or sell?"},
            "property_type": {"fr": "Quel type de bien ?", "en": "What type of property?", "pcm": "Wetin kind property?"},
            "city": {"fr": "Dans quelle ville ?", "en": "In which city?", "pcm": "Which city?"},
            "neighborhood": {"fr": "Dans quel quartier ?", "en": "In which neighborhood?", "pcm": "Which area?"},
            "budget_max": {"fr": "Quel est votre budget maximum ?", "en": "What is your maximum budget?", "pcm": "Your maximum budget?"},
            "budget_min": {"fr": "Quel est votre budget minimum ?", "en": "What is your minimum budget?", "pcm": "Your minimum budget?"},
            "bedroom_count": {"fr": "Combien de chambres ?", "en": "How many bedrooms?", "pcm": "How many bedrooms?"},
            "surface": {"fr": "Quelle surface ?", "en": "What surface area?", "pcm": "Wetin be surface?"},
        }
        return QUESTIONS.get(field, {}).get(language, QUESTIONS.get(field, {}).get("fr", ""))

    def _build_greeting_plan(self, state: ConversationState) -> ResponsePlan:
        text = _GREETING_RESPONSES.get(state.language, _GREETING_RESPONSES["fr"])
        return ResponsePlan(
            language=state.language,
            response_type="GREETING",
            next_action="await_intent",
            response_template=text,
        )

    def _build_handover_plan(self, state: ConversationState) -> ResponsePlan:
        messages: dict[str, str] = {
            "fr": "Je comprends. Je vais vous mettre en relation avec un conseiller LAWIM qui pourra vous assister.",
            "en": "I understand. I will connect you with a LAWIM advisor who can assist you.",
            "pcm": "I sabi. I go connect you with LAWIM advisor wey fit help you.",
        }
        text = messages.get(state.language, messages["fr"])
        return ResponsePlan(
            language=state.language,
            response_type="HANDOVER_ACK",
            next_action="handover",
            handover_required=True,
            handover_reason="user_requested_human",
            response_template=text,
        )

    def _build_response_plan(
        self,
        state: ConversationState,
        wizard_result: dict[str, Any] | None,
    ) -> ResponsePlan:
        if wizard_result is None:
            return ResponsePlan(
                language=state.language,
                response_type="ACKNOWLEDGE",
                next_action="await_input",
                acknowledgement_facts=dict(state.known_slots),
            )

        completed = wizard_result.get("completed", False)
        next_q_key = wizard_result.get("next_question_key", "")
        next_q_text = wizard_result.get("next_question_text", "")

        if completed:
            return ResponsePlan(
                language=state.language,
                response_type="QUALIFICATION_COMPLETE",
                next_action="search",
                next_question_key="",
                next_question_text="",
                response_template="Merci ! Vos informations sont completes. Je lance la recherche..." if state.language == "fr" else "Thank you! Your information is complete. Starting search...",
            )

        if next_q_key:
            return ResponsePlan(
                language=state.language,
                response_type="QUESTION",
                next_action="collect_field",
                next_question_key=next_q_key,
                next_question_text=next_q_text,
                response_template=next_q_text,
            )

        return ResponsePlan(
            language=state.language,
            response_type="ACKNOWLEDGE",
            next_action="await_input",
            response_template="Merci. Pouvez-vous me donner plus de details ?" if state.language == "fr" else "Thank you. Can you provide more details?",
        )

    def _generate_response(self, plan: ResponsePlan, state: ConversationState) -> str:
        if plan.response_template:
            return plan.response_template
        if plan.next_question_text:
            return plan.next_question_text
        messages: dict[str, str] = {
            "fr": "Merci. Continuez a nous fournir les informations necessaires.",
            "en": "Thank you. Please continue providing the required information.",
            "pcm": "Thank you. Abeg continue to give us di information wey we need.",
        }
        return messages.get(state.language, messages["fr"])
