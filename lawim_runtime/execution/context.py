from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .request import ActionExecutionRequest
from ..decision.actions import ActionDefinition


@dataclass
class ActionExecutionContext:
    execution_id: str = field(default_factory=lambda: uuid4().hex[:16])
    request: ActionExecutionRequest = field(default_factory=ActionExecutionRequest)
    action_definition: ActionDefinition | None = None
    handler_name: str = ""
    services: dict[str, Any] = field(default_factory=dict)
    attempt_number: int = 0
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    deadline: str = ""
    correlation_id: str = ""
    causation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def record_event(self, event_type: str, details: dict[str, Any] | None = None) -> None:
        events: list[dict[str, Any]] = self.metadata.setdefault("events", [])
        events.append({
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details or {},
        })
