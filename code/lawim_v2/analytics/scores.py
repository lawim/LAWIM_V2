from __future__ import annotations

from .engines import AnalyticsPlatformEngine


class ScoreModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = AnalyticsPlatformEngine().score

    def compute(self) -> dict[str, object]:
        return self.repository.compute_scores()
