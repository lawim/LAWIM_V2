from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from ..repository_introspection import table_exists
from .schema_ddl import SQLITE_BRAIN_TABLES_SCRIPT, POSTGRESQL_BRAIN_STATEMENTS


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class BrainRepositoryMixin:
    def brain_tables_present(self) -> bool:
        return table_exists(self, "brain_intents")

    def seed_brain_schema(self) -> None:
        if self.brain_tables_present():
            return
        driver = getattr(self, "_driver", "sqlite")
        if driver == "postgresql":
            for statement in POSTGRESQL_BRAIN_STATEMENTS:
                self.execute(statement)
        else:
            for statement in SQLITE_BRAIN_TABLES_SCRIPT.split(";"):
                stmt = statement.strip()
                if stmt:
                    self.execute(stmt)

    # brain intents
    def create_brain_intent(
        self,
        *,
        project_id: int,
        session_id: int | None = None,
        source_message_id: int | None = None,
        intent_type: str,
        entities_json: dict[str, Any] | None = None,
        language: str = "fr",
        confidence: int = 50,
        status: str = "hypothesis",
        engine_version: str = "1.0.0",
        origin: str = "conversation",
    ) -> dict[str, Any]:
        now = _utcnow()
        row = self.one(
            """
            INSERT INTO brain_intents
                (project_id, session_id, source_message_id, intent_type, entities_json,
                 language, confidence, status, engine_version, origin, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING *
            """,
            (
                project_id, session_id, source_message_id, intent_type,
                _json(entities_json or {}), language, confidence, status,
                engine_version, origin, now,
            ),
        )
        if row is None:
            return {}
        return dict(row)

    def list_brain_intents(
        self,
        project_id: int,
        *,
        intent_type: str | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        conditions = ["project_id = ?"]
        params: list[Any] = [project_id]
        if intent_type is not None:
            conditions.append("intent_type = ?")
            params.append(intent_type)
        if status is not None:
            conditions.append("status = ?")
            params.append(status)
        sql = f"SELECT * FROM brain_intents WHERE {' AND '.join(conditions)} ORDER BY id DESC LIMIT ?"
        params.append(limit)
        return [dict(row) for row in self.all(sql, tuple(params))]

    def update_brain_intent_status(
        self,
        intent_id: int,
        status: str,
    ) -> dict[str, Any] | None:
        row = self.one(
            "UPDATE brain_intents SET status = ? WHERE id = ? RETURNING *",
            (status, intent_id),
        )
        return dict(row) if row else None

    # brain memory items
    def create_brain_memory(
        self,
        *,
        project_id: int,
        kind: str,
        memory_key: str,
        label: str,
        value: str,
        source_table: str | None = None,
        source_id: int | None = None,
        confidence: int = 50,
        status: str = "active",
        is_global: bool = False,
        field_key: str | None = None,
        metadata_json: dict[str, Any] | None = None,
        created_at: str | None = None,
    ) -> dict[str, Any]:
        now = created_at or _utcnow()
        row = self.one(
            """
            INSERT INTO brain_memory_items
                (project_id, memory_key, kind, label, value, source_table, source_id,
                 confidence, status, is_global, field_key, metadata_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING *
            """,
            (
                project_id, memory_key, kind, label, value, source_table, source_id,
                confidence, status, 1 if is_global else 0, field_key,
                _json(metadata_json or {}), now, now,
            ),
        )
        if row is None:
            return {}
        return dict(row)

    def get_brain_memory(self, project_id: int, memory_key: str) -> dict[str, Any] | None:
        row = self.one(
            "SELECT * FROM brain_memory_items WHERE project_id = ? AND memory_key = ?",
            (project_id, memory_key),
        )
        return dict(row) if row else None

    def list_brain_memory(
        self,
        project_id: int,
        *,
        kind: str | None = None,
        status: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        conditions = ["project_id = ?"]
        params: list[Any] = [project_id]
        if kind is not None:
            conditions.append("kind = ?")
            params.append(kind)
        if status is not None:
            conditions.append("status = ?")
            params.append(status)
        sql = f"SELECT * FROM brain_memory_items WHERE {' AND '.join(conditions)} ORDER BY updated_at DESC LIMIT ?"
        params.append(limit)
        return [dict(row) for row in self.all(sql, tuple(params))]

    def update_brain_memory(
        self,
        *,
        project_id: int,
        memory_key: str,
        kind: str | None = None,
        status: str | None = None,
        confidence: int | None = None,
        updated_at: str | None = None,
    ) -> dict[str, Any] | None:
        now = updated_at or _utcnow()
        sets: list[str] = ["updated_at = ?"]
        params: list[Any] = [now]
        if kind is not None:
            sets.append("kind = ?")
            params.append(kind)
        if status is not None:
            sets.append("status = ?")
            params.append(status)
        if confidence is not None:
            sets.append("confidence = ?")
            params.append(confidence)
        params.extend([project_id, memory_key])
        row = self.one(
            f"UPDATE brain_memory_items SET {', '.join(sets)} WHERE project_id = ? AND memory_key = ? RETURNING *",
            tuple(params),
        )
        return dict(row) if row else None

    def expire_brain_memory(self, project_id: int, older_than_minutes: int = 60) -> int:
        from datetime import datetime, timezone, timedelta
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=older_than_minutes)).replace(microsecond=0).isoformat()
        self.execute(
            """
            UPDATE brain_memory_items SET status = 'expired', updated_at = ?
            WHERE project_id = ? AND kind = 'temporary' AND status = 'active' AND created_at < ?
            """,
            (_utcnow(), project_id, cutoff),
        )
        return self.cursor.rowcount if hasattr(self, 'cursor') and self.cursor else 0

    # brain progression state
    def get_brain_progression(self, project_id: int, intent_type: str) -> dict[str, Any] | None:
        row = self.one(
            "SELECT * FROM brain_progression_state WHERE project_id = ? AND intent_type = ?",
            (project_id, intent_type),
        )
        return dict(row) if row else None

    def upsert_brain_progression(
        self,
        *,
        project_id: int,
        intent_type: str,
        current_step: int = 0,
        total_steps: int = 0,
        asked_questions: list[dict[str, Any]] | None = None,
        answers: dict[str, Any] | None = None,
        missing_fields: list[str] | None = None,
        next_question: str | None = None,
        next_question_key: str | None = None,
        status: str = "in_progress",
    ) -> dict[str, Any]:
        now = _utcnow()
        existing = self.get_brain_progression(project_id, intent_type)
        if existing:
            row = self.one(
                """
                UPDATE brain_progression_state SET
                    current_step = ?, total_steps = ?, asked_questions_json = ?,
                    answers_json = ?, missing_fields_json = ?, next_question = ?,
                    next_question_key = ?, status = ?, updated_at = ?
                WHERE project_id = ? AND intent_type = ?
                RETURNING *
                """,
                (
                    current_step, total_steps, _json(asked_questions or []),
                    _json(answers or {}), _json(missing_fields or []),
                    next_question, next_question_key, status, now,
                    project_id, intent_type,
                ),
            )
        else:
            row = self.one(
                """
                INSERT INTO brain_progression_state
                    (project_id, intent_type, current_step, total_steps, asked_questions_json,
                     answers_json, missing_fields_json, next_question, next_question_key,
                     status, schema_version, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '1.0.0', ?, ?)
                RETURNING *
                """,
                (
                    project_id, intent_type, current_step, total_steps,
                    _json(asked_questions or []), _json(answers or {}),
                    _json(missing_fields or []), next_question, next_question_key,
                    status, now, now,
                ),
            )
        return dict(row) if row else {}

    # brain suggestions
    def create_brain_suggestion(
        self,
        *,
        project_id: int,
        suggestion_type: str,
        content: str,
        justification: str = "",
        priority: str = "medium",
        status: str = "active",
        target_action: str | None = None,
        target_partner: str | None = None,
        language: str = "fr",
        expires_at: str | None = None,
    ) -> dict[str, Any]:
        now = _utcnow()
        row = self.one(
            """
            INSERT INTO brain_suggestions
                (project_id, suggestion_type, content, justification, priority, status,
                 target_action, target_partner, language, expires_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING *
            """,
            (
                project_id, suggestion_type, content, justification, priority, status,
                target_action, target_partner, language, expires_at, now,
            ),
        )
        if row is None:
            return {}
        return dict(row)

    def list_brain_suggestions(
        self,
        project_id: int,
        *,
        suggestion_type: str | None = None,
        status: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        conditions = ["project_id = ?"]
        params: list[Any] = [project_id]
        if suggestion_type is not None:
            conditions.append("suggestion_type = ?")
            params.append(suggestion_type)
        if status is not None:
            conditions.append("status = ?")
            params.append(status)
        sql = f"SELECT * FROM brain_suggestions WHERE {' AND '.join(conditions)} ORDER BY priority DESC, id DESC LIMIT ?"
        params.append(limit)
        return [dict(row) for row in self.all(sql, tuple(params))]

    def update_brain_suggestion_status(
        self,
        suggestion_id: int,
        status: str,
    ) -> dict[str, Any] | None:
        now = _utcnow()
        set_clause = "status = ?, "
        if status == "accepted":
            set_clause += "accepted_at = ?"
        elif status == "rejected":
            set_clause += "rejected_at = ?"
        else:
            set_clause += "created_at = created_at"
        row = self.one(
            f"UPDATE brain_suggestions SET {set_clause} WHERE id = ? RETURNING *",
            (status, now, suggestion_id) if status in {"accepted", "rejected"} else (status, suggestion_id),
        )
        return dict(row) if row else None
