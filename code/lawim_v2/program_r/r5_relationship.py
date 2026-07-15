from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ConsentStatus(str, Enum):
    REQUESTED = "REQUESTED"
    GRANTED = "GRANTED"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


CONSENT_TRANSITIONS: dict[ConsentStatus, list[ConsentStatus]] = {
    ConsentStatus.REQUESTED: [ConsentStatus.GRANTED, ConsentStatus.REVOKED],
    ConsentStatus.GRANTED: [ConsentStatus.ACTIVE, ConsentStatus.REVOKED],
    ConsentStatus.ACTIVE: [ConsentStatus.EXPIRED, ConsentStatus.REVOKED],
    ConsentStatus.EXPIRED: [ConsentStatus.REQUESTED],
    ConsentStatus.REVOKED: [],
}


@dataclass
class Consent:
    consent_id: str = ""
    consent_type: str = ""
    grantor_id: int = 0
    grantee_id: int = 0
    status: ConsentStatus = ConsentStatus.REQUESTED
    granted_at: str = ""
    expires_at: str = ""
    revoked_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def can_transition(self, target: ConsentStatus) -> bool:
        return target in CONSENT_TRANSITIONS.get(self.status, [])

    def grant(self) -> bool:
        if self.can_transition(ConsentStatus.GRANTED):
            self.status = ConsentStatus.GRANTED
            self.granted_at = datetime.now(timezone.utc).isoformat()
            return True
        return False

    def revoke(self) -> bool:
        if self.can_transition(ConsentStatus.REVOKED):
            self.status = ConsentStatus.REVOKED
            self.revoked_at = datetime.now(timezone.utc).isoformat()
            return True
        return False

    def is_active(self) -> bool:
        return self.status in (ConsentStatus.GRANTED, ConsentStatus.ACTIVE)


@dataclass
class Relationship:
    relationship_id: str = ""
    demandeur_id: int = 0
    holder_id: int = 0
    property_id: int | None = None
    agent_id: int | None = None
    status: str = "PENDING"
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"relationship_id": self.relationship_id, "status": self.status}


class RelationshipRole(str, Enum):
    DEMANDEUR = "DEMANDEUR"
    HOLDER = "HOLDER"
    AGENT_DEMANDEUR = "AGENT_DEMANDEUR"
    AGENT_HOLDER = "AGENT_HOLDER"
    MEDIATOR = "MEDIATOR"


@dataclass
class RelationshipParticipant:
    relationship_id: str = ""
    actor_id: int = 0
    role: RelationshipRole = RelationshipRole.DEMANDEUR
    joined_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"actor_id": self.actor_id, "role": self.role.value}


@dataclass
class Introduction:
    introduction_id: str = ""
    relationship_id: str = ""
    method: str = ""
    outcome: str = ""
    assigned_agent_id: int | None = None
    introduced_at: str = ""


@dataclass
class DataScope:
    scope_id: str = ""
    relationship_id: str = ""
    field_visibility: dict[str, bool] = field(default_factory=dict)

    def can_see(self, field: str) -> bool:
        return self.field_visibility.get(field, False)


@dataclass
class ConsentAuditRecord:
    audit_id: str = ""
    consent_id: str = ""
    actor_id: int = 0
    action: str = ""
    previous_state: str = ""
    new_state: str = ""
    timestamp: str = ""


@dataclass
class HumanHandover:
    handover_id: str = ""
    source_agent_id: str = ""
    target_actor_id: int = 0
    summary: str = ""
    status: str = "REQUESTED"
    created_at: str = ""
    resolved_at: str = ""
