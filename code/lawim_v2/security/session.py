from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from .identity import Identity


@dataclass(frozen=True, slots=True)
class AADSession:
    session_id: str
    identity: Identity
    ttl_seconds: int
    created_at: str = "mock"


class AADSessionManager:
    def __init__(self) -> None:
        self._sessions: dict[str, AADSession] = {}

    def create_session(self, identity: Identity, ttl_seconds: int = 60) -> AADSession:
        session = AADSession(session_id=str(uuid4()), identity=identity, ttl_seconds=ttl_seconds)
        self._sessions[session.session_id] = session
        return session

    def is_active(self, session_id: str) -> bool:
        return session_id in self._sessions

    def get_session(self, session_id: str) -> AADSession | None:
        return self._sessions.get(session_id)

    def destroy_session(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None
