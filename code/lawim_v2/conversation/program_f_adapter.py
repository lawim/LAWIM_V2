from __future__ import annotations

import copy
import json
import logging
from datetime import datetime, timezone
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


class _MemoryJourneyRepository:
    _shared: dict[str, dict[str, Any]] = {}

    def __init__(self) -> None:
        self._states = self._shared

    def load(self, conversation_id: str) -> dict[str, Any] | None:
        return self._states.get(conversation_id)

    def save(self, conversation_id: str, data: dict[str, Any]) -> None:
        self._states[conversation_id] = data

    def delete(self, conversation_id: str) -> None:
        self._states.pop(conversation_id, None)


class ProgramFEngineAdapter:
    def __init__(
        self,
        repository: _MemoryJourneyRepository | None = None,
    ) -> None:
        if not HAS_PROGRAM_F:
            _log.error("Program F engine not available — install lawim_runtime")
            raise ImportError("lawim_runtime package required for ProgramFEngineAdapter")
        self._orchestrator = ConversationJourneyOrchestrator()
        self._repository = repository or _MemoryJourneyRepository()

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
