from __future__ import annotations

from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as cdto


class CognitionService:
    def __init__(self, repository, project_service: ProjectService) -> None:
        self.repository = repository
        self.projects = project_service

    def _require_access(self, actor: dict[str, object], project_id: int) -> None:
        self.projects._require_access(actor, project_id)

    def _require_manage(self, actor: dict[str, object], project_id: int) -> None:
        self.projects._require_manage(actor, project_id)

    def get_graph(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        METRICS.increment("cognition_graph")
        return {"graph": cdto.knowledge_graph_dto(self.repository.get_knowledge_graph(project_id))}

    def get_context(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        METRICS.increment("cognition_context")
        return {"context": self.repository.get_knowledge_context(project_id)}

    def refresh(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_manage(actor, project_id)
        payload = self.repository.refresh_project_cognition(project_id)
        METRICS.increment("cognition_refresh")
        return {"intelligence": payload}

    def list_decisions(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        return {"decisions": [cdto.decision_dto(d) for d in self.repository.list_cognition_decisions(project_id)]}

    def get_decision(self, *, actor: dict[str, object], project_id: int, decision_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        return {"decision": cdto.decision_dto(self.repository.get_cognition_decision(project_id, decision_id))}

    def list_reasoning(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        METRICS.increment("cognition_reasoning")
        return {"reasoning": [cdto.reasoning_dto(r) for r in self.repository.list_reasoning_traces(project_id)]}

    def list_simulations(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        return {
            "scenarios": self.repository.list_simulation_scenarios(),
            "runs": [cdto.simulation_dto(r) for r in self.repository.list_simulation_runs(project_id)],
        }

    def run_simulation(self, *, actor: dict[str, object], project_id: int, scenario_key: str, parameters: dict[str, object] | None = None) -> dict[str, object]:
        self._require_manage(actor, project_id)
        result = self.repository.run_simulation(project_id, scenario_key, parameters)
        METRICS.increment("cognition_simulation")
        return {"simulation": cdto.simulation_dto(result)}

    def get_intelligence(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        METRICS.increment("cognition_intelligence")
        return {"intelligence": cdto.intelligence_workspace_dto(self.repository.get_intelligence_workspace(project_id))}

    def get_next_action(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        METRICS.increment("cognition_next_action")
        return {"next_action": cdto.next_best_action_dto(self.repository.get_next_best_action(project_id))}

    def list_risks(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        METRICS.increment("cognition_risks")
        return {"risks": [cdto.risk_intelligence_dto(r) for r in self.repository.list_risk_intelligence(project_id)]}

    def list_opportunities(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        METRICS.increment("cognition_opportunities")
        return {"opportunities": [cdto.opportunity_intelligence_dto(o) for o in self.repository.list_opportunity_intelligence(project_id)]}

    def list_inferences(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        return {"inferences": self.repository.list_knowledge_inferences(project_id)}

    def list_history(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        return {"history": self.repository.list_knowledge_history(project_id)}
