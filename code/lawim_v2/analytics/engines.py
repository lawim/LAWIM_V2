from __future__ import annotations

import json
import statistics
import uuid
from datetime import datetime, timezone
from typing import Any

from .constants import (
    AGGREGATION_TYPES,
    ANALYTIC_SOURCES,
    DASHBOARD_TYPES,
    EVENT_TYPES,
    EXPORT_FORMATS,
    KPI_CATEGORIES,
    METRIC_CATEGORIES,
    PROGRAM_CODES,
    REPORT_FORMATS,
    SCORE_TYPES,
    TREND_TYPES,
)


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class AnalyticsEngine:
    def validate_event_type(self, event_type: str) -> str:
        return event_type if event_type in EVENT_TYPES else "generic"

    def validate_category(self, category: str) -> str:
        return category if category in METRIC_CATEGORIES else "general"

    def build_event_payload(
        self,
        *,
        event_type: str,
        source_program: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        return {
            "event_type": self.validate_event_type(event_type),
            "source_program": source_program if source_program in PROGRAM_CODES else "global",
            "payload": payload or {},
            "occurred_at": _utcnow(),
        }


class AnalyticsAggregationEngine:
    def validate_type(self, aggregation_type: str) -> str:
        return aggregation_type if aggregation_type in AGGREGATION_TYPES else "sum"

    def aggregate(self, values: list[float], aggregation_type: str = "sum") -> float:
        if not values:
            return 0.0
        kind = self.validate_type(aggregation_type)
        if kind == "sum":
            return float(sum(values))
        if kind == "avg":
            return float(statistics.mean(values))
        if kind == "min":
            return float(min(values))
        if kind == "max":
            return float(max(values))
        if kind == "count":
            return float(len(values))
        if kind == "median":
            return float(statistics.median(values))
        return float(sum(values))


class AnalyticsQueryEngine:
    def build_query(
        self,
        *,
        name: str,
        query_type: str = "aggregate",
        dimensions: list[str] | None = None,
        measures: list[str] | None = None,
        filters: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        return {
            "name": name,
            "query_type": query_type,
            "dimensions": dimensions or [],
            "measures": measures or [],
            "filters": filters or {},
        }

    def execute(self, query: dict[str, object], data: list[dict[str, object]]) -> dict[str, object]:
        return {
            "query": query,
            "row_count": len(data),
            "rows": data[:100],
            "executed_at": _utcnow(),
        }


class AnalyticsSnapshotEngine:
    def build_snapshot(self, metrics: dict[str, object], *, scope: str = "global") -> dict[str, object]:
        return {
            "scope": scope,
            "metrics": metrics,
            "snapshot_at": _utcnow(),
        }


class AnalyticsPermissionEngine:
    ROLES = frozenset({"viewer", "editor", "admin"})

    def validate_role(self, role: str) -> str:
        return role if role in self.ROLES else "viewer"

    def can_view(self, role: str) -> bool:
        return self.validate_role(role) in self.ROLES

    def can_edit(self, role: str) -> bool:
        return self.validate_role(role) in {"editor", "admin"}


class KpiEngine:
    def validate_category(self, category: str) -> str:
        return category if category in KPI_CATEGORIES else "general"

    def compute_from_source(self, source_value: float | None, *, default: float = 0.0) -> float:
        if source_value is None:
            return default
        return float(source_value)

    def evaluate_threshold(
        self,
        value: float,
        *,
        min_value: float | None = None,
        max_value: float | None = None,
    ) -> dict[str, object]:
        breached = False
        severity = "ok"
        if min_value is not None and value < min_value:
            breached = True
            severity = "warning"
        if max_value is not None and value < max_value:
            breached = True
            severity = "critical"
        return {"breached": breached, "severity": severity, "value": value}


class DashboardEngine:
    def validate_type(self, dashboard_type: str) -> str:
        return dashboard_type if dashboard_type in DASHBOARD_TYPES else "custom"

    def build_layout(self, widgets: list[dict[str, object]] | None = None) -> dict[str, object]:
        return {"widgets": widgets or [], "version": 1}


class ReportingEngine:
    def validate_format(self, fmt: str) -> str:
        return fmt if fmt in REPORT_FORMATS else "json"

    def generate_output(
        self,
        *,
        report_type: str,
        data: dict[str, object],
        fmt: str = "json",
    ) -> dict[str, object]:
        output_format = self.validate_format(fmt)
        if output_format == "csv":
            rows = data.get("rows") or []
            lines = [",".join(str(k) for k in (rows[0].keys() if rows else []))]
            for row in rows:
                if isinstance(row, dict):
                    lines.append(",".join(str(v) for v in row.values()))
            content = "\n".join(lines)
        elif output_format == "html":
            content = f"<html><body><pre>{json.dumps(data, ensure_ascii=False)}</pre></body></html>"
        else:
            content = json.dumps(data, ensure_ascii=False, sort_keys=True)
        return {
            "format": output_format,
            "content": content,
            "generated_at": _utcnow(),
            "architecture_only": output_format in {"pdf", "excel", "xml"},
        }


class BusinessIntelligenceEngine:
    def build_cube(
        self,
        *,
        name: str,
        dimensions: list[str] | None = None,
        measures: list[str] | None = None,
    ) -> dict[str, object]:
        return {
            "name": name,
            "dimensions": dimensions or [],
            "measures": measures or [],
        }

    def drill_down(self, path: list[str], level: int = 1) -> dict[str, object]:
        return {"path": path, "level": level, "direction": "down"}

    def drill_up(self, path: list[str], level: int = 1) -> dict[str, object]:
        return {"path": path, "level": level, "direction": "up"}

    def compare(
        self,
        current: dict[str, float],
        previous: dict[str, float],
    ) -> dict[str, object]:
        deltas: dict[str, float] = {}
        for key, value in current.items():
            prev = previous.get(key, 0.0)
            deltas[key] = value - prev
        return {"current": current, "previous": previous, "deltas": deltas}


class DataMartEngine:
    def build_view(
        self,
        *,
        mart_type: str,
        sources: list[dict[str, object]],
    ) -> dict[str, object]:
        return {
            "mart_type": mart_type,
            "sources": sources,
            "logical_only": True,
            "refreshed_at": _utcnow(),
        }


class TrendAnalysisEngine:
    def validate_type(self, trend_type: str) -> str:
        return trend_type if trend_type in TREND_TYPES else "linear"

    def compute_growth(self, values: list[float]) -> dict[str, object]:
        if len(values) < 2:
            return {"growth_rate": 0.0, "direction": "stable"}
        first, last = values[0], values[-1]
        if first == 0:
            rate = 100.0 if last > 0 else 0.0
        else:
            rate = ((last - first) / abs(first)) * 100.0
        direction = "up" if rate > 0 else "down" if rate < 0 else "stable"
        return {"growth_rate": round(rate, 2), "direction": direction}

    def detect_anomalies(self, values: list[float], *, threshold: float = 2.0) -> list[dict[str, object]]:
        if len(values) < 3:
            return []
        mean = statistics.mean(values)
        stdev = statistics.pstdev(values) or 1.0
        anomalies = []
        for idx, value in enumerate(values):
            z = abs(value - mean) / stdev
            if z >= threshold:
                anomalies.append(
                    {
                        "index": idx,
                        "value": value,
                        "z_score": round(z, 2),
                        "anomaly_type": "spike" if value > mean else "drop",
                    }
                )
        return anomalies

    def simple_forecast(self, values: list[float], horizon: int = 7) -> list[float]:
        if not values:
            return [0.0] * horizon
        if len(values) == 1:
            return [values[0]] * horizon
        slope = (values[-1] - values[0]) / max(len(values) - 1, 1)
        return [max(0.0, values[-1] + slope * (i + 1)) for i in range(horizon)]


class ScoreEngine:
    def validate_type(self, score_type: str) -> str:
        return score_type if score_type in SCORE_TYPES else "platform_health"

    def aggregate_components(
        self,
        components: list[dict[str, object]],
        *,
        reuse_existing: bool = True,
    ) -> float:
        if not components:
            return 0.0
        total_weight = sum(float(c.get("weight") or 1) for c in components)
        if total_weight <= 0:
            return 0.0
        weighted = sum(float(c.get("value") or 0) * float(c.get("weight") or 1) for c in components)
        return round(weighted / total_weight, 2)


class ExecutiveDashboardEngine:
    def build_summary(
        self,
        *,
        kpis: list[dict[str, object]],
        alerts: list[dict[str, object]],
        trends: dict[str, object],
        health: dict[str, object],
    ) -> dict[str, object]:
        return {
            "kpis": kpis,
            "alerts": alerts,
            "trends": trends,
            "health": health,
            "generated_at": _utcnow(),
        }


class RealTimeAnalyticsEngine:
    def increment_counter(self, counters: dict[str, int], name: str, delta: int = 1) -> dict[str, int]:
        counters[name] = counters.get(name, 0) + delta
        return counters

    def process_event(self, event: dict[str, object]) -> dict[str, object]:
        return {
            "processed": True,
            "event_type": event.get("event_type"),
            "processed_at": _utcnow(),
        }


class ExportEngine:
    def validate_format(self, fmt: str) -> str:
        return fmt if fmt in EXPORT_FORMATS else "json"

    def build_export(
        self,
        *,
        name: str,
        data: dict[str, object],
        fmt: str = "json",
    ) -> dict[str, object]:
        output_format = self.validate_format(fmt)
        return {
            "name": name,
            "format": output_format,
            "data": data,
            "architecture_only": output_format in {"pdf", "excel", "xml"},
            "exported_at": _utcnow(),
        }


class AiAnalyticsEngine:
    def generate_insight(
        self,
        *,
        insight_type: str,
        title: str,
        content: dict[str, Any],
        confidence: float = 0.75,
    ) -> dict[str, object]:
        return {
            "insight_key": f"insight-{uuid.uuid4().hex[:12]}",
            "insight_type": insight_type,
            "title": title,
            "content": content,
            "confidence": min(max(confidence, 0.0), 1.0),
            "generated_at": _utcnow(),
            "traceable": True,
        }

    def explain_kpi(self, kpi_name: str, value: float, context: dict[str, object]) -> str:
        return f"{kpi_name} is {value:.2f} based on {len(context)} source metrics (Program L aggregation)."

    def recommend(
        self,
        *,
        recommendation_type: str,
        title: str,
        content: dict[str, Any],
        score: float = 0.5,
    ) -> dict[str, object]:
        return {
            "recommendation_key": f"rec-{uuid.uuid4().hex[:12]}",
            "recommendation_type": recommendation_type,
            "title": title,
            "content": content,
            "score": score,
            "generated_at": _utcnow(),
            "traceable": True,
        }


class AnalyticsPlatformEngine:
    def __init__(self) -> None:
        self.analytics = AnalyticsEngine()
        self.aggregation = AnalyticsAggregationEngine()
        self.query = AnalyticsQueryEngine()
        self.snapshot = AnalyticsSnapshotEngine()
        self.permission = AnalyticsPermissionEngine()
        self.kpi = KpiEngine()
        self.dashboard = DashboardEngine()
        self.reporting = ReportingEngine()
        self.bi = BusinessIntelligenceEngine()
        self.datamart = DataMartEngine()
        self.trend = TrendAnalysisEngine()
        self.score = ScoreEngine()
        self.executive = ExecutiveDashboardEngine()
        self.realtime = RealTimeAnalyticsEngine()
        self.export = ExportEngine()
        self.ai = AiAnalyticsEngine()

    def integration_catalog(self) -> list[dict[str, str]]:
        return [
            {"source_key": key, "program": program, "source_type": source_type}
            for key, program, source_type in ANALYTIC_SOURCES
        ]
