# Program J — Analytics, Dashboards and Recalculation Tests
from __future__ import annotations

import json
import unittest
from datetime import datetime, timedelta, timezone

from lawim_v2.program_j.analytics_config import AnalyticsConfig
from lawim_v2.program_j.analytics_engine import AnalyticsDataQualityService, AnalyticsEngine, DashboardBuilder
from lawim_v2.program_j.analytics_models import (
    ANALYTICS_DIMENSIONS,
    AggregationType,
    AnalyticAggregate,
    AnalyticsRun,
    DashboardSummary,
    DataQualityCheck,
    DataQualityStatus,
    MetricDefinition,
    MetricDomain,
    MetricStatus,
    RecalculationMode,
    RecalculationStatus,
)
from lawim_v2.program_j.analytics_registry import get_metric, list_metrics, metric_codes, to_dict_list
from lawim_v2.program_j.tracking_models import (
    ConversionEvent,
    ExternalCampaign,
    ExternalPublication,
    RedirectLog,
)

# ── Helpers ────────────────────────────────────────────────────────────────


def _ts(days_ago: int = 0) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


# ── Metric Catalog Tests ───────────────────────────────────────────────────


class MetricCatalogTest(unittest.TestCase):
    def test_catalog_not_empty(self):
        self.assertGreater(len(list_metrics()), 0)

    def test_unique_codes(self):
        codes = metric_codes()
        self.assertEqual(len(codes), len(set(codes)))

    def test_required_metrics_exist(self):
        for code in ("CAMPAIGNS_TOTAL", "PUBLICATIONS_TOTAL", "CLICKS_TOTAL",
                      "CONVERSIONS_TOTAL", "CONVERSION_RATE", "REVENUE_TOTAL"):
            self.assertIsNotNone(get_metric(code), f"Missing: {code}")

    def test_all_have_formula(self):
        for m in list_metrics():
            self.assertTrue(m.formula, f"{m.metric_code} missing formula")

    def test_all_have_version(self):
        for m in list_metrics():
            self.assertTrue(m.formula_version, f"{m.metric_code} missing version")

    def test_all_have_domain(self):
        for m in list_metrics():
            self.assertIn(m.domain, MetricDomain)

    def test_metric_to_dict(self):
        m = get_metric("CAMPAIGNS_TOTAL")
        self.assertIsNotNone(m)
        d = m.to_dict()
        self.assertEqual(d["metric_code"], "CAMPAIGNS_TOTAL")
        self.assertEqual(d["aggregation_type"], "COUNT")

    def test_conversion_rate_is_rate(self):
        m = get_metric("CONVERSION_RATE")
        self.assertEqual(m.aggregation_type, AggregationType.RATE)

    def test_revenue_total_is_sum(self):
        m = get_metric("REVENUE_TOTAL")
        self.assertEqual(m.aggregation_type, AggregationType.SUM)

    def test_metric_count(self):
        self.assertGreaterEqual(len(list_metrics()), 25)

    def test_to_dict_list(self):
        dl = to_dict_list()
        self.assertEqual(len(dl), len(list_metrics()))

    def test_json_serializable(self):
        dl = to_dict_list()
        s = json.dumps(dl, ensure_ascii=False, sort_keys=True)
        self.assertGreater(len(s), 100)


# ── Analytics Dimensions Tests ─────────────────────────────────────────────


class AnalyticsDimensionsTest(unittest.TestCase):
    def test_dimensions_not_empty(self):
        self.assertGreater(len(ANALYTICS_DIMENSIONS), 0)

    def test_channel_dimension(self):
        self.assertIn("channel", ANALYTICS_DIMENSIONS)

    def test_campaign_dimension(self):
        self.assertIn("campaign", ANALYTICS_DIMENSIONS)

    def test_actor_role_dimension(self):
        self.assertIn("actor_role_at_publication", ANALYTICS_DIMENSIONS)

    def test_historical_role_dimension(self):
        self.assertIn("current_actor_role", ANALYTICS_DIMENSIONS)

    def test_unique_dimensions(self):
        self.assertEqual(len(ANALYTICS_DIMENSIONS), len(set(ANALYTICS_DIMENSIONS)))


# ── Analytics Engine Tests ─────────────────────────────────────────────────


class AnalyticsEngineMetricTest(unittest.TestCase):
    def setUp(self):
        self.engine = AnalyticsEngine()
        self.events = [
            {"channel": "FACEBOOK", "actor_id": "a1", "monetary_value": 100000},
            {"channel": "WHATSAPP", "actor_id": "a2", "monetary_value": 200000},
            {"channel": "FACEBOOK", "actor_id": "a1", "monetary_value": 300000},
            {"channel": "TELEGRAM", "actor_id": "a3", "monetary_value": 0},
        ]

    def test_count_metric(self):
        result = self.engine.calculate_metric("CAMPAIGNS_TOTAL", self.events)
        self.assertEqual(result["value"], 4)
        self.assertEqual(result["source_count"], 4)

    def test_unknown_metric(self):
        result = self.engine.calculate_metric("UNKNOWN", self.events)
        self.assertIn("error", result)

    def test_metric_with_filters(self):
        result = self.engine.calculate_metric("CAMPAIGNS_TOTAL", self.events,
                                               {"channel": "FACEBOOK"})
        self.assertEqual(result["value"], 2)

    def test_metric_with_multiple_filters(self):
        result = self.engine.calculate_metric("CAMPAIGNS_TOTAL", self.events,
                                               {"channel": "FACEBOOK", "actor_id": "a1"})
        self.assertEqual(result["value"], 2)

    def test_filter_none_value(self):
        result = self.engine.calculate_metric("CAMPAIGNS_TOTAL", self.events, {"channel": None})
        self.assertEqual(result["value"], 4)


class AnalyticsEngineGroupByTest(unittest.TestCase):
    def setUp(self):
        self.engine = AnalyticsEngine()
        self.events = [
            {"channel": "FACEBOOK", "actor_id": "a1"},
            {"channel": "WHATSAPP", "actor_id": "a2"},
            {"channel": "FACEBOOK", "actor_id": "a3"},
        ]

    def test_group_by_channel(self):
        result = self.engine.group_by("CAMPAIGNS_TOTAL", self.events, "channel")
        self.assertGreaterEqual(len(result), 2)
        fb = [r for r in result if r["dimension_value"] == "FACEBOOK"]
        wa = [r for r in result if r["dimension_value"] == "WHATSAPP"]
        self.assertEqual(len(fb), 1)
        self.assertEqual(len(wa), 1)
        self.assertEqual(fb[0]["source_count"], 2)
        self.assertEqual(wa[0]["source_count"], 1)

    def test_group_by_unknown_dimension(self):
        result = self.engine.group_by("CAMPAIGNS_TOTAL", self.events, "unknown_dim")
        self.assertIn("error", result[0])

    def test_empty_events(self):
        result = self.engine.group_by("CAMPAIGNS_TOTAL", [], "channel")
        self.assertEqual(len(result), 0)


class AnalyticsEngineComparePeriodsTest(unittest.TestCase):
    def setUp(self):
        self.engine = AnalyticsEngine()
        self.events = [
            {"channel": "FB", "occurred_at": "2026-06-01T00:00:00"},
            {"channel": "FB", "occurred_at": "2026-06-15T00:00:00"},
            {"channel": "WA", "occurred_at": "2026-07-01T00:00:00"},
        ]

    def test_compare_periods_increase(self):
        result = self.engine.compare_periods(
            "CAMPAIGNS_TOTAL", self.events,
            "2026-06-01", "2026-06-30",
            "2026-07-01", "2026-07-31",
        )
        self.assertEqual(result["period1"]["value"], 2)
        self.assertEqual(result["period2"]["value"], 1)
        self.assertEqual(result["absolute_change"], -1)

    def test_compare_periods_no_change(self):
        result = self.engine.compare_periods(
            "CAMPAIGNS_TOTAL", self.events,
            "2026-06-01", "2026-06-30",
            "2026-06-01", "2026-06-30",
        )
        self.assertEqual(result["absolute_change"], 0)


class AnalyticsEngineExplainTest(unittest.TestCase):
    def setUp(self):
        self.engine = AnalyticsEngine()

    def test_explain_metric(self):
        result = self.engine.explain_metric("CAMPAIGNS_TOTAL")
        self.assertEqual(result["metric_code"], "CAMPAIGNS_TOTAL")

    def test_explain_unknown(self):
        result = self.engine.explain_metric("UNKNOWN")
        self.assertIn("error", result)


class AnalyticsEngineRecalculationTest(unittest.TestCase):
    def setUp(self):
        self.engine = AnalyticsEngine()
        self.events = [{"channel": "FB"}, {"channel": "WA"}, {"channel": "TG"}]

    def test_rebuild_full(self):
        run = self.engine.rebuild_aggregates(self.events, RecalculationMode.FULL_REBUILD)
        self.assertEqual(run.status, RecalculationStatus.COMPLETED)
        self.assertEqual(run.source_event_count, 3)

    def test_rebuild_with_metric_filter(self):
        run = self.engine.rebuild_aggregates(self.events, metric_filter=["CAMPAIGNS_TOTAL"])
        self.assertEqual(run.status, RecalculationStatus.COMPLETED)

    def test_rebuild_mode(self):
        run = self.engine.rebuild_aggregates(self.events, RecalculationMode.INCREMENTAL)
        self.assertEqual(run.mode, RecalculationMode.INCREMENTAL)

    def test_rebuild_validation_only(self):
        run = self.engine.rebuild_aggregates(self.events, RecalculationMode.VALIDATION_ONLY)
        self.assertEqual(run.mode, RecalculationMode.VALIDATION_ONLY)


class AnalyticsEngineValidateAggregatesTest(unittest.TestCase):
    def setUp(self):
        self.engine = AnalyticsEngine()

    def test_validate_no_duplicates(self):
        aggs = [
            AnalyticAggregate(metric_code="C1", dimension_key="channel", dimension_value="FB",
                               metric_value=10),
            AnalyticAggregate(metric_code="C2", dimension_key="channel", dimension_value="WA",
                               metric_value=20),
        ]
        checks = self.engine.validate_aggregates(aggs)
        dupes = [c for c in checks if c.check_type == "duplicate_aggregate"]
        self.assertEqual(len(dupes), 0)

    def test_validate_with_duplicates(self):
        aggs = [
            AnalyticAggregate(metric_code="C1", dimension_key="channel", dimension_value="FB",
                               metric_value=10),
            AnalyticAggregate(metric_code="C1", dimension_key="channel", dimension_value="FB",
                               metric_value=20),
        ]
        checks = self.engine.validate_aggregates(aggs)
        dupes = [c for c in checks if c.check_type == "duplicate_aggregate"]
        self.assertGreaterEqual(len(dupes), 1)


# ── Data Quality Tests ─────────────────────────────────────────────────────


class AnalyticsDataQualityTest(unittest.TestCase):
    def setUp(self):
        self.svc = AnalyticsDataQualityService()

    def test_orphan_events_no_actor(self):
        events = [{"actor_id": ""}, {"channel": "FB"}]
        checks = self.svc._check_orphan_events(events)
        self.assertGreaterEqual(len(checks), 1)

    def test_orphan_events_no_channel(self):
        events = [{"actor_id": "a1", "channel": ""}]
        checks = self.svc._check_orphan_events(events)
        self.assertGreaterEqual(len(checks), 1)

    def test_no_orphans(self):
        events = [{"actor_id": "a1", "channel": "FB"}]
        checks = self.svc._check_orphan_events(events)
        self.assertEqual(len(checks), 0)

    def test_duplicate_conversions(self):
        svc = __import__("lawim_v2.program_j.tracking_services", fromlist=["ConversionLinkingService"])
        linking = svc.ConversionLinkingService()
        e1 = linking.finalize(ConversionEvent(event_id="e1", conversion_type="sale", conversation_id="c1"))
        e2 = linking.finalize(ConversionEvent(event_id="e2", conversion_type="sale", conversation_id="c1"))
        checks = self.svc._check_duplicate_conversions([e1, e2])
        self.assertGreaterEqual(len(checks), 1)

    def test_no_duplicate_conversions(self):
        e1 = ConversionEvent(event_id="e1", conversion_type="sale", conversation_id="c1")
        e2 = ConversionEvent(event_id="e2", conversion_type="sale", conversation_id="c2")
        checks = self.svc._check_duplicate_conversions([e1, e2])
        self.assertEqual(len(checks), 0)

    def test_run_checks(self):
        events = [{"actor_id": ""}, {"channel": "FB", "actor_id": "a1"}]
        conversions = [ConversionEvent(event_id="e1", conversion_type="sale", conversation_id="c1")]
        checks = self.svc.run_checks(events, conversions)
        self.assertGreaterEqual(len(checks), 1)

    def test_data_quality_check_to_dict(self):
        check = DataQualityCheck(check_id="c1", check_type="orphan", status=DataQualityStatus.WARNING,
                                  message="test", affected_count=3)
        d = check.to_dict()
        self.assertEqual(d["status"], "WARNING")


# ── Dashboard Builder Tests ────────────────────────────────────────────────


class DashboardBuilderTest(unittest.TestCase):
    def setUp(self):
        self.builder = DashboardBuilder()

    def test_admin_summary(self):
        campaigns = [{"campaign_id": "c1"}, {"campaign_id": "c2"}]
        publications = [{"publication_id": "p1"}]
        redirects = [
            {"is_bot": False, "session_id": "s1"},
            {"is_bot": True, "session_id": "s2"},
            {"is_bot": False, "session_id": "s1"},
        ]
        conversations = [{"conversation_id": "conv1"}]
        conversions = [{"monetary_value": 500000}, {"monetary_value": 300000}]
        payments = [{"status": "confirmed"}, {"status": "pending"}]
        summary = self.builder.build_admin(campaigns, publications, redirects,
                                            conversations, conversions, payments)
        self.assertEqual(summary.total_campaigns, 2)
        self.assertEqual(summary.total_publications, 1)
        self.assertEqual(summary.total_clicks, 2)
        self.assertEqual(summary.total_unique_clicks, 1)
        self.assertEqual(summary.total_bots, 1)
        self.assertEqual(summary.total_redirects, 3)
        self.assertEqual(summary.total_conversations, 1)
        self.assertEqual(summary.total_conversions, 2)
        self.assertEqual(summary.total_payments, 1)
        self.assertEqual(summary.total_revenue, 800000)

    def test_empty_summary(self):
        summary = self.builder.build_admin([], [], [], [], [], [])
        self.assertEqual(summary.total_campaigns, 0)
        self.assertEqual(summary.total_revenue, 0)

    def test_summary_to_dict(self):
        summary = DashboardSummary(total_campaigns=5, total_revenue=1000000)
        d = summary.to_dict()
        self.assertEqual(d["total_campaigns"], 5)
        self.assertEqual(d["total_revenue"], 1000000)


# ── Analytics Config Tests ─────────────────────────────────────────────────


class AnalyticsConfigTest(unittest.TestCase):
    def test_default_disabled(self):
        cfg = AnalyticsConfig()
        self.assertFalse(cfg.marketing_analytics_enabled)
        self.assertFalse(cfg.analytics_dashboards_enabled)
        self.assertFalse(cfg.analytics_recalculation_enabled)

    def test_enable_marketing(self):
        cfg = AnalyticsConfig(marketing_analytics_enabled=True)
        self.assertTrue(cfg.marketing_analytics_enabled)

    def test_enable_dashboards(self):
        cfg = AnalyticsConfig(analytics_dashboards_enabled=True)
        self.assertTrue(cfg.analytics_dashboards_enabled)

    def test_enable_recalculation(self):
        cfg = AnalyticsConfig(analytics_recalculation_enabled=True)
        self.assertTrue(cfg.analytics_recalculation_enabled)


# ── AnalyticsRun Tests ─────────────────────────────────────────────────────


class AnalyticsRunTest(unittest.TestCase):
    def test_create_full_rebuild(self):
        run = AnalyticsRun(run_id="r1", mode=RecalculationMode.FULL_REBUILD)
        self.assertEqual(run.status, RecalculationStatus.PENDING)
        self.assertEqual(run.mode, RecalculationMode.FULL_REBUILD)

    def test_to_dict(self):
        run = AnalyticsRun(run_id="r1", mode=RecalculationMode.FULL_REBUILD)
        d = run.to_dict()
        self.assertEqual(d["run_id"], "r1")

    def test_completed_status(self):
        run = AnalyticsRun(run_id="r1", mode=RecalculationMode.FULL_REBUILD,
                            status=RecalculationStatus.COMPLETED, source_event_count=100)
        self.assertEqual(run.status, RecalculationStatus.COMPLETED)
        self.assertEqual(run.source_event_count, 100)


# ── JSON Serialization ─────────────────────────────────────────────────────


class AnalyticsSerializationTest(unittest.TestCase):
    def test_metric_definition_json(self):
        m = MetricDefinition("TEST", "Test", "Test metric", MetricDomain.GENERAL,
                              "unit", AggregationType.COUNT, "COUNT(*)", "1.0")
        s = json.dumps(m.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("TEST", s)

    def test_dashboard_summary_json(self):
        ds = DashboardSummary(total_campaigns=10, total_revenue=500000)
        s = json.dumps(ds.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("500000", s)

    def test_analytics_run_json(self):
        run = AnalyticsRun(run_id="r1", mode=RecalculationMode.FULL_REBUILD,
                            status=RecalculationStatus.COMPLETED)
        s = json.dumps(run.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("FULL_REBUILD", s)

    def test_aggregate_json(self):
        agg = AnalyticAggregate(metric_code="CLICKS_TOTAL", dimension_key="channel",
                                 dimension_value="FB", metric_value=100)
        s = json.dumps(agg.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("CLICKS_TOTAL", s)


# ── Recalculation Mode Enum Tests ─────────────────────────────────────────


class RecalculationModeEnumTest(unittest.TestCase):
    def test_full_rebuild(self):
        self.assertEqual(RecalculationMode.FULL_REBUILD.value, "FULL_REBUILD")

    def test_incremental(self):
        self.assertEqual(RecalculationMode.INCREMENTAL.value, "INCREMENTAL")

    def test_targeted(self):
        self.assertEqual(RecalculationMode.TARGETED.value, "TARGETED")

    def test_validation_only(self):
        self.assertEqual(RecalculationMode.VALIDATION_ONLY.value, "VALIDATION_ONLY")


class RecalculationStatusEnumTest(unittest.TestCase):
    def test_pending(self):
        self.assertEqual(RecalculationStatus.PENDING.value, "PENDING")

    def test_completed(self):
        self.assertEqual(RecalculationStatus.COMPLETED.value, "COMPLETED")

    def test_failed(self):
        self.assertEqual(RecalculationStatus.FAILED.value, "FAILED")


class AggregationTypeEnumTest(unittest.TestCase):
    def test_count(self):
        self.assertEqual(AggregationType.COUNT.value, "COUNT")

    def test_rate(self):
        self.assertEqual(AggregationType.RATE.value, "RATE")

    def test_distinct_count(self):
        self.assertEqual(AggregationType.DISTINCT_COUNT.value, "DISTINCT_COUNT")


# ── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main()
