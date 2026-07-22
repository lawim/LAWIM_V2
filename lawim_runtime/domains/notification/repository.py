from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .models import NotificationData, NotificationStatus


@dataclass
class NotificationRecord:
    record_id: str = field(default_factory=lambda: uuid4().hex[:16])
    data: NotificationData = field(default_factory=NotificationData)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class NotificationRepository(ABC):

    @abstractmethod
    def save(self, notification: NotificationData) -> None:
        ...

    @abstractmethod
    def get(self, notification_id: str) -> NotificationData | None:
        ...

    @abstractmethod
    def list_by_project(self, project_id: str) -> list[NotificationData]:
        ...

    @abstractmethod
    def list_pending(self) -> list[NotificationData]:
        ...

    @abstractmethod
    def cancel(self, notification_id: str) -> None:
        ...

    @abstractmethod
    def mark_sent(self, notification_id: str) -> None:
        ...


class InMemoryNotificationRepository(NotificationRepository):

    def __init__(self) -> None:
        self._records: dict[str, NotificationRecord] = {}

    def save(self, notification: NotificationData) -> None:
        record = NotificationRecord(
            data=notification,
            updated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._records[notification.notification_id] = record

    def get(self, notification_id: str) -> NotificationData | None:
        record = self._records.get(notification_id)
        if record is None:
            return None
        return record.data

    def list_by_project(self, project_id: str) -> list[NotificationData]:
        return [
            r.data
            for r in self._records.values()
            if r.data.project_id == project_id
        ]

    def list_pending(self) -> list[NotificationData]:
        return [
            r.data
            for r in self._records.values()
            if r.data.status in (NotificationStatus.PENDING, NotificationStatus.PREPARED, NotificationStatus.SCHEDULED)
        ]

    def cancel(self, notification_id: str) -> None:
        record = self._records.get(notification_id)
        if record is not None:
            record.data.status = NotificationStatus.CANCELLED
            record.updated_at = datetime.now(timezone.utc).isoformat()

    def mark_sent(self, notification_id: str) -> None:
        record = self._records.get(notification_id)
        if record is not None:
            record.data.status = NotificationStatus.SENT
            record.updated_at = datetime.now(timezone.utc).isoformat()
