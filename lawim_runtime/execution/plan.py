from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .retry import RetryPolicy
from .step import ActionStep
from .timeout import TimeoutPolicy


@dataclass
class CompensationPolicy:
    enabled: bool = False
    max_compensation_attempts: int = 1
    fail_on_compensation_error: bool = False
    compensation_timeout_seconds: float = 30.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionExecutionPlan:
    plan_id: str
    execution_request_id: str
    action_code: str
    steps: list[ActionStep] = field(default_factory=list)
    dependencies: dict[str, list[str]] = field(default_factory=dict)
    timeout_policy: TimeoutPolicy | None = None
    retry_policy: RetryPolicy | None = None
    compensation_policy: CompensationPolicy | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = "1.0"
    checksum: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def total_steps(self) -> int:
        return len(self.steps)

    @property
    def step_count(self) -> int:
        return len(self.steps)

    def step_by_id(self, step_id: str) -> ActionStep | None:
        for step in self.steps:
            if step.step_id == step_id:
                return step
        return None

    def execution_order(self) -> list[ActionStep]:
        resolved: list[ActionStep] = []
        visited: set[str] = set()

        def _visit(step_id: str) -> None:
            if step_id in visited:
                return
            visited.add(step_id)
            deps = self.dependencies.get(step_id, [])
            for dep_id in deps:
                _visit(dep_id)
            step = self.step_by_id(step_id)
            if step is not None:
                resolved.append(step)

        for step in self.steps:
            _visit(step.step_id)
        return resolved
