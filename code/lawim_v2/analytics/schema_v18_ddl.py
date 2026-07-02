"""Schema v18 DDL — Analytics BI Reporting platform (RELEASE PROGRAM L)."""

V18_TABLE_NAMES: tuple[str, ...] = (
    "analytics_events",
    "analytics_event_sources",
    "analytics_metrics",
    "analytics_metric_values",
    "analytics_metric_snapshots",
    "analytics_aggregations",
    "analytics_aggregation_results",
    "analytics_dimensions",
    "analytics_measures",
    "analytics_filters",
    "analytics_queries",
    "analytics_query_results",
    "analytics_kpi_definitions",
    "analytics_kpi_values",
    "analytics_kpi_targets",
    "analytics_kpi_thresholds",
    "analytics_kpi_alerts",
    "analytics_kpi_history",
    "analytics_kpi_categories",
    "analytics_dashboards",
    "analytics_dashboard_widgets",
    "analytics_dashboard_layouts",
    "analytics_dashboard_filters",
    "analytics_dashboard_permissions",
    "analytics_dashboard_snapshots",
    "analytics_dashboard_exports",
    "analytics_reports",
    "analytics_report_templates",
    "analytics_report_sections",
    "analytics_report_runs",
    "analytics_report_outputs",
    "analytics_report_schedules",
    "analytics_report_recipients",
    "analytics_report_history",
    "bi_dimensions",
    "bi_measures",
    "bi_cubes",
    "bi_cube_dimensions",
    "bi_cube_measures",
    "bi_segments",
    "bi_segment_members",
    "bi_benchmarks",
    "bi_drill_paths",
    "bi_comparisons",
    "analytics_data_marts",
    "analytics_data_mart_sources",
    "analytics_data_mart_fields",
    "analytics_data_mart_views",
    "analytics_data_mart_refreshes",
    "analytics_data_mart_permissions",
    "analytics_trends",
    "analytics_trend_points",
    "analytics_anomalies",
    "analytics_forecasts",
    "analytics_forecast_points",
    "analytics_seasonality_profiles",
    "analytics_score_definitions",
    "analytics_score_values",
    "analytics_score_components",
    "analytics_score_history",
    "analytics_score_rules",
    "executive_dashboard_snapshots",
    "executive_dashboard_kpis",
    "executive_dashboard_alerts",
    "executive_dashboard_sections",
    "realtime_event_streams",
    "realtime_counters",
    "realtime_activity_logs",
    "realtime_alerts",
    "realtime_sessions",
    "realtime_processing_stats",
    "analytics_exports",
    "analytics_export_files",
    "analytics_export_jobs",
    "analytics_export_permissions",
    "analytics_export_logs",
    "analytics_ai_insights",
    "analytics_ai_recommendations",
    "analytics_ai_anomaly_reviews",
    "analytics_ai_forecasts",
    "analytics_ai_explanations",
    "analytics_ai_feedback",
)

SQLITE_V18_TABLES_SCRIPT = """
CREATE TABLE IF NOT EXISTS analytics_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    event_type TEXT NOT NULL DEFAULT 'generic', source_program TEXT NOT NULL DEFAULT 'global', payload_json TEXT NOT NULL DEFAULT '{}', occurred_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_events_status ON analytics_events(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_event_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    program_code TEXT NOT NULL DEFAULT 'global', source_type TEXT NOT NULL DEFAULT 'metrics', config_json TEXT NOT NULL DEFAULT '{}', enabled INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_analytics_event_sources_status ON analytics_event_sources(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', category TEXT NOT NULL DEFAULT 'general', unit TEXT NOT NULL DEFAULT 'count', source_program TEXT NOT NULL DEFAULT 'global', definition_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_metrics_status ON analytics_metrics(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_metric_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metric_id INTEGER, value REAL NOT NULL DEFAULT 0, dimensions_json TEXT NOT NULL DEFAULT '{}', recorded_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_metric_values_status ON analytics_metric_values(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_metric_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global', metrics_json TEXT NOT NULL DEFAULT '{}', snapshot_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_metric_snapshots_status ON analytics_metric_snapshots(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_aggregations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aggregation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', aggregation_type TEXT NOT NULL DEFAULT 'sum', config_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_aggregations_status ON analytics_aggregations(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_aggregation_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    aggregation_id INTEGER, result_json TEXT NOT NULL DEFAULT '{}', computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_aggregation_results_status ON analytics_aggregation_results(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_dimensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dimension_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', dimension_type TEXT NOT NULL DEFAULT 'string', config_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_dimensions_status ON analytics_dimensions(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_measures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    measure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', measure_type TEXT NOT NULL DEFAULT 'count', expression TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_analytics_measures_status ON analytics_measures(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_filters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filter_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', filter_type TEXT NOT NULL DEFAULT 'equals', expression_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_filters_status ON analytics_filters(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', query_type TEXT NOT NULL DEFAULT 'aggregate', query_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_queries_status ON analytics_queries(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_query_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    query_id INTEGER, result_json TEXT NOT NULL DEFAULT '{}', executed_at TEXT NOT NULL, duration_ms REAL NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_analytics_query_results_status ON analytics_query_results(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_kpi_definitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kpi_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', category TEXT NOT NULL DEFAULT 'general', formula_json TEXT NOT NULL DEFAULT '{}', source_program TEXT NOT NULL DEFAULT 'global'
);
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_definitions_status ON analytics_kpi_definitions(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_kpi_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, value REAL NOT NULL DEFAULT 0, period TEXT NOT NULL DEFAULT 'daily', computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_values_status ON analytics_kpi_values(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_kpi_targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, target_value REAL NOT NULL DEFAULT 0, period TEXT NOT NULL DEFAULT 'monthly', effective_from TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_targets_status ON analytics_kpi_targets(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_kpi_thresholds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    threshold_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, threshold_type TEXT NOT NULL DEFAULT 'warning', min_value REAL, max_value REAL, config_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_thresholds_status ON analytics_kpi_thresholds(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_kpi_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, alert_type TEXT NOT NULL DEFAULT 'threshold', severity TEXT NOT NULL DEFAULT 'warning', message TEXT NOT NULL DEFAULT '', triggered_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_alerts_status ON analytics_kpi_alerts(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_kpi_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, value REAL NOT NULL DEFAULT 0, period TEXT NOT NULL DEFAULT 'daily', recorded_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_history_status ON analytics_kpi_history(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_kpi_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', description TEXT NOT NULL DEFAULT '', parent_key TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_categories_status ON analytics_kpi_categories(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_dashboards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dashboard_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', dashboard_type TEXT NOT NULL DEFAULT 'custom', layout_json TEXT NOT NULL DEFAULT '{}', owner_user_id INTEGER
);
CREATE INDEX IF NOT EXISTS idx_analytics_dashboards_status ON analytics_dashboards(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_dashboard_widgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    widget_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, widget_type TEXT NOT NULL DEFAULT 'metric', config_json TEXT NOT NULL DEFAULT '{}', position_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_widgets_status ON analytics_dashboard_widgets(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_dashboard_layouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    layout_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, layout_json TEXT NOT NULL DEFAULT '{}', version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_layouts_status ON analytics_dashboard_layouts(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_dashboard_filters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filter_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, filter_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_filters_status ON analytics_dashboard_filters(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_dashboard_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, user_id INTEGER, role TEXT NOT NULL DEFAULT 'viewer', granted_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_permissions_status ON analytics_dashboard_permissions(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_dashboard_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, snapshot_json TEXT NOT NULL DEFAULT '{}', snapshot_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_snapshots_status ON analytics_dashboard_snapshots(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_dashboard_exports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    export_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, format TEXT NOT NULL DEFAULT 'json', file_path TEXT NOT NULL DEFAULT '', exported_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_exports_status ON analytics_dashboard_exports(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', report_type TEXT NOT NULL DEFAULT 'standard', config_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_reports_status ON analytics_reports(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_report_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', format TEXT NOT NULL DEFAULT 'html', template_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_report_templates_status ON analytics_report_templates(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_report_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, section_type TEXT NOT NULL DEFAULT 'summary', content_json TEXT NOT NULL DEFAULT '{}', sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_analytics_report_sections_status ON analytics_report_sections(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_report_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, run_status TEXT NOT NULL DEFAULT 'pending', started_at TEXT NOT NULL, completed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_analytics_report_runs_status ON analytics_report_runs(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_report_outputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    output_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    run_id INTEGER, format TEXT NOT NULL DEFAULT 'json', output_json TEXT NOT NULL DEFAULT '{}', generated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_report_outputs_status ON analytics_report_outputs(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_report_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, cron_expression TEXT NOT NULL DEFAULT '0 0 * * *', next_run_at TEXT, enabled INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_analytics_report_schedules_status ON analytics_report_schedules(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_report_recipients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    schedule_id INTEGER, user_id INTEGER, email TEXT NOT NULL DEFAULT '', delivery_format TEXT NOT NULL DEFAULT 'json'
);
CREATE INDEX IF NOT EXISTS idx_analytics_report_recipients_status ON analytics_report_recipients(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_report_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, run_id INTEGER, summary_json TEXT NOT NULL DEFAULT '{}', recorded_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_report_history_status ON analytics_report_history(status, created_at);
CREATE TABLE IF NOT EXISTS bi_dimensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dimension_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', hierarchy_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_bi_dimensions_status ON bi_dimensions(status, created_at);
CREATE TABLE IF NOT EXISTS bi_measures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    measure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', aggregation TEXT NOT NULL DEFAULT 'sum', expression TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_bi_measures_status ON bi_measures(status, created_at);
CREATE TABLE IF NOT EXISTS bi_cubes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cube_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', config_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_bi_cubes_status ON bi_cubes(status, created_at);
CREATE TABLE IF NOT EXISTS bi_cube_dimensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    link_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    cube_id INTEGER, dimension_id INTEGER, sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_bi_cube_dimensions_status ON bi_cube_dimensions(status, created_at);
CREATE TABLE IF NOT EXISTS bi_cube_measures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    link_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    cube_id INTEGER, measure_id INTEGER, sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_bi_cube_measures_status ON bi_cube_measures(status, created_at);
CREATE TABLE IF NOT EXISTS bi_segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    segment_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', filter_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_bi_segments_status ON bi_segments(status, created_at);
CREATE TABLE IF NOT EXISTS bi_segment_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    segment_id INTEGER, entity_type TEXT NOT NULL DEFAULT 'user', entity_id INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_bi_segment_members_status ON bi_segment_members(status, created_at);
CREATE TABLE IF NOT EXISTS bi_benchmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    benchmark_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', benchmark_type TEXT NOT NULL DEFAULT 'industry', value REAL NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_bi_benchmarks_status ON bi_benchmarks(status, created_at);
CREATE TABLE IF NOT EXISTS bi_drill_paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    cube_id INTEGER, path_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_bi_drill_paths_status ON bi_drill_paths(status, created_at);
CREATE TABLE IF NOT EXISTS bi_comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comparison_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', comparison_type TEXT NOT NULL DEFAULT 'period', config_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_bi_comparisons_status ON bi_comparisons(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_data_marts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mart_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', mart_type TEXT NOT NULL DEFAULT 'crm', config_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_data_marts_status ON analytics_data_marts(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_data_mart_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, source_program TEXT NOT NULL DEFAULT 'crm', source_table TEXT NOT NULL DEFAULT '', mapping_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_sources_status ON analytics_data_mart_sources(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_data_mart_fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    field_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, field_name TEXT NOT NULL DEFAULT '', field_type TEXT NOT NULL DEFAULT 'string', expression TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_fields_status ON analytics_data_mart_fields(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_data_mart_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    view_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, view_json TEXT NOT NULL DEFAULT '{}', refreshed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_views_status ON analytics_data_mart_views(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_data_mart_refreshes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    refresh_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, refresh_status TEXT NOT NULL DEFAULT 'completed', started_at TEXT NOT NULL, completed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_refreshes_status ON analytics_data_mart_refreshes(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_data_mart_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, user_id INTEGER, role TEXT NOT NULL DEFAULT 'viewer', granted_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_permissions_status ON analytics_data_mart_permissions(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trend_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', metric_key TEXT NOT NULL DEFAULT '', trend_type TEXT NOT NULL DEFAULT 'linear', config_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_trends_status ON analytics_trends(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_trend_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    point_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, value REAL NOT NULL DEFAULT 0, recorded_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_trend_points_status ON analytics_trend_points(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anomaly_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, anomaly_type TEXT NOT NULL DEFAULT 'spike', severity TEXT NOT NULL DEFAULT 'warning', detected_at TEXT NOT NULL, details_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_anomalies_status ON analytics_anomalies(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    forecast_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, horizon_days INTEGER NOT NULL DEFAULT 30, model TEXT NOT NULL DEFAULT 'simple', config_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_forecasts_status ON analytics_forecasts(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_forecast_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    point_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    forecast_id INTEGER, value REAL NOT NULL DEFAULT 0, forecast_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_forecast_points_status ON analytics_forecast_points(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_seasonality_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, profile_json TEXT NOT NULL DEFAULT '{}', computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_seasonality_profiles_status ON analytics_seasonality_profiles(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_score_definitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', score_type TEXT NOT NULL DEFAULT 'customer', formula_json TEXT NOT NULL DEFAULT '{}', source_program TEXT NOT NULL DEFAULT 'global'
);
CREATE INDEX IF NOT EXISTS idx_analytics_score_definitions_status ON analytics_score_definitions(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_score_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, entity_type TEXT NOT NULL DEFAULT 'contact', entity_id INTEGER NOT NULL DEFAULT 0, value REAL NOT NULL DEFAULT 0, computed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_score_values_status ON analytics_score_values(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_score_components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    component_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, component_name TEXT NOT NULL DEFAULT '', weight REAL NOT NULL DEFAULT 1, value REAL NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_analytics_score_components_status ON analytics_score_components(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_score_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, entity_id INTEGER NOT NULL DEFAULT 0, value REAL NOT NULL DEFAULT 0, recorded_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_score_history_status ON analytics_score_history(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_score_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, rule_type TEXT NOT NULL DEFAULT 'threshold', rule_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_analytics_score_rules_status ON analytics_score_rules(status, created_at);
CREATE TABLE IF NOT EXISTS executive_dashboard_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global', snapshot_json TEXT NOT NULL DEFAULT '{}', snapshot_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_executive_dashboard_snapshots_status ON executive_dashboard_snapshots(status, created_at);
CREATE TABLE IF NOT EXISTS executive_dashboard_kpis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kpi_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, display_name TEXT NOT NULL DEFAULT '', value REAL NOT NULL DEFAULT 0, trend TEXT NOT NULL DEFAULT 'stable'
);
CREATE INDEX IF NOT EXISTS idx_executive_dashboard_kpis_status ON executive_dashboard_kpis(status, created_at);
CREATE TABLE IF NOT EXISTS executive_dashboard_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    alert_type TEXT NOT NULL DEFAULT 'info', severity TEXT NOT NULL DEFAULT 'info', message TEXT NOT NULL DEFAULT '', triggered_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_executive_dashboard_alerts_status ON executive_dashboard_alerts(status, created_at);
CREATE TABLE IF NOT EXISTS executive_dashboard_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', section_type TEXT NOT NULL DEFAULT 'overview', content_json TEXT NOT NULL DEFAULT '{}', sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_executive_dashboard_sections_status ON executive_dashboard_sections(status, created_at);
CREATE TABLE IF NOT EXISTS realtime_event_streams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stream_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', source_program TEXT NOT NULL DEFAULT 'global', config_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_realtime_event_streams_status ON realtime_event_streams(status, created_at);
CREATE TABLE IF NOT EXISTS realtime_counters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    counter_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, counter_name TEXT NOT NULL DEFAULT '', value INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_realtime_counters_status ON realtime_counters(status, created_at);
CREATE TABLE IF NOT EXISTS realtime_activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, activity_type TEXT NOT NULL DEFAULT 'event', payload_json TEXT NOT NULL DEFAULT '{}', logged_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_realtime_activity_logs_status ON realtime_activity_logs(status, created_at);
CREATE TABLE IF NOT EXISTS realtime_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, alert_type TEXT NOT NULL DEFAULT 'threshold', severity TEXT NOT NULL DEFAULT 'warning', message TEXT NOT NULL DEFAULT '', triggered_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_realtime_alerts_status ON realtime_alerts(status, created_at);
CREATE TABLE IF NOT EXISTS realtime_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    user_id INTEGER, started_at TEXT NOT NULL, last_activity_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_realtime_sessions_status ON realtime_sessions(status, created_at);
CREATE TABLE IF NOT EXISTS realtime_processing_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, events_processed INTEGER NOT NULL DEFAULT 0, avg_latency_ms REAL NOT NULL DEFAULT 0, recorded_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_realtime_processing_stats_status ON realtime_processing_stats(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_exports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    export_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', export_type TEXT NOT NULL DEFAULT 'csv', config_json TEXT NOT NULL DEFAULT '{}', requested_by INTEGER
);
CREATE INDEX IF NOT EXISTS idx_analytics_exports_status ON analytics_exports(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_export_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, format TEXT NOT NULL DEFAULT 'csv', file_path TEXT NOT NULL DEFAULT '', size_bytes INTEGER NOT NULL DEFAULT 0, created_at_file TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_export_files_status ON analytics_export_files(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_export_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, job_status TEXT NOT NULL DEFAULT 'pending', started_at TEXT NOT NULL, completed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_analytics_export_jobs_status ON analytics_export_jobs(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_export_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, user_id INTEGER, role TEXT NOT NULL DEFAULT 'viewer', granted_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_export_permissions_status ON analytics_export_permissions(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_export_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, action TEXT NOT NULL DEFAULT 'create', details_json TEXT NOT NULL DEFAULT '{}', logged_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_export_logs_status ON analytics_export_logs(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_ai_insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    insight_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    insight_type TEXT NOT NULL DEFAULT 'trend', title TEXT NOT NULL DEFAULT '', content_json TEXT NOT NULL DEFAULT '{}', confidence REAL NOT NULL DEFAULT 0, generated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_ai_insights_status ON analytics_ai_insights(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_ai_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recommendation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    recommendation_type TEXT NOT NULL DEFAULT 'action', title TEXT NOT NULL DEFAULT '', content_json TEXT NOT NULL DEFAULT '{}', score REAL NOT NULL DEFAULT 0, generated_at TEXT NOT NULL, user_id INTEGER
);
CREATE INDEX IF NOT EXISTS idx_analytics_ai_recommendations_status ON analytics_ai_recommendations(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_ai_anomaly_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    anomaly_id INTEGER, review_status TEXT NOT NULL DEFAULT 'pending', reviewer_user_id INTEGER, notes TEXT NOT NULL DEFAULT '', reviewed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_analytics_ai_anomaly_reviews_status ON analytics_ai_anomaly_reviews(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_ai_forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    forecast_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metric_key TEXT NOT NULL DEFAULT '', horizon_days INTEGER NOT NULL DEFAULT 30, forecast_json TEXT NOT NULL DEFAULT '{}', generated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_ai_forecasts_status ON analytics_ai_forecasts(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_ai_explanations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    explanation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, explanation_text TEXT NOT NULL DEFAULT '', generated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_ai_explanations_status ON analytics_ai_explanations(status, created_at);
CREATE TABLE IF NOT EXISTS analytics_ai_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feedback_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    insight_id INTEGER, user_id INTEGER, rating INTEGER NOT NULL DEFAULT 0, comment TEXT NOT NULL DEFAULT '', submitted_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_analytics_ai_feedback_status ON analytics_ai_feedback(status, created_at);
"""

POSTGRESQL_V18_STATEMENTS: tuple[str, ...] = (
    """
CREATE TABLE IF NOT EXISTS analytics_events (
    id SERIAL PRIMARY KEY,
    event_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    event_type TEXT NOT NULL DEFAULT 'generic', source_program TEXT NOT NULL DEFAULT 'global', payload_json TEXT NOT NULL DEFAULT '{}', occurred_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_events_status ON analytics_events(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_event_sources (
    id SERIAL PRIMARY KEY,
    source_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    program_code TEXT NOT NULL DEFAULT 'global', source_type TEXT NOT NULL DEFAULT 'metrics', config_json TEXT NOT NULL DEFAULT '{}', enabled INTEGER NOT NULL DEFAULT 1
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_event_sources_status ON analytics_event_sources(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_metrics (
    id SERIAL PRIMARY KEY,
    metric_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', category TEXT NOT NULL DEFAULT 'general', unit TEXT NOT NULL DEFAULT 'count', source_program TEXT NOT NULL DEFAULT 'global', definition_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_metrics_status ON analytics_metrics(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_metric_values (
    id SERIAL PRIMARY KEY,
    value_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metric_id INTEGER, value REAL NOT NULL DEFAULT 0, dimensions_json TEXT NOT NULL DEFAULT '{}', recorded_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_metric_values_status ON analytics_metric_values(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_metric_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global', metrics_json TEXT NOT NULL DEFAULT '{}', snapshot_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_metric_snapshots_status ON analytics_metric_snapshots(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_aggregations (
    id SERIAL PRIMARY KEY,
    aggregation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', aggregation_type TEXT NOT NULL DEFAULT 'sum', config_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_aggregations_status ON analytics_aggregations(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_aggregation_results (
    id SERIAL PRIMARY KEY,
    result_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    aggregation_id INTEGER, result_json TEXT NOT NULL DEFAULT '{}', computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_aggregation_results_status ON analytics_aggregation_results(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_dimensions (
    id SERIAL PRIMARY KEY,
    dimension_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', dimension_type TEXT NOT NULL DEFAULT 'string', config_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_dimensions_status ON analytics_dimensions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_measures (
    id SERIAL PRIMARY KEY,
    measure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', measure_type TEXT NOT NULL DEFAULT 'count', expression TEXT NOT NULL DEFAULT ''
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_measures_status ON analytics_measures(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_filters (
    id SERIAL PRIMARY KEY,
    filter_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', filter_type TEXT NOT NULL DEFAULT 'equals', expression_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_filters_status ON analytics_filters(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_queries (
    id SERIAL PRIMARY KEY,
    query_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', query_type TEXT NOT NULL DEFAULT 'aggregate', query_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_queries_status ON analytics_queries(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_query_results (
    id SERIAL PRIMARY KEY,
    result_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    query_id INTEGER, result_json TEXT NOT NULL DEFAULT '{}', executed_at TEXT NOT NULL, duration_ms REAL NOT NULL DEFAULT 0
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_query_results_status ON analytics_query_results(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_kpi_definitions (
    id SERIAL PRIMARY KEY,
    kpi_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', category TEXT NOT NULL DEFAULT 'general', formula_json TEXT NOT NULL DEFAULT '{}', source_program TEXT NOT NULL DEFAULT 'global'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_definitions_status ON analytics_kpi_definitions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_kpi_values (
    id SERIAL PRIMARY KEY,
    value_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, value REAL NOT NULL DEFAULT 0, period TEXT NOT NULL DEFAULT 'daily', computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_values_status ON analytics_kpi_values(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_kpi_targets (
    id SERIAL PRIMARY KEY,
    target_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, target_value REAL NOT NULL DEFAULT 0, period TEXT NOT NULL DEFAULT 'monthly', effective_from TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_targets_status ON analytics_kpi_targets(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_kpi_thresholds (
    id SERIAL PRIMARY KEY,
    threshold_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, threshold_type TEXT NOT NULL DEFAULT 'warning', min_value REAL, max_value REAL, config_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_thresholds_status ON analytics_kpi_thresholds(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_kpi_alerts (
    id SERIAL PRIMARY KEY,
    alert_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, alert_type TEXT NOT NULL DEFAULT 'threshold', severity TEXT NOT NULL DEFAULT 'warning', message TEXT NOT NULL DEFAULT '', triggered_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_alerts_status ON analytics_kpi_alerts(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_kpi_history (
    id SERIAL PRIMARY KEY,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, value REAL NOT NULL DEFAULT 0, period TEXT NOT NULL DEFAULT 'daily', recorded_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_history_status ON analytics_kpi_history(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_kpi_categories (
    id SERIAL PRIMARY KEY,
    category_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', description TEXT NOT NULL DEFAULT '', parent_key TEXT NOT NULL DEFAULT ''
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_kpi_categories_status ON analytics_kpi_categories(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_dashboards (
    id SERIAL PRIMARY KEY,
    dashboard_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', dashboard_type TEXT NOT NULL DEFAULT 'custom', layout_json TEXT NOT NULL DEFAULT '{}', owner_user_id INTEGER,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_dashboards_status ON analytics_dashboards(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_dashboard_widgets (
    id SERIAL PRIMARY KEY,
    widget_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, widget_type TEXT NOT NULL DEFAULT 'metric', config_json TEXT NOT NULL DEFAULT '{}', position_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_widgets_status ON analytics_dashboard_widgets(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_dashboard_layouts (
    id SERIAL PRIMARY KEY,
    layout_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, layout_json TEXT NOT NULL DEFAULT '{}', version INTEGER NOT NULL DEFAULT 1
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_layouts_status ON analytics_dashboard_layouts(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_dashboard_filters (
    id SERIAL PRIMARY KEY,
    filter_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, filter_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_filters_status ON analytics_dashboard_filters(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_dashboard_permissions (
    id SERIAL PRIMARY KEY,
    permission_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, user_id INTEGER, role TEXT NOT NULL DEFAULT 'viewer', granted_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_permissions_status ON analytics_dashboard_permissions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_dashboard_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, snapshot_json TEXT NOT NULL DEFAULT '{}', snapshot_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_snapshots_status ON analytics_dashboard_snapshots(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_dashboard_exports (
    id SERIAL PRIMARY KEY,
    export_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dashboard_id INTEGER, format TEXT NOT NULL DEFAULT 'json', file_path TEXT NOT NULL DEFAULT '', exported_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_dashboard_exports_status ON analytics_dashboard_exports(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_reports (
    id SERIAL PRIMARY KEY,
    report_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', report_type TEXT NOT NULL DEFAULT 'standard', config_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_reports_status ON analytics_reports(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_report_templates (
    id SERIAL PRIMARY KEY,
    template_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', format TEXT NOT NULL DEFAULT 'html', template_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_report_templates_status ON analytics_report_templates(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_report_sections (
    id SERIAL PRIMARY KEY,
    section_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, section_type TEXT NOT NULL DEFAULT 'summary', content_json TEXT NOT NULL DEFAULT '{}', sort_order INTEGER NOT NULL DEFAULT 0
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_report_sections_status ON analytics_report_sections(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_report_runs (
    id SERIAL PRIMARY KEY,
    run_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, run_status TEXT NOT NULL DEFAULT 'pending', started_at TEXT NOT NULL, completed_at TEXT
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_report_runs_status ON analytics_report_runs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_report_outputs (
    id SERIAL PRIMARY KEY,
    output_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    run_id INTEGER, format TEXT NOT NULL DEFAULT 'json', output_json TEXT NOT NULL DEFAULT '{}', generated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_report_outputs_status ON analytics_report_outputs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_report_schedules (
    id SERIAL PRIMARY KEY,
    schedule_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, cron_expression TEXT NOT NULL DEFAULT '0 0 * * *', next_run_at TEXT, enabled INTEGER NOT NULL DEFAULT 1
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_report_schedules_status ON analytics_report_schedules(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_report_recipients (
    id SERIAL PRIMARY KEY,
    recipient_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    schedule_id INTEGER, user_id INTEGER, email TEXT NOT NULL DEFAULT '', delivery_format TEXT NOT NULL DEFAULT 'json',
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_report_recipients_status ON analytics_report_recipients(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_report_history (
    id SERIAL PRIMARY KEY,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    report_id INTEGER, run_id INTEGER, summary_json TEXT NOT NULL DEFAULT '{}', recorded_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_report_history_status ON analytics_report_history(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS bi_dimensions (
    id SERIAL PRIMARY KEY,
    dimension_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', hierarchy_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_bi_dimensions_status ON bi_dimensions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS bi_measures (
    id SERIAL PRIMARY KEY,
    measure_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', aggregation TEXT NOT NULL DEFAULT 'sum', expression TEXT NOT NULL DEFAULT ''
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_bi_measures_status ON bi_measures(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS bi_cubes (
    id SERIAL PRIMARY KEY,
    cube_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', config_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_bi_cubes_status ON bi_cubes(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS bi_cube_dimensions (
    id SERIAL PRIMARY KEY,
    link_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    cube_id INTEGER, dimension_id INTEGER, sort_order INTEGER NOT NULL DEFAULT 0
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_bi_cube_dimensions_status ON bi_cube_dimensions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS bi_cube_measures (
    id SERIAL PRIMARY KEY,
    link_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    cube_id INTEGER, measure_id INTEGER, sort_order INTEGER NOT NULL DEFAULT 0
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_bi_cube_measures_status ON bi_cube_measures(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS bi_segments (
    id SERIAL PRIMARY KEY,
    segment_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', filter_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_bi_segments_status ON bi_segments(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS bi_segment_members (
    id SERIAL PRIMARY KEY,
    member_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    segment_id INTEGER, entity_type TEXT NOT NULL DEFAULT 'user', entity_id INTEGER NOT NULL DEFAULT 0
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_bi_segment_members_status ON bi_segment_members(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS bi_benchmarks (
    id SERIAL PRIMARY KEY,
    benchmark_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', benchmark_type TEXT NOT NULL DEFAULT 'industry', value REAL NOT NULL DEFAULT 0
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_bi_benchmarks_status ON bi_benchmarks(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS bi_drill_paths (
    id SERIAL PRIMARY KEY,
    path_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    cube_id INTEGER, path_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_bi_drill_paths_status ON bi_drill_paths(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS bi_comparisons (
    id SERIAL PRIMARY KEY,
    comparison_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', comparison_type TEXT NOT NULL DEFAULT 'period', config_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_bi_comparisons_status ON bi_comparisons(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_data_marts (
    id SERIAL PRIMARY KEY,
    mart_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', mart_type TEXT NOT NULL DEFAULT 'crm', config_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_data_marts_status ON analytics_data_marts(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_data_mart_sources (
    id SERIAL PRIMARY KEY,
    source_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, source_program TEXT NOT NULL DEFAULT 'crm', source_table TEXT NOT NULL DEFAULT '', mapping_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_sources_status ON analytics_data_mart_sources(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_data_mart_fields (
    id SERIAL PRIMARY KEY,
    field_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, field_name TEXT NOT NULL DEFAULT '', field_type TEXT NOT NULL DEFAULT 'string', expression TEXT NOT NULL DEFAULT ''
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_fields_status ON analytics_data_mart_fields(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_data_mart_views (
    id SERIAL PRIMARY KEY,
    view_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, view_json TEXT NOT NULL DEFAULT '{}', refreshed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_views_status ON analytics_data_mart_views(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_data_mart_refreshes (
    id SERIAL PRIMARY KEY,
    refresh_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, refresh_status TEXT NOT NULL DEFAULT 'completed', started_at TEXT NOT NULL, completed_at TEXT
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_refreshes_status ON analytics_data_mart_refreshes(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_data_mart_permissions (
    id SERIAL PRIMARY KEY,
    permission_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    mart_id INTEGER, user_id INTEGER, role TEXT NOT NULL DEFAULT 'viewer', granted_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_data_mart_permissions_status ON analytics_data_mart_permissions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_trends (
    id SERIAL PRIMARY KEY,
    trend_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', metric_key TEXT NOT NULL DEFAULT '', trend_type TEXT NOT NULL DEFAULT 'linear', config_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_trends_status ON analytics_trends(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_trend_points (
    id SERIAL PRIMARY KEY,
    point_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, value REAL NOT NULL DEFAULT 0, recorded_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_trend_points_status ON analytics_trend_points(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_anomalies (
    id SERIAL PRIMARY KEY,
    anomaly_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, anomaly_type TEXT NOT NULL DEFAULT 'spike', severity TEXT NOT NULL DEFAULT 'warning', detected_at TEXT NOT NULL, details_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_anomalies_status ON analytics_anomalies(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_forecasts (
    id SERIAL PRIMARY KEY,
    forecast_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, horizon_days INTEGER NOT NULL DEFAULT 30, model TEXT NOT NULL DEFAULT 'simple', config_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_forecasts_status ON analytics_forecasts(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_forecast_points (
    id SERIAL PRIMARY KEY,
    point_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    forecast_id INTEGER, value REAL NOT NULL DEFAULT 0, forecast_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_forecast_points_status ON analytics_forecast_points(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_seasonality_profiles (
    id SERIAL PRIMARY KEY,
    profile_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    trend_id INTEGER, profile_json TEXT NOT NULL DEFAULT '{}', computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_seasonality_profiles_status ON analytics_seasonality_profiles(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_score_definitions (
    id SERIAL PRIMARY KEY,
    score_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', score_type TEXT NOT NULL DEFAULT 'customer', formula_json TEXT NOT NULL DEFAULT '{}', source_program TEXT NOT NULL DEFAULT 'global'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_score_definitions_status ON analytics_score_definitions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_score_values (
    id SERIAL PRIMARY KEY,
    value_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, entity_type TEXT NOT NULL DEFAULT 'contact', entity_id INTEGER NOT NULL DEFAULT 0, value REAL NOT NULL DEFAULT 0, computed_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_score_values_status ON analytics_score_values(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_score_components (
    id SERIAL PRIMARY KEY,
    component_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, component_name TEXT NOT NULL DEFAULT '', weight REAL NOT NULL DEFAULT 1, value REAL NOT NULL DEFAULT 0
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_score_components_status ON analytics_score_components(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_score_history (
    id SERIAL PRIMARY KEY,
    history_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, entity_id INTEGER NOT NULL DEFAULT 0, value REAL NOT NULL DEFAULT 0, recorded_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_score_history_status ON analytics_score_history(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_score_rules (
    id SERIAL PRIMARY KEY,
    rule_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    score_id INTEGER, rule_type TEXT NOT NULL DEFAULT 'threshold', rule_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_score_rules_status ON analytics_score_rules(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS executive_dashboard_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    scope TEXT NOT NULL DEFAULT 'global', snapshot_json TEXT NOT NULL DEFAULT '{}', snapshot_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_executive_dashboard_snapshots_status ON executive_dashboard_snapshots(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS executive_dashboard_kpis (
    id SERIAL PRIMARY KEY,
    kpi_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, display_name TEXT NOT NULL DEFAULT '', value REAL NOT NULL DEFAULT 0, trend TEXT NOT NULL DEFAULT 'stable'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_executive_dashboard_kpis_status ON executive_dashboard_kpis(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS executive_dashboard_alerts (
    id SERIAL PRIMARY KEY,
    alert_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    alert_type TEXT NOT NULL DEFAULT 'info', severity TEXT NOT NULL DEFAULT 'info', message TEXT NOT NULL DEFAULT '', triggered_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_executive_dashboard_alerts_status ON executive_dashboard_alerts(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS executive_dashboard_sections (
    id SERIAL PRIMARY KEY,
    section_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', section_type TEXT NOT NULL DEFAULT 'overview', content_json TEXT NOT NULL DEFAULT '{}', sort_order INTEGER NOT NULL DEFAULT 0
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_executive_dashboard_sections_status ON executive_dashboard_sections(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS realtime_event_streams (
    id SERIAL PRIMARY KEY,
    stream_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', source_program TEXT NOT NULL DEFAULT 'global', config_json TEXT NOT NULL DEFAULT '{}'
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_realtime_event_streams_status ON realtime_event_streams(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS realtime_counters (
    id SERIAL PRIMARY KEY,
    counter_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, counter_name TEXT NOT NULL DEFAULT '', value INTEGER NOT NULL DEFAULT 0
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_realtime_counters_status ON realtime_counters(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS realtime_activity_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, activity_type TEXT NOT NULL DEFAULT 'event', payload_json TEXT NOT NULL DEFAULT '{}', logged_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_realtime_activity_logs_status ON realtime_activity_logs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS realtime_alerts (
    id SERIAL PRIMARY KEY,
    alert_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, alert_type TEXT NOT NULL DEFAULT 'threshold', severity TEXT NOT NULL DEFAULT 'warning', message TEXT NOT NULL DEFAULT '', triggered_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_realtime_alerts_status ON realtime_alerts(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS realtime_sessions (
    id SERIAL PRIMARY KEY,
    session_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    user_id INTEGER, started_at TEXT NOT NULL, last_activity_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_realtime_sessions_status ON realtime_sessions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS realtime_processing_stats (
    id SERIAL PRIMARY KEY,
    stat_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    stream_id INTEGER, events_processed INTEGER NOT NULL DEFAULT 0, avg_latency_ms REAL NOT NULL DEFAULT 0, recorded_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_realtime_processing_stats_status ON realtime_processing_stats(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_exports (
    id SERIAL PRIMARY KEY,
    export_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '', export_type TEXT NOT NULL DEFAULT 'csv', config_json TEXT NOT NULL DEFAULT '{}', requested_by INTEGER,
    requested_by INTEGER REFERENCES users(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_exports_status ON analytics_exports(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_export_files (
    id SERIAL PRIMARY KEY,
    file_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, format TEXT NOT NULL DEFAULT 'csv', file_path TEXT NOT NULL DEFAULT '', size_bytes INTEGER NOT NULL DEFAULT 0, created_at_file TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_export_files_status ON analytics_export_files(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_export_jobs (
    id SERIAL PRIMARY KEY,
    job_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, job_status TEXT NOT NULL DEFAULT 'pending', started_at TEXT NOT NULL, completed_at TEXT
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_export_jobs_status ON analytics_export_jobs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_export_permissions (
    id SERIAL PRIMARY KEY,
    permission_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, user_id INTEGER, role TEXT NOT NULL DEFAULT 'viewer', granted_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_export_permissions_status ON analytics_export_permissions(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_export_logs (
    id SERIAL PRIMARY KEY,
    log_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    export_id INTEGER, action TEXT NOT NULL DEFAULT 'create', details_json TEXT NOT NULL DEFAULT '{}', logged_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_export_logs_status ON analytics_export_logs(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_ai_insights (
    id SERIAL PRIMARY KEY,
    insight_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    insight_type TEXT NOT NULL DEFAULT 'trend', title TEXT NOT NULL DEFAULT '', content_json TEXT NOT NULL DEFAULT '{}', confidence REAL NOT NULL DEFAULT 0, generated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_ai_insights_status ON analytics_ai_insights(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_ai_recommendations (
    id SERIAL PRIMARY KEY,
    recommendation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    recommendation_type TEXT NOT NULL DEFAULT 'action', title TEXT NOT NULL DEFAULT '', content_json TEXT NOT NULL DEFAULT '{}', score REAL NOT NULL DEFAULT 0, generated_at TEXT NOT NULL, user_id INTEGER,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_ai_recommendations_status ON analytics_ai_recommendations(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_ai_anomaly_reviews (
    id SERIAL PRIMARY KEY,
    review_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    anomaly_id INTEGER, review_status TEXT NOT NULL DEFAULT 'pending', reviewer_user_id INTEGER, notes TEXT NOT NULL DEFAULT '', reviewed_at TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_ai_anomaly_reviews_status ON analytics_ai_anomaly_reviews(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_ai_forecasts (
    id SERIAL PRIMARY KEY,
    forecast_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metric_key TEXT NOT NULL DEFAULT '', horizon_days INTEGER NOT NULL DEFAULT 30, forecast_json TEXT NOT NULL DEFAULT '{}', generated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_ai_forecasts_status ON analytics_ai_forecasts(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_ai_explanations (
    id SERIAL PRIMARY KEY,
    explanation_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    kpi_id INTEGER, explanation_text TEXT NOT NULL DEFAULT '', generated_at TEXT NOT NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_ai_explanations_status ON analytics_ai_explanations(status, created_at)
    """,
    """
CREATE TABLE IF NOT EXISTS analytics_ai_feedback (
    id SERIAL PRIMARY KEY,
    feedback_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    insight_id INTEGER, user_id INTEGER, rating INTEGER NOT NULL DEFAULT 0, comment TEXT NOT NULL DEFAULT '', submitted_at TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
)
    """,
    """
CREATE INDEX IF NOT EXISTS idx_analytics_ai_feedback_status ON analytics_ai_feedback(status, created_at)
    """,
)
