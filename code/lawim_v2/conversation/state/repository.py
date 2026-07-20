from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from .state import ConversationState


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


class ConversationStateRepository:
    def __init__(self, db) -> None:
        if not hasattr(db, 'fetch_one'):
            db = _ConnectionWrapper(db)
        self.db = db
        self._ensure_table()

    def _ensure_table(self) -> None:
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS conversation_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor_id TEXT,
                channel TEXT NOT NULL,
                channel_session_id TEXT NOT NULL,
                language TEXT DEFAULT 'fr',
                current_intent TEXT,
                intent_confidence REAL DEFAULT 0.0,
                previous_intent TEXT,
                transaction_type TEXT,
                known_slots TEXT DEFAULT '{}',
                missing_slots TEXT DEFAULT '[]',
                changed_slots TEXT DEFAULT '{}',
                last_user_message TEXT DEFAULT '',
                last_lawim_message TEXT DEFAULT '',
                last_question_key TEXT DEFAULT '',
                last_question_slot TEXT DEFAULT '',
                last_action TEXT DEFAULT '',
                qualification_status TEXT DEFAULT 'unqualified',
                qualification_step INTEGER DEFAULT 0,
                selected_agent TEXT,
                handover_status TEXT,
                wizard_session_id TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                version INTEGER DEFAULT 1,
                UNIQUE(channel, channel_session_id)
            )
        """)

    def load(self, channel: str, channel_session_id: str) -> ConversationState | None:
        row = self.db.fetch_one(
            "SELECT * FROM conversation_states WHERE channel = ? AND channel_session_id = ?",
            [channel, channel_session_id],
        )
        if not row:
            return None
        return self._row_to_state(row)

    def save(self, state: ConversationState) -> ConversationState:
        now = datetime.now(timezone.utc).isoformat()
        self.db.execute(
            """INSERT INTO conversation_states (
                actor_id, channel, channel_session_id, language,
                current_intent, intent_confidence, previous_intent, transaction_type,
                known_slots, missing_slots, changed_slots,
                last_user_message, last_lawim_message, last_question_key, last_question_slot, last_action,
                qualification_status, qualification_step, selected_agent, handover_status,
                wizard_session_id, created_at, updated_at, version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(channel, channel_session_id) DO UPDATE SET
                actor_id=excluded.actor_id, language=excluded.language,
                current_intent=excluded.current_intent, intent_confidence=excluded.intent_confidence,
                previous_intent=excluded.previous_intent, transaction_type=excluded.transaction_type,
                known_slots=excluded.known_slots, missing_slots=excluded.missing_slots,
                changed_slots=excluded.changed_slots,
                last_user_message=excluded.last_user_message, last_lawim_message=excluded.last_lawim_message,
                last_question_key=excluded.last_question_key, last_question_slot=excluded.last_question_slot, last_action=excluded.last_action,
                qualification_status=excluded.qualification_status, qualification_step=excluded.qualification_step,
                selected_agent=excluded.selected_agent, handover_status=excluded.handover_status,
                wizard_session_id=excluded.wizard_session_id,
                updated_at=excluded.updated_at, version=excluded.version + 1""",
            [
                str(state.actor_id) if state.actor_id else None,
                state.channel,
                state.channel_session_id,
                state.language,
                state.current_intent,
                state.intent_confidence,
                state.previous_intent,
                state.transaction_type,
                json.dumps(state.known_slots, ensure_ascii=False),
                json.dumps(state.missing_slots, ensure_ascii=False),
                json.dumps(state.changed_slots, ensure_ascii=False),
                state.last_user_message,
                state.last_lawim_message,
                state.last_question_key,
                state.last_question_slot,
                state.last_action,
                state.qualification_status,
                state.qualification_step,
                state.selected_agent,
                state.handover_status,
                state.wizard_session_id,
                now,
                now,
                state.version,
            ],
        )
        return state

    def update(self, state: ConversationState) -> None:
        self.save(state)

    def _row_to_state(self, row: dict[str, Any]) -> ConversationState:
        def _json_load(val: str | None) -> Any:
            if not val:
                return {}
            try:
                return json.loads(val)
            except (json.JSONDecodeError, TypeError):
                return {}

        return ConversationState(
            actor_id=row.get("actor_id"),
            channel=row.get("channel", ""),
            channel_session_id=row.get("channel_session_id", ""),
            language=row.get("language", "fr"),
            current_intent=row.get("current_intent"),
            intent_confidence=row.get("intent_confidence", 0.0),
            previous_intent=row.get("previous_intent"),
            transaction_type=row.get("transaction_type"),
            known_slots=_json_load(row.get("known_slots")),
            missing_slots=_json_load(row.get("missing_slots")),
            changed_slots=_json_load(row.get("changed_slots")),
            last_user_message=row.get("last_user_message", ""),
            last_lawim_message=row.get("last_lawim_message", ""),
            last_question_key=row.get("last_question_key", ""),
            last_question_slot=row.get("last_question_slot", ""),
            last_action=row.get("last_action", ""),
            qualification_status=row.get("qualification_status", "unqualified"),
            qualification_step=row.get("qualification_step", 0),
            selected_agent=row.get("selected_agent"),
            handover_status=row.get("handover_status"),
            wizard_session_id=row.get("wizard_session_id") or (str(row["id"]) if "wizard_session_id" in row else None),
            created_at=row.get("created_at", ""),
            updated_at=row.get("updated_at", ""),
            version=row.get("version", 1),
        )
