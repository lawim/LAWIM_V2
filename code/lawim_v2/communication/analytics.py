from __future__ import annotations

from .engines import CommunicationPlatformEngine


class AnalyticsModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = CommunicationPlatformEngine().analytics

    def stats(self) -> dict[str, object]:
        return self.repository.communication_stats()

    def dashboard(self) -> dict[str, object]:
        return self.repository.communication_dashboard()

    def analytics(self) -> dict[str, object]:
        return self.repository.communication_analytics()

    def snapshot(self) -> dict[str, object]:
        return self.repository.snapshot_communication_dashboard()

    def ai_recommendations(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_ai_recommendations(**kwargs)
