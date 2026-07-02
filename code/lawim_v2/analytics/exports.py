from __future__ import annotations

from .engines import AnalyticsPlatformEngine


class ExportModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = AnalyticsPlatformEngine().export

    def list(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_exports(**kwargs)

    def create(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_export(**kwargs)

    def run(self, export_id: int) -> dict[str, object]:
        return self.repository.run_export(export_id)
