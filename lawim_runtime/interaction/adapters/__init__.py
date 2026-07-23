from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from ..envelope import InteractionEnvelope, MessageType
from ..response_plan import InteractionResponsePlan


@dataclass
class ChannelDeliveryRequest:
    channel: str = ""
    recipient_id: str = ""
    text: str = ""
    parse_mode: str = "text"
    response_plan: InteractionResponsePlan | None = None
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChannelDeliveryResult:
    success: bool = False
    provider_message_id: str = ""
    error: str = ""
    status_code: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


class InboundChannelAdapter(ABC):

    @abstractmethod
    def parse_webhook(self, raw_payload: dict[str, Any], headers: dict[str, str] | None = None) -> InteractionEnvelope | None:
        ...

    @abstractmethod
    def extract_identifiers(self, raw_payload: dict[str, Any]) -> dict[str, str]:
        ...


class OutboundChannelAdapter(ABC):

    @abstractmethod
    def send(self, request: ChannelDeliveryRequest) -> ChannelDeliveryResult:
        ...

    @abstractmethod
    def validate_webhook(self, headers: dict[str, str], raw_body: bytes) -> bool:
        ...


class ChannelAdapter(InboundChannelAdapter, OutboundChannelAdapter, ABC):
    channel_name: str = ""
