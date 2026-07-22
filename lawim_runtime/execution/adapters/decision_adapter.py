from __future__ import annotations

from typing import Any

from ..request import ActionExecutionRequest


class DecisionAdapter:
    def to_execution_request(
        self,
        decision_id: str,
        project_id: str,
        action_code: str,
        parameters: dict[str, Any] | None = None,
        priority: int = 100,
    ) -> ActionExecutionRequest:
        return ActionExecutionRequest(
            decision_id=decision_id,
            project_id=project_id,
            action_code=action_code,
            action_parameters=parameters or {},
            priority=priority,
        )

    def from_execution_request(self, request: ActionExecutionRequest) -> dict[str, Any]:
        return {
            "decision_id": request.decision_id,
            "project_id": request.project_id,
            "action_code": request.action_code,
            "parameters": request.action_parameters,
        }
