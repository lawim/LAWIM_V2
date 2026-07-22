from __future__ import annotations

import pytest

from lawim_runtime.execution.dispatcher import ExecutionDispatcher
from lawim_runtime.execution.handler import ActionHandler
from lawim_runtime.execution.plan import ActionExecutionPlan
from lawim_runtime.execution.request import ActionExecutionRequest
from lawim_runtime.execution.result import ExecutionStatus


class _SuccessHandler(ActionHandler):
    handler_name = "success_handler"
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
        return {"compensated": True}


class _ValidationFailHandler(ActionHandler):
    handler_name = "validation_fail_handler"
    supported_actions = ["test_action"]

    def can_handle(self, action_code):
        return True

    def validate(self, context):
        return ["error_1", "error_2"]

    def prepare(self, context):
        return {}

    def execute(self, context):
        return {}

    def verify(self, context, raw_result):
        return True

    def compensate(self, context, result):
        return {}


class _ExecuteFailHandler(ActionHandler):
    handler_name = "execute_fail_handler"
    supported_actions = ["test_action"]

    def can_handle(self, action_code):
        return True

    def validate(self, context):
        return []

    def prepare(self, context):
        return {}

    def execute(self, context):
        raise ValueError("execution failed")

    def verify(self, context, raw_result):
        return True

    def compensate(self, context, result):
        return {"compensated": True}


class _VerifyFailHandler(ActionHandler):
    handler_name = "verify_fail_handler"
    supported_actions = ["test_action"]
    supports_compensation = True

    def can_handle(self, action_code):
        return True

    def validate(self, context):
        return []

    def prepare(self, context):
        return {}

    def execute(self, context):
        return {"result": "bad"}

    def verify(self, context, raw_result):
        return False

    def compensate(self, context, result):
        return {"compensated": True}


class TestExecutionDispatcher:
    def test_dispatch_count_starts_at_zero(self):
        dispatcher = ExecutionDispatcher()
        assert dispatcher.dispatch_count == 0

    def test_successful_dispatch(self):
        dispatcher = ExecutionDispatcher()
        req = ActionExecutionRequest(action_code="test_action")
        handler = _SuccessHandler()
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test_action")

        result = dispatcher.dispatch(req, handler, plan)

        assert result.status == ExecutionStatus.SUCCEEDED
        assert result.output["result"] == "ok"
        assert dispatcher.dispatch_count == 1

    def test_validation_failure(self):
        dispatcher = ExecutionDispatcher()
        req = ActionExecutionRequest(action_code="test_action")
        handler = _ValidationFailHandler()
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test_action")

        result = dispatcher.dispatch(req, handler, plan)

        assert result.status == ExecutionStatus.FAILED
        assert result.failure is not None

    def test_execution_exception(self):
        dispatcher = ExecutionDispatcher()
        req = ActionExecutionRequest(action_code="test_action")
        handler = _ExecuteFailHandler()
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test_action")

        result = dispatcher.dispatch(req, handler, plan)

        assert result.status == ExecutionStatus.FAILED
        assert "ValueError" in result.failure["error"]

    def test_verify_failure_compensates(self):
        dispatcher = ExecutionDispatcher()
        req = ActionExecutionRequest(action_code="test_action")
        handler = _VerifyFailHandler()
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test_action")

        result = dispatcher.dispatch(req, handler, plan)

        assert result.status == ExecutionStatus.COMPENSATED
        assert result.verification_passed is False
        assert result.compensation_required is True

    def test_dispatch_increments_count(self):
        dispatcher = ExecutionDispatcher()
        req = ActionExecutionRequest(action_code="test_action")
        handler = _SuccessHandler()
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test_action")

        dispatcher.dispatch(req, handler, plan)
        dispatcher.dispatch(req, handler, plan)
        assert dispatcher.dispatch_count == 2

    def test_services_passed_to_context(self):
        dispatcher = ExecutionDispatcher()
        req = ActionExecutionRequest(action_code="test_action")
        handler = _ServiceCheckingHandler()
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test_action")

        result = dispatcher.dispatch(req, handler, plan, services={"db": "connected"})
        assert result.status == ExecutionStatus.SUCCEEDED


class _ServiceCheckingHandler(ActionHandler):
    handler_name = "svc_check"
    supported_actions = ["test_action"]

    def can_handle(self, action_code):
        return True

    def validate(self, context):
        if "db" not in context.services:
            return ["missing db service"]
        return []

    def prepare(self, context):
        return {}

    def execute(self, context):
        return {"service_ok": True}

    def verify(self, context, raw_result):
        return True

    def compensate(self, context, result):
        return {}
