from __future__ import annotations

from lawim_runtime.execution.dispatcher import ExecutionDispatcher
from lawim_runtime.execution.handler import ActionHandler
from lawim_runtime.execution.registry import ActionHandlerRegistry
from lawim_runtime.execution.request import ActionExecutionRequest
from lawim_runtime.execution.result import ExecutionStatus
from lawim_runtime.execution.worker import ExecutionWorker


class _FullHandler(ActionHandler):
    handler_name = "full_handler"
    supported_actions = ["action_1", "action_2"]

    def can_handle(self, action_code):
        return action_code in self.supported_actions

    def validate(self, context):
        if not context.request.action_parameters.get("valid"):
            return ["Validation failed: missing valid flag"]
        return []

    def prepare(self, context):
        return {"prepared": context.request.action_parameters}

    def execute(self, context):
        return {"executed": True, "input": context.request.action_parameters}

    def verify(self, context, raw_result):
        return raw_result.get("executed") is True

    def compensate(self, context, result):
        return {"compensated": True}


class TestIntegration:
    def test_full_success_path(self):
        dispatcher = ExecutionDispatcher()
        handler = _FullHandler()
        registry = ActionHandlerRegistry()
        registry.register_handler(handler)
        worker = ExecutionWorker("integration-worker", dispatcher=dispatcher)

        req = ActionExecutionRequest(
            action_code="action_1",
            action_parameters={"valid": True, "data": "test"},
        )

        result = worker.execute(req, registry)
        assert result.status == ExecutionStatus.SUCCEEDED
        assert result.output["executed"] is True
        assert worker.execution_count == 1
        assert dispatcher.dispatch_count == 1

    def test_validation_failure_integration(self):
        registry = ActionHandlerRegistry()
        registry.register_handler(_FullHandler())
        worker = ExecutionWorker()

        req = ActionExecutionRequest(
            action_code="action_1",
            action_parameters={"valid": False},
        )

        result = worker.execute(req, registry)
        assert result.status == ExecutionStatus.FAILED

    def test_handler_not_found(self):
        registry = ActionHandlerRegistry()
        registry.register_handler(_FullHandler())
        worker = ExecutionWorker()

        req = ActionExecutionRequest(action_code="unknown_action")

        import pytest
        with pytest.raises(Exception):
            worker.execute(req, registry)

    def test_execution_idempotent_across_workers(self):
        dispatcher1 = ExecutionDispatcher()
        dispatcher2 = ExecutionDispatcher()
        handler = _FullHandler()
        registry = ActionHandlerRegistry()
        registry.register_handler(handler)

        worker1 = ExecutionWorker("worker-1", dispatcher=dispatcher1)
        worker2 = ExecutionWorker("worker-2", dispatcher=dispatcher2)

        req = ActionExecutionRequest(
            action_code="action_1",
            action_parameters={"valid": True},
        )

        result1 = worker1.execute(req, registry)
        result2 = worker2.execute(req, registry)

        assert result1.status == ExecutionStatus.SUCCEEDED
        assert result2.status == ExecutionStatus.SUCCEEDED

    def test_worker_shutdown_blocks(self):
        registry = ActionHandlerRegistry()
        registry.register_handler(_FullHandler())
        worker = ExecutionWorker()
        worker.shutdown()

        req = ActionExecutionRequest(action_code="action_1", action_parameters={"valid": True})

        import pytest
        with pytest.raises(Exception, match="shut down"):
            worker.execute(req, registry)

    def test_dispatcher_receives_correct_handler_and_plan(self):
        class _TrackingDispatcher(ExecutionDispatcher):
            def __init__(self):
                super().__init__()
                self.last_handler = None
                self.last_plan = None

            def dispatch(self, execution_request, handler, plan, services=None):
                self.last_handler = handler
                self.last_plan = plan
                return super().dispatch(execution_request, handler, plan, services)

        dispatcher = _TrackingDispatcher()
        handler = _FullHandler()
        registry = ActionHandlerRegistry()
        registry.register_handler(handler)
        worker = ExecutionWorker(dispatcher=dispatcher)

        req = ActionExecutionRequest(action_code="action_1", action_parameters={"valid": True})
        worker.execute(req, registry)

        assert dispatcher.last_handler is handler
        assert dispatcher.last_plan.action_code == "action_1"

    def test_worker_heartbeat_after_execution(self):
        worker = ExecutionWorker()
        registry = ActionHandlerRegistry()
        registry.register_handler(_FullHandler())
        req = ActionExecutionRequest(action_code="action_1", action_parameters={"valid": True})

        worker.execute(req, registry)
        assert worker.last_heartbeat is not None
