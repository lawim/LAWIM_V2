from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AIContext:
    context_id: str = ""
    request_id: str = ""
    interaction_id: str = ""
    project_id: str = ""
    session_id: str = ""
    conversation_id: str = ""
    language: str = "fr"
    allowed_fields: tuple[str, ...] = ()
    allowed_sources: tuple[str, ...] = ()
    feature_flags: dict[str, bool] = field(default_factory=dict)
    shadow_mode: bool = False
    mode: str = "deterministic"
    correlation_id: str = ""
    causation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
