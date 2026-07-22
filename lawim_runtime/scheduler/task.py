from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskPriority(Enum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3


@dataclass
class Task:
    task_id: str = ""
    engine_name: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: list[str] = field(default_factory=list)
    timeout_seconds: float = 30.0
    retry_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
