from __future__ import annotations

from .base import AIProvider, AIProviderRequest, AIProviderResponse, AIModelCapabilities, ModelCapability, LatencyClass, CostClass, DataPolicy


class DeterministicProvider(AIProvider):
    provider_name: str = "deterministic"

    def __init__(self) -> None:
        self._capabilities = AIModelCapabilities(
            model_name="deterministic-v1",
            provider="deterministic",
            capabilities=set(),
            context_window=0,
            max_output_tokens=0,
            latency_class=LatencyClass.FAST,
            cost_class=CostClass.LOW,
            data_policy=DataPolicy.NO_TRAINING,
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        return AIProviderResponse(
            model="deterministic-v1",
            provider="deterministic",
            success=True,
            text="",
            metadata={"mode": "deterministic"},
        )

    def health(self) -> bool:
        return True

    @property
    def capabilities(self) -> AIModelCapabilities:
        return self._capabilities
