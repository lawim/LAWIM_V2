from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from ...interaction.response_plan import InteractionResponsePlan, ResponseType
from ...interaction.response_writer import DeterministicResponseWriter, ResponseWriterRequest

logger = logging.getLogger(__name__)


@dataclass
class AIResponseWriterRequest:
    request_id: str = field(default_factory=lambda: uuid4().hex[:16])
    response_plan: InteractionResponsePlan | None = None
    context: dict[str, Any] = field(default_factory=dict)
    language: str = "fr"
    channel: str = ""
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponseWriterResult:
    result_id: str = field(default_factory=lambda: uuid4().hex[:16])
    text: str = ""
    formatted_text: str = ""
    parse_mode: str = "text"
    success: bool = False
    fallback_used: bool = False
    validation_errors: list[str] = field(default_factory=list)
    error: str = ""
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class AIResponseWriter:
    def __init__(
        self,
        llm_writer: Any = None,
        deterministic_fallback: DeterministicResponseWriter | None = None,
        validator: Any = None,
    ) -> None:
        self._llm = llm_writer
        self._fallback = deterministic_fallback or DeterministicResponseWriter()
        self._validator = validator

    def write(self, request: AIResponseWriterRequest) -> AIResponseWriterResult:
        plan = request.response_plan

        if not plan or plan.is_empty():
            return AIResponseWriterResult(success=True, text="", correlation_id=request.correlation_id)

        if self._llm:
            try:
                result = self._llm.write(request)
                if result.success and self._validate(result.text, plan):
                    return result
            except Exception as e:
                logger.error("llm writer error, falling back: %s", e)

        fallback_req = ResponseWriterRequest(
            response_plan=plan,
            language=request.language,
        )
        fallback_result = self._fallback.write(fallback_req)

        return AIResponseWriterResult(
            text=fallback_result.text,
            formatted_text=fallback_result.formatted_text,
            parse_mode="text",
            success=True,
            fallback_used=True,
            correlation_id=request.correlation_id,
        )

    def _validate(self, text: str, plan: InteractionResponsePlan) -> bool:
        if self._validator:
            vresult = self._validator.validate(text, plan)
            return vresult.valid
        return True
