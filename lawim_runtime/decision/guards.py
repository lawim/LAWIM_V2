from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from ..project.status import ProjectStatus, VALID_TRANSITIONS
from ..runtime.state_machine import RuntimeStateMachine


@dataclass
class GuardResult:
    allowed: bool = True
    reason: str = ""
    target_status: str = ""


class TransitionGuard:
    @staticmethod
    def check(current_status: ProjectStatus, target_action: str) -> GuardResult:
        return GuardResult(allowed=True, reason="Guard check passed")

    @staticmethod
    def can_transition(
        current: ProjectStatus, target: ProjectStatus
    ) -> GuardResult:
        if RuntimeStateMachine.can_transition(current, target):
            return GuardResult(
                allowed=True,
                reason=f"Transition from {current.value} to {target.value} allowed",
                target_status=target.value,
            )
        return GuardResult(
            allowed=False,
            reason=f"Transition from {current.value} to {target.value} not allowed",
            target_status=current.value,
        )

    @staticmethod
    def enforce_transition(
        current: ProjectStatus, target: ProjectStatus
    ) -> ProjectStatus:
        return RuntimeStateMachine.transition(current, target)

    @staticmethod
    def next_statuses(current: ProjectStatus) -> list[ProjectStatus]:
        return RuntimeStateMachine.next_statuses(current)
