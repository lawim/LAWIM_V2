from __future__ import annotations

from .engines import CommunicationPlatformEngine


class NotificationsModule:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = CommunicationPlatformEngine().notification

    def create(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_notification_event(**kwargs)

    def list_events(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_notification_events(**kwargs)

    def deliver(self, notification_id: int) -> dict[str, object]:
        return self.repository.deliver_notification(notification_id)

    def acknowledge(self, *, notification_id: int, user_id: int) -> dict[str, object]:
        return self.repository.acknowledge_notification(notification_id=notification_id, user_id=user_id)
