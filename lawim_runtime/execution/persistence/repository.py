from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from ..result import ActionExecutionResult, ExecutionStatus
from ..state import ExecutionState


class ExecutionRepository(ABC):
    @abstractmethod
    def save(self, execution: ActionExecutionResult) -> None:
        ...

    @abstractmethod
    def get_execution(self, execution_id: str) -> ActionExecutionResult | None:
        ...

    @abstractmethod
    def update_status(self, execution_id: str, status: ExecutionState | ExecutionStatus) -> None:
        ...

    @abstractmethod
    def list_executions(
        self,
        status: ExecutionState | ExecutionStatus | None = None,
        limit: int = 100,
    ) -> list[ActionExecutionResult]:
        ...

    @abstractmethod
    def delete(self, execution_id: str) -> bool:
        ...

    @abstractmethod
    def count(self) -> int:
        ...


@dataclass
class ExecutionRecord:
    execution_id: str
    request_id: str
    action_code: str
    status: str
    created_at: str
    updated_at: str
    data: dict[str, Any] = field(default_factory=dict)
