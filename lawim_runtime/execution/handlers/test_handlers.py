from __future__ import annotations

from typing import Any

from ..handler import ActionHandler
from ..context import ActionExecutionContext


class SuccessHandler(ActionHandler):
    handler_name = "success"
    supported_actions = ["test_success"]
    version = "1.0.0"
    idempotent = True

    def can_handle(self, action_code: str) -> bool:
        return action_code in self.supported_actions

    def validate(self, context: ActionExecutionContext) -> list[str]:
        return []

    def prepare(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {}

    def execute(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {"status": "ok"}

    def verify(self, context: ActionExecutionContext, raw_result: dict[str, Any]) -> bool:
        return raw_result.get("status") == "ok"

    def compensate(self, context: ActionExecutionContext, result) -> dict[str, Any]:
        return {}


class FailHandler(ActionHandler):
    handler_name = "fail"
    supported_actions = ["test_fail"]
    version = "1.0.0"

    def can_handle(self, action_code: str) -> bool:
        return action_code in self.supported_actions

    def validate(self, context: ActionExecutionContext) -> list[str]:
        return []

    def prepare(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {}

    def execute(self, context: ActionExecutionContext) -> dict[str, Any]:
        raise RuntimeError("Intentional failure for testing")

    def verify(self, context: ActionExecutionContext, raw_result: dict[str, Any]) -> bool:
        return True

    def compensate(self, context: ActionExecutionContext, result) -> dict[str, Any]:
        return {"compensated": True}


class ValidationFailHandler(ActionHandler):
    handler_name = "validation_fail"
    supported_actions = ["test_validation_fail"]
    version = "1.0.0"

    def can_handle(self, action_code: str) -> bool:
        return action_code in self.supported_actions

    def validate(self, context: ActionExecutionContext) -> list[str]:
        return ["Validation failed for testing"]

    def prepare(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {}

    def execute(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {}

    def verify(self, context: ActionExecutionContext, raw_result: dict[str, Any]) -> bool:
        return True

    def compensate(self, context: ActionExecutionContext, result) -> dict[str, Any]:
        return {}
