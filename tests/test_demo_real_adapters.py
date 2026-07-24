from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from lawim_v2.db import LawimRepository
from lawim_v2.user_roles import accept_user_role

from lawim_demo.adapters import V2UserAdapter, V2AuthAdapter, V2PropertyAdapter, V2AuthorizationAdapter


@pytest.fixture
def db():
    with tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False) as f:
        db_path = Path(f.name)
    repo = LawimRepository(db_path)
    repo.initialize(seed_demo_data=False)
    yield str(db_path)
    os.unlink(str(db_path))


@pytest.fixture
def ua(db):
    return V2UserAdapter(db)

@pytest.fixture
def aa(ua):
    return V2AuthAdapter(ua)

@pytest.fixture
def pa(ua):
    return V2PropertyAdapter(ua)

@pytest.fixture
def authz(ua):
    return V2AuthorizationAdapter(ua)


class TestV2Roles:
    def test_commercial_role_accepted(self):
        assert accept_user_role("commercial") == "commercial"

    def test_auditor_role_accepted(self):
        assert accept_user_role("auditor") == "auditor"

    def test_super_admin_role_accepted(self):
        assert accept_user_role("super_admin") == "super_admin"

    def test_service_provider_role_accepted(self):
        assert accept_user_role("service_provider") == "service_provider"


class TestV2AuthStatus:
    def test_active_login_success(self, db, ua, aa):
        ua.create_or_update("DEMO-ACT-001", "act@demo.lawim.local", "Active", "client", "Pass123", True, "ACTIVE")
        ok, code, _ = aa.verify("act@demo.lawim.local", "Pass123")
        assert ok, f"Expected LOGIN_SUCCESS got {code}"
        assert code == "LOGIN_SUCCESS"

    def test_login_disabled_rejected(self, db, ua, aa):
        ua.create_or_update("DEMO-NOAUTH-001", "noauth@demo.lawim.local", "NoAuth", "client", None, False, "LOGIN_DISABLED")
        ok, code, _ = aa.verify("noauth@demo.lawim.local", "anything")
        assert not ok
        assert code == "ACCOUNT_LOGIN_DISABLED"

    def test_suspended_rejected(self, db, ua, aa):
        ua.create_or_update("DEMO-SUSP-001", "susp@demo.lawim.local", "Susp", "owner", "Pass", True, "SUSPENDED")
        ok, code, _ = aa.verify("susp@demo.lawim.local", "Pass")
        assert not ok
        assert code == "ACCOUNT_SUSPENDED"

    def test_blocked_rejected(self, db, ua, aa):
        ua.create_or_update("DEMO-BLK-001", "blk@demo.lawim.local", "Blk", "agent", "Pass", True, "BLOCKED")
        ok, code, _ = aa.verify("blk@demo.lawim.local", "Pass")
        assert not ok
        assert code == "ACCOUNT_BLOCKED"

    def test_wrong_password_rejected(self, db, ua, aa):
        ua.create_or_update("DEMO-WPW-001", "wpw@demo.lawim.local", "Wpw", "client", "Correct", True, "ACTIVE")
        ok, code, _ = aa.verify("wpw@demo.lawim.local", "Wrong")
        assert not ok
        assert code == "INVALID_CREDENTIALS"

    def test_user_not_found(self, aa):
        ok, code, _ = aa.verify("ghost@demo.lawim.local", "Pass")
        assert not ok
        assert code == "USER_NOT_FOUND"


class TestV2Authorization:
    def test_support_cannot_modify_payment(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-SUP-001", "sup@demo.lawim.local", "Support", "support", "Pass", True, "ACTIVE")
        assert not authz.check(uid, "payments:write")

    def test_commercial_cannot_create_admin(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-COM-001", "com@demo.lawim.local", "Commercial", "commercial", "Pass", True, "ACTIVE")
        assert not authz.check(uid, "users:write")

    def test_auditor_read_only(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-AUD-001", "aud@demo.lawim.local", "Auditor", "auditor", "Pass", True, "ACTIVE")
        assert authz.check(uid, "users:read")
        assert not authz.check(uid, "properties:write")

    def test_commercial_can_create_property(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-COM2-001", "com2@demo.lawim.local", "Commercial2", "commercial", "Pass", True, "ACTIVE")
        assert authz.check(uid, "properties:write")

    def test_admin_can_manage_users(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-ADM-001", "adm@demo.lawim.local", "Admin", "admin", "Pass", True, "ACTIVE")
        assert authz.check(uid, "users:write")

    def test_super_admin_has_all(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-SADM-001", "sadm@demo.lawim.local", "SuperAdmin", "super_admin", "Pass", True, "ACTIVE")
        assert authz.check(uid, "payments:write")


class TestV2PropertyAdapter:
    def test_owner_creates_apartment(self, db, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-OWN-001", "own@demo.lawim.local", "Owner", "owner", "Pass", True, "ACTIVE")
        prop = pa.create(uid, uid, "APARTMENT", "RENT", "Yaoundé", "Mvan", 200000)
        assert prop["id"] is not None
        assert prop["city"] == "Yaoundé"

    def test_agent_creates_house(self, db, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-AGT-001", "agt@demo.lawim.local", "Agent", "agent", "Pass", True, "ACTIVE")
        owner = ua.create_or_update("DEMO-PROP-OWN2-001", "own2@demo.lawim.local", "Owner2", "owner", "Pass", True, "ACTIVE")
        prop = pa.create(owner, uid, "HOUSE", "SELL", "Yaoundé", "Bastos", 50000000)
        assert prop["id"] is not None

    def test_commercial_creates_studio(self, db, ua, pa):
        cid = ua.create_or_update("DEMO-PROP-COM-001", "com@demo.lawim.local", "Commercial", "commercial", "Pass", True, "ACTIVE")
        owner = ua.create_or_update("DEMO-PROP-OWN3-001", "own3@demo.lawim.local", "Owner3", "owner", "Pass", True, "ACTIVE")
        prop = pa.create(owner, cid, "STUDIO", "RENT", "Douala", "Akwa", 150000)
        assert prop["id"] is not None

    def test_admin_creates_land(self, db, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-ADM-001", "adm@demo.lawim.local", "Admin", "admin", "Pass", True, "ACTIVE")
        prop = pa.create(uid, uid, "LAND", "SELL", "Yaoundé", "Nkoabang", 10000000)
        assert prop["id"] is not None

    def test_property_persists_after_reopen(self, db, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-PERSIST-001", "persist@demo.lawim.local", "Persist", "owner", "Pass", True, "ACTIVE")
        prop = pa.create(uid, uid, "APARTMENT", "RENT", "Yaoundé", "Mvan", 200000)
        pid = prop["id"]
        pa2 = V2PropertyAdapter(V2UserAdapter(db))
        reloaded = pa2.find_by_id(pid)
        assert reloaded is not None
        assert reloaded["price_min"] == 200000

    def test_property_lifecycle(self, db, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-LIFE-001", "life@demo.lawim.local", "Life", "owner", "Pass", True, "ACTIVE")
        prop = pa.create(uid, uid, "STUDIO", "RENT", "Douala", "Akwa", 150000)
        assert pa.transition(prop["id"], "published", uid) == "OK"
        assert pa.find_by_id(prop["id"])["status"] == "published"
