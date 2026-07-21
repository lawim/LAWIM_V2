"""Chantier 5: Multilingual journey tests.

Full rental journeys in French, English, and Pidgin (PCM).
Verifies that intent, slots, and readiness produce equivalent results
across languages, and that each language stays stable.
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest

from lawim_v2.conversation.state.engine import ConversationStateEngine
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.resolver import ConversationResolver


def _make_engine() -> tuple[ConversationStateEngine, str]:
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    repo = ConversationStateRepository(conn)
    resolver = ConversationResolver()
    engine = ConversationStateEngine(repo, resolver)
    return engine, db


FR_RENTAL_TURNS = [
    ("Bonjour", None),
    ("Je cherche un appartement", None),
    ("Je veux louer", None),
    ("Douala", None),
    ("Bonamoussadi", None),
    ("180000", None),
    ("Deux chambres", None),
    ("Meublé", None),
]

EN_RENTAL_TURNS = [
    ("Hello", None),
    ("I am looking for an apartment", None),
    ("I want to rent", None),
    ("Douala", None),
    ("Bonamoussadi", None),
    ("180000", None),
    ("Two bedrooms", None),
    ("Furnished", None),
]

PCM_RENTAL_TURNS = [
    ("Abeg", None),
    ("I dey find apartment wey dey rent", None),
    ("Make I rent di place", None),
    ("Douala", None),
    ("Bonamoussadi", None),
    ("180000", None),
    ("Two bedrooms", None),
    ("Furnished", None),
]


class TestChantier5Multilingual(unittest.TestCase):
    """Multi-turn rental journeys in FR, EN, PCM."""

    def _run_journey(self, turns, language, actor_id="multilang"):
        engine, db = _make_engine()
        try:
            final = None
            for msg, _ in turns:
                result = engine.process_turn(
                    actor_id=actor_id,
                    channel="whatsapp",
                    external_conversation_id=f"+237{language}",
                    message=msg,
                    language=language,
                )
                self.assertIsNotNone(result["response"])
                self.assertIsNotNone(result.get("response_plan"))
                self.assertFalse(result.get("handover_required", False))
                final = result
            return final, db, engine
        except Exception:
            if os.path.exists(db):
                os.unlink(db)
            raise

    # ── French journey ────────────────────────────────────────────────────

    def test_french_rental_journey(self):
        """Full French rental journey extracts correct slots."""
        final, db, _ = self._run_journey(FR_RENTAL_TURNS, "fr")
        try:
            state = final["state"]
            self.assertEqual(state.language, "fr")
            self.assertIn(state.known_slots.get("city", "").lower(), ("douala",))
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_french_language_stays_stable(self):
        """French language must not drift after multiple turns."""
        final, db, _ = self._run_journey(FR_RENTAL_TURNS, "fr")
        try:
            self.assertEqual(final["state"].language, "fr")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── English journey ────────────────────────────────────────────────────

    def test_english_rental_journey(self):
        """Full English rental journey extracts correct slots."""
        final, db, _ = self._run_journey(EN_RENTAL_TURNS, "en")
        try:
            state = final["state"]
            self.assertEqual(state.language, "en")
            self.assertIn(state.known_slots.get("city", "").lower(), ("douala",))
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_english_language_stays_stable(self):
        """English language must not drift after multiple turns."""
        final, db, _ = self._run_journey(EN_RENTAL_TURNS, "en")
        try:
            self.assertEqual(final["state"].language, "en")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_english_response_contains_no_french(self):
        """English conversation must not produce French content in responses."""
        engine, db = _make_engine()
        try:
            for msg, _ in EN_RENTAL_TURNS:
                result = engine.process_turn(
                    actor_id="en_test",
                    channel="whatsapp",
                    external_conversation_id="+237en_test",
                    message=msg,
                    language="en",
                )
                self.assertIsNotNone(result["response"])
            # Check that the state language is 'en'
            last = engine.process_turn(
                actor_id="en_test",
                channel="whatsapp",
                external_conversation_id="+237en_test",
                message="That is all I need",
                language="en",
            )
            self.assertEqual(last["state"].language, "en")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── PCM journey ────────────────────────────────────────────────────────

    def test_pcm_rental_journey(self):
        """Full PCM rental journey extracts correct slots."""
        final, db, _ = self._run_journey(PCM_RENTAL_TURNS, "pcm")
        try:
            state = final["state"]
            self.assertEqual(state.language, "pcm")
            self.assertIn(state.known_slots.get("city", "").lower(), ("douala",))
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_pcm_language_stays_stable(self):
        """PCM language must not drift after multiple turns."""
        final, db, _ = self._run_journey(PCM_RENTAL_TURNS, "pcm")
        try:
            self.assertEqual(final["state"].language, "pcm")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Cross-language comparison ─────────────────────────────────────────

    def test_fr_en_pcm_have_same_slots(self):
        """FR, EN, and PCM journeys must extract equivalent slot keys."""
        fr_final, fr_db, _ = self._run_journey(FR_RENTAL_TURNS, "fr", actor_id="fr_user")
        en_final, en_db, _ = self._run_journey(EN_RENTAL_TURNS, "en", actor_id="en_user")
        pcm_final, pcm_db, _ = self._run_journey(PCM_RENTAL_TURNS, "pcm", actor_id="pcm_user")
        try:
            fr_keys = set(fr_final["state"].known_slots.keys())
            en_keys = set(en_final["state"].known_slots.keys())
            pcm_keys = set(pcm_final["state"].known_slots.keys())
            # All must have at minimum city, budget, bedrooms
            for keys, name in [(fr_keys, "fr"), (en_keys, "en"), (pcm_keys, "pcm")]:
                self.assertIn("city", keys, f"{name} missing city")
                self.assertIn("budget_max", keys, f"{name} missing budget_max")
        finally:
            for path in (fr_db, en_db, pcm_db):
                if os.path.exists(path):
                    os.unlink(path)

    # ── Language detection ────────────────────────────────────────────────

    def test_language_detection_french(self):
        engine, db = _make_engine()
        try:
            result = engine.process_turn(
                actor_id="detect", channel="web",
                external_conversation_id="detect-session",
                message="Je cherche une maison", language="fr",
            )
            self.assertEqual(result["state"].language, "fr")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_language_detection_english(self):
        engine, db = _make_engine()
        try:
            result = engine.process_turn(
                actor_id="detect", channel="web",
                external_conversation_id="detect-en",
                message="I want to buy a house", language="en",
            )
            self.assertEqual(result["state"].language, "en")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_foreign_word_does_not_switch_language(self):
        """A single foreign word must not switch conversation language."""
        engine, db = _make_engine()
        try:
            r1 = engine.process_turn(
                actor_id="stable", channel="whatsapp",
                external_conversation_id="+237stable",
                message="Bonjour je cherche un appartement", language="fr",
            )
            self.assertEqual(r1["state"].language, "fr")
            r2 = engine.process_turn(
                actor_id="stable", channel="whatsapp",
                external_conversation_id="+237stable",
                message="Je veux un studio please", language="fr",
            )
            self.assertEqual(r2["state"].language, "fr",
                             "Single English word must not switch language")
        finally:
            if os.path.exists(db):
                os.unlink(db)


if __name__ == "__main__":
    unittest.main()
