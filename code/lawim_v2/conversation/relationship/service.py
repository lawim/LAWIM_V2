from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .consent import (
    ConsentDecision,
    ConsentDirection,
    ConsentManager,
    ConsentStatus,
    RelationshipConsentRequest,
)
from .introductions import Introduction, IntroductionBuilder, IntroductionManager
from .lifecycle import Relationship, RelationshipLifecycle, RelationshipStatus
from .participants import Participant, ParticipantManager, ParticipantRole, ParticipantStatus
from .privacy import DataCategory, PrivacyController
from .proposals import ProposalManager, ProposalStatus, RelationshipProposal

from ..domain.errors import ConversationError


class RelationshipError(ConversationError):
    def __init__(self, message: str, relationship_id: str | None = None):
        super().__init__(message, code="relationship_error", details={"relationship_id": relationship_id})


class ConsentError(ConversationError):
    def __init__(self, message: str, request_id: str | None = None):
        super().__init__(message, code="consent_error", details={"request_id": request_id})


@dataclass
class RelationshipService:
    proposal_manager: ProposalManager = field(default_factory=ProposalManager)
    consent_manager: ConsentManager = field(default_factory=ConsentManager)
    participant_manager: ParticipantManager = field(default_factory=ParticipantManager)
    lifecycle: RelationshipLifecycle = field(default_factory=RelationshipLifecycle)
    introduction_manager: IntroductionManager = field(default_factory=IntroductionManager)
    privacy_controller: PrivacyController = field(default_factory=PrivacyController)
    introduction_builder: IntroductionBuilder = field(default_factory=IntroductionBuilder)

    def create_proposal(
        self,
        requester_user_id: int,
        target_user_id: int,
        target_item_id: str,
        relationship_type: str = "buyer_seller",
        project_id: int | None = None,
        dossier_id: int | None = None,
        context: dict[str, Any] | None = None,
        notes: str | None = None,
        expires_in_hours: int = 48,
    ) -> RelationshipProposal:
        now = datetime.utcnow().isoformat()
        import datetime as dt
        expires_at = (
            datetime.utcnow() + dt.timedelta(hours=expires_in_hours)
        ).isoformat()

        proposal = RelationshipProposal(
            proposal_id=f"prop_{uuid.uuid4().hex[:12]}",
            project_id=project_id,
            dossier_id=dossier_id,
            requester_user_id=requester_user_id,
            target_user_id=target_user_id,
            target_item_id=target_item_id,
            relationship_type=relationship_type,
            status=ProposalStatus.DRAFT,
            context=context or {},
            notes=notes,
            created_at=now,
            updated_at=now,
            expires_at=expires_at,
        )

        self.proposal_manager.add(proposal)
        return proposal

    def request_consent(
        self,
        proposal_id: str,
        data_categories: list[DataCategory] | None = None,
        direction: ConsentDirection = ConsentDirection.MUTUAL,
    ) -> RelationshipConsentRequest:
        proposal = self.proposal_manager.get(proposal_id)
        if proposal is None:
            raise RelationshipError(f"Proposal {proposal_id} not found")

        if proposal.is_terminal():
            raise RelationshipError(f"Proposal {proposal_id} is in terminal state {proposal.status.value}")

        categories = data_categories or [
            DataCategory.NAME,
            DataCategory.CONTACT_INFO,
        ]

        required_categories = self.privacy_controller.get_required_consent_categories(categories)

        now = datetime.utcnow().isoformat()
        import datetime as dt
        expires_at = (
            datetime.utcnow() + dt.timedelta(hours=72)
        ).isoformat()

        consent_request = RelationshipConsentRequest(
            consent_request_id=f"creq_{uuid.uuid4().hex[:12]}",
            proposal_id=proposal_id,
            requester_user_id=proposal.requester_user_id,
            target_user_id=proposal.target_user_id,
            direction=direction,
            data_categories=[c.value for c in required_categories],
            status=ConsentStatus.PENDING,
            purpose=f"Share information for {proposal.relationship_type} relationship",
            created_at=now,
            expires_at=expires_at,
        )

        self.consent_manager.create_request(consent_request)

        proposal.status = ProposalStatus.PENDING_CONSENT
        proposal.updated_at = now

        return consent_request

    def record_consent_decision(
        self,
        consent_request_id: str,
        user_id: int,
        granted: bool,
        reason: str | None = None,
    ) -> ConsentDecision:
        request = self.consent_manager.get_request(consent_request_id)
        if request is None:
            raise ConsentError(f"Consent request {consent_request_id} not found")

        if not request.is_valid():
            raise ConsentError(f"Consent request {consent_request_id} is no longer valid")

        if request.target_user_id != user_id:
            raise ConsentError(f"User {user_id} is not the target of this consent request")

        decision_status = ConsentStatus.GRANTED if granted else ConsentStatus.DENIED

        decision = ConsentDecision(
            decision_id=f"dec_{uuid.uuid4().hex[:12]}",
            consent_request_id=consent_request_id,
            user_id=user_id,
            decision=decision_status,
            reason=reason,
            decided_at=datetime.utcnow().isoformat(),
        )

        success = self.consent_manager.record_decision(decision)
        if not success:
            raise ConsentError(f"Failed to record decision for request {consent_request_id}")

        proposal = self.proposal_manager.get(request.proposal_id)
        if proposal:
            if granted:
                proposal.status = ProposalStatus.CONSENT_GRANTED
            else:
                proposal.status = ProposalStatus.CONSENT_DENIED
            proposal.updated_at = datetime.utcnow().isoformat()

        return decision

    def create_relationship(
        self,
        proposal_id: str,
        requester_user_id: int,
        target_user_id: int,
        requester_data: dict[str, Any],
        target_data: dict[str, Any],
    ) -> Relationship:
        proposal = self.proposal_manager.get(proposal_id)
        if proposal is None:
            raise RelationshipError(f"Proposal {proposal_id} not found")

        if proposal.status != ProposalStatus.CONSENT_GRANTED:
            raise RelationshipError(
                f"Proposal {proposal_id} must have consent granted before creating relationship"
            )

        now = datetime.utcnow().isoformat()

        relationship = Relationship(
            relationship_id=f"rel_{uuid.uuid4().hex[:12]}",
            proposal_id=proposal_id,
            project_id=proposal.project_id,
            dossier_id=proposal.dossier_id,
            status=RelationshipStatus.ACTIVE,
            relationship_type=proposal.relationship_type,
            created_at=now,
            updated_at=now,
            activated_at=now,
        )

        self.lifecycle.create(relationship)

        requester_participant = Participant(
            participant_id=f"part_{uuid.uuid4().hex[:12]}",
            relationship_id=relationship.relationship_id,
            user_id=requester_user_id,
            role=ParticipantRole.REQUESTER,
            status=ParticipantStatus.ACTIVE,
            joined_at=now,
        )
        self.participant_manager.add(requester_participant)

        target_participant = Participant(
            participant_id=f"part_{uuid.uuid4().hex[:12]}",
            relationship_id=relationship.relationship_id,
            user_id=target_user_id,
            role=ParticipantRole.TARGET,
            status=ParticipantStatus.ACTIVE,
            joined_at=now,
        )
        self.participant_manager.add(target_participant)

        consent_request = self._find_granted_consent(proposal_id)
        consented_categories = []
        if consent_request:
            consented_categories = [
                DataCategory(cat) for cat in consent_request.data_categories
            ]

        introduction = self.introduction_builder.build(
            introduction_id=f"intro_{uuid.uuid4().hex[:12]}",
            relationship_id=relationship.relationship_id,
            proposal_id=proposal_id,
            requester_user_id=requester_user_id,
            target_user_id=target_user_id,
            requester_data=requester_data,
            target_data=target_data,
            consented_categories=consented_categories,
        )
        self.introduction_manager.add(introduction)

        proposal.status = ProposalStatus.ACCEPTED
        proposal.updated_at = now

        return relationship

    def complete_relationship(self, relationship_id: str) -> bool:
        return self.lifecycle.complete(relationship_id)

    def pause_relationship(self, relationship_id: str) -> bool:
        return self.lifecycle.pause(relationship_id)

    def resume_relationship(self, relationship_id: str) -> bool:
        return self.lifecycle.resume(relationship_id)

    def cancel_relationship(self, relationship_id: str) -> bool:
        return self.lifecycle.cancel(relationship_id)

    def get_proposal(self, proposal_id: str) -> RelationshipProposal | None:
        return self.proposal_manager.get(proposal_id)

    def get_relationship(self, relationship_id: str) -> Relationship | None:
        return self.lifecycle.get(relationship_id)

    def get_participants(self, relationship_id: str) -> list[Participant]:
        return self.participant_manager.get_by_relationship(relationship_id)

    def get_introduction(self, introduction_id: str) -> Introduction | None:
        return self.introduction_manager.get(introduction_id)

    def shareable_data(
        self,
        data: dict[str, Any],
        relationship_id: str,
    ) -> dict[str, Any]:
        relationship = self.lifecycle.get(relationship_id)
        has_relationship = relationship is not None and relationship.is_active()
        has_consent = has_relationship

        return self.privacy_controller.filter_shareable_data(
            data,
            has_consent=has_consent,
            has_relationship=has_relationship,
        )

    def _find_granted_consent(
        self,
        proposal_id: str,
    ) -> RelationshipConsentRequest | None:
        for request in self.consent_manager._requests.values():
            if request.proposal_id == proposal_id and request.status == ConsentStatus.GRANTED:
                return request
        return None
