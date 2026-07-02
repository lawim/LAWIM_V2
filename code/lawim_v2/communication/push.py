from __future__ import annotations

from .engines import CommunicationPlatformEngine


class PushModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = CommunicationPlatformEngine().push

    def send(self, **kwargs: object) -> dict[str, object]:
        return self.repository.send_push(**kwargs)

    def list_notifications(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_push_notifications(**kwargs)

    def register_device(self, **kwargs: object) -> dict[str, object]:
        return self.repository.register_push_device(**kwargs)
