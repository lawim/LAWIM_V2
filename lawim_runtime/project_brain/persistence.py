from __future__ import annotations
from typing import Any
from .state import ProjectBrainState
from ..qualification.result import QualificationResult
from ..decision.result import DecisionResult


class ProjectBrainRepository:
    def __init__(self) -> None:
        self._qual_results: list[QualificationResult] = []
        self._decisions: list[DecisionResult] = []
        self._brain_states: dict[str, ProjectBrainState] = {}

    def save_qualification(self, result: QualificationResult) -> None:
        self._qual_results.append(result)

    def get_latest_qualification(self, project_id: str) -> QualificationResult | None:
        for r in reversed(self._qual_results):
            if r.project_id == project_id:
                return r
        return None

    def save_decision(self, result: DecisionResult) -> None:
        self._decisions.append(result)

    def get_latest_decision(self, project_id: str) -> DecisionResult | None:
        for r in reversed(self._decisions):
            if r.project_id == project_id:
                return r
        return None

    def save_brain_state(self, state: ProjectBrainState) -> None:
        self._brain_states[state.project_id] = state

    def get_brain_state(self, project_id: str) -> ProjectBrainState | None:
        return self._brain_states.get(project_id)

    def list_all_brain_states(self) -> list[ProjectBrainState]:
        return list(self._brain_states.values())

    def list_all_qualifications(self) -> list[QualificationResult]:
        return list(self._qual_results)

    def list_all_decisions(self) -> list[DecisionResult]:
        return list(self._decisions)

    def clear(self) -> None:
        self._qual_results.clear()
        self._decisions.clear()
        self._brain_states.clear()
