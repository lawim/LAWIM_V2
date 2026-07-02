from __future__ import annotations

import json
from typing import Any


def _parse_json(value: str | None) -> Any:
    if not value:
        return {}
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {}


def event_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "event_key": row["event_key"],
        "event_type": row["event_type"],
        "source_program": row["source_program"],
        "payload": _parse_json(str(row.get("payload_json") or "{}")),
        "occurred_at": row["occurred_at"],
        "status": row["status"],
        "created_at": row["created_at"],
    }


def metric_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "metric_key": row["metric_key"],
        "name": row["name"],
        "category": row["category"],
        "unit": row["unit"],
        "source_program": row["source_program"],
        "definition": _parse_json(str(row.get("definition_json") or "{}")),
        "status": row["status"],
    }


def kpi_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "kpi_key": row["kpi_key"],
        "name": row["name"],
        "category": row["category"],
        "source_program": row["source_program"],
        "formula": _parse_json(str(row.get("formula_json") or "{}")),
        "status": row["status"],
    }


def dashboard_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "dashboard_key": row["dashboard_key"],
        "name": row["name"],
        "dashboard_type": row["dashboard_type"],
        "layout": _parse_json(str(row.get("layout_json") or "{}")),
        "status": row["status"],
    }


def report_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "report_key": row["report_key"],
        "name": row["name"],
        "report_type": row["report_type"],
        "config": _parse_json(str(row.get("config_json") or "{}")),
        "status": row["status"],
    }


def insight_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "insight_key": row["insight_key"],
        "insight_type": row["insight_type"],
        "title": row["title"],
        "content": _parse_json(str(row.get("content_json") or "{}")),
        "confidence": row["confidence"],
        "generated_at": row["generated_at"],
        "status": row["status"],
    }


def export_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "export_key": row["export_key"],
        "name": row["name"],
        "export_type": row["export_type"],
        "config": _parse_json(str(row.get("config_json") or "{}")),
        "status": row["status"],
    }


def score_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "score_key": row["score_key"],
        "name": row["name"],
        "score_type": row["score_type"],
        "source_program": row["source_program"],
        "formula": _parse_json(str(row.get("formula_json") or "{}")),
        "status": row["status"],
    }


def datamart_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "mart_key": row["mart_key"],
        "name": row["name"],
        "mart_type": row["mart_type"],
        "config": _parse_json(str(row.get("config_json") or "{}")),
        "status": row["status"],
    }
