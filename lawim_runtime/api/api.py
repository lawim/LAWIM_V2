from __future__ import annotations
from typing import Any
from ..events.base import RuntimeEvent
from ..runtime.director import RuntimeDirector


class RuntimeAPI:
    def __init__(self, director: RuntimeDirector) -> None:
        self._director = director

    def handle_event(self, event: RuntimeEvent) -> dict[str, Any]:
        return self._director.handle_event(event)

    def create_project(self, project_type: str, owner: str) -> dict[str, Any]:
        event = RuntimeEvent(
            event_type="PROJECT_CREATED",
            project_id="",
            actor=owner,
            source="api",
            payload={"project_type": project_type, "owner": owner},
        )
        return self.handle_event(event)
