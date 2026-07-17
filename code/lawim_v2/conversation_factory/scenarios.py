from __future__ import annotations
from .models import ConversationScenario

SCENARIOS: list[ConversationScenario] = [
    ConversationScenario(
        scenario_id="SC-RENT-001", title="Location appartement Douala", category="property_search",
        user_persona="prospect_rent_fr", user_goal="Trouver un appartement 2 pièces à Douala",
        required_agents=["CONVERSATION", "QUALIFICATION", "REAL_ESTATE"], language="fr",
    ),
    ConversationScenario(
        scenario_id="SC-BUY-001", title="Achat maison Yaoundé", category="property_search",
        user_persona="prospect_buy_en", user_goal="Buy a 3-bedroom house in Yaounde",
        required_agents=["CONVERSATION", "QUALIFICATION", "REAL_ESTATE"], language="en",
    ),
    ConversationScenario(
        scenario_id="SC-LIST-001", title="Publication bien Buea", category="owner_listing",
        user_persona="owner_pcm", user_goal="List my property for rent for Buea",
        required_agents=["CONVERSATION", "REAL_ESTATE", "DOCUMENT"], language="pcm",
    ),
    ConversationScenario(
        scenario_id="SC-VISIT-001", title="Demande de visite", category="visit",
        user_persona="prospect_rent_fr", user_goal="Schedule a visit for a listed property",
        required_agents=["CONVERSATION", "VISIT_TRANSACTION"], language="fr",
    ),
    ConversationScenario(
        scenario_id="SC-SUPPORT-001", title="Réclamation", category="complaint",
        user_persona="frustrated_pcm", user_goal="Complain about a failed visit",
        required_agents=["CONVERSATION", "SUPPORT"], language="pcm",
    ),
    ConversationScenario(
        scenario_id="SC-INVEST-001", title="Investissement Kribi", category="property_search",
        user_persona="investor_fr", user_goal="Find land investment opportunity in Kribi",
        required_agents=["CONVERSATION", "QUALIFICATION", "FINANCIAL"], language="fr",
    ),
    ConversationScenario(
        scenario_id="SC-STUDIO-001", title="Studio Bamenda", category="property_search",
        user_persona="student_en", user_goal="Find an affordable studio in Bamenda",
        required_agents=["CONVERSATION", "QUALIFICATION", "REAL_ESTATE"], language="en",
    ),
]
