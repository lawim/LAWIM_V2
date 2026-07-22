from __future__ import annotations

from lawim_runtime.execution.compensation import (
    CompensationAction,
    CompensationEngine,
    CompensationPlan,
    CompensationStatus,
)


def _success_handler(action, context):
    return {"compensated": action.action_code}


def _fail_handler(action, context):
    raise RuntimeError("compensation failed")


class TestCompensationEngine:
    def test_empty_plan_skipped(self):
        engine = CompensationEngine()
        plan = CompensationPlan(execution_id="exec-1")
        result = engine.execute_compensation(plan)
        assert result.status == CompensationStatus.SKIPPED

    def test_single_action_succeeds(self):
        engine = CompensationEngine()
        engine.register_handler("action-1", _success_handler)
        plan = CompensationPlan(execution_id="exec-1")
        plan.add_action(CompensationAction(action_code="action-1", handler_name="h1"))
        result = engine.execute_compensation(plan)
        assert result.status == CompensationStatus.SUCCEEDED

    def test_action_fails_required(self):
        engine = CompensationEngine()
        engine.register_handler("action-1", _fail_handler)
        plan = CompensationPlan(execution_id="exec-1")
        plan.add_action(CompensationAction(action_code="action-1", handler_name="h1"))
        result = engine.execute_compensation(plan)
        assert result.status == CompensationStatus.FAILED or result.status == CompensationStatus.PARTIAL

    def test_unregistered_handler_skipped(self):
        engine = CompensationEngine()
        plan = CompensationPlan(execution_id="exec-1")
        plan.add_action(CompensationAction(action_code="unknown", handler_name="h1"))
        result = engine.execute_compensation(plan)
        assert result.status == CompensationStatus.PARTIAL

    def test_mixed_results_partial(self):
        engine = CompensationEngine()
        engine.register_handler("ok", _success_handler)
        engine.register_handler("fail", _fail_handler)
        plan = CompensationPlan(execution_id="exec-1")
        plan.add_action(CompensationAction(action_code="ok", handler_name="h1", order=1))
        plan.add_action(CompensationAction(action_code="fail", handler_name="h2", order=2, required=True))
        result = engine.execute_compensation(plan)
        assert result.requires_attention is True

    def test_execution_order(self):
        engine = CompensationEngine()
        order = []

        def _ordered_handler(action, context):
            order.append(action.action_code)
            return {}

        engine.register_handler("first", _ordered_handler)
        engine.register_handler("second", _ordered_handler)
        plan = CompensationPlan(execution_id="exec-1")
        plan.add_action(CompensationAction(action_code="second", handler_name="h2", order=2))
        plan.add_action(CompensationAction(action_code="first", handler_name="h1", order=1))
        engine.execute_compensation(plan)
        assert order == ["first", "second"]

    def test_can_compensate(self):
        engine = CompensationEngine()
        engine.register_handler("action-1", _success_handler)
        assert engine.can_compensate("action-1") is True
        assert engine.can_compensate("unknown") is False
