from __future__ import annotations

from ..domain.states import ConversationState, STATE_TRANSITIONS


def allowed_events(state: ConversationState) -> list[str]:
    return [t.event for t in STATE_TRANSITIONS if t.source == state]


def allowed_destinations(state: ConversationState) -> list[ConversationState]:
    return list({t.destination for t in STATE_TRANSITIONS if t.source == state})


def can_transition(state: ConversationState, event: str) -> bool:
    return any(t.source == state and t.event == event for t in STATE_TRANSITIONS)


def find_transition(state: ConversationState, event: str) -> dict | None:
    for t in STATE_TRANSITIONS:
        if t.source == state and t.event == event:
            return {
                "source": t.source,
                "event": t.event,
                "destination": t.destination,
                "guard": t.guard,
                "failure_state": t.failure_state,
                "audit_event": t.audit_event,
            }
    return None


def resolve_transition(
    state: ConversationState,
    event: str,
    *,
    guard_conditions: dict | None = None,
) -> dict:
    guard_conditions = guard_conditions or {}
    for t in STATE_TRANSITIONS:
        if t.source == state and t.event == event:
            if t.guard:
                guard_value = guard_conditions.get(t.guard)
                if not guard_value:
                    return {
                        "allowed": False,
                        "reason": f"guard '{t.guard}' not satisfied",
                        "destination": t.failure_state,
                        "audit_event": t.audit_event,
                    }
            return {
                "allowed": True,
                "destination": t.destination,
                "audit_event": t.audit_event,
            }
    return {
        "allowed": False,
        "reason": f"no transition from {state.value} with event '{event}'",
        "destination": ConversationState.ERROR,
        "audit_event": "state.error",
    }


def is_terminal(state: ConversationState) -> bool:
    return state in {ConversationState.CLOSED}


def is_error_state(state: ConversationState) -> bool:
    return state in {ConversationState.ERROR, ConversationState.HUMAN_HANDOVER}


def can_receive_messages(state: ConversationState) -> bool:
    non_receiving = {
        ConversationState.CLOSED,
        ConversationState.ERROR,
    }
    return state not in non_receiving


def requires_immediate_action(state: ConversationState) -> bool:
    return state in {
        ConversationState.HUMAN_HANDOVER,
        ConversationState.ERROR,
    }


def get_state_category(state: ConversationState) -> str:
    if state in {
        ConversationState.NEW,
        ConversationState.AWAITING_PROJECT_SELECTION,
        ConversationState.AWAITING_INTENT,
    }:
        return "onboarding"
    if state in {
        ConversationState.QUALIFYING,
        ConversationState.AWAITING_CLARIFICATION,
    }:
        return "qualification"
    if state in {
        ConversationState.READY_FOR_SEARCH,
        ConversationState.SEARCHING,
        ConversationState.RESULTS_AVAILABLE,
        ConversationState.AWAITING_RESULT_SELECTION,
    }:
        return "search"
    if state in {
        ConversationState.AWAITING_RELATIONSHIP_CONSENT,
        ConversationState.RELATIONSHIP_PROPOSED,
        ConversationState.RELATIONSHIP_PENDING,
        ConversationState.RELATIONSHIP_ACTIVE,
    }:
        return "relationship"
    if state in {
        ConversationState.VISIT_PENDING,
        ConversationState.VISIT_CONFIRMED,
        ConversationState.VISIT_COMPLETED,
    }:
        return "visit"
    if state == ConversationState.FOLLOW_UP:
        return "follow_up"
    if state == ConversationState.HUMAN_HANDOVER:
        return "handover"
    if state == ConversationState.ERROR:
        return "error"
    if state == ConversationState.CLOSED:
        return "closed"
    return "unknown"
