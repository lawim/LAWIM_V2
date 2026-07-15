"""Program K Final — Governance, Publication, Rollout, Rollback Services."""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any

from .learning_governance import (
    DriftEvent,
    DriftStatus,
    DriftType,
    FinalKnowledgeEvolutionPackage,
    GateStatus,
    GuardrailAction,
    KnowledgeRollbackPlan,
    KnowledgeVersion,
    LearningGovernancePolicy,
    LearningGuardrail,
    LearningRolloutPlan,
    PackageStatus,
    PostPublicationEvaluation,
    PostPublicationResult,
    RELEASE_GATES,
    RiskLevel,
    RolloutStage,
    RolloutStrategy,
    SemanticDiff,
    VersionStatus,
)

_now = lambda: datetime.now(timezone.utc).isoformat()


# ── Governance Policy Service ──────────────────────────────────────────────

class GovernancePolicyService:
    def __init__(self):
        self._policies: list[LearningGovernancePolicy] = []

    def create(self, p: LearningGovernancePolicy) -> LearningGovernancePolicy:
        p.policy_id = str(uuid.uuid4())
        p.created_at = _now()
        self._policies.append(p)
        return p

    def get(self, pid: str) -> LearningGovernancePolicy | None:
        for p in self._policies:
            if p.policy_id == pid:
                return p
        return None

    def get_for_risk(self, risk: RiskLevel) -> LearningGovernancePolicy | None:
        for p in self._policies:
            if p.risk_level == risk:
                return p
        return None

    def list(self) -> list[LearningGovernancePolicy]:
        return list(self._policies)

    def check_separation(self, actor_id: str, action: str, policy: LearningGovernancePolicy) -> bool:
        return True  # Stub — would check actor's roles/permissions


# ── Knowledge Evolution Package Service ────────────────────────────────────

class FinalEvolutionPackageService:
    def __init__(self):
        self._packages: list[FinalKnowledgeEvolutionPackage] = []

    def create(self, pkg: FinalKnowledgeEvolutionPackage) -> FinalKnowledgeEvolutionPackage:
        pkg.package_id = str(uuid.uuid4())
        pkg.created_at = _now()
        pkg.status = PackageStatus.DRAFT
        self._packages.append(pkg)
        return pkg

    def get(self, pid: str) -> FinalKnowledgeEvolutionPackage | None:
        for p in self._packages:
            if p.package_id == pid:
                return p
        return None

    def list(self, status: PackageStatus | None = None) -> list[FinalKnowledgeEvolutionPackage]:
        if status is None:
            return list(self._packages)
        return [p for p in self._packages if p.status == status]

    def update_gate(self, pid: str, gate: str, status: GateStatus) -> FinalKnowledgeEvolutionPackage | None:
        pkg = self.get(pid)
        if pkg and gate in pkg.release_gates:
            pkg.release_gates[gate] = status
        return pkg

    def submit_for_review(self, pid: str) -> FinalKnowledgeEvolutionPackage | None:
        pkg = self.get(pid)
        if pkg and pkg.status == PackageStatus.DRAFT:
            pkg.checksum = pkg.compute_checksum()
            pkg.status = PackageStatus.READY_FOR_REVIEW
        return pkg

    def approve(self, pid: str) -> FinalKnowledgeEvolutionPackage | None:
        pkg = self.get(pid)
        if pkg and pkg.status == PackageStatus.READY_FOR_REVIEW:
            if pkg.all_gates_passed():
                pkg.status = PackageStatus.READY_FOR_PUBLICATION
            else:
                pkg.status = PackageStatus.APPROVED
        return pkg


# ── Semantic Diff Service ──────────────────────────────────────────────────

class SemanticDiffService:
    def compute(self, pkg: FinalKnowledgeEvolutionPackage) -> SemanticDiff:
        diff = SemanticDiff(
            diff_id=str(uuid.uuid4()),
            package_id=pkg.package_id,
            created_at=_now(),
        )
        diff.compatibility = "COMPATIBLE"
        return diff

    def check_runtime_compatibility(self, pkg: FinalKnowledgeEvolutionPackage) -> str:
        return "COMPATIBLE"


# ── Knowledge Publication Service ──────────────────────────────────────────

class KnowledgePublicationService:
    def __init__(self):
        self._versions: list[KnowledgeVersion] = []
        self._publications: list[dict[str, Any]] = []

    def prepare(self, pkg: FinalKnowledgeEvolutionPackage) -> dict[str, Any]:
        return {"status": "PREPARED", "package_id": pkg.package_id}

    def validate(self, pkg: FinalKnowledgeEvolutionPackage) -> list[str]:
        issues: list[str] = []
        if pkg.status != PackageStatus.READY_FOR_PUBLICATION:
            issues.append(f"Invalid status: {pkg.status}")
        if not pkg.all_gates_passed():
            failed = [k for k, v in pkg.release_gates.items() if v != GateStatus.PASSED]
            issues.append(f"Gates not passed: {failed}")
        return issues

    def publish(self, pkg: FinalKnowledgeEvolutionPackage,
                 published_by: str = "") -> KnowledgeVersion | None:
        issues = self.validate(pkg)
        if issues:
            return None
        pkg.status = PackageStatus.PUBLISHED
        version = KnowledgeVersion(
            version_id=str(uuid.uuid4()),
            component="knowledge_rules",
            version=pkg.target_versions.get("knowledge_rules", "1.0"),
            package_id=pkg.package_id,
            checksum=pkg.checksum,
            published_at=_now(),
            published_by=published_by,
            status=VersionStatus.PUBLISHED,
        )
        self._versions.append(version)
        self._publications.append({
            "publication_id": str(uuid.uuid4()),
            "package_id": pkg.package_id,
            "version_id": version.version_id,
            "published_at": _now(),
            "published_by": published_by,
        })
        return version

    def get_versions(self, component: str | None = None) -> list[KnowledgeVersion]:
        if component is None:
            return list(self._versions)
        return [v for v in self._versions if v.component == component]


# ── Rollout Service ───────────────────────────────────────────────────────

class LearningRolloutService:
    def __init__(self):
        self._plans: list[LearningRolloutPlan] = []

    def create_plan(self, plan: LearningRolloutPlan) -> LearningRolloutPlan:
        plan.rollout_plan_id = str(uuid.uuid4())
        self._plans.append(plan)
        return plan

    def get_plan(self, pid: str) -> LearningRolloutPlan | None:
        for p in self._plans:
            if p.rollout_plan_id == pid:
                return p
        return None

    def start(self, pid: str) -> LearningRolloutPlan | None:
        plan = self.get_plan(pid)
        if plan:
            plan.status = "RUNNING"
            plan.started_at = _now()
        return plan

    def advance(self, pid: str) -> LearningRolloutPlan | None:
        plan = self.get_plan(pid)
        if plan and plan.advance_stage():
            return plan
        return plan

    def pause(self, pid: str) -> LearningRolloutPlan | None:
        plan = self.get_plan(pid)
        if plan:
            plan.status = "PAUSED"
            plan.paused_at = _now()
        return plan

    def stop(self, pid: str) -> LearningRolloutPlan | None:
        plan = self.get_plan(pid)
        if plan:
            plan.status = "STOPPED"
            plan.stopped_at = _now()
        return plan


# ── Deterministic Assignment Service ───────────────────────────────────────

class RolloutAssignmentService:
    def assign(self, user_id: str, plan: LearningRolloutPlan) -> str:
        h = hashlib.sha256(str(user_id).encode()).hexdigest()
        val = int(h[:8], 16) % 100
        stage_map = {
            RolloutStage.ZERO_PERCENT: 0, RolloutStage.INTERNAL: 0,
            RolloutStage.ONE_PERCENT: 1, RolloutStage.FIVE_PERCENT: 5,
            RolloutStage.TEN_PERCENT: 10, RolloutStage.TWENTYFIVE_PERCENT: 25,
            RolloutStage.FIFTY_PERCENT: 50, RolloutStage.HUNDRED_PERCENT: 100,
        }
        threshold = stage_map.get(plan.current_stage, 0)
        if val < threshold:
            return "treatment"
        if val < threshold + int(plan.control_population_pct):
            return "control"
        return "inactive"


# ── Guardrail Service ─────────────────────────────────────────────────────

class GuardrailService:
    def __init__(self):
        self._guardrails: list[LearningGuardrail] = []

    def register(self, g: LearningGuardrail) -> LearningGuardrail:
        g.guardrail_id = str(uuid.uuid4())
        self._guardrails.append(g)
        return g

    def list(self) -> list[LearningGuardrail]:
        return list(self._guardrails)

    def evaluate_all(self, metrics: dict[str, float]) -> list[GuardrailAction]:
        actions: list[GuardrailAction] = []
        for g in self._guardrails:
            value = metrics.get(g.metric_code)
            if value is not None:
                action = g.evaluate(value)
                if action:
                    actions.append(action)
        return actions


# ── Monitoring Service ────────────────────────────────────────────────────

class LearningRolloutMonitoringService:
    def check_guardrails(self, guardrails: list[LearningGuardrail],
                          metrics: dict[str, float]) -> list[dict[str, Any]]:
        alerts: list[dict[str, Any]] = []
        for g in guardrails:
            value = metrics.get(g.metric_code)
            if value is not None:
                action = g.evaluate(value)
                if action:
                    alerts.append({
                        "guardrail_id": g.guardrail_id,
                        "metric": g.metric_code,
                        "value": value,
                        "threshold": g.threshold,
                        "action": action.value,
                    })
        return alerts


# ── Drift Detection Service ────────────────────────────────────────────────

class LearningDriftDetectionService:
    def __init__(self):
        self._drifts: list[DriftEvent] = []

    def detect(self, drift: DriftEvent) -> DriftEvent:
        drift.drift_id = str(uuid.uuid4())
        drift.detected_at = _now()
        drift.status = DriftStatus.OPEN
        self._drifts.append(drift)
        return drift

    def acknowledge(self, did: str) -> DriftEvent | None:
        for d in self._drifts:
            if d.drift_id == did:
                d.status = DriftStatus.ACKNOWLEDGED
                return d
        return None

    def list(self, status: DriftStatus | None = None) -> list[DriftEvent]:
        if status is None:
            return list(self._drifts)
        return [d for d in self._drifts if d.status == status]


# ── Emergency Control Service ─────────────────────────────────────────────

class LearningEmergencyControlService:
    def pause_rollout(self, plan: LearningRolloutPlan) -> LearningRolloutPlan:
        plan.status = "PAUSED"
        plan.paused_at = _now()
        return plan

    def stop_rollout(self, plan: LearningRolloutPlan) -> LearningRolloutPlan:
        plan.status = "STOPPED"
        plan.stopped_at = _now()
        return plan

    def emergency_rollback(self, plan: LearningRolloutPlan,
                            pkg: FinalKnowledgeEvolutionPackage) -> FinalKnowledgeEvolutionPackage:
        plan.status = "ROLLED_BACK"
        pkg.status = PackageStatus.ROLLED_BACK
        return pkg


# ── Rollback Service ──────────────────────────────────────────────────────

class KnowledgeRollbackService:
    def __init__(self):
        self._plans: list[KnowledgeRollbackPlan] = []
        self._executions: list[dict[str, Any]] = []

    def create_plan(self, rp: KnowledgeRollbackPlan) -> KnowledgeRollbackPlan:
        rp.rollback_plan_id = str(uuid.uuid4())
        self._plans.append(rp)
        return rp

    def execute(self, rp: KnowledgeRollbackPlan, pkg: FinalKnowledgeEvolutionPackage) -> dict[str, Any]:
        pkg.status = PackageStatus.ROLLED_BACK
        execution = {
            "execution_id": str(uuid.uuid4()),
            "rollback_plan_id": rp.rollback_plan_id,
            "package_id": pkg.package_id,
            "source_version": rp.source_version,
            "target_version": rp.target_version,
            "executed_at": _now(),
            "status": "COMPLETED",
        }
        self._executions.append(execution)
        return execution


# ── Post-Publication Evaluation Service ────────────────────────────────────

class PostPublicationEvaluationService:
    def __init__(self):
        self._evaluations: list[PostPublicationEvaluation] = []

    def evaluate(self, ev: PostPublicationEvaluation) -> PostPublicationEvaluation:
        ev.evaluation_id = str(uuid.uuid4())
        ev.evaluated_at = _now()
        self._evaluations.append(ev)
        return ev

    def get(self, eid: str) -> PostPublicationEvaluation | None:
        for e in self._evaluations:
            if e.evaluation_id == eid:
                return e
        return None

    def list(self) -> list[PostPublicationEvaluation]:
        return list(self._evaluations)


# ── API Handler ────────────────────────────────────────────────────────────

from .learning_config_p2 import LearningConfigP2 as KConfig

_config = KConfig(
    learning_dataset_builder_enabled=False,
    learning_analysis_enabled=False,
    learning_proposal_engine_enabled=False,
    learning_experiments_enabled=False,
    knowledge_evolution_packages_enabled=False,
)


def handle_k_final_get(path: str, query: dict[str, list[str]],
                        actor: dict[str, object]) -> dict[str, Any] | None:
    if path == "learning/policies":
        return {"status": "disabled", "message": "learning_governance_enabled=false"}
    if path == "learning/final/packages":
        return {"status": "disabled", "message": "knowledge_publication_enabled=false"}
    if path == "learning/versions":
        return {"status": "disabled", "message": "knowledge_publication_enabled=false"}
    if path == "learning/rollouts":
        return {"status": "disabled", "message": "learning_rollout_enabled=false"}
    if path == "learning/guardrails":
        return {"status": "disabled", "message": "learning_guardrails_enabled=false"}
    if path == "learning/drift":
        return {"status": "disabled", "message": "learning_drift_detection_enabled=false"}
    if path == "learning/rollback":
        return {"status": "disabled", "message": "learning_rollback_enabled=false"}
    return None
