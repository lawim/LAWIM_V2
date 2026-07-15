from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Metric Catalog ─────────────────────────────────────────────────────────


class AggregationType(str, Enum):
    COUNT = "COUNT"
    SUM = "SUM"
    AVG = "AVG"
    RATE = "RATE"
    DISTINCT_COUNT = "DISTINCT_COUNT"
    MIN = "MIN"
    MAX = "MAX"
    PERCENTILE = "PERCENTILE"
    DURATION = "DURATION"


class MetricDomain(str, Enum):
    CHANNEL = "CHANNEL"
    CAMPAIGN = "CAMPAIGN"
    PUBLICATION = "PUBLICATION"
    ACTOR = "ACTOR"
    CONVERSATION = "CONVERSATION"
    QUALIFICATION = "QUALIFICATION"
    MATCHING = "MATCHING"
    VISIT = "VISIT"
    TRANSACTION = "TRANSACTION"
    PAYMENT = "PAYMENT"
    CONVERSION = "CONVERSION"
    GENERAL = "GENERAL"


class MetricStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    DRAFT = "DRAFT"


@dataclass(frozen=True)
class MetricDefinition:
    metric_code: str
    name: str
    description: str
    domain: MetricDomain
    unit: str
    aggregation_type: AggregationType
    formula: str
    formula_version: str
    dimensions: tuple[str, ...] = ()
    privacy_level: int = 0
    status: MetricStatus = MetricStatus.ACTIVE

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_code": self.metric_code,
            "name": self.name,
            "domain": self.domain.value,
            "unit": self.unit,
            "aggregation_type": self.aggregation_type.value,
            "formula": self.formula,
            "formula_version": self.formula_version,
            "dimensions": list(self.dimensions),
            "status": self.status.value,
        }


# ── Valid Dimensions ───────────────────────────────────────────────────────

ANALYTICS_DIMENSIONS: tuple[str, ...] = (
    "channel", "provider", "campaign", "publication", "tracking_code",
    "publication_actor", "actor_role_at_publication", "current_actor_role",
    "organization", "agency", "team",
    "conversation_actor", "exchange_type", "business_intent", "content_type",
    "exchange_result", "qualification_type", "property_type", "service",
    "matching", "visit", "transaction", "payment", "conversion_type",
    "language", "country", "city", "lawim_zone",
    "year", "quarter", "month", "week", "day", "hour",
)


# ── Aggregate ──────────────────────────────────────────────────────────────


@dataclass
class AnalyticAggregate:
    aggregate_id: str = ""
    domain: str = ""
    period_start: str = ""
    period_end: str = ""
    dimension_key: str = ""
    dimension_value: str = ""
    metric_code: str = ""
    metric_value: float = 0.0
    formula_version: str = "1.0"
    source_event_count: int = 0
    calculated_at: str = ""
    calculation_run_id: str = ""
    data_quality_status: str = "VALID"

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "dimension_key": self.dimension_key,
            "dimension_value": self.dimension_value,
            "metric_code": self.metric_code,
            "metric_value": self.metric_value,
            "formula_version": self.formula_version,
            "source_event_count": self.source_event_count,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "data_quality_status": self.data_quality_status,
        }


# ── Recalculation ──────────────────────────────────────────────────────────


class RecalculationMode(str, Enum):
    FULL_REBUILD = "FULL_REBUILD"
    INCREMENTAL = "INCREMENTAL"
    TARGETED = "TARGETED"
    VALIDATION_ONLY = "VALIDATION_ONLY"


class RecalculationStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class AnalyticsRun:
    run_id: str = ""
    mode: RecalculationMode = RecalculationMode.FULL_REBUILD
    scope: str = ""
    period_start: str = ""
    period_end: str = ""
    metric_codes: list[str] = field(default_factory=list)
    dimensions: list[str] = field(default_factory=list)
    formula_versions: dict[str, str] = field(default_factory=dict)
    started_at: str = ""
    completed_at: str = ""
    status: RecalculationStatus = RecalculationStatus.PENDING
    source_event_count: int = 0
    aggregate_count: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    initiated_by: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "mode": self.mode.value,
            "scope": self.scope,
            "status": self.status.value,
            "source_event_count": self.source_event_count,
            "aggregate_count": self.aggregate_count,
            "warning_count": len(self.warnings),
            "error_count": len(self.errors),
        }


# ── Data Quality ───────────────────────────────────────────────────────────


class DataQualityStatus(str, Enum):
    VALID = "VALID"
    WARNING = "WARNING"
    INCOMPLETE = "INCOMPLETE"
    INCONSISTENT = "INCONSISTENT"
    STALE = "STALE"
    REBUILD_REQUIRED = "REBUILD_REQUIRED"


@dataclass
class DataQualityCheck:
    check_id: str = ""
    check_type: str = ""
    dimension: str = ""
    status: DataQualityStatus = DataQualityStatus.VALID
    message: str = ""
    affected_count: int = 0
    checked_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "check_type": self.check_type,
            "status": self.status.value,
            "message": self.message,
            "affected_count": self.affected_count,
        }


# ── Dashboard Stats ────────────────────────────────────────────────────────


@dataclass
class DashboardSummary:
    total_campaigns: int = 0
    total_publications: int = 0
    total_clicks: int = 0
    total_unique_clicks: int = 0
    total_bots: int = 0
    total_redirects: int = 0
    total_conversations: int = 0
    total_leads: int = 0
    total_conversions: int = 0
    total_payments: int = 0
    total_revenue: float = 0.0
    currency: str = "XAF"
    top_channels: list[dict[str, Any]] = field(default_factory=list)
    top_actors: list[dict[str, Any]] = field(default_factory=list)
    data_quality_status: str = "VALID"
    last_recalculation: str = ""
    period_start: str = ""
    period_end: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_campaigns": self.total_campaigns,
            "total_publications": self.total_publications,
            "total_clicks": self.total_clicks,
            "total_unique_clicks": self.total_unique_clicks,
            "total_redirects": self.total_redirects,
            "total_conversations": self.total_conversations,
            "total_leads": self.total_leads,
            "total_conversions": self.total_conversions,
            "total_payments": self.total_payments,
            "total_revenue": self.total_revenue,
            "currency": self.currency,
            "top_channel_count": len(self.top_channels),
            "top_actor_count": len(self.top_actors),
            "data_quality_status": self.data_quality_status,
            "period_start": self.period_start,
            "period_end": self.period_end,
        }
