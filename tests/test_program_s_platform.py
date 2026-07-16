# Program S — Analytics, Learning, AI, Ecosystem, Future & Debt Tests
from __future__ import annotations

import unittest

from lawim_v2.program_s.s1_analytics import (
    AggregateStatus, AnalyticsAggregate, AnalyticsEngine,
    AnalyticsEvent, DashboardSnapshot, MetricDefinition, MetricDomain,
    ReportSchedule, AnalyticsRecalculation,
)
from lawim_v2.program_s.s2_learning import (
    EventBus, EventBusMessage, FeatureEngineeringPipeline,
    ModelDefinition, ModelRegistry, TrainingJob, TrainingPipeline,
    TrainingStatus, DriftDetector, PersistedLearningEvent,
)
from lawim_v2.program_s.s3_agents import (
    AGENT_ACTIVATIONS, AgentActivation, AgentMetrics,
    PersistedAgentMemory,
)
from lawim_v2.program_s.s4_ecosystem import (
    CONNECTOR_TYPES, ApiKey, ConnectorInstance, ExtensionInstallation,
    Partner, Tenant, TenantQuota, WhiteLabelConfig,
)
from lawim_v2.program_s.s5_future import (
    CONSTITUTION, ConstitutionalRule, DigitalTwin, FutureConsoleView,
    IntelligenceNode, Prediction, PredictiveEngine, WorkflowSimulation,
)
from lawim_v2.program_s.s6_debt import (
    FRONTEND_REQUIREMENTS, DatabaseMigration, MigrationRunner,
    NotificationPreference, RBAC_PERMISSIONS, TechnicalDebtItem,
    check_permission,
)

# ── S1: Analytics ─────────────────────────────────────────────────────


class AnalyticsTest(unittest.TestCase):
    def test_metric_domain(self):
        self.assertEqual(MetricDomain.ADMIN.value, "ADMIN")

    def test_analytics_engine(self):
        engine = AnalyticsEngine()
        metric = MetricDefinition(code="conv_total", name="Conversions",
                                    domain=MetricDomain.ADMIN, formula="COUNT(*)")
        events = [AnalyticsEvent(metric_code="conv_total", value=1) for _ in range(5)]
        agg = engine.compute_aggregate(metric, events)
        self.assertEqual(agg.value, 5)
        self.assertEqual(agg.status, AggregateStatus.COMPUTED)

    def test_rebuild(self):
        engine = AnalyticsEngine()
        metrics = [MetricDefinition(code="m1", domain=MetricDomain.ADMIN, formula="COUNT")]
        events = [AnalyticsEvent(metric_code="m1", value=1)]
        run = engine.rebuild(metrics, events)
        self.assertEqual(run.status, "COMPLETED")

    def test_dashboard_snapshot(self):
        s = DashboardSnapshot(domain=MetricDomain.REPORTING, metrics={"conv": 100.0})
        self.assertEqual(s.metrics["conv"], 100.0)

    def test_report_schedule(self):
        s = ReportSchedule(name="Weekly", cron="0 6 * * 1")
        self.assertEqual(s.cron, "0 6 * * 1")


# ── S2: Learning ──────────────────────────────────────────────────────


class LearningTest(unittest.TestCase):
    def test_event_bus(self):
        bus = EventBus()
        results = []
        def handler(msg): results.append(msg)
        bus.subscribe("test.event", handler)
        bus.publish(EventBusMessage(event_type="test.event", message_id="m1"))
        self.assertEqual(len(results), 1)

    def test_event_bus_dead_letter(self):
        bus = EventBus()
        def failing(msg): raise ValueError("fail")
        bus.subscribe("fail.event", failing)
        msg = EventBusMessage(event_type="fail.event", message_id="fail1")
        for _ in range(4):
            bus.publish(msg)
        self.assertGreaterEqual(len(bus.dead_letters()), 1)

    def test_feature_pipeline(self):
        pipe = FeatureEngineeringPipeline()
        features = pipe.transform({"channel": "whatsapp", "message_count": 10})
        self.assertGreaterEqual(len(features), 3)

    def test_training_pipeline(self):
        pipe = TrainingPipeline()
        job = TrainingJob(name="test_model", model_type="classifier")
        pipe.submit(job)
        self.assertEqual(job.status, TrainingStatus.QUEUED)

    def test_model_registry(self):
        reg = ModelRegistry()
        m = ModelDefinition(name="test", model_type="scoring")
        reg.register(m)
        reg.approve(m.model_id, "admin")
        self.assertEqual(m.status, "APPROVED")

    def test_drift_detector(self):
        d = DriftDetector()
        result = d.check("conversion_rate", 0.15, 0.08, threshold_pct=20)
        self.assertTrue(result.drifted)

    def test_no_drift(self):
        d = DriftDetector()
        result = d.check("conv", 0.15, 0.14, threshold_pct=20)
        self.assertFalse(result.drifted)


# ── S3: Agents ────────────────────────────────────────────────────────


class AgentsTest(unittest.TestCase):
    def test_agent_count(self):
        self.assertEqual(len(AGENT_ACTIVATIONS), 16)

    def test_agent_activation(self):
        a = AgentActivation(agent_code="conversation")
        self.assertEqual(a.status.value, "DRAFT")

    def test_agent_metrics(self):
        m = AgentMetrics(agent_code="qualification", invocations=100, success_rate=95.0)
        d = m.to_dict()
        self.assertEqual(d["invocations"], 100)


# ── S4: Ecosystem ─────────────────────────────────────────────────────


class EcosystemTest(unittest.TestCase):
    def test_tenant(self):
        t = Tenant(tenant_id="t1", name="Test Agency")
        self.assertEqual(t.name, "Test Agency")

    def test_tenant_features(self):
        t = Tenant(tenant_id="t1", features={"analytics": True})
        self.assertTrue(t.can("analytics"))
        self.assertFalse(t.can("agent"))

    def test_connector_types(self):
        self.assertEqual(len(CONNECTOR_TYPES), 15)

    def test_api_key(self):
        k = ApiKey(key_prefix="lawim_", partner_id="p1")
        d = k.to_dict()
        self.assertEqual(d["key_prefix"], "lawim_")

    def test_white_label(self):
        w = WhiteLabelConfig(tenant_id="t1", company_name="Agency X",
                               primary_color="#ff6600")
        self.assertEqual(w.company_name, "Agency X")


# ── S5: Future Platform ──────────────────────────────────────────────


class FuturePlatformTest(unittest.TestCase):
    def test_digital_twin(self):
        t = DigitalTwin(entity_type="property", entity_id="p1")
        self.assertEqual(t.entity_type, "property")

    def test_prediction(self):
        engine = PredictiveEngine()
        p = engine.predict("conversion", {"channel": "whatsapp"})
        self.assertEqual(p.prediction_type, "conversion")

    def test_constitution_count(self):
        self.assertGreaterEqual(len(CONSTITUTION), 5)

    def test_constitutional_rule(self):
        r = ConstitutionalRule(rule_id="C001", principle="Human Oversight")
        self.assertTrue(r.non_negotiable)

    def test_workflow_simulation(self):
        s = WorkflowSimulation(workflow_type="matching")
        self.assertTrue(s.requires_approval)


# ── S6: Technical Debt ──────────────────────────────────────────────


class TechnicalDebtTest(unittest.TestCase):
    def test_rbac_permissions(self):
        self.assertIn("admin", RBAC_PERMISSIONS)
        self.assertIn("user", RBAC_PERMISSIONS)

    def test_check_permission_admin(self):
        self.assertTrue(check_permission("admin", "any_action"))

    def test_check_permission_user(self):
        self.assertFalse(check_permission("user", "write"))

    def test_check_permission_tenant_admin(self):
        self.assertTrue(check_permission("tenant_admin", "manage_tenant"))

    def test_migration_runner(self):
        runner = MigrationRunner()
        runner.add(DatabaseMigration(version="001", description="init"))
        runner.add(DatabaseMigration(version="002", description="add_table"))
        results = runner.run_all()
        self.assertEqual(len(results), 2)

    def test_technical_debt_item(self):
        item = TechnicalDebtItem(debt_id="td1", category="database",
                                   description="Missing index")
        item.resolve("Index created")
        self.assertEqual(item.status, "RESOLVED")

    def test_frontend_requirements(self):
        self.assertIn("responsive_design", FRONTEND_REQUIREMENTS)

    def test_notification_preference(self):
        p = NotificationPreference(user_id=1, whatsapp=True)
        self.assertTrue(p.whatsapp)


if __name__ == "__main__":
    unittest.main()
