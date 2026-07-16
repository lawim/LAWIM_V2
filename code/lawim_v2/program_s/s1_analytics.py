from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class MetricDomain(str, Enum):
    ADMIN = "ADMIN"
    REPORTING = "REPORTING"
    MATCHING = "MATCHING"
    PAYMENT = "PAYMENT"
    LEARNING = "LEARNING"
    EXECUTIVE = "EXECUTIVE"


class AggregateStatus(str, Enum):
    PENDING = "PENDING"
    COMPUTED = "COMPUTED"
    STALE = "STALE"
    FAILED = "FAILED"


@dataclass
class MetricDefinition:
    code: str = ""
    name: str = ""
    domain: MetricDomain = MetricDomain.ADMIN
    formula: str = ""
    unit: str = ""
    version: str = "1.0"


@dataclass
class AnalyticsEvent:
    event_id: str = ""
    metric_code: str = ""
    value: float = 0.0
    dimension_key: str = ""
    dimension_value: str = ""
    timestamp: str = ""
    source: str = ""


@dataclass
class AnalyticsAggregate:
    aggregate_id: str = ""
    metric_code: str = ""
    period_start: str = ""
    period_end: str = ""
    dimension_key: str = ""
    dimension_value: str = ""
    value: float = 0.0
    count: int = 0
    status: AggregateStatus = AggregateStatus.PENDING
    version: str = "1.0"
    calculated_at: str = ""


@dataclass
class DashboardSnapshot:
    snapshot_id: str = ""
    domain: MetricDomain = MetricDomain.ADMIN
    metrics: dict[str, float] = field(default_factory=dict)
    period: str = ""
    taken_at: str = ""


@dataclass
class ReportSchedule:
    schedule_id: str = ""
    name: str = ""
    metric_codes: list[str] = field(default_factory=list)
    cron: str = "0 6 * * 1"
    recipients: list[str] = field(default_factory=list)
    active: bool = False


@dataclass
class ReportDelivery:
    delivery_id: str = ""
    schedule_id: str = ""
    status: str = "PENDING"
    delivered_at: str = ""
    error: str = ""


@dataclass
class AnalyticsRecalculation:
    run_id: str = ""
    mode: str = "FULL_REBUILD"
    metric_codes: list[str] = field(default_factory=list)
    period_start: str = ""
    period_end: str = ""
    status: str = "PENDING"
    started_at: str = ""
    completed_at: str = ""
    aggregates_updated: int = 0
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"run_id": self.run_id, "mode": self.mode, "status": self.status,
                "aggregates_updated": self.aggregates_updated}


class AnalyticsEngine:
    def compute_aggregate(self, metric: MetricDefinition,
                           events: list[AnalyticsEvent]) -> AnalyticsAggregate:
        values = [e.value for e in events if e.metric_code == metric.code]
        total = sum(values)
        count = len(values)
        value = total / count if count and metric.domain in (
            MetricDomain.REPORTING, MetricDomain.EXECUTIVE) else total
        return AnalyticsAggregate(
            metric_code=metric.code, value=value, count=count,
            status=AggregateStatus.COMPUTED,
            calculated_at=datetime.now(timezone.utc).isoformat())

    def rebuild(self, metrics: list[MetricDefinition],
                 events: list[AnalyticsEvent]) -> AnalyticsRecalculation:
        run = AnalyticsRecalculation(mode="FULL_REBUILD",
                                       started_at=datetime.now(timezone.utc).isoformat())
        for m in metrics:
            self.compute_aggregate(m, events)
            run.aggregates_updated += 1
        run.status = "COMPLETED"
        run.completed_at = datetime.now(timezone.utc).isoformat()
        return run
