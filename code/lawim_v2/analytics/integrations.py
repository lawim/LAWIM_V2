from __future__ import annotations


class IntegrationsModule:
    def __init__(self, repository) -> None:
        self.repository = repository

    def sources(self) -> dict[str, object]:
        return self.repository.analytics_integration_sources()

    def collect_metrics(self) -> dict[str, object]:
        return self.repository.collect_program_metrics()
