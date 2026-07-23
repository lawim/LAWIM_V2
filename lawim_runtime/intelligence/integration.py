from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from .gateway import AIIntelligenceGateway, AIGatewayMode
from .request import AIRequest, AITaskType
from .result import AIResult, AIResultStatus
from .extraction.candidate import ExtractionCandidate, ExtractionEvidence, ExtractionMethod
from .extraction.engine import StructuredExtractionEngine, ExtractionRequest, ExtractionResult, ExtractionConfidencePolicy
from .writing.writer import AIResponseWriter, AIResponseWriterRequest, AIResponseWriterResult
from .safety.validation import ResponseValidator
from ..interaction.response_plan import InteractionResponsePlan, ResponseType
from ..interaction.response_writer import DeterministicResponseWriter, ResponseWriterRequest
from ..project_profile.candidate import CandidateUpdate

logger = logging.getLogger(__name__)


@dataclass
class AIIntegrationConfig:
    ai_intelligence_enabled: bool = False
    ai_extraction_enabled: bool = False
    ai_response_writer_enabled: bool = False
    ai_knowledge_enabled: bool = False
    ai_rag_enabled: bool = False
    ai_shadow_mode: bool = True
    ai_provider_calls_enabled: bool = False
    ai_gateway_mode: AIGatewayMode = AIGatewayMode.DETERMINISTIC


@dataclass
class AIDivergenceRecord:
    interaction_id: str = ""
    correlation_id: str = ""
    channel: str = ""
    field_name: str = ""
    deterministic_value: Any = None
    ai_value: Any = None
    category: str = "field_mismatch"
    severity: str = "info"


class AIDivergenceAnalyzer:
    def __init__(self) -> None:
        self._records: list[AIDivergenceRecord] = []

    def compare_extraction(
        self,
        interaction_id: str,
        correlation_id: str,
        channel: str,
        deterministic_candidates: list[ExtractionCandidate],
        ai_candidates: list[ExtractionCandidate],
    ) -> list[AIDivergenceRecord]:
        divergences: list[AIDivergenceRecord] = []
        det_map = {c.field_name: c for c in deterministic_candidates}
        ai_map = {c.field_name: c for c in ai_candidates}

        all_fields = set(det_map.keys()) | set(ai_map.keys())
        for field in all_fields:
            det_val = det_map[field].value if field in det_map else None
            ai_val = ai_map[field].value if field in ai_map else None
            if det_val != ai_val:
                rec = AIDivergenceRecord(
                    interaction_id=interaction_id,
                    correlation_id=correlation_id,
                    channel=channel,
                    field_name=field,
                    deterministic_value=det_val,
                    ai_value=ai_val,
                )
                self._records.append(rec)
                divergences.append(rec)
        return divergences

    def count(self) -> int:
        return len(self._records)


class CandidateUpdateFactory:
    def from_extraction_result(self, ext_result: ExtractionResult, project_id: str, correlation_id: str = "") -> list[CandidateUpdate]:
        updates: list[CandidateUpdate] = []
        for cand in ext_result.candidates:
            if cand.is_negation:
                continue
            update = CandidateUpdate(
                project_id=project_id,
                field_name=cand.field_name,
                raw_value=cand.raw_value,
                proposed_value=cand.value,
                confidence=cand.confidence,
                source_message_id=cand.evidence.source_message_id if cand.evidence else "",
                correlation_id=correlation_id,
                extraction_method=cand.evidence.extraction_method.value if cand.evidence else "DETERMINISTIC",
            )
            updates.append(update)
        return updates


class AIIntegrationPolicy:
    def __init__(self, config: AIIntegrationConfig | None = None) -> None:
        self._config = config or AIIntegrationConfig()
        self._gateway: AIIntelligenceGateway | None = None
        self._extraction_engine: StructuredExtractionEngine | None = None
        self._ai_writer: AIResponseWriter | None = None
        self._det_writer: DeterministicResponseWriter | None = None
        self._response_validator: ResponseValidator | None = None
        self._divergence: AIDivergenceAnalyzer | None = None

    def configure(
        self,
        gateway: AIIntelligenceGateway | None = None,
        extraction_engine: StructuredExtractionEngine | None = None,
        ai_writer: AIResponseWriter | None = None,
        det_writer: DeterministicResponseWriter | None = None,
        response_validator: ResponseValidator | None = None,
        divergence: AIDivergenceAnalyzer | None = None,
    ) -> None:
        self._gateway = gateway
        self._extraction_engine = extraction_engine
        self._ai_writer = ai_writer
        self._det_writer = det_writer or DeterministicResponseWriter()
        self._response_validator = response_validator or ResponseValidator()
        self._divergence = divergence

    @property
    def gateway(self) -> AIIntelligenceGateway | None:
        return self._gateway

    @property
    def extraction_engine(self) -> StructuredExtractionEngine | None:
        return self._extraction_engine

    @property
    def ai_writer(self) -> AIResponseWriter | None:
        return self._ai_writer

    @property
    def det_writer(self) -> DeterministicResponseWriter:
        return self._det_writer

    @property
    def response_validator(self) -> ResponseValidator:
        return self._response_validator

    @property
    def divergence(self) -> AIDivergenceAnalyzer | None:
        return self._divergence

    @property
    def config(self) -> AIIntegrationConfig:
        return self._config

    def is_extraction_enabled(self) -> bool:
        return self._config.ai_extraction_enabled and self._config.ai_intelligence_enabled

    def is_writer_enabled(self) -> bool:
        return self._config.ai_response_writer_enabled and self._config.ai_intelligence_enabled

    def is_shadow(self) -> bool:
        return self._config.ai_shadow_mode or self._config.ai_gateway_mode == AIGatewayMode.SHADOW

    def get_gateway_mode(self) -> AIGatewayMode:
        return self._config.ai_gateway_mode
