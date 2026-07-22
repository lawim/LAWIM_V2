from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class Snapshot:
    snapshot_id: str = field(default_factory=lambda: uuid4().hex[:16])
    project_id: str = ""
    state: dict[str, Any] = field(default_factory=dict)
    version: int = 1
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
