from __future__ import annotations

from .engines import AnalyticsPlatformEngine


class TrendModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = AnalyticsPlatformEngine().trend

    def analyze(self) -> dict[str, object]:
        return self.repository.analyze_trends()
