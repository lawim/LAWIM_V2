from __future__ import annotations

from .engines import AnalyticsPlatformEngine


class RealtimeModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = AnalyticsPlatformEngine().realtime

    def summary(self) -> dict[str, object]:
        return self.repository.realtime_summary()

    def record_event(self, **kwargs: object) -> dict[str, object]:
        return self.repository.record_realtime_event(**kwargs)
