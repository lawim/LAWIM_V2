from __future__ import annotations

from lawim_runtime.execution.snapshots import SnapshotManager


class TestSnapshotManager:
    def test_take_snapshot(self):
        mgr = SnapshotManager()
        snap = mgr.take_snapshot("exec-1", "RUNNING", {"key": "val"})
        assert snap.execution_id == "exec-1"
        assert snap.state == "RUNNING"
        assert snap.version == 1

    def test_get_latest(self):
        mgr = SnapshotManager()
        mgr.take_snapshot("exec-1", "CREATED", {})
        snap2 = mgr.take_snapshot("exec-1", "RUNNING", {"key": "val"})
        latest = mgr.get_latest("exec-1")
        assert latest is snap2

    def test_get_latest_none(self):
        mgr = SnapshotManager()
        assert mgr.get_latest("ghost") is None

    def test_list_for_execution(self):
        mgr = SnapshotManager()
        mgr.take_snapshot("exec-1", "CREATED", {})
        mgr.take_snapshot("exec-1", "RUNNING", {})
        assert len(mgr.list_for_execution("exec-1")) == 2

    def test_versions_increment(self):
        mgr = SnapshotManager()
        s1 = mgr.take_snapshot("exec-1", "CREATED", {})
        s2 = mgr.take_snapshot("exec-1", "RUNNING", {})
        assert s1.version == 1
        assert s2.version == 2
