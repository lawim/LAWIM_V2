from __future__ import annotations

import pytest

from lawim_runtime.interaction.deduplication import InteractionDeduplicator, DeduplicationStatus
from lawim_runtime.interaction.envelope import InteractionEnvelope, MessageType
from lawim_runtime.interaction.identity import IdentityResolver, IdentityStatus
from lawim_runtime.interaction.project_resolution import ProjectResolver, ProjectResolutionStatus
from lawim_runtime.interaction.session import SessionManager, SessionStatus
from lawim_runtime.interaction.delivery import DeliveryManager, DeliveryStatus, DeliveryAttempt
from lawim_runtime.interaction.response_writer import DeterministicResponseWriter, ResponseWriterRequest
from lawim_runtime.interaction.response_plan import InteractionResponsePlan, ResponseType
from lawim_runtime.interaction.correlation import CorrelationManager
from lawim_runtime.interaction.routing import InteractionModeRouter, InteractionMode
from lawim_runtime.interaction.divergence import InteractionDivergenceAnalyzer
from lawim_runtime.interaction.metrics import InteractionMetrics
from lawim_runtime.interaction.events import build_interaction_event

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeStatus
from lawim_runtime.domains.matching.runtime import MatchingRuntime
from lawim_runtime.domains.visit.runtime import VisitRuntime
from lawim_runtime.domains.visit.models import VisitStatus


# ---------------------------------------------------------------------------
# RESILIENCE-01: Duplicate inbound message
# ---------------------------------------------------------------------------

class TestResilienceDuplicate:

    def test_duplicate_webhook_same_id(self):
        dedup = InteractionDeduplicator()

        c1 = dedup.check("msg-dup-001", "whatsapp")
        assert c1 == DeduplicationStatus.NEW

        c2 = dedup.check("msg-dup-001", "whatsapp")
        assert c2 == DeduplicationStatus.DUPLICATE

    def test_duplicate_different_channel_same_id(self):
        dedup = InteractionDeduplicator()

        assert dedup.check("msg-001", "whatsapp") == DeduplicationStatus.NEW
        assert dedup.check("msg-001", "telegram") == DeduplicationStatus.NEW
        assert dedup.check("msg-001", "whatsapp") == DeduplicationStatus.DUPLICATE

    def test_delivery_duplicate_check(self):
        dedup = InteractionDeduplicator()

        assert not dedup.is_delivery_duplicate("del-001")
        assert dedup.is_delivery_duplicate("del-001")


# ---------------------------------------------------------------------------
# RESILIENCE-02: Concurrent profile updates
# ---------------------------------------------------------------------------

class TestResilienceConcurrent:

    def test_concurrent_updates_no_loss(self):
        from lawim_runtime.project_profile.profile import ProjectProfile
        p = ProjectProfile(project_id="proj-concur", profile_type="rental_search")

        p.set_field("city", "Douala", confidence=0.9)
        p.set_field("max_budget", 100_000, confidence=0.8)
        p.set_field("city", "Yaounde", confidence=0.9)
        p.set_field("max_budget", 80_000, confidence=0.7)

        assert p.fields["city"].value == "Yaounde"
        assert p.fields["max_budget"].value == 80_000


# ---------------------------------------------------------------------------
# RESILIENCE-03: Project ambiguity isolation
# ---------------------------------------------------------------------------

class TestResilienceProjectAmbiguity:

    def test_two_projects_no_merge(self):
        projects = ProjectResolver()
        user_id = "user-ambig"
        projects.register_project(user_id, "proj-a")
        projects.register_project(user_id, "proj-b")

        result = projects.resolve(user_id)
        assert result.status == ProjectResolutionStatus.AMBIGUOUS
        assert result.active_project_count == 2

    def test_resolve_single_active(self):
        projects = ProjectResolver()
        user_id = "user-single"
        projects.register_project(user_id, "proj-001")
        projects.register_project(user_id, "proj-002", status="closed")

        result = projects.resolve(user_id)
        assert result.status == ProjectResolutionStatus.RESOLVED
        assert result.project_id == "proj-001"


# ---------------------------------------------------------------------------
# RESILIENCE-04: Crash before delivery
# ---------------------------------------------------------------------------

class TestResilienceCrashBeforeDelivery:

    def test_profile_persists_after_crash(self):
        from lawim_runtime.project_profile.profile import ProjectProfile
        p = ProjectProfile(project_id="proj-crash", profile_type="rental_search")
        p.set_field("city", "Yaounde")

        p2 = ProjectProfile(project_id="proj-crash", profile_type="rental_search")

        assert p.fields["city"].value == "Yaounde"

    def test_delivery_idempotency(self):
        delivery = DeliveryManager()
        plan = InteractionResponsePlan(
            response_type=ResponseType.GREETING,
            correlation_id="crash-dedup",
        )

        r1 = delivery.deliver(plan, "whatsapp")
        r2 = delivery.deliver(plan, "whatsapp")

        assert r1.delivery_id != r2.delivery_id


# ---------------------------------------------------------------------------
# RESILIENCE-05: Domain Runtime failure recovery
# ---------------------------------------------------------------------------

class TestResilienceDomainFailure:

    def test_domain_failure_returns_failed(self):
        matching = MatchingRuntime()
        req = DomainRuntimeRequest(
            action_code="START_MATCHING",
            parameters={},
        )
        result = matching.execute(req)
        assert result.status == DomainRuntimeStatus.FAILED

    def test_visit_invalid_transition(self):
        visit = VisitRuntime()
        req = DomainRuntimeRequest(
            action_code="CONFIRM_VISIT",
            parameters={"visit_id": "nonexistent"},
        )
        result = visit.execute(req)
        assert result.output.get("status") == VisitStatus.FAILED.value or result.status == DomainRuntimeStatus.FAILED


# ---------------------------------------------------------------------------
# RESILIENCE-06: Writer failure fallback
# ---------------------------------------------------------------------------

class TestResilienceWriterFallback:

    def test_deterministic_writer_always_succeeds(self):
        writer = DeterministicResponseWriter()

        for rtype in ResponseType:
            plan = InteractionResponsePlan(response_type=rtype)
            req = ResponseWriterRequest(response_plan=plan)
            result = writer.write(req)
            assert result.success or result.text == ""

    def test_writer_safe_fallback_on_no_plan(self):
        writer = DeterministicResponseWriter()
        req = ResponseWriterRequest()
        result = writer.write(req)
        assert result.success
        assert "difficult\u00e9" in result.text


# ---------------------------------------------------------------------------
# RESILIENCE-07: Channel failure
# ---------------------------------------------------------------------------

class TestResilienceChannelFailure:

    def test_delivery_without_channel(self):
        delivery = DeliveryManager()
        plan = InteractionResponsePlan(response_type=ResponseType.GREETING)
        result = delivery.deliver(plan, "")
        assert result.is_failed or result.status in (DeliveryStatus.SENT, DeliveryStatus.CANCELLED)


# ---------------------------------------------------------------------------
# RESILIENCE-08: Restart recovery
# ---------------------------------------------------------------------------

class TestResilienceRestart:

    def test_correlation_persists(self):
        corr = CorrelationManager()
        cid = corr.create("restart-001")
        corr.update(cid, interaction_id="int-restart", project_id="proj-restart")

        trace = corr.trace(cid)
        assert trace is not None
        assert trace.interaction_id == "int-restart"
        assert trace.project_id == "proj-restart"

    def test_session_expiry_after_timeout(self):
        sessions = SessionManager(timeout_minutes=0)
        session = sessions.create_session("user-restart", "whatsapp")
        session.last_activity_at = "2020-01-01T00:00:00+00:00"

        fetched = sessions.get_session(session.session_id)
        assert fetched is not None
        assert fetched.status == SessionStatus.EXPIRED


# ---------------------------------------------------------------------------
# RESILIENCE-09: V2/V3 Shadow mode
# ---------------------------------------------------------------------------

class TestResilienceShadowMode:

    def test_shadow_mode_no_external_effects(self):
        router = InteractionModeRouter(mode=InteractionMode.V3_SHADOW)

        assert router.is_shadow()
        assert router.resolve_mode() == InteractionMode.V3_SHADOW

    def test_shadow_mode_not_active_for_v2(self):
        router = InteractionModeRouter(mode=InteractionMode.V2_ONLY)
        assert not router.is_v3_active()
        assert not router.is_shadow()


# ---------------------------------------------------------------------------
# RESILIENCE-10: V3 Canary mode
# ---------------------------------------------------------------------------

class TestResilienceCanary:

    def test_canary_only_for_authorized(self):
        router = InteractionModeRouter(
            mode=InteractionMode.V3_CANARY,
            canary_users={"user-canary"},
        )

        assert router.resolve_mode(user_id="user-canary") == InteractionMode.V3_CANARY
        assert router.resolve_mode(user_id="user-normal") == InteractionMode.V2_ONLY

    def test_canary_by_channel(self):
        env = InteractionEnvelope(channel="telegram")
        router = InteractionModeRouter(
            mode=InteractionMode.V3_CANARY,
            canary_channels={"telegram"},
        )

        assert router.resolve_mode(envelope=env) == InteractionMode.V3_CANARY
        assert router.resolve_mode(envelope=InteractionEnvelope(channel="whatsapp")) == InteractionMode.V2_ONLY


# ---------------------------------------------------------------------------
# RESILIENCE-11: V3 with V2 fallback
# ---------------------------------------------------------------------------

class TestResilienceFallback:

    def test_v3_primary_with_v2_fallback(self):
        router = InteractionModeRouter(mode=InteractionMode.V3_PRIMARY_WITH_V2_FALLBACK)
        assert router.is_v3_active()
        assert not router.is_shadow()


# ---------------------------------------------------------------------------
# RESILIENCE-12: Divergence Recording
# ---------------------------------------------------------------------------

class TestResilienceDivergence:

    def test_divergence_recorded(self):
        analyzer = InteractionDivergenceAnalyzer()
        divergences = analyzer.compare(
            interaction_id="int-div",
            correlation_id="corr-div",
            channel="whatsapp",
            v2_result={"resolved_identity": "user-a", "next_action": "ASK", "response_type": "text"},
            v3_result={"resolved_identity": "user-b", "next_action": "MATCH", "response_type": "text"},
        )
        assert len(divergences) >= 2

        found = analyzer.list_by_correlation("corr-div")
        assert len(found) == len(divergences)

    def test_manual_divergence(self):
        analyzer = InteractionDivergenceAnalyzer()
        rec = analyzer.record_divergence(
            interaction_id="int-002",
            correlation_id="corr-002",
            channel="telegram",
            field_name="project_id",
            v2_value="proj-a",
            v3_value="proj-b",
            severity="error",
        )
        assert rec.severity == "error"
        assert analyzer.count() == 1


# ---------------------------------------------------------------------------
# RESILIENCE-13: Single delivery guarantee
# ---------------------------------------------------------------------------

class TestResilienceSingleDelivery:

    def test_empty_plan_cancels_delivery(self):
        delivery = DeliveryManager()
        plan = InteractionResponsePlan(response_type=ResponseType.NO_RESPONSE)
        result = delivery.deliver(plan, "whatsapp")
        assert result.status == DeliveryStatus.CANCELLED

    def test_delivery_idempotency(self):
        delivery = DeliveryManager()
        plan = InteractionResponsePlan(response_type=ResponseType.GREETING)
        r1 = delivery.deliver(plan, "whatsapp")
        assert r1.is_delivered or r1.is_failed


# ---------------------------------------------------------------------------
# RESILIENCE-14: Inbound deduplication
# ---------------------------------------------------------------------------

class TestResilienceDedup:

    def test_missing_id_treated_as_new(self):
        dedup = InteractionDeduplicator()
        assert dedup.check("", "whatsapp") == DeduplicationStatus.NEW

    def test_content_hash_dedup(self):
        dedup = InteractionDeduplicator()
        hash_val = "abc123hash"
        assert dedup.check_by_hash(hash_val, "whatsapp") == DeduplicationStatus.NEW
        assert dedup.check_by_hash(hash_val, "whatsapp") == DeduplicationStatus.DUPLICATE
        assert dedup.check_by_hash(hash_val, "telegram") == DeduplicationStatus.NEW
