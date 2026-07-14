from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class RelationshipStatus(str, Enum):
    PROPOSED = "PROPOSED"
    PENDING_CONSENT = "PENDING_CONSENT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


VALID_TRANSITIONS: dict[RelationshipStatus, set[RelationshipStatus]] = {
    RelationshipStatus.PROPOSED: {
        RelationshipStatus.PENDING_CONSENT,
        RelationshipStatus.CANCELLED,
    },
    RelationshipStatus.PENDING_CONSENT: {
        RelationshipStatus.ACTIVE,
        RelationshipStatus.CANCELLED,
        RelationshipStatus.EXPIRED,
    },
    RelationshipStatus.ACTIVE: {
        RelationshipStatus.PAUSED,
        RelationshipStatus.COMPLETED,
        RelationshipStatus.CANCELLED,
    },
    RelationshipStatus.PAUSED: {
        RelationshipStatus.ACTIVE,
        RelationshipStatus.CANCELLED,
        RelationshipStatus.COMPLETED,
    },
    RelationshipStatus.COMPLETED: set(),
    RelationshipStatus.CANCELLED: set(),
    RelationshipStatus.EXPIRED: set(),
}


@dataclass
class Relationship:
    relationship_id: str = ""
    proposal_id: str = ""
    project_id: int | None = None
    dossier_id: int | None = None
    status: RelationshipStatus = RelationshipStatus.PROPOSED
    relationship_type: str = "buyer_seller"
    created_at: str | None = None
    updated_at: str | None = None
    activated_at: str | None = None
    completed_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def can_transition_to(self, new_status: RelationshipStatus) -> bool:
        return new_status in VALID_TRANSITIONS.get(self.status, set())

    def transition_to(self, new_status: RelationshipStatus) -> bool:
        if not self.can_transition_to(new_status):
            return False
        self.status = new_status
        self.updated_at = datetime.utcnow().isoformat()

        if new_status == RelationshipStatus.ACTIVE:
            self.activated_at = self.activated_at or self.updated_at
        elif new_status == RelationshipStatus.COMPLETED:
            self.completed_at = self.updated_at

        return True

    def is_active(self) -> bool:
        return self.status == RelationshipStatus.ACTIVE

    def is_terminal(self) -> bool:
        return self.status in {
            RelationshipStatus.COMPLETED,
            RelationshipStatus.CANCELLED,
            RelationshipStatus.EXPIRED,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "relationship_id": self.relationship_id,
            "proposal_id": self.proposal_id,
            "project_id": self.project_id,
            "dossier_id": self.dossier_id,
            "status": self.status.value,
            "relationship_type": self.relationship_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "activated_at": self.activated_at,
            "completed_at": self.completed_at,
            "is_active": self.is_active(),
            "is_terminal": self.is_terminal(),
        }


class RelationshipLifecycle:
    def __init__(self) -> None:
        self._relationships: dict[str, Relationship] = {}

    def create(self, relationship: Relationship) -> None:
        self._relationships[relationship.relationship_id] = relationship

    def get(self, relationship_id: str) -> Relationship | None:
        return self._relationships.get(relationship_id)

    def activate(self, relationship_id: str) -> bool:
        relationship = self.get(relationship_id)
        if relationship is None:
            return False
        return relationship.transition_to(RelationshipStatus.ACTIVE)

    def pause(self, relationship_id: str) -> bool:
        relationship = self.get(relationship_id)
        if relationship is None:
            return False
        return relationship.transition_to(RelationshipStatus.PAUSED)

    def resume(self, relationship_id: str) -> bool:
        relationship = self.get(relationship_id)
        if relationship is None:
            return False
        return relationship.transition_to(RelationshipStatus.ACTIVE)

    def complete(self, relationship_id: str) -> bool:
        relationship = self.get(relationship_id)
        if relationship is None:
            return False
        return relationship.transition_to(RelationshipStatus.COMPLETED)

    def cancel(self, relationship_id: str) -> bool:
        relationship = self.get(relationship_id)
        if relationship is None:
            return False
        return relationship.transition_to(RelationshipStatus.CANCELLED)

    def list_by_project(self, project_id: int) -> list[Relationship]:
        return [
            r for r in self._relationships.values()
            if r.project_id == project_id
        ]

    def list_active(self) -> list[Relationship]:
        return [
            r for r in self._relationships.values()
            if r.is_active()
        ]

    def list_by_status(self, status: RelationshipStatus) -> list[Relationship]:
        return [
            r for r in self._relationships.values()
            if r.status == status
        ]
