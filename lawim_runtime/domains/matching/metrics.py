from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class MatchingMetrics:
    searches_started: int = 0
    searches_completed: int = 0
    matches_found: int = 0
    no_match_count: int = 0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "searches_started": self.searches_started,
            "searches_completed": self.searches_completed,
            "matches_found": self.matches_found,
            "no_match_count": self.no_match_count,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.searches_started = 0
        self.searches_completed = 0
        self.matches_found = 0
        self.no_match_count = 0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()
