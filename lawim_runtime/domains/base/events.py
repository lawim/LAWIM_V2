from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class DomainEvent:
    event_id: str = field(default_factory=lambda: uuid4().hex[:16])
    event_type: str = ""
    runtime_name: str = ""
    execution_id: str = ""
    action_code: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    data: dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""


class EventCollector:
    def __init__(self) -> None:
        self._events: list[DomainEvent] = []

    def record(self, event: DomainEvent) -> None:
        self._events.append(event)

    def flush(self) -> list[DomainEvent]:
        events = list(self._events)
        self._events.clear()
        return events

    def list_all(self) -> list[DomainEvent]:
        return list(self._events)

    def count(self) -> int:
        return len(self._events)

    def clear(self) -> None:
        self._events.clear()
