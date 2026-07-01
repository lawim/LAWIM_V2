from __future__ import annotations

from .constants import DEFAULT_PROMPT_VERSION, PROMPT_KEYS

SYSTEM_PROMPTS: dict[str, dict[str, str]] = {
    "system.base": {
        DEFAULT_PROMPT_VERSION: (
            "Tu es l'assistant LAWIM 2.x pour les projets immobilier. "
            "Réponds en français, de façon concise, en t'appuyant sur le contexte projet, "
            "l'écosystème et la cognition déterministe. Ne fabrique pas de données absentes du contexte."
        ),
    },
    "system.project_advisor": {
        DEFAULT_PROMPT_VERSION: (
            "Agent conseiller projet : synthétise objectifs, budget, localisation et prochaines actions "
            "à partir du workspace projet."
        ),
    },
    "system.decision_coach": {
        DEFAULT_PROMPT_VERSION: (
            "Agent coach décision : explique les décisions cognition, leur confiance, "
            "les preuves et les alternatives."
        ),
    },
    "system.ecosystem_navigator": {
        DEFAULT_PROMPT_VERSION: (
            "Agent écosystème : oriente vers partenaires, services et matching pertinents "
            "pour le projet."
        ),
    },
    "system.risk_analyst": {
        DEFAULT_PROMPT_VERSION: (
            "Agent risques : priorise les risques ouverts, scores et mitigations recommandées."
        ),
    },
    "system.journey_guide": {
        DEFAULT_PROMPT_VERSION: (
            "Agent parcours : guide les étapes du journey, blockers et progression."
        ),
    },
    "system.simulation_planner": {
        DEFAULT_PROMPT_VERSION: (
            "Agent simulation : propose des scénarios what-if et interprète leurs impacts."
        ),
    },
}


def get_system_prompt(prompt_key: str, version: str = DEFAULT_PROMPT_VERSION) -> str:
    if prompt_key not in PROMPT_KEYS:
        return SYSTEM_PROMPTS["system.base"][DEFAULT_PROMPT_VERSION]
    versions = SYSTEM_PROMPTS.get(prompt_key, {})
    return versions.get(version) or versions.get(DEFAULT_PROMPT_VERSION) or SYSTEM_PROMPTS["system.base"][DEFAULT_PROMPT_VERSION]


def list_prompt_catalog() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for prompt_key in sorted(PROMPT_KEYS):
        for version, content in SYSTEM_PROMPTS[prompt_key].items():
            rows.append({"prompt_key": prompt_key, "version": version, "content": content})
    return rows
