from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from ..delivery import DeliveryResult
from ..deduplication import DeduplicationStatus
from ..envelope import InteractionEnvelope
from ..session import InteractionSession


class SessionRepository(ABC):

    @abstractmethod
    def save(self, session: InteractionSession) -> None:
        ...

    @abstractmethod
    def get(self, session_id: str) -> InteractionSession | None:
        ...

    @abstractmethod
    def list_by_user(self, user_id: str) -> list[InteractionSession]:
        ...

    @abstractmethod
    def update(self, session: InteractionSession) -> None:
        ...


class InMemorySessionRepository(SessionRepository):
    def __init__(self) -> None:
        self._sessions: dict[str, InteractionSession] = {}
        self._user_index: dict[str, list[str]] = {}

    def save(self, session: InteractionSession) -> None:
        self._sessions[session.session_id] = session
        if session.user_id not in self._user_index:
            self._user_index[session.user_id] = []
        if session.session_id not in self._user_index[session.user_id]:
            self._user_index[session.user_id].append(session.session_id)

    def get(self, session_id: str) -> InteractionSession | None:
        return self._sessions.get(session_id)

    def list_by_user(self, user_id: str) -> list[InteractionSession]:
        sids = self._user_index.get(user_id, [])
        return [self._sessions[sid] for sid in sids if sid in self._sessions]

    def update(self, session: InteractionSession) -> None:
        self._sessions[session.session_id] = session


class ChannelIdentityRepository(ABC):

    @abstractmethod
    def save(self, channel: str, external_user_id: str, user_id: str) -> None:
        ...

    @abstractmethod
    def resolve(self, channel: str, external_user_id: str) -> str | None:
        ...

    @abstractmethod
    def list_channels_for_user(self, user_id: str) -> list[str]:
        ...


class InMemoryChannelIdentityRepository(ChannelIdentityRepository):
    def __init__(self) -> None:
        self._channel_map: dict[str, str] = {}
        self._user_channels: dict[str, list[str]] = {}

    def save(self, channel: str, external_user_id: str, user_id: str) -> None:
        key = f"{channel}:{external_user_id}"
        self._channel_map[key] = user_id
        if user_id not in self._user_channels:
            self._user_channels[user_id] = []
        if key not in self._user_channels[user_id]:
            self._user_channels[user_id].append(key)

    def resolve(self, channel: str, external_user_id: str) -> str | None:
        key = f"{channel}:{external_user_id}"
        return self._channel_map.get(key)

    def list_channels_for_user(self, user_id: str) -> list[str]:
        return list(self._user_channels.get(user_id, []))


class DeduplicationRepository(ABC):

    @abstractmethod
    def is_duplicate(self, key: str) -> bool:
        ...

    @abstractmethod
    def mark_seen(self, key: str) -> None:
        ...

    @abstractmethod
    def count(self) -> int:
        ...


class InMemoryDeduplicationRepository(DeduplicationRepository):
    def __init__(self) -> None:
        self._seen: dict[str, str] = {}

    def is_duplicate(self, key: str) -> bool:
        if key in self._seen:
            return True
        return False

    def mark_seen(self, key: str) -> None:
        self._seen[key] = datetime.now(timezone.utc).isoformat()

    def count(self) -> int:
        return len(self._seen)


class DeliveryRepository(ABC):

    @abstractmethod
    def save(self, result: DeliveryResult) -> None:
        ...

    @abstractmethod
    def get(self, delivery_id: str) -> DeliveryResult | None:
        ...

    @abstractmethod
    def list_by_correlation(self, correlation_id: str) -> list[DeliveryResult]:
        ...


class InMemoryDeliveryRepository(DeliveryRepository):
    def __init__(self) -> None:
        self._results: dict[str, DeliveryResult] = {}
        self._correlation_index: dict[str, list[str]] = {}

    def save(self, result: DeliveryResult) -> None:
        self._results[result.delivery_id] = result
        if result.correlation_id:
            if result.correlation_id not in self._correlation_index:
                self._correlation_index[result.correlation_id] = []
            if result.delivery_id not in self._correlation_index[result.correlation_id]:
                self._correlation_index[result.correlation_id].append(result.delivery_id)

    def get(self, delivery_id: str) -> DeliveryResult | None:
        return self._results.get(delivery_id)

    def list_by_correlation(self, correlation_id: str) -> list[DeliveryResult]:
        dids = self._correlation_index.get(correlation_id, [])
        return [self._results[did] for did in dids if did in self._results]


class DivergenceRepository(ABC):

    @abstractmethod
    def save(self, record: Any) -> None:
        ...

    @abstractmethod
    def list_by_correlation(self, correlation_id: str) -> list[Any]:
        ...

    @abstractmethod
    def count(self) -> int:
        ...


class InMemoryDivergenceRepository(DivergenceRepository):
    def __init__(self) -> None:
        self._records: list[Any] = []
        self._correlation_index: dict[str, list[int]] = {}

    def save(self, record: Any) -> None:
        idx = len(self._records)
        self._records.append(record)
        corr_id = getattr(record, "correlation_id", "")
        if corr_id:
            if corr_id not in self._correlation_index:
                self._correlation_index[corr_id] = []
            self._correlation_index[corr_id].append(idx)

    def list_by_correlation(self, correlation_id: str) -> list[Any]:
        indices = self._correlation_index.get(correlation_id, [])
        return [self._records[i] for i in indices if i < len(self._records)]

    def count(self) -> int:
        return len(self._records)
