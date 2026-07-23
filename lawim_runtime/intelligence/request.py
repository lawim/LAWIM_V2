from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class AITaskType(str, Enum):
    LANGUAGE_DETECTION = "LANGUAGE_DETECTION"
    INTENT_EXTRACTION = "INTENT_EXTRACTION"
    ENTITY_EXTRACTION = "ENTITY_EXTRACTION"
    FIELD_EXTRACTION = "FIELD_EXTRACTION"
    CORRECTION_DETECTION = "CORRECTION_DETECTION"
    CONFIRMATION_DETECTION = "CONFIRMATION_DETECTION"
    NEGATION_DETECTION = "NEGATION_DETECTION"
    REFERENCE_RESOLUTION = "REFERENCE_RESOLUTION"
    DOCUMENT_METADATA_EXTRACTION = "DOCUMENT_METADATA_EXTRACTION"
    LOCATION_EXTRACTION = "LOCATION_EXTRACTION"
    DATE_EXTRACTION = "DATE_EXTRACTION"
    BUDGET_EXTRACTION = "BUDGET_EXTRACTION"
    CONTACT_EXTRACTION = "CONTACT_EXTRACTION"
    MULTI_PROJECT_SIGNAL_DETECTION = "MULTI_PROJECT_SIGNAL_DETECTION"
    RESPONSE_WRITING = "RESPONSE_WRITING"
    KNOWLEDGE_QUERY = "KNOWLEDGE_QUERY"
    RAG_QUERY = "RAG_QUERY"


@dataclass(frozen=True)
class AIRequest:
    request_id: str = field(default_factory=lambda: uuid4().hex[:16])
    task_type: AITaskType = AITaskType.FIELD_EXTRACTION
    interaction_id: str = ""
    project_id: str = ""
    session_id: str = ""
    conversation_id: str = ""
    language: str = "fr"
    input_text: str = ""
    structured_context: dict[str, Any] = field(default_factory=dict)
    allowed_fields: tuple[str, ...] = ()
    allowed_sources: tuple[str, ...] = ()
    response_schema: dict[str, Any] | None = None
    prompt_version: str = ""
    provider_policy: str = ""
    timeout_ms: int = 30000
    correlation_id: str = ""
    causation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
