from __future__ import annotations

import logging
from typing import Any

from ..models.intent import Intent
from .base import BaseRegistry
from .errors import DuplicateEntryError, RegistryNotFoundError

logger = logging.getLogger(__name__)


class IntentRegistry(BaseRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._by_id: dict[str, Intent] = {}

    def register(self, item: Intent) -> None:
        self._check_readonly()
        if item.id in self._by_id:
            raise DuplicateEntryError(
                f"Duplicate intent: {item.id}",
                identifier=item.id,
            )
        self._by_id[item.id] = item

    def lock(self) -> None:
        self._lock()

    def get(self, intent_id: str) -> Intent:
        if intent_id in self._by_id:
            return self._by_id[intent_id]
        raise RegistryNotFoundError(f"Intent not found: {intent_id}", identifier=intent_id)

    def all(self) -> list[Intent]:
        return list(self._by_id.values())

    def count(self) -> int:
        return len(self._by_id)

    def summary(self) -> dict[str, Any]:
        base = super().summary()
        base.update({"registrations": self.count()})
        return base
