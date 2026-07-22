from __future__ import annotations

from lawim_runtime.execution.audit import AuditEntry, AuditTrail


class TestAuditTrail:
    def test_record_entry(self):
        trail = AuditTrail()
        entry = AuditEntry(
            entry_id="a1",
            execution_id="exec-1",
            action="test_action",
            actor="system",
        )
        trail.record(entry)
        assert trail.count() == 1

    def test_list_for_execution(self):
        trail = AuditTrail()
        trail.record(AuditEntry(entry_id="a1", execution_id="exec-1", action="act1", actor="sys"))
        trail.record(AuditEntry(entry_id="a2", execution_id="exec-2", action="act2", actor="sys"))
        entries = trail.list_for_execution("exec-1")
        assert len(entries) == 1

    def test_list_all(self):
        trail = AuditTrail()
        trail.record(AuditEntry(entry_id="a1", execution_id="exec-1", action="act1", actor="sys"))
        assert len(trail.list_all()) == 1

    def test_clear(self):
        trail = AuditTrail()
        trail.record(AuditEntry(entry_id="a1", execution_id="exec-1", action="act1", actor="sys"))
        trail.clear()
        assert trail.count() == 0
