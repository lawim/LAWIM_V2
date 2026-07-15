from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class MemoryType(str, Enum):
    CONVERSATION = "CONVERSATION"
    CASE = "CASE"
    USER_PREFERENCE = "USER_PREFERENCE"
    RELATIONSHIP = "RELATIONSHIP"
    AGENT_WORKING = "AGENT_WORKING"
    KNOWLEDGE_REFERENCE = "KNOWLEDGE_REFERENCE"
    LEARNING_REFERENCE = "LEARNING_REFERENCE"


@dataclass
class MemoryEntry:
    entry_id: str = ""
    memory_type: MemoryType = MemoryType.CONVERSATION
    key: str = ""
    value: str = ""
    actor_id: str = ""
    conversation_id: str = ""
    case_id: str = ""
    ttl_days: int = 365
    created_at: str = ""
    expires_at: str = ""

    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        try:
            exp = datetime.fromisoformat(self.expires_at)
            return datetime.now(timezone.utc) > exp
        except (ValueError, TypeError):
            return False


@dataclass
class MemorySummary:
    summary_id: str = ""
    conversation_id: str = ""
    content: str = ""
    fact_count: int = 0
    created_at: str = ""
    version: int = 1


@dataclass
class IntelligenceReview:
    review_id: str = ""
    proposal_ids: list[str] = field(default_factory=list)
    reviewer_id: str = ""
    decision: str = "PENDING"
    comments: str = ""
    risk_level: str = "LOW"
    reviewed_at: str = ""

    def approve(self) -> None:
        self.decision = "APPROVED"
        self.reviewed_at = datetime.now(timezone.utc).isoformat()

    def reject(self) -> None:
        self.decision = "REJECTED"
        self.reviewed_at = datetime.now(timezone.utc).isoformat()


class GovernanceAction(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REQUEST_CHANGES = "REQUEST_CHANGES"
    DEFER = "DEFER"


@dataclass
class GovernanceRecord:
    record_id: str = ""
    target_type: str = ""
    target_id: str = ""
    action: GovernanceAction = GovernanceAction.APPROVE
    actor_id: str = ""
    justification: str = ""
    created_at: str = ""


@dataclass
class MemoryRetentionRule:
    memory_type: MemoryType = MemoryType.CONVERSATION
    retention_days: int = 365
    auto_summarize: bool = True
    auto_delete: bool = False
    requires_approval: bool = False
