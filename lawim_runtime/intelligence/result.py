from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class AIResultStatus(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    INVALID_OUTPUT = "INVALID_OUTPUT"
    UNSAFE_OUTPUT = "UNSAFE_OUTPUT"
    TIMEOUT = "TIMEOUT"
    PROVIDER_ERROR = "PROVIDER_ERROR"
    RATE_LIMITED = "RATE_LIMITED"
    UNAVAILABLE = "UNAVAILABLE"
    FALLBACK_SUCCESS = "FALLBACK_SUCCESS"
    FAILED = "FAILED"


@dataclass
class AIUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0
    latency_ms: float = 0.0


@dataclass
class AIResult:
    result_id: str = field(default_factory=lambda: uuid4().hex[:16])
    request_id: str = ""
    status: AIResultStatus = AIResultStatus.FAILED
    task_type: str = ""
    structured_output: dict[str, Any] | None = None
    text_output: str = ""
    provider: str = ""
    model: str = ""
    prompt_version: str = ""
    schema_version: str = ""
    confidence: float = 0.0
    warnings: list[str] = field(default_factory=list)
    safety_flags: list[str] = field(default_factory=list)
    citations: list[dict[str, Any]] = field(default_factory=list)
    usage: AIUsage | None = None
    latency_ms: float = 0.0
    fallback_used: bool = False
    fallback_chain: list[str] = field(default_factory=list)
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
