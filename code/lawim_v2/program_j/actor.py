from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ActorType(str, Enum):
    AI_ASSISTANT = "AI_ASSISTANT"
    LAWIM_STAFF = "LAWIM_STAFF"
    USER = "USER"
    OWNER = "OWNER"
    BUYER = "BUYER"
    TENANT = "TENANT"
    REAL_ESTATE_AGENT = "REAL_ESTATE_AGENT"
    AGENCY = "AGENCY"
    ARCHITECT = "ARCHITECT"
    ENGINEER = "ENGINEER"
    TECHNICIAN = "TECHNICIAN"
    NOTARY = "NOTARY"
    INVESTOR = "INVESTOR"
    PARTNER = "PARTNER"
    SYSTEM = "SYSTEM"

    @classmethod
    def from_role_label(cls, label: str) -> ActorType:
        mapping = {
            "agent immobilier": ActorType.REAL_ESTATE_AGENT,
            "notaire": ActorType.NOTARY,
            "architecte": ActorType.ARCHITECT,
            "ingenieur": ActorType.ENGINEER,
            "electricien": ActorType.TECHNICIAN,
            "plombier": ActorType.TECHNICIAN,
            "investisseur": ActorType.INVESTOR,
            "acheteur": ActorType.BUYER,
            "locataire": ActorType.TENANT,
            "proprietaire": ActorType.OWNER,
            "agence": ActorType.AGENCY,
            "partenaire": ActorType.PARTNER,
            "admin": ActorType.LAWIM_STAFF,
            "staff": ActorType.LAWIM_STAFF,
            "user": ActorType.USER,
        }
        return mapping.get(label.strip().lower(), ActorType.USER)


class ActorStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    SUSPENDED = "SUSPENDED"


@dataclass
class Actor:
    actor_id: str
    actor_type: ActorType
    display_name: str
    user_id: int | None = None
    organization_id: int | None = None
    agency_id: int | None = None
    team_id: int | None = None
    current_role: str = ""
    historical_role: str = ""
    trust_level: int = 0
    privacy_level: int = 0
    status: ActorStatus = ActorStatus.ACTIVE
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "actor_id": self.actor_id,
            "actor_type": self.actor_type.value,
            "display_name": self.display_name,
            "user_id": self.user_id,
            "organization_id": self.organization_id,
            "current_role": self.current_role,
            "historical_role": self.historical_role,
            "trust_level": self.trust_level,
            "privacy_level": self.privacy_level,
            "status": self.status.value,
        }
