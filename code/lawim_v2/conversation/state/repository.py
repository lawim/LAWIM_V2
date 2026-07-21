from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from .errors import StateConflictError
from .state import ConversationState

logger = logging.getLogger(__name__)


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
        if row is None:
            return None
        if hasattr(row, 'keys'):
            return dict(row)
        columns = [desc[0] for desc in cur.description]
        return dict(zip(columns, row))


_NEW_COLUMNS = [
    ("case_id", "TEXT"),
    ("journey_code", "TEXT DEFAULT ''"),
    ("state_version", "INTEGER DEFAULT 1"),
    ("updated_by", "TEXT DEFAULT 'system'"),
    ("change_source", "TEXT DEFAULT ''"),
]


class ConversationStateRepository:
    def __init__(self, db) -> None:
        if not hasattr(db, 'fetch_one'):
            db = _ConnectionWrapper(db)
        self.db = db
        self._ensure_table()
        self._migrate_columns()

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

    def _migrate_columns(self) -> None:
        for col_name, col_type in _NEW_COLUMNS:
            try:
                self.db.execute(
                    f"ALTER TABLE conversation_states ADD COLUMN {col_name} {col_type}",
                )
            except Exception:
                pass

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
        existing = self.load(state.channel, state.channel_session_id)

        if existing is not None:
            expected = state.expected_version if state.expected_version is not None else state.state_version
            if existing.state_version != expected:
                logger.warning(
                    "StateConflict channel=%s session=%s expected_version=%d actual_version=%d",
                    state.channel, state.channel_session_id, expected, existing.state_version,
                )
                raise StateConflictError(
                    f"Version conflict for {state.channel}/{state.channel_session_id}: "
                    f"expected {expected}, got {existing.state_version}",
                    expected_version=expected,
                    actual_version=existing.state_version,
                )

            new_version = existing.state_version + 1
            self.db.execute(
                """UPDATE conversation_states SET
                    actor_id=?, language=?, current_intent=?, intent_confidence=?,
                    previous_intent=?, transaction_type=?,
                    known_slots=?, missing_slots=?, changed_slots=?,
                    last_user_message=?, last_lawim_message=?,
                    last_question_key=?, last_question_slot=?, last_action=?,
                    qualification_status=?, qualification_step=?,
                    selected_agent=?, handover_status=?, wizard_session_id=?,
                    case_id=?, journey_code=?, state_version=?, updated_by=?,
                    change_source=?,
                    updated_at=?
                WHERE channel=? AND channel_session_id=?""",
                [
                    str(state.actor_id) if state.actor_id else None,
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
                    state.case_id,
                    state.journey_code,
                    new_version,
                    state.updated_by,
                    state.change_source,
                    now,
                    state.channel,
                    state.channel_session_id,
                ],
            )
            state.state_version = new_version
            state.expected_version = None
            state.updated_at = now
        else:
            self.db.execute(
                """INSERT INTO conversation_states (
                    actor_id, channel, channel_session_id, language,
                    current_intent, intent_confidence, previous_intent, transaction_type,
                    known_slots, missing_slots, changed_slots,
                    last_user_message, last_lawim_message, last_question_key, last_question_slot, last_action,
                    qualification_status, qualification_step, selected_agent, handover_status,
                    wizard_session_id, case_id, journey_code, state_version, updated_by, change_source,
                    created_at, updated_at, version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
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
                    state.case_id,
                    state.journey_code,
                    1,
                    state.updated_by,
                    state.change_source,
                    now,
                    now,
                    state.version,
                ],
            )
            state.state_version = 1
            state.updated_at = now

        if not state.created_at:
            state.created_at = now

        return state

    def update(self, state: ConversationState) -> ConversationState:
        return self.save(state)

    def reload(self, channel: str, channel_session_id: str) -> ConversationState | None:
        return self.load(channel, channel_session_id)

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
            case_id=row.get("case_id"),
            journey_code=row.get("journey_code", ""),
            state_version=row.get("state_version", 1),
            updated_by=row.get("updated_by", "system"),
            change_source=row.get("change_source", ""),
        )
