from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging
import time
from typing import Any
import uuid

from ..ai.contracts import AIMessage, AIRequest, AIResponse
from ..ai.internal_reasoning import InternalReasoningEngine, ReasoningContext

from .config import DEFAULT_MAX_RETRIES, DEFAULT_TOTAL_TIMEOUT
from .errors import AllProvidersFailedError, ProviderTimeoutError
from .provider_registry import ProviderRegistry
from .selection import ProviderSelectionPolicy

logger = logging.getLogger(__name__)


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _generate_request_id() -> str:
    return f"orchestra-{uuid.uuid4().hex[:16]}"


@dataclass
class ControlledGenerationRequest:
    text: str
    conversation_key: str = ""
    channel: str = "api"
    language: str = "fr"
    system_prompt: str | None = None
    max_output_tokens: int = 512
    context_messages: tuple[AIMessage, ...] = ()
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass
class AttemptInfo:
    provider: str
    model: str
    latency_ms: float
    success: bool
    error: str | None = None
    response: str | None = None


@dataclass
class GenerationResult:
    success: bool
    content: str
    provider: str
    model: str
    latency_ms: float
    all_attempts: list[AttemptInfo]
    fallback_used: bool
    internal_fallback: bool
    error: str | None = None


class ProviderOrchestrator:
    """Orchestrates calls to AI providers with timeouts, retries, circuit breakers, and fallback.

    This wraps the existing AIOrchestrator and providers with a cleaner contract.
    """

    def __init__(
        self,
        registry: ProviderRegistry,
        selection_policy: ProviderSelectionPolicy,
        internal_engine: InternalReasoningEngine | None = None,
    ) -> None:
        self._registry = registry
        self._selection = selection_policy
        self._internal = internal_engine

    def generate(
        self,
        request: ControlledGenerationRequest,
        timeout_seconds: float = DEFAULT_TOTAL_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> GenerationResult:
        """Generate a response using the provider chain."""
        provider_chain = self._selection.select_chain(
            language=request.language,
        )
        if not provider_chain:
            provider_chain = self._registry.get_available_providers()
        all_attempts: list[AttemptInfo] = []
        final_response: AIResponse | None = None
        final_provider = ""
        deadline = time.perf_counter() + timeout_seconds

        for provider_name in provider_chain:
            if time.perf_counter() >= deadline:
                logger.warning("Deadline reached before trying provider %s", provider_name)
                break

            provider = self._registry.get(provider_name)
            if provider is None:
                continue

            if not self._registry.is_available(provider_name):
                continue

            for attempt_num in range(1 + max_retries):
                if time.perf_counter() >= deadline:
                    break

                latency_ms = 0.0
                start = time.perf_counter()
                try:
                    provider_request = self._build_provider_request(request)
                    remaining = max(deadline - time.perf_counter(), 1.0)
                    effective_timeout = min(remaining, timeout_seconds)
                    response_text, latency_ms, error = self._call_single(
                        provider_name, provider, provider_request, effective_timeout,
                    )
                    if not error and response_text is not None:
                        self._handle_success(provider_name, response_text)
                        model = getattr(provider, "model", provider_name)
                        all_attempts.append(AttemptInfo(
                            provider=provider_name,
                            model=model,
                            latency_ms=latency_ms,
                            success=True,
                            response=response_text,
                        ))
                        return GenerationResult(
                            success=True,
                            content=response_text,
                            provider=provider_name,
                            model=model,
                            latency_ms=latency_ms,
                            all_attempts=list(all_attempts),
                            fallback_used=len(all_attempts) > 1,
                            internal_fallback=False,
                        )
                    self._handle_failure(provider_name, error or "empty_response")
                    all_attempts.append(AttemptInfo(
                        provider=provider_name,
                        model=getattr(provider, "model", provider_name),
                        latency_ms=latency_ms,
                        success=False,
                        error=error or "empty_response",
                    ))
                    if not _is_retryable(error):
                        break
                except ProviderTimeoutError:
                    self._handle_timeout_and_record(provider_name, all_attempts, provider)
                    if not max_retries:
                        break
                except Exception as exc:
                    err_msg = str(exc)
                    self._handle_failure(provider_name, err_msg)
                    all_attempts.append(AttemptInfo(
                        provider=provider_name,
                        model=getattr(provider, "model", provider_name),
                        latency_ms=(time.perf_counter() - start) * 1000,
                        success=False,
                        error=err_msg,
                    ))
                    if not max_retries:
                        break

        internal_result = self._call_internal_fallback(request)
        if internal_result is not None:
            all_attempts.append(AttemptInfo(
                provider="internal",
                model="lawim_v2_internal",
                latency_ms=0.0,
                success=True,
                response=internal_result,
            ))
            return GenerationResult(
                success=True,
                content=internal_result,
                provider="internal",
                model="lawim_v2_internal",
                latency_ms=0.0,
                all_attempts=all_attempts,
                fallback_used=True,
                internal_fallback=True,
            )

        raise AllProvidersFailedError(
            f"All providers failed. Attempts: {[a.provider + ':' + (a.error or 'ok') for a in all_attempts]}"
        )

    def _build_provider_request(
        self,
        request: ControlledGenerationRequest,
    ) -> AIRequest:
        return AIRequest(
            request_id=_generate_request_id(),
            channel=request.channel,
            conversation_key=request.conversation_key,
            text=request.text,
            sanitized_text=request.text,
            language=request.language,
            max_output_tokens=request.max_output_tokens,
            context_messages=request.context_messages,
            metadata=request.metadata,
        )

    def _call_single(
        self,
        provider_name: str,
        provider: Any,
        provider_request: AIRequest,
        timeout: float,
    ) -> tuple[str | None, float, str]:
        """Call a single provider with timeout. Returns (response_text, latency_ms, error)."""
        start = time.perf_counter()
        try:
            response: AIResponse = provider.generate(provider_request)
            elapsed = (time.perf_counter() - start) * 1000
            if response.success and response.content.strip():
                return response.content, elapsed, ""
            if not response.success:
                err = response.error_type or "provider_error"
                return None, elapsed, err
            if not response.content.strip():
                return None, elapsed, "empty_response"
            return response.content, elapsed, ""
        except Exception as exc:
            elapsed = (time.perf_counter() - start) * 1000
            err = str(exc) or exc.__class__.__name__
            return None, elapsed, err

    def _handle_timeout_and_record(
        self,
        provider_name: str,
        all_attempts: list[AttemptInfo],
        provider: Any,
    ) -> None:
        self._registry.record_timeout(provider_name)
        all_attempts.append(AttemptInfo(
            provider=provider_name,
            model=getattr(provider, "model", provider_name),
            latency_ms=0.0,
            success=False,
            error="timeout",
        ))

    def _handle_timeout(self, provider_name: str) -> None:
        self._registry.record_timeout(provider_name)

    def _handle_failure(self, provider_name: str, error: str) -> None:
        self._registry.record_failure(provider_name, error)

    def _handle_success(self, provider_name: str, response: str) -> None:
        self._registry.record_success(provider_name)

    def _call_internal_fallback(self, request: ControlledGenerationRequest) -> str | None:
        """Call InternalReasoningEngine as final fallback."""
        if self._internal is None:
            return None
        try:
            ctx = ReasoningContext(
                user_text=request.text,
                conversation_key=request.conversation_key,
                language=request.language,
            )
            result = self._internal.reason(ctx)
            return result.content
        except Exception as exc:
            logger.error("Internal reasoning fallback failed: %s", exc)
            return None


def _is_retryable(error: str | None) -> bool:
    if error is None:
        return False
    err_lower = error.lower()
    retryable_patterns = [
        "timeout",
        "rate_limit",
        "server_error",
        "429",
        "500",
        "503",
        "connection",
        "temporary",
        "too many requests",
        "service unavailable",
    ]
    return any(pattern in err_lower for pattern in retryable_patterns)
