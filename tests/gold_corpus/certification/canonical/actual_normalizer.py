"""ActualNormalizer — transforms runtime execution output into canonical form."""

from typing import Any, Dict, List, Optional

from tests.gold_corpus.certification.canonical.canonical_turn import (
    CanonicalTurn, CanonicalValue,
)
from tests.gold_corpus.certification.canonical.enum_mapping import (
    INTENT_MAP, PHASE_MAP, PENDING_ACTION_MAP, BUSINESS_ACTION_MAP,
    LANGUAGE_MAP, map_value,
)


class ActualNormalizer:
    """Normalize actual runtime output to canonical form."""

    def normalize_turn(self, actual_run: Dict[str, Any],
                        turn_dict: Dict[str, Any]) -> CanonicalTurn:
        """Convert a runtime turn dict to canonical turn."""
        turn = CanonicalTurn(
            conversation_id=actual_run.get("conversation_id", "unknown"),
            turn_index=turn_dict.get("turn_index", 0),
            status="actual",
        )

        # Intent
        intent_raw = turn_dict.get("intent_detected", "")
        if not intent_raw:
            intent_raw = turn_dict.get("intent", "")
        turn.intent = CanonicalValue(
            value=map_value(INTENT_MAP, intent_raw, intent_raw.lower()),
            source="RuntimeExecutor.intent_detected",
            source_type="RUNTIME_EXECUTION",
        )

        # Phase (from state or journey_status)
        state = turn_dict.get("state_after", {})
        phase_raw = state.get("journey_status", "")
        if not phase_raw:
            phase_raw = turn_dict.get("journey_status", "")
        turn.phase = CanonicalValue(
            value=map_value(PHASE_MAP, phase_raw, phase_raw.lower()),
            source="JourneyState.journey_status",
            source_type="RUNTIME_EXECUTION",
        )

        # Facts (from confirmed_facts)
        facts = state.get("confirmed_facts", {})
        if not facts:
            facts = state.get("facts", {})
        for k, v in facts.items():
            turn.facts[k] = CanonicalValue(
                value=v,
                source=f"JourneyState.confirmed_facts.{k}",
                source_type="RUNTIME_EXECUTION",
            )

        # Pending user action
        pending_raw = turn_dict.get("pending_after", "")
        if not pending_raw:
            pending_raw = state.get("pending_user_action", "NONE")
        turn.pending_user_action = CanonicalValue(
            value=map_value(PENDING_ACTION_MAP, pending_raw, pending_raw.lower()),
            source="RuntimeExecutor.pending_after",
            source_type="RUNTIME_EXECUTION",
        )

        # Business action (from business_actions list or state)
        biz_actions = turn_dict.get("business_actions", [])
        if biz_actions:
            biz_raw = biz_actions[0] if isinstance(biz_actions[0], str) else biz_actions[0].get("action", "")
            turn.business_action = CanonicalValue(
                value=map_value(BUSINESS_ACTION_MAP, biz_raw, biz_raw.lower()),
                source="RuntimeExecutor.business_actions[0]",
                source_type="RUNTIME_EXECUTION",
            )
        else:
            biz_raw = state.get("business_action", "none")
            turn.business_action = CanonicalValue(
                value=map_value(BUSINESS_ACTION_MAP, biz_raw, biz_raw.lower()),
                source="JourneyState.business_action",
                source_type="RUNTIME_EXECUTION",
            )

        # Language
        lang_raw = state.get("language", state.get("conversation_language", ""))
        if not lang_raw:
            lang_raw = turn_dict.get("language", "")
        turn.conversation_language = CanonicalValue(
            value=map_value(LANGUAGE_MAP, lang_raw, lang_raw.lower()),
            source="RuntimeExecutor.state.language",
            source_type="RUNTIME_EXECUTION",
        )
        turn.effective_language = CanonicalValue(
            value=map_value(LANGUAGE_MAP, lang_raw, lang_raw.lower()),
            source="RuntimeExecutor.state.language",
            source_type="RUNTIME_EXECUTION",
        )

        return turn
