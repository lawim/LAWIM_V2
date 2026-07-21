"""Test handover lifecycle: initiate, accept, resolve, return to LAWIM.

The HandoverRepository and HandoverContinuityService are defined here since
the production modules do not yet exist.  Once they do, these tests should be
refactored to import from the real modules.
"""

from __future__ import annotations

import json
import sqlite3
import unittest
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


# ── Inline domain models (handover does not exist in production yet) ────

class HandoverStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    RETURNED = "RETURNED"
    CANCELLED = "CANCELLED"


@dataclass
class AgentHandover:
    handover_id: str = ""
    case_id: str = ""
    actor_id: str = ""
    reason: str = ""
    target_team: str = ""
    status: HandoverStatus = HandoverStatus.PENDING
    initiated_by: str = "LAWIM_AI"
    accepted_by: str | None = None
    resolved_by: str | None = None
    snapshot: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    accepted_at: str | None = None
    resolved_at: str | None = None
    notes: str = ""
    version: int = 1


# ── HandoverRepository ──────────────────────────────────────────────────

class _ConnectionWrapper:
    def __init__(self, conn):
        self.conn = conn

    def execute(self, sql: str, params: object = ()) -> Any:
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


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id() -> str:
    return uuid4().hex[:16]


class HandoverRepository:
    def __init__(self, db):
        if not hasattr(db, "fetch_one"):
            db = _ConnectionWrapper(db)
        self.db = db
        self._ensure_tables()

    def _ensure_tables(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS agent_handovers (
                handover_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                actor_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                target_team TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'PENDING',
                initiated_by TEXT NOT NULL DEFAULT 'LAWIM_AI',
                accepted_by TEXT,
                resolved_by TEXT,
                snapshot TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                accepted_at TEXT,
                resolved_at TEXT,
                notes TEXT DEFAULT '',
                version INTEGER DEFAULT 1
            )
        """)

    def save(self, handover: AgentHandover) -> AgentHandover:
        now = _utcnow()
        if not handover.created_at:
            handover.created_at = now
        self.db.execute(
            """INSERT INTO agent_handovers (
                handover_id, case_id, actor_id, reason, target_team,
                status, initiated_by, accepted_by, resolved_by,
                snapshot, created_at, accepted_at, resolved_at, notes, version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(handover_id) DO UPDATE SET
                status=excluded.status,
                accepted_by=excluded.accepted_by,
                resolved_by=excluded.resolved_by,
                snapshot=excluded.snapshot,
                accepted_at=excluded.accepted_at,
                resolved_at=excluded.resolved_at,
                notes=excluded.notes,
                version=excluded.version + 1""",
            [
                handover.handover_id, handover.case_id, handover.actor_id,
                handover.reason, handover.target_team,
                handover.status.value, handover.initiated_by,
                handover.accepted_by, handover.resolved_by,
                json.dumps(handover.snapshot),
                handover.created_at, handover.accepted_at,
                handover.resolved_at, handover.notes, handover.version,
            ],
        )
        return handover

    def load(self, handover_id: str) -> AgentHandover | None:
        row = self.db.fetch_one(
            "SELECT * FROM agent_handovers WHERE handover_id = ?",
            [handover_id],
        )
        if not row:
            return None
        return self._row_to_handover(row)

    def load_by_case(self, case_id: str) -> list[AgentHandover]:
        rows = self.db.fetch_all(
            "SELECT * FROM agent_handovers WHERE case_id = ? ORDER BY created_at DESC",
            [case_id],
        )
        return [self._row_to_handover(r) for r in rows]

    def load_active(self, case_id: str) -> AgentHandover | None:
        row = self.db.fetch_one(
            """SELECT * FROM agent_handovers
             WHERE case_id = ? AND status IN ('PENDING', 'ACCEPTED', 'IN_PROGRESS')
             ORDER BY created_at DESC LIMIT 1""",
            [case_id],
        )
        if not row:
            return None
        return self._row_to_handover(row)

    def _row_to_handover(self, row: dict) -> AgentHandover:
        return AgentHandover(
            handover_id=row["handover_id"],
            case_id=row["case_id"],
            actor_id=row["actor_id"],
            reason=row["reason"],
            target_team=row.get("target_team", ""),
            status=HandoverStatus(row["status"]),
            initiated_by=row.get("initiated_by", "LAWIM_AI"),
            accepted_by=row.get("accepted_by"),
            resolved_by=row.get("resolved_by"),
            snapshot=json.loads(row.get("snapshot", "{}")),
            created_at=row["created_at"],
            accepted_at=row.get("accepted_at"),
            resolved_at=row.get("resolved_at"),
            notes=row.get("notes", ""),
            version=row.get("version", 1),
        )


class HandoverContinuityService:
    def __init__(self, repository: HandoverRepository):
        self._repo = repository

    def initiate_handover(
        self,
        case_id: str,
        actor_id: str,
        reason: str,
        target_team: str = "",
        snapshot: dict | None = None,
        initiated_by: str = "LAWIM_AI",
    ) -> AgentHandover:
        handover = AgentHandover(
            handover_id=_new_id(),
            case_id=case_id,
            actor_id=actor_id,
            reason=reason,
            target_team=target_team,
            status=HandoverStatus.PENDING,
            initiated_by=initiated_by,
            snapshot=snapshot or {},
            created_at=_utcnow(),
        )
        return self._repo.save(handover)

    def accept_handover(
        self, handover_id: str, accepted_by: str,
    ) -> AgentHandover:
        handover = self._repo.load(handover_id)
        if handover is None:
            raise ValueError(f"Handover not found: {handover_id}")
        handover.status = HandoverStatus.ACCEPTED
        handover.accepted_by = accepted_by
        handover.accepted_at = _utcnow()
        return self._repo.save(handover)

    def resolve_handover(
        self, handover_id: str, resolved_by: str, notes: str = "",
    ) -> AgentHandover:
        handover = self._repo.load(handover_id)
        if handover is None:
            raise ValueError(f"Handover not found: {handover_id}")
        handover.status = HandoverStatus.RESOLVED
        handover.resolved_by = resolved_by
        handover.resolved_at = _utcnow()
        handover.notes = notes
        return self._repo.save(handover)

    def return_to_lawim(
        self, handover_id: str, notes: str = "",
    ) -> AgentHandover:
        handover = self._repo.load(handover_id)
        if handover is None:
            raise ValueError(f"Handover not found: {handover_id}")
        handover.status = HandoverStatus.RETURNED
        handover.notes = notes
        return self._repo.save(handover)

    def get_active_handover(self, case_id: str) -> AgentHandover | None:
        return self._repo.load_active(case_id)


class TestHandoverContinuity(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.repo = HandoverRepository(self.conn)
        self.service = HandoverContinuityService(self.repo)

    def tearDown(self):
        self.conn.close()

    def test_initiate_handover(self):
        h = self.service.initiate_handover(
            case_id="case_1",
            actor_id="actor_1",
            reason="User requests complex legal review",
            target_team="legal",
        )
        self.assertEqual(h.case_id, "case_1")
        self.assertEqual(h.status, HandoverStatus.PENDING)
        self.assertEqual(h.target_team, "legal")

    def test_accept_handover(self):
        h = self.service.initiate_handover(
            case_id="case_1", actor_id="actor_1",
            reason="Complex request",
        )
        accepted = self.service.accept_handover(h.handover_id, "agent_1")
        self.assertEqual(accepted.status, HandoverStatus.ACCEPTED)
        self.assertEqual(accepted.accepted_by, "agent_1")
        self.assertIsNotNone(accepted.accepted_at)

    def test_resolve_handover(self):
        h = self.service.initiate_handover(
            case_id="case_1", actor_id="actor_1",
            reason="Complex request",
        )
        self.service.accept_handover(h.handover_id, "agent_1")
        resolved = self.service.resolve_handover(
            h.handover_id, "agent_1", notes="Issue resolved",
        )
        self.assertEqual(resolved.status, HandoverStatus.RESOLVED)
        self.assertEqual(resolved.resolved_by, "agent_1")

    def test_return_to_lawim(self):
        h = self.service.initiate_handover(
            case_id="case_1", actor_id="actor_1",
            reason="Complex request",
        )
        returned = self.service.return_to_lawim(h.handover_id, notes="Handing back")
        self.assertEqual(returned.status, HandoverStatus.RETURNED)

    def test_handover_context_snapshot(self):
        snapshot = {
            "known_slots": {"city": "Douala", "budget": "150000"},
            "missing_slots": ["bedrooms"],
            "last_question": "How many bedrooms?",
        }
        h = self.service.initiate_handover(
            case_id="case_1", actor_id="actor_1",
            reason="Needs human review",
            target_team="legal",
            snapshot=snapshot,
        )
        self.assertEqual(h.snapshot["known_slots"]["city"], "Douala")
        self.assertIn("bedrooms", h.snapshot["missing_slots"])

    def test_active_handover_check(self):
        h = self.service.initiate_handover(
            case_id="case_1", actor_id="actor_1",
            reason="Complex request",
        )
        active = self.service.get_active_handover("case_1")
        self.assertIsNotNone(active)
        self.assertEqual(active.handover_id, h.handover_id)

    def test_active_handover_check_after_resolve(self):
        h = self.service.initiate_handover(
            case_id="case_1", actor_id="actor_1",
            reason="Complex request",
        )
        self.service.resolve_handover(h.handover_id, "agent_1")
        active = self.service.get_active_handover("case_1")
        self.assertIsNone(active)

    def test_active_handover_check_no_handover(self):
        active = self.service.get_active_handover("nonexistent_case")
        self.assertIsNone(active)


if __name__ == "__main__":
    unittest.main()
