from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class PaymentMetrics:
    intents_created: int = 0
    payments_succeeded: int = 0
    payments_failed: int = 0
    payments_refunded: int = 0
    payments_unknown: int = 0
    payments_reconciled: int = 0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "intents_created": self.intents_created,
            "payments_succeeded": self.payments_succeeded,
            "payments_failed": self.payments_failed,
            "payments_refunded": self.payments_refunded,
            "payments_unknown": self.payments_unknown,
            "payments_reconciled": self.payments_reconciled,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.intents_created = 0
        self.payments_succeeded = 0
        self.payments_failed = 0
        self.payments_refunded = 0
        self.payments_unknown = 0
        self.payments_reconciled = 0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()
