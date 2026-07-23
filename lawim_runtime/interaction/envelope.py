from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class MessageType(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"
    DOCUMENT = "DOCUMENT"
    LOCATION = "LOCATION"
    CONTACT = "CONTACT"
    BUTTON = "BUTTON"
    COMMAND = "COMMAND"
    SYSTEM = "SYSTEM"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class AttachmentRef:
    attachment_id: str = ""
    mime_type: str = ""
    file_name: str = ""
    url: str = ""
    size_bytes: int = 0


@dataclass(frozen=True)
class InteractionEnvelope:
    interaction_id: str = field(default_factory=lambda: uuid4().hex[:16])
    channel: str = ""
    external_message_id: str = ""
    external_thread_id: str = ""
    external_user_id: str = ""
    raw_sender: str = ""
    raw_recipient: str = ""
    message_type: MessageType = MessageType.UNKNOWN
    raw_content: str = ""
    normalized_content: str = ""
    attachments: tuple[AttachmentRef, ...] = field(default_factory=tuple)
    received_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    language_hint: str = ""
    correlation_id: str = ""
    causation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
