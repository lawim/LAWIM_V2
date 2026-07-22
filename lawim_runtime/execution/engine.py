from __future__ import annotations

from typing import Any

from .dispatcher import ExecutionDispatcher
from .handler import ActionHandler
from .idempotency import IdempotencyManager
from .locking.locks import ActionLockManager
from .locking.leases import ActionLeaseManager
from .metrics import MetricsCollector
from .plan import ActionExecutionPlan
from .registry import ActionHandlerRegistry
from .request import ActionExecutionRequest
from .result import ActionExecutionResult, ExecutionStatus
from .state import ExecutionState, ActionExecutionStateMachine
from .verification import ExecutionVerifier
from .audit import AuditTrail, AuditEntry
from .events import EventCollector, ExecutionEvent, ExecutionEventType
from .worker import ExecutionWorker


class ExecutionEngine:
    def __init__(
        self,
        worker: ExecutionWorker | None = None,
        dispatcher: ExecutionDispatcher | None = None,
        registry: ActionHandlerRegistry | None = None,
        idempotency: IdempotencyManager | None = None,
        lock_manager: ActionLockManager | None = None,
        lease_manager: ActionLeaseManager | None = None,
        verifier: ExecutionVerifier | None = None,
        metrics: MetricsCollector | None = None,
        audit: AuditTrail | None = None,
        events: EventCollector | None = None,
        shadow_mode: bool = True,
        enabled: bool = False,
    ) -> None:
        self._worker = worker or ExecutionWorker(dispatcher=dispatcher)
        self._dispatcher = dispatcher or ExecutionDispatcher()
        self._registry = registry or ActionHandlerRegistry()
        self._idempotency = idempotency or IdempotencyManager()
        self._lock_manager = lock_manager or ActionLockManager()
        self._lease_manager = lease_manager or ActionLeaseManager()
        self._verifier = verifier or ExecutionVerifier()
        self._metrics = metrics or MetricsCollector()
        self._audit = audit or AuditTrail()
        self._events = events or EventCollector()
        self._shadow_mode = shadow_mode
        self._enabled = enabled

    @property
    def shadow_mode(self) -> bool:
        return self._shadow_mode

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def metrics(self) -> MetricsCollector:
        return self._metrics

    @property
    def audit(self) -> AuditTrail:
        return self._audit

    @property
    def events(self) -> EventCollector:
        return self._events

    @property
    def registry(self) -> ActionHandlerRegistry:
        return self._registry

    @property
    def worker(self) -> ExecutionWorker:
        return self._worker

    def execute(
        self,
        request: ActionExecutionRequest,
        services: dict[str, Any] | None = None,
    ) -> ActionExecutionResult:
        if not self._enabled:
            return ActionExecutionResult(
                request_id=request.execution_request_id,
                action_code=request.action_code,
                status=ExecutionStatus.SUCCEEDED,
                output={"mode": "disabled", "message": "Execution engine is disabled"},
            )

        self._metrics.record_started()
        action_code = request.action_code
        handler = self._registry.resolve_handler(action_code)

        if self._shadow_mode:
            result = ActionExecutionResult(
                request_id=request.execution_request_id,
                action_code=action_code,
                status=ExecutionStatus.SUCCEEDED,
                output={
                    "mode": "shadow",
                    "handler": handler.handler_name,
                    "message": "Shadow mode — no real execution performed",
                },
            )
            result.metadata["shadow_mode"] = True
            self._metrics.record_succeeded()
            self._events.record(ExecutionEvent(
                event_id="shadow-" + request.execution_request_id,
                event_type=ExecutionEventType.EXECUTION_COMPLETED,
                execution_id=request.execution_request_id,
                data={"mode": "shadow", "action_code": action_code},
            ))
            return result

        result = self._worker.execute(request, self._registry, services)
        if result.status.is_success:
            self._metrics.record_succeeded()
        else:
            self._metrics.record_failed()

        self._audit.record(AuditEntry(
            entry_id="audit-" + request.execution_request_id,
            execution_id=request.execution_request_id,
            action=action_code,
            actor=request.requested_by,
            new_state=result.status.value,
        ))
        return result
