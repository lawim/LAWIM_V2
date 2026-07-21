from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from ..domain.case import CaseStatus, LawimCase


class _ConnectionWrapper:
    def __init__(self, conn) -> None:
        self.conn = conn

    def execute(self, sql: str, params: object = ()) -> object:
        cur = self.conn.execute(sql, params or ())
        self.conn.commit()
        return cur

    def fetch_one(self, sql: str, params: object = ()) -> dict | None:
        cur = self.conn.execute(sql, params or ())
        row = cur.fetchone()
        return dict(row) if row else None

    def fetch_all(self, sql: str, params: object = ()) -> list[dict]:
        cur = self.conn.execute(sql, params or ())
        return [dict(row) for row in cur.fetchall()]


class LawimCaseRepository:
    def __init__(self, db) -> None:
        if not hasattr(db, 'fetch_one'):
            db = _ConnectionWrapper(db)
        self.db = db
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS lawim_cases (
                case_id TEXT PRIMARY KEY,
                case_code TEXT NOT NULL DEFAULT '',
                case_type TEXT NOT NULL DEFAULT '',
                primary_actor_id TEXT NOT NULL DEFAULT '',
                title TEXT NOT NULL DEFAULT '',
                active_intent TEXT NOT NULL DEFAULT '',
                journey_code TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'DRAFT',
                active_language TEXT NOT NULL DEFAULT 'fr',
                qualification_state TEXT NOT NULL DEFAULT '{}',
                readiness_status TEXT NOT NULL DEFAULT 'not_started',
                property_reference TEXT,
                assigned_agent TEXT,
                handover_status TEXT,
                active_conversation_id TEXT,
                known_slots TEXT NOT NULL DEFAULT '{}',
                last_question_key TEXT NOT NULL DEFAULT '',
                last_question_slot TEXT NOT NULL DEFAULT '',
                summary TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                closed_at TEXT,
                version INTEGER NOT NULL DEFAULT 1
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS case_conversation_links (
                link_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                conversation_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                actor_id TEXT NOT NULL DEFAULT '',
                linked_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                unlinked_at TEXT
            )
        """)
        self.db.execute("""
            CREATE INDEX IF NOT EXISTS idx_case_actor
            ON lawim_cases(primary_actor_id, status)
        """)
        self.db.execute("""
            CREATE INDEX IF NOT EXISTS idx_case_conversation
            ON case_conversation_links(conversation_id)
        """)
        self.db.execute("""
            CREATE INDEX IF NOT EXISTS idx_case_link_case
            ON case_conversation_links(case_id)
        """)

    def save(self, case: LawimCase) -> LawimCase:
        now = datetime.now(timezone.utc).isoformat()
        if not case.created_at:
            case.created_at = now
        case.updated_at = now

        self.db.execute(
            """INSERT INTO lawim_cases (
                case_id, case_code, case_type, primary_actor_id, title,
                active_intent, journey_code, status, active_language,
                qualification_state, readiness_status, property_reference,
                assigned_agent, handover_status, active_conversation_id,
                known_slots, last_question_key, last_question_slot,
                summary, created_at, updated_at, closed_at, version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(case_id) DO UPDATE SET
                case_code=excluded.case_code,
                case_type=excluded.case_type,
                primary_actor_id=excluded.primary_actor_id,
                title=excluded.title,
                active_intent=excluded.active_intent,
                journey_code=excluded.journey_code,
                status=excluded.status,
                active_language=excluded.active_language,
                qualification_state=excluded.qualification_state,
                readiness_status=excluded.readiness_status,
                property_reference=excluded.property_reference,
                assigned_agent=excluded.assigned_agent,
                handover_status=excluded.handover_status,
                active_conversation_id=excluded.active_conversation_id,
                known_slots=excluded.known_slots,
                last_question_key=excluded.last_question_key,
                last_question_slot=excluded.last_question_slot,
                summary=excluded.summary,
                updated_at=excluded.updated_at,
                closed_at=excluded.closed_at,
                version=excluded.version + 1""",
            [
                case.case_id,
                case.case_code,
                case.case_type,
                case.primary_actor_id,
                case.title,
                case.active_intent,
                case.journey_code,
                case.status.value,
                case.active_language,
                json.dumps(case.qualification_state, ensure_ascii=False),
                case.readiness_status,
                case.property_reference,
                case.assigned_agent,
                case.handover_status,
                case.active_conversation_id,
                json.dumps(case.known_slots, ensure_ascii=False),
                case.last_question_key,
                case.last_question_slot,
                case.summary,
                case.created_at,
                case.updated_at,
                case.closed_at,
                case.version,
            ],
        )
        case.version += 1
        return case

    def load(self, case_id: str) -> LawimCase | None:
        if not case_id:
            return None
        row = self.db.fetch_one(
            "SELECT * FROM lawim_cases WHERE case_id = ?", [case_id],
        )
        if not row:
            return None
        return self._row_to_case(row)

    def load_by_actor(self, actor_id: str) -> list[LawimCase]:
        if not actor_id:
            return []
        rows = self.db.fetch_all(
            "SELECT * FROM lawim_cases WHERE primary_actor_id = ? ORDER BY updated_at DESC",
            [actor_id],
        )
        return [self._row_to_case(row) for row in rows]

    def load_active_by_actor(self, actor_id: str) -> list[LawimCase]:
        if not actor_id:
            return []
        active_statuses = [
            s.value for s in (
                CaseStatus.ACTIVE, CaseStatus.WAITING_USER,
                CaseStatus.WAITING_LAWIM, CaseStatus.READY,
                CaseStatus.IN_PROGRESS,
            )
        ]
        placeholders = ",".join("?" for _ in active_statuses)
        rows = self.db.fetch_all(
            f"SELECT * FROM lawim_cases WHERE primary_actor_id = ? AND status IN ({placeholders}) ORDER BY updated_at DESC",
            [actor_id, *active_statuses],
        )
        return [self._row_to_case(row) for row in rows]

    def load_by_conversation(self, conversation_id: str) -> LawimCase | None:
        if not conversation_id:
            return None
        row = self.db.fetch_one(
            """SELECT c.* FROM lawim_cases c
               INNER JOIN case_conversation_links l ON l.case_id = c.case_id
               WHERE l.conversation_id = ? AND l.is_active = 1
               LIMIT 1""",
            [conversation_id],
        )
        if not row:
            return None
        return self._row_to_case(row)

    def search(self, query: str) -> list[LawimCase]:
        if not query:
            return []
        pattern = f"%{query}%"
        rows = self.db.fetch_all(
            """SELECT * FROM lawim_cases
               WHERE case_id LIKE ?
                  OR case_code LIKE ?
                  OR primary_actor_id LIKE ?
                  OR title LIKE ?
                  OR property_reference LIKE ?
               ORDER BY updated_at DESC
               LIMIT 50""",
            [pattern, pattern, pattern, pattern, pattern],
        )
        return [self._row_to_case(row) for row in rows]

    def delete(self, case_id: str) -> bool:
        if not case_id:
            return False
        self.db.execute(
            "DELETE FROM lawim_cases WHERE case_id = ?", [case_id],
        )
        self.db.execute(
            "DELETE FROM case_conversation_links WHERE case_id = ?", [case_id],
        )
        return True

    def save_link(self, link) -> None:
        self.db.execute(
            """INSERT INTO case_conversation_links (
                link_id, case_id, conversation_id, channel, actor_id,
                linked_at, is_active, unlinked_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(link_id) DO UPDATE SET
                is_active=excluded.is_active,
                unlinked_at=excluded.unlinked_at""",
            [
                link.link_id,
                link.case_id,
                link.conversation_id,
                link.channel,
                link.actor_id,
                link.linked_at,
                1 if link.is_active else 0,
                link.unlinked_at,
            ],
        )

    def load_active_link(self, case_id: str) -> dict | None:
        return self.db.fetch_one(
            "SELECT * FROM case_conversation_links WHERE case_id = ? AND is_active = 1 LIMIT 1",
            [case_id],
        )

    def load_link_by_conversation(self, conversation_id: str) -> dict | None:
        return self.db.fetch_one(
            "SELECT * FROM case_conversation_links WHERE conversation_id = ? AND is_active = 1 LIMIT 1",
            [conversation_id],
        )

    def _row_to_case(self, row: dict[str, Any]) -> LawimCase:
        def _json_load(val: str | None) -> Any:
            if not val:
                return {}
            try:
                return json.loads(val)
            except (json.JSONDecodeError, TypeError):
                return {}

        return LawimCase(
            case_id=row.get("case_id", ""),
            case_code=row.get("case_code", ""),
            case_type=row.get("case_type", ""),
            primary_actor_id=row.get("primary_actor_id", ""),
            title=row.get("title", ""),
            active_intent=row.get("active_intent", ""),
            journey_code=row.get("journey_code", ""),
            status=CaseStatus(row.get("status", "DRAFT")),
            active_language=row.get("active_language", "fr"),
            qualification_state=_json_load(row.get("qualification_state")),
            readiness_status=row.get("readiness_status", "not_started"),
            property_reference=row.get("property_reference"),
            assigned_agent=row.get("assigned_agent"),
            handover_status=row.get("handover_status"),
            active_conversation_id=row.get("active_conversation_id"),
            known_slots=_json_load(row.get("known_slots")),
            last_question_key=row.get("last_question_key", ""),
            last_question_slot=row.get("last_question_slot", ""),
            summary=row.get("summary", ""),
            created_at=row.get("created_at", ""),
            updated_at=row.get("updated_at", ""),
            closed_at=row.get("closed_at"),
            version=row.get("version", 1),
        )
