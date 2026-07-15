from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProgramJConfig:
    unified_conversation_enabled: bool = False
    actor_registry_enabled: bool = False
    exchange_taxonomy_enabled: bool = False
