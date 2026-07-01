from __future__ import annotations

from typing import Any


def agent_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "agent_key": row.get("agent_key"),
        "title": row.get("title"),
        "description": row.get("description"),
        "prompt_key": row.get("prompt_key"),
        "status": row.get("status"),
    }


def prompt_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "prompt_key": row.get("prompt_key"),
        "version": row.get("version"),
        "content": row.get("content"),
        "status": row.get("status"),
    }


def session_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "project_id": row.get("project_id"),
        "user_id": row.get("user_id"),
        "session_key": row.get("session_key"),
        "agent_key": row.get("agent_key"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def message_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "session_id": row.get("session_id"),
        "project_id": row.get("project_id"),
        "role": row.get("role"),
        "content": row.get("content"),
        "created_at": row.get("created_at"),
    }


def turn_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "session_id": row.get("session_id"),
        "agent_key": row.get("agent_key"),
        "mode": row.get("mode"),
        "provider": row.get("provider"),
        "fallback_used": bool(row.get("fallback_used")),
        "created_at": row.get("created_at"),
    }


def chat_response_dto(payload: dict[str, Any]) -> dict[str, object]:
    return {
        "session": session_dto(payload["session"]),
        "user_message": message_dto(payload["user_message"]),
        "assistant_message": message_dto(payload["assistant_message"]),
        "turn": turn_dto(payload["turn"]),
        "agent_key": payload.get("agent_key"),
        "mode": payload.get("mode"),
        "provider": payload.get("provider"),
        "fallback_used": payload.get("fallback_used"),
        "rag_chunks": payload.get("rag_chunks", []),
        "context_snapshot_key": payload.get("context_snapshot_key"),
    }
