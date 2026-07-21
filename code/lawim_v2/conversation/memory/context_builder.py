from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class BusinessMemoryContext:
    conversation_state: Any | None = None
    case: Any | None = None
    active_slots: dict[str, Any] = field(default_factory=dict)
    missing_slots: list[str] = field(default_factory=list)
    last_question: str = ""
    intent: str = ""
    journey_code: str = ""
    readiness: str = "not_started"
    language: str = "fr"
    handover_status: str | None = None
    recent_decisions: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ProviderMemoryContext:
    language: str = "fr"
    intent: str = ""
    active_facts: dict[str, Any] = field(default_factory=dict)
    last_question_text: str = ""
    response_instructions: list[str] = field(default_factory=list)
    prohibitions: list[str] = field(default_factory=list)
    summary: str = ""


@dataclass
class HumanHandoverContext:
    case_id: str = ""
    case_code: str = ""
    actor_id: str = ""
    summary: str = ""
    known_information: dict[str, Any] = field(default_factory=dict)
    missing_information: list[str] = field(default_factory=list)
    recent_interactions: list[dict[str, Any]] = field(default_factory=list)
    handover_reason: str = ""
    expected_actions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    language: str = "fr"
    contact_info: dict[str, Any] = field(default_factory=dict)


class MemoryContextBuilder:
    def __init__(
        self,
        lawim_case_service: Any = None,
        conversation_state_repository: Any = None,
        fact_repository: Any = None,
    ) -> None:
        self._case_service = lawim_case_service
        self._state_repo = conversation_state_repository
        self._fact_repo = fact_repository

    def build_business_context(
        self,
        conversation_id: str,
        case_id: str | None = None,
    ) -> BusinessMemoryContext:
        state = self._load_state(conversation_id)
        case = self._load_case(case_id) if case_id else None
        active_slots = self._collect_active_slots(state, case)
        missing_slots = list(state.missing_slots) if state else []
        readiness = self._compute_readiness(state)

        return BusinessMemoryContext(
            conversation_state=state,
            case=case,
            active_slots=active_slots,
            missing_slots=missing_slots,
            last_question=state.last_lawim_message if state else "",
            intent=state.current_intent or "" if state else "",
            journey_code=readiness.get("journey_code", ""),
            readiness=readiness.get("status", "not_started"),
            language=state.language if state else "fr",
            handover_status=state.handover_status if state else None,
        )

    def build_provider_context(
        self,
        conversation_id: str,
        case_id: str | None = None,
        max_chars: int = 2000,
    ) -> ProviderMemoryContext:
        state = self._load_state(conversation_id)
        if not state:
            return ProviderMemoryContext()

        active_facts = self._collect_active_slots(state, None)
        summary_text = self._build_summary_snippet(state, active_facts, max_chars)

        response_instructions = self._build_response_instructions(state)
        prohibitions = self._build_prohibitions()

        return ProviderMemoryContext(
            language=state.language or "fr",
            intent=state.current_intent or "",
            active_facts=active_facts,
            last_question_text=state.last_lawim_message or "",
            response_instructions=response_instructions,
            prohibitions=prohibitions,
            summary=summary_text,
        )

    def build_handover_context(self, case_id: str) -> HumanHandoverContext:
        case = self._load_case(case_id) if case_id else None
        if not case:
            return HumanHandoverContext(
                case_id=case_id,
                handover_reason="case_not_found",
                limitations=["Case data unavailable for handover context"],
            )

        case_dict = self._to_case_dict(case)
        known_info = case_dict.get("known_slots", {})
        missing_info = case_dict.get("missing_slots", [])
        lang = case_dict.get("language", "fr")

        return HumanHandoverContext(
            case_id=case_id,
            case_code=case_dict.get("case_code", ""),
            actor_id=case_dict.get("actor_id", ""),
            summary=self._build_handover_summary(case_dict),
            known_information=known_info,
            missing_information=missing_info,
            handover_reason=case_dict.get("handover_reason", ""),
            expected_actions=case_dict.get("expected_actions", []),
            limitations=["LAWIM AI cannot handle this request. Human intervention required."],
            language=lang,
            contact_info=case_dict.get("contact_info", {}),
        )

    def build_resume_context(
        self,
        actor_id: str,
        conversation_id: str,
    ) -> dict[str, Any]:
        state = self._load_state(conversation_id)
        context: dict[str, Any] = {
            "actor_id": actor_id,
            "conversation_id": conversation_id,
            "language": state.language if state else "fr",
            "intent": state.current_intent if state else None,
            "known_slots": dict(state.known_slots) if state else {},
            "missing_slots": list(state.missing_slots) if state else [],
            "qualification_status": state.qualification_status if state else "unqualified",
            "last_question": state.last_lawim_message if state else "",
            "handover_status": state.handover_status if state else None,
            "resumed_at": datetime.now(timezone.utc).isoformat(),
        }
        return context

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_state(self, conversation_id: str) -> Any | None:
        if not self._state_repo:
            return None
        try:
            if hasattr(self._state_repo, "load_by_conversation_id"):
                return self._state_repo.load_by_conversation_id(conversation_id)
            if hasattr(self._state_repo, "load") and conversation_id.isdigit():
                return self._state_repo.load(conversation_id)
        except Exception:
            return None
        return None

    def _load_case(self, case_id: str) -> Any | None:
        if not self._case_service:
            return None
        try:
            if hasattr(self._case_service, "get_case"):
                return self._case_service.get_case(case_id)
            if hasattr(self._case_service, "load"):
                return self._case_service.load(case_id)
        except Exception:
            return None
        return None

    def _collect_active_slots(
        self,
        state: Any | None,
        case: Any | None,
    ) -> dict[str, Any]:
        slots: dict[str, Any] = {}
        if state and hasattr(state, "known_slots"):
            slots.update(state.known_slots)
        if case:
            case_slots = self._to_case_dict(case).get("known_slots", {})
            for k, v in case_slots.items():
                slots.setdefault(k, v)
        return slots

    def _compute_readiness(self, state: Any | None) -> dict[str, str]:
        if not state:
            return {"status": "not_started", "journey_code": ""}
        return {
            "status": state.qualification_status or "not_started",
            "journey_code": state.current_intent or "",
        }

    def _build_summary_snippet(
        self,
        state: Any,
        active_facts: dict[str, Any],
        max_chars: int,
    ) -> str:
        parts: list[str] = []
        if state.current_intent:
            parts.append(f"intent={state.current_intent}")
        if active_facts:
            parts.append(f"slots={json.dumps(active_facts, ensure_ascii=False)}")
        if state.handover_status:
            parts.append(f"handover={state.handover_status}")
        text = " | ".join(parts)
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        return text

    def _build_response_instructions(self, state: Any) -> list[str]:
        instructions: list[str] = []
        if state.current_intent:
            instructions.append(
                f"Intent: {state.current_intent}"  # noqa: E501
            )
        if state.missing_slots:
            fields = ", ".join(state.missing_slots[:5])
            instructions.append(f"Missing information: {fields}. Continue qualifying.")
        if state.last_question_key:
            instructions.append(
                "Respond naturally based on the conversation plan."  # noqa: E501
            )
        return instructions

    def _build_prohibitions(self) -> list[str]:
        return [
            "Do not refer the user to external real-estate platforms (Jumia, SeLoger, Leboncoin, Facebook, Lamudi).",
            "Do not act as a neutral assistant; you are LAWIM AI.",
            "Do not provide unsolicited translations or grammar corrections.",
            "Do not make business decisions on behalf of the platform.",
            "Do not expose internal system details, secrets, or message IDs.",
        ]

    def _build_handover_summary(self, case_dict: dict[str, Any]) -> str:
        intent = case_dict.get("current_intent") or case_dict.get("intent", "")
        lang = case_dict.get("language", "fr")
        known = case_dict.get("known_slots", {})
        missing = case_dict.get("missing_slots", [])
        lines: list[str] = []
        if intent:
            lines.append(f"Intent: {intent}")
        if known:
            lines.append(
                f"Known: {json.dumps(known, ensure_ascii=False)}"  # noqa: E501
            )
        if missing:
            lines.append(f"Missing: {', '.join(missing)}")
        lines.append(f"Language: {lang}")
        return "\n".join(lines)

    def _to_case_dict(self, case: Any) -> dict[str, Any]:
        if isinstance(case, dict):
            return case
        if hasattr(case, "to_dict"):
            return case.to_dict()
        result: dict[str, Any] = {}
        for attr in (
            "case_code",
            "actor_id",
            "language",
            "current_intent",
            "intent",
            "known_slots",
            "missing_slots",
            "handover_reason",
            "expected_actions",
            "contact_info",
            "qualification_status",
        ):
            if hasattr(case, attr):
                result[attr] = getattr(case, attr)
        return result
