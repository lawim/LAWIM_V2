from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class IdempotencyRecord:
    idempotency_key: str = ""
    execution_id: str = ""
    status: str = "PENDING"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    checksum: str = ""

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc).isoformat()


class IdempotencyConflictError(Exception):
    pass


class IdempotencyManager:
    def __init__(self) -> None:
        self._records: dict[str, IdempotencyRecord] = {}

    def generate_key(self, namespace: str, identifier: str) -> str:
        import hashlib
        raw = f"{namespace}:{identifier}:{uuid4().hex[:8]}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    def reserve_key(
        self,
        idempotency_key: str,
        execution_id: str,
        checksum: str = "",
    ) -> IdempotencyRecord:
        existing = self._records.get(idempotency_key)
        if existing is not None:
            if existing.execution_id != execution_id:
                raise IdempotencyConflictError(
                    f"Key '{idempotency_key}' already reserved by execution "
                    f"'{existing.execution_id}'"
                )
            return existing
        record = IdempotencyRecord(
            idempotency_key=idempotency_key,
            execution_id=execution_id,
            status="RESERVED",
            checksum=checksum,
        )
        self._records[idempotency_key] = record
        return record

    def get_record(self, idempotency_key: str) -> IdempotencyRecord | None:
        return self._records.get(idempotency_key)

    def mark_started(self, idempotency_key: str) -> IdempotencyRecord | None:
        record = self._records.get(idempotency_key)
        if record is None:
            return None
        record.status = "STARTED"
        record.touch()
        return record

    def mark_succeeded(self, idempotency_key: str) -> IdempotencyRecord | None:
        record = self._records.get(idempotency_key)
        if record is None:
            return None
        record.status = "SUCCEEDED"
        record.touch()
        return record

    def mark_failed(self, idempotency_key: str) -> IdempotencyRecord | None:
        record = self._records.get(idempotency_key)
        if record is None:
            return None
        record.status = "FAILED"
        record.touch()
        return record

    def release_key(self, idempotency_key: str) -> bool:
        record = self._records.get(idempotency_key)
        if record is None:
            return False
        self._records.pop(idempotency_key, None)
        return True

    def has_key(self, idempotency_key: str) -> bool:
        return idempotency_key in self._records

    def count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records.clear()
