from __future__ import annotations

from typing import Any

from .exchange_taxonomy import ContentType


INCOMING_CONTRACT_KEYS = frozenset({
    "provider", "channel", "external_sender_id", "external_recipient_id",
    "external_message_id", "external_thread_id", "direction",
    "content", "content_type", "sent_at", "received_at",
    "reply_to", "attachments", "raw_metadata",
})


def normalize_webhook_payload(provider: str, channel: str,
                                payload: dict[str, Any]) -> dict[str, Any]:
    if provider == "green_api":
        return _normalize_green_api(channel, payload)
    if provider == "telegram":
        return _normalize_telegram(channel, payload)
    return _normalize_generic(provider, channel, payload)


def _normalize_green_api(channel: str, payload: dict[str, Any]) -> dict[str, Any]:
    from ..communication.green_api import normalize_webhook_payload as ga_normalize
    raw = ga_normalize(payload)
    sender = raw.get("sender") or raw.get("chat_id") or ""
    return {
        "provider": "green_api",
        "channel": channel or "whatsapp",
        "external_sender_id": str(raw.get("chat_id", sender)),
        "external_recipient_id": str(raw.get("recipient", "")),
        "external_message_id": str(raw.get("id_message", raw.get("message_id", ""))),
        "external_thread_id": str(raw.get("chat_id", "")),
        "direction": "INBOUND",
        "content": raw.get("body", raw.get("text", "")),
        "content_type": _detect_content_type(raw),
        "sent_at": raw.get("timestamp", ""),
        "received_at": raw.get("timestamp", ""),
        "reply_to": str(raw.get("quoted_message_id", "")) if raw.get("quoted_message_id") else "",
        "attachments": raw.get("attachments", []),
        "raw_metadata": {k: v for k, v in raw.items() if k not in ("body", "text", "sender", "chat_id",
                        "id_message", "message_id", "recipient", "timestamp", "quoted_message_id")},
    }


def _normalize_telegram(channel: str, payload: dict[str, Any]) -> dict[str, Any]:
    from ..communication.telegram_webhook import normalize_webhook_payload as tg_normalize
    raw = tg_normalize(payload)
    sender = raw.get("from_id") or raw.get("chat_id") or ""
    return {
        "provider": "telegram",
        "channel": channel or "telegram",
        "external_sender_id": str(raw.get("from_id", sender)),
        "external_recipient_id": str(raw.get("chat_id", "")),
        "external_message_id": str(raw.get("message_id", raw.get("update_id", ""))),
        "external_thread_id": str(raw.get("chat_id", "")),
        "direction": "INBOUND",
        "content": raw.get("body", raw.get("text", "")),
        "content_type": _detect_content_type(raw),
        "sent_at": raw.get("date", raw.get("timestamp", "")),
        "received_at": raw.get("timestamp", raw.get("date", "")),
        "reply_to": str(raw.get("reply_to_message_id", "")) if raw.get("reply_to_message_id") else "",
        "attachments": raw.get("attachments", []),
        "raw_metadata": {k: v for k, v in raw.items() if k not in ("body", "text", "from_id", "chat_id",
                        "message_id", "update_id", "date", "timestamp", "reply_to_message_id")},
    }


def _normalize_generic(provider: str, channel: str,
                        payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "provider": provider,
        "channel": channel,
        "external_sender_id": str(payload.get("from", payload.get("sender", ""))),
        "external_recipient_id": str(payload.get("to", payload.get("recipient", ""))),
        "external_message_id": str(payload.get("message_id", payload.get("id", ""))),
        "external_thread_id": str(payload.get("thread_id", payload.get("conversation_id", ""))),
        "direction": str(payload.get("direction", "INBOUND")).upper(),
        "content": payload.get("content", payload.get("body", payload.get("text", ""))),
        "content_type": _detect_content_type(payload),
        "sent_at": payload.get("timestamp", payload.get("date", "")),
        "received_at": payload.get("received_at", payload.get("timestamp", "")),
        "reply_to": str(payload.get("reply_to", "")),
        "attachments": payload.get("attachments", []),
        "raw_metadata": {k: v for k, v in payload.items()
                         if k not in ("from", "sender", "to", "recipient", "message_id", "id",
                                      "thread_id", "conversation_id", "direction", "content",
                                      "body", "text", "timestamp", "date", "received_at",
                                      "reply_to", "attachments")},
    }


def _detect_content_type(raw: dict[str, Any]) -> str:
    t = (raw.get("type") or "").lower()
    if t in ("location",) or raw.get("location"):
        return "LOCATION"
    if t in ("contact",) or raw.get("contact"):
        return "CONTACT"
    if t in ("image", "photo") or raw.get("photo") or raw.get("image"):
        return "IMAGE"
    if t in ("video",) or raw.get("video"):
        return "VIDEO"
    if t in ("audio",) or raw.get("audio"):
        return "AUDIO"
    if t in ("document", "file") or raw.get("document") or raw.get("file"):
        return "DOCUMENT"
    if raw.get("attachments"):
        for att in raw["attachments"]:
            mime = (att.get("mime_type") or att.get("type") or "")
            ct = ContentType.from_mime(mime)
            if ct != ContentType.TEXT:
                return ct.value
    return "TEXT"
