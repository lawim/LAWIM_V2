# Program J — Foundation Bundle Tests
from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from uuid import uuid4

from lawim_v2.program_j import (
    Actor,
    ActorStatus,
    ActorType,
    ChannelEndpoint,
    ChannelEndpointStatus,
    ChannelSession,
    ContentType,
    ConversationParticipant,
    ConversationStatus,
    Direction,
    EndpointVerification,
    ExchangeResult,
    ExchangeType,
    MessageDelivery,
    UnifiedConversation,
    UnifiedMessage,
    VisualRoleRegistry,
    visual_role_registry,
)
from lawim_v2.program_j.channel_normalizer import normalize_webhook_payload
from lawim_v2.program_j.config import ProgramJConfig
from lawim_v2.program_j.services import (
    ActorResolutionService,
    ConversationResolutionService,
    MessageIngestionService,
    ParticipantDisplayService,
)
from lawim_v2.program_j.visual_role import PrivacyLevel, VisualRole

# ── Helpers ────────────────────────────────────────────────────────────────


def _fake_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Exchange Taxonomy Tests ────────────────────────────────────────────────


class ExchangeTaxonomyDirectionTest(unittest.TestCase):
    def test_inbound_value(self):
        self.assertEqual(Direction.INBOUND.value, "INBOUND")

    def test_outbound_value(self):
        self.assertEqual(Direction.OUTBOUND.value, "OUTBOUND")

    def test_internal_value(self):
        self.assertEqual(Direction.INTERNAL.value, "INTERNAL")

    def test_system_value(self):
        self.assertEqual(Direction.SYSTEM.value, "SYSTEM")

    def test_from_communication_inbound(self):
        self.assertEqual(Direction.from_communication_direction("inbound"), Direction.INBOUND)

    def test_from_communication_outbound(self):
        self.assertEqual(Direction.from_communication_direction("outbound"), Direction.OUTBOUND)

    def test_from_communication_unknown(self):
        self.assertEqual(Direction.from_communication_direction("unknown"), Direction.SYSTEM)

    def test_all_values_distinct(self):
        values = [d.value for d in Direction]
        self.assertEqual(len(values), len(set(values)))


class ExchangeTaxonomyContentTypeTest(unittest.TestCase):
    def test_text_value(self):
        self.assertEqual(ContentType.TEXT.value, "TEXT")

    def test_image_value(self):
        self.assertEqual(ContentType.IMAGE.value, "IMAGE")

    def test_from_mime_image(self):
        self.assertEqual(ContentType.from_mime("image/jpeg"), ContentType.IMAGE)

    def test_from_mime_audio(self):
        self.assertEqual(ContentType.from_mime("audio/mpeg"), ContentType.AUDIO)

    def test_from_mime_video(self):
        self.assertEqual(ContentType.from_mime("video/mp4"), ContentType.VIDEO)

    def test_from_mime_document(self):
        self.assertEqual(ContentType.from_mime("application/pdf"), ContentType.DOCUMENT)

    def test_from_mime_empty(self):
        self.assertEqual(ContentType.from_mime(""), ContentType.TEXT)

    def test_all_values_distinct(self):
        values = [c.value for c in ContentType]
        self.assertEqual(len(values), len(set(values)))


class ExchangeTaxonomyExchangeTypeTest(unittest.TestCase):
    def test_property_search_from_intent(self):
        self.assertEqual(ExchangeType.from_intent("BUY"), ExchangeType.PROPERTY_SEARCH)

    def test_qualification_from_intent(self):
        self.assertEqual(ExchangeType.from_intent("QUALIFICATION"), ExchangeType.QUALIFICATION)

    def test_human_handover_from_intent(self):
        self.assertEqual(ExchangeType.from_intent("HANDOVER"), ExchangeType.HUMAN_HANDOVER)

    def test_information_request_default(self):
        self.assertEqual(ExchangeType.from_intent(None), ExchangeType.INFORMATION_REQUEST)

    def test_information_request_unknown(self):
        self.assertEqual(ExchangeType.from_intent("UNKNOWN"), ExchangeType.INFORMATION_REQUEST)


class ExchangeTaxonomyResultTest(unittest.TestCase):
    def test_received_value(self):
        self.assertEqual(ExchangeResult.RECEIVED.value, "RECEIVED")

    def test_duplicate_value(self):
        self.assertEqual(ExchangeResult.DUPLICATE.value, "DUPLICATE")


# ── Actor Model Tests ──────────────────────────────────────────────────────


class ActorModelTest(unittest.TestCase):
    def test_create_minimal(self):
        actor = Actor(actor_id="a1", actor_type=ActorType.USER, display_name="Test")
        self.assertEqual(actor.actor_id, "a1")
        self.assertEqual(actor.actor_type, ActorType.USER)
        self.assertEqual(actor.status, ActorStatus.ACTIVE)

    def test_ai_assistant_type(self):
        actor = Actor(actor_id="ai", actor_type=ActorType.AI_ASSISTANT, display_name="LAWIM AI")
        self.assertEqual(actor.actor_type, ActorType.AI_ASSISTANT)

    def test_lawim_staff_type(self):
        actor = Actor(actor_id="staff", actor_type=ActorType.LAWIM_STAFF, display_name="Abel")
        self.assertEqual(actor.actor_type, ActorType.LAWIM_STAFF)

    def test_real_estate_agent_type(self):
        actor = Actor(actor_id="agent", actor_type=ActorType.REAL_ESTATE_AGENT, display_name="Jean")
        self.assertEqual(actor.actor_type, ActorType.REAL_ESTATE_AGENT)

    def test_agency_type(self):
        actor = Actor(actor_id="agency", actor_type=ActorType.AGENCY, display_name="Agence Centrale")
        self.assertEqual(actor.actor_type, ActorType.AGENCY)

    def test_architect_type(self):
        actor = Actor(actor_id="arch", actor_type=ActorType.ARCHITECT, display_name="Paul")
        self.assertEqual(actor.actor_type, ActorType.ARCHITECT)

    def test_engineer_type(self):
        actor = Actor(actor_id="eng", actor_type=ActorType.ENGINEER, display_name="Marie")
        self.assertEqual(actor.actor_type, ActorType.ENGINEER)

    def test_notary_type(self):
        actor = Actor(actor_id="not", actor_type=ActorType.NOTARY, display_name="David")
        self.assertEqual(actor.actor_type, ActorType.NOTARY)

    def test_investor_type(self):
        actor = Actor(actor_id="inv", actor_type=ActorType.INVESTOR, display_name="Pierre")
        self.assertEqual(actor.actor_type, ActorType.INVESTOR)

    def test_system_type(self):
        actor = Actor(actor_id="sys", actor_type=ActorType.SYSTEM, display_name="System")
        self.assertEqual(actor.actor_type, ActorType.SYSTEM)

    def test_owner_type(self):
        actor = Actor(actor_id="own", actor_type=ActorType.OWNER, display_name="Owner")
        self.assertEqual(actor.actor_type, ActorType.OWNER)

    def test_buyer_type(self):
        actor = Actor(actor_id="buy", actor_type=ActorType.BUYER, display_name="Buyer")
        self.assertEqual(actor.actor_type, ActorType.BUYER)

    def test_tenant_type(self):
        actor = Actor(actor_id="ten", actor_type=ActorType.TENANT, display_name="Tenant")
        self.assertEqual(actor.actor_type, ActorType.TENANT)

    def test_partner_type(self):
        actor = Actor(actor_id="part", actor_type=ActorType.PARTNER, display_name="Partner")
        self.assertEqual(actor.actor_type, ActorType.PARTNER)

    def test_technician_type(self):
        actor = Actor(actor_id="tech", actor_type=ActorType.TECHNICIAN, display_name="Tech")
        self.assertEqual(actor.actor_type, ActorType.TECHNICIAN)

    def test_historical_role(self):
        actor = Actor(actor_id="a1", actor_type=ActorType.USER, display_name="Test",
                       historical_role="buyer", current_role="owner")
        self.assertEqual(actor.historical_role, "buyer")
        self.assertEqual(actor.current_role, "owner")

    def test_trust_and_privacy(self):
        actor = Actor(actor_id="a1", actor_type=ActorType.USER, display_name="Test",
                       trust_level=3, privacy_level=2)
        self.assertEqual(actor.trust_level, 3)
        self.assertEqual(actor.privacy_level, 2)

    def test_to_dict(self):
        actor = Actor(actor_id="a1", actor_type=ActorType.USER, display_name="Test User")
        d = actor.to_dict()
        self.assertEqual(d["actor_id"], "a1")
        self.assertEqual(d["actor_type"], "USER")
        self.assertEqual(d["display_name"], "Test User")
        self.assertEqual(d["status"], "ACTIVE")

    def test_from_role_label_agent(self):
        self.assertEqual(ActorType.from_role_label("agent immobilier"), ActorType.REAL_ESTATE_AGENT)

    def test_from_role_label_notary(self):
        self.assertEqual(ActorType.from_role_label("notaire"), ActorType.NOTARY)

    def test_from_role_label_architect(self):
        self.assertEqual(ActorType.from_role_label("architecte"), ActorType.ARCHITECT)

    def test_from_role_label_unknown(self):
        self.assertEqual(ActorType.from_role_label("inconnu"), ActorType.USER)

    def test_archived_status(self):
        actor = Actor(actor_id="a1", actor_type=ActorType.USER, display_name="X",
                       status=ActorStatus.ARCHIVED)
        self.assertEqual(actor.status, ActorStatus.ARCHIVED)

    def test_suspended_status(self):
        actor = Actor(actor_id="a1", actor_type=ActorType.USER, display_name="X",
                       status=ActorStatus.SUSPENDED)
        self.assertEqual(actor.status, ActorStatus.SUSPENDED)


# ── Visual Role Registry Tests ──────────────────────────────────────────────


class VisualRoleRegistryTest(unittest.TestCase):
    def test_registry_not_none(self):
        self.assertIsNotNone(visual_role_registry)

    def test_registry_count(self):
        self.assertGreaterEqual(visual_role_registry.count(), 14)

    def test_get_ai(self):
        role = visual_role_registry.get(ActorType.AI_ASSISTANT)
        self.assertEqual(role.emoji, "\U0001f916")
        self.assertEqual(role.code, "AI")

    def test_get_staff(self):
        role = visual_role_registry.get(ActorType.LAWIM_STAFF)
        self.assertEqual(role.code, "STAFF")
        self.assertIn("LAWIM", role.display_format)

    def test_get_agent(self):
        role = visual_role_registry.get(ActorType.REAL_ESTATE_AGENT)
        self.assertEqual(role.emoji, "\U0001f3e0")
        self.assertIn("Agent", role.label_fr)

    def test_get_agency(self):
        role = visual_role_registry.get(ActorType.AGENCY)
        self.assertEqual(role.code, "AGENCY")

    def test_get_architect(self):
        role = visual_role_registry.get(ActorType.ARCHITECT)
        self.assertEqual(role.emoji, "\U0001f4d0")

    def test_get_engineer(self):
        role = visual_role_registry.get(ActorType.ENGINEER)
        self.assertEqual(role.emoji, "\U0001f477")

    def test_get_notary(self):
        role = visual_role_registry.get(ActorType.NOTARY)
        self.assertEqual(role.emoji, "\u2696\ufe0f")

    def test_get_investor(self):
        role = visual_role_registry.get(ActorType.INVESTOR)
        self.assertEqual(role.emoji, "\U0001f4b0")

    def test_get_user_fallback(self):
        role = visual_role_registry.get(ActorType.USER)
        self.assertEqual(role.code, "USER")

    def test_format_display_with_name(self):
        role = visual_role_registry.get(ActorType.REAL_ESTATE_AGENT)
        result = role.format_display("Jean")
        self.assertIn("Jean", result)
        self.assertIn("\U0001f3e0", result)

    def test_format_display_ai(self):
        role = visual_role_registry.get(ActorType.AI_ASSISTANT)
        result = role.format_display()
        self.assertIn("LAWIM AI", result)

    def test_list_all(self):
        roles = visual_role_registry.list_all()
        self.assertGreaterEqual(len(roles), 14)
        codes = [r.code for r in roles]
        self.assertEqual(len(codes), len(set(codes)))

    def test_to_dict_list(self):
        lst = visual_role_registry.to_dict_list()
        self.assertGreaterEqual(len(lst), 14)
        for entry in lst:
            self.assertIn("actor_type", entry)
            self.assertIn("emoji", entry)
            self.assertIn("label_fr", entry)

    def test_all_have_emoji(self):
        for role in visual_role_registry.list_all():
            self.assertTrue(role.emoji, f"{role.code} missing emoji")

    def test_all_have_label_fr(self):
        for role in visual_role_registry.list_all():
            self.assertTrue(role.label_fr, f"{role.code} missing label_fr")

    def test_all_have_display_format(self):
        for role in visual_role_registry.list_all():
            self.assertTrue(role.display_format, f"{role.code} missing display_format")

    def test_privacy_levels(self):
        for role in visual_role_registry.list_all():
            self.assertIn(role.privacy_level, PrivacyLevel)

    def test_ai_privacy_public(self):
        role = visual_role_registry.get(ActorType.AI_ASSISTANT)
        self.assertEqual(role.privacy_level, PrivacyLevel.PUBLIC)

    def test_system_privacy_internal(self):
        role = visual_role_registry.get(ActorType.SYSTEM)
        self.assertEqual(role.privacy_level, PrivacyLevel.INTERNAL)

    def test_mask_phone_default(self):
        role = visual_role_registry.get(ActorType.USER)
        self.assertTrue(role.mask_phone)


# ── ChannelEndpoint Tests ──────────────────────────────────────────────────


class ChannelEndpointTest(unittest.TestCase):
    def test_create(self):
        ep = ChannelEndpoint(
            endpoint_id="ep1", provider="green_api", channel="whatsapp",
            provider_user_id="237686822667", external_id="whatsapp:237686822667",
        )
        self.assertEqual(ep.provider, "green_api")
        self.assertEqual(ep.channel, "whatsapp")

    def test_verification_default(self):
        ep = ChannelEndpoint(
            endpoint_id="ep1", provider="telegram", channel="telegram",
            provider_user_id="12345", external_id="tg:12345",
        )
        self.assertFalse(ep.verification.verified)

    def test_verification_set(self):
        ep = ChannelEndpoint(
            endpoint_id="ep1", provider="green_api", channel="whatsapp",
            provider_user_id="237686822667", external_id="whatsapp:237686822667",
            verification=EndpointVerification(verified=True, method="otp", trust_level=2),
        )
        self.assertTrue(ep.verification.verified)
        self.assertEqual(ep.verification.method, "otp")

    def test_consent(self):
        ep = ChannelEndpoint(
            endpoint_id="ep1", provider="green_api", channel="whatsapp",
            provider_user_id="237686822667", external_id="whatsapp:237686822667",
            consent_granted=True, consent_type="whatsapp",
        )
        self.assertTrue(ep.consent_granted)

    def test_to_dict(self):
        ep = ChannelEndpoint(
            endpoint_id="ep1", provider="green_api", channel="whatsapp",
            provider_user_id="237686822667", external_id="whatsapp:237686822667",
        )
        d = ep.to_dict()
        self.assertEqual(d["endpoint_id"], "ep1")
        self.assertEqual(d["channel"], "whatsapp")

    def test_status_pending(self):
        ep = ChannelEndpoint(
            endpoint_id="ep1", provider="green_api", channel="whatsapp",
            provider_user_id="237686822667", external_id="whatsapp:237686822667",
            status=ChannelEndpointStatus.PENDING,
        )
        self.assertEqual(ep.status, ChannelEndpointStatus.PENDING)

    def test_status_blocked(self):
        ep = ChannelEndpoint(
            endpoint_id="ep1", provider="green_api", channel="whatsapp",
            provider_user_id="237686822667", external_id="whatsapp:237686822667",
            status=ChannelEndpointStatus.BLOCKED,
        )
        self.assertEqual(ep.status, ChannelEndpointStatus.BLOCKED)


# ── Unified Conversation Model Tests ────────────────────────────────────────


class UnifiedConversationTest(unittest.TestCase):
    def test_create(self):
        conv = UnifiedConversation(conversation_id="c1", initial_channel="whatsapp")
        self.assertEqual(conv.status, ConversationStatus.ACTIVE)
        self.assertEqual(conv.initial_channel, "whatsapp")

    def test_add_participant(self):
        conv = UnifiedConversation(conversation_id="c1")
        conv.add_participant("actor1", role="primary", is_primary=True)
        self.assertEqual(len(conv.participants), 1)
        self.assertEqual(conv.participants[0].actor_id, "actor1")

    def test_add_channel_session(self):
        conv = UnifiedConversation(conversation_id="c1")
        session = ChannelSession(
            session_id="s1", conversation_id="c1", channel="telegram",
            provider="telegram", user_endpoint_id="ep1",
        )
        conv.add_channel_session(session)
        self.assertEqual(len(conv.channel_sessions), 1)
        self.assertEqual(conv.current_channel, "telegram")

    def test_to_dict(self):
        conv = UnifiedConversation(conversation_id="c1", subject="Test")
        d = conv.to_dict()
        self.assertEqual(d["conversation_id"], "c1")
        self.assertEqual(d["participant_count"], 0)

    def test_closed_status(self):
        conv = UnifiedConversation(conversation_id="c1", status=ConversationStatus.CLOSED)
        self.assertEqual(conv.status, ConversationStatus.CLOSED)

    def test_archived_status(self):
        conv = UnifiedConversation(conversation_id="c1", status=ConversationStatus.ARCHIVED)
        self.assertEqual(conv.status, ConversationStatus.ARCHIVED)

    def test_dossier_link(self):
        conv = UnifiedConversation(conversation_id="c1", dossier_id=42, project_id=7)
        self.assertEqual(conv.dossier_id, 42)
        self.assertEqual(conv.project_id, 7)

    def test_multi_participant(self):
        conv = UnifiedConversation(conversation_id="c1")
        conv.add_participant("actor1", is_primary=True)
        conv.add_participant("actor2")
        self.assertEqual(len(conv.participants), 2)
        self.assertTrue(conv.participants[0].is_primary)
        self.assertFalse(conv.participants[1].is_primary)

    def test_multi_session(self):
        conv = UnifiedConversation(conversation_id="c1")
        conv.add_channel_session(ChannelSession(
            session_id="s1", conversation_id="c1", channel="whatsapp",
            provider="green_api", user_endpoint_id="ep1",
        ))
        conv.add_channel_session(ChannelSession(
            session_id="s2", conversation_id="c1", channel="telegram",
            provider="telegram", user_endpoint_id="ep2",
        ))
        self.assertEqual(len(conv.channel_sessions), 2)
        self.assertEqual(conv.current_channel, "telegram")

    def test_participant_to_dict(self):
        p = ConversationParticipant(conversation_id="c1", actor_id="a1")
        d = p.to_dict()
        self.assertEqual(d["actor_id"], "a1")

    def test_channel_session_to_dict(self):
        s = ChannelSession(
            session_id="s1", conversation_id="c1", channel="whatsapp",
            provider="green_api", user_endpoint_id="ep1",
        )
        d = s.to_dict()
        self.assertEqual(d["channel"], "whatsapp")


# ── Unified Message Model Tests ─────────────────────────────────────────────


class UnifiedMessageTest(unittest.TestCase):
    def test_create_inbound(self):
        msg = UnifiedMessage(
            message_id="m1", conversation_id="c1",
            direction=Direction.INBOUND, content="Bonjour",
        )
        self.assertEqual(msg.direction, Direction.INBOUND)
        self.assertEqual(msg.content, "Bonjour")

    def test_create_outbound(self):
        msg = UnifiedMessage(
            message_id="m2", conversation_id="c1",
            direction=Direction.OUTBOUND, content="Merci",
        )
        self.assertEqual(msg.direction, Direction.OUTBOUND)

    def test_external_message_id(self):
        msg = UnifiedMessage(
            message_id="m1", conversation_id="c1",
            external_message_id="ext_123",
        )
        self.assertEqual(msg.external_message_id, "ext_123")

    def test_exchange_type_default(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1")
        self.assertEqual(msg.exchange_type, ExchangeType.INFORMATION_REQUEST)

    def test_exchange_result_default(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1")
        self.assertEqual(msg.exchange_result, ExchangeResult.RECEIVED)

    def test_to_dict(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1", channel="whatsapp")
        d = msg.to_dict()
        self.assertEqual(d["message_id"], "m1")
        self.assertEqual(d["channel"], "whatsapp")

    def test_with_deliveries(self):
        delivery = MessageDelivery(delivery_id="d1", message_id="m1", provider="green_api")
        msg = UnifiedMessage(message_id="m1", conversation_id="c1", deliveries=[delivery])
        self.assertEqual(len(msg.deliveries), 1)

    def test_delivery_to_dict(self):
        d = MessageDelivery(delivery_id="d1", message_id="m1", provider="green_api", status="sent")
        dd = d.to_dict()
        self.assertEqual(dd["status"], "sent")

    def test_attachments(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1",
                              attachments=[{"type": "image", "url": "https://example.com/img.jpg"}])
        self.assertEqual(len(msg.attachments), 1)
        self.assertEqual(msg.to_dict()["attachment_count"], 1)

    def test_content_type_text(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1", content_type=ContentType.TEXT)
        self.assertEqual(msg.content_type, ContentType.TEXT)

    def test_content_type_image(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1", content_type=ContentType.IMAGE)
        self.assertEqual(msg.content_type, ContentType.IMAGE)

    def test_channel_whatsapp(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1", channel="whatsapp", provider="green_api")
        self.assertEqual(msg.channel, "whatsapp")
        self.assertEqual(msg.provider, "green_api")

    def test_channel_telegram(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1", channel="telegram", provider="telegram")
        self.assertEqual(msg.channel, "telegram")

    def test_channel_web(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1", channel="web", provider="web")
        self.assertEqual(msg.channel, "web")

    def test_with_correlation_id(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1", correlation_id="corr_123")
        self.assertEqual(msg.correlation_id, "corr_123")

    def test_reply_to(self):
        msg = UnifiedMessage(message_id="m2", conversation_id="c1", reply_to_message_id="m1")
        self.assertEqual(msg.reply_to_message_id, "m1")

    def test_status_received(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1", status="received")
        self.assertEqual(msg.status, "received")

    def test_status_sent(self):
        msg = UnifiedMessage(message_id="m1", conversation_id="c1", status="sent")
        self.assertEqual(msg.status, "sent")


# ── Service Tests ──────────────────────────────────────────────────────────


class ActorResolutionServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = ActorResolutionService()

    def test_resolve_by_user_none(self):
        repo = DummyRepo()
        actor = self.svc.resolve_by_user(999, repo)
        self.assertIsNone(actor)

    def test_resolve_by_user_found(self):
        repo = DummyRepo(users={1: {"id": 1, "full_name": "Jean", "email": "jean@ex.com", "role": "agent immobilier"}})
        actor = self.svc.resolve_by_user(1, repo)
        self.assertIsNotNone(actor)
        self.assertEqual(actor.actor_type, ActorType.REAL_ESTATE_AGENT)

    def test_create_minimal(self):
        actor = self.svc.create_minimal(ActorType.USER, "Test")
        self.assertIsNotNone(actor.actor_id)
        self.assertEqual(actor.actor_type, ActorType.USER)

    def test_resolve_by_provider_user_not_found(self):
        repo = DummyRepo()
        actor = self.svc.resolve_by_provider_user("green_api", "whatsapp", "+237600000000", repo)
        self.assertIsNone(actor)


class DummyRepo:
    def __init__(self, users=None):
        self._users = users or {}
        self._contacts = []

    def get_user(self, user_id):
        return self._users.get(user_id)

    def list_crm_contacts(self, limit=1000):
        return self._contacts


class ConversationResolutionServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = ConversationResolutionService()

    def test_create(self):
        conv = self.svc.create("actor1", "whatsapp", "Test conversation")
        self.assertIsNotNone(conv.conversation_id)
        self.assertEqual(conv.initial_channel, "whatsapp")
        self.assertEqual(len(conv.participants), 1)
        self.assertEqual(conv.participants[0].actor_id, "actor1")

    def test_create_telegram(self):
        conv = self.svc.create("actor2", "telegram")
        self.assertEqual(conv.current_channel, "telegram")

    def test_resolve_none(self):
        repo = DummyRepo()
        conv = self.svc.resolve("actor1", "whatsapp", repo)
        self.assertIsNone(conv)

    def test_resolve_or_create_creates(self):
        repo = DummyRepo()
        conv = self.svc.resolve_or_create("actor1", "whatsapp", repo)
        self.assertIsNotNone(conv)


class MessageIngestionServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = MessageIngestionService()

    def test_build_outbound(self):
        msg = self.svc.build_outbound("c1", "Hello", "actor1", "whatsapp")
        self.assertEqual(msg.conversation_id, "c1")
        self.assertEqual(msg.direction, Direction.OUTBOUND)
        self.assertEqual(msg.content, "Hello")

    def test_build_outbound_exchange_type(self):
        msg = self.svc.build_outbound("c1", "Visit?", "actor1", "whatsapp",
                                       ExchangeType.VISIT_REQUEST)
        self.assertEqual(msg.exchange_type, ExchangeType.VISIT_REQUEST)

    def test_normalize_webhook_simple(self):
        msg = self.svc.normalize_webhook("web", "web", {"content": "Hello", "external_message_id": "e1"})
        self.assertEqual(msg.content, "Hello")
        self.assertEqual(msg.direction, Direction.INBOUND)
        self.assertEqual(msg.external_message_id, "e1")


class ParticipantDisplayServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = ParticipantDisplayService()

    def test_format_ai(self):
        actor = Actor(actor_id="ai", actor_type=ActorType.AI_ASSISTANT, display_name="LAWIM AI")
        result = self.svc.format(actor)
        self.assertIn("LAWIM AI", result)
        self.assertIn("\U0001f916", result)

    def test_format_agent(self):
        actor = Actor(actor_id="a1", actor_type=ActorType.REAL_ESTATE_AGENT, display_name="Jean")
        result = self.svc.format(actor)
        self.assertIn("Jean", result)
        self.assertIn("Agent immobilier", result)

    def test_format_staff(self):
        actor = Actor(actor_id="s1", actor_type=ActorType.LAWIM_STAFF, display_name="Abel")
        result = self.svc.format(actor)
        self.assertIn("Abel", result)
        self.assertIn("LAWIM", result)

    def test_format_notary(self):
        actor = Actor(actor_id="n1", actor_type=ActorType.NOTARY, display_name="David")
        result = self.svc.format(actor)
        self.assertIn("David", result)
        self.assertIn("Notaire", result)

    def test_format_investor(self):
        actor = Actor(actor_id="i1", actor_type=ActorType.INVESTOR, display_name="Pierre")
        result = self.svc.format(actor)
        self.assertIn("Pierre", result)
        self.assertIn("Investisseur", result)

    def test_format_agency(self):
        actor = Actor(actor_id="ag1", actor_type=ActorType.AGENCY, display_name="Agence Centrale")
        result = self.svc.format(actor)
        self.assertIn("Agence", result)

    def test_format_safe_masks_phone(self):
        actor = Actor(actor_id="u1", actor_type=ActorType.USER, display_name="+237686822667")
        result = self.svc.format_safe(actor)
        self.assertNotIn("686822667", result)

    def test_format_safe_masked_user(self):
        actor = Actor(actor_id="u1", actor_type=ActorType.USER, display_name="")
        result = self.svc.format_safe(actor)
        self.assertEqual(result, "\U0001f464 Utilisateur")

    def test_format_ai_method(self):
        result = self.svc.format_ai()
        self.assertEqual(result, "\U0001f916 LAWIM AI")

    def test_format_staff_method(self):
        result = self.svc.format_staff("Abel")
        self.assertEqual(result, "\U0001f9d1\U0000200d\U0001f4bc LAWIM (Abel)")


# ── Channel Normalizer Tests ────────────────────────────────────────────────


class ChannelNormalizerTest(unittest.TestCase):
    def test_normalize_generic(self):
        result = normalize_webhook_payload("web", "web", {
            "from": "user1", "message_id": "msg1", "content": "Hello",
        })
        self.assertEqual(result["provider"], "web")
        self.assertEqual(result["external_sender_id"], "user1")
        self.assertEqual(result["external_message_id"], "msg1")
        self.assertEqual(result["content"], "Hello")
        self.assertEqual(result["direction"], "INBOUND")
        self.assertEqual(result["content_type"], "TEXT")

    def test_normalize_generic_outbound(self):
        result = normalize_webhook_payload("web", "web", {
            "from": "system", "direction": "OUTBOUND", "content": "Reply",
        })
        self.assertEqual(result["direction"], "OUTBOUND")

    def test_contract_keys_present(self):
        result = normalize_webhook_payload("web", "web", {"content": "Hi"})
        for key in ("provider", "channel", "external_sender_id", "external_message_id",
                     "direction", "content", "content_type"):
            self.assertIn(key, result, f"Missing key: {key}")

    def test_image_content_type(self):
        result = normalize_webhook_payload("web", "web", {"content": "", "type": "image"})
        self.assertEqual(result["content_type"], "IMAGE")

    def test_location_content_type(self):
        result = normalize_webhook_payload("web", "web", {"content": "", "location": {"lat": 4.0}})
        self.assertEqual(result["content_type"], "LOCATION")


# ── Config / Feature Flag Tests ──────────────────────────────────────────────


class ProgramJConfigTest(unittest.TestCase):
    def test_default_disabled(self):
        config = ProgramJConfig()
        self.assertFalse(config.unified_conversation_enabled)
        self.assertFalse(config.actor_registry_enabled)
        self.assertFalse(config.exchange_taxonomy_enabled)

    def test_enable_unified_conversation(self):
        config = ProgramJConfig(unified_conversation_enabled=True)
        self.assertTrue(config.unified_conversation_enabled)

    def test_enable_actor_registry(self):
        config = ProgramJConfig(actor_registry_enabled=True)
        self.assertTrue(config.actor_registry_enabled)

    def test_enable_exchange_taxonomy(self):
        config = ProgramJConfig(exchange_taxonomy_enabled=True)
        self.assertTrue(config.exchange_taxonomy_enabled)


# ── JSON Serialization Stability ────────────────────────────────────────────


class SerializationTest(unittest.TestCase):
    def test_visual_role_json_stable(self):
        roles = visual_role_registry.to_dict_list()
        s = json.dumps(roles, ensure_ascii=False, sort_keys=True)
        self.assertGreater(len(s), 100)
        parsed = json.loads(s)
        self.assertEqual(len(parsed), len(roles))

    def test_actor_to_dict_stable(self):
        actor = Actor(actor_id="a1", actor_type=ActorType.USER, display_name="Test")
        d = actor.to_dict()
        s = json.dumps(d, ensure_ascii=False, sort_keys=True)
        parsed = json.loads(s)
        self.assertEqual(parsed["actor_id"], "a1")


# ── Run ─────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    unittest.main()
