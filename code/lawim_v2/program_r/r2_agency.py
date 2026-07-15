from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class TrustLevel(str, Enum):
    LEVEL_1 = "LEVEL_1"
    LEVEL_2 = "LEVEL_2"
    LEVEL_3 = "LEVEL_3"
    LEVEL_4 = "LEVEL_4"
    LEVEL_5 = "LEVEL_5"
    LEVEL_6 = "LEVEL_6"


TRUST_LEVEL_REQUIREMENTS: dict[TrustLevel, dict[str, Any]] = {
    TrustLevel.LEVEL_1: {"otp_phone": True},
    TrustLevel.LEVEL_2: {"identity_docs": True},
    TrustLevel.LEVEL_3: {"professional_docs": True},
    TrustLevel.LEVEL_4: {"professional_verification": True},
    TrustLevel.LEVEL_5: {"reference_account": True},
    TrustLevel.LEVEL_6: {"full_kyc": True},
}


class BadgeType(str, Enum):
    PHONE_VERIFIED = "PHONE_VERIFIED"
    IDENTITY_VERIFIED = "IDENTITY_VERIFIED"
    PROFESSIONAL_VERIFIED = "PROFESSIONAL_VERIFIED"
    AGENT_ACTIVE = "AGENT_ACTIVE"
    TOP_AGENT = "TOP_AGENT"
    TRUSTED_PARTNER = "TRUSTED_PARTNER"
    PREMIUM_AGENCY = "PREMIUM_AGENCY"
    DIASPORA_SPECIALIST = "DIASPORA_SPECIALIST"


@dataclass
class Badge:
    badge_type: BadgeType = BadgeType.PHONE_VERIFIED
    label: str = ""
    earned_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"badge_type": self.badge_type.value, "label": self.label}


@dataclass
class AgencyMember:
    user_id: int = 0
    role: str = ""
    joined_at: str = ""
    trust_level: TrustLevel = TrustLevel.LEVEL_1
    badges: list[Badge] = field(default_factory=list)
    zone: str = ""


@dataclass
class AgencyOnboarding:
    status: str = "PENDING"
    profile_complete: bool = False
    training_complete: bool = False
    documents_submitted: bool = False
    approved_by: str = ""
    activated_at: str = ""
    steps: dict[str, bool] = field(default_factory=lambda: {
        "profile": False, "training": False, "documents": False,
        "approval": False, "activation": False,
    })

    def complete_step(self, step: str) -> None:
        if step in self.steps:
            self.steps[step] = True
        if all(self.steps.values()):
            self.status = "COMPLETED"
            self.activated_at = datetime.now(timezone.utc).isoformat()


@dataclass
class Agency:
    agency_id: int = 0
    name: str = ""
    trust_level: TrustLevel = TrustLevel.LEVEL_1
    verification_status: str = "PENDING"
    rccm: str = ""
    tax_id: str = ""
    cni_document: str = ""
    members: list[AgencyMember] = field(default_factory=list)
    minimum_agents: int = 3

    def is_operational(self) -> bool:
        active = sum(1 for m in self.members if m.role in ("agent", "admin"))
        return active >= self.minimum_agents

    def trust_score(self) -> float:
        if not self.members:
            return 0.0
        return sum(TRUST_LEVEL_ORDER.index(m.trust_level) + 1 for m in self.members) / len(self.members) / 6 * 100


TRUST_LEVEL_ORDER: list[TrustLevel] = list(TrustLevel)


class AgencyRole(str, Enum):
    RESPONSIBLE = "RESPONSIBLE"
    ADMIN = "ADMIN"
    AGENT = "AGENT"
    ASSISTANT = "ASSISTANT"


@dataclass
class AgentCredit:
    credits: float = 0.0
    total_spent: float = 0.0
    last_recharge: str = ""

    def deduct(self, amount: float) -> bool:
        if self.credits >= amount:
            self.credits -= amount
            self.total_spent += amount
            return True
        return False

    def recharge(self, amount: float) -> None:
        self.credits += amount
        self.last_recharge = datetime.now(timezone.utc).isoformat()


@dataclass
class AgentSubscription:
    subscription_type: str = ""
    price: float = 0.0
    currency: str = "XAF"
    start_at: str = ""
    end_at: str = ""
    trial: bool = False
    status: str = "ACTIVE"


@dataclass
class AgentZone:
    zone_code: str = ""
    name: str = ""
    agent_ids: list[int] = field(default_factory=list)
    capacity: int = 10

    def assign(self, agent_id: int) -> bool:
        if len(self.agent_ids) < self.capacity:
            self.agent_ids.append(agent_id)
            return True
        return False
