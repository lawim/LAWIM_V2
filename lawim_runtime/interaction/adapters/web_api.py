from __future__ import annotations

import json
import logging
from typing import Any

from ..envelope import InteractionEnvelope, MessageType
from . import ChannelAdapter, ChannelDeliveryRequest, ChannelDeliveryResult

logger = logging.getLogger(__name__)


class WebAPIAdapter(ChannelAdapter):
    channel_name: str = "web_api"

    def parse_webhook(
        self,
        raw_payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> InteractionEnvelope | None:
        try:
            text = raw_payload.get("message", "") or raw_payload.get("text", "")
            user_id = raw_payload.get("user_id", "") or raw_payload.get("userId", "")
            session_id = raw_payload.get("session_id", "") or raw_payload.get("sessionId", "")
            correlation_id = raw_payload.get("correlation_id", "") or raw_payload.get("correlationId", "")
            message_type_str = raw_payload.get("type", "text")

            msg_type_map = {
                "text": MessageType.TEXT,
                "image": MessageType.IMAGE,
                "audio": MessageType.AUDIO,
                "video": MessageType.VIDEO,
                "document": MessageType.DOCUMENT,
                "location": MessageType.LOCATION,
                "contact": MessageType.CONTACT,
                "button": MessageType.BUTTON,
                "command": MessageType.COMMAND,
                "system": MessageType.SYSTEM,
            }
            msg_type = msg_type_map.get(message_type_str, MessageType.TEXT)

            return InteractionEnvelope(
                channel="web_api",
                external_message_id=raw_payload.get("message_id", ""),
                external_user_id=user_id,
                raw_sender=raw_payload.get("sender_name", "") or user_id,
                raw_recipient="",
                message_type=msg_type,
                raw_content=text,
                normalized_content=text,
                metadata={
                    "session_id": session_id,
                    "source_ip": (headers or {}).get("X-Forwarded-For", ""),
                    "user_agent": (headers or {}).get("User-Agent", ""),
                    **(raw_payload.get("metadata", {}) or {}),
                },
                correlation_id=correlation_id,
            )
        except Exception as e:
            logger.error("web_api parse_webhook error: %s", e)
            return None

    def extract_identifiers(self, raw_payload: dict[str, Any]) -> dict[str, str]:
        return {
            "channel": "web_api",
            "external_user_id": raw_payload.get("user_id", "") or raw_payload.get("userId", ""),
            "external_thread_id": raw_payload.get("session_id", "") or raw_payload.get("sessionId", ""),
            "raw_sender": raw_payload.get("sender_name", "") or "",
        }

    def send(self, request: ChannelDeliveryRequest) -> ChannelDeliveryResult:
        try:
            provider_id = f"web_api_{request.correlation_id[:8]}"
            logger.info(
                "web_api send simulated: text_len=%d provider_id=%s",
                len(request.text),
                provider_id,
            )
            return ChannelDeliveryResult(
                success=True,
                provider_message_id=provider_id,
                status_code=200,
                metadata={"simulated": True, "format": request.parse_mode},
            )
        except Exception as e:
            logger.error("web_api send error: %s", e)
            return ChannelDeliveryResult(success=False, error=str(e), status_code=500)

    def validate_webhook(self, headers: dict[str, str], raw_body: bytes) -> bool:
        return True
