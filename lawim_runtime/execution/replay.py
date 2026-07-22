from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from .request import ActionExecutionRequest
from .result import ActionExecutionResult, ExecutionStatus


@dataclass
class ReplayStep:
    step_index: int = 0
    action_code: str = ""
    handler_name: str = ""
    input_snapshot: dict[str, Any] = field(default_factory=dict)
    output: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    duration_ms: float = 0.0
    error: str = ""


@dataclass
class ReplayResult:
    execution_id: str = ""
    original_status: str = ""
    replayed_status: str = ""
    steps: list[ReplayStep] = field(default_factory=list)
    match: bool = True
    divergences: list[dict[str, Any]] = field(default_factory=list)
    dry_run: bool = True
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_match(self) -> bool:
        return self.match and not self.divergences

    @property
    def step_count(self) -> int:
        return len(self.steps)


AsyncHandler = Callable[[ActionExecutionRequest], ActionExecutionResult]
SyncHandler = Callable[[ActionExecutionRequest], ActionExecutionResult]


class ExecutionReplayService:
    def __init__(self, repository: Any | None = None) -> None:
        self._repository = repository

    def replay(
        self,
        execution_id: str,
        dry_run: bool = True,
        handler: SyncHandler | None = None,
        context: dict[str, Any] | None = None,
    ) -> ReplayResult:
        result = ReplayResult(
            execution_id=execution_id,
            dry_run=dry_run,
        )

        if self._repository is None:
            result.match = False
            result.divergences.append({"error": "No repository configured"})
            result.completed_at = datetime.now(timezone.utc).isoformat()
            return result

        original = self._repository.get_execution(execution_id)
        if original is None:
            result.match = False
            result.divergences.append({"error": f"Execution {execution_id} not found"})
            result.completed_at = datetime.now(timezone.utc).isoformat()
            return result

        original_status_val = (
            original.status.value if hasattr(original.status, "value") else str(original.status)
        ) if hasattr(original, "status") else "UNKNOWN"
        result.original_status = original_status_val

        request_data = getattr(original, "request", None) or original.get("request", {})
        if isinstance(request_data, dict):
            req = ActionExecutionRequest(**request_data)
        else:
            req = request_data

        if handler is None:
            result.replayed_status = "skipped"
            result.match = False
            result.divergences.append({"error": "No handler provided for replay"})
            result.completed_at = datetime.now(timezone.utc).isoformat()
            return result

        try:
            import time
            step_start = time.perf_counter()
            replayed = handler(req)
            step_duration = (time.perf_counter() - step_start) * 1000.0

            replayed_status_val = (
                replayed.status.value if hasattr(replayed.status, "value") else str(replayed.status)
            ) if hasattr(replayed, "status") else "UNKNOWN"
            result.replayed_status = replayed_status_val

            step = ReplayStep(
                step_index=0,
                action_code=req.action_code,
                handler_name=getattr(handler, "__name__", "unknown"),
                output=getattr(replayed, "output", {}) if isinstance(getattr(replayed, "output", {}), dict) else {},
                status=replayed_status_val,
                duration_ms=round(step_duration, 2),
            )
            result.steps.append(step)

            if original_status_val != replayed_status_val and not dry_run:
                result.match = False
                result.divergences.append({
                    "field": "status",
                    "original": original_status_val,
                    "replayed": replayed_status_val,
                })

        except Exception as exc:
            result.replayed_status = "error"
            result.match = False
            result.divergences.append({"error": str(exc)})
            result.steps.append(ReplayStep(
                step_index=0,
                action_code=req.action_code,
                status="error",
                error=str(exc),
            ))

        result.completed_at = datetime.now(timezone.utc).isoformat()
        return result

    def simulate(
        self,
        execution_request: ActionExecutionRequest,
        handler: SyncHandler,
    ) -> ActionExecutionResult:
        return handler(execution_request)
