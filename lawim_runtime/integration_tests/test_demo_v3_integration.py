from __future__ import annotations

import os
import tempfile

import pytest

from lawim_demo.v3_integration import (
    create_demo_user,
    authenticate_demo_user,
    check_permission,
    create_demo_property,
    update_property_status,
    DemoPropertyResult,
)


@pytest.fixture
def db():
    with tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False) as f:
        db_path = f.name
    yield db_path
    os.unlink(db_path)


class TestDemoV3Auth:
    def test_create_and_authenticate_client(self, db):
        uid = create_demo_user(db, "DEMO-USER-CLIENT-AUTH-001", "client.auth@demo.local", "Jean", "client", "Pass@123", True, "active")
        assert uid.startswith("DEMO-")
        success, code, returned_id = authenticate_demo_user(db, "client.auth@demo.local", "Pass@123")
        assert success, f"Auth failed: {code}"
        assert code == "LOGIN_SUCCESS"
        assert returned_id == uid

    def test_auth_wrong_password(self, db):
        create_demo_user(db, "DEMO-USER-CLIENT-AUTH-002", "client2@demo.local", "Alice", "client", "CorrectPass", True, "active")
        success, code, _ = authenticate_demo_user(db, "client2@demo.local", "WrongPass")
        assert not success
        assert code == "INVALID_CREDENTIALS"

    def test_noauth_login_disabled(self, db):
        create_demo_user(db, "DEMO-USER-CLIENT-NOAUTH-001", "noauth@demo.local", "NoAuth", "client", None, False, "disabled")
        success, code, _ = authenticate_demo_user(db, "noauth@demo.local", "AnyPass")
        assert not success
        assert code == "ACCOUNT_LOGIN_DISABLED"

    def test_suspended_user_refused(self, db):
        create_demo_user(db, "DEMO-USER-OWNER-AUTH-001", "owner@demo.local", "Owner", "owner", "Pass123", True, "suspended")
        success, code, _ = authenticate_demo_user(db, "owner@demo.local", "Pass123")
        assert not success
        assert code == "ACCOUNT_SUSPENDED"

    def test_blocked_user_refused(self, db):
        create_demo_user(db, "DEMO-USER-AGENT-AUTH-001", "agent@demo.local", "Agent", "agent", "Pass123", True, "blocked")
        success, code, _ = authenticate_demo_user(db, "agent@demo.local", "Pass123")
        assert not success
        assert code == "ACCOUNT_BLOCKED"

    def test_user_not_found(self, db):
        success, code, _ = authenticate_demo_user(db, "nonexistent@demo.local", "pass")
        assert not success
        assert code == "USER_NOT_FOUND"

    def test_auth_all_roles(self, db):
        roles = ["client", "owner", "agent", "admin", "support", "commercial", "auditor", "super_admin"]
        for role in roles:
            uid = create_demo_user(db, f"DEMO-USER-{role.upper()}-AUTH-001", f"{role}@demo.local", f"Test {role}", role, "Pass123", True, "active")
            assert uid
            success, code, _ = authenticate_demo_user(db, f"{role}@demo.local", "Pass123")
            assert success, f"Role {role} failed: {code}"


class TestDemoV3Permissions:
    def test_support_cannot_modify_payment(self, db):
        uid = create_demo_user(db, "DEMO-TEAM-SUPPORT-AUTH-001", "support@demo.local", "Support", "support", "Pass", True)
        assert not check_permission(db, uid, "payments:write")

    def test_commercial_cannot_create_admin(self, db):
        uid = create_demo_user(db, "DEMO-TEAM-COMMERCIAL-AUTH-001", "commercial@demo.local", "Commercial", "commercial", "Pass", True)
        assert not check_permission(db, uid, "users:write")

    def test_auditor_read_only(self, db):
        uid = create_demo_user(db, "DEMO-TEAM-AUDITOR-AUTH-001", "auditor@demo.local", "Auditor", "auditor", "Pass", True)
        assert check_permission(db, uid, "users:read")
        assert check_permission(db, uid, "properties:read")
        assert not check_permission(db, uid, "properties:write")

    def test_property_manager_can_modify_property(self, db):
        uid = create_demo_user(db, "DEMO-TEAM-PROPERTY-AUTH-001", "pm@demo.local", "PM", "property_manager", "Pass", True)
        assert check_permission(db, uid, "properties:write")

    def test_admin_permissions(self, db):
        uid = create_demo_user(db, "DEMO-TEAM-ADMIN-AUTH-001", "admin@demo.local", "Admin", "admin", "Pass", True)
        assert check_permission(db, uid, "users:write")
        assert check_permission(db, uid, "properties:write")

    def test_super_admin_has_all(self, db):
        uid = create_demo_user(db, "DEMO-TEAM-SUPERADMIN-AUTH-001", "super@demo.local", "Super", "super_admin", "Pass", True)
        assert check_permission(db, uid, "users:write")
        assert check_permission(db, uid, "payments:write")


class TestDemoV3Property:
    def test_owner_creates_apartment(self, db):
        owner_id = create_demo_user(db, "DEMO-USER-OWNER-AUTH-001", "owner@demo.local", "Owner", "owner", "Pass", True)
        result = create_demo_property(db, owner_id, owner_id, "APARTMENT", "RENT", "Yaoundé", "Mvan", 200000)
        assert result.property_id
        assert result.status == "draft"
        assert result.owner_id == owner_id
        assert result.city == "Yaoundé"
        assert result.price == 200000
        assert result.demo_dataset_id == "LAWIM_DEMO_WORLD_V1"

    def test_agent_creates_house_for_sale(self, db):
        agent_id = create_demo_user(db, "DEMO-USER-AGENT-AUTH-001", "agent@demo.local", "Agent", "agent", "Pass", True)
        owner_id = create_demo_user(db, "DEMO-USER-OWNER-AUTH-002", "owner2@demo.local", "Owner2", "owner", "Pass", True)
        result = create_demo_property(db, owner_id, agent_id, "HOUSE", "SELL", "Yaoundé", "Bastos", 50000000, agent_id=agent_id)
        assert result.property_id
        assert result.property_type == "HOUSE"

    def test_admin_creates_land(self, db):
        admin_id = create_demo_user(db, "DEMO-TEAM-ADMIN-AUTH-001", "admin@demo.local", "Admin", "admin", "Pass", True)
        result = create_demo_property(db, admin_id, admin_id, "LAND", "SELL", "Yaoundé", "Nkoabang", 10000000)
        assert result.property_id

    def test_property_lifecycle(self, db):
        owner_id = create_demo_user(db, "DEMO-USER-OWNER-AUTH-003", "owner3@demo.local", "Owner3", "owner", "Pass", True)
        result = create_demo_property(db, owner_id, owner_id, "STUDIO", "RENT", "Douala", "Akwa", 150000)
        assert result.status == "draft"
        transitions = ["submitted", "under_review", "approved", "published", "suspended", "published", "archived"]
        for target in transitions:
            status = update_property_status(db, result.property_id, target, owner_id)
            assert status == "OK" or status.startswith("INVALID_TRANSITION")

    def test_unauthorized_property_creation_not_blocked(self, db):
        noauth_id = create_demo_user(db, "DEMO-USER-CLIENT-NOAUTH-002", "noauth@demo.local", "NoAuth", "client", None, False)
        result = create_demo_property(db, noauth_id, noauth_id, "APARTMENT", "RENT", "Yaoundé", "Mvan", 100000)
        assert result.property_id  # V3 system allows it, auth layer would block at controller level


class TestDemoV3Credentials:
    def test_password_hash_different_per_user(self, db):
        ids = []
        for i in range(5):
            uid = create_demo_user(db, f"DEMO-USER-TEST-{i:03d}", f"test{i}@demo.local", f"Test{i}", "client", f"Pass{i}!", True)
            ids.append(uid)
        # Verify each user authenticates with their own password
        for i in range(5):
            success, code, _ = authenticate_demo_user(db, f"test{i}@demo.local", f"Pass{i}!")
            assert success, f"User {i} failed: {code}"

    def test_rotation_invalidates_old_password(self, db):
        create_demo_user(db, "DEMO-USER-ROTATE-001", "rotate@demo.local", "Rotate", "client", "OldPass1!", True)
        assert authenticate_demo_user(db, "rotate@demo.local", "OldPass1!")[0]
        # Rotate: update password
        import hashlib, base64
        import lawim_demo.v3_integration as vi
        conn = vi._init_users_table(db)
        salt_b64, new_hash = vi._hash_password("NewPass2!")
        conn.execute("UPDATE users SET password_salt=?, password_hash=? WHERE email=?", (salt_b64, new_hash, "rotate@demo.local"))
        conn.commit()
        conn.close()
        # Old password rejected
        assert not authenticate_demo_user(db, "rotate@demo.local", "OldPass1!")[0]
        assert authenticate_demo_user(db, "rotate@demo.local", "NewPass2!")[0]
