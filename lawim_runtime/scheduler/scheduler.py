from __future__ import annotations
from typing import Any
from ..events.base import RuntimeEvent
from ..registry.registry import RuntimeRegistry
from ..project.model import ProjectRuntime
from ..runtime.errors import RuntimeError


class RuntimeScheduler:
    def __init__(self) -> None:
        self._engine_order: list[str] = []

    def set_order(self, order: list[str]) -> None:
        self._engine_order = order

    def execute(
        self,
        project: ProjectRuntime | None,
        event: RuntimeEvent,
        registry: RuntimeRegistry,
    ) -> ProjectRuntime | None:
        engines = self._resolve_engines(event, registry)
        for engine in engines:
            try:
                project = engine.execute(project, event)
            except Exception as exc:
                raise RuntimeError(f"Engine {engine.name()} failed: {exc}") from exc
        return project

    def _resolve_engines(self, event: RuntimeEvent, registry: RuntimeRegistry) -> list[Any]:
        all_engines = registry.get_all()
        matching = [e for e in all_engines if e.can_handle(event)]
        ordered = []
        for name in self._engine_order:
            for e in matching:
                if e.name() == name:
                    ordered.append(e)
        for e in matching:
            if e not in ordered:
                ordered.append(e)
        return ordered
