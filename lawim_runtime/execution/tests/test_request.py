from __future__ import annotations

from lawim_runtime.execution.request import ActionExecutionRequest


class TestActionExecutionRequest:
    def test_default_construction(self):
        req = ActionExecutionRequest()
        assert req.execution_request_id
        assert req.action_code == ""
        assert req.priority == 100

    def test_idempotency_key_generation(self):
        key = ActionExecutionRequest.create_idempotency_key(
            project_id="proj-1", action_code="action-1"
        )
        assert isinstance(key, str)
        assert len(key) == 32

    def test_idempotency_key_deterministic_with_decision(self):
        key1 = ActionExecutionRequest.create_idempotency_key(
            project_id="proj-1", action_code="action-1", decision_id="dec-1"
        )
        key2 = ActionExecutionRequest.create_idempotency_key(
            project_id="proj-1", action_code="action-1", decision_id="dec-1"
        )
        assert key1 == key2

    def test_idempotency_key_differs_without_decision(self):
        key1 = ActionExecutionRequest.create_idempotency_key(
            project_id="proj-1", action_code="action-1"
        )
        key2 = ActionExecutionRequest.create_idempotency_key(
            project_id="proj-1", action_code="action-1"
        )
        assert key1 != key2  # each call generates a random suffix

    def test_frozen_by_convention(self):
        req = ActionExecutionRequest(action_code="test")
        assert req.action_code == "test"

    def test_requested_at_set(self):
        req = ActionExecutionRequest()
        assert req.requested_at != ""
