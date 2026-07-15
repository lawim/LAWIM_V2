from __future__ import annotations

import logging
from typing import Any

from ..models.matching_semantic import MatchingSemantic
from .base import BaseRegistry
from .errors import DuplicateEntryError, RegistryNotFoundError

logger = logging.getLogger(__name__)


class MatchingSemanticRegistry(BaseRegistry):
    EXPECTED_SEMANTICS: frozenset[str] = frozenset({
        "hard_constraint",
        "soft_constraint",
        "ranking_preference",
        "exclusion",
        "boost",
        "penalty",
        "informational_only",
        "verification_only",
        "transaction_blocker",
    })

    def __init__(self) -> None:
        super().__init__()
        self._by_id: dict[str, MatchingSemantic] = {}

    def register(self, item: MatchingSemantic) -> None:
        self._check_readonly()
        if item.role_id in self._by_id:
            raise DuplicateEntryError(
                f"Duplicate matching semantic: {item.role_id}",
                identifier=item.role_id,
            )
        self._by_id[item.role_id] = item

    def lock(self) -> None:
        self._validate_all_nine_loaded()
        self._lock()

    def _validate_all_nine_loaded(self) -> None:
        loaded = set(self._by_id.keys())
        missing = self.EXPECTED_SEMANTICS - loaded
        if missing:
            logger.warning("Missing matching semantics: %s", missing)

    def get(self, role_id: str) -> MatchingSemantic:
        if role_id in self._by_id:
            return self._by_id[role_id]
        raise RegistryNotFoundError(f"Matching semantic not found: {role_id}", identifier=role_id)

    def all(self) -> list[MatchingSemantic]:
        return list(self._by_id.values())

    def count(self) -> int:
        return len(self._by_id)

    def summary(self) -> dict[str, Any]:
        base = super().summary()
        loaded = set(self._by_id.keys())
        missing = self.EXPECTED_SEMANTICS - loaded
        base.update({
            "registrations": self.count(),
            "expected": len(self.EXPECTED_SEMANTICS),
            "missing": sorted(missing),
        })
        return base
