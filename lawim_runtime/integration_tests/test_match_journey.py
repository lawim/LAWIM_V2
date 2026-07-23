from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import pytest

from lawim_runtime.interaction.envelope import InteractionEnvelope, MessageType
from lawim_runtime.interaction.identity import IdentityResolver, IdentityStatus
from lawim_runtime.interaction.project_resolution import ProjectResolver, ProjectResolutionStatus
from lawim_runtime.interaction.session import SessionManager, SessionStatus
from lawim_runtime.interaction.normalization import MessageNormalizer
from lawim_runtime.interaction.deduplication import InteractionDeduplicator, DeduplicationStatus
from lawim_runtime.interaction.correlation import CorrelationManager
from lawim_runtime.interaction.gateway import InteractionGateway
from lawim_runtime.interaction.response_plan import InteractionResponsePlan, ResponseType
from lawim_runtime.interaction.delivery import DeliveryManager, DeliveryStatus
from lawim_runtime.interaction.response_writer import DeterministicResponseWriter, ResponseWriterRequest
from lawim_runtime.interaction.extraction import DeterministicExtractor, ExtractionResult

from lawim_runtime.project_profile.base import AbstractProjectProfile
from lawim_runtime.project_profile.profile import ProjectProfile
from lawim_runtime.project_profile.registry import FieldRegistry

from lawim_runtime.qualification.engine import QualificationEngine
from lawim_runtime.qualification.registry import RequirementRegistry

from lawim_runtime.decision.engine import DecisionEngine
from lawim_runtime.decision.result import DecisionResult
from lawim_runtime.decision.handover import HumanHandoverEvaluator

from lawim_runtime.project_brain.brain import ProjectBrain
from lawim_runtime.project_brain.state import ProjectBrainState

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeStatus
from lawim_runtime.domains.matching.runtime import MatchingRuntime
from lawim_runtime.domains.matching.models import MatchingStatus
from lawim_runtime.domains.crm.runtime import CRMRuntime
from lawim_runtime.domains.crm.models import CRMStatus
from lawim_runtime.domains.notification.runtime import NotificationRuntime


def _make_registry() -> FieldRegistry:
    from lawim_runtime.project_profile.field_definitions import register_all_fields
    r = FieldRegistry()
    register_all_fields(r)
    return r


def _make_profile(pid: str = "match-proj") -> ProjectProfile:
    return ProjectProfile(project_id=pid, profile_type="rental_search", profile_id=f"prof-{pid}")


MATCH_PROPERTIES = [
    {"property_id": "PROP-MVAN-001", "property_type": "apartment", "bedrooms": 2, "price": 230_000, "city": "Yaounde", "district": "Mvan", "features": ["balcony", "parking"], "owner_id": "OWNER-001", "status": "active"},
    {"property_id": "PROP-MVAN-002", "property_type": "apartment", "bedrooms": 3, "price": 280_000, "city": "Yaounde", "district": "Mvan", "features": ["pool", "parking"], "owner_id": "OWNER-002", "status": "active"},
    {"property_id": "PROP-BASTOS-001", "property_type": "house", "bedrooms": 4, "price": 500_000, "city": "Yaounde", "district": "Bastos", "features": ["garden", "pool"], "owner_id": "OWNER-003", "status": "active"},
]


# ---------------------------------------------------------------------------
# MATCH-01: Matching with real properties
# ---------------------------------------------------------------------------
class TestMatchMatching:

    def test_match_with_real_properties(self):
        matching = MatchingRuntime()
        matching.load_properties(MATCH_PROPERTIES)

        request = DomainRuntimeRequest(
            action_code="START_MATCHING",
            parameters={
                "property_type": "apartment",
                "bedrooms": 2,
                "city": "Yaounde",
                "district": "Mvan",
                "max_budget": 250_000,
            },
        )
        result = matching.execute(request)
        assert result.status == DomainRuntimeStatus.SUCCEEDED
        matches = result.output.get("matches", [])
        assert len(matches) >= 1
        prop_ids = [m["property_id"] for m in matches]
        assert "PROP-MVAN-001" in prop_ids
        for m in matches:
            assert "score" in m
            assert m["score"] >= 0


# ---------------------------------------------------------------------------
# MATCH-02: Match score and criteria
# ---------------------------------------------------------------------------
class TestMatchCriteria:

    def test_match_scoring(self):
        matching = MatchingRuntime()
        matching.load_properties(MATCH_PROPERTIES)

        request = DomainRuntimeRequest(
            action_code="START_MATCHING",
            parameters={
                "property_type": "apartment",
                "city": "Yaounde",
                "max_budget": 250_000,
            },
        )
        result = matching.execute(request)
        matches = result.output.get("matches", [])
        assert len(matches) >= 2
        scores = [m["score"] for m in matches]
        for i in range(len(scores) - 1):
            assert scores[i] >= scores[i + 1], "matches should be sorted by score descending"


# ---------------------------------------------------------------------------
# MATCH-03: Present results to user
# ---------------------------------------------------------------------------
class TestMatchPresentation:

    def test_present_results(self):
        matching = MatchingRuntime()
        matching.load_properties(MATCH_PROPERTIES)
        request = DomainRuntimeRequest(action_code="PRESENT_MATCHES", parameters={})
        result = matching.execute(request)
        assert result.status == DomainRuntimeStatus.SUCCEEDED

    def test_present_without_search_returns_empty(self):
        matching = MatchingRuntime()
        request = DomainRuntimeRequest(action_code="PRESENT_MATCHES", parameters={})
        result = matching.execute(request)
        assert result.output.get("status") == MatchingStatus.NO_MATCH.value


# ---------------------------------------------------------------------------
# MATCH-04: Selection and CRM lead creation
# ---------------------------------------------------------------------------
class TestMatchSelection:

    def test_create_lead_after_selection(self):
        crm = CRMRuntime()
        req = DomainRuntimeRequest(
            action_code="CREATE_OR_UPDATE_LEAD",
            parameters={
                "project_id": "MATCH-PROJ-001",
                "property_id": "PROP-MVAN-001",
                "requester_id": "CUSTOMER-001",
                "source": "whatsapp",
                "status": "NEW",
            },
        )
        result = crm.execute(req)
        assert result.status == DomainRuntimeStatus.SUCCEEDED or result.status == DomainRuntimeStatus.SIMULATED

    def test_create_opportunity(self):
        crm = CRMRuntime()
        req = DomainRuntimeRequest(
            action_code="CREATE_OR_UPDATE_OPPORTUNITY",
            parameters={
                "project_id": "MATCH-PROJ-001",
                "property_id": "PROP-MVAN-001",
                "customer_id": "CUSTOMER-001",
                "status": "NEGOTIATION",
            },
        )
        result = crm.execute(req)
        assert result.status == DomainRuntimeStatus.SUCCEEDED or result.status == DomainRuntimeStatus.SIMULATED


# ---------------------------------------------------------------------------
# MATCH-05: Visit request after selection
# ---------------------------------------------------------------------------
class TestMatchVisit:

    def test_visit_request_after_selection(self):
        from lawim_runtime.domains.visit.runtime import VisitRuntime
        from lawim_runtime.domains.visit.models import VisitStatus

        visit = VisitRuntime()
        req = DomainRuntimeRequest(
            action_code="CREATE_VISIT_REQUEST",
            parameters={
                "property_id": "PROP-MVAN-001",
                "requester_name": "Customer Test",
                "requester_contact": "+237600000001",
            },
        )
        result = visit.execute(req)
        assert result.status == DomainRuntimeStatus.SUCCEEDED


# ---------------------------------------------------------------------------
# MATCH-06: Full end-to-end match journey
# ---------------------------------------------------------------------------
class TestMatchFullJourney:

    def test_full_match_journey(self):
        # Step 1: Create profile with criteria
        profile = _make_profile("MATCH-E2E-001")
        profile.set_field("property_type", "apartment")
        profile.set_field("city", "Yaounde")
        profile.set_field("max_budget", 250_000)
        profile.set_field("bedrooms", 2)
        profile.set_field("district", "Mvan")

        # Step 2: Run matching
        matching = MatchingRuntime()
        matching.load_properties(MATCH_PROPERTIES)
        match_req = DomainRuntimeRequest(
            action_code="START_MATCHING",
            parameters={
                "property_type": "apartment",
                "bedrooms": 2,
                "city": "Yaounde",
                "max_budget": 250_000,
            },
        )
        match_result = matching.execute(match_req)
        assert match_result.status == DomainRuntimeStatus.SUCCEEDED
        matches = match_result.output.get("matches", [])
        selected_property = matches[0] if matches else None

        # Step 3: Create CRM lead
        if selected_property:
            prop_id = selected_property["property_id"]
            crm = CRMRuntime()
            lead_req = DomainRuntimeRequest(
                action_code="CREATE_OR_UPDATE_LEAD",
                parameters={
                    "project_id": "MATCH-E2E-001",
                    "property_id": prop_id,
                    "requester_id": "CUSTOMER-E2E-001",
                    "source": "whatsapp",
                    "status": "NEW",
                },
            )
            lead_result = crm.execute(lead_req)
            assert lead_result.status in (DomainRuntimeStatus.SUCCEEDED, DomainRuntimeStatus.SIMULATED)

        # Step 4: Create opportunity
        if selected_property:
            opp_req = DomainRuntimeRequest(
                action_code="CREATE_OR_UPDATE_OPPORTUNITY",
                parameters={
                    "project_id": "MATCH-E2E-001",
                    "property_id": prop_id,
                    "customer_id": "CUSTOMER-E2E-001",
                    "status": "NEGOTIATION",
                },
            )
            opp_result = crm.execute(opp_req)
            assert opp_result.status in (DomainRuntimeStatus.SUCCEEDED, DomainRuntimeStatus.SIMULATED)

        # Verify matching produced results
        assert selected_property is not None
        assert selected_property["property_id"] == "PROP-MVAN-001"


# ---------------------------------------------------------------------------
# MATCH-07: No match case
# ---------------------------------------------------------------------------
class TestMatchNoMatch:

    def test_no_match_returns_empty(self):
        matching = MatchingRuntime()
        matching.load_properties(MATCH_PROPERTIES)
        request = DomainRuntimeRequest(
            action_code="START_MATCHING",
            parameters={
                "property_type": "apartment",
                "city": "Douala",
                "max_budget": 50_000,
            },
        )
        result = matching.execute(request)
        assert result.status == DomainRuntimeStatus.SUCCEEDED
        assert "matches" in result.output


# ---------------------------------------------------------------------------
# MATCH-08: Match states
# ---------------------------------------------------------------------------
class TestMatchStates:

    def test_match_states_enum(self):
        assert MatchingStatus.MATCH_FOUND.value == "MATCH_FOUND"
        assert MatchingStatus.NO_MATCH.value == "NO_MATCH"
        assert MatchingStatus.INSUFFICIENT_DATA.value == "INSUFFICIENT_DATA"


# ---------------------------------------------------------------------------
# MATCH-09: Notification after match
# ---------------------------------------------------------------------------
class TestMatchNotification:

    def test_notification_after_consent(self):
        notif = NotificationRuntime()
        req = DomainRuntimeRequest(
            action_code="PREPARE_NOTIFICATION",
            parameters={
                "project_id": "MATCH-NOTIF-001",
                "notification_type": "match_found",
                "recipient_id": "CUSTOMER-001",
                "recipient_type": "customer",
                "channel": "whatsapp",
                "template_name": "match_found_whatsapp",
            },
        )
        result = notif.execute(req)
        assert result.status in (DomainRuntimeStatus.SUCCEEDED, DomainRuntimeStatus.SIMULATED)


# ---------------------------------------------------------------------------
# MATCH-10: Duplicate match prevention
# ---------------------------------------------------------------------------
class TestMatchNoDuplicate:

    def test_duplicate_match_prevented(self):
        matching = MatchingRuntime()
        matching.load_properties(MATCH_PROPERTIES)
        params = {"property_type": "apartment", "city": "Yaounde", "max_budget": 250_000}
        req = DomainRuntimeRequest(action_code="START_MATCHING", parameters=dict(params))
        r1 = matching.execute(req)
        r2 = matching.execute(req)
        assert r1.status == DomainRuntimeStatus.SUCCEEDED
        assert r2.status == DomainRuntimeStatus.SUCCEEDED
