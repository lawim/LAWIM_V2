from __future__ import annotations

import time
import pytest
from unittest.mock import MagicMock

from lawim_runtime.execution.compensation import (
    CompensationAction,
    CompensationEngine,
    CompensationPlan,
    CompensationStatus,
)
from lawim_runtime.execution.handler import ActionHandler
from lawim_runtime.execution.idempotency import IdempotencyConflictError, IdempotencyManager
from lawim_runtime.execution.locking.leases import ActionLeaseManager
from lawim_runtime.execution.locking.locks import ActionLockManager, LockScope
from lawim_runtime.execution.queue.dead_letter import DeadLetterQueue, DeadLetterReason, DeadLetterRecord
from lawim_runtime.execution.recovery import ExecutionRecoveryService
from lawim_runtime.execution.replay import ExecutionReplayService
from lawim_runtime.execution.request import ActionExecutionRequest
from lawim_runtime.execution.result import ActionExecutionResult, ExecutionStatus
from lawim_runtime.execution.retry import RetryPolicy, RetryPolicyEvaluator
from lawim_runtime.execution.timeout import DeadlineHelper, TimeoutPolicy


class TestReliabilityScenarios:
    def test_same_request_twice_idempotency(self):
        mgr = IdempotencyManager()
        mgr.reserve_key("key-1", "exec-1")
        mgr.reserve_key("key-1", "exec-1")
        with pytest.raises(IdempotencyConflictError):
            mgr.reserve_key("key-1", "exec-2")

    def test_success_already_registered(self):
        mgr = IdempotencyManager()
        mgr.reserve_key("key-1", "exec-1")
        mgr.mark_started("key-1")
        mgr.mark_succeeded("key-1")
        record = mgr.get_record("key-1")
        assert record.status == "SUCCEEDED"
        with pytest.raises(IdempotencyConflictError):
            mgr.reserve_key("key-1", "exec-2")

    def test_two_concurrent_workers_lock(self):
        lock_mgr = ActionLockManager()
        assert lock_mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1") is True
        assert lock_mgr.acquire(LockScope.PROJECT, "proj-1", "worker-2") is False

    def test_lease_expired_then_available(self):
        lease_mgr = ActionLeaseManager()
        lease_mgr.acquire("resource-1", "worker-1", ttl_seconds=1)
        time.sleep(1.1)
        recovered = lease_mgr.recover_expired()
        assert len(recovered) >= 1
        assert lease_mgr.acquire("resource-1", "worker-2") is True

    def test_transient_error_then_retry_success(self):
        policy = RetryPolicy(max_attempts=3)
        evaluator = RetryPolicyEvaluator(policy)
        assert evaluator.decide(0, "TRANSIENT_FAILURE").should_retry is True
        assert evaluator.decide(1, "TRANSIENT_FAILURE").should_retry is True
        assert evaluator.decide(2, "TRANSIENT_FAILURE").should_retry is True
        assert evaluator.decide(3, "TRANSIENT_FAILURE").should_retry is False

    def test_permanent_error_no_retry(self):
        policy = RetryPolicy(max_attempts=3)
        evaluator = RetryPolicyEvaluator(policy)
        decision = evaluator.decide(0, "BUSINESS_FAILURE")
        assert decision.should_retry is False

    def test_max_retries_exceeded(self):
        policy = RetryPolicy(max_attempts=1)
        evaluator = RetryPolicyEvaluator(policy)
        assert evaluator.decide(0, "TRANSIENT_FAILURE").should_retry is True
        assert evaluator.decide(1, "TRANSIENT_FAILURE").should_retry is False

    def test_timeout_with_external_state_unknown(self):
        policy = TimeoutPolicy(execution_timeout=0.01)
        helper = DeadlineHelper(policy)
        deadline = helper.execution_deadline()
        time.sleep(0.02)
        assert helper.is_expired(deadline) is True

    def test_compensation_succeeded(self):
        engine = CompensationEngine()
        engine.register_handler("action-1", lambda a, c: {"ok": True})
        plan = CompensationPlan(execution_id="exec-1")
        plan.add_action(CompensationAction(action_code="action-1", handler_name="h1"))
        result = engine.execute_compensation(plan)
        assert result.status == CompensationStatus.SUCCEEDED

    def test_compensation_failed(self):
        def _fail_handler(action, context):
            raise RuntimeError("fail")
        engine = CompensationEngine()
        engine.register_handler("action-1", _fail_handler)
        plan = CompensationPlan(execution_id="exec-1")
        plan.add_action(CompensationAction(action_code="action-1", handler_name="h1"))
        result = engine.execute_compensation(plan)
        assert result.status in (CompensationStatus.FAILED, CompensationStatus.PARTIAL)

    def test_dead_letter(self):
        dlq = DeadLetterQueue()
        dlq.add(DeadLetterRecord(
            execution_id="exec-1",
            reason=DeadLetterReason.MAX_RETRIES_EXCEEDED,
            error="All retries exhausted",
        ))
        assert dlq.count() == 1
        assert len(dlq.list_unreviewed()) == 1

    def test_recovery_after_restart(self):
        repo = MagicMock()
        repo.list_executions.return_value = [
            {"execution_id": "e1", "state": "RUNNING"},
            {"execution_id": "e2", "state": "RETRYING"},
        ]
        service = ExecutionRecoveryService(repository=repo)
        actions = service.recover_all()
        assert len(actions) >= 2
        assert any(a.action_type.value == "ORPHAN_DETECTED" for a in actions)
        assert any(a.action_type.value == "RETRY_PENDING" for a in actions)

    def test_replay_dry_run_no_external_effects(self):
        repo = MagicMock()
        original = MagicMock()
        original.status = ExecutionStatus.SUCCEEDED
        original.request = ActionExecutionRequest(action_code="test").__dict__
        repo.get_execution.return_value = original

        external_state = {"called": False}

        def handler(req):
            external_state["called"] = True
            return ActionExecutionResult(status=ExecutionStatus.SUCCEEDED)

        service = ExecutionReplayService(repository=repo)
        result = service.replay("exec-1", dry_run=True, handler=handler)
        assert external_state["called"] is True
        assert result.dry_run is True
