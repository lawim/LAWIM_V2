from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class LockScope(str, Enum):
    GLOBAL = "GLOBAL"
    PROJECT = "PROJECT"
    PROFILE = "PROFILE"
    ACTION = "ACTION"
    RESOURCE = "RESOURCE"
    CUSTOM = "CUSTOM"


@dataclass
class LockRecord:
    lock_id: str
    scope: LockScope
    key: str
    owner: str
    acquired_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ttl_seconds: int = 30
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        elapsed = (datetime.now(timezone.utc) - self.acquired_at).total_seconds()
        return elapsed > self.ttl_seconds

    @property
    def remaining_ttl(self) -> float:
        elapsed = (datetime.now(timezone.utc) - self.acquired_at).total_seconds()
        return max(0.0, self.ttl_seconds - elapsed)


class ActionLockManager:
    def __init__(self) -> None:
        self._locks: dict[str, LockRecord] = {}

    def _lock_key(self, scope: LockScope, key: str) -> str:
        return f"{scope.value}:{key}"

    def acquire(
        self,
        scope: LockScope,
        key: str,
        owner: str,
        ttl_seconds: int = 30,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        lk = self._lock_key(scope, key)
        existing = self._locks.get(lk)
        if existing is not None and not existing.is_expired:
            return False
        self._locks[lk] = LockRecord(
            lock_id=lk,
            scope=scope,
            key=key,
            owner=owner,
            ttl_seconds=ttl_seconds,
            metadata=metadata or {},
        )
        return True

    def release(self, scope: LockScope, key: str, owner: str) -> bool:
        lk = self._lock_key(scope, key)
        existing = self._locks.get(lk)
        if existing is None:
            return False
        if existing.owner != owner:
            return False
        del self._locks[lk]
        return True

    def is_locked(self, scope: LockScope, key: str) -> bool:
        lk = self._lock_key(scope, key)
        existing = self._locks.get(lk)
        if existing is None:
            return False
        if existing.is_expired:
            del self._locks[lk]
            return False
        return True

    def get_owner(self, scope: LockScope, key: str) -> str | None:
        lk = self._lock_key(scope, key)
        existing = self._locks.get(lk)
        if existing is None or existing.is_expired:
            if existing is not None and existing.is_expired:
                del self._locks[lk]
            return None
        return existing.owner

    def get_lock(self, scope: LockScope, key: str) -> LockRecord | None:
        lk = self._lock_key(scope, key)
        existing = self._locks.get(lk)
        if existing is None or existing.is_expired:
            if existing is not None and existing.is_expired:
                del self._locks[lk]
            return None
        return existing

    def list_locks(self, scope: LockScope | None = None) -> list[LockRecord]:
        result: list[LockRecord] = []
        expired_keys: list[str] = []
        for lk, record in self._locks.items():
            if record.is_expired:
                expired_keys.append(lk)
                continue
            if scope is None or record.scope == scope:
                result.append(record)
        for k in expired_keys:
            del self._locks[k]
        return result

    def clear_expired(self) -> int:
        before = len(self._locks)
        self._locks = {k: v for k, v in self._locks.items() if not v.is_expired}
        return before - len(self._locks)

    def clear(self) -> None:
        self._locks.clear()
