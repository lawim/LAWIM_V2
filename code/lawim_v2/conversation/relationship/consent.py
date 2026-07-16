from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ConsentDirection(str, Enum):
    REQUESTER_TO_TARGET = "requester_to_target"
    TARGET_TO_REQUESTER = "target_to_requester"
    MUTUAL = "mutual"


class ConsentStatus(str, Enum):
    PENDING = "PENDING"
    GRANTED = "GRANTED"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


@dataclass
class RelationshipConsentRequest:
    consent_request_id: str = ""
    proposal_id: str = ""
    requester_user_id: int | None = None
    target_user_id: int | None = None
    direction: ConsentDirection = ConsentDirection.MUTUAL
    data_categories: list[str] = field(default_factory=list)
    status: ConsentStatus = ConsentStatus.PENDING
    purpose: str = ""
    created_at: str | None = None
    expires_at: str | None = None

    def is_valid(self) -> bool:
        if self.status != ConsentStatus.PENDING:
            return False
        if not self.expires_at:
            return False
        try:
            expires = datetime.fromisoformat(self.expires_at)
            if expires.tzinfo is None:
                expires = expires.replace(tzinfo=timezone.utc)
            return expires > datetime.now(timezone.utc)
        except (TypeError, ValueError):
            return False

    def to_dict(self) -> dict[str, Any]:
        return {
            "consent_request_id": self.consent_request_id,
            "proposal_id": self.proposal_id,
            "requester_user_id": self.requester_user_id,
            "target_user_id": self.target_user_id,
            "direction": self.direction.value,
            "data_categories": list(self.data_categories),
            "status": self.status.value,
            "purpose": self.purpose,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
        }


@dataclass
class ConsentDecision:
    decision_id: str = ""
    consent_request_id: str = ""
    user_id: int | None = None
    decision: ConsentStatus = ConsentStatus.PENDING
    reason: str | None = None
    decided_at: str | None = None

    def is_approval(self) -> bool:
        return self.decision == ConsentStatus.GRANTED

    def is_denial(self) -> bool:
        return self.decision == ConsentStatus.DENIED

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "consent_request_id": self.consent_request_id,
            "user_id": self.user_id,
            "decision": self.decision.value,
            "reason": self.reason,
            "decided_at": self.decided_at,
        }


class ConsentManager:
    def __init__(self) -> None:
        self._requests: dict[str, RelationshipConsentRequest] = {}
        self._decisions: dict[str, ConsentDecision] = {}

    def create_request(self, request: RelationshipConsentRequest) -> None:
        self._requests[request.consent_request_id] = request

    def get_request(self, request_id: str) -> RelationshipConsentRequest | None:
        return self._requests.get(request_id)

    def record_decision(self, decision: ConsentDecision) -> bool:
        request = self.get_request(decision.consent_request_id)
        if request is None:
            return False
        if not request.is_valid():
            return False

        self._decisions[decision.decision_id] = decision
        request.status = decision.decision
        return True

    def get_decision(self, decision_id: str) -> ConsentDecision | None:
        return self._decisions.get(decision_id)

    def get_decisions_for_request(
        self, request_id: str
    ) -> list[ConsentDecision]:
        return [
            d for d in self._decisions.values()
            if d.consent_request_id == request_id
        ]

    def is_consent_granted(self, request_id: str) -> bool:
        request = self.get_request(request_id)
        if request is None:
            return False
        return request.status == ConsentStatus.GRANTED

    def is_consent_denied(self, request_id: str) -> bool:
        request = self.get_request(request_id)
        if request is None:
            return False
        return request.status == ConsentStatus.DENIED

    def revoke_consent(self, request_id: str) -> bool:
        request = self.get_request(request_id)
        if request is None:
            return False
        if request.status != ConsentStatus.GRANTED:
            return False
        request.status = ConsentStatus.REVOKED
        return True

    def list_pending_for_user(self, user_id: int) -> list[RelationshipConsentRequest]:
        return [
            r for r in self._requests.values()
            if r.target_user_id == user_id and r.status == ConsentStatus.PENDING
        ]
