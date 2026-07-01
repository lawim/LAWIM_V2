from __future__ import annotations

AGENT_KEYS: frozenset[str] = frozenset(
    {
        "project_advisor",
        "decision_coach",
        "ecosystem_navigator",
        "risk_analyst",
        "journey_guide",
        "simulation_planner",
    }
)

PROMPT_KEYS: frozenset[str] = frozenset(
    {
        "system.base",
        "system.project_advisor",
        "system.decision_coach",
        "system.ecosystem_navigator",
        "system.risk_analyst",
        "system.journey_guide",
        "system.simulation_planner",
    }
)

RAG_SOURCE_TYPES: frozenset[str] = frozenset(
    {
        "knowledge_fact",
        "knowledge_node",
        "cognition_decision",
        "project_metadata",
        "ecosystem_match",
        "journey_step",
    }
)

INTENT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "decision_coach": ("décision", "decision", "choisir", "alternative", "confiance"),
    "ecosystem_navigator": ("partenaire", "partner", "service", "matching", "agence", "notaire"),
    "risk_analyst": ("risque", "risk", "danger", "mitigation", "bloquant"),
    "journey_guide": ("parcours", "journey", "étape", "step", "progression", "timeline"),
    "simulation_planner": ("simulation", "scénario", "scenario", "budget", "prêt", "loan"),
}

ASSISTANT_MODES: frozenset[str] = frozenset({"deterministic", "llm"})

DEFAULT_PROMPT_VERSION = "1.0.0"
