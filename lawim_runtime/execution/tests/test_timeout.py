from __future__ import annotations

from datetime import datetime, timedelta, timezone

from lawim_runtime.execution.timeout import DeadlineHelper, TimeoutPolicy


class TestDeadlineHelper:
    def test_deadline_from_now(self):
        policy = TimeoutPolicy(prepare_timeout=5.0)
        helper = DeadlineHelper(policy)
        deadline = helper.deadline_from_now(10.0)
        dt = datetime.fromisoformat(deadline)
        assert dt.tzinfo is not None

    def test_is_expired_future_deadline(self):
        policy = TimeoutPolicy()
        helper = DeadlineHelper(policy)
        future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        assert helper.is_expired(future) is False

    def test_is_expired_past_deadline(self):
        policy = TimeoutPolicy()
        helper = DeadlineHelper(policy)
        past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        assert helper.is_expired(past) is True

    def test_is_expired_empty_string(self):
        policy = TimeoutPolicy()
        helper = DeadlineHelper(policy)
        assert helper.is_expired("") is False

    def test_is_expired_malformed(self):
        policy = TimeoutPolicy()
        helper = DeadlineHelper(policy)
        assert helper.is_expired("not-a-date") is False

    def test_remaining_seconds_future(self):
        policy = TimeoutPolicy()
        helper = DeadlineHelper(policy)
        future = (datetime.now(timezone.utc) + timedelta(seconds=60)).isoformat()
        remaining = helper.remaining_seconds(future)
        assert 55.0 <= remaining <= 65.0

    def test_remaining_seconds_past(self):
        policy = TimeoutPolicy()
        helper = DeadlineHelper(policy)
        past = (datetime.now(timezone.utc) - timedelta(seconds=60)).isoformat()
        assert helper.remaining_seconds(past) == 0.0

    def test_remaining_seconds_empty(self):
        policy = TimeoutPolicy()
        helper = DeadlineHelper(policy)
        assert helper.remaining_seconds("") == 0.0

    def test_prepare_deadline(self):
        policy = TimeoutPolicy(prepare_timeout=10.0)
        helper = DeadlineHelper(policy)
        deadline = helper.prepare_deadline()
        assert deadline != ""

    def test_execution_deadline(self):
        policy = TimeoutPolicy(execution_timeout=30.0)
        helper = DeadlineHelper(policy)
        deadline = helper.execution_deadline()
        assert deadline != ""

    def test_verify_deadline(self):
        policy = TimeoutPolicy(verify_timeout=15.0)
        helper = DeadlineHelper(policy)
        deadline = helper.verify_deadline()
        assert deadline != ""

    def test_global_deadline(self):
        policy = TimeoutPolicy(global_timeout=120.0)
        helper = DeadlineHelper(policy)
        deadline = helper.global_deadline()
        assert deadline != ""

    def test_policy_property(self):
        policy = TimeoutPolicy(execution_timeout=30.0)
        helper = DeadlineHelper(policy)
        assert helper.policy is policy
