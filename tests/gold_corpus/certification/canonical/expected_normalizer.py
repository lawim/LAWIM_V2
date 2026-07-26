"""ExpectedNormalizer — transforms Gold Corpus expected spec into canonical form."""

from typing import Any, Dict, List, Optional

from tests.gold_corpus.certification.canonical.canonical_turn import (
    CanonicalTurn, CanonicalValue,
)
from tests.gold_corpus.certification.canonical.enum_mapping import (
    INTENT_MAP, PHASE_MAP, PENDING_ACTION_MAP, BUSINESS_ACTION_MAP,
    LANGUAGE_MAP, map_value,
)


class ExpectedNormalizer:
    """Normalize expected specification from Gold Corpus to canonical form."""

    def normalize(self, expected: Dict[str, Any]) -> CanonicalTurn:
        """Convert expected spec dict to canonical turn."""
        conv = expected.get("conversation", {})
        es = expected.get("expected_state", {})
        eb = expected.get("expected_business", {})
        el = expected.get("expected_language", {})

        turn = CanonicalTurn(
            conversation_id=conv.get("id", "unknown"),
            status="expected",
        )

        # Intent
        intent_raw = es.get("intent", "unknown")
        turn.intent = CanonicalValue(
            value=map_value(INTENT_MAP, intent_raw, intent_raw),
            source="expected_state.intent",
            source_type="CORPUS_SPECIFICATION",
            inferred=False,
            confidence=1.0 if intent_raw != "unknown" else 0.0,
        )

        # Phase (from qualification_status)
        qual_raw = es.get("qualification_status", "unknown")
        turn.phase = CanonicalValue(
            value=map_value(PHASE_MAP, qual_raw, qual_raw),
            source="expected_state.qualification_status",
            source_type="CORPUS_SPECIFICATION",
        )

        # Facts (from slots_filled)
        slots = es.get("slots_filled", {})
        for k, v in slots.items():
            turn.facts[k] = CanonicalValue(
                value=v,
                source=f"expected_state.slots_filled.{k}",
                source_type="CORPUS_SPECIFICATION",
            )

        # Pending user action (from next_action)
        next_raw = es.get("next_action", "none")
        turn.pending_user_action = CanonicalValue(
            value=map_value(PENDING_ACTION_MAP, next_raw, next_raw.lower()),
            source="expected_state.next_action",
            source_type="CORPUS_SPECIFICATION",
        )

        # Language
        lang_raw = el.get("responses_language", el.get("primary_language", "unknown"))
        turn.conversation_language = CanonicalValue(
            value=map_value(LANGUAGE_MAP, lang_raw, lang_raw),
            source="expected_language.responses_language",
            source_type="CORPUS_SPECIFICATION",
        )
        turn.effective_language = CanonicalValue(
            value=map_value(LANGUAGE_MAP, lang_raw, lang_raw),
            source="expected_language.primary_language",
            source_type="CORPUS_SPECIFICATION",
        )

        # Business action
        biz_raw = eb.get("business_action", "none")
        turn.business_action = CanonicalValue(
            value=map_value(BUSINESS_ACTION_MAP, biz_raw, biz_raw),
            source="expected_business.business_action",
            source_type="CORPUS_SPECIFICATION",
        )

        return turn
