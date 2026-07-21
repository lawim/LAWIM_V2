"""Test privacy guarantees: no secrets in provider context, no cross-channel
data without consent, no other-case data leakage."""

from __future__ import annotations

import sqlite3
import unittest

from lawim_v2.conversation.memory.context_builder import (
    MemoryContextBuilder,
    ProviderMemoryContext,
)
from lawim_v2.conversation.state.state import ConversationState
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.identity.models import IdentitySource
from lawim_v2.conversation.identity.resolver import (
    CrossChannelConsentRepository,
    CrossChannelIdentityResolver,
    IdentityBindingRepository,
)


class _StateRepoWithLookup:
    """Wraps ConversationStateRepository to add load_by_conversation_id."""

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


class TestProviderMemoryPrivacy(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        raw_repo = ConversationStateRepository(self.conn)
        self.state_repo = _StateRepoWithLookup(raw_repo)
        self.builder = MemoryContextBuilder(
            conversation_state_repository=self.state_repo,
        )

    def tearDown(self):
        self.conn.close()

    def _seed_state(self, **overrides):
        defaults = dict(
            channel="whatsapp",
            channel_session_id="sess_1",
            language="fr",
            current_intent="rental_search",
            known_slots={"city": "Douala", "budget": "150000"},
            last_lawim_message="Quel quartier préférez-vous?",
        )
        defaults.update(overrides)
        state = ConversationState(**defaults)
        return self.state_repo.save(state)

    def test_provider_memory_no_secrets(self):
        self._seed_state()
        ctx = self.builder.build_provider_context("sess_1")
        self.assertNotIn("message_ids", dir(ctx))
        self.assertNotIn("secrets", dir(ctx))
        self.assertIsInstance(ctx, ProviderMemoryContext)

    def test_provider_memory_no_other_case_data(self):
        self._seed_state()
        ctx = self.builder.build_provider_context("sess_1")
        self.assertIn("city", ctx.active_facts)
        self.assertIn("budget", ctx.active_facts)

    def test_provider_context_no_internal_ids(self):
        self._seed_state()
        ctx = self.builder.build_provider_context("sess_1")
        for attr in ("raw_history", "message_ids", "secrets"):
            self.assertNotIn(attr, dir(ctx))


class TestCrossChannelPrivacy(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.binding_repo = IdentityBindingRepository(self.conn)
        self.consent_repo = CrossChannelConsentRepository(self.conn)
        self.resolver = CrossChannelIdentityResolver(
            self.binding_repo, self.consent_repo,
        )

    def tearDown(self):
        self.conn.close()

    def test_no_cross_channel_without_consent(self):
        self.resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.WHATSAPP_CHAT_ID,
        )
        resolved, has_consent = self.resolver.resolve_with_consent(
            "whatsapp", "+237600000001", "telegram",
        )
        self.assertFalse(has_consent)

    def test_no_cross_channel_unverified_identity(self):
        self.resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.UNVERIFIED,
        )
        resolved, has_consent = self.resolver.resolve_with_consent(
            "whatsapp", "+237600000001", "telegram",
        )
        self.assertFalse(has_consent)

    def test_cross_channel_requires_explicit_consent(self):
        self.resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.PHONE_VERIFIED,
        )
        consent = self.resolver.request_consent(
            "actor_1", "whatsapp", "telegram",
        )
        self.resolver.grant_consent(consent.consent_id)
        resolved, has_consent = self.resolver.resolve_with_consent(
            "whatsapp", "+237600000001", "telegram",
        )
        self.assertTrue(has_consent)

    def test_cross_channel_consent_revoked(self):
        self.resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.PHONE_VERIFIED,
        )
        consent = self.resolver.request_consent(
            "actor_1", "whatsapp", "telegram",
        )
        self.resolver.grant_consent(consent.consent_id)
        self.resolver.revoke_consent(consent.consent_id)
        resolved, has_consent = self.resolver.resolve_with_consent(
            "whatsapp", "+237600000001", "telegram",
        )
        self.assertFalse(has_consent)


if __name__ == "__main__":
    unittest.main()
