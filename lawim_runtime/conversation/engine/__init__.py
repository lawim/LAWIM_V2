from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..intent import IntentEngine, IntentResult
from ..entity import EntityExtractionEngine, EntityResult
from ..memory import ConversationMemory, MemoryContext
from ..qualification import QualificationEngine, QualificationResult, QualificationLevel
from ..llm import LLMAdapter, LLMContract


@dataclass
class ConversationTurnResult:
    turn_id: str = ""
    intent: IntentResult | None = None
    entities: EntityResult | None = None
    qualification: QualificationResult | None = None
    memory: MemoryContext | None = None
    llm_analysis: LLMContract | None = None
    response_type: str = ""
    missing_fields: list[str] = field(default_factory=list)
    needs_clarification: bool = False
    error: str = ""


class ConversationEngine:
    def __init__(
        self,
        intent_engine: IntentEngine | None = None,
        entity_engine: EntityExtractionEngine | None = None,
        memory: ConversationMemory | None = None,
        qualification_engine: QualificationEngine | None = None,
        llm_adapter: LLMAdapter | None = None,
    ) -> None:
        self._intent = intent_engine or IntentEngine()
        self._entity = entity_engine or EntityExtractionEngine()
        self._memory = memory or ConversationMemory()
        self._qualification = qualification_engine or QualificationEngine()
        self._llm = llm_adapter

    def process(self, text: str, context: dict[str, Any] | None = None) -> ConversationTurnResult:
        result = ConversationTurnResult()

        if not text or not text.strip():
            result.error = "empty_input"
            return result

        # 1. LLM analysis (optional, provider-independent)
        llm_result = None
        if self._llm:
            try:
                llm_result = self._llm.analyze(text, context)
                result.llm_analysis = llm_result
            except Exception:
                pass

        # 2. Intent detection (LLM-independent)
        intent_result = self._intent.detect(text, context)
        if llm_result and llm_result.confidence > intent_result.confidence:
            intent_result.intent = llm_result.intent
            intent_result.confidence = llm_result.confidence
        result.intent = intent_result

        # 3. Entity extraction (LLM-independent)
        entity_result = self._entity.extract(text)
        if llm_result and llm_result.entities:
            for k, v in llm_result.entities.items():
                if k not in entity_result.entities:
                    entity_result.entities[k] = v
        result.entities = entity_result

        # 4. Memory update
        self._memory.add_entry("user", text, intent_result.intent, entity_result.entities)
        self._memory.update_preferences(entity_result.entities)
        result.memory = self._memory.get_context()

        # 5. Qualification (LLM-independent)
        qual_result = self._qualification.evaluate(intent_result.intent, entity_result.entities, context)
        self._memory.set_qualification(qual_result.level.value)
        result.qualification = qual_result
        result.missing_fields = qual_result.missing_fields
        result.needs_clarification = intent_result.needs_clarification or qual_result.level in (
            QualificationLevel.INCOMPLETE, QualificationLevel.INITIAL,
        )

        # 6. Response type determination (business logic, no LLM)
        result.response_type = self._determine_response_type(intent_result, qual_result, entity_result)

        return result

    def add_assistant_response(self, text: str) -> None:
        self._memory.add_entry("assistant", text)

    def _determine_response_type(
        self,
        intent: IntentResult,
        qual: QualificationResult,
        entities: EntityResult,
    ) -> str:
        if intent.needs_clarification:
            return "CLARIFY_INTENT"
        if qual.level in (QualificationLevel.INCOMPLETE, QualificationLevel.INITIAL):
            return "ASK_MISSING_FIELDS"
        if qual.level == QualificationLevel.PARTIAL:
            return "CONFIRM_AND_ASK"
        if qual.level == QualificationLevel.READY_FOR_DECISION:
            return "READY_FOR_PROCESSING"
        return "PROCESS"
