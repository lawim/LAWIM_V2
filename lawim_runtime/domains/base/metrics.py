from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class DomainMetrics:
    executions_started: int = 0
    executions_succeeded: int = 0
    executions_failed: int = 0
    total_duration_ms: float = 0.0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "executions_started": self.executions_started,
            "executions_succeeded": self.executions_succeeded,
            "executions_failed": self.executions_failed,
            "total_duration_ms": self.total_duration_ms,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.executions_started = 0
        self.executions_succeeded = 0
        self.executions_failed = 0
        self.total_duration_ms = 0.0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()


class MetricsCollector:
    def __init__(self) -> None:
        self._metrics = DomainMetrics()

    @property
    def metrics(self) -> DomainMetrics:
        return self._metrics

    def record_started(self) -> None:
        self._metrics.executions_started += 1

    def record_succeeded(self) -> None:
        self._metrics.executions_succeeded += 1

    def record_failed(self) -> None:
        self._metrics.executions_failed += 1

    def record_duration(self, duration_ms: float) -> None:
        self._metrics.total_duration_ms += duration_ms

    def snapshot(self) -> dict[str, Any]:
        return self._metrics.snapshot()

    def reset(self) -> None:
        self._metrics.reset()
