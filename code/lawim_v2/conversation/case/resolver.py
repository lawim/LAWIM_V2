from __future__ import annotations

from typing import Any

from ..domain.case import CaseStatus, LawimCase
from .repository import LawimCaseRepository
from .service import LawimCaseService


class ActiveCaseResolver:
    def __init__(
        self,
        repository: LawimCaseRepository,
        case_service: LawimCaseService,
    ) -> None:
        self._repository = repository
        self._case_service = case_service
        self.multiple_active: bool = False

    def resolve(
        self,
        case_id: str | None = None,
        conversation_id: str | None = None,
        actor_id: str | None = None,
        intent: str | None = None,
    ) -> LawimCase | None:
        self.multiple_active = False

        # 1. explicit case_id
        if case_id:
            case = self._repository.load(case_id)
            if case is not None:
                return case

        # 2. property_reference / transaction_reference
        if case_id and case_id.startswith("PR-"):
            cases = self._search_by_reference(case_id)
            if len(cases) == 1:
                return cases[0]
            if len(cases) > 1:
                self.multiple_active = True
                return None

        if conversation_id and conversation_id.startswith("TR-"):
            cases = self._search_by_reference(conversation_id)
            if len(cases) == 1:
                return cases[0]
            if len(cases) > 1:
                self.multiple_active = True
                return None

        # 3. case linked to current conversation
        if conversation_id:
            case = self._repository.load_by_conversation(conversation_id)
            if case is not None:
                return case

        # 4. active case matching intent for actor
        if actor_id and intent:
            active_cases = self._repository.load_active_by_actor(actor_id)
            if len(active_cases) > 1:
                matching = [c for c in active_cases if c.active_intent == intent]
                if len(matching) == 1:
                    return matching[0]
                if len(matching) > 1:
                    self.multiple_active = True
                    return None
                self.multiple_active = True
                return None

            if len(active_cases) == 1:
                return active_cases[0]

        # 5. controlled resume proposal — any non-terminal case for actor
        if actor_id:
            all_cases = self._repository.load_by_actor(actor_id)
            terminal = {CaseStatus.COMPLETED, CaseStatus.CANCELLED, CaseStatus.ARCHIVED}
            non_terminal = [c for c in all_cases if c.status not in terminal]
            if len(non_terminal) == 1:
                return non_terminal[0]
            if len(non_terminal) > 1:
                self.multiple_active = True
                return None

        # 6. no match — case_id was requested but not found
        if case_id:
            return None

        # 7. new case creation (DRAFT) — handled by caller
        return None

    def _search_by_reference(self, reference: str) -> list[LawimCase]:
        return self._repository.search(reference)
