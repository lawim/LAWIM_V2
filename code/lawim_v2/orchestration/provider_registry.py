from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any

from .config import (
    DEFAULT_CIRCUIT_BREAKER_RECOVERY_SECONDS,
    DEFAULT_CIRCUIT_BREAKER_THRESHOLD,
    DEFAULT_PROVIDER_CHAIN,
)


class ProviderStatus(str, Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    CIRCUIT_OPEN = "CIRCUIT_OPEN"
    CIRCUIT_HALF_OPEN = "CIRCUIT_HALF_OPEN"
    RATE_LIMITED = "RATE_LIMITED"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"


@dataclass
class ProviderHealth:
    provider: str = ""
    model: str = ""
    status: ProviderStatus = ProviderStatus.ENABLED
    latency_p50_ms: float = 0.0
    latency_p95_ms: float = 0.0
    error_rate: float = 0.0
    last_check: str = ""
    consecutive_failures: int = 0
    is_available: bool = True


@dataclass
class CircuitBreakerState:
    provider: str = ""
    state: str = "CLOSED"
    failure_count: int = 0
    success_count: int = 0
    last_failure: str = ""
    last_success: str = ""
    open_until: str = ""
    half_open_attempts: int = 0

    def is_open(self) -> bool:
        if self.state != "OPEN":
            return False
        if not self.open_until:
            return True
        try:
            return datetime.now(timezone.utc).isoformat() < self.open_until
        except (ValueError, TypeError):
            return True


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class ProviderRegistry:
    """Registry of all available providers with health and circuit breaker state."""

    def __init__(self) -> None:
        self._providers: dict[str, Any] = {}
        self._circuit_breakers: dict[str, CircuitBreakerState] = {}
        self._health: dict[str, ProviderHealth] = {}
        self._default_chain: list[str] = list(DEFAULT_PROVIDER_CHAIN)

    def register(self, name: str, provider_instance: Any) -> None:
        """Register a provider."""
        self._providers[name] = provider_instance
        if name not in self._circuit_breakers:
            self._circuit_breakers[name] = CircuitBreakerState(provider=name)
        if name not in self._health:
            self._health[name] = ProviderHealth(provider=name)

    def get(self, name: str) -> Any | None:
        """Get a provider by name."""
        return self._providers.get(name)

    def get_available_providers(self) -> list[str]:
        """Return list of providers that are registered and not circuit-open."""
        available: list[str] = []
        for name in self._providers:
            cb = self._circuit_breakers.get(name)
            if cb is not None and cb.is_open():
                continue
            available.append(name)
        return available

    def get_chain(self) -> list[str]:
        """Return the ordered provider chain (excluding circuit-open)."""
        chain: list[str] = []
        for name in self._default_chain:
            if name not in self._providers:
                continue
            cb = self._circuit_breakers.get(name)
            if cb is not None and cb.is_open():
                continue
            chain.append(name)
        return chain

    def record_success(self, provider: str) -> None:
        """Record a successful call."""
        cb = self._circuit_breakers.get(provider)
        if cb is not None:
            cb.state = "CLOSED"
            cb.failure_count = 0
            cb.success_count += 1
            cb.last_success = _utcnow()
            cb.open_until = ""
            cb.half_open_attempts = 0
        health = self._health.get(provider)
        if health is not None:
            health.is_available = True
            health.consecutive_failures = 0
            health.last_check = _utcnow()
            if health.status in (ProviderStatus.CIRCUIT_OPEN, ProviderStatus.CIRCUIT_HALF_OPEN):
                health.status = ProviderStatus.ENABLED

    def record_failure(self, provider: str, error_type: str) -> None:
        """Record a failed call. Opens circuit if threshold exceeded."""
        cb = self._circuit_breakers.get(provider)
        if cb is None:
            cb = CircuitBreakerState(provider=provider)
            self._circuit_breakers[provider] = cb
        cb.failure_count += 1
        cb.last_failure = _utcnow()
        if cb.failure_count >= DEFAULT_CIRCUIT_BREAKER_THRESHOLD:
            cb.state = "OPEN"
            cb.open_until = (
                datetime.now(timezone.utc) + timedelta(seconds=DEFAULT_CIRCUIT_BREAKER_RECOVERY_SECONDS)
            ).isoformat()
        health = self._health.get(provider)
        if health is not None:
            health.consecutive_failures = cb.failure_count
            health.error_rate = cb.failure_count / max(cb.failure_count + cb.success_count, 1)
            health.last_check = _utcnow()
            if cb.state == "OPEN":
                health.status = ProviderStatus.CIRCUIT_OPEN
                health.is_available = False

    def record_timeout(self, provider: str) -> None:
        """Record a timeout. Counts as a failure."""
        self.record_failure(provider, "timeout")

    def is_available(self, provider: str) -> bool:
        """Check if provider can be called."""
        if provider not in self._providers:
            return False
        cb = self._circuit_breakers.get(provider)
        if cb is not None and cb.is_open():
            return False
        health = self._health.get(provider)
        if health is not None and not health.is_available:
            return False
        return True

    def get_health(self, provider: str) -> ProviderHealth | None:
        return self._health.get(provider)

    def set_chain(self, chain: list[str]) -> None:
        """Override the default provider chain."""
        self._default_chain = list(chain)
