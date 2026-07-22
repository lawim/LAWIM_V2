from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class VerificationMetrics:
    verifications_started: int = 0
    verifications_completed: int = 0
    verifications_passed: int = 0
    verifications_failed: int = 0
    verifications_escalated: int = 0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "verifications_started": self.verifications_started,
            "verifications_completed": self.verifications_completed,
            "verifications_passed": self.verifications_passed,
            "verifications_failed": self.verifications_failed,
            "verifications_escalated": self.verifications_escalated,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.verifications_started = 0
        self.verifications_completed = 0
        self.verifications_passed = 0
        self.verifications_failed = 0
        self.verifications_escalated = 0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()
