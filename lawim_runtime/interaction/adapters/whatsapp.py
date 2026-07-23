from __future__ import annotations

import hashlib
import hmac
import json
import logging
from typing import Any

from ..envelope import AttachmentRef, InteractionEnvelope, MessageType
from ..response_plan import InteractionResponsePlan, ResponseType
from . import ChannelAdapter, ChannelDeliveryRequest, ChannelDeliveryResult

logger = logging.getLogger(__name__)

WHATSAPP_MEDIA_MAP: dict[str, MessageType] = {
    "image": MessageType.IMAGE,
    "audio": MessageType.AUDIO,
    "video": MessageType.VIDEO,
    "document": MessageType.DOCUMENT,
    "location": MessageType.LOCATION,
    "contact": MessageType.CONTACT,
    "button": MessageType.BUTTON,
    "interactive": MessageType.BUTTON,
}


class WhatsAppAdapter(ChannelAdapter):
    channel_name: str = "whatsapp"

    def parse_webhook(
        self,
        raw_payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> InteractionEnvelope | None:
        try:
            message_data = raw_payload.get("messageData", {})
            sender_data = raw_payload.get("senderData", {})

            text_data = message_data.get("textMessageData", {})
            raw_text = text_data.get("textMessage", "")

            msg_type_data = message_data.get("typeMessage", "")
            msg_type = WHATSAPP_MEDIA_MAP.get(msg_type_data, MessageType.TEXT)

            chat_id = sender_data.get("chatId", "")
            sender = sender_data.get("sender", "")
            sender_name = sender_data.get("senderName", "")

            external_message_id = (
                message_data.get("idMessage")
                or raw_payload.get("idMessage")
                or ""
            )

            attachments: list[AttachmentRef] = []
            if "fileMessageData" in message_data:
                file_data = message_data["fileMessageData"]
                attachments.append(AttachmentRef(
                    attachment_id=file_data.get("idFile", ""),
                    mime_type=file_data.get("mimeType", file_data.get("type", "")),
                    file_name=file_data.get("fileName", ""),
                    url=file_data.get("downloadUrl", ""),
                    size_bytes=file_data.get("fileSize", 0),
                ))

            if "locationMessageData" in message_data:
                loc = message_data["locationMessageData"]
                attachments.append(AttachmentRef(
                    attachment_id=f"loc:{loc.get('latitude','')},{loc.get('longitude','')}",
                    mime_type="application/vnd.whatsapp.location",
                    url=f"https://maps.google.com/?q={loc.get('latitude','')},{loc.get('longitude','')}",
                ))

            if not external_message_id:
                hash_input = f"{chat_id}:{raw_text}:{sender}"
                external_message_id = hashlib.md5(hash_input.encode()).hexdigest()[:16]

            return InteractionEnvelope(
                channel="whatsapp",
                external_message_id=external_message_id,
                external_thread_id=chat_id,
                external_user_id=sender or chat_id,
                raw_sender=sender_name or sender or "",
                raw_recipient=raw_payload.get("instanceData", {}).get("idInstance", ""),
                message_type=msg_type,
                raw_content=raw_text,
                normalized_content=raw_text,
                attachments=tuple(attachments),
                metadata={
                    "chat_id": chat_id,
                    "sender_name": sender_name,
                    "type_message": msg_type_data,
                },
            )
        except Exception as e:
            logger.error("whatsapp parse_webhook error: %s", e)
            return None

    def extract_identifiers(self, raw_payload: dict[str, Any]) -> dict[str, str]:
        sender_data = raw_payload.get("senderData", {})
        return {
            "channel": "whatsapp",
            "external_user_id": sender_data.get("sender", ""),
            "external_thread_id": sender_data.get("chatId", ""),
            "raw_sender": sender_data.get("senderName", "") or sender_data.get("sender", ""),
        }

    def send(self, request: ChannelDeliveryRequest) -> ChannelDeliveryResult:
        try:
            if not request.recipient_id:
                return ChannelDeliveryResult(
                    success=False,
                    error="recipient_id is required",
                    status_code=400,
                )

            provider_id = f"sim_whatsapp_{request.correlation_id[:8]}"
            logger.info(
                "whatsapp send simulated: to=%s text_len=%d provider_id=%s",
                request.recipient_id,
                len(request.text),
                provider_id,
            )
            return ChannelDeliveryResult(
                success=True,
                provider_message_id=provider_id,
                status_code=200,
                metadata={"simulated": True},
            )
        except Exception as e:
            logger.error("whatsapp send error: %s", e)
            return ChannelDeliveryResult(success=False, error=str(e), status_code=500)

    def validate_webhook(self, headers: dict[str, str], raw_body: bytes) -> bool:
        return True


class WhatsAppGreenAPIAdapter(WhatsAppAdapter):
    def send(self, request: ChannelDeliveryRequest) -> ChannelDeliveryResult:
        from lawim_runtime.interaction.adapters.whatsapp_green_api import send_green_api_message
        return send_green_api_message(request)
