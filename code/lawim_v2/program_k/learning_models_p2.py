from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Dataset ────────────────────────────────────────────────────────────────


class DatasetStatus(str, Enum):
    DRAFT = "DRAFT"
    BUILDING = "BUILDING"
    READY = "READY"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
    SUPERSEDED = "SUPERSEDED"


class DatasetCategory(str, Enum):
    CONVERSATION_QUALITY = "CONVERSATION_QUALITY"
    QUALIFICATION_EFFECTIVENESS = "QUALIFICATION_EFFECTIVENESS"
    MATCHING_EFFECTIVENESS = "MATCHING_EFFECTIVENESS"
    VISIT_CONVERSION = "VISIT_CONVERSION"
    TRANSACTION_CONVERSION = "TRANSACTION_CONVERSION"
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"
    CAMPAIGN_PERFORMANCE = "CAMPAIGN_PERFORMANCE"
    PUBLICATION_PERFORMANCE = "PUBLICATION_PERFORMANCE"
    CHANNEL_PERFORMANCE = "CHANNEL_PERFORMANCE"
    ACTOR_PERFORMANCE = "ACTOR_PERFORMANCE"
    RESPONSE_EFFECTIVENESS = "RESPONSE_EFFECTIVENESS"
    HUMAN_HANDOVER = "HUMAN_HANDOVER"
    ABANDONMENT_ANALYSIS = "ABANDONMENT_ANALYSIS"
    CUSTOMER_SATISFACTION = "CUSTOMER_SATISFACTION"


@dataclass
class LearningDataset:
    dataset_id: str = ""
    dataset_code: str = ""
    name: str = ""
    description: str = ""
    domain: str = ""
    purpose: str = ""
    category: DatasetCategory = DatasetCategory.CONVERSATION_QUALITY
    source_event_types: list[str] = field(default_factory=list)
    source_outcome_types: list[str] = field(default_factory=list)
    source_feedback_types: list[str] = field(default_factory=list)
    filters: dict[str, Any] = field(default_factory=dict)
    inclusion_rules: list[str] = field(default_factory=list)
    exclusion_rules: list[str] = field(default_factory=list)
    time_window_days: int = 90
    created_at: str = ""
    created_by: str = ""
    version: str = "1.0"
    schema_version: str = "1.0"
    status: DatasetStatus = DatasetStatus.DRAFT
    privacy_level: int = 0
    retention_days: int = 365
    row_count: int = 0
    quality_status: str = "DRAFT"
    checksum: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "dataset_code": self.dataset_code,
            "name": self.name,
            "domain": self.domain,
            "category": self.category.value,
            "version": self.version,
            "status": self.status.value,
            "row_count": self.row_count,
            "quality_status": self.quality_status,
            "checksum": self.checksum[:16] if self.checksum else "",
        }


# ── Feature Definition ─────────────────────────────────────────────────────


@dataclass(frozen=True)
class FeatureDefinition:
    feature_code: str
    name: str
    description: str
    domain: str
    data_type: str
    source: str
    calculation: str
    calculation_version: str
    allowed_values: tuple[str, ...] = ()
    missing_value_policy: str = "DROP"
    privacy_level: int = 0
    bias_risk: str = "LOW"
    leakage_risk: str = "LOW"
    status: str = "ACTIVE"

    def to_dict(self) -> dict[str, Any]:
        return {
            "feature_code": self.feature_code,
            "name": self.name,
            "domain": self.domain,
            "data_type": self.data_type,
            "calculation_version": self.calculation_version,
            "bias_risk": self.bias_risk,
            "leakage_risk": self.leakage_risk,
        }


# ── Hypothesis ─────────────────────────────────────────────────────────────


class HypothesisStatus(str, Enum):
    DRAFT = "DRAFT"
    PROPOSED = "PROPOSED"
    APPROVED_FOR_EXPERIMENT = "APPROVED_FOR_EXPERIMENT"
    REJECTED = "REJECTED"
    RUNNING = "RUNNING"
    VALIDATED = "VALIDATED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"


@dataclass
class LearningHypothesis:
    hypothesis_id: str = ""
    title: str = ""
    description: str = ""
    domain: str = ""
    source_analysis: str = ""
    expected_effect: str = ""
    target_metric: str = ""
    baseline_value: float = 0.0
    target_value: float = 0.0
    population: str = ""
    time_window_days: int = 30
    risk_level: str = "LOW"
    created_by: str = ""
    created_at: str = ""
    status: HypothesisStatus = HypothesisStatus.DRAFT
    evidence: str = ""
    limitations: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "hypothesis_id": self.hypothesis_id,
            "title": self.title,
            "domain": self.domain,
            "target_metric": self.target_metric,
            "status": self.status.value,
            "risk_level": self.risk_level,
        }


# ── Proposal ───────────────────────────────────────────────────────────────


class ProposalStatus(str, Enum):
    DRAFT = "DRAFT"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPERIMENTAL = "EXPERIMENTAL"
    PUBLISHED = "PUBLISHED"
    ROLLED_BACK = "ROLLED_BACK"
    ARCHIVED = "ARCHIVED"


class ProposalType(str, Enum):
    MODIFY_QUESTION_ORDER = "MODIFY_QUESTION_ORDER"
    MODIFY_THRESHOLD = "MODIFY_THRESHOLD"
    MODIFY_WEIGHT = "MODIFY_WEIGHT"
    ADD_RECOMMENDATION = "ADD_RECOMMENDATION"
    REMOVE_RULE = "REMOVE_RULE"
    ADAPT_CHANNEL = "ADAPT_CHANNEL"
    ADAPT_LANGUAGE = "ADAPT_LANGUAGE"
    ADAPT_TERRITORY = "ADAPT_TERRITORY"
    ADAPT_PROPERTY_TYPE = "ADAPT_PROPERTY_TYPE"
    ADAPT_HANDOVER = "ADAPT_HANDOVER"
    ADAPT_WORKFLOW = "ADAPT_WORKFLOW"


@dataclass
class LearningProposal:
    proposal_id: str = ""
    proposal_type: ProposalType = ProposalType.MODIFY_QUESTION_ORDER
    target_component: str = ""
    target_version: str = ""
    proposed_change: str = ""
    current_value: str = ""
    proposed_value: str = ""
    source_dataset_id: str = ""
    source_analysis_id: str = ""
    supporting_metrics: dict[str, float] = field(default_factory=dict)
    sample_size: int = 0
    confidence: float = 0.0
    expected_impact: str = ""
    risk: str = "LOW"
    limitations: str = ""
    rollback_plan: str = ""
    hypothesis_id: str = ""
    created_by: str = ""
    created_at: str = ""
    status: ProposalStatus = ProposalStatus.DRAFT

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "proposal_type": self.proposal_type.value,
            "target_component": self.target_component,
            "status": self.status.value,
            "sample_size": self.sample_size,
            "confidence": self.confidence,
            "risk": self.risk,
        }


# ── Review ─────────────────────────────────────────────────────────────────


class ReviewDecision(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REQUEST_CHANGES = "REQUEST_CHANGES"
    APPROVE_FOR_EXPERIMENT = "APPROVE_FOR_EXPERIMENT"


@dataclass
class LearningReview:
    review_id: str = ""
    proposal_id: str = ""
    reviewer_actor_id: str = ""
    decision: ReviewDecision = ReviewDecision.REQUEST_CHANGES
    comment: str = ""
    risk_assessment: str = ""
    requested_changes: str = ""
    reviewed_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "proposal_id": self.proposal_id,
            "decision": self.decision.value,
            "reviewer_actor_id": self.reviewer_actor_id,
        }


# ── Experiment ─────────────────────────────────────────────────────────────


class ExperimentStatus(str, Enum):
    DRAFT = "DRAFT"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"


class ExperimentResult(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    INCONCLUSIVE = "INCONCLUSIVE"
    STOPPED_FOR_RISK = "STOPPED_FOR_RISK"
    INVALID_DATA = "INVALID_DATA"


@dataclass
class LearningExperiment:
    experiment_id: str = ""
    hypothesis_id: str = ""
    proposal_id: str = ""
    name: str = ""
    population: str = ""
    control_group: str = ""
    treatment_group: str = ""
    allocation_method: str = "RANDOM"
    start_at: str = ""
    end_at: str = ""
    target_metrics: list[str] = field(default_factory=list)
    guardrail_metrics: list[str] = field(default_factory=list)
    feature_flag: str = ""
    status: ExperimentStatus = ExperimentStatus.DRAFT
    result: ExperimentResult = ExperimentResult.INCONCLUSIVE
    conclusion: str = ""
    rollback_status: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "status": self.status.value,
            "result": self.result.value,
            "feature_flag": self.feature_flag,
        }


# ── Evolution Package ─────────────────────────────────────────────────────


@dataclass
class KnowledgeEvolutionPackage:
    package_id: str = ""
    proposal_ids: list[str] = field(default_factory=list)
    target_components: list[str] = field(default_factory=list)
    base_versions: dict[str, str] = field(default_factory=dict)
    proposed_versions: dict[str, str] = field(default_factory=dict)
    diff: str = ""
    tests_required: list[str] = field(default_factory=list)
    migration_required: bool = False
    feature_flags: list[str] = field(default_factory=list)
    rollback_plan: str = ""
    approvals: list[str] = field(default_factory=list)
    status: str = "DRAFT"
    created_at: str = ""
    published_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "proposal_count": len(self.proposal_ids),
            "status": self.status,
            "migration_required": self.migration_required,
        }


# ── Version Record ─────────────────────────────────────────────────────────


@dataclass
class VersionRecord:
    version_id: str = ""
    component_type: str = ""
    component_id: str = ""
    version: str = ""
    parent_version: str = ""
    checksum: str = ""
    created_at: str = ""
    created_by: str = ""
    status: str = "ACTIVE"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version_id": self.version_id,
            "component_type": self.component_type,
            "component_id": self.component_id,
            "version": self.version,
            "status": self.status,
        }
