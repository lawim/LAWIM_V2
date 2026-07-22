from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class VisitMetrics:
    visits_requested: int = 0
    visits_scheduled: int = 0
    visits_completed: int = 0
    visits_cancelled: int = 0
    no_shows: int = 0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "visits_requested": self.visits_requested,
            "visits_scheduled": self.visits_scheduled,
            "visits_completed": self.visits_completed,
            "visits_cancelled": self.visits_cancelled,
            "no_shows": self.no_shows,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.visits_requested = 0
        self.visits_scheduled = 0
        self.visits_completed = 0
        self.visits_cancelled = 0
        self.no_shows = 0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()
