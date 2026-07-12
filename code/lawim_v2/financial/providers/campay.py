from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...errors import ValidationError
from ..exceptions import PaymentProviderUnavailable
from .base import ProviderHealth


@dataclass(slots=True)
class CampayProviderAdapter:
    config: Any
    code: str = "CAMPAY"
    name: str = "Campay"

    def _enabled(self) -> bool:
        return bool(getattr(self.config, "campay_enabled", False))

    def authenticate(self) -> dict[str, object]:
        if not self._enabled():
            raise PaymentProviderUnavailable("Campay is disabled")
        token = getattr(self.config, "campay_token", None)
        if not token:
            raise PaymentProviderUnavailable("Campay token is missing")
        return {
            "provider": self.code,
            "status": "authenticated",
            "environment": getattr(self.config, "campay_environment", "sandbox"),
        }

    def create_payment(self, *, payload: dict[str, object]) -> dict[str, object]:
        raise PaymentProviderUnavailable("Campay integration is not activated yet")

    def get_payment_status(self, *, provider_reference: str) -> dict[str, object]:
        raise PaymentProviderUnavailable("Campay integration is not activated yet")

    def cancel_payment(self, *, provider_reference: str) -> dict[str, object]:
        raise PaymentProviderUnavailable("Campay integration is not activated yet")

    def refund_payment(self, *, provider_reference: str, amount_minor: int) -> dict[str, object]:
        raise PaymentProviderUnavailable("Campay integration is not activated yet")

    def validate_webhook(self, *, headers: dict[str, str], payload: bytes) -> bool:
        if not self._enabled():
            return False
        secret = getattr(self.config, "campay_webhook_secret", None)
        return bool(secret)

    def parse_webhook(self, *, payload: bytes) -> dict[str, object]:
        return {"provider": self.code, "payload_size": len(payload), "status": "unparsed"}

    def verify_transaction(self, *, provider_reference: str) -> dict[str, object]:
        raise PaymentProviderUnavailable("Campay integration is not activated yet")

    def health_check(self) -> ProviderHealth:
        status = "active" if self._enabled() else "disabled"
        details = {
            "has_base_url": bool(getattr(self.config, "campay_base_url", None)),
            "has_username": bool(getattr(self.config, "campay_app_username", None)),
            "has_password": bool(getattr(self.config, "campay_app_password", None)),
            "has_token": bool(getattr(self.config, "campay_token", None)),
            "webhook_configured": bool(getattr(self.config, "campay_webhook_url", None)),
        }
        return ProviderHealth(
            code=self.code,
            name=self.name,
            status=status,
            environment=str(getattr(self.config, "campay_environment", "sandbox")),
            available=self._enabled(),
            details=details,
        )
