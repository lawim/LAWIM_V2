from __future__ import annotations

from typing import Any


def workflow_definition_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "workflow_key": row.get("workflow_key"),
        "domain": row.get("domain"),
        "process_key": row.get("process_key"),
        "title": row.get("title"),
        "description": row.get("description"),
        "version": row.get("version"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def template_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "template_key": row.get("template_key"),
        "workflow_key": row.get("workflow_key"),
        "title": row.get("title"),
        "domain": row.get("domain"),
        "status": row.get("status"),
    }


def instance_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "instance_key": row.get("instance_key"),
        "workflow_key": row.get("workflow_key"),
        "project_id": row.get("project_id"),
        "current_state_key": row.get("current_state_key"),
        "status": row.get("status"),
        "priority": row.get("priority"),
        "started_at": row.get("started_at"),
        "completed_at": row.get("completed_at"),
    }


def execution_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "execution_key": row.get("execution_key"),
        "instance_id": row.get("instance_id"),
        "workflow_key": row.get("workflow_key"),
        "status": row.get("status"),
        "current_step_key": row.get("current_step_key"),
        "attempt": row.get("attempt"),
        "duration_ms": row.get("duration_ms"),
    }


def task_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "task_key": row.get("task_key"),
        "instance_id": row.get("instance_id"),
        "title": row.get("title"),
        "task_type": row.get("task_type"),
        "status": row.get("status"),
        "priority": row.get("priority"),
        "assignee_id": row.get("assignee_id"),
        "due_at": row.get("due_at"),
    }


def queue_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "queue_key": row.get("queue_key"),
        "title": row.get("title"),
        "domain": row.get("domain"),
        "status": row.get("status"),
        "capacity": row.get("capacity"),
        "depth": row.get("depth"),
    }


def event_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "event_key": row.get("event_key"),
        "instance_id": row.get("instance_id"),
        "event_type": row.get("event_type"),
        "source": row.get("source"),
    }


def approval_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "approval_key": row.get("approval_key"),
        "instance_id": row.get("instance_id"),
        "level": row.get("level"),
        "status": row.get("status"),
        "approver_id": row.get("approver_id"),
    }


def rule_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "rule_key": row.get("rule_key"),
        "workflow_key": row.get("workflow_key"),
        "title": row.get("title"),
        "domain": row.get("domain"),
        "expression": row.get("expression"),
        "priority": row.get("priority"),
        "status": row.get("status"),
    }


def schedule_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "schedule_key": row.get("schedule_key"),
        "workflow_key": row.get("workflow_key"),
        "cron_expr": row.get("cron_expr"),
        "status": row.get("status"),
        "next_run_at": row.get("next_run_at"),
    }


def timer_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "timer_key": row.get("timer_key"),
        "instance_id": row.get("instance_id"),
        "fire_at": row.get("fire_at"),
        "status": row.get("status"),
    }


def notification_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "notification_key": row.get("notification_key"),
        "title": row.get("title"),
        "channel": row.get("channel"),
        "status": row.get("status"),
    }


def audit_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "audit_key": row.get("audit_key"),
        "action": row.get("action"),
        "resource_type": row.get("resource_type"),
        "resource_id": row.get("resource_id"),
        "created_at": row.get("created_at"),
    }


def history_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "instance_id": row.get("instance_id"),
        "from_state_key": row.get("from_state_key"),
        "to_state_key": row.get("to_state_key"),
        "transition_key": row.get("transition_key"),
        "note": row.get("note"),
        "created_at": row.get("created_at"),
    }


def monitoring_dto(payload: dict[str, Any]) -> dict[str, object]:
    return {"monitoring": payload}
