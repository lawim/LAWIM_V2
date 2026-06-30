from __future__ import annotations

from http import HTTPStatus

from ..dto import project_dto, project_progress_dto, project_step_dto
from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as idto


class IntelligentCoreService:
    def __init__(self, repository, project_service: ProjectService) -> None:
        self.repository = repository
        self.projects = project_service

    def _require_access(self, actor: dict[str, object], project_id: int) -> None:
        self.projects._require_access(actor, project_id)

    def _require_manage(self, actor: dict[str, object], project_id: int) -> None:
        self.projects._require_manage(actor, project_id)

    def get_workspace(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        payload = self.repository.get_project_workspace(project_id)
        METRICS.increment("intelligent_workspace")
        return idto.workspace_dto(payload, project_dto_fn=project_dto, step_dto_fn=project_step_dto, progress_dto_fn=project_progress_dto)

    def refresh_intelligence(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_manage(actor, project_id)
        result = self.repository.refresh_project_intelligence(project_id)
        return {
            "decision": idto.decision_dto(result["decision"]),
            "recommendations": [idto.recommendation_dto(row) for row in result["recommendations"]],
            "intelligence": result["intelligence"],
            "trust_score": idto.trust_score_dto(result["trust_score"]),
        }

    def journey_state(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        return self.repository.journey_engine_state(project_id)

    def replan_journey(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_manage(actor, project_id)
        return self.repository.replan_journey(project_id)

    def list_goals(self, *, actor: dict[str, object], project_id: int) -> list[dict[str, object]]:
        self._require_access(actor, project_id)
        return [idto.goal_dto(row) for row in self.repository.list_project_goals(project_id)]

    def create_goal(self, *, actor: dict[str, object], project_id: int, goal_key: str, title: str, priority: str = "normal") -> dict[str, object]:
        self._require_manage(actor, project_id)
        row = self.repository.create_project_goal(project_id=project_id, goal_key=goal_key, title=title, priority=priority)
        self.repository.refresh_project_intelligence(project_id)
        return idto.goal_dto(row)

    def list_knowledge(self, *, actor: dict[str, object], project_id: int, category: str | None = None) -> list[dict[str, object]]:
        self._require_access(actor, project_id)
        return [idto.knowledge_fact_dto(row) for row in self.repository.list_knowledge_facts(project_id=project_id, category=category)]

    def create_knowledge(self, *, actor: dict[str, object], project_id: int, category: str, fact_key: str, title: str, content: str) -> dict[str, object]:
        self._require_manage(actor, project_id)
        row = self.repository.create_knowledge_fact(project_id=project_id, category=category, fact_key=fact_key, title=title, content=content)
        return idto.knowledge_fact_dto(row)

    def list_recommendations(self, *, actor: dict[str, object], project_id: int) -> list[dict[str, object]]:
        self._require_access(actor, project_id)
        return [idto.recommendation_dto(row) for row in self.repository.list_project_recommendations(project_id)]

    def list_decisions(self, *, actor: dict[str, object], project_id: int) -> list[dict[str, object]]:
        self._require_access(actor, project_id)
        return [idto.decision_dto(row) for row in self.repository.list_project_decisions(project_id)]

    def list_actions(self, *, actor: dict[str, object], project_id: int) -> list[dict[str, object]]:
        self._require_access(actor, project_id)
        return [idto.action_dto(row) for row in self.repository.list_project_actions(project_id)]

    def create_action(self, *, actor: dict[str, object], project_id: int, action_key: str, title: str, priority: str = "normal", due_at: str | None = None) -> dict[str, object]:
        self._require_manage(actor, project_id)
        return idto.action_dto(self.repository.create_project_action(project_id=project_id, action_key=action_key, title=title, priority=priority, due_at=due_at))

    def list_tasks(self, *, actor: dict[str, object], project_id: int) -> list[dict[str, object]]:
        self._require_access(actor, project_id)
        return [idto.task_dto(row) for row in self.repository.list_project_tasks(project_id)]

    def create_task(self, *, actor: dict[str, object], project_id: int, title: str, action_id: int | None = None, due_at: str | None = None) -> dict[str, object]:
        self._require_manage(actor, project_id)
        return idto.task_dto(self.repository.create_project_task(project_id=project_id, title=title, action_id=action_id, assignee_user_id=int(actor["id"]), due_at=due_at))

    def list_life_events(self, *, actor: dict[str, object], project_id: int) -> list[dict[str, object]]:
        self._require_access(actor, project_id)
        return [idto.life_event_dto(row) for row in self.repository.list_life_events(project_id)]

    def create_life_event(self, *, actor: dict[str, object], project_id: int, event_type: str, title: str, occurred_at: str | None = None) -> dict[str, object]:
        self._require_manage(actor, project_id)
        return idto.life_event_dto(self.repository.create_life_event(project_id=project_id, user_id=int(actor["id"]), event_type=event_type, title=title, occurred_at=occurred_at))

    def get_timeline(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        from .engines import TimelineEngine

        return TimelineEngine().build_timeline(
            history=self.repository.list_project_step_history(project_id),
            entries=self.repository.list_timeline_entries(project_id),
            actions=self.repository.list_project_actions(project_id),
            milestones=self.repository.all("SELECT * FROM project_milestones WHERE project_id = ? ORDER BY id ASC", (project_id,)),
        )

    def link_property(self, *, actor: dict[str, object], project_id: int, property_id: int) -> dict[str, object]:
        self._require_manage(actor, project_id)
        self.repository.get_property(property_id)
        return self.repository.link_project_resource(project_id=project_id, resource_type="property", resource_id=property_id, role="candidate")

    def list_resources(self, *, actor: dict[str, object], project_id: int) -> list[dict[str, object]]:
        self._require_access(actor, project_id)
        return self.repository.list_project_resources(project_id)

    def search_knowledge_global(self, *, actor: dict[str, object], category: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if not self.projects.policy.is_admin(actor):
            raise ProjectPermissionDenied("Knowledge global search requires admin in this baseline")
        return [idto.knowledge_fact_dto(row) for row in self.repository.list_knowledge_facts(project_id=None, category=category, limit=limit)]
