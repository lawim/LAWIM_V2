from __future__ import annotations

import logging
from typing import Any

from ..models.transaction import Transaction
from .base import BaseRegistry
from .errors import DuplicateEntryError, RegistryNotFoundError

logger = logging.getLogger(__name__)


class TransactionRegistry(BaseRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._by_id: dict[str, Transaction] = {}

    def register(self, item: Transaction) -> None:
        self._check_readonly()
        if item.id in self._by_id:
            raise DuplicateEntryError(
                f"Duplicate transaction: {item.id}",
                identifier=item.id,
            )
        self._by_id[item.id] = item

    def lock(self) -> None:
        self._lock()

    def get(self, transaction_id: str) -> Transaction:
        if transaction_id in self._by_id:
            return self._by_id[transaction_id]
        raise RegistryNotFoundError(
            f"Transaction not found: {transaction_id}",
            identifier=transaction_id,
        )

    def by_type(self, ttype: str) -> list[Transaction]:
        return [t for t in self._by_id.values() if t.transaction_type == ttype]

    def all(self) -> list[Transaction]:
        return list(self._by_id.values())

    def count(self) -> int:
        return len(self._by_id)

    def summary(self) -> dict[str, Any]:
        base = super().summary()
        base.update({"registrations": self.count()})
        return base
