from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Agent Types ────────────────────────────────────────────────────────────


class AgentType(str, Enum):
    ORCHESTRATOR = "ORCHESTRATOR"
    CONVERSATION = "CONVERSATION"
    QUALIFICATION = "QUALIFICATION"
    REAL_ESTATE = "REAL_ESTATE"
    SEARCH = "SEARCH"
    MATCHING = "MATCHING"
    COMMERCIAL = "COMMERCIAL"
    RELATIONSHIP = "RELATIONSHIP"
    DOCUMENT = "DOCUMENT"
    LEGAL_ASSISTANCE = "LEGAL_ASSISTANCE"
    FINANCIAL = "FINANCIAL"
    PAYMENT = "PAYMENT"
    SUPPORT = "SUPPORT"
    ADMINISTRATION = "ADMINISTRATION"
    DIRECTOR = "DIRECTOR"
    LEARNING = "LEARNING"
    SYSTEM = "SYSTEM"


class AgentStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DEPRECATED = "DEPRECATED"
    BLOCKED = "BLOCKED"
    ARCHIVED = "ARCHIVED"


# ── Agent Definition ───────────────────────────────────────────────────────


@dataclass
class AgentDefinition:
    agent_id: str = ""
    agent_code: str = ""
    name: str = ""
    description: str = ""
    agent_type: AgentType = AgentType.CONVERSATION
    domain: str = ""
    version: str = "1.0"
    status: AgentStatus = AgentStatus.DRAFT
    risk_level: str = "LOW"
    default_language: str = "fr"
    supported_languages: list[str] = field(default_factory=lambda: ["fr", "en"])
    capabilities: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    required_permissions: list[str] = field(default_factory=list)
    forbidden_actions: list[str] = field(default_factory=list)
    handover_policy: str = "manual"
    memory_policy: str = "conversation_only"
    context_policy: str = "strict"
    timeout_seconds: int = 30
    retry_count: int = 2
    feature_flag: str = ""
    created_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_code": self.agent_code,
            "name": self.name,
            "agent_type": self.agent_type.value,
            "domain": self.domain,
            "status": self.status.value,
            "version": self.version,
            "risk_level": self.risk_level,
            "feature_flag": self.feature_flag,
        }


# ── Capabilities ───────────────────────────────────────────────────────────


class CapabilityCode(str, Enum):
    CONVERSE = "CONVERSE"
    QUALIFY_REQUEST = "QUALIFY_REQUEST"
    SEARCH_PROPERTIES = "SEARCH_PROPERTIES"
    MATCH_PROPERTIES = "MATCH_PROPERTIES"
    CREATE_VISIT_REQUEST = "CREATE_VISIT_REQUEST"
    PREPARE_TRANSACTION = "PREPARE_TRANSACTION"
    ANALYZE_DOCUMENT = "ANALYZE_DOCUMENT"
    PREPARE_DOCUMENT = "PREPARE_DOCUMENT"
    EXPLAIN_PAYMENT = "EXPLAIN_PAYMENT"
    INITIATE_PAYMENT_REQUEST = "INITIATE_PAYMENT_REQUEST"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    SUMMARIZE_CASE = "SUMMARIZE_CASE"
    ANALYZE_ANALYTICS = "ANALYZE_ANALYTICS"
    REVIEW_LEARNING_PROPOSAL = "REVIEW_LEARNING_PROPOSAL"
    EXPLAIN_CONTRACT = "EXPLAIN_CONTRACT"
    MANAGE_RELATIONSHIP = "MANAGE_RELATIONSHIP"
    PROVIDE_SUPPORT = "PROVIDE_SUPPORT"
    ADMINISTER_SYSTEM = "ADMINISTER_SYSTEM"


@dataclass
class AgentCapability:
    capability_code: str = ""
    name: str = ""
    description: str = ""
    domain: str = ""
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    required_permissions: list[str] = field(default_factory=list)
    required_feature_flags: list[str] = field(default_factory=list)
    risk_level: str = "LOW"
    idempotent: bool = False
    human_confirmation_required: bool = False
    allowed_tools: list[str] = field(default_factory=list)
    forbidden_tools: list[str] = field(default_factory=list)
    version: str = "1.0"
    status: str = "ACTIVE"

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_code": self.capability_code,
            "name": self.name,
            "domain": self.domain,
            "risk_level": self.risk_level,
            "human_confirmation_required": self.human_confirmation_required,
        }


# ── Invocation ─────────────────────────────────────────────────────────────


class InvocationStatus(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    WAITING_FOR_TOOL = "WAITING_FOR_TOOL"
    WAITING_FOR_AGENT = "WAITING_FOR_AGENT"
    WAITING_FOR_HUMAN = "WAITING_FOR_HUMAN"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMED_OUT = "TIMED_OUT"
    ESCALATED = "ESCALATED"


@dataclass
class AgentInvocation:
    invocation_id: str = ""
    agent_id: str = ""
    agent_code: str = ""
    conversation_id: str = ""
    actor_id: str = ""
    user_id: int | None = None
    case_id: str = ""
    parent_invocation_id: str = ""
    correlation_id: str = ""
    input_text: str = ""
    context_reference: str = ""
    requested_capability: str = ""
    status: InvocationStatus = InvocationStatus.CREATED
    started_at: str = ""
    completed_at: str = ""
    timeout_at: str = ""
    result: str = ""
    error: str = ""
    risk_level: str = "LOW"
    human_confirmation_status: str = "NOT_REQUIRED"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "invocation_id": self.invocation_id,
            "agent_code": self.agent_code,
            "conversation_id": self.conversation_id,
            "status": self.status.value,
            "requested_capability": self.requested_capability,
            "started_at": self.started_at,
        }


# ── Response ───────────────────────────────────────────────────────────────


@dataclass
class AgentResponse:
    response_id: str = ""
    invocation_id: str = ""
    agent_id: str = ""
    agent_code: str = ""
    content: str = ""
    content_type: str = "text"
    language: str = "fr"
    confidence: float = 1.0
    sources: list[str] = field(default_factory=list)
    actions: list[dict[str, Any]] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    requires_human_review: bool = False
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "response_id": self.response_id,
            "agent_code": self.agent_code,
            "content": self.content[:100],
            "confidence": self.confidence,
            "requires_human_review": self.requires_human_review,
        }


# ── Action ─────────────────────────────────────────────────────────────────


@dataclass
class AgentAction:
    action_id: str = ""
    invocation_id: str = ""
    agent_id: str = ""
    action_type: str = ""
    target_type: str = ""
    target_id: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    status: str = "PENDING"
    approval_required: bool = False
    approved_by: str = ""
    executed_at: str = ""
    result: str = ""
    error: str = ""
    idempotency_key: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "target_type": self.target_type,
            "status": self.status,
            "approval_required": self.approval_required,
        }


# ── Handover ───────────────────────────────────────────────────────────────


class HandoverStatus(str, Enum):
    REQUESTED = "REQUESTED"
    QUEUED = "QUEUED"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


@dataclass
class AgentHandover:
    handover_id: str = ""
    conversation_id: str = ""
    source_agent_id: str = ""
    target_actor_or_team: str = ""
    reason: str = ""
    priority: str = "NORMAL"
    summary: str = ""
    context_references: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    recommended_action: str = ""
    status: HandoverStatus = HandoverStatus.REQUESTED
    created_at: str = ""
    accepted_at: str = ""
    resolved_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "handover_id": self.handover_id,
            "source_agent_id": self.source_agent_id,
            "target": self.target_actor_or_team,
            "reason": self.reason,
            "status": self.status.value,
        }


# ── Memory ─────────────────────────────────────────────────────────────────


class MemoryType(str, Enum):
    WORKING = "WORKING"
    CONVERSATION = "CONVERSATION"
    CASE = "CASE"
    USER_PREFERENCE = "USER_PREFERENCE"
    RELATIONSHIP = "RELATIONSHIP"
    AGENT_WORKING = "AGENT_WORKING"
    KNOWLEDGE_REFERENCE = "KNOWLEDGE_REFERENCE"
    LEARNING_REFERENCE = "LEARNING_REFERENCE"


@dataclass
class AgentMemory:
    memory_id: str = ""
    memory_type: MemoryType = MemoryType.WORKING
    conversation_id: str = ""
    actor_id: str = ""
    case_id: str = ""
    key: str = ""
    value: str = ""
    ttl_seconds: int = 0
    created_at: str = ""
    expires_at: str = ""


# ── Runtime Context ────────────────────────────────────────────────────────


@dataclass
class AgentRuntimeContext:
    actor_id: str = ""
    user_id: int | None = None
    conversation_id: str = ""
    channel: str = ""
    language: str = "fr"
    case_id: str = ""
    property_id: int | None = None
    feature_flags: dict[str, bool] = field(default_factory=dict)
    permissions: list[str] = field(default_factory=list)
    memory_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "actor_id": self.actor_id,
            "conversation_id": self.conversation_id,
            "channel": self.channel,
            "language": self.language,
        }


# ── Tool ───────────────────────────────────────────────────────────────────


class ToolRiskLevel(str, Enum):
    READ_ONLY = "READ_ONLY"
    LOW_RISK_WRITE = "LOW_RISK_WRITE"
    SENSITIVE_WRITE = "SENSITIVE_WRITE"
    FINANCIAL = "FINANCIAL"
    LEGAL = "LEGAL"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    IRREVERSIBLE = "IRREVERSIBLE"


@dataclass
class AgentTool:
    tool_code: str = ""
    name: str = ""
    domain: str = ""
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    risk_level: ToolRiskLevel = ToolRiskLevel.READ_ONLY
    required_permissions: list[str] = field(default_factory=list)
    confirmation_required: bool = False
    idempotent: bool = False
    timeout_seconds: int = 30
    audit_level: str = "STANDARD"
    status: str = "ACTIVE"

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_code": self.tool_code,
            "name": self.name,
            "risk_level": self.risk_level.value,
            "confirmation_required": self.confirmation_required,
        }


@dataclass
class AgentToolInvocation:
    invocation_id: str = ""
    tool_code: str = ""
    agent_id: str = ""
    input: dict[str, Any] = field(default_factory=dict)
    output: dict[str, Any] = field(default_factory=dict)
    status: str = "PENDING"
    error: str = ""
    started_at: str = ""
    completed_at: str = ""


# ── Safety ─────────────────────────────────────────────────────────────────


class RiskCategory(str, Enum):
    READ_ONLY = "READ_ONLY"
    LOW_RISK_WRITE = "LOW_RISK_WRITE"
    SENSITIVE_WRITE = "SENSITIVE_WRITE"
    FINANCIAL = "FINANCIAL"
    LEGAL = "LEGAL"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    IRREVERSIBLE = "IRREVERSIBLE"


class SafetyDecision(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_MASKING = "ALLOW_WITH_MASKING"
    ALLOW_WITH_CONFIRMATION = "ALLOW_WITH_CONFIRMATION"
    HANDOVER_REQUIRED = "HANDOVER_REQUIRED"
    DENY = "DENY"


# ── Delegation ─────────────────────────────────────────────────────────────


@dataclass
class AgentDelegation:
    delegation_id: str = ""
    parent_invocation_id: str = ""
    source_agent_id: str = ""
    target_agent_id: str = ""
    capability: str = ""
    input_summary: str = ""
    context_scope: str = ""
    status: str = "PENDING"
    started_at: str = ""
    completed_at: str = ""
    result: str = ""
    error: str = ""


# ── Evaluation ─────────────────────────────────────────────────────────────


class EvalStatus(str, Enum):
    PASS = "PASS"
    PASS_WITH_WARNINGS = "PASS_WITH_WARNINGS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"


@dataclass
class AgentEvaluationResult:
    evaluation_id: str = ""
    agent_id: str = ""
    scenario: str = ""
    status: EvalStatus = EvalStatus.FAIL
    accuracy: float = 0.0
    consistency: float = 0.0
    safety: float = 0.0
    latency_ms: float = 0.0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evaluated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "evaluation_id": self.evaluation_id,
            "agent_id": self.agent_id,
            "scenario": self.scenario,
            "status": self.status.value,
            "accuracy": self.accuracy,
            "safety": self.safety,
        }
