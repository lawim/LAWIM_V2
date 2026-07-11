from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

SUGGESTION_RULES: dict[str, list[dict[str, Any]]] = {
    "buy": [
        {"trigger": "budget_known", "suggestion": "Vérifier votre capacité d'emprunt", "partner": "banque", "priority": "high"},
        {"trigger": "city_known", "suggestion": "Consulter les annonces disponibles", "action": "search_properties", "priority": "high"},
        {"trigger": "property_type_known", "suggestion": "Rechercher un notaire spécialisé", "partner": "notaire", "priority": "medium"},
        {"trigger": "progression_complete", "suggestion": "Lancer une recherche de biens", "action": "search_properties", "priority": "high"},
    ],
    "rent": [
        {"trigger": "budget_known", "suggestion": "Consulter les locations disponibles", "action": "search_properties", "priority": "high"},
        {"trigger": "city_known", "suggestion": "Planifier des visites", "action": "plan_visit", "priority": "high"},
        {"trigger": "progression_complete", "suggestion": "Préparer votre dossier locataire", "action": "prepare_documents", "priority": "medium"},
    ],
    "sell": [
        {"trigger": "property_type_known", "suggestion": "Estimer votre bien", "action": "estimate_property", "priority": "high"},
        {"trigger": "city_known", "suggestion": "Préparer les photos et documents", "action": "prepare_documents", "priority": "medium"},
        {"trigger": "progression_complete", "suggestion": "Publier votre annonce", "action": "publish_property", "priority": "high"},
    ],
    "invest": [
        {"trigger": "budget_known", "suggestion": "Analyser les rendements par ville", "action": "market_analysis", "priority": "high"},
        {"trigger": "city_known", "suggestion": "Rechercher des opportunités d'investissement", "action": "search_properties", "priority": "high"},
        {"trigger": "progression_complete", "suggestion": "Simuler un investissement", "action": "run_simulation", "priority": "high"},
    ],
    "build": [
        {"trigger": "city_known", "suggestion": "Rechercher un terrain", "action": "search_land", "priority": "high"},
        {"trigger": "land_status_known", "suggestion": "Consulter un architecte", "partner": "architecte", "priority": "high"},
        {"trigger": "budget_known", "suggestion": "Estimer le coût de construction", "action": "estimate_build", "priority": "high"},
        {"trigger": "progression_complete", "suggestion": "Préparer le dossier de permis de construire", "action": "prepare_documents", "priority": "high"},
    ],
    "find_land": [
        {"trigger": "city_known", "suggestion": "Consulter les terrains disponibles", "action": "search_land", "priority": "high"},
        {"trigger": "budget_known", "suggestion": "Vérifier le titre foncier", "partner": "notaire", "priority": "high"},
        {"trigger": "progression_complete", "suggestion": "Contacter un géomètre", "partner": "géomètre", "priority": "medium"},
    ],
    "find_partner": [
        {"trigger": "partner_type_known", "suggestion": "Consulter l'annuaire LAWIM", "action": "search_partners", "priority": "high"},
    ],
    "find_funding": [
        {"trigger": "amount_known", "suggestion": "Simuler un prêt bancaire", "action": "run_simulation", "priority": "high"},
        {"trigger": "project_type_known", "suggestion": "Comparer les offres de financement", "action": "compare_funding", "priority": "high"},
        {"trigger": "progression_complete", "suggestion": "Préparer votre dossier de financement", "action": "prepare_documents", "priority": "medium"},
    ],
}

PRIORITY_ORDER = {"high": 3, "medium": 2, "low": 1}


def _known_triggers(entities: dict[str, Any], progression: dict[str, Any], memory: dict[str, Any]) -> set[str]:
    triggers: set[str] = set()
    known = set(progression.get("known_fields", []))
    if "city" in known:
        triggers.add("city_known")
    if any(b for b in ["budget_max", "budget_min", "budget"] if b in known):
        triggers.add("budget_known")
    if "property_type" in known:
        triggers.add("property_type_known")
    if "partner_type" in known:
        triggers.add("partner_type_known")
    if "land_status" in known:
        triggers.add("land_status_known")
    if "amount" in known or "budget_max" in known:
        triggers.add("amount_known")
    if "project_type" in known:
        triggers.add("project_type_known")
    if progression.get("complete"):
        triggers.add("progression_complete")
    return triggers


def evaluate_suggestions(
    *,
    intent: str,
    entities: dict[str, Any],
    progression: dict[str, Any],
    memory_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rules = SUGGESTION_RULES.get(intent, [])
    if not rules:
        rules = SUGGESTION_RULES.get("buy", [])

    triggers = _known_triggers(entities, progression, {"items": memory_items})
    suggestions: list[dict[str, Any]] = []
    seen: set[str] = set()

    for rule in rules:
        if rule["trigger"] in triggers:
            key = rule.get("action") or rule.get("partner") or rule["suggestion"]
            if key in seen:
                continue
            seen.add(key)
            suggestions.append({
                "type": rule.get("action") and "action" or "partner",
                "content": rule["suggestion"],
                "action": rule.get("action"),
                "partner": rule.get("partner"),
                "priority": rule["priority"],
                "priority_order": PRIORITY_ORDER.get(rule["priority"], 0),
            })

    suggestions.sort(key=lambda s: s["priority_order"], reverse=True)
    return suggestions[:5]


class AccompanimentEngine:
    def suggest(
        self,
        *,
        intent: str,
        entities: dict[str, Any],
        progression: dict[str, Any],
        memory_items: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        return evaluate_suggestions(
            intent=intent,
            entities=entities,
            progression=progression,
            memory_items=memory_items,
        )

    def persist_suggestions(
        self,
        repository,
        *,
        project_id: int,
        suggestions: list[dict[str, Any]],
        language: str = "fr",
    ) -> list[dict[str, Any]]:
        persisted: list[dict[str, Any]] = []
        for sug in suggestions:
            row = repository.create_brain_suggestion(
                project_id=project_id,
                suggestion_type=sug.get("type", "action"),
                content=sug["content"],
                justification=sug.get("content", ""),
                priority=sug.get("priority", "medium"),
                status="active",
                target_action=sug.get("action"),
                target_partner=sug.get("partner"),
                language=language,
                expires_at=None,
            )
            persisted.append(dict(row))
        return persisted
