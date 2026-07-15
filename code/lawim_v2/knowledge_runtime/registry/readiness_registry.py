from __future__ import annotations

import logging
from typing import Any

from ..models.readiness import ReadinessDefinition, ReadinessLevel
from .base import BaseRegistry
from .errors import DuplicateEntryError

logger = logging.getLogger(__name__)


class ReadinessRegistry(BaseRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._by_level: dict[ReadinessLevel, ReadinessDefinition] = {}
        self._by_order: dict[int, ReadinessDefinition] = {}

    def register(self, item: ReadinessDefinition) -> None:
        self._check_readonly()
        if item.level in self._by_level:
            raise DuplicateEntryError(
                f"Duplicate readiness level: {item.level.value}",
                identifier=item.level.value,
            )
        self._by_level[item.level] = item
        self._by_order[item.order] = item

    def lock(self) -> None:
        self._lock()

    def get(self, level: ReadinessLevel) -> ReadinessDefinition:
        return self._by_level.get(level)

    def get_by_order(self, order: int) -> ReadinessDefinition:
        return self._by_order.get(order)

    def all(self) -> list[ReadinessDefinition]:
        return [self._by_order[o] for o in sorted(self._by_order)]

    def count(self) -> int:
        return len(self._by_level)

    def summary(self) -> dict[str, Any]:
        base = super().summary()
        base.update({"registrations": self.count()})
        return base
