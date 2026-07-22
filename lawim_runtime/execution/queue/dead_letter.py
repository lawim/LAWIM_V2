from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class DeadLetterReason(str, Enum):
    MAX_RETRIES_EXCEEDED = "MAX_RETRIES_EXCEEDED"
    PERMANENT_FAILURE = "PERMANENT_FAILURE"
    COMPENSATION_FAILED = "COMPENSATION_FAILED"
    TIMEOUT = "TIMEOUT"
    ORPHANED = "ORPHANED"
    MANUAL = "MANUAL"


@dataclass
class DeadLetterRecord:
    dead_letter_id: str = field(default_factory=lambda: uuid4().hex[:16])
    execution_id: str = ""
    reason: DeadLetterReason = DeadLetterReason.PERMANENT_FAILURE
    error: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reviewed: bool = False
    resolution: str = ""


class DeadLetterQueue:
    def __init__(self) -> None:
        self._records: list[DeadLetterRecord] = []

    def add(self, record: DeadLetterRecord) -> None:
        self._records.append(record)

    def list(self) -> list[DeadLetterRecord]:
        return list(self._records)

    def list_unreviewed(self) -> list[DeadLetterRecord]:
        return [r for r in self._records if not r.reviewed]

    def get(self, dead_letter_id: str) -> DeadLetterRecord | None:
        for r in self._records:
            if r.dead_letter_id == dead_letter_id:
                return r
        return None

    def mark_reviewed(self, dead_letter_id: str, resolution: str = "") -> bool:
        record = self.get(dead_letter_id)
        if record is None:
            return False
        record.reviewed = True
        record.resolution = resolution
        return True

    def remove(self, dead_letter_id: str) -> bool:
        before = len(self._records)
        self._records = [r for r in self._records if r.dead_letter_id != dead_letter_id]
        return len(self._records) < before

    def count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records.clear()
