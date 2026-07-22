from __future__ import annotations
from typing import Any
from .requirements import Condition, ConditionGroup, ConditionOperator, RequirementDefinition
from ..project_profile.base import AbstractProjectProfile
from ..runtime.errors import RuntimeError


class RequirementRegistryError(RuntimeError):
    pass


class RequirementRegistry:
    def __init__(self) -> None:
        self._requirements: dict[str, RequirementDefinition] = {}

    def register(self, req: RequirementDefinition) -> None:
        self._requirements[req.requirement_id] = req

    def get(self, requirement_id: str) -> RequirementDefinition:
        if requirement_id not in self._requirements:
            raise RequirementRegistryError(f"Requirement '{requirement_id}' not found")
        return self._requirements[requirement_id]

    def list_all(self) -> list[RequirementDefinition]:
        return list(self._requirements.values())

    def list_for_profile(self, profile_type: str) -> list[RequirementDefinition]:
        return [r for r in self._requirements.values() if not r.profile_types or profile_type in r.profile_types]

    def list_for_stage(self, stage: str) -> list[RequirementDefinition]:
        return [r for r in self._requirements.values() if not r.required_for_stages or stage in r.required_for_stages]

    def list_for_action(self, action: str) -> list[RequirementDefinition]:
        return [r for r in self._requirements.values() if not r.required_for_actions or action in r.required_for_actions]

    def evaluate_condition(self, condition: ConditionGroup, profile: AbstractProjectProfile) -> bool:
        def _check(c: Condition) -> bool:
            fv = profile.get_field(c.field)
            val = fv.value if fv else None
            if c.operator == ConditionOperator.EQ:
                return val == c.value
            if c.operator == ConditionOperator.NE:
                return val != c.value
            if c.operator == ConditionOperator.IN:
                return val in (c.value or [])
            if c.operator == ConditionOperator.NOT_IN:
                return val not in (c.value or [])
            if c.operator == ConditionOperator.EXISTS:
                return fv is not None
            if c.operator == ConditionOperator.NOT_EXISTS:
                return fv is None
            if c.operator == ConditionOperator.GT:
                return (val or 0) > (c.value or 0)
            if c.operator == ConditionOperator.GTE:
                return (val or 0) >= (c.value or 0)
            if c.operator == ConditionOperator.LT:
                return (val or 0) < (c.value or 0)
            if c.operator == ConditionOperator.LTE:
                return (val or 0) <= (c.value or 0)
            if c.operator == ConditionOperator.CONTAINS:
                if isinstance(val, list):
                    return c.value in val
                if isinstance(val, str):
                    return c.value in val
                return False
            return False

        if condition.all:
            return all(_check(c) for c in condition.all)
        if condition.any:
            return any(_check(c) for c in condition.any)
        return True
