from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
from uuid import uuid4

from .candidate import ExtractionCandidate, ExtractionEvidence, ExtractionMethod, ExtractionWarning
from ..request import AIRequest, AITaskType
from ..result import AIResult, AIResultStatus

logger = logging.getLogger(__name__)


class ExtractionConfidencePolicy(str, Enum):
    AUTO_ACCEPT = "AUTO_ACCEPT_CANDIDATE"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"
    REJECT = "REJECT_CANDIDATE"


@dataclass
class ExtractionRequest:
    request_id: str = field(default_factory=lambda: uuid4().hex[:16])
    text: str = ""
    language: str = "fr"
    project_id: str = ""
    session_id: str = ""
    interaction_id: str = ""
    allowed_fields: tuple[str, ...] = ()
    field_registry: Any = None
    confidence_policy: ExtractionConfidencePolicy = ExtractionConfidencePolicy.AUTO_ACCEPT
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractionResult:
    extraction_id: str = field(default_factory=lambda: uuid4().hex[:16])
    candidates: list[ExtractionCandidate] = field(default_factory=list)
    intent: str = ""
    language: str = ""
    warnings: list[ExtractionWarning] = field(default_factory=list)
    has_negation: bool = False
    has_correction: bool = False
    is_ambiguous: bool = False
    requires_clarification: bool = False
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


CandidateUpdateFactory = Callable[[ExtractionCandidate, str], Any]


class StructuredExtractionEngine:
    def __init__(
        self,
        primary_handler: Callable[[ExtractionRequest], ExtractionResult] | None = None,
        deterministic_handler: Callable[[ExtractionRequest], ExtractionResult] | None = None,
        candidate_factory: CandidateUpdateFactory | None = None,
    ) -> None:
        self._primary = primary_handler
        self._deterministic = deterministic_handler
        self._candidate_factory = candidate_factory
        self._confidence_thresholds = {
            ExtractionConfidencePolicy.AUTO_ACCEPT: 0.7,
            ExtractionConfidencePolicy.REQUIRE_CONFIRMATION: 0.4,
            ExtractionConfidencePolicy.REJECT: 0.0,
        }

    def extract(self, request: ExtractionRequest) -> ExtractionResult:
        result = ExtractionResult(
            correlation_id=request.correlation_id,
        )

        if self._deterministic:
            det_result = self._deterministic(request)
            if det_result.candidates:
                result.candidates.extend(det_result.candidates)
                result.intent = det_result.intent
                result.has_negation = det_result.has_negation
                result.has_correction = det_result.has_correction
                result.is_ambiguous = det_result.is_ambiguous
                result.requires_clarification = det_result.requires_clarification

        if self._primary:
            ai_result = self._primary(request)
            for cand in ai_result.candidates:
                existing = [c for c in result.candidates if c.field_name == cand.field_name]
                if not existing:
                    result.candidates.append(cand)
                elif cand.confidence > existing[0].confidence:
                    result.candidates.remove(existing[0])
                    result.candidates.append(cand)

        result.candidates = self._filter_by_confidence(result.candidates, request.confidence_policy)

        return result

    def _filter_by_confidence(
        self,
        candidates: list[ExtractionCandidate],
        policy: ExtractionConfidencePolicy,
    ) -> list[ExtractionCandidate]:
        threshold = self._confidence_thresholds.get(policy, 0.5)
        return [c for c in candidates if c.confidence >= threshold]

    def to_candidate_updates(self, result: ExtractionResult, project_id: str) -> list[Any]:
        if not self._candidate_factory:
            return []
        from lawim_runtime.project_profile.candidate import CandidateUpdate
        updates: list[CandidateUpdate] = []
        for cand in result.candidates:
            update = CandidateUpdate(
                project_id=project_id,
                field_name=cand.field_name,
                raw_value=cand.raw_value,
                proposed_value=cand.value,
                confidence=cand.confidence,
                source_message_id=cand.evidence.source_message_id if cand.evidence else "",
                correlation_id=result.correlation_id,
                extraction_method="DETERMINISTIC",
            )
            updates.append(update)
        return updates
