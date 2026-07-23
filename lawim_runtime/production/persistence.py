from __future__ import annotations

import json
import logging
import os
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from lawim_runtime.interaction.session import InteractionSession, SessionStatus
from lawim_runtime.interaction.envelope import InteractionEnvelope
from lawim_runtime.interaction.delivery import DeliveryResult, DeliveryStatus
from lawim_runtime.project_profile.profile import ProjectProfile

logger = logging.getLogger(__name__)


class SessionStore(ABC):
    @abstractmethod
    def save_session(self, session: InteractionSession) -> None:
        ...

    @abstractmethod
    def get_session(self, session_id: str) -> InteractionSession | None:
        ...

    @abstractmethod
    def list_by_user(self, user_id: str) -> list[InteractionSession]:
        ...


class SQLiteSessionStore(SessionStore):
    def __init__(self, db_path: str = "") -> None:
        self._db_path = db_path or os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")
        self._conn: sqlite3.Connection | None = None

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_path)
            self._conn.row_factory = sqlite3.Row
            self._init_db()
        return self._conn

    def _init_db(self) -> None:
        conn = self._conn
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                channel TEXT NOT NULL DEFAULT '',
                conversation_id TEXT DEFAULT '',
                active_project_id TEXT DEFAULT '',
                started_at TEXT NOT NULL,
                last_activity_at TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                locale TEXT DEFAULT 'fr',
                metadata TEXT DEFAULT '{}'
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id)")
        conn.commit()

    def save_session(self, session: InteractionSession) -> None:
        conn = self._get_conn()
        conn.execute("""
            INSERT OR REPLACE INTO sessions
            (session_id, user_id, channel, conversation_id, active_project_id, started_at, last_activity_at, status, locale, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session.session_id, session.user_id, session.channel, session.conversation_id,
            session.active_project_id, session.started_at, session.last_activity_at,
            session.status.value if hasattr(session.status, 'value') else session.status,
            session.locale, json.dumps(session.metadata),
        ))
        conn.commit()

    def get_session(self, session_id: str) -> InteractionSession | None:
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,)).fetchone()
        if row is None:
            return None
        return InteractionSession(
            session_id=row["session_id"],
            user_id=row["user_id"],
            channel=row["channel"],
            conversation_id=row["conversation_id"],
            active_project_id=row["active_project_id"],
            started_at=row["started_at"],
            last_activity_at=row["last_activity_at"],
            status=SessionStatus(row["status"]),
            locale=row["locale"],
            metadata=json.loads(row["metadata"]),
        )

    def list_by_user(self, user_id: str) -> list[InteractionSession]:
        conn = self._get_conn()
        rows = conn.execute("SELECT * FROM sessions WHERE user_id = ? ORDER BY last_activity_at DESC", (user_id,)).fetchall()
        return [
            InteractionSession(
                session_id=r["session_id"], user_id=r["user_id"], channel=r["channel"],
                conversation_id=r["conversation_id"], active_project_id=r["active_project_id"],
                started_at=r["started_at"], last_activity_at=r["last_activity_at"],
                status=SessionStatus(r["status"]), locale=r["locale"],
                metadata=json.loads(r["metadata"]),
            ) for r in rows
        ]


class ProfileStore(ABC):
    @abstractmethod
    def save_profile(self, profile: ProjectProfile) -> None:
        ...

    @abstractmethod
    def get_profile(self, project_id: str) -> ProjectProfile | None:
        ...


class SQLiteProfileStore(ProfileStore):
    def __init__(self, db_path: str = "") -> None:
        self._db_path = db_path or os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")
        self._conn: sqlite3.Connection | None = None

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_path)
            self._conn.row_factory = sqlite3.Row
            self._init_db()
        return self._conn

    def _init_db(self) -> None:
        conn = self._conn
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                profile_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                profile_type TEXT NOT NULL DEFAULT '',
                fields_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                version INTEGER DEFAULT 1
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_profiles_project ON profiles(project_id)")
        conn.commit()

    def save_profile(self, profile: ProjectProfile) -> None:
        conn = self._get_conn()
        fields_data = {}
        for name, fv in profile.fields.items():
            fields_data[name] = {
                "value": fv.value,
                "confidence": fv.confidence,
                "status": fv.status.value if hasattr(fv.status, 'value') else str(fv.status),
            }
        conn.execute("""
            INSERT OR REPLACE INTO profiles
            (profile_id, project_id, profile_type, fields_json, created_at, updated_at, version)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            profile.profile_id, profile.project_id, profile.profile_type,
            json.dumps(fields_data), profile.created_at, profile.updated_at, profile.version,
        ))
        conn.commit()

    def get_profile(self, project_id: str) -> ProjectProfile | None:
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM profiles WHERE project_id = ?", (project_id,)).fetchone()
        if row is None:
            return None
        from lawim_runtime.project_profile.values import FieldValue, FieldValueStatus
        profile = ProjectProfile(
            profile_id=row["profile_id"],
            project_id=row["project_id"],
            profile_type=row["profile_type"],
        )
        fields_data = json.loads(row["fields_json"])
        for name, data in fields_data.items():
            status = data.get("status", "CANDIDATE")
            profile.fields[name] = FieldValue(
                field_name=name,
                value=data.get("value"),
                confidence=data.get("confidence", 1.0),
                status=FieldValueStatus(status) if hasattr(FieldValueStatus, status) else FieldValueStatus.CANDIDATE,
            )
        return profile
