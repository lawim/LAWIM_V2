from __future__ import annotations

from .engines import CommunicationPlatformEngine


class PreferencesModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = CommunicationPlatformEngine().preference

    def get(self, **kwargs: object) -> dict[str, object] | None:
        return self.repository.get_communication_preference(**kwargs)

    def upsert(self, **kwargs: object) -> dict[str, object]:
        return self.repository.upsert_communication_preference(**kwargs)

    def list_consents(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_communication_consents(**kwargs)

    def record_consent(self, **kwargs: object) -> dict[str, object]:
        return self.repository.record_communication_consent(**kwargs)

    def is_quiet_hours(self, *, user_id: int) -> bool:
        quiet = self.repository.get_quiet_hours(user_id=user_id)
        return self.engine.is_quiet_hours(quiet_hours=quiet)
