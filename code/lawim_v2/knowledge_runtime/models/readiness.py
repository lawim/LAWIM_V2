from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ReadinessLevel(str, Enum):
    INTENT_IDENTIFIED = "INTENT_IDENTIFIED"
    MINIMUM_INTAKE_READY = "MINIMUM_INTAKE_READY"
    MINIMUM_SEARCH_READY = "MINIMUM_SEARCH_READY"
    MINIMUM_MATCHING_READY = "MINIMUM_MATCHING_READY"
    INTRODUCTION_READY = "INTRODUCTION_READY"
    VISIT_READY = "VISIT_READY"
    TRANSACTION_READY = "TRANSACTION_READY"


@dataclass(frozen=True, slots=True)
class ReadinessDefinition:
    level: ReadinessLevel
    order: int
    description: str
    required_fields: tuple[str, ...] = ()
    conditional_requirements: tuple[dict, ...] = ()
    blocking_conditions: tuple[str, ...] = ()
    non_blocking_missing_fields: tuple[str, ...] = ()
    allowed_actions: tuple[str, ...] = ()
    forbidden_actions: tuple[str, ...] = ()
    threshold_score: str = ""
    max_exchanges: int = 0
