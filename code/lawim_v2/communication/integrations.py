from __future__ import annotations

from .engines import CommunicationPlatformEngine


class IntegrationsModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = CommunicationPlatformEngine().integration

    def sources(self) -> dict[str, object]:
        return self.repository.integration_sources()

    def process_event(self, **kwargs: object) -> dict[str, object]:
        return self.repository.process_communication_event(**kwargs)

    def map_event_kind(self, event_kind: str) -> dict[str, object]:
        return self.engine.map_event_kind(event_kind)
