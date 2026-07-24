from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any
from uuid import uuid4

from lawim_v2.db import LawimRepository
from lawim_v2.security import hash_password, verify_password, create_session_token
from lawim_v2.user_roles import accept_user_role, OFFICIAL_USER_ROLES, USER_ROLE_ALIASES

from .ports import DemoUserPort, DemoAuthPort, DemoPropertyPort

DEMO_ROLE_MAP = {
    "client": "owner",
    "commercial": "agent",
    "support": "support",
    "auditor": "admin",
    "super_admin": "admin",
    "property_manager": "agent",
    "service_provider": "agent",
    "doc_manager": "agent",
    "finance_manager": "agent",
    "visit_manager": "agent",
    "moderator": "admin",
}


class V2UserAdapter(DemoUserPort):
    """Délègue au LawimRepository V2 réel pour créer et retrouver les utilisateurs Demo."""

    def __init__(self, db_path: str | None = None):
        self._db_path = db_path or os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")
        self._repo: LawimRepository | None = None

    def _get_repo(self) -> LawimRepository:
        if self._repo is None:
            self._repo = LawimRepository(Path(self._db_path))
            self._repo.initialize(seed_demo_data=False)
            # Create demo_registry table for Demo World tracking
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

    def create_or_update(self, ref_id: str, email: str, full_name: str, role: str, password: str | None = None, can_login: bool = True, account_status: str = "active", org_id: str | None = None) -> str:
        repo = self._get_repo()
        normalized_role = accept_user_role(role)
        if not normalized_role:
            normalized_role = DEMO_ROLE_MAP.get(role, "user")
        pw = password if password else "DemoNoAuthPlaceholder!"
        user_data = repo.create_user(
            email=email,
            full_name=full_name,
            role=normalized_role,
            password=pw,
            organization_id=int(org_id) if org_id and org_id.isdigit() else None,
        )
        actual_id = str(user_data["id"])
        repo.connection.execute(
            "INSERT OR IGNORE INTO demo_registry (demo_reference_id, demo_dataset_id, demo_section, object_type, object_id) VALUES (?,?,?,?,?)",
            (ref_id, "LAWIM_DEMO_WORLD_V1", "users", "user", actual_id),
        )
        repo.connection.commit()
        return actual_id

    def find_by_ref(self, ref_id: str) -> dict[str, Any] | None:
        repo = self._ua._get_repo()
        row = repo.connection.execute(
            "SELECT u.id, u.email, u.full_name, u.role, u.created_at FROM users u JOIN demo_registry d ON d.object_id=CAST(u.id AS TEXT) AND d.demo_section='users' WHERE d.demo_reference_id=?",
            (ref_id,),
        ).fetchone()
        if row is None:
            return None
        return dict(row)


class V2AuthAdapter(DemoAuthPort):
    """Délègue à LawimRepository.authenticate() et lawim_v2.security pour la vérification des credentials."""

    def __init__(self, user_adapter: V2UserAdapter):
        self._ua = user_adapter

    def verify(self, email: str, password: str) -> tuple[bool, str, str]:
        repo = self._ua._get_repo()
        row = repo.connection.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
        if row is None:
            return False, "USER_NOT_FOUND", ""
        try:
            auth_result = repo.authenticate(email, password)
            if auth_result is None:
                return False, "INVALID_CREDENTIALS", str(row["id"])
            return True, "LOGIN_SUCCESS", str(row["id"])
        except Exception as e:
            return False, "INVALID_CREDENTIALS", str(row["id"])

    def update_password(self, email: str, new_password: str) -> None:
        repo = self._ua._get_repo()
        pw_record = hash_password(new_password)
        repo.connection.execute(
            "UPDATE users SET password_salt=?, password_hash=? WHERE email=?",
            (pw_record["salt"], pw_record["hash"], email),
        )
        repo.connection.commit()


class V2AuthorizationAdapter:
    """Délègue au mécanisme d'autorisation V2 via les rôles utilisateur."""

    def __init__(self, user_adapter: V2UserAdapter):
        self._ua = user_adapter

    def check(self, actor_id: str, action: str, resource_type: str = "") -> bool:
        repo = self._ua._get_repo()
        row = repo.connection.execute("SELECT role FROM users WHERE id=?", (actor_id,)).fetchone()
        if row is None:
            return False
        role = row["role"]
        if role == "super_admin":
            return True
        perms = {
            "super_admin": True,
            "admin": {"users:read": True, "users:write": True, "properties:read": True, "properties:write": True, "settings:read": True, "settings:write": True},
            "support": {"users:read": True, "properties:read": True, "tickets:read": True, "tickets:write": True},
            "commercial": {"properties:read": True, "properties:write": True, "leads:read": True, "leads:write": True},
            "property_manager": {"properties:read": True, "properties:write": True, "media:read": True, "media:write": True},
            "auditor": {"audit:read": True, "users:read": True, "properties:read": True},
            "agent": {"properties:read": True, "properties:write": True},
            "owner": {"properties:read": True, "properties:write": True},
        }
        role_perms = perms.get(role, {})
        if isinstance(role_perms, dict):
            return role_perms.get(action, False)
        return role_perms


class V2PropertyAdapter(DemoPropertyPort):
    """Délègue au LawimRepository V2 pour la création et la gestion des biens immobiliers Demo."""

    def __init__(self, user_adapter: V2UserAdapter):
        self._ua = user_adapter

    def create(self, owner_id: str, created_by: str, property_type: str, transaction_type: str, city: str, district: str, price: float, agent_id: str = "", org_id: str = "", title: str = "") -> dict[str, Any]:
        repo = self._ua._get_repo()
        conn = repo.connection
        if not title:
            labels = {"APARTMENT": "Appartement", "HOUSE": "Maison", "STUDIO": "Studio", "LAND": "Terrain"}
            title = f"{labels.get(property_type, property_type)} à {district}, {city}"
        ref_id = f"DEMO-PROP-{uuid4().hex[:12]}"
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        listing_code = f"DEMO-{ref_id[-8:]}"
        conn.execute(
            "INSERT INTO properties (listing_code, title, summary, city, region, country, price_min, price_max, currency, status, property_type, bedrooms, owner_organization_id, created_at) VALUES (?,?,?,?,?,?,?,?,'XAF','draft',?,0,NULL,?)",
            (listing_code, title, f"Annonce {title}", city, city, "Cameroun", price, price, property_type, now),
        )
        conn.execute(
            "INSERT INTO demo_registry (demo_reference_id, demo_dataset_id, demo_section, object_type, object_id, created_at) VALUES (?,?,?,?,?,?)",
            (ref_id, "LAWIM_DEMO_WORLD_V1", "properties", "property", str(conn.execute("SELECT last_insert_rowid()").fetchone()[0]), now),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM properties WHERE listing_code=?", (listing_code,)).fetchone()
        return dict(row)

    def transition(self, property_id: str, new_status: str, changed_by: str) -> str:
        repo = self._ua._get_repo()
        conn = repo.connection
        row = conn.execute("SELECT status FROM properties WHERE id=?", (property_id,)).fetchone()
        if row is None:
            return "PROPERTY_NOT_FOUND"
        conn.execute("UPDATE properties SET status=? WHERE id=?", (new_status, property_id))
        conn.commit()
        return "OK"

    def find_by_id(self, property_id: str) -> dict[str, Any] | None:
        repo = self._ua._get_repo()
        row = repo.connection.execute("SELECT * FROM properties WHERE id=?", (property_id,)).fetchone()
        if row is None:
            return None
        return dict(row)
