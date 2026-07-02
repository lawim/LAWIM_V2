from __future__ import annotations

from .engines import AnalyticsPlatformEngine


class KpiModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = AnalyticsPlatformEngine().kpi

    def list_definitions(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_kpi_definitions(**kwargs)

    def compute(self) -> dict[str, object]:
        return self.repository.compute_kpis()
