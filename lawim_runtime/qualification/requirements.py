from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RequirementType(str, Enum):
    MANDATORY = "MANDATORY"
    IMPORTANT = "IMPORTANT"
    OPTIONAL = "OPTIONAL"
    CONDITIONAL = "CONDITIONAL"
    BLOCKING = "BLOCKING"
    CONFIRMATION_REQUIRED = "CONFIRMATION_REQUIRED"
    ACTION_SPECIFIC = "ACTION_SPECIFIC"
    STAGE_SPECIFIC = "STAGE_SPECIFIC"


class ConditionOperator(str, Enum):
    EQ = "EQ"
    NE = "NE"
    IN = "IN"
    NOT_IN = "NOT_IN"
    EXISTS = "EXISTS"
    NOT_EXISTS = "NOT_EXISTS"
    GT = "GT"
    GTE = "GTE"
    LT = "LT"
    LTE = "LTE"
    CONTAINS = "CONTAINS"


@dataclass(frozen=True)
class Condition:
    field: str = ""
    operator: ConditionOperator = ConditionOperator.EQ
    value: Any = None


@dataclass(frozen=True)
class ConditionGroup:
    all: tuple[Condition, ...] = ()
    any: tuple[Condition, ...] = ()


@dataclass(frozen=True)
class RequirementDefinition:
    requirement_id: str = ""
    profile_types: tuple[str, ...] = ()
    field_name: str = ""
    requirement_type: RequirementType = RequirementType.MANDATORY
    required_for_stages: tuple[str, ...] = ()
    required_for_actions: tuple[str, ...] = ()
    weight: float = 1.0
    priority: int = 100
    minimum_confidence: float = 0.0
    accepted_validation_statuses: tuple[str, ...] = ("VALID",)
    allow_conflict: bool = False
    blocking: bool = False
    condition: ConditionGroup | None = None
    dependencies: tuple[str, ...] = ()
    description: str = ""
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)
