from __future__ import annotations

from abc import ABC, abstractmethod

from .models import NegotiationEntry, TransactionData


class TransactionRepository(ABC):

    @abstractmethod
    def save(self, transaction: TransactionData) -> None:
        ...

    @abstractmethod
    def get(self, transaction_id: str) -> TransactionData | None:
        ...

    @abstractmethod
    def list_by_project(self, project_id: str) -> list[TransactionData]:
        ...

    @abstractmethod
    def update_stage(self, transaction_id: str, stage: str) -> None:
        ...

    @abstractmethod
    def add_negotiation_entry(self, transaction_id: str, entry: NegotiationEntry) -> None:
        ...


class InMemoryTransactionRepository(TransactionRepository):

    def __init__(self) -> None:
        self._transactions: dict[str, TransactionData] = {}

    def save(self, transaction: TransactionData) -> None:
        self._transactions[transaction.transaction_id] = transaction

    def get(self, transaction_id: str) -> TransactionData | None:
        return self._transactions.get(transaction_id)

    def list_by_project(self, project_id: str) -> list[TransactionData]:
        return [t for t in self._transactions.values() if t.project_id == project_id]

    def update_stage(self, transaction_id: str, stage: str) -> None:
        transaction = self._transactions.get(transaction_id)
        if transaction:
            transaction.stage = stage

    def add_negotiation_entry(self, transaction_id: str, entry: NegotiationEntry) -> None:
        transaction = self._transactions.get(transaction_id)
        if transaction:
            transaction.negotiation_history.append(entry)
