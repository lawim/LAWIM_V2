from __future__ import annotations

from unittest.mock import MagicMock

from lawim_runtime.execution.replay import ExecutionReplayService
from lawim_runtime.execution.request import ActionExecutionRequest
from lawim_runtime.execution.result import ActionExecutionResult, ExecutionStatus


class TestExecutionReplayService:
    def test_no_repository_returns_divergence(self):
        service = ExecutionReplayService()
        result = service.replay("exec-1")
        assert result.match is False
        assert "No repository" in result.divergences[0]["error"]

    def test_execution_not_found(self):
        repo = MagicMock()
        repo.get_execution.return_value = None
        service = ExecutionReplayService(repository=repo)
        result = service.replay("exec-1")
        assert result.match is False
        assert "not found" in result.divergences[0]["error"]

    def test_no_handler_returns_skipped(self):
        repo = MagicMock()
        repo.get_execution.return_value = MagicMock(
            status=ExecutionStatus.SUCCEEDED,
            request=ActionExecutionRequest(action_code="test").__dict__,
        )
        service = ExecutionReplayService(repository=repo)
        result = service.replay("exec-1")
        assert result.replayed_status == "skipped"

    def test_dry_run_does_not_check_status(self):
        repo = MagicMock()
        original = MagicMock()
        original.status = ExecutionStatus.SUCCEEDED
        original.request = ActionExecutionRequest(action_code="test").__dict__
        repo.get_execution.return_value = original

        def handler(req):
            return ActionExecutionResult(status=ExecutionStatus.FAILED)

        service = ExecutionReplayService(repository=repo)
        result = service.replay("exec-1", dry_run=True, handler=handler)
        assert result.match is True

    def test_replay_matches(self):
        repo = MagicMock()
        original = MagicMock()
        original.status = ExecutionStatus.SUCCEEDED
        original.request = ActionExecutionRequest(action_code="test").__dict__
        repo.get_execution.return_value = original

        def handler(req):
            return ActionExecutionResult(status=ExecutionStatus.SUCCEEDED)

        service = ExecutionReplayService(repository=repo)
        result = service.replay("exec-1", dry_run=False, handler=handler)
        assert result.match is True

    def test_replay_diverges(self):
        repo = MagicMock()
        original = MagicMock()
        original.status = ExecutionStatus.SUCCEEDED
        original.request = ActionExecutionRequest(action_code="test").__dict__
        repo.get_execution.return_value = original

        def handler(req):
            return ActionExecutionResult(status=ExecutionStatus.FAILED)

        service = ExecutionReplayService(repository=repo)
        result = service.replay("exec-1", dry_run=False, handler=handler)
        assert result.match is False

    def test_replay_handler_exception(self):
        repo = MagicMock()
        original = MagicMock()
        original.status = ExecutionStatus.SUCCEEDED
        original.request = ActionExecutionRequest(action_code="test").__dict__
        repo.get_execution.return_value = original

        def handler(req):
            raise RuntimeError("handler crash")

        service = ExecutionReplayService(repository=repo)
        result = service.replay("exec-1", dry_run=True, handler=handler)
        assert result.match is False
        assert len(result.steps) == 1
        assert result.steps[0].status == "error"

    def test_simulate_calls_handler(self):
        service = ExecutionReplayService()
        req = ActionExecutionRequest(action_code="test")

        def handler(req):
            return ActionExecutionResult(status=ExecutionStatus.SUCCEEDED)

        result = service.simulate(req, handler)
        assert result.status == ExecutionStatus.SUCCEEDED
