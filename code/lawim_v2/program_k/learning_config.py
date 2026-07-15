from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LearningConfig:
    learning_events_enabled: bool = False
    outcome_registry_enabled: bool = False
    feedback_engine_enabled: bool = False
