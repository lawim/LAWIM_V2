from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .privacy import DataCategory, PrivacyController


@dataclass
class Introduction:
    introduction_id: str = ""
    relationship_id: str = ""
    proposal_id: str = ""
    initiated_by_user_id: int | None = None
    data_shared: dict[str, Any] = field(default_factory=dict)
    presented_to_requester: bool = False
    presented_to_target: bool = False
    created_at: str | None = None
    completed_at: str | None = None

    @property
    def is_complete(self) -> bool:
        return self.presented_to_requester and self.presented_to_target

    def to_dict(self) -> dict[str, Any]:
        return {
            "introduction_id": self.introduction_id,
            "relationship_id": self.relationship_id,
            "proposal_id": self.proposal_id,
            "initiated_by_user_id": self.initiated_by_user_id,
            "is_complete": self.is_complete,
            "presented_to_requester": self.presented_to_requester,
            "presented_to_target": self.presented_to_target,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }


class IntroductionBuilder:
    def __init__(self, privacy_controller: PrivacyController | None = None):
        self.privacy_controller = privacy_controller or PrivacyController()

    def build(
        self,
        introduction_id: str,
        relationship_id: str,
        proposal_id: str,
        requester_user_id: int,
        target_user_id: int,
        requester_data: dict[str, Any],
        target_data: dict[str, Any],
        consented_categories: list[DataCategory],
    ) -> Introduction:
        consented_set = set(consented_categories)

        filtered_requester = self._filter_data(
            requester_data, consented_set
        )
        filtered_target = self._filter_data(
            target_data, consented_set
        )

        data_shared = {
            "requester": filtered_requester,
            "target": filtered_target,
        }

        now = datetime.utcnow().isoformat()
        return Introduction(
            introduction_id=introduction_id,
            relationship_id=relationship_id,
            proposal_id=proposal_id,
            initiated_by_user_id=requester_user_id,
            data_shared=data_shared,
            created_at=now,
        )

    def _filter_data(
        self,
        data: dict[str, Any],
        consented_categories: set[DataCategory],
    ) -> dict[str, Any]:
        filtered: dict[str, Any] = {}
        for key, value in data.items():
            try:
                category = DataCategory(key)
            except ValueError:
                filtered[key] = value
                continue
            if category in consented_categories:
                filtered[key] = value
        return filtered


class IntroductionManager:
    def __init__(self) -> None:
        self._introductions: dict[str, Introduction] = {}

    def add(self, introduction: Introduction) -> None:
        self._introductions[introduction.introduction_id] = introduction

    def get(self, introduction_id: str) -> Introduction | None:
        return self._introductions.get(introduction_id)

    def complete(self, introduction_id: str) -> bool:
        introduction = self.get(introduction_id)
        if introduction is None:
            return False
        introduction.presented_to_requester = True
        introduction.presented_to_target = True
        introduction.completed_at = datetime.utcnow().isoformat()
        return True

    def mark_presented_to_requester(self, introduction_id: str) -> bool:
        introduction = self.get(introduction_id)
        if introduction is None:
            return False
        introduction.presented_to_requester = True
        if introduction.is_complete:
            introduction.completed_at = datetime.utcnow().isoformat()
        return True

    def mark_presented_to_target(self, introduction_id: str) -> bool:
        introduction = self.get(introduction_id)
        if introduction is None:
            return False
        introduction.presented_to_target = True
        if introduction.is_complete:
            introduction.completed_at = datetime.utcnow().isoformat()
        return True
