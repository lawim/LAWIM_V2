from __future__ import annotations

from .engines import CommunicationPlatformEngine


class SmsModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = CommunicationPlatformEngine().sms

    def send(self, **kwargs: object) -> dict[str, object]:
        return self.repository.send_sms(**kwargs)

    def list_messages(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_sms_messages(**kwargs)

    def build_payload(self, **kwargs: object) -> dict[str, object]:
        return self.engine.build_payload(**kwargs)
