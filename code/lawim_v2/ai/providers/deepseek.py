from __future__ import annotations

from .base import OpenAICompatibleProvider, ProviderHTTPConfig


class DeepSeekProvider(OpenAICompatibleProvider):
    name = "deepseek"

    def __init__(self, *, api_key: str | None, model: str | None, base_url: str | None, enabled: bool, timeout_seconds: int) -> None:
        super().__init__(
            ProviderHTTPConfig(
                provider=self.name,
                model=model or "deepseek-v4-flash",
                enabled=enabled,
                base_url=base_url or "https://api.deepseek.com",
                api_key=api_key,
                timeout_seconds=timeout_seconds,
                input_cost_per_million=0.14,
                output_cost_per_million=0.28,
            )
        )
