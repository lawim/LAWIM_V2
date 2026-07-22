from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .context import DomainRuntimeContext
from .errors import DomainValidationError
from .request import DomainRuntimeRequest
from .result import DomainRuntimeResult, DomainRuntimeStatus


class DomainRuntime(ABC):
    runtime_name: str = ""
    supported_actions: list[str] = []
    version: str = "1.0.0"

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not cls.runtime_name:
            cls.runtime_name = cls.__name__

    def execute(self, request: DomainRuntimeRequest) -> DomainRuntimeResult:
        context = self._build_context(request)
        errors = self.validate(request)
        if errors:
            return DomainRuntimeResult(
                request_id=request.request_id,
                action_code=request.action_code,
                status=DomainRuntimeStatus.FAILED,
                error="; ".join(errors),
            )
        try:
            output = self.execute_op(request, context)
            verified = self.verify(request, output)
            status = DomainRuntimeStatus.SUCCEEDED if verified else DomainRuntimeStatus.FAILED
            return DomainRuntimeResult(
                request_id=request.request_id,
                action_code=request.action_code,
                status=status,
                output=output,
            )
        except DomainValidationError as e:
            return DomainRuntimeResult(
                request_id=request.request_id,
                action_code=request.action_code,
                status=DomainRuntimeStatus.FAILED,
                error=str(e),
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
