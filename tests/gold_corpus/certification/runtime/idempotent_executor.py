"""IdempotentRuntimeExecutor — exécute les conversations avec idempotence et restart réels.

Fournit un PropertySearchService mock qui simule la création métier avec idempotence.
Supporte les événements SERVICE_RESTART.
"""

import json
import os
import sys
import tempfile
import time
import hashlib
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

_base = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(_base, "lawim_runtime"))
sys.path.insert(0, os.path.join(_base, "code"))
sys.path.insert(0, _base)

from tests.gold_corpus.certification.runtime.models import ActualConversationRun, ActualTurn


class MockPropertySearchService:
    """Mock service that simulates business object creation with idempotence.

    Tracks idempotency keys to return consistent results on replay.
    """

    def __init__(self):
        self._results: Dict[str, dict] = {}
        self._call_count: Dict[str, int] = {}
        self._objects_created: Dict[str, str] = {}
        self._total_create_calls = 0

    def create_search_request(self, *, conversation_id, user_id=None, channel="web", facts=None, idempotency_key=""):
        from lawim_runtime.conversation.journey import BusinessActionResult

        self._total_create_calls += 1
        self._call_count[idempotency_key] = self._call_count.get(idempotency_key, 0) + 1
        is_replay = self._call_count[idempotency_key] > 1

        if idempotency_key in self._results:
            result = self._results[idempotency_key]
            return BusinessActionResult(
                success=result["success"],
                action="create_search_request",
                object_type="property_search_request",
                object_id=result["object_id"],
                message="DUPLICATE_DETECTED" if is_replay else result.get("message", ""),
                error_code=None,
            )

        object_id = f"obj_{hashlib.md5(idempotency_key.encode()).hexdigest()[:12]}"
        self._results[idempotency_key] = {
            "success": True,
            "object_id": object_id,
            "message": "CREATED",
        }
        self._objects_created[idempotency_key] = object_id

        return BusinessActionResult(
            success=True,
            action="create_search_request",
            object_type="property_search_request",
            object_id=object_id,
            message="CREATED",
            error_code=None,
        )

    @property
    def total_create_calls(self):
        return self._total_create_calls


class IdempotentRuntimeExecutor:
    """Executes conversations against real runtime with idempotence and restart support."""

    def __init__(self, property_search_service=None):
        self._adapter_class = ""
        self._orchestrator_class = ""
        self._call_count = 0
        self._service = property_search_service or MockPropertySearchService()
        self._db_path = None

    @property
    def service(self):
        return self._service

    def execute_conversation(self, conversation_spec: Dict[str, Any],
                              db_path: Optional[str] = None,
                              isolate_repo: bool = True) -> ActualConversationRun:
        """Execute conversation with optional persistence and restart handling."""
        from lawim_v2.conversation.program_f_adapter import ProgramFEngineAdapter

        own_db = False
        if db_path is None:
            fd, db_path = tempfile.mkstemp(suffix="_lawim_idemp.sqlite3")
            os.close(fd)
            own_db = True

        run = ActualConversationRun(
            conversation_id=conversation_spec.get("id", "test_conv"),
            runtime_called=True,
        )

        self._db_path = db_path

        try:
            adapter = ProgramFEngineAdapter(db_path=db_path, property_search_service=self._service)
            run.adapter_class = f"{ProgramFEngineAdapter.__module__}.{ProgramFEngineAdapter.__qualname__}"
            if hasattr(adapter, '_orchestrator'):
                run.orchestrator_class = (
                    f"{adapter._orchestrator.__class__.__module__}."
                    f"{adapter._orchestrator.__class__.__qualname__}"
                )

            messages = conversation_spec.get("messages", [])
            actor_id = f"gold_test_{conversation_spec.get('id', 'unknown')}"
            channel = conversation_spec.get("channel", "web")
            language = conversation_spec.get("language", "fr")

            i = 0
            while i < len(messages):
                msg = messages[i]

                if msg.get("role") == "system":
                    if "RESTART" in msg.get("text", "").upper():
                        turn = ActualTurn(turn_index=i, user_input="[SYSTEM_RESTART]")
                        state_before = adapter.load_state(f"pf_{channel}_{actor_id}")
                        turn.state_after = state_before or {}

                        # Recreate adapter (new instance, same db)
                        adapter = ProgramFEngineAdapter(
                            db_path=db_path,
                            property_search_service=self._service,
                        )
                        run.runtime_errors.append(f"Restart at turn {i}")
                        turn.assistant_output = "[RESTART_COMPLETE]"
                        run.turns.append(turn)
                        i += 1
                        continue

                if msg.get("role") != "user":
                    i += 1
                    continue

                turn_start = time.time()
                turn = ActualTurn(turn_index=i, user_input=msg.get("text", ""))

                try:
                    result = adapter.process_turn(
                        actor_id=actor_id,
                        channel=channel,
                        message=msg.get("text", ""),
                        language=language,
                    )

                    turn.duration_ms = (time.time() - turn_start) * 1000
                    turn.assistant_output = result.get("response", "")
                    turn.intent_detected = result.get("state", {}).get("current_intent", "")
                    turn.intent_confidence = result.get("state", {}).get("intent_confidence", 0)

                    state = result.get("state", {})
                    turn.state_after = state
                    turn.facts_after = state.get("confirmed_facts", {})
                    turn.pending_after = state.get("pending_user_action", "")

                    actions = result.get("actions", [])
                    turn.business_actions = [a.get("action", "") for a in actions] if actions else []

                    if state.get("business_object_ids"):
                        biz_ids = state["business_object_ids"]
                        if biz_ids.get("success"):
                            turn.business_actions.append(f"create_search_request:{biz_ids.get('object_id','')}")

                    self._call_count += 1
                    run.call_count += 1

                except Exception as e:
                    turn.error = str(e)
                    turn.duration_ms = (time.time() - turn_start) * 1000
                    run.runtime_errors.append(f"Turn {i}: {e}")

                run.turns.append(turn)
                i += 1

            run.total_duration_ms = sum(t.duration_ms for t in run.turns)

        finally:
            if own_db:
                try:
                    os.unlink(db_path)
                except OSError:
                    pass

        return run

    def replay_last_event(self, conversation_spec: Dict[str, Any],
                           db_path: str) -> ActualConversationRun:
        """Replay the last user message only for idempotence verification."""
        from lawim_v2.conversation.program_f_adapter import ProgramFEngineAdapter

        run = ActualConversationRun(
            conversation_id=conversation_spec.get("id", "test_conv"),
            runtime_called=True,
        )

        try:
            adapter = ProgramFEngineAdapter(db_path=db_path, property_search_service=self._service)
            run.adapter_class = f"{ProgramFEngineAdapter.__module__}.{ProgramFEngineAdapter.__qualname__}"

            messages = conversation_spec.get("messages", [])
            last_user_msg = None
            for msg in reversed(messages):
                if msg.get("role") == "user":
                    last_user_msg = msg
                    break

            if not last_user_msg:
                run.runtime_errors.append("No user message to replay")
                return run

            actor_id = f"gold_test_{conversation_spec.get('id', 'unknown')}"
            channel = conversation_spec.get("channel", "web")
            language = conversation_spec.get("language", "fr")

            turn_start = time.time()
            turn = ActualTurn(turn_index=999, user_input=last_user_msg.get("text", ""))

            try:
                result = adapter.process_turn(
                    actor_id=actor_id,
                    channel=channel,
                    message=last_user_msg.get("text", ""),
                    language=language,
                )

                turn.duration_ms = (time.time() - turn_start) * 1000
                turn.assistant_output = result.get("response", "")
                turn.intent_detected = result.get("state", {}).get("current_intent", "")
                turn.intent_confidence = result.get("state", {}).get("intent_confidence", 0)
                turn.state_after = result.get("state", {})
                turn.facts_after = result.get("state", {}).get("confirmed_facts", {})
                turn.pending_after = result.get("state", {}).get("pending_user_action", "")

                actions = result.get("actions", [])
                turn.business_actions = [a.get("action", "") for a in actions] if actions else []
                biz_ids = result.get("state", {}).get("business_object_ids", {})
                if biz_ids.get("success"):
                    turn.business_actions.append(f"create_search_request:{biz_ids.get('object_id','')}")

                run.call_count += 1

            except Exception as e:
                turn.error = str(e)
                turn.duration_ms = (time.time() - turn_start) * 1000
                run.runtime_errors.append(f"Replay error: {e}")

            run.turns.append(turn)
            run.total_duration_ms = turn.duration_ms

        finally:
            pass

        return run

    @staticmethod
    def extract_business_object_ids(state: dict) -> dict:
        return state.get("business_object_ids", {})

    @staticmethod
    def get_db_sha256(db_path: str) -> str:
        import hashlib
        with open(db_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
