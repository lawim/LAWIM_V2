from __future__ import annotations

import logging
from typing import Any

from ..models.source_trace import SourceTrace
from .base import BaseRegistry
from .errors import DuplicateEntryError, RegistryNotFoundError

logger = logging.getLogger(__name__)


class SourceTraceRegistry(BaseRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._by_id: dict[str, SourceTrace] = {}

    def register(self, item: SourceTrace) -> None:
        self._check_readonly()
        if item.concept_id in self._by_id:
            raise DuplicateEntryError(
                f"Duplicate source trace: {item.concept_id}",
                identifier=item.concept_id,
            )
        self._by_id[item.concept_id] = item

    def lock(self) -> None:
        self._lock()

    def get(self, concept_id: str) -> SourceTrace:
        if concept_id in self._by_id:
            return self._by_id[concept_id]
        raise RegistryNotFoundError(f"Source trace not found: {concept_id}", identifier=concept_id)

    def by_type(self, concept_type: str) -> list[SourceTrace]:
        return [t for t in self._by_id.values() if t.concept_type == concept_type]

    def all(self) -> list[SourceTrace]:
        return list(self._by_id.values())

    def count(self) -> int:
        return len(self._by_id)

    def summary(self) -> dict[str, Any]:
        base = super().summary()
        base.update({"registrations": self.count()})
        return base
