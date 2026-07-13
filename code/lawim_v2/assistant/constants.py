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

DEFAULT_PROMPT_VERSION = "1.0.0"
