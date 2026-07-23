from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class ProjectResolutionStatus(str, Enum):
    RESOLVED = "RESOLVED"
    NEW_PROJECT = "NEW_PROJECT"
    AMBIGUOUS = "AMBIGUOUS"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"
    NOT_FOUND = "NOT_FOUND"


@dataclass
class ProjectResolutionResult:
    resolution_id: str = field(default_factory=lambda: uuid4().hex[:16])
    status: ProjectResolutionStatus = ProjectResolutionStatus.NOT_FOUND
    project_id: str = ""
    active_project_count: int = 0
    candidate_ids: list[str] = field(default_factory=list)
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class ProjectResolver:
    def __init__(self) -> None:
        self._user_projects: dict[str, list[dict[str, Any]]] = {}

    def register_project(self, user_id: str, project_id: str, status: str = "active") -> None:
        if user_id not in self._user_projects:
            self._user_projects[user_id] = []
        existing = [p for p in self._user_projects[user_id] if p["project_id"] == project_id]
        if not existing:
            self._user_projects[user_id].append({
                "project_id": project_id,
                "status": status,
            })

    def update_project_status(self, user_id: str, project_id: str, status: str) -> None:
        projects = self._user_projects.get(user_id, [])
        for p in projects:
            if p["project_id"] == project_id:
                p["status"] = status

    def resolve(self, user_id: str, known_intent: str = "") -> ProjectResolutionResult:
        if not user_id:
            return ProjectResolutionResult(
                status=ProjectResolutionStatus.NOT_FOUND,
                error="no user_id provided",
            )

        projects = self._user_projects.get(user_id, [])
        active = [p for p in projects if p["status"] == "active"]

        if len(active) == 1:
            return ProjectResolutionResult(
                status=ProjectResolutionStatus.RESOLVED,
                project_id=active[0]["project_id"],
                active_project_count=1,
                candidate_ids=[p["project_id"] for p in active],
            )

        if len(active) > 1:
            return ProjectResolutionResult(
                status=ProjectResolutionStatus.AMBIGUOUS,
                active_project_count=len(active),
                candidate_ids=[p["project_id"] for p in active],
                error="multiple active projects found",
            )

        closed = [p for p in projects if p["status"] == "closed"]
        if closed:
            return ProjectResolutionResult(
                status=ProjectResolutionStatus.CLOSED,
                project_id=closed[-1]["project_id"],
                active_project_count=0,
                candidate_ids=[p["project_id"] for p in closed],
            )

        return ProjectResolutionResult(
            status=ProjectResolutionStatus.NEW_PROJECT,
            active_project_count=0,
        )

    def count_projects(self, user_id: str) -> int:
        return len(self._user_projects.get(user_id, []))
