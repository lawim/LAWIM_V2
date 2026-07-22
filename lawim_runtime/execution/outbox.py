from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class OutboxStatus(str, Enum):
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"


@dataclass
class OutboxMessage:
    message_id: str = field(default_factory=lambda: uuid4().hex[:16])
    topic: str = ""
    key: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    status: OutboxStatus = OutboxStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    published_at: str = ""
    retry_count: int = 0
    last_error: str = ""


class ExecutionOutbox:
    def __init__(self) -> None:
        self._messages: list[OutboxMessage] = []

    def publish(self, topic: str, key: str, payload: dict[str, Any]) -> OutboxMessage:
        msg = OutboxMessage(topic=topic, key=key, payload=payload, status=OutboxStatus.PUBLISHED)
        self._messages.append(msg)
        return msg

    def enqueue(self, topic: str, key: str, payload: dict[str, Any]) -> OutboxMessage:
        msg = OutboxMessage(topic=topic, key=key, payload=payload, status=OutboxStatus.PENDING)
        self._messages.append(msg)
        return msg

    def mark_published(self, message_id: str) -> bool:
        for msg in self._messages:
            if msg.message_id == message_id:
                msg.status = OutboxStatus.PUBLISHED
                msg.published_at = datetime.now(timezone.utc).isoformat()
                return True
        return False

    def mark_failed(self, message_id: str, error: str) -> bool:
        for msg in self._messages:
            if msg.message_id == message_id:
                msg.status = OutboxStatus.FAILED
                msg.last_error = error
                return True
        return False

    def list_pending(self) -> list[OutboxMessage]:
        return [m for m in self._messages if m.status == OutboxStatus.PENDING]

    def list_published(self) -> list[OutboxMessage]:
        return [m for m in self._messages if m.status == OutboxStatus.PUBLISHED]

    def count(self) -> int:
        return len(self._messages)

    def clear(self) -> None:
        self._messages.clear()
