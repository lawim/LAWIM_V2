from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from .response_plan import InteractionResponsePlan


class DeliveryStatus(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    SENDING = "SENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    READ = "READ"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"


@dataclass
class DeliveryAttempt:
    attempt_id: str = field(default_factory=lambda: uuid4().hex[:16])
    delivery_id: str = ""
    attempt_number: int = 1
    status: DeliveryStatus = DeliveryStatus.CREATED
    provider_message_id: str = ""
    error: str = ""
    attempted_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class DeliveryResult:
    delivery_id: str = field(default_factory=lambda: uuid4().hex[:16])
    status: DeliveryStatus = DeliveryStatus.CREATED
    channel: str = ""
    provider_message_id: str = ""
    attempts: list[DeliveryAttempt] = field(default_factory=list)
    error: str = ""
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_delivered(self) -> bool:
        return self.status in (DeliveryStatus.SENT, DeliveryStatus.DELIVERED, DeliveryStatus.READ)

    @property
    def is_failed(self) -> bool:
        return self.status == DeliveryStatus.FAILED


class DeliveryManager:
    def __init__(self, max_retries: int = 3) -> None:
        self._max_retries = max_retries
        self._results: dict[str, DeliveryResult] = {}

    def deliver(self, plan: InteractionResponsePlan, channel: str) -> DeliveryResult:
        result = DeliveryResult(channel=channel, correlation_id=plan.correlation_id)
        if plan.is_empty():
            result.status = DeliveryStatus.CANCELLED
            self._results[result.delivery_id] = result
            return result

        attempt = DeliveryAttempt(delivery_id=result.delivery_id)
        try:
            provider_id = self._simulate_send(plan, channel)
            attempt.status = DeliveryStatus.SENT
            attempt.provider_message_id = provider_id
            result.status = DeliveryStatus.SENT
            result.provider_message_id = provider_id
        except Exception as e:
            attempt.status = DeliveryStatus.FAILED
            attempt.error = str(e)
            result.status = DeliveryStatus.FAILED
            result.error = str(e)

        result.attempts.append(attempt)
        self._results[result.delivery_id] = result
        return result

    def _simulate_send(self, plan: InteractionResponsePlan, channel: str) -> str:
        return uuid4().hex[:16]

    def get_result(self, delivery_id: str) -> DeliveryResult | None:
        return self._results.get(delivery_id)

    def count(self) -> int:
        return len(self._results)
