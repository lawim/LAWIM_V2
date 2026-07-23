from lawim_runtime.interaction.correlation import CorrelationManager


def test_create_correlation():
    mgr = CorrelationManager()
    cid = mgr.create()
    assert cid != ""
    assert mgr.count() == 1


def test_get_correlation():
    mgr = CorrelationManager()
    cid = mgr.create()
    record = mgr.get(cid)
    assert record is not None
    assert record.correlation_id == cid


def test_update():
    mgr = CorrelationManager()
    cid = mgr.create()
    mgr.update(cid, session_id="sess-001", project_id="proj-001")
    record = mgr.get(cid)
    assert record is not None
    assert record.session_id == "sess-001"
    assert record.project_id == "proj-001"
