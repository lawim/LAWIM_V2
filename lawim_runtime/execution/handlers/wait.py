from __future__ import annotations

from typing import Any

from ..handler import ActionHandler
from ..context import ActionExecutionContext


class WaitHandler(ActionHandler):
    handler_name = "wait"
    supported_actions = ["wait", "delay"]
    version = "1.0.0"

    def can_handle(self, action_code: str) -> bool:
        return action_code in self.supported_actions

    def validate(self, context: ActionExecutionContext) -> list[str]:
        params = context.request.action_parameters
        if "duration" not in params:
            return ["Missing 'duration' parameter"]
        return []

    def prepare(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {"prepared": True, "duration": context.request.action_parameters.get("duration", 0)}

    def execute(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {"waited": True, "duration": context.request.action_parameters.get("duration", 1.0)}

    def verify(self, context: ActionExecutionContext, raw_result: dict[str, Any]) -> bool:
        return True

    def compensate(self, context: ActionExecutionContext, result) -> dict[str, Any]:
        return {"compensated": True}
