from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from ..qualification.priority_registry import (
    QualificationJourneyDefinition,
    QualificationPriorityRegistry,
    QualificationSlotDefinition,
)
from ..qualification.question_catalog import get_question as get_catalog_question
from ..understanding.extractor import extract_all
from ...knowledge_runtime.engine.wizard import ProgressiveWizard
from .resolver import ConversationResolver
from .repository import ConversationStateRepository
from .state import (
    ConversationState,
    ConversationStateUpdate,
    QualificationDecision,
    ResponsePlan,
)
from .validator import ConversationResponseValidator


_GREETING_WORDS = {"bonjour", "bonsoir", "salut", "hello", "hi", "slt", "bjr", "cc", "coucou", "hey", "yo"}
_HANDOVER_PHRASES = [
    "parler a une personne", "parler a un conseiller", "agent lawim",
    "conseiller lawim", "humain", "personne reelle", "parler a quelqu'un",
    "operateur", "assistance", "parler à une personne", "parler à un conseiller",
]
_REPHRASE_PHRASES = [
    "je ne comprends pas", "je n'ai pas compris", "expliquez",
    "reformulez", "c'est-à-dire", "c'est a dire", "what do you mean",
    "i don't understand", "i no understand", "explain",
]
_REAL_ESTATE_DOMAIN_WORDS = {
    "appartement", "studio", "maison", "villa", "terrain", "bureau", "local",
    "commerce", "magasin", "entrepôt", "entrepot", "garage", "parking",
    "chambre", "duplex", "immeuble", "logement", "propriete", "bien",
    "location", "louer", "acheter", "vendre", "investir", "habitation",
    "residence", "surface", "m2", "piece", "cuisine", "salon", "balcon",
}
_FRENCH_MARKERS = {"bonjour", "je", "j'", "mon", "ma", "mes", "ton", "ta", "ses", "nous", "vous", "ils", "elles", "le", "la", "les", "un", "une", "des", "du", "au", "aux", "est", "sont", "dans", "pour", "avec", "sur", "que", "qui", "quoi", "comment", "pourquoi", "quand", "ou", "où", "merci", "s'il vous plaît", "s'il te plaît", "svp", "stp"}
_ENGLISH_MARKERS = {"hello", "hi", "the", "a", "an", "my", "your", "his", "her", "our", "their", "i", "you", "he", "she", "it", "we", "they", "is", "are", "was", "were", "in", "on", "at", "for", "with", "to", "from", "this", "that", "please", "thank", "would", "could", "should", "want", "need"}
_PCM_MARKERS = {"dey", "na", "di", "wey", "fit", "abi", "komot", "wetin", "make", "sabi", "abeg", "broda", "sista"}

def _detect_language(text: str) -> str | None:
    """Detect the language of a message based on common markers."""
    words = set(text.lower().split())
    fr_score = len(words & _FRENCH_MARKERS)
    en_score = len(words & _ENGLISH_MARKERS)
    pcm_score = len(words & _PCM_MARKERS)
    # PCM markers also match some English — subtract commonality
    en_score -= pcm_score // 2
    if fr_score > en_score and fr_score > pcm_score:
        return "fr"
    if pcm_score > en_score and pcm_score > fr_score:
        return "pcm"
    if en_score > 0:
        return "en"
    return None

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
        policy = None,
    ) -> None:
        self._repository = repository
        self._resolver = resolver
        self._wizard = wizard
        self._policy = policy

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

        clean_message = message.strip().rstrip("!.,?;: ")
        normalized_lower = clean_message.lower()
        first_word = normalized_lower.split()[0] if normalized_lower.split() else ""

        # Preserve active language — never switch unless user explicitly uses another language for several turns
        detected_lang = _detect_language(message)
        if detected_lang and detected_lang != state.language:
            state.language = detected_lang

        # Detect real estate domain for ambiguous terms
        has_real_estate_keywords = any(kw in normalized_lower for kw in _REAL_ESTATE_DOMAIN_WORDS)

        is_greeting = first_word in _GREETING_WORDS or normalized_lower in _GREETING_WORDS
        is_handover = any(phrase in normalized_lower for phrase in _HANDOVER_PHRASES)
        is_rephrase_request = any(phrase in normalized_lower for phrase in _REPHRASE_PHRASES)

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

        # Handle rephrase requests — reformulate last question without changing state
        if is_rephrase_request and state.last_question_key:
            plan = self._build_rephrase_plan(state)
            response_text = self._generate_response(plan, state)
            state.last_lawim_message = response_text
            state.last_action = "rephrase"
            self._repository.save(state)
            return {
                "state": state,
                "response": response_text,
                "response_plan": plan,
                "handover_required": False,
                "wizard_completed": False,
                "actions": [{"action": "rephrase", "status": "executed"}],
            }

        if is_rephrase_request:
            plan = self._build_acknowledge_plan(state)
            response_text = self._generate_response(plan, state)
            state.last_lawim_message = response_text
            state.last_action = "rephrase"
            self._repository.save(state)
            return {
                "state": state,
                "response": response_text,
                "response_plan": plan,
                "handover_required": False,
                "wizard_completed": False,
                "actions": [{"action": "rephrase", "status": "executed"}],
            }

        # Contextualize short answers based on last question
        if state.last_question_key and len(message.split()) <= 5 and (
            not has_real_estate_keywords
            or any(w in normalized_lower for w in ("habitation", "residen", "vivre", "loger", "usage personnel", "personnel"))
        ):
            contextualized = self._try_contextualize_short_answer(state, message)
            if contextualized:
                return contextualized

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

        correction = self._handle_correction(message, state)
        if correction:
            return correction

        extracted = extract_all(clean_message)
        update = self._extracted_to_update(extracted, message)

        if not update.new_slots and clean_message and state.last_question_slot:
            contextual = self._contextualize_short_reply(clean_message, state)
            if contextual:
                update.new_slots.update(contextual)

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

        plan = self._build_response_plan(state, wizard_result, update.new_slots)
        response_text = self._generate_response(plan, state)

        state.last_lawim_message = response_text
        state.last_question_key = next_question_key
        state.last_question_slot = plan.next_question_key or ""
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

    def _contextualize_short_reply(self, clean_message: str, state: ConversationState) -> dict[str, object]:
        from ..understanding.money import normalize_amount
        from ..understanding.geography import KNOWN_NEIGHBORHOODS, NEIGHBORHOOD_TO_CITY
        result: dict[str, object] = {}
        slot = state.last_question_slot
        if slot in ("budget_max", "budget", "budget_min", "budget_xaf"):
            amount = normalize_amount(clean_message)
            if amount.confidence > 0 and amount.normalized_amount is not None:
                result[slot] = amount.normalized_amount
            else:
                import re
                budget_match = re.search(r'(\d[\d\s]{2,})\s*(?:fcf a|francs|cfa)?', clean_message, re.IGNORECASE)
                if budget_match:
                    val = int(re.sub(r'\s', '', budget_match.group(1)))
                    result[slot] = val
                elif re.match(r'^\d{4,}$', clean_message.strip()):
                    result[slot] = int(clean_message.strip())
                elif re.match(r'^(\d+)\s*k$', clean_message.strip(), re.IGNORECASE):
                    result[slot] = int(re.match(r'^(\d+)\s*k$', clean_message.strip(), re.IGNORECASE).group(1)) * 1000
        if slot in ("neighborhood", "district", "city", "location"):
            lower = clean_message.lower()
            if lower in KNOWN_NEIGHBORHOODS:
                result["neighborhood"] = KNOWN_NEIGHBORHOODS[lower]
                city = NEIGHBORHOOD_TO_CITY.get(lower)
                if city:
                    result["city"] = city
            elif lower in {k.lower(): v for k, v in KNOWN_NEIGHBORHOODS.items()}:
                pass
            elif lower in ("akwa", "bonamoussadi", "makepe", "bali", "bonanjo", "bonapriso", "deido", "ndokoti", "bassa", "logbaba", "bepanda"):
                result["district"] = lower.title()
        if slot in ("bedrooms", "bedroom_count", "chambres"):
            import re
            bedroom_map = {"un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6}
            lower = clean_message.lower().strip()
            if lower in bedroom_map:
                result[slot] = bedroom_map[lower]
            elif re.match(r'^\d+$', lower):
                result[slot] = int(lower)
        if slot in ("furnished", "meuble"):
            lower = clean_message.lower().strip()
            if lower in ("oui", "yes", "meublé", "meuble", "yeah", "d'accord", "ok"):
                result[slot] = True
            elif lower in ("non", "no", "pas meublé", "pas meuble", "vide", "nope"):
                result[slot] = False
        if slot in ("move_in_date", "availability_date", "preferred_date"):
            import re
            lower = clean_message.lower()
            date_map = {
                "le mois prochain": "next_month",
                "dans 2 mois": "in_2_months",
                "dans 3 mois": "in_3_months",
                "ce mois-ci": "this_month",
                "cette semaine": "this_week",
                "la semaine prochaine": "next_week",
                "dès que possible": "asap",
                "asap": "asap",
            }
            if lower in date_map:
                result[slot] = date_map[lower]
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', clean_message.strip()):
                result[slot] = clean_message.strip()
        if slot in ("confirmation", "consent"):
            lower = clean_message.lower().strip()
            if lower in ("oui", "yes", "ok", "d'accord", "d accord", "yeah", "confirmé", "confirme"):
                result[slot] = True
            elif lower in ("non", "no", "nope", "pas maintenant", "annuler"):
                result[slot] = False
        return result

    def _handle_correction(
        self,
        message: str,
        state: ConversationState,
    ) -> dict[str, Any] | None:
        lower = message.lower().strip()
        correction_keywords = {"finalement", "plutôt", "plutot", "je voulais dire", "je voulais plutôt", "correction", "rectification", "non pas", "pas ça", "je veux dire"}
        has_correction = any(kw in lower for kw in correction_keywords)

        if not has_correction:
            return None

        from ..understanding.extractor import extract_all
        extracted = extract_all(message)
        update = ConversationStateUpdate()
        corrected_slots: dict[str, Any] = {}

        for fact in extracted.get("facts", []):
            field = fact.get("field")
            value = fact.get("normalized_value") or fact.get("raw_value")
            if field and value is not None:
                corrected_slots[field] = value
                if field in state.known_slots:
                    update.corrected_slots[field] = state.known_slots[field]
                update.new_slots[field] = value

        if "finalement" in lower and "budget" in lower:
            import re
            nums = re.findall(r'[\d\s]{3,}', message)
            if nums:
                val = int(re.sub(r'\s', '', nums[0]))
                if "budget_max" in state.known_slots:
                    update.corrected_slots["budget_max"] = state.known_slots["budget_max"]
                update.new_slots["budget_max"] = val
                corrected_slots["budget_max"] = val
            else:
                amount_match = re.search(r'(\d[\d\s]{2,})\s*(?:fcf ?a|francs|cfa)?', message, re.IGNORECASE)
                if amount_match:
                    val = int(re.sub(r'\s', '', amount_match.group(1)))
                    if "budget_max" in state.known_slots:
                        update.corrected_slots["budget_max"] = state.known_slots["budget_max"]
                    update.new_slots["budget_max"] = val
                    corrected_slots["budget_max"] = val

        if corrected_slots:
            for key, new_value in corrected_slots.items():
                state.known_slots[key] = new_value
            state.updated_at = __import__("datetime").datetime.now(
                __import__("datetime").timezone.utc
            ).isoformat()
            channel = getattr(state, 'channel', 'whatsapp')
            return self._continue_with_wizard(state, corrected_slots, channel=channel)

        return None

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
        catalog_key = f"qualification.{field}"
        catalog_text = get_catalog_question(catalog_key, language)
        if catalog_text:
            return catalog_text
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

    def _try_contextualize_short_answer(
        self,
        state: ConversationState,
        message: str,
    ) -> dict[str, Any] | None:
        """Try to interpret a short message as an answer to the last question."""
        last_slot = state.last_question_slot
        if not last_slot:
            return None

        clean = message.strip().lower().rstrip("!.,?;: ")
        update = ConversationStateUpdate()

        if last_slot in ("budget_xaf", "budget_max", "budget_min", "budget"):
            from ..understanding.extractor import extract_all
            extracted = extract_all(message)
            for fact in extracted.get("facts", []):
                field = fact.get("field")
                value = fact.get("normalized_value") or fact.get("raw_value")
                if field and value is not None:
                    update.new_slots[field.replace("price_", "budget_")] = value
            if not update.new_slots:
                import re
                budget_match = re.search(r'(\d[\d\s]{2,})\s*(?:fcf ?a|francs|cfa)?', message, re.IGNORECASE)
                if budget_match:
                    val = int(re.sub(r'\s', '', budget_match.group(1)))
                    update.new_slots[last_slot] = val
                elif re.match(r'^\d{4,}$', clean):
                    update.new_slots[last_slot] = int(clean)
                elif re.match(r'^(\d+)\s*k$', clean, re.IGNORECASE):
                    val = int(re.match(r'^(\d+)\s*k$', clean, re.IGNORECASE).group(1)) * 1000
                    update.new_slots[last_slot] = val
                else:
                    nums = re.findall(r'[\d\s]{3,}', message)
                    if nums:
                        val = int(re.sub(r'\s', '', nums[0]))
                        update.new_slots[last_slot] = val
            if last_slot in update.new_slots:
                update.new_slots["budget_period"] = "monthly"

        elif last_slot in ("city", "ville"):
            update.new_slots["city"] = clean.title()

        elif last_slot in ("neighborhood", "district", "quartier"):
            known_districts = {"akwa", "bonamoussadi", "makepe", "bali", "bonanjo", "bonapriso", "deido", "ndokoti", "bassa", "logbaba", "bepanda", "nkolbisson", "mendong", "biyem-assi", "mfoundi", "bastos", "tsinga", "omnisports"}
            if clean in known_districts:
                update.new_slots["district"] = clean.title()
            else:
                update.new_slots["district"] = clean.title()

        elif last_slot in ("transaction_type",):
            _habitation_in_clean = any(
                w in clean for w in ("habitation", "residen", "vivre", "loger", "usage personnel", "personnel")
            )
            if _habitation_in_clean:
                update.new_slots["property_usage"] = "residential"
                if state.known_slots.get("property_type"):
                    update.new_slots["property_type"] = state.known_slots["property_type"]
            elif "louer" in clean or "location" in clean or "loc" in clean:
                update.new_slots["transaction_type"] = "rent"
            elif "acheter" in clean or "achat" in clean or "buy" in clean:
                update.new_slots["transaction_type"] = "buy"
            elif "vendre" in clean or "vente" in clean or "sell" in clean:
                update.new_slots["transaction_type"] = "sell"

        elif last_slot in ("property_type", "type_bien"):
            _habitation_in_clean = any(
                w in clean for w in ("habitation", "residen", "vivre", "loger", "usage personnel", "personnel")
            )
            if _habitation_in_clean:
                update.new_slots["property_usage"] = "residential"
                if state.known_slots.get("property_type"):
                    update.new_slots["property_type"] = state.known_slots["property_type"]
            elif "studio" in clean:
                update.new_slots["property_type"] = "studio"
                update.new_slots["property_usage"] = "residential"
            elif "appartement" in clean or "apartment" in clean:
                update.new_slots["property_type"] = "apartment"
            elif "maison" in clean or "house" in clean:
                update.new_slots["property_type"] = "house"
            elif "terrain" in clean or "land" in clean:
                update.new_slots["property_type"] = "land"
            elif "bureau" in clean or "office" in clean:
                update.new_slots["property_type"] = "office"
            elif "local" in clean:
                update.new_slots["property_type"] = "commercial"

        elif last_slot in ("furnished", "meuble"):
            if clean in ("oui", "yes", "meublé", "meuble", "yeah", "d'accord", "d accord", "ok"):
                update.new_slots["furnished"] = True
            elif clean in ("non", "no", "pas meublé", "pas meuble", "vide", "nope", "pas"):
                update.new_slots["furnished"] = False

        elif last_slot in ("property_usage", "usage"):
            if "habitation" in clean or "residen" in clean or "vivre" in clean or "loger" in clean:
                update.new_slots["property_usage"] = "residential"
            elif "commercial" in clean or "bureau" in clean or "professionnel" in clean:
                update.new_slots["property_usage"] = "commercial"

        elif last_slot in ("bedrooms", "bedroom_count", "chambres"):
            bedroom_map = {"un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6}
            if clean in bedroom_map:
                update.new_slots[last_slot] = bedroom_map[clean]
            else:
                import re
                if re.match(r'^\d+$', clean):
                    update.new_slots[last_slot] = int(clean)

        elif last_slot in ("move_in_date", "availability_date", "preferred_date"):
            import re
            date_map = {
                "le mois prochain": "next_month",
                "dans 2 mois": "in_2_months",
                "dans 3 mois": "in_3_months",
                "ce mois-ci": "this_month",
                "cette semaine": "this_week",
                "la semaine prochaine": "next_week",
                "dès que possible": "asap",
                "asap": "asap",
            }
            if clean in date_map:
                update.new_slots[last_slot] = date_map[clean]
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', clean):
                update.new_slots[last_slot] = clean

        elif last_slot in ("confirmation", "consent"):
            if clean in ("oui", "yes", "ok", "d'accord", "d accord", "yeah", "confirmé", "confirme"):
                update.new_slots[last_slot] = True
            elif clean in ("non", "no", "nope", "pas maintenant", "annuler"):
                update.new_slots[last_slot] = False

        if not update.new_slots:
            return None

        state = self._merge_update(state, update)
        return self._continue_with_wizard(state, update.new_slots, channel="whatsapp")

    def _continue_with_wizard(
        self,
        state: ConversationState,
        new_slots: dict[str, Any],
        channel: str,
    ) -> dict[str, Any] | None:
        wizard_result = None
        wizard_completed = False
        next_question_key = ""
        next_question_text = ""

        if self._wizard is not None and state.qualification_status != "completed":
            wizard_result = self._run_wizard(state, new_slots, channel)
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

    def _build_rephrase_plan(self, state: ConversationState) -> ResponsePlan:
        """Reformulate the last question without changing state."""
        rephrase_texts: dict[str, str] = {
            "budget_max": "Quel est votre budget maximum ? Par exemple : 100 000 FCFA par mois.",
            "budget_xaf": "Quel budget avez-vous prévu ?",
            "city": "Dans quelle ville ou localité cherchez-vous ?",
            "neighborhood": "Dans quel quartier préférez-vous ?",
            "district": "Quel quartier vous intéresse ?",
            "property_type": "Quel type de bien cherchez-vous ? (appartement, studio, maison, terrain...)",
            "transaction_type": "Souhaitez-vous louer, acheter ou vendre ?",
            "furnished": "Voulez-vous un logement meublé ou non meublé ?",
            "property_usage": "S'agit-il d'une habitation ou d'un usage commercial ?",
            "bedrooms": "Combien de chambres souhaitez-vous ?",
        }
        base = rephrase_texts.get(state.last_question_key or "", "")
        if not base:
            base = "Pourriez-vous reformuler votre réponse ?"
        text = f"Je reformule ma question : {base}"
        return ResponsePlan(
            language=state.language,
            response_type="REPHRASE",
            next_action="await_input",
            next_question_key=state.last_question_key or "",
            next_question_text=base,
            response_template=text,
        )

    def _build_greeting_plan(self, state: ConversationState) -> ResponsePlan:
        text = _GREETING_RESPONSES.get(state.language, _GREETING_RESPONSES["fr"])
        return ResponsePlan(
            language=state.language,
            response_type="GREETING",
            next_action="await_intent",
            response_template=text,
        )

    def _build_handover_plan(self, state: ConversationState) -> ResponsePlan:
        from uuid import uuid4
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
            handover_target_team="support",
            handover_id=str(uuid4()),
            response_template=text,
        )

    def _build_clarify_plan(
        self,
        state: ConversationState,
        slot_key: str = "",
    ) -> ResponsePlan:
        key = slot_key or state.last_question_key or state.last_question_slot
        question_key = ""
        if key and not key.startswith("qualification."):
            question_key = f"qualification.{key}"
        else:
            question_key = key
        clarification_text = get_catalog_question(
            question_key.replace("qualification.", "qualification.clarify."),
            state.language,
        )
        if not clarification_text:
            clarification_text = get_catalog_question(question_key, state.language)
        if not clarification_text:
            clarification_text = "Pourriez-vous reformuler votre réponse ?"
        return ResponsePlan(
            language=state.language,
            response_type="CLARIFICATION",
            next_action="CLARIFY_CURRENT_SLOT",
            next_question_key=key,
            next_question_text=clarification_text,
            response_template=clarification_text,
        )

    def _build_acknowledge_plan(self, state: ConversationState) -> ResponsePlan:
        messages: dict[str, str] = {
            "fr": "Merci. Pouvez-vous reformuler votre demande ?",
            "en": "Thank you. Could you rephrase your request?",
            "pcm": "Thank you. You fit talk am again?",
        }
        text = messages.get(state.language, messages["fr"])
        return ResponsePlan(
            language=state.language,
            response_type="ACKNOWLEDGE",
            next_action="await_input",
            response_template=text,
        )

    def _build_response_plan(
        self,
        state: ConversationState,
        wizard_result: dict[str, Any] | None,
        updated_slots: dict[str, Any] | None = None,
    ) -> ResponsePlan:
        resolved_updated = dict(updated_slots or {})
        if wizard_result is None:
            return ResponsePlan(
                language=state.language,
                response_type="ACKNOWLEDGE",
                next_action="await_input",
                acknowledgement_facts=dict(state.known_slots),
                updated_slots=resolved_updated,
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
                updated_slots=resolved_updated,
            )

        if next_q_key:
            return ResponsePlan(
                language=state.language,
                response_type="QUESTION",
                next_action="collect_field",
                next_question_key=next_q_key,
                next_question_text=next_q_text,
                response_template=next_q_text,
                updated_slots=resolved_updated,
            )

        ambiguous = wizard_result.get("ambiguous", False)
        if ambiguous:
            return self._build_clarify_plan(
                state,
                slot_key=wizard_result.get("next_question_key", ""),
            )

        return ResponsePlan(
            language=state.language,
            response_type="ACKNOWLEDGE",
            next_action="await_input",
            response_template="Merci. Pouvez-vous me donner plus de details ?" if state.language == "fr" else "Thank you. Can you provide more details?",
            updated_slots=resolved_updated,
        )

    def _build_acknowledgement_text(self, slots: dict[str, Any], language: str) -> str:
        parts: list[str] = []
        for key, value in slots.items():
            if key in ("budget_max", "budget"):
                parts.append(f"avec un budget de {value} FCFA")
            elif key == "property_type":
                parts.append(f"de type {value}")
            elif key == "city":
                parts.append(f"à {value}")
            elif key == "neighborhood":
                parts.append(f"dans le quartier {value}")
            elif key == "bedroom_count":
                parts.append(f"de {value} chambres")
        if not parts:
            return ""
        if language == "fr":
            return "Très bien. Vous recherchez " + ", ".join(parts) + "."
        if language == "en":
            return "Very well. You are looking for " + ", ".join(parts) + "."
        return "Okay. You dey find " + ", ".join(parts) + "."

    def _generate_response(self, plan: ResponsePlan, state: ConversationState) -> str:
        if self._policy is not None:
            try:
                dialogue_plan = self._policy.build_dialogue_plan(
                    state=state,
                    response_plan=plan,
                    message=state.last_user_message,
                )
                return self._policy.internal_engine.generate(dialogue_plan)
            except Exception:
                pass

        if plan.response_template and not plan.updated_slots:
            return plan.response_template
        if plan.response_template and plan.updated_slots:
            ack = self._build_acknowledgement_text(plan.updated_slots, state.language)
            if ack:
                return f"{ack}\n\n{plan.response_template}"
            return plan.response_template
        if plan.next_question_text:
            ack = self._build_acknowledgement_text(plan.acknowledgement_facts, state.language)
            if ack:
                return f"{ack}\n\n{plan.next_question_text}"
            return plan.next_question_text
        if plan.acknowledgement_facts:
            ack = self._build_acknowledgement_text(plan.acknowledgement_facts, state.language)
            if ack:
                return ack
        messages: dict[str, str] = {
            "fr": "Merci. Continuez a nous fournir les informations necessaires.",
            "en": "Thank you. Please continue providing the required information.",
            "pcm": "Thank you. Abeg continue to give us di information wey we need.",
        }
        return messages.get(state.language, messages["fr"])
