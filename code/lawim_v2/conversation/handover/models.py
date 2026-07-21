from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class HandoverStatus(str, Enum):
    REQUESTED = "REQUESTED"
    QUEUED = "QUEUED"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    RETURNED_TO_LAWIM = "RETURNED_TO_LAWIM"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


_STATUS_FLOW = {
    HandoverStatus.REQUESTED,
    HandoverStatus.QUEUED,
    HandoverStatus.ACCEPTED,
    HandoverStatus.IN_PROGRESS,
    HandoverStatus.RESOLVED,
}


def _is_active(status: HandoverStatus) -> bool:
    return status in _STATUS_FLOW


@dataclass
class AgentHandover:
    handover_id: str = ""
    case_id: str = ""
    conversation_id: str = ""
    actor_id: str = ""
    source_agent_id: str = ""
    target_actor_or_team: str = ""
    reason: str = ""
    priority: str = "NORMAL"
    summary: str = ""
    context_snapshot: dict[str, Any] = field(default_factory=dict)
    open_questions: list[str] = field(default_factory=list)
    recommended_action: str = ""
    human_instructions: str = ""
    human_decision: str = ""
    human_decision_notes: str = ""
    next_action: str = ""
    status: HandoverStatus = HandoverStatus.REQUESTED
    created_at: str = ""
    accepted_at: str = ""
    resolved_at: str = ""
    returned_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "handover_id": self.handover_id,
            "case_id": self.case_id,
            "conversation_id": self.conversation_id,
            "actor_id": self.actor_id,
            "source_agent_id": self.source_agent_id,
            "target_actor_or_team": self.target_actor_or_team,
            "reason": self.reason,
            "priority": self.priority,
            "summary": self.summary,
            "context_snapshot": dict(self.context_snapshot),
            "open_questions": list(self.open_questions),
            "recommended_action": self.recommended_action,
            "human_instructions": self.human_instructions,
            "human_decision": self.human_decision,
            "human_decision_notes": self.human_decision_notes,
            "next_action": self.next_action,
            "status": self.status.value,
            "created_at": self.created_at,
            "accepted_at": self.accepted_at,
            "resolved_at": self.resolved_at,
            "returned_at": self.returned_at,
        }

    def is_active(self) -> bool:
        return _is_active(self.status)


@dataclass
class HandoverSnapshot:
    snapshot_id: str = ""
    handover_id: str = ""
    case_id: str = ""
    conversation_state: dict[str, Any] = field(default_factory=dict)
    known_slots: dict[str, Any] = field(default_factory=dict)
    missing_slots: list[str] = field(default_factory=list)
    active_intent: str = ""
    qualification_readiness: str = ""
    last_question: str = ""
    language: str = "fr"
    interaction_count: int = 0
    recent_messages: list[dict[str, str]] = field(default_factory=list)
    created_at: str = ""
