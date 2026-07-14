from __future__ import annotations

from typing import Any

from ..domain.facts import Fact, FactStatus


class MemoryRepository:
    def __init__(self, db):
        self.db = db

    def save_fact(self, fact: Fact) -> Fact:
        row = self.db.execute(
            """INSERT INTO conversation_facts (
                field, raw_value, normalized_value, source_message_id, source_channel,
                source_type, confidence, confirmation_status, project_id, dossier_id,
                conversation_id, supersedes_fact_id, valid_from, valid_to, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id""",
            [
                fact.field,
                fact.raw_value,
                str(fact.normalized_value) if fact.normalized_value is not None else None,
                fact.source_message_id,
                fact.source_channel,
                fact.source_type,
                fact.confidence,
                fact.confirmation_status.value,
                fact.project_id,
                fact.dossier_id,
                fact.conversation_id,
                fact.supersedes_fact_id,
                fact.valid_from,
                fact.valid_to,
                fact.created_at,
                fact.updated_at,
            ],
        )
        fact.fact_id = str(row["id"])
        return fact

    def supersede_fact(self, fact_id: str, timestamp: str) -> None:
        self.db.execute(
            "UPDATE conversation_facts SET confirmation_status = ?, valid_to = ? WHERE id = ?",
            [FactStatus.SUPERSEDED.value, timestamp, int(fact_id)],
        )

    def update_fact_status(self, fact_id: str, status: FactStatus) -> None:
        self.db.execute(
            "UPDATE conversation_facts SET confirmation_status = ?, updated_at = ? WHERE id = ?",
            [status.value, __import__("datetime").datetime.utcnow().isoformat(), int(fact_id)],
        )

    def get_active_facts(
        self,
        project_id: int | None = None,
        dossier_id: int | None = None,
        conversation_id: int | None = None,
    ) -> list[Fact]:
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
        rows = self.db.fetch_all(
            f"SELECT * FROM conversation_facts WHERE {where} ORDER BY created_at DESC",
            params,
        )
        return [self._row_to_fact(r) for r in rows]

    def get_latest_confirmed_fact(self, field: str, project_id: int | None = None) -> Fact | None:
        conditions = ["field = ?", "valid_to IS NULL"]
        params: list[Any] = [field]
        if project_id is not None:
            conditions.append("project_id = ?")
            params.append(project_id)
        where = " AND ".join(conditions)
        row = self.db.fetch_one(
            f"SELECT * FROM conversation_facts WHERE {where} ORDER BY created_at DESC LIMIT 1",
            params,
        )
        if row:
            return self._row_to_fact(row)
        return None

    def get_facts_by_status(self, status: FactStatus, project_id: int | None = None) -> list[Fact]:
        conditions = ["confirmation_status = ?", "valid_to IS NULL"]
        params: list[Any] = [status.value]
        if project_id is not None:
            conditions.append("project_id = ?")
            params.append(project_id)
        where = " AND ".join(conditions)
        rows = self.db.fetch_all(
            f"SELECT * FROM conversation_facts WHERE {where} ORDER BY created_at DESC",
            params,
        )
        return [self._row_to_fact(r) for r in rows]

    def _row_to_fact(self, row: dict[str, Any]) -> Fact:
        import json
        normalized = row.get("normalized_value")
        if normalized:
            try:
                normalized = json.loads(normalized)
            except (json.JSONDecodeError, TypeError):
                pass
        return Fact(
            fact_id=str(row["id"]),
            field=row["field"],
            raw_value=row["raw_value"],
            normalized_value=normalized,
            source_message_id=row.get("source_message_id"),
            source_channel=row.get("source_channel"),
            source_type=row["source_type"],
            confidence=row["confidence"],
            confirmation_status=FactStatus(row["confirmation_status"]),
            project_id=row.get("project_id"),
            dossier_id=row.get("dossier_id"),
            conversation_id=row.get("conversation_id"),
            supersedes_fact_id=str(row["supersedes_fact_id"]) if row.get("supersedes_fact_id") else None,
            valid_from=row.get("valid_from"),
            valid_to=row.get("valid_to"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )
