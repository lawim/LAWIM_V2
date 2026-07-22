from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class TimelineEntry:
    entry_id: str = field(default_factory=lambda: uuid4().hex[:16])
    project_id: str = ""
    event_type: str = ""
    before_state: dict[str, Any] = field(default_factory=dict)
    after_state: dict[str, Any] = field(default_factory=dict)
    actor: str = "system"
    source: str = ""
    correlation_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Timeline:
    def __init__(self) -> None:
        self._entries: list[TimelineEntry] = []

    def append(self, entry: TimelineEntry) -> None:
        self._entries.append(entry)

    def get_entries(self, project_id: str | None = None) -> list[TimelineEntry]:
        if project_id is None:
            return list(self._entries)
        return [e for e in self._entries if e.project_id == project_id]

    def replay(self, project_id: str, from_index: int = 0) -> list[TimelineEntry]:
        entries = self.get_entries(project_id)
        return entries[from_index:]

    def clear(self) -> None:
        self._entries.clear()
