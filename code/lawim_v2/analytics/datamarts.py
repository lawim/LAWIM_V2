from __future__ import annotations

from .engines import AnalyticsPlatformEngine


class DataMartModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = AnalyticsPlatformEngine().datamart

    def list(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_data_marts(**kwargs)

    def refresh(self, mart_id: int) -> dict[str, object]:
        return self.repository.refresh_data_mart(mart_id)
