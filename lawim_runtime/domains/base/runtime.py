from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable

from .context import DomainRuntimeContext
from .errors import DomainValidationError
from .events import DomainEvent
from .request import DomainRuntimeRequest
from .result import DomainRuntimeResult, DomainRuntimeStatus

EventPublisher = Callable[[DomainEvent], None]


class DomainRuntime(ABC):
    runtime_name: str = ""
    supported_actions: list[str] = []
    version: str = "1.0.0"

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not cls.runtime_name:
            cls.runtime_name = cls.__name__

    def set_event_publisher(self, publisher: EventPublisher) -> None:
        self._event_publisher = publisher

    def _publish_event(self, event: DomainEvent) -> None:
        publisher = getattr(self, '_event_publisher', None)
        if publisher:
            publisher(event)

    def execute(self, request: DomainRuntimeRequest) -> DomainRuntimeResult:
        context = self._build_context(request)
        errors = self.validate(request)
        if errors:
            result = DomainRuntimeResult(
                request_id=request.request_id,
                action_code=request.action_code,
                status=DomainRuntimeStatus.FAILED,
                error="; ".join(errors),
            )
            self._publish_event(self._build_event("FAILED", request, errors=errors))
            return result
        try:
            output = self.execute_op(request, context)
            verified = self.verify(request, output)
            status = DomainRuntimeStatus.SUCCEEDED if verified else DomainRuntimeStatus.FAILED
            result = DomainRuntimeResult(
                request_id=request.request_id,
                action_code=request.action_code,
                status=status,
                output=output,
            )
            self._publish_event(self._build_event(status.value, request, output=output))
            return result
        except DomainValidationError as e:
            result = DomainRuntimeResult(
                request_id=request.request_id,
                action_code=request.action_code,
                status=DomainRuntimeStatus.FAILED,
                error=str(e),
            )
            self._publish_event(self._build_event("FAILED", request, error=str(e)))
            return result

    def _build_event(self, status: str, request: DomainRuntimeRequest, output: dict[str, Any] | None = None, errors: list[str] | None = None, error: str = "") -> DomainEvent:
        from .events import DomainEvent
        return DomainEvent(
            event_type=f"{self.runtime_name.upper()}_{status}",
            runtime_name=self.runtime_name,
            action_code=request.action_code,
            data={
                "request_id": request.request_id,
                "correlation_id": request.correlation_id,
                "output": output or {},
                "errors": errors or [],
                "error": error,
            },
            correlation_id=request.correlation_id,
        )

    def _build_context(self, request: DomainRuntimeRequest) -> DomainRuntimeContext:
        return DomainRuntimeContext(
            request=request,
            runtime_name=self.runtime_name,
        )

    def validate(self, request: DomainRuntimeRequest) -> list[str]:
        errors: list[str] = []
        if request.action_code and request.action_code not in self.supported_actions:
            errors.append(f"action_code '{request.action_code}' not supported by {self.runtime_name}")
        return errors

    @abstractmethod
    def execute_op(self, request: DomainRuntimeRequest, context: DomainRuntimeContext) -> dict[str, Any]:
        ...

    def verify(self, request: DomainRuntimeRequest, output: dict[str, Any]) -> bool:
        return True
