from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import PaymentProviderAdapter, ProviderHealth


@dataclass(slots=True)
class PaymentProviderRegistry:
    providers: dict[str, PaymentProviderAdapter] = field(default_factory=dict)

    def register(self, provider: PaymentProviderAdapter) -> None:
        self.providers[provider.code.upper()] = provider

    def get(self, code: str) -> PaymentProviderAdapter | None:
        return self.providers.get(code.upper())

    def list(self) -> list[PaymentProviderAdapter]:
        return [self.providers[key] for key in sorted(self.providers)]

    def health_snapshot(self) -> list[dict[str, object]]:
        return [provider.health_check().to_dict() for provider in self.list()]


def build_default_provider_registry(config: Any) -> PaymentProviderRegistry:
    from .campay import CampayProviderAdapter

    registry = PaymentProviderRegistry()
    registry.register(CampayProviderAdapter(config))
    return registry
