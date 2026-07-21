from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from ..conversation.memory.context_builder import ProviderMemoryContext
from ..conversation.policy.dialogue_plan import DialoguePlan
from ..conversation.state.state import ResponsePlan


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class ControlledGenerationRequest:
    request_id: str = ""
    conversation_id: str = ""
    case_id: str = ""
    state_version: int = 0
    language: str = "fr"
    persona: str = "LAWIM AI"
    intent: str = ""
    journey_code: str = ""
    dialogue_act: str = ""
    facts_to_acknowledge: dict[str, Any] = field(default_factory=dict)
    facts_not_to_repeat: list[str] = field(default_factory=list)
    next_action: str = ""
    next_question_key: str = ""
    rendered_next_question: str = ""
    allowed_content: list[str] = field(default_factory=list)
    forbidden_content: list[str] = field(default_factory=list)
    maximum_questions: int = 1
    maximum_sentences: int = 3
    maximum_characters: int = 500
    channel: str = ""
    provider_memory_context: dict[str, Any] = field(default_factory=dict)
    response_schema_version: str = "1.0"
    user_message: str = ""
    known_facts: dict[str, Any] = field(default_factory=dict)
    missing_required_facts: list[str] = field(default_factory=list)
    handover_status: str | None = None
    readiness_status: str = ""
    created_at: str = ""


@dataclass
class ControlledGenerationResponse:
    content: str = ""
    language: str = ""
    dialogue_act: str = ""
    question_count: int = 0
    provider: str = ""
    model: str = ""
    latency_ms: float = 0.0
    finish_reason: str = ""
    confidence: float = 0.0
    schema_version: str = "1.0"
    valid: bool = True
    validation_errors: list[str] = field(default_factory=list)
    created_at: str = ""


@dataclass
class GenerationPolicy:
    maximum_questions: int = 1
    maximum_sentences: int = 3
    maximum_characters: int = 500
    require_json_output: bool = True
    enforce_allowed_content: bool = True
    enforce_forbidden_content: bool = True
    validate_language: bool = True
    validate_question_count: bool = True
    validate_dialogue_act: bool = True
    response_schema_version: str = "1.0"


@dataclass
class GenerationAttempt:
    attempt_id: str = ""
    request_id: str = ""
    provider: str = ""
    model: str = ""
    started_at: str = ""
    completed_at: str = ""
    latency_ms: float = 0.0
    status: str = "PENDING"
    error: str = ""
    response: ControlledGenerationResponse | None = None


@dataclass
class GenerationResult:
    response: ControlledGenerationResponse | None = None
    attempts: list[GenerationAttempt] = field(default_factory=list)
    provider_chain: list[str] = field(default_factory=list)
    internal_fallback_used: bool = False
    repair_attempted: bool = False
    repair_successful: bool = False
    final_status: str = "PENDING"
    total_latency_ms: float = 0.0


def build_request_from_plan(
    response_plan: ResponsePlan,
    dialogue_plan: DialoguePlan,
    provider_memory_context: ProviderMemoryContext,
    conversation_id: str = "",
    case_id: str = "",
    state_version: int = 0,
    channel: str = "",
) -> ControlledGenerationRequest:
    now = _utcnow()
    dialogue_act = (
        response_plan.response_type
        or dialogue_plan.dialogue_act
        or ""
    )
    language = response_plan.language or dialogue_plan.language or "fr"
    max_questions = max(response_plan.maximum_questions, dialogue_plan.maximum_questions)
    max_sentences = dialogue_plan.maximum_sentences
    max_chars = min(
        response_plan.maximum_length or 500,
        dialogue_plan.maximum_characters or 600,
    )

    known_facts = dict(provider_memory_context.active_facts) if provider_memory_context else {}

    merged_forbidden = list(response_plan.forbidden_content)
    for p in dialogue_plan.forbidden_phrases:
        if p not in merged_forbidden:
            merged_forbidden.append(p)
    for t in dialogue_plan.forbidden_topics:
        merged_forbidden.append(f"topic:{t}")

    return ControlledGenerationRequest(
        request_id=f"gen-{conversation_id}-{now}",
        conversation_id=conversation_id,
        case_id=case_id,
        state_version=state_version,
        language=language,
        persona=response_plan.speaker or "LAWIM AI",
        intent=provider_memory_context.intent if provider_memory_context else "",
        journey_code=provider_memory_context.summary if provider_memory_context else "",
        dialogue_act=dialogue_act,
        facts_to_acknowledge=dict(response_plan.acknowledgement_facts),
        facts_not_to_repeat=list(dialogue_plan.facts_not_to_repeat),
        next_action=response_plan.next_action,
        next_question_key=response_plan.next_question_key,
        rendered_next_question=response_plan.next_question_text,
        allowed_content=list(response_plan.allowed_content),
        forbidden_content=merged_forbidden,
        maximum_questions=max_questions,
        maximum_sentences=max_sentences,
        maximum_characters=max_chars,
        channel=channel,
        provider_memory_context={
            "language": provider_memory_context.language if provider_memory_context else language,
            "intent": provider_memory_context.intent if provider_memory_context else "",
            "active_facts": known_facts,
            "last_question_text": provider_memory_context.last_question_text if provider_memory_context else "",
            "response_instructions": list(provider_memory_context.response_instructions) if provider_memory_context else [],
            "prohibitions": list(provider_memory_context.prohibitions) if provider_memory_context else [],
            "summary": provider_memory_context.summary if provider_memory_context else "",
        } if provider_memory_context else {},
        handover_status=(
            response_plan.handover_reason
            if response_plan.handover_required
            else None
        ),
        known_facts=known_facts,
        created_at=now,
    )


def build_response_from_provider(
    provider_raw_response: str,
    provider_name: str,
    model: str,
    latency_ms: float,
    request: ControlledGenerationRequest,
) -> ControlledGenerationResponse:
    now = _utcnow()
    return ControlledGenerationResponse(
        content=provider_raw_response,
        language=request.language,
        dialogue_act=request.dialogue_act,
        provider=provider_name,
        model=model,
        latency_ms=latency_ms,
        schema_version=request.response_schema_version,
        created_at=now,
    )
