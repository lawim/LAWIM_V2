from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from ..envelope import InteractionEnvelope
from ..session import InteractionSession
from ..delivery import DeliveryResult


class InteractionRepository(ABC):

    @abstractmethod
    def save_envelope(self, envelope: InteractionEnvelope) -> None:
        ...

    @abstractmethod
    def get_envelope(self, interaction_id: str) -> InteractionEnvelope | None:
        ...


class InMemoryInteractionRepository(InteractionRepository):
    def __init__(self) -> None:
        self._envelopes: dict[str, InteractionEnvelope] = {}

    def save_envelope(self, envelope: InteractionEnvelope) -> None:
        self._envelopes[envelope.interaction_id] = envelope

    def get_envelope(self, interaction_id: str) -> InteractionEnvelope | None:
        return self._envelopes.get(interaction_id)
