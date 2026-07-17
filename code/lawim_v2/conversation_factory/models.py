from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

PERSONAS: dict[str, dict[str, Any]] = {
    "prospect_rent_fr": {
        "role": "prospect", "language": "fr", "location": "Douala", "financial_profile": "mid",
        "knowledge_level": "beginner", "digital_literacy": "medium", "communication_style": "polite",
        "urgency": "normal", "trust_level": "medium", "objectives": ["find_apartment"],
    },
    "prospect_buy_en": {
        "role": "prospect", "language": "en", "location": "Yaounde", "financial_profile": "high",
        "knowledge_level": "intermediate", "digital_literacy": "high", "communication_style": "direct",
        "urgency": "high", "trust_level": "low", "objectives": ["buy_house"],
    },
    "owner_pcm": {
        "role": "owner", "language": "pcm", "location": "Buea", "financial_profile": "mid",
        "knowledge_level": "beginner", "digital_literacy": "low", "communication_style": "casual",
        "urgency": "normal", "trust_level": "medium", "objectives": ["list_property"],
    },
    "investor_fr": {
        "role": "buyer", "language": "fr", "location": "Kribi", "financial_profile": "premium",
        "knowledge_level": "expert", "digital_literacy": "high", "communication_style": "formal",
        "urgency": "low", "trust_level": "low", "objectives": ["find_investment"],
    },
    "student_en": {
        "role": "prospect", "language": "en", "location": "Bamenda", "financial_profile": "low",
        "knowledge_level": "beginner", "digital_literacy": "high", "communication_style": "casual",
        "urgency": "normal", "trust_level": "high", "objectives": ["find_studio"],
    },
    "frustrated_pcm": {
        "role": "prospect", "language": "pcm", "location": "Limbe", "financial_profile": "mid",
        "knowledge_level": "intermediate", "digital_literacy": "medium", "communication_style": "aggressive",
        "urgency": "high", "trust_level": "low", "emotion": "frustrated",
        "objectives": ["find_apartment", "complain"],
    },
}

EMOTIONS: tuple[str, ...] = ("calm", "urgent", "enthusiastic", "distrustful", "frustrated", "aggressive", "indecisive", "chatty", "silent", "confused", "impatient", "negotiator", "worried", "dissatisfied", "satisfied")

SCENARIO_CATEGORIES: tuple[str, ...] = (
    "greeting", "property_search", "owner_listing", "qualification", "visit",
    "offer", "payment", "document", "support", "handover", "complaint",
)


@dataclass
class ConversationScenario:
    scenario_id: str
    title: str
    category: str
    user_persona: str
    user_goal: str
    required_agents: list[str]
    language: str = "fr"
    channel: str = "web"
    difficulty: str = "medium"
    max_turns: int = 20
    synthetic: bool = True


@dataclass
class ConversationSimulationState:
    simulation_id: str
    scenario_id: str
    current_turn: int = 0
    known_slots: dict[str, Any] = field(default_factory=dict)
    events: list[str] = field(default_factory=list)
    completed: bool = False
    outcome: str | None = None


@dataclass
class ScenarioOutcome:
    accepted: bool
    score: float
    reasons: list[str] = field(default_factory=list)
    turns: int = 0
