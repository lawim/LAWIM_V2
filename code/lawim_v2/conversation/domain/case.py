from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class CaseStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    WAITING_USER = "WAITING_USER"
    WAITING_LAWIM = "WAITING_LAWIM"
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    SUSPENDED = "SUSPENDED"
    HANDED_OVER = "HANDED_OVER"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"


_ACTIVE_STATUSES = {
    CaseStatus.ACTIVE,
    CaseStatus.WAITING_USER,
    CaseStatus.WAITING_LAWIM,
    CaseStatus.READY,
    CaseStatus.IN_PROGRESS,
}


class CaseType(str, Enum):
    BUY = "BUY"
    RENT = "RENT"
    SELL = "SELL"
    LIST = "LIST"
    PUBLISH = "PUBLISH"
    DOCUMENT_REQUEST = "DOCUMENT_REQUEST"
    COMPLAINT = "COMPLAINT"
    OTHER = "OTHER"


@dataclass
class LawimCase:
    case_id: str = ""
    case_code: str = ""
    case_type: str = ""
    primary_actor_id: str = ""
    title: str = ""
    active_intent: str = ""
    journey_code: str = ""
    status: CaseStatus = CaseStatus.DRAFT
    active_language: str = "fr"
    qualification_state: dict[str, Any] = field(default_factory=dict)
    readiness_status: str = "not_started"
    property_reference: str | None = None
    assigned_agent: str | None = None
    handover_status: str | None = None
    active_conversation_id: str | None = None
    known_slots: dict[str, Any] = field(default_factory=dict)
    last_question_key: str = ""
    last_question_slot: str = ""
    summary: str = ""
    created_at: str = ""
    updated_at: str = ""
    closed_at: str | None = None
    version: int = 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "case_code": self.case_code,
            "case_type": self.case_type,
            "primary_actor_id": self.primary_actor_id,
            "title": self.title,
            "active_intent": self.active_intent,
            "journey_code": self.journey_code,
            "status": self.status.value,
            "active_language": self.active_language,
            "qualification_state": dict(self.qualification_state),
            "readiness_status": self.readiness_status,
            "property_reference": self.property_reference,
            "assigned_agent": self.assigned_agent,
            "handover_status": self.handover_status,
            "active_conversation_id": self.active_conversation_id,
            "known_slots": dict(self.known_slots),
            "last_question_key": self.last_question_key,
            "last_question_slot": self.last_question_slot,
            "summary": self.summary,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "closed_at": self.closed_at,
            "version": self.version,
        }

    def is_active(self) -> bool:
        return self.status in _ACTIVE_STATUSES
