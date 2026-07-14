from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from json import JSONDecodeError
from urllib import error as urlerror
from urllib import parse, request
import json
import time
import uuid

from ..complexity import classify_text
from ..contracts import AIMessage, AIProvider, AIRequest, AIResponse, CostEstimate, ProviderHealth, UsageStatus
from ..safety import ResponseQuality, estimate_simple_token_count, validate_response

SYSTEM_PROMPT = "You are a neutral language processing capability. Do not decide LAWIM business actions."


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json_loads(value: bytes | str | None) -> dict[str, object]:
    if value is None:
        return {}
    if isinstance(value, bytes):
        text = value.decode("utf-8", errors="replace")
    else:
        text = value
    if not text.strip():
        return {}
    try:
        parsed = json.loads(text)
    except JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _json_request(url: str, *, method: str, headers: dict[str, str], payload: dict[str, object] | None = None, timeout: int = 30) -> tuple[int, dict[str, object], dict[str, str]]:
    body = None
    request_headers = dict(headers)
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    req = request.Request(url, data=body, headers=request_headers, method=method.upper())
    with request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
        status = int(getattr(response, "status", HTTPStatus.OK))
        response_headers = {key: value for key, value in response.headers.items()}
    return status, _json_loads(raw), response_headers


@dataclass(slots=True)
class ProviderHTTPConfig:
    provider: str
    model: str
    enabled: bool
    base_url: str
    api_key: str | None
    timeout_seconds: int
    input_cost_per_million: float = 0.0
    output_cost_per_million: float = 0.0


class BaseAIProvider:
    name = "base"

    def __init__(self, config: ProviderHTTPConfig) -> None:
        self.config = config
        self._last_health: ProviderHealth | None = None

    @property
    def model(self) -> str:
        return self.config.model

    @property
    def base_url(self) -> str:
        return self.config.base_url.rstrip("/")

    @property
    def api_key(self) -> str | None:
        return self.config.api_key

    @property
    def timeout_seconds(self) -> int:
        return self.config.timeout_seconds

    def is_enabled(self) -> bool:
        return bool(self.config.enabled and self.config.api_key and self.config.model and self.config.base_url)

    def estimate_cost(self, request: AIRequest) -> CostEstimate:
        input_tokens = estimate_simple_token_count(request.sanitized_text or request.text)
        output_tokens = max(1, min(request.max_output_tokens, 512))
        estimated_cost = ((input_tokens / 1_000_000.0) * self.config.input_cost_per_million) + (
            (output_tokens / 1_000_000.0) * self.config.output_cost_per_million
        )
        return CostEstimate(
            provider=self.name,
            model=self.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=estimated_cost,
        )

    def get_usage_status(self) -> UsageStatus:
        health = self._last_health
        return UsageStatus(
            provider=self.name,
            model=self.model,
            last_success_at=health.last_success_at if health else None,
            last_failure_at=health.last_failure_at if health else None,
            consecutive_failures=0,
        )

    def health_check(self) -> ProviderHealth:
        started = time.perf_counter()
        checked_at = _utcnow()
        if not self.is_enabled():
            health = ProviderHealth(
                provider=self.name,
                model=self.model,
                enabled=False,
                available=False,
                state="disabled",
                checked_at=checked_at,
                latency_ms=0,
                details={"reason": "provider_disabled"},
            )
            self._last_health = health
            return health
        try:
            models = self.list_models()
            available = self.model in models if models else True
            health = ProviderHealth(
                provider=self.name,
                model=self.model,
                enabled=True,
                available=available,
                state="ready" if available else "model_unavailable",
                checked_at=checked_at,
                latency_ms=int((time.perf_counter() - started) * 1000),
                details={"models": models[:20]},
            )
            self._last_health = health
            return health
        except Exception as exc:
            health = ProviderHealth(
                provider=self.name,
                model=self.model,
                enabled=True,
                available=False,
                state="unavailable",
                checked_at=checked_at,
                latency_ms=int((time.perf_counter() - started) * 1000),
                error_type=exc.__class__.__name__,
                error_code="health_check_failed",
                details={"message": str(exc)},
            )
            self._last_health = health
            return health

    def generate(self, request: AIRequest) -> AIResponse:
        started = time.perf_counter()
        request_id = request.request_id
        provider_request_id = f"{self.name}-{uuid.uuid4().hex[:12]}"
        if not self.is_enabled():
            return AIResponse(
                provider=self.name,
                model=self.model,
                success=False,
                content="",
                latency_ms=0,
                input_tokens=0,
                output_tokens=0,
                estimated_cost=0.0,
                finish_reason=None,
                error_type="disabled",
                error_code="provider_disabled",
                retryable=False,
                fallback_required=True,
                request_id=request_id,
                provider_request_id=provider_request_id,
                valid=False,
                complete=False,
                relevant=False,
                safe=True,
                well_formed=False,
                confidence_score=0.0,
                metadata={"reason": "provider_disabled"},
            )
        try:
            content, info = self._generate_content(request)
            latency_ms = int((time.perf_counter() - started) * 1000)
            response_quality: ResponseQuality = validate_response(content, max_chars=4000)
            input_tokens = int(info.get("input_tokens") or estimate_simple_token_count(request.sanitized_text or request.text))
            output_tokens = int(info.get("output_tokens") or estimate_simple_token_count(content))
            estimated_cost = float(info.get("estimated_cost") or self.estimate_cost(request).estimated_cost)
            response = AIResponse(
                provider=self.name,
                model=self.model,
                success=True,
                content=str(content or "").strip(),
                latency_ms=latency_ms,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                estimated_cost=estimated_cost,
                finish_reason=str(info.get("finish_reason") or "") or None,
                error_type=None,
                error_code=None,
                retryable=False,
                fallback_required=not response_quality.valid,
                request_id=request_id,
                provider_request_id=str(info.get("provider_request_id") or provider_request_id),
                valid=response_quality.valid,
                complete=response_quality.complete,
                relevant=response_quality.relevant,
                safe=response_quality.safe,
                well_formed=response_quality.well_formed,
                confidence_score=response_quality.confidence_score,
                metadata={**info, "quality": response_quality.to_dict()},
            )
            return response
        except urlerror.HTTPError as exc:
            latency_ms = int((time.perf_counter() - started) * 1000)
            raw_body = exc.read() if hasattr(exc, "read") else b""
            payload = _json_loads(raw_body)
            error_type, retryable = self._map_http_error(exc.code)
            return AIResponse(
                provider=self.name,
                model=self.model,
                success=False,
                content="",
                latency_ms=latency_ms,
                input_tokens=0,
                output_tokens=0,
                estimated_cost=0.0,
                finish_reason=None,
                error_type=error_type,
                error_code=str(exc.code),
                retryable=retryable,
                fallback_required=True,
                request_id=request_id,
                provider_request_id=provider_request_id,
                valid=False,
                complete=False,
                relevant=False,
                safe=True,
                well_formed=False,
                confidence_score=0.0,
                metadata={"message": str(payload or {}).strip() or str(exc)},
            )
        except (TimeoutError, urlerror.URLError, OSError, ValueError) as exc:
            latency_ms = int((time.perf_counter() - started) * 1000)
            return AIResponse(
                provider=self.name,
                model=self.model,
                success=False,
                content="",
                latency_ms=latency_ms,
                input_tokens=0,
                output_tokens=0,
                estimated_cost=0.0,
                finish_reason=None,
                error_type=exc.__class__.__name__,
                error_code="request_failed",
                retryable=True,
                fallback_required=True,
                request_id=request_id,
                provider_request_id=provider_request_id,
                valid=False,
                complete=False,
                relevant=False,
                safe=True,
                well_formed=False,
                confidence_score=0.0,
                metadata={"message": str(exc)},
            )

    def list_models(self) -> list[str]:
        raise NotImplementedError

    def _generate_content(self, request: AIRequest) -> tuple[str, dict[str, object]]:
        raise NotImplementedError

    def _map_http_error(self, status_code: int) -> tuple[str, bool]:
        if status_code in {401, 403}:
            return "authentication_error", False
        if status_code == 429:
            return "rate_limit_error", True
        if 500 <= status_code < 600:
            return "server_error", True
        return "http_error", True

    def _build_prompt_messages(self, request: AIRequest) -> list[dict[str, str]]:
        messages = [AIMessage(role="system", content=SYSTEM_PROMPT)]
        messages.extend(request.context_messages)
        messages.append(AIMessage(role="user", content=request.sanitized_text or request.text))
        return [message.to_dict() for message in messages]

    def _post_json(self, path: str, payload: dict[str, object], headers: dict[str, str] | None = None) -> tuple[int, dict[str, object], dict[str, str]]:
        request_headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json",
        }
        if headers:
            request_headers.update(headers)
        request_headers = {key: value for key, value in request_headers.items() if value}
        return _json_request(
            f"{self.base_url}{path}",
            method="POST",
            headers=request_headers,
            payload=payload,
            timeout=self.timeout_seconds,
        )

    def _get_json(self, path: str, headers: dict[str, str] | None = None) -> tuple[int, dict[str, object], dict[str, str]]:
        request_headers = {}
        if self.api_key:
            request_headers["Authorization"] = f"Bearer {self.api_key}"
        if headers:
            request_headers.update(headers)
        return _json_request(
            f"{self.base_url}{path}",
            method="GET",
            headers=request_headers,
            timeout=self.timeout_seconds,
        )


class OpenAICompatibleProvider(BaseAIProvider):
    def list_models(self) -> list[str]:
        status, payload, _ = self._get_json("/models")
        if status != 200:
            return []
        models = payload.get("data") if isinstance(payload.get("data"), list) else []
        names: list[str] = []
        for model in models:
            if isinstance(model, dict):
                name = str(model.get("id") or model.get("name") or "").strip()
                if name:
                    names.append(name)
        return names

    def _generate_content(self, request: AIRequest) -> tuple[str, dict[str, object]]:
        payload = {
            "model": self.model,
            "messages": self._build_prompt_messages(request),
            "max_tokens": request.max_output_tokens,
            "temperature": 0.2,
        }
        status, response, _ = self._post_json("/chat/completions", payload)
        if status != 200:
            raise urlerror.HTTPError(
                f"{self.base_url}/chat/completions",
                status,
                f"provider returned status {status}",
                hdrs=None,
                fp=None,
            )
        choices = response.get("choices") if isinstance(response.get("choices"), list) else []
        content = ""
        finish_reason = None
        if choices:
            first = choices[0]
            if isinstance(first, dict):
                message = first.get("message")
                if isinstance(message, dict):
                    content = str(message.get("content") or "")
                finish_reason = str(first.get("finish_reason") or "") or None
        usage = response.get("usage") if isinstance(response.get("usage"), dict) else {}
        return content, {
            "finish_reason": finish_reason,
            "input_tokens": int(usage.get("prompt_tokens") or 0),
            "output_tokens": int(usage.get("completion_tokens") or 0),
            "provider_request_id": response.get("id"),
        }
