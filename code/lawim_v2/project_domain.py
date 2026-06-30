from __future__ import annotations

import json
from typing import Any

from .errors import ValidationError

PROJECT_TYPES = frozenset({"buy", "rent", "sell", "invest", "build", "other"})
PROJECT_STATUSES = frozenset({"draft", "active", "paused", "completed", "archived"})
PROJECT_PRIORITIES = frozenset({"low", "normal", "high"})
TIMELINE_HORIZONS = frozenset({"1_month", "3_months", "6_months", "1_year", "2_years", "flexible"})
STEP_STATUSES = frozenset({"pending", "in_progress", "completed", "skipped", "blocked"})
SUPPORTED_CURRENCIES = frozenset({"XAF", "EUR", "USD", "GBP", "XOF"})

STATUS_TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"draft", "active", "archived"}),
    "active": frozenset({"active", "paused", "completed", "archived"}),
    "paused": frozenset({"paused", "active", "archived"}),
    "completed": frozenset({"completed", "archived"}),
    "archived": frozenset({"archived"}),
}

STEP_STATUS_TRANSITIONS: dict[str, frozenset[str]] = {
    "pending": frozenset({"pending", "in_progress", "completed", "skipped", "blocked"}),
    "in_progress": frozenset({"in_progress", "completed", "blocked", "skipped"}),
    "blocked": frozenset({"blocked", "in_progress", "skipped"}),
    "completed": frozenset({"completed"}),
    "skipped": frozenset({"skipped"}),
}

JOURNEY_STEP_TEMPLATES: dict[str, tuple[dict[str, str], ...]] = {
    "buy": (
        {"step_key": "qualification", "title": "Qualification du besoin", "description": "Préciser budget, zone et critères.", "milestone": "Besoin clarifié", "next_action": "Compléter votre profil de recherche"},
        {"step_key": "search", "title": "Recherche de biens", "description": "Explorer et comparer les annonces pertinentes.", "milestone": "Shortlist constituée", "next_action": "Lancer une recherche ciblée"},
        {"step_key": "visit", "title": "Visites", "description": "Organiser et réaliser les visites.", "milestone": "Visite effectuée", "next_action": "Planifier une visite"},
        {"step_key": "negotiation", "title": "Négociation", "description": "Échanger et négocier les conditions.", "milestone": "Offre formulée", "next_action": "Ouvrir une conversation"},
        {"step_key": "closing", "title": "Clôture", "description": "Finaliser l'acquisition.", "milestone": "Projet abouti", "next_action": "Préparer les documents"},
    ),
    "rent": (
        {"step_key": "qualification", "title": "Qualification du besoin", "description": "Définir loyer, durée et quartier.", "milestone": "Besoin clarifié", "next_action": "Indiquer votre budget locatif"},
        {"step_key": "search", "title": "Recherche de logement", "description": "Identifier les locations disponibles.", "milestone": "Options identifiées", "next_action": "Filtrer par ville"},
        {"step_key": "visit", "title": "Visites", "description": "Visiter les logements retenus.", "milestone": "Visite effectuée", "next_action": "Demander une visite"},
        {"step_key": "negotiation", "title": "Négociation", "description": "Discuter loyer et conditions.", "milestone": "Accord de principe", "next_action": "Négocier les termes"},
        {"step_key": "closing", "title": "Signature", "description": "Signer le bail et emménager.", "milestone": "Location conclue", "next_action": "Préparer le dossier locataire"},
    ),
    "sell": (
        {"step_key": "qualification", "title": "Qualification du bien", "description": "Décrire le bien et fixer un prix indicatif.", "milestone": "Bien décrit", "next_action": "Compléter la fiche bien"},
        {"step_key": "preparation", "title": "Préparation", "description": "Photos, documents et mise en valeur.", "milestone": "Annonce prête", "next_action": "Publier l'annonce"},
        {"step_key": "promotion", "title": "Diffusion", "description": "Mettre en visibilité le bien.", "milestone": "Annonce publiée", "next_action": "Publier sur LAWIM"},
        {"step_key": "negotiation", "title": "Négociation", "description": "Gérer les demandes et offres.", "milestone": "Offre reçue", "next_action": "Répondre aux prospects"},
        {"step_key": "closing", "title": "Vente", "description": "Finaliser la transaction.", "milestone": "Vente conclue", "next_action": "Clôturer le dossier"},
    ),
    "invest": (
        {"step_key": "qualification", "title": "Stratégie d'investissement", "description": "Objectif rendement, horizon et budget.", "milestone": "Stratégie définie", "next_action": "Préciser votre objectif"},
        {"step_key": "analysis", "title": "Analyse marché", "description": "Étudier zones et rendements.", "milestone": "Zone ciblée", "next_action": "Comparer les quartiers"},
        {"step_key": "search", "title": "Sélection d'actifs", "description": "Identifier les opportunités.", "milestone": "Actif sélectionné", "next_action": "Rechercher des biens"},
        {"step_key": "due_diligence", "title": "Due diligence", "description": "Vérifier titres et risques.", "milestone": "Vérifications OK", "next_action": "Valider les documents"},
        {"step_key": "closing", "title": "Acquisition", "description": "Conclure l'investissement.", "milestone": "Investissement réalisé", "next_action": "Finaliser l'achat"},
    ),
    "build": (
        {"step_key": "qualification", "title": "Définition du projet", "description": "Terrain, budget et plans.", "milestone": "Projet défini", "next_action": "Décrire votre projet"},
        {"step_key": "land", "title": "Recherche terrain", "description": "Identifier parcelle et localisation.", "milestone": "Terrain identifié", "next_action": "Rechercher un terrain"},
        {"step_key": "design", "title": "Conception", "description": "Plans et permis.", "milestone": "Plans validés", "next_action": "Consulter un professionnel"},
        {"step_key": "construction", "title": "Construction", "description": "Suivi des travaux.", "milestone": "Travaux lancés", "next_action": "Planifier le chantier"},
        {"step_key": "closing", "title": "Livraison", "description": "Réception des ouvrages.", "milestone": "Projet livré", "next_action": "Organiser la réception"},
    ),
    "other": (
        {"step_key": "qualification", "title": "Qualification", "description": "Comprendre votre besoin immobilier.", "milestone": "Besoin identifié", "next_action": "Décrire votre objectif"},
        {"step_key": "planning", "title": "Planification", "description": "Structurer les étapes.", "milestone": "Plan établi", "next_action": "Définir les prochaines actions"},
        {"step_key": "execution", "title": "Exécution", "description": "Avancer sur le projet.", "milestone": "Actions en cours", "next_action": "Passer à l'étape suivante"},
        {"step_key": "review", "title": "Revue", "description": "Évaluer l'avancement.", "milestone": "Point d'étape", "next_action": "Mettre à jour la progression"},
        {"step_key": "closing", "title": "Clôture", "description": "Terminer le projet.", "milestone": "Projet terminé", "next_action": "Archiver le projet"},
    ),
}

DEFAULT_CHECKLIST_BY_STEP: dict[str, tuple[str, ...]] = {
    "qualification": ("Budget défini", "Zone géographique choisie", "Critères principaux listés"),
    "search": ("Annonces consultées", "Shortlist établie", "Comparatif réalisé"),
    "visit": ("Visite planifiée", "Visite effectuée", "Retour de visite consigné"),
    "negotiation": ("Contact établi", "Offre ou demande formulée", "Accord de principe"),
    "closing": ("Documents préparés", "Signature ou clôture confirmée"),
}


def normalize_project_type(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in PROJECT_TYPES:
        raise ValidationError(f"unsupported project_type: {normalized}")
    return normalized


def normalize_status(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in PROJECT_STATUSES:
        raise ValidationError(f"unsupported project status: {normalized}")
    return normalized


def normalize_priority(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in PROJECT_PRIORITIES:
        raise ValidationError(f"unsupported priority: {normalized}")
    return normalized


def normalize_timeline_horizon(value: str | None) -> str | None:
    if value is None or not str(value).strip():
        return None
    normalized = str(value).strip().lower()
    if normalized not in TIMELINE_HORIZONS:
        raise ValidationError(f"unsupported timeline_horizon: {normalized}")
    return normalized


def normalize_currency(currency: str) -> str:
    normalized = currency.strip().upper()
    if normalized not in SUPPORTED_CURRENCIES:
        raise ValidationError(f"unsupported currency: {normalized}")
    return normalized


def normalize_step_status(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in STEP_STATUSES:
        raise ValidationError(f"unsupported step status: {normalized}")
    return normalized


def validate_status_transition(current: str, nxt: str) -> None:
    current_norm = current.lower()
    next_norm = nxt.lower()
    allowed = STATUS_TRANSITIONS.get(current_norm, frozenset({next_norm}))
    if next_norm not in allowed:
        raise ValidationError(f"invalid project status transition: {current_norm} -> {next_norm}")


def validate_step_status_transition(current: str, nxt: str) -> None:
    current_norm = current.lower()
    next_norm = nxt.lower()
    allowed = STEP_STATUS_TRANSITIONS.get(current_norm, frozenset({next_norm}))
    if next_norm not in allowed:
        raise ValidationError(f"invalid step status transition: {current_norm} -> {next_norm}")


def validate_budget_range(budget_min: int | None, budget_max: int | None) -> None:
    if budget_min is not None and budget_min < 0:
        raise ValidationError("budget_min must be non-negative")
    if budget_max is not None and budget_max < 0:
        raise ValidationError("budget_max must be non-negative")
    if budget_min is not None and budget_max is not None and budget_min > budget_max:
        raise ValidationError("budget_min cannot exceed budget_max")


def normalize_metadata(metadata: dict[str, Any] | str | None) -> str:
    if metadata is None:
        return "{}"
    if isinstance(metadata, str):
        try:
            parsed = json.loads(metadata)
        except json.JSONDecodeError as exc:
            raise ValidationError("metadata must be valid JSON") from exc
        if not isinstance(parsed, dict):
            raise ValidationError("metadata must be a JSON object")
        return json.dumps(parsed, ensure_ascii=False, sort_keys=True)
    if not isinstance(metadata, dict):
        raise ValidationError("metadata must be a JSON object")
    return json.dumps(metadata, ensure_ascii=False, sort_keys=True)


def metadata_dict(metadata_json: str | None) -> dict[str, object]:
    if not metadata_json:
        return {}
    try:
        parsed = json.loads(metadata_json)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def journey_templates(project_type: str) -> tuple[dict[str, str], ...]:
    return JOURNEY_STEP_TEMPLATES.get(project_type, JOURNEY_STEP_TEMPLATES["other"])


def compute_progress(steps: list[dict[str, object]]) -> int:
    if not steps:
        return 0
    completed = sum(1 for step in steps if str(step.get("status")) in {"completed", "skipped"})
    return min(100, int(round(completed * 100 / len(steps))))


def derive_next_actions(steps: list[dict[str, object]], *, project_status: str) -> list[dict[str, object]]:
    if project_status == "archived":
        return []
    actions: list[dict[str, object]] = []
    for step in sorted(steps, key=lambda row: int(row.get("position", 0))):
        status = str(step.get("status", "pending"))
        if status in {"pending", "in_progress", "blocked"}:
            actions.append(
                {
                    "step_id": step.get("id"),
                    "step_key": step.get("step_key"),
                    "title": step.get("title"),
                    "status": status,
                    "next_action": step.get("next_action"),
                }
            )
            if len(actions) >= 3:
                break
    return actions


def build_project_input(
    *,
    title: str,
    project_type: str,
    objective: str,
    user_id: int,
    organization_id: int | None = None,
    budget_min: int | None = None,
    budget_max: int | None = None,
    currency: str = "XAF",
    location_city: str | None = None,
    location_region: str | None = None,
    location_country: str = "Cameroon",
    location_latitude: float | None = None,
    location_longitude: float | None = None,
    timeline_horizon: str | None = None,
    status: str = "draft",
    priority: str = "normal",
    metadata: dict[str, Any] | str | None = None,
) -> dict[str, object]:
    title = title.strip()
    objective = objective.strip()
    if not title:
        raise ValidationError("title is required")
    if not objective:
        raise ValidationError("objective is required")
    if user_id < 1:
        raise ValidationError("user_id is required")
    validate_budget_range(budget_min, budget_max)
    return {
        "title": title,
        "project_type": normalize_project_type(project_type),
        "objective": objective,
        "user_id": user_id,
        "organization_id": organization_id,
        "budget_min": budget_min,
        "budget_max": budget_max,
        "currency": normalize_currency(currency),
        "location_city": location_city.strip() if location_city else None,
        "location_region": location_region.strip() if location_region else None,
        "location_country": location_country.strip() if location_country else "Cameroon",
        "location_latitude": location_latitude,
        "location_longitude": location_longitude,
        "timeline_horizon": normalize_timeline_horizon(timeline_horizon),
        "status": normalize_status(status),
        "priority": normalize_priority(priority),
        "metadata_json": normalize_metadata(metadata),
    }
