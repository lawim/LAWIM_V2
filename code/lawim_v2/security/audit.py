from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class AuditEvent:
    event: str
    details: dict[str, object]


class AADAuditLogger:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def log(self, event: str, *, details: Mapping[str, object] | None = None) -> AuditEvent:
        sanitized = {str(key): value for key, value in (details or {}).items() if str(key) != "token" and str(key) != "secret"}
        audit_event = AuditEvent(event=event, details=sanitized)
        self._events.append(audit_event)
        return audit_event
