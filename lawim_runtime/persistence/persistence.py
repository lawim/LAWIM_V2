from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from ..events.base import RuntimeEvent
from ..project.model import ProjectRuntime
from ..project.timeline import TimelineEntry


class RuntimePersistence(ABC):
    @abstractmethod
    def save_project(self, project: ProjectRuntime) -> None: ...

    @abstractmethod
    def load_project(self, project_id: str) -> ProjectRuntime | None: ...

    @abstractmethod
    def save_event(self, event: RuntimeEvent) -> None: ...

    @abstractmethod
    def load_events(self, project_id: str) -> list[RuntimeEvent]: ...

    @abstractmethod
    def save_timeline_entry(self, entry: TimelineEntry) -> None: ...
