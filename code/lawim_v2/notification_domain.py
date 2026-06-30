from __future__ import annotations

import json

NOTIFICATION_KINDS = frozenset(
    {
        "conversation_created",
        "message_received",
        "conversation_updated",
        "match_found",
        "system",
    }
)


def normalize_kind(kind: str) -> str:
    normalized = kind.strip().lower()
    if normalized not in NOTIFICATION_KINDS:
        raise ValueError(f"unsupported notification kind: {normalized}")
    return normalized


def build_notification_payload(payload: dict[str, object] | None) -> str:
    if payload is None:
        return "{}"
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def payload_dict(payload_json: str | None) -> dict[str, object]:
    if not payload_json:
        return {}
    try:
        parsed = json.loads(payload_json)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}
