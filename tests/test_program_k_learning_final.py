# Program K Final — Governance, Publication, Rollout, Monitoring, Rollback Tests
from __future__ import annotations

import json
import unittest

from lawim_v2.program_k.learning_governance import (
    DriftEvent, DriftStatus, DriftType,
    FinalKnowledgeEvolutionPackage, GateStatus,
    GuardrailAction, KnowledgeRollbackPlan, KnowledgeVersion,
    LEARNING_PERMISSIONS, LearningGovernancePolicy,
    LearningGuardrail, LearningRolloutPlan,
    PackageStatus, PostPublicationEvaluation, PostPublicationResult,
    RELEASE_GATES, RiskLevel, RolloutStage, RolloutStrategy,
    SemanticDiff, VersionStatus,
)
from lawim_v2.program_k.learning_gov_services import (
    FinalEvolutionPackageService,
    GovernancePolicyService,
    GuardrailService,
    KnowledgePublicationService,
    KnowledgeRollbackService,
    LearningDriftDetectionService,
    LearningEmergencyControlService,
    LearningRolloutMonitoringService,
    LearningRolloutService,
    PostPublicationEvaluationService,
    RolloutAssignmentService,
    SemanticDiffService,
)


# ── Governance Policy Tests ──────────────────────────────────────────────


class GovernancePolicyServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = GovernancePolicyService()

    def test_create_low_risk(self):
        p = self.svc.create(LearningGovernancePolicy(
            policy_code="POL-LOW-001", name="Low Risk",
            risk_level=RiskLevel.LOW, required_reviews=1))
        self.assertIsNotNone(p.policy_id)
        self.assertEqual(p.risk_level, RiskLevel.LOW)

    def test_create_critical(self):
        p = self.svc.create(LearningGovernancePolicy(
            policy_code="POL-CRIT-001", name="Critical",
            risk_level=RiskLevel.CRITICAL, required_reviews=2, required_approvals=2))
        self.assertEqual(p.risk_level, RiskLevel.CRITICAL)
        self.assertEqual(p.required_approvals, 2)

    def test_get(self):
        p = self.svc.create(LearningGovernancePolicy(name="Test"))
        self.assertIsNotNone(self.svc.get(p.policy_id))

    def test_get_for_risk(self):
        self.svc.create(LearningGovernancePolicy(name="L", risk_level=RiskLevel.LOW))
        found = self.svc.get_for_risk(RiskLevel.LOW)
        self.assertIsNotNone(found)

    def test_to_dict(self):
        p = self.svc.create(LearningGovernancePolicy(name="Test", risk_level=RiskLevel.HIGH))
        d = p.to_dict()
        self.assertEqual(d["risk_level"], "HIGH")

    def test_permissions_list(self):
        self.assertIn("learning.events.read", LEARNING_PERMISSIONS)
        self.assertIn("learning.publications.approve", LEARNING_PERMISSIONS)
        self.assertIn("learning.emergency_stop", LEARNING_PERMISSIONS)


# ── Evolution Package Tests ──────────────────────────────────────────────


class FinalEvolutionPackageServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = FinalEvolutionPackageService()

    def test_create(self):
        pkg = self.svc.create(FinalKnowledgeEvolutionPackage(
            title="Improve wizard ordering"))
        self.assertIsNotNone(pkg.package_id)
        self.assertEqual(pkg.status, PackageStatus.DRAFT)

    def test_compute_checksum(self):
        pkg = FinalKnowledgeEvolutionPackage(title="Test")
        cs1 = pkg.compute_checksum()
        cs2 = pkg.compute_checksum()
        self.assertEqual(cs1, cs2)

    def test_submit_for_review(self):
        pkg = self.svc.create(FinalKnowledgeEvolutionPackage(title="Test"))
        self.svc.submit_for_review(pkg.package_id)
        self.assertEqual(pkg.status, PackageStatus.READY_FOR_REVIEW)
        self.assertTrue(len(pkg.checksum) > 0)

    def test_all_gates_passed_default_false(self):
        pkg = FinalKnowledgeEvolutionPackage()
        self.assertFalse(pkg.all_gates_passed())

    def test_all_gates_passed_true(self):
        pkg = FinalKnowledgeEvolutionPackage()
        for g in pkg.release_gates:
            pkg.release_gates[g] = GateStatus.PASSED
        self.assertTrue(pkg.all_gates_passed())

    def test_update_gate(self):
        pkg = self.svc.create(FinalKnowledgeEvolutionPackage(title="Test"))
        self.svc.update_gate(pkg.package_id, "SCHEMA_VALID", GateStatus.PASSED)
        self.assertEqual(pkg.release_gates["SCHEMA_VALID"], GateStatus.PASSED)

    def test_approve_without_gates(self):
        pkg = self.svc.create(FinalKnowledgeEvolutionPackage(title="Test"))
        self.svc.submit_for_review(pkg.package_id)
        self.svc.approve(pkg.package_id)
        self.assertEqual(pkg.status, PackageStatus.APPROVED)

    def test_approve_with_all_gates(self):
        pkg = self.svc.create(FinalKnowledgeEvolutionPackage(title="Test"))
        for g in pkg.release_gates:
            pkg.release_gates[g] = GateStatus.PASSED
        self.svc.submit_for_review(pkg.package_id)
        self.svc.approve(pkg.package_id)
        self.assertEqual(pkg.status, PackageStatus.READY_FOR_PUBLICATION)

    def test_to_dict(self):
        pkg = self.svc.create(FinalKnowledgeEvolutionPackage(title="Test"))
        d = pkg.to_dict()
        self.assertEqual(d["title"], "Test")
        self.assertIn("release_gates", d)

    def test_release_gates_list(self):
        self.assertIn("SCHEMA_VALID", RELEASE_GATES)
        self.assertIn("ROLLBACK_TESTED", RELEASE_GATES)
        self.assertIn("APPROVALS_COMPLETE", RELEASE_GATES)
        self.assertEqual(len(RELEASE_GATES), 13)


# ── Semantic Diff Tests ─────────────────────────────────────────────────


class SemanticDiffServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = SemanticDiffService()

    def test_compute(self):
        pkg = FinalKnowledgeEvolutionPackage(title="Test")
        diff = self.svc.compute(pkg)
        self.assertIsNotNone(diff.diff_id)
        self.assertEqual(diff.compatibility, "COMPATIBLE")

    def test_runtime_compatibility(self):
        pkg = FinalKnowledgeEvolutionPackage(title="Test")
        result = self.svc.check_runtime_compatibility(pkg)
        self.assertEqual(result, "COMPATIBLE")

    def test_diff_to_dict(self):
        diff = SemanticDiff(diff_id="d1", compatibility="COMPATIBLE_WITH_MIGRATION",
                             migrations_required=True)
        d = diff.to_dict()
        self.assertTrue(d["migrations_required"])


# ── Publication Service Tests ────────────────────────────────────────────


class KnowledgePublicationServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = KnowledgePublicationService()

    def test_prepare(self):
        pkg = FinalKnowledgeEvolutionPackage(title="Test")
        result = self.svc.prepare(pkg)
        self.assertEqual(result["status"], "PREPARED")

    def test_validate_fails_if_not_ready(self):
        pkg = FinalKnowledgeEvolutionPackage(title="Test")
        issues = self.svc.validate(pkg)
        self.assertGreaterEqual(len(issues), 1)

    def test_publish_success(self):
        pkg = FinalKnowledgeEvolutionPackage(title="Test", checksum="abc")
        pkg.status = PackageStatus.READY_FOR_PUBLICATION
        for g in pkg.release_gates:
            pkg.release_gates[g] = GateStatus.PASSED
        version = self.svc.publish(pkg, "admin1")
        self.assertIsNotNone(version)
        self.assertEqual(version.status, VersionStatus.PUBLISHED)

    def test_publish_fails_if_not_ready(self):
        pkg = FinalKnowledgeEvolutionPackage(title="Test")
        version = self.svc.publish(pkg)
        self.assertIsNone(version)

    def test_get_versions(self):
        self.assertEqual(len(self.svc.get_versions()), 0)

    def test_version_to_dict(self):
        v = KnowledgeVersion(version_id="v1", component="rules", version="2.0",
                              status=VersionStatus.ACTIVE)
        d = v.to_dict()
        self.assertEqual(d["version"], "2.0")


# ── Rollout Plan Tests ──────────────────────────────────────────────────


class LearningRolloutServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = LearningRolloutService()

    def test_create_plan(self):
        plan = self.svc.create_plan(LearningRolloutPlan(strategy=RolloutStrategy.PERCENTAGE))
        self.assertIsNotNone(plan.rollout_plan_id)
        self.assertEqual(plan.strategy, RolloutStrategy.PERCENTAGE)

    def test_start(self):
        plan = self.svc.create_plan(LearningRolloutPlan())
        self.svc.start(plan.rollout_plan_id)
        self.assertEqual(plan.status, "RUNNING")

    def test_pause(self):
        plan = self.svc.create_plan(LearningRolloutPlan())
        self.svc.start(plan.rollout_plan_id)
        self.svc.pause(plan.rollout_plan_id)
        self.assertEqual(plan.status, "PAUSED")

    def test_stop(self):
        plan = self.svc.create_plan(LearningRolloutPlan())
        self.svc.start(plan.rollout_plan_id)
        self.svc.stop(plan.rollout_plan_id)
        self.assertEqual(plan.status, "STOPPED")

    def test_advance_stage(self):
        plan = LearningRolloutPlan()
        self.assertEqual(plan.current_stage, RolloutStage.ZERO_PERCENT)
        plan.advance_stage()
        self.assertEqual(plan.current_stage, RolloutStage.INTERNAL)

    def test_to_dict(self):
        plan = self.svc.create_plan(LearningRolloutPlan(strategy=RolloutStrategy.FULL))
        d = plan.to_dict()
        self.assertEqual(d["strategy"], "FULL")


# ── Rollout Assignment Tests ─────────────────────────────────────────────


class RolloutAssignmentServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = RolloutAssignmentService()

    def test_deterministic(self):
        plan = LearningRolloutPlan(current_stage=RolloutStage.HUNDRED_PERCENT)
        r1 = self.svc.assign("user1", plan)
        r2 = self.svc.assign("user1", plan)
        self.assertEqual(r1, r2)

    def test_zero_percent_inactive(self):
        plan = LearningRolloutPlan(current_stage=RolloutStage.ZERO_PERCENT)
        r = self.svc.assign("user2", plan)
        self.assertEqual(r, "inactive")

    def test_different_users_may_differ(self):
        plan = LearningRolloutPlan(current_stage=RolloutStage.FIFTY_PERCENT)
        r1 = self.svc.assign("user_a", plan)
        r2 = self.svc.assign("user_b", plan)
        # both should be valid assignments
        self.assertIn(r1, ("treatment", "control", "inactive"))
        self.assertIn(r2, ("treatment", "control", "inactive"))


# ── Guardrail Tests ─────────────────────────────────────────────────────


class GuardrailServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = GuardrailService()

    def test_register(self):
        g = self.svc.register(LearningGuardrail(
            metric_code="ERROR_RATE", operator="GREATER_THAN",
            threshold=0.05, action=GuardrailAction.PAUSE_ROLLOUT))
        self.assertIsNotNone(g.guardrail_id)
        self.assertEqual(g.action, GuardrailAction.PAUSE_ROLLOUT)

    def test_evaluate_triggers(self):
        g = LearningGuardrail(metric_code="ERROR_RATE", operator="GREATER_THAN",
                               threshold=0.05, action=GuardrailAction.STOP_ROLLOUT)
        action = g.evaluate(0.10)
        self.assertEqual(action, GuardrailAction.STOP_ROLLOUT)

    def test_evaluate_no_trigger(self):
        g = LearningGuardrail(metric_code="ERROR_RATE", operator="GREATER_THAN",
                               threshold=0.05, action=GuardrailAction.WARN)
        action = g.evaluate(0.01)
        self.assertIsNone(action)

    def test_evaluate_all(self):
        self.svc.register(LearningGuardrail(
            metric_code="ERROR_RATE", operator="GREATER_THAN",
            threshold=0.05, action=GuardrailAction.PAUSE_ROLLOUT))
        actions = self.svc.evaluate_all({"ERROR_RATE": 0.10})
        self.assertEqual(len(actions), 1)

    def test_to_dict(self):
        g = LearningGuardrail(guardrail_id="g1", metric_code="LATENCY", threshold=2000)
        d = g.to_dict()
        self.assertEqual(d["metric_code"], "LATENCY")


# ── Monitoring Tests ────────────────────────────────────────────────────


class LearningRolloutMonitoringServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = LearningRolloutMonitoringService()

    def test_check_guardrails(self):
        guardrails = [LearningGuardrail(
            metric_code="ERROR_RATE", operator="GREATER_THAN",
            threshold=0.05, action=GuardrailAction.WARN)]
        alerts = self.svc.check_guardrails(guardrails, {"ERROR_RATE": 0.10})
        self.assertEqual(len(alerts), 1)

    def test_no_alert_below_threshold(self):
        guardrails = [LearningGuardrail(
            metric_code="ERROR_RATE", operator="GREATER_THAN",
            threshold=0.05, action=GuardrailAction.WARN)]
        alerts = self.svc.check_guardrails(guardrails, {"ERROR_RATE": 0.01})
        self.assertEqual(len(alerts), 0)


# ── Drift Detection Tests ───────────────────────────────────────────────


class LearningDriftDetectionServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = LearningDriftDetectionService()

    def test_detect(self):
        d = self.svc.detect(DriftEvent(drift_type=DriftType.PERFORMANCE_DRIFT,
                                        metric="conversion_rate",
                                        baseline_value=0.15, current_value=0.08))
        self.assertIsNotNone(d.drift_id)
        self.assertEqual(d.status, DriftStatus.OPEN)

    def test_acknowledge(self):
        d = self.svc.detect(DriftEvent(drift_type=DriftType.DATA_DRIFT))
        self.svc.acknowledge(d.drift_id)
        self.assertEqual(d.status, DriftStatus.ACKNOWLEDGED)

    def test_list(self):
        self.svc.detect(DriftEvent(drift_type=DriftType.OUTCOME_DRIFT))
        self.svc.detect(DriftEvent(drift_type=DriftType.FEATURE_DRIFT))
        self.assertEqual(len(self.svc.list()), 2)

    def test_to_dict(self):
        d = DriftEvent(drift_id="d1", drift_type=DriftType.CHANNEL_DRIFT,
                        metric="wa_messages", difference=0.3, severity="HIGH")
        dd = d.to_dict()
        self.assertEqual(dd["drift_type"], "CHANNEL_DRIFT")
        self.assertEqual(dd["difference"], 0.3)


# ── Emergency Control Tests ─────────────────────────────────────────────


class LearningEmergencyControlServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = LearningEmergencyControlService()

    def test_pause(self):
        plan = LearningRolloutPlan()
        self.svc.pause_rollout(plan)
        self.assertEqual(plan.status, "PAUSED")

    def test_stop(self):
        plan = LearningRolloutPlan()
        self.svc.stop_rollout(plan)
        self.assertEqual(plan.status, "STOPPED")

    def test_emergency_rollback(self):
        plan = LearningRolloutPlan()
        pkg = FinalKnowledgeEvolutionPackage(title="Test")
        self.svc.emergency_rollback(plan, pkg)
        self.assertEqual(plan.status, "ROLLED_BACK")
        self.assertEqual(pkg.status, PackageStatus.ROLLED_BACK)


# ── Rollback Service Tests ──────────────────────────────────────────────


class KnowledgeRollbackServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = KnowledgeRollbackService()

    def test_create_plan(self):
        rp = self.svc.create_plan(KnowledgeRollbackPlan(
            source_version="2.0", target_version="1.0"))
        self.assertIsNotNone(rp.rollback_plan_id)

    def test_execute(self):
        rp = self.svc.create_plan(KnowledgeRollbackPlan(
            source_version="2.0", target_version="1.0"))
        pkg = FinalKnowledgeEvolutionPackage(title="Test", status=PackageStatus.PUBLISHED)
        result = self.svc.execute(rp, pkg)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(pkg.status, PackageStatus.ROLLED_BACK)


# ── Post-Publication Evaluation Tests ───────────────────────────────────


class PostPublicationEvaluationServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = PostPublicationEvaluationService()

    def test_evaluate(self):
        ev = self.svc.evaluate(PostPublicationEvaluation(
            result=PostPublicationResult.SUCCESS, adoption_rate=0.85))
        self.assertIsNotNone(ev.evaluation_id)
        self.assertEqual(ev.result, PostPublicationResult.SUCCESS)

    def test_get(self):
        ev = self.svc.evaluate(PostPublicationEvaluation())
        self.assertIsNotNone(self.svc.get(ev.evaluation_id))

    def test_list(self):
        self.svc.evaluate(PostPublicationEvaluation())
        self.svc.evaluate(PostPublicationEvaluation())
        self.assertEqual(len(self.svc.list()), 2)

    def test_to_dict(self):
        ev = PostPublicationEvaluation(evaluation_id="e1", result=PostPublicationResult.FAILED)
        d = ev.to_dict()
        self.assertEqual(d["result"], "FAILED")


# ── Risk Enum Tests ─────────────────────────────────────────────────────


class RiskLevelEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(RiskLevel.LOW.value, "LOW")
        self.assertEqual(RiskLevel.CRITICAL.value, "CRITICAL")


class PackageStatusEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(PackageStatus.DRAFT.value, "DRAFT")
        self.assertEqual(PackageStatus.PUBLISHED.value, "PUBLISHED")
        self.assertEqual(PackageStatus.ROLLED_BACK.value, "ROLLED_BACK")


class RolloutStageEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(RolloutStage.ZERO_PERCENT.value, "0_PERCENT")
        self.assertEqual(RolloutStage.HUNDRED_PERCENT.value, "100_PERCENT")


class VersionStatusEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(VersionStatus.PUBLISHED.value, "PUBLISHED")
        self.assertEqual(VersionStatus.ROLLED_BACK.value, "ROLLED_BACK")


class DriftTypeEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(DriftType.DATA_DRIFT.value, "DATA_DRIFT")
        self.assertEqual(DriftType.LANGUAGE_DRIFT.value, "LANGUAGE_DRIFT")


class PostPublicationResultEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(PostPublicationResult.SUCCESS.value, "SUCCESS")
        self.assertEqual(PostPublicationResult.ROLLED_BACK.value, "ROLLED_BACK")


class GuardrailActionEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(GuardrailAction.WARN.value, "WARN")
        self.assertEqual(GuardrailAction.ROLLBACK.value, "ROLLBACK")


# ── JSON Serialization ──────────────────────────────────────────────────


class FinalSerializationTest(unittest.TestCase):
    def test_package_json(self):
        pkg = FinalKnowledgeEvolutionPackage(title="Test", risk_level=RiskLevel.MEDIUM)
        s = json.dumps(pkg.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("MEDIUM", s)

    def test_drift_json(self):
        d = DriftEvent(drift_type=DriftType.OUTCOME_DRIFT, metric="conv", difference=0.2)
        s = json.dumps(d.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("OUTCOME_DRIFT", s)

    def test_version_json(self):
        v = KnowledgeVersion(version_id="v1", component="rules", version="2.0")
        s = json.dumps(v.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("2.0", s)


if __name__ == "__main__":
    unittest.main()
