from __future__ import annotations

from .base import OpenAICompatibleProvider, ProviderHTTPConfig


class OpenAIProvider(OpenAICompatibleProvider):
    name = "openai"

    def __init__(self, *, api_key: str | None, model: str | None, enabled: bool, timeout_seconds: int) -> None:
        super().__init__(
            ProviderHTTPConfig(
                provider=self.name,
                model=model or "gpt-4o-mini",
                enabled=enabled,
                base_url="https://api.openai.com/v1",
                api_key=api_key,
                timeout_seconds=timeout_seconds,
                input_cost_per_million=0.15,
                output_cost_per_million=0.60,
            )
        )
