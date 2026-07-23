from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .envelope import InteractionEnvelope


class InteractionMode(str, Enum):
    V2_ONLY = "V2_ONLY"
    V3_SHADOW = "V3_SHADOW"
    V3_CANARY = "V3_CANARY"
    V3_PRIMARY_WITH_V2_FALLBACK = "V3_PRIMARY_WITH_V2_FALLBACK"
    V3_ONLY = "V3_ONLY"


@dataclass
class InteractionModeRouter:
    mode: InteractionMode = InteractionMode.V2_ONLY
    canary_users: set[str] = field(default_factory=set)
    canary_channels: set[str] = field(default_factory=set)
    canary_projects: set[str] = field(default_factory=set)

    def resolve_mode(
        self,
        envelope: InteractionEnvelope | None = None,
        user_id: str = "",
        project_id: str = "",
    ) -> InteractionMode:
        if self.mode == InteractionMode.V2_ONLY:
            return InteractionMode.V2_ONLY
        if self.mode == InteractionMode.V3_SHADOW:
            return InteractionMode.V3_SHADOW
        if self.mode == InteractionMode.V3_ONLY:
            return InteractionMode.V3_ONLY
        if self.mode == InteractionMode.V3_PRIMARY_WITH_V2_FALLBACK:
            return InteractionMode.V3_PRIMARY_WITH_V2_FALLBACK
        if self.mode == InteractionMode.V3_CANARY:
            if user_id in self.canary_users:
                return InteractionMode.V3_CANARY
            if envelope and envelope.channel in self.canary_channels:
                return InteractionMode.V3_CANARY
            if project_id in self.canary_projects:
                return InteractionMode.V3_CANARY
            return InteractionMode.V2_ONLY
        return InteractionMode.V2_ONLY

    def is_v3_active(self, envelope: InteractionEnvelope | None = None, user_id: str = "", project_id: str = "") -> bool:
        mode = self.resolve_mode(envelope, user_id, project_id)
        return mode in (
            InteractionMode.V3_SHADOW,
            InteractionMode.V3_CANARY,
            InteractionMode.V3_PRIMARY_WITH_V2_FALLBACK,
            InteractionMode.V3_ONLY,
        )

    def is_shadow(self, envelope: InteractionEnvelope | None = None, user_id: str = "", project_id: str = "") -> bool:
        mode = self.resolve_mode(envelope, user_id, project_id)
        return mode == InteractionMode.V3_SHADOW
