from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from .analytics_models import (
    ANALYTICS_DIMENSIONS,
    AnalyticAggregate,
    AnalyticsRun,
    DataQualityCheck,
    DataQualityStatus,
    DashboardSummary,
    MetricDefinition,
    RecalculationMode,
    RecalculationStatus,
)
from .analytics_registry import get_metric, list_metrics, metric_codes
from .tracking_models import (
    AttributionModel,
    AttributionTouchpoint,
    ConversionEvent,
    ExternalCampaign,
    ExternalPublication,
    LeadAttribution,
    TouchpointType,
)


class AnalyticsEngine:
    def calculate_metric(self, metric_code: str, events: list[Any],
                          filters: dict[str, Any] | None = None) -> dict[str, Any]:
        metric = get_metric(metric_code)
        if metric is None:
            return {"error": f"Unknown metric: {metric_code}", "value": None}

        filtered = self._apply_filters(events, filters) if filters else events
        value = self._compute(metric, filtered)
        return {
            "metric_code": metric_code,
            "value": value,
            "formula": metric.formula,
            "formula_version": metric.formula_version,
            "source_count": len(filtered),
            "unit": metric.unit,
        }

    def calculate_metrics(self, metric_codes_list: list[str], events: list[Any],
                           filters: dict[str, Any] | None = None) -> dict[str, Any]:
        results = {}
        for code in metric_codes_list:
            results[code] = self.calculate_metric(code, events, filters)
        return results

    def group_by(self, metric_code: str, events: list[Any],
                  dimension: str, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        if dimension not in ANALYTICS_DIMENSIONS:
            return [{"error": f"Unknown dimension: {dimension}"}]
        metric = get_metric(metric_code)
        if metric is None:
            return [{"error": f"Unknown metric: {metric_code}"}]
        filtered = self._apply_filters(events, filters) if filters else events
        groups: dict[str, list[Any]] = {}
        for evt in filtered:
            val = self._get_dimension_value(evt, dimension)
            if val not in groups:
                groups[val] = []
            groups[val].append(evt)
        result = []
        for val, grp in sorted(groups.items(), key=lambda x: len(x[1]), reverse=True):
            result.append({
                "dimension": dimension,
                "dimension_value": val or "UNKNOWN",
                "metric_code": metric_code,
                "metric_value": self._compute(metric, grp),
                "source_count": len(grp),
            })
        return result

    def compare_periods(self, metric_code: str, events: list[Any],
                         period1_start: str, period1_end: str,
                         period2_start: str, period2_end: str) -> dict[str, Any]:
        p1 = [e for e in events if self._in_period(e, period1_start, period1_end)]
        p2 = [e for e in events if self._in_period(e, period2_start, period2_end)]
        metric = get_metric(metric_code)
        v1 = self._compute(metric, p1) if metric else 0
        v2 = self._compute(metric, p2) if metric else 0
        change = ((v2 - v1) / v1 * 100) if v1 else 0
        return {
            "metric_code": metric_code,
            "period1": {"start": period1_start, "end": period1_end, "value": v1, "count": len(p1)},
            "period2": {"start": period2_start, "end": period2_end, "value": v2, "count": len(p2)},
            "absolute_change": v2 - v1,
            "relative_change_pct": round(change, 2),
        }

    def rebuild_aggregates(self, events: list[Any], mode: RecalculationMode = RecalculationMode.FULL_REBUILD,
                            period_start: str = "", period_end: str = "",
                            metric_filter: list[str] | None = None) -> AnalyticsRun:
        run = AnalyticsRun(
            run_id=str(uuid.uuid4()),
            mode=mode,
            status=RecalculationStatus.RUNNING,
            started_at=datetime.now(timezone.utc).isoformat(),
            metric_codes=metric_filter or metric_codes(),
        )
        try:
            codes = metric_filter or metric_codes()
            for code in codes:
                self.calculate_metric(code, events)
            run.status = RecalculationStatus.COMPLETED
            run.source_event_count = len(events)
            run.completed_at = datetime.now(timezone.utc).isoformat()
        except Exception as e:
            run.status = RecalculationStatus.FAILED
            run.errors.append(str(e))
        return run

    def validate_aggregates(self, aggregates: list[AnalyticAggregate]) -> list[DataQualityCheck]:
        checks: list[DataQualityCheck] = []
        seen: dict[str, int] = {}
        for agg in aggregates:
            key = f"{agg.metric_code}:{agg.dimension_key}:{agg.dimension_value}"
            if key in seen:
                checks.append(DataQualityCheck(
                    check_id=str(uuid.uuid4()),
                    check_type="duplicate_aggregate",
                    status=DataQualityStatus.INCONSISTENT,
                    message=f"Duplicate aggregate for {key}",
                    affected_count=1,
                ))
            seen[key] = seen.get(key, 0) + 1
        for code in metric_codes():
            found = any(a.metric_code == code for a in aggregates)
            if not found:
                checks.append(DataQualityCheck(
                    check_id=str(uuid.uuid4()),
                    check_type="missing_metric",
                    status=DataQualityStatus.INCOMPLETE,
                    message=f"No aggregates for metric {code}",
                ))
        return checks

    def explain_metric(self, metric_code: str) -> dict[str, Any]:
        metric = get_metric(metric_code)
        if metric is None:
            return {"error": f"Unknown metric: {metric_code}"}
        return metric.to_dict()

    def _compute(self, metric: MetricDefinition, events: list[Any]) -> float:
        if metric.aggregation_type.value == "COUNT":
            return float(len(events))
        if metric.aggregation_type.value == "SUM":
            return float(sum(self._get_numeric(e) for e in events))
        if metric.aggregation_type.value == "AVG":
            return float(sum(self._get_numeric(e) for e in events)) / max(len(events), 1)
        return float(len(events))

    def _apply_filters(self, events: list[Any], filters: dict[str, Any]) -> list[Any]:
        result = list(events)
        for key, val in filters.items():
            if val is None:
                continue
            result = [e for e in result if self._match_filter(e, key, val)]
        return result

    def _match_filter(self, event: Any, key: str, value: Any) -> bool:
        if isinstance(event, dict):
            ev = event.get(key, event.get(key.lower(), ""))
        else:
            ev = getattr(event, key, getattr(event, key.lower(), ""))
        if ev is None:
            ev = ""
        if isinstance(value, list):
            return str(ev) in [str(v) for v in value]
        return str(ev).lower() == str(value).lower()

    def _get_dimension_value(self, event: Any, dimension: str) -> str:
        if isinstance(event, dict):
            return str(event.get(dimension, event.get(dimension.lower(), "UNKNOWN")))
        return str(getattr(event, dimension, getattr(event, dimension.lower(), "UNKNOWN")))

    def _get_numeric(self, event: Any) -> float:
        if isinstance(event, (int, float)):
            return float(event)
        if isinstance(event, dict):
            for key in ("monetary_value", "touchpoint_value", "amount", "value", "score"):
                v = event.get(key)
                if v is not None:
                    try:
                        return float(v)
                    except (ValueError, TypeError):
                        pass
        return 1.0

    def _in_period(self, event: Any, start: str, end: str) -> bool:
        ts = ""
        if isinstance(event, dict):
            ts = event.get("occurred_at", event.get("created_at", event.get("timestamp", "")))
        else:
            ts = getattr(event, "occurred_at", getattr(event, "created_at", ""))
        if not ts:
            return True
        return start <= ts <= end


# ── Data Quality Service ──────────────────────────────────────────────────


class AnalyticsDataQualityService:
    def run_checks(self, events: list[Any], conversions: list[ConversionEvent],
                    campaigns: list[ExternalCampaign] | None = None) -> list[DataQualityCheck]:
        checks: list[DataQualityCheck] = []
        checks.extend(self._check_orphan_events(events))
        checks.extend(self._check_duplicate_conversions(conversions))
        checks.extend(self._check_missing_campaigns(events, campaigns))
        return checks

    def _check_orphan_events(self, events: list[Any]) -> list[DataQualityCheck]:
        results = []
        no_actor = sum(1 for e in events if self._field_empty(e, "actor_id"))
        if no_actor:
            results.append(DataQualityCheck(
                check_id=str(uuid.uuid4()), check_type="orphan_event_no_actor",
                status=DataQualityStatus.WARNING,
                message=f"{no_actor} events without actor_id", affected_count=no_actor,
            ))
        no_channel = sum(1 for e in events if self._field_empty(e, "channel"))
        if no_channel:
            results.append(DataQualityCheck(
                check_id=str(uuid.uuid4()), check_type="orphan_event_no_channel",
                status=DataQualityStatus.WARNING,
                message=f"{no_channel} events without channel", affected_count=no_channel,
            ))
        return results

    def _check_duplicate_conversions(self, conversions: list[ConversionEvent]) -> list[DataQualityCheck]:
        results = []
        seen: set[str] = set()
        dups = 0
        for c in conversions:
            dk = getattr(c, "deduplication_key", None) or c.deduplication_key
            if dk and dk in seen:
                dups += 1
            elif dk:
                seen.add(dk)
        if dups:
            results.append(DataQualityCheck(
                check_id=str(uuid.uuid4()), check_type="duplicate_conversion",
                status=DataQualityStatus.INCONSISTENT,
                message=f"{dups} duplicate conversions detected", affected_count=dups,
            ))
        return results

    def _check_missing_campaigns(self, events: list[Any],
                                   campaigns: list[ExternalCampaign] | None) -> list[DataQualityCheck]:
        results = []
        if not campaigns:
            return results
        campaign_ids = {c.campaign_id for c in campaigns}
        missing = 0
        for e in events:
            cid = self._get_field(e, "campaign_id")
            if cid and cid not in campaign_ids:
                missing += 1
        if missing:
            results.append(DataQualityCheck(
                check_id=str(uuid.uuid4()), check_type="orphaned_campaign_ref",
                status=DataQualityStatus.INCOMPLETE,
                message=f"{missing} events reference unknown campaigns", affected_count=missing,
            ))
        return results

    def _field_empty(self, event: Any, field: str) -> bool:
        val = self._get_field(event, field)
        return val is None or str(val).strip() == ""

    def _get_field(self, event: Any, field: str) -> Any:
        if isinstance(event, dict):
            return event.get(field, event.get(field.lower()))
        return getattr(event, field, getattr(event, field.lower(), None))


# ── Dashboard Builder ──────────────────────────────────────────────────────


class DashboardBuilder:
    def build_admin(self, campaigns: list[Any], publications: list[Any],
                     redirects: list[Any], conversations: list[Any],
                     conversions: list[Any], payments: list[Any]) -> DashboardSummary:
        now = datetime.now(timezone.utc).isoformat()
        return DashboardSummary(
            total_campaigns=len(campaigns),
            total_publications=len(publications),
            total_clicks=sum(1 for r in redirects if not self._is_bot(r)),
            total_unique_clicks=len({self._get_session(r) for r in redirects if not self._is_bot(r)}),
            total_bots=sum(1 for r in redirects if self._is_bot(r)),
            total_redirects=len(redirects),
            total_conversations=len(conversations),
            total_conversions=len(conversions),
            total_payments=sum(1 for p in payments if self._is_confirmed(p)),
            total_revenue=sum(float(self._get_monetary(c)) for c in conversions),
            period_start="",
            period_end=now,
            last_recalculation=now,
        )

    def _is_bot(self, redirect: Any) -> bool:
        if isinstance(redirect, dict):
            return redirect.get("is_bot", False)
        return getattr(redirect, "is_bot", False)

    def _is_confirmed(self, payment: Any) -> bool:
        if isinstance(payment, dict):
            return payment.get("status", "") in ("confirmed", "completed", "CONFIRMED")
        s = getattr(payment, "status", getattr(payment, "state", ""))
        return str(s).lower() in ("confirmed", "completed")

    def _get_session(self, redirect: Any) -> str:
        if isinstance(redirect, dict):
            return str(redirect.get("session_id", ""))
        return str(getattr(redirect, "session_id", ""))

    def _get_monetary(self, conversion: Any) -> float:
        if isinstance(conversion, dict):
            return float(conversion.get("monetary_value", 0))
        return float(getattr(conversion, "monetary_value", 0))
