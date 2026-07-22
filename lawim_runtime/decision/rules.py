from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DecisionRule:
    rule_id: str = ""
    name: str = ""
    priority: int = 100
    profile_types: tuple[str, ...] = ()
    stages: tuple[str, ...] = ()
    condition: str = ""
    action: str = ""
    stop_processing: bool = False
    severity: str = "NORMAL"
    version: int = 1
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
