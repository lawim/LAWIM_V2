from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class DivergenceRecord:
    record_id: str = field(default_factory=lambda: uuid4().hex[:16])
    interaction_id: str = ""
    correlation_id: str = ""
    channel: str = ""
    field_name: str = ""
    v2_value: Any = None
    v3_value: Any = None
    category: str = ""
    severity: str = "info"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class InteractionDivergenceAnalyzer:
    def __init__(self) -> None:
        self._records: list[DivergenceRecord] = []

    def compare(
        self,
        interaction_id: str,
        correlation_id: str,
        channel: str,
        v2_result: dict[str, Any],
        v3_result: dict[str, Any],
    ) -> list[DivergenceRecord]:
        divergences: list[DivergenceRecord] = []
        for field_name in ("resolved_identity", "resolved_project", "intent", "next_action", "response_type", "handover"):
            v2_val = v2_result.get(field_name)
            v3_val = v3_result.get(field_name)
            if v2_val != v3_val:
                record = DivergenceRecord(
                    interaction_id=interaction_id,
                    correlation_id=correlation_id,
                    channel=channel,
                    field_name=field_name,
                    v2_value=v2_val,
                    v3_value=v3_val,
                    category="field_mismatch",
                    severity="warning" if field_name in ("next_action", "handover") else "info",
                )
                self._records.append(record)
                divergences.append(record)
        return divergences

    def record_divergence(
        self,
        interaction_id: str,
        correlation_id: str,
        channel: str,
        field_name: str,
        v2_value: Any,
        v3_value: Any,
        category: str = "field_mismatch",
        severity: str = "info",
    ) -> DivergenceRecord:
        record = DivergenceRecord(
            interaction_id=interaction_id,
            correlation_id=correlation_id,
            channel=channel,
            field_name=field_name,
            v2_value=v2_value,
            v3_value=v3_value,
            category=category,
            severity=severity,
        )
        self._records.append(record)
        return record

    def list_by_correlation(self, correlation_id: str) -> list[DivergenceRecord]:
        return [r for r in self._records if r.correlation_id == correlation_id]

    def count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records.clear()
