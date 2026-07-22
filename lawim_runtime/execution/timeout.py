from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class TimeoutPolicy:
    prepare_timeout: float = 10.0
    execution_timeout: float = 30.0
    verify_timeout: float = 15.0
    global_timeout: float = 120.0
    external_wait_timeout: float = 300.0


class DeadlineHelper:
    def __init__(self, policy: TimeoutPolicy) -> None:
        self._policy = policy

    @property
    def policy(self) -> TimeoutPolicy:
        return self._policy

    def deadline_from_now(self, timeout: float) -> str:
        dt = datetime.now(timezone.utc).timestamp() + timeout
        return datetime.fromtimestamp(dt, tz=timezone.utc).isoformat()

    def is_expired(self, deadline_str: str, now: datetime | None = None) -> bool:
        if not deadline_str:
            return False
        now = now or datetime.now(timezone.utc)
        try:
            deadline = datetime.fromisoformat(deadline_str)
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            return False
        return now >= deadline

    def remaining_seconds(self, deadline_str: str) -> float:
        if not deadline_str:
            return 0.0
        now = datetime.now(timezone.utc)
        try:
            deadline = datetime.fromisoformat(deadline_str)
            if deadline.tzinfo is None:
                deadline = deadline.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            return 0.0
        remaining = (deadline - now).total_seconds()
        return max(0.0, remaining)

    def prepare_deadline(self) -> str:
        return self.deadline_from_now(self._policy.prepare_timeout)

    def execution_deadline(self) -> str:
        return self.deadline_from_now(self._policy.execution_timeout)

    def verify_deadline(self) -> str:
        return self.deadline_from_now(self._policy.verify_timeout)

    def global_deadline(self) -> str:
        return self.deadline_from_now(self._policy.global_timeout)
