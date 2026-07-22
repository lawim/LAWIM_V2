from __future__ import annotations
from typing import Any
from ..runtime.director import RuntimeDirector
from ..events.base import RuntimeEvent
from ..project.model import ProjectRuntime


class RuntimeFacade:
    """Simplified facade for V2 module integration."""

    def __init__(self, director: RuntimeDirector) -> None:
        self._director = director

    def process_event(
        self,
        event_type: str,
        project_id: str = "",
        actor: str = "system",
        **payload: Any,
    ) -> dict[str, Any]:
        event = RuntimeEvent(
            event_type=event_type,
            project_id=project_id,
            actor=actor,
            source="v2_facade",
            payload=payload,
        )
        return self._director.handle_event(event)

    def get_project(self, project_id: str) -> ProjectRuntime | None:
        return None

    def health(self) -> dict[str, Any]:
        return {"status": "ok", "runtime": "LROS", "version": "3.0.0-alpha"}
