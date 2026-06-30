from __future__ import annotations

import json
from typing import Any

from .engines import parse_json_list


def _json_dict(value: str | None) -> dict[str, object]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def goal_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "project_id": row["project_id"],
        "goal_key": row["goal_key"],
        "title": row["title"],
        "priority": row.get("priority"),
        "status": row.get("status"),
        "influence": _json_dict(str(row.get("influence_json") or "{}")),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def need_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row["id"], "project_id": row["project_id"], "need_key": row["need_key"], "description": row["description"], "priority": row.get("priority"), "status": row.get("status")}


def constraint_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row["id"], "project_id": row["project_id"], "constraint_type": row["constraint_type"], "description": row["description"], "severity": row.get("severity")}


def preference_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row["id"], "project_id": row["project_id"], "preference_key": row["preference_key"], "value": _json_dict(str(row.get("value_json") or "{}")), "weight": row.get("weight")}


def funding_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row["id"], "project_id": row["project_id"], "source_type": row["source_type"], "amount": row.get("amount"), "currency": row.get("currency"), "status": row.get("status")}


def life_event_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row["id"], "project_id": row["project_id"], "user_id": row["user_id"], "event_type": row["event_type"], "title": row["title"], "impact": _json_dict(str(row.get("impact_json") or "{}")), "occurred_at": row.get("occurred_at")}


def risk_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row["id"], "project_id": row["project_id"], "risk_key": row["risk_key"], "severity": row.get("severity"), "likelihood": row.get("likelihood"), "description": row["description"], "status": row.get("status")}


def opportunity_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row["id"], "project_id": row["project_id"], "opportunity_key": row["opportunity_key"], "value_score": row.get("value_score"), "description": row["description"], "status": row.get("status")}


def decision_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "project_id": row["project_id"],
        "decision_key": row["decision_key"],
        "title": row["title"],
        "status": row.get("status"),
        "reason": row.get("reason"),
        "confidence": row.get("confidence"),
        "alternatives": parse_json_list(str(row.get("alternatives_json"))),
        "tradeoffs": parse_json_list(str(row.get("tradeoffs_json"))),
        "next_action": row.get("next_action"),
        "created_at": row.get("created_at"),
    }


def recommendation_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "project_id": row["project_id"],
        "recommendation_key": row["recommendation_key"],
        "title": row["title"],
        "priority": row.get("priority"),
        "confidence": row.get("confidence"),
        "score": row.get("score"),
        "reasons": parse_json_list(str(row.get("reasons_json"))),
        "status": row.get("status"),
    }


def action_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row["id"], "project_id": row["project_id"], "action_key": row["action_key"], "title": row["title"], "status": row.get("status"), "priority": row.get("priority"), "due_at": row.get("due_at")}


def task_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row["id"], "project_id": row["project_id"], "action_id": row.get("action_id"), "title": row["title"], "status": row.get("status"), "assignee_user_id": row.get("assignee_user_id"), "due_at": row.get("due_at")}


def knowledge_fact_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "project_id": row.get("project_id"),
        "user_id": row.get("user_id"),
        "category": row["category"],
        "fact_key": row["fact_key"],
        "title": row["title"],
        "content": row["content"],
        "source": row.get("source"),
        "confidence": row.get("confidence"),
        "metadata": _json_dict(str(row.get("metadata_json") or "{}")),
    }


def journey_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row["id"], "project_id": row["project_id"], "journey_key": row["journey_key"], "status": row.get("status"), "replan_count": row.get("replan_count"), "started_at": row.get("started_at"), "completed_at": row.get("completed_at")}


def trust_score_dto(row: dict[str, object] | None) -> dict[str, object] | None:
    if row is None:
        return None
    return {"subject_type": row["subject_type"], "subject_id": row["subject_id"], "score": row["score"], "factors": parse_json_list(str(row.get("factors_json"))), "computed_at": row.get("computed_at")}


def timeline_entry_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row["id"], "project_id": row["project_id"], "entry_type": row["entry_type"], "title": row["title"], "description": row.get("description"), "status": row.get("status"), "scheduled_at": row.get("scheduled_at"), "occurred_at": row.get("occurred_at")}


def workspace_dto(payload: dict[str, object], *, project_dto_fn, step_dto_fn, progress_dto_fn) -> dict[str, object]:
    return {
        "project": project_dto_fn(payload["project"]),
        "journey": journey_dto(payload["journey"]),
        "journey_state": payload["journey_state"],
        "goals": [goal_dto(row) for row in payload["goals"]],
        "needs": [need_dto(row) for row in payload["needs"]],
        "constraints": [constraint_dto(row) for row in payload["constraints"]],
        "preferences": [preference_dto(row) for row in payload["preferences"]],
        "funding": [funding_dto(row) for row in payload["funding"]],
        "life_events": [life_event_dto(row) for row in payload["life_events"]],
        "risks": [risk_dto(row) for row in payload["risks"]],
        "opportunities": [opportunity_dto(row) for row in payload["opportunities"]],
        "decisions": [decision_dto(row) for row in payload["decisions"]],
        "recommendations": [recommendation_dto(row) for row in payload["recommendations"]],
        "actions": [action_dto(row) for row in payload["actions"]],
        "tasks": [task_dto(row) for row in payload["tasks"]],
        "knowledge": [knowledge_fact_dto(row) for row in payload["knowledge"]],
        "timeline": payload["timeline"],
        "intelligence": payload["intelligence"],
        "trust_score": trust_score_dto(payload.get("trust_score")),
        "resources": payload["resources"],
        "partner_suggestions": payload["partner_suggestions"],
        "service_suggestions": payload["service_suggestions"],
        "progress_snapshots": payload["progress_snapshots"],
        "steps": [step_dto_fn(step) for step in payload["steps"]],
        "progress": progress_dto_fn(payload["progress"]),
    }
