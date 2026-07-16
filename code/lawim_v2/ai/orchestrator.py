from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import logging
import time
from typing import Any, Iterable
import uuid

logger = logging.getLogger(__name__)

from ..contact import COMPANY_NAME
from .complexity import ComplexityReport, classify_text
from .contracts import AIMessage, AIProvider, AIRequest, AIResponse
from .disclaimer import DisclaimerManager
from .internal_reasoning import InternalReasoningEngine, ReasoningContext
from .learning import LearningEngine
from .memory import MemoryOptimizer
from .models import RoutingDecision
from .monitoring import CircuitBreakerManager
from .prompt_reconstruction import PromptReconstructionEngine, ReconstructedContext
from .providers import DeepSeekProvider, GeminiProvider, OpenAIProvider
from .router import build_provider_chain, dedupe_chain
from .safety import (
    estimate_simple_token_count,
    looks_like_prompt_injection,
    redact_sensitive_object,
    redact_sensitive_text,
    stable_hash,
)


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _today_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _month_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


@dataclass(frozen=True, slots=True)
class OrchestrationOutcome:
    request: AIRequest
    decision: RoutingDecision
    response: AIResponse
    attempts: tuple[AIResponse, ...] = ()
    provider_chain: tuple[str, ...] = ()
    internal_response: bool = False
    disclaimer_added: bool = False
    continuity_context: ReconstructedContext | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "request": self.request.request_id,
            "decision": self.decision.to_dict(),
            "response": self.response.to_dict(),
            "attempts": [attempt.to_dict() for attempt in self.attempts],
            "provider_chain": list(self.provider_chain),
            "internal_response": self.internal_response,
            "disclaimer_added": self.disclaimer_added,
        }


class AIOrchestrator:
    def __init__(
        self,
        repository,
        config,
        *,
        providers: dict[str, AIProvider] | None = None,
        learning_engine: LearningEngine | None = None,
        circuit_breakers: CircuitBreakerManager | None = None,
        continuity_engine: PromptReconstructionEngine | None = None,
        memory_optimizer: MemoryOptimizer | None = None,
        internal_reasoning: InternalReasoningEngine | None = None,
        disclaimer_manager: DisclaimerManager | None = None,
        knowledge_runtime=None,
    ) -> None:
        self.repository = repository
        self.config = config
        self.learning_engine = learning_engine or LearningEngine(repository, config)
        self.circuit_breakers = circuit_breakers or CircuitBreakerManager(repository, config)
        self.providers = providers or self._build_default_providers()
        self.continuity_engine = continuity_engine or PromptReconstructionEngine(repository, config)
        self.memory_optimizer = memory_optimizer or MemoryOptimizer(repository, config)
        self.internal_reasoning = internal_reasoning or InternalReasoningEngine(repository, config, knowledge_runtime)
        self.disclaimer_manager = disclaimer_manager or DisclaimerManager(repository, config)

    def _build_default_providers(self) -> dict[str, AIProvider]:
        return {
            "deepseek": DeepSeekProvider(
                api_key=self.config.deepseek_api_key,
                model=self.config.deepseek_model,
                base_url=self.config.deepseek_base_url,
                enabled=self.config.ai_provider_deepseek_enabled,
                timeout_seconds=self.config.ai_request_timeout_seconds,
            ),
            "openai": OpenAIProvider(
                api_key=self.config.openai_api_key,
                model=self.config.openai_model,
                enabled=self.config.ai_provider_openai_enabled,
                timeout_seconds=self.config.ai_request_timeout_seconds,
            ),
            "gemini_primary": GeminiProvider(
                provider_name="gemini_primary",
                api_key=self.config.gemini_primary_api_key,
                model=self.config.gemini_primary_model,
                enabled=self.config.ai_provider_gemini_primary_enabled,
                timeout_seconds=self.config.ai_request_timeout_seconds,
            ),
            "gemini_secondary": GeminiProvider(
                provider_name="gemini_secondary",
                api_key=self.config.gemini_secondary_api_key,
                model=self.config.gemini_secondary_model,
                enabled=self.config.ai_provider_gemini_secondary_enabled,
                timeout_seconds=self.config.ai_request_timeout_seconds,
            ),
        }

    def classify(self, text: str | None, *, context_messages: int = 0) -> ComplexityReport:
        report = classify_text(text, context_messages=context_messages)
        if looks_like_prompt_injection(text):
            return ComplexityReport(
                "complex",
                "prompt_injection_suspected",
                report.signals + ("prompt_injection",),
            )
        return report

    def build_request(
        self,
        *,
        channel: str,
        text: str,
        conversation_key: str,
        external_chat_id: str = "",
        external_user_id: str = "",
        message_id: str = "",
        thread_id: int | None = None,
        contact_id: int | None = None,
        organization_id: int | None = None,
        language: str | None = None,
        context_messages: Iterable[AIMessage] = (),
        metadata: dict[str, object] | None = None,
        max_output_tokens: int = 512,
    ) -> AIRequest:
        messages = self._limit_context_messages(tuple(context_messages))
        report = self.classify(text, context_messages=len(messages))
        sanitized_text = redact_sensitive_text(text) if self.config.ai_context_redaction_enabled else str(text or "")
        filtered_metadata = redact_sensitive_object(metadata or {})
        if not isinstance(filtered_metadata, dict):
            filtered_metadata = {}
        filtered_metadata.update(
            {
                "prompt_injection_suspected": looks_like_prompt_injection(text),
                "company_name": COMPANY_NAME,
            }
        )
        request_id = f"ai-{stable_hash(f'{conversation_key}:{message_id}:{sanitized_text}')[:20]}"

        continuity = self.continuity_engine.reconstruct(
            conversation_key=conversation_key,
            user_id=filtered_metadata.get("user_id"),
            organization_id=organization_id,
            agent_code=filtered_metadata.get("agent_code"),
            language=language or "fr",
            current_text=text,
        )
        memory_bundle = self.memory_optimizer.load_for_conversation(
            conversation_key=conversation_key,
            user_id=filtered_metadata.get("user_id"),
            organization_id=organization_id,
            agent_code=filtered_metadata.get("agent_code"),
        )
        continuity_block = continuity.to_prompt_block()
        memory_block = memory_bundle.to_prompt()

        if continuity_block:
            filtered_metadata["continuity_context"] = continuity_block
        if memory_block:
            filtered_metadata["memory_context"] = memory_block

        return AIRequest(
            request_id=request_id,
            channel=channel,
            conversation_key=conversation_key,
            text=str(text or ""),
            sanitized_text=sanitized_text,
            language=language,
            complexity=report.complexity,
            external_chat_id=str(external_chat_id or ""),
            external_user_id=str(external_user_id or ""),
            message_id=str(message_id or ""),
            thread_id=thread_id,
            contact_id=contact_id,
            organization_id=organization_id,
            context_messages=messages,
            metadata=filtered_metadata,
            max_output_tokens=max_output_tokens,
            allow_retry=self.config.ai_allow_provider_retry,
        )

    def generate(self, request: AIRequest) -> OrchestrationOutcome:
        provider_chain = self._provider_chain(request)
        request_row = self.repository.create_ai_request(
            request_key=request.request_id,
            conversation_key=request.conversation_key,
            channel=request.channel,
            external_chat_id=request.external_chat_id,
            external_user_id=request.external_user_id,
            message_id=request.message_id,
            language=request.language,
            complexity=request.complexity,
            prompt_text=request.text,
            sanitized_text=request.sanitized_text,
            context_json=[message.to_dict() for message in request.context_messages],
            metadata=request.metadata,
            provider_chain_json=list(provider_chain) + ["internal"],
            status="pending",
        )
        attempts: list[AIResponse] = []
        selected_response: AIResponse | None = None
        selected_provider = ""
        reason = "provider_unavailable"
        routing_started = time.perf_counter()
        time_budget = float(self.config.ai_total_timeout_seconds)
        deadline = routing_started + time_budget
        complexity_report = self.classify(request.text, context_messages=len(request.context_messages))
        fallback_chain_trace: list[dict[str, object]] = []
        internal_used = False

        for provider_key in provider_chain:
            if time.perf_counter() >= deadline:
                break
            provider = self.providers.get(provider_key)
            if provider is None:
                continue
            if not provider.is_enabled():
                self._record_provider_skip(provider_key, request, "provider_disabled")
                fallback_chain_trace.append({"provider": provider_key, "reason": "disabled"})
                continue
            if not self.circuit_breakers.can_attempt(provider_key):
                self._record_provider_skip(provider_key, request, "circuit_open")
                self._record_alert(
                    provider_key,
                    "warning",
                    "circuit_open",
                    f"Circuit breaker open for {provider_key}",
                    {"request_key": request.request_id, "conversation_key": request.conversation_key},
                )
                fallback_chain_trace.append({"provider": provider_key, "reason": "circuit_open"})
                continue

            response = self._call_provider(provider, request)
            attempts.append(response)
            self._persist_attempt(request, response, provider_key=provider_key)
            fallback_chain_trace.append({
                "provider": provider_key,
                "success": response.success,
                "error_type": response.error_type,
                "latency_ms": response.latency_ms,
            })

            if response.success and self._response_is_acceptable(response):
                selected_response = response
                selected_provider = provider_key
                reason = "provider_response"
                self.circuit_breakers.record_success(provider_key)
                break

            self.circuit_breakers.record_failure(provider_key)
            self._record_response_alert(provider_key, request, response)
            if response.success and not self._response_is_acceptable(response):
                self._record_alert(
                    provider_key,
                    "warning",
                    "invalid_response",
                    f"Provider {provider_key} returned an invalid response",
                    {"request_key": request.request_id, "conversation_key": request.conversation_key},
                )
                fallback_chain_trace[-1]["reason_detail"] = "invalid_response"

        if selected_response is None:
            internal_used = True
            internal_result = self.internal_reasoning.reason(
                ReasoningContext(
                    user_text=request.text,
                    conversation_key=request.conversation_key,
                    language=request.language or "fr",
                    known_facts=tuple(
                        request.metadata.get("continuity_context", "").split("\n")
                        if isinstance(request.metadata.get("continuity_context"), str)
                        else ()
                    ),
                    known_intent=complexity_report.complexity,
                )
            )
            selected_response = AIResponse(
                provider="internal",
                model="lawim_v2_internal",
                success=True,
                content=internal_result.content,
                latency_ms=internal_result.latency_ms,
                input_tokens=0,
                output_tokens=len(internal_result.content.split()),
                estimated_cost=0.0,
                finish_reason="internal_reasoning",
                error_type=None,
                error_code=None,
                retryable=False,
                fallback_required=True,
                request_id=request.request_id,
                provider_request_id=None,
                valid=True,
                complete=True,
                relevant=True,
                safe=True,
                well_formed=True,
                confidence_score=internal_result.confidence,
                metadata={
                    "internal_reasoning": True,
                    "reasoning_path": internal_result.reasoning_path,
                    "sources": list(internal_result.sources),
                    "requires_escalation": internal_result.requires_escalation,
                    "escalation_reason": internal_result.escalation_reason,
                },
            )
            selected_provider = "internal"
            reason = "internal_reasoning_fallback"
            attempts.append(selected_response)
            self._persist_attempt(request, selected_response, provider_key="internal")
            fallback_chain_trace.append({
                "provider": "internal",
                "success": True,
                "reason": "all_external_providers_failed",
            })

        final_response = selected_response
        fallback_used = reason not in {"provider_response", ""}

        disclaimer_added = self._apply_disclaimer(final_response, request)

        self._persist_request_completion(
            request_row=request_row,
            request=request,
            response=final_response,
            selected_provider=selected_provider,
            provider_chain=provider_chain,
            fallback_used=fallback_used,
            reason=reason,
        )
        self._persist_fallback_observability(
            request=request,
            selected_provider=selected_provider,
            reason=reason,
            attempts=attempts,
            fallback_chain_trace=fallback_chain_trace,
            internal_used=internal_used,
        )
        routing_decision = RoutingDecision(
            request_id=request.request_id,
            conversation_key=request.conversation_key,
            complexity=complexity_report.complexity,
            selected_provider=selected_provider,
            chain=tuple(list(provider_chain) + (["internal"] if internal_used else [])),
            reason=reason,
            fallback_used=fallback_used,
            created_at=_utcnow(),
        )
        self.repository.record_ai_routing_decision(
            routing_key=f"route-{uuid.uuid4().hex[:12]}",
            request_key=request.request_id,
            conversation_key=request.conversation_key,
            complexity=complexity_report.complexity,
            selected_provider=selected_provider,
            fallback_used=fallback_used,
            chain=list(provider_chain) + (["internal"] if internal_used else []),
            rationale={
                "reason": reason,
                "signals": list(complexity_report.signals),
                "attempts": [attempt.provider for attempt in attempts],
                "internal_used": internal_used,
                "fallback_trace": fallback_chain_trace,
            },
        )
        if self.config.ai_learning_enabled:
            learning_reason = reason if not final_response.success or not final_response.valid or fallback_used else ""
            if learning_reason:
                self.learning_engine.maybe_create_candidate(request=request, response=final_response, reason=learning_reason)
        return OrchestrationOutcome(
            request=request,
            decision=routing_decision,
            response=final_response,
            attempts=tuple(attempts),
            provider_chain=provider_chain,
            internal_response=internal_used,
            disclaimer_added=disclaimer_added,
            continuity_context=None,
        )

    def list_providers(self) -> list[dict[str, object]]:
        rows = self.repository.list_ai_providers(limit=100)
        result: list[dict[str, object]] = []
        for row in rows:
            provider_key = str(row.get("provider_key") or "")
            provider = self.providers.get(provider_key)
            health = provider.health_check().to_dict() if provider is not None else None
            payload = dict(row)
            if health:
                payload["health"] = health
            result.append(payload)
        return result

    def list_health(self) -> list[dict[str, object]]:
        payload: list[dict[str, object]] = []
        for provider_key, provider in self.providers.items():
            health = provider.health_check()
            row = self.repository.upsert_ai_provider_health(
                provider_key=provider_key,
                credential_alias=provider_key.upper(),
                model=health.model,
                state=health.state,
                available=health.available,
                checked_at=health.checked_at,
                latency_ms=health.latency_ms,
                error_type=health.error_type,
                error_code=health.error_code,
                credit_remaining=health.credit_remaining,
                credit_limit=health.credit_limit,
                quota_status=health.quota_status,
                last_success_at=health.last_success_at,
                last_failure_at=health.last_failure_at,
                consecutive_failures=0,
                details=health.details,
            )
            payload.append(row)
        return payload

    def list_usage(self, *, period: str = "daily") -> list[dict[str, object]]:
        return self.repository.list_ai_usage(period=period, limit=100)

    def list_alerts(self, *, status: str | None = None) -> list[dict[str, object]]:
        return self.repository.list_ai_alerts(status=status, limit=100)

    def list_fallback_entries(self, *, status: str | None = None) -> list[dict[str, object]]:
        return self.repository.list_ai_fallback_entries(status=status, limit=100)

    def list_learning_candidates(self, *, status: str | None = None) -> list[dict[str, object]]:
        return self.repository.list_ai_learning_candidates(status=status, limit=100)

    def list_knowledge_versions(self) -> list[dict[str, object]]:
        return self.repository.list_ai_knowledge_versions(limit=100)

    def list_fallback_metrics(self) -> dict[str, object]:
        return self.repository.get_ai_fallback_metrics()

    def review_learning_candidate(self, *, candidate_key: str, decision: str, notes: str = "", reviewer_user_id: int | None = None) -> dict[str, object]:
        return self.repository.review_ai_learning_candidate(
            candidate_key=candidate_key,
            decision=decision,
            notes=notes,
            reviewer_user_id=reviewer_user_id,
        )

    def publish_learning_candidate(self, *, candidate_key: str, reviewer_user_id: int | None = None) -> dict[str, object]:
        return self.repository.publish_ai_learning_candidate(candidate_key=candidate_key, reviewer_user_id=reviewer_user_id)

    def deprecate_learning_candidate(self, *, candidate_key: str) -> dict[str, object]:
        return self.repository.deprecate_ai_learning_candidate(candidate_key=candidate_key)

    def rollback_knowledge_version(self, *, version_key: str) -> dict[str, object]:
        return self.repository.rollback_ai_knowledge_version(version_key=version_key)

    def ai_overview(self) -> dict[str, object]:
        overview = self.repository.ai_overview()
        overview["providers"] = len(self.providers)
        overview["provider_health"] = self.list_health()
        disclaimer_config = self.disclaimer_manager.get_config()
        overview["disclaimer"] = {
            "enabled": disclaimer_config.enabled,
            "globally_disabled": disclaimer_config.globally_disabled,
            "position": disclaimer_config.position,
        }
        overview["internal_reasoning_available"] = True
        overview["continuity_engine_available"] = True
        return overview

    def _provider_chain(self, request: AIRequest) -> tuple[str, ...]:
        chain = build_provider_chain(
            complexity=request.complexity,
            primary_provider=self.config.ai_primary_provider,
            complex_provider=self.config.ai_complex_provider,
            fallback_chain=tuple(self.config.ai_fallback_chain),
        )
        filtered: list[str] = []
        for provider_key in chain:
            if provider_key in self.providers:
                filtered.append(provider_key)
        return dedupe_chain(filtered)

    def _limit_context_messages(self, messages: tuple[AIMessage, ...]) -> tuple[AIMessage, ...]:
        limited = tuple(messages)[-self.config.ai_max_context_messages:]
        if self.config.ai_max_context_tokens is None:
            return limited
        while limited and estimate_simple_token_count(" ".join(message.content for message in limited)) > self.config.ai_max_context_tokens:
            limited = limited[1:]
        return limited

    def _response_is_acceptable(self, response: AIResponse) -> bool:
        if not response.success:
            return False
        if not response.valid or not response.complete or not response.safe or not response.well_formed:
            return False
        if not response.content.strip():
            return False
        if self.config.ai_max_cost_per_request is not None and response.estimated_cost > self.config.ai_max_cost_per_request:
            return False
        return True

    def _apply_disclaimer(self, response: AIResponse, request: AIRequest) -> bool:
        if response.provider == "internal":
            return False
        try:
            new_content = self.disclaimer_manager.inject_disclaimer(
                response.content,
                channel=request.channel,
                provider=response.provider,
                language=request.language or "fr",
                organization_id=request.organization_id,
            )
            if new_content != response.content:
                object.__setattr__(response, "content", new_content)
                return True
        except Exception as exc:
            logger.warning("Disclaimer injection failed: %s", exc)
        return False

    def _call_provider(self, provider: AIProvider, request: AIRequest) -> AIResponse:
        if provider.name != "internal" and provider.name not in self.providers:
            raise KeyError(provider.name)
        response = provider.generate(request)
        response = self._detect_provider_anomalies(response)
        return response

    def _detect_provider_anomalies(self, response: AIResponse) -> AIResponse:
        if not response.success:
            return response
        if response.content and len(response.content) < 10 and response.finish_reason != "stop":
            object.__setattr__(response, "valid", False)
            object.__setattr__(response, "error_type", "truncated_response")
        if response.latency_ms > (self.config.ai_request_timeout_seconds * 1000 * 0.8):
            object.__setattr__(response, "metadata", {**response.metadata, "provider_slow": True})
        return response

    def _persist_attempt(self, request: AIRequest, response: AIResponse, *, provider_key: str) -> None:
        self.repository.create_ai_response(
            request_key=request.request_id,
            provider_key=provider_key,
            model=response.model,
            success=response.success,
            content=response.content,
            latency_ms=response.latency_ms,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            estimated_cost=response.estimated_cost,
            finish_reason=response.finish_reason,
            error_type=response.error_type,
            error_code=response.error_code,
            retryable=response.retryable,
            fallback_required=response.fallback_required,
            provider_request_id=response.provider_request_id,
            valid=response.valid,
            complete=response.complete,
            relevant=response.relevant,
            safe=response.safe,
            well_formed=response.well_formed,
            confidence_score=response.confidence_score,
            metadata=response.metadata,
        )
        self._record_usage(request, response, provider_key=provider_key)
        self.repository.upsert_ai_provider_health(
            provider_key=provider_key,
            credential_alias=provider_key.upper(),
            model=response.model,
            state="ready" if self._response_is_acceptable(response) else (response.error_type or "unavailable"),
            available=self._response_is_acceptable(response),
            checked_at=_utcnow(),
            latency_ms=response.latency_ms,
            error_type=response.error_type,
            error_code=response.error_code,
            last_success_at=_utcnow() if response.success and response.valid else None,
            last_failure_at=_utcnow() if not response.success or not response.valid else None,
            consecutive_failures=0 if response.success and response.valid else 1,
            details={
                "request_id": request.request_id,
                "fallback_required": response.fallback_required,
                "confidence_score": response.confidence_score,
            },
        )

    def _record_usage(self, request: AIRequest, response: AIResponse, *, provider_key: str) -> None:
        period_day = _today_key()
        period_month = _month_key()
        base_usage = {
            "requests_total": 1,
            "requests_success": 1 if response.success else 0,
            "requests_failed": 0 if response.success else 1,
            "fallbacks_triggered": 0,
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
            "estimated_cost": response.estimated_cost,
            "rate_limit_errors": 1 if response.error_type == "rate_limit_error" else 0,
            "authentication_errors": 1 if response.error_type == "authentication_error" else 0,
            "timeouts": 1 if response.error_type in {"timeout_error", "request_failed"} else 0,
            "empty_responses": 1 if not response.content.strip() else 0,
            "invalid_responses": 1 if not response.valid else 0,
            "circuit_open_count": 1 if response.error_type == "circuit_open" else 0,
            "last_success_at": _utcnow() if response.success and response.valid else None,
            "last_failure_at": _utcnow() if not response.success or not response.valid else None,
        }
        self.repository.upsert_ai_usage(period="daily", provider_key=provider_key, values={**base_usage, "period_day": period_day})
        self.repository.upsert_ai_usage(period="monthly", provider_key=provider_key, values={**base_usage, "period_month": period_month})
        self.repository.record_ai_cost_estimate(
            request_key=request.request_id,
            provider_key=provider_key,
            model=response.model,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            estimated_cost=response.estimated_cost,
        )

    def _persist_fallback_observability(
        self,
        *,
        request: AIRequest,
        selected_provider: str,
        reason: str,
        attempts: list[AIResponse],
        fallback_chain_trace: list[dict[str, object]],
        internal_used: bool,
    ) -> None:
        fallback_count = sum(1 for a in attempts if a.provider != selected_provider)
        try:
            self.repository.record_ai_fallback_metrics(
                request_key=request.request_id,
                conversation_key=request.conversation_key,
                final_provider=selected_provider,
                reason=reason,
                fallback_count=fallback_count,
                total_attempts=len(attempts),
                internal_used=internal_used,
                total_latency_ms=sum(a.latency_ms for a in attempts),
                trace=fallback_chain_trace,
            )
        except Exception as exc:
            logger.warning("Failed to track fallback metrics: %s", exc)

    def _persist_request_completion(
        self,
        *,
        request_row: dict[str, object],
        request: AIRequest,
        response: AIResponse,
        selected_provider: str,
        provider_chain: tuple[str, ...],
        fallback_used: bool,
        reason: str,
    ) -> None:
        metadata = dict(request.metadata)
        metadata.update(
            {
                "final_provider": selected_provider,
                "fallback_used": fallback_used,
                "reason": reason,
                "response_quality": {
                    "valid": response.valid,
                    "complete": response.complete,
                    "relevant": response.relevant,
                    "safe": response.safe,
                    "well_formed": response.well_formed,
                    "confidence_score": response.confidence_score,
                },
            }
        )
        self.repository.create_ai_request(
            request_key=request.request_id,
            conversation_key=request.conversation_key,
            channel=request.channel,
            external_chat_id=request.external_chat_id,
            external_user_id=request.external_user_id,
            message_id=request.message_id,
            language=request.language,
            complexity=request.complexity,
            prompt_text=request.text,
            sanitized_text=request.sanitized_text,
            context_json=[message.to_dict() for message in request.context_messages],
            metadata=metadata,
            provider_chain_json=list(provider_chain),
            status="completed" if response.success else "failed",
            created_at=request_row.get("created_at"),
            updated_at=_utcnow(),
        )

    def _record_provider_skip(self, provider_key: str, request: AIRequest, reason: str) -> None:
        if not self.config.ai_alerts_enabled:
            return
        self._record_alert(
            provider_key,
            "info",
            "provider_skipped",
            f"Provider {provider_key} skipped: {reason}",
            {"request_key": request.request_id, "conversation_key": request.conversation_key, "reason": reason},
        )

    def _record_response_alert(self, provider_key: str, request: AIRequest, response: AIResponse) -> None:
        if not self.config.ai_alerts_enabled:
            return
        alert_type = response.error_type or "provider_failure"
        severity = "critical" if alert_type == "authentication_error" else "warning"
        self._record_alert(
            provider_key,
            severity,
            alert_type,
            f"Provider {provider_key} failed for request {request.request_id}",
            {
                "request_key": request.request_id,
                "conversation_key": request.conversation_key,
                "error_code": response.error_code,
                "retryable": response.retryable,
            },
        )

    def _record_alert(self, provider_key: str, severity: str, alert_type: str, message: str, payload: dict[str, object]) -> None:
        if not self.config.ai_alerts_enabled:
            return
        try:
            self.repository.record_ai_alert(
                provider_key=provider_key,
                severity=severity,
                alert_type=alert_type,
                message=message,
                payload=payload,
            )
        except Exception:
            return
