from __future__ import annotations

import base64
import hashlib
import os
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from .ports import DemoUserPort, DemoAuthPort, DemoPropertyPort


class V2UserAdapter(DemoUserPort):
    def __init__(self, db_path: str | None = None):
        self._db_path = db_path or os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        conn = self._get_conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT,
                full_name TEXT NOT NULL DEFAULT '',
                phone_e164 TEXT,
                preferred_language TEXT DEFAULT 'fr',
                role TEXT NOT NULL DEFAULT 'user',
                organization_id INTEGER,
                password_salt TEXT,
                password_hash TEXT,
                can_login INTEGER DEFAULT 1,
                account_status TEXT DEFAULT 'active',
                is_demo_data INTEGER DEFAULT 0,
                demo_dataset_id TEXT,
                demo_reference_id TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS demo_registry (
                demo_reference_id TEXT PRIMARY KEY,
                demo_dataset_id TEXT NOT NULL,
                demo_section TEXT NOT NULL,
                object_type TEXT NOT NULL,
                object_id TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
        """)
        conn.commit()
        conn.close()

    def create_or_update(self, ref_id: str, email: str, full_name: str, role: str, password: str | None = None, can_login: bool = True, account_status: str = "active", org_id: str | None = None) -> str:
        conn = self._get_conn()
        existing = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
        if existing:
            conn.close()
            return str(existing["id"])
        salt, pwh = None, None
        if password and can_login:
            salt_bytes = os.urandom(16)
            salt = base64.b64encode(salt_bytes).decode()
            pwh = hashlib.pbkdf2_hmac('sha256', password.encode(), salt_bytes, 100000).hex()
        conn.execute(
            "INSERT INTO users (email, full_name, role, password_salt, password_hash, can_login, account_status, is_demo_data, demo_dataset_id, demo_reference_id) VALUES (?,?,?,?,?,?,?,1,?,?)",
            (email, full_name, role, salt, pwh, 1 if can_login else 0, account_status, "LAWIM_DEMO_WORLD_V1", ref_id),
        )
        uid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute("INSERT OR IGNORE INTO demo_registry (demo_reference_id, demo_dataset_id, demo_section, object_type, object_id) VALUES (?,?,?,?,?)",
                     (ref_id, "LAWIM_DEMO_WORLD_V1", "users", "user", str(uid)))
        conn.commit()
        conn.close()
        return str(uid)

    def find_by_ref(self, ref_id: str) -> dict[str, Any] | None:
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM users WHERE demo_reference_id=?", (ref_id,)).fetchone()
        conn.close()
        return dict(row) if row else None


class V2AuthAdapter(DemoAuthPort):
    def __init__(self, user_adapter: V2UserAdapter):
        self._ua = user_adapter

    def verify(self, email: str, password: str) -> tuple[bool, str, str]:
        conn = self._ua._get_conn()
        row = conn.execute("SELECT id, can_login, account_status, password_salt, password_hash FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        if not row:
            return False, "USER_NOT_FOUND", ""
        uid, can_login, status, salt, pwh = row["id"], row["can_login"], row["account_status"], row["password_salt"], row["password_hash"]
        if not can_login:
            return False, "ACCOUNT_LOGIN_DISABLED", str(uid)
        if status == "suspended":
            return False, "ACCOUNT_SUSPENDED", str(uid)
        if status == "blocked":
            return False, "ACCOUNT_BLOCKED", str(uid)
        if not pwh or not salt:
            return False, "ACCOUNT_LOGIN_DISABLED", str(uid)
        salt_bytes = base64.b64decode(salt)
        expected = hashlib.pbkdf2_hmac('sha256', password.encode(), salt_bytes, 100000).hex()
        if expected != pwh:
            return False, "INVALID_CREDENTIALS", str(uid)
        return True, "LOGIN_SUCCESS", str(uid)

    def update_password(self, email: str, new_password: str) -> None:
        conn = self._ua._get_conn()
        salt_bytes = os.urandom(16)
        salt = base64.b64encode(salt_bytes).decode()
        pwh = hashlib.pbkdf2_hmac('sha256', new_password.encode(), salt_bytes, 100000).hex()
        conn.execute("UPDATE users SET password_salt=?, password_hash=? WHERE email=?", (salt, pwh, email))
        conn.commit()
        conn.close()


class V2PropertyAdapter(DemoPropertyPort):
    def __init__(self, db_path: str | None = None):
        self._db_path = db_path or os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER,
                created_by INTEGER,
                agent_id INTEGER,
                organization_id INTEGER,
                property_type TEXT,
                transaction_type TEXT,
                title TEXT,
                city TEXT,
                district TEXT,
                price REAL,
                status TEXT DEFAULT 'draft',
                is_demo_data INTEGER DEFAULT 0,
                demo_dataset_id TEXT,
                demo_reference_id TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.commit()
        return conn

    def create(self, owner_id: str, created_by: str, property_type: str, transaction_type: str, city: str, district: str, price: float, agent_id: str = "", org_id: str = "", title: str = "") -> dict[str, Any]:
        conn = self._get_conn()
        ref_id = f"DEMO-PROP-{uuid4().hex[:12]}"
        if not title:
            labels = {"APARTMENT": "Appartement", "HOUSE": "Maison", "STUDIO": "Studio", "LAND": "Terrain"}
            title = f"{labels.get(property_type, property_type)} à {district}, {city}"
        conn.execute(
            "INSERT INTO properties (owner_id, created_by, agent_id, organization_id, property_type, transaction_type, title, city, district, price, status, is_demo_data, demo_dataset_id, demo_reference_id) VALUES (?,?,?,?,?,?,?,?,?,?,'draft',1,?,?)",
            (owner_id, created_by, agent_id, org_id, property_type, transaction_type, title, city, district, price, "LAWIM_DEMO_WORLD_V1", ref_id),
        )
        prop_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute("INSERT OR IGNORE INTO demo_registry (demo_reference_id, demo_dataset_id, demo_section, object_type, object_id) VALUES (?,?,?,?,?)",
                     (ref_id, "LAWIM_DEMO_WORLD_V1", "properties", "property", str(prop_id)))
        conn.commit()
        row = conn.execute("SELECT * FROM properties WHERE id=?", (prop_id,)).fetchone()
        conn.close()
        return dict(row)

    def transition(self, property_id: str, new_status: str, changed_by: str) -> str:
        conn = self._get_conn()
        row = conn.execute("SELECT status FROM properties WHERE id=?", (property_id,)).fetchone()
        if not row:
            conn.close()
            return "PROPERTY_NOT_FOUND"
        conn.execute("UPDATE properties SET status=? WHERE id=?", (new_status, property_id))
        conn.commit()
        conn.close()
        return "OK"

    def find_by_id(self, property_id: str) -> dict[str, Any] | None:
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM properties WHERE id=?", (property_id,)).fetchone()
        conn.close()
        return dict(row) if row else None
