from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class TransactionMetrics:
    transactions_prepared: int = 0
    transactions_confirmed: int = 0
    transactions_completed: int = 0
    transactions_cancelled: int = 0
    negotiations_started: int = 0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "transactions_prepared": self.transactions_prepared,
            "transactions_confirmed": self.transactions_confirmed,
            "transactions_completed": self.transactions_completed,
            "transactions_cancelled": self.transactions_cancelled,
            "negotiations_started": self.negotiations_started,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.transactions_prepared = 0
        self.transactions_confirmed = 0
        self.transactions_completed = 0
        self.transactions_cancelled = 0
        self.negotiations_started = 0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()
