from __future__ import annotations

import re
from typing import Any


def normalize_language(language: str | None, fallback: str = "fr") -> str:
    candidate = str(language or "").strip().lower()
    if candidate in {"fr", "en", "pcm"}:
        return candidate
    return fallback


def normalize_text(text: str | None) -> str:
    return str(text or "").strip()


def normalize_whatsapp_number(value: str | None) -> str:
    raw = re.sub(r"[^0-9+]", "", str(value or ""))
    if not raw:
        return ""
    digits = re.sub(r"\D", "", raw)
    if not digits:
        return ""
    if raw.startswith("+"):
        return f"+{digits}"
    if len(digits) == 12 and digits.startswith("237"):
        return f"+{digits}"
    if len(digits) == 9 and digits.startswith("6"):
        return f"+237{digits}"
    if len(digits) == 10 and digits.startswith("0"):
        return f"+237{digits[1:]}"
    return f"+{digits}"


def resolve_conversation_key(
    *,
    channel: str,
    project_id: int | None = None,
    contact_id: int | None = None,
    external_chat_id: str | None = None,
    external_user_id: str | None = None,
    message_id: str | None = None,
) -> str:
    if project_id is not None:
        return f"project:{project_id}"
    if contact_id is not None:
        return f"contact:{contact_id}"
    base = normalize_text(external_chat_id) or normalize_text(external_user_id) or normalize_text(message_id)
    if base:
        return f"{channel}:{base}"
    return f"{channel}:unknown"


def sanitize_metadata(metadata: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        return {}
    return {str(key): value for key, value in metadata.items()}
