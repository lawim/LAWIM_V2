from __future__ import annotations

from enum import Enum


class ConversationState(str, Enum):
    NEW = "NEW"
    AWAITING_PROJECT_SELECTION = "AWAITING_PROJECT_SELECTION"
    AWAITING_INTENT = "AWAITING_INTENT"
    QUALIFYING = "QUALIFYING"
    AWAITING_CLARIFICATION = "AWAITING_CLARIFICATION"
    READY_FOR_SEARCH = "READY_FOR_SEARCH"
    SEARCHING = "SEARCHING"
    RESULTS_AVAILABLE = "RESULTS_AVAILABLE"
    AWAITING_RESULT_SELECTION = "AWAITING_RESULT_SELECTION"
    AWAITING_RELATIONSHIP_CONSENT = "AWAITING_RELATIONSHIP_CONSENT"
    RELATIONSHIP_PROPOSED = "RELATIONSHIP_PROPOSED"
    RELATIONSHIP_PENDING = "RELATIONSHIP_PENDING"
    RELATIONSHIP_ACTIVE = "RELATIONSHIP_ACTIVE"
    VISIT_PENDING = "VISIT_PENDING"
    VISIT_CONFIRMED = "VISIT_CONFIRMED"
    VISIT_COMPLETED = "VISIT_COMPLETED"
    FOLLOW_UP = "FOLLOW_UP"
    CLOSED = "CLOSED"
    HUMAN_HANDOVER = "HUMAN_HANDOVER"
    ERROR = "ERROR"


class StateTransition:
    def __init__(
        self,
        source: ConversationState,
        event: str,
        destination: ConversationState,
        guard: str | None = None,
        failure_state: ConversationState | None = None,
        audit_event: str | None = None,
    ):
        self.source = source
        self.event = event
        self.destination = destination
        self.guard = guard
        self.failure_state = failure_state or ConversationState.ERROR
        self.audit_event = audit_event or f"state.{source.value.lower()}_to_{destination.value.lower()}"


STATE_TRANSITIONS: list[StateTransition] = [
    StateTransition(
        ConversationState.NEW,
        "message_received",
        ConversationState.AWAITING_INTENT,
        audit_event="conversation.started",
    ),
    StateTransition(
        ConversationState.NEW,
        "user_identified",
        ConversationState.AWAITING_PROJECT_SELECTION,
        guard="has_active_projects",
        audit_event="user.identified",
    ),
    StateTransition(
        ConversationState.AWAITING_PROJECT_SELECTION,
        "project_selected",
        ConversationState.AWAITING_INTENT,
        audit_event="project.selected",
    ),
    StateTransition(
        ConversationState.AWAITING_PROJECT_SELECTION,
        "new_project_requested",
        ConversationState.AWAITING_INTENT,
        audit_event="project.created",
    ),
    StateTransition(
        ConversationState.AWAITING_PROJECT_SELECTION,
        "ambiguity_detected",
        ConversationState.AWAITING_PROJECT_SELECTION,
        audit_event="project.selection.ambiguous",
    ),
    StateTransition(
        ConversationState.AWAITING_INTENT,
        "intent_identified",
        ConversationState.QUALIFYING,
        audit_event="intent.identified",
    ),
    StateTransition(
        ConversationState.AWAITING_INTENT,
        "ambiguity_detected",
        ConversationState.AWAITING_INTENT,
        audit_event="intent.ambiguous",
    ),
    StateTransition(
        ConversationState.QUALIFYING,
        "fact_confirmed",
        ConversationState.QUALIFYING,
        guard="more_fields_required",
        audit_event="fact.confirmed",
    ),
    StateTransition(
        ConversationState.QUALIFYING,
        "fact_ambiguous",
        ConversationState.AWAITING_CLARIFICATION,
        audit_event="fact.ambiguous",
    ),
    StateTransition(
        ConversationState.QUALIFYING,
        "clarification_provided",
        ConversationState.QUALIFYING,
        audit_event="clarification.provided",
    ),
    StateTransition(
        ConversationState.QUALIFYING,
        "minimum_readiness",
        ConversationState.READY_FOR_SEARCH,
        audit_event="qualification.minimum_ready",
    ),
    StateTransition(
        ConversationState.AWAITING_CLARIFICATION,
        "clarification_provided",
        ConversationState.QUALIFYING,
        audit_event="clarification.resolved",
    ),
    StateTransition(
        ConversationState.AWAITING_CLARIFICATION,
        "loop_detected",
        ConversationState.AWAITING_CLARIFICATION,
        guard="repeat_under_threshold",
        audit_event="clarification.repeated",
    ),
    StateTransition(
        ConversationState.AWAITING_CLARIFICATION,
        "loop_exceeded",
        ConversationState.HUMAN_HANDOVER,
        audit_event="clarification.loop_exceeded",
    ),
    StateTransition(
        ConversationState.READY_FOR_SEARCH,
        "search_requested",
        ConversationState.SEARCHING,
        audit_event="search.requested",
    ),
    StateTransition(
        ConversationState.SEARCHING,
        "results_available",
        ConversationState.RESULTS_AVAILABLE,
        audit_event="search.results_available",
    ),
    StateTransition(
        ConversationState.SEARCHING,
        "zero_results",
        ConversationState.QUALIFYING,
        guard="can_widen_criteria",
        audit_event="search.zero_results",
    ),
    StateTransition(
        ConversationState.RESULTS_AVAILABLE,
        "result_selected",
        ConversationState.AWAITING_RELATIONSHIP_CONSENT,
        audit_event="match.selected",
    ),
    StateTransition(
        ConversationState.RESULTS_AVAILABLE,
        "result_dismissed",
        ConversationState.QUALIFYING,
        audit_event="match.dismissed",
    ),
    StateTransition(
        ConversationState.AWAITING_RELATIONSHIP_CONSENT,
        "consent_granted",
        ConversationState.RELATIONSHIP_PROPOSED,
        audit_event="consent.granted",
    ),
    StateTransition(
        ConversationState.AWAITING_RELATIONSHIP_CONSENT,
        "consent_denied",
        ConversationState.QUALIFYING,
        audit_event="consent.denied",
    ),
    StateTransition(
        ConversationState.RELATIONSHIP_PROPOSED,
        "proposal_accepted",
        ConversationState.RELATIONSHIP_ACTIVE,
        audit_event="relationship.created",
    ),
    StateTransition(
        ConversationState.RELATIONSHIP_PROPOSED,
        "proposal_rejected",
        ConversationState.QUALIFYING,
        audit_event="relationship.rejected",
    ),
    StateTransition(
        ConversationState.RELATIONSHIP_ACTIVE,
        "visit_requested",
        ConversationState.VISIT_PENDING,
        audit_event="visit.requested",
    ),
    StateTransition(
        ConversationState.VISIT_PENDING,
        "visit_confirmed",
        ConversationState.VISIT_CONFIRMED,
        audit_event="visit.confirmed",
    ),
    StateTransition(
        ConversationState.VISIT_CONFIRMED,
        "visit_completed",
        ConversationState.VISIT_COMPLETED,
        audit_event="visit.completed",
    ),
    StateTransition(
        ConversationState.VISIT_COMPLETED,
        "follow_up_needed",
        ConversationState.FOLLOW_UP,
        audit_event="follow_up.started",
    ),
    StateTransition(
        ConversationState.FOLLOW_UP,
        "all_complete",
        ConversationState.CLOSED,
        audit_event="project.closed",
    ),
    StateTransition(
        ConversationState.HUMAN_HANDOVER,
        "resolved",
        ConversationState.QUALIFYING,
        audit_event="handover.resolved",
    ),
    StateTransition(
        ConversationState.ERROR,
        "recover",
        ConversationState.QUALIFYING,
        audit_event="state.recovered",
    ),
    StateTransition(
        ConversationState.CLOSED,
        "reopened",
        ConversationState.AWAITING_INTENT,
        audit_event="project.reopened",
    ),
]

# Direct handover transitions from any non-terminal state
_HANDOVER_STATES = [
    ConversationState.NEW,
    ConversationState.AWAITING_PROJECT_SELECTION,
    ConversationState.AWAITING_INTENT,
    ConversationState.QUALIFYING,
    ConversationState.AWAITING_CLARIFICATION,
    ConversationState.READY_FOR_SEARCH,
    ConversationState.SEARCHING,
    ConversationState.RESULTS_AVAILABLE,
    ConversationState.AWAITING_RESULT_SELECTION,
    ConversationState.AWAITING_RELATIONSHIP_CONSENT,
    ConversationState.RELATIONSHIP_PROPOSED,
    ConversationState.RELATIONSHIP_PENDING,
    ConversationState.VISIT_PENDING,
    ConversationState.VISIT_CONFIRMED,
    ConversationState.VISIT_COMPLETED,
    ConversationState.FOLLOW_UP,
]
for _hs in _HANDOVER_STATES:
    STATE_TRANSITIONS.append(
        StateTransition(
            _hs,
            "handover_requested",
            ConversationState.HUMAN_HANDOVER,
            audit_event="handover.requested",
        )
    )
