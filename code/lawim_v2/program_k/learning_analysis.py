from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from .learning_models import LearningEvent, OutcomeResult, OutcomeStatus
from .learning_models_p2 import (
    ExperimentResult,
    ExperimentStatus,
    HypothesisStatus,
    KnowledgeEvolutionPackage,
    LearningExperiment,
    LearningHypothesis,
    LearningProposal,
    LearningReview,
    ProposalStatus,
    ProposalType,
    ReviewDecision,
    VersionRecord,
)
from .learning_datasets import LearningDataset

_now = lambda: datetime.now(timezone.utc).isoformat()


class LearningAnalysisEngine:
    def analyze_outcomes(self, outcomes: list[OutcomeResult],
                          group_by: str = "outcome_type") -> list[dict[str, Any]]:
        groups: dict[str, list[OutcomeResult]] = {}
        for o in outcomes:
            key = str(getattr(o, group_by, "unknown"))
            if key not in groups:
                groups[key] = []
            groups[key].append(o)

        results = []
        for key, grp in sorted(groups.items()):
            total = len(grp)
            successes = sum(1 for o in grp if o.status == OutcomeStatus.SUCCESS)
            failures = sum(1 for o in grp if o.status == OutcomeStatus.FAILURE)
            revenue = sum(o.monetary_value for o in grp)
            results.append({
                "group": key,
                "total": total,
                "successes": successes,
                "failures": failures,
                "success_rate_pct": round(successes / total * 100, 2) if total else 0,
                "total_revenue": revenue,
            })
        return results

    def analyze_trend(self, outcomes: list[OutcomeResult],
                       time_field: str = "occurred_at") -> dict[str, Any]:
        if not outcomes:
            return {"trend": "NO_DATA", "total": 0}
        successes = sum(1 for o in outcomes if o.status == OutcomeStatus.SUCCESS)
        total = len(outcomes)
        return {
            "trend": "POSITIVE" if successes / total > 0.5 else "NEGATIVE",
            "total": total,
            "successes": successes,
            "success_rate": round(successes / total * 100, 2),
            "total_revenue": sum(o.monetary_value for o in outcomes),
        }

    def cohort_analysis(self, outcomes: list[OutcomeResult],
                         dimension: str) -> list[dict[str, Any]]:
        cohorts: dict[str, list[OutcomeResult]] = {}
        for o in outcomes:
            key = str(getattr(o, dimension, "UNKNOWN"))
            if key not in cohorts:
                cohorts[key] = []
            cohorts[key].append(o)

        results = []
        for key, grp in sorted(cohorts.items()):
            total = len(grp)
            successes = sum(1 for o in grp if o.status == OutcomeStatus.SUCCESS)
            results.append({
                "cohort": key,
                "dimension": dimension,
                "sample_size": total,
                "successes": successes,
                "success_rate_pct": round(successes / total * 100, 2) if total else 0,
                "avg_monetary_value": round(sum(o.monetary_value for o in grp) / total, 2) if total else 0,
            })
        return sorted(results, key=lambda r: r["success_rate_pct"], reverse=True)


# ── Hypothesis Service ──────────────────────────────────────────────────────


class LearningHypothesisService:
    def __init__(self) -> None:
        self._hypotheses: list[LearningHypothesis] = []

    def create(self, h: LearningHypothesis) -> LearningHypothesis:
        h.hypothesis_id = str(uuid.uuid4())
        h.created_at = _now()
        h.status = HypothesisStatus.DRAFT
        self._hypotheses.append(h)
        return h

    def get(self, hid: str) -> LearningHypothesis | None:
        for h in self._hypotheses:
            if h.hypothesis_id == hid:
                return h
        return None

    def list(self, status: HypothesisStatus | None = None) -> list[LearningHypothesis]:
        if status is None:
            return list(self._hypotheses)
        return [h for h in self._hypotheses if h.status == status]

    def update_status(self, hid: str, status: HypothesisStatus) -> LearningHypothesis | None:
        h = self.get(hid)
        if h:
            h.status = status
        return h


# ── Proposal Engine ────────────────────────────────────────────────────────


class LearningProposalEngine:
    def __init__(self) -> None:
        self._proposals: list[LearningProposal] = []
        self._reviews: list[LearningReview] = []

    def create(self, p: LearningProposal) -> LearningProposal:
        p.proposal_id = str(uuid.uuid4())
        p.created_at = _now()
        p.status = ProposalStatus.DRAFT
        self._proposals.append(p)
        return p

    def get(self, pid: str) -> LearningProposal | None:
        for p in self._proposals:
            if p.proposal_id == pid:
                return p
        return None

    def list(self, status: ProposalStatus | None = None) -> list[LearningProposal]:
        if status is None:
            return list(self._proposals)
        return [p for p in self._proposals if p.status == status]

    def submit_for_review(self, pid: str) -> LearningProposal | None:
        p = self.get(pid)
        if p and p.status == ProposalStatus.DRAFT:
            p.status = ProposalStatus.READY_FOR_REVIEW
        return p

    def review(self, pid: str, reviewer_id: str, decision: ReviewDecision,
                comment: str = "") -> LearningReview | None:
        p = self.get(pid)
        if p is None:
            return None
        review = LearningReview(
            review_id=str(uuid.uuid4()),
            proposal_id=pid,
            reviewer_actor_id=reviewer_id,
            decision=decision,
            comment=comment,
            reviewed_at=_now(),
        )
        self._reviews.append(review)
        if decision == ReviewDecision.APPROVE:
            p.status = ProposalStatus.APPROVED
        elif decision == ReviewDecision.APPROVE_FOR_EXPERIMENT:
            p.status = ProposalStatus.EXPERIMENTAL
        elif decision == ReviewDecision.REJECT:
            p.status = ProposalStatus.REJECTED
        return review

    def get_reviews(self, pid: str) -> list[LearningReview]:
        return [r for r in self._reviews if r.proposal_id == pid]


# ── Experiment Service ──────────────────────────────────────────────────────


class LearningExperimentService:
    def __init__(self) -> None:
        self._experiments: list[LearningExperiment] = []

    def create(self, e: LearningExperiment) -> LearningExperiment:
        e.experiment_id = str(uuid.uuid4())
        e.status = ExperimentStatus.DRAFT
        self._experiments.append(e)
        return e

    def get(self, eid: str) -> LearningExperiment | None:
        for e in self._experiments:
            if e.experiment_id == eid:
                return e
        return None

    def list(self) -> list[LearningExperiment]:
        return list(self._experiments)

    def start(self, eid: str) -> LearningExperiment | None:
        e = self.get(eid)
        if e:
            e.status = ExperimentStatus.RUNNING
            e.start_at = _now()
        return e

    def stop(self, eid: str) -> LearningExperiment | None:
        e = self.get(eid)
        if e:
            e.status = ExperimentStatus.STOPPED
            e.end_at = _now()
        return e


class ExperimentEvaluationService:
    def evaluate(self, experiment: LearningExperiment,
                  control_outcomes: list[OutcomeResult],
                  treatment_outcomes: list[OutcomeResult]) -> LearningExperiment:
        control_success = sum(1 for o in control_outcomes if o.status == OutcomeStatus.SUCCESS)
        treatment_success = sum(1 for o in treatment_outcomes if o.status == OutcomeStatus.SUCCESS)
        control_rate = control_success / max(len(control_outcomes), 1)
        treatment_rate = treatment_success / max(len(treatment_outcomes), 1)

        if len(control_outcomes) < 5 or len(treatment_outcomes) < 5:
            experiment.result = ExperimentResult.INCONCLUSIVE
            experiment.conclusion = "Sample size too small"
        elif treatment_rate > control_rate * 1.05:
            experiment.result = ExperimentResult.POSITIVE
            experiment.conclusion = f"Treatment improved rate from {control_rate:.1%} to {treatment_rate:.1%}"
        elif treatment_rate < control_rate * 0.95:
            experiment.result = ExperimentResult.NEGATIVE
            experiment.conclusion = f"Treatment decreased rate from {control_rate:.1%} to {treatment_rate:.1%}"
        else:
            experiment.result = ExperimentResult.INCONCLUSIVE
            experiment.conclusion = "No significant difference detected"

        experiment.status = ExperimentStatus.COMPLETED
        experiment.end_at = _now()
        return experiment


# ── Evolution Package Service ──────────────────────────────────────────────


class EvolutionPackageService:
    def __init__(self) -> None:
        self._packages: list[KnowledgeEvolutionPackage] = []

    def create(self, pkg: KnowledgeEvolutionPackage) -> KnowledgeEvolutionPackage:
        pkg.package_id = str(uuid.uuid4())
        pkg.created_at = _now()
        self._packages.append(pkg)
        return pkg

    def get(self, pid: str) -> KnowledgeEvolutionPackage | None:
        for p in self._packages:
            if p.package_id == pid:
                return p
        return None

    def list(self) -> list[KnowledgeEvolutionPackage]:
        return list(self._packages)


# ── Version Service ────────────────────────────────────────────────────────


class VersionService:
    def __init__(self) -> None:
        self._versions: list[VersionRecord] = []

    def register(self, component_type: str, component_id: str,
                  version: str, parent: str = "", created_by: str = "") -> VersionRecord:
        v = VersionRecord(
            version_id=str(uuid.uuid4()),
            component_type=component_type,
            component_id=component_id,
            version=version,
            parent_version=parent,
            created_at=_now(),
            created_by=created_by,
        )
        self._versions.append(v)
        return v

    def get_history(self, component_type: str, component_id: str) -> list[VersionRecord]:
        return [v for v in self._versions
                if v.component_type == component_type and v.component_id == component_id]

    def list_all(self) -> list[VersionRecord]:
        return list(self._versions)
