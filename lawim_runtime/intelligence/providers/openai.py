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

OPENAI_API_BASE = "https://api.openai.com/v1"


class OpenAIProvider(AIProvider):
    provider_name: str = "openai"

    def __init__(self, api_key: str = "", model: str = "gpt-4o-mini", timeout_ms: int = 30000) -> None:
        self._api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self._model = model
        self._timeout_ms = timeout_ms
        self._capabilities = AIModelCapabilities(
            model_name=model,
            provider="openai",
            capabilities={ModelCapability.STRUCTURED_OUTPUT, ModelCapability.JSON_SCHEMA, ModelCapability.TOOL_CALLING, ModelCapability.STREAMING},
            context_window=128000,
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
            return AIProviderResponse(success=False, error="OPENAI_API_KEY not configured", error_category="auth", provider="openai")

        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        if request.user_prompt:
            messages.append({"role": "user", "content": request.user_prompt})
        messages.extend(request.messages)

        payload: dict[str, Any] = {
            "model": request.model or self._model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        if request.response_schema:
            payload["response_format"] = {"type": "json_object", "schema": request.response_schema}

        body = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{OPENAI_API_BASE}/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=request.timeout_ms / 1000) as resp:
                data = json.loads(resp.read())
                elapsed = (time.time() - start) * 1000
                choice = data.get("choices", [{}])[0]
                text = choice.get("message", {}).get("content", "")
                usage = data.get("usage", {})
                return AIProviderResponse(
                    text=text,
                    model=data.get("model", self._model),
                    provider="openai",
                    usage={"input_tokens": usage.get("prompt_tokens", 0), "output_tokens": usage.get("completion_tokens", 0)},
                    latency_ms=elapsed,
                    success=True,
                )
        except urllib.error.HTTPError as e:
            elapsed = (time.time() - start) * 1000
            category = "auth" if e.code == 401 else "rate_limit" if e.code == 429 else "provider_error"
            return AIProviderResponse(
                success=False,
                error=f"HTTP {e.code}: {e.reason}",
                error_category=category,
                latency_ms=elapsed,
                provider="openai",
            )
        except urllib.error.URLError as e:
            elapsed = (time.time() - start) * 1000
            return AIProviderResponse(
                success=False,
                error=f"Connection error: {e.reason}",
                error_category="network",
                latency_ms=elapsed,
                provider="openai",
            )
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            return AIProviderResponse(
                success=False,
                error=str(e),
                error_category="unknown",
                latency_ms=elapsed,
                provider="openai",
            )

    def health(self) -> bool:
        return bool(self._api_key)

    @property
    def capabilities(self) -> AIModelCapabilities:
        return self._capabilities
