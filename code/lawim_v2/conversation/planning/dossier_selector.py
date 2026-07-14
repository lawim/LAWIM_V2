from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..understanding.short_replies import is_project_selection_ambiguity


@dataclass
class DossierSelectionResult:
    action: str  # "select_existing", "request_new", "list_dossiers", "ambiguous", "none"
    dossier_id: int | None = None
    requires_confirmation: bool = False
    requires_clarification: bool = False
    requires_human: bool = False
    alternatives: list[dict[str, Any]] = field(default_factory=list)
    reply_text: str | None = None


def resolve_dossier_selection(
    user_message: str,
    active_dossiers: list[dict[str, Any]],
    *,
    user_id: int | None = None,
    conversation_dossier_id: int | None = None,
    project_id: int | None = None,
) -> DossierSelectionResult:
    if not active_dossiers:
        return DossierSelectionResult(
            action="request_new",
            reply_text="Aucun dossier trouvé pour ce projet. Souhaitez-vous en créer un ?",
        )

    cleaned = user_message.strip().lower().rstrip("!.,?")

    if is_project_selection_ambiguity(user_message):
        if len(active_dossiers) == 1:
            return DossierSelectionResult(
                action="select_existing",
                dossier_id=active_dossiers[0]["id"],
                requires_confirmation=True,
                reply_text=f"Voulez-vous utiliser le dossier « {active_dossiers[0].get('title', '') } » ?",
            )
        return DossierSelectionResult(
            action="ambiguous",
            requires_clarification=True,
            alternatives=_format_dossiers(active_dossiers),
            reply_text="Je n'ai pas compris quel dossier. Veuillez préciser.",
        )

    if len(active_dossiers) == 1 and conversation_dossier_id is None:
        return DossierSelectionResult(
            action="select_existing",
            dossier_id=active_dossiers[0]["id"],
            requires_confirmation=True,
            reply_text=f"Souhaitez-vous travailler sur le dossier « {active_dossiers[0].get('title', '') } » ?",
        )

    if len(active_dossiers) == 1:
        sole = active_dossiers[0]
        if sole["id"] == conversation_dossier_id:
            return DossierSelectionResult(
                action="select_existing",
                dossier_id=sole["id"],
                requires_confirmation=False,
            )

    exact_match = _find_exact_match(cleaned, active_dossiers)
    if exact_match is not None:
        return DossierSelectionResult(
            action="select_existing",
            dossier_id=exact_match["id"],
            requires_confirmation=False,
            reply_text=f"Très bien, je continue avec « {exact_match.get('title', '') } ».",
        )

    partial_matches = _find_partial_matches(cleaned, active_dossiers)
    if len(partial_matches) == 1:
        return DossierSelectionResult(
            action="select_existing",
            dossier_id=partial_matches[0]["id"],
            requires_confirmation=True,
            reply_text=f"Voulez-vous dire « {partial_matches[0].get('title', '') } » ?",
        )

    if len(active_dossiers) > 1 and conversation_dossier_id is None:
        return DossierSelectionResult(
            action="list_dossiers",
            requires_clarification=True,
            alternatives=_format_dossiers(active_dossiers),
            reply_text="Vous avez plusieurs dossiers. Lequel souhaitez-vous utiliser ?",
        )

    return DossierSelectionResult(
        action="none",
        requires_clarification=True,
        alternatives=_format_dossiers(active_dossiers),
        reply_text="Je n'ai pas trouvé de dossier correspondant. Pouvez-vous reformuler ?",
    )


def _find_exact_match(cleaned: str, dossiers: list[dict[str, Any]]) -> dict[str, Any] | None:
    for d in dossiers:
        title = str(d.get("title", "")).strip().lower()
        if cleaned == title or cleaned in title:
            return d
    for d in dossiers:
        did = str(d.get("id", "")).strip()
        if cleaned == did:
            return d
    return None


def _find_partial_matches(cleaned: str, dossiers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    words = cleaned.split()
    matches: list[dict[str, Any]] = []
    for d in dossiers:
        title = str(d.get("title", "")).strip().lower()
        if any(w in title for w in words if len(w) > 2):
            matches.append(d)
    return matches


def _format_dossiers(dossiers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": d["id"],
            "title": d.get("title", ""),
            "status": d.get("status", ""),
        }
        for d in dossiers
    ]
