from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from .state import ExecutionState


class ExecutionStatus(str, Enum):
    CREATED = "CREATED"
    VALIDATING = "VALIDATING"
    READY = "READY"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    RETRYING = "RETRYING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    COMPENSATING = "COMPENSATING"
    COMPENSATED = "COMPENSATED"
    CANCELLED = "CANCELLED"
    DEAD_LETTERED = "DEAD_LETTERED"
    EXPIRED = "EXPIRED"

    @classmethod
    def from_execution_state(cls, state: ExecutionState) -> ExecutionStatus:
        mapping = {
            ExecutionState.CREATED: cls.CREATED,
            ExecutionState.VALIDATING: cls.VALIDATING,
            ExecutionState.READY: cls.READY,
            ExecutionState.SCHEDULED: cls.SCHEDULED,
            ExecutionState.RUNNING: cls.RUNNING,
            ExecutionState.WAITING: cls.WAITING,
            ExecutionState.RETRYING: cls.RETRYING,
            ExecutionState.SUCCEEDED: cls.SUCCEEDED,
            ExecutionState.FAILED: cls.FAILED,
            ExecutionState.COMPENSATING: cls.COMPENSATING,
            ExecutionState.COMPENSATED: cls.COMPENSATED,
            ExecutionState.CANCELLED: cls.CANCELLED,
            ExecutionState.DEAD_LETTERED: cls.DEAD_LETTERED,
            ExecutionState.EXPIRED: cls.EXPIRED,
        }
        return mapping[state]

    @property
    def is_terminal(self) -> bool:
        return self in {
            ExecutionStatus.SUCCEEDED,
            ExecutionStatus.FAILED,
            ExecutionStatus.COMPENSATED,
            ExecutionStatus.CANCELLED,
            ExecutionStatus.DEAD_LETTERED,
            ExecutionStatus.EXPIRED,
        }

    @property
    def is_success(self) -> bool:
        return self == ExecutionStatus.SUCCEEDED

    @property
    def is_failure(self) -> bool:
        return self in {
            ExecutionStatus.FAILED,
            ExecutionStatus.DEAD_LETTERED,
            ExecutionStatus.EXPIRED,
        }

    @property
    def requires_compensation(self) -> bool:
        return self in {
            ExecutionStatus.FAILED,
            ExecutionStatus.DEAD_LETTERED,
            ExecutionStatus.EXPIRED,
            ExecutionStatus.CANCELLED,
        }


@dataclass
class ActionExecutionResult:
    execution_id: str = ""
    request_id: str = ""
    decision_id: str = ""
    project_id: str = ""
    action_code: str = ""
    handler_name: str = ""
    handler_version: str = ""
    status: ExecutionStatus = ExecutionStatus.CREATED
    started_at: str = ""
    completed_at: str = ""
    attempts: int = 0
    step_results: list[dict[str, Any]] = field(default_factory=list)
    output: dict[str, Any] = field(default_factory=dict)
    failure: dict[str, Any] | None = None
    verification_status: str = ""
    verification_passed: bool = False
    compensation_status: str = ""
    compensation_required: bool = False
    compensation_result: dict[str, Any] | None = None
    produced_events: list[dict[str, Any]] = field(default_factory=list)
    idempotency_key: str = ""
    correlation_id: str = ""
    causation_id: str = ""
    checksum: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def mark_started(self) -> None:
        self.status = ExecutionStatus.RUNNING
        self.started_at = datetime.now(timezone.utc).isoformat()

    def mark_completed(self, output: dict[str, Any] | None = None) -> None:
        self.status = ExecutionStatus.SUCCEEDED
        self.completed_at = datetime.now(timezone.utc).isoformat()
        if output is not None:
            self.output = output

    def mark_failed(self, error: str = "", failure_type: str = "") -> None:
        self.status = ExecutionStatus.FAILED
        self.completed_at = datetime.now(timezone.utc).isoformat()
        self.failure = {
            "error": error,
            "failure_type": failure_type or "UNKNOWN",
            "timestamp": self.completed_at,
        }
