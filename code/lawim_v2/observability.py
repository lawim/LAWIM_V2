from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field


@dataclass
class RuntimeMetrics:
    started_at: float = field(default_factory=time.time)
    requests_total: int = 0
    requests_failed: int = 0
    matches_total: int = 0
    conversations_total: int = 0
    notifications_total: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)

    def increment(self, name: str, *, failed: bool = False) -> None:
        with self.lock:
            self.requests_total += 1
            if failed:
                self.requests_failed += 1
            if name == "matches":
                self.matches_total += 1
            elif name == "conversations":
                self.conversations_total += 1
            elif name == "notifications":
                self.notifications_total += 1

    def snapshot(self) -> dict[str, object]:
        with self.lock:
            uptime_seconds = max(0, int(time.time() - self.started_at))
            return {
                "uptime_seconds": uptime_seconds,
                "requests_total": self.requests_total,
                "requests_failed": self.requests_failed,
                "matches_total": self.matches_total,
                "conversations_total": self.conversations_total,
                "notifications_total": self.notifications_total,
            }


METRICS = RuntimeMetrics()
