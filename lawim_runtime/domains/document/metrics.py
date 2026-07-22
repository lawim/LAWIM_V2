from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class DocumentMetrics:
    documents_requested: int = 0
    documents_registered: int = 0
    documents_analyzed: int = 0
    documents_review_required: int = 0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "documents_requested": self.documents_requested,
            "documents_registered": self.documents_registered,
            "documents_analyzed": self.documents_analyzed,
            "documents_review_required": self.documents_review_required,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.documents_requested = 0
        self.documents_registered = 0
        self.documents_analyzed = 0
        self.documents_review_required = 0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()
