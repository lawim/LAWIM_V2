from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .provider_registry import ProviderRegistry


class ProviderSelectionPolicy:
    """Selects the best provider based on availability, health, and constraints."""

    def __init__(self, registry: ProviderRegistry) -> None:
        self._registry = registry

    def select(
        self,
        language: str = "fr",
        complexity: str = "simple",
        preferred_provider: str | None = None,
        exclude: list[str] | None = None,
    ) -> str | None:
        """Select the best available provider."""
        excluded = set(exclude or [])

        if preferred_provider and preferred_provider not in excluded:
            if self._registry.is_available(preferred_provider):
                return preferred_provider

        chain = self._registry.get_chain()
        for name in chain:
            if name in excluded:
                continue
            if self._registry.is_available(name):
                return name

        for name in self._registry.get_available_providers():
            if name in excluded or name in chain:
                continue
            if self._registry.is_available(name):
                return name

        return None

    def select_chain(
        self,
        language: str = "fr",
        complexity: str = "simple",
    ) -> list[str]:
        """Return the ordered provider chain to try."""
        return self._registry.get_chain()
