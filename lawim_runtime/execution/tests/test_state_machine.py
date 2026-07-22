from __future__ import annotations

import pytest

from lawim_runtime.execution.state import (
    ActionExecutionStateMachine,
    ExecutionState,
    VALID_TRANSITIONS,
)


class TestActionExecutionStateMachine:
    def test_initial_state(self):
        sm = ActionExecutionStateMachine()
        assert sm.state == ExecutionState.CREATED

    def test_initial_state_custom(self):
        sm = ActionExecutionStateMachine(ExecutionState.READY)
        assert sm.state == ExecutionState.READY

    def test_valid_transition(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.VALIDATING)
        assert sm.state == ExecutionState.VALIDATING

    def test_transition_to_same_state(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.CREATED)
        assert sm.state == ExecutionState.CREATED

    def test_metadata_preserved_on_same_transition(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.CREATED, metadata={"key": "val"})
        assert sm.metadata["key"] == "val"

    def test_invalid_transition_raises(self):
        sm = ActionExecutionStateMachine()
        with pytest.raises(Exception):
            sm.transition_to(ExecutionState.SUCCEEDED)

    def test_metadata_update_on_transition(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.VALIDATING, metadata={"reason": "test"})
        assert sm.metadata["reason"] == "test"

    def test_can_transition_to_returns_true(self):
        sm = ActionExecutionStateMachine()
        assert sm.can_transition_to(ExecutionState.VALIDATING) is True
        assert sm.can_transition_to(ExecutionState.CANCELLED) is True

    def test_can_transition_to_returns_false(self):
        sm = ActionExecutionStateMachine()
        assert sm.can_transition_to(ExecutionState.SUCCEEDED) is False

    def test_full_success_path(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.VALIDATING)
        sm.transition_to(ExecutionState.READY)
        sm.transition_to(ExecutionState.RUNNING)
        sm.transition_to(ExecutionState.SUCCEEDED)
        assert sm.state == ExecutionState.SUCCEEDED
        assert sm.state.is_terminal

    def test_full_failure_path(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.VALIDATING)
        sm.transition_to(ExecutionState.READY)
        sm.transition_to(ExecutionState.RUNNING)
        sm.transition_to(ExecutionState.FAILED)
        sm.transition_to(ExecutionState.COMPENSATING)
        sm.transition_to(ExecutionState.COMPENSATED)
        assert sm.state.is_terminal

    def test_retry_path(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.VALIDATING)
        sm.transition_to(ExecutionState.READY)
        sm.transition_to(ExecutionState.RUNNING)
        sm.transition_to(ExecutionState.RETRYING)
        sm.transition_to(ExecutionState.RUNNING)
        sm.transition_to(ExecutionState.SUCCEEDED)
        assert sm.state == ExecutionState.SUCCEEDED

    def test_dead_letter_path(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.VALIDATING)
        sm.transition_to(ExecutionState.READY)
        sm.transition_to(ExecutionState.RUNNING)
        sm.transition_to(ExecutionState.FAILED)
        sm.transition_to(ExecutionState.DEAD_LETTERED)
        assert sm.state.is_terminal

    def test_cancel_from_created(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.CANCELLED)
        assert sm.state == ExecutionState.CANCELLED
        assert sm.state.is_terminal

    def test_expire_from_created(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.EXPIRED)
        assert sm.state == ExecutionState.EXPIRED
        assert sm.state.is_terminal

    def test_fully_terminal_states_have_no_outgoing(self):
        fully_terminal = {
            ExecutionState.COMPENSATED,
            ExecutionState.CANCELLED,
            ExecutionState.DEAD_LETTERED,
            ExecutionState.EXPIRED,
        }
        for state in fully_terminal:
            assert len(VALID_TRANSITIONS.get(state, set())) == 0

    def test_illegal_transition_from_terminal(self):
        sm = ActionExecutionStateMachine(ExecutionState.SUCCEEDED)
        with pytest.raises(Exception):
            sm.transition_to(ExecutionState.RUNNING)

    def test_is_active_created(self):
        assert ExecutionState.CREATED.is_active

    def test_is_active_running(self):
        assert ExecutionState.RUNNING.is_active

    def test_terminal_not_active(self):
        assert not ExecutionState.SUCCEEDED.is_active
        assert not ExecutionState.FAILED.is_active

    def test_reset(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.VALIDATING)
        sm.reset()
        assert sm.state == ExecutionState.CREATED
        assert sm.metadata == {}

    def test_reset_custom(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.VALIDATING)
        sm.reset(ExecutionState.READY)
        assert sm.state == ExecutionState.READY

    def test_no_direct_succeeded_from_created(self):
        sm = ActionExecutionStateMachine()
        with pytest.raises(Exception):
            sm.transition_to(ExecutionState.SUCCEEDED)

    def test_no_direct_compensated_from_running(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.VALIDATING)
        sm.transition_to(ExecutionState.READY)
        sm.transition_to(ExecutionState.RUNNING)
        with pytest.raises(Exception):
            sm.transition_to(ExecutionState.COMPENSATED)

    def test_waiting_transitions(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.VALIDATING)
        sm.transition_to(ExecutionState.READY)
        sm.transition_to(ExecutionState.SCHEDULED)
        sm.transition_to(ExecutionState.WAITING)
        sm.transition_to(ExecutionState.RUNNING)
        assert sm.state == ExecutionState.RUNNING

    def test_metadata_isolation(self):
        sm = ActionExecutionStateMachine()
        meta = sm.metadata
        meta["external"] = "test"
        assert "external" not in sm.metadata

    def test_transition_from_ready_to_failed(self):
        sm = ActionExecutionStateMachine()
        sm.transition_to(ExecutionState.VALIDATING)
        sm.transition_to(ExecutionState.READY)
        sm.transition_to(ExecutionState.FAILED)
        assert sm.state == ExecutionState.FAILED
