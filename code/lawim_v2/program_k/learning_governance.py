"""Program K Final — Governance, Publication, Rollout, Monitoring, Rollback."""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

_now = lambda: datetime.now(timezone.utc).isoformat()


# ── Risk Levels ────────────────────────────────────────────────────────────

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ── Governance Permissions ───────────────────────────────────────────────

LEARNING_PERMISSIONS: tuple[str, ...] = (
    "learning.events.read",
    "learning.datasets.read", "learning.datasets.build",
    "learning.analysis.read",
    "learning.hypotheses.manage",
    "learning.proposals.manage", "learning.proposals.review",
    "learning.proposals.approve",
    "learning.experiments.manage",
    "learning.publications.prepare", "learning.publications.approve",
    "learning.publications.execute",
    "learning.rollouts.manage", "learning.rollbacks.execute",
    "learning.audit.read", "learning.emergency_stop",
)


# ── Governance Policy ─────────────────────────────────────────────────────

@dataclass
class LearningGovernancePolicy:
    policy_id: str = ""
    policy_code: str = ""
    name: str = ""
    description: str = ""
    scope: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    required_reviews: int = 1
    required_approvals: int = 1
    required_roles: list[str] = field(default_factory=list)
    prohibited_role_combinations: list[list[str]] = field(default_factory=list)
    testing_requirements: str = ""
    rollout_requirements: str = ""
    monitoring_requirements: str = ""
    rollback_requirements: str = ""
    status: str = "ACTIVE"
    version: str = "1.0"
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_code": self.policy_code,
            "name": self.name,
            "risk_level": self.risk_level.value,
            "required_reviews": self.required_reviews,
            "required_approvals": self.required_approvals,
            "status": self.status,
        }


# ── Release Gates ─────────────────────────────────────────────────────────

class GateStatus(str, Enum):
    PENDING = "PENDING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


RELEASE_GATES: tuple[str, ...] = (
    "SCHEMA_VALID", "REFERENCES_VALID", "UNIT_TESTS_PASS",
    "INTEGRATION_TESTS_PASS", "NON_REGRESSION_PASS",
    "DATA_QUALITY_PASS", "BIAS_CHECK_PASS", "LEAKAGE_CHECK_PASS",
    "RUNTIME_COMPATIBILITY_PASS", "ROLLBACK_TESTED",
    "APPROVALS_COMPLETE", "FEATURE_FLAGS_READY", "MONITORING_READY",
)


# ── Knowledge Evolution Package (Final) ──────────────────────────────────

class PackageStatus(str, Enum):
    DRAFT = "DRAFT"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"
    UNDER_REVIEW = "UNDER_REVIEW"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    APPROVED = "APPROVED"
    READY_FOR_PUBLICATION = "READY_FOR_PUBLICATION"
    PUBLISHING = "PUBLISHING"
    PUBLISHED = "PUBLISHED"
    PARTIALLY_ROLLED_OUT = "PARTIALLY_ROLLED_OUT"
    FULLY_ROLLED_OUT = "FULLY_ROLLED_OUT"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    ARCHIVED = "ARCHIVED"


@dataclass
class FinalKnowledgeEvolutionPackage:
    package_id: str = ""
    package_code: str = ""
    title: str = ""
    description: str = ""
    proposal_ids: list[str] = field(default_factory=list)
    hypothesis_ids: list[str] = field(default_factory=list)
    experiment_ids: list[str] = field(default_factory=list)
    target_components: list[str] = field(default_factory=list)
    base_versions: dict[str, str] = field(default_factory=dict)
    target_versions: dict[str, str] = field(default_factory=dict)
    semantic_diff: str = ""
    machine_diff: str = ""
    migration_plan: str = ""
    test_plan: list[str] = field(default_factory=list)
    validation_results: dict[str, str] = field(default_factory=dict)
    risk_level: RiskLevel = RiskLevel.LOW
    governance_policy_id: str = ""
    feature_flags: list[str] = field(default_factory=list)
    rollout_plan_id: str = ""
    rollback_plan_id: str = ""
    checksum: str = ""
    created_by: str = ""
    created_at: str = ""
    status: PackageStatus = PackageStatus.DRAFT
    release_gates: dict[str, GateStatus] = field(default_factory=lambda: {g: GateStatus.PENDING for g in RELEASE_GATES})

    def compute_checksum(self) -> str:
        raw = json.dumps({
            "proposal_ids": sorted(self.proposal_ids),
            "target_components": sorted(self.target_components),
            "base_versions": self.base_versions,
            "target_versions": self.target_versions,
            "semantic_diff": self.semantic_diff,
            "migration_plan": self.migration_plan,
        }, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        gate_results = {k: v.value for k, v in self.release_gates.items()}
        return {
            "package_id": self.package_id,
            "package_code": self.package_code,
            "title": self.title,
            "risk_level": self.risk_level.value,
            "status": self.status.value,
            "checksum": self.checksum[:16] if self.checksum else "",
            "release_gates": gate_results,
        }

    def all_gates_passed(self) -> bool:
        return all(v == GateStatus.PASSED for v in self.release_gates.values())


# ── Semantic Diff ─────────────────────────────────────────────────────────

@dataclass
class SemanticDiff:
    diff_id: str = ""
    package_id: str = ""
    added_taxonomies: list[str] = field(default_factory=list)
    removed_taxonomies: list[str] = field(default_factory=list)
    modified_taxonomies: list[str] = field(default_factory=list)
    added_fields: list[str] = field(default_factory=list)
    removed_fields: list[str] = field(default_factory=list)
    modified_fields: list[str] = field(default_factory=list)
    modified_thresholds: list[str] = field(default_factory=list)
    modified_weights: list[str] = field(default_factory=list)
    added_rules: list[str] = field(default_factory=list)
    removed_rules: list[str] = field(default_factory=list)
    modified_rules: list[str] = field(default_factory=list)
    affected_matrices: list[str] = field(default_factory=list)
    affected_apis: list[str] = field(default_factory=list)
    migrations_required: bool = False
    compatibility: str = "UNKNOWN"
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "diff_id": self.diff_id,
            "compatibility": self.compatibility,
            "migrations_required": self.migrations_required,
            "added_taxonomies": len(self.added_taxonomies),
            "removed_taxonomies": len(self.removed_taxonomies),
            "affected_matrices": len(self.affected_matrices),
        }


# ── Knowledge Version ─────────────────────────────────────────────────────

class VersionStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    PUBLISHED = "PUBLISHED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DEPRECATED = "DEPRECATED"
    ROLLED_BACK = "ROLLED_BACK"
    ARCHIVED = "ARCHIVED"


@dataclass
class KnowledgeVersion:
    version_id: str = ""
    component: str = ""
    version: str = ""
    parent_version: str = ""
    package_id: str = ""
    checksum: str = ""
    schema_version: str = "1.0"
    created_at: str = ""
    published_at: str = ""
    published_by: str = ""
    status: VersionStatus = VersionStatus.DRAFT
    feature_flag: str = ""
    rollout_status: str = "NOT_STARTED"
    snapshot_location: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version_id": self.version_id,
            "component": self.component,
            "version": self.version,
            "status": self.status.value,
            "rollout_status": self.rollout_status,
        }


# ── Rollout ───────────────────────────────────────────────────────────────

class RolloutStrategy(str, Enum):
    INTERNAL_ONLY = "INTERNAL_ONLY"
    PILOT_GROUP = "PILOT_GROUP"
    PERCENTAGE = "PERCENTAGE"
    ROLE_BASED = "ROLE_BASED"
    AGENCY_BASED = "AGENCY_BASED"
    CHANNEL_BASED = "CHANNEL_BASED"
    REGION_BASED = "REGION_BASED"
    FULL = "FULL"


class RolloutStage(str, Enum):
    ZERO_PERCENT = "0_PERCENT"
    INTERNAL = "INTERNAL"
    ONE_PERCENT = "1_PERCENT"
    FIVE_PERCENT = "5_PERCENT"
    TEN_PERCENT = "10_PERCENT"
    TWENTYFIVE_PERCENT = "25_PERCENT"
    FIFTY_PERCENT = "50_PERCENT"
    HUNDRED_PERCENT = "100_PERCENT"


@dataclass
class LearningRolloutPlan:
    rollout_plan_id: str = ""
    package_id: str = ""
    strategy: RolloutStrategy = RolloutStrategy.INTERNAL_ONLY
    stages: list[RolloutStage] = field(default_factory=lambda: [
        RolloutStage.ZERO_PERCENT, RolloutStage.INTERNAL,
        RolloutStage.ONE_PERCENT, RolloutStage.FIVE_PERCENT,
        RolloutStage.TEN_PERCENT, RolloutStage.TWENTYFIVE_PERCENT,
        RolloutStage.FIFTY_PERCENT, RolloutStage.HUNDRED_PERCENT,
    ])
    current_stage: RolloutStage = RolloutStage.ZERO_PERCENT
    control_population_pct: float = 5.0
    success_metrics: list[str] = field(default_factory=list)
    guardrail_metrics: list[str] = field(default_factory=list)
    stop_conditions: list[str] = field(default_factory=list)
    rollback_conditions: list[str] = field(default_factory=list)
    status: str = "DRAFT"
    created_by: str = ""
    approved_by: str = ""
    started_at: str = ""
    paused_at: str = ""
    stopped_at: str = ""
    completed_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "rollout_plan_id": self.rollout_plan_id,
            "strategy": self.strategy.value,
            "current_stage": self.current_stage.value,
            "status": self.status,
        }

    def advance_stage(self) -> bool:
        idx = self.stages.index(self.current_stage) if self.current_stage in self.stages else -1
        if idx < len(self.stages) - 1:
            self.current_stage = self.stages[idx + 1]
            return True
        return False


# ── Guardrail ─────────────────────────────────────────────────────────────

class GuardrailAction(str, Enum):
    WARN = "WARN"
    PAUSE_ROLLOUT = "PAUSE_ROLLOUT"
    STOP_ROLLOUT = "STOP_ROLLOUT"
    ROLLBACK = "ROLLBACK"
    REQUIRE_REVIEW = "REQUIRE_REVIEW"


@dataclass
class LearningGuardrail:
    guardrail_id: str = ""
    metric_code: str = ""
    operator: str = "GREATER_THAN"
    threshold: float = 0.0
    window_minutes: int = 60
    minimum_sample: int = 10
    severity: str = "WARNING"
    action: GuardrailAction = GuardrailAction.WARN
    status: str = "ACTIVE"

    def evaluate(self, current_value: float) -> GuardrailAction | None:
        if self.operator == "GREATER_THAN" and current_value > self.threshold:
            return self.action
        if self.operator == "LESS_THAN" and current_value < self.threshold:
            return self.action
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "guardrail_id": self.guardrail_id,
            "metric_code": self.metric_code,
            "threshold": self.threshold,
            "action": self.action.value,
            "status": self.status,
        }


# ── Drift ─────────────────────────────────────────────────────────────────

class DriftType(str, Enum):
    DATA_DRIFT = "DATA_DRIFT"
    FEATURE_DRIFT = "FEATURE_DRIFT"
    OUTCOME_DRIFT = "OUTCOME_DRIFT"
    FEEDBACK_DRIFT = "FEEDBACK_DRIFT"
    PERFORMANCE_DRIFT = "PERFORMANCE_DRIFT"
    CHANNEL_DRIFT = "CHANNEL_DRIFT"
    REGIONAL_DRIFT = "REGIONAL_DRIFT"
    LANGUAGE_DRIFT = "LANGUAGE_DRIFT"


class DriftStatus(str, Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    UNDER_REVIEW = "UNDER_REVIEW"
    RESOLVED = "RESOLVED"
    FALSE_POSITIVE = "FALSE_POSITIVE"


@dataclass
class DriftEvent:
    drift_id: str = ""
    drift_type: DriftType = DriftType.DATA_DRIFT
    dataset_id: str = ""
    baseline_period: str = ""
    current_period: str = ""
    metric: str = ""
    baseline_value: float = 0.0
    current_value: float = 0.0
    difference: float = 0.0
    severity: str = "LOW"
    sample_size: int = 0
    detected_at: str = ""
    status: DriftStatus = DriftStatus.OPEN
    recommendation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "drift_id": self.drift_id,
            "drift_type": self.drift_type.value,
            "metric": self.metric,
            "baseline_value": self.baseline_value,
            "current_value": self.current_value,
            "difference": self.difference,
            "severity": self.severity,
            "status": self.status.value,
        }


# ── Rollback Plan ─────────────────────────────────────────────────────────

@dataclass
class KnowledgeRollbackPlan:
    rollback_plan_id: str = ""
    package_id: str = ""
    source_version: str = ""
    target_version: str = ""
    trigger_conditions: list[str] = field(default_factory=list)
    data_rollback_strategy: str = ""
    runtime_rollback_strategy: str = ""
    session_handling: str = ""
    migration_rollback: str = ""
    validation_steps: list[str] = field(default_factory=list)
    estimated_impact: str = ""
    status: str = "DRAFT"

    def to_dict(self) -> dict[str, Any]:
        return {
            "rollback_plan_id": self.rollback_plan_id,
            "source_version": self.source_version,
            "target_version": self.target_version,
            "status": self.status,
        }


# ── Post-Publication Evaluation ───────────────────────────────────────────

class PostPublicationResult(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    INCONCLUSIVE = "INCONCLUSIVE"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"


@dataclass
class PostPublicationEvaluation:
    evaluation_id: str = ""
    package_id: str = ""
    target_metrics: dict[str, float] = field(default_factory=dict)
    guardrail_results: dict[str, str] = field(default_factory=dict)
    adoption_rate: float = 0.0
    error_count: int = 0
    latency_p95: float = 0.0
    quality_score: float = 0.0
    bias_detected: bool = False
    satisfaction_score: float = 0.0
    conversion_rate: float = 0.0
    handover_rate: float = 0.0
    result: PostPublicationResult = PostPublicationResult.INCONCLUSIVE
    conclusion: str = ""
    evaluated_at: str = ""
    evaluator: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "evaluation_id": self.evaluation_id,
            "result": self.result.value,
            "adoption_rate": self.adoption_rate,
            "error_count": self.error_count,
        }
