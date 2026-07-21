"""Test concurrent updates, version conflict detection, and integrity."""

from __future__ import annotations

import sqlite3
import unittest

from lawim_v2.conversation.state.state import ConversationState
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.errors import StateConflictError
from lawim_v2.conversation.case.repository import LawimCaseRepository
from lawim_v2.conversation.domain.case import LawimCase


class TestConcurrentUpdates(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.state_repo = ConversationStateRepository(self.conn)
        self.case_repo = LawimCaseRepository(self.conn)

    def tearDown(self):
        self.conn.close()

    def _create_state(self) -> ConversationState:
        state = ConversationState(
            channel="whatsapp",
            channel_session_id="sess_concurrent",
            language="fr",
            current_intent="rental_search",
            known_slots={"city": "Douala"},
            missing_slots=["budget"],
            qualification_status="in_progress",
        )
        return self.state_repo.save(state)

    def test_simulate_concurrent_updates(self):
        self._create_state()

        reader_a = self.state_repo.load("whatsapp", "sess_concurrent")
        reader_b = self.state_repo.load("whatsapp", "sess_concurrent")

        reader_a.known_slots["budget"] = "150000"
        reader_a.missing_slots = ["bedrooms"]
        self.state_repo.update(reader_a)

        reader_b.known_slots["city"] = "Yaoundé"
        with self.assertRaises(StateConflictError):
            self.state_repo.update(reader_b)

    def test_simulate_concurrent_updates_with_refresh(self):
        self._create_state()

        reader_a = self.state_repo.load("whatsapp", "sess_concurrent")
        reader_a.known_slots["budget"] = "150000"
        reader_a.missing_slots = ["bedrooms"]
        self.state_repo.update(reader_a)

        reader_b = self.state_repo.load("whatsapp", "sess_concurrent")
        reader_b.known_slots["city"] = "Yaoundé"
        self.state_repo.update(reader_b)

        final = self.state_repo.load("whatsapp", "sess_concurrent")
        self.assertEqual(final.known_slots.get("city"), "Yaoundé")
        self.assertEqual(final.known_slots.get("budget"), "150000")
        self.assertIn("bedrooms", final.missing_slots)

    def test_version_conflict_detection(self):
        case = LawimCase(
            case_id="case_v1",
            case_type="RENT",
            primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        case = self.case_repo.save(case)
        version_before = case.version

        case.title = "Update A"
        self.case_repo.save(case)
        version_after_a = case.version
        self.assertGreater(version_after_a, version_before)

        case.title = "Update B"
        self.case_repo.save(case)
        version_after_b = case.version
        self.assertGreater(version_after_b, version_after_a)

    def test_no_double_response_on_conflict(self):
        self._create_state()

        s1 = self.state_repo.load("whatsapp", "sess_concurrent")
        s1.last_lawim_message = "Response 1"
        self.state_repo.update(s1)

        s2 = self.state_repo.load("whatsapp", "sess_concurrent")
        s2.last_lawim_message = "Response 2"
        s2.known_slots["budget"] = "200000"
        self.state_repo.update(s2)

        final = self.state_repo.load("whatsapp", "sess_concurrent")
        self.assertEqual(final.last_lawim_message, "Response 2")

    def test_concurrent_slot_updates_with_refresh(self):
        self._create_state()

        writer_1 = self.state_repo.load("whatsapp", "sess_concurrent")
        writer_1.known_slots["budget"] = "100000"
        writer_1.known_slots["bedrooms"] = "2"
        self.state_repo.update(writer_1)

        writer_2 = self.state_repo.load("whatsapp", "sess_concurrent")
        writer_2.known_slots["furnished"] = "yes"
        writer_2.known_slots["city"] = "Yaoundé"
        self.state_repo.update(writer_2)

        final = self.state_repo.load("whatsapp", "sess_concurrent")
        self.assertIn("budget", final.known_slots)
        self.assertIn("bedrooms", final.known_slots)
        self.assertIn("furnished", final.known_slots)
        self.assertEqual(final.known_slots["city"], "Yaoundé")

    def test_state_version_increments_on_update(self):
        self._create_state()
        v1 = self.state_repo.load("whatsapp", "sess_concurrent").state_version

        loaded = self.state_repo.load("whatsapp", "sess_concurrent")
        loaded.current_intent = "new_intent"
        self.state_repo.update(loaded)

        v2 = self.state_repo.load("whatsapp", "sess_concurrent").state_version
        self.assertGreater(v2, v1)

    def test_case_version_increments_on_save(self):
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        repo = LawimCaseRepository(conn)

        case = LawimCase(
            case_id="case_ver", case_type="RENT",
            primary_actor_id="actor_1",
        )
        saved = repo.save(case)
        v1 = saved.version

        saved.title = "Updated"
        saved2 = repo.save(saved)
        v2 = saved2.version
        self.assertGreater(v2, v1)

        saved2.title = "Updated again"
        saved3 = repo.save(saved2)
        v3 = saved3.version
        self.assertGreater(v3, v2)

        conn.close()


if __name__ == "__main__":
    unittest.main()
