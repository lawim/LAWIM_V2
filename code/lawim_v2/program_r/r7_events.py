from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class EventPrivacy(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"


@dataclass
class EnrichedEvent:
    event_id: str = ""
    event_type: str = ""
    entity_type: str = ""
    entity_id: str = ""
    actor_id: str = ""
    previous_state: str = ""
    new_state: str = ""
    transition: str = ""
    source: str = ""
    correlation_id: str = ""
    severity: str = "INFO"
    privacy_level: EventPrivacy = EventPrivacy.INTERNAL
    retention_days: int = 365
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = "1.0"
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"event_id": self.event_id, "event_type": self.event_type,
                "entity_type": self.entity_type, "actor_id": self.actor_id,
                "transition": self.transition, "severity": self.severity}


EVENT_CATALOG_ENTRIES: list[dict[str, Any]] = [
    {"type": "user.created", "entity": "user", "privacy": "INTERNAL"},
    {"type": "user.updated", "entity": "user", "privacy": "INTERNAL"},
    {"type": "property.created", "entity": "property", "privacy": "INTERNAL"},
    {"type": "property.state_changed", "entity": "property", "privacy": "INTERNAL"},
    {"type": "match.created", "entity": "match", "privacy": "RESTRICTED"},
    {"type": "match.consented", "entity": "match", "privacy": "RESTRICTED"},
    {"type": "consent.granted", "entity": "consent", "privacy": "CONFIDENTIAL"},
    {"type": "consent.revoked", "entity": "consent", "privacy": "CONFIDENTIAL"},
    {"type": "payment.initiated", "entity": "payment", "privacy": "RESTRICTED"},
    {"type": "payment.confirmed", "entity": "payment", "privacy": "RESTRICTED"},
    {"type": "conversion.recorded", "entity": "conversion", "privacy": "INTERNAL"},
    {"type": "agent.invoked", "entity": "agent", "privacy": "INTERNAL"},
    {"type": "permission.denied", "entity": "permission", "privacy": "RESTRICTED"},
    {"type": "security.alert", "entity": "security", "privacy": "CONFIDENTIAL"},
    {"type": "learning.feedback", "entity": "learning", "privacy": "INTERNAL"},
]


@dataclass
class AuditTrailEntry:
    audit_id: str = ""
    actor_id: str = ""
    action: str = ""
    target_type: str = ""
    target_id: str = ""
    previous_value: str = ""
    new_value: str = ""
    ip_address: str = ""
    user_agent: str = ""
    correlation_id: str = ""
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"audit_id": self.audit_id, "actor_id": self.actor_id,
                "action": self.action, "target_type": self.target_type}


class PermissionLevel(str, Enum):
    N1_READ = "N1_READ"
    N2_CREATE = "N2_CREATE"
    N3_EDIT = "N3_EDIT"
    N4_APPROVE = "N4_APPROVE"


EDIT_TIERS: list[str] = ["OWN", "MANAGED", "ALL"]


@dataclass
class ApprovalWorkflow:
    approval_id: str = ""
    target_type: str = ""
    target_id: str = ""
    approver_role: str = ""
    status: str = "PENDING"
    reviewed_by: str = ""
    reviewed_at: str = ""

    def approve(self, reviewer: str) -> bool:
        if self.status == "PENDING":
            self.status = "APPROVED"
            self.reviewed_by = reviewer
            self.reviewed_at = datetime.now(timezone.utc).isoformat()
            return True
        return False

    def reject(self, reviewer: str) -> bool:
        if self.status == "PENDING":
            self.status = "REJECTED"
            self.reviewed_by = reviewer
            self.reviewed_at = datetime.now(timezone.utc).isoformat()
            return True
        return False


@dataclass
class RetentionPolicy:
    event_type: str = ""
    retention_days: int = 365
    auto_archive: bool = True
    auto_purge: bool = False

    def should_retain(self, created_at: str) -> bool:
        try:
            from datetime import datetime, timezone, timedelta
            dt = datetime.fromisoformat(created_at)
            age = datetime.now(timezone.utc) - dt
            return age.days < self.retention_days
        except (ValueError, TypeError):
            return True
