from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class CircuitBreakerSnapshot:
    provider_key: str
    credential_alias: str
    state: str
    failure_count: int
    success_count: int
    window_started_at: str | None
    opened_at: str | None
    last_failure_at: str | None
    last_success_at: str | None
    half_open_requests: int

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_key": self.provider_key,
            "credential_alias": self.credential_alias,
            "state": self.state,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "window_started_at": self.window_started_at,
            "opened_at": self.opened_at,
            "last_failure_at": self.last_failure_at,
            "last_success_at": self.last_success_at,
            "half_open_requests": self.half_open_requests,
        }


class CircuitBreakerManager:
    def __init__(self, repository, config) -> None:
        self.repository = repository
        self.config = config

    def get(self, provider_key: str) -> CircuitBreakerSnapshot:
        row = self.repository.get_ai_circuit_breaker(provider_key)
        if row is None:
            return CircuitBreakerSnapshot(
                provider_key=provider_key,
                credential_alias=provider_key,
                state="CLOSED",
                failure_count=0,
                success_count=0,
                window_started_at=None,
                opened_at=None,
                last_failure_at=None,
                last_success_at=None,
                half_open_requests=0,
            )
        return CircuitBreakerSnapshot(
            provider_key=str(row.get("provider_key") or provider_key),
            credential_alias=str(row.get("credential_alias") or provider_key),
            state=str(row.get("state") or "CLOSED"),
            failure_count=int(row.get("failure_count") or 0),
            success_count=int(row.get("success_count") or 0),
            window_started_at=row.get("window_started_at"),
            opened_at=row.get("opened_at"),
            last_failure_at=row.get("last_failure_at"),
            last_success_at=row.get("last_success_at"),
            half_open_requests=int(row.get("half_open_requests") or 0),
        )

    def can_attempt(self, provider_key: str) -> bool:
        if not self.config.ai_circuit_breaker_enabled:
            return True
        snapshot = self.get(provider_key)
        if snapshot.state == "CLOSED":
            return True
        if snapshot.state == "OPEN":
            opened_at = snapshot.opened_at or snapshot.window_started_at
            if not opened_at:
                return False
            opened = _parse_datetime(opened_at)
            if opened is None:
                return False
            if datetime.now(timezone.utc) >= opened + timedelta(seconds=self.config.ai_circuit_breaker_open_seconds):
                return True
            return False
        if snapshot.state == "HALF_OPEN":
            return snapshot.half_open_requests < self.config.ai_circuit_breaker_half_open_requests
        return True

    def record_success(self, provider_key: str) -> CircuitBreakerSnapshot:
        snapshot = self.get(provider_key)
        updated = self.repository.upsert_ai_circuit_breaker(
            provider_key=provider_key,
            state="CLOSED",
            failure_count=0,
            success_count=snapshot.success_count + 1,
            half_open_requests=0,
            opened_at=None,
            last_success_at=_utcnow(),
            last_failure_at=snapshot.last_failure_at,
        )
        return CircuitBreakerSnapshot(
            provider_key=str(updated.get("provider_key") or provider_key),
            credential_alias=str(updated.get("credential_alias") or provider_key),
            state=str(updated.get("state") or "CLOSED"),
            failure_count=int(updated.get("failure_count") or 0),
            success_count=int(updated.get("success_count") or 0),
            window_started_at=updated.get("window_started_at"),
            opened_at=updated.get("opened_at"),
            last_failure_at=updated.get("last_failure_at"),
            last_success_at=updated.get("last_success_at"),
            half_open_requests=int(updated.get("half_open_requests") or 0),
        )

    def record_failure(self, provider_key: str) -> CircuitBreakerSnapshot:
        snapshot = self.get(provider_key)
        failure_count = snapshot.failure_count + 1
        state = "CLOSED"
        opened_at = snapshot.opened_at
        half_open_requests = snapshot.half_open_requests
        if failure_count >= self.config.ai_circuit_breaker_failure_threshold:
            state = "OPEN"
            opened_at = _utcnow()
            half_open_requests = 0
        updated = self.repository.upsert_ai_circuit_breaker(
            provider_key=provider_key,
            state=state,
            failure_count=failure_count,
            success_count=snapshot.success_count,
            half_open_requests=half_open_requests,
            opened_at=opened_at,
            last_failure_at=_utcnow(),
            last_success_at=snapshot.last_success_at,
        )
        return CircuitBreakerSnapshot(
            provider_key=str(updated.get("provider_key") or provider_key),
            credential_alias=str(updated.get("credential_alias") or provider_key),
            state=str(updated.get("state") or "CLOSED"),
            failure_count=int(updated.get("failure_count") or 0),
            success_count=int(updated.get("success_count") or 0),
            window_started_at=updated.get("window_started_at"),
            opened_at=updated.get("opened_at"),
            last_failure_at=updated.get("last_failure_at"),
            last_success_at=updated.get("last_success_at"),
            half_open_requests=int(updated.get("half_open_requests") or 0),
        )
