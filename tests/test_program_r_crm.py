# Program R — CRM, Services, Agency & Workflows Tests
from __future__ import annotations

import unittest

from lawim_v2.program_r import ProgramRConfig
from lawim_v2.program_r.r1_crm import (
    BOOSTER_DEFINITIONS, PENALTY_DEFINITIONS, CRMRoutingEngine,
    LEAD_CLASS_THRESHOLDS, LeadClass, LeadScore, LeadScoringEngine,
    LeadSLA, PipelineItem, PipelineStage, SLA_THRESHOLDS_MINUTES,
)
from lawim_v2.program_r.r2_agency import (
    TRUST_LEVEL_ORDER, Agency, AgencyOnboarding, AgentCredit,
    AgentSubscription, AgentZone, Badge, BadgeType, TrustLevel,
)
from lawim_v2.program_r.r3_service import (
    BoostPurchase, LeadPurchase, PaymentState,
    PremiumListing, SERVICE_ORDER_TRANSITIONS, ServiceOrder,
    ServiceOrderStatus, Visit, VisitStatus, VISIT_TRANSITIONS,
)
from lawim_v2.program_r.r4_project import (
    DOSSIER_TRANSITIONS, Dossier, DossierHealthScore, DossierRematch,
    DossierState, DoubleConsent, HolderDecision,
)
from lawim_v2.program_r.r5_relationship import (
    CONSENT_TRANSITIONS, Consent, ConsentStatus, HumanHandover,
    Relationship, RelationshipRole,
)
from lawim_v2.program_r.r6_workflow import (
    NBAEngine, WorkflowInstance, WorkflowType, WORKFLOW_STATE_MACHINES,
)
from lawim_v2.program_r.r7_events import (
    EVENT_CATALOG_ENTRIES, ApprovalWorkflow, AuditTrailEntry,
    EnrichedEvent, EventPrivacy, PermissionLevel, RetentionPolicy,
)
from lawim_v2.program_r.r8_sla import (
    SLABreach, SLABreachEscalation, SLAPriority, SLA_TARGETS,
    AntiFraudEngine, HolderSilenceTracker,
)
from lawim_v2.program_r.r9_migration import (
    CROSSWALK_ENTRIES, GOLD_WORKFLOW_STATES, WorkflowMigrationHelper,
)
from lawim_v2.program_r.r10_memory import (
    GovernanceRecord, IntelligenceReview, MemoryEntry, MemoryType,
)


# ── R1: CRM Pipeline ───────────────────────────────────────────────────


class CRMPipelineTest(unittest.TestCase):
    def test_lead_scoring(self):
        engine = LeadScoringEngine()
        score = engine.score(50, {"budget_detected": True, "city_detected": True})
        self.assertGreater(score.score, 50)

    def test_lead_classify_hot(self):
        score = LeadScore(score=85)
        self.assertEqual(score.classify(), LeadClass.HOT)

    def test_lead_classify_dead(self):
        score = LeadScore(score=5)
        self.assertEqual(score.classify(), LeadClass.DEAD)

    def test_boosters_count(self):
        self.assertEqual(len(BOOSTER_DEFINITIONS), 13)

    def test_penalties_count(self):
        self.assertEqual(len(PENALTY_DEFINITIONS), 8)

    def test_routing(self):
        engine = CRMRoutingEngine()
        score = LeadScore(score=85)
        route = engine.route(score)
        self.assertEqual(route["strategy"], "immediate")

    def test_pipeline_advance(self):
        item = PipelineItem(stage=PipelineStage.LEAD_IN)
        self.assertTrue(item.can_advance())
        item.advance()
        self.assertEqual(item.stage, PipelineStage.QUALIFICATION)

    def test_pipeline_full(self):
        item = PipelineItem(stage=PipelineStage.RECYCLED)
        self.assertFalse(item.can_advance())

    def test_sla_thresholds(self):
        self.assertEqual(SLA_THRESHOLDS_MINUTES[LeadSLA.HOT_15M], 15)


# ── R2: Agency ─────────────────────────────────────────────────────────


class AgencyTest(unittest.TestCase):
    def test_trust_levels(self):
        self.assertEqual(len(TRUST_LEVEL_ORDER), 6)

    def test_badge_types(self):
        self.assertEqual(BadgeType.PHONE_VERIFIED.value, "PHONE_VERIFIED")

    def test_agency_operational(self):
        agency = Agency(members=[])
        self.assertFalse(agency.is_operational())

    def test_onboarding_complete(self):
        o = AgencyOnboarding()
        o.complete_step("profile")
        o.complete_step("training")
        o.complete_step("documents")
        o.complete_step("approval")
        o.complete_step("activation")
        self.assertEqual(o.status, "COMPLETED")

    def test_agent_credit(self):
        c = AgentCredit(credits=1000)
        self.assertTrue(c.deduct(500))
        self.assertEqual(c.credits, 500)

    def test_agent_credit_insufficient(self):
        c = AgentCredit(credits=100)
        self.assertFalse(c.deduct(500))

    def test_agent_zone(self):
        z = AgentZone(zone_code="DLA-1", capacity=2)
        self.assertTrue(z.assign(1))
        self.assertTrue(z.assign(2))
        self.assertFalse(z.assign(3))


# ── R3: Service Orders ────────────────────────────────────────────────


class ServiceOrderTest(unittest.TestCase):
    def test_service_order_transitions(self):
        self.assertIn(ServiceOrderStatus.CONFIRMED,
                      SERVICE_ORDER_TRANSITIONS[ServiceOrderStatus.CREATED])

    def test_service_order_flow(self):
        o = ServiceOrder(order_id="o1", service_type="visit")
        o.transition(ServiceOrderStatus.CONFIRMED)
        self.assertEqual(o.status, ServiceOrderStatus.CONFIRMED)

    def test_payment_states(self):
        self.assertEqual(PaymentState.INITIATED.value, "INITIATED")
        self.assertEqual(PaymentState.CONFIRMED.value, "CONFIRMED")

    def test_visit_status(self):
        v = Visit(visit_id="v1", status=VisitStatus.REQUESTED)
        v.transition(VisitStatus.SCHEDULED)
        self.assertEqual(v.status, VisitStatus.SCHEDULED)

    def test_lead_purchase_packs(self):
        packs = LeadPurchase.pack_options()
        self.assertEqual(len(packs), 3)


# ── R4: Projects ──────────────────────────────────────────────────────


class ProjectDossierTest(unittest.TestCase):
    def test_dossier_transitions(self):
        self.assertIn(DossierState.QUALIFYING,
                      DOSSIER_TRANSITIONS[DossierState.DRAFT])

    def test_dossier_flow(self):
        d = Dossier(dossier_id="d1", state=DossierState.DRAFT)
        d.transition(DossierState.QUALIFYING)
        self.assertEqual(d.state, DossierState.QUALIFYING)

    def test_double_consent(self):
        c = DoubleConsent(dossier_id="d1")
        self.assertFalse(c.is_complete())
        c.c1_demandeur = True
        c.c2_holder = True
        self.assertTrue(c.is_complete())

    def test_dossier_rematch(self):
        r = DossierRematch(max_rematches=2)
        self.assertTrue(r.rematch("no_match"))
        self.assertTrue(r.rematch("declined"))
        self.assertFalse(r.rematch("expired"))
        self.assertEqual(r.count, 2)

    def test_health_score(self):
        h = DossierHealthScore().compute(8, 10, 5)
        self.assertGreater(h.total, 0)


# ── R5: Relationship ──────────────────────────────────────────────────


class RelationshipTest(unittest.TestCase):
    def test_consent_grant(self):
        c = Consent(consent_id="c1")
        c.grant()
        self.assertEqual(c.status, ConsentStatus.GRANTED)

    def test_consent_revoke(self):
        c = Consent(consent_id="c1")
        c.grant()
        c.revoke()
        self.assertEqual(c.status, ConsentStatus.REVOKED)

    def test_consent_active(self):
        c = Consent(consent_id="c1")
        c.grant()
        self.assertTrue(c.is_active())

    def test_relationship_roles(self):
        self.assertEqual(RelationshipRole.DEMANDEUR.value, "DEMANDEUR")

    def test_human_handover(self):
        h = HumanHandover(handover_id="h1", summary="Need help")
        self.assertEqual(h.status, "REQUESTED")


# ── R6: Workflow ──────────────────────────────────────────────────────


class WorkflowTest(unittest.TestCase):
    def test_workflow_types(self):
        self.assertGreater(len(WORKFLOW_STATE_MACHINES), 10)

    def test_workflow_instance(self):
        wf = WorkflowInstance(workflow_type=WorkflowType.MATCHING)
        self.assertTrue(wf.can_advance())
        wf.advance()
        self.assertEqual(wf.current_state, "scored")

    def test_nba_engine(self):
        nba = NBAEngine()
        action = nba.next_best_action("qualifying", "response")
        self.assertEqual(action["action"], "ask_next_question")


# ── R7: Events ────────────────────────────────────────────────────────


class EventsTest(unittest.TestCase):
    def test_event_catalog(self):
        self.assertGreater(len(EVENT_CATALOG_ENTRIES), 10)

    def test_enriched_event(self):
        e = EnrichedEvent(event_type="user.created", severity="INFO")
        self.assertEqual(e.severity, "INFO")

    def test_audit_trail(self):
        a = AuditTrailEntry(audit_id="a1", action="update", target_type="property")
        self.assertEqual(a.action, "update")

    def test_approval_workflow(self):
        a = ApprovalWorkflow(approval_id="a1")
        a.approve("reviewer1")
        self.assertEqual(a.status, "APPROVED")

    def test_retention_policy(self):
        p = RetentionPolicy(event_type="test", retention_days=30)
        import datetime
        old = (datetime.datetime.now(datetime.timezone.utc) -
               datetime.timedelta(days=60)).isoformat()
        self.assertFalse(p.should_retain(old))


# ── R8: SLA & Fraud ───────────────────────────────────────────────────


class SLAFraudTest(unittest.TestCase):
    def test_sla_priority(self):
        self.assertEqual(SLA_TARGETS[SLAPriority.P0], 5)

    def test_sla_breach(self):
        b = SLABreach(threshold_minutes=30, actual_minutes=45)
        self.assertTrue(b.is_breached())

    def test_fraud_detection(self):
        engine = AntiFraudEngine()
        signals = engine.check_message("Offre unique: achetez maintenant 100000000")
        self.assertGreaterEqual(len(signals), 1)

    def test_holder_silence(self):
        tracker = HolderSilenceTracker(silence_threshold_hours=24)
        self.assertTrue(tracker.is_silent(48))


# ── R9: Migration ─────────────────────────────────────────────────────


class WorkflowMigrationTest(unittest.TestCase):
    def test_gold_to_v2(self):
        helper = WorkflowMigrationHelper()
        wf_type = helper.gold_to_v2("matching")
        self.assertEqual(wf_type, WorkflowType.MATCHING)

    def test_state_compatibility(self):
        helper = WorkflowMigrationHelper()
        result = helper.state_compatibility("matching",
                                             GOLD_WORKFLOW_STATES["matching"])
        self.assertTrue(result["compatible"])

    def test_crosswalk_entries(self):
        self.assertGreater(len(CROSSWALK_ENTRIES), 5)


# ── R10: Memory ───────────────────────────────────────────────────────


class MemoryGovernanceTest(unittest.TestCase):
    def test_memory_types(self):
        self.assertEqual(MemoryType.CONVERSATION.value, "CONVERSATION")

    def test_intelligence_review(self):
        r = IntelligenceReview(review_id="r1", proposal_ids=["p1"])
        r.approve()
        self.assertEqual(r.decision, "APPROVED")

    def test_governance_record(self):
        from lawim_v2.program_r.r10_memory import GovernanceAction
        g = GovernanceRecord(record_id="g1", action=GovernanceAction.APPROVE)
        self.assertEqual(g.action.value, "APPROVE")


# ── Config ────────────────────────────────────────────────────────────


class ProgramRConfigTest(unittest.TestCase):
    def test_default_disabled(self):
        cfg = ProgramRConfig()
        self.assertFalse(cfg.crm_pipeline_enabled)


if __name__ == "__main__":
    unittest.main()
