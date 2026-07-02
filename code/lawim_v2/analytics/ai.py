from __future__ import annotations

from .engines import AnalyticsPlatformEngine


class AiModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = AnalyticsPlatformEngine().ai

    def generate(self) -> dict[str, object]:
        return self.repository.generate_ai_insights()

    def list_insights(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_ai_insights(**kwargs)
