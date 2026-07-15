from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentConfig:
    agent_platform_enabled: bool = False
    conversation_agent_enabled: bool = False
    qualification_agent_enabled: bool = False
    real_estate_agent_enabled: bool = False
    search_agent_enabled: bool = False
    matching_agent_enabled: bool = False
    commercial_agent_enabled: bool = False
    relationship_agent_enabled: bool = False
    document_agent_enabled: bool = False
    legal_assistance_agent_enabled: bool = False
    financial_agent_enabled: bool = False
    payment_agent_enabled: bool = False
    support_agent_enabled: bool = False
    administration_agent_enabled: bool = False
    director_agent_enabled: bool = False
    learning_agent_enabled: bool = False
    multi_agent_orchestration_enabled: bool = False
    agent_memory_enabled: bool = False
    agent_admin_controls_enabled: bool = False
