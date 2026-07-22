from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.events import DomainEvent


class NotificationEventType(str, Enum):
    NOTIFICATION_PREPARED = "NOTIFICATION_PREPARED"
    NOTIFICATION_SCHEDULED = "NOTIFICATION_SCHEDULED"
    NOTIFICATION_SENT = "NOTIFICATION_SENT"
    NOTIFICATION_DELIVERED = "NOTIFICATION_DELIVERED"
    NOTIFICATION_FAILED = "NOTIFICATION_FAILED"
    NOTIFICATION_CANCELLED = "NOTIFICATION_CANCELLED"


@dataclass(frozen=True)
class NotificationEvent:
    event_type: NotificationEventType = NotificationEventType.NOTIFICATION_PREPARED
    notification_id: str = ""
    project_id: str = ""
    template_name: str = ""
    channel: str = ""
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_event(self, runtime_name: str = "notification", correlation_id: str = "") -> DomainEvent:
        return DomainEvent(
            event_type=self.event_type.value,
            runtime_name=runtime_name,
            data={
                "notification_id": self.notification_id,
                "project_id": self.project_id,
                "template_name": self.template_name,
                "channel": self.channel,
                "error": self.error,
                **self.metadata,
            },
            correlation_id=correlation_id,
        )
