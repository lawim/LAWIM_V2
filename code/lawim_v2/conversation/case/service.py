from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from ..domain.case import CaseStatus, CaseType, LawimCase
from ..domain.case_link import CaseConversationLink
from .repository import LawimCaseRepository


class LawimCaseService:
    def __init__(self, repository: LawimCaseRepository) -> None:
        self._repository = repository

    def create_case(
        self,
        *,
        case_type: str = "",
        primary_actor_id: str = "",
        title: str = "",
        active_intent: str = "",
        journey_code: str = "",
        active_language: str = "fr",
        property_reference: str | None = None,
    ) -> LawimCase:
        now = datetime.now(timezone.utc).isoformat()
        case_id = str(uuid4())
        case_code = f"CS-{case_id[:8].upper()}"
        case = LawimCase(
            case_id=case_id,
            case_code=case_code,
            case_type=case_type,
            primary_actor_id=primary_actor_id,
            title=title,
            active_intent=active_intent,
            journey_code=journey_code,
            status=CaseStatus.DRAFT,
            active_language=active_language,
            property_reference=property_reference,
            created_at=now,
            updated_at=now,
            version=1,
        )
        return self._repository.save(case)

    def get_case(self, case_id: str) -> LawimCase | None:
        if not case_id:
            return None
        return self._repository.load(case_id)

    def update_case(self, case: LawimCase) -> LawimCase:
        if not case.case_id:
            raise ValueError("Cannot update a case without a case_id")
        return self._repository.save(case)

    def get_active_cases(self, actor_id: str) -> list[LawimCase]:
        if not actor_id:
            return []
        return self._repository.load_active_by_actor(actor_id)

    def close_case(self, case_id: str) -> LawimCase | None:
        case = self._repository.load(case_id)
        if case is None:
            return None
        now = datetime.now(timezone.utc).isoformat()
        case.status = CaseStatus.COMPLETED
        case.closed_at = now
        case.updated_at = now
        return self._repository.save(case)

    def archive_case(self, case_id: str) -> LawimCase | None:
        case = self._repository.load(case_id)
        if case is None:
            return None
        case.status = CaseStatus.ARCHIVED
        case.updated_at = datetime.now(timezone.utc).isoformat()
        return self._repository.save(case)

    def link_conversation(
        self,
        case_id: str,
        conversation_id: str,
        channel: str,
        actor_id: str,
    ) -> CaseConversationLink:
        existing = self._repository.load_link_by_conversation(conversation_id)
        if existing:
            link = CaseConversationLink(
                link_id=existing["link_id"],
                case_id=existing["case_id"],
                conversation_id=existing["conversation_id"],
                channel=existing["channel"],
                actor_id=existing.get("actor_id", actor_id),
                linked_at=existing["linked_at"],
                is_active=bool(existing["is_active"]),
                unlinked_at=existing.get("unlinked_at"),
            )
            if link.is_active and link.case_id == case_id:
                return link
            if link.is_active:
                link.is_active = False
                link.unlinked_at = datetime.now(timezone.utc).isoformat()
                self._repository.save_link(link)

        link_id = str(uuid4())
        now = datetime.now(timezone.utc).isoformat()
        link = CaseConversationLink(
            link_id=link_id,
            case_id=case_id,
            conversation_id=conversation_id,
            channel=channel,
            actor_id=actor_id,
            linked_at=now,
            is_active=True,
            unlinked_at=None,
        )
        self._repository.save_link(link)
        case = self._repository.load(case_id)
        if case is not None:
            case.active_conversation_id = conversation_id
            self._repository.save(case)
        return link

    def unlink_conversation(self, case_id: str, conversation_id: str) -> None:
        link_row = self._repository.load_link_by_conversation(conversation_id)
        if link_row is None:
            return
        now = datetime.now(timezone.utc).isoformat()
        link = CaseConversationLink(
            link_id=link_row["link_id"],
            case_id=link_row["case_id"],
            conversation_id=link_row["conversation_id"],
            channel=link_row["channel"],
            actor_id=link_row.get("actor_id", ""),
            linked_at=link_row["linked_at"],
            is_active=False,
            unlinked_at=now,
        )
        self._repository.save_link(link)
        case = self._repository.load(case_id)
        if case is not None and case.active_conversation_id == conversation_id:
            case.active_conversation_id = None
            self._repository.save(case)

    def get_linked_conversation(self, case_id: str) -> dict | None:
        return self._repository.load_active_link(case_id)

    def resolve_or_create(
        self,
        *,
        actor_id: str = "",
        case_type: str = "",
        active_intent: str = "",
        journey_code: str = "",
        active_language: str = "fr",
    ) -> LawimCase:
        terminal_statuses = {
            CaseStatus.COMPLETED,
            CaseStatus.CANCELLED,
            CaseStatus.ARCHIVED,
        }
        all_cases = self._repository.load_by_actor(actor_id)
        existing = [
            c for c in all_cases
            if c.active_intent == active_intent and c.status not in terminal_statuses
        ]
        if existing:
            return existing[0]
        return self.create_case(
            case_type=case_type,
            primary_actor_id=actor_id,
            active_intent=active_intent,
            journey_code=journey_code,
            active_language=active_language,
        )
