# Program L — AI Agent Platform Tests
from __future__ import annotations

import json
import unittest

from lawim_v2.program_l import (
    AgentAction, AgentCapability, AgentConfig, AgentContextBuilder,
    AgentDefinition, AgentEvaluationResult, AgentEvaluationService,
    AgentHandover, AgentInvocation, AgentInvocationService,
    AgentMemory, AgentMemoryService, AgentResponse, AgentResponseBuilder,
    AgentRouter, AgentRuntimeContext, AgentSafetyService,
    AgentTool, AgentToolInvocation, AgentType, CapabilityCode,
    EvalStatus, HandoverStatus, InvocationStatus, MemoryType,
    RiskCategory, SafetyDecision, ToolRiskLevel,
    agent_registry,
)
from lawim_v2.program_l.agent_registry import capability_registry
from lawim_v2.program_l.agent_orchestrator import MultiAgentOrchestrator

# ── Agent Registry Tests ───────────────────────────────────────────────


class AgentRegistryTest(unittest.TestCase):
    def test_registry_has_agents(self):
        self.assertGreater(agent_registry.count(), 0)

    def test_get_conversation(self):
        a = agent_registry.get("conversation")
        self.assertIsNotNone(a)
        self.assertEqual(a.agent_code, "conversation")

    def test_get_orchestrator(self):
        a = agent_registry.get("orchestrator")
        self.assertIsNotNone(a)
        self.assertEqual(a.agent_type, AgentType.ORCHESTRATOR)

    def test_list_by_type(self):
        agents = agent_registry.get_by_type(AgentType.CONVERSATION)
        self.assertGreaterEqual(len(agents), 1)

    def test_unique_codes(self):
        agents = agent_registry.list()
        codes = [a.agent_code for a in agents]
        self.assertEqual(len(codes), len(set(codes)))

    def test_all_have_feature_flags(self):
        for a in agent_registry.list():
            self.assertTrue(a.feature_flag, f"{a.agent_code} missing feature_flag")

    def test_to_dict(self):
        a = agent_registry.get("conversation")
        d = a.to_dict()
        self.assertEqual(d["agent_code"], "conversation")

    def test_all_agent_types(self):
        types = {a.agent_type for a in agent_registry.list()}
        self.assertIn(AgentType.CONVERSATION, types)
        self.assertIn(AgentType.QUALIFICATION, types)
        self.assertIn(AgentType.LEARNING, types)


# ── Capability Registry Tests ─────────────────────────────────────────


class CapabilityRegistryTest(unittest.TestCase):
    def test_has_capabilities(self):
        self.assertGreater(capability_registry.count(), 0)

    def test_get_converse(self):
        c = capability_registry.get("CONVERSE")
        self.assertIsNotNone(c)

    def test_unique_codes(self):
        caps = capability_registry.list()
        codes = [c.capability_code for c in caps]
        self.assertEqual(len(codes), len(set(codes)))


# ── Agent Definition Tests ────────────────────────────────────────────


class AgentDefinitionTest(unittest.TestCase):
    def test_create(self):
        a = AgentDefinition(agent_code="test", name="Test Agent",
                             agent_type=AgentType.CONVERSATION)
        self.assertEqual(a.status.value, "DRAFT")

    def test_risk_level(self):
        a = AgentDefinition(agent_code="legal", risk_level="MEDIUM")
        self.assertEqual(a.risk_level, "MEDIUM")


# ── Agent Invocation Tests ────────────────────────────────────────────


class AgentInvocationServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = AgentInvocationService()

    def test_create(self):
        inv = self.svc.create(AgentInvocation(agent_code="conversation"))
        self.assertIsNotNone(inv.invocation_id)
        self.assertEqual(inv.status, InvocationStatus.CREATED)

    def test_complete(self):
        inv = self.svc.create(AgentInvocation(agent_code="test"))
        self.svc.complete(inv.invocation_id, "done")
        self.assertEqual(inv.status, InvocationStatus.COMPLETED)

    def test_fail(self):
        inv = self.svc.create(AgentInvocation(agent_code="test"))
        self.svc.fail(inv.invocation_id, "error")
        self.assertEqual(inv.status, InvocationStatus.FAILED)

    def test_list_by_conversation(self):
        self.svc.create(AgentInvocation(agent_code="a", conversation_id="c1"))
        self.svc.create(AgentInvocation(agent_code="b", conversation_id="c1"))
        self.assertEqual(len(self.svc.list("c1")), 2)


# ── Agent Router Tests ────────────────────────────────────────────────


class AgentRouterTest(unittest.TestCase):
    def setUp(self):
        self.router = AgentRouter()

    def test_route_conversation_default(self):
        self.assertEqual(self.router.route("Bonjour"), "conversation")

    def test_route_support(self):
        self.assertEqual(self.router.route("J'ai besoin d'aide"), "support")

    def test_route_real_estate(self):
        self.assertEqual(self.router.route("Je cherche une maison"), "real_estate")

    def test_route_qualification(self):
        self.assertEqual(self.router.route("J'ai une question"), "qualification")

    def test_route_payment(self):
        self.assertEqual(self.router.route("Mon paiement"), "payment")

    def test_route_document(self):
        self.assertEqual(self.router.route("Mon document"), "document")

    def test_route_legal(self):
        self.assertEqual(self.router.route("Conseil juridique"), "legal")

    def test_route_statistics(self):
        self.assertEqual(self.router.route("Les statistiques"), "director")

    def test_route_learning(self):
        self.assertEqual(self.router.route("Proposition d'apprentissage"), "learning")

    def test_get_agent(self):
        agent = self.router.get_agent("conversation")
        self.assertIsNotNone(agent)


# ── Safety Service Tests ──────────────────────────────────────────────


class AgentSafetyServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = AgentSafetyService()

    def test_allow_read(self):
        d = self.svc.check("read", "data", RiskCategory.READ_ONLY)
        self.assertEqual(d, SafetyDecision.ALLOW)

    def test_handover_irreversible(self):
        d = self.svc.check("write", "system", RiskCategory.IRREVERSIBLE)
        self.assertEqual(d, SafetyDecision.HANDOVER_REQUIRED)

    def test_confirmation_financial(self):
        d = self.svc.check("pay", "amount", RiskCategory.FINANCIAL)
        self.assertEqual(d, SafetyDecision.ALLOW_WITH_CONFIRMATION)

    def test_confirmation_legal(self):
        d = self.svc.check("sign", "contract", RiskCategory.LEGAL)
        self.assertEqual(d, SafetyDecision.ALLOW_WITH_CONFIRMATION)


# ── Agent Action Tests ────────────────────────────────────────────────


class AgentActionTest(unittest.TestCase):
    def test_create(self):
        a = AgentAction(action_type="qualify", target_type="session")
        self.assertEqual(a.status, "PENDING")

    def test_approval_required(self):
        a = AgentAction(action_type="payment", target_type="transaction",
                          approval_required=True)
        self.assertTrue(a.approval_required)


# ── Agent Handover Tests ──────────────────────────────────────────────


class AgentHandoverTest(unittest.TestCase):
    def test_create(self):
        h = AgentHandover(conversation_id="c1", source_agent_id="qualification",
                           reason="Need human validation")
        self.assertEqual(h.status, HandoverStatus.REQUESTED)

    def test_to_dict(self):
        h = AgentHandover(conversation_id="c1", source_agent_id="agent1",
                           target_actor_or_team="support")
        d = h.to_dict()
        self.assertEqual(d["target"], "support")


# ── Agent Memory Tests ────────────────────────────────────────────────


class AgentMemoryServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = AgentMemoryService()

    def test_store(self):
        m = self.svc.store(AgentMemory(key="pref_lang", value="fr",
                                        conversation_id="c1"))
        self.assertIsNotNone(m.memory_id)

    def test_get_by_conversation(self):
        self.svc.store(AgentMemory(key="k1", value="v1", conversation_id="c1"))
        results = self.svc.get_by_conversation("c1")
        self.assertGreaterEqual(len(results), 1)

    def test_get_by_key(self):
        self.svc.store(AgentMemory(key="k1", value="v1"))
        m = self.svc.get_by_key("k1")
        self.assertIsNotNone(m)


# ── Context Builder Tests ─────────────────────────────────────────────


class AgentContextBuilderTest(unittest.TestCase):
    def setUp(self):
        self.builder = AgentContextBuilder()

    def test_build_minimal(self):
        ctx = self.builder.build()
        self.assertEqual(ctx.language, "fr")

    def test_build_with_values(self):
        ctx = self.builder.build(actor_id="a1", conversation_id="c1",
                                  channel="whatsapp", language="en")
        self.assertEqual(ctx.channel, "whatsapp")
        self.assertEqual(ctx.language, "en")

    def test_to_dict(self):
        ctx = self.builder.build(actor_id="a1", conversation_id="c1")
        d = ctx.to_dict()
        self.assertEqual(d["actor_id"], "a1")


# ── Agent Config Tests ────────────────────────────────────────────────


class AgentConfigTest(unittest.TestCase):
    def test_default_disabled(self):
        cfg = AgentConfig()
        self.assertFalse(cfg.agent_platform_enabled)
        self.assertFalse(cfg.conversation_agent_enabled)
        self.assertFalse(cfg.multi_agent_orchestration_enabled)
        self.assertFalse(cfg.agent_memory_enabled)

    def test_enable_one(self):
        cfg = AgentConfig(conversation_agent_enabled=True)
        self.assertTrue(cfg.conversation_agent_enabled)


# ── Evaluation Tests ──────────────────────────────────────────────────


class AgentEvaluationServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = AgentEvaluationService()

    def test_evaluate_pass(self):
        r = self.svc.evaluate("conv", "basic", accuracy=0.9, safety=0.9)
        self.assertEqual(r.status, EvalStatus.PASS)

    def test_evaluate_fail(self):
        r = self.svc.evaluate("conv", "bad", accuracy=0.3, safety=0.2)
        self.assertEqual(r.status, EvalStatus.FAIL)

    def test_evaluate_warning(self):
        r = self.svc.evaluate("conv", "ok", accuracy=0.7, safety=0.6)
        self.assertEqual(r.status, EvalStatus.PASS_WITH_WARNINGS)


# ── Enum Tests ────────────────────────────────────────────────────────


class AgentTypeEnumTest(unittest.TestCase):
    def test_types(self):
        self.assertEqual(AgentType.ORCHESTRATOR.value, "ORCHESTRATOR")
        self.assertEqual(AgentType.LEARNING.value, "LEARNING")


class InvocationStatusEnumTest(unittest.TestCase):
    def test_statuses(self):
        self.assertEqual(InvocationStatus.CREATED.value, "CREATED")
        self.assertEqual(InvocationStatus.COMPLETED.value, "COMPLETED")
        self.assertEqual(InvocationStatus.ESCALATED.value, "ESCALATED")


class SafetyDecisionEnumTest(unittest.TestCase):
    def test_decisions(self):
        self.assertEqual(SafetyDecision.ALLOW.value, "ALLOW")
        self.assertEqual(SafetyDecision.DENY.value, "DENY")


class MemoryTypeEnumTest(unittest.TestCase):
    def test_types(self):
        self.assertEqual(MemoryType.CONVERSATION.value, "CONVERSATION")
        self.assertEqual(MemoryType.AGENT_WORKING.value, "AGENT_WORKING")


class CapabilityCodeEnumTest(unittest.TestCase):
    def test_codes(self):
        self.assertEqual(CapabilityCode.CONVERSE.value, "CONVERSE")
        self.assertEqual(CapabilityCode.REVIEW_LEARNING_PROPOSAL.value, "REVIEW_LEARNING_PROPOSAL")


class ToolRiskLevelEnumTest(unittest.TestCase):
    def test_levels(self):
        self.assertEqual(ToolRiskLevel.READ_ONLY.value, "READ_ONLY")
        self.assertEqual(ToolRiskLevel.IRREVERSIBLE.value, "IRREVERSIBLE")


# ── Serialization Tests ───────────────────────────────────────────────


class AgentSerializationTest(unittest.TestCase):
    def test_definition_json(self):
        a = AgentDefinition(agent_code="test", name="Test")
        s = json.dumps(a.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("test", s)

    def test_invocation_json(self):
        inv = AgentInvocation(invocation_id="i1", agent_code="conv",
                               status=InvocationStatus.RUNNING)
        s = json.dumps(inv.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("RUNNING", s)

    def test_response_json(self):
        r = AgentResponse(response_id="r1", agent_code="test", content="Hello")
        s = json.dumps(r.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("Hello", s)


if __name__ == "__main__":
    unittest.main()
