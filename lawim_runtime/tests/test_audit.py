from ..telemetry.audit import RuntimeAudit
from ..events.base import RuntimeEvent


def test_audit_record():
    a = RuntimeAudit()
    event = RuntimeEvent(event_type="TEST", project_id="p1", actor="user")
    before = {"status": "DRAFT"}
    after = {"status": "ACTIVE"}
    a.record(event, before, after)
    entries = a.get_entries("p1")
    assert len(entries) == 1
    assert entries[0].before["status"] == "DRAFT"
    assert entries[0].after["status"] == "ACTIVE"


def test_audit_filter():
    a = RuntimeAudit()
    a.record(RuntimeEvent(event_type="A", project_id="p1"), {}, {})
    a.record(RuntimeEvent(event_type="B", project_id="p2"), {}, {})
    assert len(a.get_entries("p1")) == 1
    assert len(a.get_entries()) == 2
