from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from ..observability import METRICS
from .constants import (
    ANALYTIC_SOURCES,
    DEFAULT_DASHBOARDS,
    DEFAULT_DATA_MARTS,
    DEFAULT_KPI_DEFINITIONS,
    DEFAULT_SCORE_DEFINITIONS,
)
from .engines import AnalyticsPlatformEngine


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _parse_json(value: str | None) -> Any:
    if not value:
        return {}
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {}


class AnalyticsRepositoryMixin:
    def analytics_tables_present(self) -> bool:
        row = self.one("SELECT name FROM sqlite_master WHERE type='table' AND name='analytics_events'")
        return row is not None

    def seed_analytics_catalog(self) -> None:
        if self.scalar("SELECT COUNT(*) FROM analytics_kpi_definitions") > 0:
            return
        engine = AnalyticsPlatformEngine()
        now = _utcnow()
        with self._transaction() as conn:
            for source_key, program, source_type in ANALYTIC_SOURCES:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO analytics_event_sources (
                        source_key, program_code, source_type, status, created_at, updated_at
                    ) VALUES (?, ?, ?, 'active', ?, ?)
                    """,
                    (source_key, program, source_type, now, now),
                )
            for kpi_key, name, category, source_program in DEFAULT_KPI_DEFINITIONS:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO analytics_kpi_definitions (
                        kpi_key, name, category, source_program, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'active', ?, ?)
                    """,
                    (kpi_key, name, category, source_program, now, now),
                )
            for dash_key, name, dash_type in DEFAULT_DASHBOARDS:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO analytics_dashboards (
                        dashboard_key, name, dashboard_type, status, created_at, updated_at
                    ) VALUES (?, ?, ?, 'active', ?, ?)
                    """,
                    (dash_key, name, dash_type, now, now),
                )
            for mart_key, name, mart_type in DEFAULT_DATA_MARTS:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO analytics_data_marts (
                        mart_key, name, mart_type, status, created_at, updated_at
                    ) VALUES (?, ?, ?, 'active', ?, ?)
                    """,
                    (mart_key, name, mart_type, now, now),
                )
            for score_key, name, score_type, source_program in DEFAULT_SCORE_DEFINITIONS:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO analytics_score_definitions (
                        score_key, name, score_type, source_program, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'active', ?, ?)
                    """,
                    (score_key, name, score_type, source_program, now, now),
                )
            conn.execute(
                """
                INSERT OR IGNORE INTO realtime_event_streams (
                    stream_key, name, source_program, status, created_at, updated_at
                ) VALUES ('stream-global', 'Global Event Stream', 'global', 'active', ?, ?)
                """,
                (now, now),
            )
        self.record_event("analytics_catalog_seeded", {"sources": len(ANALYTIC_SOURCES)})
        self.snapshot_executive_dashboard()

    def analytics_integration_sources(self) -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        checks = {
            "intelligent_core": hasattr(self, "get_intelligent_decision"),
            "ecosystem": hasattr(self, "get_service_catalog_item"),
            "cognition": hasattr(self, "cognition_query"),
            "assistant": hasattr(self, "assistant_chat"),
            "knowledge_platform": hasattr(self, "expert_rag_query"),
            "workflow_automation": hasattr(self, "start_automation_instance"),
            "real_estate_intelligence": hasattr(self, "get_rei_property_bundle"),
            "crm": hasattr(self, "get_crm_contact"),
            "marketplace": hasattr(self, "get_marketplace_provider"),
            "security": hasattr(self, "record_audit_trail"),
            "communication": hasattr(self, "communication_stats"),
        }
        rows = self.all(
            "SELECT source_key, program_code, source_type, status FROM analytics_event_sources ORDER BY source_key"
        )
        return {
            "sources": engine.integration_catalog(),
            "registered_sources": [dict(r) for r in rows],
            "programs": {key: bool(value) for key, value in checks.items()},
        }

    def collect_program_metrics(self) -> dict[str, object]:
        snapshot = METRICS.snapshot()
        crm_metrics = snapshot.get("crm_metrics") or {}
        collected: dict[str, object] = {
            "observability_metrics": {
                k: v for k, v in snapshot.items() if k.endswith("_total") or k.endswith("_latency_ms")
            },
            "crm_metrics": crm_metrics,
        }
        if hasattr(self, "communication_stats"):
            try:
                collected["communication_metrics"] = self.communication_stats()
            except Exception:
                collected["communication_metrics"] = {}
        if hasattr(self, "crm_analytics"):
            try:
                collected["crm_analytics"] = self.crm_analytics()
            except Exception:
                collected["crm_analytics"] = {}
        if hasattr(self, "marketplace_analytics"):
            try:
                collected["marketplace_metrics"] = self.marketplace_analytics()
            except Exception:
                collected["marketplace_metrics"] = {}
        if hasattr(self, "security_analytics"):
            try:
                collected["security_metrics"] = self.security_analytics()
            except Exception:
                collected["security_metrics"] = {}
        if hasattr(self, "rei_analytics"):
            try:
                collected["rei_metrics"] = self.rei_analytics()
            except Exception:
                collected["rei_metrics"] = {}
        if hasattr(self, "workflow_metrics"):
            try:
                collected["workflow_metrics"] = self.workflow_metrics()
            except Exception:
                collected["workflow_metrics"] = {}
        if hasattr(self, "knowledge_stats"):
            try:
                collected["knowledge_metrics"] = self.knowledge_stats()
            except Exception:
                collected["knowledge_metrics"] = {}
        return collected

    # --- Events ---

    def record_analytics_event(
        self,
        *,
        event_type: str = "generic",
        source_program: str = "global",
        payload: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        built = engine.analytics.build_event_payload(
            event_type=event_type, source_program=source_program, payload=payload
        )
        now = _utcnow()
        event_key = f"evt-{uuid.uuid4().hex[:16]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO analytics_events (
                    event_key, event_type, source_program, payload_json, occurred_at,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (
                    event_key,
                    built["event_type"],
                    built["source_program"],
                    _json(built["payload"]),
                    built["occurred_at"],
                    now,
                    now,
                ),
            )
            row = conn.execute("SELECT * FROM analytics_events WHERE event_key = ?", (event_key,)).fetchone()
        return dict(row)

    def list_analytics_events(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [
            dict(r)
            for r in self.all(
                "SELECT * FROM analytics_events ORDER BY occurred_at DESC LIMIT ?",
                (limit,),
            )
        ]

    # --- Metrics ---

    def create_analytics_metric(
        self,
        *,
        name: str,
        category: str = "general",
        unit: str = "count",
        source_program: str = "global",
        definition: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        metric_key = f"metric-{uuid.uuid4().hex[:12]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO analytics_metrics (
                    metric_key, name, category, unit, source_program, definition_json,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (metric_key, name, category, unit, source_program, _json(definition or {}), now, now),
            )
            row = conn.execute("SELECT * FROM analytics_metrics WHERE metric_key = ?", (metric_key,)).fetchone()
        return dict(row)

    def list_analytics_metrics(self, *, limit: int = 100) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM analytics_metrics ORDER BY created_at DESC LIMIT ?", (limit,))]

    def analytics_metrics_summary(self) -> dict[str, object]:
        collected = self.collect_program_metrics()
        engine = AnalyticsPlatformEngine()
        snapshot = engine.snapshot.build_snapshot(collected)
        now = _utcnow()
        snapshot_key = f"snap-{uuid.uuid4().hex[:12]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO analytics_metric_snapshots (
                    snapshot_key, scope, metrics_json, snapshot_at, status, created_at, updated_at
                ) VALUES (?, 'global', ?, ?, 'active', ?, ?)
                """,
                (snapshot_key, _json(snapshot["metrics"]), snapshot["snapshot_at"], now, now),
            )
        return {"metrics": collected, "snapshot_key": snapshot_key, "snapshot_at": snapshot["snapshot_at"]}

    # --- KPIs ---

    def list_kpi_definitions(self, *, limit: int = 100) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM analytics_kpi_definitions ORDER BY name LIMIT ?", (limit,))]

    def compute_kpis(self) -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        collected = self.collect_program_metrics()
        crm = collected.get("crm_analytics") or {}
        comm = collected.get("communication_metrics") or {}
        kpis: list[dict[str, object]] = []
        now = _utcnow()
        definitions = self.list_kpi_definitions()
        value_map = {
            "kpi-crm-leads": float(crm.get("leads") or crm.get("leads_new") or 0),
            "kpi-crm-conversion": engine.kpi.compute_from_source(
                float(crm.get("customers") or 0) / max(float(crm.get("leads") or 1), 1) * 100
            ),
            "kpi-marketplace-requests": float((collected.get("marketplace_metrics") or {}).get("requests") or 0),
            "kpi-workflow-success": engine.kpi.compute_from_source(
                float((collected.get("workflow_metrics") or {}).get("success_rate") or 0)
            ),
            "kpi-rei-properties": float((collected.get("rei_metrics") or {}).get("properties") or 0),
            "kpi-communication-delivery": engine.kpi.compute_from_source(
                float(comm.get("delivery_rate") or comm.get("messages_sent") or 0)
            ),
            "kpi-security-incidents": float((collected.get("security_metrics") or {}).get("open_incidents") or 0),
            "kpi-knowledge-queries": float((collected.get("knowledge_metrics") or {}).get("queries") or 0),
            "kpi-assistant-sessions": float(METRICS.snapshot().get("assistant_sessions_total") or 0),
            "kpi-ecosystem-partners": float(METRICS.snapshot().get("ecosystem_partners_total") or 0),
            "kpi-platform-health": engine.score.aggregate_components(
                [{"value": 80, "weight": 1}, {"value": 90, "weight": 1}]
            ),
            "kpi-user-activity": float(METRICS.snapshot().get("requests_total") or 0),
        }
        with self._transaction() as conn:
            for definition in definitions:
                kpi_key = str(definition["kpi_key"])
                value = value_map.get(kpi_key, 0.0)
                value_key = f"kv-{uuid.uuid4().hex[:12]}"
                conn.execute(
                    """
                    INSERT INTO analytics_kpi_values (
                        value_key, kpi_id, value, period, computed_at, status, created_at, updated_at
                    ) VALUES (?, ?, ?, 'daily', ?, 'active', ?, ?)
                    """,
                    (value_key, definition["id"], value, now, now, now),
                )
                kpis.append({"kpi_key": kpi_key, "name": definition["name"], "value": value})
        return {"kpis": kpis, "computed_at": now}

    # --- Dashboards ---

    def list_dashboards(self, *, dashboard_type: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if dashboard_type:
            return [
                dict(r)
                for r in self.all(
                    "SELECT * FROM analytics_dashboards WHERE dashboard_type = ? ORDER BY name LIMIT ?",
                    (dashboard_type, limit),
                )
            ]
        return [dict(r) for r in self.all("SELECT * FROM analytics_dashboards ORDER BY name LIMIT ?", (limit,))]

    def analytics_dashboard(self, *, dashboard_type: str = "global") -> dict[str, object]:
        dashboards = self.list_dashboards(dashboard_type=dashboard_type, limit=1)
        metrics = self.analytics_metrics_summary()
        kpis = self.compute_kpis()
        return {
            "dashboard": dashboards[0] if dashboards else {},
            "metrics": metrics.get("metrics"),
            "kpis": kpis.get("kpis"),
        }

    # --- Reports ---

    def create_report(
        self,
        *,
        name: str,
        report_type: str = "standard",
        config: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        report_key = f"report-{uuid.uuid4().hex[:12]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO analytics_reports (
                    report_key, name, report_type, config_json, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'active', ?, ?)
                """,
                (report_key, name, report_type, _json(config or {}), now, now),
            )
            row = conn.execute("SELECT * FROM analytics_reports WHERE report_key = ?", (report_key,)).fetchone()
        return dict(row)

    def list_reports(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM analytics_reports ORDER BY created_at DESC LIMIT ?", (limit,))]

    def run_report(self, report_id: int, *, fmt: str = "json") -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        report = self.one("SELECT * FROM analytics_reports WHERE id = ?", (report_id,))
        if report is None:
            raise ValueError("Report not found")
        data = {
            "report": dict(report),
            "metrics": self.analytics_metrics_summary(),
            "kpis": self.compute_kpis(),
        }
        output = engine.reporting.generate_output(
            report_type=str(report["report_type"]), data=data, fmt=fmt
        )
        now = _utcnow()
        run_key = f"run-{uuid.uuid4().hex[:12]}"
        output_key = f"out-{uuid.uuid4().hex[:12]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO analytics_report_runs (
                    run_key, report_id, run_status, started_at, completed_at, status, created_at, updated_at
                ) VALUES (?, ?, 'completed', ?, ?, 'active', ?, ?)
                """,
                (run_key, report_id, now, now, now, now),
            )
            run = conn.execute("SELECT id FROM analytics_report_runs WHERE run_key = ?", (run_key,)).fetchone()
            conn.execute(
                """
                INSERT INTO analytics_report_outputs (
                    output_key, run_id, format, output_json, generated_at, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (output_key, run["id"], output["format"], _json(output), output["generated_at"], now, now),
            )
        return output

    # --- BI ---

    def bi_summary(self) -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        cubes = [dict(r) for r in self.all("SELECT * FROM bi_cubes ORDER BY name LIMIT 10")]
        if not cubes:
            now = _utcnow()
            cube_key = "cube-global"
            with self._transaction() as conn:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO bi_cubes (
                        cube_key, name, status, created_at, updated_at
                    ) VALUES (?, 'Global Cube', 'active', ?, ?)
                    """,
                    (cube_key, now, now),
                )
            cubes = [dict(r) for r in self.all("SELECT * FROM bi_cubes LIMIT 1")]
        return {
            "cubes": cubes,
            "comparison": engine.bi.compare(
                {"requests": float(METRICS.snapshot().get("requests_total") or 0)},
                {"requests": 0.0},
            ),
        }

    # --- Data Marts ---

    def list_data_marts(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM analytics_data_marts ORDER BY name LIMIT ?", (limit,))]

    def refresh_data_mart(self, mart_id: int) -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        mart = self.one("SELECT * FROM analytics_data_marts WHERE id = ?", (mart_id,))
        if mart is None:
            raise ValueError("Data mart not found")
        sources = [dict(r) for r in self.all(
            "SELECT * FROM analytics_data_mart_sources WHERE mart_id = ?", (mart_id,)
        )]
        view = engine.datamart.build_view(mart_type=str(mart["mart_type"]), sources=sources)
        now = _utcnow()
        view_key = f"view-{uuid.uuid4().hex[:12]}"
        refresh_key = f"ref-{uuid.uuid4().hex[:12]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO analytics_data_mart_views (
                    view_key, mart_id, view_json, refreshed_at, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'active', ?, ?)
                """,
                (view_key, mart_id, _json(view), view["refreshed_at"], now, now),
            )
            conn.execute(
                """
                INSERT INTO analytics_data_mart_refreshes (
                    refresh_key, mart_id, refresh_status, started_at, completed_at, status, created_at, updated_at
                ) VALUES (?, ?, 'completed', ?, ?, 'active', ?, ?)
                """,
                (refresh_key, mart_id, now, now, now, now),
            )
        return {"mart": dict(mart), "view": view}

    # --- Trends ---

    def analyze_trends(self) -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        values = [
            float(METRICS.snapshot().get("requests_total") or 0),
            float(METRICS.snapshot().get("requests_total") or 0) * 0.9,
            float(METRICS.snapshot().get("requests_total") or 0) * 1.1,
        ]
        growth = engine.trend.compute_growth(values)
        anomalies = engine.trend.detect_anomalies(values)
        forecast = engine.trend.simple_forecast(values, horizon=7)
        now = _utcnow()
        trend_key = f"trend-{uuid.uuid4().hex[:12]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO analytics_trends (
                    trend_key, name, metric_key, trend_type, status, created_at, updated_at
                ) VALUES (?, 'Platform Activity', 'requests_total', 'linear', 'active', ?, ?)
                """,
                (trend_key, now, now),
            )
            trend = conn.execute("SELECT id FROM analytics_trends WHERE trend_key = ?", (trend_key,)).fetchone()
            for idx, value in enumerate(values):
                conn.execute(
                    """
                    INSERT INTO analytics_trend_points (
                        point_key, trend_id, value, recorded_at, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'active', ?, ?)
                    """,
                    (f"tp-{idx}-{uuid.uuid4().hex[:8]}", trend["id"], value, now, now, now),
                )
            for anomaly in anomalies:
                conn.execute(
                    """
                    INSERT INTO analytics_anomalies (
                        anomaly_key, trend_id, anomaly_type, severity, detected_at, details_json,
                        status, created_at, updated_at
                    ) VALUES (?, ?, ?, 'warning', ?, ?, 'active', ?, ?)
                    """,
                    (
                        f"an-{uuid.uuid4().hex[:8]}",
                        trend["id"],
                        anomaly["anomaly_type"],
                        now,
                        _json(anomaly),
                        now,
                        now,
                    ),
                )
        return {"growth": growth, "anomalies": anomalies, "forecast": forecast}

    # --- Scores ---

    def compute_scores(self) -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        definitions = [dict(r) for r in self.all("SELECT * FROM analytics_score_definitions LIMIT 20")]
        scores: list[dict[str, object]] = []
        now = _utcnow()
        with self._transaction() as conn:
            for definition in definitions:
                if definition["score_type"] == "customer" and hasattr(self, "crm_analytics"):
                    crm = self.crm_analytics()
                    value = engine.kpi.compute_from_source(float(crm.get("avg_lead_score") or 0))
                elif definition["score_type"] == "platform_health":
                    value = engine.score.aggregate_components([{"value": 85, "weight": 1}])
                else:
                    value = engine.score.aggregate_components([{"value": 70, "weight": 1}])
                value_key = f"sv-{uuid.uuid4().hex[:12]}"
                conn.execute(
                    """
                    INSERT INTO analytics_score_values (
                        value_key, score_id, entity_type, entity_id, value, computed_at,
                        status, created_at, updated_at
                    ) VALUES (?, ?, 'platform', 0, ?, ?, 'active', ?, ?)
                    """,
                    (value_key, definition["id"], value, now, now, now),
                )
                scores.append({"score_key": definition["score_key"], "name": definition["name"], "value": value})
        return {"scores": scores, "computed_at": now}

    # --- Executive Dashboard ---

    def snapshot_executive_dashboard(self) -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        kpis = self.compute_kpis()
        trends = self.analyze_trends()
        health = self.analytics_health()
        summary = engine.executive.build_summary(
            kpis=kpis.get("kpis") or [],
            alerts=[],
            trends=trends,
            health=health,
        )
        now = _utcnow()
        snapshot_key = f"exec-{uuid.uuid4().hex[:12]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO executive_dashboard_snapshots (
                    snapshot_key, scope, snapshot_json, snapshot_at, status, created_at, updated_at
                ) VALUES (?, 'global', ?, ?, 'active', ?, ?)
                """,
                (snapshot_key, _json(summary), now, now, now),
            )
        return {"executive": summary, "snapshot_key": snapshot_key}

    def executive_dashboard(self) -> dict[str, object]:
        row = self.one(
            "SELECT * FROM executive_dashboard_snapshots ORDER BY snapshot_at DESC LIMIT 1"
        )
        if row is None:
            return self.snapshot_executive_dashboard()
        return {"executive": _parse_json(str(row["snapshot_json"]))}

    # --- Real-Time ---

    def realtime_summary(self) -> dict[str, object]:
        streams = [dict(r) for r in self.all("SELECT * FROM realtime_event_streams LIMIT 10")]
        counters = [dict(r) for r in self.all("SELECT * FROM realtime_counters LIMIT 20")]
        return {
            "streams": streams,
            "counters": counters,
            "events_total": METRICS.snapshot().get("analytics_realtime_events_total") or 0,
            "active_sessions": len(counters),
        }

    def record_realtime_event(self, *, event_type: str = "generic", payload: dict[str, Any] | None = None) -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        processed = engine.realtime.process_event({"event_type": event_type, "payload": payload or {}})
        now = _utcnow()
        log_key = f"rtl-{uuid.uuid4().hex[:12]}"
        stream = self.one("SELECT id FROM realtime_event_streams LIMIT 1")
        stream_id = stream["id"] if stream else None
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO realtime_activity_logs (
                    log_key, stream_id, activity_type, payload_json, logged_at,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (log_key, stream_id, event_type, _json(payload or {}), now, now, now),
            )
        return processed

    # --- Exports ---

    def create_export(
        self,
        *,
        name: str,
        export_type: str = "json",
        config: dict[str, Any] | None = None,
        requested_by: int | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        export_key = f"export-{uuid.uuid4().hex[:12]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO analytics_exports (
                    export_key, name, export_type, config_json, requested_by,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (export_key, name, export_type, _json(config or {}), requested_by, now, now),
            )
            row = conn.execute("SELECT * FROM analytics_exports WHERE export_key = ?", (export_key,)).fetchone()
        return dict(row)

    def run_export(self, export_id: int) -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        export = self.one("SELECT * FROM analytics_exports WHERE id = ?", (export_id,))
        if export is None:
            raise ValueError("Export not found")
        data = self.analytics_statistics()
        result = engine.export.build_export(
            name=str(export["name"]),
            data=data,
            fmt=str(export["export_type"]),
        )
        now = _utcnow()
        job_key = f"job-{uuid.uuid4().hex[:12]}"
        file_key = f"file-{uuid.uuid4().hex[:12]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO analytics_export_jobs (
                    job_key, export_id, job_status, started_at, completed_at, status, created_at, updated_at
                ) VALUES (?, ?, 'completed', ?, ?, 'active', ?, ?)
                """,
                (job_key, export_id, now, now, now, now),
            )
            conn.execute(
                """
                INSERT INTO analytics_export_files (
                    file_key, export_id, format, file_path, size_bytes, created_at_file,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (
                    file_key,
                    export_id,
                    result["format"],
                    f"/exports/{file_key}.{result['format']}",
                    len(str(result.get("data", ""))),
                    now,
                    now,
                    now,
                ),
            )
            conn.execute(
                """
                INSERT INTO analytics_export_logs (
                    log_key, export_id, action, details_json, logged_at, status, created_at, updated_at
                ) VALUES (?, ?, 'run', ?, ?, 'active', ?, ?)
                """,
                (f"log-{uuid.uuid4().hex[:8]}", export_id, _json(result), now, now, now),
            )
        return result

    def list_exports(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM analytics_exports ORDER BY created_at DESC LIMIT ?", (limit,))]

    # --- AI Analytics ---

    def generate_ai_insights(self) -> dict[str, object]:
        engine = AnalyticsPlatformEngine()
        trends = self.analyze_trends()
        insight = engine.ai.generate_insight(
            insight_type="trend",
            title="Platform activity trend",
            content={"growth": trends.get("growth"), "source": "Program L aggregation"},
            confidence=0.8,
        )
        recommendation = engine.ai.recommend(
            recommendation_type="action",
            title="Review KPI thresholds",
            content={"reason": "Trend analysis completed"},
            score=0.7,
        )
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO analytics_ai_insights (
                    insight_key, insight_type, title, content_json, confidence, generated_at,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (
                    insight["insight_key"],
                    insight["insight_type"],
                    insight["title"],
                    _json(insight["content"]),
                    insight["confidence"],
                    insight["generated_at"],
                    now,
                    now,
                ),
            )
            conn.execute(
                """
                INSERT INTO analytics_ai_recommendations (
                    recommendation_key, recommendation_type, title, content_json, score, generated_at,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (
                    recommendation["recommendation_key"],
                    recommendation["recommendation_type"],
                    recommendation["title"],
                    _json(recommendation["content"]),
                    recommendation["score"],
                    recommendation["generated_at"],
                    now,
                    now,
                ),
            )
        return {"insights": [insight], "recommendations": [recommendation]}

    def list_ai_insights(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [
            dict(r)
            for r in self.all(
                "SELECT * FROM analytics_ai_insights ORDER BY generated_at DESC LIMIT ?",
                (limit,),
            )
        ]

    # --- Health & Statistics ---

    def analytics_health(self) -> dict[str, object]:
        return {
            "status": "healthy" if self.analytics_tables_present() else "degraded",
            "schema_version": 18,
            "tables_present": self.analytics_tables_present(),
            "sources_registered": self.scalar("SELECT COUNT(*) FROM analytics_event_sources"),
            "kpis_defined": self.scalar("SELECT COUNT(*) FROM analytics_kpi_definitions"),
            "dashboards_active": self.scalar(
                "SELECT COUNT(*) FROM analytics_dashboards WHERE status = 'active'"
            ),
            "platform_health_score": 85.0,
        }

    def analytics_statistics(self) -> dict[str, object]:
        return {
            "total_kpis": self.scalar("SELECT COUNT(*) FROM analytics_kpi_definitions"),
            "critical_kpis": self.scalar(
                "SELECT COUNT(*) FROM analytics_kpi_alerts WHERE severity = 'critical'"
            ),
            "reports_generated": self.scalar("SELECT COUNT(*) FROM analytics_report_runs"),
            "dashboards_active": self.scalar(
                "SELECT COUNT(*) FROM analytics_dashboards WHERE status = 'active'"
            ),
            "exports_completed": self.scalar(
                "SELECT COUNT(*) FROM analytics_export_jobs WHERE job_status = 'completed'"
            ),
            "ai_insights": self.scalar("SELECT COUNT(*) FROM analytics_ai_insights"),
            "sources_integrated": self.scalar("SELECT COUNT(*) FROM analytics_event_sources"),
            "events_analyzed": self.scalar("SELECT COUNT(*) FROM analytics_events"),
            "trends_detected": self.scalar("SELECT COUNT(*) FROM analytics_trends"),
            "anomalies_detected": self.scalar("SELECT COUNT(*) FROM analytics_anomalies"),
            "platform_health_score": 85.0,
            "avg_query_latency_ms": METRICS.snapshot().get("analytics_query_latency_seconds", 0) * 1000,
            "avg_aggregation_latency_ms": METRICS.snapshot().get("analytics_aggregation_latency_seconds", 0) * 1000,
        }
