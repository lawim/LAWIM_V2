from __future__ import annotations

import pytest

from lawim_runtime.execution.dispatcher import ExecutionDispatcher
from lawim_runtime.execution.handler import ActionHandler
from lawim_runtime.execution.registry import ActionHandlerRegistry
from lawim_runtime.execution.request import ActionExecutionRequest
from lawim_runtime.execution.result import ExecutionStatus
from lawim_runtime.execution.worker import ExecutionWorker, WorkerError


class _TestHandler(ActionHandler):
    handler_name = "test_handler"
    supported_actions = ["test_action"]

    def can_handle(self, action_code):
        return True

    def validate(self, context):
        return []

    def prepare(self, context):
        return {"prepared": True}

    def execute(self, context):
        return {"result": "ok"}

    def verify(self, context, raw_result):
        return True

    def compensate(self, context, result):
        return {}


class _FailingHandler(ActionHandler):
    handler_name = "failing_handler"
    supported_actions = ["fail_action"]

    def can_handle(self, action_code):
        return True

    def validate(self, context):
        return []

    def prepare(self, context):
        return {}

    def execute(self, context):
        raise RuntimeError("handler failure")

    def verify(self, context, raw_result):
        return True

    def compensate(self, context, result):
        return {}


class TestExecutionWorker:
    def test_initial_state(self):
        worker = ExecutionWorker("test-worker")
        assert worker.name == "test-worker"
        assert worker.is_running is False
        assert worker.execution_count == 0
        assert worker.last_heartbeat is None
        assert worker.shutdown_requested is False

    def test_start_initializes(self):
        worker = ExecutionWorker()
        worker.start()
        assert worker.is_running is True
        assert worker.shutdown_requested is False
        assert worker.last_heartbeat is not None

    def test_shutdown_stops_worker(self):
        worker = ExecutionWorker()
        worker.start()
        worker.shutdown()
        assert worker.is_running is False
        assert worker.shutdown_requested is True

    def test_execute_success(self):
        worker = ExecutionWorker()
        registry = ActionHandlerRegistry()
        registry.register_handler(_TestHandler())
        req = ActionExecutionRequest(action_code="test_action")

        result = worker.execute(req, registry)

        assert result.status == ExecutionStatus.SUCCEEDED

    def test_running_true_during_execution(self):
        running_values = []
        handler = _TestHandler()

        class _TrackingDispatcher(ExecutionDispatcher):
            def dispatch(self, execution_request, hnd, plan, services=None):
                running_values.append(worker.is_running)
                return super().dispatch(execution_request, hnd, plan, services)

        worker = ExecutionWorker(dispatcher=_TrackingDispatcher())
        registry = ActionHandlerRegistry()
        registry.register_handler(handler)
        req = ActionExecutionRequest(action_code="test_action")

        worker.execute(req, registry)
        assert running_values == [True]

    def test_running_false_after_success(self):
        worker = ExecutionWorker()
        worker.start()
        registry = ActionHandlerRegistry()
        registry.register_handler(_TestHandler())
        req = ActionExecutionRequest(action_code="test_action")

        worker.execute(req, registry)
        assert worker.is_running is False

    def test_running_false_after_exception(self):
        worker = ExecutionWorker()
        registry = ActionHandlerRegistry()
        registry.register_handler(_FailingHandler())
        req = ActionExecutionRequest(action_code="fail_action")

        worker.execute(req, registry)
        assert worker.is_running is False

    def test_heartbeat_updated(self):
        worker = ExecutionWorker()
        registry = ActionHandlerRegistry()
        registry.register_handler(_TestHandler())
        req = ActionExecutionRequest(action_code="test_action")

        before = worker.last_heartbeat
        result = worker.execute(req, registry)
        assert worker.last_heartbeat is not None
        if before is not None:
            assert worker.last_heartbeat >= before

    def test_execution_count_increments(self):
        worker = ExecutionWorker()
        registry = ActionHandlerRegistry()
        registry.register_handler(_TestHandler())
        req = ActionExecutionRequest(action_code="test_action")

        assert worker.execution_count == 0
        worker.execute(req, registry)
        assert worker.execution_count == 1
        worker.execute(req, registry)
        assert worker.execution_count == 2

    def test_handler_not_found_error(self):
        worker = ExecutionWorker()
        registry = ActionHandlerRegistry()
        req = ActionExecutionRequest(action_code="nonexistent")

        with pytest.raises(Exception):
            worker.execute(req, registry)

    def test_shutdown_blocks_execution(self):
        worker = ExecutionWorker()
        worker.shutdown()
        registry = ActionHandlerRegistry()
        req = ActionExecutionRequest(action_code="test_action")

        with pytest.raises(WorkerError, match="shut down"):
            worker.execute(req, registry)

    def test_dispatcher_injected_properly(self):
        dispatcher = ExecutionDispatcher()
        worker = ExecutionWorker(dispatcher=dispatcher)
        registry = ActionHandlerRegistry()
        registry.register_handler(_TestHandler())
        req = ActionExecutionRequest(action_code="test_action")

        worker.execute(req, registry)
        assert dispatcher.dispatch_count == 1

    def test_status_report(self):
        worker = ExecutionWorker("custom")
        status = worker.status()
        assert status["name"] == "custom"
        assert status["running"] is False
        assert status["execution_count"] == 0

    def test_heartbeat_method(self):
        worker = ExecutionWorker()
        hb = worker.heartbeat()
        assert hb is not None
        assert worker.last_heartbeat == hb

    def test_no_exception_masked(self):
        worker = ExecutionWorker()
        registry = ActionHandlerRegistry()
        registry.register_handler(_FailingHandler())
        req = ActionExecutionRequest(action_code="fail_action")
        result = worker.execute(req, registry)
        assert result.status == ExecutionStatus.FAILED
