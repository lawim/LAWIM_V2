from __future__ import annotations

from .engines import AnalyticsPlatformEngine


class BiModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = AnalyticsPlatformEngine().bi

    def summary(self) -> dict[str, object]:
        return self.repository.bi_summary()
