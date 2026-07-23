from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class IdentityStatus(str, Enum):
    RESOLVED = "RESOLVED"
    ANONYMOUS = "ANONYMOUS"
    AMBIGUOUS = "AMBIGUOUS"
    CONFLICTED = "CONFLICTED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class ChannelIdentity:
    channel: str = ""
    external_user_id: str = ""
    raw_sender: str = ""
    channel_identity_key: str = ""

    @property
    def identity_key(self) -> str:
        if self.channel_identity_key:
            return self.channel_identity_key
        return f"{self.channel}:{self.external_user_id or self.raw_sender}"


@dataclass
class IdentityResolutionResult:
    identity_id: str = field(default_factory=lambda: uuid4().hex[:16])
    status: IdentityStatus = IdentityStatus.ANONYMOUS
    actor_id: str = ""
    user_id: str = ""
    contact_id: str = ""
    channel_identity: ChannelIdentity | None = None
    confidence: float = 0.0
    matched_identities: list[str] = field(default_factory=list)
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class IdentityResolver:
    def __init__(self) -> None:
        self._channel_map: dict[str, str] = {}
        self._user_channels: dict[str, list[str]] = {}

    def resolve(self, channel: str, external_user_id: str, raw_sender: str) -> IdentityResolutionResult:
        identity_key = f"{channel}:{external_user_id or raw_sender}"
        user_id = self._channel_map.get(identity_key)

        if user_id:
            channels = self._user_channels.get(user_id, [])
            return IdentityResolutionResult(
                status=IdentityStatus.RESOLVED,
                actor_id=user_id,
                user_id=user_id,
                contact_id=user_id,
                channel_identity=ChannelIdentity(
                    channel=channel,
                    external_user_id=external_user_id,
                    raw_sender=raw_sender,
                ),
                confidence=1.0,
                matched_identities=channels,
            )

        return IdentityResolutionResult(
            status=IdentityStatus.ANONYMOUS,
            channel_identity=ChannelIdentity(
                channel=channel,
                external_user_id=external_user_id,
                raw_sender=raw_sender,
            ),
            confidence=0.0,
        )

    def link_channel_to_user(self, user_id: str, channel: str, external_user_id: str, raw_sender: str = "") -> None:
        identity_key = f"{channel}:{external_user_id or raw_sender}"
        self._channel_map[identity_key] = user_id
        if user_id not in self._user_channels:
            self._user_channels[user_id] = []
        if identity_key not in self._user_channels[user_id]:
            self._user_channels[user_id].append(identity_key)

    def get_user_channels(self, user_id: str) -> list[str]:
        return list(self._user_channels.get(user_id, []))

    def count(self) -> int:
        return len(self._channel_map)
