from __future__ import annotations

from typing import Any

from ..request import ActionExecutionRequest


class WorkflowAdapter:
    def to_execution_request(
        self,
        workflow_id: str,
        task_id: str,
        action_code: str,
        parameters: dict[str, Any] | None = None,
    ) -> ActionExecutionRequest:
        return ActionExecutionRequest(
            decision_id=workflow_id,
            project_id=task_id,
            action_code=action_code,
            action_parameters=parameters or {},
        )
