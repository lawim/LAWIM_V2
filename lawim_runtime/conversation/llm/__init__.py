from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LLMContract:
    intent: str = ""
    confidence: float = 0.0
    entities: dict[str, Any] = field(default_factory=dict)
    missing_information: list[str] = field(default_factory=list)
    summary: str = ""
    needs_clarification: bool = False
    raw_response: str = ""


class LLMAdapter(ABC):

    @abstractmethod
    def analyze(self, text: str, context: dict[str, Any] | None = None) -> LLMContract:
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...


class DeterministicLLMAdapter(LLMAdapter):
    provider_name = "deterministic"

    def analyze(self, text: str, context: dict[str, Any] | None = None) -> LLMContract:
        from ..intent import IntentEngine
        intent_result = IntentEngine().detect(text)
        from ..entity import EntityExtractionEngine
        entity_result = EntityExtractionEngine().extract(text)
        return LLMContract(
            intent=intent_result.intent,
            confidence=intent_result.confidence,
            entities=entity_result.entities,
            missing_information=entity_result.missing,
            summary=text[:100],
            needs_clarification=intent_result.confidence < 0.5,
        )
