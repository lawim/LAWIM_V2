from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ChannelEndpointStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    BLOCKED = "BLOCKED"
    ARCHIVED = "ARCHIVED"


@dataclass
class EndpointVerification:
    verified: bool = False
    verified_at: str | None = None
    method: str = ""
    trust_level: int = 0


@dataclass
class ChannelEndpoint:
    endpoint_id: str
    provider: str
    channel: str
    provider_user_id: str
    external_id: str
    raw_external_id: str = ""
    user_id: int | None = None
    actor_id: str | None = None
    verification: EndpointVerification = field(default_factory=EndpointVerification)
    consent_granted: bool = False
    consent_type: str = ""
    status: ChannelEndpointStatus = ChannelEndpointStatus.ACTIVE
    display_name: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "endpoint_id": self.endpoint_id,
            "provider": self.provider,
            "channel": self.channel,
            "provider_user_id": self.provider_user_id,
            "external_id": self.external_id,
            "user_id": self.user_id,
            "actor_id": self.actor_id,
            "verified": self.verification.verified,
            "consent_granted": self.consent_granted,
            "status": self.status.value,
            "display_name": self.display_name,
        }
