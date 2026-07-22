from __future__ import annotations

from abc import ABC
from typing import Any

from lawim_runtime.execution.handler import ActionHandler, ActionExecutionContext, ActionExecutionResult


class DomainRuntimeHandler(ActionHandler, ABC):
    runtime_name: str = ""
    domain_action_codes: list[str] = []

    def can_handle(self, action_code: str) -> bool:
        return action_code in self.domain_action_codes or action_code in self.supported_actions

    def validate(self, context: ActionExecutionContext) -> list[str]:
        return []

    def prepare(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {}

    def execute(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {}

    def verify(self, context: ActionExecutionContext, raw_result: dict[str, Any]) -> bool:
        return True

    def compensate(self, context: ActionExecutionContext, result: ActionExecutionResult) -> dict[str, Any]:
        return {}
