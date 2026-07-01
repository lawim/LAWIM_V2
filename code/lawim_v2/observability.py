from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field


def _percentile(values: list[float], ratio: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * ratio))))
    return round(ordered[index], 2)


@dataclass
class RuntimeMetrics:
    started_at: float = field(default_factory=time.time)
    requests_total: int = 0
    requests_failed: int = 0
    matches_total: int = 0
    conversations_total: int = 0
    notifications_total: int = 0
    projects_total: int = 0
    intelligent_workspace_total: int = 0
    ecosystem_partners_total: int = 0
    ecosystem_services_total: int = 0
    ecosystem_matching_total: int = 0
    ecosystem_workflows_total: int = 0
    ecosystem_reputation_total: int = 0
    ecosystem_notifications_total: int = 0
    ecosystem_orchestration_total: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)
    _latency_samples: list[float] = field(default_factory=list)
    _route_counts: dict[str, int] = field(default_factory=dict)

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
            elif name == "projects":
                self.projects_total += 1
            elif name == "intelligent_workspace":
                self.intelligent_workspace_total += 1
            elif name == "ecosystem_partners":
                self.ecosystem_partners_total += 1
            elif name == "ecosystem_services":
                self.ecosystem_services_total += 1
            elif name == "ecosystem_matching":
                self.ecosystem_matching_total += 1
            elif name == "ecosystem_workflows":
                self.ecosystem_workflows_total += 1
            elif name == "ecosystem_reputation":
                self.ecosystem_reputation_total += 1
            elif name == "ecosystem_notifications":
                self.ecosystem_notifications_total += 1
            elif name == "ecosystem_orchestration":
                self.ecosystem_orchestration_total += 1

    def record_request(self, *, route: str, duration_ms: float, failed: bool = False) -> None:
        with self.lock:
            self.requests_total += 1
            if failed:
                self.requests_failed += 1
            self._latency_samples.append(duration_ms)
            if len(self._latency_samples) > 1000:
                self._latency_samples = self._latency_samples[-1000:]
            self._route_counts[route] = self._route_counts.get(route, 0) + 1

    def snapshot(self) -> dict[str, object]:
        with self.lock:
            uptime_seconds = max(0, int(time.time() - self.started_at))
            samples = list(self._latency_samples)
            top_routes = sorted(self._route_counts.items(), key=lambda item: item[1], reverse=True)[:10]
            return {
                "uptime_seconds": uptime_seconds,
                "requests_total": self.requests_total,
                "requests_failed": self.requests_failed,
                "matches_total": self.matches_total,
                "conversations_total": self.conversations_total,
                "notifications_total": self.notifications_total,
                "projects_total": self.projects_total,
                "intelligent_workspace_total": self.intelligent_workspace_total,
                "ecosystem_partners_total": self.ecosystem_partners_total,
                "ecosystem_services_total": self.ecosystem_services_total,
                "ecosystem_matching_total": self.ecosystem_matching_total,
                "ecosystem_workflows_total": self.ecosystem_workflows_total,
                "ecosystem_reputation_total": self.ecosystem_reputation_total,
                "ecosystem_notifications_total": self.ecosystem_notifications_total,
                "ecosystem_orchestration_total": self.ecosystem_orchestration_total,
                "latency_ms": {
                    "p50": _percentile(samples, 0.50),
                    "p95": _percentile(samples, 0.95),
                    "max": round(max(samples), 2) if samples else 0.0,
                    "samples": len(samples),
                },
                "routes_top": [{"route": route, "count": count} for route, count in top_routes],
            }


METRICS = RuntimeMetrics()
