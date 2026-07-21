"""Test ConversationState persistence with versioning using in-memory SQLite."""

from __future__ import annotations

import json
import sqlite3
import unittest
from datetime import datetime, timezone

from lawim_v2.conversation.state.state import ConversationState
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.errors import StateConflictError


class TestConversationStatePersistence(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.repo = ConversationStateRepository(self.conn)

    def tearDown(self):
        self.conn.close()

    def _make_state(self, **overrides) -> ConversationState:
        defaults = dict(
            channel="whatsapp",
            channel_session_id="+237600000001",
            language="fr",
            current_intent="rental_search",
            known_slots={"city": "Douala", "budget": "150000"},
            missing_slots=["bedrooms"],
            last_question_key="bedrooms",
            qualification_status="in_progress",
        )
        defaults.update(overrides)
        return ConversationState(**defaults)

    def test_create_state(self):
        state = self._make_state()
        saved = self.repo.save(state)
        self.assertIsNotNone(saved)
        self.assertEqual(saved.channel, "whatsapp")
        self.assertEqual(saved.channel_session_id, "+237600000001")

    def test_save_updates_version(self):
        state = self._make_state()
        saved = self.repo.save(state)
        self.assertEqual(saved.state_version, 1)

    def test_load_state(self):
        self.repo.save(self._make_state())
        loaded = self.repo.load("whatsapp", "+237600000001")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.current_intent, "rental_search")
        self.assertEqual(loaded.known_slots.get("city"), "Douala")

    def test_load_state_not_found(self):
        loaded = self.repo.load("whatsapp", "nonexistent")
        self.assertIsNone(loaded)

    def test_update_state(self):
        self.repo.save(self._make_state())
        loaded = self.repo.load("whatsapp", "+237600000001")
        loaded.current_intent = "buy_search"
        loaded.known_slots["city"] = "Yaoundé"
        self.repo.update(loaded)
        reloaded = self.repo.load("whatsapp", "+237600000001")
        self.assertEqual(reloaded.current_intent, "buy_search")
        self.assertEqual(reloaded.known_slots["city"], "Yaoundé")

    def test_persists_language(self):
        self.repo.save(self._make_state(language="en"))
        loaded = self.repo.load("whatsapp", "+237600000001")
        self.assertEqual(loaded.language, "en")

    def test_persists_last_question(self):
        self.repo.save(self._make_state(
            last_question_key="budget",
            last_question_slot="budget_max",
        ))
        loaded = self.repo.load("whatsapp", "+237600000001")
        self.assertEqual(loaded.last_question_key, "budget")
        self.assertEqual(loaded.last_question_slot, "budget_max")

    def test_persists_slots(self):
        state = self._make_state(
            known_slots={"city": "Douala", "budget": "150000", "bedrooms": "2"},
            missing_slots=["furnished"],
        )
        self.repo.save(state)
        loaded = self.repo.load("whatsapp", "+237600000001")
        self.assertEqual(loaded.known_slots["city"], "Douala")
        self.assertEqual(loaded.known_slots["budget"], "150000")
        self.assertIn("furnished", loaded.missing_slots)

    def test_persists_readiness(self):
        self.repo.save(self._make_state(
            qualification_status="ready",
            qualification_step=5,
        ))
        loaded = self.repo.load("whatsapp", "+237600000001")
        self.assertEqual(loaded.qualification_status, "ready")
        self.assertEqual(loaded.qualification_step, 5)

    def test_restart_recovery(self):
        self.repo.save(self._make_state())
        self.conn.close()
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.repo = ConversationStateRepository(self.conn)
        loaded = self.repo.load("whatsapp", "+237600000001")
        self.assertIsNone(loaded)

    def test_restart_recovery_with_file_db(self):
        import tempfile, os
        db_path = tempfile.mktemp(suffix=".db")
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            repo = ConversationStateRepository(conn)
            repo.save(self._make_state())
            conn.close()

            conn2 = sqlite3.connect(db_path)
            conn2.row_factory = sqlite3.Row
            repo2 = ConversationStateRepository(conn2)
            loaded = repo2.load("whatsapp", "+237600000001")
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.current_intent, "rental_search")
            self.assertEqual(loaded.known_slots["city"], "Douala")
            conn2.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)

    def test_optimistic_locking_conflict(self):
        self.repo.save(self._make_state())
        loaded_a = self.repo.load("whatsapp", "+237600000001")

        loaded_b = self.repo.load("whatsapp", "+237600000001")
        loaded_b.known_slots["budget"] = "200000"
        self.repo.update(loaded_b)

        loaded_a.known_slots["city"] = "Yaoundé"
        with self.assertRaises(StateConflictError):
            self.repo.update(loaded_a)

    def test_optimistic_locking_success_with_refresh(self):
        self.repo.save(self._make_state())
        loaded_a = self.repo.load("whatsapp", "+237600000001")

        loaded_b = self.repo.load("whatsapp", "+237600000001")
        loaded_b.known_slots["budget"] = "200000"
        self.repo.update(loaded_b)

        loaded_a = self.repo.load("whatsapp", "+237600000001")
        loaded_a.known_slots["city"] = "Yaoundé"
        self.repo.update(loaded_a)

        final = self.repo.load("whatsapp", "+237600000001")
        self.assertEqual(final.known_slots["city"], "Yaoundé")
        self.assertEqual(final.known_slots["budget"], "200000")

    def test_state_version_increments_on_update(self):
        self.repo.save(self._make_state())
        v1 = self.repo.load("whatsapp", "+237600000001").state_version

        loaded = self.repo.load("whatsapp", "+237600000001")
        loaded.current_intent = "buy_search"
        self.repo.update(loaded)

        v2 = self.repo.load("whatsapp", "+237600000001").state_version
        self.assertGreater(v2, v1)

    def test_case_id_in_state(self):
        self.repo.save(self._make_state(case_id="case_1"))
        loaded = self.repo.load("whatsapp", "+237600000001")
        self.assertEqual(loaded.case_id, "case_1")


if __name__ == "__main__":
    unittest.main()
