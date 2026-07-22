from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class CRMMetrics:
    leads_created: int = 0
    leads_updated: int = 0
    opportunities_created: int = 0
    handovers_created: int = 0
    handovers_resolved: int = 0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "leads_created": self.leads_created,
            "leads_updated": self.leads_updated,
            "opportunities_created": self.opportunities_created,
            "handovers_created": self.handovers_created,
            "handovers_resolved": self.handovers_resolved,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.leads_created = 0
        self.leads_updated = 0
        self.opportunities_created = 0
        self.handovers_created = 0
        self.handovers_resolved = 0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()
