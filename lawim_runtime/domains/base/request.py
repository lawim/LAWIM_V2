from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DomainRuntimeRequest:
    request_id: str = ""
    action_code: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""
    causation_id: str = ""
    idempotency_key: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
