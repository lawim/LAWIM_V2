from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class AgentActivationStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BLOCKED = "BLOCKED"


@dataclass
class AgentActivation:
    agent_code: str = ""
    status: AgentActivationStatus = AgentActivationStatus.DRAFT
    version: str = "1.0"
    feature_flag: str = ""
    activated_at: str = ""
    deactivated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"agent_code": self.agent_code, "status": self.status.value,
                "feature_flag": self.feature_flag}


AGENT_ACTIVATIONS: list[AgentActivation] = [
    AgentActivation("conversation", feature_flag="conversation_agent_enabled"),
    AgentActivation("qualification", feature_flag="qualification_agent_enabled"),
    AgentActivation("real_estate", feature_flag="real_estate_agent_enabled"),
    AgentActivation("search", feature_flag="search_agent_enabled"),
    AgentActivation("matching", feature_flag="matching_agent_enabled"),
    AgentActivation("commercial", feature_flag="commercial_agent_enabled"),
    AgentActivation("relationship", feature_flag="relationship_agent_enabled"),
    AgentActivation("document", feature_flag="document_agent_enabled"),
    AgentActivation("legal", feature_flag="legal_assistance_agent_enabled"),
    AgentActivation("financial", feature_flag="financial_agent_enabled"),
    AgentActivation("payment", feature_flag="payment_agent_enabled"),
    AgentActivation("support", feature_flag="support_agent_enabled"),
    AgentActivation("admin", feature_flag="administration_agent_enabled"),
    AgentActivation("director", feature_flag="director_agent_enabled"),
    AgentActivation("learning", feature_flag="learning_agent_enabled"),
    AgentActivation("orchestrator", feature_flag="multi_agent_orchestration_enabled"),
]


@dataclass
class AgentMetrics:
    agent_code: str = ""
    invocations: int = 0
    success_rate: float = 0.0
    avg_latency_ms: float = 0.0
    handover_count: int = 0
    error_count: int = 0
    last_invocation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"agent_code": self.agent_code, "invocations": self.invocations,
                "success_rate": round(self.success_rate, 1), "avg_latency_ms": self.avg_latency_ms}


@dataclass
class AgentEvaluationResult:
    agent_code: str = ""
    scenario: str = ""
    accuracy: float = 0.0
    safety: float = 0.0
    latency_ms: float = 0.0
    passed: bool = False
    evaluated_at: str = ""


@dataclass
class PersistedAgentMemory:
    memory_id: str = ""
    agent_code: str = ""
    memory_type: str = ""
    conversation_id: str = ""
    key: str = ""
    value: str = ""
    ttl_days: int = 30
    created_at: str = ""
    expires_at: str = ""
    tenant_id: str = ""
