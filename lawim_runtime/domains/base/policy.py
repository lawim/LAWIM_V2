from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DomainRuntimePolicy:
    idempotent: bool = False
    max_attempts: int = 1
    timeout_seconds: float = 30.0
    requires_verification: bool = False
    requires_compensation: bool = False
    shadow_mode: bool = False
    feature_flag: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
