from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class RetentionCategory(str, Enum):
    TURN_MEMORY = "TURN_MEMORY"
    CONVERSATION_MEMORY = "CONVERSATION_MEMORY"
    CASE_MEMORY = "CASE_MEMORY"
    USER_PREFERENCE = "USER_PREFERENCE"
    RELATIONSHIP_MEMORY = "RELATIONSHIP_MEMORY"
    CONSENT_RECORD = "CONSENT_RECORD"
    HANDOVER_RECORD = "HANDOVER_RECORD"
    AUDIT_LOG = "AUDIT_LOG"
    TRANSACTION_RECORD = "TRANSACTION_RECORD"


@dataclass
class MemoryRetentionPolicy:
    category: RetentionCategory = RetentionCategory.CONVERSATION_MEMORY
    retention_days: int = 365
    auto_archive: bool = False
    auto_anonymize: bool = False
    auto_delete: bool = False
    requires_approval: bool = False
    legal_exception: bool = False
    legal_exception_note: str = ""

    def should_retain(self, created_at: str) -> bool:
        try:
            created = datetime.fromisoformat(created_at)
            age = datetime.now(timezone.utc) - created
            return age.days < self.retention_days
        except (ValueError, TypeError):
            return True


RETENTION_POLICIES: dict[RetentionCategory, MemoryRetentionPolicy] = {
    RetentionCategory.TURN_MEMORY: MemoryRetentionPolicy(
        category=RetentionCategory.TURN_MEMORY,
        retention_days=7,
        auto_delete=True,
    ),
    RetentionCategory.CONVERSATION_MEMORY: MemoryRetentionPolicy(
        category=RetentionCategory.CONVERSATION_MEMORY,
        retention_days=365,
        auto_archive=True,
        auto_anonymize=True,
    ),
    RetentionCategory.CASE_MEMORY: MemoryRetentionPolicy(
        category=RetentionCategory.CASE_MEMORY,
        retention_days=1825,
        auto_archive=True,
    ),
    RetentionCategory.USER_PREFERENCE: MemoryRetentionPolicy(
        category=RetentionCategory.USER_PREFERENCE,
        retention_days=1825,
    ),
    RetentionCategory.RELATIONSHIP_MEMORY: MemoryRetentionPolicy(
        category=RetentionCategory.RELATIONSHIP_MEMORY,
        retention_days=1825,
    ),
    RetentionCategory.CONSENT_RECORD: MemoryRetentionPolicy(
        category=RetentionCategory.CONSENT_RECORD,
        retention_days=3650,
        legal_exception=True,
        legal_exception_note="Consent records retained for legal compliance",
    ),
    RetentionCategory.HANDOVER_RECORD: MemoryRetentionPolicy(
        category=RetentionCategory.HANDOVER_RECORD,
        retention_days=1825,
        auto_archive=True,
    ),
    RetentionCategory.AUDIT_LOG: MemoryRetentionPolicy(
        category=RetentionCategory.AUDIT_LOG,
        retention_days=3650,
        legal_exception=True,
        legal_exception_note="Audit logs retained for legal compliance",
    ),
    RetentionCategory.TRANSACTION_RECORD: MemoryRetentionPolicy(
        category=RetentionCategory.TRANSACTION_RECORD,
        retention_days=3650,
        legal_exception=True,
        legal_exception_note="Transaction records retained for legal compliance",
    ),
}


@dataclass
class RetentionAuditLog:
    log_id: str = ""
    action: str = ""
    category: str = ""
    target_id: str = ""
    actor: str = "system"
    reason: str = ""
    performed_at: str = ""
    details: dict[str, Any] = field(default_factory=dict)
