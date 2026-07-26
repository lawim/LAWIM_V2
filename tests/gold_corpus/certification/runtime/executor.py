"""RuntimeExecutor — exécute une conversation contre le vrai runtime LAWIM.

Utilise ProgramFEngineAdapter et ConversationJourneyOrchestrator réels.
Chaque conversation utilise un repository SQLite isolé.
"""

import json
import os
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional

_base = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(_base, "lawim_runtime"))
sys.path.insert(0, os.path.join(_base, "code"))
sys.path.insert(0, _base)

from tests.gold_corpus.certification.runtime.models import (
    ActualConversationRun,
    ActualTurn,
)


class RuntimeExecutor:
    """Executes a conversation against the real LAWIM runtime.

    Each conversation gets its own isolated SQLite repository (temp file).
    """

    def __init__(self):
        self._adapter_class = ""
        self._orchestrator_class = ""
        self._call_count = 0

    def execute_conversation(self, conversation_spec: Dict[str, Any]) -> ActualConversationRun:
        """Execute a full conversation (all turns) against the runtime."""
        from lawim_v2.conversation.program_f_adapter import ProgramFEngineAdapter

        # Create isolated temp DB for this conversation
        db_fd, db_path = tempfile.mkstemp(suffix="_lawim_test.sqlite3")
        os.close(db_fd)

        run = ActualConversationRun(
            conversation_id=conversation_spec.get("id", "test_conv"),
            runtime_called=True,
        )

        try:
            adapter = ProgramFEngineAdapter(db_path=db_path)
            run.adapter_class = f"{ProgramFEngineAdapter.__module__}.{ProgramFEngineAdapter.__qualname__}"
            # Get orchestrator class name from the adapter's internal orchestrator
            if hasattr(adapter, '_orchestrator'):
                run.orchestrator_class = (
                    f"{adapter._orchestrator.__class__.__module__}."
                    f"{adapter._orchestrator.__class__.__qualname__}"
                )

            messages = conversation_spec.get("messages", [])
            actor_id = f"gold_test_{conversation_spec.get('id', 'unknown')}"
            channel = conversation_spec.get("channel", "web")
            language = conversation_spec.get("language", "fr")

            for i, msg in enumerate(messages):
                if msg.get("role") != "user":
                    continue

                turn_start = time.time()
                turn = ActualTurn(
                    turn_index=i,
                    user_input=msg.get("text", ""),
                )

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

                    self._call_count += 1
                    run.call_count += 1

                except Exception as e:
                    turn.error = str(e)
                    turn.duration_ms = (time.time() - turn_start) * 1000
                    run.runtime_errors.append(f"Turn {i}: {e}")

                run.turns.append(turn)

            run.total_duration_ms = sum(t.duration_ms for t in run.turns)

        finally:
            # Cleanup temp DB
            try:
                os.unlink(db_path)
            except OSError:
                pass

        return run

    @property
    def call_count(self) -> int:
        return self._call_count
