from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any

from .constants import FINANCIAL_EVENT_TYPES


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def payload_hash(payload: Any) -> str:
    return sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def build_event(
    event_type: str,
    *,
    source: str,
    actor: dict[str, object] | None = None,
    obj: dict[str, object] | None = None,
    data: dict[str, object] | None = None,
    idempotency_key: str | None = None,
    correlation_id: str | None = None,
    causality_id: str | None = None,
    version: int = 1,
) -> dict[str, object]:
    normalized_type = event_type if event_type in FINANCIAL_EVENT_TYPES else "event.unknown"
    payload = {
        "id": f"fin-evt-{sha256(f'{normalized_type}|{source}|{utcnow()}'.encode('utf-8')).hexdigest()[:12]}",
        "type": normalized_type,
        "version": version,
        "date": utcnow(),
        "source": source,
        "actor": actor or {},
        "object": obj or {},
        "data": data or {},
        "key": idempotency_key,
        "correlation": correlation_id,
        "causality": causality_id,
    }
    return payload


@dataclass(frozen=True, slots=True)
class FinancialEventEnvelope:
    event_type: str
    source: str
    actor: dict[str, object] | None = None
    obj: dict[str, object] | None = None
    data: dict[str, object] | None = None
    idempotency_key: str | None = None
    correlation_id: str | None = None
    causality_id: str | None = None
    version: int = 1

    def to_dict(self) -> dict[str, object]:
        return build_event(
            self.event_type,
            source=self.source,
            actor=self.actor,
            obj=self.obj,
            data=self.data,
            idempotency_key=self.idempotency_key,
            correlation_id=self.correlation_id,
            causality_id=self.causality_id,
            version=self.version,
        )
