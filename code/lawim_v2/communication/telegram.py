from __future__ import annotations

from .engines import CommunicationPlatformEngine


class TelegramModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = CommunicationPlatformEngine().telegram

    def send(self, **kwargs: object) -> dict[str, object]:
        return self.repository.send_telegram(**kwargs)

    def list_messages(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_telegram_messages(**kwargs)

    def build_payload(self, **kwargs: object) -> dict[str, object]:
        return self.engine.build_payload(**kwargs)
