from __future__ import annotations

from ..handler import ActionHandler
from ..context import ActionExecutionContext


class NoopHandler(ActionHandler):
    handler_name = "noop"
    supported_actions = ["noop", "no_op"]
    version = "1.0.0"
    idempotent = True

    def can_handle(self, action_code: str) -> bool:
        return action_code in self.supported_actions

    def validate(self, context: ActionExecutionContext) -> list[str]:
        return []

    def prepare(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {"prepared": True}

    def execute(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {"executed": True, "action": context.request.action_code}

    def verify(self, context: ActionExecutionContext, raw_result: dict[str, Any]) -> bool:
        return raw_result.get("executed") is True

    def compensate(self, context: ActionExecutionContext, result) -> dict[str, Any]:
        return {"compensated": True}
