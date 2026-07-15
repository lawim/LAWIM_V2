from __future__ import annotations

from typing import Any

from .agent_models import (
    AgentCapability,
    AgentDefinition,
    AgentStatus,
    AgentType,
    CapabilityCode,
)


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, AgentDefinition] = {}

    def register(self, agent: AgentDefinition) -> AgentDefinition:
        self._agents[agent.agent_code] = agent
        return agent

    def get(self, code: str) -> AgentDefinition | None:
        return self._agents.get(code)

    def get_by_type(self, atype: AgentType) -> list[AgentDefinition]:
        return [a for a in self._agents.values() if a.agent_type == atype]

    def list(self, status: AgentStatus | None = None) -> list[AgentDefinition]:
        if status is None:
            return list(self._agents.values())
        return [a for a in self._agents.values() if a.status == status]

    def count(self) -> int:
        return len(self._agents)


def _seed_registry() -> AgentRegistry:
    reg = AgentRegistry()
    agents = [
        AgentDefinition(agent_code="conversation", name="Conversation Agent",
                         agent_type=AgentType.CONVERSATION, domain="customer_interaction",
                         description="Handles general conversation and intent detection",
                         capabilities=["CONVERSE", "SUMMARIZE_CASE"],
                         feature_flag="conversation_agent_enabled"),
        AgentDefinition(agent_code="qualification", name="Qualification Agent",
                         agent_type=AgentType.QUALIFICATION, domain="qualification",
                         description="Manages qualification wizard sessions",
                         capabilities=["QUALIFY_REQUEST"],
                         feature_flag="qualification_agent_enabled"),
        AgentDefinition(agent_code="real_estate", name="Real Estate Agent",
                         agent_type=AgentType.REAL_ESTATE, domain="real_estate",
                         description="Coordinates property search and matching",
                         capabilities=["SEARCH_PROPERTIES", "MATCH_PROPERTIES"],
                         feature_flag="real_estate_agent_enabled"),
        AgentDefinition(agent_code="search", name="Search Agent",
                         agent_type=AgentType.SEARCH, domain="search",
                         description="Executes property searches",
                         capabilities=["SEARCH_PROPERTIES"],
                         feature_flag="search_agent_enabled"),
        AgentDefinition(agent_code="matching", name="Matching Agent",
                         agent_type=AgentType.MATCHING, domain="matching",
                         description="Computes property matches",
                         capabilities=["MATCH_PROPERTIES"],
                         feature_flag="matching_agent_enabled"),
        AgentDefinition(agent_code="commercial", name="Commercial Agent",
                         agent_type=AgentType.COMMERCIAL, domain="commercial",
                         description="Proposes next commercial actions",
                         capabilities=["SUMMARIZE_CASE", "MANAGE_RELATIONSHIP"],
                         feature_flag="commercial_agent_enabled"),
        AgentDefinition(agent_code="relationship", name="Relationship Agent",
                         agent_type=AgentType.RELATIONSHIP, domain="relationship",
                         description="Tracks and nurtures user relationships",
                         capabilities=["MANAGE_RELATIONSHIP"],
                         feature_flag="relationship_agent_enabled"),
        AgentDefinition(agent_code="document", name="Document Agent",
                         agent_type=AgentType.DOCUMENT, domain="document",
                         description="Handles document identification and preparation",
                         capabilities=["ANALYZE_DOCUMENT", "PREPARE_DOCUMENT"],
                         feature_flag="document_agent_enabled"),
        AgentDefinition(agent_code="legal", name="Legal Assistance Agent",
                         agent_type=AgentType.LEGAL_ASSISTANCE, domain="legal",
                         description="Provides document assistance and guidance",
                         capabilities=["ANALYZE_DOCUMENT", "EXPLAIN_CONTRACT"],
                         risk_level="MEDIUM",
                         feature_flag="legal_assistance_agent_enabled"),
        AgentDefinition(agent_code="financial", name="Financial Agent",
                         agent_type=AgentType.FINANCIAL, domain="financial",
                         description="Explains costs and payment status",
                         capabilities=["EXPLAIN_PAYMENT", "ANALYZE_ANALYTICS"],
                         feature_flag="financial_agent_enabled"),
        AgentDefinition(agent_code="payment", name="Payment Agent",
                         agent_type=AgentType.PAYMENT, domain="payment",
                         description="Handles payment requests and status",
                         capabilities=["EXPLAIN_PAYMENT", "INITIATE_PAYMENT_REQUEST"],
                         risk_level="MEDIUM",
                         feature_flag="payment_agent_enabled"),
        AgentDefinition(agent_code="support", name="Support Agent",
                         agent_type=AgentType.SUPPORT, domain="support",
                         description="Provides user support and issue resolution",
                         capabilities=["PROVIDE_SUPPORT", "SUMMARIZE_CASE"],
                         feature_flag="support_agent_enabled"),
        AgentDefinition(agent_code="admin", name="Administration Agent",
                         agent_type=AgentType.ADMINISTRATION, domain="administration",
                         description="Manages system configuration and monitoring",
                         capabilities=["ADMINISTER_SYSTEM", "ANALYZE_ANALYTICS"],
                         risk_level="MEDIUM",
                         feature_flag="administration_agent_enabled"),
        AgentDefinition(agent_code="director", name="Director Agent",
                         agent_type=AgentType.DIRECTOR, domain="director",
                         description="Synthesizes KPIs and strategic insights",
                         capabilities=["ANALYZE_ANALYTICS"],
                         feature_flag="director_agent_enabled"),
        AgentDefinition(agent_code="learning", name="Learning Agent",
                         agent_type=AgentType.LEARNING, domain="learning",
                         description="Presents learning insights and proposals",
                         capabilities=["ANALYZE_ANALYTICS", "REVIEW_LEARNING_PROPOSAL"],
                         feature_flag="learning_agent_enabled"),
        AgentDefinition(agent_code="orchestrator", name="Orchestrator Agent",
                         agent_type=AgentType.ORCHESTRATOR, domain="orchestration",
                         description="Routes requests and coordinates multi-agent workflows",
                         capabilities=["CONVERSE"],
                         feature_flag="multi_agent_orchestration_enabled"),
    ]
    for a in agents:
        reg.register(a)
    return reg


agent_registry = _seed_registry()


class AgentCapabilityRegistry:
    def __init__(self) -> None:
        self._caps: dict[str, AgentCapability] = {}

    def register(self, cap: AgentCapability) -> AgentCapability:
        self._caps[cap.capability_code] = cap
        return cap

    def get(self, code: str) -> AgentCapability | None:
        return self._caps.get(code)

    def list(self) -> list[AgentCapability]:
        return list(self._caps.values())

    def count(self) -> int:
        return len(self._caps)


capability_registry = AgentCapabilityRegistry()
for cc in CapabilityCode:
    capability_registry.register(AgentCapability(
        capability_code=cc.value, name=cc.value,
        description=cc.value.replace("_", " ").title(),
        domain="general",
    ))
