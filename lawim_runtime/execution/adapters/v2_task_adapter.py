from __future__ import annotations

from typing import Any

from ..request import ActionExecutionRequest


class V2TaskAdapter:
    def to_execution_request(
        self,
        task_type: str,
        task_data: dict[str, Any],
        task_id: str = "",
    ) -> ActionExecutionRequest:
        return ActionExecutionRequest(
            decision_id=task_id or task_data.get("decision_id", ""),
            project_id=task_data.get("project_id", ""),
            action_code=task_type,
            action_parameters=task_data,
            correlation_id=task_data.get("correlation_id", ""),
        )
