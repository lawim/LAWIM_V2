from __future__ import annotations

import json
import logging
import os
import time
import urllib.request
import urllib.error
from typing import Any

from .base import AIProvider, AIProviderRequest, AIProviderResponse, AIModelCapabilities, ModelCapability, LatencyClass, CostClass, DataPolicy

logger = logging.getLogger(__name__)

ANTHROPIC_API_BASE = "https://api.anthropic.com/v1"


class AnthropicProvider(AIProvider):
    provider_name: str = "anthropic"

    def __init__(self, api_key: str = "", model: str = "claude-3-haiku-20240307", timeout_ms: int = 30000) -> None:
        self._api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self._model = model
        self._timeout_ms = timeout_ms
        self._capabilities = AIModelCapabilities(
            model_name=model,
            provider="anthropic",
            capabilities={ModelCapability.STRUCTURED_OUTPUT, ModelCapability.TOOL_CALLING, ModelCapability.STREAMING},
            context_window=200000,
            max_output_tokens=4096,
            languages=["fr", "en"],
            latency_class=LatencyClass.MEDIUM,
            cost_class=CostClass.MEDIUM,
            data_policy=DataPolicy.NO_TRAINING,
            version="1.0",
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        start = time.time()
        if not self._api_key:
            return AIProviderResponse(success=False, error="ANTHROPIC_API_KEY not configured", error_category="auth", provider="anthropic")

        system = request.system_prompt
        messages = []
        if request.user_prompt:
            messages.append({"role": "user", "content": request.user_prompt})
        messages.extend(request.messages)

        payload: dict[str, Any] = {
            "model": request.model or self._model,
            "max_tokens": request.max_tokens,
            "messages": messages,
        }
        if system:
            payload["system"] = system

        body = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{ANTHROPIC_API_BASE}/messages",
            data=body,
            headers={
                "x-api-key": self._api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=request.timeout_ms / 1000) as resp:
                data = json.loads(resp.read())
                elapsed = (time.time() - start) * 1000
                content_blocks = data.get("content", [])
                text = " ".join(b.get("text", "") for b in content_blocks if b.get("type") == "text")
                usage = data.get("usage", {})
                return AIProviderResponse(
                    text=text,
                    model=data.get("model", self._model),
                    provider="anthropic",
                    usage={"input_tokens": usage.get("input_tokens", 0), "output_tokens": usage.get("output_tokens", 0)},
                    latency_ms=elapsed,
                    success=True,
                )
        except urllib.error.HTTPError as e:
            elapsed = (time.time() - start) * 1000
            category = "auth" if e.code == 401 else "rate_limit" if e.code == 429 else "provider_error"
            return AIProviderResponse(success=False, error=f"HTTP {e.code}: {e.reason}", error_category=category, latency_ms=elapsed, provider="anthropic")
        except urllib.error.URLError as e:
            elapsed = (time.time() - start) * 1000
            return AIProviderResponse(success=False, error=f"Connection error: {e.reason}", error_category="network", latency_ms=elapsed, provider="anthropic")
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            return AIProviderResponse(success=False, error=str(e), error_category="unknown", latency_ms=elapsed, provider="anthropic")

    def health(self) -> bool:
        return bool(self._api_key)

    @property
    def capabilities(self) -> AIModelCapabilities:
        return self._capabilities
