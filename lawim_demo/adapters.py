from __future__ import annotations

import os
import secrets
from pathlib import Path
from typing import Any
from uuid import uuid4

from lawim_v2.db import LawimRepository
from lawim_v2.security import hash_password, verify_password
from lawim_v2.user_roles import accept_user_role

from .ports import DemoUserPort, DemoAuthPort, DemoPropertyPort


ACCOUNT_STATUSES = {"ACTIVE", "LOGIN_DISABLED", "SUSPENDED", "BLOCKED"}


class V2UserAdapter(DemoUserPort):

    def __init__(self, db_path: str | None = None):
        self._db_path = db_path or os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")
        self._repo: LawimRepository | None = None

    def _get_repo(self) -> LawimRepository:
        if self._repo is None:
            self._repo = LawimRepository(Path(self._db_path))
            self._repo.initialize(seed_demo_data=False)
            self._repo.connection.execute("""
                CREATE TABLE IF NOT EXISTS demo_account_status (
                    user_id INTEGER PRIMARY KEY,
                    account_status TEXT NOT NULL DEFAULT 'ACTIVE',
                    can_login INTEGER NOT NULL DEFAULT 1,
                    is_demo_data INTEGER DEFAULT 1,
                    demo_dataset_id TEXT,
                    demo_reference_id TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            self._repo.connection.execute("""
                CREATE TABLE IF NOT EXISTS demo_registry (
                    demo_reference_id TEXT PRIMARY KEY,
                    demo_dataset_id TEXT NOT NULL,
                    demo_section TEXT NOT NULL,
                    object_type TEXT NOT NULL,
                    object_id TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
                )
            """)
            self._repo.connection.commit()
        return self._repo

    def create_or_update(self, ref_id: str, email: str, full_name: str, role: str, password: str | None = None, can_login: bool = True, account_status: str = "ACTIVE", org_id: str | None = None) -> str:
        repo = self._get_repo()
        normalized_role = accept_user_role(role)
        if not normalized_role:
            normalized_role = "user"
        status = account_status.upper() if account_status.upper() in ACCOUNT_STATUSES else "ACTIVE"
        if not can_login:
            status = "LOGIN_DISABLED"
        pw = password if password else secrets.token_urlsafe(32)
        user_data = repo.create_user(
            email=email, full_name=full_name, role=normalized_role,
            password=pw,
            organization_id=int(org_id) if org_id and org_id.isdigit() else None,
        )
        actual_id = str(user_data["id"])
        repo.connection.execute(
            "INSERT OR REPLACE INTO demo_account_status (user_id, account_status, can_login, is_demo_data, demo_dataset_id, demo_reference_id) VALUES (?,?,?,1,?,?)",
            (actual_id, status, 1 if can_login else 0, "LAWIM_DEMO_WORLD_V1", ref_id),
        )
        repo.connection.execute(
            "INSERT OR IGNORE INTO demo_registry (demo_reference_id, demo_dataset_id, demo_section, object_type, object_id) VALUES (?,?,?,?,?)",
            (ref_id, "LAWIM_DEMO_WORLD_V1", "users", "user", actual_id),
        )
        repo.connection.commit()
        return actual_id

    def find_by_ref(self, ref_id: str) -> dict[str, Any] | None:
        repo = self._get_repo()
        row = repo.connection.execute(
            "SELECT u.id, u.email, u.full_name, u.role, s.account_status, s.can_login FROM users u JOIN demo_account_status s ON s.user_id=u.id WHERE s.demo_reference_id=?",
            (ref_id,),
        ).fetchone()
        if row is None:
            return None
        return dict(row)


class V2AuthAdapter(DemoAuthPort):

    def __init__(self, user_adapter: V2UserAdapter):
        self._ua = user_adapter

    def verify(self, email: str, password: str) -> tuple[bool, str, str]:
        repo = self._ua._get_repo()
        row = repo.connection.execute(
            "SELECT u.id, s.account_status, s.can_login FROM users u JOIN demo_account_status s ON s.user_id=u.id WHERE u.email=?",
            (email,),
        ).fetchone()
        if row is None:
            return False, "USER_NOT_FOUND", ""
        uid = str(row["id"])
        status = row["account_status"]
        if not row["can_login"] or status == "LOGIN_DISABLED":
            return False, "ACCOUNT_LOGIN_DISABLED", uid
        if status == "SUSPENDED":
            return False, "ACCOUNT_SUSPENDED", uid
        if status == "BLOCKED":
            return False, "ACCOUNT_BLOCKED", uid
        try:
            auth_result = repo.authenticate(email=email, password=password)
            if auth_result is None:
                return False, "INVALID_CREDENTIALS", uid
            return True, "LOGIN_SUCCESS", uid
        except Exception:
            return False, "INVALID_CREDENTIALS", uid

    def update_password(self, email: str, new_password: str) -> None:
        repo = self._ua._get_repo()
        pw_record = hash_password(new_password)
        repo.connection.execute(
            "UPDATE users SET password_salt=?, password_hash=? WHERE email=?",
            (pw_record.salt, pw_record.hash, email),
        )
        repo.connection.commit()


class V2AuthorizationAdapter:

    def __init__(self, user_adapter: V2UserAdapter):
        self._ua = user_adapter

    def check(self, actor_id: str, action: str, resource_type: str = "") -> bool:
        repo = self._ua._get_repo()
        row = repo.connection.execute(
            "SELECT u.role FROM users u WHERE u.id=?", (actor_id,)
        ).fetchone()
        if row is None:
            return False
        role = row["role"]
        perms = {
            "super_admin": True,
            "admin": {"users:read": True, "users:write": True, "properties:read": True, "properties:write": True, "settings:read": True, "settings:write": True},
            "support": {"users:read": True, "properties:read": True, "tickets:read": True, "tickets:write": True},
            "commercial": {"properties:read": True, "properties:write": True, "leads:read": True, "leads:write": True},
            "property_manager": {"properties:read": True, "properties:write": True, "media:read": True, "media:write": True},
            "auditor": {"audit:read": True, "users:read": True, "properties:read": True},
            "operator": {"properties:read": True, "properties:write": True},
            "user": {"properties:read": True, "properties:write": True},
        }
        role_perms = perms.get(role, {})
        if role_perms is True:
            return True
        if isinstance(role_perms, dict):
            return role_perms.get(action, False)
        return role_perms


class V2PropertyAdapter(DemoPropertyPort):

    def __init__(self, user_adapter: V2UserAdapter):
        self._ua = user_adapter

    def create(self, owner_id: str, created_by: str, property_type: str, transaction_type: str, city: str, district: str, price: float, agent_id: str = "", org_id: str = "", title: str = "") -> dict[str, Any]:
        repo = self._ua._get_repo()
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        if not title:
            labels = {"APARTMENT": "Appartement", "HOUSE": "Maison", "STUDIO": "Studio", "LAND": "Terrain"}
            title = f"{labels.get(property_type, property_type)} à {district}, {city}"
        ref_id = f"DEMO-PROP-{uuid4().hex[:12]}"
        listing_code = f"DEMO-{ref_id[-8:]}"
        repo.connection.execute(
            "INSERT INTO properties (listing_code, title, summary, city, region, country, price_min, price_max, currency, status, property_type, bedrooms, created_at) VALUES (?,?,?,?,?,?,?,?,'XAF','draft',?,0,?)",
            (listing_code, title, f"{title} — Bien de démonstration LAWIM", city, "Centre" if "Yaoundé" in city or "Mvan" in city else "Littoral", "Cameroun", int(price), int(price), "APARTMENT" if not property_type else property_type, now),
        )
        prop_id = str(repo.connection.execute("SELECT last_insert_rowid()").fetchone()[0])
        repo.connection.execute(
            "INSERT INTO demo_registry (demo_reference_id, demo_dataset_id, demo_section, object_type, object_id) VALUES (?,?,?,?,?)",
            (ref_id, "LAWIM_DEMO_WORLD_V1", "properties", "property", prop_id),
        )
        repo.connection.commit()
        row = repo.connection.execute("SELECT * FROM properties WHERE id=?", (prop_id,)).fetchone()
        return dict(row)

    def transition(self, property_id: str, new_status: str, changed_by: str) -> str:
        repo = self._ua._get_repo()
        row = repo.connection.execute("SELECT status FROM properties WHERE id=?", (property_id,)).fetchone()
        if row is None:
            return "PROPERTY_NOT_FOUND"
        repo.connection.execute("UPDATE properties SET status=? WHERE id=?", (new_status, property_id))
        repo.connection.commit()
        return "OK"

    def find_by_id(self, property_id: str) -> dict[str, Any] | None:
        repo = self._ua._get_repo()
        row = repo.connection.execute("SELECT * FROM properties WHERE id=?", (property_id,)).fetchone()
        if row is None:
            return None
        return dict(row)
