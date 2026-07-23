from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .envelope import InteractionEnvelope


@dataclass
class InteractionContext:
    interaction: InteractionEnvelope | None = None
    actor_id: str = ""
    user_id: str = ""
    contact_id: str = ""
    channel_identity: str = ""
    session_id: str = ""
    conversation_id: str = ""
    project_id: str = ""
    profile_id: str = ""
    project_brain_state: str = ""
    current_stage: str = ""
    current_action: str = ""
    feature_flags: dict[str, bool] = field(default_factory=dict)
    shadow_mode: bool = False
    correlation_id: str = ""
    causation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
