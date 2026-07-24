from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from lawim_v2.db import LawimRepository
from lawim_v2.security import hash_password, verify_password

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


class TestV2UserAdapter:
    def test_creates_user_in_real_v2_table(self, db, ua):
        uid = ua.create_or_update("DEMO-TEST-USER-001", "test@demo.lawim.local", "Test User", "agent", "Pass123", True)
        repo = LawimRepository(Path(db))
        repo.initialize(seed_demo_data=False)
        row = repo._connection.execute("SELECT id, email, role, can_login FROM users WHERE demo_reference_id=?", ("DEMO-TEST-USER-001",)).fetchone()
        assert row is not None
        assert row["email"] == "test@demo.lawim.local"
        assert row["role"] == "agent"

    def test_readable_by_real_v2_repository(self, db, ua):
        ua.create_or_update("DEMO-READ-001", "read@demo.lawim.local", "Read Test", "owner", "Pass123", True)
        repo = LawimRepository(Path(db))
        repo.initialize(seed_demo_data=False)
        auth_result = repo.authenticate("read@demo.lawim.local", "Pass123")
        assert auth_result is not None


class TestV2AuthAdapter:
    def test_auth_delegates_to_real_v2_mechanism(self, db, ua, aa):
        ua.create_or_update("DEMO-AUTH-CLIENT-001", "client@demo.lawim.local", "Client", "client", "Pass123", True)
        ok, code, uid = aa.verify("client@demo.lawim.local", "Pass123")
        assert ok
        assert code == "LOGIN_SUCCESS"

    def test_password_uses_real_v2_hasher(self, db, ua):
        ua.create_or_update("DEMO-HASH-001", "hash@demo.lawim.local", "Hash Test", "agent", "Secret99", True)
        repo = LawimRepository(Path(db))
        repo.initialize(seed_demo_data=False)
        row = repo._connection.execute("SELECT password_salt, password_hash FROM users WHERE demo_reference_id=?", ("DEMO-HASH-001",)).fetchone()
        assert verify_password("Secret99", row["password_salt"], row["password_hash"])

    def test_noauth_rejected_by_real_v2_auth(self, db, ua, aa):
        ua.create_or_update("DEMO-NOAUTH-001", "noauth@demo.lawim.local", "NoAuth", "client", None, False)
        ok, code, _ = aa.verify("noauth@demo.lawim.local", "AnyPass")
        assert not ok
        assert code == "ACCOUNT_LOGIN_DISABLED"

    def test_suspended_rejected(self, db, ua, aa):
        ua.create_or_update("DEMO-SUSP-001", "susp@demo.lawim.local", "Susp", "owner", "Pass", True, "suspended")
        ok, code, _ = aa.verify("susp@demo.lawim.local", "Pass")
        assert not ok
        assert code == "ACCOUNT_SUSPENDED"

    def test_blocked_rejected(self, db, ua, aa):
        ua.create_or_update("DEMO-BLK-001", "blk@demo.lawim.local", "Blk", "agent", "Pass", True, "blocked")
        ok, code, _ = aa.verify("blk@demo.lawim.local", "Pass")
        assert not ok
        assert code == "ACCOUNT_BLOCKED"

    def test_wrong_password_rejected(self, db, ua, aa):
        ua.create_or_update("DEMO-WPW-001", "wpw@demo.lawim.local", "Wpw", "client", "Correct", True)
        ok, code, _ = aa.verify("wpw@demo.lawim.local", "Wrong")
        assert not ok
        assert code == "INVALID_CREDENTIALS"


class TestV2AuthRotation:
    def test_rotation_updates_real_v2_credentials(self, db, ua, aa):
        ua.create_or_update("DEMO-ROT-001", "rot@demo.lawim.local", "Rot", "client", "OldPass", True)
        assert aa.verify("rot@demo.lawim.local", "OldPass")[0]
        repo = LawimRepository(Path(db))
        repo.initialize(seed_demo_data=False)
        before = repo._connection.execute("SELECT password_hash FROM users WHERE demo_reference_id=?", ("DEMO-ROT-001",)).fetchone()["password_hash"]
        aa.update_password("rot@demo.lawim.local", "NewPass")
        after = repo._connection.execute("SELECT password_hash FROM users WHERE demo_reference_id=?", ("DEMO-ROT-001",)).fetchone()["password_hash"]
        assert before != after
        assert not aa.verify("rot@demo.lawim.local", "OldPass")[0]
        assert aa.verify("rot@demo.lawim.local", "NewPass")[0]


class TestV2AuthorizationAdapter:
    def test_support_cannot_modify_payment(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-AUTHZ-SUP-001", "sup@demo.lawim.local", "Support", "support", "Pass", True)
        assert not authz.check(uid, "payments:write")

    def test_commercial_cannot_create_admin(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-AUTHZ-COM-001", "com@demo.lawim.local", "Commercial", "commercial", "Pass", True)
        assert not authz.check(uid, "users:write")

    def test_auditor_read_only(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-AUTHZ-AUD-001", "aud@demo.lawim.local", "Auditor", "auditor", "Pass", True)
        assert authz.check(uid, "users:read")
        assert not authz.check(uid, "properties:write")

    def test_property_manager_can_modify_property(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-AUTHZ-PM-001", "pm@demo.lawim.local", "PM", "property_manager", "Pass", True)
        assert authz.check(uid, "properties:write")

    def test_admin_permissions(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-AUTHZ-ADM-001", "adm@demo.lawim.local", "Admin", "admin", "Pass", True)
        assert authz.check(uid, "users:write")
        assert authz.check(uid, "properties:write")

    def test_super_admin_has_all(self, db, ua, authz):
        uid = ua.create_or_update("DEMO-AUTHZ-SADM-001", "sadm@demo.lawim.local", "SuperAdmin", "super_admin", "Pass", True)
        assert authz.check(uid, "payments:write")


class TestV2PropertyAdapter:
    def test_property_is_readable_by_real_v2_repository(self, db, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-R-001", "prop@demo.lawim.local", "Prop Owner", "owner", "Pass", True)
        prop = pa.create(uid, uid, "APARTMENT", "RENT", "Yaoundé", "Mvan", 200000)
        repo = LawimRepository(Path(db))
        repo.initialize(seed_demo_data=False)
        row = repo.connection.execute("SELECT id, property_type, city, price_min, price_max FROM properties WHERE id=?", (prop["id"],)).fetchone()
        assert row is not None
        assert row["city"] == "Yaoundé"
        assert row["price_min"] == 200000

    def test_owner_creates_property(self, db, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-OWN-001", "own@demo.lawim.local", "Owner", "owner", "Pass", True)
        prop = pa.create(uid, uid, "APARTMENT", "RENT", "Yaoundé", "Mvan", 200000)
        assert prop["id"] is not None

    def test_agent_creates_property(self, db, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-AGT-001", "agt@demo.lawim.local", "Agent", "agent", "Pass", True)
        owner = ua.create_or_update("DEMO-PROP-OWN2-001", "own2@demo.lawim.local", "Owner2", "owner", "Pass", True)
        prop = pa.create(owner, uid, "HOUSE", "SELL", "Yaoundé", "Bastos", 50000000, agent_id=uid)
        assert prop["id"] is not None

    def test_commercial_creates_property(self, db, ua, pa):
        cid = ua.create_or_update("DEMO-PROP-COM-001", "com@demo.lawim.local", "Commercial", "commercial", "Pass", True)
        owner = ua.create_or_update("DEMO-PROP-OWN3-001", "own3@demo.lawim.local", "Owner3", "owner", "Pass", True)
        prop = pa.create(owner, cid, "STUDIO", "RENT", "Douala", "Akwa", 150000)
        assert prop["id"] is not None
        assert prop["created_by"] == cid

    def test_admin_creates_property(self, db, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-ADM-001", "adm@demo.lawim.local", "Admin", "admin", "Pass", True)
        prop = pa.create(uid, uid, "LAND", "SELL", "Yaoundé", "Nkoabang", 10000000)
        assert prop["id"] is not None

    def test_property_lifecycle(self, db, ua, pa):
        uid = ua.create_or_update("DEMO-PROP-LIFE-001", "life@demo.lawim.local", "Life", "owner", "Pass", True)
        prop = pa.create(uid, uid, "STUDIO", "RENT", "Douala", "Akwa", 150000)
        assert pa.transition(prop["id"], "published", uid) == "OK"
        assert pa.find_by_id(prop["id"])["status"] == "published"
        assert pa.transition(prop["id"], "archived", uid) == "OK"
        assert pa.find_by_id(prop["id"])["status"] == "archived"
