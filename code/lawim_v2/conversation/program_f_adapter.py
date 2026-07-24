from __future__ import annotations

import copy
import json
import logging
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_log = logging.getLogger("lawim_v2.conversation.program_f_adapter")

try:
    from lawim_runtime.conversation.journey import (
        ConversationJourneyOrchestrator,
        JourneyState,
    )
    HAS_PROGRAM_F = True
except ImportError:
    ConversationJourneyOrchestrator = None  # type: ignore
    JourneyState = None  # type: ignore
    HAS_PROGRAM_F = False
    _log.warning("lawim_runtime not available — Program F engine disabled")


class _SQLiteJourneyRepository:
    def __init__(self, db_path: str = "") -> None:
        if not db_path:
            _data_dir = Path(os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3")).expanduser().parent
            _conv_dir = _data_dir / "conversation"
            _conv_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(_conv_dir / "program_f_state.sqlite3")
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS program_f_state (
                conversation_id TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        self._conn.commit()

    def load(self, conversation_id: str) -> dict[str, Any] | None:
        cur = self._conn.execute(
            "SELECT state_json FROM program_f_state WHERE conversation_id = ?",
            (conversation_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        try:
            return json.loads(row["state_json"])
        except (json.JSONDecodeError, KeyError):
            _log.warning("corrupt state for conversation %s", conversation_id)
            return None

    def save(self, conversation_id: str, data: dict[str, Any]) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO program_f_state (conversation_id, state_json, updated_at) VALUES (?, ?, ?)",
            (conversation_id, json.dumps(data, default=str), datetime.now(timezone.utc).isoformat()),
        )
        self._conn.commit()

    def delete(self, conversation_id: str) -> None:
        self._conn.execute("DELETE FROM program_f_state WHERE conversation_id = ?", (conversation_id,))
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


class ProgramFEngineAdapter:
    def __init__(
        self,
        repository: _SQLiteJourneyRepository | None = None,
        db_path: str = "",
        property_search_service: Any = None,
    ) -> None:
        if not HAS_PROGRAM_F:
            _log.error("Program F engine not available — install lawim_runtime")
            raise ImportError("lawim_runtime package required for ProgramFEngineAdapter")
        self._orchestrator = ConversationJourneyOrchestrator(
            property_search_service=property_search_service,
        )
        self._repository = repository or _SQLiteJourneyRepository(db_path=db_path)

    def process_turn(
        self,
        actor_id: int | str | None = None,
        channel: str = "web",
        external_conversation_id: str = "",
        message: str = "",
        language: str = "fr",
    ) -> dict[str, Any]:
        conversation_id = external_conversation_id or f"pf_{channel}_{actor_id or 'anon'}"

        raw = self._repository.load(conversation_id)
        if raw:
            state = self._deserialize_state(raw)
        else:
            state = JourneyState()
            state.conversation_id = conversation_id

        try:
            result = self._orchestrator.process(
                text=message,
                state=state,
                channel=channel,
            )
        except Exception as exc:
            _log.exception("ProgramFEngineAdapter.process failed")
            return {
                "state": self._serialize_state(state) if state else {},
                "response": self._safety_text(language),
                "response_plan": None,
                "handover_required": True,
                "wizard_completed": False,
                "actions": [{"action": "engine_failed", "status": "error", "error": str(exc)}],
            }

        rp = result.response_plan
        if rp and rp.message:
            response_text = rp.message
        elif rp and rp.question_text:
            response_text = rp.question_text
        else:
            response_text = ""

        if result.error:
            response_text = self._safety_text(language)
        elif not response_text:
            response_text = self._safety_text(language)

        if result.state:
            self._repository.save(conversation_id, self._serialize_state(result.state))
            state_serialized = self._serialize_state(result.state)
        else:
            state_serialized = {}

        actions = []
        if result.state and result.state.business_object_ids:
            actions.append({
                "action": "business_action",
                "status": "completed" if result.state.business_object_ids.get("success") else "failed",
                "result": dict(result.state.business_object_ids),
            })

        return {
            "state": state_serialized,
            "response": response_text,
            "response_plan": None,
            "handover_required": result.state and result.state.journey_status.value == "CANCELLED" or False,
            "wizard_completed": bool(state.business_object_ids) if state else False,
            "actions": actions,
        }

    def load_state(self, conversation_id: str) -> dict[str, Any] | None:
        return self._repository.load(conversation_id)

    def delete_state(self, conversation_id: str) -> None:
        self._repository.delete(conversation_id)

    @staticmethod
    def _serialize_state(state: JourneyState) -> dict[str, Any]:
        from dataclasses import asdict
        base = asdict(state)
        base["journey_status"] = state.journey_status.value
        return base

    @staticmethod
    def _deserialize_state(raw: dict[str, Any]) -> JourneyState:
        from lawim_runtime.conversation.journey import JourneyStatus
        data = dict(raw)
        if "journey_status" in data:
            try:
                data["journey_status"] = JourneyStatus(data["journey_status"])
            except ValueError:
                data["journey_status"] = JourneyStatus.STARTED
        return JourneyState(**data)

    @staticmethod
    def _safety_text(language: str) -> str:
        return "Je ne peux pas traiter votre message pour le moment. Veuillez réessayer."
