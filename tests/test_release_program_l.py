from __future__ import annotations

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


class ReleaseProgramLPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v18(self) -> None:
        self.assertEqual(self.repository.schema_version(), 19)

    def test_application_schema_version_constant(self) -> None:
        self.assertEqual(APPLICATION_SCHEMA_VERSION, 19)

    def test_analytics_tables_present(self) -> None:
        self.assertTrue(self.repository.analytics_tables_present())

    def test_all_v18_tables_exist(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V18_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v17_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V17_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v16_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V16_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v15_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V15_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v14_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V14_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v13_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V13_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v12_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V12_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v11_tables_still_present(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V11_TABLE_NAMES:
            self.assertIn(table, names)

    def test_analytics_catalog_seeded(self) -> None:
        self.assertGreaterEqual(self.repository.scalar('SELECT COUNT(*) FROM analytics_kpi_definitions'), 1)
        self.assertGreaterEqual(self.repository.scalar('SELECT COUNT(*) FROM analytics_dashboards'), 1)

    def test_v17_to_v18_legacy_migration(self) -> None:
        db_path = Path(tempfile.mkdtemp()) / 'v17.sqlite3'
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute('PRAGMA foreign_keys = OFF')
        for table in V18_TABLE_NAMES:
            conn.execute(f'DROP TABLE IF EXISTS {table}')
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute("UPDATE schema_meta SET value='17' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn('analytics_events', names)
        for table in V17_TABLE_NAMES:
            self.assertIn(table, names)

    def test_seed_analytics_catalog_idempotent(self) -> None:
        before = self.repository.scalar('SELECT COUNT(*) FROM analytics_kpi_definitions')
        self.repository.seed_analytics_catalog()
        after = self.repository.scalar('SELECT COUNT(*) FROM analytics_kpi_definitions')
        self.assertEqual(before, after)


class ReleaseProgramLConstantsTests(LawimTestHarness):
    def test_event_types_aggregation_completed(self) -> None:
        self.assertIn('aggregation_completed', EVENT_TYPES)

    def test_event_types_anomaly_detected(self) -> None:
        self.assertIn('anomaly_detected', EVENT_TYPES)

    def test_event_types_dashboard_viewed(self) -> None:
        self.assertIn('dashboard_viewed', EVENT_TYPES)

    def test_event_types_export_completed(self) -> None:
        self.assertIn('export_completed', EVENT_TYPES)

    def test_event_types_generic(self) -> None:
        self.assertIn('generic', EVENT_TYPES)

    def test_event_types_insight_generated(self) -> None:
        self.assertIn('insight_generated', EVENT_TYPES)

    def test_event_types_kpi_computed(self) -> None:
        self.assertIn('kpi_computed', EVENT_TYPES)

    def test_event_types_metric_recorded(self) -> None:
        self.assertIn('metric_recorded', EVENT_TYPES)

    def test_event_types_report_generated(self) -> None:
        self.assertIn('report_generated', EVENT_TYPES)

    def test_event_types_score_updated(self) -> None:
        self.assertIn('score_updated', EVENT_TYPES)

    def test_metric_categories_activity(self) -> None:
        self.assertIn('activity', METRIC_CATEGORIES)

    def test_metric_categories_assistant(self) -> None:
        self.assertIn('assistant', METRIC_CATEGORIES)

    def test_metric_categories_cognition(self) -> None:
        self.assertIn('cognition', METRIC_CATEGORIES)

    def test_metric_categories_commercial(self) -> None:
        self.assertIn('commercial', METRIC_CATEGORIES)

    def test_metric_categories_communication(self) -> None:
        self.assertIn('communication', METRIC_CATEGORIES)

    def test_metric_categories_crm(self) -> None:
        self.assertIn('crm', METRIC_CATEGORIES)

    def test_metric_categories_ecosystem(self) -> None:
        self.assertIn('ecosystem', METRIC_CATEGORIES)

    def test_metric_categories_financial(self) -> None:
        self.assertIn('financial', METRIC_CATEGORIES)

    def test_metric_categories_general(self) -> None:
        self.assertIn('general', METRIC_CATEGORIES)

    def test_metric_categories_infrastructure(self) -> None:
        self.assertIn('infrastructure', METRIC_CATEGORIES)

    def test_metric_categories_knowledge(self) -> None:
        self.assertIn('knowledge', METRIC_CATEGORIES)

    def test_metric_categories_marketplace(self) -> None:
        self.assertIn('marketplace', METRIC_CATEGORIES)

    def test_metric_categories_performance(self) -> None:
        self.assertIn('performance', METRIC_CATEGORIES)

    def test_metric_categories_quality(self) -> None:
        self.assertIn('quality', METRIC_CATEGORIES)

    def test_metric_categories_rei(self) -> None:
        self.assertIn('rei', METRIC_CATEGORIES)

    def test_metric_categories_security(self) -> None:
        self.assertIn('security', METRIC_CATEGORIES)

    def test_metric_categories_users(self) -> None:
        self.assertIn('users', METRIC_CATEGORIES)

    def test_metric_categories_workflow(self) -> None:
        self.assertIn('workflow', METRIC_CATEGORIES)

    def test_kpi_categories_activity(self) -> None:
        self.assertIn('activity', KPI_CATEGORIES)

    def test_kpi_categories_assistant(self) -> None:
        self.assertIn('assistant', KPI_CATEGORIES)

    def test_kpi_categories_cognition(self) -> None:
        self.assertIn('cognition', KPI_CATEGORIES)

    def test_kpi_categories_commercial(self) -> None:
        self.assertIn('commercial', KPI_CATEGORIES)

    def test_kpi_categories_communication(self) -> None:
        self.assertIn('communication', KPI_CATEGORIES)

    def test_kpi_categories_crm(self) -> None:
        self.assertIn('crm', KPI_CATEGORIES)

    def test_kpi_categories_ecosystem(self) -> None:
        self.assertIn('ecosystem', KPI_CATEGORIES)

    def test_kpi_categories_executive(self) -> None:
        self.assertIn('executive', KPI_CATEGORIES)

    def test_kpi_categories_financial(self) -> None:
        self.assertIn('financial', KPI_CATEGORIES)

    def test_kpi_categories_infrastructure(self) -> None:
        self.assertIn('infrastructure', KPI_CATEGORIES)

    def test_kpi_categories_knowledge(self) -> None:
        self.assertIn('knowledge', KPI_CATEGORIES)

    def test_kpi_categories_marketplace(self) -> None:
        self.assertIn('marketplace', KPI_CATEGORIES)

    def test_kpi_categories_performance(self) -> None:
        self.assertIn('performance', KPI_CATEGORIES)

    def test_kpi_categories_quality(self) -> None:
        self.assertIn('quality', KPI_CATEGORIES)

    def test_kpi_categories_rei(self) -> None:
        self.assertIn('rei', KPI_CATEGORIES)

    def test_kpi_categories_security(self) -> None:
        self.assertIn('security', KPI_CATEGORIES)

    def test_kpi_categories_users(self) -> None:
        self.assertIn('users', KPI_CATEGORIES)

    def test_kpi_categories_workflow(self) -> None:
        self.assertIn('workflow', KPI_CATEGORIES)

    def test_dashboard_types_administrator(self) -> None:
        self.assertIn('administrator', DASHBOARD_TYPES)

    def test_dashboard_types_ai(self) -> None:
        self.assertIn('ai', DASHBOARD_TYPES)

    def test_dashboard_types_communication(self) -> None:
        self.assertIn('communication', DASHBOARD_TYPES)

    def test_dashboard_types_crm(self) -> None:
        self.assertIn('crm', DASHBOARD_TYPES)

    def test_dashboard_types_custom(self) -> None:
        self.assertIn('custom', DASHBOARD_TYPES)

    def test_dashboard_types_executive(self) -> None:
        self.assertIn('executive', DASHBOARD_TYPES)

    def test_dashboard_types_global(self) -> None:
        self.assertIn('global', DASHBOARD_TYPES)

    def test_dashboard_types_marketplace(self) -> None:
        self.assertIn('marketplace', DASHBOARD_TYPES)

    def test_dashboard_types_rag(self) -> None:
        self.assertIn('rag', DASHBOARD_TYPES)

    def test_dashboard_types_realtime(self) -> None:
        self.assertIn('realtime', DASHBOARD_TYPES)

    def test_dashboard_types_rei(self) -> None:
        self.assertIn('rei', DASHBOARD_TYPES)

    def test_dashboard_types_security(self) -> None:
        self.assertIn('security', DASHBOARD_TYPES)

    def test_dashboard_types_workflow(self) -> None:
        self.assertIn('workflow', DASHBOARD_TYPES)

    def test_report_formats_csv(self) -> None:
        self.assertIn('csv', REPORT_FORMATS)

    def test_report_formats_excel(self) -> None:
        self.assertIn('excel', REPORT_FORMATS)

    def test_report_formats_html(self) -> None:
        self.assertIn('html', REPORT_FORMATS)

    def test_report_formats_json(self) -> None:
        self.assertIn('json', REPORT_FORMATS)

    def test_report_formats_pdf(self) -> None:
        self.assertIn('pdf', REPORT_FORMATS)

    def test_report_formats_xml(self) -> None:
        self.assertIn('xml', REPORT_FORMATS)

    def test_export_formats_csv(self) -> None:
        self.assertIn('csv', EXPORT_FORMATS)

    def test_export_formats_excel(self) -> None:
        self.assertIn('excel', EXPORT_FORMATS)

    def test_export_formats_html(self) -> None:
        self.assertIn('html', EXPORT_FORMATS)

    def test_export_formats_json(self) -> None:
        self.assertIn('json', EXPORT_FORMATS)

    def test_export_formats_pdf(self) -> None:
        self.assertIn('pdf', EXPORT_FORMATS)

    def test_export_formats_xml(self) -> None:
        self.assertIn('xml', EXPORT_FORMATS)

    def test_report_statuses_archived(self) -> None:
        self.assertIn('archived', REPORT_STATUSES)

    def test_report_statuses_cancelled(self) -> None:
        self.assertIn('cancelled', REPORT_STATUSES)

    def test_report_statuses_completed(self) -> None:
        self.assertIn('completed', REPORT_STATUSES)

    def test_report_statuses_draft(self) -> None:
        self.assertIn('draft', REPORT_STATUSES)

    def test_report_statuses_failed(self) -> None:
        self.assertIn('failed', REPORT_STATUSES)

    def test_report_statuses_pending(self) -> None:
        self.assertIn('pending', REPORT_STATUSES)

    def test_report_statuses_running(self) -> None:
        self.assertIn('running', REPORT_STATUSES)

    def test_aggregation_types_avg(self) -> None:
        self.assertIn('avg', AGGREGATION_TYPES)

    def test_aggregation_types_count(self) -> None:
        self.assertIn('count', AGGREGATION_TYPES)

    def test_aggregation_types_max(self) -> None:
        self.assertIn('max', AGGREGATION_TYPES)

    def test_aggregation_types_median(self) -> None:
        self.assertIn('median', AGGREGATION_TYPES)

    def test_aggregation_types_min(self) -> None:
        self.assertIn('min', AGGREGATION_TYPES)

    def test_aggregation_types_percentile(self) -> None:
        self.assertIn('percentile', AGGREGATION_TYPES)

    def test_aggregation_types_rate(self) -> None:
        self.assertIn('rate', AGGREGATION_TYPES)

    def test_aggregation_types_sum(self) -> None:
        self.assertIn('sum', AGGREGATION_TYPES)

    def test_trend_types_exponential(self) -> None:
        self.assertIn('exponential', TREND_TYPES)

    def test_trend_types_linear(self) -> None:
        self.assertIn('linear', TREND_TYPES)

    def test_trend_types_moving_average(self) -> None:
        self.assertIn('moving_average', TREND_TYPES)

    def test_trend_types_regression(self) -> None:
        self.assertIn('regression', TREND_TYPES)

    def test_trend_types_seasonal(self) -> None:
        self.assertIn('seasonal', TREND_TYPES)

    def test_score_types_ai_confidence(self) -> None:
        self.assertIn('ai_confidence', SCORE_TYPES)

    def test_score_types_communication(self) -> None:
        self.assertIn('communication', SCORE_TYPES)

    def test_score_types_customer(self) -> None:
        self.assertIn('customer', SCORE_TYPES)

    def test_score_types_knowledge(self) -> None:
        self.assertIn('knowledge', SCORE_TYPES)

    def test_score_types_partner(self) -> None:
        self.assertIn('partner', SCORE_TYPES)

    def test_score_types_platform_health(self) -> None:
        self.assertIn('platform_health', SCORE_TYPES)

    def test_score_types_property(self) -> None:
        self.assertIn('property', SCORE_TYPES)

    def test_score_types_provider(self) -> None:
        self.assertIn('provider', SCORE_TYPES)

    def test_score_types_security(self) -> None:
        self.assertIn('security', SCORE_TYPES)

    def test_score_types_workflow(self) -> None:
        self.assertIn('workflow', SCORE_TYPES)

    def test_data_mart_types_assistant(self) -> None:
        self.assertIn('assistant', DATA_MART_TYPES)

    def test_data_mart_types_communication(self) -> None:
        self.assertIn('communication', DATA_MART_TYPES)

    def test_data_mart_types_crm(self) -> None:
        self.assertIn('crm', DATA_MART_TYPES)

    def test_data_mart_types_global(self) -> None:
        self.assertIn('global', DATA_MART_TYPES)

    def test_data_mart_types_knowledge(self) -> None:
        self.assertIn('knowledge', DATA_MART_TYPES)

    def test_data_mart_types_marketplace(self) -> None:
        self.assertIn('marketplace', DATA_MART_TYPES)

    def test_data_mart_types_rei(self) -> None:
        self.assertIn('rei', DATA_MART_TYPES)

    def test_data_mart_types_security(self) -> None:
        self.assertIn('security', DATA_MART_TYPES)

    def test_data_mart_types_workflow(self) -> None:
        self.assertIn('workflow', DATA_MART_TYPES)

    def test_insight_types_anomaly(self) -> None:
        self.assertIn('anomaly', INSIGHT_TYPES)

    def test_insight_types_explanation(self) -> None:
        self.assertIn('explanation', INSIGHT_TYPES)

    def test_insight_types_forecast(self) -> None:
        self.assertIn('forecast', INSIGHT_TYPES)

    def test_insight_types_prioritization(self) -> None:
        self.assertIn('prioritization', INSIGHT_TYPES)

    def test_insight_types_recommendation(self) -> None:
        self.assertIn('recommendation', INSIGHT_TYPES)

    def test_insight_types_segmentation(self) -> None:
        self.assertIn('segmentation', INSIGHT_TYPES)

    def test_insight_types_summary(self) -> None:
        self.assertIn('summary', INSIGHT_TYPES)

    def test_insight_types_trend(self) -> None:
        self.assertIn('trend', INSIGHT_TYPES)

    def test_program_codes_assistant(self) -> None:
        self.assertIn('assistant', PROGRAM_CODES)

    def test_program_codes_cognition(self) -> None:
        self.assertIn('cognition', PROGRAM_CODES)

    def test_program_codes_communication(self) -> None:
        self.assertIn('communication', PROGRAM_CODES)

    def test_program_codes_crm(self) -> None:
        self.assertIn('crm', PROGRAM_CODES)

    def test_program_codes_ecosystem(self) -> None:
        self.assertIn('ecosystem', PROGRAM_CODES)

    def test_program_codes_global(self) -> None:
        self.assertIn('global', PROGRAM_CODES)

    def test_program_codes_intelligent_core(self) -> None:
        self.assertIn('intelligent_core', PROGRAM_CODES)

    def test_program_codes_knowledge(self) -> None:
        self.assertIn('knowledge', PROGRAM_CODES)

    def test_program_codes_marketplace(self) -> None:
        self.assertIn('marketplace', PROGRAM_CODES)

    def test_program_codes_observability(self) -> None:
        self.assertIn('observability', PROGRAM_CODES)

    def test_program_codes_rei(self) -> None:
        self.assertIn('rei', PROGRAM_CODES)

    def test_program_codes_security(self) -> None:
        self.assertIn('security', PROGRAM_CODES)

    def test_program_codes_workflow(self) -> None:
        self.assertIn('workflow', PROGRAM_CODES)


class ReleaseProgramLEnginesTests(LawimTestHarness):
    def test_analytics_engine_validate_event(self) -> None:
        engine = AnalyticsEngine()
        self.assertEqual(engine.validate_event_type('kpi_computed'), 'kpi_computed')

    def test_aggregation_engine_sum(self) -> None:
        engine = AnalyticsAggregationEngine()
        self.assertEqual(engine.aggregate([1, 2, 3], 'sum'), 6.0)

    def test_query_engine_execute(self) -> None:
        engine = AnalyticsQueryEngine()
        q = engine.build_query(name='test')
        result = engine.execute(q, [{'a': 1}])
        self.assertEqual(result['row_count'], 1)

    def test_reporting_engine_pdf_architecture(self) -> None:
        engine = ReportingEngine()
        out = engine.generate_output(report_type='x', data={}, fmt='pdf')
        self.assertTrue(out['architecture_only'])

    def test_trend_anomalies(self) -> None:
        engine = TrendAnalysisEngine()
        anomalies = engine.detect_anomalies([1, 1, 1, 1, 1, 50], threshold=1.5)
        self.assertTrue(anomalies)

    def test_ai_engine_insight(self) -> None:
        engine = AiAnalyticsEngine()
        insight = engine.generate_insight(insight_type='trend', title='T', content={})
        self.assertTrue(insight['traceable'])

    def test_platform_engine_catalog(self) -> None:
        engine = AnalyticsPlatformEngine()
        self.assertGreater(len(engine.integration_catalog()), 10)

    def test_aggregation_engine_avg(self) -> None:
        engine = AnalyticsAggregationEngine()
        self.assertEqual(engine.validate_type('avg'), 'avg')

    def test_aggregation_engine_count(self) -> None:
        engine = AnalyticsAggregationEngine()
        self.assertEqual(engine.validate_type('count'), 'count')

    def test_aggregation_engine_max(self) -> None:
        engine = AnalyticsAggregationEngine()
        self.assertEqual(engine.validate_type('max'), 'max')

    def test_aggregation_engine_median(self) -> None:
        engine = AnalyticsAggregationEngine()
        self.assertEqual(engine.validate_type('median'), 'median')

    def test_aggregation_engine_min(self) -> None:
        engine = AnalyticsAggregationEngine()
        self.assertEqual(engine.validate_type('min'), 'min')

    def test_aggregation_engine_percentile(self) -> None:
        engine = AnalyticsAggregationEngine()
        self.assertEqual(engine.validate_type('percentile'), 'percentile')

    def test_aggregation_engine_rate(self) -> None:
        engine = AnalyticsAggregationEngine()
        self.assertEqual(engine.validate_type('rate'), 'rate')

    def test_aggregation_engine_sum(self) -> None:
        engine = AnalyticsAggregationEngine()
        self.assertEqual(engine.validate_type('sum'), 'sum')

    def test_reporting_engine_csv(self) -> None:
        engine = ReportingEngine()
        self.assertEqual(engine.validate_format('csv'), 'csv')

    def test_reporting_engine_excel(self) -> None:
        engine = ReportingEngine()
        self.assertEqual(engine.validate_format('excel'), 'excel')

    def test_reporting_engine_html(self) -> None:
        engine = ReportingEngine()
        self.assertEqual(engine.validate_format('html'), 'html')

    def test_reporting_engine_json(self) -> None:
        engine = ReportingEngine()
        self.assertEqual(engine.validate_format('json'), 'json')

    def test_reporting_engine_pdf(self) -> None:
        engine = ReportingEngine()
        self.assertEqual(engine.validate_format('pdf'), 'pdf')

    def test_reporting_engine_xml(self) -> None:
        engine = ReportingEngine()
        self.assertEqual(engine.validate_format('xml'), 'xml')

    def test_score_engine_ai_confidence(self) -> None:
        engine = ScoreEngine()
        self.assertEqual(engine.validate_type('ai_confidence'), 'ai_confidence')

    def test_score_engine_communication(self) -> None:
        engine = ScoreEngine()
        self.assertEqual(engine.validate_type('communication'), 'communication')

    def test_score_engine_customer(self) -> None:
        engine = ScoreEngine()
        self.assertEqual(engine.validate_type('customer'), 'customer')

    def test_score_engine_knowledge(self) -> None:
        engine = ScoreEngine()
        self.assertEqual(engine.validate_type('knowledge'), 'knowledge')

    def test_score_engine_partner(self) -> None:
        engine = ScoreEngine()
        self.assertEqual(engine.validate_type('partner'), 'partner')

    def test_score_engine_platform_health(self) -> None:
        engine = ScoreEngine()
        self.assertEqual(engine.validate_type('platform_health'), 'platform_health')

    def test_score_engine_property(self) -> None:
        engine = ScoreEngine()
        self.assertEqual(engine.validate_type('property'), 'property')

    def test_score_engine_provider(self) -> None:
        engine = ScoreEngine()
        self.assertEqual(engine.validate_type('provider'), 'provider')

    def test_score_engine_security(self) -> None:
        engine = ScoreEngine()
        self.assertEqual(engine.validate_type('security'), 'security')

    def test_score_engine_workflow(self) -> None:
        engine = ScoreEngine()
        self.assertEqual(engine.validate_type('workflow'), 'workflow')

    def test_dashboard_engine_administrator(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('administrator'), 'administrator')

    def test_dashboard_engine_ai(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('ai'), 'ai')

    def test_dashboard_engine_communication(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('communication'), 'communication')

    def test_dashboard_engine_crm(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('crm'), 'crm')

    def test_dashboard_engine_custom(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('custom'), 'custom')

    def test_dashboard_engine_executive(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('executive'), 'executive')

    def test_dashboard_engine_global(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('global'), 'global')

    def test_dashboard_engine_marketplace(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('marketplace'), 'marketplace')

    def test_dashboard_engine_rag(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('rag'), 'rag')

    def test_dashboard_engine_realtime(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('realtime'), 'realtime')

    def test_dashboard_engine_rei(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('rei'), 'rei')

    def test_dashboard_engine_security(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('security'), 'security')

    def test_dashboard_engine_workflow(self) -> None:
        engine = DashboardEngine()
        self.assertEqual(engine.validate_type('workflow'), 'workflow')

    def test_trend_engine_exponential(self) -> None:
        engine = TrendAnalysisEngine()
        self.assertEqual(engine.validate_type('exponential'), 'exponential')

    def test_trend_engine_linear(self) -> None:
        engine = TrendAnalysisEngine()
        self.assertEqual(engine.validate_type('linear'), 'linear')

    def test_trend_engine_moving_average(self) -> None:
        engine = TrendAnalysisEngine()
        self.assertEqual(engine.validate_type('moving_average'), 'moving_average')

    def test_trend_engine_regression(self) -> None:
        engine = TrendAnalysisEngine()
        self.assertEqual(engine.validate_type('regression'), 'regression')

    def test_trend_engine_seasonal(self) -> None:
        engine = TrendAnalysisEngine()
        self.assertEqual(engine.validate_type('seasonal'), 'seasonal')

    def test_export_engine_csv(self) -> None:
        engine = ExportEngine()
        self.assertEqual(engine.validate_format('csv'), 'csv')

    def test_export_engine_excel(self) -> None:
        engine = ExportEngine()
        self.assertEqual(engine.validate_format('excel'), 'excel')

    def test_export_engine_html(self) -> None:
        engine = ExportEngine()
        self.assertEqual(engine.validate_format('html'), 'html')

    def test_export_engine_json(self) -> None:
        engine = ExportEngine()
        self.assertEqual(engine.validate_format('json'), 'json')

    def test_export_engine_pdf(self) -> None:
        engine = ExportEngine()
        self.assertEqual(engine.validate_format('pdf'), 'pdf')

    def test_export_engine_xml(self) -> None:
        engine = ExportEngine()
        self.assertEqual(engine.validate_format('xml'), 'xml')


class ReleaseProgramLRepositoryTests(LawimTestHarness):
    def test_record_analytics_event(self) -> None:
        row = self.repository.record_analytics_event(event_type='metric_recorded', source_program='crm')
        self.assertEqual(row['event_type'], 'metric_recorded')

    def test_compute_kpis(self) -> None:
        result = self.repository.compute_kpis()
        self.assertIn('kpis', result)

    def test_executive_dashboard(self) -> None:
        dashboard = self.repository.executive_dashboard()
        self.assertIn('executive', dashboard)

    def test_analytics_health(self) -> None:
        health = self.repository.analytics_health()
        self.assertEqual(health['status'], 'healthy')

    def test_create_analytics_metric(self) -> None:
        row = self.repository.create_analytics_metric(name='Repo Metric')
        self.assertEqual(row['name'], 'Repo Metric')

    def test_run_report(self) -> None:
        report = self.repository.create_report(name='Repo Report')
        output = self.repository.run_report(int(report['id']))
        self.assertIn('format', output)

    def test_run_export(self) -> None:
        export = self.repository.create_export(name='Repo Export')
        output = self.repository.run_export(int(export['id']))
        self.assertIn('format', output)

    def test_source_crm_metrics(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('crm_metrics', keys)

    def test_source_marketplace_metrics(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('marketplace_metrics', keys)

    def test_source_communication_metrics(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('communication_metrics', keys)

    def test_source_security_metrics(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('security_metrics', keys)

    def test_source_workflow_metrics(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('workflow_metrics', keys)

    def test_source_rei_metrics(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('rei_metrics', keys)

    def test_source_knowledge_metrics(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('knowledge_metrics', keys)

    def test_source_assistant_metrics(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('assistant_metrics', keys)

    def test_source_cognition_metrics(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('cognition_metrics', keys)

    def test_source_ecosystem_metrics(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('ecosystem_metrics', keys)

    def test_source_observability_metrics(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('observability_metrics', keys)

    def test_source_audit_events(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('audit_events', keys)

    def test_source_notification_events(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('notification_events', keys)

    def test_source_workflow_events(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('workflow_events', keys)

    def test_source_marketplace_events(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('marketplace_events', keys)

    def test_source_crm_events(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('crm_events', keys)

    def test_source_security_events(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('security_events', keys)

    def test_source_communication_events(self) -> None:
        sources = self.repository.analytics_integration_sources()
        keys = {item['source_key'] for item in sources['sources']}
        self.assertIn('communication_events', keys)


class ReleaseProgramLApiTests(LawimTestHarness):
    def _admin_token(self) -> str:
        return self.login(email='admin@lawim.local')

    def test_get_health(self) -> None:
        response = self.invoke('/api/v2/analytics/health')
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_integrations(self) -> None:
        response = self.invoke('/api/v2/analytics/integrations')
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_events(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/events', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_metrics(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/metrics', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_kpis(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/kpis', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_dashboards(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/dashboards', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_reports(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/reports', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_bi(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/bi', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_datamarts(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/datamarts', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_trends(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/trends', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_scores(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/scores', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_realtime(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/realtime', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_exports(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/exports', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_ai(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/ai', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_executive(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/executive', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_dashboard(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/dashboard', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_get_statistics(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/statistics', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIsInstance(response.body_json(), dict)

    def test_post_events(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/events', method='POST', body={'event_type': 'generic'}, token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIsInstance(response.body_json(), dict)

    def test_post_metrics(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/metrics', method='POST', body={'name': 'Test'}, token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIsInstance(response.body_json(), dict)

    def test_post_reports(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/reports', method='POST', body={'name': 'Test'}, token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIsInstance(response.body_json(), dict)

    def test_post_exports(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/exports', method='POST', body={'name': 'Test'}, token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIsInstance(response.body_json(), dict)

    def test_post_ai(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/ai', method='POST', body={}, token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIsInstance(response.body_json(), dict)

    def test_post_kpis(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/kpis', method='POST', body={}, token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIsInstance(response.body_json(), dict)

    def test_post_trends(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/trends', method='POST', body={}, token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIsInstance(response.body_json(), dict)

    def test_post_scores(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/scores', method='POST', body={}, token=token)
        self.assertIn(response.status, {HTTPStatus.OK, HTTPStatus.CREATED})
        self.assertIsInstance(response.body_json(), dict)


class ReleaseProgramLUiTests(LawimTestHarness):
    def test_index_contains_analytics_center(self) -> None:
        html = self.invoke('/')
        self.assertIn('Analytics &amp; BI Center', html.body_text())

    def test_app_js_references_analytics_api(self) -> None:
        js = self.invoke('/app.js')
        self.assertIn('/api/v2/analytics/statistics', js.body_text())

    def test_app_js_refresh_analytics_admin(self) -> None:
        js = self.invoke('/app.js')
        self.assertIn('refreshAnalyticsAdmin', js.body_text())

    def test_index_has_analytics_admin_stats(self) -> None:
        html = self.invoke('/')
        self.assertIn('id="analytics-admin-stats"', html.body_text())


class ReleaseProgramLHealthTests(LawimTestHarness):
    def test_migration_profile_v18(self) -> None:
        profile = migration_strategy_profile()
        self.assertEqual(profile['schema_version'], 19)

    def test_analytics_health_public(self) -> None:
        response = self.invoke('/api/v2/analytics/health')
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn('health', response.body_json())

    def test_bootstrap_schema_v18(self) -> None:
        bootstrap = self.invoke('/api/bootstrap')
        self.assertEqual(bootstrap.status, HTTPStatus.OK)
        self.assertEqual(self.repository.schema_version(), 19)


class ReleaseProgramLV18TableTests(LawimTestHarness):
    def test_v18_table_analytics_events(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_events', names)

    def test_v18_table_analytics_event_sources(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_event_sources', names)

    def test_v18_table_analytics_metrics(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_metrics', names)

    def test_v18_table_analytics_metric_values(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_metric_values', names)

    def test_v18_table_analytics_metric_snapshots(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_metric_snapshots', names)

    def test_v18_table_analytics_aggregations(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_aggregations', names)

    def test_v18_table_analytics_aggregation_results(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_aggregation_results', names)

    def test_v18_table_analytics_dimensions(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_dimensions', names)

    def test_v18_table_analytics_measures(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_measures', names)

    def test_v18_table_analytics_filters(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_filters', names)

    def test_v18_table_analytics_queries(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_queries', names)

    def test_v18_table_analytics_query_results(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_query_results', names)

    def test_v18_table_analytics_kpi_definitions(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_kpi_definitions', names)

    def test_v18_table_analytics_kpi_values(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_kpi_values', names)

    def test_v18_table_analytics_kpi_targets(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_kpi_targets', names)

    def test_v18_table_analytics_kpi_thresholds(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_kpi_thresholds', names)

    def test_v18_table_analytics_kpi_alerts(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_kpi_alerts', names)

    def test_v18_table_analytics_kpi_history(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_kpi_history', names)

    def test_v18_table_analytics_kpi_categories(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_kpi_categories', names)

    def test_v18_table_analytics_dashboards(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_dashboards', names)

    def test_v18_table_analytics_dashboard_widgets(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_dashboard_widgets', names)

    def test_v18_table_analytics_dashboard_layouts(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_dashboard_layouts', names)

    def test_v18_table_analytics_dashboard_filters(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_dashboard_filters', names)

    def test_v18_table_analytics_dashboard_permissions(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_dashboard_permissions', names)

    def test_v18_table_analytics_dashboard_snapshots(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_dashboard_snapshots', names)

    def test_v18_table_analytics_dashboard_exports(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_dashboard_exports', names)

    def test_v18_table_analytics_reports(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_reports', names)

    def test_v18_table_analytics_report_templates(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_report_templates', names)

    def test_v18_table_analytics_report_sections(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_report_sections', names)

    def test_v18_table_analytics_report_runs(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_report_runs', names)

    def test_v18_table_analytics_report_outputs(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_report_outputs', names)

    def test_v18_table_analytics_report_schedules(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_report_schedules', names)

    def test_v18_table_analytics_report_recipients(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_report_recipients', names)

    def test_v18_table_analytics_report_history(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_report_history', names)

    def test_v18_table_bi_dimensions(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('bi_dimensions', names)

    def test_v18_table_bi_measures(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('bi_measures', names)

    def test_v18_table_bi_cubes(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('bi_cubes', names)

    def test_v18_table_bi_cube_dimensions(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('bi_cube_dimensions', names)

    def test_v18_table_bi_cube_measures(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('bi_cube_measures', names)

    def test_v18_table_bi_segments(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('bi_segments', names)

    def test_v18_table_bi_segment_members(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('bi_segment_members', names)

    def test_v18_table_bi_benchmarks(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('bi_benchmarks', names)

    def test_v18_table_bi_drill_paths(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('bi_drill_paths', names)

    def test_v18_table_bi_comparisons(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('bi_comparisons', names)

    def test_v18_table_analytics_data_marts(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_data_marts', names)

    def test_v18_table_analytics_data_mart_sources(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_data_mart_sources', names)

    def test_v18_table_analytics_data_mart_fields(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_data_mart_fields', names)

    def test_v18_table_analytics_data_mart_views(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_data_mart_views', names)

    def test_v18_table_analytics_data_mart_refreshes(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_data_mart_refreshes', names)

    def test_v18_table_analytics_data_mart_permissions(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_data_mart_permissions', names)

    def test_v18_table_analytics_trends(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_trends', names)

    def test_v18_table_analytics_trend_points(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_trend_points', names)

    def test_v18_table_analytics_anomalies(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_anomalies', names)

    def test_v18_table_analytics_forecasts(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_forecasts', names)

    def test_v18_table_analytics_forecast_points(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_forecast_points', names)

    def test_v18_table_analytics_seasonality_profiles(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_seasonality_profiles', names)

    def test_v18_table_analytics_score_definitions(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_score_definitions', names)

    def test_v18_table_analytics_score_values(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_score_values', names)

    def test_v18_table_analytics_score_components(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_score_components', names)

    def test_v18_table_analytics_score_history(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_score_history', names)

    def test_v18_table_analytics_score_rules(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_score_rules', names)

    def test_v18_table_executive_dashboard_snapshots(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('executive_dashboard_snapshots', names)

    def test_v18_table_executive_dashboard_kpis(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('executive_dashboard_kpis', names)

    def test_v18_table_executive_dashboard_alerts(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('executive_dashboard_alerts', names)

    def test_v18_table_executive_dashboard_sections(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('executive_dashboard_sections', names)

    def test_v18_table_realtime_event_streams(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('realtime_event_streams', names)

    def test_v18_table_realtime_counters(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('realtime_counters', names)

    def test_v18_table_realtime_activity_logs(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('realtime_activity_logs', names)

    def test_v18_table_realtime_alerts(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('realtime_alerts', names)

    def test_v18_table_realtime_sessions(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('realtime_sessions', names)

    def test_v18_table_realtime_processing_stats(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('realtime_processing_stats', names)

    def test_v18_table_analytics_exports(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_exports', names)

    def test_v18_table_analytics_export_files(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_export_files', names)

    def test_v18_table_analytics_export_jobs(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_export_jobs', names)

    def test_v18_table_analytics_export_permissions(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_export_permissions', names)

    def test_v18_table_analytics_export_logs(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_export_logs', names)

    def test_v18_table_analytics_ai_insights(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_ai_insights', names)

    def test_v18_table_analytics_ai_recommendations(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_ai_recommendations', names)

    def test_v18_table_analytics_ai_anomaly_reviews(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_ai_anomaly_reviews', names)

    def test_v18_table_analytics_ai_forecasts(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_ai_forecasts', names)

    def test_v18_table_analytics_ai_explanations(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_ai_explanations', names)

    def test_v18_table_analytics_ai_feedback(self) -> None:
        names = {row['name'] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn('analytics_ai_feedback', names)


class ReleaseProgramLIntegrationTests(LawimTestHarness):
    def test_integration_intelligent_core(self) -> None:
        sources = self.repository.analytics_integration_sources()
        self.assertIn('intelligent_core', sources['programs'])

    def test_integration_ecosystem(self) -> None:
        sources = self.repository.analytics_integration_sources()
        self.assertIn('ecosystem', sources['programs'])

    def test_integration_cognition(self) -> None:
        sources = self.repository.analytics_integration_sources()
        self.assertIn('cognition', sources['programs'])

    def test_integration_assistant(self) -> None:
        sources = self.repository.analytics_integration_sources()
        self.assertIn('assistant', sources['programs'])

    def test_integration_knowledge_platform(self) -> None:
        sources = self.repository.analytics_integration_sources()
        self.assertIn('knowledge_platform', sources['programs'])

    def test_integration_workflow_automation(self) -> None:
        sources = self.repository.analytics_integration_sources()
        self.assertIn('workflow_automation', sources['programs'])

    def test_integration_real_estate_intelligence(self) -> None:
        sources = self.repository.analytics_integration_sources()
        self.assertIn('real_estate_intelligence', sources['programs'])

    def test_integration_crm(self) -> None:
        sources = self.repository.analytics_integration_sources()
        self.assertIn('crm', sources['programs'])

    def test_integration_marketplace(self) -> None:
        sources = self.repository.analytics_integration_sources()
        self.assertIn('marketplace', sources['programs'])

    def test_integration_security(self) -> None:
        sources = self.repository.analytics_integration_sources()
        self.assertIn('security', sources['programs'])

    def test_integration_communication(self) -> None:
        sources = self.repository.analytics_integration_sources()
        self.assertIn('communication', sources['programs'])

    def test_analytic_sources_count(self) -> None:
        self.assertEqual(len(ANALYTIC_SOURCES), 18)

    def test_default_kpi_definitions(self) -> None:
        self.assertEqual(len(DEFAULT_KPI_DEFINITIONS), 12)


class ReleaseProgramLObservabilityTests(LawimTestHarness):
    def _admin_token(self) -> str:
        return self.login(email='admin@lawim.local')

    def test_metrics_endpoint_includes_analytics(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn('analytics_requests_total', response.body_json()['metrics'])

    def test_metric_analytics_requests_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_requests_total', response.body_json()['metrics'])

    def test_metric_analytics_events_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_events_total', response.body_json()['metrics'])

    def test_metric_analytics_metrics_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_metrics_total', response.body_json()['metrics'])

    def test_metric_analytics_kpi_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_kpi_total', response.body_json()['metrics'])

    def test_metric_analytics_dashboard_views_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_dashboard_views_total', response.body_json()['metrics'])

    def test_metric_analytics_report_runs_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_report_runs_total', response.body_json()['metrics'])

    def test_metric_analytics_exports_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_exports_total', response.body_json()['metrics'])

    def test_metric_analytics_ai_insights_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_ai_insights_total', response.body_json()['metrics'])

    def test_metric_analytics_query_latency_seconds(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_query_latency_seconds', response.body_json()['metrics'])

    def test_metric_analytics_aggregation_latency_seconds(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_aggregation_latency_seconds', response.body_json()['metrics'])

    def test_metric_analytics_realtime_events_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_realtime_events_total', response.body_json()['metrics'])

    def test_metric_analytics_failures_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('analytics_failures_total', response.body_json()['metrics'])

    def test_metric_bi_queries_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('bi_queries_total', response.body_json()['metrics'])

    def test_metric_reporting_outputs_total(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/metrics', token=token)
        self.assertIn('reporting_outputs_total', response.body_json()['metrics'])


class ReleaseProgramLModuleTests(LawimTestHarness):
    def _admin_token(self) -> str:
        return self.login(email='admin@lawim.local')

    def test_analytics_health_endpoint(self) -> None:
        response = self.invoke('/api/v2/analytics/health')
        self.assertIn('health', response.body_json())

    def test_analytics_kpi_endpoint(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/kpis', token=token)
        self.assertIn('kpis', response.body_json())

    def test_analytics_dashboard_endpoint(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/dashboards', token=token)
        self.assertIn('dashboards', response.body_json())

    def test_analytics_reporting_endpoint(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/reports', token=token)
        self.assertIn('reports', response.body_json())

    def test_analytics_bi_endpoint(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/bi', token=token)
        self.assertIn('bi', response.body_json())

    def test_analytics_trends_endpoint(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/trends', token=token)
        self.assertIn('trends', response.body_json())

    def test_analytics_scores_endpoint(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/scores', token=token)
        self.assertIn('scores', response.body_json())

    def test_analytics_realtime_endpoint(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/realtime', token=token)
        self.assertIn('realtime', response.body_json())

    def test_analytics_exports_endpoint(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/exports', token=token)
        self.assertIn('exports', response.body_json())

    def test_analytics_ai_endpoint(self) -> None:
        token = self._admin_token()
        response = self.invoke('/api/v2/analytics/ai', token=token)
        self.assertIn('insights', response.body_json())

    def test_analytics_integrations_endpoint(self) -> None:
        response = self.invoke('/api/v2/analytics/integrations')
        self.assertIn('programs', response.body_json())

class ReleaseProgramLCatalogTests(LawimTestHarness):
    def test_default_kpi_kpi_crm_leads(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-crm-leads', keys)

    def test_default_kpi_kpi_crm_conversion(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-crm-conversion', keys)

    def test_default_kpi_kpi_marketplace_requests(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-marketplace-requests', keys)

    def test_default_kpi_kpi_workflow_success(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-workflow-success', keys)

    def test_default_kpi_kpi_rei_properties(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-rei-properties', keys)

    def test_default_kpi_kpi_communication_delivery(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-communication-delivery', keys)

    def test_default_kpi_kpi_security_incidents(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-security-incidents', keys)

    def test_default_kpi_kpi_knowledge_queries(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-knowledge-queries', keys)

    def test_default_kpi_kpi_assistant_sessions(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-assistant-sessions', keys)

    def test_default_kpi_kpi_ecosystem_partners(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-ecosystem-partners', keys)

    def test_default_kpi_kpi_platform_health(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-platform-health', keys)

    def test_default_kpi_kpi_user_activity(self) -> None:
        rows = self.repository.list_kpi_definitions()
        keys = {row['kpi_key'] for row in rows}
        self.assertIn('kpi-user-activity', keys)

    def test_default_dashboard_dashboard_executive(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-executive', keys)

    def test_default_dashboard_dashboard_admin(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-admin', keys)

    def test_default_dashboard_dashboard_crm(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-crm', keys)

    def test_default_dashboard_dashboard_marketplace(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-marketplace', keys)

    def test_default_dashboard_dashboard_workflow(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-workflow', keys)

    def test_default_dashboard_dashboard_rei(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-rei', keys)

    def test_default_dashboard_dashboard_security(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-security', keys)

    def test_default_dashboard_dashboard_communication(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-communication', keys)

    def test_default_dashboard_dashboard_ai(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-ai', keys)

    def test_default_dashboard_dashboard_rag(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-rag', keys)

    def test_default_dashboard_dashboard_global(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-global', keys)

    def test_default_dashboard_dashboard_realtime(self) -> None:
        rows = self.repository.list_dashboards()
        keys = {row['dashboard_key'] for row in rows}
        self.assertIn('dashboard-realtime', keys)

    def test_default_mart_mart_crm(self) -> None:
        rows = self.repository.list_data_marts()
        keys = {row['mart_key'] for row in rows}
        self.assertIn('mart-crm', keys)

    def test_default_mart_mart_marketplace(self) -> None:
        rows = self.repository.list_data_marts()
        keys = {row['mart_key'] for row in rows}
        self.assertIn('mart-marketplace', keys)

    def test_default_mart_mart_workflow(self) -> None:
        rows = self.repository.list_data_marts()
        keys = {row['mart_key'] for row in rows}
        self.assertIn('mart-workflow', keys)

    def test_default_mart_mart_communication(self) -> None:
        rows = self.repository.list_data_marts()
        keys = {row['mart_key'] for row in rows}
        self.assertIn('mart-communication', keys)

    def test_default_mart_mart_security(self) -> None:
        rows = self.repository.list_data_marts()
        keys = {row['mart_key'] for row in rows}
        self.assertIn('mart-security', keys)

    def test_default_mart_mart_knowledge(self) -> None:
        rows = self.repository.list_data_marts()
        keys = {row['mart_key'] for row in rows}
        self.assertIn('mart-knowledge', keys)

    def test_default_mart_mart_rei(self) -> None:
        rows = self.repository.list_data_marts()
        keys = {row['mart_key'] for row in rows}
        self.assertIn('mart-rei', keys)

    def test_default_mart_mart_assistant(self) -> None:
        rows = self.repository.list_data_marts()
        keys = {row['mart_key'] for row in rows}
        self.assertIn('mart-assistant', keys)

    def test_default_mart_mart_global(self) -> None:
        rows = self.repository.list_data_marts()
        keys = {row['mart_key'] for row in rows}
        self.assertIn('mart-global', keys)

    def test_default_score_score_customer(self) -> None:
        rows = self.repository.all('SELECT score_key FROM analytics_score_definitions')
        keys = {row['score_key'] for row in rows}
        self.assertIn('score-customer', keys)

    def test_default_score_score_partner(self) -> None:
        rows = self.repository.all('SELECT score_key FROM analytics_score_definitions')
        keys = {row['score_key'] for row in rows}
        self.assertIn('score-partner', keys)

    def test_default_score_score_provider(self) -> None:
        rows = self.repository.all('SELECT score_key FROM analytics_score_definitions')
        keys = {row['score_key'] for row in rows}
        self.assertIn('score-provider', keys)

    def test_default_score_score_property(self) -> None:
        rows = self.repository.all('SELECT score_key FROM analytics_score_definitions')
        keys = {row['score_key'] for row in rows}
        self.assertIn('score-property', keys)

    def test_default_score_score_workflow(self) -> None:
        rows = self.repository.all('SELECT score_key FROM analytics_score_definitions')
        keys = {row['score_key'] for row in rows}
        self.assertIn('score-workflow', keys)

    def test_default_score_score_communication(self) -> None:
        rows = self.repository.all('SELECT score_key FROM analytics_score_definitions')
        keys = {row['score_key'] for row in rows}
        self.assertIn('score-communication', keys)

    def test_default_score_score_security(self) -> None:
        rows = self.repository.all('SELECT score_key FROM analytics_score_definitions')
        keys = {row['score_key'] for row in rows}
        self.assertIn('score-security', keys)

    def test_default_score_score_knowledge(self) -> None:
        rows = self.repository.all('SELECT score_key FROM analytics_score_definitions')
        keys = {row['score_key'] for row in rows}
        self.assertIn('score-knowledge', keys)

    def test_default_score_score_ai_confidence(self) -> None:
        rows = self.repository.all('SELECT score_key FROM analytics_score_definitions')
        keys = {row['score_key'] for row in rows}
        self.assertIn('score-ai-confidence', keys)

    def test_default_score_score_platform_health(self) -> None:
        rows = self.repository.all('SELECT score_key FROM analytics_score_definitions')
        keys = {row['score_key'] for row in rows}
        self.assertIn('score-platform-health', keys)
