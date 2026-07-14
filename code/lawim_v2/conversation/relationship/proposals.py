from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ProposalStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_CONSENT = "PENDING_CONSENT"
    CONSENT_GRANTED = "CONSENT_GRANTED"
    CONSENT_DENIED = "CONSENT_DENIED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    WITHDRAWN = "WITHDRAWN"


@dataclass
class RelationshipProposal:
    proposal_id: str = ""
    project_id: int | None = None
    dossier_id: int | None = None
    requester_user_id: int | None = None
    target_user_id: int | None = None
    target_item_id: str | None = None
    target_partner_id: int | None = None
    relationship_type: str = "buyer_seller"
    status: ProposalStatus = ProposalStatus.DRAFT
    context: dict[str, Any] = field(default_factory=dict)
    notes: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    expires_at: str | None = None

    def is_pending(self) -> bool:
        return self.status in {
            ProposalStatus.DRAFT,
            ProposalStatus.PENDING_CONSENT,
        }

    def is_actionable(self) -> bool:
        return self.status in {
            ProposalStatus.CONSENT_GRANTED,
            ProposalStatus.PENDING_CONSENT,
        }

    def is_terminal(self) -> bool:
        return self.status in {
            ProposalStatus.ACCEPTED,
            ProposalStatus.REJECTED,
            ProposalStatus.EXPIRED,
            ProposalStatus.WITHDRAWN,
        }

    def has_expired(self) -> bool:
        if not self.expires_at:
            return False
        try:
            now = datetime.utcnow().isoformat()
            return self.expires_at < now
        except Exception:
            return False

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "project_id": self.project_id,
            "dossier_id": self.dossier_id,
            "requester_user_id": self.requester_user_id,
            "target_user_id": self.target_user_id,
            "target_item_id": self.target_item_id,
            "target_partner_id": self.target_partner_id,
            "relationship_type": self.relationship_type,
            "status": self.status.value,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "expires_at": self.expires_at,
        }


class ProposalManager:
    def __init__(self) -> None:
        self._proposals: dict[str, RelationshipProposal] = {}

    def add(self, proposal: RelationshipProposal) -> None:
        self._proposals[proposal.proposal_id] = proposal

    def get(self, proposal_id: str) -> RelationshipProposal | None:
        return self._proposals.get(proposal_id)

    def update_status(self, proposal_id: str, status: ProposalStatus) -> bool:
        proposal = self.get(proposal_id)
        if proposal is None:
            return False
        proposal.status = status
        proposal.updated_at = datetime.utcnow().isoformat()
        return True

    def list_by_requester(self, user_id: int) -> list[RelationshipProposal]:
        return [
            p for p in self._proposals.values()
            if p.requester_user_id == user_id
        ]

    def list_by_target(self, user_id: int) -> list[RelationshipProposal]:
        return [
            p for p in self._proposals.values()
            if p.target_user_id == user_id
        ]

    def list_pending(self) -> list[RelationshipProposal]:
        return [
            p for p in self._proposals.values()
            if p.is_pending()
        ]

    def remove_expired(self) -> list[RelationshipProposal]:
        expired = [p for p in self._proposals.values() if p.has_expired()]
        for p in expired:
            p.status = ProposalStatus.EXPIRED
            p.updated_at = datetime.utcnow().isoformat()
        return expired
