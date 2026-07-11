from __future__ import annotations

from typing import Any

from ..observability import METRICS
from .advisor import AdvisorEngine
from .relation import RelationEngine
from . import dto as bdto


class BrainService:
    def __init__(self, repository, project_service) -> None:
        self.repository = repository
        self.projects = project_service
        self.advisor = AdvisorEngine(repository)
        self.relations = RelationEngine(repository)

    def _require_access(self, actor: dict[str, object], project_id: int) -> None:
        self.projects._require_access(actor, project_id)

    def _user_id(self, actor: dict[str, object]) -> int:
        user_id = actor.get("id")
        if user_id is None:
            from ..project_service import ProjectPermissionDenied
            raise ProjectPermissionDenied("Authentication required")
        return int(user_id)

    def process_chat(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
        message: str,
        session_id: int | None = None,
        language: str | None = None,
        channel: str = "web",
    ) -> dict[str, Any]:
        self._require_access(actor, project_id)
        METRICS.increment("brain_chat")

        result = self.advisor.process_message(
            project_id=project_id,
            message=message,
            language=language or "fr",
            session_id=session_id,
        )

        intent_row = self.advisor.store_intent(
            project_id=project_id,
            analysis=result["analysis"],
            session_id=session_id,
        )

        progression = result.get("progression", {})
        self.repository.upsert_brain_progression(
            project_id=project_id,
            intent_type=result["analysis"]["primary_intent"],
            current_step=progression.get("progress_pct", 0),
            total_steps=progression.get("total_steps", 0),
            missing_fields=progression.get("missing_fields", []),
            next_question=progression.get("next_question"),
            next_question_key=progression.get("next_key"),
            status="complete" if progression.get("complete") else "in_progress",
        )

        suggestions = result.get("suggestions", [])
        if suggestions:
            self.advisor.accompaniment.persist_suggestions(
                self.repository,
                project_id=project_id,
                suggestions=suggestions,
                language=result.get("detected_language", "fr"),
            )

        METRICS.increment("brain_intents")
        return {
            "analysis": bdto.intent_dto(result["analysis"]),
            "detected_language": result["detected_language"],
            "progression": bdto.progression_dto(progression),
            "suggestions": [bdto.suggestion_dto(s) for s in suggestions],
            "memory_summary": result.get("memory_summary"),
            "intent_id": intent_row.get("id") if intent_row else None,
        }

    def get_resumption(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
        language: str = "fr",
    ) -> dict[str, Any]:
        self._require_access(actor, project_id)
        METRICS.increment("brain_resumption")
        resumption = self.advisor.build_resumption(
            project_id=project_id,
            language=language,
        )
        return {"resumption": bdto.resumption_dto(resumption)}

    def get_memory_summary(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
    ) -> dict[str, Any]:
        self._require_access(actor, project_id)
        METRICS.increment("brain_memory")
        summary = self.advisor.memory.get_summary(project_id)
        return {"memory": summary}

    def get_suggestions(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
        status: str | None = "active",
    ) -> dict[str, Any]:
        self._require_access(actor, project_id)
        suggestions = self.repository.list_brain_suggestions(project_id, status=status)
        return {"suggestions": [bdto.suggestion_dto(s) for s in suggestions]}

    def list_dossiers(
        self,
        *,
        actor: dict[str, object],
        status: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        METRICS.increment("brain_dossiers")
        user_id = self._user_id(actor)
        result = self.projects.list_projects(
            actor=actor,
            user_id=user_id,
            status=status,
            limit=limit,
        )
        projects = result.get("projects", []) if isinstance(result, dict) else result
        if not isinstance(projects, list):
            projects = []
        results: list[dict[str, Any]] = []
        for proj in projects:
            pid = int(proj["id"])
            lang = str(proj.get("preferred_language") or actor.get("preferred_language") or "fr")
            resumption = self.advisor.build_resumption(
                project_id=pid,
                language=lang,
            )
            results.append({
                "project": proj,
                "resume": bdto.resumption_dto(resumption),
            })
        return {"dossiers": results}

    def handle_confirmation(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
        message: str,
        language: str = "fr",
    ) -> dict[str, Any]:
        self._require_access(actor, project_id)
        METRICS.increment("brain_confirmation")
        return self.advisor.handle_confirmation(
            project_id=project_id,
            message=message,
            language=language,
        )

    # ── Relation methods ──

    def find_matches(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
        partner_type: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        self._require_access(actor, project_id)
        METRICS.increment("brain_relation_find")
        project = self.repository.get_project(project_id)
        analysis = None
        recent_intents = self.repository.list_brain_intents(project_id, limit=1)
        if recent_intents:
            analysis = {"primary_intent": recent_intents[0].get("intent_type"), "entities": {}, "language": "fr"}
        result = self.relations.run_full_match(
            project_id=project_id,
            project=project,
            analysis=analysis,
        )
        return result

    def get_proposals(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
        status: str | None = None,
    ) -> dict[str, Any]:
        self._require_access(actor, project_id)
        proposals = self.relations.list_proposals(project_id, status=status)
        return {"proposals": proposals}

    def accept_proposal(
        self,
        *,
        actor: dict[str, object],
        proposal_id: int,
    ) -> dict[str, Any]:
        result = self.relations.accept_proposal(proposal_id)
        if result is None:
            from ..errors import NotFoundError
            raise NotFoundError("Proposal not found")
        return {"proposal": result}

    def reject_proposal(
        self,
        *,
        actor: dict[str, object],
        proposal_id: int,
    ) -> dict[str, Any]:
        result = self.relations.reject_proposal(proposal_id)
        if result is None:
            from ..errors import NotFoundError
            raise NotFoundError("Proposal not found")
        return {"proposal": result}

    def request_consent(
        self,
        *,
        actor: dict[str, object],
        proposal_id: int,
    ) -> dict[str, Any]:
        result = self.relations.request_consent(proposal_id)
        if result is None:
            from ..errors import NotFoundError
            raise NotFoundError("Proposal not found")
        return {"proposal": result}

    def grant_consent(
        self,
        *,
        actor: dict[str, object],
        proposal_id: int,
    ) -> dict[str, Any]:
        result = self.relations.grant_consent(proposal_id)
        if result is None:
            from ..errors import NotFoundError
            raise NotFoundError("Proposal not found")
        return {"proposal": result}

    def list_established_relations(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
    ) -> list[dict[str, Any]]:
        self._require_access(actor, project_id)
        return self.repository.list_relations(project_id)
