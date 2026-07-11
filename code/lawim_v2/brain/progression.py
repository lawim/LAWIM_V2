from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

QUESTION_TEMPLATES: dict[str, dict[str, Any]] = {
    "buy": {
        "qualification_steps": (
            {"field": "city", "question": "Dans quelle ville souhaitez-vous acheter ?", "key": "buy_city"},
            {"field": "budget_max", "question": "Quel est votre budget maximum ?", "key": "buy_budget"},
            {"field": "property_type", "question": "Quel type de bien recherchez-vous ? (maison, appartement, villa, terrain)", "key": "buy_property_type"},
            {"field": "surface_m2", "question": "Quelle surface recherchez-vous ?", "key": "buy_surface"},
            {"field": "bedrooms", "question": "Combien de chambres souhaitez-vous ?", "key": "buy_bedrooms"},
            {"field": "neighborhood", "question": "Avez-vous une préférence de quartier ?", "key": "buy_neighborhood"},
            {"field": "timeline", "question": "Quand souhaitez-vous finaliser l'achat ?", "key": "buy_timeline"},
        ),
        "next_actions": ("Vérifier le titre foncier", "Rechercher un financement", "Consulter un notaire"),
    },
    "rent": {
        "qualification_steps": (
            {"field": "city", "question": "Dans quelle ville cherchez-vous une location ?", "key": "rent_city"},
            {"field": "budget_max", "question": "Quel loyer maximum pouvez-vous payer ?", "key": "rent_budget"},
            {"field": "property_type", "question": "Quel type de logement cherchez-vous ? (appartement, maison, studio)", "key": "rent_property_type"},
            {"field": "bedrooms", "question": "Combien de pièces souhaitez-vous ?", "key": "rent_bedrooms"},
            {"field": "neighborhood", "question": "Quel quartier préférez-vous ?", "key": "rent_neighborhood"},
            {"field": "duration", "question": "Pour quelle durée de location ?", "key": "rent_duration"},
        ),
        "next_actions": ("Planifier des visites", "Préparer votre dossier locataire"),
    },
    "sell": {
        "qualification_steps": (
            {"field": "city", "question": "Où se situe le bien que vous souhaitez vendre ?", "key": "sell_city"},
            {"field": "property_type", "question": "Quel type de bien vendez-vous ?", "key": "sell_property_type"},
            {"field": "budget_min", "question": "Quel prix de vente souhaitez-vous ?", "key": "sell_price"},
            {"field": "surface_m2", "question": "Quelle est la surface du bien ?", "key": "sell_surface"},
            {"field": "status", "question": "Le bien est-il actuellement occupé ou libre ?", "key": "sell_status"},
        ),
        "next_actions": ("Estimer le bien", "Préparer les documents", "Publier l'annonce"),
    },
    "invest": {
        "qualification_steps": (
            {"field": "city", "question": "Dans quelle ville souhaitez-vous investir ?", "key": "invest_city"},
            {"field": "budget_max", "question": "Quel budget d'investissement ?", "key": "invest_budget"},
            {"field": "property_type", "question": "Quel type d'actif recherchez-vous ? (immeuble, terrain, commerce)", "key": "invest_property_type"},
            {"field": "objective", "question": "Quel est votre objectif de rendement ?", "key": "invest_objective"},
            {"field": "timeline", "question": "Quel est votre horizon d'investissement ?", "key": "invest_timeline"},
        ),
        "next_actions": ("Analyse de marché", "Due diligence", "Simulation de rendement"),
    },
    "build": {
        "qualification_steps": (
            {"field": "city", "question": "Dans quelle ville souhaitez-vous construire ?", "key": "build_city"},
            {"field": "land_status", "question": "Avez-vous déjà un terrain ?", "key": "build_land_status"},
            {"field": "budget_max", "question": "Quel budget pour la construction ?", "key": "build_budget"},
            {"field": "building_type", "question": "Quel type de construction ? (maison, immeuble, clinique, commerce)", "key": "build_type"},
            {"field": "surface_m2", "question": "Quelle surface construite ?", "key": "build_surface"},
        ),
        "next_actions": ("Trouver un architecte", "Obtenir un permis de construire", "Rechercher un terrain"),
    },
    "find_land": {
        "qualification_steps": (
            {"field": "city", "question": "Dans quelle ville recherchez-vous un terrain ?", "key": "land_city"},
            {"field": "budget_max", "question": "Quel budget pour le terrain ?", "key": "land_budget"},
            {"field": "surface_m2", "question": "Quelle superficie recherchez-vous ?", "key": "land_surface"},
            {"field": "purpose", "question": "Quel usage pour ce terrain ? (construction, investissement, agricole)", "key": "land_purpose"},
        ),
        "next_actions": ("Vérifier le titre foncier", "Rechercher un géomètre", "Consulter un notaire"),
    },
    "find_partner": {
        "qualification_steps": (
            {"field": "partner_type", "question": "Quel type de professionnel recherchez-vous ?", "key": "partner_type"},
            {"field": "city", "question": "Dans quelle ville ?", "key": "partner_city"},
            {"field": "specialty", "question": "Avez-vous une spécialité particulière ?", "key": "partner_specialty"},
        ),
        "next_actions": ("Rechercher dans l'annuaire LAWIM", "Voir les recommandations"),
    },
    "find_funding": {
        "qualification_steps": (
            {"field": "amount", "question": "Quel montant de financement recherchez-vous ?", "key": "funding_amount"},
            {"field": "project_type", "question": "Pour quel type de projet ? (achat, construction, investissement)", "key": "funding_project"},
            {"field": "duration", "question": "Sur quelle durée ?", "key": "funding_duration"},
        ),
        "next_actions": ("Simuler un prêt", "Comparer les banques", "Préparer le dossier"),
    },
}

REQUIRED_CONFIRMATION_FIELDS: frozenset[str] = frozenset({
    "budget_max", "budget_min", "city", "property_type", "transaction_type",
    "amount", "partner_type",
})


def _known_fields_from_memory(memory_items: list[dict[str, Any]]) -> set[str]:
    known: set[str] = set()
    for item in memory_items:
        label = str(item.get("label", "")).lower()
        field_key = str(item.get("field_key", "")).lower()
        if label == "ville" or field_key == "city":
            known.add("city")
        elif "budget" in label or "budget" in field_key:
            known.add("budget_max")
            known.add("budget")
        elif "type" in label or label == "type de bien":
            known.add("property_type")
        elif "surface" in label or "superficie" in label or "surface" in field_key:
            known.add("surface_m2")
        elif "chambre" in label or "pièce" in label or "chambre" in field_key:
            known.add("bedrooms")
        elif "quartier" in label or "quartier" in field_key:
            known.add("neighborhood")
        elif "usage" in label or "purpose" in field_key or "usage" in field_key:
            known.add("purpose")
        elif "durée" in label or "duration" in field_key or "duree" in label:
            known.add("duration")
        elif "terrain" in label or "land" in field_key:
            known.add("land_status")
        elif "échéance" in label or "timeline" in field_key:
            known.add("timeline")
    return known


def _known_fields_from_entities(entities: dict[str, Any]) -> set[str]:
    known: set[str] = set()
    if entities.get("cities"):
        known.add("city")
    if entities.get("budgets"):
        known.add("budget_max")
        known.add("budget")
    if entities.get("property_types"):
        known.add("property_type")
    if entities.get("surfaces_m2"):
        known.add("surface_m2")
    if entities.get("bedrooms"):
        known.add("bedrooms")
    return known


def _known_fields_from_project(project: dict[str, Any] | None) -> set[str]:
    if project is None:
        return set()
    known: set[str] = set()
    if project.get("location_city"):
        known.add("city")
    if project.get("budget_min") is not None or project.get("budget_max") is not None:
        known.add("budget_max")
        known.add("budget")
    if project.get("property_type"):
        known.add("property_type")
    return known


def _field_to_label(field: str, lang: str = "fr") -> str:
    labels = {
        "fr": {
            "city": "ville",
            "budget_max": "budget maximum",
            "budget_min": "budget minimum",
            "budget": "budget",
            "property_type": "type de bien",
            "surface_m2": "surface",
            "bedrooms": "nombre de pièces",
            "neighborhood": "quartier",
            "timeline": "échéance",
            "duration": "durée",
            "status": "statut du bien",
            "land_status": "terrain",
            "building_type": "type de construction",
            "purpose": "usage",
            "partner_type": "type de professionnel",
            "specialty": "spécialité",
            "objective": "objectif",
            "amount": "montant",
            "project_type": "type de projet",
            "language": "langue",
            "coord": "coordonnées",
        },
    }
    return labels.get(lang, labels["fr"]).get(field, field)


def _find_question_template(intent: str, field: str) -> str | None:
    template = QUESTION_TEMPLATES.get(intent)
    if template is None:
        return None
    for step in template["qualification_steps"]:
        if step["field"] == field:
            return step["question"]
    return None


def build_progression_state(
    *,
    project_id: int,
    intent: str,
    entities: dict[str, Any],
    memory_items: list[dict[str, Any]],
    project: dict[str, Any] | None = None,
) -> dict[str, Any]:
    template = QUESTION_TEMPLATES.get(intent)
    if template is None:
        intent = "find_property"
        template = QUESTION_TEMPLATES.get("buy")
    if template is None:
        return {"next_question": None, "known_fields": [], "missing_fields": [], "complete": False}

    known = _known_fields_from_memory(memory_items) | _known_fields_from_entities(entities) | _known_fields_from_project(project)
    all_steps = template["qualification_steps"]
    next_question: str | None = None
    next_key: str | None = None
    missing_fields: list[dict[str, Any]] = []
    known_fields: list[dict[str, Any]] = []
    asked_before = {str(m.get("field_key")) for m in memory_items if m.get("kind") in {"temporary", "hypothesis", "confirmed_fact"}}

    for step in all_steps:
        field = step["field"]
        step_key = step["key"]
        if field in known:
            known_fields.append({"field": field, "key": step_key, "label": _field_to_label(field)})
        else:
            was_asked = step_key in asked_before
            missing_fields.append({
                "field": field,
                "key": step_key,
                "question": step["question"],
                "was_asked": was_asked,
            })

    if missing_fields:
        next_step = missing_fields[0]
        next_question = next_step["question"]
        next_key = next_step["key"]

    return {
        "intent": intent,
        "progress_pct": int(len(known_fields) * 100 / max(len(all_steps), 1)) if all_steps else 100,
        "total_steps": len(all_steps),
        "known_fields": [k["field"] for k in known_fields],
        "known_labels": [k["label"] for k in known_fields],
        "missing_fields": [m["field"] for m in missing_fields],
        "missing_keys": [m["key"] for m in missing_fields],
        "next_question": next_question,
        "next_key": next_key,
        "complete": len(missing_fields) == 0,
        "next_actions": list(template.get("next_actions", [])),
    }


class ProgressionEngine:
    def compute(
        self,
        *,
        project_id: int,
        intent: str,
        entities: dict[str, Any],
        memory_items: list[dict[str, Any]],
        project: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return build_progression_state(
            project_id=project_id,
            intent=intent,
            entities=entities,
            memory_items=memory_items,
            project=project,
        )

    def requires_confirmation(self, field: str) -> bool:
        return field in REQUIRED_CONFIRMATION_FIELDS

    def confirmation_question(self, memory_item: dict[str, Any], lang: str = "fr") -> str:
        label = str(memory_item.get("label", "cette information"))
        value = str(memory_item.get("value", ""))
        questions = {
            "fr": f"Je comprends que {label} est {value}. C'est bien cela ?",
            "en": f"I understand that {label} is {value}. Is that correct?",
            "pcm": f"I don make say {label} na {value}. Na so?",
        }
        return questions.get(lang, questions["fr"])
