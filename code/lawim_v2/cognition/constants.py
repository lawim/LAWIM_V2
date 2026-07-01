from __future__ import annotations

NODE_TYPES: frozenset[str] = frozenset(
    {
        "project",
        "goal",
        "need",
        "constraint",
        "life_event",
        "decision",
        "partner",
        "service",
        "recommendation",
        "task",
        "action",
        "workflow",
        "resource",
        "document",
        "timeline",
        "milestone",
        "risk",
        "opportunity",
        "knowledge_fact",
        "context",
    }
)

EDGE_TYPES: frozenset[str] = frozenset(
    {
        "has_goal",
        "has_need",
        "has_constraint",
        "triggered_by",
        "informs",
        "requires",
        "recommends",
        "blocks",
        "enables",
        "depends_on",
        "assigned_to",
        "linked_to",
        "mitigates",
        "exploits",
    }
)

RELATION_TYPES: frozenset[str] = frozenset(
    {
        "influence",
        "dependency",
        "conflict",
        "support",
        "sequence",
        "correlation",
    }
)

SIMULATION_SCENARIOS: dict[str, dict[str, object]] = {
    "budget_increase": {
        "title": "Augmentation budget",
        "description": "Simule une hausse du budget projet.",
        "parameter": "budget_delta_percent",
        "default_value": 15,
    },
    "budget_decrease": {
        "title": "Réduction budget",
        "description": "Simule une baisse du budget projet.",
        "parameter": "budget_delta_percent",
        "default_value": -10,
    },
    "new_loan": {
        "title": "Nouveau prêt",
        "description": "Simule l'ajout d'un financement bancaire.",
        "parameter": "loan_amount",
        "default_value": 5000000,
    },
    "prior_sale": {
        "title": "Vente préalable",
        "description": "Simule la vente d'un bien existant avant achat.",
        "parameter": "sale_proceeds",
        "default_value": 3000000,
    },
    "relocation": {
        "title": "Mutation professionnelle",
        "description": "Simule un changement de zone géographique.",
        "parameter": "new_city",
        "default_value": "Douala",
    },
    "birth": {
        "title": "Naissance",
        "description": "Simule l'impact d'une naissance sur le projet.",
        "parameter": "space_need_increase",
        "default_value": 1,
    },
    "construction_delay": {
        "title": "Retard chantier",
        "description": "Simule un retard de construction.",
        "parameter": "delay_days",
        "default_value": 30,
    },
    "interest_rate_change": {
        "title": "Variation taux d'intérêt",
        "description": "Simule une variation du taux de crédit.",
        "parameter": "rate_delta_percent",
        "default_value": 2,
    },
    "new_partner": {
        "title": "Nouveau partenaire",
        "description": "Simule l'engagement d'un partenaire supplémentaire.",
        "parameter": "partner_type",
        "default_value": "real_estate_agency",
    },
}

REASONING_RULES: tuple[dict[str, str], ...] = (
    {"key": "budget_incomplete", "condition": "missing_budget", "conclusion": "Qualifier le budget avant d'avancer"},
    {"key": "high_risk_open", "condition": "high_risk", "conclusion": "Traiter les risques élevés en priorité"},
    {"key": "blocked_journey", "condition": "journey_blocked", "conclusion": "Débloquer le parcours avant nouvelles actions"},
    {"key": "open_opportunity", "condition": "open_opportunity", "conclusion": "Évaluer l'opportunité ouverte"},
    {"key": "workflow_pending", "condition": "workflow_step_pending", "conclusion": "Exécuter l'étape workflow courante"},
    {"key": "partner_gap", "condition": "missing_partner_match", "conclusion": "Mobiliser un partenaire adapté"},
)

SEVERITY_WEIGHTS: dict[str, int] = {"low": 10, "medium": 25, "high": 50, "critical": 75}
LIKELIHOOD_WEIGHTS: dict[str, int] = {"low": 5, "medium": 15, "high": 30, "certain": 45}
