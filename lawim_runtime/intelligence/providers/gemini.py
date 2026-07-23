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

GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"


class GeminiProvider(AIProvider):
    provider_name: str = "gemini"

    def __init__(self, api_key: str = "", model: str = "gemini-2.0-flash", timeout_ms: int = 30000) -> None:
        self._api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self._model = model
        self._timeout_ms = timeout_ms
        self._capabilities = AIModelCapabilities(
            model_name=model,
            provider="gemini",
            capabilities={ModelCapability.STRUCTURED_OUTPUT, ModelCapability.VISION, ModelCapability.STREAMING},
            context_window=1048576,
            max_output_tokens=8192,
            languages=["fr", "en"],
            latency_class=LatencyClass.MEDIUM,
            cost_class=CostClass.LOW,
            data_policy=DataPolicy.STANDARD,
            version="1.0",
        )

    def generate(self, request: AIProviderRequest) -> AIProviderResponse:
        start = time.time()
        if not self._api_key:
            return AIProviderResponse(success=False, error="GEMINI_API_KEY not configured", error_category="auth", provider="gemini")

        contents: list[dict[str, Any]] = []
        if request.system_prompt:
            contents.append({"role": "user", "parts": [{"text": request.system_prompt}]})
        if request.user_prompt:
            contents.append({"role": "user", "parts": [{"text": request.user_prompt}]})
        for msg in request.messages:
            contents.append({"role": msg.get("role", "user"), "parts": [{"text": msg.get("content", "")}]})

        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens,
            },
        }

        model = request.model or self._model
        url = f"{GEMINI_API_BASE}/models/{model}:generateContent?key={self._api_key}"
        body = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=request.timeout_ms / 1000) as resp:
                data = json.loads(resp.read())
                elapsed = (time.time() - start) * 1000
                candidates = data.get("candidates", [])
                text = ""
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    text = " ".join(p.get("text", "") for p in parts)
                usage = data.get("usageMetadata", {})
                return AIProviderResponse(
                    text=text,
                    model=model,
                    provider="gemini",
                    usage={"input_tokens": usage.get("promptTokenCount", 0), "output_tokens": usage.get("candidatesTokenCount", 0)},
                    latency_ms=elapsed,
                    success=True,
                )
        except urllib.error.HTTPError as e:
            elapsed = (time.time() - start) * 1000
            category = "auth" if e.code == 403 else "rate_limit" if e.code == 429 else "provider_error"
            return AIProviderResponse(success=False, error=f"HTTP {e.code}: {e.reason}", error_category=category, latency_ms=elapsed, provider="gemini")
        except urllib.error.URLError as e:
            elapsed = (time.time() - start) * 1000
            return AIProviderResponse(success=False, error=f"Connection error: {e.reason}", error_category="network", latency_ms=elapsed, provider="gemini")
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            return AIProviderResponse(success=False, error=str(e), error_category="unknown", latency_ms=elapsed, provider="gemini")

    def health(self) -> bool:
        return bool(self._api_key)

    @property
    def capabilities(self) -> AIModelCapabilities:
        return self._capabilities
