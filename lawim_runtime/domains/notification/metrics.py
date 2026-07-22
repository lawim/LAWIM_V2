from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class NotificationMetrics:
    notifications_prepared: int = 0
    notifications_sent: int = 0
    notifications_delivered: int = 0
    notifications_failed: int = 0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "notifications_prepared": self.notifications_prepared,
            "notifications_sent": self.notifications_sent,
            "notifications_delivered": self.notifications_delivered,
            "notifications_failed": self.notifications_failed,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.notifications_prepared = 0
        self.notifications_sent = 0
        self.notifications_delivered = 0
        self.notifications_failed = 0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()
