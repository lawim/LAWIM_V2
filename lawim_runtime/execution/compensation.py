from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable
from uuid import uuid4


class CompensationStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    PARTIAL = "PARTIAL"


@dataclass(frozen=True)
class CompensationAction:
    action_code: str
    handler_name: str
    parameters: dict[str, Any] = field(default_factory=dict)
    required: bool = True
    order: int = 0


@dataclass
class CompensationPlan:
    plan_id: str = field(default_factory=lambda: uuid4().hex[:16])
    execution_id: str = ""
    project_id: str = ""
    action_code: str = ""
    actions: list[CompensationAction] = field(default_factory=list)
    strategy: str = "linear"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_action(self, action: CompensationAction) -> None:
        self.actions.append(action)

    @property
    def has_actions(self) -> bool:
        return len(self.actions) > 0


@dataclass
class CompensationResult:
    plan_id: str = ""
    execution_id: str = ""
    status: CompensationStatus = CompensationStatus.PENDING
    results: list[dict[str, Any]] = field(default_factory=list)
    failure: str = ""
    compensated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        return self.status in (CompensationStatus.SUCCEEDED, CompensationStatus.SKIPPED)

    @property
    def requires_attention(self) -> bool:
        return self.status in (CompensationStatus.FAILED, CompensationStatus.PARTIAL)


CompensationHandler = Callable[[CompensationAction, dict[str, Any]], dict[str, Any]]


class CompensationEngine:
    def __init__(self) -> None:
        self._handlers: dict[str, CompensationHandler] = {}

    def register_handler(self, action_code: str, handler: CompensationHandler) -> None:
        self._handlers[action_code] = handler

    def can_compensate(self, action_code: str) -> bool:
        return action_code in self._handlers

    def execute_compensation(
        self,
        plan: CompensationPlan,
        context: dict[str, Any] | None = None,
    ) -> CompensationResult:
        ctx = context or {}
        result = CompensationResult(
            plan_id=plan.plan_id,
            execution_id=plan.execution_id,
            status=CompensationStatus.IN_PROGRESS,
        )

        if not plan.has_actions:
            result.status = CompensationStatus.SKIPPED
            return result

        sorted_actions = sorted(plan.actions, key=lambda a: a.order)
        all_succeeded = True
        any_failed = False

        for action in sorted_actions:
            handler = self._handlers.get(action.action_code)
            if handler is None:
                step = {
                    "action_code": action.action_code,
                    "status": "skipped",
                    "reason": f"No handler registered for {action.action_code}",
                }
                result.results.append(step)
                if action.required:
                    any_failed = True
                    all_succeeded = False
                continue

            try:
                handler_result = handler(action, ctx)
                step = {
                    "action_code": action.action_code,
                    "status": "succeeded",
                    "output": handler_result,
                }
                result.results.append(step)
            except Exception as exc:
                step = {
                    "action_code": action.action_code,
                    "status": "failed",
                    "error": str(exc),
                }
                result.results.append(step)
                if action.required:
                    any_failed = True
                    all_succeeded = False

        if not all_succeeded and any_failed:
            result.status = CompensationStatus.PARTIAL
            result.failure = "One or more required compensation actions failed"
        elif all_succeeded:
            result.status = CompensationStatus.SUCCEEDED
        else:
            result.status = CompensationStatus.PARTIAL

        return result
