from __future__ import annotations

import pytest

from lawim_runtime.execution.plan import ActionExecutionPlan
from lawim_runtime.execution.request import ActionExecutionRequest
from lawim_runtime.execution.scheduler import ExecutionScheduler, SchedulerError


class TestExecutionScheduler:
    def test_initial_queue_empty(self):
        sched = ExecutionScheduler()
        assert sched.queue_size == 0
        assert sched.task_count == 0

    def test_schedule_task(self):
        sched = ExecutionScheduler()
        req = ActionExecutionRequest(action_code="test")
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test")
        schedule_id = sched.schedule(req, plan)
        assert schedule_id != ""
        assert sched.queue_size == 1
        assert sched.task_count == 1

    def test_dequeue_task(self):
        sched = ExecutionScheduler()
        req = ActionExecutionRequest(action_code="test")
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test")
        sched.schedule(req, plan)
        task = sched.dequeue()
        assert task is not None
        assert sched.queue_size == 0

    def test_dequeue_empty_returns_none(self):
        sched = ExecutionScheduler()
        assert sched.dequeue() is None

    def test_peek_returns_first(self):
        sched = ExecutionScheduler()
        req1 = ActionExecutionRequest(action_code="a1", priority=50)
        req2 = ActionExecutionRequest(action_code="a2", priority=10)
        plan1 = ActionExecutionPlan(plan_id="p1", execution_request_id=req1.execution_request_id, action_code="a1")
        plan2 = ActionExecutionPlan(plan_id="p2", execution_request_id=req2.execution_request_id, action_code="a2")
        sched.schedule(req1, plan1)
        sched.schedule(req2, plan2)
        task = sched.peek()
        assert task.request.action_code == "a2"  # higher priority dequeued first

    def test_cancel_task(self):
        sched = ExecutionScheduler()
        req = ActionExecutionRequest(action_code="test")
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test")
        sid = sched.schedule(req, plan)
        assert sched.cancel(sid) is True
        assert sched.queue_size == 0

    def test_cancel_nonexistent(self):
        sched = ExecutionScheduler()
        assert sched.cancel("ghost") is False

    def test_get_task(self):
        sched = ExecutionScheduler()
        req = ActionExecutionRequest(action_code="test")
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test")
        sid = sched.schedule(req, plan)
        task = sched.get_task(sid)
        assert task is not None

    def test_get_task_nonexistent(self):
        sched = ExecutionScheduler()
        assert sched.get_task("ghost") is None

    def test_list_pending(self):
        sched = ExecutionScheduler()
        req = ActionExecutionRequest(action_code="test")
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test")
        sched.schedule(req, plan)
        assert len(sched.list_pending()) == 1

    def test_prioritize(self):
        sched = ExecutionScheduler()
        req1 = ActionExecutionRequest(action_code="a1", priority=100)
        plan1 = ActionExecutionPlan(plan_id="p1", execution_request_id=req1.execution_request_id, action_code="a1")
        sid = sched.schedule(req1, plan1, priority=100)
        sched.prioritize(sid, 1)
        assert sched.peek().priority == 1

    def test_prioritize_nonexistent(self):
        sched = ExecutionScheduler()
        with pytest.raises(SchedulerError):
            sched.prioritize("ghost", 1)

    def test_queue_full_raises(self):
        sched = ExecutionScheduler()
        sched._max_queue_size = 2
        req = ActionExecutionRequest(action_code="test")
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test")
        sched.schedule(req, plan)
        sched.schedule(req, plan)
        with pytest.raises(SchedulerError, match="full"):
            sched.schedule(req, plan)

    def test_clear(self):
        sched = ExecutionScheduler()
        req = ActionExecutionRequest(action_code="test")
        plan = ActionExecutionPlan(plan_id="p1", execution_request_id=req.execution_request_id, action_code="test")
        sched.schedule(req, plan)
        sched.clear()
        assert sched.queue_size == 0
        assert sched.task_count == 0
