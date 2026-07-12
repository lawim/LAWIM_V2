from __future__ import annotations

import json
from hashlib import sha256
from hmac import compare_digest
from typing import Any, Mapping

GREEN_API_SOURCE = "green_api"
GREEN_API_MESSAGE_WEBHOOKS = frozenset({"incomingMessageReceived", "outgoingAPIMessageReceived", "outgoingMessageStatus"})
GREEN_API_SUPPORTED_WEBHOOKS = GREEN_API_MESSAGE_WEBHOOKS | frozenset({"stateInstanceChanged"})
GREEN_API_MESSAGE_STATUS_MAP = {
    "pending": "queued",
    "sendqueue": "queued",
    "serverack": "sent",
    "sent": "sent",
    "delivered": "delivered",
    "read": "delivered",
    "notsent": "failed",
    "failed": "failed",
    "paused": "queued",
    "deleted": "cancelled",
}


def _text(value: object | None) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _mapping(value: object | None) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {}


def _first_text(*values: object | None) -> str:
    for value in values:
        text = _text(value)
        if text:
            return text
    return ""


def _int_or_none(value: object | None) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def canonical_payload(payload: Mapping[str, Any]) -> str:
    return json.dumps(dict(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def payload_hash(payload: Mapping[str, Any]) -> str:
    return sha256(canonical_payload(payload).encode("utf-8")).hexdigest()


def redact_headers(headers: Mapping[str, str]) -> dict[str, str]:
    redacted: dict[str, str] = {}
    for key, value in headers.items():
        if key.lower() == "authorization":
            redacted[key] = "[redacted]"
        else:
            redacted[key] = str(value)
    return redacted


def parse_authorization_header(value: str | None) -> tuple[str, str] | None:
    header = _text(value)
    if not header:
        return None
    parts = header.split(None, 1)
    if len(parts) != 2:
        return None
    return parts[0], parts[1].strip()


def validate_webhook_authorization(value: str | None, secret: str | None) -> bool:
    expected = _text(secret)
    if not expected:
        return False
    parsed = parse_authorization_header(value)
    if parsed is None:
        return False
    scheme, token = parsed
    if scheme.lower() not in {"bearer", "basic"}:
        return False
    return compare_digest(token, expected)


def extract_message_body(message_data: Mapping[str, Any]) -> str:
    type_message = _text(message_data.get("typeMessage"))
    text_candidates: list[object | None] = [
        message_data.get("textMessage"),
        _mapping(message_data.get("textMessageData")).get("textMessage"),
        _mapping(message_data.get("extendedTextMessageData")).get("text"),
        _mapping(message_data.get("extendedTextMessageData")).get("textMessage"),
        _mapping(message_data.get("imageMessageData")).get("caption"),
        _mapping(message_data.get("videoMessageData")).get("caption"),
        _mapping(message_data.get("documentMessageData")).get("caption"),
        _mapping(message_data.get("audioMessageData")).get("caption"),
        _mapping(message_data.get("locationMessageData")).get("nameLocation"),
    ]
    for candidate in text_candidates:
        text = _text(candidate)
        if text:
            return text
    if type_message:
        location = _mapping(message_data.get("locationMessageData"))
        latitude = _first_text(location.get("latitude"))
        longitude = _first_text(location.get("longitude"))
        if latitude or longitude:
            return f"[{type_message}] {latitude}, {longitude}".strip()
        return f"[{type_message}]"
    return ""


def normalize_webhook_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    raw_payload = dict(payload)
    instance_data = _mapping(payload.get("instanceData"))
    sender_data = _mapping(payload.get("senderData"))
    message_data = _mapping(payload.get("messageData"))
    type_webhook = _first_text(payload.get("typeWebhook")) or "unknown"
    timestamp = _int_or_none(payload.get("timestamp"))
    id_message = _first_text(payload.get("idMessage"))
    status = _first_text(payload.get("status"))
    state_instance = _first_text(payload.get("stateInstance"))
    chat_id = _first_text(payload.get("chatId"), sender_data.get("chatId"))
    message_type = _first_text(message_data.get("typeMessage"))
    message_body = extract_message_body(message_data)
    sender = _first_text(sender_data.get("sender"))
    sender_name = _first_text(sender_data.get("senderName"), sender_data.get("senderContactName"))
    instance_id = _int_or_none(instance_data.get("idInstance"))
    if instance_id is None:
        instance_id = _int_or_none(payload.get("idInstance"))
    normalized: dict[str, Any] = {
        "type_webhook": type_webhook,
        "timestamp": timestamp,
        "id_message": id_message,
        "status": status,
        "state_instance": state_instance,
        "chat_id": chat_id,
        "sender": sender,
        "sender_name": sender_name,
        "message_type": message_type,
        "message_body": message_body,
        "send_by_api": bool(payload.get("sendByApi")),
        "instance_id": instance_id,
        "instance_wid": _first_text(instance_data.get("wid")),
        "instance_type": _first_text(instance_data.get("typeInstance")),
        "raw_payload": raw_payload,
        "payload_hash": payload_hash(raw_payload),
        "message_data": message_data,
        "sender_data": sender_data,
        "instance_data": instance_data,
    }
    return normalized


def build_event_key(normalized: Mapping[str, Any]) -> str:
    type_webhook = _first_text(normalized.get("type_webhook")) or "unknown"
    payload_hash_value = _first_text(normalized.get("payload_hash"))
    id_message = _first_text(normalized.get("id_message"))
    status = _first_text(normalized.get("status")).lower()
    state_instance = _first_text(normalized.get("state_instance"))
    timestamp = _first_text(normalized.get("timestamp"))
    chat_id = _first_text(normalized.get("chat_id"))
    if type_webhook in {"incomingMessageReceived", "outgoingAPIMessageReceived"}:
        basis = id_message or payload_hash_value
        return f"green-api:{type_webhook}:{basis}"
    if type_webhook == "outgoingMessageStatus":
        basis = ":".join(part for part in (chat_id, id_message, status, timestamp) if part)
        return f"green-api:{type_webhook}:{basis or payload_hash_value}"
    if type_webhook == "stateInstanceChanged":
        basis = ":".join(part for part in (state_instance, timestamp) if part)
        return f"green-api:{type_webhook}:{basis or payload_hash_value}"
    return f"green-api:{type_webhook}:{payload_hash_value[:24]}"


def build_message_key(normalized: Mapping[str, Any]) -> str:
    id_message = _first_text(normalized.get("id_message"))
    payload_hash_value = _first_text(normalized.get("payload_hash"))
    basis = id_message or payload_hash_value
    return f"green-api:message:{basis}"


def map_message_status(status: str | None) -> str:
    normalized = _text(status).lower()
    return GREEN_API_MESSAGE_STATUS_MAP.get(normalized, "sent")


def summarize_for_log(normalized: Mapping[str, Any], *, duplicate: bool, event_key: str, message_key: str | None = None) -> dict[str, Any]:
    return {
        "source": GREEN_API_SOURCE,
        "type_webhook": _first_text(normalized.get("type_webhook")) or "unknown",
        "event_key": event_key,
        "message_key": message_key,
        "duplicate": duplicate,
        "status": _first_text(normalized.get("status")),
        "state_instance": _first_text(normalized.get("state_instance")),
        "message_type": _first_text(normalized.get("message_type")),
        "send_by_api": bool(normalized.get("send_by_api")),
    }

