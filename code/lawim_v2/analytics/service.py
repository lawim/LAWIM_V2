from __future__ import annotations

from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as adto
from .ai import AiModule
from .bi import BiModule
from .dashboards import DashboardModule
from .datamarts import DataMartModule
from .engines import AnalyticsPlatformEngine
from .exports import ExportModule
from .integrations import IntegrationsModule
from .kpi import KpiModule
from .realtime import RealtimeModule
from .reporting import ReportingModule
from .scores import ScoreModule
from .trends import TrendModule


class KpiService:
    def __init__(self, repository) -> None:
        self.module = KpiModule(repository)

    def list_definitions(self, **kwargs: object) -> dict[str, object]:
        rows = self.module.list_definitions(**kwargs)
        return {"kpis": [adto.kpi_dto(r) for r in rows]}

    def compute(self) -> dict[str, object]:
        METRICS.increment("analytics_kpi_total")
        return self.module.compute()


class DashboardService:
    def __init__(self, repository) -> None:
        self.module = DashboardModule(repository)

    def list(self, **kwargs: object) -> dict[str, object]:
        rows = self.module.list(**kwargs)
        METRICS.increment("analytics_dashboard_views_total")
        return {"dashboards": [adto.dashboard_dto(r) for r in rows]}

    def get(self, **kwargs: object) -> dict[str, object]:
        METRICS.increment("analytics_dashboard_views_total")
        return self.module.get(**kwargs)


class ReportingService:
    def __init__(self, repository) -> None:
        self.module = ReportingModule(repository)

    def list(self, **kwargs: object) -> dict[str, object]:
        rows = self.module.list(**kwargs)
        return {"reports": [adto.report_dto(r) for r in rows]}

    def create(self, **kwargs: object) -> dict[str, object]:
        row = self.module.create(**kwargs)
        return {"report": adto.report_dto(row)}

    def run(self, report_id: int, **kwargs: object) -> dict[str, object]:
        METRICS.increment("analytics_report_runs_total")
        METRICS.increment("reporting_outputs_total")
        return self.module.run(report_id, **kwargs)


class BusinessIntelligenceService:
    def __init__(self, repository) -> None:
        self.module = BiModule(repository)

    def summary(self) -> dict[str, object]:
        METRICS.increment("bi_queries_total")
        return {"bi": self.module.summary()}


class DataMartService:
    def __init__(self, repository) -> None:
        self.module = DataMartModule(repository)

    def list(self, **kwargs: object) -> dict[str, object]:
        rows = self.module.list(**kwargs)
        return {"datamarts": [adto.datamart_dto(r) for r in rows]}

    def refresh(self, mart_id: int) -> dict[str, object]:
        return {"datamart": self.module.refresh(mart_id)}


class TrendService:
    def __init__(self, repository) -> None:
        self.module = TrendModule(repository)

    def analyze(self) -> dict[str, object]:
        return {"trends": self.module.analyze()}


class ScoreService:
    def __init__(self, repository) -> None:
        self.module = ScoreModule(repository)

    def compute(self) -> dict[str, object]:
        return self.module.compute()


class ExecutiveDashboardService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def get(self) -> dict[str, object]:
        METRICS.increment("analytics_dashboard_views_total")
        return self.repository.executive_dashboard()


class RealTimeAnalyticsService:
    def __init__(self, repository) -> None:
        self.module = RealtimeModule(repository)

    def summary(self) -> dict[str, object]:
        return {"realtime": self.module.summary()}

    def record_event(self, **kwargs: object) -> dict[str, object]:
        METRICS.increment("analytics_realtime_events_total")
        return self.module.record_event(**kwargs)


class ExportService:
    def __init__(self, repository) -> None:
        self.module = ExportModule(repository)

    def list(self, **kwargs: object) -> dict[str, object]:
        rows = self.module.list(**kwargs)
        return {"exports": [adto.export_dto(r) for r in rows]}

    def create(self, **kwargs: object) -> dict[str, object]:
        row = self.module.create(**kwargs)
        return {"export": adto.export_dto(row)}

    def run(self, export_id: int) -> dict[str, object]:
        METRICS.increment("analytics_exports_total")
        return self.module.run(export_id)


class AiAnalyticsService:
    def __init__(self, repository) -> None:
        self.module = AiModule(repository)

    def generate(self) -> dict[str, object]:
        METRICS.increment("analytics_ai_insights_total")
        return self.module.generate()

    def list_insights(self, **kwargs: object) -> dict[str, object]:
        rows = self.module.list_insights(**kwargs)
        return {"insights": [adto.insight_dto(r) for r in rows]}


class AnalyticsIntegrationService:
    def __init__(self, repository) -> None:
        self.module = IntegrationsModule(repository)

    def sources(self) -> dict[str, object]:
        return self.module.sources()

    def collect_metrics(self) -> dict[str, object]:
        return {"metrics": self.module.collect_metrics()}


class AnalyticsService:
    def __init__(self, repository, project_service: ProjectService, policy) -> None:
        self.repository = repository
        self.projects = project_service
        self.policy = policy
        self.engine = AnalyticsPlatformEngine()
        self.kpi = KpiService(repository)
        self.dashboards = DashboardService(repository)
        self.reporting = ReportingService(repository)
        self.bi = BusinessIntelligenceService(repository)
        self.datamarts = DataMartService(repository)
        self.trends = TrendService(repository)
        self.scores = ScoreService(repository)
        self.executive = ExecutiveDashboardService(repository)
        self.realtime = RealTimeAnalyticsService(repository)
        self.exports = ExportService(repository)
        self.ai = AiAnalyticsService(repository)
        self.integrations = AnalyticsIntegrationService(repository)

    def _require_auth(self, actor: dict[str, object] | None) -> None:
        if actor is None:
            raise ProjectPermissionDenied("Authentication required")

    def _require_admin(self, actor: dict[str, object]) -> None:
        if not self.policy.is_admin(actor):
            raise ProjectPermissionDenied("Admin required")

    def health(self, *, actor: dict[str, object] | None = None) -> dict[str, object]:
        return {"health": self.repository.analytics_health()}

    def statistics(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("analytics_requests_total")
        return {"statistics": self.repository.analytics_statistics()}

    def list_events(self, *, actor: dict[str, object], limit: int = 50) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("analytics_events_total")
        rows = self.repository.list_analytics_events(limit=limit)
        return {"events": [adto.event_dto(r) for r in rows]}

    def record_event(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("analytics_events_total")
        row = self.repository.record_analytics_event(
            event_type=str(body.get("event_type") or "generic"),
            source_program=str(body.get("source_program") or "global"),
            payload=dict(body.get("payload") or {}),
        )
        return {"event": adto.event_dto(row)}

    def list_metrics(self, *, actor: dict[str, object], limit: int = 100) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("analytics_metrics_total")
        rows = self.repository.list_analytics_metrics(limit=limit)
        return {"metrics": [adto.metric_dto(r) for r in rows]}

    def create_metric(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("analytics_metrics_total")
        row = self.repository.create_analytics_metric(
            name=str(body["name"]),
            category=str(body.get("category") or "general"),
            unit=str(body.get("unit") or "count"),
            source_program=str(body.get("source_program") or "global"),
            definition=dict(body.get("definition") or {}),
        )
        return {"metric": adto.metric_dto(row)}

    def metrics_summary(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("analytics_aggregation_latency_seconds")
        return self.repository.analytics_metrics_summary()

    def dashboard(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return self.dashboards.get(dashboard_type="global")

    def integration_sources(self, *, actor: dict[str, object] | None = None) -> dict[str, object]:
        return self.integrations.sources()
