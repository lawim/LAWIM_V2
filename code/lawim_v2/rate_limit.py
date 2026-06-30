"""In-memory sliding-window rate limiter for auth endpoints."""

from __future__ import annotations

import time
from collections import defaultdict
from threading import Lock


class AuthRateLimiter:
    def __init__(self, *, max_attempts: int, window_seconds: int) -> None:
        self.max_attempts = max(1, max_attempts)
        self.window_seconds = max(1, window_seconds)
        self._events: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()

    def is_allowed(self, key: str) -> bool:
        now = time.monotonic()
        window_start = now - self.window_seconds
        with self._lock:
            hits = [stamp for stamp in self._events[key] if stamp >= window_start]
            if len(hits) >= self.max_attempts:
                return False
            hits.append(now)
            self._events[key] = hits
            return True
