"""Test MemoryContextBuilder with real repository and state data."""

from __future__ import annotations

import sqlite3
import unittest

from lawim_v2.conversation.memory.context_builder import (
    BusinessMemoryContext,
    HumanHandoverContext,
    MemoryContextBuilder,
    ProviderMemoryContext,
)
from lawim_v2.conversation.state.state import ConversationState
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.case.repository import LawimCaseRepository
from lawim_v2.conversation.case.service import LawimCaseService


class _StateRepoWithLookup:
    """Wraps ConversationStateRepository to add load_by_conversation_id
    via a simple in-memory index."""

    def __init__(self, repo):
        self._repo = repo
        self._lookup: dict[str, tuple[str, str]] = {}

    def load(self, channel, channel_session_id):
        return self._repo.load(channel, channel_session_id)

    def save(self, state):
        result = self._repo.save(state)
        key = state.channel_session_id or state.channel
        self._lookup[key] = (state.channel, state.channel_session_id)
        return result

    def load_by_conversation_id(self, conversation_id: str):
        pair = self._lookup.get(conversation_id)
        if not pair:
            return None
        return self._repo.load(pair[0], pair[1])


class TestMemoryContextBuilder(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        raw_repo = ConversationStateRepository(self.conn)
        self.state_repo = _StateRepoWithLookup(raw_repo)
        self.case_repo = LawimCaseRepository(self.conn)
        self.case_service = LawimCaseService(self.case_repo)
        self.builder = MemoryContextBuilder(
            lawim_case_service=self.case_service,
            conversation_state_repository=self.state_repo,
        )

    def tearDown(self):
        self.conn.close()

    def _seed_state(self, **overrides) -> ConversationState:
        defaults = dict(
            channel="whatsapp",
            channel_session_id="sess_1",
            language="fr",
            current_intent="rental_search",
            known_slots={"city": "Douala", "budget": "150000"},
            missing_slots=["bedrooms"],
            qualification_status="in_progress",
        )
        defaults.update(overrides)
        state = ConversationState(**defaults)
        return self.state_repo.save(state)

    def test_business_context_basic(self):
        self._seed_state()
        ctx = self.builder.build_business_context("sess_1")
        self.assertIsInstance(ctx, BusinessMemoryContext)
        self.assertEqual(ctx.intent, "rental_search")
        self.assertEqual(ctx.active_slots.get("city"), "Douala")
        self.assertEqual(ctx.active_slots.get("budget"), "150000")
        self.assertIn("bedrooms", ctx.missing_slots)
        self.assertEqual(ctx.language, "fr")

    def test_business_context_with_case(self):
        self._seed_state()
        case = self.case_service.create_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        ctx = self.builder.build_business_context("sess_1", case_id=case.case_id)
        self.assertIsNotNone(ctx.case)
        self.assertEqual(ctx.case.case_id, case.case_id)

    def test_provider_context_limited(self):
        self._seed_state(
            known_slots={"city": "Douala", "budget": "150000", "bedrooms": "2"},
        )
        ctx = self.builder.build_provider_context("sess_1", max_chars=100)
        self.assertIsInstance(ctx, ProviderMemoryContext)
        self.assertEqual(ctx.intent, "rental_search")
        self.assertEqual(ctx.active_facts.get("city"), "Douala")

    def test_provider_context_no_secrets(self):
        self._seed_state()
        ctx = self.builder.build_provider_context("sess_1")
        self.assertNotIn("raw_history", dir(ctx))
        self.assertNotIn("message_ids", dir(ctx))
        self.assertNotIn("conversation_state", dir(ctx))

    def test_provider_context_no_inactive_slots(self):
        self._seed_state(known_slots={"city": "Douala"})
        ctx = self.builder.build_provider_context("sess_1")
        self.assertIn("city", ctx.active_facts)

    def test_handover_context(self):
        case = self.case_service.create_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
            title="Test case",
        )
        case.known_slots["city"] = "Douala"
        case.last_question_key = "budget"
        self.case_service.update_case(case)

        ctx = self.builder.build_handover_context(case.case_id)
        self.assertIsInstance(ctx, HumanHandoverContext)
        self.assertEqual(ctx.case_code, case.case_code)
        self.assertIn("city", ctx.known_information)
        self.assertEqual(ctx.case_id, case.case_id)

    def test_handover_context_not_found(self):
        ctx = self.builder.build_handover_context("nonexistent")
        self.assertEqual(ctx.handover_reason, "case_not_found")
        self.assertGreater(len(ctx.limitations), 0)

    def test_resume_context(self):
        self._seed_state()
        ctx = self.builder.build_resume_context("actor_1", "sess_1")
        self.assertEqual(ctx["actor_id"], "actor_1")
        self.assertEqual(ctx["intent"], "rental_search")
        self.assertEqual(ctx["known_slots"]["city"], "Douala")
        self.assertIn("resumed_at", ctx)


class TestProviderContextSecrets(unittest.TestCase):
    def test_provider_context_no_secrets_attribute(self):
        ctx = ProviderMemoryContext()
        for attr in ("secrets", "raw_history", "message_ids", "internal_ids"):
            self.assertNotIn(attr, dir(ctx))


class TestBusinessContextDefaults(unittest.TestCase):
    def test_business_context_defaults(self):
        ctx = BusinessMemoryContext()
        self.assertIsNone(ctx.conversation_state)
        self.assertIsNone(ctx.case)
        self.assertEqual(ctx.active_slots, {})
        self.assertEqual(ctx.missing_slots, [])
        self.assertEqual(ctx.language, "fr")
        self.assertEqual(ctx.readiness, "not_started")


if __name__ == "__main__":
    unittest.main()
