from lawim_runtime.interaction.session import SessionManager, SessionStatus


def test_create_session():
    mgr = SessionManager()
    session = mgr.create_session("user-001", "whatsapp")
    assert session.user_id == "user-001"
    assert session.channel == "whatsapp"
    assert session.status == SessionStatus.ACTIVE
    assert session.session_id != ""


def test_resume_or_create_new():
    mgr = SessionManager()
    session = mgr.resume_or_create("user-001", "whatsapp")
    assert session.status == SessionStatus.ACTIVE


def test_resume_existing():
    mgr = SessionManager()
    s1 = mgr.create_session("user-001", "whatsapp")
    s2 = mgr.resume_or_create("user-001", "whatsapp")
    assert s2.session_id == s1.session_id


def test_close_session():
    mgr = SessionManager()
    session = mgr.create_session("user-001", "whatsapp")
    mgr.close_session(session.session_id)
    closed = mgr.get_session(session.session_id)
    assert closed is None or closed.status == SessionStatus.CLOSED


def test_list_active():
    mgr = SessionManager(timeout_minutes=60)
    mgr.create_session("user-001", "whatsapp")
    mgr.create_session("user-002", "telegram")
    active = mgr.list_active()
    assert len(active) == 2


def test_count_active():
    mgr = SessionManager(timeout_minutes=60)
    mgr.create_session("user-001", "whatsapp")
    assert mgr.count_active() == 1
