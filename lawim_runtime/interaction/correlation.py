from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class CorrelationRecord:
    correlation_id: str = ""
    interaction_id: str = ""
    session_id: str = ""
    conversation_id: str = ""
    project_id: str = ""
    decision_id: str = ""
    execution_id: str = ""
    delivery_id: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CorrelationManager:
    def __init__(self) -> None:
        self._records: dict[str, CorrelationRecord] = {}

    def create(self, correlation_id: str = "") -> str:
        cid = correlation_id or uuid4().hex[:16]
        self._records[cid] = CorrelationRecord(correlation_id=cid)
        return cid

    def get(self, correlation_id: str) -> CorrelationRecord | None:
        return self._records.get(correlation_id)

    def update(self, correlation_id: str, **kwargs: Any) -> None:
        record = self._records.get(correlation_id)
        if record:
            for key, value in kwargs.items():
                if hasattr(record, key):
                    setattr(record, key, value)

    def trace(self, correlation_id: str) -> CorrelationRecord | None:
        return self._records.get(correlation_id)

    def count(self) -> int:
        return len(self._records)
