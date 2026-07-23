from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ModelCapability(str, Enum):
    STRUCTURED_OUTPUT = "structured_output"
    TOOL_CALLING = "tool_calling"
    VISION = "vision"
    AUDIO = "audio"
    STREAMING = "streaming"
    JSON_SCHEMA = "json_schema"


class LatencyClass(str, Enum):
    FAST = "fast"
    MEDIUM = "medium"
    SLOW = "slow"


class CostClass(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DataPolicy(str, Enum):
    EU_ONLY = "eu_only"
    NO_TRAINING = "no_training"
    STANDARD = "standard"
    UNKNOWN = "unknown"


@dataclass
class AIModelCapabilities:
    model_name: str = ""
    provider: str = ""
    capabilities: set[ModelCapability] = field(default_factory=set)
    context_window: int = 4096
    max_output_tokens: int = 1024
    languages: list[str] = field(default_factory=lambda: ["fr", "en"])
    latency_class: LatencyClass = LatencyClass.MEDIUM
    cost_class: CostClass = CostClass.MEDIUM
    data_policy: DataPolicy = DataPolicy.STANDARD
    version: str = "1.0"


@dataclass
class AIProviderRequest:
    request_id: str = field(default_factory=lambda: uuid4().hex[:16])
    system_prompt: str = ""
    user_prompt: str = ""
    response_schema: dict[str, Any] | None = None
    messages: list[dict[str, str]] = field(default_factory=list)
    model: str = ""
    temperature: float = 0.1
    max_tokens: int = 1024
    timeout_ms: int = 30000
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AIProviderResponse:
    response_id: str = field(default_factory=lambda: uuid4().hex[:16])
    text: str = ""
    structured: dict[str, Any] | None = None
    model: str = ""
    provider: str = ""
    usage: dict[str, int] = field(default_factory=dict)
    latency_ms: float = 0.0
    success: bool = False
    error: str = ""
    error_category: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class AIProvider(ABC):
    provider_name: str = ""

    @abstractmethod
    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        ...

    @abstractmethod
    def health(self) -> bool:
        ...

    @property
    @abstractmethod
    def capabilities(self) -> AIModelCapabilities:
        ...
