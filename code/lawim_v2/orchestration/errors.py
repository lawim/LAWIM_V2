from __future__ import annotations


class OrchestrationError(Exception):
    """Base error for orchestration failures."""


class AllProvidersFailedError(OrchestrationError):
    """All providers in the chain failed."""


class CircuitBreakerOpenError(OrchestrationError):
    """Circuit breaker is open for this provider."""


class ProviderTimeoutError(OrchestrationError):
    """Provider timed out."""


class InvalidProviderResponseError(OrchestrationError):
    """Provider returned an invalid response."""
