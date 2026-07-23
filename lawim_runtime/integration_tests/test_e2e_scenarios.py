from __future__ import annotations

from typing import Any

import pytest

from lawim_runtime.interaction.envelope import InteractionEnvelope, MessageType
from lawim_runtime.interaction.identity import IdentityResolver, ChannelIdentity, IdentityStatus
from lawim_runtime.interaction.session import SessionManager, InteractionSession, SessionStatus
from lawim_runtime.interaction.project_resolution import ProjectResolver, ProjectResolutionStatus
from lawim_runtime.interaction.normalization import MessageNormalizer
from lawim_runtime.interaction.deduplication import InteractionDeduplicator, DeduplicationStatus
from lawim_runtime.interaction.correlation import CorrelationManager
from lawim_runtime.interaction.gateway import InteractionGateway
from lawim_runtime.interaction.response_plan import InteractionResponsePlan, ResponseType
from lawim_runtime.interaction.delivery import DeliveryManager, DeliveryStatus
from lawim_runtime.interaction.divergence import InteractionDivergenceAnalyzer
from lawim_runtime.interaction.routing import InteractionModeRouter, InteractionMode
from lawim_runtime.interaction.metrics import InteractionMetrics
from lawim_runtime.interaction.response_writer import DeterministicResponseWriter, ResponseWriterRequest
from lawim_runtime.interaction.extraction import DeterministicExtractor, ExtractionResult

from lawim_runtime.project_profile.base import AbstractProjectProfile
from lawim_runtime.project_profile.profile import ProjectProfile
from lawim_runtime.project_profile.registry import FieldRegistry
from lawim_runtime.project_profile.candidate import CandidateUpdate

from lawim_runtime.qualification.engine import QualificationEngine
from lawim_runtime.qualification.registry import RequirementRegistry

from lawim_runtime.decision.engine import DecisionEngine
from lawim_runtime.decision.result import DecisionResult
from lawim_runtime.decision.handover import HumanHandoverEvaluator

from lawim_runtime.project_brain.brain import ProjectBrain
from lawim_runtime.project_brain.state import ProjectBrainState

from lawim_runtime.execution.request import ActionExecutionRequest
from lawim_runtime.execution.result import ActionExecutionResult, ExecutionStatus
from lawim_runtime.execution.registry import ActionHandlerRegistry

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus
from lawim_runtime.domains.matching.runtime import MatchingRuntime
from lawim_runtime.domains.matching.models import MatchingStatus
from lawim_runtime.domains.visit.runtime import VisitRuntime
from lawim_runtime.domains.visit.models import VisitStatus, VisitRecord
from lawim_runtime.domains.document.runtime import DocumentRuntime
from lawim_runtime.domains.verification.runtime import VerificationRuntime
from lawim_runtime.domains.transaction.runtime import TransactionRuntime
from lawim_runtime.domains.payment.runtime import PaymentRuntime
from lawim_runtime.domains.visit.handlers import VisitHandler
from lawim_runtime.domains.matching.handlers import MatchingHandler
from lawim_runtime.domains.base.handler import DomainRuntimeHandler


def _make_profile(project_id: str = "proj-001") -> ProjectProfile:
    profile = ProjectProfile(
        project_id=project_id,
        profile_type="rental_search",
        profile_id=f"prof-{project_id}",
    )
    return profile


def _make_field_registry() -> FieldRegistry:
    from lawim_runtime.project_profile.field_definitions import register_all_fields
    registry = FieldRegistry()
    register_all_fields(registry)
    return registry


def _make_qual_engine(field_registry: FieldRegistry | None = None) -> QualificationEngine:
    registry = field_registry or _make_field_registry()
    req_registry = RequirementRegistry()
    return QualificationEngine(req_registry, registry)


# ---------------------------------------------------------------------------
# E2E-01: Project Creation
# ---------------------------------------------------------------------------

class TestE2E01ProjectCreation:

    def test_full_project_creation_pipeline(self):
        text = "Je cherche un appartement de 4 chambres à Biyem-Assi, Yaoundé, avec un budget maximum de 100 000 FCFA, pour septembre."

        gateway = InteractionGateway()
        normalizer = MessageNormalizer()
        dedup = InteractionDeduplicator()
        identity = IdentityResolver()
        sessions = SessionManager()
        projects = ProjectResolver()
        delivery = DeliveryManager()
        extractor = DeterministicExtractor()
        writer = DeterministicResponseWriter()
        registry = _make_field_registry()

        env = gateway.prepare_envelope(
            channel="whatsapp",
            external_message_id="e2e-01-msg-001",
            external_user_id="+237600000001",
            raw_sender="+237600000001",
            raw_content=text,
            message_type=MessageType.TEXT,
        )

        assert env.channel == "whatsapp"
        assert env.raw_content == text

        norm = normalizer.normalize(env.raw_content)
        assert not norm.is_empty

        id_result = identity.resolve(env.channel, env.external_user_id, env.raw_sender)
        assert id_result.status == IdentityStatus.ANONYMOUS

        session = sessions.resume_or_create(
            id_result.actor_id or id_result.identity_id,
            env.channel,
        )
        assert session.status == SessionStatus.ACTIVE

        proj_result = projects.resolve(id_result.actor_id or id_result.identity_id)
        assert proj_result.status == ProjectResolutionStatus.NEW_PROJECT

        new_project_id = "e2e-proj-001"
        projects.register_project(
            id_result.actor_id or id_result.identity_id,
            new_project_id,
        )

        extraction = extractor.extract(text, project_id=new_project_id)
        assert len(extraction.candidates) >= 4

        field_names = {c.field_name for c in extraction.candidates}
        assert "property_type" in field_names
        assert "bedrooms" in field_names or any("chambre" in str(f) for f in field_names)
        assert "city" in field_names or "district" in field_names
        assert "max_budget" in field_names or "move_in_date" in field_names

        profile = _make_profile(project_id=new_project_id)
        for cand in extraction.candidates:
            profile.set_field(cand.field_name, cand.proposed_value, confidence=cand.confidence)

        assert profile.fields.get("property_type", None) is not None

        qual_engine = _make_qual_engine(registry)
        handover_eval = HumanHandoverEvaluator()
        decision_engine = DecisionEngine(registry)
        brain = ProjectBrain(qual_engine, decision_engine, handover_eval)

        qual_result, decision, brain_state = brain.evaluate(profile, text)

        assert brain_state.project_id == new_project_id
        assert decision.selected_action in ("ASK_MISSING_FIELD", "START_MATCHING", "INSUFFICIENT_DATA")

        plan = InteractionResponsePlan(
            project_id=new_project_id,
            correlation_id=env.correlation_id,
            response_type=ResponseType.ASK_MISSING_FIELD if decision.selected_action == "ASK_MISSING_FIELD" else ResponseType.WAIT,
            selected_field=decision.selected_field or "",
            decision_id=decision.decision_id,
            structured_facts={"decision": decision.selected_action},
        )

        write_req = ResponseWriterRequest(response_plan=plan)
        write_result = writer.write(write_req)
        assert write_result.success

        delivery_result = delivery.deliver(plan, env.channel)
        assert delivery_result.status in (DeliveryStatus.SENT, DeliveryStatus.CANCELLED)


# ---------------------------------------------------------------------------
# E2E-02: Multiturn
# ---------------------------------------------------------------------------

class TestE2E02Multiturn:

    def test_multiturn_builds_profile(self):
        gateway = InteractionGateway()
        normalizer = MessageNormalizer()
        identity = IdentityResolver()
        sessions = SessionManager()
        projects = ProjectResolver()
        extractor = DeterministicExtractor()
        writer = DeterministicResponseWriter()
        registry = _make_field_registry()

        user_id = "e2e-user-002"
        project_id = "e2e-proj-002"
        identity.link_channel_to_user(user_id, "whatsapp", "+237600002")
        projects.register_project(user_id, project_id)

        turns = [
            "Bonjour",
            "Je cherche un studio à Douala",
            "\u00c0 Makepe",
            "Mon budget est de 80 000 FCFA",
            "Je veux entrer en septembre",
            "Je suis disponible samedi",
        ]

        profile = _make_profile(project_id=project_id)
        previous_session_id = None

        for i, turn_text in enumerate(turns):
            env = gateway.prepare_envelope(
                channel="whatsapp",
                external_message_id=f"e2e-02-msg-{i:03d}",
                external_user_id="+237600002",
                raw_sender="+237600002",
                raw_content=turn_text,
            )

            id_result = identity.resolve(env.channel, env.external_user_id, env.raw_sender)
            assert id_result.status == IdentityStatus.RESOLVED
            assert id_result.actor_id == user_id

            session = sessions.resume_or_create(user_id, env.channel)
            if previous_session_id is not None:
                assert session.session_id == previous_session_id
            previous_session_id = session.session_id

            proj_result = projects.resolve(user_id)
            assert proj_result.project_id == project_id

            extraction = extractor.extract(turn_text, project_id=project_id)
            for cand in extraction.candidates:
                profile.set_field(cand.field_name, cand.proposed_value, confidence=cand.confidence)

        assert profile.fields.get("property_type") is not None
        assert profile.fields.get("city") is not None or profile.fields.get("district") is not None
        assert profile.fields.get("max_budget") is not None

        max_budget_field = profile.fields.get("max_budget")
        if max_budget_field:
            assert float(max_budget_field.value) == 80_000


# ---------------------------------------------------------------------------
# E2E-03: Session Resume
# ---------------------------------------------------------------------------

class TestE2E03SessionResume:

    def test_session_expiry_and_resume(self):
        identity = IdentityResolver()
        sessions = SessionManager(timeout_minutes=0)
        projects = ProjectResolver()

        user_id = "e2e-user-003"
        project_id = "e2e-proj-003"
        identity.link_channel_to_user(user_id, "whatsapp", "+237600003")
        projects.register_project(user_id, project_id)

        session1 = sessions.resume_or_create(user_id, "whatsapp")
        assert session1.status == SessionStatus.ACTIVE

        session1.last_activity_at = "2020-01-01T00:00:00+00:00"

        session2 = sessions.get_session(session1.session_id)
        assert session2 is not None
        assert session2.status == SessionStatus.EXPIRED

        session3 = sessions.resume_or_create(user_id, "whatsapp")
        assert session3.session_id != session1.session_id

        proj_result = projects.resolve(user_id)
        assert proj_result.project_id == project_id


# ---------------------------------------------------------------------------
# E2E-04: Multichannel Continuity
# ---------------------------------------------------------------------------

class TestE2E04Multichannel:

    def test_same_user_multichannel(self):
        identity = IdentityResolver()
        sessions = SessionManager()
        projects = ProjectResolver()
        extractor = DeterministicExtractor()

        user_id = "e2e-user-004"
        project_id = "e2e-proj-004"
        identity.link_channel_to_user(user_id, "whatsapp", "+237600004")
        identity.link_channel_to_user(user_id, "telegram", "tg-004")

        profile = _make_profile(project_id=project_id)
        projects.register_project(user_id, project_id)

        env_wa = InteractionEnvelope(
            channel="whatsapp",
            external_message_id="wa-msg-001",
            external_user_id="+237600004",
            raw_sender="+237600004",
            raw_content="Je cherche un appartement \u00e0 Douala",
        )
        id_wa = identity.resolve(env_wa.channel, env_wa.external_user_id, env_wa.raw_sender)
        assert id_wa.status == IdentityStatus.RESOLVED
        assert id_wa.actor_id == user_id

        session_wa = sessions.resume_or_create(user_id, "whatsapp")

        extraction_wa = extractor.extract(env_wa.raw_content, project_id=project_id)
        for c in extraction_wa.candidates:
            profile.set_field(c.field_name, c.proposed_value)

        env_tg = InteractionEnvelope(
            channel="telegram",
            external_message_id="tg-msg-001",
            external_user_id="tg-004",
            raw_sender="tg-004",
            raw_content="Mon budget est de 150 000 FCFA",
        )
        id_tg = identity.resolve(env_tg.channel, env_tg.external_user_id, env_tg.raw_sender)
        assert id_tg.status == IdentityStatus.RESOLVED
        assert id_tg.actor_id == user_id

        session_tg = sessions.resume_or_create(user_id, "telegram")
        assert session_tg.user_id == user_id

        extraction_tg = extractor.extract(env_tg.raw_content, project_id=project_id)
        for c in extraction_tg.candidates:
            profile.set_field(c.field_name, c.proposed_value)

        assert profile.fields.get("max_budget") is not None

        proj_check = projects.resolve(user_id)
        assert proj_check.project_id == project_id


    def test_multichannel_unconfirmed_identity(self):
        identity = IdentityResolver()

        identity.link_channel_to_user("e2e-user-005", "whatsapp", "+237600005")

        env_wa = InteractionEnvelope(
            channel="whatsapp",
            external_message_id="wa-msg-002",
            external_user_id="+237600005",
            raw_sender="+237600005",
            raw_content="test",
        )
        id_wa = identity.resolve(env_wa.channel, env_wa.external_user_id, env_wa.raw_sender)
        assert id_wa.status == IdentityStatus.RESOLVED

        env_tg = InteractionEnvelope(
            channel="telegram",
            external_message_id="tg-msg-002",
            external_user_id="tg-005",
            raw_sender="tg-005",
            raw_content="test",
        )
        id_tg = identity.resolve(env_tg.channel, env_tg.external_user_id, env_tg.raw_sender)
        assert id_tg.status == IdentityStatus.ANONYMOUS
        assert id_tg.actor_id != id_wa.actor_id


# ---------------------------------------------------------------------------
# E2E-05: Matching Success
# ---------------------------------------------------------------------------

class TestE2E05MatchingSuccess:

    def test_matching_with_sufficient_data(self):
        matching = MatchingRuntime()
        matching.load_properties([
            {"property_id": "prop-001", "property_type": "apartment", "bedrooms": 3, "price": 90_000, "city": "Yaounde", "district": "Biyem-Assi", "features": ["balcony", "parking"]},
            {"property_id": "prop-002", "property_type": "apartment", "bedrooms": 4, "price": 95_000, "city": "Yaounde", "district": "Biyem-Assi", "features": ["balcony", "pool"]},
            {"property_id": "prop-003", "property_type": "house", "bedrooms": 4, "price": 150_000, "city": "Yaounde", "district": "Mvan", "features": ["garden", "parking"]},
        ])

        request = DomainRuntimeRequest(
            action_code="START_MATCHING",
            parameters={
                "property_type": "apartment",
                "bedrooms": 4,
                "city": "Yaounde",
                "district": "Biyem-Assi",
                "max_budget": 100_000,
            },
            correlation_id="corr-match-001",
        )

        result = matching.execute(request)
        assert result.status == DomainRuntimeStatus.SUCCEEDED, f"matching failed: {result.error}"
        output = result.output
        assert output["status"] == MatchingStatus.MATCH_FOUND.value
        assert output["total_count"] >= 1
        matches = output.get("matches", [])
        assert all("property_id" in m for m in matches)
        prop_002 = [m for m in matches if m["property_id"] == "prop-002"]
        prop_003 = [m for m in matches if m["property_id"] == "prop-003"]
        assert len(prop_002) == 1
        assert prop_002[0]["score"] >= 80
        if prop_003:
            assert prop_003[0]["score"] < prop_002[0]["score"]


# ---------------------------------------------------------------------------
# E2E-06: Matching Insufficient Data
# ---------------------------------------------------------------------------

class TestE2E06MatchingInsufficient:

    def test_insufficient_data(self):
        matching = MatchingRuntime()
        request = DomainRuntimeRequest(
            action_code="START_MATCHING",
            parameters={"city": "Yaounde"},
            correlation_id="corr-insuf-001",
        )

        result = matching.execute(request)
        assert "INSUFFICIENT_DATA" in result.error, f"expected INSUFFICIENT_DATA error, got: {result.error}"

        insufficient = matching._execute_check_insufficient_data({"city": "Yaounde"})
        assert insufficient is not None
        assert insufficient["status"] == MatchingStatus.INSUFFICIENT_DATA.value
        assert "missing_fields" in insufficient
        assert len(insufficient["missing_fields"]) >= 2
        assert insufficient["matching_not_started"] is True


# ---------------------------------------------------------------------------
# E2E-07: Visit
# ---------------------------------------------------------------------------

class TestE2E07Visit:

    def test_visit_full_flow(self):
        visit = VisitRuntime()
        prop_id = "prop-visit-e2e-001"

        create_req = DomainRuntimeRequest(
            action_code="CREATE_VISIT_REQUEST",
            parameters={
                "property_id": prop_id,
                "requester_name": "Jean Dupont",
                "requester_contact": "+237600000",
            },
            idempotency_key="visit-001",
        )
        create_result = visit.execute(create_req)
        assert create_result.status == DomainRuntimeStatus.SUCCEEDED, f"create failed: {create_result.error}"
        visit_id = create_result.output.get("visit_id", "")
        assert visit_id

        schedule_req = DomainRuntimeRequest(
            action_code="SCHEDULE_VISIT",
            parameters={
                "visit_id": visit_id,
                "property_id": prop_id,
                "scheduled_date": "2026-07-25T10:00:00",
            },
        )
        sched_result = visit.execute(schedule_req)
        assert sched_result.status == DomainRuntimeStatus.SUCCEEDED, f"schedule failed: {sched_result.error}"
        assert sched_result.output.get("status") == VisitStatus.SCHEDULED.value

        confirm_req = DomainRuntimeRequest(
            action_code="CONFIRM_VISIT",
            parameters={"visit_id": visit_id},
        )
        confirm_result = visit.execute(confirm_req)
        assert confirm_result.status == DomainRuntimeStatus.SUCCEEDED
        assert confirm_result.output.get("status") == VisitStatus.CONFIRMED.value

        complete_req = DomainRuntimeRequest(
            action_code="COMPLETE_VISIT",
            parameters={"visit_id": visit_id},
        )
        complete_result = visit.execute(complete_req)
        assert complete_result.status == DomainRuntimeStatus.SUCCEEDED
        assert complete_result.output.get("status") == VisitStatus.COMPLETED.value

        cancel_req2 = DomainRuntimeRequest(
            action_code="CANCEL_VISIT",
            parameters={"visit_id": visit_id},
        )
        cancel_result = visit.execute(cancel_req2)
        assert cancel_result.output.get("status") == VisitStatus.FAILED.value


# ---------------------------------------------------------------------------
# E2E-08: Handover
# ---------------------------------------------------------------------------

class TestE2E08Handover:

    def test_handover_evaluation_no_false_positive(self):
        registry = _make_field_registry()
        qual_engine = _make_qual_engine(registry)
        handover_eval = HumanHandoverEvaluator()
        decision_engine = DecisionEngine(registry)
        brain = ProjectBrain(qual_engine, decision_engine, handover_eval)

        profile = _make_profile(project_id="e2e-handover-001")

        _, decision, state = brain.evaluate(profile, "Je veux un appartement")

        assert decision.selected_action != "ESCALATE_TO_HUMAN"


# ---------------------------------------------------------------------------
# E2E-09: Document and Verification
# ---------------------------------------------------------------------------

class TestE2E09DocumentVerification:

    def test_document_runtime(self):
        doc_runtime = DocumentRuntime()
        doc_req = DomainRuntimeRequest(
            action_code="REGISTER_DOCUMENT",
            parameters={
                "document_id": "doc-001",
                "project_id": "proj-001",
                "document_type": "identity_card",
                "file_reference": "file-001.pdf",
            },
        )
        doc_result = doc_runtime.execute(doc_req)
        assert doc_result.status == DomainRuntimeStatus.SUCCEEDED or doc_result.status == DomainRuntimeStatus.SIMULATED

        verify = VerificationRuntime()
        verify_req = DomainRuntimeRequest(
            action_code="START_VERIFICATION",
            parameters={
                "project_id": "proj-001",
                "document_id": "doc-001",
                "verification_type": "identity",
            },
        )
        verify_result = verify.execute(verify_req)
        assert verify_result.status == DomainRuntimeStatus.SUCCEEDED or verify_result.status == DomainRuntimeStatus.SIMULATED, f"verify: {verify_result.error}"


# ---------------------------------------------------------------------------
# E2E-10: Transaction Preconditions
# ---------------------------------------------------------------------------

class TestE2E10TransactionPreconditions:

    def test_transaction_refuses_without_preconditions(self):
        tx = TransactionRuntime()
        req = DomainRuntimeRequest(
            action_code="PREPARE_TRANSACTION",
            parameters={
                "property_id": "prop-001",
                "buyer_id": "user-001",
                "transaction_type": "rental",
            },
        )
        result = tx.execute(req)
        assert result.status == DomainRuntimeStatus.FAILED


# ---------------------------------------------------------------------------
# E2E-11: Payment Idempotency
# ---------------------------------------------------------------------------

class TestE2E11PaymentIdempotency:

    def test_payment_no_double_execution(self):
        pay = PaymentRuntime()
        req = DomainRuntimeRequest(
            action_code="CREATE_PAYMENT_INTENT",
            parameters={
                "project_id": "proj-pay-001",
                "transaction_id": "tx-001",
                "amount": 100_000,
                "currency": "XAF",
                "payment_method": "mobile_money",
            },
            idempotency_key="pay-e2e-001",
            correlation_id="corr-pay-001",
        )

        result1 = pay.execute(req)
        result2 = pay.execute(req)

        assert result1.status == DomainRuntimeStatus.SUCCEEDED or result1.status == DomainRuntimeStatus.SIMULATED, f"first pay: {result1.error}"
        intent_id_1 = result1.output.get("payment_intent_id", "")
        intent_id_2 = result2.output.get("payment_intent_id", "")
        assert intent_id_1 == intent_id_2 or not intent_id_2


# ---------------------------------------------------------------------------
# Complete Orchestration flow with full pipeline
# ---------------------------------------------------------------------------

class TestE2EIntegrationFullPipeline:

    def test_full_integration_pipeline(self):
        text = "Je cherche un appartement de 4 chambres \\u00e0 Biyem-Assi, Yaound\u00e9, avec un budget maximum de 100 000 FCFA, pour septembre."

        registry = _make_field_registry()
        identity = IdentityResolver()
        sessions = SessionManager()
        projects = ProjectResolver()
        normalizer = MessageNormalizer()
        dedup = InteractionDeduplicator()
        correlation = CorrelationManager()
        gateway = InteractionGateway()
        delivery = DeliveryManager()
        extractor = DeterministicExtractor()
        writer = DeterministicResponseWriter()
        metrics = InteractionMetrics()

        user_id = "e2e-user-full-001"
        project_id = "e2e-proj-full-001"
        identity.link_channel_to_user(user_id, "whatsapp", "+237600999")

        metrics.interaction_received_total += 1

        env = gateway.prepare_envelope(
            channel="whatsapp",
            external_message_id="e2e-full-msg-001",
            external_user_id="+237600999",
            raw_sender="+237600999",
            raw_content=text,
        )
        assert gateway.validate_envelope(env).valid

        metrics.interaction_processed_total += 1

        assert dedup.check(env.external_message_id, env.channel) == DeduplicationStatus.NEW

        norm = normalizer.normalize(env.raw_content)
        assert not norm.is_empty

        id_result = identity.resolve(env.channel, env.external_user_id, env.raw_sender)
        assert id_result.status == IdentityStatus.RESOLVED
        metrics.identity_resolution_total += 1

        session = sessions.resume_or_create(user_id, env.channel)
        metrics.session_created_total += 1

        proj_result = projects.resolve(user_id)
        assert proj_result.status == ProjectResolutionStatus.NEW_PROJECT

        projects.register_project(user_id, project_id)
        profile = _make_profile(project_id=project_id)
        metrics.project_resolution_total += 1

        extraction = extractor.extract(text, project_id=project_id)
        candidates = extraction.candidates

        for cand in candidates:
            profile.set_field(cand.field_name, cand.proposed_value, confidence=cand.confidence)
        metrics.profile_patch_created_total += 1

        qual_engine = _make_qual_engine(registry)
        decision_engine = DecisionEngine(registry)
        handover_eval = HumanHandoverEvaluator()
        brain = ProjectBrain(qual_engine, decision_engine, handover_eval)

        qual_result, decision, brain_state = brain.evaluate(profile, text)

        if decision.selected_action == "START_MATCHING":
            matching = MatchingRuntime()
            matching.load_properties([
                {"property_id": "prop-e2e-001", "property_type": "apartment", "bedrooms": 4, "price": 95_000, "city": "Yaound\u00e9", "district": "Biyem-Assi"},
                {"property_id": "prop-e2e-002", "property_type": "apartment", "bedrooms": 3, "price": 80_000, "city": "Yaound\u00e9", "district": "Biyem-Assi"},
            ])
            match_req = DomainRuntimeRequest(
                action_code="START_MATCHING",
                parameters={
                    "property_type": "apartment",
                    "bedrooms": 4,
                    "city": "Yaound\u00e9",
                    "max_budget": 100_000,
                },
                correlation_id=env.correlation_id,
            )
            match_result = matching.execute(match_req)
            assert match_result.output.get("status") == MatchingStatus.MATCH_FOUND.value

        metrics.response_plan_created_total += 1
        plan = InteractionResponsePlan(
            project_id=project_id,
            decision_id=decision.decision_id,
            response_type=ResponseType.PRESENT_RESULTS if decision.selected_action == "START_MATCHING" else ResponseType.ASK_MISSING_FIELD,
            selected_field=decision.selected_field or "",
            correlation_id=env.correlation_id,
        )

        metrics.delivery_requested_total += 1
        delivery_result = delivery.deliver(plan, env.channel)
        if delivery_result.status == DeliveryStatus.SENT:
            metrics.delivery_sent_total += 1

        assert delivery_result.status in (DeliveryStatus.SENT, DeliveryStatus.CANCELLED)

        metrics_snapshot = metrics.snapshot()
        assert metrics_snapshot["interaction_received_total"] >= 1
        assert metrics_snapshot["interaction_processed_total"] >= 1


# ---------------------------------------------------------------------------
# Concurrent updates
# ---------------------------------------------------------------------------

class TestE2EConcurrentUpdates:

    def test_two_simultaneous_updates_no_loss(self):
        profile = _make_profile(project_id="e2e-concur-001")
        profile.set_field("city", "Douala")
        profile.set_field("min_budget", 50_000)
        profile.set_field("city", "Yaound\u00e9")
        profile.set_field("min_budget", 80_000)

        assert profile.fields["city"].value == "Yaound\u00e9"
        assert profile.fields["min_budget"].value == 80_000


# ---------------------------------------------------------------------------
# Project ambiguity isolation
# ---------------------------------------------------------------------------

class TestE2EProjectAmbiguity:

    def test_multiple_active_projects_no_merge(self):
        user_id = "e2e-user-ambig"
        projects = ProjectResolver()
        projects.register_project(user_id, "proj-rental-001")
        projects.register_project(user_id, "proj-purchase-001")

        result = projects.resolve(user_id)
        assert result.status == ProjectResolutionStatus.AMBIGUOUS
        assert result.active_project_count == 2


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

class TestE2EDeduplication:

    def test_duplicate_webhook(self):
        dedup = InteractionDeduplicator()
        msg_id = "dup-msg-001"

        c1 = dedup.check(msg_id, "whatsapp")
        assert c1 == DeduplicationStatus.NEW

        c2 = dedup.check(msg_id, "whatsapp")
        assert c2 == DeduplicationStatus.DUPLICATE


# ---------------------------------------------------------------------------
# V2/V3 Routing
# ---------------------------------------------------------------------------

class TestE2ERouting:

    def test_v2_only(self):
        router = InteractionModeRouter(mode=InteractionMode.V2_ONLY)
        assert router.resolve_mode() == InteractionMode.V2_ONLY
        assert not router.is_v3_active()

    def test_v3_shadow(self):
        router = InteractionModeRouter(mode=InteractionMode.V3_SHADOW)
        assert router.is_v3_active()
        assert router.is_shadow()

    def test_v3_canary_by_user(self):
        router = InteractionModeRouter(
            mode=InteractionMode.V3_CANARY,
            canary_users={"canary-user-001"},
        )
        assert router.resolve_mode(user_id="canary-user-001") == InteractionMode.V3_CANARY
        assert router.resolve_mode(user_id="normal-user") == InteractionMode.V2_ONLY

    def test_v3_primary_with_v2_fallback(self):
        router = InteractionModeRouter(mode=InteractionMode.V3_PRIMARY_WITH_V2_FALLBACK)
        assert router.is_v3_active()

    def test_v3_only(self):
        router = InteractionModeRouter(mode=InteractionMode.V3_ONLY)
        assert router.is_v3_active()
        assert not router.is_shadow()


# ---------------------------------------------------------------------------
# Divergence analysis
# ---------------------------------------------------------------------------

class TestE2EDivergence:

    def test_divergence_detection(self):
        analyzer = InteractionDivergenceAnalyzer()
        divergences = analyzer.compare(
            interaction_id="int-001",
            correlation_id="corr-001",
            channel="whatsapp",
            v2_result={"resolved_identity": "user-a", "next_action": "ASK_MISSING_FIELD", "response_type": "text"},
            v3_result={"resolved_identity": "user-b", "next_action": "START_MATCHING", "response_type": "text"},
        )
        assert len(divergences) >= 2


# ---------------------------------------------------------------------------
# Metrics verification
# ---------------------------------------------------------------------------

class TestE2EMetrics:

    def test_metrics_counters(self):
        metrics = InteractionMetrics()
        metrics.interaction_received_total = 10
        metrics.interaction_processed_total = 8
        metrics.interaction_failed_total = 1
        metrics.interaction_duplicate_total = 1
        metrics.delivery_sent_total = 7
        metrics.delivery_failed_total = 1
        metrics.safe_fallback_total = 1

        snap = metrics.snapshot()
        assert snap["interaction_received_total"] == 10
        assert snap["interaction_duplicate_total"] == 1
        assert snap["safe_fallback_total"] == 1

        metrics.reset()
        assert metrics.interaction_received_total == 0


# ---------------------------------------------------------------------------
# Correlation trace
# ---------------------------------------------------------------------------

class TestE2ECorrelation:

    def test_correlation_trace(self):
        corr = CorrelationManager()
        cid = corr.create("e2e-trace-001")
        corr.update(cid, interaction_id="int-001", session_id="sess-001", project_id="proj-001")

        trace = corr.trace(cid)
        assert trace is not None
        assert trace.interaction_id == "int-001"
        assert trace.project_id == "proj-001"
        assert trace.correlation_id == "e2e-trace-001"


# ---------------------------------------------------------------------------
# Visit transitions verification
# ---------------------------------------------------------------------------

class TestE2EVisitTransitions:

    def _create_and_schedule(self, visit: VisitRuntime, prop_id: str, key: str) -> str:
        create = visit.execute(DomainRuntimeRequest(
            action_code="CREATE_VISIT_REQUEST",
            parameters={"property_id": prop_id, "requester_name": "Test"},
            idempotency_key=key,
        ))
        vid = create.output.get("visit_id", "")
        schedule = visit.execute(DomainRuntimeRequest(
            action_code="SCHEDULE_VISIT",
            parameters={"visit_id": vid, "property_id": prop_id, "scheduled_date": "2026-07-25"},
        ))
        assert schedule.status == DomainRuntimeStatus.SUCCEEDED, f"schedule: {schedule.error}"
        return vid

    def test_all_transitions(self):
        visit = VisitRuntime()
        vid = self._create_and_schedule(visit, "prop-t-001", "vt-001")

        confirm = visit.execute(DomainRuntimeRequest(
            action_code="CONFIRM_VISIT",
            parameters={"visit_id": vid},
        ))
        assert confirm.status == DomainRuntimeStatus.SUCCEEDED
        assert confirm.output.get("status") == VisitStatus.CONFIRMED.value

        complete = visit.execute(DomainRuntimeRequest(
            action_code="COMPLETE_VISIT",
            parameters={"visit_id": vid},
        ))
        assert complete.status == DomainRuntimeStatus.SUCCEEDED
        assert complete.output.get("status") == VisitStatus.COMPLETED.value

    def test_no_show_transition(self):
        visit = VisitRuntime()
        vid = self._create_and_schedule(visit, "prop-ns-001", "vt-ns-001")

        no_show = visit.execute(DomainRuntimeRequest(
            action_code="NO_SHOW_VISIT",
            parameters={"visit_id": vid},
        ))
        assert no_show.status == DomainRuntimeStatus.SUCCEEDED
        assert no_show.output.get("status") == VisitStatus.NO_SHOW.value

    def test_reschedule_transition(self):
        visit = VisitRuntime()
        vid = self._create_and_schedule(visit, "prop-rs-001", "vt-rs-001")

        resched = visit.execute(DomainRuntimeRequest(
            action_code="RESCHEDULE_VISIT",
            parameters={"visit_id": vid, "scheduled_date": "2026-07-28"},
        ))
        assert resched.status == DomainRuntimeStatus.SUCCEEDED
        assert resched.output.get("status") == VisitStatus.SCHEDULED.value
        assert resched.output.get("scheduled_date") == "2026-07-28"
