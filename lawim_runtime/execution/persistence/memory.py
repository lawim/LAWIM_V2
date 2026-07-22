from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..result import ActionExecutionResult, ExecutionStatus
from ..state import ExecutionState
from .repository import ExecutionRepository


class InMemoryExecutionRepository(ExecutionRepository):
    def __init__(self) -> None:
        self._store: dict[str, ActionExecutionResult] = {}

    def save(self, execution: ActionExecutionResult) -> None:
        self._store[execution.execution_id] = execution

    def get_execution(self, execution_id: str) -> ActionExecutionResult | None:
        return self._store.get(execution_id)

    def update_status(self, execution_id: str, status: ExecutionState | ExecutionStatus) -> None:
        execution = self._store.get(execution_id)
        if execution is None:
            return
        status_value = status.value if isinstance(status, (ExecutionState, ExecutionStatus)) else str(status)
        execution.status = ExecutionStatus(status_value)

    def list_executions(
        self,
        status: ExecutionState | ExecutionStatus | None = None,
        limit: int = 100,
    ) -> list[ActionExecutionResult]:
        if status is None:
            return list(self._store.values())[:limit]
        status_value = status.value if isinstance(status, (ExecutionState, ExecutionStatus)) else str(status)
        return [
            e for e in self._store.values()
            if e.status.value == status_value
        ][:limit]

    def delete(self, execution_id: str) -> bool:
        return self._store.pop(execution_id, None) is not None

    def count(self) -> int:
        return len(self._store)
