from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .base import AIProvider, AIProviderRequest, AIProviderResponse, AIModelCapabilities, ModelCapability

logger = logging.getLogger(__name__)


class RetryPolicy(str, Enum):
    NO_RETRY = "no_retry"
    NETWORK_ONLY = "network_only"
    RATE_LIMIT_BACKOFF = "rate_limit_backoff"
    ALL_ERRORS = "all_errors"


@dataclass
class ProviderPolicy:
    primary_provider: str = ""
    fallback_provider: str = ""
    allowed_models: tuple[str, ...] = ()
    max_latency_ms: int = 30000
    max_tokens: int = 2048
    max_cost_class: str = "medium"
    required_capabilities: tuple[ModelCapability, ...] = ()
    data_classification: str = "internal"
    retry_policy: RetryPolicy = RetryPolicy.NETWORK_ONLY
    max_retries: int = 2
    timeout_ms: int = 30000


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, AIProvider] = {}

    def register(self, name: str, provider: AIProvider) -> None:
        self._providers[name] = provider
        logger.info("provider registered: %s (%s)", name, provider.provider_name)

    def get(self, name: str) -> AIProvider | None:
        return self._providers.get(name)

    def list(self) -> list[str]:
        return list(self._providers.keys())

    def resolve(self, policy: ProviderPolicy) -> AIProvider | None:
        if policy.primary_provider and policy.primary_provider in self._providers:
            provider = self._providers[policy.primary_provider]
            if self._check_capabilities(provider.capabilities, policy.required_capabilities):
                return provider
        return None

    def resolve_fallback(self, policy: ProviderPolicy) -> AIProvider | None:
        if policy.fallback_provider and policy.fallback_provider in self._providers:
            return self._providers[policy.fallback_provider]
        return None

    def _check_capabilities(
        self,
        capabilities: AIModelCapabilities,
        required: tuple[ModelCapability, ...],
    ) -> bool:
        return all(cap in capabilities.capabilities for cap in required)

    def count(self) -> int:
        return len(self._providers)


class ModelRouter:
    def __init__(self, registry: ProviderRegistry) -> None:
        self._registry = registry

    def route(self, task_type: str, language: str = "fr", required_capabilities: tuple[ModelCapability, ...] = ()) -> str | None:
        providers = self._registry.list()
        for name in providers:
            provider = self._registry.get(name)
            if provider and self._registry._check_capabilities(provider.capabilities, required_capabilities):
                return name
        return None
