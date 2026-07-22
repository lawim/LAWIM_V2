from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

from ..runtime.errors import RuntimeError
from .context import ActionExecutionContext
from .handler import ActionHandler
from .plan import ActionExecutionPlan
from .request import ActionExecutionRequest
from .result import ActionExecutionResult, ExecutionStatus


class DispatcherError(RuntimeError):
    pass


class ExecutionDispatcher:
    def __init__(self) -> None:
        self._dispatch_count: int = 0

    @property
    def dispatch_count(self) -> int:
        return self._dispatch_count

    def dispatch(
        self,
        execution_request: ActionExecutionRequest,
        handler: ActionHandler,
        plan: ActionExecutionPlan,
        services: dict[str, Any] | None = None,
    ) -> ActionExecutionResult:
        self._dispatch_count += 1
        result = ActionExecutionResult(
            request_id=execution_request.execution_request_id,
            action_code=execution_request.action_code,
        )
        result.mark_started()

        context = ActionExecutionContext(
            request=execution_request,
            handler_name=handler.handler_name,
            services=services or {},
            attempt_number=result.attempts,
        )
        context.record_event("dispatch.start", {"handler": handler.handler_name})

        errors = handler.validate(context)
        if errors:
            result.mark_failed("; ".join(errors), "VALIDATION")
            context.record_event("dispatch.validation_failed", {"errors": errors})
            return result

        try:
            prepared = handler.prepare(context)
            context.record_event("dispatch.prepared", {"prepared_keys": list(prepared.keys())})

            raw_result = handler.execute(context)
            context.record_event("dispatch.executed")

            verified = handler.verify(context, raw_result)
            context.record_event("dispatch.verified", {"verified": verified})

            result.verification_passed = verified
            result.mark_completed(raw_result)

            if not verified and handler.supports_compensation:
                result.compensation_required = True
                compensation = handler.compensate(context, result)
                result.compensation_result = compensation
                result.status = ExecutionStatus.COMPENSATED
                context.record_event("dispatch.compensated")

        except Exception as exc:
            error_msg = f"{type(exc).__name__}: {exc}"
            result.mark_failed(error_msg)
            context.record_event("dispatch.failed", {"error": error_msg})

            if handler.supports_compensation and handler.can_handle(execution_request.action_code):
                try:
                    compensation = handler.compensate(context, result)
                    result.compensation_result = compensation
                    result.compensation_required = True
                    result.status = ExecutionStatus.COMPENSATED
                    context.record_event("dispatch.compensated_after_failure")
                except Exception as comp_exc:
                    context.record_event("dispatch.compensation_failed", {
                        "error": f"{type(comp_exc).__name__}: {comp_exc}",
                    })

        result.metadata["dispatch_count"] = self._dispatch_count
        return result
