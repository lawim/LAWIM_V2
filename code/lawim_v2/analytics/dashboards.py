from __future__ import annotations

from .engines import AnalyticsPlatformEngine


class DashboardModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = AnalyticsPlatformEngine().dashboard

    def list(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_dashboards(**kwargs)

    def get(self, **kwargs: object) -> dict[str, object]:
        return self.repository.analytics_dashboard(**kwargs)
