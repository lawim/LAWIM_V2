from __future__ import annotations

from .engines import AnalyticsPlatformEngine


class ReportingModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = AnalyticsPlatformEngine().reporting

    def list(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_reports(**kwargs)

    def create(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_report(**kwargs)

    def run(self, report_id: int, **kwargs: object) -> dict[str, object]:
        return self.repository.run_report(report_id, **kwargs)
