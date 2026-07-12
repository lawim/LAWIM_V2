from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class AIMessage:
    role: str
    content: str

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass(frozen=True, slots=True)
class AIRequest:
    request_id: str
    channel: str
    conversation_key: str
    text: str
    sanitized_text: str
    language: str = "fr"
    complexity: str = "simple"
    external_chat_id: str = ""
    external_user_id: str = ""
    message_id: str = ""
    thread_id: int | None = None
    contact_id: int | None = None
    organization_id: int | None = None
    context_messages: tuple[AIMessage, ...] = ()
    metadata: dict[str, object] = field(default_factory=dict)
    max_output_tokens: int = 512
    allow_retry: bool = False

    def to_prompt_messages(self) -> list[dict[str, str]]:
        return [message.to_dict() for message in self.context_messages]


@dataclass(frozen=True, slots=True)
class CostEstimate:
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    currency: str = "USD"

    def to_dict(self) -> dict[str, object]:
        return {
            "provider": self.provider,
            "model": self.model,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "estimated_cost": self.estimated_cost,
            "currency": self.currency,
        }


@dataclass(frozen=True, slots=True)
class ProviderHealth:
    provider: str
    model: str
    enabled: bool
    available: bool
    state: str
    checked_at: str
    latency_ms: int
    error_type: str | None = None
    error_code: str | None = None
    request_id: str | None = None
    provider_request_id: str | None = None
    credit_remaining: float | None = None
    credit_limit: float | None = None
    quota_status: str | None = None
    last_success_at: str | None = None
    last_failure_at: str | None = None
    details: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        payload = {
            "provider": self.provider,
            "model": self.model,
            "enabled": self.enabled,
            "available": self.available,
            "state": self.state,
            "checked_at": self.checked_at,
            "latency_ms": self.latency_ms,
            "error_type": self.error_type,
            "error_code": self.error_code,
            "request_id": self.request_id,
            "provider_request_id": self.provider_request_id,
            "credit_remaining": self.credit_remaining,
            "credit_limit": self.credit_limit,
            "quota_status": self.quota_status,
            "last_success_at": self.last_success_at,
            "last_failure_at": self.last_failure_at,
            "details": self.details,
        }
        return {key: value for key, value in payload.items() if value is not None}


@dataclass(frozen=True, slots=True)
class UsageStatus:
    provider: str
    model: str
    requests_today: int = 0
    tokens_today: int = 0
    estimated_cost_today: float = 0.0
    estimated_cost_month: float = 0.0
    credit_remaining: float | None = None
    credit_limit: float | None = None
    quota_status: str | None = None
    rate_limit_remaining: int | None = None
    rate_limit_reset: str | None = None
    last_success_at: str | None = None
    last_failure_at: str | None = None
    consecutive_failures: int = 0

    def to_dict(self) -> dict[str, object]:
        payload = {
            "provider": self.provider,
            "model": self.model,
            "requests_today": self.requests_today,
            "tokens_today": self.tokens_today,
            "estimated_cost_today": self.estimated_cost_today,
            "estimated_cost_month": self.estimated_cost_month,
            "credit_remaining": self.credit_remaining,
            "credit_limit": self.credit_limit,
            "quota_status": self.quota_status,
            "rate_limit_remaining": self.rate_limit_remaining,
            "rate_limit_reset": self.rate_limit_reset,
            "last_success_at": self.last_success_at,
            "last_failure_at": self.last_failure_at,
            "consecutive_failures": self.consecutive_failures,
        }
        return {key: value for key, value in payload.items() if value is not None}


@dataclass(frozen=True, slots=True)
class AIResponse:
    provider: str
    model: str
    success: bool
    content: str
    latency_ms: int
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    finish_reason: str | None
    error_type: str | None
    error_code: str | None
    retryable: bool
    fallback_required: bool
    request_id: str
    provider_request_id: str | None
    valid: bool
    complete: bool
    relevant: bool
    safe: bool
    well_formed: bool
    confidence_score: float
    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        payload = {
            "provider": self.provider,
            "model": self.model,
            "success": self.success,
            "content": self.content,
            "latency_ms": self.latency_ms,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "estimated_cost": self.estimated_cost,
            "finish_reason": self.finish_reason,
            "error_type": self.error_type,
            "error_code": self.error_code,
            "retryable": self.retryable,
            "fallback_required": self.fallback_required,
            "request_id": self.request_id,
            "provider_request_id": self.provider_request_id,
            "valid": self.valid,
            "complete": self.complete,
            "relevant": self.relevant,
            "safe": self.safe,
            "well_formed": self.well_formed,
            "confidence_score": self.confidence_score,
            "metadata": self.metadata,
        }
        return {key: value for key, value in payload.items() if value is not None}


@runtime_checkable
class AIProvider(Protocol):
    name: str

    def is_enabled(self) -> bool: ...

    def health_check(self) -> ProviderHealth: ...

    def generate(self, request: AIRequest) -> AIResponse: ...

    def estimate_cost(self, request: AIRequest) -> CostEstimate: ...

    def get_usage_status(self) -> UsageStatus: ...
