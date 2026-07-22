from __future__ import annotations

from lawim_runtime.execution.retry import (
    BackoffStrategy,
    RetryPolicy,
    RetryPolicyEvaluator,
)


class TestRetryPolicyEvaluator:
    def test_no_retry_for_permanent_error(self):
        policy = RetryPolicy(max_attempts=3)
        evaluator = RetryPolicyEvaluator(policy)
        decision = evaluator.decide(0, "VALIDATION_FAILURE")
        assert decision.should_retry is False

    def test_retry_for_transient_error(self):
        policy = RetryPolicy(max_attempts=3)
        evaluator = RetryPolicyEvaluator(policy)
        decision = evaluator.decide(0, "TRANSIENT_FAILURE")
        assert decision.should_retry is True

    def test_max_attempts_exceeded(self):
        policy = RetryPolicy(max_attempts=2)
        evaluator = RetryPolicyEvaluator(policy)
        decision = evaluator.decide(2, "TRANSIENT_FAILURE")
        assert decision.should_retry is False

    def test_retry_count_below_max(self):
        policy = RetryPolicy(max_attempts=3)
        evaluator = RetryPolicyEvaluator(policy)
        decision = evaluator.decide(1, "TRANSIENT_FAILURE")
        assert decision.should_retry is True

    def test_deadline_exceeded(self):
        policy = RetryPolicy(max_attempts=5, retry_deadline=10.0)
        evaluator = RetryPolicyEvaluator(policy)
        decision = evaluator.decide(0, "TRANSIENT_FAILURE", elapsed_time=15.0)
        assert decision.should_retry is False

    def test_backoff_fixed(self):
        policy = RetryPolicy(
            max_attempts=3,
            initial_delay=2.0,
            backoff_strategy=BackoffStrategy.FIXED,
            jitter=0.0,
        )
        evaluator = RetryPolicyEvaluator(policy)
        delay = evaluator.compute_delay(0)
        assert delay == 2.0
        delay = evaluator.compute_delay(5)
        assert delay == 2.0

    def test_backoff_linear(self):
        policy = RetryPolicy(
            max_attempts=3,
            initial_delay=1.0,
            backoff_strategy=BackoffStrategy.LINEAR,
            backoff_multiplier=2.0,
            jitter=0.0,
        )
        evaluator = RetryPolicyEvaluator(policy)
        delay = evaluator.compute_delay(0)
        assert delay == 1.0
        delay = evaluator.compute_delay(1)
        assert delay == 3.0
        delay = evaluator.compute_delay(2)
        assert delay == 5.0

    def test_backoff_exponential(self):
        policy = RetryPolicy(
            max_attempts=3,
            initial_delay=1.0,
            backoff_strategy=BackoffStrategy.EXPONENTIAL,
            backoff_multiplier=2.0,
            jitter=0.0,
        )
        evaluator = RetryPolicyEvaluator(policy)
        delay = evaluator.compute_delay(0)
        assert delay == 1.0
        delay = evaluator.compute_delay(1)
        assert delay == 2.0
        delay = evaluator.compute_delay(2)
        assert delay == 4.0

    def test_backoff_none(self):
        policy = RetryPolicy(
            max_attempts=3,
            backoff_strategy=BackoffStrategy.NONE,
            jitter=0.0,
        )
        evaluator = RetryPolicyEvaluator(policy)
        delay = evaluator.compute_delay(0)
        assert delay == 0.0

    def test_backoff_respects_max_delay(self):
        policy = RetryPolicy(
            max_attempts=10,
            initial_delay=10.0,
            backoff_strategy=BackoffStrategy.EXPONENTIAL,
            backoff_multiplier=10.0,
            max_delay=30.0,
            jitter=0.0,
        )
        evaluator = RetryPolicyEvaluator(policy)
        delay = evaluator.compute_delay(5)
        assert delay <= 30.0

    def test_jitter_applied(self):
        policy = RetryPolicy(
            max_attempts=3,
            initial_delay=10.0,
            backoff_strategy=BackoffStrategy.FIXED,
            jitter=0.5,
        )
        evaluator = RetryPolicyEvaluator(policy)
        delays = [evaluator.compute_delay(0) for _ in range(10)]
        assert any(d != 10.0 for d in delays)

    def test_non_retryable_on_retryable_list(self):
        policy = RetryPolicy(
            max_attempts=3,
            retryable_error_types=("TRANSIENT_FAILURE",),
        )
        evaluator = RetryPolicyEvaluator(policy)
        decision = evaluator.decide(0, "TIMEOUT_FAILURE")
        assert decision.should_retry is False

    def test_retry_decision_has_reason(self):
        policy = RetryPolicy(max_attempts=1)
        evaluator = RetryPolicyEvaluator(policy)
        decision = evaluator.decide(0, "TRANSIENT_FAILURE")
        assert decision.reason != ""
