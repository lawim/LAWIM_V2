from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from .envelope import InteractionEnvelope, MessageType


@dataclass
class GatewayValidationResult:
    valid: bool = True
    error: str = ""
    warnings: list[str] = field(default_factory=list)


class InteractionGateway:
    def validate_envelope(self, envelope: InteractionEnvelope) -> GatewayValidationResult:
        if not envelope.channel:
            return GatewayValidationResult(valid=False, error="channel is required")
        if not envelope.raw_content and not envelope.attachments:
            if envelope.message_type not in (MessageType.SYSTEM, MessageType.COMMAND, MessageType.UNKNOWN):
                return GatewayValidationResult(valid=False, error="raw_content or attachments required")
        return GatewayValidationResult()

    def prepare_envelope(
        self,
        channel: str,
        external_message_id: str,
        external_user_id: str,
        raw_sender: str,
        raw_content: str,
        message_type: MessageType = MessageType.TEXT,
        correlation_id: str = "",
        causation_id: str = "",
        external_thread_id: str = "",
        raw_recipient: str = "",
        attachments: tuple | None = None,
        language_hint: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> InteractionEnvelope:
        return InteractionEnvelope(
            channel=channel,
            external_message_id=external_message_id,
            external_thread_id=external_thread_id,
            external_user_id=external_user_id,
            raw_sender=raw_sender,
            raw_recipient=raw_recipient,
            message_type=message_type,
            raw_content=raw_content,
            normalized_content=raw_content,
            attachments=attachments or (),
            language_hint=language_hint,
            correlation_id=correlation_id,
            causation_id=causation_id,
            metadata=metadata or {},
        )
