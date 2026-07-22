from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from .context import ActionExecutionContext
from .result import ActionExecutionResult


@dataclass
class HandlerMetadata:
    handler_name: str = ""
    version: str = "1.0.0"
    description: str = ""
    idempotent: bool = False
    supports_compensation: bool = False
    supports_retry: bool = False
    default_timeout: float = 30.0
    required_services: list[str] = field(default_factory=list)
    concurrency_scope: str = "global"
    metadata: dict[str, Any] = field(default_factory=dict)


class ActionHandler(ABC):
    handler_name: str = ""
    supported_actions: list[str] = []
    version: str = "1.0.0"
    idempotent: bool = False
    supports_compensation: bool = False
    supports_retry: bool = False
    default_timeout: float = 30.0
    required_services: list[str] = []
    concurrency_scope: str = "global"

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not cls.handler_name:
            cls.handler_name = cls.__name__

    def metadata(self) -> HandlerMetadata:
        return HandlerMetadata(
            handler_name=self.handler_name,
            version=self.version,
            description=self.__doc__ or "",
            idempotent=self.idempotent,
            supports_compensation=self.supports_compensation,
            supports_retry=self.supports_retry,
            default_timeout=self.default_timeout,
            required_services=list(self.required_services),
            concurrency_scope=self.concurrency_scope,
        )

    @abstractmethod
    def can_handle(self, action_code: str) -> bool:
        return action_code in self.supported_actions

    @abstractmethod
    def validate(self, context: ActionExecutionContext) -> list[str]:
        ...

    @abstractmethod
    def prepare(self, context: ActionExecutionContext) -> dict[str, Any]:
        ...

    @abstractmethod
    def execute(self, context: ActionExecutionContext) -> dict[str, Any]:
        ...

    @abstractmethod
    def verify(self, context: ActionExecutionContext, raw_result: dict[str, Any]) -> bool:
        ...

    @abstractmethod
    def compensate(self, context: ActionExecutionContext, result: ActionExecutionResult) -> dict[str, Any]:
        ...
