from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from ..decision.actions import ActionCategory


@dataclass(frozen=True)
class ExecutionPolicy:
    timeout_seconds: int = 30
    max_retries: int = 0
    idempotent: bool = False
    locking_scope: str = "project"
    compensation_policy: str = "none"
    verification_required: bool = False
    priority: int = 100
    concurrency_limit: int = 1
    allowed_stages: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


DEFAULT_POLICY_MAP: dict[ActionCategory, ExecutionPolicy] = {
    ActionCategory.INFORMATION: ExecutionPolicy(
        timeout_seconds=10,
        max_retries=1,
        idempotent=True,
        compensation_policy="none",
        priority=10,
    ),
    ActionCategory.QUALIFICATION: ExecutionPolicy(
        timeout_seconds=30,
        max_retries=2,
        idempotent=True,
        compensation_policy="none",
        priority=20,
    ),
    ActionCategory.COLLECTION: ExecutionPolicy(
        timeout_seconds=60,
        max_retries=3,
        idempotent=True,
        compensation_policy="rollback",
        priority=30,
    ),
    ActionCategory.CONFIRMATION: ExecutionPolicy(
        timeout_seconds=30,
        max_retries=2,
        idempotent=True,
        compensation_policy="none",
        priority=40,
    ),
    ActionCategory.MATCHING: ExecutionPolicy(
        timeout_seconds=120,
        max_retries=2,
        idempotent=True,
        compensation_policy="none",
        priority=50,
    ),
    ActionCategory.VISIT: ExecutionPolicy(
        timeout_seconds=300,
        max_retries=3,
        idempotent=False,
        compensation_policy="cancel",
        priority=60,
    ),
    ActionCategory.DOCUMENT: ExecutionPolicy(
        timeout_seconds=120,
        max_retries=3,
        idempotent=True,
        compensation_policy="rollback",
        priority=70,
    ),
    ActionCategory.TRANSACTION: ExecutionPolicy(
        timeout_seconds=600,
        max_retries=5,
        idempotent=True,
        compensation_policy="rollback",
        priority=80,
    ),
    ActionCategory.ESCALATION: ExecutionPolicy(
        timeout_seconds=60,
        max_retries=0,
        idempotent=True,
        compensation_policy="none",
        priority=90,
    ),
    ActionCategory.HANDOVER: ExecutionPolicy(
        timeout_seconds=60,
        max_retries=0,
        idempotent=True,
        compensation_policy="none",
        priority=100,
    ),
    ActionCategory.COMPLETION: ExecutionPolicy(
        timeout_seconds=30,
        max_retries=1,
        idempotent=True,
        compensation_policy="none",
        priority=110,
    ),
}
