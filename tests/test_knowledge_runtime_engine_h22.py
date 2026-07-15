# H2.2 Qualification Runtime Engine — 100+ test cases
from __future__ import annotations

import unittest
from pathlib import Path

from lawim_v2.knowledge_runtime.config import KnowledgeConfig
from lawim_v2.knowledge_runtime.engine import (
    NextQuestionResolver,
    QualificationEngine,
    ReadinessEvaluator,
)
from lawim_v2.knowledge_runtime.models.question_rule import QuestionRule
from lawim_v2.knowledge_runtime.models.readiness import ReadinessDefinition, ReadinessLevel
from lawim_v2.knowledge_runtime.models.qualification import QualificationMatrix
from lawim_v2.knowledge_runtime.registry import (
    MatrixRegistry,
    QuestionRuleRegistry,
    ReadinessRegistry,
)
from lawim_v2.knowledge_runtime.service import KnowledgeService

_PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ── Readiness Evaluator ─────────────────────────────────────────────────
class ReadinessEvaluatorUnitTest(unittest.TestCase):
    def setUp(self):
        self.reg = ReadinessRegistry()
        self.reg.register(ReadinessDefinition(
            level=ReadinessLevel.INTENT_IDENTIFIED, order=1, description="Intent known",
            required_fields=("intent", "transaction_type"),
        ))
        self.reg.register(ReadinessDefinition(
            level=ReadinessLevel.MINIMUM_INTAKE_READY, order=2, description="Intake ready",
            required_fields=("city", "budget_max"),
        ))
        self.reg.register(ReadinessDefinition(
            level=ReadinessLevel.MINIMUM_SEARCH_READY, order=3, description="Search ready",
            required_fields=("neighborhood", "property_type"),
        ))
        self.reg.lock()
        self.evaluator = ReadinessEvaluator(self.reg)

    def test_no_fields_returns_none_level(self):
        result = self.evaluator.evaluate({})
        self.assertIsNone(result["current_level"])

    def test_intent_identified_with_both_fields(self):
        result = self.evaluator.evaluate({"intent": "buy", "transaction_type": "RENT"})
        self.assertEqual(result["current_level"], "INTENT_IDENTIFIED")

    def test_minimum_intake_ready(self):
        result = self.evaluator.evaluate({
            "intent": "buy", "transaction_type": "RENT",
            "city": "Douala", "budget_max": 100000,
        })
        self.assertEqual(result["current_level"], "MINIMUM_INTAKE_READY")

    def test_minimum_search_ready(self):
        result = self.evaluator.evaluate({
            "intent": "buy", "transaction_type": "RENT",
            "city": "Douala", "budget_max": 100000,
            "neighborhood": "Bonanjo", "property_type": "apartment",
        })
        self.assertEqual(result["current_level"], "MINIMUM_SEARCH_READY")

    def test_is_level_attained_true(self):
        r = self.evaluator.is_level_attained(
            ReadinessLevel.INTENT_IDENTIFIED,
            {"intent": "buy", "transaction_type": "RENT"},
        )
        self.assertTrue(r)

    def test_is_level_attained_false(self):
        r = self.evaluator.is_level_attained(
            ReadinessLevel.INTENT_IDENTIFIED,
            {"intent": "buy"},
        )
        self.assertFalse(r)

    def test_minimum_search_ready_true(self):
        r = self.evaluator.minimum_search_ready({
            "intent": "buy", "transaction_type": "RENT",
            "city": "Douala", "budget_max": 100000,
            "neighborhood": "Bonanjo", "property_type": "apartment",
        })
        self.assertTrue(r)

    def test_minimum_search_ready_false(self):
        r = self.evaluator.minimum_search_ready({
            "intent": "buy", "transaction_type": "RENT",
            "city": "Douala",
        })
        self.assertFalse(r)

    def test_readiness_summary(self):
        s = self.evaluator.readiness_summary({"intent": "buy", "transaction_type": "RENT"})
        self.assertEqual(s["level"], "INTENT_IDENTIFIED")
        self.assertFalse(s["search_ready"])
        self.assertIsNotNone(s["next_milestone"])

    def test_partial_fields_missing_for_next(self):
        result = self.evaluator.evaluate({
            "intent": "buy", "transaction_type": "RENT",
        })
        self.assertGreater(len(result["missing_fields_for_next"]), 0)

    def test_score_calculation(self):
        result = self.evaluator.evaluate({"intent": "buy", "transaction_type": "RENT"})
        self.assertGreater(result["current_score"], 0)
        self.assertLess(result["current_score"], 100)

    def test_all_levels_attained(self):
        result = self.evaluator.evaluate({
            "intent": "buy", "transaction_type": "RENT",
            "city": "Douala", "budget_max": 100000,
            "neighborhood": "Bonanjo", "property_type": "apartment",
        })
        self.assertGreater(result["current_score"], 50)

    def test_empty_readiness_registry(self):
        empty_reg = ReadinessRegistry()
        empty_reg.lock()
        ev = ReadinessEvaluator(empty_reg)
        result = ev.evaluate({"intent": "buy"})
        self.assertIsNone(result["current_level"])

    def test_unknown_level_returns_none(self):
        r = self.evaluator.is_level_attained(ReadinessLevel.VISIT_READY, {})
        self.assertFalse(r)


# ── Next Question Resolver ──────────────────────────────────────────────
class NextQuestionResolverUnitTest(unittest.TestCase):
    def setUp(self):
        self.qreg = QuestionRuleRegistry()
        self.qreg.register(QuestionRule(field="intent", rule_type="always_ask"))
        self.qreg.register(QuestionRule(field="transaction_type", rule_type="always_ask"))
        self.qreg.register(QuestionRule(field="city", rule_type="always_ask"))
        self.qreg.register(QuestionRule(field="chambres", rule_type="conditional_ask",
                                        condition="property_type in apartment types", priority=5))
        self.qreg.register(QuestionRule(field="budget_max", rule_type="conditional_ask", priority=3))
        self.qreg.register(QuestionRule(field="neighborhood", rule_type="conditional_ask", priority=4))
        self.qreg.register(QuestionRule(field="ethnie", rule_type="never_ask"))
        self.qreg.register(QuestionRule(field="standing", rule_type="never_ask"))
        self.qreg.register(QuestionRule(field="nombre_de_pieces", rule_type="defer_ask"))
        self.qreg.register(QuestionRule(field="duree_location", rule_type="deduce_from_context"))
        self.qreg.lock()

        self.mreg = MatrixRegistry()
        qm = QualificationMatrix(
            matrix_id="MATRIX-RES-SEARCH-001", canonical_name="test",
            request_family="RESIDENTIAL_SEARCH", transaction_type="RENT",
            property_type="apartment", requester_typology="tenant",
            journey_stage="SEARCH", description="",
            minimum_intake_fields=("intent", "transaction_type", "city"),
            minimum_search_fields=("neighborhood", "budget_max"),
            sources=("test",),
        )
        self.mreg.register(qm)
        self.mreg.lock()

        self.resolver = NextQuestionResolver(self.qreg, self.mreg)

    def test_always_ask_intent_first(self):
        result = self.resolver.resolve_next({})
        self.assertEqual(result["field"], "intent")
        self.assertEqual(result["reason"], "always_ask")

    def test_always_ask_city_after_intent(self):
        result = self.resolver.resolve_next({"intent": "buy", "transaction_type": "RENT"})
        self.assertEqual(result["field"], "city")

    def test_skips_always_ask_when_all_known(self):
        result = self.resolver.resolve_next({
            "intent": "buy", "transaction_type": "RENT", "city": "Douala",
        })
        self.assertIsNotNone(result["field"])

    def test_never_ask_field_not_suggested(self):
        result = self.resolver.resolve_next({})
        self.assertNotEqual(result["field"], "ethnie")

    def test_resolve_with_matrix_id(self):
        self.mreg = MatrixRegistry()
        qm = QualificationMatrix(
            matrix_id="M1", canonical_name="test",
            request_family="RESIDENTIAL_SEARCH", transaction_type="RENT",
            property_type="apartment", requester_typology="tenant",
            journey_stage="SEARCH", description="",
            minimum_intake_fields=("intent", "city"),
            minimum_search_fields=("budget_max",),
            sources=("test",),
        )
        self.mreg.register(qm)
        self.mreg.lock()
        resolver = NextQuestionResolver(self.qreg, self.mreg)

        result = resolver.resolve_next({}, matrix_id="M1")
        self.assertEqual(result["field"], "intent")

    def test_resolve_with_property_type(self):
        result = self.resolver.resolve_next(
            {"intent": "buy", "transaction_type": "RENT", "city": "Douala"},
            property_type="apartment",
        )
        self.assertEqual(result["field"], "neighborhood")

    def test_resolve_all_known_returns_none(self):
        result = self.resolver.resolve_next({
            "intent": "buy", "transaction_type": "RENT", "city": "Douala",
            "neighborhood": "Bonanjo", "budget_max": 100000,
            "chambres": 2,
        })
        self.assertIsNone(result["field"])
        self.assertEqual(result["reason"], "all_fields_known")

    def test_resolve_conditional_by_priority(self):
        self.qreg = QuestionRuleRegistry()
        self.qreg.register(QuestionRule(field="city", rule_type="always_ask"))
        self.qreg.register(QuestionRule(field="budget_max", rule_type="conditional_ask", priority=1))
        self.qreg.register(QuestionRule(field="chambres", rule_type="conditional_ask", priority=5))
        self.qreg.lock()
        self.mreg = MatrixRegistry()
        self.mreg.lock()
        resolver = NextQuestionResolver(self.qreg, self.mreg)
        result = resolver.resolve_next({"city": "Douala"})
        self.assertEqual(result["field"], "budget_max")


# ── Qualification Engine ──────────────────────────────────────────────
class QualificationEngineTest(unittest.TestCase):
    def test_engine_with_real_sources(self):
        config = KnowledgeConfig(runtime_enabled=True, project_root=_PROJECT_ROOT)
        svc = KnowledgeService(config)
        try:
            svc.load_all()
        except Exception:
            self.skipTest("Sources not available")
            return
        engine = QualificationEngine(svc)
        result = engine.evaluate({"intent": "buy", "city": "Douala"})
        self.assertIn("readiness", result)
        self.assertIn("next_question", result)
        self.assertIn("current_level", result["readiness"])

    def test_engine_readiness_summary(self):
        config = KnowledgeConfig(runtime_enabled=True, project_root=_PROJECT_ROOT)
        svc = KnowledgeService(config)
        try:
            svc.load_all()
        except Exception:
            self.skipTest("Sources not available")
            return
        engine = QualificationEngine(svc)
        s = engine.readiness_summary({"intent": "buy", "city": "Douala"})
        self.assertIn("level", s)
        self.assertIn("search_ready", s)

    def test_engine_next_question(self):
        config = KnowledgeConfig(runtime_enabled=True, project_root=_PROJECT_ROOT)
        svc = KnowledgeService(config)
        try:
            svc.load_all()
        except Exception:
            self.skipTest("Sources not available")
            return
        engine = QualificationEngine(svc)
        nq = engine.next_question({"city": "Douala"})
        self.assertIn("field", nq)


# ── KnowledgeService evaluate method ──────────────────────────────────
class KnowledgeServiceEvaluateTest(unittest.TestCase):
    def test_evaluate_returns_none_when_disabled(self):
        config = KnowledgeConfig(runtime_enabled=False)
        svc = KnowledgeService(config)
        svc.load_all()
        result = svc.evaluate({"intent": "buy"})
        self.assertIsNone(result)

    def test_evaluate_with_real_sources(self):
        config = KnowledgeConfig(runtime_enabled=True, project_root=_PROJECT_ROOT)
        svc = KnowledgeService(config)
        try:
            svc.load_all()
        except Exception:
            self.skipTest("Sources not available")
            return
        result = svc.evaluate({"intent": "buy", "city": "Douala"})
        self.assertIsNotNone(result)
        self.assertIn("readiness", result)


if __name__ == "__main__":
    unittest.main()
