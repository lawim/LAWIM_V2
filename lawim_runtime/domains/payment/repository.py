from __future__ import annotations

from abc import ABC, abstractmethod

from .models import PaymentData, PaymentIntent


class PaymentRepository(ABC):

    @abstractmethod
    def save_intent(self, intent: PaymentIntent) -> None:
        ...

    @abstractmethod
    def get_intent(self, intent_id: str) -> PaymentIntent | None:
        ...

    @abstractmethod
    def get_by_idempotency(self, idempotency_key: str) -> PaymentData | None:
        ...

    @abstractmethod
    def save_payment(self, payment: PaymentData) -> None:
        ...

    @abstractmethod
    def get_payment(self, payment_id: str) -> PaymentData | None:
        ...

    @abstractmethod
    def list_by_project(self, project_id: str) -> list[PaymentData]:
        ...


class InMemoryPaymentRepository(PaymentRepository):

    def __init__(self) -> None:
        self._intents: dict[str, PaymentIntent] = {}
        self._payments: dict[str, PaymentData] = {}
        self._by_idempotency: dict[str, PaymentData] = {}

    def save_intent(self, intent: PaymentIntent) -> None:
        self._intents[intent.intent_id] = intent

    def get_intent(self, intent_id: str) -> PaymentIntent | None:
        return self._intents.get(intent_id)

    def get_by_idempotency(self, idempotency_key: str) -> PaymentData | None:
        return self._by_idempotency.get(idempotency_key)

    def save_payment(self, payment: PaymentData) -> None:
        self._payments[payment.payment_id] = payment
        if payment.idempotency_key:
            self._by_idempotency[payment.idempotency_key] = payment

    def get_payment(self, payment_id: str) -> PaymentData | None:
        return self._payments.get(payment_id)

    def list_by_project(self, project_id: str) -> list[PaymentData]:
        return [p for p in self._payments.values() if p.project_id == project_id]
