from __future__ import annotations
from enum import Enum
from typing import Any


class ExecutionState(str, Enum):
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

    @property
    def is_terminal(self) -> bool:
        return self in {
            ExecutionState.SUCCEEDED,
            ExecutionState.FAILED,
            ExecutionState.COMPENSATED,
            ExecutionState.CANCELLED,
            ExecutionState.DEAD_LETTERED,
            ExecutionState.EXPIRED,
        }

    @property
    def is_active(self) -> bool:
        return self in {
            ExecutionState.CREATED,
            ExecutionState.VALIDATING,
            ExecutionState.READY,
            ExecutionState.SCHEDULED,
            ExecutionState.RUNNING,
            ExecutionState.WAITING,
            ExecutionState.RETRYING,
            ExecutionState.COMPENSATING,
        }


VALID_TRANSITIONS: dict[ExecutionState, set[ExecutionState]] = {
    ExecutionState.CREATED: {
        ExecutionState.VALIDATING,
        ExecutionState.CANCELLED,
        ExecutionState.EXPIRED,
    },
    ExecutionState.VALIDATING: {
        ExecutionState.READY,
        ExecutionState.FAILED,
        ExecutionState.CANCELLED,
        ExecutionState.EXPIRED,
    },
    ExecutionState.READY: {
        ExecutionState.SCHEDULED,
        ExecutionState.RUNNING,
        ExecutionState.FAILED,
        ExecutionState.CANCELLED,
        ExecutionState.EXPIRED,
    },
    ExecutionState.SCHEDULED: {
        ExecutionState.RUNNING,
        ExecutionState.WAITING,
        ExecutionState.CANCELLED,
        ExecutionState.EXPIRED,
    },
    ExecutionState.RUNNING: {
        ExecutionState.SUCCEEDED,
        ExecutionState.FAILED,
        ExecutionState.WAITING,
        ExecutionState.RETRYING,
        ExecutionState.COMPENSATING,
        ExecutionState.CANCELLED,
        ExecutionState.EXPIRED,
    },
    ExecutionState.WAITING: {
        ExecutionState.RUNNING,
        ExecutionState.RETRYING,
        ExecutionState.FAILED,
        ExecutionState.CANCELLED,
        ExecutionState.EXPIRED,
    },
    ExecutionState.RETRYING: {
        ExecutionState.RUNNING,
        ExecutionState.FAILED,
        ExecutionState.DEAD_LETTERED,
        ExecutionState.CANCELLED,
        ExecutionState.EXPIRED,
    },
    ExecutionState.SUCCEEDED: {
        ExecutionState.COMPENSATING,
    },
    ExecutionState.FAILED: {
        ExecutionState.RETRYING,
        ExecutionState.COMPENSATING,
        ExecutionState.DEAD_LETTERED,
    },
    ExecutionState.COMPENSATING: {
        ExecutionState.COMPENSATED,
        ExecutionState.FAILED,
        ExecutionState.CANCELLED,
        ExecutionState.EXPIRED,
    },
    ExecutionState.COMPENSATED: set(),
    ExecutionState.CANCELLED: set(),
    ExecutionState.DEAD_LETTERED: set(),
    ExecutionState.EXPIRED: set(),
}


class ActionExecutionStateMachine:
    def __init__(self, initial_state: ExecutionState = ExecutionState.CREATED) -> None:
        self._state = initial_state
        self._metadata: dict[str, Any] = {}

    @property
    def state(self) -> ExecutionState:
        return self._state

    @property
    def metadata(self) -> dict[str, Any]:
        return dict(self._metadata)

    def can_transition_to(self, target: ExecutionState) -> bool:
        return target in VALID_TRANSITIONS.get(self._state, set())

    def transition_to(
        self,
        target: ExecutionState,
        metadata: dict[str, Any] | None = None,
    ) -> ExecutionState:
        if metadata:
            self._metadata.update(metadata)
        if target == self._state:
            return self._state
        allowed = VALID_TRANSITIONS.get(self._state)
        if allowed is None or target not in allowed:
            from ..runtime.errors import InvalidTransitionError
            raise InvalidTransitionError(
                f"Cannot transition from {self._state.value} to {target.value}"
            )
        self._state = target
        return self._state

    def reset(self, state: ExecutionState = ExecutionState.CREATED) -> None:
        self._state = state
        self._metadata.clear()
