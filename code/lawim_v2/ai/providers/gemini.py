from __future__ import annotations

from urllib import error as urlerror

from .base import BaseAIProvider, ProviderHTTPConfig, SYSTEM_PROMPT, _json_request


class GeminiProvider(BaseAIProvider):
    def __init__(
        self,
        *,
        provider_name: str,
        api_key: str | None,
        model: str | None,
        enabled: bool,
        timeout_seconds: int,
        input_cost_per_million: float = 0.0,
        output_cost_per_million: float = 0.0,
    ) -> None:
        self.name = provider_name
        super().__init__(
            ProviderHTTPConfig(
                provider=provider_name,
                model=model or "gemini-3.5-flash",
                enabled=enabled,
                base_url="https://generativelanguage.googleapis.com/v1beta",
                api_key=api_key,
                timeout_seconds=timeout_seconds,
                input_cost_per_million=input_cost_per_million,
                output_cost_per_million=output_cost_per_million,
            )
        )

    def list_models(self) -> list[str]:
        if not self.api_key:
            return []
        status, payload, _ = _json_request(
            f"{self.base_url}/models?key={self.api_key}",
            method="GET",
            headers={},
            timeout=self.timeout_seconds,
        )
        if status != 200:
            return []
        models = payload.get("models") if isinstance(payload.get("models"), list) else []
        names: list[str] = []
        for model in models:
            if isinstance(model, dict):
                name = str(model.get("name") or model.get("model") or "").strip()
                if name:
                    names.append(name.rsplit("/", 1)[-1])
        return names

    def _generate_content(self, request):
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        contents = []
        for message in request.context_messages:
            role = "model" if message.role == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": message.content}]})
        contents.append({"role": "user", "parts": [{"text": request.sanitized_text or request.text}]})
        system_prompt = request.metadata.get("system_prompt")
        if not isinstance(system_prompt, str) or not system_prompt.strip():
            system_prompt = SYSTEM_PROMPT
        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": request.max_output_tokens,
            },
        }
        status, response, _ = _json_request(url, method="POST", headers={"Content-Type": "application/json"}, payload=payload, timeout=self.timeout_seconds)
        if status != 200:
            raise urlerror.HTTPError(url, status, f"provider returned status {status}", hdrs=None, fp=None)
        candidates = response.get("candidates") if isinstance(response.get("candidates"), list) else []
        content = ""
        finish_reason = None
        if candidates:
            candidate = candidates[0]
            if isinstance(candidate, dict):
                content_data = candidate.get("content")
                if isinstance(content_data, dict):
                    parts = content_data.get("parts") if isinstance(content_data.get("parts"), list) else []
                    texts = [str(part.get("text") or "") for part in parts if isinstance(part, dict)]
                    content = "".join(texts)
                finish_reason = str(candidate.get("finishReason") or "") or None
        usage = response.get("usageMetadata") if isinstance(response.get("usageMetadata"), dict) else {}
        return content, {
            "finish_reason": finish_reason,
            "input_tokens": int(usage.get("promptTokenCount") or 0),
            "output_tokens": int(usage.get("candidatesTokenCount") or usage.get("outputTokenCount") or 0),
            "provider_request_id": response.get("responseId") or response.get("id"),
        }
