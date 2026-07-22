from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

from ..runtime.errors import RuntimeError
from .dispatcher import ExecutionDispatcher
from .handler import ActionHandler
from .plan import ActionExecutionPlan
from .registry import ActionHandlerRegistry
from .request import ActionExecutionRequest
from .result import ActionExecutionResult, ExecutionStatus


class WorkerError(RuntimeError):
    pass


class ExecutionWorker:
    def __init__(
        self,
        name: str = "default",
        dispatcher: ExecutionDispatcher | None = None,
    ) -> None:
        self._name = name
        self._dispatcher = dispatcher or ExecutionDispatcher()
        self._running: bool = False
        self._shutdown_requested: bool = False
        self._execution_count: int = 0
        self._last_heartbeat: datetime | None = None
        self._heartbeat_interval: float = 5.0

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def execution_count(self) -> int:
        return self._execution_count

    @property
    def last_heartbeat(self) -> datetime | None:
        return self._last_heartbeat

    @property
    def shutdown_requested(self) -> bool:
        return self._shutdown_requested

    def start(self) -> None:
        self._running = True
        self._shutdown_requested = False
        self._last_heartbeat = datetime.now(timezone.utc)

    def shutdown(self) -> None:
        self._shutdown_requested = True
        self._running = False

    def heartbeat(self) -> datetime:
        self._last_heartbeat = datetime.now(timezone.utc)
        return self._last_heartbeat

    def execute(
        self,
        execution_request: ActionExecutionRequest,
        handler_registry: ActionHandlerRegistry,
        services: dict[str, Any] | None = None,
    ) -> ActionExecutionResult:
        if self._shutdown_requested:
            raise WorkerError("Worker has been shut down, cannot execute")

        self._running = True
        self._execution_count += 1
        self.heartbeat()

        try:
            handler = handler_registry.resolve_handler(execution_request.action_code)
            plan = ActionExecutionPlan(
                plan_id=f"plan-{execution_request.execution_request_id}",
                execution_request_id=execution_request.execution_request_id,
                action_code=execution_request.action_code,
            )

            result = self._dispatcher.dispatch(
                execution_request, handler, plan, services
            )
        finally:
            self._running = False
            self.heartbeat()

        return result

    def status(self) -> dict[str, Any]:
        return {
            "name": self._name,
            "running": self._running,
            "shutdown_requested": self._shutdown_requested,
            "execution_count": self._execution_count,
            "last_heartbeat": self._last_heartbeat.isoformat() if self._last_heartbeat else None,
            "heartbeat_interval": self._heartbeat_interval,
        }
