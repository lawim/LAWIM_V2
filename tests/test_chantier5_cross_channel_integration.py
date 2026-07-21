"""Chantier 5: Cross-channel integration tests.

Simulates identity resolution, consent, and conversation continuity
across WhatsApp, Telegram and Web channels.
"""

from __future__ import annotations

import sqlite3
import unittest
from datetime import datetime, timedelta, timezone

from lawim_v2.conversation.identity.models import (
    CrossChannelConsent,
    IdentityConfidence,
    IdentitySource,
)
from lawim_v2.conversation.identity.resolver import (
    CrossChannelConsentRepository,
    CrossChannelIdentityResolver,
    IdentityBindingRepository,
    _new_id,
    _utcnow,
)
from lawim_v2.conversation.state.engine import ConversationStateEngine
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.resolver import ConversationResolver


def _make_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    return conn


class TestChantier5CrossChannelIntegration(unittest.TestCase):
    """Cross-channel identity resolution and conversation continuity."""

    def setUp(self):
        self.conn = _make_db()
        self.binding_repo = IdentityBindingRepository(self.conn)
        self.consent_repo = CrossChannelConsentRepository(self.conn)
        self.resolver = CrossChannelIdentityResolver(
            self.binding_repo, self.consent_repo,
        )
        self.state_conn = _make_db()
        self.state_repo = ConversationStateRepository(self.state_conn)
        self.state_resolver = ConversationResolver()

    def tearDown(self):
        self.conn.close()
        self.state_conn.close()

    # ── Identity binding ──────────────────────────────────────────────────

    def test_whatsapp_identity_binding(self):
        binding = self.resolver.bind_identity(
            actor_id="actor_wa",
            channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.WHATSAPP_CHAT_ID,
        )
        self.assertEqual(binding.actor_id, "actor_wa")
        self.assertEqual(binding.channel, "whatsapp")
        self.assertEqual(binding.confidence, IdentityConfidence.UNVERIFIED)

    def test_telegram_identity_binding(self):
        binding = self.resolver.bind_identity(
            actor_id="actor_tg",
            channel="telegram",
            channel_identifier="123456789",
            source=IdentitySource.TELEGRAM_USER_ID,
        )
        self.assertEqual(binding.actor_id, "actor_tg")
        self.assertEqual(binding.channel, "telegram")
        self.assertEqual(binding.confidence, IdentityConfidence.UNVERIFIED)

    def test_web_identity_binding(self):
        binding = self.resolver.bind_identity(
            actor_id="actor_web",
            channel="web",
            channel_identifier="anon_session_abc",
            source=IdentitySource.WEB_SESSION,
        )
        self.assertEqual(binding.actor_id, "actor_web")
        self.assertEqual(binding.channel, "web")
        self.assertEqual(binding.confidence, IdentityConfidence.UNVERIFIED)

    # ── Cross-channel resolution ──────────────────────────────────────────

    def test_simulate_whatsapp_to_telegram(self):
        """Bind WhatsApp to actor, grant consent, resolve for Telegram."""
        self.resolver.bind_identity(
            actor_id="actor_multi",
            channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.PHONE_VERIFIED,
        )
        consent = self.resolver.request_consent(
            "actor_multi", "whatsapp", "telegram",
        )
        self.resolver.grant_consent(consent.consent_id)

        resolved, has_consent = self.resolver.resolve_with_consent(
            "whatsapp", "+237600000001", "telegram",
        )
        self.assertTrue(has_consent)
        self.assertEqual(resolved.actor_id, "actor_multi")
        self.assertIn("whatsapp", resolved.channels)

    def test_web_to_whatsapp_continuity(self):
        """Web session resolves to same actor as WhatsApp."""
        self.resolver.bind_identity(
            actor_id="actor_web2wa",
            channel="web",
            channel_identifier="web_sess_001",
            source=IdentitySource.EMAIL_VERIFIED,
        )
        self.resolver.bind_identity(
            actor_id="actor_web2wa",
            channel="whatsapp",
            channel_identifier="+237600000002",
            source=IdentitySource.PHONE_VERIFIED,
        )
        consent = self.resolver.request_consent(
            "actor_web2wa", "web", "whatsapp",
        )
        self.resolver.grant_consent(consent.consent_id)

        resolved_web = self.resolver.resolve("web", "web_sess_001")
        self.assertEqual(resolved_web.actor_id, "actor_web2wa")
        self.assertIn("whatsapp", resolved_web.channels)

    def test_unknown_channel_returns_empty(self):
        resolved = self.resolver.resolve("whatsapp", "+237999999999")
        self.assertEqual(resolved.actor_id, "")
        self.assertEqual(resolved.confidence, IdentityConfidence.UNVERIFIED)
        self.assertFalse(resolved.can_auto_merge())

    # ── Consent lifecycle ─────────────────────────────────────────────────

    def test_consent_full_lifecycle(self):
        consent = self.resolver.request_consent(
            actor_id="actor_cl",
            source_channel="whatsapp",
            target_channel="telegram",
        )
        self.assertEqual(consent.status, "PENDING")
        self.assertIsNone(consent.granted_at)

        granted = self.resolver.grant_consent(consent.consent_id)
        self.assertEqual(granted.status, "GRANTED")
        self.assertIsNotNone(granted.granted_at)
        self.assertTrue(granted.is_active())

        self.resolver.revoke_consent(consent.consent_id)
        reloaded = self.consent_repo.load_consent(consent.consent_id)
        self.assertEqual(reloaded.status, "REVOKED")
        self.assertFalse(reloaded.is_active())

    def test_consent_expires(self):
        now = datetime.now(timezone.utc)
        expired_at = (now - timedelta(hours=1)).isoformat()
        consent = CrossChannelConsent(
            consent_id=_new_id(),
            actor_id="actor_exp",
            source_channel="whatsapp",
            target_channel="telegram",
            status="GRANTED",
            granted_at=(now - timedelta(days=1)).isoformat(),
            expires_at=expired_at,
            created_at=(now - timedelta(days=1)).isoformat(),
        )
        self.consent_repo.save_consent(consent)
        self.assertFalse(consent.is_active())

    def test_consent_required_for_unverified(self):
        self.resolver.bind_identity(
            actor_id="actor_unv",
            channel="whatsapp",
            channel_identifier="+237600000003",
            source=IdentitySource.WHATSAPP_CHAT_ID,
        )
        resolved, has_consent = self.resolver.resolve_with_consent(
            "whatsapp", "+237600000003", "telegram",
        )
        self.assertFalse(has_consent)
        self.assertEqual(resolved.confidence, IdentityConfidence.UNVERIFIED)

    def test_resume_with_consent(self):
        self.resolver.bind_identity(
            actor_id="actor_rs",
            channel="whatsapp",
            channel_identifier="+237600000004",
            source=IdentitySource.PHONE_VERIFIED,
        )
        consent = self.resolver.request_consent(
            "actor_rs", "whatsapp", "telegram",
        )
        self.resolver.grant_consent(consent.consent_id)
        resolved, has_consent = self.resolver.resolve_with_consent(
            "whatsapp", "+237600000004", "telegram",
        )
        self.assertTrue(has_consent)
        self.assertEqual(resolved.actor_id, "actor_rs")

    def test_resume_without_consent(self):
        self.resolver.bind_identity(
            actor_id="actor_rs2",
            channel="whatsapp",
            channel_identifier="+237600000005",
            source=IdentitySource.PHONE_VERIFIED,
        )
        resolved, has_consent = self.resolver.resolve_with_consent(
            "whatsapp", "+237600000005", "telegram",
        )
        self.assertFalse(has_consent)

    # ── Conflict detection ────────────────────────────────────────────────

    def test_conflict_detection(self):
        self.resolver.bind_identity(
            actor_id="actor_conflict",
            channel="whatsapp",
            channel_identifier="+237600000006",
            source=IdentitySource.PHONE_VERIFIED,
        )
        self.resolver.bind_identity(
            actor_id="actor_conflict",
            channel="telegram",
            channel_identifier="555111",
            source=IdentitySource.PHONE_VERIFIED,
        )
        resolved = self.resolver.resolve("whatsapp", "+237600000006")
        self.assertEqual(resolved.confidence, IdentityConfidence.CONFLICT)

    # ── Known channels retrieval ──────────────────────────────────────────

    def test_get_known_channels(self):
        self.resolver.bind_identity(
            actor_id="actor_kc",
            channel="whatsapp",
            channel_identifier="+237600000007",
            source=IdentitySource.PHONE_VERIFIED,
        )
        self.resolver.bind_identity(
            actor_id="actor_kc",
            channel="telegram",
            channel_identifier="555222",
            source=IdentitySource.TELEGRAM_USER_ID,
        )
        channels = self.resolver.get_known_channels("actor_kc")
        channel_names = {c["channel"] for c in channels}
        self.assertIn("whatsapp", channel_names)
        self.assertIn("telegram", channel_names)

    # ── Negative edge cases ───────────────────────────────────────────────

    def test_empty_actor_returns_no_channels(self):
        channels = self.resolver.get_known_channels("")
        self.assertEqual(len(channels), 0)

    def test_bind_same_channel_twice_updates(self):
        b1 = self.resolver.bind_identity(
            actor_id="actor_upd",
            channel="whatsapp",
            channel_identifier="+237600000008",
            source=IdentitySource.WHATSAPP_CHAT_ID,
        )
        b2 = self.resolver.bind_identity(
            actor_id="actor_upd",
            channel="whatsapp",
            channel_identifier="+237600000008",
            source=IdentitySource.PHONE_VERIFIED,
        )
        self.assertEqual(b2.binding_id, b1.binding_id)
        self.assertEqual(b2.confidence, IdentityConfidence.VERIFIED)

    def test_grant_nonexistent_consent_raises(self):
        with self.assertRaises(ValueError):
            self.resolver.grant_consent("nonexistent_id")


if __name__ == "__main__":
    unittest.main()
