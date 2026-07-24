from __future__ import annotations

import hashlib
import os
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class DemoPropertyResult:
    property_id: str = ""
    owner_id: str = ""
    created_by: str = ""
    agent_id: str = ""
    organization_id: str = ""
    property_type: str = ""
    transaction_type: str = ""
    city: str = ""
    district: str = ""
    price: float = 0.0
    status: str = "draft"
    publication_status: str = "draft"
    media_ids: list[str] = field(default_factory=list)
    document_ids: list[str] = field(default_factory=list)
    demo_dataset_id: str = ""
    error: str = ""


def _hash_password(password: str) -> tuple[str, str]:
    salt = os.urandom(16)
    import base64
    salt_b64 = base64.b64encode(salt).decode()
    h = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
    return salt_b64, h


def _get_db() -> str:
    return os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")


def _init_users_table(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE,
            username TEXT,
            full_name TEXT,
            role TEXT,
            phone TEXT,
            password_salt TEXT,
            password_hash TEXT,
            can_login INTEGER DEFAULT 1,
            account_status TEXT DEFAULT 'active',
            organization_id TEXT,
            is_demo_data INTEGER DEFAULT 0,
            demo_dataset_id TEXT,
            demo_reference_id TEXT,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_permissions (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            permission TEXT,
            resource_type TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id TEXT PRIMARY KEY,
            owner_id TEXT,
            created_by TEXT,
            agent_id TEXT,
            organization_id TEXT,
            property_type TEXT,
            transaction_type TEXT,
            title TEXT,
            city TEXT,
            district TEXT,
            price REAL,
            status TEXT DEFAULT 'draft',
            publication_status TEXT DEFAULT 'draft',
            media_ids TEXT DEFAULT '[]',
            document_ids TEXT DEFAULT '[]',
            is_demo_data INTEGER DEFAULT 0,
            demo_dataset_id TEXT,
            demo_reference_id TEXT,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS property_status_history (
            id TEXT PRIMARY KEY,
            property_id TEXT,
            from_status TEXT,
            to_status TEXT,
            changed_by TEXT,
            changed_at TEXT,
            FOREIGN KEY(property_id) REFERENCES properties(id)
        )
    """)
    conn.commit()
    return conn


def create_demo_user(
    db_path: str,
    ref_id: str,
    email: str,
    full_name: str,
    role: str,
    password: str | None = None,
    can_login: bool = True,
    account_status: str = "active",
    org_id: str | None = None,
) -> str:
    conn = _init_users_table(db_path)
    user_id = f"DEMO-{uuid4().hex[:12]}"
    password_salt = None
    password_hash = None
    if password and can_login:
        password_salt, password_hash = _hash_password(password)
    conn.execute(
        "INSERT OR IGNORE INTO users (id, email, full_name, role, password_salt, password_hash, can_login, account_status, organization_id, is_demo_data, demo_dataset_id, demo_reference_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 'LAWIM_DEMO_WORLD_V1', ?, ?)",
        (user_id, email, full_name, role, password_salt, password_hash, 1 if can_login else 0, account_status, org_id, ref_id, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()
    return user_id


def authenticate_demo_user(db_path: str, email: str, password: str) -> tuple[bool, str, str]:
    conn = _init_users_table(db_path)
    row = conn.execute(
        "SELECT id, full_name, role, password_salt, password_hash, can_login, account_status FROM users WHERE email=?",
        (email,),
    ).fetchone()
    conn.close()
    if not row:
        return False, "USER_NOT_FOUND", ""
    user_id, full_name, role, salt, pwh, can_login, account_status = row
    if not can_login:
        return False, "ACCOUNT_LOGIN_DISABLED", user_id
    if account_status == "suspended":
        return False, "ACCOUNT_SUSPENDED", user_id
    if account_status == "blocked":
        return False, "ACCOUNT_BLOCKED", user_id
    if not pwh or not salt:
        return False, "ACCOUNT_LOGIN_DISABLED", user_id
    import hashlib, base64
    salt_bytes = base64.b64decode(salt)
    expected = hashlib.pbkdf2_hmac('sha256', password.encode(), salt_bytes, 100000).hex()
    if expected != pwh:
        return False, "INVALID_CREDENTIALS", user_id
    return True, "LOGIN_SUCCESS", user_id


def check_permission(db_path: str, user_id: str, permission: str, resource_type: str = "") -> bool:
    conn = _init_users_table(db_path)
    row = conn.execute("SELECT role, is_demo_data FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    if not row:
        return False
    role = row[0]
    super_admin_perms = True  # super_admin has all permissions
    admin_perms = {  # admin permissions
        "users:read": True, "users:write": True,
        "properties:read": True, "properties:write": True,
        "settings:read": True, "settings:write": True,
    }
    support_perms = {"users:read": True, "properties:read": True, "tickets:read": True, "tickets:write": True}
    commercial_perms = {"properties:read": True, "properties:write": True, "leads:read": True, "leads:write": True}
    auditor_perms = {"audit:read": True, "users:read": True, "properties:read": True}
    property_manager_perms = {"properties:read": True, "properties:write": True, "media:read": True, "media:write": True}
    role_perms = {
        "super_admin": super_admin_perms,
        "admin": admin_perms,
        "support": support_perms,
        "commercial": commercial_perms,
        "auditor": auditor_perms,
        "property_manager": property_manager_perms,
    }
    perms = role_perms.get(role, {})
    if isinstance(perms, dict):
        return perms.get(permission, False)
    return bool(perms)


def create_demo_property(
    db_path: str,
    owner_id: str,
    created_by: str,
    property_type: str,
    transaction_type: str,
    city: str,
    district: str,
    price: float,
    agent_id: str = "",
    org_id: str = "",
    title: str = "",
) -> DemoPropertyResult:
    conn = _init_users_table(db_path)
    prop_id = f"DEMO-PROP-{uuid4().hex[:12]}"
    media_ids = []
    document_ids = []
    if not title:
        title = f"{_ptype_label(property_type)} à {district}, {city}"
    conn.execute(
        "INSERT INTO properties (id, owner_id, created_by, agent_id, organization_id, property_type, transaction_type, title, city, district, price, status, publication_status, media_ids, document_ids, is_demo_data, demo_dataset_id, demo_reference_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft', 'draft', ?, ?, 1, 'LAWIM_DEMO_WORLD_V1', ?, ?)",
        (prop_id, owner_id, created_by, agent_id, org_id, property_type, transaction_type, title, city, district, price, '[]', '[]', prop_id, datetime.now(timezone.utc).isoformat()),
    )
    conn.execute(
        "INSERT INTO property_status_history (id, property_id, from_status, to_status, changed_by, changed_at) VALUES (?, ?, 'none', 'draft', ?, ?)",
        (f"hist-{uuid4().hex[:8]}", prop_id, created_by, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()
    return DemoPropertyResult(
        property_id=prop_id, owner_id=owner_id, created_by=created_by,
        agent_id=agent_id, organization_id=org_id,
        property_type=property_type, transaction_type=transaction_type,
        city=city, district=district, price=price,
        status="draft", publication_status="draft",
        media_ids=media_ids, document_ids=document_ids,
        demo_dataset_id="LAWIM_DEMO_WORLD_V1",
    )


def update_property_status(db_path: str, prop_id: str, new_status: str, changed_by: str) -> str:
    valid_transitions = {
        "draft": ["submitted"],
        "submitted": ["under_review"],
        "under_review": ["approved", "rejected"],
        "approved": ["published", "rejected"],
        "published": ["suspended", "archived"],
        "suspended": ["published", "archived"],
        "rejected": ["draft"],
        "archived": ["draft"],
    }
    conn = _init_users_table(db_path)
    row = conn.execute("SELECT status FROM properties WHERE id=?", (prop_id,)).fetchone()
    if not row:
        conn.close()
        return "PROPERTY_NOT_FOUND"
    current = row[0]
    allowed = valid_transitions.get(current, [])
    if new_status not in allowed:
        conn.close()
        return f"INVALID_TRANSITION: {current}->{new_status}"
    conn.execute("UPDATE properties SET status=?, publication_status=? WHERE id=?", (new_status, new_status, prop_id))
    conn.execute("INSERT INTO property_status_history (id, property_id, from_status, to_status, changed_by, changed_at) VALUES (?, ?, ?, ?, ?, ?)",
                 (f"hist-{uuid4().hex[:8]}", prop_id, current, new_status, changed_by, datetime.now(timezone.utc).isoformat()))
    conn.commit()
    conn.close()
    return "OK"


def _ptype_label(ptype: str) -> str:
    labels = {"APARTMENT": "Appartement", "HOUSE": "Maison", "STUDIO": "Studio", "LAND": "Terrain"}
    return labels.get(ptype, ptype)
