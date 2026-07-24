from __future__ import annotations

import os
import tempfile

import pytest

from lawim_demo.ports import DemoUserPort, DemoAuthPort, DemoPropertyPort
from lawim_demo.adapters import V2UserAdapter, V2AuthAdapter, V2PropertyAdapter


@pytest.fixture
def db():
    with tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False) as f:
        db_path = f.name
    yield db_path
    os.unlink(db_path)

@pytest.fixture
def ua(db):
    return V2UserAdapter(db)

@pytest.fixture
def aa(ua):
    return V2AuthAdapter(ua)

@pytest.fixture
def pa(db):
    return V2PropertyAdapter(db)


class TestV2UserAdapter:
    def test_implements_port(self, ua):
        assert isinstance(ua, DemoUserPort)

    def test_create_user(self, ua):
        uid = ua.create_or_update("DEMO-TEST-USER-001", "test@demo.lawim.local", "Test User", "client", "Pass123", True)
        assert uid

    def test_create_noauth_user(self, ua):
        uid = ua.create_or_update("DEMO-TEST-NOAUTH-001", "noauth@demo.lawim.local", "NoAuth", "client", None, False)
        assert uid

    def test_find_by_ref(self, ua):
        ua.create_or_update("DEMO-TEST-FIND-001", "find@demo.lawim.local", "Find Me", "owner", "Pass", True)
        found = ua.find_by_ref("DEMO-TEST-FIND-001")
        assert found is not None
        assert found["full_name"] == "Find Me"

    def test_no_duplicate_on_second_create(self, ua):
        ua.create_or_update("DEMO-TEST-DUP-001", "dup@demo.lawim.local", "Original", "agent", "Pass", True)
        ua.create_or_update("DEMO-TEST-DUP-001", "dup@demo.lawim.local", "Original", "agent", "Pass", True)
        found = ua.find_by_ref("DEMO-TEST-DUP-001")
        assert found is not None


class TestV2AuthAdapter:
    def test_login_success(self, ua, aa):
        ua.create_or_update("DEMO-AUTH-CLIENT-001", "client@demo.lawim.local", "Client", "client", "Pass123", True)
        ok, code, uid = aa.verify("client@demo.lawim.local", "Pass123")
        assert ok, f"Auth failed: {code}"
        assert code == "LOGIN_SUCCESS"

    def test_wrong_password(self, ua, aa):
        ua.create_or_update("DEMO-AUTH-BADPW-001", "badpw@demo.lawim.local", "BadPW", "client", "Correct", True)
        ok, code, _ = aa.verify("badpw@demo.lawim.local", "Wrong")
        assert not ok
        assert code == "INVALID_CREDENTIALS"

    def test_noauth_login_disabled(self, ua, aa):
        ua.create_or_update("DEMO-AUTH-NOAUTH-001", "noauth@demo.lawim.local", "NoAuth", "client", None, False)
        ok, code, _ = aa.verify("noauth@demo.lawim.local", "AnyPass")
        assert not ok
        assert code == "ACCOUNT_LOGIN_DISABLED"

    def test_suspended_refused(self, ua, aa):
        ua.create_or_update("DEMO-AUTH-SUSP-001", "susp@demo.lawim.local", "Suspended", "owner", "Pass", True, "suspended")
        ok, code, _ = aa.verify("susp@demo.lawim.local", "Pass")
        assert not ok
        assert code == "ACCOUNT_SUSPENDED"

    def test_blocked_refused(self, ua, aa):
        ua.create_or_update("DEMO-AUTH-BLOCK-001", "block@demo.lawim.local", "Blocked", "agent", "Pass", True, "blocked")
        ok, code, _ = aa.verify("block@demo.lawim.local", "Pass")
        assert not ok
        assert code == "ACCOUNT_BLOCKED"

    def test_user_not_found(self, aa):
        ok, code, _ = aa.verify("ghost@demo.lawim.local", "Pass")
        assert not ok
        assert code == "USER_NOT_FOUND"

    def test_update_password(self, ua, aa):
        ua.create_or_update("DEMO-AUTH-ROTATE-001", "rotate@demo.lawim.local", "Rotate", "client", "OldPass", True)
        assert aa.verify("rotate@demo.lawim.local", "OldPass")[0]
        aa.update_password("rotate@demo.lawim.local", "NewPass")
        assert not aa.verify("rotate@demo.lawim.local", "OldPass")[0]
        assert aa.verify("rotate@demo.lawim.local", "NewPass")[0]


class TestV2PropertyAdapter:
    def test_implements_port(self, pa):
        assert isinstance(pa, DemoPropertyPort)

    def test_create_property(self, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-OWNER-001", "owner@demo.lawim.local", "Owner", "owner", "Pass", True)
        prop = pa.create(uid, uid, "APARTMENT", "RENT", "Yaoundé", "Mvan", 200000)
        assert prop["id"] is not None
        assert prop["city"] == "Yaoundé"
        assert prop["price"] == 200000.0

    def test_property_persists(self, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-PERSIST-001", "persist@demo.lawim.local", "Persist", "owner", "Pass", True)
        prop = pa.create(uid, uid, "HOUSE", "SELL", "Yaoundé", "Bastos", 50000000)
        pid = prop["id"]
        # Re-open connection (simulate service restart)
        pa2 = V2PropertyAdapter(pa._db_path)
        reloaded = pa2.find_by_id(pid)
        assert reloaded is not None
        assert reloaded["price"] == 50000000.0

    def test_property_lifecycle(self, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-LIFE-001", "life@demo.lawim.local", "Life", "owner", "Pass", True)
        prop = pa.create(uid, uid, "STUDIO", "RENT", "Douala", "Akwa", 150000)
        status = pa.transition(prop["id"], "published", uid)
        assert status == "OK"
        reloaded = pa.find_by_id(prop["id"])
        assert reloaded["status"] == "published"
