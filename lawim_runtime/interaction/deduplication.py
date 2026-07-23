from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class DeduplicationStatus(str, Enum):
    NEW = "NEW"
    DUPLICATE = "DUPLICATE"
    REPLAYED = "REPLAYED"
    BLOCKED = "BLOCKED"


@dataclass
class InteractionDeduplicator:
    _seen: dict[str, str] = field(default_factory=dict)

    def check(self, external_message_id: str, channel: str) -> DeduplicationStatus:
        key = f"{channel}:{external_message_id}"
        if not external_message_id:
            return DeduplicationStatus.NEW
        if key in self._seen:
            return DeduplicationStatus.DUPLICATE
        self._seen[key] = datetime.now(timezone.utc).isoformat()
        return DeduplicationStatus.NEW

    def check_by_hash(self, content_hash: str, channel: str) -> DeduplicationStatus:
        key = f"{channel}:hash:{content_hash}"
        if key in self._seen:
            return DeduplicationStatus.DUPLICATE
        self._seen[key] = datetime.now(timezone.utc).isoformat()
        return DeduplicationStatus.NEW

    def is_delivery_duplicate(self, delivery_key: str) -> bool:
        key = f"delivery:{delivery_key}"
        if key in self._seen:
            return True
        self._seen[key] = datetime.now(timezone.utc).isoformat()
        return False

    def count_seen(self) -> int:
        return len(self._seen)
