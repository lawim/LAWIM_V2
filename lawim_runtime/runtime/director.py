from __future__ import annotations
from typing import Any
from ..events.base import RuntimeEvent
from ..events.bus import EventBus
from ..registry.registry import RuntimeRegistry
from ..scheduler.scheduler import RuntimeScheduler
from ..project.model import ProjectRuntime
from ..project.timeline import Timeline, TimelineEntry
from ..persistence.persistence import RuntimePersistence
from ..telemetry.audit import RuntimeAudit
from ..telemetry.metrics import RuntimeMetrics
from ..runtime.errors import ProjectNotFoundError


class RuntimeDirector:
    def __init__(
        self,
        bus: EventBus,
        registry: RuntimeRegistry,
        scheduler: RuntimeScheduler,
        persistence: RuntimePersistence,
        timeline: Timeline,
        audit: RuntimeAudit,
        metrics: RuntimeMetrics,
    ) -> None:
        self._bus = bus
        self._registry = registry
        self._scheduler = scheduler
        self._persistence = persistence
        self._timeline = timeline
        self._audit = audit
        self._metrics = metrics

    def handle_event(self, event: RuntimeEvent) -> dict[str, Any]:
        self._metrics.record_event_received(event.event_type)
        with self._metrics.measure(event.event_type):
            project = self._load_project(event.project_id)
            before = project.to_dict() if project else {}
            project = self._scheduler.execute(project, event, self._registry)
            after = project.to_dict() if project else {}
            self._persist(project, event)
            self._record_timeline(project, event, before, after)
            self._audit.record(event, before, after)
            self._bus.publish(event)
            return {"project": after if project else {}, "event": event}

    def _load_project(self, project_id: str) -> ProjectRuntime | None:
        if not project_id:
            return ProjectRuntime()
        return self._persistence.load_project(project_id)

    def _persist(self, project: ProjectRuntime | None, event: RuntimeEvent) -> None:
        if project is not None:
            self._persistence.save_project(project)
        self._persistence.save_event(event)

    def _record_timeline(self, project: ProjectRuntime | None, event: RuntimeEvent, before: dict, after: dict) -> None:
        entry = TimelineEntry(
            project_id=event.project_id,
            event_type=event.event_type,
            before_state=before,
            after_state=after,
            actor=event.actor,
            source=event.source,
            correlation_id=event.correlation_id,
        )
        self._timeline.append(entry)
