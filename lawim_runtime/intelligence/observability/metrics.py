from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AIMetrics:
    ai_request_total: int = 0
    ai_success_total: int = 0
    ai_failure_total: int = 0
    ai_fallback_total: int = 0
    ai_timeout_total: int = 0
    ai_rate_limited_total: int = 0
    ai_invalid_output_total: int = 0
    ai_unsafe_output_total: int = 0
    ai_schema_validation_failed_total: int = 0
    ai_prompt_injection_detected_total: int = 0
    ai_latency_ms: float = 0.0
    ai_input_tokens_total: int = 0
    ai_output_tokens_total: int = 0
    ai_cost_estimate: float = 0.0
    ai_provider_switch_total: int = 0
    ai_response_validation_failed_total: int = 0
    rag_query_total: int = 0
    rag_no_result_total: int = 0
    rag_citation_total: int = 0
    last_reset_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def snapshot(self) -> dict[str, Any]:
        return {
            "ai_request_total": self.ai_request_total,
            "ai_success_total": self.ai_success_total,
            "ai_failure_total": self.ai_failure_total,
            "ai_fallback_total": self.ai_fallback_total,
            "ai_timeout_total": self.ai_timeout_total,
            "ai_rate_limited_total": self.ai_rate_limited_total,
            "ai_invalid_output_total": self.ai_invalid_output_total,
            "ai_unsafe_output_total": self.ai_unsafe_output_total,
            "ai_schema_validation_failed_total": self.ai_schema_validation_failed_total,
            "ai_prompt_injection_detected_total": self.ai_prompt_injection_detected_total,
            "ai_latency_ms": round(self.ai_latency_ms, 2),
            "ai_input_tokens_total": self.ai_input_tokens_total,
            "ai_output_tokens_total": self.ai_output_tokens_total,
            "ai_cost_estimate": round(self.ai_cost_estimate, 4),
            "ai_provider_switch_total": self.ai_provider_switch_total,
            "ai_response_validation_failed_total": self.ai_response_validation_failed_total,
            "rag_query_total": self.rag_query_total,
            "rag_no_result_total": self.rag_no_result_total,
            "rag_citation_total": self.rag_citation_total,
            "last_reset_at": self.last_reset_at,
        }

    def reset(self) -> None:
        self.ai_request_total = 0
        self.ai_success_total = 0
        self.ai_failure_total = 0
        self.ai_fallback_total = 0
        self.ai_timeout_total = 0
        self.ai_rate_limited_total = 0
        self.ai_invalid_output_total = 0
        self.ai_unsafe_output_total = 0
        self.ai_schema_validation_failed_total = 0
        self.ai_prompt_injection_detected_total = 0
        self.ai_latency_ms = 0.0
        self.ai_input_tokens_total = 0
        self.ai_output_tokens_total = 0
        self.ai_cost_estimate = 0.0
        self.ai_provider_switch_total = 0
        self.ai_response_validation_failed_total = 0
        self.rag_query_total = 0
        self.rag_no_result_total = 0
        self.rag_citation_total = 0
        self.last_reset_at = datetime.now(timezone.utc).isoformat()


AIMetricsSnapshot = AIMetrics
