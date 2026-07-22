from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from .retry import RetryPolicy


class StepStatus(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    WAITING = "WAITING"
    RETRY_SCHEDULED = "RETRY_SCHEDULED"
    COMPENSATING = "COMPENSATING"
    COMPENSATED = "COMPENSATED"
    CANCELLED = "CANCELLED"
    SKIPPED = "SKIPPED"
    DEAD_LETTERED = "DEAD_LETTERED"

    @property
    def is_terminal(self) -> bool:
        return self in {
            StepStatus.SUCCEEDED,
            StepStatus.FAILED,
            StepStatus.COMPENSATED,
            StepStatus.CANCELLED,
            StepStatus.SKIPPED,
            StepStatus.DEAD_LETTERED,
        }

    @property
    def is_active(self) -> bool:
        return self in {
            StepStatus.READY,
            StepStatus.RUNNING,
            StepStatus.WAITING,
            StepStatus.RETRY_SCHEDULED,
            StepStatus.COMPENSATING,
        }


@dataclass
class ActionStep:
    step_id: str
    name: str = ""
    handler_operation: str = ""
    sequence: int = 0
    dependencies: list[str] = field(default_factory=list)
    timeout: float = 30.0
    retry_policy: RetryPolicy | None = None
    compensation_step: str = ""
    required: bool = True
    idempotent: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def display_name(self) -> str:
        return self.name or f"step-{self.step_id}"


@dataclass
class ActionStepResult:
    step_id: str
    status: StepStatus = StepStatus.PENDING
    started_at: datetime | None = None
    completed_at: datetime | None = None
    attempt_number: int = 0
    output: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    verification_result: bool = False
    retryable: bool = False
    compensation_required: bool = False
    checksum: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def duration_seconds(self) -> float | None:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def mark_started(self) -> None:
        self.status = StepStatus.RUNNING
        self.started_at = datetime.now(timezone.utc)

    def mark_completed(self, output: dict[str, Any] | None = None) -> None:
        self.status = StepStatus.SUCCEEDED
        self.completed_at = datetime.now(timezone.utc)
        if output is not None:
            self.output = output

    def mark_failed(self, error: str, retryable: bool = False) -> None:
        self.status = StepStatus.FAILED
        self.error = error
        self.retryable = retryable
        self.completed_at = datetime.now(timezone.utc)
