from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from .locking.leases import LeaseStatus
from .state import ExecutionState


class RecoveryActionType(str, Enum):
    ORPHAN_DETECTED = "ORPHAN_DETECTED"
    LEASE_EXPIRED = "LEASE_EXPIRED"
    RETRY_PENDING = "RETRY_PENDING"
    COMPENSATION_UNFINISHED = "COMPENSATION_UNFINISHED"
    DEAD_LETTER_REVIEW = "DEAD_LETTER_REVIEW"


@dataclass
class RecoveryAction:
    action_id: str = field(default_factory=lambda: uuid4().hex[:16])
    action_type: RecoveryActionType = RecoveryActionType.ORPHAN_DETECTED
    execution_id: str = ""
    resource_key: str = ""
    description: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    detected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resolved: bool = False


class ExecutionRecoveryService:
    def __init__(
        self,
        lock_manager: Any | None = None,
        lease_manager: Any | None = None,
        dead_letter_queue: Any | None = None,
        repository: Any | None = None,
        compensation_engine: Any | None = None,
    ) -> None:
        self._lock_manager = lock_manager
        self._lease_manager = lease_manager
        self._dead_letter_queue = dead_letter_queue
        self._repository = repository
        self._compensation_engine = compensation_engine

    def recover_all(self) -> list[RecoveryAction]:
        actions: list[RecoveryAction] = []
        actions.extend(self.detect_orphaned())
        actions.extend(self.detect_expired_leases())
        actions.extend(self.detect_pending_retries())
        actions.extend(self.detect_unfinished_compensations())
        actions.extend(self.detect_dead_letter_review())
        return actions

    def detect_orphaned(self) -> list[RecoveryAction]:
        result: list[RecoveryAction] = []
        if self._repository is None:
            return result
        try:
            executions = self._repository.list_executions()
        except Exception:
            return result
        active_states = {
            ExecutionState.CREATED,
            ExecutionState.VALIDATING,
            ExecutionState.READY,
            ExecutionState.SCHEDULED,
            ExecutionState.RUNNING,
            ExecutionState.WAITING,
            ExecutionState.RETRYING,
            ExecutionState.COMPENSATING,
        }
        for exe in executions:
            state_val = exe.get("state", "") if isinstance(exe, dict) else getattr(exe, "state", "")
            try:
                es = ExecutionState(state_val) if isinstance(state_val, str) else state_val
            except (ValueError, TypeError):
                continue
            if es in active_states:
                result.append(RecoveryAction(
                    action_type=RecoveryActionType.ORPHAN_DETECTED,
                    execution_id=exe.get("execution_id", "") if isinstance(exe, dict) else getattr(exe, "execution_id", ""),
                    description=f"Execution in active state {es.value} may be orphaned",
                    details={"state": es.value, "execution": exe},
                ))
        return result

    def detect_expired_leases(self) -> list[RecoveryAction]:
        result: list[RecoveryAction] = []
        if self._lease_manager is None:
            return result
        try:
            expired = self._lease_manager.recover_expired()
        except Exception:
            return result
        for lease in expired:
            result.append(RecoveryAction(
                action_type=RecoveryActionType.LEASE_EXPIRED,
                resource_key=lease.resource_key,
                description=f"Lease {lease.lease_id} expired for resource {lease.resource_key}",
                details={
                    "lease_id": lease.lease_id,
                    "resource_key": lease.resource_key,
                    "owner": lease.owner,
                    "acquired_at": lease.acquired_at.isoformat() if hasattr(lease.acquired_at, "isoformat") else str(lease.acquired_at),
                },
            ))
        return result

    def detect_pending_retries(self) -> list[RecoveryAction]:
        result: list[RecoveryAction] = []
        if self._repository is None:
            return result
        try:
            executions = self._repository.list_executions()
        except Exception:
            return result
        for exe in executions:
            state_val = exe.get("state", "") if isinstance(exe, dict) else getattr(exe, "state", "")
            try:
                es = ExecutionState(state_val) if isinstance(state_val, str) else state_val
            except (ValueError, TypeError):
                continue
            if es == ExecutionState.RETRYING:
                eid = exe.get("execution_id", "") if isinstance(exe, dict) else getattr(exe, "execution_id", "")
                result.append(RecoveryAction(
                    action_type=RecoveryActionType.RETRY_PENDING,
                    execution_id=eid,
                    description=f"Execution {eid} in RETRYING state pending retry",
                    details={"state": es.value},
                ))
        return result

    def detect_unfinished_compensations(self) -> list[RecoveryAction]:
        result: list[RecoveryAction] = []
        if self._repository is None:
            return result
        try:
            executions = self._repository.list_executions()
        except Exception:
            return result
        for exe in executions:
            state_val = exe.get("state", "") if isinstance(exe, dict) else getattr(exe, "state", "")
            try:
                es = ExecutionState(state_val) if isinstance(state_val, str) else state_val
            except (ValueError, TypeError):
                continue
            if es == ExecutionState.COMPENSATING:
                eid = exe.get("execution_id", "") if isinstance(exe, dict) else getattr(exe, "execution_id", "")
                result.append(RecoveryAction(
                    action_type=RecoveryActionType.COMPENSATION_UNFINISHED,
                    execution_id=eid,
                    description=f"Execution {eid} in COMPENSATING state not resolved",
                    details={"state": es.value},
                ))
        return result

    def detect_dead_letter_review(self) -> list[RecoveryAction]:
        result: list[RecoveryAction] = []
        if self._dead_letter_queue is None:
            return result
        try:
            records = self._dead_letter_queue.list()
        except Exception:
            return result
        for record in records:
            dl_id = record.dead_letter_id if hasattr(record, "dead_letter_id") else record.get("dead_letter_id", "")
            eid = record.execution_id if hasattr(record, "execution_id") else record.get("execution_id", "")
            result.append(RecoveryAction(
                action_type=RecoveryActionType.DEAD_LETTER_REVIEW,
                execution_id=eid,
                resource_key=dl_id,
                description=f"Dead letter record {dl_id} requires manual review",
                details={"dead_letter_id": dl_id},
            ))
        return result
