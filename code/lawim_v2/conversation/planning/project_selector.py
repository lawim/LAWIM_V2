from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..understanding.short_replies import is_project_selection_ambiguity


@dataclass
class ProjectSelectionResult:
    action: str  # "select_existing", "request_new", "list_projects", "ambiguous", "none"
    project_id: int | None = None
    requires_confirmation: bool = False
    requires_clarification: bool = False
    requires_human: bool = False
    alternatives: list[dict[str, Any]] = field(default_factory=list)
    reply_text: str | None = None


def resolve_project_selection(
    user_message: str,
    active_projects: list[dict[str, Any]],
    *,
    user_id: int | None = None,
    conversation_project_id: int | None = None,
) -> ProjectSelectionResult:
    if not active_projects:
        return ProjectSelectionResult(
            action="request_new",
            requires_clarification=False,
            reply_text="Vous n'avez pas encore de projet. Souhaitez-vous en créer un nouveau ?",
        )

    cleaned = user_message.strip().lower().rstrip("!.,?")

    if is_project_selection_ambiguity(user_message):
        if len(active_projects) == 1:
            return ProjectSelectionResult(
                action="select_existing",
                project_id=active_projects[0]["id"],
                requires_confirmation=True,
                reply_text=f"Je vois que vous travaillez sur le projet « {active_projects[0].get('title', '')} ». Est-ce bien celui-ci ?",
            )
        return ProjectSelectionResult(
            action="ambiguous",
            requires_clarification=True,
            alternatives=_format_projects(active_projects),
            reply_text="Je n'ai pas compris quel projet vous voulez utiliser. Veuillez préciser.",
        )

    if len(active_projects) == 1 and conversation_project_id is None:
        return ProjectSelectionResult(
            action="select_existing",
            project_id=active_projects[0]["id"],
            requires_confirmation=True,
            reply_text=f"Vous avez un projet en cours : « {active_projects[0].get('title', '')} ». Est-ce le bon ?",
        )

    if len(active_projects) == 1:
        sole = active_projects[0]
        if sole["id"] == conversation_project_id:
            return ProjectSelectionResult(
                action="select_existing",
                project_id=sole["id"],
                requires_confirmation=False,
            )

    exact_match = _find_exact_match(cleaned, active_projects)
    if exact_match is not None:
        return ProjectSelectionResult(
            action="select_existing",
            project_id=exact_match["id"],
            requires_confirmation=False,
            reply_text=f"D'accord, je continue avec le projet « {exact_match.get('title', '') } ».",
        )

    partial_matches = _find_partial_matches(cleaned, active_projects)
    if len(partial_matches) == 1:
        return ProjectSelectionResult(
            action="select_existing",
            project_id=partial_matches[0]["id"],
            requires_confirmation=True,
            reply_text=f"Voulez-vous dire le projet « {partial_matches[0].get('title', '') } » ?",
        )

    if len(active_projects) > 1 and conversation_project_id is None:
        return ProjectSelectionResult(
            action="list_projects",
            requires_clarification=True,
            alternatives=_format_projects(active_projects),
            reply_text="Vous avez plusieurs projets. Lequel souhaitez-vous utiliser ?",
        )

    return ProjectSelectionResult(
        action="none",
        requires_clarification=True,
        alternatives=_format_projects(active_projects),
        reply_text="Je n'ai pas trouvé de projet correspondant. Pouvez-vous reformuler ?",
    )


def _find_exact_match(cleaned: str, projects: list[dict[str, Any]]) -> dict[str, Any] | None:
    for p in projects:
        title = str(p.get("title", "")).strip().lower()
        if cleaned == title or cleaned in title:
            return p
    for p in projects:
        pid = str(p.get("id", "")).strip()
        if cleaned == pid:
            return p
    return None


def _find_partial_matches(cleaned: str, projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    words = cleaned.split()
    matches: list[dict[str, Any]] = []
    for p in projects:
        title = str(p.get("title", "")).strip().lower()
        if any(w in title for w in words if len(w) > 2):
            matches.append(p)
    return matches


def _format_projects(projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": p["id"],
            "title": p.get("title", ""),
            "project_type": p.get("project_type", ""),
            "status": p.get("status", ""),
        }
        for p in projects
    ]
