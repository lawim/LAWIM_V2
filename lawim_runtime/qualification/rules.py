from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RuleEffect(str, Enum):
    ADD_SCORE = "ADD_SCORE"
    REMOVE_SCORE = "REMOVE_SCORE"
    CAP_SCORE = "CAP_SCORE"
    MARK_READY = "MARK_READY"
    MARK_NOT_READY = "MARK_NOT_READY"
    ADD_BLOCKER = "ADD_BLOCKER"
    ADD_WARNING = "ADD_WARNING"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"
    REQUIRE_HUMAN_REVIEW = "REQUIRE_HUMAN_REVIEW"
    ADD_MISSING_REQUIREMENT = "ADD_MISSING_REQUIREMENT"


@dataclass(frozen=True)
class QualificationRule:
    rule_id: str = ""
    name: str = ""
    profile_types: tuple[str, ...] = ()
    stages: tuple[str, ...] = ()
    priority: int = 100
    condition_field: str = ""
    effect: RuleEffect = RuleEffect.ADD_SCORE
    effect_value: float = 0.0
    blocking: bool = False
    severity: str = "WARNING"
    version: int = 1
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
