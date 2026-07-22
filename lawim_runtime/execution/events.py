from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ExecutionEventType(str, Enum):
    EXECUTION_CREATED = "EXECUTION_CREATED"
    EXECUTION_STARTED = "EXECUTION_STARTED"
    EXECUTION_VALIDATED = "EXECUTION_VALIDATED"
    EXECUTION_FAILED = "EXECUTION_FAILED"
    EXECUTION_COMPLETED = "EXECUTION_COMPLETED"
    EXECUTION_COMPENSATED = "EXECUTION_COMPENSATED"
    EXECUTION_DEAD_LETTERED = "EXECUTION_DEAD_LETTERED"
    EXECUTION_EXPIRED = "EXECUTION_EXPIRED"
    EXECUTION_CANCELLED = "EXECUTION_CANCELLED"
    EXECUTION_RETRYING = "EXECUTION_RETRYING"
    EXECUTION_HEARTBEAT = "EXECUTION_HEARTBEAT"
    STEP_STARTED = "STEP_STARTED"
    STEP_COMPLETED = "STEP_COMPLETED"
    STEP_FAILED = "STEP_FAILED"
    LOCK_ACQUIRED = "LOCK_ACQUIRED"
    LOCK_RELEASED = "LOCK_RELEASED"
    LEASE_ACQUIRED = "LEASE_ACQUIRED"
    LEASE_EXPIRED = "LEASE_EXPIRED"
    COMPENSATION_STARTED = "COMPENSATION_STARTED"
    COMPENSATION_COMPLETED = "COMPENSATION_COMPLETED"
    COMPENSATION_FAILED = "COMPENSATION_FAILED"


@dataclass(frozen=True)
class ExecutionEvent:
    event_id: str
    event_type: ExecutionEventType
    execution_id: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    data: dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""
    causation_id: str = ""


class EventCollector:
    def __init__(self) -> None:
        self._events: list[ExecutionEvent] = []

    def record(self, event: ExecutionEvent) -> None:
        self._events.append(event)

    def flush(self) -> list[ExecutionEvent]:
        events = list(self._events)
        self._events.clear()
        return events

    def list_all(self) -> list[ExecutionEvent]:
        return list(self._events)

    def count(self) -> int:
        return len(self._events)

    def clear(self) -> None:
        self._events.clear()
