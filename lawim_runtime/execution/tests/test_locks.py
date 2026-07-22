from __future__ import annotations

import time

from lawim_runtime.execution.locking.locks import ActionLockManager, LockScope


class TestActionLockManager:
    def test_acquire_lock(self):
        mgr = ActionLockManager()
        assert mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1") is True

    def test_acquire_existing_lock_fails(self):
        mgr = ActionLockManager()
        mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1")
        assert mgr.acquire(LockScope.PROJECT, "proj-1", "worker-2") is False

    def test_release_lock(self):
        mgr = ActionLockManager()
        mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1")
        assert mgr.release(LockScope.PROJECT, "proj-1", "worker-1") is True

    def test_release_wrong_owner_fails(self):
        mgr = ActionLockManager()
        mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1")
        assert mgr.release(LockScope.PROJECT, "proj-1", "worker-2") is False

    def test_release_nonexistent(self):
        mgr = ActionLockManager()
        assert mgr.release(LockScope.PROJECT, "ghost", "worker-1") is False

    def test_is_locked(self):
        mgr = ActionLockManager()
        mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1")
        assert mgr.is_locked(LockScope.PROJECT, "proj-1") is True

    def test_is_locked_released(self):
        mgr = ActionLockManager()
        mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1")
        mgr.release(LockScope.PROJECT, "proj-1", "worker-1")
        assert mgr.is_locked(LockScope.PROJECT, "proj-1") is False

    def test_lock_expires(self):
        mgr = ActionLockManager()
        mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1", ttl_seconds=1)
        time.sleep(1.1)
        assert mgr.is_locked(LockScope.PROJECT, "proj-1") is False

    def test_get_owner(self):
        mgr = ActionLockManager()
        mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1")
        assert mgr.get_owner(LockScope.PROJECT, "proj-1") == "worker-1"

    def test_get_owner_none(self):
        mgr = ActionLockManager()
        assert mgr.get_owner(LockScope.PROJECT, "ghost") is None

    def test_list_locks(self):
        mgr = ActionLockManager()
        mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1")
        mgr.acquire(LockScope.ACTION, "action-1", "worker-2")
        locks = mgr.list_locks()
        assert len(locks) == 2

    def test_list_locks_filtered(self):
        mgr = ActionLockManager()
        mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1")
        mgr.acquire(LockScope.ACTION, "action-1", "worker-2")
        locks = mgr.list_locks(LockScope.PROJECT)
        assert len(locks) == 1

    def test_clear_expired(self):
        mgr = ActionLockManager()
        mgr.acquire(LockScope.PROJECT, "p1", "w1", ttl_seconds=1)
        mgr.acquire(LockScope.ACTION, "a1", "w2", ttl_seconds=30)
        time.sleep(1.1)
        cleared = mgr.clear_expired()
        assert cleared >= 1

    def test_clear(self):
        mgr = ActionLockManager()
        mgr.acquire(LockScope.PROJECT, "proj-1", "worker-1")
        mgr.clear()
        assert mgr.list_locks() == []
