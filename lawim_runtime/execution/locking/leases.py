from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class LeaseStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    RELEASED = "RELEASED"
    RECOVERED = "RECOVERED"


@dataclass
class LeaseRecord:
    lease_id: str
    resource_key: str
    owner: str
    acquired_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(seconds=30))
    heartbeat_at: datetime | None = None
    status: LeaseStatus = LeaseStatus.ACTIVE
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at

    @property
    def remaining_seconds(self) -> float:
        remaining = (self.expires_at - datetime.now(timezone.utc)).total_seconds()
        return max(0.0, remaining)

    @property
    def age_seconds(self) -> float:
        return (datetime.now(timezone.utc) - self.acquired_at).total_seconds()


class ActionLeaseManager:
    def __init__(self) -> None:
        self._leases: dict[str, LeaseRecord] = {}

    def acquire(
        self,
        resource_key: str,
        owner: str,
        ttl_seconds: int = 30,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        existing = self._get_active_by_resource(resource_key)
        if existing is not None:
            return False
        now = datetime.now(timezone.utc)
        lease = LeaseRecord(
            lease_id=uuid4().hex[:16],
            resource_key=resource_key,
            owner=owner,
            acquired_at=now,
            expires_at=now + timedelta(seconds=ttl_seconds),
            heartbeat_at=None,
            status=LeaseStatus.ACTIVE,
            metadata=metadata or {},
        )
        self._leases[lease.lease_id] = lease
        return True

    def release(self, lease_id: str) -> bool:
        lease = self._leases.get(lease_id)
        if lease is None:
            return False
        lease.status = LeaseStatus.RELEASED
        return True

    def renew(self, lease_id: str, ttl_seconds: int = 30) -> bool:
        lease = self._leases.get(lease_id)
        if lease is None:
            return False
        if lease.status != LeaseStatus.ACTIVE:
            return False
        now = datetime.now(timezone.utc)
        lease.expires_at = now + timedelta(seconds=ttl_seconds)
        lease.heartbeat_at = now
        return True

    def is_expired(self, lease_id: str) -> bool:
        lease = self._leases.get(lease_id)
        if lease is None:
            return True
        return lease.is_expired

    def get_lease(self, lease_id: str) -> LeaseRecord | None:
        return self._leases.get(lease_id)

    def get_active_lease(self, resource_key: str) -> LeaseRecord | None:
        return self._get_active_by_resource(resource_key)

    def _get_active_by_resource(self, resource_key: str) -> LeaseRecord | None:
        for lease in self._leases.values():
            if lease.resource_key == resource_key and lease.status == LeaseStatus.ACTIVE and not lease.is_expired:
                return lease
        return None

    def recover_expired(self) -> list[LeaseRecord]:
        recovered: list[LeaseRecord] = []
        for lease in self._leases.values():
            if lease.status == LeaseStatus.ACTIVE and lease.is_expired:
                lease.status = LeaseStatus.RECOVERED
                recovered.append(lease)
        return recovered

    def list_active(self) -> list[LeaseRecord]:
        return [l for l in self._leases.values() if l.status == LeaseStatus.ACTIVE and not l.is_expired]

    def list_all(self) -> list[LeaseRecord]:
        return list(self._leases.values())

    def clear(self) -> None:
        self._leases.clear()
