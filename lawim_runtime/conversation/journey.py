from __future__ import annotations

import copy
import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from .intent import IntentEngine, IntentResult
from .entity import EntityExtractionEngine, EntityResult
from .memory import ConversationMemory, MemoryContext
from .qualification import QualificationEngine, QualificationResult, QualificationLevel
from .llm import LLMAdapter, LLMContract

logger = logging.getLogger(__name__)


class JourneyStatus(str, Enum):
    STARTED = "STARTED"
    QUALIFYING = "QUALIFYING"
    WAITING_FOR_CLARIFICATION = "WAITING_FOR_CLARIFICATION"
    READY_FOR_ACTION = "READY_FOR_ACTION"
    ACTION_IN_PROGRESS = "ACTION_IN_PROGRESS"
    ACTION_COMPLETED = "ACTION_COMPLETED"
    ACTION_FAILED = "ACTION_FAILED"
    CANCELLED = "CANCELLED"


class ResponseType(str, Enum):
    ACKNOWLEDGE_AND_CONTINUE = "ACKNOWLEDGE_AND_CONTINUE"
    ASK_CLARIFICATION = "ASK_CLARIFICATION"
    ASK_MISSING_INFORMATION = "ASK_MISSING_INFORMATION"
    ANSWER_DIGRESSION_AND_RESUME = "ANSWER_DIGRESSION_AND_RESUME"
    CONFIRM_QUALIFICATION = "CONFIRM_QUALIFICATION"
    PRESENT_RESULTS = "PRESENT_RESULTS"
    CONFIRM_BUSINESS_ACTION = "CONFIRM_BUSINESS_ACTION"
    REPORT_ACTION_FAILURE = "REPORT_ACTION_FAILURE"
    HANDOFF_TO_HUMAN = "HANDOFF_TO_HUMAN"
    GREETING = "GREETING"


QUESTION_PRIORITY: dict[str, list[str]] = {
    "property_search": ["transaction_type", "property_type", "city", "district", "budget_max", "bedrooms", "move_in_date"],
    "owner_registration": ["property_type", "city", "transaction_type", "price", "bedrooms"],
    "visit_request": ["property_type", "city", "preferred_date"],
}

QUESTION_TEMPLATES_FR: dict[str, str] = {
    "transaction_type": "Vous cherchez à louer, acheter ou vendre ?",
    "property_type": "Quel type de bien recherchez-vous ? (appartement, maison, studio, terrain...)",
    "city": "Dans quelle ville recherchez-vous ?",
    "district": "Dans quel quartier ou zone préférez-vous ?",
    "budget_max": "Quel budget mensuel maximum prévoyez-vous ?",
    "bedrooms": "Combien de chambres souhaitez-vous ?",
    "move_in_date": "À partir de quand souhaitez-vous emménager ?",
    "price": "Quel prix envisagez-vous ?",
    "preferred_date": "Quelle date préférez-vous pour la visite ?",
}


@dataclass
class JourneyState:
    conversation_id: str = field(default_factory=lambda: uuid4().hex[:16])
    journey_type: str = ""
    journey_status: JourneyStatus = JourneyStatus.STARTED
    current_intent: str = ""
    confirmed_facts: dict[str, Any] = field(default_factory=dict)
    fact_history: list[dict[str, Any]] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    last_question: str = ""
    last_question_field: str = ""
    last_user_answer: str = ""
    digression: dict[str, Any] | None = None
    business_object_ids: dict[str, str] = field(default_factory=dict)
    next_step: str = ""
    version: int = 1


@dataclass
class ResponsePlan:
    response_type: ResponseType = ResponseType.ACKNOWLEDGE_AND_CONTINUE
    facts_to_acknowledge: dict[str, Any] = field(default_factory=dict)
    question_field: str = ""
    question_text: str = ""
    business_result: dict[str, Any] | None = None
    safety_constraints: list[str] = field(default_factory=list)
    language: str = "fr"
    message: str = ""


@dataclass
class OrchestrationResult:
    turn_id: str = field(default_factory=lambda: uuid4().hex[:16])
    state: JourneyState | None = None
    intent: IntentResult | None = None
    entities: EntityResult | None = None
    qualification: QualificationResult | None = None
    response_plan: ResponsePlan | None = None
    memory: MemoryContext | None = None
    needs_clarification: bool = False
    error: str = ""


class FactFusionEngine:
    def fuse(self, existing: dict[str, Any], new: dict[str, Any], history: list[dict[str, Any]]) -> dict[str, Any]:
        merged = dict(existing)
        for key, value in new.items():
            if key in existing:
                history.append({"field": key, "previous": existing[key], "new": value, "timestamp": datetime.now(timezone.utc).isoformat()})
            merged[key] = value
        return merged

    def detect_correction(self, existing: dict[str, Any], new: dict[str, Any]) -> list[dict[str, Any]]:
        corrections = []
        for key, value in new.items():
            if key in existing and existing[key] != value:
                corrections.append({"field": key, "old": existing[key], "new": value})
        return corrections


class ConversationJourneyOrchestrator:
    def __init__(
        self,
        intent_engine: IntentEngine | None = None,
        entity_engine: EntityExtractionEngine | None = None,
        memory: ConversationMemory | None = None,
        qualification_engine: QualificationEngine | None = None,
        llm_adapter: LLMAdapter | None = None,
    ) -> None:
        self._intent = intent_engine or IntentEngine()
        self._entity = entity_engine or EntityExtractionEngine()
        self._memory = memory or ConversationMemory()
        self._qualification = qualification_engine or QualificationEngine()
        self._llm = llm_adapter
        self._fusion = FactFusionEngine()

    def process(
        self,
        text: str,
        state: JourneyState | None = None,
        channel: str = "web",
    ) -> OrchestrationResult:
        result = OrchestrationResult()

        if not text or not text.strip():
            result.error = "empty_input"
            return result

        if state is None:
            state = JourneyState()

        # 1. Intent detection
        intent_result = self._intent.detect(text)
        if state.current_intent and intent_result.intent in ("greeting", "unknown"):
            intent_result.intent = state.current_intent
            intent_result.confidence = 0.8
        result.intent = intent_result

        if state.journey_status == JourneyStatus.STARTED:
            state.current_intent = intent_result.intent
            if intent_result.intent == "greeting":
                state.journey_status = JourneyStatus.QUALIFYING
                result.response_plan = ResponsePlan(
                    response_type=ResponseType.GREETING,
                    message="\U0001f916 LAWIM AI\n\nBonjour et bienvenue sur LAWIM. Veuillez décrire votre projet immobilier du jour en quelques lignes : achat, vente, location, terrain, gestion ou autre besoin.",
                )
                return result

        # 2. Entity extraction
        entity_result = self._entity.extract(text)
        result.entities = entity_result

        # 3. Check for digression (question not matching current journey)
        is_digression = self._detect_digression(text, entity_result, state)
        if is_digression and state.journey_status == JourneyStatus.QUALIFYING:
            state.digression = {"question": text, "answer": self._answer_digression(text)}
            result.response_plan = ResponsePlan(
                response_type=ResponseType.ANSWER_DIGRESSION_AND_RESUME,
                message=state.digression["answer"],
            )
            return result

        # 4. Fact fusion
        corrections = self._fusion.detect_correction(state.confirmed_facts, entity_result.entities)
        state.confirmed_facts = self._fusion.fuse(state.confirmed_facts, entity_result.entities, state.fact_history)

        # 5. Detect ambiguity
        if self._detect_ambiguity(text, entity_result):
            state.journey_status = JourneyStatus.WAITING_FOR_CLARIFICATION
            result.response_plan = ResponsePlan(
                response_type=ResponseType.ASK_CLARIFICATION,
                question_field="location_precision",
                question_text="Pouvez-vous préciser le lieu ? Proche de quel quartier ou repère ?",
            )
            result.needs_clarification = True
            return result

        # 6. Memory update
        self._memory.add_entry("user", text, intent_result.intent, entity_result.entities)
        if entity_result.entities:
            self._memory.update_preferences(entity_result.entities)

        # 7. Qualification
        qual_result = self._qualification.evaluate(state.current_intent, state.confirmed_facts)
        state.missing_fields = qual_result.missing_fields
        result.qualification = qual_result
        self._memory.set_qualification(qual_result.level.value)

        # 8. Build response plan
        response_plan = self._build_response_plan(state, qual_result, corrections, entity_result)
        result.response_plan = response_plan

        # 9. If qualified, attempt business action
        if qual_result.level in (QualificationLevel.QUALIFIED, QualificationLevel.READY_FOR_DECISION) and not state.business_object_ids:
            biz_result = self._execute_business_action(state)
            if biz_result:
                state.business_object_ids.update(biz_result)
                state.journey_status = JourneyStatus.ACTION_COMPLETED if biz_result.get("success") else JourneyStatus.ACTION_FAILED

        state.journey_status = JourneyStatus.QUALIFYING if qual_result.missing_fields else JourneyStatus.READY_FOR_ACTION
        state.version += 1
        result.state = state
        result.memory = self._memory.get_context()
        self._memory.add_entry("assistant", response_plan.message if response_plan else "")

        return result

    def _detect_digression(self, text: str, entity: EntityResult, state: JourneyState) -> bool:
        if not state.confirmed_facts:
            return False
        question_markers = ["comment", "pourquoi", "est-ce que", "c'est quoi", "combien coûte", "frais", "payant", "gratuit"]
        lower = text.lower()
        for marker in question_markers:
            if marker in lower:
                return True
        return False

    def _answer_digression(self, text: str) -> str:
        lower = text.lower()
        if "frais" in lower or "payant" in lower or "gratuit" in lower:
            return "Les visites sont généralement gratuites. Certains propriétaires ou agences peuvent demander une participation symbolique. Je vous conseille de vérifier directement avec le propriétaire au moment de la visite."
        if "document" in lower or "papier" in lower:
            return "Les documents habituellement demandés sont une pièce d'identité, un justificatif de revenus et parfois un garant. Chaque propriétaire peut avoir ses propres exigences."
        return "Je prends note de votre question. Pouvons-nous reprendre là où nous étions ?"

    def _detect_ambiguity(self, text: str, entity: EntityResult) -> bool:
        ambiguous = ["proche", "pas loin", "près", "vers", "du côté de", "quelque part"]
        lower = text.lower()
        for word in ambiguous:
            if word in lower and "city" not in entity.entities and "district" not in entity.entities:
                return True
        return False

    def _build_response_plan(self, state: JourneyState, qual: QualificationResult, corrections: list[dict[str, Any]], entity: EntityResult) -> ResponsePlan:
        plan = ResponsePlan(language="fr")

        if qual.level == QualificationLevel.READY_FOR_DECISION:
            plan.response_type = ResponseType.CONFIRM_QUALIFICATION
            facts = state.confirmed_facts
            parts = []
            if "property_type" in facts:
                labels = {"apartment": "appartement", "house": "maison", "studio": "studio", "land": "terrain"}
                parts.append(f"un {labels.get(facts['property_type'], facts['property_type'])}")
            if "bedrooms" in facts:
                parts.append(f"{facts['bedrooms']} chambres")
            if "transaction_type" in facts:
                t = {"rent": "louer", "buy": "acheter", "sell": "vendre"}
                parts.append(f"à {t.get(facts['transaction_type'], facts['transaction_type'])}")
            if "city" in facts:
                parts.append(f"à {facts['city']}")
            if "district" in facts:
                parts.append(f"dans le quartier {facts['district']}")
            if "budget_max" in facts:
                parts.append(f"avec un budget de {facts['budget_max']} FCFA")
            plan.message = "Je récapitule votre recherche : " + ", ".join(parts) + ". Je procède à la recherche des biens correspondants."
            return plan

        if corrections:
            corr = corrections[0]
            plan.facts_to_acknowledge = {corr["field"]: corr["new"]}
            plan.response_type = ResponseType.ACKNOWLEDGE_AND_CONTINUE
            plan.message = f"Je prends note de votre correction : {corr['field']} passe à {corr['new']}."
            missing = self._next_question(state, qual)
            if missing:
                plan.question_field = missing
                plan.question_text = QUESTION_TEMPLATES_FR.get(missing, f"Pouvez-vous préciser {missing} ?")
                plan.response_type = ResponseType.ASK_MISSING_INFORMATION
            return plan

        missing = self._next_question(state, qual)
        if missing:
            plan.response_type = ResponseType.ASK_MISSING_INFORMATION
            plan.question_field = missing
            plan.question_text = QUESTION_TEMPLATES_FR.get(missing, f"Pouvez-vous indiquer {missing} ?")
            ack = self._build_acknowledgement(state)
            if ack:
                plan.facts_to_acknowledge = state.confirmed_facts
                plan.message = ack
            return plan

        plan.response_type = ResponseType.CONFIRM_QUALIFICATION
        return plan

    def _next_question(self, state: JourneyState, qual: QualificationResult) -> str:
        if not qual.missing_fields:
            return ""
        priority = QUESTION_PRIORITY.get(state.current_intent, list(QUESTION_TEMPLATES_FR.keys()))
        for field in priority:
            if field in qual.missing_fields and field != state.last_question_field:
                state.last_question_field = field
                return field
        for field in qual.missing_fields:
            if field != state.last_question_field:
                state.last_question_field = field
                return field
        return qual.missing_fields[0] if qual.missing_fields else ""

    def _build_acknowledgement(self, state: JourneyState) -> str:
        facts = state.confirmed_facts
        parts = []
        if "city" in facts:
            parts.append(f"J'ai noté que vous cherchez à {facts.get('transaction_type', 'louer')}")
            if "property_type" in facts:
                labels = {"apartment": "un appartement", "house": "une maison", "studio": "un studio", "land": "un terrain"}
                parts.append(labels.get(facts["property_type"], facts["property_type"]))
            parts.append(f"à {facts['city']}")
            return " ".join(parts) + "."
        return ""

    def _execute_business_action(self, state: JourneyState) -> dict[str, Any] | None:
        try:
            facts = state.confirmed_facts
            intent = state.current_intent
            if intent == "property_search":
                return {
                    "success": True,
                    "action": "search_created",
                    "search_id": uuid4().hex[:16],
                    "message": "Recherche enregistrée",
                }
            elif intent == "owner_registration":
                return {
                    "success": True,
                    "action": "property_registered",
                    "property_id": uuid4().hex[:16],
                    "message": "Bien enregistré",
                }
        except Exception as e:
            return {"success": False, "action": "failed", "error": str(e)}
        return None

    def load_state(self, state: JourneyState) -> None:
        self._memory = ConversationMemory()
        for entry in getattr(state, "fact_history", []):
            self._memory.update_preferences(entry)

    def get_memory(self) -> ConversationMemory:
        return self._memory
