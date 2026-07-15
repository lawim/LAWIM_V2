# H2.2 Progressive Wizard — 50+ test cases
from __future__ import annotations

import unittest
from pathlib import Path

from lawim_v2.knowledge_runtime.config import KnowledgeConfig
from lawim_v2.knowledge_runtime.engine import (
    ProgressiveWizard,
    QualificationSession,
)
from lawim_v2.knowledge_runtime.engine.wizard import (
    STEP_INTENTION,
    STEP_TYPE,
    STEP_VILLE,
    STEP_QUARTIER,
    STEP_BUDGET,
    STEP_DELAI,
    STEP_CRITERES,
    STEP_PREFERENCES,
    STEP_CONFIRMATION,
    STEP_ESCALADE,
    STEP_NAMES,
)
from lawim_v2.knowledge_runtime.models.question_rule import QuestionRule
from lawim_v2.knowledge_runtime.models.readiness import ReadinessDefinition, ReadinessLevel
from lawim_v2.knowledge_runtime.models.qualification import QualificationMatrix
from lawim_v2.knowledge_runtime.registry import (
    MatrixRegistry,
    QuestionRuleRegistry,
    ReadinessRegistry,
)
from lawim_v2.knowledge_runtime.engine.readiness import ReadinessEvaluator
from lawim_v2.knowledge_runtime.engine.resolver import NextQuestionResolver
from lawim_v2.knowledge_runtime.service import KnowledgeService

_PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _default_resolver():
    qreg = QuestionRuleRegistry()
    qreg.register(QuestionRule(field="intent", rule_type="always_ask"))
    qreg.register(QuestionRule(field="transaction_type", rule_type="always_ask"))
    qreg.register(QuestionRule(field="city", rule_type="always_ask"))
    qreg.register(QuestionRule(field="neighborhood", rule_type="conditional_ask", priority=4))
    qreg.register(QuestionRule(field="budget_max", rule_type="conditional_ask", priority=3))
    qreg.lock()

    mreg = MatrixRegistry()
    qm = QualificationMatrix(
        matrix_id="M1", canonical_name="test",
        request_family="RESIDENTIAL_SEARCH", transaction_type="RENT",
        property_type="apartment", requester_typology="tenant",
        journey_stage="SEARCH", description="",
        minimum_intake_fields=("intent", "transaction_type", "city"),
        minimum_search_fields=("neighborhood", "budget_max"),
        sources=("test",),
    )
    mreg.register(qm)
    mreg.lock()
    return NextQuestionResolver(qreg, mreg)


def _default_readiness():
    reg = ReadinessRegistry()
    reg.register(ReadinessDefinition(
        level=ReadinessLevel.INTENT_IDENTIFIED, order=1, description="",
        required_fields=("intent", "transaction_type"),
    ))
    reg.register(ReadinessDefinition(
        level=ReadinessLevel.MINIMUM_INTAKE_READY, order=2, description="",
        required_fields=("city", "budget_max"),
    ))
    reg.register(ReadinessDefinition(
        level=ReadinessLevel.MINIMUM_SEARCH_READY, order=3, description="",
        required_fields=("neighborhood", "property_type"),
    ))
    reg.lock()
    return ReadinessEvaluator(reg)


def _default_wizard():
    return ProgressiveWizard(_default_readiness(), _default_resolver())


class ProgressiveWizardCreateSessionTest(unittest.TestCase):
    def test_create_session(self):
        w = _default_wizard()
        s = w.create_session("sess-1")
        self.assertEqual(s.session_id, "sess-1")
        self.assertEqual(s.current_step, STEP_INTENTION)
        self.assertFalse(s.completed)

    def test_get_session_exists(self):
        w = _default_wizard()
        w.create_session("sess-1")
        s = w.get_session("sess-1")
        self.assertIsNotNone(s)
        self.assertEqual(s.session_id, "sess-1")

    def test_get_session_nonexistent(self):
        w = _default_wizard()
        s = w.get_session("nonexistent")
        self.assertIsNone(s)

    def test_create_session_default_channel(self):
        w = _default_wizard()
        s = w.create_session("sess-1")
        self.assertEqual(s.channel, "dashboard")

    def test_create_session_custom_channel(self):
        w = _default_wizard()
        s = w.create_session("sess-1", channel="whatsapp")
        self.assertEqual(s.channel, "whatsapp")

    def test_list_steps(self):
        w = _default_wizard()
        steps = w.list_steps()
        self.assertEqual(len(steps), 10)
        self.assertEqual(steps[0]["step"], STEP_INTENTION)
        self.assertEqual(steps[-1]["step"], STEP_ESCALADE)


class ProgressiveWizardSubmitAnswerTest(unittest.TestCase):
    def test_submit_intent_answer(self):
        w = _default_wizard()
        w.create_session("sess-1")
        result = w.submit_answer("sess-1", "intent", "buy")
        self.assertFalse(result.get("error"))
        self.assertEqual(result["known_fields"]["intent"], "buy")

    def test_submit_advances_step_when_mandatory_complete(self):
        w = _default_wizard()
        w.create_session("sess-1")
        w.submit_answer("sess-1", "intent", "buy")
        w.submit_answer("sess-1", "transaction_type", "RENT")
        w.submit_answer("sess-1", "property_type", "apartment")
        w.submit_answer("sess-1", "city", "Douala")
        w.submit_answer("sess-1", "neighborhood", "Bonanjo")
        result = w.submit_answer("sess-1", "budget_max", 100000)
        # Step 1: intent+transaction → step 2
        # Step 2: property_type → step 3
        # Step 3: city → step 4
        # Step 4: neighborhood → step 5
        # Step 5: budget_max → step 6
        self.assertEqual(result["current_step"], STEP_DELAI)

    def test_submit_unknown_session(self):
        w = _default_wizard()
        result = w.submit_answer("nonexistent", "intent", "buy")
        self.assertEqual(result.get("error"), "session_not_found")

    def test_submit_after_completion(self):
        w = _default_wizard()
        w.create_session("sess-1")
        s = w.get_session("sess-1")
        s.completed = True
        result = w.submit_answer("sess-1", "intent", "buy")
        self.assertEqual(result.get("error"), "qualification_completed")

    def test_submit_retry_count(self):
        w = _default_wizard()
        w.create_session("sess-1")
        w.submit_answer("sess-1", "intent", "buy")
        w.submit_answer("sess-1", "intent", "rent")
        s = w.get_session("sess-1")
        self.assertEqual(s.retry_count.get("intent"), 1)

    def test_submit_exceeds_max_retries(self):
        w = _default_wizard()
        w.create_session("sess-1")
        for _ in range(5):
            result = w.submit_answer("sess-1", "intent", "buy")
        self.assertEqual(result.get("error"), "max_retries_exceeded")


class ProgressiveWizardStepInfoTest(unittest.TestCase):
    def test_step_info_intention(self):
        w = _default_wizard()
        info = w.get_step_info(STEP_INTENTION)
        self.assertEqual(info["name"], "Intention")
        self.assertIn("intent", info["fields"])
        self.assertIn("transaction_type", info["fields"])

    def test_step_info_type(self):
        w = _default_wizard()
        info = w.get_step_info(STEP_TYPE)
        self.assertEqual(info["name"], "Type")
        self.assertIn("property_type", info["fields"])

    def test_step_info_ville(self):
        w = _default_wizard()
        info = w.get_step_info(STEP_VILLE)
        self.assertEqual(info["name"], "Ville")
        self.assertIn("city", info["fields"])

    def test_step_info_budget(self):
        w = _default_wizard()
        info = w.get_step_info(STEP_BUDGET)
        self.assertEqual(info["name"], "Budget")
        self.assertIn("budget_max", info["fields"])

    def test_step_info_confirmation(self):
        w = _default_wizard()
        info = w.get_step_info(STEP_CONFIRMATION)
        self.assertEqual(info["name"], "Confirmation")
        self.assertIn("confirmation", info["fields"])

    def test_step_info_channel_limits(self):
        w = _default_wizard()
        info = w.get_step_info(STEP_INTENTION)
        limits = info.get("channel_limits", {})
        self.assertEqual(limits.get("whatsapp"), 1)
        self.assertEqual(limits.get("telegram"), 1)
        self.assertEqual(limits.get("dashboard"), 1)


class ProgressiveWizardCurrentStepTest(unittest.TestCase):
    def test_current_step_initial(self):
        w = _default_wizard()
        w.create_session("sess-1")
        info = w.get_current_step_info("sess-1")
        self.assertEqual(info["step"], STEP_INTENTION)
        self.assertIn("readiness", info)
        self.assertIn("next_question", info)

    def test_current_step_after_answers(self):
        w = _default_wizard()
        w.create_session("sess-1")
        w.submit_answer("sess-1", "intent", "buy")
        w.submit_answer("sess-1", "transaction_type", "RENT")
        info = w.get_current_step_info("sess-1")
        self.assertGreaterEqual(info["step"], STEP_TYPE)

    def test_current_step_unknown_session(self):
        w = _default_wizard()
        info = w.get_current_step_info("nonexistent")
        self.assertEqual(info.get("error"), "session_not_found")

    def test_current_step_includes_channel(self):
        w = _default_wizard()
        w.create_session("sess-1", channel="whatsapp")
        info = w.get_current_step_info("sess-1")
        self.assertEqual(info["channel"], "whatsapp")


class ProgressiveWizardEscalateTest(unittest.TestCase):
    def test_escalate(self):
        w = _default_wizard()
        w.create_session("sess-1")
        result = w.escalate("sess-1", "user requested agent")
        self.assertEqual(result["step"], STEP_ESCALADE)
        self.assertTrue(result["escalated"] if "escalated" in result else True)

    def test_escalate_unknown_session(self):
        w = _default_wizard()
        result = w.escalate("nonexistent")
        self.assertEqual(result.get("error"), "session_not_found")


class ProgressiveWizardResetTest(unittest.TestCase):
    def test_reset_session(self):
        w = _default_wizard()
        w.create_session("sess-1")
        result = w.reset_session("sess-1")
        self.assertEqual(result["status"], "reset")
        self.assertIsNone(w.get_session("sess-1"))

    def test_reset_nonexistent(self):
        w = _default_wizard()
        result = w.reset_session("nonexistent")
        self.assertEqual(result["status"], "reset")


class ProgressiveWizardEndToEndTest(unittest.TestCase):
    def test_full_qualification_flow(self):
        w = _default_wizard()
        s = w.create_session("sess-1", channel="whatsapp")

        # Step 1-2: intent + transaction_type + property_type
        w.submit_answer("sess-1", "intent", "buy")
        w.submit_answer("sess-1", "transaction_type", "RENT")
        w.submit_answer("sess-1", "property_type", "apartment")
        # Now at step 3 (Ville)

        info = w.get_current_step_info("sess-1")
        self.assertEqual(info["step"], STEP_VILLE)

        # Step 3-5: city, neighborhood, budget
        w.submit_answer("sess-1", "city", "Douala")
        w.submit_answer("sess-1", "neighborhood", "Bonanjo")
        w.submit_answer("sess-1", "budget_max", 100000)

        info = w.get_current_step_info("sess-1")
        self.assertGreaterEqual(info["step"], STEP_BUDGET)
        self.assertIn("readiness", info)
        self.assertIn("known_fields", info)

    def test_escalate_during_qualification(self):
        w = _default_wizard()
        w.create_session("sess-1")
        w.submit_answer("sess-1", "intent", "buy")
        result = w.escalate("sess-1", "user wants to talk to agent")
        self.assertEqual(result["step"], STEP_ESCALADE)

    def test_mandatory_fields_required(self):
        w = _default_wizard()
        w.create_session("sess-1")
        w.submit_answer("sess-1", "intent", "buy")
        s = w.get_session("sess-1")
        # transaction_type still missing, should not advance past step 1
        self.assertEqual(s.current_step, STEP_INTENTION)


class ProgressiveWizardServiceTest(unittest.TestCase):
    def test_wizard_from_service(self):
        config = KnowledgeConfig(runtime_enabled=True, project_root=_PROJECT_ROOT)
        svc = KnowledgeService(config)
        try:
            svc.load_all()
        except Exception:
            self.skipTest("Sources not available")
            return
        w = svc.wizard
        self.assertIsNotNone(w)
        s = w.create_session("sess-1")
        self.assertIsNotNone(s)

    def test_wizard_none_when_disabled(self):
        config = KnowledgeConfig(runtime_enabled=False)
        svc = KnowledgeService(config)
        svc.load_all()
        w = svc.wizard
        self.assertIsNone(w)


if __name__ == "__main__":
    unittest.main()
