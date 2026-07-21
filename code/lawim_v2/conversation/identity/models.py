from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class IdentityConfidence(str, Enum):
    VERIFIED = "VERIFIED"
    HIGH_CONFIDENCE = "HIGH_CONFIDENCE"
    PROBABLE = "PROBABLE"
    UNVERIFIED = "UNVERIFIED"
    CONFLICT = "CONFLICT"


class IdentitySource(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    USER_ID = "USER_ID"
    PHONE_VERIFIED = "PHONE_VERIFIED"
    EMAIL_VERIFIED = "EMAIL_VERIFIED"
    WHATSAPP_CHAT_ID = "WHATSAPP_CHAT_ID"
    TELEGRAM_USER_ID = "TELEGRAM_USER_ID"
    WEB_SESSION = "WEB_SESSION"
    AUTHENTICATED_ACCOUNT = "AUTHENTICATED_ACCOUNT"


@dataclass
class ResolvedIdentity:
    actor_id: str = ""
    internal_user_id: str | None = None
    confidence: IdentityConfidence = IdentityConfidence.UNVERIFIED
    sources: list[str] = field(default_factory=list)
    channels: list[str] = field(default_factory=list)
    phone: str | None = None
    email: str | None = None
    resolved_at: str = ""

    def can_auto_merge(self) -> bool:
        return self.confidence in {
            IdentityConfidence.VERIFIED,
            IdentityConfidence.HIGH_CONFIDENCE,
        }


@dataclass
class IdentityBinding:
    binding_id: str = ""
    actor_id: str = ""
    channel: str = ""
    channel_identifier: str = ""
    source: IdentitySource = IdentitySource.UNVERIFIED
    confidence: IdentityConfidence = IdentityConfidence.UNVERIFIED
    created_at: str = ""
    verified_at: str | None = None

    @property
    def binding_key(self) -> str:
        return f"{self.channel}:{self.channel_identifier}"


@dataclass
class CrossChannelConsent:
    consent_id: str = ""
    consent_type: str = "cross_channel_continuity"
    actor_id: str = ""
    source_channel: str = ""
    target_channel: str = ""
    status: str = "PENDING"
    granted_at: str | None = None
    expires_at: str | None = None
    revoked_at: str | None = None
    evidence: str = ""
    created_at: str = ""

    def is_active(self) -> bool:
        if self.status != "GRANTED":
            return False
        if self.expires_at:
            try:
                exp = datetime.fromisoformat(self.expires_at)
                if datetime.now(timezone.utc) > exp:
                    return False
            except (ValueError, TypeError):
                pass
        return True
