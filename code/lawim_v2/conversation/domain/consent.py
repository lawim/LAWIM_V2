from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ConsentStatus(str, Enum):
    PENDING = "PENDING"
    GRANTED = "GRANTED"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


@dataclass
class ConsentRequest:
    request_id: str = ""
    requester_user_id: int | None = None
    target_user_id: int | None = None
    relationship_proposal_id: str | None = None
    purpose: str = ""
    data_to_share: list[str] = field(default_factory=list)
    status: ConsentStatus = ConsentStatus.PENDING
    created_at: str | None = None
    expires_at: str | None = None

    def is_valid(self) -> bool:
        return self.status == ConsentStatus.PENDING and self.expires_at is not None

    def to_shareable_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "purpose": self.purpose,
            "data_to_share": list(self.data_to_share),
            "status": self.status.value,
            "expires_at": self.expires_at,
        }


@dataclass
class ConsentDecision:
    decision_id: str = ""
    request_id: str = ""
    user_id: int | None = None
    decision: ConsentStatus = ConsentStatus.PENDING
    reason: str | None = None
    decided_at: str | None = None
