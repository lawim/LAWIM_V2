from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from .relation_ddl import (
    SQLITE_RELATION_TABLES_SCRIPT,
    POSTGRESQL_RELATION_STATEMENTS,
    RELATION_TABLE_NAMES,
)


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class BrainRelationRepositoryMixin:
    def relation_tables_present(self) -> bool:
        from ..repository_introspection import table_exists
        return table_exists(self, "brain_relation_proposals")

    def seed_relation_schema(self) -> None:
        if self.relation_tables_present():
            return
        driver = getattr(self, "_driver", "sqlite")
        if driver == "postgresql":
            for statement in POSTGRESQL_RELATION_STATEMENTS:
                self.execute(statement)
        else:
            for statement in SQLITE_RELATION_TABLES_SCRIPT.split(";"):
                stmt = statement.strip()
                if stmt:
                    self.execute(stmt)

    def create_relation_proposal(
        self,
        *,
        project_id: int,
        relation_type: str,
        target_type: str,
        target_id: int,
        score: int = 50,
        justification: str = "",
        metadata_json: dict[str, Any] | None = None,
        status: str = "detected",
    ) -> dict[str, Any]:
        now = _utcnow()
        row = self.one(
            """
            INSERT INTO brain_relation_proposals
                (project_id, relation_type, target_type, target_id, score, justification,
                 metadata_json, status, proposed_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING *
            """,
            (project_id, relation_type, target_type, target_id, score, justification,
             _json(metadata_json or {}), status, now, now, now),
        )
        return dict(row) if row else {}

    def get_relation_proposal(self, proposal_id: int) -> dict[str, Any] | None:
        row = self.one(
            "SELECT * FROM brain_relation_proposals WHERE id = ?", (proposal_id,)
        )
        return dict(row) if row else None

    def update_relation_proposal_status(
        self, proposal_id: int, status: str
    ) -> dict[str, Any] | None:
        now = _utcnow()
        set_clause = "status = ?, updated_at = ?"
        if status == "accepted":
            set_clause += ", accepted_at = ?"
        elif status == "rejected":
            set_clause += ", rejected_at = ?"
        elif status == "consent_pending":
            set_clause += ", consent_requested_at = ?"
        elif status == "relation_established":
            set_clause += ", consent_granted_at = ?"

        params = [status, now]
        if status in ("accepted", "rejected", "consent_pending", "relation_established"):
            params.append(now)
        params.append(proposal_id)

        row = self.one(
            f"UPDATE brain_relation_proposals SET {set_clause} WHERE id = ? RETURNING *",
            tuple(params),
        )
        return dict(row) if row else None

    def list_relation_proposals(
        self,
        project_id: int,
        *,
        status: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        conditions = ["project_id = ?"]
        params: list[Any] = [project_id]
        if status is not None:
            conditions.append("status = ?")
            params.append(status)
        sql = f"SELECT * FROM brain_relation_proposals WHERE {' AND '.join(conditions)} ORDER BY score DESC, id DESC LIMIT ?"
        params.append(limit)
        return [dict(row) for row in self.all(sql, tuple(params))]

    def create_relation(
        self,
        *,
        project_id: int,
        relation_type: str,
        source_type: str,
        source_id: int | None,
        target_type: str,
        target_id: int,
        status: str = "established",
        metadata_json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        now = _utcnow()
        row = self.one(
            """
            INSERT INTO brain_relations
                (project_id, relation_type, source_type, source_id, target_type, target_id,
                 status, metadata_json, established_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING *
            """,
            (project_id, relation_type, source_type, source_id, target_type, target_id,
             status, _json(metadata_json or {}), now, now, now),
        )
        return dict(row) if row else {}

    def list_relations(
        self,
        project_id: int,
        *,
        relation_type: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        conditions = ["project_id = ?"]
        params: list[Any] = [project_id]
        if relation_type is not None:
            conditions.append("relation_type = ?")
            params.append(relation_type)
        sql = f"SELECT * FROM brain_relations WHERE {' AND '.join(conditions)} ORDER BY id DESC LIMIT ?"
        params.append(limit)
        return [dict(row) for row in self.all(sql, tuple(params))]

    def list_properties_for_matching(self) -> list[dict[str, Any]]:
        return [dict(row) for row in self.all(
            "SELECT * FROM properties WHERE status IN ('published', 'open') AND deleted_at IS NULL ORDER BY id"
        )]

    def list_partners_for_matching(self) -> list[dict[str, Any]]:
        return [dict(row) for row in self.all(
            "SELECT * FROM partner_profiles WHERE status = 'active' ORDER BY id"
        )]
