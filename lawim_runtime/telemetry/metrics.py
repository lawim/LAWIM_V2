from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from time import perf_counter
from typing import Any


@dataclass
class RuntimeMetrics:
    events_received: dict[str, int] = field(default_factory=dict)
    engines_executed: dict[str, int] = field(default_factory=dict)
    transitions_count: int = 0
    errors_count: int = 0
    total_latency_ms: float = 0.0
    engine_latency: dict[str, list[float]] = field(default_factory=dict)
    event_latency: dict[str, list[float]] = field(default_factory=dict)

    def record_event_received(self, event_type: str) -> None:
        self.events_received[event_type] = self.events_received.get(event_type, 0) + 1

    def record_engine_executed(self, engine_name: str) -> None:
        self.engines_executed[engine_name] = self.engines_executed.get(engine_name, 0) + 1

    def record_transition(self) -> None:
        self.transitions_count += 1

    def record_error(self) -> None:
        self.errors_count += 1

    def record_latency(self, engine: str, latency_ms: float) -> None:
        if engine not in self.engine_latency:
            self.engine_latency[engine] = []
        self.engine_latency[engine].append(latency_ms)
        self.total_latency_ms += latency_ms

    @contextmanager
    def measure(self, event_type: str):
        start = perf_counter()
        try:
            yield
        finally:
            duration = (perf_counter() - start) * 1000
            if event_type not in self.event_latency:
                self.event_latency[event_type] = []
            self.event_latency[event_type].append(duration)

    def get_summary(self) -> dict[str, Any]:
        return {
            "total_events": sum(self.events_received.values()),
            "events_by_type": dict(self.events_received),
            "transitions": self.transitions_count,
            "errors": self.errors_count,
            "total_latency_ms": round(self.total_latency_ms, 2),
        }
