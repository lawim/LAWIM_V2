from __future__ import annotations

from typing import Any

from ..persona import assistant_greeting, assistant_persona, assistant_start_message
from .intent_engine import IntentEngine, analyze_message
from .memory import BrainMemory
from .progression import ProgressionEngine, build_progression_state
from .resumption import ResumeEngine, build_resumption
from .accompaniment import AccompanimentEngine, evaluate_suggestions

ADVISOR_PERSONAS: dict[str, str] = {
    "fr": assistant_persona("fr"),
    "en": assistant_persona("en"),
    "pcm": assistant_persona("pcm"),
}

GREETINGS: dict[str, str] = {
    "fr": assistant_start_message("fr"),
    "en": assistant_start_message("en"),
    "pcm": assistant_start_message("pcm"),
}


def _project_type_from_intent(intent: str) -> str:
    mapping = {
        "buy": "buy",
        "rent": "rent",
        "sell": "sell",
        "invest": "invest",
        "build": "build",
        "find_land": "buy",
        "find_property": "buy",
        "find_partner": "other",
        "find_funding": "buy",
        "manage": "other",
    }
    return mapping.get(intent, "other")


class AdvisorEngine:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.intent_engine = IntentEngine()
        self.memory = BrainMemory(repository)
        self.progression = ProgressionEngine()
        self.resumption = ResumeEngine()
        self.accompaniment = AccompanimentEngine()

    def process_message(
        self,
        *,
        project_id: int | None,
        message: str,
        language: str = "fr",
        session_id: int | None = None,
    ) -> dict[str, Any]:
        analysis = analyze_message(message)
        detected_lang = analysis.get("language", language)
        lang = detected_lang if detected_lang in {"fr", "en", "pcm"} else language

        project = None
        if project_id is not None:
            project = self.repository.get_project(project_id)

        memory_items = []
        if project_id is not None:
            memory_items = self.memory.get_active(project_id)

        progression = self.progression.compute(
            project_id=project_id or 0,
            intent=analysis["primary_intent"],
            entities=analysis.get("entities", {}),
            memory_items=memory_items,
            project=project,
        )

        suggestions = self.accompaniment.suggest(
            intent=analysis["primary_intent"],
            entities=analysis.get("entities", {}),
            progression=progression,
            memory_items=memory_items,
        )

        return {
            "analysis": analysis,
            "detected_language": lang,
            "project": project,
            "progression": progression,
            "suggestions": suggestions,
            "memory_summary": self.memory.get_summary(project_id) if project_id else None,
        }

    def build_resumption(
        self,
        *,
        project_id: int,
        language: str = "fr",
    ) -> dict[str, Any]:
        project = self.repository.get_project(project_id)
        confirmed = self.memory.get_active(project_id, kind="confirmed_fact")
        pending = self.memory.get_pending(project_id)
        progression = self.progression.compute(
            project_id=project_id,
            intent=project.get("project_type", "other") if project else "other",
            entities={},
            memory_items=confirmed + pending,
            project=project,
        )

        last_action = None
        recent_suggestions = self.repository.list_brain_suggestions(
            project_id, status="active", limit=1
        )
        if recent_suggestions:
            last_action = str(recent_suggestions[0].get("content", ""))

        return build_resumption(
            project=project,
            confirmed_facts=confirmed,
            pending_hypotheses=pending,
            last_action=last_action,
            next_step=progression.get("next_actions", [None])[0] if progression.get("next_actions") else None,
            next_question=progression.get("next_question"),
            language=language,
        )

    def get_greeting(self, language: str = "fr") -> str:
        lang = language if language in GREETINGS else "fr"
        return assistant_greeting(lang)

    def get_persona(self, language: str = "fr") -> str:
        lang = language if language in ADVISOR_PERSONAS else "fr"
        return assistant_persona(lang)

    def handle_confirmation(
        self,
        *,
        project_id: int,
        message: str,
        language: str = "fr",
    ) -> dict[str, Any]:
        analysis = analyze_message(message)
        is_confirm = analysis.get("is_confirmation")
        if is_confirm is None:
            return {"handled": False, "reason": "ambiguous"}

        pending = self.memory.get_pending(project_id)
        if not pending:
            return {"handled": False, "reason": "no_pending"}

        results: list[dict[str, Any]] = []
        for item in pending:
            if is_confirm:
                result = self.memory.confirm(project_id, str(item["memory_key"]))
                results.append({"key": item["memory_key"], "action": "confirmed", "success": result is not None})
            else:
                result = self.memory.reject(project_id, str(item["memory_key"]))
                results.append({"key": item["memory_key"], "action": "rejected", "success": result is not None})

        return {"handled": True, "results": results}

    def store_intent(
        self,
        *,
        project_id: int,
        analysis: dict[str, Any],
        session_id: int | None = None,
        source_message_id: int | None = None,
    ) -> dict[str, Any] | None:
        return self.repository.create_brain_intent(
            project_id=project_id,
            session_id=session_id,
            source_message_id=source_message_id,
            intent_type=analysis["primary_intent"],
            entities_json=analysis.get("entities", {}),
            language=analysis.get("language", "fr"),
            confidence=analysis["primary_score"],
            status="hypothesis",
            engine_version="1.0.0",
        )
