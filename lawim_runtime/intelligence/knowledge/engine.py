from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)


class TrustLevel(str, Enum):
    AUTHORITATIVE = "AUTHORITATIVE"
    VERIFIED_INTERNAL = "VERIFIED_INTERNAL"
    APPROVED_EXTERNAL = "APPROVED_EXTERNAL"
    UNVERIFIED = "UNVERIFIED"
    BLOCKED = "BLOCKED"


class AnswerStatus(str, Enum):
    ANSWER_SUPPORTED = "ANSWER_SUPPORTED"
    ANSWER_PARTIALLY_SUPPORTED = "ANSWER_PARTIALLY_SUPPORTED"
    NO_RELEVANT_SOURCE = "NO_RELEVANT_SOURCE"
    CONFLICTING_SOURCES = "CONFLICTING_SOURCES"
    SOURCE_BLOCKED = "SOURCE_BLOCKED"


@dataclass
class KnowledgeSource:
    source_id: str = ""
    source_type: str = ""
    title: str = ""
    origin: str = ""
    version: str = "1.0"
    updated_at: str = ""
    trust_level: TrustLevel = TrustLevel.UNVERIFIED
    access_policy: str = "public"
    language: str = "fr"
    checksum: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeCitation:
    citation_id: str = field(default_factory=lambda: uuid4().hex[:16])
    source: KnowledgeSource | None = None
    text: str = ""
    relevance_score: float = 0.0
    page_ref: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeQuery:
    query_id: str = field(default_factory=lambda: uuid4().hex[:16])
    text: str = ""
    project_id: str = ""
    allowed_sources: tuple[str, ...] = ()
    max_results: int = 5
    min_score: float = 0.3
    language: str = "fr"
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeResult:
    result_id: str = field(default_factory=lambda: uuid4().hex[:16])
    query_id: str = ""
    status: AnswerStatus = AnswerStatus.NO_RELEVANT_SOURCE
    answer: str = ""
    citations: list[KnowledgeCitation] = field(default_factory=list)
    sources: list[KnowledgeSource] = field(default_factory=list)
    confidence: float = 0.0
    warnings: list[str] = field(default_factory=list)
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class KnowledgeGateway:
    def __init__(self, knowledge_service: Any = None, rag_service: Any = None) -> None:
        self._knowledge = knowledge_service
        self._rag = rag_service

    def query(self, request: KnowledgeQuery) -> KnowledgeResult:
        result = KnowledgeResult(
            query_id=request.query_id,
            correlation_id=request.correlation_id,
        )

        if self._knowledge:
            try:
                kr = self._knowledge.query(request.text)
                if kr:
                    result.sources.extend(kr)
            except Exception as e:
                logger.error("knowledge query error: %s", e)

        if self._rag:
            try:
                rr = self._rag.retrieve(request.text, top_k=request.max_results)
                if rr:
                    for r in rr:
                        result.sources.append(
                            KnowledgeSource(
                                source_id=r.get("id", ""),
                                title=r.get("title", ""),
                                trust_level=TrustLevel.VERIFIED_INTERNAL,
                            )
                        )
            except Exception as e:
                logger.error("rag retrieve error: %s", e)

        if result.sources:
            result.status = AnswerStatus.ANSWER_SUPPORTED

        return result
