from __future__ import annotations

import time

from lawim_runtime.execution.locking.leases import ActionLeaseManager, LeaseStatus


class TestActionLeaseManager:
    def test_acquire_lease(self):
        mgr = ActionLeaseManager()
        assert mgr.acquire("resource-1", "worker-1") is True

    def test_acquire_existing_lease_fails(self):
        mgr = ActionLeaseManager()
        mgr.acquire("resource-1", "worker-1")
        assert mgr.acquire("resource-1", "worker-2") is False

    def test_release_lease(self):
        mgr = ActionLeaseManager()
        mgr.acquire("resource-1", "worker-1")
        leases = mgr.list_active()
        assert len(leases) == 1
        mgr.release(leases[0].lease_id)
        assert len(mgr.list_active()) == 0

    def test_release_nonexistent(self):
        mgr = ActionLeaseManager()
        assert mgr.release("ghost") is False

    def test_renew_lease(self):
        mgr = ActionLeaseManager()
        mgr.acquire("resource-1", "worker-1")
        leases = mgr.list_active()
        assert mgr.renew(leases[0].lease_id) is True

    def test_renew_expired_lease_fails(self):
        mgr = ActionLeaseManager()
        mgr.acquire("resource-1", "worker-1", ttl_seconds=1)
        time.sleep(1.1)
        leases = mgr.list_active()
        mgr2 = ActionLeaseManager()
        mgr2.acquire("resource-1", "worker-2", ttl_seconds=1)
        time.sleep(1.1)
        active = mgr2.list_active()
        assert len(active) == 0

    def test_is_expired(self):
        mgr = ActionLeaseManager()
        mgr.acquire("resource-1", "worker-1")
        leases = mgr.list_all()
        assert mgr.is_expired(leases[0].lease_id) is False

    def test_is_expired_nonexistent(self):
        mgr = ActionLeaseManager()
        assert mgr.is_expired("ghost") is True

    def test_recover_expired(self):
        mgr = ActionLeaseManager()
        mgr.acquire("resource-1", "worker-1", ttl_seconds=1)
        time.sleep(1.1)
        recovered = mgr.recover_expired()
        assert len(recovered) >= 1
        assert recovered[0].status == LeaseStatus.RECOVERED

    def test_list_active(self):
        mgr = ActionLeaseManager()
        mgr.acquire("resource-1", "worker-1")
        assert len(mgr.list_active()) == 1

    def test_list_all(self):
        mgr = ActionLeaseManager()
        mgr.acquire("resource-1", "worker-1")
        assert len(mgr.list_all()) == 1

    def test_get_active_lease(self):
        mgr = ActionLeaseManager()
        mgr.acquire("resource-1", "worker-1")
        lease = mgr.get_active_lease("resource-1")
        assert lease is not None
        assert lease.owner == "worker-1"

    def test_get_active_lease_none(self):
        mgr = ActionLeaseManager()
        assert mgr.get_active_lease("ghost") is None

    def test_clear(self):
        mgr = ActionLeaseManager()
        mgr.acquire("resource-1", "worker-1")
        mgr.clear()
        assert mgr.list_all() == []

    def test_lease_has_remaining_seconds(self):
        mgr = ActionLeaseManager()
        mgr.acquire("resource-1", "worker-1", ttl_seconds=30)
        leases = mgr.list_all()
        assert 25.0 <= leases[0].remaining_seconds <= 30.0
