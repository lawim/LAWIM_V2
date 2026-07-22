from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class AuditEntry:
    entry_id: str
    execution_id: str
    action: str
    actor: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    details: dict[str, Any] = field(default_factory=dict)
    previous_state: str = ""
    new_state: str = ""


class AuditTrail:
    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def record(self, entry: AuditEntry) -> None:
        self._entries.append(entry)

    def list_for_execution(self, execution_id: str) -> list[AuditEntry]:
        return [e for e in self._entries if e.execution_id == execution_id]

    def list_all(self) -> list[AuditEntry]:
        return list(self._entries)

    def count(self) -> int:
        return len(self._entries)

    def clear(self) -> None:
        self._entries.clear()
