from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class ConversationSummary:
    summary_id: str = ""
    conversation_id: str = ""
    case_id: str = ""
    intent: str = ""
    active_slots: dict[str, Any] = field(default_factory=dict)
    important_decisions: list[dict[str, Any]] = field(default_factory=list)
    pending_question: str = ""
    readiness: str = ""
    user_constraints: list[str] = field(default_factory=list)
    human_actions: list[dict[str, Any]] = field(default_factory=list)
    language: str = "fr"
    interaction_count: int = 0
    last_updated_at: str = ""
    created_at: str = ""
    version: int = 1


class ConversationSummaryService:
    def __init__(self, repository: Any = None) -> None:
        self._repository = repository

    def generate_or_refresh(
        self,
        conversation_id: str,
        case_id: str | None = None,
        force: bool = False,
    ) -> ConversationSummary:
        existing = self.get_summary(conversation_id)

        if existing and not force:
            if self._is_fresh(existing):
                return existing

        if existing:
            turns = self._load_turns(conversation_id)
            summary = self._reconcile(existing, turns, case_id)
        else:
            turns = self._load_turns(conversation_id)
            summary = self._build_initial(conversation_id, turns, case_id)

        summary.last_updated_at = datetime.now(timezone.utc).isoformat()
        summary.version = (existing.version + 1) if existing else 1
        return self.save_summary(summary)

    def get_summary(self, conversation_id: str) -> ConversationSummary | None:
        if not self._repository:
            return None
        try:
            if hasattr(self._repository, "get_summary"):
                return self._repository.get_summary(conversation_id)
            if hasattr(self._repository, "load"):
                raw = self._repository.load(conversation_id)
                if raw:
                    return self._deserialize(raw)
        except Exception:
            return None
        return None

    def save_summary(self, summary: ConversationSummary) -> ConversationSummary:
        if not self._repository:
            return summary
        try:
            if hasattr(self._repository, "save_summary"):
                return self._repository.save_summary(summary)
            if hasattr(self._repository, "save"):
                self._repository.save(summary)
        except Exception:
            pass
        return summary

    def summarize_turns(self, turns: list[dict[str, Any]], max_tokens: int = 500) -> str:
        if not turns:
            return ""

        compressed: list[str] = []
        for t in turns[-20:]:
            msg = t.get("message", t.get("user_message", ""))[:200]
            compressed.append(msg)

        text = " | ".join(compressed)
        if len(text) > max_tokens * 4:
            text = text[: max_tokens * 4] + "..."
        return text

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _is_fresh(self, summary: ConversationSummary, max_age_seconds: int = 60) -> bool:
        if not summary.last_updated_at:
            return False
        try:
            updated = datetime.fromisoformat(summary.last_updated_at)
            delta = datetime.now(timezone.utc) - updated.replace(tzinfo=timezone.utc)
            return delta.total_seconds() < max_age_seconds
        except (ValueError, TypeError):
            return False

    def _load_turns(self, conversation_id: str) -> list[dict[str, Any]]:
        if not self._repository:
            return []
        try:
            if hasattr(self._repository, "get_turns"):
                return self._repository.get_turns(conversation_id)
            if hasattr(self._repository, "load_turns"):
                return self._repository.load_turns(conversation_id)
        except Exception:
            pass
        return []

    def _reconcile(
        self,
        existing: ConversationSummary,
        turns: list[dict[str, Any]],
        case_id: str | None,
    ) -> ConversationSummary:
        if case_id:
            existing.case_id = case_id
        existing.interaction_count = len(turns) if turns else existing.interaction_count

        decisions = self._extract_decisions(turns)
        if decisions:
            existing.important_decisions.extend(decisions)

        if case_id and not existing.case_id:
            existing.case_id = case_id

        return existing

    def _build_initial(
        self,
        conversation_id: str,
        turns: list[dict[str, Any]],
        case_id: str | None,
    ) -> ConversationSummary:
        now = datetime.now(timezone.utc).isoformat()
        intent = ""
        active_slots: dict[str, Any] = {}
        decisions: list[dict[str, Any]] = []
        pending = ""
        readiness = ""
        user_constraints: list[str] = []
        language = "fr"

        for t in turns:
            msg = t.get("message", "") or t.get("user_message", "") or ""
            intent = t.get("intent") or t.get("current_intent") or intent
            lang = t.get("language") or ""
            if lang:
                language = lang
            slots = t.get("known_slots") or t.get("slots") or {}
            if isinstance(slots, dict):
                active_slots.update(slots)
            if t.get("pending_question"):
                pending = t["pending_question"]
            if t.get("readiness"):
                readiness = t["readiness"]

        decisions = self._extract_decisions(turns)

        return ConversationSummary(
            summary_id=str(uuid4()),
            conversation_id=conversation_id,
            case_id=case_id or "",
            intent=intent,
            active_slots=active_slots,
            important_decisions=decisions,
            pending_question=pending,
            readiness=readiness or "in_progress",
            user_constraints=user_constraints,
            language=language,
            interaction_count=len(turns),
            created_at=now,
            last_updated_at=now,
            version=1,
        )

    def _extract_decisions(self, turns: list[dict[str, Any]]) -> list[dict[str, Any]]:
        decisions: list[dict[str, Any]] = []
        for t in turns:
            action = t.get("action") or t.get("decision") or ""
            if action in ("correction", "consent", "handover", "qualification_complete"):
                decisions.append(
                    {
                        "type": action,
                        "timestamp": t.get("created_at", t.get("timestamp", "")),
                        "details": t.get("message", t.get("user_message", "")),
                    }
                )
        return decisions

    def _deserialize(self, raw: Any) -> ConversationSummary | None:
        if isinstance(raw, ConversationSummary):
            return raw
        if isinstance(raw, dict):
            return ConversationSummary(
                summary_id=raw.get("summary_id", ""),
                conversation_id=raw.get("conversation_id", ""),
                case_id=raw.get("case_id", ""),
                intent=raw.get("intent", ""),
                active_slots=raw.get("active_slots", {}),
                important_decisions=raw.get("important_decisions", []),
                pending_question=raw.get("pending_question", ""),
                readiness=raw.get("readiness", ""),
                user_constraints=raw.get("user_constraints", []),
                human_actions=raw.get("human_actions", []),
                language=raw.get("language", "fr"),
                interaction_count=raw.get("interaction_count", 0),
                last_updated_at=raw.get("last_updated_at", ""),
                created_at=raw.get("created_at", ""),
                version=raw.get("version", 1),
            )
        return None
