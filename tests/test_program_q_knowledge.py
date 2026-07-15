# Program Q — Knowledge & Decision Tests
from __future__ import annotations

import unittest

from lawim_v2.program_q import (
    AgriculturalProperty, AvailabilityState, BusinessTransactionType,
    ChannelAdapter, CognitiveDecision, CompatibilityLevel,
    DataQualityScore, EntityExtraction, ExclusionRule,
    ExplainabilityGuardrail, GeoAutocompleteEngine, GeoConstraintEngine,
    GeoReferenceEngine, GeoScoringTier, GeographicRelation,
    HotelProperty, IntentCandidate, IntentClassifier, IntentRoleMapping,
    InvestmentProperty, MarketEquivalent, MatchingEngine,
    MatchingResult, MemoryRetentionPolicy, MobilityMode,
    MultiIntentHandler, NBAPriorityMatrix, PriceConcept, PriceType,
    PriorityEngine, ProgramQConfig, ProgressiveSearchExpansion,
    PropertyPublicationRule, PropertyState, PropertyStateMachine,
    PropertyTypeSchema, QualificationStepMachine, QuestionPriority,
    RematchingEngine, RuleConflictResolver, SLARegistryEntry,
    ScoringDimension, ScoringHarmonizer, StateManagementGuard,
    TransactionSuccessScore, UrgencyDetector, WorkflowPreview,
    channel_limits_for, classify_intent,
    compute_compatibility, compute_market_tension, compute_score,
    data_quality_score,
    expansion_stage_for, explain_decision,
    market_equivalent_for, mobility_adjusted_radius,
    resolve_rule_conflict, validate_publication_rules,
    validate_state_transition,
)

# ── Q1: Property Model Extensions ───────────────────────────────────────


class PropertyFamilyTest(unittest.TestCase):
    def test_agricultural(self):
        p = AgriculturalProperty(crop_types=["maize", "coffee"], land_use="farming",
                                  soil_quality="fertile", farm_size_hectares=5.0)
        self.assertIn("maize", p.crop_types)

    def test_hotel(self):
        p = HotelProperty(star_rating=4, room_count=50, amenities=["pool", "restaurant"])
        self.assertEqual(p.star_rating, 4)

    def test_investment_types(self):
        types = ["buy_to_let", "fix_and_flip", "development", "commercial_investment", "land_banking"]
        self.assertEqual(len(types), 5)

    def test_investment(self):
        p = InvestmentProperty(investment_type="buy_to_let", roi_target=12.0)
        self.assertEqual(p.investment_type, "buy_to_let")

    def test_data_quality(self):
        dq = data_quality_score(8, 10, verified=True, has_photos=True, has_price=True)
        self.assertGreater(dq.total_score, 50)

    def test_property_state_machine(self):
        sm = PropertyStateMachine(PropertyState.DRAFT)
        self.assertTrue(sm.can_transition(PropertyState.PENDING_REVIEW))
        self.assertFalse(sm.can_transition(PropertyState.DELETED))

    def test_property_state_transition(self):
        sm = PropertyStateMachine(PropertyState.PUBLISHED)
        sm.transition(PropertyState.RESERVED)
        self.assertEqual(sm.current_state, PropertyState.RESERVED)

    def test_availability_transitions(self):
        from lawim_v2.program_q.q1_property import AvailabilityState, AVAILABILITY_TRANSITIONS
        self.assertIn(AvailabilityState.RESERVED, AVAILABILITY_TRANSITIONS[AvailabilityState.AVAILABLE])

    def test_price_concepts(self):
        p = PriceConcept(price_displayed=50000000, negotiable=True)
        self.assertTrue(p.negotiable)

    def test_price_types(self):
        self.assertEqual(PriceType.ASKING.value, "ASKING")
        self.assertEqual(PriceType.NOTARY_FEES.value, "NOTARY_FEES")

    def test_publication_rules(self):
        rules = validate_publication_rules({"property_family": "residential", "city": "Douala"})
        self.assertGreaterEqual(len(rules), 1)


# ── Q2: Qualification Engine ─────────────────────────────────────────────


class QualificationEngineTest(unittest.TestCase):
    def test_question_priority(self):
        self.assertEqual(QuestionPriority.MANDATORY.value, "MANDATORY")

    def test_priority_engine_order(self):
        from lawim_v2.program_q.q2_qualification import FieldRoleAssignment
        engine = PriorityEngine()
        fields = [
            FieldRoleAssignment(field_code="b", priority=QuestionPriority.OPTIONAL),
            FieldRoleAssignment(field_code="a", priority=QuestionPriority.MANDATORY),
        ]
        ordered = engine.order_fields(fields)
        self.assertEqual(ordered[0].field_code, "a")

    def test_channel_limits(self):
        limits = channel_limits_for("whatsapp")
        self.assertEqual(limits["mandatory"], 1)

    def test_channel_adapter(self):
        ca = ChannelAdapter(channel="telegram")
        self.assertGreaterEqual(ca.questions_per_interaction(QuestionPriority.MANDATORY), 1)

    def test_step_machine(self):
        sm = QualificationStepMachine()
        self.assertTrue(sm.can_advance())
        sm.advance()
        self.assertEqual(sm.current_step, 2)

    def test_step_abandon(self):
        sm = QualificationStepMachine()
        sm.abandon()
        from lawim_v2.program_q.q2_qualification import StepStatus
        self.assertEqual(sm.status, StepStatus.ABANDONED)

    def test_step_resume(self):
        sm = QualificationStepMachine()
        sm.resume(5)
        self.assertEqual(sm.current_step, 5)


# ── Q3: Geography & Search ──────────────────────────────────────────────


class GeographySearchTest(unittest.TestCase):
    def test_mobility_modes(self):
        self.assertEqual(MobilityMode.CAR.value, "CAR")

    def test_mobility_adjusted_radius(self):
        r = mobility_adjusted_radius(1.0, MobilityMode.CAR)
        self.assertEqual(r, 5.0)

    def test_geo_relation(self):
        r = GeographicRelation(relation_type="contains", source_geo_id="CM", target_geo_id="DLA")
        self.assertEqual(r.relation_type, "contains")

    def test_market_equivalent(self):
        eqs = market_equivalent_for("Douala")
        self.assertGreaterEqual(len(eqs), 1)

    def test_progressive_expansion(self):
        exp = ProgressiveSearchExpansion()
        self.assertEqual(exp.current_level, 0)
        exp.expand()
        self.assertEqual(exp.current_level, 1)

    def test_expansion_stage(self):
        stage = expansion_stage_for(0)
        self.assertEqual(stage["name"], "Exact")

    def test_geo_constraints(self):
        engine = GeoConstraintEngine()
        types = engine.valid_transaction_types("city")
        self.assertIn("buy", types)

    def test_geo_autocomplete(self):
        engine = GeoAutocompleteEngine()
        results = engine.search("doua")
        self.assertGreaterEqual(len(results), 1)

    def test_geo_reference(self):
        engine = GeoReferenceEngine()
        self.assertEqual(len(engine.countries()), 1)


# ── Q4: Intent Detection ─────────────────────────────────────────────────


class IntentDetectionTest(unittest.TestCase):
    def test_classify_buy_fr(self):
        self.assertEqual(classify_intent("Je veux acheter une maison"), "buy")

    def test_classify_buy_en(self):
        self.assertEqual(classify_intent("I want to buy a house"), "buy")

    def test_classify_rent(self):
        self.assertEqual(classify_intent("Je cherche une location"), "rent")

    def test_classify_unknown(self):
        self.assertEqual(classify_intent("Bonjour"), "unknown")

    def test_classifier_confidence(self):
        c = IntentClassifier()
        result = c.classify("Je veux acheter")
        self.assertGreaterEqual(result.confidence, 0.0)
        self.assertEqual(result.intent, "buy")

    def test_multi_intent(self):
        handler = MultiIntentHandler()
        handler.process("Je veux acheter une maison et aussi investir dans un terrain")
        self.assertIsNotNone(handler.primary)

    def test_entity_extraction(self):
        ex = EntityExtraction().extract("Je cherche un appartement à Douala budget 50 millions")
        self.assertEqual(ex.city, "Douala")
        self.assertEqual(ex.property_type, "apartment")

    def test_urgency_detector_high(self):
        d = UrgencyDetector().detect("C'est urgent!")
        self.assertEqual(d.level, "HIGH")

    def test_urgency_detector_normal(self):
        d = UrgencyDetector().detect("Bonjour")
        self.assertEqual(d.level, "NORMAL")

    def test_intent_role_mapping(self):
        mapper = IntentRoleMapping()
        self.assertEqual(mapper.map("buy"), "buyer")

    def test_transaction_types(self):
        self.assertEqual(BusinessTransactionType.BUY.value, "BUY")
        self.assertEqual(BusinessTransactionType.SHORT_STAY.value, "SHORT_STAY")


# ── Q5: Matching & Scoring ──────────────────────────────────────────────


class MatchingScoringTest(unittest.TestCase):
    def test_scoring_dimensions(self):
        self.assertEqual(ScoringDimension.LOCATION.value, "LOCATION")

    def test_geo_tier_scores(self):
        self.assertEqual(GeoScoringTier.SAME_NEIGHBORHOOD.value, "SAME_NEIGHBORHOOD")

    def test_compute_score(self):
        s = compute_score({"LOCATION": 80, "BUDGET": 100, "PROPERTY_TYPE": 100})
        self.assertGreater(s, 50)

    def test_compute_compatibility_excellent(self):
        self.assertEqual(compute_compatibility(90), CompatibilityLevel.EXCELLENT)

    def test_compute_compatibility_low(self):
        self.assertEqual(compute_compatibility(30), CompatibilityLevel.LOW)

    def test_matching_engine_basic(self):
        engine = MatchingEngine()
        demand = {"city": "Douala", "budget_max": 50000000, "property_type": "apartment"}
        offers = [{"city": "Douala", "price": 45000000, "property_type": "apartment"}]
        results = engine.match(demand, offers)
        self.assertGreaterEqual(len(results), 1)

    def test_matching_engine_exclusion(self):
        engine = MatchingEngine()
        engine.add_exclusion_rule(ExclusionRule(rule_code="same_owner"))
        demand = {"owner_id": "1"}
        offers = [{"owner_id": "1", "price": 100000}]
        results = engine.match(demand, offers)
        self.assertGreaterEqual(len(results[0].exclusions), 1)

    def test_rematching(self):
        r = RematchingEngine()
        self.assertTrue(r.can_rematch())
        r.rematch("user_declined")
        self.assertEqual(r.rematch_count, 1)

    def test_rematching_max(self):
        r = RematchingEngine(max_rematches=1)
        r.rematch("reason1")
        self.assertFalse(r.rematch("reason2"))

    def test_transaction_success_score(self):
        t = TransactionSuccessScore().compute(80, 100)
        self.assertEqual(t.score, 80.0)

    def test_market_tension(self):
        t = compute_market_tension(100, 50)
        self.assertEqual(t, 100.0)

    def test_exclusion_rule_budget_mismatch(self):
        rule = ExclusionRule(rule_code="budget_mismatch")
        result = rule.evaluate({"budget_min": 100000}, {"price": 200000})
        self.assertTrue(result)


# ── Q6: Architecture Open Points ────────────────────────────────────────


class ArchitectureOpenPointsTest(unittest.TestCase):
    def test_rule_conflict_resolver(self):
        rules = [{"id": "R1", "domain": "A"}, {"id": "R1", "domain": "B"}]
        resolutions = resolve_rule_conflict(rules)
        self.assertGreaterEqual(len(resolutions), 1)

    def test_sla_registry(self):
        entry = SLARegistryEntry(entity_type="visit", state="requested", threshold_ms=300000)
        self.assertEqual(entry.threshold_ms, 300000)

    def test_nba_matrix(self):
        matrix = NBAPriorityMatrix()
        action = matrix.resolve("qualifying", "response")
        self.assertEqual(action, "ask_next_question")

    def test_scoring_harmonizer(self):
        h = ScoringHarmonizer()
        self.assertAlmostEqual(h.v1_to_v5(75), 0.75)
        self.assertAlmostEqual(h.v5_to_v1(0.8), 80.0)

    def test_memory_retention(self):
        policy = MemoryRetentionPolicy(retention_days=365)
        self.assertTrue(policy.apply("2026-01-01T00:00:00"))

    def test_geo_hierarchy_gap(self):
        from lawim_v2.program_q.q6_architecture import GeoHierarchyPolicy
        g = GeoHierarchyPolicy(implemented_levels=8, gold_levels=9)
        self.assertEqual(g.gap(), 1)


# ── Q7: Cognitive Core ──────────────────────────────────────────────────


class CognitiveCoreTest(unittest.TestCase):
    def test_explainability_guardrail(self):
        g = explain_decision("d1", ["R1", "R2"], "Budget match", 0.85)
        self.assertEqual(g.decision_id, "d1")

    def test_state_management_guard(self):
        guard = StateManagementGuard(allowed_transitions={"draft": ["active"]}, current_state="draft")
        self.assertTrue(guard.can_transition("active"))
        self.assertFalse(guard.can_transition("invalid"))

    def test_validate_state_transition(self):
        transitions = {"draft": ["published"]}
        self.assertTrue(validate_state_transition("draft", "published", transitions))
        self.assertFalse(validate_state_transition("draft", "deleted", transitions))

    def test_cognitive_decision(self):
        d = CognitiveDecision(decision_id="d1", decision_type="qualify", risk_level="MEDIUM")
        self.assertEqual(d.risk_level, "MEDIUM")

    def test_workflow_preview(self):
        w = WorkflowPreview(workflow_id="w1", name="Test", requires_approval=True)
        self.assertTrue(w.requires_approval)


# ── Config Tests ────────────────────────────────────────────────────────


class ProgramQConfigTest(unittest.TestCase):
    def test_default_disabled(self):
        cfg = ProgramQConfig()
        self.assertFalse(cfg.property_model_extensions_enabled)
        self.assertFalse(cfg.qualification_enhancements_enabled)
        self.assertFalse(cfg.matching_scoring_enabled)


# ── Run ─────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    unittest.main()
