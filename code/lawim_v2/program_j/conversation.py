from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ConversationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


@dataclass
class ConversationParticipant:
    conversation_id: str
    actor_id: str
    role: str = ""
    is_primary: bool = False
    joined_at: str = ""
    left_at: str | None = None
    visible: bool = True
    status: str = "ACTIVE"

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "actor_id": self.actor_id,
            "role": self.role,
            "is_primary": self.is_primary,
            "joined_at": self.joined_at,
            "visible": self.visible,
        }


@dataclass
class ChannelSession:
    session_id: str
    conversation_id: str
    channel: str
    provider: str
    user_endpoint_id: str
    lawim_endpoint_id: str = ""
    external_thread_id: str = ""
    status: str = "ACTIVE"
    started_at: str = ""
    last_activity_at: str = ""
    closed_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "conversation_id": self.conversation_id,
            "channel": self.channel,
            "provider": self.provider,
            "user_endpoint_id": self.user_endpoint_id,
            "external_thread_id": self.external_thread_id,
            "status": self.status,
            "started_at": self.started_at,
            "last_activity_at": self.last_activity_at,
        }


@dataclass
class UnifiedConversation:
    conversation_id: str
    subject: str = ""
    context: str = ""
    dossier_id: int | None = None
    project_id: int | None = None
    initial_channel: str = ""
    current_channel: str = ""
    primary_actor_id: str = ""
    status: ConversationStatus = ConversationStatus.ACTIVE
    participants: list[ConversationParticipant] = field(default_factory=list)
    channel_sessions: list[ChannelSession] = field(default_factory=list)
    created_at: str = ""
    last_activity_at: str = ""
    closed_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "subject": self.subject,
            "dossier_id": self.dossier_id,
            "project_id": self.project_id,
            "initial_channel": self.initial_channel,
            "current_channel": self.current_channel,
            "primary_actor_id": self.primary_actor_id,
            "status": self.status.value,
            "participant_count": len(self.participants),
            "session_count": len(self.channel_sessions),
            "created_at": self.created_at,
            "last_activity_at": self.last_activity_at,
        }

    def add_participant(self, actor_id: str, role: str = "", is_primary: bool = False) -> None:
        self.participants.append(ConversationParticipant(
            conversation_id=self.conversation_id,
            actor_id=actor_id,
            role=role,
            is_primary=is_primary,
        ))

    def add_channel_session(self, session: ChannelSession) -> None:
        self.channel_sessions.append(session)
        self.current_channel = session.channel
