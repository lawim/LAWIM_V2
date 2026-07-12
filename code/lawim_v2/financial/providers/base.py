from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class ProviderHealth:
    code: str
    name: str
    status: str
    environment: str
    available: bool
    latency_ms: float | None = None
    details: dict[str, object] | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "name": self.name,
            "status": self.status,
            "environment": self.environment,
            "available": self.available,
            "latency_ms": self.latency_ms,
            "details": self.details or {},
        }


@runtime_checkable
class PaymentProviderAdapter(Protocol):
    code: str
    name: str

    def authenticate(self) -> dict[str, object]: ...
    def create_payment(self, *, payload: dict[str, object]) -> dict[str, object]: ...
    def get_payment_status(self, *, provider_reference: str) -> dict[str, object]: ...
    def cancel_payment(self, *, provider_reference: str) -> dict[str, object]: ...
    def refund_payment(self, *, provider_reference: str, amount_minor: int) -> dict[str, object]: ...
    def validate_webhook(self, *, headers: dict[str, str], payload: bytes) -> bool: ...
    def parse_webhook(self, *, payload: bytes) -> dict[str, object]: ...
    def verify_transaction(self, *, provider_reference: str) -> dict[str, object]: ...
    def health_check(self) -> ProviderHealth: ...
