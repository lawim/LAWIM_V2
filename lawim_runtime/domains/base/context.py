from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .request import DomainRuntimeRequest


@dataclass
class DomainRuntimeContext:
    request: DomainRuntimeRequest = field(default_factory=DomainRuntimeRequest)
    runtime_name: str = ""
    services: dict[str, Any] = field(default_factory=dict)
    attempt_number: int = 0
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)
