from __future__ import annotations

from lawim_runtime.execution.engine import ExecutionEngine
from lawim_runtime.execution.handler import ActionHandler
from lawim_runtime.execution.registry import ActionHandlerRegistry
from lawim_runtime.execution.request import ActionExecutionRequest
from lawim_runtime.execution.result import ExecutionStatus


class _SimpleHandler(ActionHandler):
    handler_name = "simple"
    supported_actions = ["test"]

    def can_handle(self, action_code):
        return True
    def validate(self, context):
        return []
    def prepare(self, context):
        return {}
    def execute(self, context):
        return {"ok": True}
    def verify(self, context, raw_result):
        return True
    def compensate(self, context, result):
        return {}


class TestExecutionEngine:
    def test_disabled_by_default(self):
        engine = ExecutionEngine()
        assert engine.enabled is False
        assert engine.shadow_mode is True

    def test_disabled_returns_immediately(self):
        engine = ExecutionEngine(enabled=False)
        registry = ActionHandlerRegistry()
        registry.register_handler(_SimpleHandler())
        engine._registry = registry

        req = ActionExecutionRequest(action_code="test")
        result = engine.execute(req)
        assert result.status == ExecutionStatus.SUCCEEDED
        assert result.output["mode"] == "disabled"

    def test_shadow_mode_returns_simulated(self):
        engine = ExecutionEngine(enabled=True, shadow_mode=True)
        registry = ActionHandlerRegistry()
        registry.register_handler(_SimpleHandler())
        engine._registry = registry

        req = ActionExecutionRequest(action_code="test")
        result = engine.execute(req)
        assert result.status == ExecutionStatus.SUCCEEDED
        assert result.output["mode"] == "shadow"

    def test_real_execution(self):
        engine = ExecutionEngine(enabled=True, shadow_mode=False)
        registry = ActionHandlerRegistry()
        registry.register_handler(_SimpleHandler())
        engine._registry = registry

        req = ActionExecutionRequest(action_code="test")
        result = engine.execute(req)
        assert result.status == ExecutionStatus.SUCCEEDED

    def test_metrics_updated(self):
        engine = ExecutionEngine(enabled=True, shadow_mode=False)
        registry = ActionHandlerRegistry()
        registry.register_handler(_SimpleHandler())
        engine._registry = registry

        req = ActionExecutionRequest(action_code="test")
        engine.execute(req)
        assert engine.metrics.metrics.executions_started == 1

    def test_audit_recorded(self):
        engine = ExecutionEngine(enabled=True, shadow_mode=False)
        registry = ActionHandlerRegistry()
        registry.register_handler(_SimpleHandler())
        engine._registry = registry

        req = ActionExecutionRequest(action_code="test")
        engine.execute(req)
        assert engine.audit.count() >= 1

    def test_handler_not_found_propagates(self):
        engine = ExecutionEngine(enabled=True, shadow_mode=False)
        registry = ActionHandlerRegistry()
        engine._registry = registry

        req = ActionExecutionRequest(action_code="nonexistent")
        import pytest
        with pytest.raises(Exception):
            engine.execute(req)

    def test_shadow_mode_metrics(self):
        engine = ExecutionEngine(enabled=True, shadow_mode=True)
        registry = ActionHandlerRegistry()
        registry.register_handler(_SimpleHandler())
        engine._registry = registry

        req = ActionExecutionRequest(action_code="test")
        engine.execute(req)
        assert engine.metrics.metrics.executions_succeeded == 1
