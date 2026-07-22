from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .base import RuntimeEvent


@dataclass(frozen=True)
class NotificationEvent(RuntimeEvent):
    event_type: str = "NOTIFICATION"
    project_id: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""
    causation_id: str = ""
    version: int = 1
