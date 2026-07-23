from __future__ import annotations

import hashlib
import hmac
import logging
from typing import Any

from ..envelope import AttachmentRef, InteractionEnvelope, MessageType
from ..response_plan import InteractionResponsePlan, ResponseType
from . import ChannelAdapter, ChannelDeliveryRequest, ChannelDeliveryResult

logger = logging.getLogger(__name__)

TELEGRAM_MEDIA_MAP: dict[str, MessageType] = {
    "photo": MessageType.IMAGE,
    "audio": MessageType.AUDIO,
    "voice": MessageType.AUDIO,
    "video": MessageType.VIDEO,
    "video_note": MessageType.VIDEO,
    "document": MessageType.DOCUMENT,
    "location": MessageType.LOCATION,
    "contact": MessageType.CONTACT,
}


class TelegramAdapter(ChannelAdapter):
    channel_name: str = "telegram"

    def parse_webhook(
        self,
        raw_payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> InteractionEnvelope | None:
        try:
            message = raw_payload.get("message", {})
            if not message:
                message = raw_payload.get("callback_query", {}).get("message", {})

            chat = message.get("chat", {})
            from_user = message.get("from", {})

            chat_id = str(chat.get("id", ""))
            user_id = str(from_user.get("id", ""))
            user_name = from_user.get("first_name", "") or from_user.get("username", "")
            message_id = str(message.get("message_id", ""))

            text = message.get("text", "") or message.get("caption", "")

            msg_type = MessageType.TEXT
            for media_key, media_type in TELEGRAM_MEDIA_MAP.items():
                if media_key in message:
                    msg_type = media_type
                    break

            if "callback_query" in raw_payload:
                msg_type = MessageType.BUTTON
                cq = raw_payload["callback_query"]
                text = cq.get("data", "")
                message_id = str(cq.get("id", message_id))

            attachments: list[AttachmentRef] = []
            if "photo" in message:
                photos = message["photo"]
                if photos:
                    best = photos[-1]
                    attachments.append(AttachmentRef(
                        attachment_id=best.get("file_id", ""),
                        mime_type="image/jpeg",
                        file_name="",
                        size_bytes=best.get("file_size", 0),
                    ))

            for doc_key in ("document", "audio", "video", "voice"):
                if doc_key in message:
                    doc = message[doc_key]
                    mime = doc.get("mime_type", "")
                    attachments.append(AttachmentRef(
                        attachment_id=doc.get("file_id", ""),
                        mime_type=mime,
                        file_name=doc.get("file_name", ""),
                        size_bytes=doc.get("file_size", 0),
                    ))

            if not message_id:
                hash_input = f"{chat_id}:{text}:{user_id}"
                message_id = hashlib.md5(hash_input.encode()).hexdigest()[:16]

            return InteractionEnvelope(
                channel="telegram",
                external_message_id=message_id,
                external_thread_id=chat_id,
                external_user_id=user_id or chat_id,
                raw_sender=user_name or str(user_id),
                raw_recipient="",
                message_type=msg_type,
                raw_content=text,
                normalized_content=text,
                attachments=tuple(attachments),
                metadata={
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "user_name": user_name,
                    "is_bot": from_user.get("is_bot", False),
                },
            )
        except Exception as e:
            logger.error("telegram parse_webhook error: %s", e)
            return None

    def extract_identifiers(self, raw_payload: dict[str, Any]) -> dict[str, str]:
        message = raw_payload.get("message", {})
        chat = message.get("chat", {})
        from_user = message.get("from", {})
        return {
            "channel": "telegram",
            "external_user_id": str(from_user.get("id", "")),
            "external_thread_id": str(chat.get("id", "")),
            "raw_sender": from_user.get("first_name", "") or str(from_user.get("id", "")),
        }

    def send(self, request: ChannelDeliveryRequest) -> ChannelDeliveryResult:
        try:
            if not request.recipient_id:
                return ChannelDeliveryResult(
                    success=False,
                    error="recipient_id (chat_id) is required",
                    status_code=400,
                )

            provider_id = f"sim_telegram_{request.correlation_id[:8]}"
            logger.info(
                "telegram send simulated: to=%s text_len=%d provider_id=%s",
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
            logger.error("telegram send error: %s", e)
            return ChannelDeliveryResult(success=False, error=str(e), status_code=500)

    def validate_webhook(self, headers: dict[str, str], raw_body: bytes) -> bool:
        secret = headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if not secret:
            return True
        return True


class TelegramBotAdapter(TelegramAdapter):
    def send(self, request: ChannelDeliveryRequest) -> ChannelDeliveryResult:
        from lawim_runtime.interaction.adapters.telegram_bot_api import send_telegram_message
        return send_telegram_message(request)
