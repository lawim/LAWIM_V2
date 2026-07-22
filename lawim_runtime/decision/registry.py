from __future__ import annotations
from typing import Any
from .actions import ActionCategory, ActionDefinition
from ..runtime.errors import RuntimeError


class ActionRegistryError(RuntimeError):
    pass


class ActionNotFoundError(ActionRegistryError):
    pass


class ActionAlreadyRegisteredError(ActionRegistryError):
    pass


class ActionRegistry:
    def __init__(self) -> None:
        self._actions: dict[str, ActionDefinition] = {}

    def register(self, action: ActionDefinition) -> None:
        if not action.action_code:
            raise ActionRegistryError("action_code is required")
        if action.action_code in self._actions:
            raise ActionAlreadyRegisteredError(
                f"Action '{action.action_code}' already registered"
            )
        self._actions[action.action_code] = action

    def get(self, action_code: str) -> ActionDefinition:
        action = self._actions.get(action_code)
        if action is None:
            raise ActionNotFoundError(f"Action '{action_code}' not found")
        return action

    def has(self, action_code: str) -> bool:
        return action_code in self._actions

    def list(self) -> list[ActionDefinition]:
        return sorted(self._actions.values(), key=lambda a: a.priority)

    def list_by_category(self, category: ActionCategory) -> list[ActionDefinition]:
        return sorted(
            (a for a in self._actions.values() if a.category == category),
            key=lambda a: a.priority,
        )

    def list_by_profile(self, profile_type: str) -> list[ActionDefinition]:
        return sorted(
            (
                a
                for a in self._actions.values()
                if not a.allowed_profile_types or profile_type in a.allowed_profile_types
            ),
            key=lambda a: a.priority,
        )

    def list_by_stage(self, stage: str) -> list[ActionDefinition]:
        return sorted(
            (
                a
                for a in self._actions.values()
                if not a.allowed_stages or stage in a.allowed_stages
            ),
            key=lambda a: a.priority,
        )

    def count(self) -> int:
        return len(self._actions)

    def register_defaults(self, actions: list[ActionDefinition]) -> None:
        for action in actions:
            try:
                self.register(action)
            except ActionAlreadyRegisteredError:
                pass
