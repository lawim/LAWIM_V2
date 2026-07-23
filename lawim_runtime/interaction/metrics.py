from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class InteractionMetrics:
    interaction_received_total: int = 0
    interaction_processed_total: int = 0
    interaction_failed_total: int = 0
    interaction_duplicate_total: int = 0
    interaction_latency_ms: float = 0.0
    identity_resolution_total: int = 0
    identity_resolution_failed_total: int = 0
    project_resolution_total: int = 0
    project_resolution_ambiguous_total: int = 0
    session_created_total: int = 0
    session_resumed_total: int = 0
    session_expired_total: int = 0
    profile_patch_created_total: int = 0
    response_plan_created_total: int = 0
    delivery_requested_total: int = 0
    delivery_sent_total: int = 0
    delivery_failed_total: int = 0
    delivery_latency_ms: float = 0.0
    double_response_prevented_total: int = 0
    v2_v3_divergence_total: int = 0
    safe_fallback_total: int = 0
    handover_triggered_total: int = 0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "interaction_received_total": self.interaction_received_total,
            "interaction_processed_total": self.interaction_processed_total,
            "interaction_failed_total": self.interaction_failed_total,
            "interaction_duplicate_total": self.interaction_duplicate_total,
            "interaction_latency_ms": round(self.interaction_latency_ms, 2),
            "identity_resolution_total": self.identity_resolution_total,
            "identity_resolution_failed_total": self.identity_resolution_failed_total,
            "project_resolution_total": self.project_resolution_total,
            "project_resolution_ambiguous_total": self.project_resolution_ambiguous_total,
            "session_created_total": self.session_created_total,
            "session_resumed_total": self.session_resumed_total,
            "session_expired_total": self.session_expired_total,
            "profile_patch_created_total": self.profile_patch_created_total,
            "response_plan_created_total": self.response_plan_created_total,
            "delivery_requested_total": self.delivery_requested_total,
            "delivery_sent_total": self.delivery_sent_total,
            "delivery_failed_total": self.delivery_failed_total,
            "delivery_latency_ms": round(self.delivery_latency_ms, 2),
            "double_response_prevented_total": self.double_response_prevented_total,
            "v2_v3_divergence_total": self.v2_v3_divergence_total,
            "safe_fallback_total": self.safe_fallback_total,
            "handover_triggered_total": self.handover_triggered_total,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.interaction_received_total = 0
        self.interaction_processed_total = 0
        self.interaction_failed_total = 0
        self.interaction_duplicate_total = 0
        self.interaction_latency_ms = 0.0
        self.identity_resolution_total = 0
        self.identity_resolution_failed_total = 0
        self.project_resolution_total = 0
        self.project_resolution_ambiguous_total = 0
        self.session_created_total = 0
        self.session_resumed_total = 0
        self.session_expired_total = 0
        self.profile_patch_created_total = 0
        self.response_plan_created_total = 0
        self.delivery_requested_total = 0
        self.delivery_sent_total = 0
        self.delivery_failed_total = 0
        self.delivery_latency_ms = 0.0
        self.double_response_prevented_total = 0
        self.v2_v3_divergence_total = 0
        self.safe_fallback_total = 0
        self.handover_triggered_total = 0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()
