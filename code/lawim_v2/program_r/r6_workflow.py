from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class WorkflowType(str, Enum):
    MATCHING = "MATCHING"
    CONTACT = "CONTACT"
    VISIT = "VISIT"
    TRANSACTION = "TRANSACTION"
    SERVICE_PAYMENT = "SERVICE_PAYMENT"
    INCIDENT = "INCIDENT"
    MEDIATION = "MEDIATION"
    PIPELINE = "PIPELINE"
    PUBLICATION = "PUBLICATION"
    REDIRECTION = "REDIRECTION"
    CONVERSION = "CONVERSION"
    AGENT_INVITATION = "AGENT_INVITATION"
    IDENTITY_RESOLUTION = "IDENTITY_RESOLUTION"
    ORCHESTRATOR = "ORCHESTRATOR"


WORKFLOW_STATE_MACHINES: dict[WorkflowType, list[str]] = {
    WorkflowType.MATCHING: ["created", "scored", "proposed", "demandeur_consented",
                            "holder_consented", "relationship", "active", "expired",
                            "closed", "archived"],
    WorkflowType.CONTACT: ["initiated", "demandeur_consented", "holder_consented",
                           "active", "closed", "archived"],
    WorkflowType.VISIT: ["requested", "scheduled", "confirmed", "reminder",
                         "in_progress", "completed", "cancelled", "no_show", "rescheduled"],
    WorkflowType.TRANSACTION: ["initiated", "offer", "negotiation", "accepted",
                                "docs", "signed", "payment", "completed", "cancelled", "disputed"],
    WorkflowType.SERVICE_PAYMENT: 18,
    WorkflowType.INCIDENT: 8,
    WorkflowType.MEDIATION: 8,
    WorkflowType.PIPELINE: ["lead_in", "qualification", "proposition", "negotiation",
                            "closing", "won", "lost", "recycled"],
    WorkflowType.PUBLICATION: 11,
    WorkflowType.REDIRECTION: 12,
    WorkflowType.CONVERSION: 12,
    WorkflowType.AGENT_INVITATION: 7,
    WorkflowType.IDENTITY_RESOLUTION: 5,
    WorkflowType.ORCHESTRATOR: 9,
}


@dataclass
class WorkflowInstance:
    workflow_id: str = ""
    workflow_type: WorkflowType = WorkflowType.MATCHING
    current_state: str = "created"
    states: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    completed_at: str = ""

    def __post_init__(self) -> None:
        if not self.states:
            sm = WORKFLOW_STATE_MACHINES.get(self.workflow_type, [])
            self.states = sm if isinstance(sm, list) else []

    def advance(self) -> str | None:
        if self.current_state in self.states:
            idx = self.states.index(self.current_state)
            if idx < len(self.states) - 1:
                self.current_state = self.states[idx + 1]
                if idx + 1 == len(self.states) - 1:
                    self.completed_at = datetime.now(timezone.utc).isoformat()
                return self.current_state
        return None

    def can_advance(self) -> bool:
        return self.current_state in self.states and \
               self.states.index(self.current_state) < len(self.states) - 1


@dataclass
class NBAEngine:
    def next_best_action(self, state: str, domain: str,
                          readiness: float = 0.0) -> dict[str, Any]:
        matrix = {
            ("qualifying", "response"): {"action": "ask_next_question", "priority": "P1"},
            ("matching", "results"): {"action": "present_matches", "priority": "P1"},
            ("visit", "scheduling"): {"action": "schedule_visit", "priority": "P2"},
            ("negotiation", "commercial"): {"action": "prepare_offer", "priority": "P2"},
            ("transaction", "payment"): {"action": "initiate_payment", "priority": "P1"},
            ("closed", "followup"): {"action": "request_feedback", "priority": "P3"},
            ("abandoned", "recovery"): {"action": "send_recovery_message", "priority": "P2"},
            ("default", "default"): {"action": "monitor", "priority": "P3"},
        }
        return matrix.get((state, domain), matrix[("default", "default")])


NBA_PRIORITY_LEVELS: list[str] = ["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]


@dataclass
class FollowUpCalendar:
    intervals_days: list[int] = field(default_factory=lambda: [1, 7, 30, 90])

    def next_followup(self, last_contact_days: int) -> int | None:
        for interval in self.intervals_days:
            if last_contact_days < interval:
                return interval - last_contact_days
        return None


@dataclass
class OrchestratorEngine:
    def delegate(self, workflow_type: WorkflowType, context: dict[str, Any]) -> WorkflowInstance:
        wf = WorkflowInstance(
            workflow_id=f"wf_{datetime.now(timezone.utc).timestamp()}",
            workflow_type=workflow_type,
            context=context,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        return wf
