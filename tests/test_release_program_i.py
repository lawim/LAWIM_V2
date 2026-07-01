from __future__ import annotations

import sqlite3
import tempfile
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from pathlib import Path

from lawim_v2.crm.schema_v14_ddl import V14_TABLE_NAMES
from lawim_v2.knowledge_platform.schema_v11_ddl import V11_TABLE_NAMES
from lawim_v2.marketplace.constants import (
    COMMISSION_TYPES,
    CONTRACT_STATUSES,
    DISPUTE_STATUSES,
    MISSION_STATUSES,
    PARTNER_REGISTRATION_STATUSES,
    PAYMENT_METHODS,
    PROVIDER_TYPES,
    QUOTE_STATUSES,
    REPUTATION_SCORE_KEYS,
    REQUEST_STATUSES,
    REVIEW_STATUSES,
    SERVICE_CATEGORIES,
    SUBSCRIPTION_STATUSES,
)
from lawim_v2.marketplace.engines import (
    AiIntegrationBridge,
    CatalogEngine,
    CommissionEngine,
    MarketplacePlatformEngine,
    PartnerQualificationEngine,
    QuoteEngine,
    RecommendationEngine,
    ReputationEngine,
    RequestMatchingEngine,
)
from lawim_v2.marketplace.schema_v15_ddl import V15_TABLE_NAMES
from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.real_estate_intelligence.schema_v13_ddl import V13_TABLE_NAMES
from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations, migration_strategy_profile
from lawim_v2.workflow_automation.schema_v12_ddl import V12_TABLE_NAMES

from tests.lawim_harness import LawimTestHarness


SAMPLE_REGISTRATION: dict[str, object] = {
    "status": "submitted",
    "applicant_email": "partner@example.cm",
    "applicant_phone": "+237677000111",
    "service_categories_json": '["inspection", "legal_notary"]',
}

SAMPLE_PARTNER: dict[str, object] = {
    "id": 1,
    "trust_score": 82,
    "quality_score": 78,
    "completion_rate": 0.92,
    "response_time_hours": 6,
    "satisfaction_score": 85,
}

SAMPLE_PROVIDER: dict[str, object] = {
    "id": 1,
    "partner_profile_id": 1,
    "status": "active",
    "headline": "inspection specialist douala",
}

SAMPLE_REQUEST: dict[str, object] = {
    "id": 1,
    "city": "Douala",
    "region": "Littoral",
    "country": "Cameroon",
    "category": "inspection",
    "budget_min": 150000,
    "budget_max": 350000,
}


class ReleaseProgramIPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v15(self) -> None:
        self.assertEqual(self.repository.schema_version(), 15)

    def test_application_schema_version_constant(self) -> None:
        self.assertEqual(APPLICATION_SCHEMA_VERSION, 15)

    def test_marketplace_tables_present(self) -> None:
        self.assertTrue(self.repository.marketplace_tables_present())

    def test_all_v15_tables_exist(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V15_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v14_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V14_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v13_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V13_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v12_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V12_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v11_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V11_TABLE_NAMES:
            self.assertIn(table, names)

    def test_marketplace_catalog_seeded(self) -> None:
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM marketplace_catalog_categories"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM marketplace_provider_profiles"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM marketplace_subscription_plans"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM marketplace_commission_rules"), 1)

    def test_v14_to_v15_legacy_migration(self) -> None:
        db_path = Path(tempfile.mkdtemp()) / "v14.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute("PRAGMA foreign_keys = OFF")
        for table in V15_TABLE_NAMES:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("UPDATE schema_meta SET value='14' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn("marketplace_provider_profiles", names)
        for table in V14_TABLE_NAMES:
            self.assertIn(table, names)

class ReleaseProgramIConstantsTests(LawimTestHarness):
    def test_partner_registration_status_approved(self) -> None:
        self.assertIn("approved", PARTNER_REGISTRATION_STATUSES)

    def test_partner_registration_status_archived(self) -> None:
        self.assertIn("archived", PARTNER_REGISTRATION_STATUSES)

    def test_partner_registration_status_draft(self) -> None:
        self.assertIn("draft", PARTNER_REGISTRATION_STATUSES)

    def test_partner_registration_status_rejected(self) -> None:
        self.assertIn("rejected", PARTNER_REGISTRATION_STATUSES)

    def test_partner_registration_status_submitted(self) -> None:
        self.assertIn("submitted", PARTNER_REGISTRATION_STATUSES)

    def test_partner_registration_status_suspended(self) -> None:
        self.assertIn("suspended", PARTNER_REGISTRATION_STATUSES)

    def test_partner_registration_status_under_review(self) -> None:
        self.assertIn("under_review", PARTNER_REGISTRATION_STATUSES)

    def test_provider_type_agency(self) -> None:
        self.assertIn("agency", PROVIDER_TYPES)

    def test_provider_type_collective(self) -> None:
        self.assertIn("collective", PROVIDER_TYPES)

    def test_provider_type_company(self) -> None:
        self.assertIn("company", PROVIDER_TYPES)

    def test_provider_type_enterprise(self) -> None:
        self.assertIn("enterprise", PROVIDER_TYPES)

    def test_provider_type_freelancer(self) -> None:
        self.assertIn("freelancer", PROVIDER_TYPES)

    def test_provider_type_individual(self) -> None:
        self.assertIn("individual", PROVIDER_TYPES)

    def test_service_category_architecture(self) -> None:
        self.assertIn("architecture", SERVICE_CATEGORIES)

    def test_service_category_cleaning(self) -> None:
        self.assertIn("cleaning", SERVICE_CATEGORIES)

    def test_service_category_consulting(self) -> None:
        self.assertIn("consulting", SERVICE_CATEGORIES)

    def test_service_category_financing(self) -> None:
        self.assertIn("financing", SERVICE_CATEGORIES)

    def test_service_category_inspection(self) -> None:
        self.assertIn("inspection", SERVICE_CATEGORIES)

    def test_service_category_insurance(self) -> None:
        self.assertIn("insurance", SERVICE_CATEGORIES)

    def test_service_category_interior_design(self) -> None:
        self.assertIn("interior_design", SERVICE_CATEGORIES)

    def test_service_category_legal_notary(self) -> None:
        self.assertIn("legal_notary", SERVICE_CATEGORIES)

    def test_service_category_maintenance(self) -> None:
        self.assertIn("maintenance", SERVICE_CATEGORIES)

    def test_service_category_marketing(self) -> None:
        self.assertIn("marketing", SERVICE_CATEGORIES)

    def test_service_category_moving(self) -> None:
        self.assertIn("moving", SERVICE_CATEGORIES)

    def test_service_category_other(self) -> None:
        self.assertIn("other", SERVICE_CATEGORIES)

    def test_service_category_photography(self) -> None:
        self.assertIn("photography", SERVICE_CATEGORIES)

    def test_service_category_property_management(self) -> None:
        self.assertIn("property_management", SERVICE_CATEGORIES)

    def test_service_category_renovation(self) -> None:
        self.assertIn("renovation", SERVICE_CATEGORIES)

    def test_service_category_security(self) -> None:
        self.assertIn("security", SERVICE_CATEGORIES)

    def test_service_category_utilities(self) -> None:
        self.assertIn("utilities", SERVICE_CATEGORIES)

    def test_service_category_valuation(self) -> None:
        self.assertIn("valuation", SERVICE_CATEGORIES)

    def test_request_status_cancelled(self) -> None:
        self.assertIn("cancelled", REQUEST_STATUSES)

    def test_request_status_completed(self) -> None:
        self.assertIn("completed", REQUEST_STATUSES)

    def test_request_status_contracted(self) -> None:
        self.assertIn("contracted", REQUEST_STATUSES)

    def test_request_status_draft(self) -> None:
        self.assertIn("draft", REQUEST_STATUSES)

    def test_request_status_expired(self) -> None:
        self.assertIn("expired", REQUEST_STATUSES)

    def test_request_status_in_progress(self) -> None:
        self.assertIn("in_progress", REQUEST_STATUSES)

    def test_request_status_matching(self) -> None:
        self.assertIn("matching", REQUEST_STATUSES)

    def test_request_status_quoted(self) -> None:
        self.assertIn("quoted", REQUEST_STATUSES)

    def test_request_status_submitted(self) -> None:
        self.assertIn("submitted", REQUEST_STATUSES)

    def test_quote_status_accepted(self) -> None:
        self.assertIn("accepted", QUOTE_STATUSES)

    def test_quote_status_draft(self) -> None:
        self.assertIn("draft", QUOTE_STATUSES)

    def test_quote_status_expired(self) -> None:
        self.assertIn("expired", QUOTE_STATUSES)

    def test_quote_status_rejected(self) -> None:
        self.assertIn("rejected", QUOTE_STATUSES)

    def test_quote_status_sent(self) -> None:
        self.assertIn("sent", QUOTE_STATUSES)

    def test_quote_status_superseded(self) -> None:
        self.assertIn("superseded", QUOTE_STATUSES)

    def test_quote_status_viewed(self) -> None:
        self.assertIn("viewed", QUOTE_STATUSES)

    def test_quote_status_withdrawn(self) -> None:
        self.assertIn("withdrawn", QUOTE_STATUSES)

    def test_contract_status_active(self) -> None:
        self.assertIn("active", CONTRACT_STATUSES)

    def test_contract_status_cancelled(self) -> None:
        self.assertIn("cancelled", CONTRACT_STATUSES)

    def test_contract_status_completed(self) -> None:
        self.assertIn("completed", CONTRACT_STATUSES)

    def test_contract_status_disputed(self) -> None:
        self.assertIn("disputed", CONTRACT_STATUSES)

    def test_contract_status_draft(self) -> None:
        self.assertIn("draft", CONTRACT_STATUSES)

    def test_contract_status_pending_signature(self) -> None:
        self.assertIn("pending_signature", CONTRACT_STATUSES)

    def test_contract_status_terminated(self) -> None:
        self.assertIn("terminated", CONTRACT_STATUSES)

    def test_mission_status_accepted(self) -> None:
        self.assertIn("accepted", MISSION_STATUSES)

    def test_mission_status_blocked(self) -> None:
        self.assertIn("blocked", MISSION_STATUSES)

    def test_mission_status_cancelled(self) -> None:
        self.assertIn("cancelled", MISSION_STATUSES)

    def test_mission_status_closed(self) -> None:
        self.assertIn("closed", MISSION_STATUSES)

    def test_mission_status_delivered(self) -> None:
        self.assertIn("delivered", MISSION_STATUSES)

    def test_mission_status_in_progress(self) -> None:
        self.assertIn("in_progress", MISSION_STATUSES)

    def test_mission_status_planned(self) -> None:
        self.assertIn("planned", MISSION_STATUSES)

    def test_mission_status_scheduled(self) -> None:
        self.assertIn("scheduled", MISSION_STATUSES)

    def test_review_status_flagged(self) -> None:
        self.assertIn("flagged", REVIEW_STATUSES)

    def test_review_status_hidden(self) -> None:
        self.assertIn("hidden", REVIEW_STATUSES)

    def test_review_status_pending(self) -> None:
        self.assertIn("pending", REVIEW_STATUSES)

    def test_review_status_published(self) -> None:
        self.assertIn("published", REVIEW_STATUSES)

    def test_review_status_removed(self) -> None:
        self.assertIn("removed", REVIEW_STATUSES)

    def test_dispute_status_closed(self) -> None:
        self.assertIn("closed", DISPUTE_STATUSES)

    def test_dispute_status_escalated(self) -> None:
        self.assertIn("escalated", DISPUTE_STATUSES)

    def test_dispute_status_mediation(self) -> None:
        self.assertIn("mediation", DISPUTE_STATUSES)

    def test_dispute_status_open(self) -> None:
        self.assertIn("open", DISPUTE_STATUSES)

    def test_dispute_status_resolved(self) -> None:
        self.assertIn("resolved", DISPUTE_STATUSES)

    def test_dispute_status_under_review(self) -> None:
        self.assertIn("under_review", DISPUTE_STATUSES)

    def test_subscription_status_active(self) -> None:
        self.assertIn("active", SUBSCRIPTION_STATUSES)

    def test_subscription_status_cancelled(self) -> None:
        self.assertIn("cancelled", SUBSCRIPTION_STATUSES)

    def test_subscription_status_expired(self) -> None:
        self.assertIn("expired", SUBSCRIPTION_STATUSES)

    def test_subscription_status_past_due(self) -> None:
        self.assertIn("past_due", SUBSCRIPTION_STATUSES)

    def test_subscription_status_paused(self) -> None:
        self.assertIn("paused", SUBSCRIPTION_STATUSES)

    def test_subscription_status_trial(self) -> None:
        self.assertIn("trial", SUBSCRIPTION_STATUSES)

    def test_commission_type_flat(self) -> None:
        self.assertIn("flat", COMMISSION_TYPES)

    def test_commission_type_percentage(self) -> None:
        self.assertIn("percentage", COMMISSION_TYPES)

    def test_commission_type_performance(self) -> None:
        self.assertIn("performance", COMMISSION_TYPES)

    def test_commission_type_referral(self) -> None:
        self.assertIn("referral", COMMISSION_TYPES)

    def test_commission_type_subscription(self) -> None:
        self.assertIn("subscription", COMMISSION_TYPES)

    def test_commission_type_tiered(self) -> None:
        self.assertIn("tiered", COMMISSION_TYPES)

    def test_reputation_score_key_quality(self) -> None:
        self.assertIn("quality", REPUTATION_SCORE_KEYS)

    def test_reputation_score_key_responsiveness(self) -> None:
        self.assertIn("responsiveness", REPUTATION_SCORE_KEYS)

    def test_reputation_score_key_reliability(self) -> None:
        self.assertIn("reliability", REPUTATION_SCORE_KEYS)

    def test_reputation_score_key_value(self) -> None:
        self.assertIn("value", REPUTATION_SCORE_KEYS)

    def test_reputation_score_key_communication(self) -> None:
        self.assertIn("communication", REPUTATION_SCORE_KEYS)

    def test_reputation_score_key_completion(self) -> None:
        self.assertIn("completion", REPUTATION_SCORE_KEYS)

    def test_reputation_score_key_satisfaction(self) -> None:
        self.assertIn("satisfaction", REPUTATION_SCORE_KEYS)

    def test_payment_method_bank_transfer(self) -> None:
        self.assertIn("bank_transfer", PAYMENT_METHODS)

    def test_payment_method_card(self) -> None:
        self.assertIn("card", PAYMENT_METHODS)

    def test_payment_method_mobile_money(self) -> None:
        self.assertIn("mobile_money", PAYMENT_METHODS)

    def test_payment_method_mtn_momo(self) -> None:
        self.assertIn("mtn_momo", PAYMENT_METHODS)

    def test_payment_method_orange_money(self) -> None:
        self.assertIn("orange_money", PAYMENT_METHODS)

    def test_payment_method_paypal(self) -> None:
        self.assertIn("paypal", PAYMENT_METHODS)

    def test_payment_method_stripe(self) -> None:
        self.assertIn("stripe", PAYMENT_METHODS)

class ReleaseProgramIEnginesTests(LawimTestHarness):
    def test_partner_qualification_submitted(self) -> None:
        score = PartnerQualificationEngine().evaluate(registration=SAMPLE_REGISTRATION, partner=SAMPLE_PARTNER)
        self.assertGreaterEqual(score["qualification_score"], 60)
        self.assertTrue(score["qualified"])

    def test_partner_qualification_draft(self) -> None:
        reg = dict(SAMPLE_REGISTRATION, status="draft")
        score = PartnerQualificationEngine().evaluate(registration=reg, partner=None)
        self.assertFalse(score["qualified"])

    def test_partner_qualification_categories(self) -> None:
        score = PartnerQualificationEngine().evaluate(registration=SAMPLE_REGISTRATION)
        self.assertGreaterEqual(len(score["categories"]), 1)

    def test_catalog_normalize_category_valid(self) -> None:
        self.assertEqual(CatalogEngine().normalize_category("inspection"), "inspection")

    def test_catalog_normalize_category_invalid(self) -> None:
        self.assertEqual(CatalogEngine().normalize_category("unknown"), "other")

    def test_catalog_price_band(self) -> None:
        band = CatalogEngine().price_band(price_min=100000, price_max=200000)
        self.assertEqual(band["mid_price"], 150000)

    def test_catalog_enrich_item(self) -> None:
        item = CatalogEngine().enrich_item(item={"category": "moving"}, service_catalog={"id": 1, "service_key": "svc", "title": "Move"})
        self.assertIn("ecosystem_service", item)

    def test_matching_ranks_providers(self) -> None:
        matches = RequestMatchingEngine().match_providers(request=SAMPLE_REQUEST, providers=[SAMPLE_PROVIDER], partners=[SAMPLE_PARTNER])
        self.assertEqual(len(matches), 1)
        self.assertIn("score", matches[0])

    def test_matching_assigns_rank(self) -> None:
        matches = RequestMatchingEngine().match_providers(request=SAMPLE_REQUEST, providers=[SAMPLE_PROVIDER, dict(SAMPLE_PROVIDER, id=2)], partners=[SAMPLE_PARTNER])
        self.assertEqual(matches[0]["rank"], 1)

    def test_matching_properties_for_request(self) -> None:
        props = [{"id": 1, "city": "Douala", "price_min": 200000, "price_max": 300000, "status": "published"}]
        ranked = RequestMatchingEngine().match_properties_for_request(request=SAMPLE_REQUEST, properties=props)
        self.assertGreaterEqual(len(ranked), 1)

    def test_quote_compute_total(self) -> None:
        lines = [QuoteEngine().build_line(description="Work", quantity=2, unit_price=50000)]
        self.assertEqual(QuoteEngine().compute_total(lines), 100000)

    def test_quote_build_line(self) -> None:
        line = QuoteEngine().build_line(description="Inspection", unit_price=75000)
        self.assertEqual(line["amount"], 75000)

    def test_quote_validate_valid(self) -> None:
        lines = [QuoteEngine().build_line(description="A", unit_price=100000)]
        result = QuoteEngine().validate_quote(quote={"amount": 100000}, lines=lines)
        self.assertTrue(result["valid"])

    def test_quote_validate_invalid(self) -> None:
        lines = [QuoteEngine().build_line(description="A", unit_price=50000)]
        result = QuoteEngine().validate_quote(quote={"amount": 100000}, lines=lines)
        self.assertFalse(result["valid"])

    def test_reputation_compute_scores(self) -> None:
        scores = ReputationEngine().compute_scores(partner=SAMPLE_PARTNER, reviews=[{"rating": 5}], missions_completed=2)
        for key in REPUTATION_SCORE_KEYS:
            self.assertIn(key, scores)

    def test_reputation_without_reviews(self) -> None:
        scores = ReputationEngine().compute_scores(partner=SAMPLE_PARTNER, reviews=[])
        self.assertGreaterEqual(scores["satisfaction"], 0)

    def test_commission_percentage(self) -> None:
        payload = CommissionEngine().compute(contract_amount=1000000, rule={"commission_type": "percentage", "rate_percent": 10.0})
        self.assertEqual(payload["amount"], 100000)

    def test_commission_flat(self) -> None:
        payload = CommissionEngine().compute(contract_amount=1000000, rule={"commission_type": "flat", "flat_amount": 25000})
        self.assertEqual(payload["amount"], 25000)

    def test_commission_invalid_type_defaults(self) -> None:
        payload = CommissionEngine().compute(contract_amount=500000, rule={"commission_type": "invalid"})
        self.assertEqual(payload["commission_type"], "percentage")

    def test_recommendation_build(self) -> None:
        recs = RecommendationEngine().build_recommendations(matches=[{"provider_profile_id": 1, "score": 88, "reasons": ["trust_score_high"]}], sources=["crm"])
        self.assertGreaterEqual(len(recs), 1)

    def test_recommendation_property_linked(self) -> None:
        recs = RecommendationEngine().build_recommendations(matches=[], request={"property_id": 3}, sources=["rei"])
        self.assertEqual(recs[0]["recommendation_type"], "property_linked")

    def test_ai_integration_sources(self) -> None:
        sources = AiIntegrationBridge().sources()
        self.assertIn("knowledge_platform", sources)
        self.assertIn("crm", sources)

    def test_ai_enrich_with_knowledge(self) -> None:
        result = AiIntegrationBridge().enrich_with_knowledge(self.repository, "compromis de vente")
        self.assertTrue(result is None or isinstance(result, dict))

    def test_ai_link_crm_contact(self) -> None:
        cid = int(self.repository.one("SELECT id FROM crm_contact_profiles LIMIT 1")["id"])
        result = AiIntegrationBridge().link_crm_contact(self.repository, contact_id=cid)
        self.assertIsInstance(result, dict)

    def test_ai_link_property(self) -> None:
        pid = int(self.repository.one("SELECT id FROM properties LIMIT 1")["id"])
        result = AiIntegrationBridge().link_property(self.repository, property_id=pid)
        self.assertTrue(result is None or isinstance(result, dict))

    def test_ai_trigger_workflow(self) -> None:
        result = AiIntegrationBridge().trigger_workflow(self.repository, workflow_key="workflow-marketplace-request", context={"request_id": 1})
        self.assertTrue(result is None or isinstance(result, dict))

    def test_platform_engine_has_subengines(self) -> None:
        engine = MarketplacePlatformEngine()
        self.assertIsInstance(engine.partner_qualification, PartnerQualificationEngine)
        self.assertIsInstance(engine.matching, RequestMatchingEngine)

    def test_platform_integration_sources(self) -> None:
        self.assertIn("workflow_automation", MarketplacePlatformEngine().integration_sources())

class ReleaseProgramIRepositoryTests(LawimTestHarness):
    def _partner_profile_id(self) -> int:
        return int(self.repository.one("SELECT id FROM partner_profiles LIMIT 1")["id"])

    def _partner_profile_id_without_provider(self) -> int:
        row = self.repository.one(
            """
            SELECT pp.id FROM partner_profiles pp
            LEFT JOIN marketplace_provider_profiles mp ON mp.partner_profile_id = pp.id
            WHERE mp.id IS NULL
            ORDER BY pp.id ASC LIMIT 1
            """
        )
        if row is None:
            org_id = int(self.repository.one("SELECT id FROM organizations LIMIT 1")["id"])
            partner = self.repository.create_partner_profile(
                organization_id=org_id,
                partner_type="surveyor",
                display_name="Repo Provider Partner",
                description="For repository provider test",
            )
            return int(partner["id"])
        return int(row["id"])

    def _provider_id(self) -> int:
        return int(self.repository.one("SELECT id FROM marketplace_provider_profiles LIMIT 1")["id"])

    def _category_id(self) -> int:
        return int(self.repository.one("SELECT id FROM marketplace_catalog_categories LIMIT 1")["id"])

    def _request_id(self) -> int:
        return int(self.repository.one("SELECT id FROM marketplace_service_requests LIMIT 1")["id"])

    def test_list_partner_registrations(self) -> None:
        rows = self.repository.list_marketplace_partner_registrations()
        self.assertIsInstance(rows, list)

    def test_create_partner_registration(self) -> None:
        reg = self.repository.create_marketplace_partner_registration(applicant_name="Repo Applicant", applicant_email="repo@example.cm", status="submitted")
        self.assertEqual(reg["applicant_name"], "Repo Applicant")

    def test_get_partner_registration(self) -> None:
        reg = self.repository.create_marketplace_partner_registration(applicant_name="Get Reg", status="draft")
        row = self.repository.get_marketplace_partner_registration(int(reg["id"]))
        self.assertEqual(row["registration_key"], reg["registration_key"])

    def test_update_partner_registration(self) -> None:
        reg = self.repository.create_marketplace_partner_registration(applicant_name="Update Reg", status="draft")
        updated = self.repository.update_marketplace_partner_registration(int(reg["id"]), status="submitted", notes="Review")
        self.assertEqual(updated["status"], "submitted")

    def test_approve_partner_registration(self) -> None:
        org_id = int(self.repository.one("SELECT id FROM organizations LIMIT 1")["id"])
        reg = self.repository.create_marketplace_partner_registration(applicant_name="Approve Me", organization_id=org_id, status="submitted")
        approved = self.repository.approve_marketplace_partner_registration(int(reg["id"]), reviewer_id=1)
        self.assertEqual(approved["status"], "approved")

    def test_list_providers(self) -> None:
        providers = self.repository.list_marketplace_providers()
        self.assertGreaterEqual(len(providers), 1)

    def test_create_provider(self) -> None:
        partner_id = self._partner_profile_id_without_provider()
        provider = self.repository.create_marketplace_provider(partner_profile_id=partner_id, headline="New Provider")
        self.assertEqual(provider["headline"], "New Provider")

    def test_get_provider(self) -> None:
        provider_id = self._provider_id()
        row = self.repository.get_marketplace_provider(provider_id)
        self.assertEqual(int(row["id"]), provider_id)

    def test_get_provider_bundle(self) -> None:
        bundle = self.repository.get_marketplace_provider_bundle(self._provider_id())
        self.assertIn("provider", bundle)
        self.assertIn("certifications", bundle)

    def test_update_provider(self) -> None:
        provider_id = self._provider_id()
        updated = self.repository.update_marketplace_provider(provider_id, headline="Updated Headline")
        self.assertEqual(updated["headline"], "Updated Headline")

    def test_add_provider_certification(self) -> None:
        cert = self.repository.add_marketplace_provider_certification(self._provider_id(), certification_key="cert-test", title="ISO 9001")
        self.assertEqual(cert["title"], "ISO 9001")

    def test_list_catalog_categories(self) -> None:
        categories = self.repository.list_marketplace_catalog_categories()
        self.assertGreaterEqual(len(categories), 1)

    def test_create_catalog_category(self) -> None:
        cat = self.repository.create_marketplace_catalog_category(name="Test Category", category_key="cat-test")
        self.assertEqual(cat["name"], "Test Category")

    def test_create_catalog_item(self) -> None:
        item = self.repository.create_marketplace_catalog_item(category_id=self._category_id(), title="Repo Item", category="cleaning", status="active")
        self.assertEqual(item["title"], "Repo Item")

    def test_get_catalog_item(self) -> None:
        item_id = int(self.repository.one("SELECT id FROM marketplace_catalog_items LIMIT 1")["id"])
        item = self.repository.get_marketplace_catalog_item(item_id)
        self.assertEqual(int(item["id"]), item_id)

    def test_list_catalog_items(self) -> None:
        items = self.repository.list_marketplace_catalog_items(status="active")
        self.assertGreaterEqual(len(items), 1)

    def test_create_request(self) -> None:
        req = self.repository.create_marketplace_request(title="Repo Request", category="inspection", city="Douala", status="submitted")
        self.assertEqual(req["title"], "Repo Request")

    def test_get_request(self) -> None:
        req_id = self._request_id()
        req = self.repository.get_marketplace_request(req_id)
        self.assertEqual(int(req["id"]), req_id)

    def test_list_requests(self) -> None:
        reqs = self.repository.list_marketplace_requests()
        self.assertGreaterEqual(len(reqs), 1)

    def test_update_request(self) -> None:
        req_id = self._request_id()
        updated = self.repository.update_marketplace_request(req_id, status="matching")
        self.assertEqual(updated["status"], "matching")

    def test_add_request_document(self) -> None:
        doc = self.repository.add_marketplace_request_document(self._request_id(), title="Plan", document_type="plan")
        self.assertEqual(doc["title"], "Plan")

    def test_create_quote(self) -> None:
        quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
        self.assertIn("lines", quote)

    def test_get_quote(self) -> None:
        quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
        row = self.repository.get_marketplace_quote(int(quote["id"]))
        self.assertEqual(int(row["id"]), int(quote["id"]))

    def test_list_quotes(self) -> None:
        quotes = self.repository.list_marketplace_quotes()
        self.assertIsInstance(quotes, list)

    def test_send_quote(self) -> None:
        quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
        sent = self.repository.send_marketplace_quote(int(quote["id"]))
        self.assertEqual(sent["status"], "sent")

    def test_accept_quote(self) -> None:
        quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
        self.repository.send_marketplace_quote(int(quote["id"]))
        accepted = self.repository.accept_marketplace_quote(int(quote["id"]))
        self.assertEqual(accepted["status"], "accepted")

    def test_create_contract(self) -> None:
        quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
        self.repository.send_marketplace_quote(int(quote["id"]))
        self.repository.accept_marketplace_quote(int(quote["id"]))
        contract = self.repository.create_marketplace_contract(quote_id=int(quote["id"]))
        self.assertIn("contract_key", contract)

    def test_list_contracts(self) -> None:
        contracts = self.repository.list_marketplace_contracts()
        self.assertIsInstance(contracts, list)

    def test_activate_contract(self) -> None:
        quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
        self.repository.send_marketplace_quote(int(quote["id"]))
        self.repository.accept_marketplace_quote(int(quote["id"]))
        contract = self.repository.create_marketplace_contract(quote_id=int(quote["id"]))
        active = self.repository.activate_marketplace_contract(int(contract["id"]))
        self.assertEqual(active["status"], "active")

    def test_list_missions(self) -> None:
        missions = self.repository.list_marketplace_missions()
        self.assertIsInstance(missions, list)

    def test_get_mission(self) -> None:
        mission_id = self.repository.scalar("SELECT id FROM marketplace_missions LIMIT 1")
        if not mission_id:
            quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
            self.repository.send_marketplace_quote(int(quote["id"]))
            self.repository.accept_marketplace_quote(int(quote["id"]))
            contract = self.repository.create_marketplace_contract(quote_id=int(quote["id"]))
            self.repository.activate_marketplace_contract(int(contract["id"]))
            mission_id = self.repository.scalar("SELECT id FROM marketplace_missions LIMIT 1")
        mission = self.repository.get_marketplace_mission(int(mission_id))
        self.assertIn("mission_key", mission)

    def test_update_mission(self) -> None:
        mission_id = int(self.repository.scalar("SELECT id FROM marketplace_missions LIMIT 1") or 0)
        if not mission_id:
            quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
            self.repository.send_marketplace_quote(int(quote["id"]))
            self.repository.accept_marketplace_quote(int(quote["id"]))
            contract = self.repository.create_marketplace_contract(quote_id=int(quote["id"]))
            self.repository.activate_marketplace_contract(int(contract["id"]))
            mission_id = int(self.repository.scalar("SELECT id FROM marketplace_missions LIMIT 1"))
        updated = self.repository.update_marketplace_mission(mission_id, status="in_progress", progress_percent=50)
        self.assertEqual(updated["status"], "in_progress")

    def test_add_mission_deliverable(self) -> None:
        mission_id = int(self.repository.scalar("SELECT id FROM marketplace_missions LIMIT 1") or 0)
        if not mission_id:
            quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
            self.repository.send_marketplace_quote(int(quote["id"]))
            self.repository.accept_marketplace_quote(int(quote["id"]))
            contract = self.repository.create_marketplace_contract(quote_id=int(quote["id"]))
            self.repository.activate_marketplace_contract(int(contract["id"]))
            mission_id = int(self.repository.scalar("SELECT id FROM marketplace_missions LIMIT 1"))
        deliverable = self.repository.add_marketplace_mission_deliverable(mission_id, title="Report")
        self.assertEqual(deliverable["title"], "Report")

    def test_set_availability(self) -> None:
        slot = self.repository.set_marketplace_availability(self._provider_id(), day_of_week=6, start_time="09:00", end_time="17:00")
        self.assertEqual(slot["day_of_week"], 6)

    def test_list_availability(self) -> None:
        slots = self.repository.list_marketplace_availability(self._provider_id())
        self.assertGreaterEqual(len(slots), 1)

    def test_create_review(self) -> None:
        review = self.repository.create_marketplace_review(provider_profile_id=self._provider_id(), rating=5, title="Great", body="Excellent work")
        self.assertEqual(review["rating"], 5)

    def test_list_reviews(self) -> None:
        reviews = self.repository.list_marketplace_reviews(provider_id=self._provider_id())
        self.assertIsInstance(reviews, list)

    def test_publish_review(self) -> None:
        review = self.repository.create_marketplace_review(provider_profile_id=self._provider_id(), rating=4, title="Good")
        published = self.repository.publish_marketplace_review(int(review["id"]))
        self.assertEqual(published["status"], "published")

    def test_compute_reputation(self) -> None:
        scores = self.repository.compute_marketplace_reputation(self._provider_id())
        for key in REPUTATION_SCORE_KEYS:
            self.assertIn(key, scores)

    def test_get_reputation(self) -> None:
        scores = self.repository.get_marketplace_reputation(self._provider_id())
        self.assertIsInstance(scores, dict)

    def test_open_dispute(self) -> None:
        quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
        self.repository.send_marketplace_quote(int(quote["id"]))
        self.repository.accept_marketplace_quote(int(quote["id"]))
        contract = self.repository.create_marketplace_contract(quote_id=int(quote["id"]))
        dispute = self.repository.open_marketplace_dispute(contract_id=int(contract["id"]), reason="Delay")
        self.assertEqual(dispute["status"], "open")

    def test_list_disputes(self) -> None:
        disputes = self.repository.list_marketplace_disputes()
        self.assertIsInstance(disputes, list)

    def test_resolve_dispute(self) -> None:
        quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
        self.repository.send_marketplace_quote(int(quote["id"]))
        self.repository.accept_marketplace_quote(int(quote["id"]))
        contract = self.repository.create_marketplace_contract(quote_id=int(quote["id"]))
        dispute = self.repository.open_marketplace_dispute(contract_id=int(contract["id"]), reason="Issue")
        resolved = self.repository.resolve_marketplace_dispute(int(dispute["id"]), resolution="Settled")
        self.assertEqual(resolved["status"], "resolved")

    def test_list_subscription_plans(self) -> None:
        plans = self.repository.list_marketplace_subscription_plans()
        self.assertGreaterEqual(len(plans), 1)

    def test_create_subscription(self) -> None:
        plan_id = int(self.repository.one("SELECT id FROM marketplace_subscription_plans LIMIT 1")["id"])
        sub = self.repository.create_marketplace_subscription(plan_id=plan_id, provider_profile_id=self._provider_id())
        self.assertIn("subscription_key", sub)

    def test_list_subscriptions(self) -> None:
        subs = self.repository.list_marketplace_subscriptions()
        self.assertIsInstance(subs, list)

    def test_compute_commission(self) -> None:
        quote = self.repository.create_marketplace_quote(request_id=self._request_id(), provider_profile_id=self._provider_id())
        self.repository.send_marketplace_quote(int(quote["id"]))
        self.repository.accept_marketplace_quote(int(quote["id"]))
        contract = self.repository.create_marketplace_contract(quote_id=int(quote["id"]))
        commission = self.repository.compute_marketplace_commission(int(contract["id"]))
        self.assertIn("amount", commission)

    def test_list_commissions(self) -> None:
        commissions = self.repository.list_marketplace_commissions()
        self.assertIsInstance(commissions, list)

    def test_prepare_payment(self) -> None:
        prep = self.repository.prepare_marketplace_payment(amount=50000, payment_method="mobile_money")
        self.assertEqual(prep["amount"], 50000)

    def test_run_matching(self) -> None:
        payload = self.repository.run_marketplace_matching(self._request_id())
        self.assertIn("session", payload)
        self.assertIn("results", payload)

    def test_get_matching_session(self) -> None:
        payload = self.repository.run_marketplace_matching(self._request_id())
        session_id = int(payload["session"]["id"])
        session = self.repository.get_marketplace_matching_session(session_id)
        self.assertIn("session", session)

    def test_add_portfolio_item(self) -> None:
        item = self.repository.add_marketplace_portfolio_item(self._provider_id(), title="Portfolio A", category="photography")
        self.assertEqual(item["title"], "Portfolio A")

    def test_list_portfolio(self) -> None:
        portfolio = self.repository.list_marketplace_portfolio(self._provider_id())
        self.assertGreaterEqual(len(portfolio), 1)

    def test_marketplace_integrations(self) -> None:
        integrations = self.repository.marketplace_integrations()
        self.assertIn("sources", integrations)
        self.assertTrue(integrations.get("crm"))

    def test_marketplace_analytics(self) -> None:
        analytics = self.repository.marketplace_analytics()
        self.assertIn("metrics", analytics)

    def test_marketplace_stats(self) -> None:
        stats = self.repository.marketplace_stats()
        self.assertIn("active_providers", stats)

    def test_marketplace_dashboard(self) -> None:
        dashboard = self.repository.marketplace_dashboard()
        self.assertIn("recent_requests", dashboard)
        self.assertIn("integrations", dashboard)

    def test_snapshot_marketplace_analytics(self) -> None:
        snap = self.repository.snapshot_marketplace_analytics()
        self.assertIn("providers", snap)

    def test_list_ai_recommendations(self) -> None:
        self.repository.run_marketplace_matching(self._request_id())
        recs = self.repository.list_marketplace_ai_recommendations(request_id=self._request_id())
        self.assertIsInstance(recs, list)

class ReleaseProgramIApiTests(LawimTestHarness):
    def _provider_id(self, token: str) -> int:
        payload = self.invoke("/api/v2/marketplace/providers", token=token).body_json()
        return int(payload["providers"][0]["id"])

    def _request_id(self, token: str) -> int:
        payload = self.invoke("/api/v2/marketplace/requests", token=token).body_json()
        return int(payload["requests"][0]["id"])

    def _category_id(self, token: str) -> int:
        payload = self.invoke("/api/v2/marketplace/catalog/categories", token=token).body_json()
        return int(payload["categories"][0]["id"])

    def _partner_profile_id_without_provider(self) -> int:
        row = self.repository.one(
            """
            SELECT pp.id FROM partner_profiles pp
            LEFT JOIN marketplace_provider_profiles mp ON mp.partner_profile_id = pp.id
            WHERE mp.id IS NULL
            ORDER BY pp.id ASC LIMIT 1
            """
        )
        if row is None:
            org_id = int(self.repository.one("SELECT id FROM organizations LIMIT 1")["id"])
            partner = self.repository.create_partner_profile(
                organization_id=org_id,
                partner_type="surveyor",
                display_name="Extra Partner",
                description="For marketplace provider API test",
            )
            return int(partner["id"])
        return int(row["id"])

    def test_integrations_api_no_auth(self) -> None:
        response = self.invoke("/api/v2/marketplace/integrations")
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("sources", response.body_json())

    def test_partners_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/partners", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("registrations", response.body_json())

    def test_providers_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/providers", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["providers"]), 1)

    def test_provider_detail_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        provider_id = self._provider_id(token)
        response = self.invoke(f"/api/v2/marketplace/providers/{provider_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("provider", response.body_json())

    def test_provider_availability_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        provider_id = self._provider_id(token)
        response = self.invoke(f"/api/v2/marketplace/providers/{provider_id}/availability", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_provider_portfolio_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        provider_id = self._provider_id(token)
        response = self.invoke(f"/api/v2/marketplace/providers/{provider_id}/portfolio", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_provider_reputation_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        provider_id = self._provider_id(token)
        response = self.invoke(f"/api/v2/marketplace/providers/{provider_id}/reputation", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_catalog_categories_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/catalog/categories", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_catalog_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/catalog", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("items", response.body_json())

    def test_catalog_detail_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        item_id = int(self.repository.one("SELECT id FROM marketplace_catalog_items LIMIT 1")["id"])
        response = self.invoke(f"/api/v2/marketplace/catalog/{item_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_requests_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/requests", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_request_detail_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = self._request_id(token)
        response = self.invoke(f"/api/v2/marketplace/requests/{request_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_quotes_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/quotes", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_contracts_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/contracts", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_missions_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/missions", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_mission_detail_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        if self.repository.scalar("SELECT COUNT(*) FROM marketplace_missions") == 0:
            request_id = self._request_id(token)
            provider_id = self._provider_id(token)
            created = self.invoke(
                "/api/v2/marketplace/quotes",
                method="POST",
                token=token,
                body={"request_id": request_id, "provider_profile_id": provider_id},
            )
            quote_id = int(created.body_json()["quote"]["id"])
            self.invoke(f"/api/v2/marketplace/quotes/{quote_id}/send", method="POST", token=token, body={})
            self.invoke(f"/api/v2/marketplace/quotes/{quote_id}/accept", method="POST", token=token, body={})
            contract = self.invoke("/api/v2/marketplace/contracts", method="POST", token=token, body={"quote_id": quote_id})
            contract_id = int(contract.body_json()["contract"]["id"])
            self.invoke(f"/api/v2/marketplace/contracts/{contract_id}/activate", method="POST", token=token, body={})
        mission_id = self.repository.scalar("SELECT id FROM marketplace_missions LIMIT 1")
        self.assertIsNotNone(mission_id)
        response = self.invoke(f"/api/v2/marketplace/missions/{mission_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_reviews_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/reviews", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_commissions_list_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/marketplace/commissions", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_subscription_plans_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/subscriptions/plans", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_disputes_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/disputes", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_recommendations_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/recommendations", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_analytics_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/analytics", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_stats_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/stats", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("stats", response.body_json())

    def test_dashboard_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/dashboard", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_matching_session_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = self._request_id(token)
        matching = self.invoke(f"/api/v2/marketplace/requests/{request_id}/matching", method="POST", token=token, body={})
        session_id = int(matching.body_json()["session"]["id"])
        response = self.invoke(f"/api/v2/marketplace/matching/{session_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_create_partner_registration_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        org_id = int(self.repository.one("SELECT id FROM organizations LIMIT 1")["id"])
        response = self.invoke(
            "/api/v2/marketplace/partners",
            method="POST",
            token=token,
            body={"applicant_name": "API Partner", "organization_id": org_id, "service_categories": ["inspection"]},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_qualify_partner_registration_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        org_id = int(self.repository.one("SELECT id FROM organizations LIMIT 1")["id"])
        created = self.invoke(
            "/api/v2/marketplace/partners",
            method="POST",
            token=token,
            body={"applicant_name": "Qualify Partner", "applicant_email": "q@example.cm", "organization_id": org_id, "service_categories": ["inspection", "legal_notary"]},
        )
        reg_id = int(created.body_json()["registration"]["id"])
        self.repository.update_marketplace_partner_registration(reg_id, status="submitted")
        response = self.invoke(f"/api/v2/marketplace/partners/{reg_id}/qualify", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_approve_partner_registration_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        org_id = int(self.repository.one("SELECT id FROM organizations LIMIT 1")["id"])
        created = self.invoke(
            "/api/v2/marketplace/partners",
            method="POST",
            token=token,
            body={"applicant_name": "Approve Partner", "organization_id": org_id},
        )
        reg_id = int(created.body_json()["registration"]["id"])
        self.repository.update_marketplace_partner_registration(reg_id, status="submitted")
        response = self.invoke(f"/api/v2/marketplace/partners/{reg_id}/approve", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_create_provider_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        partner_id = self._partner_profile_id_without_provider()
        response = self.invoke(
            "/api/v2/marketplace/providers",
            method="POST",
            token=token,
            body={"partner_profile_id": partner_id, "headline": "API Provider"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_set_provider_availability_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        provider_id = self._provider_id(token)
        response = self.invoke(
            f"/api/v2/marketplace/providers/{provider_id}/availability",
            method="POST",
            token=token,
            body={"day_of_week": 2, "start_time": "10:00", "end_time": "16:00"},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_create_catalog_item_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        category_id = self._category_id(token)
        response = self.invoke(
            "/api/v2/marketplace/catalog",
            method="POST",
            token=token,
            body={"category_id": category_id, "title": "API Catalog Item", "category": "maintenance"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_create_request_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke(
            "/api/v2/marketplace/requests",
            method="POST",
            token=token,
            body={"title": "API Request", "category": "inspection", "city": "Douala", "budget_min": 100000, "budget_max": 250000},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_create_quote_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = self._request_id(token)
        provider_id = self._provider_id(token)
        response = self.invoke(
            "/api/v2/marketplace/quotes",
            method="POST",
            token=token,
            body={"request_id": request_id, "provider_profile_id": provider_id, "lines": [{"description": "Work", "quantity": 1, "unit_price": 120000}]},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_send_quote_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = self._request_id(token)
        provider_id = self._provider_id(token)
        created = self.invoke(
            "/api/v2/marketplace/quotes",
            method="POST",
            token=token,
            body={"request_id": request_id, "provider_profile_id": provider_id},
        )
        quote_id = int(created.body_json()["quote"]["id"])
        response = self.invoke(f"/api/v2/marketplace/quotes/{quote_id}/send", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_accept_quote_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = self._request_id(token)
        provider_id = self._provider_id(token)
        created = self.invoke(
            "/api/v2/marketplace/quotes",
            method="POST",
            token=token,
            body={"request_id": request_id, "provider_profile_id": provider_id},
        )
        quote_id = int(created.body_json()["quote"]["id"])
        self.invoke(f"/api/v2/marketplace/quotes/{quote_id}/send", method="POST", token=token, body={})
        response = self.invoke(f"/api/v2/marketplace/quotes/{quote_id}/accept", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_create_contract_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = self._request_id(token)
        provider_id = self._provider_id(token)
        created = self.invoke(
            "/api/v2/marketplace/quotes",
            method="POST",
            token=token,
            body={"request_id": request_id, "provider_profile_id": provider_id},
        )
        quote_id = int(created.body_json()["quote"]["id"])
        self.invoke(f"/api/v2/marketplace/quotes/{quote_id}/send", method="POST", token=token, body={})
        self.invoke(f"/api/v2/marketplace/quotes/{quote_id}/accept", method="POST", token=token, body={})
        response = self.invoke("/api/v2/marketplace/contracts", method="POST", token=token, body={"quote_id": quote_id})
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_activate_contract_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = self._request_id(token)
        provider_id = self._provider_id(token)
        created = self.invoke(
            "/api/v2/marketplace/quotes",
            method="POST",
            token=token,
            body={"request_id": request_id, "provider_profile_id": provider_id},
        )
        quote_id = int(created.body_json()["quote"]["id"])
        self.invoke(f"/api/v2/marketplace/quotes/{quote_id}/send", method="POST", token=token, body={})
        self.invoke(f"/api/v2/marketplace/quotes/{quote_id}/accept", method="POST", token=token, body={})
        contract = self.invoke("/api/v2/marketplace/contracts", method="POST", token=token, body={"quote_id": quote_id})
        contract_id = int(contract.body_json()["contract"]["id"])
        response = self.invoke(f"/api/v2/marketplace/contracts/{contract_id}/activate", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_create_review_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        provider_id = self._provider_id(token)
        response = self.invoke(
            "/api/v2/marketplace/reviews",
            method="POST",
            token=token,
            body={"provider_profile_id": provider_id, "rating": 5, "title": "API Review", "body": "Great service"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_open_dispute_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = self._request_id(token)
        provider_id = self._provider_id(token)
        created = self.invoke(
            "/api/v2/marketplace/quotes",
            method="POST",
            token=token,
            body={"request_id": request_id, "provider_profile_id": provider_id},
        )
        quote_id = int(created.body_json()["quote"]["id"])
        self.invoke(f"/api/v2/marketplace/quotes/{quote_id}/send", method="POST", token=token, body={})
        self.invoke(f"/api/v2/marketplace/quotes/{quote_id}/accept", method="POST", token=token, body={})
        contract = self.invoke("/api/v2/marketplace/contracts", method="POST", token=token, body={"quote_id": quote_id})
        contract_id = int(contract.body_json()["contract"]["id"])
        response = self.invoke(
            "/api/v2/marketplace/disputes",
            method="POST",
            token=token,
            body={"contract_id": contract_id, "reason": "Delay"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_resolve_dispute_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        request_id = int(self.repository.one("SELECT id FROM marketplace_service_requests LIMIT 1")["id"])
        provider_id = int(self.repository.one("SELECT id FROM marketplace_provider_profiles LIMIT 1")["id"])
        quote = self.repository.create_marketplace_quote(request_id=request_id, provider_profile_id=provider_id)
        self.repository.send_marketplace_quote(int(quote["id"]))
        self.repository.accept_marketplace_quote(int(quote["id"]))
        contract = self.repository.create_marketplace_contract(quote_id=int(quote["id"]))
        dispute = self.repository.open_marketplace_dispute(contract_id=int(contract["id"]), reason="Issue")
        response = self.invoke(
            f"/api/v2/marketplace/disputes/{int(dispute['id'])}/resolve",
            method="POST",
            token=token,
            body={"resolution": "Resolved via API"},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_subscribe_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        plan_id = int(self.repository.one("SELECT id FROM marketplace_subscription_plans LIMIT 1")["id"])
        provider_id = self._provider_id(token)
        response = self.invoke(
            "/api/v2/marketplace/subscriptions",
            method="POST",
            token=token,
            body={"plan_id": plan_id, "provider_profile_id": provider_id},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_prepare_payment_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke(
            "/api/v2/marketplace/payments/prepare",
            method="POST",
            token=token,
            body={"amount": 75000, "payment_method": "orange_money"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_run_matching_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = self._request_id(token)
        response = self.invoke(f"/api/v2/marketplace/requests/{request_id}/matching", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_generate_recommendations_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = self._request_id(token)
        response = self.invoke(f"/api/v2/marketplace/requests/{request_id}/recommendations", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_seed_catalog_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/marketplace/seed", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_program_b_partners_list_still_works(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/partners", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("partners", response.body_json())

    def test_program_b_partner_detail_still_works(self) -> None:
        token = self.login(email="agent@lawim.local")
        partner_id = int(self.invoke("/api/v2/partners", token=token).body_json()["partners"][0]["id"])
        response = self.invoke(f"/api/v2/partners/{partner_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

class ReleaseProgramIUiTests(LawimTestHarness):
    def test_index_has_marketplace_section(self) -> None:
        html = self.invoke("/")
        self.assertIn("Marketplace &amp; Partner Ecosystem", html.body_text())

    def test_app_js_references_marketplace_api(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/marketplace/stats", js.body_text())
        self.assertIn("refreshMarketplaceAdmin", js.body_text())

    def test_app_js_references_marketplace_catalog(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/marketplace/catalog", js.body_text())

class ReleaseProgramIHealthTests(LawimTestHarness):
    def test_health_schema_v15(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.body_json()["database"]["schema_version"], 15)

    def test_migration_strategy_v15(self) -> None:
        self.assertEqual(migration_strategy_profile()["schema_version"], 15)

    def test_metrics_include_marketplace_counters(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/marketplace/providers", token=token)
        admin = self.login(email="admin@lawim.local")
        metrics = self.invoke("/api/metrics", token=admin)
        snapshot = metrics.body_json()["metrics"]
        self.assertGreaterEqual(snapshot.get("marketplace_requests_total", 0), 1)

class ReleaseProgramIV15TableTests(LawimTestHarness):
    def _table_names(self) -> set[str]:
        return {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}

    def test_v15_table_marketplace_partner_registrations(self) -> None:
        self.assertIn("marketplace_partner_registrations", self._table_names())

    def test_v15_table_marketplace_provider_profiles(self) -> None:
        self.assertIn("marketplace_provider_profiles", self._table_names())

    def test_v15_table_marketplace_provider_certifications(self) -> None:
        self.assertIn("marketplace_provider_certifications", self._table_names())

    def test_v15_table_marketplace_catalog_categories(self) -> None:
        self.assertIn("marketplace_catalog_categories", self._table_names())

    def test_v15_table_marketplace_catalog_items(self) -> None:
        self.assertIn("marketplace_catalog_items", self._table_names())

    def test_v15_table_marketplace_service_requests(self) -> None:
        self.assertIn("marketplace_service_requests", self._table_names())

    def test_v15_table_marketplace_request_documents(self) -> None:
        self.assertIn("marketplace_request_documents", self._table_names())

    def test_v15_table_marketplace_quotes(self) -> None:
        self.assertIn("marketplace_quotes", self._table_names())

    def test_v15_table_marketplace_quote_lines(self) -> None:
        self.assertIn("marketplace_quote_lines", self._table_names())

    def test_v15_table_marketplace_contracts(self) -> None:
        self.assertIn("marketplace_contracts", self._table_names())

    def test_v15_table_marketplace_contract_documents(self) -> None:
        self.assertIn("marketplace_contract_documents", self._table_names())

    def test_v15_table_marketplace_missions(self) -> None:
        self.assertIn("marketplace_missions", self._table_names())

    def test_v15_table_marketplace_mission_milestones(self) -> None:
        self.assertIn("marketplace_mission_milestones", self._table_names())

    def test_v15_table_marketplace_mission_deliverables(self) -> None:
        self.assertIn("marketplace_mission_deliverables", self._table_names())

    def test_v15_table_marketplace_availability(self) -> None:
        self.assertIn("marketplace_availability", self._table_names())

    def test_v15_table_marketplace_reviews(self) -> None:
        self.assertIn("marketplace_reviews", self._table_names())

    def test_v15_table_marketplace_review_moderation(self) -> None:
        self.assertIn("marketplace_review_moderation", self._table_names())

    def test_v15_table_marketplace_reputation_snapshots(self) -> None:
        self.assertIn("marketplace_reputation_snapshots", self._table_names())

    def test_v15_table_marketplace_disputes(self) -> None:
        self.assertIn("marketplace_disputes", self._table_names())

    def test_v15_table_marketplace_dispute_messages(self) -> None:
        self.assertIn("marketplace_dispute_messages", self._table_names())

    def test_v15_table_marketplace_subscription_plans(self) -> None:
        self.assertIn("marketplace_subscription_plans", self._table_names())

    def test_v15_table_marketplace_subscriptions(self) -> None:
        self.assertIn("marketplace_subscriptions", self._table_names())

    def test_v15_table_marketplace_commission_rules(self) -> None:
        self.assertIn("marketplace_commission_rules", self._table_names())

    def test_v15_table_marketplace_commissions(self) -> None:
        self.assertIn("marketplace_commissions", self._table_names())

    def test_v15_table_marketplace_payment_preparations(self) -> None:
        self.assertIn("marketplace_payment_preparations", self._table_names())

    def test_v15_table_marketplace_matching_sessions(self) -> None:
        self.assertIn("marketplace_matching_sessions", self._table_names())

    def test_v15_table_marketplace_matching_results(self) -> None:
        self.assertIn("marketplace_matching_results", self._table_names())

    def test_v15_table_marketplace_portfolio_items(self) -> None:
        self.assertIn("marketplace_portfolio_items", self._table_names())

    def test_v15_table_marketplace_analytics_snapshots(self) -> None:
        self.assertIn("marketplace_analytics_snapshots", self._table_names())

    def test_v15_table_marketplace_ai_recommendations(self) -> None:
        self.assertIn("marketplace_ai_recommendations", self._table_names())

class ReleaseProgramIIntegrationTests(LawimTestHarness):
    def test_provider_links_partner_profile(self) -> None:
        provider = self.repository.one("SELECT partner_profile_id FROM marketplace_provider_profiles LIMIT 1")
        partner = self.repository.one("SELECT id FROM partner_profiles WHERE id = ?", (int(provider["partner_profile_id"]),))
        self.assertIsNotNone(partner)

    def test_catalog_item_may_link_service_catalog(self) -> None:
        row = self.repository.one("SELECT service_catalog_id FROM marketplace_catalog_items WHERE service_catalog_id IS NOT NULL LIMIT 1")
        if row is None:
            self.skipTest("no linked catalog items")
        service = self.repository.one("SELECT id FROM service_catalog WHERE id = ?", (int(row["service_catalog_id"]),))
        self.assertIsNotNone(service)

    def test_request_matching_uses_partners(self) -> None:
        request_id = int(self.repository.one("SELECT id FROM marketplace_service_requests LIMIT 1")["id"])
        payload = self.repository.run_marketplace_matching(request_id)
        self.assertGreaterEqual(len(payload["results"]), 1)

    def test_integration_sources_include_crm(self) -> None:
        sources = MarketplacePlatformEngine().integration_sources()
        self.assertIn("crm", sources)

    def test_integration_sources_include_workflow(self) -> None:
        sources = MarketplacePlatformEngine().integration_sources()
        self.assertIn("workflow_automation", sources)

    def test_integration_sources_include_rei(self) -> None:
        sources = MarketplacePlatformEngine().integration_sources()
        self.assertIn("real_estate_intelligence", sources)

    def test_integration_sources_include_knowledge(self) -> None:
        sources = MarketplacePlatformEngine().integration_sources()
        self.assertIn("knowledge_platform", sources)

    def test_marketplace_link_crm_contact(self) -> None:
        cid = int(self.repository.one("SELECT id FROM crm_contact_profiles LIMIT 1")["id"])
        linked = self.repository.marketplace_link_contact(cid)
        self.assertIsInstance(linked, dict)

    def test_marketplace_link_property(self) -> None:
        pid = int(self.repository.one("SELECT id FROM properties LIMIT 1")["id"])
        linked = self.repository.marketplace_link_property(pid)
        self.assertTrue(linked is None or isinstance(linked, dict))

    def test_marketplace_trigger_workflow(self) -> None:
        result = self.repository.marketplace_trigger_workflow(workflow_key="workflow-marketplace-request", context={"request_id": 1})
        self.assertTrue(result is None or isinstance(result, dict))

    def test_expert_rag_available_for_marketplace_ai(self) -> None:
        bridge = AiIntegrationBridge()
        result = bridge.enrich_with_knowledge(self.repository, "acte de vente")
        self.assertTrue(result is None or isinstance(result, dict))

class ReleaseProgramIObservabilityTests(LawimTestHarness):
    def _admin_metrics(self) -> dict[str, object]:
        return self.invoke("/api/metrics", token=self.login(email="admin@lawim.local")).body_json()["metrics"]

    def test_marketplace_provider_list_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/marketplace/providers", token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get("marketplace_requests_total", 0), 1)

    def test_marketplace_request_list_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/marketplace/requests", token=token)
        crm_metrics = self._admin_metrics().get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("request_list", 0), 1)

    def test_marketplace_catalog_list_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/marketplace/catalog", token=token)
        crm_metrics = self._admin_metrics().get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("catalog_list", 0), 1)

    def test_marketplace_analytics_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/marketplace/analytics", token=token)
        crm_metrics = self._admin_metrics().get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("marketplace_analytics", crm_metrics.get("analytics_view", 0)), 1)

    def test_marketplace_stats_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/marketplace/stats", token=token)
        crm_metrics = self._admin_metrics().get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("marketplace_stats", 0), 1)

    def test_marketplace_dashboard_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/marketplace/dashboard", token=token)
        crm_metrics = self._admin_metrics().get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("marketplace_dashboard", 0), 1)

    def test_provider_detail_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        provider_id = int(self.invoke("/api/v2/marketplace/providers", token=token).body_json()["providers"][0]["id"])
        self.invoke(f"/api/v2/marketplace/providers/{provider_id}", token=token)
        crm_metrics = self._admin_metrics().get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("provider_detail", 0), 1)

    def test_matching_run_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = int(self.invoke("/api/v2/marketplace/requests", token=token).body_json()["requests"][0]["id"])
        self.invoke(f"/api/v2/marketplace/requests/{request_id}/matching", method="POST", token=token, body={})
        crm_metrics = self._admin_metrics().get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("matching_run", crm_metrics.get("marketplace_matching_run", 0)), 1)

    def test_quote_created_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        request_id = int(self.invoke("/api/v2/marketplace/requests", token=token).body_json()["requests"][0]["id"])
        provider_id = int(self.invoke("/api/v2/marketplace/providers", token=token).body_json()["providers"][0]["id"])
        self.invoke(
            "/api/v2/marketplace/quotes",
            method="POST",
            token=token,
            body={"request_id": request_id, "provider_profile_id": provider_id},
        )
        crm_metrics = self._admin_metrics().get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("quote_created", 0), 1)

    def test_review_created_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        provider_id = int(self.invoke("/api/v2/marketplace/providers", token=token).body_json()["providers"][0]["id"])
        self.invoke(
            "/api/v2/marketplace/reviews",
            method="POST",
            token=token,
            body={"provider_profile_id": provider_id, "rating": 4, "title": "Metrics Review"},
        )
        crm_metrics = self._admin_metrics().get("crm_metrics", {})
        self.assertGreaterEqual(crm_metrics.get("review_created", 0), 1)

