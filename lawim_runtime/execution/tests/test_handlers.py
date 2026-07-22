from __future__ import annotations

from lawim_runtime.execution.handlers.noop import NoopHandler
from lawim_runtime.execution.handlers.wait import WaitHandler
from lawim_runtime.execution.handlers.test_handlers import SuccessHandler, FailHandler, ValidationFailHandler
from lawim_runtime.execution.context import ActionExecutionContext
from lawim_runtime.execution.request import ActionExecutionRequest
from lawim_runtime.execution.result import ActionExecutionResult


class _TestContext:
    pass


class TestNoopHandler:
    def test_execute(self):
        handler = NoopHandler()
        ctx = ActionExecutionContext(
            request=ActionExecutionRequest(action_code="noop"),
        )
        result = handler.execute(ctx)
        assert result["executed"] is True

    def test_verify(self):
        handler = NoopHandler()
        assert handler.verify(None, {"executed": True}) is True


class TestSuccessHandler:
    def test_execute(self):
        handler = SuccessHandler()
        ctx = ActionExecutionContext(
            request=ActionExecutionRequest(action_code="test_success"),
        )
        result = handler.execute(ctx)
        assert result["status"] == "ok"

    def test_verify(self):
        handler = SuccessHandler()
        assert handler.verify(None, {"status": "ok"}) is True


class TestFailHandler:
    def test_execute_raises(self):
        handler = FailHandler()
        ctx = ActionExecutionContext(
            request=ActionExecutionRequest(action_code="test_fail"),
        )
        import pytest
        with pytest.raises(RuntimeError):
            handler.execute(ctx)

    def test_compensate(self):
        handler = FailHandler()
        result = handler.compensate(None, ActionExecutionResult())
        assert result["compensated"] is True


class TestValidationFailHandler:
    def test_validate_returns_errors(self):
        handler = ValidationFailHandler()
        ctx = ActionExecutionContext(
            request=ActionExecutionRequest(action_code="test_validation_fail"),
        )
        errors = handler.validate(ctx)
        assert len(errors) >= 1


class TestWaitHandler:
    def test_validate_without_duration(self):
        handler = WaitHandler()
        ctx = ActionExecutionContext(
            request=ActionExecutionRequest(action_code="wait"),
        )
        errors = handler.validate(ctx)
        assert len(errors) == 1

    def test_validate_with_duration(self):
        handler = WaitHandler()
        ctx = ActionExecutionContext(
            request=ActionExecutionRequest(action_code="wait", action_parameters={"duration": 1.0}),
        )
        errors = handler.validate(ctx)
        assert errors == []
