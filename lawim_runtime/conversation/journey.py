from __future__ import annotations

import copy
import json
import logging
import re
import unicodedata
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Protocol
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

TRANSACTION_LABELS_FR: dict[str, str] = {
    "rent": "à louer",
    "buy": "à acheter",
    "sell": "à vendre",
    "invest": "pour investir",
}

PROPERTY_LABELS_FR: dict[str, str] = {
    "apartment": "un appartement",
    "house": "une maison",
    "studio": "un studio",
    "land": "un terrain",
    "commercial": "un local commercial",
}

CITY_DISPLAY: dict[str, str] = {
    "Yaounde": "Yaoundé",
    "Douala": "Douala",
    "Bafoussam": "Bafoussam",
    "Kribi": "Kribi",
    "Limbe": "Limbe",
}

CONFIRMATION_KEYWORDS = [
    "oui", "enregistre", "valide", "confirme", "vas-y", "vas y", "d'accord", "ok",
    "bien", "procède", "procédez", "je confirme", "je valide", "envoie",
]


@dataclass
class BusinessActionResult:
    success: bool = False
    action: str = ""
    object_type: str | None = None
    object_id: str | None = None
    message: str | None = None
    error_code: str | None = None


class PropertySearchService(Protocol):
    def create_search_request(
        self,
        *,
        conversation_id: str,
        user_id: str | None = None,
        channel: str = "web",
        facts: dict[str, Any] | None = None,
        idempotency_key: str = "",
    ) -> BusinessActionResult:
        ...


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
    last_facts_snapshot: dict[str, Any] = field(default_factory=dict)


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


CLARIFICATION_DISTRICTS: dict[str, str] = {
    "centre-ville": "Centre-Ville", "centre ville": "Centre-Ville",
    "mvan": "Mvan", "bastos": "Bastos", "odza": "Odza",
    "nlongkak": "Nlongkak", "tsinga": "Tsinga", "ngousso": "Ngousso",
    "essos": "Essos", "mendong": "Mendong", "biyem-assi": "Biyem-Assi",
    "biyem assi": "Biyem-Assi", "makepe": "Makepe",
    "bonanjo": "Bonanjo", "bonamoussadi": "Bonamoussadi",
    "akwa": "Akwa", "melen": "Melen", "ngoa": "Ngoa",
    "ngoa-ekellé": "Ngoa-Ekellé", "ngoa-ekelle": "Ngoa-Ekellé",
    "ekoumdoum": "Ekoumdoum", "tam-tam": "Tam-Tam",
    "mokolo": "Mokolo", "mimboman": "Mimboman",
    "nyalla": "Nyalla", "carrière": "Carrière",
    "carriere": "Carrière",
}

CLARIFICATION_LANDMARKS: dict[str, str] = {
    "hôpital": "hôpital", "hopital": "hôpital", "centre de santé": "centre de santé",
    "marché": "marché", "marche": "marché",
    "lycée": "lycée", "école": "école", "ecole": "école", "université": "université",
    "carrefour": "carrefour",
    "axe": "axe", "route": "axe",
    "gare": "gare", "aéroport": "aéroport",
    "banque": "banque",
    "église": "église", "mosquée": "mosquée",
}


def _normalize(text: str) -> str:
    """Strip accents and lowercase for matching, preserving original for display."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).casefold()


def _build_landmark_pattern() -> re.Pattern:
    raw = (
        r"(?:"
        r"à côté (?:du|de la|de l['’]|des)?"
        r"|a cote (?:du|de la|de l['’]|des)?"
        r"|près de l['’]?"
        r"|pres de l['’]?"
        r"|proche (?:du|de la|de l['’]|des)?"
        r"|vers (?:le|la|l['’])?"
        r"|autour (?:du|de la|de l['’])?"
        r"|au (?:niveau du|niveau de la)?"
        r"|dans le secteur"
        r"|dans la zone"
        r")\s*"
        r"(.{3,80})$"
    )
    return re.compile(raw, re.IGNORECASE | re.DOTALL)


_LANDMARK_PATTERN = _build_landmark_pattern()


class ConversationJourneyOrchestrator:
    def __init__(
        self,
        intent_engine: IntentEngine | None = None,
        entity_engine: EntityExtractionEngine | None = None,
        memory: ConversationMemory | None = None,
        qualification_engine: QualificationEngine | None = None,
        llm_adapter: LLMAdapter | None = None,
        property_search_service: PropertySearchService | None = None,
    ) -> None:
        self._intent = intent_engine or IntentEngine()
        self._entity = entity_engine or EntityExtractionEngine()
        self._memory = memory or ConversationMemory()
        self._qualification = qualification_engine or QualificationEngine()
        self._llm = llm_adapter
        self._fusion = FactFusionEngine()
        self._property_search_service = property_search_service

    def process(
        self,
        text: str,
        state: JourneyState | None = None,
        channel: str = "web",
    ) -> OrchestrationResult:
        result = OrchestrationResult()

        if not text or not text.strip():
            result.error = "empty_input"
            result.response_plan = ResponsePlan(
                response_type=ResponseType.ACKNOWLEDGE_AND_CONTINUE,
                message="Je n'ai pas compris votre message. Pouvez-vous reformuler ?",
            )
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
                setattr(state, "_channel", channel)
                result.response_plan = ResponsePlan(
                    response_type=ResponseType.GREETING,
                    message="\U0001f916 LAWIM AI\n\nBonjour et bienvenue sur LAWIM. Veuillez décrire votre projet immobilier du jour en quelques lignes : achat, vente, location, terrain, gestion ou autre besoin.",
                )
                return result
        else:
            # Update current intent from non-greeting, non-digression intent
            # (preserve main intent through digressions)
            is_question = any(m in _normalize(text) for m in 
                ["comment", "pourquoi", "est-ce que", "c'est quoi", "combien", "frais", "payant", "gratuit"])
            if intent_result.intent not in ("greeting", "unknown") and not is_question:
                state.current_intent = intent_result.intent

        # 2. Entity extraction (always runs)
        entity_result = self._entity.extract(text)
        result.entities = entity_result

        # 3. Fact fusion (always runs, regardless of journey status)
        corrections = self._fusion.detect_correction(state.confirmed_facts, entity_result.entities)
        state.confirmed_facts = self._fusion.fuse(state.confirmed_facts, entity_result.entities, state.fact_history)

        # 4. Memory update (always runs)
        self._memory.add_entry("user", text, intent_result.intent, entity_result.entities)
        if entity_result.entities:
            self._memory.update_preferences(entity_result.entities)

        # 5. Handle WAITING_FOR_CLARIFICATION (resolve ambiguity)
        if state.journey_status == JourneyStatus.WAITING_FOR_CLARIFICATION:
            return self._handle_clarification(text, entity_result, state, result)

        # 6. Check for digression
        is_digression = self._detect_digression(text, entity_result, state)
        if is_digression and state.journey_status != JourneyStatus.ACTION_COMPLETED:
            state.digression = {"question": text, "answer": self._answer_digression(text)}
            if state.journey_status == JourneyStatus.READY_FOR_ACTION:
                state.journey_status = JourneyStatus.QUALIFYING
            result.state = state
            result.response_plan = ResponsePlan(
                response_type=ResponseType.ANSWER_DIGRESSION_AND_RESUME,
                message=state.digression["answer"],
            )
            return result

        # 7. Detect ambiguity
        if self._detect_ambiguity(text, entity_result):
            state.journey_status = JourneyStatus.WAITING_FOR_CLARIFICATION
            state.last_facts_snapshot = dict(state.confirmed_facts)
            result.state = state
            result.response_plan = ResponsePlan(
                response_type=ResponseType.ASK_CLARIFICATION,
                question_field="location_precision",
                question_text="Pouvez-vous préciser le lieu ? Proche de quel quartier ou repère ?",
            )
            result.needs_clarification = True
            return result

        # 8. Qualification
        qual_result = self._qualification.evaluate(state.current_intent, state.confirmed_facts)
        state.missing_fields = qual_result.missing_fields
        result.qualification = qual_result
        self._memory.set_qualification(qual_result.level.value)

        # 9. Check for explicit user confirmation or corrections to execute business action
        if state.journey_status in (JourneyStatus.READY_FOR_ACTION, JourneyStatus.QUALIFYING, JourneyStatus.ACTION_COMPLETED):
            lower = text.lower().strip()
            is_confirmation = any(kw in lower for kw in CONFIRMATION_KEYWORDS)
            already_completed = bool(state.business_object_ids)
            is_ready = qual_result.level == QualificationLevel.READY_FOR_DECISION

            if already_completed and corrections:
                # Correction after business action completed — re-execute
                biz_result = self._execute_business_action(state)
                if biz_result:
                    state.business_object_ids.update(biz_result)
                    state.journey_status = JourneyStatus.ACTION_COMPLETED if biz_result.get("success") else JourneyStatus.ACTION_FAILED
            elif not already_completed and is_confirmation and is_ready:
                biz_result = self._execute_business_action(state)
                if biz_result:
                    state.business_object_ids.update(biz_result)
                    state.journey_status = JourneyStatus.ACTION_COMPLETED if biz_result.get("success") else JourneyStatus.ACTION_FAILED

        # 10. Build response plan
        response_plan = self._build_response_plan(state, qual_result, corrections, entity_result)
        result.response_plan = response_plan

        if state.journey_status not in (JourneyStatus.ACTION_COMPLETED, JourneyStatus.ACTION_FAILED):
            can_be_ready = qual_result.level == QualificationLevel.READY_FOR_DECISION and state.current_intent not in ("", "greeting", "unknown")
            state.journey_status = JourneyStatus.QUALIFYING if (qual_result.missing_fields or not can_be_ready) else JourneyStatus.READY_FOR_ACTION
        state.last_facts_snapshot = dict(state.confirmed_facts)
        state.version += 1
        result.state = state
        result.memory = self._memory.get_context()
        self._memory.add_entry("assistant", response_plan.message if response_plan else "")

        return result

    def _handle_clarification(self, text: str, entity: EntityResult, state: JourneyState, result: OrchestrationResult) -> OrchestrationResult:
        lower = text.lower().strip()
        affirmation = lower in ("oui", "d'accord", "ok", "bien", "dac", "si", "exactement", "voilà", "ça marche")
        if affirmation:
            state.journey_status = JourneyStatus.QUALIFYING
            qual_result = self._qualification.evaluate(state.current_intent, state.confirmed_facts)
            state.missing_fields = qual_result.missing_fields
            result.qualification = qual_result
            missing = self._next_question(state, qual_result)
            if missing:
                result.response_plan = ResponsePlan(
                    response_type=ResponseType.ASK_MISSING_INFORMATION,
                    question_field=missing,
                    question_text=QUESTION_TEMPLATES_FR.get(missing, f"Pouvez-vous indiquer {missing} ?"),
                    message="D'accord, je conserve les informations actuelles.",
                )
            else:
                result.response_plan = ResponsePlan(
                    response_type=ResponseType.CONFIRM_QUALIFICATION,
                    message="D'accord, je conserve les informations actuelles.",
                )
            result.state = state
            return result

        # Try entity engine first (may extract city or district from the answer)
        has_district = "district" in entity.entities
        has_city = "city" in entity.entities
        clarification_field = None
        clarification_value = None

        if has_district:
            clarification_field = "district"
            clarification_value = entity.entities["district"]
        elif has_city:
            clarification_field = "city"
            clarification_value = entity.entities["city"]
        else:
            # Try known districts
            for fr_key, en_val in CLARIFICATION_DISTRICTS.items():
                if fr_key in lower:
                    clarification_field = "district"
                    clarification_value = en_val
                    break

        if not clarification_field:
            # Try landmarks — capture the full landmark name from text
            lower_norm = _normalize(text)
            for fr_key, en_val in CLARIFICATION_LANDMARKS.items():
                if _normalize(fr_key) in lower_norm:
                    # Use the regex to capture the full landmark phrase
                    landmark_match = _LANDMARK_PATTERN.search(text)
                    if landmark_match:
                        raw = landmark_match.group(1).strip().rstrip(".,!?;")
                        clarification_field = "proximity_reference"
                        clarification_value = raw
                    else:
                        clarification_field = "proximity_reference"
                        clarification_value = en_val
                    break

            if not clarification_field:
                # Try capturing any location phrase after ambiguous triggers
                landmark_match = _LANDMARK_PATTERN.search(text)
                if landmark_match:
                    raw = landmark_match.group(1).strip().rstrip(".,!?;")
                    if len(raw) >= 3:
                        clarification_field = "proximity_reference"
                        clarification_value = raw

        if not clarification_field:
            # Check if unrelated answer (digression during clarification)
            is_new_digression = self._detect_digression(text, entity, state)
            if is_new_digression:
                state.digression = {"question": text, "answer": self._answer_digression(text)}
                result.state = state
                result.response_plan = ResponsePlan(
                    response_type=ResponseType.ANSWER_DIGRESSION_AND_RESUME,
                    message=state.digression["answer"],
                )
                state.journey_status = JourneyStatus.WAITING_FOR_CLARIFICATION
                return result
            # Unresolved — ask again with different wording
            state.journey_status = JourneyStatus.WAITING_FOR_CLARIFICATION
            result.state = state
            retry_count = getattr(state, "_clarification_retry", 0) + 1
            setattr(state, "_clarification_retry", retry_count)
            retry_messages = [
                "Je n'ai pas bien compris. Pouvez-vous préciser le nom d'un quartier, d'un point de repère ou d'un axe routier ?",
                "Je n'arrive pas à identifier le lieu. Donnez-moi le nom d'un quartier, d'un marché ou d'un carrefour connu.",
                "Pouvez-vous être plus précis ? Un quartier, une rue ou un bâtiment connu m'aiderait.",
            ]
            question_text = retry_messages[min(retry_count - 1, len(retry_messages) - 1)]
            result.response_plan = ResponsePlan(
                response_type=ResponseType.ASK_CLARIFICATION,
                question_field="location_precision",
                question_text=question_text,
            )
            result.needs_clarification = True
            return result

        # Handle the resolved clarification
        state.confirmed_facts = self._fusion.fuse(state.confirmed_facts, {clarification_field: clarification_value}, state.fact_history)
        state.journey_status = JourneyStatus.QUALIFYING
        result.state = state

        qual_result = self._qualification.evaluate(state.current_intent, state.confirmed_facts)
        state.missing_fields = qual_result.missing_fields
        result.qualification = qual_result

        label = clarification_value or "ce lieu"
        missing = self._next_question(state, qual_result)
        if missing:
            result.response_plan = ResponsePlan(
                response_type=ResponseType.ASK_MISSING_INFORMATION,
                question_field=missing,
                question_text=QUESTION_TEMPLATES_FR.get(missing, f"Pouvez-vous indiquer {missing} ?"),
                message=f"Merci, je note {label}.",
            )
        else:
            result.response_plan = ResponsePlan(
                response_type=ResponseType.CONFIRM_QUALIFICATION,
                message=f"Merci, je note {label}.",
            )
        state.last_facts_snapshot = dict(state.confirmed_facts)
        state.version += 1
        return result

    def _detect_digression(self, text: str, entity: EntityResult, state: JourneyState) -> bool:
        if not state.confirmed_facts:
            return False
        question_markers = ["comment", "pourquoi", "est-ce que", "c'est quoi", "combien coûte", "frais", "payant", "gratuit"]
        lower = _normalize(text)
        for marker in question_markers:
            if marker in lower:
                return True
        return False

    def _answer_digression(self, text: str) -> str:
        lower = text.lower()
        if "frais" in lower or "payant" in lower or "gratuit" in lower:
            return "Les conditions d'une visite peuvent dépendre du bien ou du partenaire concerné. Elles doivent vous être précisées avant toute visite."
        if "document" in lower or "papier" in lower:
            return "Les documents habituellement demandés sont une pièce d'identité, un justificatif de revenus et parfois un garant. Chaque propriétaire peut avoir ses propres exigences."
        return "Je prends note de votre question. Pouvons-nous reprendre là où nous étions ?"

    def _detect_ambiguity(self, text: str, entity: EntityResult) -> bool:
        ambiguous = ["proche", "pres", "pas loin", "près", "vers", "du côté de", "quelque part", "a cote", "autour"]
        lower = _normalize(text)
        for word in ambiguous:
            if word in lower and "city" not in entity.entities and "district" not in entity.entities:
                return True
        return False

    def _build_response_plan(self, state: JourneyState, qual: QualificationResult, corrections: list[dict[str, Any]], entity: EntityResult) -> ResponsePlan:
        plan = ResponsePlan(language="fr")

        facts = state.confirmed_facts
        original_recap = self._format_facts(facts)
        recap_text = ", ".join(original_recap) if original_recap else ""
        facts_changed = bool(corrections) or (state.last_facts_snapshot and facts != state.last_facts_snapshot)
        biz_completed = bool(state.business_object_ids)
        biz_success = biz_completed and state.business_object_ids.get("success") == True

        # Level 3 — business action succeeded with confirmed persistence
        if biz_completed and biz_success:
            if qual.level == QualificationLevel.READY_FOR_DECISION and not facts_changed:
                plan.response_type = ResponseType.CONFIRM_BUSINESS_ACTION
                plan.message = "Votre demande a bien été enregistrée. Puis-je vous aider avec autre chose ?"
                return plan
            if facts_changed and recap_text:
                plan.response_type = ResponseType.CONFIRM_BUSINESS_ACTION
                plan.message = "Je mets à jour votre demande : " + recap_text + "."
                return plan

        # Level 2 — business action failed
        if biz_completed and not biz_success:
            plan.response_type = ResponseType.REPORT_ACTION_FAILURE
            plan.message = "Je n'ai pas pu enregistrer votre demande pour le moment. Vous pouvez réessayer plus tard."
            return plan

        if qual.level == QualificationLevel.READY_FOR_DECISION:
            plan.response_type = ResponseType.CONFIRM_QUALIFICATION
            if not facts_changed and state.last_facts_snapshot:
                if state.missing_fields:
                    plan.message = "J'ai déjà pris en compte ces informations. " + self._next_question_message(state)
                else:
                    plan.message = "Les informations de votre recherche sont complètes. Souhaitez-vous que je l'enregistre ?"
                return plan
            if recap_text:
                plan.message = "Je récapitule votre recherche : " + recap_text + ". Je procède à la recherche des biens correspondants."
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
        if not plan.message and state.missing_fields:
            plan.message = "Pouvez-vous preciser " + ", ".join(state.missing_fields[:3]) + " ?"
        elif not plan.message:
            plan.message = "Je prends note de vos informations. Continuez lorsque vous serez prets."
        return plan

    def _format_facts(self, facts: dict[str, Any]) -> list[str]:
        parts = []
        if "property_type" in facts:
            plabel = PROPERTY_LABELS_FR.get(facts["property_type"], facts["property_type"])
            parts.append(plabel)
        if "bedrooms" in facts:
            parts.append(f"{facts['bedrooms']} chambres")
        if "transaction_type" in facts:
            tlabel = TRANSACTION_LABELS_FR.get(facts["transaction_type"], facts["transaction_type"])
            parts.append(tlabel)
        if "city" in facts:
            cdisplay = CITY_DISPLAY.get(facts["city"], facts["city"])
            parts.append(f"à {cdisplay}")
        if "preferred_areas" in facts and isinstance(facts["preferred_areas"], list) and facts["preferred_areas"]:
            areas = ", ".join(facts["preferred_areas"])
            parts.append(f"dans le secteur {areas}")
        elif "district" in facts:
            parts.append(f"dans le quartier {facts['district']}")
        if "budget_max" in facts:
            parts.append(f"avec un budget de {facts['budget_max']} FCFA")
        if "move_in_date" in facts:
            parts.append(f"emménagement {facts['move_in_date']}")
        return parts

    def _next_question_message(self, state: JourneyState) -> str:
        if state.missing_fields:
            field = state.missing_fields[0]
            return QUESTION_TEMPLATES_FR.get(field, f"Pouvez-vous indiquer {field} ?")
        return ""

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
            ttype = facts.get("transaction_type", "")
            tlabel = TRANSACTION_LABELS_FR.get(ttype, ttype) if ttype else "louer"
            parts.append(f"J'ai noté que vous cherchez {tlabel}")
            if "property_type" in facts:
                plabel = PROPERTY_LABELS_FR.get(facts["property_type"], facts["property_type"])
                parts.append(plabel)
            cdisplay = CITY_DISPLAY.get(facts.get("city", ""), facts.get("city", ""))
            parts.append(f"à {cdisplay}")
            return " ".join(parts) + "."
        return ""

    def _execute_business_action(self, state: JourneyState) -> dict[str, Any] | None:
        if self._property_search_service is None:
            return None
        facts = state.confirmed_facts
        intent = state.current_intent
        if intent == "property_search":
            conv_id = state.conversation_id
            idem_key = f"pf:{conv_id}:property_search"
            result = self._property_search_service.create_search_request(
                conversation_id=conv_id,
                channel=getattr(state, "_channel", "web"),
                facts=facts,
                idempotency_key=idem_key,
            )
            if result.success:
                return {
                    "success": True,
                    "action": result.action,
                    "object_type": result.object_type or "property_search_request",
                    "object_id": result.object_id or "",
                    "message": result.message or "",
                }
            else:
                return {
                    "success": False,
                    "action": result.action,
                    "error": result.error_code or "business_error",
                }
        return None

    def load_state(self, state: JourneyState) -> None:
        self._memory = ConversationMemory()
        for entry in getattr(state, "fact_history", []):
            self._memory.update_preferences(entry)

    def get_memory(self) -> ConversationMemory:
        return self._memory
