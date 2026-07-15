# Program J — Publication Tracking, Attribution and Conversion Tests
from __future__ import annotations

import json
import re
import unittest
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from lawim_v2.program_j.tracking_config import TrackingConfig
from lawim_v2.program_j.tracking_models import (
    AttributionModel,
    AttributionTouchpoint,
    CampaignStatus,
    ConversionEvent,
    ExternalCampaign,
    ExternalChannelCode,
    ExternalPublication,
    LeadAttribution,
    LeadSource,
    PublicationStatus,
    RedirectLog,
    TouchpointType,
    channel_code_from_source,
    generate_tracking_code,
    parse_tracking_code,
)
from lawim_v2.program_j.tracking_services import (
    AttributionEngine,
    ConversionLinkingService,
    TouchpointIngestionService,
    TrackingResolutionService,
)

TRACKING_PATTERN = r"^[A-Z]{2}-LAWIM-\d{6}-\d{4}-\d{2}-\d{3}$"

# ── Helpers ────────────────────────────────────────────────────────────────


def _ts(days_ago: int = 0) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


# ── External Channel Code Tests ────────────────────────────────────────────


class ExternalChannelCodeTest(unittest.TestCase):
    def test_facebook_code(self):
        self.assertEqual(ExternalChannelCode.FACEBOOK.value, "FB")

    def test_whatsapp_code(self):
        self.assertEqual(ExternalChannelCode.WHATSAPP.value, "WA")

    def test_telegram_code(self):
        self.assertEqual(ExternalChannelCode.TELEGRAM.value, "TG")

    def test_all_codes_two_chars(self):
        for code in ExternalChannelCode:
            self.assertEqual(len(code.value), 2)

    def test_all_codes_uppercase(self):
        for code in ExternalChannelCode:
            self.assertTrue(code.value.isupper())

    def test_channel_code_from_source_facebook(self):
        self.assertEqual(channel_code_from_source("facebook"), ExternalChannelCode.FACEBOOK)

    def test_channel_code_from_source_whatsapp(self):
        self.assertEqual(channel_code_from_source("whatsapp"), ExternalChannelCode.WHATSAPP)

    def test_channel_code_from_source_telegram(self):
        self.assertEqual(channel_code_from_source("telegram"), ExternalChannelCode.TELEGRAM)

    def test_channel_code_from_source_unknown(self):
        self.assertEqual(channel_code_from_source("unknown"), ExternalChannelCode.OTHER)

    def test_channel_code_from_source_qr(self):
        self.assertEqual(channel_code_from_source("qr_code"), ExternalChannelCode.QR_CODE)

    def test_unique_channel_codes(self):
        codes = [c.value for c in ExternalChannelCode]
        self.assertEqual(len(codes), len(set(codes)))


# ── Tracking Code Format Tests ─────────────────────────────────────────────


class TrackingCodeFormatTest(unittest.TestCase):
    def test_generate_facebook(self):
        code = generate_tracking_code("FB", 128, 2026, 6, 1)
        self.assertEqual(code, "FB-LAWIM-000128-2026-06-001")

    def test_generate_whatsapp(self):
        code = generate_tracking_code("WA", 14, 2026, 6, 14)
        self.assertEqual(code, "WA-LAWIM-000014-2026-06-014")

    def test_generate_telegram(self):
        code = generate_tracking_code("TG", 45, 2026, 7, 3)
        self.assertEqual(code, "TG-LAWIM-000045-2026-07-003")

    def test_generate_matches_pattern(self):
        code = generate_tracking_code("FB", 1, 2026, 1, 1)
        self.assertTrue(re.match(TRACKING_PATTERN, code))

    def test_generate_auto_date(self):
        code = generate_tracking_code("WA", 100)
        self.assertTrue(re.match(TRACKING_PATTERN, code))

    def test_parse_facebook(self):
        parsed = parse_tracking_code("FB-LAWIM-000128-2026-06-001")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["channel_code"], "FB")
        self.assertEqual(parsed["publication_id"], 128)
        self.assertEqual(parsed["year"], 2026)
        self.assertEqual(parsed["month"], 6)
        self.assertEqual(parsed["sequence"], 1)

    def test_parse_whatsapp(self):
        parsed = parse_tracking_code("WA-LAWIM-000014-2026-06-014")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["channel_code"], "WA")
        self.assertEqual(parsed["publication_id"], 14)
        self.assertEqual(parsed["sequence"], 14)

    def test_parse_invalid_empty(self):
        self.assertIsNone(parse_tracking_code(""))

    def test_parse_invalid_format(self):
        self.assertIsNone(parse_tracking_code("XX-LAWIM-abcdef-2026-06-001"))

    def test_parse_invalid_month(self):
        self.assertIsNone(parse_tracking_code("FB-LAWIM-000001-2026-13-001"))

    def test_parse_invalid_chars(self):
        self.assertIsNone(parse_tracking_code("FB-LAWIM-000001-2026-06-abc"))

    def test_uniqueness_different_channels(self):
        c1 = generate_tracking_code("FB", 1, 2026, 6, 1)
        c2 = generate_tracking_code("WA", 1, 2026, 6, 1)
        self.assertNotEqual(c1, c2)

    def test_uniqueness_different_publications(self):
        c1 = generate_tracking_code("FB", 1, 2026, 6, 1)
        c2 = generate_tracking_code("FB", 2, 2026, 6, 1)
        self.assertNotEqual(c1, c2)

    def test_uniqueness_different_sequences(self):
        c1 = generate_tracking_code("FB", 1, 2026, 6, 1)
        c2 = generate_tracking_code("FB", 1, 2026, 6, 2)
        self.assertNotEqual(c1, c2)

    def test_stable_generation(self):
        c1 = generate_tracking_code("FB", 1, 2026, 6, 1)
        c2 = generate_tracking_code("FB", 1, 2026, 6, 1)
        self.assertEqual(c1, c2)

    def test_json_serializable(self):
        code = generate_tracking_code("FB", 128, 2026, 6, 1)
        s = json.dumps({"code": code})
        self.assertIn("FB-LAWIM-000128-2026-06-001", s)


# ── External Campaign Tests ────────────────────────────────────────────────


class ExternalCampaignTest(unittest.TestCase):
    def test_create_minimal(self):
        c = ExternalCampaign(campaign_id="c1", campaign_name="Test")
        self.assertEqual(c.status, CampaignStatus.DRAFT)

    def test_create_facebook(self):
        c = ExternalCampaign(campaign_id="c1", campaign_name="FB Q3",
                              campaign_type="social", provider="facebook",
                              campaign_owner_actor_id="actor1", status=CampaignStatus.ACTIVE)
        self.assertEqual(c.provider, "facebook")
        self.assertEqual(c.status, CampaignStatus.ACTIVE)

    def test_to_dict(self):
        c = ExternalCampaign(campaign_id="c1", campaign_name="Test")
        d = c.to_dict()
        self.assertEqual(d["campaign_id"], "c1")
        self.assertEqual(d["status"], "DRAFT")

    def test_status_completed(self):
        c = ExternalCampaign(campaign_id="c1", campaign_name="Test", status=CampaignStatus.COMPLETED)
        self.assertEqual(c.status, CampaignStatus.COMPLETED)

    def test_budget(self):
        c = ExternalCampaign(campaign_id="c1", campaign_name="Test", budget=500000, currency="XAF")
        self.assertEqual(c.budget, 500000)

    def test_actor_owner(self):
        c = ExternalCampaign(campaign_id="c1", campaign_name="Test", campaign_owner_actor_id="actor_1")
        self.assertEqual(c.campaign_owner_actor_id, "actor_1")


# ── External Publication Tests ─────────────────────────────────────────────


class ExternalPublicationTest(unittest.TestCase):
    def test_create_minimal(self):
        p = ExternalPublication(publication_id="p1")
        self.assertEqual(p.status, PublicationStatus.DRAFT)

    def test_create_with_tracking_code(self):
        p = ExternalPublication(
            publication_id="p1",
            tracking_code="FB-LAWIM-000001-2026-06-001",
            actor_id="actor1",
            actor_role_at_publication="REAL_ESTATE_AGENT",
            campaign_id="c1",
            channel_code=ExternalChannelCode.FACEBOOK,
        )
        self.assertEqual(p.tracking_code, "FB-LAWIM-000001-2026-06-001")
        self.assertEqual(p.actor_role_at_publication, "REAL_ESTATE_AGENT")

    def test_to_dict(self):
        p = ExternalPublication(publication_id="p1", tracking_code="FB-LAWIM-000001-2026-06-001")
        d = p.to_dict()
        self.assertEqual(d["tracking_code"], "FB-LAWIM-000001-2026-06-001")

    def test_actor_role_preserved(self):
        p = ExternalPublication(publication_id="p1", actor_id="a1",
                                  actor_role_at_publication="AGENT", actor_roles_snapshot=["AGENT", "USER"])
        self.assertEqual(p.actor_role_at_publication, "AGENT")
        self.assertIn("USER", p.actor_roles_snapshot)

    def test_published_status(self):
        p = ExternalPublication(publication_id="p1", status=PublicationStatus.PUBLISHED)
        self.assertEqual(p.status, PublicationStatus.PUBLISHED)

    def test_property_link(self):
        p = ExternalPublication(publication_id="p1", property_id=42)
        self.assertEqual(p.property_id, 42)

    def test_service_link(self):
        p = ExternalPublication(publication_id="p1", service_id=7)
        self.assertEqual(p.service_id, 7)

    def test_language(self):
        p = ExternalPublication(publication_id="p1", language="fr")
        self.assertEqual(p.language, "fr")

    def test_content_reference(self):
        p = ExternalPublication(publication_id="p1", content_reference="https://example.com/prop/123",
                                  content_hash="abc123")
        self.assertEqual(p.content_hash, "abc123")


# ── Redirect Log Tests ─────────────────────────────────────────────────────


class RedirectLogTest(unittest.TestCase):
    def test_create(self):
        r = RedirectLog(redirect_id="r1", tracking_code="FB-LAWIM-000001-2026-06-001",
                         occurred_at=_ts())
        self.assertIsNotNone(r.redirect_id)

    def test_bot_detection(self):
        r = RedirectLog(redirect_id="r1", tracking_code="FB-LAWIM-000001-2026-06-001",
                         is_bot=True, occurred_at=_ts())
        self.assertTrue(r.is_bot)

    def test_duplicate_flag(self):
        r = RedirectLog(redirect_id="r1", tracking_code="FB-LAWIM-000001-2026-06-001",
                         is_duplicate=True, occurred_at=_ts())
        self.assertTrue(r.is_duplicate)

    def test_to_dict(self):
        r = RedirectLog(redirect_id="r1", tracking_code="FB-LAWIM-000001-2026-06-001",
                         occurred_at=_ts(), session_id="sess1")
        d = r.to_dict()
        self.assertEqual(d["session_id"], "sess1")
        self.assertIn("tracking_code", d)

    def test_geo_data(self):
        r = RedirectLog(redirect_id="r1", tracking_code="FB-LAWIM-000001-2026-06-001",
                         country="Cameroon", city="Douala", language="fr",
                         occurred_at=_ts())
        self.assertEqual(r.country, "Cameroon")
        self.assertEqual(r.city, "Douala")


# ── Touchpoint Tests ───────────────────────────────────────────────────────


class AttributionTouchpointTest(unittest.TestCase):
    def test_create_click(self):
        tp = AttributionTouchpoint(
            touchpoint_id="tp1", subject_id="sub1",
            touchpoint_type=TouchpointType.CLICK, channel="FACEBOOK",
            tracking_code="FB-LAWIM-000001-2026-06-001",
        )
        self.assertEqual(tp.touchpoint_type, TouchpointType.CLICK)

    def test_create_conversation(self):
        tp = AttributionTouchpoint(
            touchpoint_id="tp2", subject_id="sub1",
            touchpoint_type=TouchpointType.CONVERSATION_OPEN,
            conversation_id="conv1",
        )
        self.assertEqual(tp.touchpoint_type, TouchpointType.CONVERSATION_OPEN)
        self.assertEqual(tp.conversation_id, "conv1")

    def test_create_payment(self):
        tp = AttributionTouchpoint(
            touchpoint_id="tp3", subject_id="sub1",
            touchpoint_type=TouchpointType.PAYMENT,
            touchpoint_value=500000, currency="XAF",
        )
        self.assertEqual(tp.touchpoint_value, 500000)

    def test_to_dict(self):
        tp = AttributionTouchpoint(
            touchpoint_id="tp1", subject_id="sub1",
            touchpoint_type=TouchpointType.REDIRECT,
        )
        d = tp.to_dict()
        self.assertEqual(d["touchpoint_type"], "REDIRECT")

    def test_with_actor_role(self):
        tp = AttributionTouchpoint(
            touchpoint_id="tp1", subject_id="sub1",
            actor_id="a1", actor_role_at_event="AGENT",
            touchpoint_type=TouchpointType.CONVERSATION_OPEN,
        )
        self.assertEqual(tp.actor_role_at_event, "AGENT")


# ── Lead Source Tests ──────────────────────────────────────────────────────


class LeadSourceTest(unittest.TestCase):
    def test_create(self):
        ls = LeadSource(source_id="s1", source_key="fb-campaign-1",
                         channel="facebook", tracking_code="FB-LAWIM-000001-2026-06-001")
        self.assertEqual(ls.channel, "facebook")

    def test_to_dict(self):
        ls = LeadSource(source_id="s1", source_key="fb-campaign-1",
                         channel="facebook", first_touch_at=_ts())
        d = ls.to_dict()
        self.assertEqual(d["channel"], "facebook")


# ── Conversion Event Tests ─────────────────────────────────────────────────


class ConversionEventTest(unittest.TestCase):
    def test_create_minimal(self):
        e = ConversionEvent(event_id="e1", conversion_type="sale")
        self.assertEqual(e.conversion_type, "sale")

    def test_with_full_chain(self):
        e = ConversionEvent(
            event_id="e1", conversion_type="property_sale",
            conversation_id="conv1", matching_id="match1",
            visit_id="visit1", transaction_id="trx1",
            payment_id="pay1", payment_provider="campay",
            monetary_value=50000000, currency="XAF",
            tracking_code="FB-LAWIM-000001-2026-06-001",
            channel="FACEBOOK",
        )
        self.assertEqual(e.monetary_value, 50000000)
        self.assertEqual(e.payment_provider, "campay")
        self.assertEqual(len(e.conversation_id), 5)

    def test_to_dict(self):
        e = ConversionEvent(event_id="e1", conversion_type="sale", monetary_value=500000)
        d = e.to_dict()
        self.assertEqual(d["monetary_value"], 500000)

    def test_deduplication_key(self):
        linking = ConversionLinkingService()
        e1 = linking.finalize(ConversionEvent(event_id="e1", conversion_type="sale", conversation_id="conv1"))
        e2 = linking.finalize(ConversionEvent(event_id="e2", conversion_type="sale", conversation_id="conv2"))
        self.assertNotEqual(e1.deduplication_key, e2.deduplication_key)


# ── Lead Attribution Tests ─────────────────────────────────────────────────


class LeadAttributionTest(unittest.TestCase):
    def test_first_touch_model(self):
        a = LeadAttribution(attribution_id="a1", model=AttributionModel.FIRST_TOUCH)
        self.assertEqual(a.model, AttributionModel.FIRST_TOUCH)

    def test_last_touch_model(self):
        a = LeadAttribution(attribution_id="a1", model=AttributionModel.LAST_TOUCH)
        self.assertEqual(a.model, AttributionModel.LAST_TOUCH)

    def test_multi_touch_model(self):
        a = LeadAttribution(attribution_id="a1", model=AttributionModel.MULTI_TOUCH)
        self.assertEqual(a.model, AttributionModel.MULTI_TOUCH)

    def test_lawim_attribution_model(self):
        a = LeadAttribution(attribution_id="a1", model=AttributionModel.LAWIM_ATTRIBUTION)
        self.assertEqual(a.model, AttributionModel.LAWIM_ATTRIBUTION)

    def test_to_dict(self):
        a = LeadAttribution(attribution_id="a1", model=AttributionModel.FIRST_TOUCH)
        d = a.to_dict()
        self.assertEqual(d["model"], "FIRST_TOUCH")

    def test_explanation(self):
        a = LeadAttribution(attribution_id="a1", model=AttributionModel.FIRST_TOUCH,
                              explanation="First click on FB ad")
        self.assertEqual(a.explanation, "First click on FB ad")


# ── TrackingResolutionService Tests ────────────────────────────────────────


class TrackingResolutionServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = TrackingResolutionService()

    def test_validate_valid_code(self):
        code = generate_tracking_code("FB", 128, 2026, 6, 1)
        self.assertTrue(self.svc.validate_tracking_code(code))

    def test_validate_invalid_code(self):
        self.assertFalse(self.svc.validate_tracking_code(""))

    def test_validate_malformed(self):
        self.assertFalse(self.svc.validate_tracking_code("XX-LAWIM-abc-2026-06-01"))

    def test_parse_valid(self):
        parsed = self.svc.parse("FB-LAWIM-000128-2026-06-001")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["channel_code"], "FB")

    def test_parse_invalid(self):
        self.assertIsNone(self.svc.parse("invalid"))

    def test_generate_with_channel_enum(self):
        code = self.svc.generate("WA", 100)
        self.assertTrue(code.startswith("WA-LAWIM"))

    def test_generate_with_channel_string(self):
        code = self.svc.generate("whatsapp", 100)
        self.assertTrue(code.startswith("WA-LAWIM"))


# ── TouchpointIngestionService Tests ───────────────────────────────────────


class TouchpointIngestionServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = TouchpointIngestionService()

    def test_create_dedup_key(self):
        key = self.svc.create_deduplication_key("CLICK", "user1", _ts(), "FACEBOOK")
        self.assertEqual(len(key), 32)

    def test_normalize_redirect(self):
        redirect = RedirectLog(
            redirect_id="r1", tracking_code="FB-LAWIM-000001-2026-06-001",
            session_id="sess1", user_id=1,
            occurred_at=_ts(),
        )
        tp = self.svc.normalize_redirect(redirect)
        self.assertEqual(tp.touchpoint_type, TouchpointType.REDIRECT)
        self.assertEqual(tp.tracking_code, "FB-LAWIM-000001-2026-06-001")
        self.assertIsNotNone(tp.deduplication_key)

    def test_create_touchpoint(self):
        tp = self.svc.create_touchpoint(TouchpointType.CONVERSATION_OPEN, "sub1")
        self.assertEqual(tp.touchpoint_type, TouchpointType.CONVERSATION_OPEN)
        self.assertIsNotNone(tp.deduplication_key)

    def test_create_with_tracking(self):
        tp = self.svc.create_touchpoint(TouchpointType.CLICK, "sub1",
                                          channel="FACEBOOK",
                                          tracking_code="FB-LAWIM-000001-2026-06-001")
        self.assertEqual(tp.tracking_code, "FB-LAWIM-000001-2026-06-001")
        self.assertEqual(tp.channel, "FACEBOOK")


# ── AttributionEngine Tests ────────────────────────────────────────────────


class AttributionEngineFirstTouchTest(unittest.TestCase):
    def setUp(self):
        self.engine = AttributionEngine(window_days=30)
        self.conversion = ConversionEvent(
            event_id="e1", conversion_type="sale",
            occurred_at=_ts(0),
        )
        self.touchpoints = [
            AttributionTouchpoint(touchpoint_id="tp1", subject_id="s1",
                                   touchpoint_type=TouchpointType.CLICK,
                                   occurred_at=_ts(25), channel="FACEBOOK"),
            AttributionTouchpoint(touchpoint_id="tp2", subject_id="s1",
                                   touchpoint_type=TouchpointType.CONVERSATION_OPEN,
                                   occurred_at=_ts(10), channel="WHATSAPP"),
            AttributionTouchpoint(touchpoint_id="tp3", subject_id="s1",
                                   touchpoint_type=TouchpointType.PAYMENT,
                                   occurred_at=_ts(1), channel="WHATSAPP"),
        ]

    def test_first_touch_returns_earliest(self):
        ft = self.engine.first_touch(self.touchpoints, self.conversion)
        self.assertIsNotNone(ft)
        self.assertEqual(ft.touchpoint_id, "tp1")

    def test_first_touch_outside_window(self):
        outside = [
            AttributionTouchpoint(touchpoint_id="tp4", subject_id="s1",
                                   touchpoint_type=TouchpointType.CLICK,
                                   occurred_at=_ts(60), channel="FACEBOOK"),
        ]
        ft = self.engine.first_touch(outside, self.conversion)
        self.assertIsNone(ft)

    def test_last_touch_returns_latest(self):
        lt = self.engine.last_touch(self.touchpoints, self.conversion)
        self.assertIsNotNone(lt)
        self.assertEqual(lt.touchpoint_id, "tp3")

    def test_multi_touch_equal_weights(self):
        mt = self.engine.multi_touch(self.touchpoints, self.conversion)
        self.assertEqual(len(mt), 3)
        for v in mt.values():
            self.assertAlmostEqual(v, 1.0 / 3)

    def test_empty_touchpoints(self):
        ft = self.engine.first_touch([], self.conversion)
        self.assertIsNone(ft)

    def test_calculate_first_touch(self):
        result = self.engine.calculate(AttributionModel.FIRST_TOUCH, self.touchpoints, self.conversion)
        self.assertEqual(result.model, AttributionModel.FIRST_TOUCH)
        self.assertEqual(result.selected_first_touch, "tp1")

    def test_calculate_last_touch(self):
        result = self.engine.calculate(AttributionModel.LAST_TOUCH, self.touchpoints, self.conversion)
        self.assertEqual(result.model, AttributionModel.LAST_TOUCH)
        self.assertEqual(result.selected_last_touch, "tp3")

    def test_calculate_multi_touch(self):
        result = self.engine.calculate(AttributionModel.MULTI_TOUCH, self.touchpoints, self.conversion)
        self.assertEqual(result.model, AttributionModel.MULTI_TOUCH)
        self.assertEqual(len(result.weights), 3)

    def test_calculate_lawim_attribution(self):
        result = self.engine.calculate(AttributionModel.LAWIM_ATTRIBUTION, self.touchpoints, self.conversion)
        self.assertEqual(result.model, AttributionModel.LAWIM_ATTRIBUTION)
        self.assertIn("weights", result.__dict__)
        self.assertTrue(len(result.explanation) > 0)

    def test_recalculation_deterministic(self):
        r1 = self.engine.calculate(AttributionModel.FIRST_TOUCH, self.touchpoints, self.conversion)
        r2 = self.engine.recalculate(r1, self.touchpoints, self.conversion)
        self.assertEqual(r2.model, AttributionModel.FIRST_TOUCH)
        self.assertEqual(r2.selected_first_touch, "tp1")
        self.assertNotEqual(r1.calculated_at, r2.calculated_at)


class AttributionEngineMultiChannelTest(unittest.TestCase):
    def setUp(self):
        self.engine = AttributionEngine(window_days=30)
        self.conversion = ConversionEvent(event_id="e1", conversion_type="sale", occurred_at=_ts(0))

    def test_multiple_channels(self):
        tps = [
            AttributionTouchpoint(touchpoint_id="tp1", subject_id="s1",
                                   touchpoint_type=TouchpointType.CLICK,
                                   occurred_at=_ts(20), channel="FACEBOOK",
                                   tracking_code="FB-LAWIM-000001-2026-06-001"),
            AttributionTouchpoint(touchpoint_id="tp2", subject_id="s1",
                                   touchpoint_type=TouchpointType.CONVERSATION_OPEN,
                                   occurred_at=_ts(15), channel="WHATSAPP",
                                   tracking_code="WA-LAWIM-000001-2026-06-001"),
            AttributionTouchpoint(touchpoint_id="tp3", subject_id="s1",
                                   touchpoint_type=TouchpointType.VISIT,
                                   occurred_at=_ts(10), channel="AGENCY"),
            AttributionTouchpoint(touchpoint_id="tp4", subject_id="s1",
                                   touchpoint_type=TouchpointType.PAYMENT,
                                   occurred_at=_ts(1), channel="WHATSAPP",
                                   touchpoint_value=500000),
        ]
        ft = self.engine.first_touch(tps, self.conversion)
        self.assertEqual(ft.channel, "FACEBOOK")
        lt = self.engine.last_touch(tps, self.conversion)
        self.assertEqual(lt.channel, "WHATSAPP")

    def test_single_touchpoint(self):
        tps = [
            AttributionTouchpoint(touchpoint_id="tp1", subject_id="s1",
                                   touchpoint_type=TouchpointType.CLICK,
                                   occurred_at=_ts(5), channel="FACEBOOK"),
        ]
        ft = self.engine.first_touch(tps, self.conversion)
        lt = self.engine.last_touch(tps, self.conversion)
        self.assertEqual(ft.touchpoint_id, lt.touchpoint_id)


# ── ConversionLinkingService Tests ─────────────────────────────────────────


class ConversionLinkingServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = ConversionLinkingService()
        self.conversion = ConversionEvent(event_id="e1", conversion_type="sale")

    def test_link_conversation(self):
        self.svc.link_conversation("conv1", self.conversion)
        self.assertEqual(self.conversion.conversation_id, "conv1")

    def test_link_matching(self):
        self.svc.link_matching("match1", self.conversion)
        self.assertEqual(self.conversion.matching_id, "match1")

    def test_link_visit(self):
        self.svc.link_visit("visit1", self.conversion)
        self.assertEqual(self.conversion.visit_id, "visit1")

    def test_link_transaction(self):
        self.svc.link_transaction("trx1", self.conversion)
        self.assertEqual(self.conversion.transaction_id, "trx1")

    def test_link_payment(self):
        self.svc.link_payment("pay1", "campay", 500000, "XAF", self.conversion)
        self.assertEqual(self.conversion.payment_id, "pay1")
        self.assertEqual(self.conversion.monetary_value, 500000)

    def test_finalize_creates_dedup_key(self):
        self.svc.link_conversation("conv1", self.conversion)
        self.svc.link_payment("pay1", "campay", 500000, "XAF", self.conversion)
        self.svc.finalize(self.conversion)
        self.assertTrue(len(self.conversion.deduplication_key) > 0)

    def test_duplicate_detection(self):
        e1 = ConversionEvent(event_id="e1", conversion_type="sale", conversation_id="conv1")
        e2 = ConversionEvent(event_id="e2", conversion_type="sale", conversation_id="conv1")
        existing = [self.svc.finalize(e1)]
        dup = self.svc.finalize(e2)
        self.assertTrue(self.svc.is_duplicate(dup, existing))

    def test_no_duplicate_different_conv(self):
        e1 = ConversionEvent(event_id="e1", conversion_type="sale", conversation_id="conv1")
        e2 = ConversionEvent(event_id="e2", conversion_type="sale", conversation_id="conv2")
        existing = [self.svc.finalize(e1)]
        not_dup = self.svc.finalize(e2)
        self.assertFalse(self.svc.is_duplicate(not_dup, existing))


# ── TrackingConfig Tests ───────────────────────────────────────────────────


class TrackingConfigTest(unittest.TestCase):
    def test_default_disabled(self):
        cfg = TrackingConfig()
        self.assertFalse(cfg.publication_tracking_enabled)
        self.assertFalse(cfg.attribution_engine_enabled)
        self.assertFalse(cfg.conversion_event_chain_enabled)

    def test_enable_publication(self):
        cfg = TrackingConfig(publication_tracking_enabled=True)
        self.assertTrue(cfg.publication_tracking_enabled)

    def test_enable_attribution(self):
        cfg = TrackingConfig(attribution_engine_enabled=True)
        self.assertTrue(cfg.attribution_engine_enabled)

    def test_enable_conversion(self):
        cfg = TrackingConfig(conversion_event_chain_enabled=True)
        self.assertTrue(cfg.conversion_event_chain_enabled)


# ── Model Status Enum Tests ────────────────────────────────────────────────


class CampaignStatusEnumTest(unittest.TestCase):
    def test_draft(self):
        self.assertEqual(CampaignStatus.DRAFT.value, "DRAFT")

    def test_active(self):
        self.assertEqual(CampaignStatus.ACTIVE.value, "ACTIVE")

    def test_completed(self):
        self.assertEqual(CampaignStatus.COMPLETED.value, "COMPLETED")

    def test_cancelled(self):
        self.assertEqual(CampaignStatus.CANCELLED.value, "CANCELLED")

    def test_archived(self):
        self.assertEqual(CampaignStatus.ARCHIVED.value, "ARCHIVED")


class PublicationStatusEnumTest(unittest.TestCase):
    def test_draft(self):
        self.assertEqual(PublicationStatus.DRAFT.value, "DRAFT")

    def test_published(self):
        self.assertEqual(PublicationStatus.PUBLISHED.value, "PUBLISHED")

    def test_scheduled(self):
        self.assertEqual(PublicationStatus.SCHEDULED.value, "SCHEDULED")

    def test_archived(self):
        self.assertEqual(PublicationStatus.ARCHIVED.value, "ARCHIVED")


class TouchpointTypeEnumTest(unittest.TestCase):
    def test_click(self):
        self.assertEqual(TouchpointType.CLICK.value, "CLICK")

    def test_qr_scan(self):
        self.assertEqual(TouchpointType.QR_SCAN.value, "QR_SCAN")

    def test_conversation_open(self):
        self.assertEqual(TouchpointType.CONVERSATION_OPEN.value, "CONVERSATION_OPEN")

    def test_payment(self):
        self.assertEqual(TouchpointType.PAYMENT.value, "PAYMENT")

    def test_conversion(self):
        self.assertEqual(TouchpointType.CONVERSION.value, "CONVERSION")


class AttributionModelEnumTest(unittest.TestCase):
    def test_first_touch(self):
        self.assertEqual(AttributionModel.FIRST_TOUCH.value, "FIRST_TOUCH")

    def test_last_touch(self):
        self.assertEqual(AttributionModel.LAST_TOUCH.value, "LAST_TOUCH")

    def test_multi_touch(self):
        self.assertEqual(AttributionModel.MULTI_TOUCH.value, "MULTI_TOUCH")

    def test_lawim(self):
        self.assertEqual(AttributionModel.LAWIM_ATTRIBUTION.value, "LAWIM_ATTRIBUTION")


# ── JSON Serialization ─────────────────────────────────────────────────────


class TrackingSerializationTest(unittest.TestCase):
    def test_campaign_json(self):
        c = ExternalCampaign(campaign_id="c1", campaign_name="FB Campaign")
        s = json.dumps(c.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("campaign_name", s)

    def test_publication_json(self):
        p = ExternalPublication(publication_id="p1", tracking_code="FB-LAWIM-000001-2026-06-001")
        s = json.dumps(p.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("FB-LAWIM", s)

    def test_conversion_json(self):
        e = ConversionEvent(event_id="e1", conversion_type="sale", monetary_value=500000)
        s = json.dumps(e.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("500000", s)

    def test_attribution_json(self):
        a = LeadAttribution(attribution_id="a1", model=AttributionModel.FIRST_TOUCH)
        s = json.dumps(a.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("FIRST_TOUCH", s)


# ── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main()
