from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class QueueItemStatus(str, Enum):
    ENQUEUED = "ENQUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DEAD_LETTERED = "DEAD_LETTERED"
    CANCELLED = "CANCELLED"


@dataclass(order=True)
class QueueItem:
    priority: int
    enqueued_at: datetime
    item_id: str = ""
    execution_id: str = ""
    action_code: str = ""
    payload: dict[str, Any] = field(default_factory=dict, compare=False)
    status: QueueItemStatus = QueueItemStatus.ENQUEUED

    def __post_init__(self) -> None:
        if not self.item_id:
            self.item_id = uuid4().hex[:16]


class ExecutionQueue:
    def __init__(self) -> None:
        self._items: list[QueueItem] = []
        self._by_id: dict[str, QueueItem] = {}
        self._max_size: int = 10000

    @property
    def size(self) -> int:
        return len(self._items)

    def enqueue(self, item: QueueItem) -> None:
        if self.size >= self._max_size:
            raise RuntimeError(f"Queue full ({self._max_size})")
        self._items.append(item)
        self._items.sort(key=lambda i: (i.priority, i.enqueued_at))
        self._by_id[item.item_id] = item

    def dequeue(self) -> QueueItem | None:
        if not self._items:
            return None
        item = self._items.pop(0)
        item.status = QueueItemStatus.PROCESSING
        return item

    def peek(self) -> QueueItem | None:
        if not self._items:
            return None
        return self._items[0]

    def get(self, item_id: str) -> QueueItem | None:
        return self._by_id.get(item_id)

    def cancel(self, item_id: str) -> bool:
        item = self._by_id.get(item_id)
        if item is None:
            return False
        item.status = QueueItemStatus.CANCELLED
        self._items[:] = [i for i in self._items if i.item_id != item_id]
        return True

    def list_pending(self) -> list[QueueItem]:
        return [i for i in self._by_id.values() if i.status == QueueItemStatus.ENQUEUED]

    def count(self) -> int:
        return len(self._by_id)

    def clear(self) -> None:
        self._items.clear()
        self._by_id.clear()
