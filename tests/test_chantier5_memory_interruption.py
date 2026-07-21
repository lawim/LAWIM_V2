"""Chantier 5: Memory interruption tests.

Verifies that conversation state survives repository recreation (simulating
server restart, crash recovery, or DB reconnection). Checks that all critical
fields — slots, language, case_id, last_question, wizard_session_id — are
preserved when the state is reloaded from persistent storage.
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest

from lawim_v2.conversation.state.errors import StateConflictError
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.state import ConversationState


class TestChantier5MemoryInterruption(unittest.TestCase):
    """State persistence and recovery across repository lifecycle."""

    def setUp(self):
        self.db_path = tempfile.mktemp(suffix=".db")

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _make_state(self, **overrides) -> ConversationState:
        defaults = dict(
            channel="whatsapp",
            channel_session_id="+237600000001",
            language="fr",
            current_intent="rental_search",
            known_slots={"city": "Douala", "budget_max": 150000},
            missing_slots=["bedrooms"],
            last_question_key="bedrooms",
            last_question_slot="bedroom_count",
            qualification_status="in_progress",
            wizard_session_id="wiz_abc123",
            case_id="case_uuid_001",
            journey_code="SEARCH_RENTAL",
        )
        defaults.update(overrides)
        return ConversationState(**defaults)

    # ── Basic persistence ─────────────────────────────────────────────────

    def test_save_and_reload_state(self):
        conn1 = self._connect()
        repo1 = ConversationStateRepository(conn1)
        original = self._make_state()
        repo1.save(original)
        conn1.close()

        conn2 = self._connect()
        repo2 = ConversationStateRepository(conn2)
        loaded = repo2.load("whatsapp", "+237600000001")
        conn2.close()

        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.current_intent, "rental_search")
        self.assertEqual(loaded.known_slots.get("city"), "Douala")
        self.assertEqual(loaded.known_slots.get("budget_max"), 150000)

    def test_language_preserved_after_restart(self):
        conn1 = self._connect()
        repo1 = ConversationStateRepository(conn1)
        original = self._make_state(language="en")
        repo1.save(original)
        conn1.close()

        conn2 = self._connect()
        repo2 = ConversationStateRepository(conn2)
        loaded = repo2.load("whatsapp", "+237600000001")
        conn2.close()

        self.assertEqual(loaded.language, "en")

    def test_last_question_preserved(self):
        conn1 = self._connect()
        repo1 = ConversationStateRepository(conn1)
        original = self._make_state(
            last_question_key="budget_max",
            last_question_slot="budget_max",
        )
        repo1.save(original)
        conn1.close()

        conn2 = self._connect()
        repo2 = ConversationStateRepository(conn2)
        loaded = repo2.load("whatsapp", "+237600000001")
        conn2.close()

        self.assertEqual(loaded.last_question_key, "budget_max")
        self.assertEqual(loaded.last_question_slot, "budget_max")

    def test_wizard_session_id_preserved(self):
        conn1 = self._connect()
        repo1 = ConversationStateRepository(conn1)
        original = self._make_state(wizard_session_id="wiz_restored_001")
        repo1.save(original)
        conn1.close()

        conn2 = self._connect()
        repo2 = ConversationStateRepository(conn2)
        loaded = repo2.load("whatsapp", "+237600000001")
        conn2.close()

        self.assertEqual(loaded.wizard_session_id, "wiz_restored_001")

    def test_case_id_preserved(self):
        conn1 = self._connect()
        repo1 = ConversationStateRepository(conn1)
        original = self._make_state(case_id="case_persist_001")
        repo1.save(original)
        conn1.close()

        conn2 = self._connect()
        repo2 = ConversationStateRepository(conn2)
        loaded = repo2.load("whatsapp", "+237600000001")
        conn2.close()

        self.assertEqual(loaded.case_id, "case_persist_001")

    # ── Slot preservation ─────────────────────────────────────────────────

    def test_slots_preserved_after_restart(self):
        conn1 = self._connect()
        repo1 = ConversationStateRepository(conn1)
        original = self._make_state(
            known_slots={
                "city": "Yaoundé",
                "budget_max": 80000000,
                "property_type": "house",
                "bedroom_count": 4,
                "district": "Bastos",
            },
            missing_slots=["furnished", "move_in_date"],
            qualification_status="in_progress",
            qualification_step=5,
        )
        repo1.save(original)
        conn1.close()

        conn2 = self._connect()
        repo2 = ConversationStateRepository(conn2)
        loaded = repo2.load("whatsapp", "+237600000001")
        conn2.close()

        self.assertEqual(loaded.known_slots["city"], "Yaoundé")
        self.assertEqual(loaded.known_slots["budget_max"], 80000000)
        self.assertEqual(loaded.known_slots["property_type"], "house")
        self.assertEqual(loaded.known_slots["bedroom_count"], 4)
        self.assertEqual(loaded.known_slots["district"], "Bastos")
        self.assertIn("furnished", loaded.missing_slots)
        self.assertIn("move_in_date", loaded.missing_slots)
        self.assertEqual(loaded.qualification_status, "in_progress")
        self.assertEqual(loaded.qualification_step, 5)

    # ── State versioning after restart ────────────────────────────────────

    def test_state_version_preserved_after_recreation(self):
        conn1 = self._connect()
        repo1 = ConversationStateRepository(conn1)
        original = self._make_state()
        saved = repo1.save(original)
        version_after_first_save = saved.state_version
        repo1.save(saved)
        conn1.close()
        # state_version should now be 2

        conn2 = self._connect()
        repo2 = ConversationStateRepository(conn2)
        loaded = repo2.load("whatsapp", "+237600000001")
        conn2.close()

        self.assertIsNotNone(loaded)
        self.assertGreaterEqual(loaded.state_version, 2)

    # ── Update after restart ──────────────────────────────────────────────

    def test_update_after_restart(self):
        conn1 = self._connect()
        repo1 = ConversationStateRepository(conn1)
        original = self._make_state()
        repo1.save(original)
        conn1.close()

        conn2 = self._connect()
        repo2 = ConversationStateRepository(conn2)
        loaded = repo2.load("whatsapp", "+237600000001")
        loaded.current_intent = "buy_search"
        loaded.known_slots["city"] = "Yaoundé"
        updated = repo2.save(loaded)
        conn2.close()

        self.assertEqual(updated.current_intent, "buy_search")
        self.assertEqual(updated.known_slots["city"], "Yaoundé")

    # ── Journey code and intent preserved ─────────────────────────────────

    def test_journey_code_preserved(self):
        conn1 = self._connect()
        repo1 = ConversationStateRepository(conn1)
        original = self._make_state(journey_code="SEARCH_PURCHASE")
        repo1.save(original)
        conn1.close()

        conn2 = self._connect()
        repo2 = ConversationStateRepository(conn2)
        loaded = repo2.load("whatsapp", "+237600000001")
        conn2.close()

        self.assertEqual(loaded.journey_code, "SEARCH_PURCHASE")

    # ── Multiple state entries ────────────────────────────────────────────

    def test_multiple_independent_states_survive_restart(self):
        conn1 = self._connect()
        repo1 = ConversationStateRepository(conn1)
        repo1.save(self._make_state(
            channel="whatsapp", channel_session_id="+237aaa",
            known_slots={"city": "Douala"},
        ))
        repo1.save(self._make_state(
            channel="telegram", channel_session_id="222",
            known_slots={"city": "Yaoundé"},
        ))
        conn1.close()

        conn2 = self._connect()
        repo2 = ConversationStateRepository(conn2)
        s1 = repo2.load("whatsapp", "+237aaa")
        s2 = repo2.load("telegram", "222")
        conn2.close()

        self.assertEqual(s1.known_slots["city"], "Douala")
        self.assertEqual(s2.known_slots["city"], "Yaoundé")

    # ── Load non-existent ─────────────────────────────────────────────────

    def test_load_nonexistent_returns_none(self):
        conn = self._connect()
        repo = ConversationStateRepository(conn)
        loaded = repo.load("whatsapp", "+237nonexistent")
        conn.close()
        self.assertIsNone(loaded)

    # ── Actor ID preserved ────────────────────────────────────────────────

    def test_actor_id_preserved(self):
        conn1 = self._connect()
        repo1 = ConversationStateRepository(conn1)
        original = self._make_state(actor_id="actor_persist_001")
        repo1.save(original)
        conn1.close()

        conn2 = self._connect()
        repo2 = ConversationStateRepository(conn2)
        loaded = repo2.load("whatsapp", "+237600000001")
        conn2.close()

        self.assertEqual(loaded.actor_id, "actor_persist_001")


if __name__ == "__main__":
    unittest.main()
