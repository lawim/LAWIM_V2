from __future__ import annotations

import json
from hashlib import sha256
from hmac import compare_digest
from typing import Any, Mapping

TELEGRAM_SOURCE = "telegram"
TELEGRAM_MESSAGE_UPDATE_TYPES = frozenset(
    {
        "message",
        "edited_message",
        "channel_post",
        "edited_channel_post",
        "business_message",
        "edited_business_message",
        "guest_message",
    }
)
TELEGRAM_STATE_UPDATE_TYPES = frozenset(
    {
        "my_chat_member",
        "chat_member",
        "callback_query",
    }
)
TELEGRAM_SUPPORTED_UPDATE_TYPES = TELEGRAM_MESSAGE_UPDATE_TYPES | TELEGRAM_STATE_UPDATE_TYPES
_TELEGRAM_UPDATE_TYPES_IN_PRIORITY_ORDER: tuple[str, ...] = (
    "message",
    "edited_message",
    "channel_post",
    "edited_channel_post",
    "business_message",
    "edited_business_message",
    "guest_message",
    "callback_query",
    "my_chat_member",
    "chat_member",
)


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
        lowered = key.lower()
        if lowered in {"authorization", "x-telegram-bot-api-secret-token"}:
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
    token = _text(value)
    if not token:
        return False
    return compare_digest(token, expected)


def extract_message_body(message_data: Mapping[str, Any]) -> str:
    candidates: list[object | None] = [
        message_data.get("text"),
        message_data.get("caption"),
        _mapping(message_data.get("text_quote")).get("text"),
        _mapping(message_data.get("reply_to_message")).get("text"),
        _mapping(message_data.get("poll")).get("question"),
    ]
    for candidate in candidates:
        text = _text(candidate)
        if text:
            return text

    location = _mapping(message_data.get("location"))
    latitude = _first_text(location.get("latitude"))
    longitude = _first_text(location.get("longitude"))
    if latitude or longitude:
        return f"[location] {latitude}, {longitude}".strip()

    contact = _mapping(message_data.get("contact"))
    phone_number = _first_text(contact.get("phone_number"))
    contact_name = _first_text(contact.get("first_name"), contact.get("last_name"))
    if phone_number or contact_name:
        parts = [part for part in (phone_number, contact_name) if part]
        return "[contact] " + " ".join(parts)

    if message_data.get("photo"):
        return "[photo]"
    if message_data.get("video"):
        return "[video]"
    if message_data.get("audio"):
        return "[audio]"
    if message_data.get("voice"):
        return "[voice]"
    if message_data.get("document"):
        return "[document]"
    if message_data.get("sticker"):
        return "[sticker]"
    if message_data.get("dice"):
        return "[dice]"

    return ""


def _first_update_type(payload: Mapping[str, Any]) -> str:
    for candidate in _TELEGRAM_UPDATE_TYPES_IN_PRIORITY_ORDER:
        if candidate in payload:
            return candidate
    return "unknown"


def normalize_webhook_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    raw_payload = dict(payload)
    update_type = _first_update_type(payload)
    update_payload = _mapping(payload.get(update_type))
    message_data = update_payload if update_type in TELEGRAM_MESSAGE_UPDATE_TYPES else {}
    callback_data = ""
    state = ""

    if update_type == "callback_query":
        callback_data = _first_text(update_payload.get("data"))
        message_data = _mapping(update_payload.get("message"))
        message_body = _first_text(callback_data, extract_message_body(message_data))
    elif update_type in {"my_chat_member", "chat_member"}:
        member_data = update_payload
        chat_data = _mapping(member_data.get("chat"))
        from_user = _mapping(member_data.get("from"))
        state = _first_text(_mapping(member_data.get("new_chat_member")).get("status"))
        message_body = state or _first_text(member_data.get("invite_link"))
        message_data = {
            "chat": chat_data,
            "from": from_user,
            "new_chat_member": _mapping(member_data.get("new_chat_member")),
            "old_chat_member": _mapping(member_data.get("old_chat_member")),
        }
    else:
        message_body = extract_message_body(message_data)

    chat_data = _mapping(message_data.get("chat"))
    from_user = _mapping(message_data.get("from"))
    if update_type == "callback_query" and not chat_data:
        chat_data = _mapping(_mapping(update_payload.get("message")).get("chat"))
    if update_type == "callback_query" and not from_user:
        from_user = _mapping(update_payload.get("from"))

    message_id = _int_or_none(message_data.get("message_id"))
    if message_id is None and update_type == "callback_query":
        message_id = _int_or_none(_mapping(update_payload.get("message")).get("message_id"))

    chat_id = _first_text(chat_data.get("id"), message_data.get("chat_id"))
    if not chat_id and update_type == "callback_query":
        chat_id = _first_text(_mapping(update_payload.get("message")).get("chat_id"))

    user_id = _int_or_none(from_user.get("id"))
    username = _first_text(from_user.get("username"))
    full_name = _first_text(from_user.get("first_name"), from_user.get("last_name"))

    normalized: dict[str, Any] = {
        "update_id": _int_or_none(payload.get("update_id")),
        "update_type": update_type,
        "message_id": message_id,
        "chat_id": chat_id,
        "chat_id_raw": chat_data.get("id"),
        "user_id": user_id,
        "username": username,
        "full_name": full_name,
        "message_body": message_body,
        "callback_data": callback_data,
        "state": state,
        "raw_payload": raw_payload,
        "payload_hash": payload_hash(raw_payload),
        "message_data": message_data,
        "update_data": update_payload,
        "from_user": from_user,
        "chat_data": chat_data,
    }
    return normalized


def build_event_key(normalized: Mapping[str, Any]) -> str:
    update_id = _int_or_none(normalized.get("update_id"))
    if update_id is not None:
        return f"telegram:update:{update_id}"
    payload_hash_value = _first_text(normalized.get("payload_hash"))
    return f"telegram:update:{payload_hash_value[:24]}"


def build_message_key(normalized: Mapping[str, Any]) -> str:
    chat_id = _first_text(normalized.get("chat_id"))
    message_id = _first_text(normalized.get("message_id"))
    payload_hash_value = _first_text(normalized.get("payload_hash"))
    basis = ":".join(part for part in (chat_id, message_id) if part)
    if basis:
        return f"telegram:message:{basis}"
    return f"telegram:message:{payload_hash_value[:24]}"


def summarize_for_log(
    normalized: Mapping[str, Any],
    *,
    duplicate: bool,
    event_key: str,
    message_key: str | None = None,
) -> dict[str, Any]:
    return {
        "source": TELEGRAM_SOURCE,
        "update_type": _first_text(normalized.get("update_type")) or "unknown",
        "event_key": event_key,
        "message_key": message_key,
        "duplicate": duplicate,
        "state": _first_text(normalized.get("state")),
        "has_message": bool(_first_text(normalized.get("message_body"))),
        "has_callback_data": bool(_first_text(normalized.get("callback_data"))),
    }
