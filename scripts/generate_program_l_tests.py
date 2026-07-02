#!/usr/bin/env python3
"""Generate tests/test_release_program_l.py for Release Program L."""
from __future__ import annotations

from pathlib import Path

from lawim_v2.analytics.constants import (
    AGGREGATION_TYPES,
    ANALYTIC_SOURCES,
    DASHBOARD_TYPES,
    DATA_MART_TYPES,
    DEFAULT_DASHBOARDS,
    DEFAULT_DATA_MARTS,
    DEFAULT_KPI_DEFINITIONS,
    DEFAULT_SCORE_DEFINITIONS,
    EVENT_TYPES,
    EXPORT_FORMATS,
    INSIGHT_TYPES,
    KPI_CATEGORIES,
    METRIC_CATEGORIES,
    PROGRAM_CODES,
    REPORT_FORMATS,
    REPORT_STATUSES,
    SCORE_TYPES,
    TREND_TYPES,
)
from lawim_v2.analytics.schema_v18_ddl import V18_TABLE_NAMES

HEADER = '''from __future__ import annotations

import sqlite3
import tempfile
from http import HTTPStatus
from pathlib import Path

from lawim_v2.analytics.constants import (
    AGGREGATION_TYPES,
    ANALYTIC_SOURCES,
    DASHBOARD_TYPES,
    DATA_MART_TYPES,
    DEFAULT_DASHBOARDS,
    DEFAULT_DATA_MARTS,
    DEFAULT_KPI_DEFINITIONS,
    DEFAULT_SCORE_DEFINITIONS,
    EVENT_TYPES,
    EXPORT_FORMATS,
    INSIGHT_TYPES,
    KPI_CATEGORIES,
    METRIC_CATEGORIES,
    PROGRAM_CODES,
    REPORT_FORMATS,
    REPORT_STATUSES,
    SCORE_TYPES,
    TREND_TYPES,
)
from lawim_v2.analytics.engines import (
    AiAnalyticsEngine,
    AnalyticsAggregationEngine,
    AnalyticsEngine,
    AnalyticsPermissionEngine,
    AnalyticsPlatformEngine,
    AnalyticsQueryEngine,
    AnalyticsSnapshotEngine,
    BusinessIntelligenceEngine,
    DashboardEngine,
    DataMartEngine,
    ExecutiveDashboardEngine,
    ExportEngine,
    KpiEngine,
    RealTimeAnalyticsEngine,
    ReportingEngine,
    ScoreEngine,
    TrendAnalysisEngine,
)
from lawim_v2.analytics.schema_v18_ddl import V18_TABLE_NAMES
from lawim_v2.communication.schema_v17_ddl import V17_TABLE_NAMES
from lawim_v2.crm.schema_v14_ddl import V14_TABLE_NAMES
from lawim_v2.knowledge_platform.schema_v11_ddl import V11_TABLE_NAMES
from lawim_v2.marketplace.schema_v15_ddl import V15_TABLE_NAMES
from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.real_estate_intelligence.schema_v13_ddl import V13_TABLE_NAMES
from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations, migration_strategy_profile
from lawim_v2.security.schema_v16_ddl import V16_TABLE_NAMES
from lawim_v2.workflow_automation.schema_v12_ddl import V12_TABLE_NAMES

from tests.lawim_harness import LawimTestHarness

'''


def const_tests(prefix: str, const_name: str, values: frozenset[str]) -> list[str]:
    out: list[str] = []
    for value in sorted(values):
        safe = value.replace("-", "_").replace(".", "_")
        out.extend(
            [
                f"    def test_{prefix}_{safe}(self) -> None:",
                f"        self.assertIn({value!r}, {const_name})",
                "",
            ]
        )
    return out


def main() -> None:
    lines = [HEADER]

    lines.extend(
        [
            "class ReleaseProgramLPersistenceTests(LawimTestHarness):",
            "    def test_schema_version_is_v18(self) -> None:",
            "        self.assertEqual(self.repository.schema_version(), 18)",
            "",
            "    def test_application_schema_version_constant(self) -> None:",
            "        self.assertEqual(APPLICATION_SCHEMA_VERSION, 18)",
            "",
            "    def test_analytics_tables_present(self) -> None:",
            "        self.assertTrue(self.repository.analytics_tables_present())",
            "",
            "    def test_all_v18_tables_exist(self) -> None:",
            "        names = {row['name'] for row in self.repository.all(\"SELECT name FROM sqlite_master WHERE type='table'\")}",
            "        for table in V18_TABLE_NAMES:",
            "            self.assertIn(table, names)",
            "",
        ]
    )
    for label, names in [
        ("v17", "V17_TABLE_NAMES"),
        ("v16", "V16_TABLE_NAMES"),
        ("v15", "V15_TABLE_NAMES"),
        ("v14", "V14_TABLE_NAMES"),
        ("v13", "V13_TABLE_NAMES"),
        ("v12", "V12_TABLE_NAMES"),
        ("v11", "V11_TABLE_NAMES"),
    ]:
        lines.extend(
            [
                f"    def test_{label}_tables_still_present(self) -> None:",
                "        names = {row['name'] for row in self.repository.all(\"SELECT name FROM sqlite_master WHERE type='table'\")}",
                f"        for table in {names}:",
                "            self.assertIn(table, names)",
                "",
            ]
        )
    lines.extend(
        [
            "    def test_analytics_catalog_seeded(self) -> None:",
            "        self.assertGreaterEqual(self.repository.scalar('SELECT COUNT(*) FROM analytics_kpi_definitions'), 1)",
            "        self.assertGreaterEqual(self.repository.scalar('SELECT COUNT(*) FROM analytics_dashboards'), 1)",
            "",
            "    def test_v17_to_v18_legacy_migration(self) -> None:",
            "        db_path = Path(tempfile.mkdtemp()) / 'v17.sqlite3'",
            "        conn = sqlite3.connect(db_path)",
            "        conn.executescript(SQLITE_INIT_SCRIPT)",
            "        conn.execute('PRAGMA foreign_keys = OFF')",
            "        for table in V18_TABLE_NAMES:",
            "            conn.execute(f'DROP TABLE IF EXISTS {table}')",
            "        conn.execute('PRAGMA foreign_keys = ON')",
            "        conn.execute(\"UPDATE schema_meta SET value='17' WHERE key='schema_version'\")",
            "        apply_sqlite_legacy_migrations(conn)",
            "        names = {r[0] for r in conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")}",
            "        conn.close()",
            "        self.assertIn('analytics_events', names)",
            "        for table in V17_TABLE_NAMES:",
            "            self.assertIn(table, names)",
            "",
            "    def test_seed_analytics_catalog_idempotent(self) -> None:",
            "        before = self.repository.scalar('SELECT COUNT(*) FROM analytics_kpi_definitions')",
            "        self.repository.seed_analytics_catalog()",
            "        after = self.repository.scalar('SELECT COUNT(*) FROM analytics_kpi_definitions')",
            "        self.assertEqual(before, after)",
            "",
            "",
        ]
    )

    lines.append("class ReleaseProgramLConstantsTests(LawimTestHarness):")
    for prefix, const_name, values in [
        ("event_types", "EVENT_TYPES", EVENT_TYPES),
        ("metric_categories", "METRIC_CATEGORIES", METRIC_CATEGORIES),
        ("kpi_categories", "KPI_CATEGORIES", KPI_CATEGORIES),
        ("dashboard_types", "DASHBOARD_TYPES", DASHBOARD_TYPES),
        ("report_formats", "REPORT_FORMATS", REPORT_FORMATS),
        ("export_formats", "EXPORT_FORMATS", EXPORT_FORMATS),
        ("report_statuses", "REPORT_STATUSES", REPORT_STATUSES),
        ("aggregation_types", "AGGREGATION_TYPES", AGGREGATION_TYPES),
        ("trend_types", "TREND_TYPES", TREND_TYPES),
        ("score_types", "SCORE_TYPES", SCORE_TYPES),
        ("data_mart_types", "DATA_MART_TYPES", DATA_MART_TYPES),
        ("insight_types", "INSIGHT_TYPES", INSIGHT_TYPES),
        ("program_codes", "PROGRAM_CODES", PROGRAM_CODES),
    ]:
        lines.extend(const_tests(prefix, const_name, values))
    lines.append("")

    lines.extend(
        [
            "class ReleaseProgramLEnginesTests(LawimTestHarness):",
            "    def test_analytics_engine_validate_event(self) -> None:",
            "        engine = AnalyticsEngine()",
            "        self.assertEqual(engine.validate_event_type('kpi_computed'), 'kpi_computed')",
            "",
            "    def test_aggregation_engine_sum(self) -> None:",
            "        engine = AnalyticsAggregationEngine()",
            "        self.assertEqual(engine.aggregate([1, 2, 3], 'sum'), 6.0)",
            "",
            "    def test_query_engine_execute(self) -> None:",
            "        engine = AnalyticsQueryEngine()",
            "        q = engine.build_query(name='test')",
            "        result = engine.execute(q, [{'a': 1}])",
            "        self.assertEqual(result['row_count'], 1)",
            "",
            "    def test_reporting_engine_pdf_architecture(self) -> None:",
            "        engine = ReportingEngine()",
            "        out = engine.generate_output(report_type='x', data={}, fmt='pdf')",
            "        self.assertTrue(out['architecture_only'])",
            "",
            "    def test_trend_anomalies(self) -> None:",
            "        engine = TrendAnalysisEngine()",
            "        anomalies = engine.detect_anomalies([1, 1, 1, 1, 1, 50], threshold=1.5)",
            "        self.assertTrue(anomalies)",
            "",
            "    def test_ai_engine_insight(self) -> None:",
            "        engine = AiAnalyticsEngine()",
            "        insight = engine.generate_insight(insight_type='trend', title='T', content={})",
            "        self.assertTrue(insight['traceable'])",
            "",
            "    def test_platform_engine_catalog(self) -> None:",
            "        engine = AnalyticsPlatformEngine()",
            "        self.assertGreater(len(engine.integration_catalog()), 10)",
            "",
        ]
    )
    for agg in sorted(AGGREGATION_TYPES):
        lines.extend(
            [
                f"    def test_aggregation_engine_{agg}(self) -> None:",
                "        engine = AnalyticsAggregationEngine()",
                f"        self.assertEqual(engine.validate_type('{agg}'), '{agg}')",
                "",
            ]
        )
    for fmt in sorted(REPORT_FORMATS):
        lines.extend(
            [
                f"    def test_reporting_engine_{fmt}(self) -> None:",
                "        engine = ReportingEngine()",
                f"        self.assertEqual(engine.validate_format('{fmt}'), '{fmt}')",
                "",
            ]
        )
    for score in sorted(SCORE_TYPES):
        lines.extend(
            [
                f"    def test_score_engine_{score}(self) -> None:",
                "        engine = ScoreEngine()",
                f"        self.assertEqual(engine.validate_type('{score}'), '{score}')",
                "",
            ]
        )
    for dash in sorted(DASHBOARD_TYPES):
        lines.extend(
            [
                f"    def test_dashboard_engine_{dash}(self) -> None:",
                "        engine = DashboardEngine()",
                f"        self.assertEqual(engine.validate_type('{dash}'), '{dash}')",
                "",
            ]
        )
    for trend in sorted(TREND_TYPES):
        lines.extend(
            [
                f"    def test_trend_engine_{trend}(self) -> None:",
                "        engine = TrendAnalysisEngine()",
                f"        self.assertEqual(engine.validate_type('{trend}'), '{trend}')",
                "",
            ]
        )
    for fmt in sorted(EXPORT_FORMATS):
        lines.extend(
            [
                f"    def test_export_engine_{fmt}(self) -> None:",
                "        engine = ExportEngine()",
                f"        self.assertEqual(engine.validate_format('{fmt}'), '{fmt}')",
                "",
            ]
        )
    lines.extend(["",])

    lines.extend(
        [
            "class ReleaseProgramLRepositoryTests(LawimTestHarness):",
            "    def test_record_analytics_event(self) -> None:",
            "        row = self.repository.record_analytics_event(event_type='metric_recorded', source_program='crm')",
            "        self.assertEqual(row['event_type'], 'metric_recorded')",
            "",
            "    def test_compute_kpis(self) -> None:",
            "        result = self.repository.compute_kpis()",
            "        self.assertIn('kpis', result)",
            "",
            "    def test_executive_dashboard(self) -> None:",
            "        dashboard = self.repository.executive_dashboard()",
            "        self.assertIn('executive', dashboard)",
            "",
            "    def test_analytics_health(self) -> None:",
            "        health = self.repository.analytics_health()",
            "        self.assertEqual(health['status'], 'healthy')",
            "",
            "    def test_create_analytics_metric(self) -> None:",
            "        row = self.repository.create_analytics_metric(name='Repo Metric')",
            "        self.assertEqual(row['name'], 'Repo Metric')",
            "",
            "    def test_run_report(self) -> None:",
            "        report = self.repository.create_report(name='Repo Report')",
            "        output = self.repository.run_report(int(report['id']))",
            "        self.assertIn('format', output)",
            "",
            "    def test_run_export(self) -> None:",
            "        export = self.repository.create_export(name='Repo Export')",
            "        output = self.repository.run_export(int(export['id']))",
            "        self.assertIn('format', output)",
            "",
        ]
    )
    for source_key, program, source_type in ANALYTIC_SOURCES:
        safe = source_key.replace("-", "_")
        lines.extend(
            [
                f"    def test_source_{safe}(self) -> None:",
                "        sources = self.repository.analytics_integration_sources()",
                f"        keys = {{item['source_key'] for item in sources['sources']}}",
                f"        self.assertIn('{source_key}', keys)",
                "",
            ]
        )
    lines.extend(["",])

    api_routes = [
        "/api/v2/analytics/health",
        "/api/v2/analytics/integrations",
        "/api/v2/analytics/events",
        "/api/v2/analytics/metrics",
        "/api/v2/analytics/kpis",
        "/api/v2/analytics/dashboards",
        "/api/v2/analytics/reports",
        "/api/v2/analytics/bi",
        "/api/v2/analytics/datamarts",
        "/api/v2/analytics/trends",
        "/api/v2/analytics/scores",
        "/api/v2/analytics/realtime",
        "/api/v2/analytics/exports",
        "/api/v2/analytics/ai",
        "/api/v2/analytics/executive",
        "/api/v2/analytics/dashboard",
        "/api/v2/analytics/statistics",
    ]
    lines.append("class ReleaseProgramLApiTests(LawimTestHarness):")
    lines.extend(
        [
            "    def _admin_token(self) -> str:",
            "        return self.login(email='admin@lawim.local')",
            "",
        ]
    )
    for route in api_routes:
        safe = route.replace("/api/v2/analytics/", "") or "root"
        auth = route not in {"/api/v2/analytics/health", "/api/v2/analytics/integrations"}
        if auth:
            lines.extend(
                [
                    f"    def test_get_{safe.replace('/', '_')}(self) -> None:",
                    "        token = self._admin_token()",
                    f"        response = self.invoke('{route}', token=token)",
                    "        self.assertEqual(response.status, HTTPStatus.OK)",
                    "        self.assertIsInstance(response.body_json(), dict)",
                    "",
                ]
            )
        else:
            lines.extend(
                [
                    f"    def test_get_{safe.replace('/', '_')}(self) -> None:",
                    f"        response = self.invoke('{route}')",
                    "        self.assertEqual(response.status, HTTPStatus.OK)",
                    "        self.assertIsInstance(response.body_json(), dict)",
                    "",
                ]
            )
    for route in [
        "/api/v2/analytics/events",
        "/api/v2/analytics/metrics",
        "/api/v2/analytics/reports",
        "/api/v2/analytics/exports",
        "/api/v2/analytics/ai",
        "/api/v2/analytics/kpis",
        "/api/v2/analytics/trends",
        "/api/v2/analytics/scores",
    ]:
        safe = route.split("/")[-1]
        body = (
            {"name": "Test"}
            if safe in {"metrics", "reports", "exports"}
            else {"event_type": "generic"}
            if safe == "events"
            else {}
        )
        lines.extend(
            [
                f"    def test_post_{safe}(self) -> None:",
                "        token = self._admin_token()",
                f"        response = self.invoke('{route}', method='POST', body={body!r}, token=token)",
                "        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})",
                "        self.assertIsInstance(response.body_json(), dict)",
                "",
            ]
        )
    lines.append("")

    lines.extend(
        [
            "class ReleaseProgramLUiTests(LawimTestHarness):",
            "    def test_index_contains_analytics_center(self) -> None:",
            "        html = self.invoke('/')",
            "        self.assertIn('Analytics &amp; BI Center', html.body_text())",
            "",
            "    def test_app_js_references_analytics_api(self) -> None:",
            "        js = self.invoke('/app.js')",
            "        self.assertIn('/api/v2/analytics/statistics', js.body_text())",
            "",
            "    def test_app_js_refresh_analytics_admin(self) -> None:",
            "        js = self.invoke('/app.js')",
            "        self.assertIn('refreshAnalyticsAdmin', js.body_text())",
            "",
            "    def test_index_has_analytics_admin_stats(self) -> None:",
            "        html = self.invoke('/')",
            "        self.assertIn('id=\"analytics-admin-stats\"', html.body_text())",
            "",
            "",
        ]
    )

    lines.extend(
        [
            "class ReleaseProgramLHealthTests(LawimTestHarness):",
            "    def test_migration_profile_v18(self) -> None:",
            "        profile = migration_strategy_profile()",
            "        self.assertEqual(profile['schema_version'], 18)",
            "",
            "    def test_analytics_health_public(self) -> None:",
            "        response = self.invoke('/api/v2/analytics/health')",
            "        self.assertEqual(response.status, HTTPStatus.OK)",
            "        self.assertIn('health', response.body_json())",
            "",
            "    def test_bootstrap_schema_v18(self) -> None:",
            "        bootstrap = self.invoke('/api/bootstrap')",
            "        self.assertEqual(bootstrap.status, HTTPStatus.OK)",
            "        self.assertEqual(self.repository.schema_version(), 18)",
            "",
            "",
        ]
    )

    lines.append("class ReleaseProgramLV18TableTests(LawimTestHarness):")
    for table in V18_TABLE_NAMES:
        lines.extend(
            [
                f"    def test_v18_table_{table}(self) -> None:",
                "        names = {row['name'] for row in self.repository.all(\"SELECT name FROM sqlite_master WHERE type='table'\")}",
                f"        self.assertIn('{table}', names)",
                "",
            ]
        )
    lines.append("")

    lines.append("class ReleaseProgramLIntegrationTests(LawimTestHarness):")
    for program in [
        "intelligent_core",
        "ecosystem",
        "cognition",
        "assistant",
        "knowledge_platform",
        "workflow_automation",
        "real_estate_intelligence",
        "crm",
        "marketplace",
        "security",
        "communication",
    ]:
        lines.extend(
            [
                f"    def test_integration_{program}(self) -> None:",
                "        sources = self.repository.analytics_integration_sources()",
                f"        self.assertIn('{program}', sources['programs'])",
                "",
            ]
        )
    lines.extend(
        [
            "    def test_analytic_sources_count(self) -> None:",
            "        self.assertEqual(len(ANALYTIC_SOURCES), 18)",
            "",
            "    def test_default_kpi_definitions(self) -> None:",
            "        self.assertEqual(len(DEFAULT_KPI_DEFINITIONS), 12)",
            "",
            "",
        ]
    )

    lines.append("class ReleaseProgramLObservabilityTests(LawimTestHarness):")
    lines.extend(
        [
            "    def _admin_token(self) -> str:",
            "        return self.login(email='admin@lawim.local')",
            "",
            "    def test_metrics_endpoint_includes_analytics(self) -> None:",
            "        token = self._admin_token()",
            "        response = self.invoke('/api/metrics', token=token)",
            "        self.assertEqual(response.status, HTTPStatus.OK)",
            "        self.assertIn('analytics_requests_total', response.body_json()['metrics'])",
            "",
        ]
    )
    for name in [
        "analytics_requests_total",
        "analytics_events_total",
        "analytics_metrics_total",
        "analytics_kpi_total",
        "analytics_dashboard_views_total",
        "analytics_report_runs_total",
        "analytics_exports_total",
        "analytics_ai_insights_total",
        "analytics_query_latency_seconds",
        "analytics_aggregation_latency_seconds",
        "analytics_realtime_events_total",
        "analytics_failures_total",
        "bi_queries_total",
        "reporting_outputs_total",
    ]:
        lines.extend(
            [
                f"    def test_metric_{name}(self) -> None:",
                "        token = self._admin_token()",
                "        response = self.invoke('/api/metrics', token=token)",
                f"        self.assertIn('{name}', response.body_json()['metrics'])",
                "",
            ]
        )
    lines.append("")

    lines.extend(
        [
            "class ReleaseProgramLModuleTests(LawimTestHarness):",
            "    def _admin_token(self) -> str:",
            "        return self.login(email='admin@lawim.local')",
            "",
            "    def test_analytics_health_endpoint(self) -> None:",
            "        response = self.invoke('/api/v2/analytics/health')",
            "        self.assertIn('health', response.body_json())",
            "",
            "    def test_analytics_kpi_endpoint(self) -> None:",
            "        token = self._admin_token()",
            "        response = self.invoke('/api/v2/analytics/kpis', token=token)",
            "        self.assertIn('kpis', response.body_json())",
            "",
            "    def test_analytics_dashboard_endpoint(self) -> None:",
            "        token = self._admin_token()",
            "        response = self.invoke('/api/v2/analytics/dashboards', token=token)",
            "        self.assertIn('dashboards', response.body_json())",
            "",
            "    def test_analytics_reporting_endpoint(self) -> None:",
            "        token = self._admin_token()",
            "        response = self.invoke('/api/v2/analytics/reports', token=token)",
            "        self.assertIn('reports', response.body_json())",
            "",
            "    def test_analytics_bi_endpoint(self) -> None:",
            "        token = self._admin_token()",
            "        response = self.invoke('/api/v2/analytics/bi', token=token)",
            "        self.assertIn('bi', response.body_json())",
            "",
            "    def test_analytics_trends_endpoint(self) -> None:",
            "        token = self._admin_token()",
            "        response = self.invoke('/api/v2/analytics/trends', token=token)",
            "        self.assertIn('trends', response.body_json())",
            "",
            "    def test_analytics_scores_endpoint(self) -> None:",
            "        token = self._admin_token()",
            "        response = self.invoke('/api/v2/analytics/scores', token=token)",
            "        self.assertIn('scores', response.body_json())",
            "",
            "    def test_analytics_realtime_endpoint(self) -> None:",
            "        token = self._admin_token()",
            "        response = self.invoke('/api/v2/analytics/realtime', token=token)",
            "        self.assertIn('realtime', response.body_json())",
            "",
            "    def test_analytics_exports_endpoint(self) -> None:",
            "        token = self._admin_token()",
            "        response = self.invoke('/api/v2/analytics/exports', token=token)",
            "        self.assertIn('exports', response.body_json())",
            "",
            "    def test_analytics_ai_endpoint(self) -> None:",
            "        token = self._admin_token()",
            "        response = self.invoke('/api/v2/analytics/ai', token=token)",
            "        self.assertIn('insights', response.body_json())",
            "",
            "    def test_analytics_integrations_endpoint(self) -> None:",
            "        response = self.invoke('/api/v2/analytics/integrations')",
            "        self.assertIn('programs', response.body_json())",
            "",
        ]
    )

    lines.append("class ReleaseProgramLCatalogTests(LawimTestHarness):")
    for kpi_key, name, category, source in DEFAULT_KPI_DEFINITIONS:
        safe = kpi_key.replace("-", "_")
        lines.extend(
            [
                f"    def test_default_kpi_{safe}(self) -> None:",
                "        rows = self.repository.list_kpi_definitions()",
                f"        keys = {{row['kpi_key'] for row in rows}}",
                f"        self.assertIn('{kpi_key}', keys)",
                "",
            ]
        )
    for dash_key, name, dash_type in DEFAULT_DASHBOARDS:
        safe = dash_key.replace("-", "_")
        lines.extend(
            [
                f"    def test_default_dashboard_{safe}(self) -> None:",
                "        rows = self.repository.list_dashboards()",
                f"        keys = {{row['dashboard_key'] for row in rows}}",
                f"        self.assertIn('{dash_key}', keys)",
                "",
            ]
        )
    for mart_key, name, mart_type in DEFAULT_DATA_MARTS:
        safe = mart_key.replace("-", "_")
        lines.extend(
            [
                f"    def test_default_mart_{safe}(self) -> None:",
                "        rows = self.repository.list_data_marts()",
                f"        keys = {{row['mart_key'] for row in rows}}",
                f"        self.assertIn('{mart_key}', keys)",
                "",
            ]
        )
    for score_key, name, score_type, source in DEFAULT_SCORE_DEFINITIONS:
        safe = score_key.replace("-", "_")
        lines.extend(
            [
                f"    def test_default_score_{safe}(self) -> None:",
                "        rows = self.repository.all('SELECT score_key FROM analytics_score_definitions')",
                f"        keys = {{row['score_key'] for row in rows}}",
                f"        self.assertIn('{score_key}', keys)",
                "",
            ]
        )

    out = Path("tests/test_release_program_l.py")
    out.write_text("\n".join(lines))
    count = sum(1 for line in lines if line.strip().startswith("def test_"))
    print(f"Wrote {out} with {count} tests")


if __name__ == "__main__":
    main()
