"""Test cross-channel identity resolution and continuity with consent."""

from __future__ import annotations

import sqlite3
import unittest
from datetime import datetime, timedelta, timezone

from lawim_v2.conversation.identity.models import (
    CrossChannelConsent,
    IdentityBinding,
    IdentityConfidence,
    IdentitySource,
    ResolvedIdentity,
)
from lawim_v2.conversation.identity.resolver import (
    CrossChannelConsentRepository,
    CrossChannelIdentityResolver,
    IdentityBindingRepository,
    _new_id,
    _utcnow,
)


def _make_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    return conn


class TestCrossChannelConversationContinuity(unittest.TestCase):
    def setUp(self):
        self.conn = _make_db()
        self.binding_repo = IdentityBindingRepository(self.conn)
        self.consent_repo = CrossChannelConsentRepository(self.conn)
        self.resolver = CrossChannelIdentityResolver(
            self.binding_repo, self.consent_repo,
        )

    def tearDown(self):
        self.conn.close()

    def test_identity_binding_create(self):
        binding = self.resolver.bind_identity(
            actor_id="actor_1",
            channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.WHATSAPP_CHAT_ID,
        )
        self.assertEqual(binding.actor_id, "actor_1")
        self.assertEqual(binding.channel, "whatsapp")
        self.assertEqual(binding.confidence, IdentityConfidence.UNVERIFIED)

    def test_identity_binding_resolve(self):
        self.resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.WHATSAPP_CHAT_ID,
        )
        resolved = self.resolver.resolve("whatsapp", "+237600000001")
        self.assertEqual(resolved.actor_id, "actor_1")
        self.assertGreater(len(resolved.channels), 0)

    def test_identity_resolve_verified(self):
        self.resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.PHONE_VERIFIED,
        )
        resolved = self.resolver.resolve("whatsapp", "+237600000001")
        self.assertEqual(resolved.confidence, IdentityConfidence.VERIFIED)
        self.assertTrue(resolved.can_auto_merge())

    def test_identity_resolve_unverified(self):
        self.resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.WHATSAPP_CHAT_ID,
        )
        resolved = self.resolver.resolve("whatsapp", "+237600000001")
        self.assertEqual(resolved.confidence, IdentityConfidence.UNVERIFIED)
        self.assertFalse(resolved.can_auto_merge())

    def test_identity_conflict_detection(self):
        self.resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.PHONE_VERIFIED,
        )
        self.resolver.bind_identity(
            actor_id="actor_1", channel="telegram",
            channel_identifier="12345",
            source=IdentitySource.PHONE_VERIFIED,
        )
        resolved = self.resolver.resolve("whatsapp", "+237600000001")
        self.assertEqual(resolved.confidence, IdentityConfidence.CONFLICT)

    def test_identity_different_channels_same_actor(self):
        self.resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.PHONE_VERIFIED,
        )
        self.resolver.bind_identity(
            actor_id="actor_1", channel="telegram",
            channel_identifier="12345",
            source=IdentitySource.WHATSAPP_CHAT_ID,
        )
        resolved = self.resolver.resolve("whatsapp", "+237600000001")
        self.assertIn("telegram", resolved.channels)
        self.assertIn("whatsapp", resolved.channels)

    def test_cross_channel_consent_grant(self):
        consent = self.resolver.request_consent(
            actor_id="actor_1",
            source_channel="whatsapp",
            target_channel="telegram",
        )
        self.assertEqual(consent.status, "PENDING")
        granted = self.resolver.grant_consent(consent.consent_id)
        self.assertEqual(granted.status, "GRANTED")

    def test_cross_channel_consent_revoke(self):
        consent = self.resolver.request_consent(
            actor_id="actor_1",
            source_channel="whatsapp",
            target_channel="telegram",
        )
        self.resolver.grant_consent(consent.consent_id)
        self.resolver.revoke_consent(consent.consent_id)
        reloaded = self.consent_repo.load_consent(consent.consent_id)
        self.assertEqual(reloaded.status, "REVOKED")

    def test_cross_channel_consent_expired(self):
        now = datetime.now(timezone.utc)
        expired_at = (now - timedelta(hours=1)).isoformat()
        consent = CrossChannelConsent(
            consent_id=_new_id(),
            actor_id="actor_1",
            source_channel="whatsapp",
            target_channel="telegram",
            status="GRANTED",
            granted_at=(now - timedelta(days=1)).isoformat(),
            expires_at=expired_at,
            created_at=(now - timedelta(days=1)).isoformat(),
        )
        self.consent_repo.save_consent(consent)
        self.assertFalse(consent.is_active())

    def test_cross_channel_consent_required_for_unverified(self):
        self.resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.WHATSAPP_CHAT_ID,
        )
        resolved, has_consent = self.resolver.resolve_with_consent(
            "whatsapp", "+237600000001", "telegram",
        )
        self.assertFalse(has_consent)

    def test_resume_with_consent(self):
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

    def test_resume_without_consent(self):
        self.resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.PHONE_VERIFIED,
        )
        resolved, has_consent = self.resolver.resolve_with_consent(
            "whatsapp", "+237600000001", "telegram",
        )
        self.assertFalse(has_consent)

    def test_simulate_whatsapp_to_telegram(self):
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
        self.assertEqual(resolved.actor_id, "actor_1")


class TestIdentityResolution(unittest.TestCase):
    def test_unknown_identity(self):
        conn = _make_db()
        binding_repo = IdentityBindingRepository(conn)
        consent_repo = CrossChannelConsentRepository(conn)
        resolver = CrossChannelIdentityResolver(binding_repo, consent_repo)
        resolved = resolver.resolve("telegram", "99999")
        self.assertEqual(resolved.actor_id, "")
        self.assertEqual(resolved.confidence, IdentityConfidence.UNVERIFIED)
        conn.close()

    def test_get_known_channels(self):
        conn = _make_db()
        binding_repo = IdentityBindingRepository(conn)
        consent_repo = CrossChannelConsentRepository(conn)
        resolver = CrossChannelIdentityResolver(binding_repo, consent_repo)
        resolver.bind_identity(
            actor_id="actor_1", channel="whatsapp",
            channel_identifier="+237600000001",
            source=IdentitySource.PHONE_VERIFIED,
        )
        channels = resolver.get_known_channels("actor_1")
        self.assertEqual(len(channels), 1)
        self.assertEqual(channels[0]["channel"], "whatsapp")
        conn.close()


if __name__ == "__main__":
    unittest.main()
