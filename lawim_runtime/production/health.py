from __future__ import annotations

import time
import logging
from dataclasses import dataclass, field
from typing import Any, Callable

logger = logging.getLogger(__name__)


@dataclass
class HealthStatus:
    status: str = "ok"
    version: str = "1.0.0"
    checks: dict[str, str] = field(default_factory=dict)
    uptime_seconds: float = 0.0
    details: dict[str, Any] = field(default_factory=dict)


class HealthChecker:
    def __init__(self, version: str = "1.0.0") -> None:
        self._version = version
        self._started_at = time.time()
        self._checks: dict[str, Callable[[], str]] = {}

    def register_check(self, name: str, check_fn: Callable[[], str]) -> None:
        self._checks[name] = check_fn

    def check(self) -> HealthStatus:
        status = HealthStatus(version=self._version, uptime_seconds=time.time() - self._started_at)
        overall = "ok"
        for name, fn in self._checks.items():
            try:
                result = fn()
                status.checks[name] = result
                if result != "ok":
                    overall = "degraded"
            except Exception as e:
                status.checks[name] = f"error: {e}"
                overall = "degraded"
        status.status = overall
        return status

    def is_ready(self) -> bool:
        return self.check().status == "ok"

    def is_live(self) -> bool:
        return True


def db_health_check(db_path: str = "data/runtime/lawim.sqlite3") -> Callable[[], str]:
    import sqlite3

    def check() -> str:
        try:
            conn = sqlite3.connect(db_path)
            conn.execute("SELECT 1")
            conn.close()
            return "ok"
        except Exception as e:
            return f"db error: {e}"

    return check
