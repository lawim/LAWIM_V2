from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from ..events.base import RuntimeEvent


@dataclass
class AuditEntry:
    entry_id: str = field(default_factory=lambda: uuid4().hex[:16])
    event_id: str = ""
    event_type: str = ""
    project_id: str = ""
    actor: str = ""
    before: dict[str, Any] = field(default_factory=dict)
    after: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RuntimeAudit:
    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def record(self, event: RuntimeEvent, before: dict, after: dict) -> None:
        entry = AuditEntry(
            event_id=event.event_id,
            event_type=event.event_type,
            project_id=event.project_id,
            actor=event.actor,
            before=before,
            after=after,
        )
        self._entries.append(entry)

    def get_entries(self, project_id: str | None = None) -> list[AuditEntry]:
        if project_id is None:
            return list(self._entries)
        return [e for e in self._entries if e.project_id == project_id]

    def clear(self) -> None:
        self._entries.clear()
