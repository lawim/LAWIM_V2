from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class ConversationRegistry:
    conversations: dict[str, dict[str, Any]] = field(default_factory=dict)
    participants: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    messages: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    events: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    def create_conversation(
        self,
        *,
        conversation_key: str,
        subject: str,
        participant_ids: list[str],
        media_ids: list[int] | None = None,
    ) -> dict[str, Any]:
        existing = self._find_by_key(conversation_key)
        if existing is not None:
            return existing

        conversation_id = len(self.conversations) + 1
        conversation = {
            "conversation_id": conversation_id,
            "conversation_key": conversation_key,
            "subject": subject,
            "status": "active",
            "lifecycle_state": "active",
            "media_ids": list(media_ids or []),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.conversations[conversation_key] = conversation
        self.participants[str(conversation_id)] = [
            {"participant_id": participant_id, "conversation_id": conversation_id}
            for participant_id in participant_ids
        ]
        self.messages[str(conversation_id)] = []
        self.events[str(conversation_id)] = [{"event": "conversation_created", "conversation_id": conversation_id}]
        return conversation

    def add_message(self, *, conversation_id: int, author_id: str, body: str) -> dict[str, Any]:
        conversation = self.get_conversation(conversation_id)
        message = {
            "message_id": len(self.messages[str(conversation_id)]) + 1,
            "conversation_id": conversation_id,
            "author_id": author_id,
            "body": body,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.messages[str(conversation_id)].append(message)
        self.events[str(conversation_id)].append({"event": "message_added", "conversation_id": conversation_id})
        return message

    def get_conversation(self, conversation_id: int) -> dict[str, Any]:
        for conversation in self.conversations.values():
            if conversation["conversation_id"] == conversation_id:
                return conversation
        raise KeyError(f"unknown conversation {conversation_id}")

    def list_conversations(self) -> list[dict[str, Any]]:
        return list(self.conversations.values())

    def list_participants(self, conversation_id: int) -> list[dict[str, Any]]:
        return list(self.participants.get(str(conversation_id), []))

    def _find_by_key(self, conversation_key: str) -> dict[str, Any] | None:
        return self.conversations.get(conversation_key)


@dataclass(slots=True)
class ConversationArchiveManifest:
    conversation_id: int
    payload: dict[str, Any]
    checksum: str
    version: str = "1.0"
    media_ids: list[int] = field(default_factory=list)


@dataclass(slots=True)
class ConversationArchiveManager:
    def build_manifest(self, *, conversation_id: int, media_ids: list[int], checksum: str) -> ConversationArchiveManifest:
        payload = {
            "version": "1.0",
            "participants": [],
            "messages": [],
            "events": [],
            "media_ids": media_ids,
            "audit_trail": ["conversation_registry"],
        }
        return ConversationArchiveManifest(
            conversation_id=conversation_id,
            payload=payload,
            checksum=checksum,
            media_ids=list(media_ids),
        )


@dataclass(slots=True)
class ConversationLifecycleEngine:
    states: tuple[str, ...] = ("active", "archived")

    def transition(self, current_state: str, target_state: str) -> str:
        if target_state not in self.states:
            raise ValueError("unsupported lifecycle state")
        if current_state == "archived" and target_state != "archived":
            raise ValueError("archived conversations cannot transition forward")
        return target_state

    def backup_state_for(self, lifecycle_state: str) -> str:
        return "archived" if lifecycle_state == "archived" else "queued"


@dataclass(slots=True)
class ConversationStorageProvider:
    name: str
    kind: str = "conversation-archive"
    quota_gb: int = 1000
    used_gb: int = 0
    status: str = "mock-ready"

    def resolve_access(self, *, conversation_id: int, kind: str) -> dict[str, Any]:
        return {
            "conversation_id": conversation_id,
            "kind": kind,
            "provider": self.name,
            "temporary_access_url": f"https://mock.example/{self.name}/{conversation_id}",
            "ttl_seconds": 900,
            "safe": True,
        }


@dataclass(slots=True)
class ConversationRestoreEngine:
    def build_restore_plan(self, *, conversation_id: int, reason: str) -> dict[str, Any]:
        return {
            "conversation_id": conversation_id,
            "reason": reason,
            "source": "drive-8",
            "status": "ready",
        }


@dataclass(slots=True)
class OVHStorageOptimizer:
    def plan(self, *, conversation_id: int, kind: str) -> dict[str, Any]:
        return {
            "conversation_id": conversation_id,
            "kind": kind,
            "drive_target": "drive-8",
            "hot_data": False,
            "thumbnail_retention": True,
        }


@dataclass(slots=True)
class StorageOrchestrator:
    providers: list[ConversationStorageProvider] = field(default_factory=list)

    def resolve_conversation_access(self, *, conversation_id: int, kind: str = "conversation_archive") -> dict[str, Any]:
        provider = self.providers[0] if self.providers else ConversationStorageProvider(name="drive-8")
        return provider.resolve_access(conversation_id=conversation_id, kind=kind)


__all__ = [
    "ConversationArchiveManager",
    "ConversationArchiveManifest",
    "ConversationLifecycleEngine",
    "ConversationRegistry",
    "ConversationRestoreEngine",
    "ConversationStorageProvider",
    "OVHStorageOptimizer",
    "StorageOrchestrator",
]
