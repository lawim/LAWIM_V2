from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ParticipantRole(str, Enum):
    REQUESTER = "requester"
    TARGET = "target"
    AGENT = "agent"
    OBSERVER = "observer"


class ParticipantStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    DECLINED = "DECLINED"
    REMOVED = "REMOVED"
    LEFT = "LEFT"


@dataclass
class Participant:
    participant_id: str = ""
    relationship_id: str = ""
    user_id: int | None = None
    role: ParticipantRole = ParticipantRole.REQUESTER
    status: ParticipantStatus = ParticipantStatus.PENDING
    joined_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_active(self) -> bool:
        return self.status == ParticipantStatus.ACTIVE

    def to_dict(self) -> dict[str, Any]:
        return {
            "participant_id": self.participant_id,
            "relationship_id": self.relationship_id,
            "user_id": self.user_id,
            "role": self.role.value,
            "status": self.status.value,
            "joined_at": self.joined_at,
        }


class ParticipantManager:
    def __init__(self) -> None:
        self._participants: dict[str, Participant] = {}

    def add(self, participant: Participant) -> None:
        self._participants[participant.participant_id] = participant

    def get(self, participant_id: str) -> Participant | None:
        return self._participants.get(participant_id)

    def get_by_user(self, user_id: int) -> list[Participant]:
        return [
            p for p in self._participants.values()
            if p.user_id == user_id
        ]

    def get_by_relationship(self, relationship_id: str) -> list[Participant]:
        return [
            p for p in self._participants.values()
            if p.relationship_id == relationship_id
        ]

    def get_active_by_relationship(self, relationship_id: str) -> list[Participant]:
        return [
            p for p in self._participants.values()
            if p.relationship_id == relationship_id and p.is_active
        ]

    def activate(self, participant_id: str) -> bool:
        participant = self.get(participant_id)
        if participant is None:
            return False
        participant.status = ParticipantStatus.ACTIVE
        return True

    def deactivate(self, participant_id: str, status: ParticipantStatus) -> bool:
        participant = self.get(participant_id)
        if participant is None:
            return False
        if status not in (ParticipantStatus.LEFT, ParticipantStatus.REMOVED, ParticipantStatus.DECLINED):
            return False
        participant.status = status
        return True

    def count_by_relationship(self, relationship_id: str) -> int:
        return len(self.get_by_relationship(relationship_id))

    def has_role(self, relationship_id: str, role: ParticipantRole) -> bool:
        return any(
            p.role == role
            for p in self.get_active_by_relationship(relationship_id)
        )
