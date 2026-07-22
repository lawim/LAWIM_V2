from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .request import ActionExecutionRequest
from .state import ExecutionState, ActionExecutionStateMachine
from .policy import ExecutionPolicy
from ..decision.actions import ActionDefinition
from ..decision.registry import ActionRegistry, ActionNotFoundError


@dataclass(frozen=True)
class GuardResult:
    allowed: bool = True
    blocking_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def merge(self, other: GuardResult) -> GuardResult:
        return GuardResult(
            allowed=self.allowed and other.allowed,
            blocking_reasons=self.blocking_reasons + other.blocking_reasons,
            warnings=self.warnings + other.warnings,
        )


class ActionExecutionGuard:
    def __init__(
        self,
        action_registry: ActionRegistry,
        state_machine: ActionExecutionStateMachine | None = None,
    ) -> None:
        self._registry = action_registry
        self._state_machine = state_machine or ActionExecutionStateMachine()

    @property
    def state_machine(self) -> ActionExecutionStateMachine:
        return self._state_machine

    @state_machine.setter
    def state_machine(self, machine: ActionExecutionStateMachine) -> None:
        self._state_machine = machine

    def validate(
        self,
        execution_request: ActionExecutionRequest,
        project_profile: Any = None,
    ) -> GuardResult:
        reasons: list[str] = []
        warnings: list[str] = []

        reason, warn = self._check_decision_exists(execution_request)
        if reason:
            reasons.append(reason)
        if warn:
            warnings.extend(warn)

        reason, warn = self._check_handler_available(execution_request)
        if reason:
            reasons.append(reason)
        if warn:
            warnings.extend(warn)

        reason, warn = self._check_transition_allowed(execution_request)
        if reason:
            reasons.append(reason)
        if warn:
            warnings.extend(warn)

        reason, warn = self._check_idempotency(execution_request)
        if reason:
            reasons.append(reason)
        if warn:
            warnings.extend(warn)

        reason, warn = self._check_locks(execution_request)
        if reason:
            reasons.append(reason)
        if warn:
            warnings.extend(warn)

        reason, warn = self._check_deadline(execution_request)
        if reason:
            reasons.append(reason)
        if warn:
            warnings.extend(warn)

        if project_profile is not None:
            reason, warn = self._check_profile_compatibility(
                execution_request, project_profile
            )
            if reason:
                reasons.append(reason)
            if warn:
                warnings.extend(warn)

        return GuardResult(
            allowed=len(reasons) == 0,
            blocking_reasons=reasons,
            warnings=warnings,
        )

    def _check_decision_exists(
        self, request: ActionExecutionRequest
    ) -> tuple[str | None, list[str]]:
        if not request.decision_id:
            return ("No decision_id provided", [])
        return (None, [])

    def _check_handler_available(
        self, request: ActionExecutionRequest
    ) -> tuple[str | None, list[str]]:
        try:
            action = self._registry.get(request.action_code)
            if not action:
                return (f"No handler for action '{request.action_code}'", [])
        except ActionNotFoundError:
            return (f"Action '{request.action_code}' not found in registry", [])
        return (None, [])

    def _check_transition_allowed(
        self, request: ActionExecutionRequest
    ) -> tuple[str | None, list[str]]:
        if request.current_stage and request.target_stage:
            if request.current_stage == request.target_stage:
                return (None, ["Source and target stage are identical"])
        if self._state_machine and not self._state_machine.can_transition_to(
            ExecutionState.READY
        ):
            return ("State machine does not allow transition to READY", [])
        return (None, [])

    def _check_idempotency(
        self, request: ActionExecutionRequest
    ) -> tuple[str | None, list[str]]:
        if request.idempotency_key:
            return (None, [])
        return ("No idempotency_key provided", [])

    def _check_locks(
        self, request: ActionExecutionRequest
    ) -> tuple[str | None, list[str]]:
        if not request.project_id:
            return ("Cannot acquire lock without project_id", [])
        return (None, [])

    def _check_deadline(
        self, request: ActionExecutionRequest
    ) -> tuple[str | None, list[str]]:
        return (None, [])

    def _check_profile_compatibility(
        self, request: ActionExecutionRequest, profile: Any
    ) -> tuple[str | None, list[str]]:
        return (None, [])
