from __future__ import annotations

import json
from typing import Any


class ConversationSessionRepository:
    def __init__(self, db: Any) -> None:
        self.db = db

    def create(
        self,
        *,
        user_id: int | None = None,
        channel_identity_id: int | None = None,
        channel: str | None = None,
        state: str = "NEW",
        project_id: int | None = None,
        dossier_id: int | None = None,
        expected_input: str | None = None,
        last_question_field: str | None = None,
        question_repeat_count: int = 0,
        loop_score: int = 0,
        human_handover_requested: bool = False,
    ) -> dict[str, Any]:
        now = _utcnow()
        with self.db._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO conversation_sessions (
                    user_id, channel_identity_id, channel, state, project_id, dossier_id,
                    expected_input, last_question_field, question_repeat_count, loop_score,
                    human_handover_requested, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    channel_identity_id,
                    channel,
                    state,
                    project_id,
                    dossier_id,
                    expected_input,
                    last_question_field,
                    question_repeat_count,
                    loop_score,
                    1 if human_handover_requested else 0,
                    now,
                    now,
                ),
            )
            row = conn.execute(
                "SELECT * FROM conversation_sessions WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return dict(row) if row else {}

    def get_by_id(self, session_id: int) -> dict[str, Any] | None:
        row = self.db.one(
            "SELECT * FROM conversation_sessions WHERE id = ?", (session_id,)
        )
        return row

    def get_by_user_id(self, user_id: int, limit: int = 1) -> list[dict[str, Any]]:
        return self.db.all(
            "SELECT * FROM conversation_sessions WHERE user_id = ? ORDER BY updated_at DESC LIMIT ?",
            (user_id, limit),
        )

    def get_by_channel_identity(
        self, channel_identity_id: int, limit: int = 1
    ) -> list[dict[str, Any]]:
        return self.db.all(
            "SELECT * FROM conversation_sessions WHERE channel_identity_id = ? ORDER BY updated_at DESC LIMIT ?",
            (channel_identity_id, limit),
        )

    def list_active(self, user_id: int, limit: int = 1) -> list[dict[str, Any]]:
        return self.db.all(
            "SELECT * FROM conversation_sessions WHERE user_id = ? AND state NOT IN ('CLOSED', 'HUMAN_HANDOVER') ORDER BY updated_at DESC LIMIT ?",
            (user_id, limit),
        )

    def update(
        self,
        session_id: int,
        *,
        state: str | None = None,
        project_id: int | None = None,
        dossier_id: int | None = None,
        expected_input: str | None = None,
        last_question_field: str | None = None,
        question_repeat_count: int | None = None,
        loop_score: int | None = None,
        human_handover_requested: bool | None = None,
        updated_at: str | None = None,
    ) -> dict[str, Any]:
        now = updated_at or _utcnow()
        changes: dict[str, object] = {"updated_at": now}
        if state is not None:
            changes["state"] = state
        if project_id is not None:
            changes["project_id"] = project_id
        if dossier_id is not None:
            changes["dossier_id"] = dossier_id
        if expected_input is not None:
            changes["expected_input"] = expected_input
        if last_question_field is not None:
            changes["last_question_field"] = last_question_field
        if question_repeat_count is not None:
            changes["question_repeat_count"] = question_repeat_count
        if loop_score is not None:
            changes["loop_score"] = loop_score
        if human_handover_requested is not None:
            changes["human_handover_requested"] = 1 if human_handover_requested else 0
        assignments = ", ".join(f"{k} = ?" for k in changes)
        params = tuple(changes.values()) + (session_id,)
        with self.db._transaction() as conn:
            conn.execute(
                f"UPDATE conversation_sessions SET {assignments} WHERE id = ?", params
            )
        updated = self.get_by_id(session_id)
        return updated or {}


class ConversationMessageRepository:
    def __init__(self, db: Any) -> None:
        self.db = db

    def create(
        self,
        *,
        conversation_id: int,
        channel: str | None = None,
        channel_message_id: str | None = None,
        user_id: int | None = None,
        raw_message: str | None = None,
        normalized_message: str | None = None,
        message_key: str | None = None,
        metadata_json: str = "{}",
        is_duplicate: bool = False,
    ) -> dict[str, Any]:
        now = _utcnow()
        with self.db._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO conversation_messages (
                    conversation_id, channel, channel_message_id, user_id,
                    raw_message, normalized_message, message_key, metadata_json,
                    is_duplicate, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    conversation_id,
                    channel,
                    channel_message_id,
                    user_id,
                    raw_message,
                    normalized_message,
                    message_key,
                    metadata_json,
                    1 if is_duplicate else 0,
                    now,
                ),
            )
            row = conn.execute(
                "SELECT * FROM conversation_messages WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return dict(row) if row else {}

    def get_by_id(self, message_id: int) -> dict[str, Any] | None:
        return self.db.one(
            "SELECT * FROM conversation_messages WHERE id = ?", (message_id,)
        )

    def get_by_conversation_id(
        self, conversation_id: int, limit: int = 50
    ) -> list[dict[str, Any]]:
        return self.db.all(
            "SELECT * FROM conversation_messages WHERE conversation_id = ? ORDER BY created_at ASC LIMIT ?",
            (conversation_id, limit),
        )

    def get_by_message_key(self, message_key: str) -> dict[str, Any] | None:
        return self.db.one(
            "SELECT * FROM conversation_messages WHERE message_key = ?", (message_key,)
        )

    def count_by_conversation(self, conversation_id: int) -> int:
        return self.db.scalar(
            "SELECT COUNT(*) FROM conversation_messages WHERE conversation_id = ?",
            (conversation_id,),
        )


class ConversationDecisionRepository:
    def __init__(self, db: Any) -> None:
        self.db = db

    def save(self, decision: dict[str, Any]) -> dict[str, Any]:
        now = _utcnow()
        with self.db._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO conversation_decisions (
                    decision_id, conversation_id, user_id, channel, project_id, dossier_id,
                    raw_message, normalized_message, state_before, state_after,
                    selected_intent, intent_confidence, transaction_type, property_type,
                    action, action_status, requires_clarification, requires_human,
                    loop_detected, decision_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    decision.get("decision_id"),
                    decision.get("conversation_id"),
                    decision.get("user_id"),
                    decision.get("channel"),
                    decision.get("project_id"),
                    decision.get("dossier_id"),
                    decision.get("raw_message"),
                    decision.get("normalized_message"),
                    decision.get("state_before"),
                    decision.get("state_after"),
                    decision.get("selected_intent"),
                    decision.get("intent_confidence", 0.0),
                    decision.get("transaction_type"),
                    decision.get("property_type"),
                    decision.get("action"),
                    decision.get("action_status"),
                    1 if decision.get("requires_clarification") else 0,
                    1 if decision.get("requires_human") else 0,
                    1 if decision.get("loop_detected") else 0,
                    json.dumps(decision, ensure_ascii=False, default=str),
                    now,
                ),
            )
            row = conn.execute(
                "SELECT * FROM conversation_decisions WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return dict(row) if row else {}

    def get_by_decision_id(self, decision_id: str) -> dict[str, Any] | None:
        return self.db.one(
            "SELECT * FROM conversation_decisions WHERE decision_id = ?", (decision_id,)
        )

    def get_by_conversation_id(
        self, conversation_id: int, limit: int = 50
    ) -> list[dict[str, Any]]:
        return self.db.all(
            "SELECT * FROM conversation_decisions WHERE conversation_id = ? ORDER BY created_at DESC LIMIT ?",
            (conversation_id, limit),
        )

    def get_by_project_id(
        self, project_id: int, limit: int = 50
    ) -> list[dict[str, Any]]:
        return self.db.all(
            "SELECT * FROM conversation_decisions WHERE project_id = ? ORDER BY created_at DESC LIMIT ?",
            (project_id, limit),
        )


class ConversationFactRepository:
    def __init__(self, db: Any) -> None:
        self.db = db

    def save_fact(self, fact_data: dict[str, Any]) -> dict[str, Any]:
        now = _utcnow()
        with self.db._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO conversation_facts (
                    field, raw_value, normalized_value, source_message_id, source_channel,
                    source_type, confidence, confirmation_status, project_id, dossier_id,
                    conversation_id, supersedes_fact_id, valid_from, valid_to, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    fact_data.get("field"),
                    fact_data.get("raw_value"),
                    fact_data.get("normalized_value"),
                    fact_data.get("source_message_id"),
                    fact_data.get("source_channel"),
                    fact_data.get("source_type", "explicit"),
                    fact_data.get("confidence", 1.0),
                    fact_data.get("confirmation_status", "EXPLICIT"),
                    fact_data.get("project_id"),
                    fact_data.get("dossier_id"),
                    fact_data.get("conversation_id"),
                    fact_data.get("supersedes_fact_id"),
                    fact_data.get("valid_from", now),
                    fact_data.get("valid_to"),
                    now,
                    now,
                ),
            )
            row = conn.execute(
                "SELECT * FROM conversation_facts WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return dict(row) if row else {}

    def get_active_facts(
        self,
        project_id: int | None = None,
        dossier_id: int | None = None,
        conversation_id: int | None = None,
    ) -> list[dict[str, Any]]:
        conditions = ["valid_to IS NULL"]
        params: list[Any] = []
        if project_id is not None:
            conditions.append("project_id = ?")
            params.append(project_id)
        if dossier_id is not None:
            conditions.append("dossier_id = ?")
            params.append(dossier_id)
        if conversation_id is not None:
            conditions.append("conversation_id = ?")
            params.append(conversation_id)
        where = " AND ".join(conditions)
        return self.db.all(
            f"SELECT * FROM conversation_facts WHERE {where} ORDER BY created_at DESC",
            tuple(params),
        )

    def get_latest_confirmed_fact(
        self, field: str, project_id: int | None = None
    ) -> dict[str, Any] | None:
        conditions = ["field = ?", "valid_to IS NULL"]
        params: list[Any] = [field]
        if project_id is not None:
            conditions.append("project_id = ?")
            params.append(project_id)
        where = " AND ".join(conditions)
        return self.db.one(
            f"SELECT * FROM conversation_facts WHERE {where} ORDER BY created_at DESC LIMIT 1",
            tuple(params),
        )

    def get_facts_by_status(
        self, status: str, project_id: int | None = None
    ) -> list[dict[str, Any]]:
        conditions = ["confirmation_status = ?", "valid_to IS NULL"]
        params: list[Any] = [status]
        if project_id is not None:
            conditions.append("project_id = ?")
            params.append(project_id)
        where = " AND ".join(conditions)
        return self.db.all(
            f"SELECT * FROM conversation_facts WHERE {where} ORDER BY created_at DESC",
            tuple(params),
        )

    def supersede_fact(self, fact_id: int, timestamp: str) -> None:
        self.db.execute(
            "UPDATE conversation_facts SET confirmation_status = ?, valid_to = ?, updated_at = ? WHERE id = ?",
            ("SUPERSEDED", timestamp, _utcnow(), fact_id),
        )

    def update_status(self, fact_id: int, status: str) -> None:
        self.db.execute(
            "UPDATE conversation_facts SET confirmation_status = ?, updated_at = ? WHERE id = ?",
            (status, _utcnow(), fact_id),
        )


def _utcnow() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
