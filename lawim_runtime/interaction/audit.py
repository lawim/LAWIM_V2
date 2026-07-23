from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class InteractionAuditEntry:
    entry_id: str = field(default_factory=lambda: uuid4().hex[:16])
    interaction_id: str = ""
    correlation_id: str = ""
    channel: str = ""
    action: str = ""
    actor_id: str = ""
    session_id: str = ""
    project_id: str = ""
    before_state: dict[str, Any] = field(default_factory=dict)
    after_state: dict[str, Any] = field(default_factory=dict)
    outcome: str = ""
    error: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class InteractionAuditor:
    def __init__(self) -> None:
        self._entries: list[InteractionAuditEntry] = []

    def record(
        self,
        interaction_id: str,
        correlation_id: str,
        channel: str,
        action: str,
        actor_id: str = "",
        session_id: str = "",
        project_id: str = "",
        before_state: dict[str, Any] | None = None,
        after_state: dict[str, Any] | None = None,
        outcome: str = "success",
        error: str = "",
    ) -> InteractionAuditEntry:
        entry = InteractionAuditEntry(
            interaction_id=interaction_id,
            correlation_id=correlation_id,
            channel=channel,
            action=action,
            actor_id=actor_id,
            session_id=session_id,
            project_id=project_id,
            before_state=before_state or {},
            after_state=after_state or {},
            outcome=outcome,
            error=error,
        )
        self._entries.append(entry)
        return entry

    def list_by_correlation(self, correlation_id: str) -> list[InteractionAuditEntry]:
        return [e for e in self._entries if e.correlation_id == correlation_id]

    def list_by_project(self, project_id: str) -> list[InteractionAuditEntry]:
        return [e for e in self._entries if e.project_id == project_id]

    def count(self) -> int:
        return len(self._entries)
