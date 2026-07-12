from __future__ import annotations

from datetime import datetime, timezone
import uuid

from ..contracts import AIRequest, AIResponse, CostEstimate, ProviderHealth, UsageStatus
from ..models import FallbackResolution


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class InternalFallbackProvider:
    name = "internal"

    def __init__(self, *, enabled: bool, resolver) -> None:
        self.enabled = enabled
        self.resolver = resolver

    def is_enabled(self) -> bool:
        return self.enabled

    def health_check(self) -> ProviderHealth:
        return ProviderHealth(
            provider=self.name,
            model="internal-fallback",
            enabled=self.enabled,
            available=True,
            state="ready" if self.enabled else "disabled",
            checked_at=_utcnow(),
            latency_ms=0,
            details={"type": "local_fallback"},
        )

    def estimate_cost(self, request: AIRequest) -> CostEstimate:
        return CostEstimate(provider=self.name, model="internal-fallback", input_tokens=0, output_tokens=0, estimated_cost=0.0)

    def get_usage_status(self) -> UsageStatus:
        return UsageStatus(provider=self.name, model="internal-fallback")

    def generate(self, request: AIRequest) -> AIResponse:
        resolution: FallbackResolution = self.resolver.resolve(request)
        request_id = request.request_id
        provider_request_id = f"fallback-{uuid.uuid4().hex[:12]}"
        return AIResponse(
            provider=self.name,
            model="internal-fallback",
            success=True,
            content=resolution.content,
            latency_ms=0,
            input_tokens=0,
            output_tokens=0,
            estimated_cost=0.0,
            finish_reason="fallback",
            error_type=None,
            error_code=None,
            retryable=False,
            fallback_required=False,
            request_id=request_id,
            provider_request_id=provider_request_id,
            valid=True,
            complete=True,
            relevant=True,
            safe=True,
            well_formed=True,
            confidence_score=resolution.confidence or 0.55,
            metadata=resolution.to_dict(),
        )
