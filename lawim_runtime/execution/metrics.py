from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ExecutionMetrics:
    executions_started: int = 0
    executions_succeeded: int = 0
    executions_failed: int = 0
    executions_compensated: int = 0
    executions_dead_lettered: int = 0
    executions_expired: int = 0
    executions_cancelled: int = 0
    total_attempts: int = 0
    total_retries: int = 0
    locks_acquired: int = 0
    locks_released: int = 0
    locks_contended: int = 0
    leases_acquired: int = 0
    leases_expired: int = 0
    compensations_run: int = 0
    compensations_failed: int = 0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "executions_started": self.executions_started,
            "executions_succeeded": self.executions_succeeded,
            "executions_failed": self.executions_failed,
            "executions_compensated": self.executions_compensated,
            "executions_dead_lettered": self.executions_dead_lettered,
            "executions_expired": self.executions_expired,
            "executions_cancelled": self.executions_cancelled,
            "total_attempts": self.total_attempts,
            "total_retries": self.total_retries,
            "locks_acquired": self.locks_acquired,
            "locks_released": self.locks_released,
            "locks_contended": self.locks_contended,
            "leases_acquired": self.leases_acquired,
            "leases_expired": self.leases_expired,
            "compensations_run": self.compensations_run,
            "compensations_failed": self.compensations_failed,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.executions_started = 0
        self.executions_succeeded = 0
        self.executions_failed = 0
        self.executions_compensated = 0
        self.executions_dead_lettered = 0
        self.executions_expired = 0
        self.executions_cancelled = 0
        self.total_attempts = 0
        self.total_retries = 0
        self.locks_acquired = 0
        self.locks_released = 0
        self.locks_contended = 0
        self.leases_acquired = 0
        self.leases_expired = 0
        self.compensations_run = 0
        self.compensations_failed = 0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()


class MetricsCollector:
    def __init__(self) -> None:
        self._metrics = ExecutionMetrics()

    @property
    def metrics(self) -> ExecutionMetrics:
        return self._metrics

    def record_started(self) -> None:
        self._metrics.executions_started += 1
        self._metrics.total_attempts += 1

    def record_succeeded(self) -> None:
        self._metrics.executions_succeeded += 1

    def record_failed(self) -> None:
        self._metrics.executions_failed += 1

    def record_compensated(self) -> None:
        self._metrics.executions_compensated += 1
        self._metrics.compensations_run += 1

    def record_compensation_failed(self) -> None:
        self._metrics.compensations_failed += 1

    def record_dead_lettered(self) -> None:
        self._metrics.executions_dead_lettered += 1

    def record_expired(self) -> None:
        self._metrics.executions_expired += 1

    def record_cancelled(self) -> None:
        self._metrics.executions_cancelled += 1

    def record_retry(self) -> None:
        self._metrics.total_retries += 1

    def record_lock_acquired(self) -> None:
        self._metrics.locks_acquired += 1

    def record_lock_released(self) -> None:
        self._metrics.locks_released += 1

    def record_lock_contended(self) -> None:
        self._metrics.locks_contended += 1

    def record_lease_acquired(self) -> None:
        self._metrics.leases_acquired += 1

    def record_lease_expired(self) -> None:
        self._metrics.leases_expired += 1

    def snapshot(self) -> dict[str, Any]:
        return self._metrics.snapshot()

    def reset(self) -> None:
        self._metrics.reset()
