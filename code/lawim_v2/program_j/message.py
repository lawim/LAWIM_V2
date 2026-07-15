from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .exchange_taxonomy import ContentType, Direction, ExchangeResult, ExchangeType


@dataclass
class MessageDelivery:
    delivery_id: str = ""
    message_id: str = ""
    provider: str = ""
    recipient: str = ""
    attempt: int = 1
    status: str = "pending"
    external_message_id: str = ""
    provider_response: str = ""
    error_code: str = ""
    idempotency_key: str = ""
    correlation_id: str = ""
    sent_at: str = ""
    delivered_at: str = ""
    read_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "delivery_id": self.delivery_id,
            "message_id": self.message_id,
            "provider": self.provider,
            "attempt": self.attempt,
            "status": self.status,
            "external_message_id": self.external_message_id,
            "sent_at": self.sent_at,
            "delivered_at": self.delivered_at,
        }


@dataclass
class UnifiedMessage:
    message_id: str
    conversation_id: str
    sender_actor_id: str = ""
    channel_session_id: str = ""
    channel: str = ""
    provider: str = ""
    external_message_id: str = ""
    direction: Direction = Direction.INBOUND
    content: str = ""
    content_type: ContentType = ContentType.TEXT
    exchange_type: ExchangeType = ExchangeType.INFORMATION_REQUEST
    exchange_result: ExchangeResult = ExchangeResult.RECEIVED
    business_intent: str = ""
    status: str = "received"
    reply_to_message_id: str = ""
    correlation_id: str = ""
    attachments: list[dict[str, Any]] = field(default_factory=list)
    deliveries: list[MessageDelivery] = field(default_factory=list)
    created_at: str = ""
    received_at: str = ""
    sent_at: str = ""
    delivered_at: str = ""
    read_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "sender_actor_id": self.sender_actor_id,
            "channel": self.channel,
            "provider": self.provider,
            "external_message_id": self.external_message_id,
            "direction": self.direction.value,
            "content_type": self.content_type.value,
            "exchange_type": self.exchange_type.value,
            "exchange_result": self.exchange_result.value,
            "status": self.status,
            "reply_to_message_id": self.reply_to_message_id,
            "correlation_id": self.correlation_id,
            "attachment_count": len(self.attachments),
            "created_at": self.created_at,
        }
