from __future__ import annotations

from typing import Protocol


class LLMProvider(Protocol):
    name: str

    def is_available(self) -> bool: ...

    def complete(self, *, system_prompt: str, user_message: str, context: dict[str, object]) -> str | None: ...


class DeterministicLLMProvider:
    name = "deterministic"

    def is_available(self) -> bool:
        return True

    def complete(self, *, system_prompt: str, user_message: str, context: dict[str, object]) -> str | None:
        return None


class OptionalLLMProvider:
    """Optional external LLM hook — disabled unless LAWIM_LLM_ENABLED=true."""

    name = "optional_llm"

    def __init__(self, enabled: bool = False) -> None:
        self.enabled = enabled

    def is_available(self) -> bool:
        return self.enabled

    def complete(self, *, system_prompt: str, user_message: str, context: dict[str, object]) -> str | None:
        return None


def resolve_llm_provider(*, enabled: bool = False) -> LLMProvider:
    if enabled:
        return OptionalLLMProvider(enabled=True)
    return DeterministicLLMProvider()
