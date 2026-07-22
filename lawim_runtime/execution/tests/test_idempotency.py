from __future__ import annotations

import pytest

from lawim_runtime.execution.idempotency import (
    IdempotencyConflictError,
    IdempotencyManager,
)


class TestIdempotencyManager:
    def test_generate_key(self):
        mgr = IdempotencyManager()
        key = mgr.generate_key("ns", "id")
        assert isinstance(key, str)
        assert len(key) == 32

    def test_reserve_new_key(self):
        mgr = IdempotencyManager()
        record = mgr.reserve_key("key-1", "exec-1")
        assert record.status == "RESERVED"
        assert record.execution_id == "exec-1"

    def test_reserve_same_key_same_execution(self):
        mgr = IdempotencyManager()
        mgr.reserve_key("key-1", "exec-1")
        record = mgr.reserve_key("key-1", "exec-1")
        assert record.status == "RESERVED"

    def test_reserve_same_key_different_execution_raises(self):
        mgr = IdempotencyManager()
        mgr.reserve_key("key-1", "exec-1")
        with pytest.raises(IdempotencyConflictError):
            mgr.reserve_key("key-1", "exec-2")

    def test_mark_started(self):
        mgr = IdempotencyManager()
        mgr.reserve_key("key-1", "exec-1")
        record = mgr.mark_started("key-1")
        assert record.status == "STARTED"

    def test_mark_succeeded(self):
        mgr = IdempotencyManager()
        mgr.reserve_key("key-1", "exec-1")
        mgr.mark_started("key-1")
        record = mgr.mark_succeeded("key-1")
        assert record.status == "SUCCEEDED"

    def test_mark_failed(self):
        mgr = IdempotencyManager()
        mgr.reserve_key("key-1", "exec-1")
        mgr.mark_started("key-1")
        record = mgr.mark_failed("key-1")
        assert record.status == "FAILED"

    def test_mark_nonexistent_returns_none(self):
        mgr = IdempotencyManager()
        assert mgr.mark_started("ghost") is None
        assert mgr.mark_succeeded("ghost") is None
        assert mgr.mark_failed("ghost") is None

    def test_release_key(self):
        mgr = IdempotencyManager()
        mgr.reserve_key("key-1", "exec-1")
        assert mgr.release_key("key-1") is True
        assert mgr.release_key("key-1") is False

    def test_has_key(self):
        mgr = IdempotencyManager()
        mgr.reserve_key("key-1", "exec-1")
        assert mgr.has_key("key-1") is True
        assert mgr.has_key("ghost") is False

    def test_count(self):
        mgr = IdempotencyManager()
        assert mgr.count() == 0
        mgr.reserve_key("k1", "e1")
        mgr.reserve_key("k2", "e2")
        assert mgr.count() == 2

    def test_clear(self):
        mgr = IdempotencyManager()
        mgr.reserve_key("k1", "e1")
        mgr.clear()
        assert mgr.count() == 0

    def test_full_lifecycle(self):
        mgr = IdempotencyManager()
        mgr.reserve_key("key-1", "exec-1")
        mgr.mark_started("key-1")
        mgr.mark_succeeded("key-1")
        record = mgr.get_record("key-1")
        assert record.status == "SUCCEEDED"
