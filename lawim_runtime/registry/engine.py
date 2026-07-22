from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from ..events.base import RuntimeEvent
from ..project.model import ProjectRuntime


class EngineBase(ABC):
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def can_handle(self, event: RuntimeEvent) -> bool: ...

    @abstractmethod
    def execute(self, project: ProjectRuntime | None, event: RuntimeEvent) -> ProjectRuntime | None: ...
