from __future__ import annotations

from typing import Any

from lawim_runtime.domains.base.handler import DomainRuntimeHandler
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus
from lawim_runtime.execution.context import ActionExecutionContext

from .runtime import VisitRuntime


class VisitHandler(DomainRuntimeHandler):
    handler_name: str = "visit_handler"
    supported_actions: list[str] = [
        "REQUEST_VISIT_AVAILABILITY",
        "CREATE_VISIT_REQUEST",
        "SCHEDULE_VISIT",
        "CANCEL_VISIT",
    ]

    def __init__(self, runtime: VisitRuntime | None = None) -> None:
        self._runtime = runtime or VisitRuntime()

    def can_handle(self, action_code: str) -> bool:
        return action_code in self.supported_actions

    def validate(self, context: ActionExecutionContext) -> list[str]:
        action_code = context.request.action_code
        if action_code not in self.supported_actions:
            return [f"action_code '{action_code}' not supported by visit handler"]
        domain_request = DomainRuntimeRequest(
            request_id=context.request.request_id,
            action_code=action_code,
            parameters=context.request.parameters,
            correlation_id=context.correlation_id,
        )
        return self._runtime.validate(domain_request)

    def prepare(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {}

    def execute(self, context: ActionExecutionContext) -> dict[str, Any]:
        action_code = context.request.action_code
        domain_request = DomainRuntimeRequest(
            request_id=context.request.request_id,
            action_code=action_code,
            parameters=context.request.parameters,
            correlation_id=context.correlation_id,
        )
        domain_context = self._runtime._build_context(domain_request)
        errors = self._runtime.validate(domain_request)
        if errors:
            return {
                "status": DomainRuntimeStatus.FAILED.value,
                "error": "; ".join(errors),
            }
        return self._runtime.execute_op(domain_request, domain_context)

    def verify(self, context: ActionExecutionContext, raw_result: dict[str, Any]) -> bool:
        return self._runtime.verify(
            DomainRuntimeRequest(
                action_code=context.request.action_code,
                parameters=context.request.parameters,
            ),
            raw_result,
        )

    def compensate(self, context: ActionExecutionContext, result: Any) -> dict[str, Any]:
        return {}
