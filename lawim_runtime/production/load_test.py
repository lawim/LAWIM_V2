from __future__ import annotations

import json
import logging
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)


@dataclass
class LoadTestResult:
    total_requests: int = 0
    successful: int = 0
    failed: int = 0
    total_time_ms: float = 0.0
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    errors: list[str] = field(default_factory=list)


class LoadTester:
    def __init__(self, base_url: str = "http://localhost:3000") -> None:
        self._base_url = base_url.rstrip("/")

    def run(
        self,
        num_users: int = 50,
        requests_per_user: int = 5,
        delay_between_requests_ms: float = 100,
    ) -> LoadTestResult:
        result = LoadTestResult()
        latencies: list[float] = []

        for user_idx in range(num_users):
            for req_idx in range(requests_per_user):
                start = time.time()
                try:
                    payload = json.dumps({
                        "message": f"Je cherche un appartement à Douala (user {user_idx}, req {req_idx})",
                        "user_id": f"load-test-user-{user_idx:04d}",
                        "session_id": str(uuid4()),
                    }).encode()

                    req = urllib.request.Request(
                        f"{self._base_url}/api/chat",
                        data=payload,
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        resp.read()
                    elapsed = (time.time() - start) * 1000
                    latencies.append(elapsed)
                    result.successful += 1
                except Exception as e:
                    elapsed = (time.time() - start) * 1000
                    latencies.append(elapsed)
                    result.failed += 1
                    result.errors.append(str(e))

                result.total_requests += 1
                if delay_between_requests_ms > 0:
                    time.sleep(delay_between_requests_ms / 1000)

            if (user_idx + 1) % 10 == 0:
                logger.info("load test: %d/%d users completed", user_idx + 1, num_users)

        if latencies:
            latencies.sort()
            result.total_time_ms = sum(latencies)
            result.p50_ms = latencies[len(latencies) // 2]
            result.p95_ms = latencies[int(len(latencies) * 0.95)]
            result.p99_ms = latencies[int(len(latencies) * 0.99)]

        return result

    def summary(self, result: LoadTestResult) -> dict[str, Any]:
        return {
            "total_requests": result.total_requests,
            "successful": result.successful,
            "failed": result.failed,
            "success_rate": f"{(result.successful / max(result.total_requests, 1)) * 100:.1f}%",
            "p50_ms": round(result.p50_ms, 1),
            "p95_ms": round(result.p95_ms, 1),
            "p99_ms": round(result.p99_ms, 1),
            "total_time_seconds": round(result.total_time_ms / 1000, 2),
        }
