from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

SESSION_TIMEOUT_MINUTES = 30


class SessionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    WAITING = "WAITING"
    SUSPENDED = "SUSPENDED"
    EXPIRED = "EXPIRED"
    CLOSED = "CLOSED"


@dataclass
class InteractionSession:
    session_id: str = field(default_factory=lambda: uuid4().hex[:16])
    user_id: str = ""
    channel: str = ""
    conversation_id: str = ""
    active_project_id: str = ""
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_activity_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: SessionStatus = SessionStatus.ACTIVE
    locale: str = "fr"
    metadata: dict[str, Any] = field(default_factory=dict)


class SessionManager:
    def __init__(self, timeout_minutes: int = SESSION_TIMEOUT_MINUTES) -> None:
        self._sessions: dict[str, InteractionSession] = {}
        self._user_sessions: dict[str, list[str]] = {}
        self._timeout = timedelta(minutes=timeout_minutes)

    def create_session(self, user_id: str, channel: str, conversation_id: str = "") -> InteractionSession:
        session = InteractionSession(
            user_id=user_id,
            channel=channel,
            conversation_id=conversation_id or "",
        )
        self._sessions[session.session_id] = session
        if user_id not in self._user_sessions:
            self._user_sessions[user_id] = []
        self._user_sessions[user_id].append(session.session_id)
        return session

    def get_session(self, session_id: str) -> InteractionSession | None:
        session = self._sessions.get(session_id)
        if session is None:
            return None
        now = datetime.now(timezone.utc)
        last = datetime.fromisoformat(session.last_activity_at)
        if session.status == SessionStatus.ACTIVE and (now - last) > self._timeout:
            session.status = SessionStatus.EXPIRED
        return session

    def resume_or_create(self, user_id: str, channel: str, conversation_id: str = "") -> InteractionSession:
        session_ids = self._user_sessions.get(user_id, [])
        for sid in reversed(session_ids):
            session = self._sessions.get(sid)
            if session and session.status == SessionStatus.ACTIVE:
                session.last_activity_at = datetime.now(timezone.utc).isoformat()
                return session
        return self.create_session(user_id, channel, conversation_id)

    def touch(self, session_id: str) -> None:
        session = self._sessions.get(session_id)
        if session:
            session.last_activity_at = datetime.now(timezone.utc).isoformat()

    def close_session(self, session_id: str) -> None:
        session = self._sessions.get(session_id)
        if session:
            session.status = SessionStatus.CLOSED

    def close_user_sessions(self, user_id: str) -> int:
        closed = 0
        for sid in self._user_sessions.get(user_id, []):
            session = self._sessions.get(sid)
            if session and session.status == SessionStatus.ACTIVE:
                session.status = SessionStatus.CLOSED
                closed += 1
        return closed

    def list_active(self) -> list[InteractionSession]:
        now = datetime.now(timezone.utc)
        active: list[InteractionSession] = []
        for session in self._sessions.values():
            if session.status == SessionStatus.ACTIVE:
                last = datetime.fromisoformat(session.last_activity_at)
                if (now - last) <= self._timeout:
                    active.append(session)
                else:
                    session.status = SessionStatus.EXPIRED
        return active

    def count_active(self) -> int:
        return len(self.list_active())
