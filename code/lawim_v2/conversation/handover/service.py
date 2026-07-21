from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .events import (
    HANDOVER_ACCEPTED,
    HANDOVER_INITIATED,
    HANDOVER_RESOLVED,
    HANDOVER_RETURNED,
)
from .models import AgentHandover, HandoverSnapshot, HandoverStatus, _now


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


class HandoverRepository:
    def __init__(self, db) -> None:
        if not hasattr(db, 'fetch_one'):
            db = _ConnectionWrapper(db)
        self.db = db
        self._ensure_table()

    def _ensure_table(self) -> None:
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS handovers (
                handover_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                conversation_id TEXT NOT NULL DEFAULT '',
                actor_id TEXT NOT NULL DEFAULT '',
                source_agent_id TEXT NOT NULL DEFAULT '',
                target_actor_or_team TEXT NOT NULL DEFAULT '',
                reason TEXT NOT NULL DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'NORMAL',
                summary TEXT NOT NULL DEFAULT '',
                context_snapshot TEXT NOT NULL DEFAULT '{}',
                open_questions TEXT NOT NULL DEFAULT '[]',
                recommended_action TEXT NOT NULL DEFAULT '',
                human_instructions TEXT NOT NULL DEFAULT '',
                human_decision TEXT NOT NULL DEFAULT '',
                human_decision_notes TEXT NOT NULL DEFAULT '',
                next_action TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'REQUESTED',
                created_at TEXT NOT NULL,
                accepted_at TEXT NOT NULL DEFAULT '',
                resolved_at TEXT NOT NULL DEFAULT '',
                returned_at TEXT
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS handover_snapshots (
                snapshot_id TEXT PRIMARY KEY,
                handover_id TEXT NOT NULL,
                case_id TEXT NOT NULL,
                conversation_state TEXT NOT NULL DEFAULT '{}',
                known_slots TEXT NOT NULL DEFAULT '{}',
                missing_slots TEXT NOT NULL DEFAULT '[]',
                active_intent TEXT NOT NULL DEFAULT '',
                qualification_readiness TEXT NOT NULL DEFAULT '',
                last_question TEXT NOT NULL DEFAULT '',
                language TEXT NOT NULL DEFAULT 'fr',
                interaction_count INTEGER NOT NULL DEFAULT 0,
                recent_messages TEXT NOT NULL DEFAULT '[]',
                created_at TEXT NOT NULL
            )
        """)
        self.db.execute("""
            CREATE INDEX IF NOT EXISTS idx_handover_case
            ON handovers(case_id, status)
        """)
        self.db.execute("""
            CREATE INDEX IF NOT EXISTS idx_handover_actor
            ON handovers(actor_id, status)
        """)
        self.db.execute("""
            CREATE INDEX IF NOT EXISTS idx_handover_snapshot_handover
            ON handover_snapshots(handover_id)
        """)

    def save_handover(self, handover: AgentHandover) -> AgentHandover:
        if not handover.created_at:
            handover.created_at = _now()
        self.db.execute(
            """INSERT INTO handovers (
                handover_id, case_id, conversation_id, actor_id,
                source_agent_id, target_actor_or_team, reason, priority,
                summary, context_snapshot, open_questions, recommended_action,
                human_instructions, human_decision, human_decision_notes,
                next_action, status, created_at, accepted_at, resolved_at,
                returned_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(handover_id) DO UPDATE SET
                case_id=excluded.case_id,
                conversation_id=excluded.conversation_id,
                actor_id=excluded.actor_id,
                source_agent_id=excluded.source_agent_id,
                target_actor_or_team=excluded.target_actor_or_team,
                reason=excluded.reason,
                priority=excluded.priority,
                summary=excluded.summary,
                context_snapshot=excluded.context_snapshot,
                open_questions=excluded.open_questions,
                recommended_action=excluded.recommended_action,
                human_instructions=excluded.human_instructions,
                human_decision=excluded.human_decision,
                human_decision_notes=excluded.human_decision_notes,
                next_action=excluded.next_action,
                status=excluded.status,
                accepted_at=excluded.accepted_at,
                resolved_at=excluded.resolved_at,
                returned_at=excluded.returned_at""",
            [
                handover.handover_id,
                handover.case_id,
                handover.conversation_id,
                handover.actor_id,
                handover.source_agent_id,
                handover.target_actor_or_team,
                handover.reason,
                handover.priority,
                handover.summary,
                json.dumps(handover.context_snapshot, ensure_ascii=False),
                json.dumps(handover.open_questions, ensure_ascii=False),
                handover.recommended_action,
                handover.human_instructions,
                handover.human_decision,
                handover.human_decision_notes,
                handover.next_action,
                handover.status.value,
                handover.created_at,
                handover.accepted_at,
                handover.resolved_at,
                handover.returned_at,
            ],
        )
        return handover

    def load_handover(self, handover_id: str) -> AgentHandover | None:
        if not handover_id:
            return None
        row = self.db.fetch_one(
            "SELECT * FROM handovers WHERE handover_id = ?", [handover_id],
        )
        if not row:
            return None
        return self._row_to_handover(row)

    def load_active_handover(self, case_id: str) -> AgentHandover | None:
        if not case_id:
            return None
        active_statuses = [
            HandoverStatus.REQUESTED.value,
            HandoverStatus.QUEUED.value,
            HandoverStatus.ACCEPTED.value,
            HandoverStatus.IN_PROGRESS.value,
        ]
        placeholders = ",".join("?" for _ in active_statuses)
        row = self.db.fetch_one(
            f"SELECT * FROM handovers WHERE case_id = ? AND status IN ({placeholders}) ORDER BY created_at DESC LIMIT 1",
            [case_id, *active_statuses],
        )
        if not row:
            return None
        return self._row_to_handover(row)

    def load_handovers_by_actor(self, actor_id: str) -> list[AgentHandover]:
        if not actor_id:
            return []
        rows = self.db.fetch_all(
            "SELECT * FROM handovers WHERE actor_id = ? ORDER BY created_at DESC",
            [actor_id],
        )
        return [self._row_to_handover(row) for row in rows]

    def save_snapshot(self, snapshot: HandoverSnapshot) -> HandoverSnapshot:
        if not snapshot.created_at:
            snapshot.created_at = _now()
        self.db.execute(
            """INSERT INTO handover_snapshots (
                snapshot_id, handover_id, case_id, conversation_state,
                known_slots, missing_slots, active_intent,
                qualification_readiness, last_question, language,
                interaction_count, recent_messages, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(snapshot_id) DO UPDATE SET
                handover_id=excluded.handover_id,
                case_id=excluded.case_id,
                conversation_state=excluded.conversation_state,
                known_slots=excluded.known_slots,
                missing_slots=excluded.missing_slots,
                active_intent=excluded.active_intent,
                qualification_readiness=excluded.qualification_readiness,
                last_question=excluded.last_question,
                language=excluded.language,
                interaction_count=excluded.interaction_count,
                recent_messages=excluded.recent_messages""",
            [
                snapshot.snapshot_id,
                snapshot.handover_id,
                snapshot.case_id,
                json.dumps(snapshot.conversation_state, ensure_ascii=False),
                json.dumps(snapshot.known_slots, ensure_ascii=False),
                json.dumps(snapshot.missing_slots, ensure_ascii=False),
                snapshot.active_intent,
                snapshot.qualification_readiness,
                snapshot.last_question,
                snapshot.language,
                snapshot.interaction_count,
                json.dumps(snapshot.recent_messages, ensure_ascii=False),
                snapshot.created_at,
            ],
        )
        return snapshot

    def load_snapshot(self, snapshot_id: str) -> HandoverSnapshot | None:
        if not snapshot_id:
            return None
        row = self.db.fetch_one(
            "SELECT * FROM handover_snapshots WHERE snapshot_id = ?",
            [snapshot_id],
        )
        if not row:
            return None
        return self._row_to_snapshot(row)

    def _row_to_handover(self, row: dict[str, Any]) -> AgentHandover:
        def _load_json(val: str | None) -> Any:
            if not val:
                return {} if val is None else []
            try:
                return json.loads(val)
            except (json.JSONDecodeError, TypeError):
                return {}

        return AgentHandover(
            handover_id=row.get("handover_id", ""),
            case_id=row.get("case_id", ""),
            conversation_id=row.get("conversation_id", ""),
            actor_id=row.get("actor_id", ""),
            source_agent_id=row.get("source_agent_id", ""),
            target_actor_or_team=row.get("target_actor_or_team", ""),
            reason=row.get("reason", ""),
            priority=row.get("priority", "NORMAL"),
            summary=row.get("summary", ""),
            context_snapshot=_load_json(row.get("context_snapshot")),
            open_questions=_load_json(row.get("open_questions")),
            recommended_action=row.get("recommended_action", ""),
            human_instructions=row.get("human_instructions", ""),
            human_decision=row.get("human_decision", ""),
            human_decision_notes=row.get("human_decision_notes", ""),
            next_action=row.get("next_action", ""),
            status=HandoverStatus(row.get("status", "REQUESTED")),
            created_at=row.get("created_at", ""),
            accepted_at=row.get("accepted_at", ""),
            resolved_at=row.get("resolved_at", ""),
            returned_at=row.get("returned_at"),
        )

    def _row_to_snapshot(self, row: dict[str, Any]) -> HandoverSnapshot:
        def _load_json(val: str | None) -> Any:
            if not val:
                return {} if val is None else []
            try:
                return json.loads(val)
            except (json.JSONDecodeError, TypeError):
                return {}

        return HandoverSnapshot(
            snapshot_id=row.get("snapshot_id", ""),
            handover_id=row.get("handover_id", ""),
            case_id=row.get("case_id", ""),
            conversation_state=_load_json(row.get("conversation_state")),
            known_slots=_load_json(row.get("known_slots")),
            missing_slots=_load_json(row.get("missing_slots")),
            active_intent=row.get("active_intent", ""),
            qualification_readiness=row.get("qualification_readiness", ""),
            last_question=row.get("last_question", ""),
            language=row.get("language", "fr"),
            interaction_count=row.get("interaction_count", 0),
            recent_messages=_load_json(row.get("recent_messages")),
            created_at=row.get("created_at", ""),
        )


class HandoverContinuityService:
    def __init__(
        self,
        handover_repository: HandoverRepository,
        case_service=None,
    ) -> None:
        self._repository = handover_repository
        self._case_service = case_service
        self._event_handlers: dict[str, list[callable]] = {}

    def on(self, event_name: str, handler: callable) -> None:
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(handler)

    def _emit(self, event_name: str, **kwargs) -> None:
        for handler in self._event_handlers.get(event_name, []):
            handler(**kwargs)

    def initiate_handover(
        self,
        case_id: str = "",
        conversation_id: str = "",
        actor_id: str = "",
        reason: str = "",
        summary: str = "",
        context: dict[str, Any] | None = None,
        target_team: str = "",
    ) -> AgentHandover:
        if not case_id:
            raise ValueError("case_id is required to initiate a handover")
        if not reason:
            raise ValueError("reason is required to initiate a handover")
        if not target_team:
            raise ValueError("target_team is required to initiate a handover")

        now = _now()
        handover_id = str(uuid4())
        handover = AgentHandover(
            handover_id=handover_id,
            case_id=case_id,
            conversation_id=conversation_id,
            actor_id=actor_id,
            source_agent_id="LAWIM_AI",
            target_actor_or_team=target_team,
            reason=reason,
            priority="NORMAL",
            summary=summary,
            context_snapshot=context or {},
            status=HandoverStatus.REQUESTED,
            created_at=now,
        )

        if self._case_service is not None:
            case = self._case_service.get_case(case_id)
            if case is not None:
                case.handover_status = HandoverStatus.REQUESTED.value
                self._case_service.update_case(case)

        result = self._repository.save_handover(handover)
        self._emit(HANDOVER_INITIATED, handover=result)
        return result

    def accept_handover(self, handover_id: str) -> AgentHandover:
        if not handover_id:
            raise ValueError("handover_id is required")

        handover = self._repository.load_handover(handover_id)
        if handover is None:
            raise ValueError(f"Handover {handover_id} not found")

        if handover.status not in (HandoverStatus.REQUESTED, HandoverStatus.QUEUED):
            raise ValueError(
                f"Cannot accept handover in status {handover.status.value}"
            )

        now = _now()
        handover.status = HandoverStatus.ACCEPTED
        handover.accepted_at = now
        result = self._repository.save_handover(handover)

        if self._case_service is not None:
            case = self._case_service.get_case(handover.case_id)
            if case is not None:
                case.handover_status = HandoverStatus.ACCEPTED.value
                self._case_service.update_case(case)

        self._emit(HANDOVER_ACCEPTED, handover=result)
        return result

    def resolve_handover(
        self,
        handover_id: str,
        decision: str = "",
        notes: str = "",
    ) -> AgentHandover:
        if not handover_id:
            raise ValueError("handover_id is required")

        handover = self._repository.load_handover(handover_id)
        if handover is None:
            raise ValueError(f"Handover {handover_id} not found")

        if handover.status != HandoverStatus.ACCEPTED:
            raise ValueError(
                f"Cannot resolve handover in status {handover.status.value}; "
                "must be ACCEPTED"
            )

        now = _now()
        handover.status = HandoverStatus.RESOLVED
        handover.human_decision = decision
        handover.human_decision_notes = notes
        handover.resolved_at = now
        result = self._repository.save_handover(handover)

        if self._case_service is not None:
            case = self._case_service.get_case(handover.case_id)
            if case is not None:
                case.handover_status = None
                self._case_service.update_case(case)

        self._emit(HANDOVER_RESOLVED, handover=result)
        return result

    def return_to_lawim(
        self,
        handover_id: str,
        human_instructions: str = "",
        next_action: str = "",
    ) -> AgentHandover:
        if not handover_id:
            raise ValueError("handover_id is required")
        if not human_instructions:
            raise ValueError("human_instructions is required for LAWIM return")
        if not next_action:
            raise ValueError("next_action is required for LAWIM return")

        handover = self._repository.load_handover(handover_id)
        if handover is None:
            raise ValueError(f"Handover {handover_id} not found")

        now = _now()
        handover.status = HandoverStatus.RETURNED_TO_LAWIM
        handover.human_instructions = human_instructions
        handover.next_action = next_action
        handover.returned_at = now
        result = self._repository.save_handover(handover)

        if self._case_service is not None:
            case = self._case_service.get_case(handover.case_id)
            if case is not None:
                case.handover_status = None
                self._case_service.update_case(case)

        self._emit(HANDOVER_RETURNED, handover=result)
        return result

    def get_active_handover(self, case_id: str) -> AgentHandover | None:
        if not case_id:
            return None
        return self._repository.load_active_handover(case_id)

    def create_snapshot(
        self,
        handover_id: str = "",
        case_id: str = "",
        conversation_state: dict[str, Any] | None = None,
        slots: dict[str, Any] | None = None,
    ) -> HandoverSnapshot:
        if not handover_id:
            raise ValueError("handover_id is required")
        if not case_id:
            raise ValueError("case_id is required")

        snapshot_id = str(uuid4())
        snapshot = HandoverSnapshot(
            snapshot_id=snapshot_id,
            handover_id=handover_id,
            case_id=case_id,
            conversation_state=conversation_state or {},
            known_slots=slots or {},
            created_at=_now(),
        )
        return self._repository.save_snapshot(snapshot)

    def get_context(self, handover_id: str) -> dict[str, Any]:
        if not handover_id:
            return {}
        handover = self._repository.load_handover(handover_id)
        if handover is None:
            return {}
        return {
            "handover": handover.to_dict(),
            "case_id": handover.case_id,
            "conversation_id": handover.conversation_id,
            "actor_id": handover.actor_id,
            "summary": handover.summary,
            "context_snapshot": handover.context_snapshot,
            "open_questions": handover.open_questions,
            "recommended_action": handover.recommended_action,
            "human_instructions": handover.human_instructions,
            "human_decision": handover.human_decision,
            "human_decision_notes": handover.human_decision_notes,
            "next_action": handover.next_action,
        }
