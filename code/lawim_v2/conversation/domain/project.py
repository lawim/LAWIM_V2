from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ProjectStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


@dataclass
class ProjectInfo:
    project_id: int | None = None
    user_id: int | None = None
    intent: str | None = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    name: str = ""
    facts: dict[str, Any] = field(default_factory=dict)
    created_at: str | None = None
    updated_at: str | None = None
