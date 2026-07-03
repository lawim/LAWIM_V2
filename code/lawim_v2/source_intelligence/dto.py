from __future__ import annotations

import json
from typing import Any


def _parse_json(value: object, fallback: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if value in (None, ""):
        return fallback
    try:
        return json.loads(str(value))
    except json.JSONDecodeError:
        return fallback


def source_context_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "source_id": row.get("source_id"),
        "network": row.get("network"),
        "publication_url": row.get("publication_url"),
        "publication_title": row.get("publication_title"),
        "publication_text": row.get("publication_text"),
        "publication_author": row.get("publication_author"),
        "campaign": row.get("campaign"),
        "city": row.get("city"),
        "district": row.get("district"),
        "property_type": row.get("property_type"),
        "target_audience": row.get("target_audience"),
        "format": row.get("format"),
        "language": row.get("language"),
        "tags": _parse_json(row.get("tags_json"), []),
        "ai_classification": row.get("ai_classification"),
        "ai_confidence": row.get("ai_confidence"),
        "analysis": _parse_json(row.get("analysis_json"), {}),
        "notes": row.get("notes"),
        "whatsapp_link": row.get("whatsapp_link"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def source_dto(row: dict[str, object]) -> dict[str, object]:
    context = source_context_dto(row) if any(key in row for key in ("publication_url", "publication_title", "ai_classification")) else None
    payload = {
        "id": row.get("id"),
        "source_key": row.get("source_key"),
        "reference_code": row.get("reference_code") or row.get("source_key"),
        "name": row.get("name"),
        "channel": row.get("channel"),
        "status": row.get("status"),
        "target": row.get("target"),
        "created_by": row.get("created_by"),
        "metadata": _parse_json(row.get("metadata_json"), {}),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
        "lead_count": row.get("lead_count"),
        "customer_count": row.get("customer_count"),
        "whatsapp_count": row.get("whatsapp_count"),
        "import_count": row.get("import_count"),
        "conversion_rate": row.get("conversion_rate"),
        "whatsapp_link": row.get("whatsapp_link"),
        "last_imported_at": row.get("last_imported_at"),
    }
    if context is not None:
        payload.update(context)
    return payload


def import_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "import_key": row.get("import_key"),
        "source_id": row.get("source_id"),
        "source_url": row.get("source_url"),
        "import_status": row.get("import_status"),
        "source_channel": row.get("source_channel"),
        "imported_at": row.get("imported_at"),
        "analyzed_at": row.get("analyzed_at"),
        "payload": _parse_json(row.get("payload_json"), {}),
        "result": _parse_json(row.get("result_json"), {}),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def dashboard_dto(payload: dict[str, object]) -> dict[str, object]:
    return {
        "stats": payload.get("stats") or {},
        "sources": [source_dto(row) for row in payload.get("sources") or []],
        "imports": [import_dto(row) for row in payload.get("imports") or []],
        "top_sources": [source_dto(row) for row in payload.get("top_sources") or []],
    }


def stats_dto(payload: dict[str, object]) -> dict[str, object]:
    return {
        "stats": payload,
    }
