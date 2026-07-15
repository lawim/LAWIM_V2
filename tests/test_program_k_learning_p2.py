# Program K Part 2 — Learning Datasets, Analysis and Proposals Tests
from __future__ import annotations

import json
import unittest

from lawim_v2.program_k.learning_analysis import (
    EvolutionPackageService,
    ExperimentEvaluationService,
    LearningAnalysisEngine,
    LearningExperimentService,
    LearningHypothesisService,
    LearningProposalEngine,
    VersionService,
)
from lawim_v2.program_k.learning_config_p2 import LearningConfigP2
from lawim_v2.program_k.learning_datasets import (
    LearningDataQualityService,
    LearningDatasetBuilder,
    LearningDatasetRegistry,
    FeatureCatalog,
    feature_catalog,
)
from lawim_v2.program_k.learning_models import (
    LearningEvent,
    LearningEventSource,
    LearningEventType,
    OutcomeResult,
    OutcomeStatus,
)
from lawim_v2.program_k.learning_models_p2 import (
    DatasetCategory,
    DatasetStatus,
    ExperimentResult,
    ExperimentStatus,
    FeatureDefinition,
    HypothesisStatus,
    KnowledgeEvolutionPackage,
    LearningDataset,
    LearningExperiment,
    LearningHypothesis,
    LearningProposal,
    LearningReview,
    ProposalStatus,
    ProposalType,
    ReviewDecision,
    VersionRecord,
)

# ── Dataset Registry Tests ────────────────────────────────────────────────


class LearningDatasetRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = LearningDatasetRegistry()

    def test_create(self):
        ds = LearningDataset(name="Test", category=DatasetCategory.CONVERSATION_QUALITY)
        created = self.reg.create(ds)
        self.assertIsNotNone(created.dataset_id)
        self.assertEqual(created.status, DatasetStatus.DRAFT)

    def test_get(self):
        ds = self.reg.create(LearningDataset(name="Test"))
        found = self.reg.get(ds.dataset_id)
        self.assertIsNotNone(found)

    def test_list_empty(self):
        self.assertEqual(len(self.reg.list()), 0)

    def test_list_with_status(self):
        self.reg.create(LearningDataset(name="A", status=DatasetStatus.DRAFT))
        self.reg.create(LearningDataset(name="B", status=DatasetStatus.READY))
        ready = self.reg.list(DatasetStatus.READY)
        self.assertEqual(len(ready), 1)

    def test_count(self):
        self.reg.create(LearningDataset(name="A"))
        self.reg.create(LearningDataset(name="B"))
        self.assertEqual(self.reg.count(), 2)


# ── Dataset Builder Tests ────────────────────────────────────────────────


class LearningDatasetBuilderTest(unittest.TestCase):
    def setUp(self):
        self.builder = LearningDatasetBuilder()

    def test_build_empty_events(self):
        ds = LearningDataset(name="Test", category=DatasetCategory.CONVERSATION_QUALITY)
        ds = self.builder.build_dataset(ds, [])
        self.assertEqual(ds.status, DatasetStatus.READY)
        self.assertEqual(ds.row_count, 0)

    def test_build_with_events(self):
        events = [LearningEvent(event_type=LearningEventType.J_CONVERSATION_STARTED,
                                 source=LearningEventSource.PROGRAM_J, actor_id="a1")]
        ds = LearningDataset(name="Test", category=DatasetCategory.CONVERSATION_QUALITY)
        ds = self.builder.build_dataset(ds, events)
        self.assertEqual(ds.row_count, 1)
        self.assertTrue(len(ds.checksum) > 0)

    def test_validate_empty(self):
        ds = LearningDataset(name="Empty", row_count=0)
        issues = self.builder.validate_dataset(ds)
        self.assertGreaterEqual(len(issues), 1)

    def test_validate_non_empty(self):
        ds = LearningDataset(name="OK", row_count=100)
        issues = self.builder.validate_dataset(ds)
        self.assertEqual(len(issues), 0)

    def test_reproducible_checksum(self):
        e1 = [LearningEvent(event_type=LearningEventType.H_QUALIFICATION_STARTED)]
        e2 = [LearningEvent(event_type=LearningEventType.H_QUALIFICATION_STARTED)]
        ds1 = LearningDataset(name="A")
        ds2 = LearningDataset(name="B")
        ds1 = self.builder.build_dataset(ds1, e1)
        ds2 = self.builder.build_dataset(ds2, e2)
        self.assertEqual(ds1.checksum, ds2.checksum)


# ── Feature Catalog Tests ────────────────────────────────────────────────


class FeatureCatalogTest(unittest.TestCase):
    def test_non_empty(self):
        self.assertGreater(feature_catalog.count(), 0)

    def test_get_existing(self):
        f = feature_catalog.get("CHANNEL_CODE")
        self.assertIsNotNone(f)
        self.assertEqual(f.feature_code, "CHANNEL_CODE")

    def test_get_nonexistent(self):
        f = feature_catalog.get("INVALID")
        self.assertIsNone(f)

    def test_unique_codes(self):
        codes = [f.feature_code for f in feature_catalog.list_all()]
        self.assertEqual(len(codes), len(set(codes)))

    def test_all_have_calculation(self):
        for f in feature_catalog.list_all():
            self.assertTrue(f.calculation, f"{f.feature_code} missing calculation")

    def test_all_have_source(self):
        for f in feature_catalog.list_all():
            self.assertTrue(f.source, f"{f.feature_code} missing source")

    def test_to_dict(self):
        f = feature_catalog.get("CHANNEL_CODE")
        d = f.to_dict()
        self.assertEqual(d["feature_code"], "CHANNEL_CODE")

    def test_json_serializable(self):
        dl = feature_catalog.to_dict_list()
        s = json.dumps(dl, ensure_ascii=False, sort_keys=True)
        self.assertGreater(len(s), 100)


# ── Data Quality Tests ────────────────────────────────────────────────────


class LearningDataQualityTest(unittest.TestCase):
    def setUp(self):
        self.svc = LearningDataQualityService()

    def test_empty_events(self):
        ds = LearningDataset(name="Test")
        issues = self.svc.check_dataset(ds, [])
        self.assertGreaterEqual(len(issues), 1)

    def test_orphan_events(self):
        events = [LearningEvent(event_type=LearningEventType.J_CONVERSATION_STARTED)]
        ds = LearningDataset(name="Test")
        issues = self.svc.check_dataset(ds, events)
        has_orphan = any(i["type"] == "ORPHAN_EVENT" for i in issues)
        self.assertTrue(has_orphan)

    def test_leakage_detection(self):
        events = [
            LearningEvent(event_type=LearningEventType.J_CONVERSATION_STARTED,
                           payload={"conversion_success": True}),
        ]
        issues = self.svc.check_leakage(events)
        self.assertGreaterEqual(len(issues), 1)

    def test_no_leakage(self):
        events = [LearningEvent(event_type=LearningEventType.J_CONVERSATION_STARTED)]
        issues = self.svc.check_leakage(events)
        self.assertEqual(len(issues), 0)


# ── Analysis Engine Tests ─────────────────────────────────────────────────


class LearningAnalysisEngineTest(unittest.TestCase):
    def setUp(self):
        self.engine = LearningAnalysisEngine()
        self.outcomes = [
            OutcomeResult(outcome_id="o1", outcome_type="qualification",
                           status=OutcomeStatus.SUCCESS, monetary_value=0),
            OutcomeResult(outcome_id="o2", outcome_type="qualification",
                           status=OutcomeStatus.FAILURE, monetary_value=0),
            OutcomeResult(outcome_id="o3", outcome_type="matching",
                           status=OutcomeStatus.SUCCESS, monetary_value=100000),
            OutcomeResult(outcome_id="o4", outcome_type="matching",
                           status=OutcomeStatus.SUCCESS, monetary_value=200000),
        ]

    def test_analyze_outcomes(self):
        results = self.engine.analyze_outcomes(self.outcomes)
        self.assertGreaterEqual(len(results), 2)

    def test_analyze_trend(self):
        trend = self.engine.analyze_trend(self.outcomes)
        self.assertIn("trend", trend)
        self.assertIn("success_rate", trend)

    def test_empty_trend(self):
        trend = self.engine.analyze_trend([])
        self.assertEqual(trend["trend"], "NO_DATA")

    def test_cohort_analysis(self):
        cohorts = self.engine.cohort_analysis(self.outcomes, "outcome_type")
        self.assertGreaterEqual(len(cohorts), 2)

    def test_cohort_sorted(self):
        cohorts = self.engine.cohort_analysis(self.outcomes, "outcome_type")
        for i in range(len(cohorts) - 1):
            self.assertGreaterEqual(cohorts[i]["success_rate_pct"],
                                     cohorts[i + 1]["success_rate_pct"])


# ── Hypothesis Tests ──────────────────────────────────────────────────────


class LearningHypothesisServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = LearningHypothesisService()

    def test_create(self):
        h = self.svc.create(LearningHypothesis(title="Test hypothesis"))
        self.assertIsNotNone(h.hypothesis_id)
        self.assertEqual(h.status, HypothesisStatus.DRAFT)

    def test_get(self):
        h = self.svc.create(LearningHypothesis(title="Test"))
        found = self.svc.get(h.hypothesis_id)
        self.assertIsNotNone(found)

    def test_list(self):
        self.svc.create(LearningHypothesis(title="A"))
        self.svc.create(LearningHypothesis(title="B"))
        self.assertEqual(len(self.svc.list()), 2)

    def test_update_status(self):
        h = self.svc.create(LearningHypothesis(title="Test"))
        self.svc.update_status(h.hypothesis_id, HypothesisStatus.PROPOSED)
        self.assertEqual(h.status, HypothesisStatus.PROPOSED)

    def test_to_dict(self):
        h = self.svc.create(LearningHypothesis(title="Test", target_metric="CONVERSION_RATE"))
        d = h.to_dict()
        self.assertEqual(d["target_metric"], "CONVERSION_RATE")


# ── Proposal Engine Tests ─────────────────────────────────────────────────


class LearningProposalEngineTest(unittest.TestCase):
    def setUp(self):
        self.engine = LearningProposalEngine()

    def test_create(self):
        p = self.engine.create(LearningProposal(proposal_type=ProposalType.MODIFY_THRESHOLD))
        self.assertIsNotNone(p.proposal_id)
        self.assertEqual(p.status, ProposalStatus.DRAFT)

    def test_submit_for_review(self):
        p = self.engine.create(LearningProposal())
        self.engine.submit_for_review(p.proposal_id)
        self.assertEqual(p.status, ProposalStatus.READY_FOR_REVIEW)

    def test_approve(self):
        p = self.engine.create(LearningProposal())
        self.engine.submit_for_review(p.proposal_id)
        self.engine.review(p.proposal_id, "reviewer1", ReviewDecision.APPROVE)
        self.assertEqual(p.status, ProposalStatus.APPROVED)

    def test_reject(self):
        p = self.engine.create(LearningProposal())
        self.engine.submit_for_review(p.proposal_id)
        self.engine.review(p.proposal_id, "reviewer1", ReviewDecision.REJECT)
        self.assertEqual(p.status, ProposalStatus.REJECTED)

    def test_approve_for_experiment(self):
        p = self.engine.create(LearningProposal())
        self.engine.submit_for_review(p.proposal_id)
        self.engine.review(p.proposal_id, "reviewer1", ReviewDecision.APPROVE_FOR_EXPERIMENT)
        self.assertEqual(p.status, ProposalStatus.EXPERIMENTAL)

    def test_get_reviews(self):
        p = self.engine.create(LearningProposal())
        self.engine.submit_for_review(p.proposal_id)
        self.engine.review(p.proposal_id, "r1", ReviewDecision.APPROVE)
        reviews = self.engine.get_reviews(p.proposal_id)
        self.assertEqual(len(reviews), 1)

    def test_get_nonexistent(self):
        p = self.engine.get("nonexistent")
        self.assertIsNone(p)

    def test_review_nonexistent(self):
        r = self.engine.review("nonexistent", "r1", ReviewDecision.APPROVE)
        self.assertIsNone(r)

    def test_to_dict(self):
        p = self.engine.create(LearningProposal(
            proposal_type=ProposalType.ADAPT_CHANNEL,
            target_component="wizard",
            sample_size=1000, confidence=0.85,
        ))
        d = p.to_dict()
        self.assertEqual(d["proposal_type"], "ADAPT_CHANNEL")
        self.assertEqual(d["sample_size"], 1000)


# ── Experiment Tests ──────────────────────────────────────────────────────


class LearningExperimentServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = LearningExperimentService()

    def test_create(self):
        e = self.svc.create(LearningExperiment(name="A/B Test"))
        self.assertIsNotNone(e.experiment_id)
        self.assertEqual(e.status, ExperimentStatus.DRAFT)

    def test_start(self):
        e = self.svc.create(LearningExperiment(name="Test"))
        self.svc.start(e.experiment_id)
        self.assertEqual(e.status, ExperimentStatus.RUNNING)

    def test_stop(self):
        e = self.svc.create(LearningExperiment(name="Test"))
        self.svc.start(e.experiment_id)
        self.svc.stop(e.experiment_id)
        self.assertEqual(e.status, ExperimentStatus.STOPPED)

    def test_to_dict(self):
        e = self.svc.create(LearningExperiment(name="Test"))
        d = e.to_dict()
        self.assertEqual(d["name"], "Test")


class ExperimentEvaluationServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = ExperimentEvaluationService()

    def test_positive_result(self):
        exp = LearningExperiment(name="Test")
        control = [OutcomeResult(status=OutcomeStatus.SUCCESS) for _ in range(10)]
        treatment = [OutcomeResult(status=OutcomeStatus.SUCCESS) for _ in range(10)]
        # Make treatment better by having failures in control
        control = [OutcomeResult(status=OutcomeStatus.SUCCESS) for _ in range(5)] + \
                  [OutcomeResult(status=OutcomeStatus.FAILURE) for _ in range(5)]
        treatment = [OutcomeResult(status=OutcomeStatus.SUCCESS) for _ in range(10)]
        result = self.svc.evaluate(exp, control, treatment)
        self.assertEqual(result.status, ExperimentStatus.COMPLETED)
        self.assertIn(result.result, (ExperimentResult.POSITIVE, ExperimentResult.INCONCLUSIVE))

    def test_inconclusive_small(self):
        exp = LearningExperiment(name="Small")
        result = self.svc.evaluate(exp, [OutcomeResult()], [OutcomeResult()])
        self.assertEqual(result.result, ExperimentResult.INCONCLUSIVE)

    def test_negative_result(self):
        exp = LearningExperiment(name="Test")
        control = [OutcomeResult(status=OutcomeStatus.SUCCESS) for _ in range(10)]
        treatment = [OutcomeResult(status=OutcomeStatus.FAILURE) for _ in range(10)]
        result = self.svc.evaluate(exp, control, treatment)
        self.assertEqual(result.status, ExperimentStatus.COMPLETED)
        self.assertEqual(result.result, ExperimentResult.NEGATIVE)


# ── Evolution Package Tests ───────────────────────────────────────────────


class EvolutionPackageServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = EvolutionPackageService()

    def test_create(self):
        pkg = self.svc.create(KnowledgeEvolutionPackage())
        self.assertIsNotNone(pkg.package_id)
        self.assertEqual(pkg.status, "DRAFT")

    def test_get(self):
        pkg = self.svc.create(KnowledgeEvolutionPackage())
        found = self.svc.get(pkg.package_id)
        self.assertIsNotNone(found)

    def test_to_dict(self):
        pkg = self.svc.create(KnowledgeEvolutionPackage(
            proposal_ids=["p1", "p2"], migration_required=True))
        d = pkg.to_dict()
        self.assertEqual(d["proposal_count"], 2)
        self.assertTrue(d["migration_required"])


# ── Version Service Tests ─────────────────────────────────────────────────


class VersionServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = VersionService()

    def test_register(self):
        v = self.svc.register("dataset", "d1", "1.0")
        self.assertIsNotNone(v.version_id)
        self.assertEqual(v.version, "1.0")

    def test_get_history(self):
        self.svc.register("dataset", "d1", "1.0")
        self.svc.register("dataset", "d1", "2.0", parent="1.0")
        history = self.svc.get_history("dataset", "d1")
        self.assertEqual(len(history), 2)

    def test_to_dict(self):
        v = self.svc.register("proposal", "p1", "1.0", created_by="admin")
        d = v.to_dict()
        self.assertEqual(d["component_type"], "proposal")


# ── Config Tests ──────────────────────────────────────────────────────────


class LearningConfigP2Test(unittest.TestCase):
    def test_default_disabled(self):
        cfg = LearningConfigP2()
        self.assertFalse(cfg.learning_dataset_builder_enabled)
        self.assertFalse(cfg.learning_analysis_enabled)
        self.assertFalse(cfg.learning_proposal_engine_enabled)
        self.assertFalse(cfg.learning_experiments_enabled)
        self.assertFalse(cfg.knowledge_evolution_packages_enabled)

    def test_enable_one(self):
        cfg = LearningConfigP2(learning_analysis_enabled=True)
        self.assertTrue(cfg.learning_analysis_enabled)

    def test_enable_all(self):
        cfg = LearningConfigP2(**{f.name: True for f in LearningConfigP2.__dataclass_fields__.values()})
        self.assertTrue(cfg.learning_dataset_builder_enabled)


# ── Dataset Category Enum Tests ────────────────────────────────────────────


class DatasetCategoryEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(DatasetCategory.CONVERSATION_QUALITY.value, "CONVERSATION_QUALITY")
        self.assertEqual(DatasetCategory.MATCHING_EFFECTIVENESS.value, "MATCHING_EFFECTIVENESS")
        self.assertEqual(DatasetCategory.CUSTOMER_SATISFACTION.value, "CUSTOMER_SATISFACTION")

    def test_unique(self):
        vals = [c.value for c in DatasetCategory]
        self.assertEqual(len(vals), len(set(vals)))


# ── Proposal Type Enum Tests ──────────────────────────────────────────────


class ProposalTypeEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(ProposalType.MODIFY_THRESHOLD.value, "MODIFY_THRESHOLD")
        self.assertEqual(ProposalType.ADAPT_CHANNEL.value, "ADAPT_CHANNEL")

    def test_unique(self):
        vals = [p.value for p in ProposalType]
        self.assertEqual(len(vals), len(set(vals)))


# ── Review Decision Enum Tests ────────────────────────────────────────────


class ReviewDecisionEnumTest(unittest.TestCase):
    def test_approve(self):
        self.assertEqual(ReviewDecision.APPROVE.value, "APPROVE")

    def test_reject(self):
        self.assertEqual(ReviewDecision.REJECT.value, "REJECT")


# ── Serialization Tests ───────────────────────────────────────────────────


class SerializationTest(unittest.TestCase):
    def test_dataset_json(self):
        ds = LearningDataset(name="Test", row_count=100, checksum="abc123")
        s = json.dumps(ds.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("abc123", s)

    def test_experiment_json(self):
        e = LearningExperiment(name="Test", status=ExperimentStatus.RUNNING)
        s = json.dumps(e.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("RUNNING", s)


if __name__ == "__main__":
    unittest.main()
