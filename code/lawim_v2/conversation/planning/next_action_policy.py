from __future__ import annotations

from typing import Any

from ..domain.actions import Action, ActionType
from ..domain.conversation import Conversation
from ..domain.states import ConversationState

REQUIRED_FIELDS_BY_INTENT: dict[str, list[str]] = {
    "rent_apartment": ["property_type", "city", "neighborhood", "budget_max", "bedrooms"],
    "rent_studio": ["property_type", "city", "neighborhood", "budget_max", "bedrooms"],
    "rent_room": ["property_type", "city", "neighborhood", "budget_max", "bedrooms"],
    "rent_house": ["property_type", "city", "neighborhood", "budget_max", "bedrooms"],
    "rent_villa": ["property_type", "city", "neighborhood", "budget_max", "bedrooms"],
    "rent_commercial": ["property_type", "city", "neighborhood", "budget_max", "bedrooms"],
    "buy_land": ["property_type", "city", "neighborhood", "budget_max", "surface_min"],
    "buy_house": ["property_type", "city", "neighborhood", "budget_max", "bedrooms"],
    "buy_apartment": ["property_type", "city", "neighborhood", "budget_max", "bedrooms"],
    "buy_villa": ["property_type", "city", "neighborhood", "budget_max", "bedrooms"],
    "buy_commercial": ["property_type", "city", "neighborhood", "budget_max", "bedrooms"],
    "buy_building": ["property_type", "city", "neighborhood", "budget_max", "bedrooms"],
    "sell_land": ["property_type", "location", "surface"],
    "sell_house": ["property_type", "location", "surface"],
    "sell_apartment": ["property_type", "location", "surface"],
    "sell_property": ["property_type", "location", "surface"],
    "rent_out": ["property_type", "location"],
    "construct": ["property_type", "budget_max", "city", "surface"],
    "renovate": ["property_type", "budget_max", "location"],
    "invest": ["budget_max", "city"],
    "find_architect": ["city"],
    "find_engineer": ["city"],
    "find_technician": ["city"],
    "find_notary": ["city"],
    "find_agent": ["city"],
    "find_contractor": ["city"],
    "find_lawyer": ["city"],
    "documentation": [],
    "information": [],
    "complaint": [],
    "greeting": [],
    "handover": [],
    "other": [],
}

FIELD_LABELS: dict[str, str] = {
    "property_type": "type de bien",
    "budget_max": "budget maximum",
    "budget_min": "budget minimum",
    "city": "ville",
    "neighborhood": "quartier",
    "location": "localisation",
    "surface_min": "surface minimale",
    "surface_max": "surface maximale",
    "surface": "surface",
    "rooms_min": "nombre de pièces minimum",
    "bedrooms": "nombre de chambres",
    "furnished": "meublé ou non",
    "urgency": "urgence",
    "timeline": "calendrier souhaité",
    "description": "description",
}

FIELD_QUESTIONS_FR: dict[str, str] = {
    "neighborhood": "Dans quel quartier souhaitez-vous orienter votre recherche ?",
    "budget_max": "Quel est votre budget mensuel maximal ?",
    "bedrooms": "Combien de chambres souhaitez-vous ?",
}

PROPERTY_TYPE_QUESTIONS_FR: dict[str, str] = {
    "APARTMENT": "appartement",
    "STUDIO": "studio",
    "HOUSE": "maison",
    "VILLA": "villa",
    "LAND": "terrain",
    "COMMERCIAL": "local commercial",
}


def determine_next_action(conversation: Conversation) -> dict[str, Any]:
    state = conversation.state
    known_fields = conversation.known_fields
    available_facts = conversation.facts

    if state == ConversationState.NEW:
        return {
            "action": ActionType.GREETING,
            "field": None,
            "reason": "new_conversation",
        }

    if state == ConversationState.AWAITING_PROJECT_SELECTION:
        return {
            "action": ActionType.SELECT_PROJECT,
            "field": None,
            "reason": "project_selection_required",
        }

    if state == ConversationState.AWAITING_INTENT:
        return {
            "action": ActionType.NOTHING,
            "field": None,
            "reason": "awaiting_intent_classification",
        }

    if state == ConversationState.QUALIFYING:
        return _qualification_action(conversation)

    if state == ConversationState.AWAITING_CLARIFICATION:
        return {
            "action": ActionType.REQUEST_CLARIFICATION,
            "field": conversation.last_question_field,
            "reason": "clarification_required",
        }

    if state == ConversationState.READY_FOR_SEARCH:
        return {
            "action": ActionType.START_SEARCH,
            "field": None,
            "reason": "minimum_readiness_reached",
        }

    if state == ConversationState.SEARCHING:
        return {
            "action": ActionType.RUN_MATCHING,
            "field": None,
            "reason": "search_in_progress",
        }

    if state == ConversationState.RESULTS_AVAILABLE:
        return {
            "action": ActionType.PRESENT_RESULTS,
            "field": None,
            "reason": "results_ready",
        }

    if state == ConversationState.AWAITING_RESULT_SELECTION:
        return {
            "action": ActionType.NOTHING,
            "field": None,
            "reason": "awaiting_result_selection",
        }

    if state == ConversationState.AWAITING_RELATIONSHIP_CONSENT:
        return {
            "action": ActionType.REQUEST_CONSENT,
            "field": None,
            "reason": "consent_required_before_proposal",
        }

    if state == ConversationState.RELATIONSHIP_PROPOSED:
        return {
            "action": ActionType.CREATE_RELATIONSHIP,
            "field": None,
            "reason": "proposal_awaiting_acceptance",
        }

    if state == ConversationState.RELATIONSHIP_PENDING:
        return {
            "action": ActionType.NOTHING,
            "field": None,
            "reason": "relationship_pending_confirmation",
        }

    if state == ConversationState.RELATIONSHIP_ACTIVE:
        return {
            "action": ActionType.PRESENT_PARTICIPANTS,
            "field": None,
            "reason": "relationship_active",
        }

    if state == ConversationState.VISIT_PENDING:
        return {
            "action": ActionType.REQUEST_VISIT,
            "field": None,
            "reason": "visit_pending",
        }

    if state == ConversationState.VISIT_CONFIRMED:
        return {
            "action": ActionType.PROVIDE_INFORMATION,
            "field": None,
            "reason": "visit_confirmed",
        }

    if state == ConversationState.VISIT_COMPLETED:
        return {
            "action": ActionType.NOTHING,
            "field": None,
            "reason": "visit_completed_awaiting_feedback",
        }

    if state == ConversationState.FOLLOW_UP:
        return {
            "action": ActionType.PROVIDE_INFORMATION,
            "field": None,
            "reason": "follow_up_phase",
        }

    if state == ConversationState.HUMAN_HANDOVER:
        return {
            "action": ActionType.HANDOVER_TO_HUMAN,
            "field": None,
            "reason": "handover_required",
        }

    if state == ConversationState.CLOSED:
        return {
            "action": ActionType.CLOSE_PROJECT,
            "field": None,
            "reason": "conversation_closed",
        }

    return {
        "action": ActionType.NOTHING,
        "field": None,
        "reason": "unknown_state",
    }


def _qualification_action(conversation: Conversation) -> dict[str, Any]:
    intent = conversation.facts.get_latest_confirmed("intent")
    intent_value = intent.normalized_value if intent else None

    if not intent_value or intent_value not in REQUIRED_FIELDS_BY_INTENT:
        return {
            "action": ActionType.NOTHING,
            "field": None,
            "reason": "awaiting_intent_for_qualification",
        }

    required_fields = REQUIRED_FIELDS_BY_INTENT.get(intent_value, [])
    for field in required_fields:
        if field not in conversation.known_fields:
            label = FIELD_LABELS.get(field, field)
            return {
                "action": ActionType.UPDATE_FACT,
                "field": field,
                "reason": f"missing_required_field:{field}",
                "label": label,
            }

    ambiguous = conversation.facts.get_ambiguous()
    if ambiguous:
        return {
            "action": ActionType.REQUEST_CLARIFICATION,
            "field": ambiguous[0].field,
            "reason": f"ambiguous_fact:{ambiguous[0].field}",
        }

    return {
        "action": ActionType.CREATE_DOSSIER,
        "field": None,
        "reason": "all_required_fields_collected",
    }


def list_missing_fields(conversation: Conversation) -> list[str]:
    intent = conversation.facts.get_latest_confirmed("intent")
    intent_value = intent.normalized_value if intent else None
    if not intent_value or intent_value not in REQUIRED_FIELDS_BY_INTENT:
        return []
    return [f for f in REQUIRED_FIELDS_BY_INTENT[intent_value] if f not in conversation.known_fields]
