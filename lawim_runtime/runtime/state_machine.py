from __future__ import annotations
from ..project.status import ProjectStatus, VALID_TRANSITIONS
from ..runtime.errors import InvalidTransitionError


class RuntimeStateMachine:
    @staticmethod
    def transition(current: ProjectStatus, target: ProjectStatus) -> ProjectStatus:
        allowed = VALID_TRANSITIONS.get(current, set())
        if target not in allowed:
            raise InvalidTransitionError(
                f"Cannot transition from {current.value} to {target.value}. "
                f"Allowed: {[s.value for s in allowed]}"
            )
        return target

    @staticmethod
    def can_transition(current: ProjectStatus, target: ProjectStatus) -> bool:
        return target in VALID_TRANSITIONS.get(current, set())

    @staticmethod
    def next_statuses(current: ProjectStatus) -> list[ProjectStatus]:
        return sorted(VALID_TRANSITIONS.get(current, set()), key=lambda s: s.value)
