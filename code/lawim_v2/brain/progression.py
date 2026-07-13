from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

QUESTION_TEMPLATES: dict[str, dict[str, Any]] = {
    "buy": {
        "qualification_steps": (
            {"field": "city", "question": "Dans quelle ville souhaitez-vous acheter ?", "key": "buy_city", "required": True},
            {"field": "budget_max", "question": "Quel est votre budget maximum ?", "key": "buy_budget", "required": True},
            {"field": "property_type", "question": "Quel type de bien recherchez-vous ? (maison, appartement, villa, terrain)", "key": "buy_property_type", "required": True},
            {"field": "surface_m2", "question": "Quelle surface recherchez-vous ?", "key": "buy_surface", "required": False},
            {"field": "bedrooms", "question": "Combien de chambres souhaitez-vous ?", "key": "buy_bedrooms", "required": False},
            {"field": "neighborhood", "question": "Avez-vous une préférence de quartier ?", "key": "buy_neighborhood", "required": False},
            {"field": "timeline", "question": "Quand souhaitez-vous finaliser l'achat ?", "key": "buy_timeline", "required": False},
        ),
        "next_actions": ("Lancer la recherche LAWIM", "Vérifier le titre foncier", "Préparer la visite"),
    },
    "rent": {
        "qualification_steps": (
            {"field": "city", "question": "Dans quelle ville cherchez-vous une location ?", "key": "rent_city", "required": True},
            {"field": "budget_max", "question": "Quel loyer maximum pouvez-vous payer ?", "key": "rent_budget", "required": True},
            {"field": "property_type", "question": "Quel type de logement cherchez-vous ? (appartement, maison, studio)", "key": "rent_property_type", "required": True},
            {"field": "bedrooms", "question": "Combien de pièces souhaitez-vous ?", "key": "rent_bedrooms", "required": False},
            {"field": "neighborhood", "question": "Quel quartier préférez-vous ?", "key": "rent_neighborhood", "required": False},
            {"field": "duration", "question": "Pour quelle durée de location ?", "key": "rent_duration", "required": False},
        ),
        "next_actions": ("Lancer la recherche LAWIM", "Planifier des visites", "Préparer votre dossier locataire"),
    },
    "sell": {
        "qualification_steps": (
            {"field": "city", "question": "Où se situe le bien que vous souhaitez vendre ?", "key": "sell_city", "required": True},
            {"field": "property_type", "question": "Quel type de bien vendez-vous ?", "key": "sell_property_type", "required": True},
            {"field": "budget_min", "question": "Quel prix de vente souhaitez-vous ?", "key": "sell_price", "required": True},
            {"field": "surface_m2", "question": "Quelle est la surface du bien ?", "key": "sell_surface", "required": False},
            {"field": "status", "question": "Le bien est-il actuellement occupé ou libre ?", "key": "sell_status", "required": False},
        ),
        "next_actions": ("Préparer la mise en vente", "Estimer le bien", "Préparer les documents"),
    },
    "invest": {
        "qualification_steps": (
            {"field": "city", "question": "Dans quelle ville souhaitez-vous investir ?", "key": "invest_city", "required": True},
            {"field": "budget_max", "question": "Quel budget d'investissement ?", "key": "invest_budget", "required": True},
            {"field": "property_type", "question": "Quel type d'actif recherchez-vous ? (immeuble, terrain, commerce)", "key": "invest_property_type", "required": True},
            {"field": "objective", "question": "Quel est votre objectif de rendement ?", "key": "invest_objective", "required": False},
            {"field": "timeline", "question": "Quel est votre horizon d'investissement ?", "key": "invest_timeline", "required": False},
        ),
        "next_actions": ("Lancer l'analyse de marché", "Due diligence", "Simulation de rendement"),
    },
    "build": {
        "qualification_steps": (
            {"field": "city", "question": "Dans quelle ville souhaitez-vous construire ?", "key": "build_city", "required": True},
            {"field": "land_status", "question": "Avez-vous déjà un terrain ?", "key": "build_land_status", "required": True},
            {"field": "budget_max", "question": "Quel budget pour la construction ?", "key": "build_budget", "required": True},
            {"field": "building_type", "question": "Quel type de construction ? (maison, immeuble, clinique, commerce)", "key": "build_type", "required": False},
            {"field": "surface_m2", "question": "Quelle surface construite ?", "key": "build_surface", "required": False},
        ),
        "next_actions": ("Rechercher un terrain", "Trouver un architecte", "Obtenir un permis de construire"),
    },
    "find_land": {
        "qualification_steps": (
            {"field": "city", "question": "Dans quelle ville recherchez-vous un terrain ?", "key": "land_city", "required": True},
            {"field": "budget_max", "question": "Quel budget pour le terrain ?", "key": "land_budget", "required": True},
            {"field": "surface_m2", "question": "Quelle superficie recherchez-vous ?", "key": "land_surface", "required": True},
            {"field": "purpose", "question": "Quel usage pour ce terrain ? (construction, investissement, agricole)", "key": "land_purpose", "required": False},
        ),
        "next_actions": ("Lancer la recherche LAWIM", "Vérifier le titre foncier", "Consulter un notaire"),
    },
    "find_partner": {
        "qualification_steps": (
            {"field": "partner_type", "question": "Quel type de professionnel recherchez-vous ?", "key": "partner_type", "required": True},
            {"field": "city", "question": "Dans quelle ville ?", "key": "partner_city", "required": True},
            {"field": "specialty", "question": "Avez-vous une spécialité particulière ?", "key": "partner_specialty", "required": False},
        ),
        "next_actions": ("Rechercher dans l'annuaire LAWIM", "Voir les recommandations"),
    },
    "find_funding": {
        "qualification_steps": (
            {"field": "amount", "question": "Quel montant de financement recherchez-vous ?", "key": "funding_amount", "required": True},
            {"field": "project_type", "question": "Pour quel type de projet ? (achat, construction, investissement)", "key": "funding_project", "required": True},
            {"field": "duration", "question": "Sur quelle durée ?", "key": "funding_duration", "required": False},
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
        elif "budget" in label or "budget" in field_key or "prix" in label or "montant" in label or "amount" in field_key:
            known.add("budget_max")
            known.add("budget_min")
            known.add("budget")
            known.add("amount")
        elif "project_type" in field_key or "type de projet" in label:
            known.add("project_type")
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
        elif "timeline" in field_key or "échéance" in label or "deadline" in field_key or "date" in label or "date" in field_key:
            known.add("timeline")
        elif "terrain" in label or "land" in field_key:
            known.add("land_status")
        elif "urgence" in label or "urgency" in field_key:
            known.add("urgency")
    return known


def _known_fields_from_entities(entities: dict[str, Any]) -> set[str]:
    known: set[str] = set()
    if entities.get("cities"):
        known.add("city")
    if entities.get("budgets"):
        known.add("budget_max")
        known.add("budget_min")
        known.add("budget")
        known.add("amount")
    if entities.get("property_types"):
        known.add("property_type")
    if entities.get("project_type") or entities.get("project_types"):
        known.add("project_type")
    if entities.get("surfaces_m2"):
        known.add("surface_m2")
    if entities.get("bedrooms"):
        known.add("bedrooms")
    if entities.get("timelines"):
        known.add("timeline")
    if entities.get("urgency"):
        known.add("timeline")
    if entities.get("land_status"):
        known.add("land_status")
    return known


def _known_fields_from_project(project: dict[str, Any] | None) -> set[str]:
    if project is None:
        return set()
    known: set[str] = set()
    if project.get("location_city"):
        known.add("city")
    if project.get("budget_min") is not None or project.get("budget_max") is not None:
        known.add("budget_max")
        known.add("budget_min")
        known.add("budget")
        known.add("amount")
    if project.get("property_type"):
        known.add("property_type")
    if project.get("timeline_horizon"):
        known.add("timeline")
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
            "urgency": "urgence",
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


def _template_fields(template: dict[str, Any], *, required: bool) -> list[str]:
    fields: list[str] = []
    for step in template.get("qualification_steps", ()):
        is_required = bool(step.get("required", True))
        if is_required == required:
            fields.append(str(step.get("field")))
    return fields


def _completion_percent(known_count: int, total_count: int) -> int:
    if total_count <= 0:
        return 100
    return int(round(known_count * 100 / total_count))


def _commercial_maturity(*, minimum_search_ready: bool, complete: bool, progress_pct: int, qualification_score: int) -> str:
    if complete:
        return "IMMEDIATE"
    if minimum_search_ready:
        return "ACTIVE"
    if qualification_score >= 35 or progress_pct >= 35:
        return "EXPLORATION"
    return "INFORMATION"


def build_progression_state(
    *,
    project_id: int,
    intent: str,
    entities: dict[str, Any],
    memory_items: list[dict[str, Any]],
    project: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_intent = str(intent or "").strip()
    project_intent = str(project.get("project_type") or "").strip() if project else ""
    if resolved_intent not in QUESTION_TEMPLATES:
        if project_intent in QUESTION_TEMPLATES:
            resolved_intent = project_intent
        elif resolved_intent == "find_property" and project_intent in QUESTION_TEMPLATES:
            resolved_intent = project_intent
        else:
            resolved_intent = "find_property"
    template = QUESTION_TEMPLATES.get(resolved_intent)
    if template is None:
        resolved_intent = "find_property"
        template = QUESTION_TEMPLATES.get("buy")
    if template is None:
        return {
            "next_question": None,
            "known_fields": [],
            "missing_fields": [],
            "complete": False,
            "minimum_search_ready": False,
            "commercial_maturity": "INFORMATION",
            "qualification_score": 0,
        }

    known = _known_fields_from_memory(memory_items) | _known_fields_from_entities(entities) | _known_fields_from_project(project)
    all_steps = template["qualification_steps"]
    required_fields = _template_fields(template, required=True)
    optional_fields = _template_fields(template, required=False)
    template_actions = list(template.get("next_actions", []))
    next_question: str | None = None
    next_key: str | None = None
    missing_fields: list[dict[str, Any]] = []
    known_fields: list[dict[str, Any]] = []
    missing_required_fields: list[dict[str, Any]] = []
    missing_optional_fields: list[dict[str, Any]] = []
    known_required_fields: list[dict[str, Any]] = []
    known_optional_fields: list[dict[str, Any]] = []
    asked_before = {str(m.get("field_key")) for m in memory_items if m.get("kind") in {"temporary", "hypothesis", "confirmed_fact"}}

    for step in all_steps:
        field = step["field"]
        step_key = step["key"]
        is_required = bool(step.get("required", True))
        if field in known:
            item = {"field": field, "key": step_key, "label": _field_to_label(field)}
            known_fields.append(item)
            if is_required:
                known_required_fields.append(item)
            else:
                known_optional_fields.append(item)
        else:
            was_asked = step_key in asked_before
            item = {
                "field": field,
                "key": step_key,
                "question": step["question"],
                "was_asked": was_asked,
                "required": is_required,
            }
            missing_fields.append(item)
            if is_required:
                missing_required_fields.append(item)
            else:
                missing_optional_fields.append(item)

    minimum_search_ready = len(missing_required_fields) == 0
    complete = len(missing_fields) == 0
    if missing_required_fields:
        next_step = missing_required_fields[0]
    elif missing_optional_fields:
        next_step = missing_optional_fields[0]
    elif missing_fields:
        next_step = missing_fields[0]
    else:
        next_step = None
    if next_step is not None:
        next_question = next_step["question"]
        next_key = next_step["key"]

    progress_pct = _completion_percent(len(known_fields), len(all_steps))
    required_completion_pct = _completion_percent(len(known_required_fields), len(required_fields))
    optional_completion_pct = _completion_percent(len(known_optional_fields), len(optional_fields))
    if optional_fields:
        qualification_score = int(round(required_completion_pct * 0.7 + optional_completion_pct * 0.3))
    else:
        qualification_score = required_completion_pct
    commercial_maturity = _commercial_maturity(
        minimum_search_ready=minimum_search_ready,
        complete=complete,
        progress_pct=progress_pct,
        qualification_score=qualification_score,
    )
    if minimum_search_ready:
        next_question = None
        next_key = None
    next_action = "Compléter la qualification"
    if minimum_search_ready:
        next_action = str(template_actions[0] if template_actions else "Lancer la recherche LAWIM")
    if complete and template_actions:
        next_action = str(template_actions[0])

    return {
        "intent": resolved_intent,
        "progress_pct": progress_pct,
        "total_steps": len(all_steps),
        "required_fields": required_fields,
        "optional_fields": optional_fields,
        "known_required_fields": [k["field"] for k in known_required_fields],
        "known_optional_fields": [k["field"] for k in known_optional_fields],
        "known_fields": [k["field"] for k in known_fields],
        "known_labels": [k["label"] for k in known_fields],
        "missing_fields": [m["field"] for m in missing_fields],
        "missing_required_fields": [m["field"] for m in missing_required_fields],
        "missing_optional_fields": [m["field"] for m in missing_optional_fields],
        "missing_keys": [m["key"] for m in missing_fields],
        "next_question": next_question,
        "next_key": next_key,
        "complete": complete,
        "minimum_search_ready": minimum_search_ready,
        "search_ready": minimum_search_ready,
        "commercial_maturity": commercial_maturity,
        "qualification_score": qualification_score,
        "required_completion_pct": required_completion_pct,
        "optional_completion_pct": optional_completion_pct,
        "next_action": next_action,
        "responsible_actor": "LAWIM_AI" if not complete else "LAWIM_AI",
        "transaction_stage": "qualification" if not minimum_search_ready else ("search_ready" if not complete else "complete"),
        "next_actions": template_actions,
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
