from __future__ import annotations

import sqlite3
import tempfile
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from pathlib import Path

from lawim_v2.knowledge_platform.schema_v11_ddl import V11_TABLE_NAMES
from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.real_estate_intelligence.constants import (
    DOCUMENT_TYPES,
    INTELLIGENCE_SCORE_KEYS,
    LISTING_STATUSES,
    NEGOTIATION_STATUSES,
    OFFER_STATUSES,
    PROPERTY_TYPES,
    RECOMMENDATION_TYPES,
    TRANSACTION_STATUSES,
    TRANSACTION_TYPES,
    VERIFICATION_STATUSES,
    VISIT_STATUSES,
)
from lawim_v2.real_estate_intelligence.engines import (
    GeoEngine,
    IntelligenceEngine,
    ListingEngine,
    MatchingEngine,
    RealEstatePlatformEngine,
    RecommendationEngine,
    SearchEngine,
    ValuationEngine,
    VerificationEngine,
)
from lawim_v2.real_estate_intelligence.schema_v13_ddl import V13_TABLE_NAMES
from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations, migration_strategy_profile
from lawim_v2.workflow_automation.schema_v12_ddl import V12_TABLE_NAMES

from tests.lawim_harness import LawimTestHarness


SAMPLE_PROPERTY: dict[str, object] = {
    "id": 1,
    "title": "Bonanjo City Loft",
    "summary": "Appartement urbain lumineux",
    "city": "Douala",
    "latitude": 4.05,
    "longitude": 9.7,
    "price_min": 250000,
    "price_max": 300000,
    "status": "published",
    "bedrooms": 2,
    "area_sqm": 78,
    "currency": "XAF",
    "listing_code": "lawim-1",
    "property_type": "apartment",
}


class ReleaseProgramGPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v13(self) -> None:
        self.assertEqual(self.repository.schema_version(), 15)

    def test_application_schema_version_constant(self) -> None:
        self.assertEqual(APPLICATION_SCHEMA_VERSION, 15)

    def test_rei_tables_present(self) -> None:
        self.assertTrue(self.repository.rei_tables_present())

    def test_all_v13_tables_exist(self) -> None:
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

    def test_rei_catalog_seeded(self) -> None:
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM rei_property_profiles"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM rei_listings"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM rei_verification_scores"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM rei_intelligence_scores"), 1)

    def test_v12_to_v13_legacy_migration(self) -> None:
        db_path = Path(tempfile.mkdtemp()) / "v12.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute("PRAGMA foreign_keys = OFF")
        for table in V13_TABLE_NAMES:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("UPDATE schema_meta SET value='12' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn("rei_property_profiles", names)
        for table in V12_TABLE_NAMES:
            self.assertIn(table, names)


class ReleaseProgramGConstantsTests(LawimTestHarness):
    def test_property_type_house(self) -> None:
        self.assertIn("house", PROPERTY_TYPES)

    def test_property_type_apartment(self) -> None:
        self.assertIn("apartment", PROPERTY_TYPES)

    def test_property_type_building(self) -> None:
        self.assertIn("building", PROPERTY_TYPES)

    def test_property_type_land(self) -> None:
        self.assertIn("land", PROPERTY_TYPES)

    def test_property_type_office(self) -> None:
        self.assertIn("office", PROPERTY_TYPES)

    def test_property_type_retail(self) -> None:
        self.assertIn("retail", PROPERTY_TYPES)

    def test_property_type_industrial(self) -> None:
        self.assertIn("industrial", PROPERTY_TYPES)

    def test_property_type_hotel(self) -> None:
        self.assertIn("hotel", PROPERTY_TYPES)

    def test_property_type_residence(self) -> None:
        self.assertIn("residence", PROPERTY_TYPES)

    def test_property_type_investment_building(self) -> None:
        self.assertIn("investment_building", PROPERTY_TYPES)

    def test_listing_status_draft(self) -> None:
        self.assertIn("draft", LISTING_STATUSES)

    def test_listing_status_published(self) -> None:
        self.assertIn("published", LISTING_STATUSES)

    def test_listing_status_suspended(self) -> None:
        self.assertIn("suspended", LISTING_STATUSES)

    def test_listing_status_expired(self) -> None:
        self.assertIn("expired", LISTING_STATUSES)

    def test_listing_status_archived(self) -> None:
        self.assertIn("archived", LISTING_STATUSES)

    def test_verification_status_pending(self) -> None:
        self.assertIn("pending", VERIFICATION_STATUSES)

    def test_verification_status_verified(self) -> None:
        self.assertIn("verified", VERIFICATION_STATUSES)

    def test_verification_status_failed(self) -> None:
        self.assertIn("failed", VERIFICATION_STATUSES)

    def test_verification_status_review(self) -> None:
        self.assertIn("review", VERIFICATION_STATUSES)

    def test_visit_status_scheduled(self) -> None:
        self.assertIn("scheduled", VISIT_STATUSES)

    def test_visit_status_confirmed(self) -> None:
        self.assertIn("confirmed", VISIT_STATUSES)

    def test_visit_status_completed(self) -> None:
        self.assertIn("completed", VISIT_STATUSES)

    def test_visit_status_cancelled(self) -> None:
        self.assertIn("cancelled", VISIT_STATUSES)

    def test_visit_status_no_show(self) -> None:
        self.assertIn("no_show", VISIT_STATUSES)

    def test_negotiation_status_open(self) -> None:
        self.assertIn("open", NEGOTIATION_STATUSES)

    def test_negotiation_status_offer(self) -> None:
        self.assertIn("offer", NEGOTIATION_STATUSES)

    def test_negotiation_status_counter(self) -> None:
        self.assertIn("counter", NEGOTIATION_STATUSES)

    def test_negotiation_status_accepted(self) -> None:
        self.assertIn("accepted", NEGOTIATION_STATUSES)

    def test_negotiation_status_rejected(self) -> None:
        self.assertIn("rejected", NEGOTIATION_STATUSES)

    def test_negotiation_status_closed(self) -> None:
        self.assertIn("closed", NEGOTIATION_STATUSES)

    def test_offer_status_draft(self) -> None:
        self.assertIn("draft", OFFER_STATUSES)

    def test_offer_status_submitted(self) -> None:
        self.assertIn("submitted", OFFER_STATUSES)

    def test_offer_status_countered(self) -> None:
        self.assertIn("countered", OFFER_STATUSES)

    def test_offer_status_accepted(self) -> None:
        self.assertIn("accepted", OFFER_STATUSES)

    def test_offer_status_rejected(self) -> None:
        self.assertIn("rejected", OFFER_STATUSES)

    def test_offer_status_withdrawn(self) -> None:
        self.assertIn("withdrawn", OFFER_STATUSES)

    def test_transaction_status_pending(self) -> None:
        self.assertIn("pending", TRANSACTION_STATUSES)

    def test_transaction_status_reserved(self) -> None:
        self.assertIn("reserved", TRANSACTION_STATUSES)

    def test_transaction_status_promised(self) -> None:
        self.assertIn("promised", TRANSACTION_STATUSES)

    def test_transaction_status_signed(self) -> None:
        self.assertIn("signed", TRANSACTION_STATUSES)

    def test_transaction_status_closed(self) -> None:
        self.assertIn("closed", TRANSACTION_STATUSES)

    def test_transaction_status_cancelled(self) -> None:
        self.assertIn("cancelled", TRANSACTION_STATUSES)

    def test_transaction_type_sale(self) -> None:
        self.assertIn("sale", TRANSACTION_TYPES)

    def test_transaction_type_rent(self) -> None:
        self.assertIn("rent", TRANSACTION_TYPES)

    def test_transaction_type_reservation(self) -> None:
        self.assertIn("reservation", TRANSACTION_TYPES)

    def test_transaction_type_lease(self) -> None:
        self.assertIn("lease", TRANSACTION_TYPES)

    def test_intelligence_score_quality(self) -> None:
        self.assertIn("quality", INTELLIGENCE_SCORE_KEYS)

    def test_intelligence_score_legal(self) -> None:
        self.assertIn("legal", INTELLIGENCE_SCORE_KEYS)

    def test_intelligence_score_investment(self) -> None:
        self.assertIn("investment", INTELLIGENCE_SCORE_KEYS)

    def test_intelligence_score_market(self) -> None:
        self.assertIn("market", INTELLIGENCE_SCORE_KEYS)

    def test_intelligence_score_profitability(self) -> None:
        self.assertIn("profitability", INTELLIGENCE_SCORE_KEYS)

    def test_intelligence_score_liquidity(self) -> None:
        self.assertIn("liquidity", INTELLIGENCE_SCORE_KEYS)

    def test_intelligence_score_risk(self) -> None:
        self.assertIn("risk", INTELLIGENCE_SCORE_KEYS)

    def test_recommendation_type_property(self) -> None:
        self.assertIn("property", RECOMMENDATION_TYPES)

    def test_recommendation_type_investment(self) -> None:
        self.assertIn("investment", RECOMMENDATION_TYPES)

    def test_recommendation_type_similar(self) -> None:
        self.assertIn("similar", RECOMMENDATION_TYPES)

    def test_recommendation_type_opportunity(self) -> None:
        self.assertIn("opportunity", RECOMMENDATION_TYPES)

    def test_recommendation_type_alert(self) -> None:
        self.assertIn("alert", RECOMMENDATION_TYPES)

    def test_recommendation_type_risk(self) -> None:
        self.assertIn("risk", RECOMMENDATION_TYPES)

    def test_document_type_title(self) -> None:
        self.assertIn("title", DOCUMENT_TYPES)

    def test_document_type_diagnostic(self) -> None:
        self.assertIn("diagnostic", DOCUMENT_TYPES)

    def test_document_type_contract(self) -> None:
        self.assertIn("contract", DOCUMENT_TYPES)

    def test_document_type_photo(self) -> None:
        self.assertIn("photo", DOCUMENT_TYPES)

    def test_document_type_plan(self) -> None:
        self.assertIn("plan", DOCUMENT_TYPES)

    def test_document_type_other(self) -> None:
        self.assertIn("other", DOCUMENT_TYPES)


class ReleaseProgramGEnginesTests(LawimTestHarness):
    def test_verification_geolocation_ok(self) -> None:
        checks = VerificationEngine().run_checks(property_row=SAMPLE_PROPERTY, owners=[{"owner_name": "A"}], documents=[])
        geo = next(c for c in checks if c["check_type"] == "geolocation")
        self.assertEqual(geo["status"], "verified")

    def test_verification_missing_geo(self) -> None:
        prop = dict(SAMPLE_PROPERTY)
        prop.pop("latitude")
        checks = VerificationEngine().run_checks(property_row=prop, owners=[{"owner_name": "A"}], documents=[])
        geo = next(c for c in checks if c["check_type"] == "geolocation")
        self.assertEqual(geo["status"], "failed")

    def test_verification_no_owner(self) -> None:
        checks = VerificationEngine().run_checks(property_row=SAMPLE_PROPERTY, owners=[], documents=[])
        owners = next(c for c in checks if c["check_type"] == "owners")
        self.assertEqual(owners["status"], "failed")

    def test_verification_title_document(self) -> None:
        docs = [{"document_type": "title"}]
        checks = VerificationEngine().run_checks(property_row=SAMPLE_PROPERTY, owners=[{"owner_name": "A"}], documents=docs)
        title = next(c for c in checks if c["check_type"] == "title")
        self.assertEqual(title["status"], "verified")

    def test_verification_price_consistency(self) -> None:
        checks = VerificationEngine().run_checks(property_row=SAMPLE_PROPERTY, owners=[{"owner_name": "A"}], documents=[{"document_type": "other"}])
        consistency = next(c for c in checks if c["check_type"] == "consistency")
        self.assertEqual(consistency["status"], "verified")

    def test_verification_aggregate_trust(self) -> None:
        checks = VerificationEngine().run_checks(property_row=SAMPLE_PROPERTY, owners=[{"owner_name": "A"}], documents=[{"document_type": "title"}])
        agg = VerificationEngine().aggregate_trust(checks)
        self.assertGreaterEqual(int(agg["trust_score"]), 50)
        self.assertIn("consistency_score", agg)

    def test_verification_empty_checks(self) -> None:
        agg = VerificationEngine().aggregate_trust([])
        self.assertEqual(agg["trust_score"], 0)

    def test_matching_engine_city(self) -> None:
        results = MatchingEngine().match(properties=[SAMPLE_PROPERTY], criteria={"city": "Douala"})
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["property_id"], 1)

    def test_matching_engine_budget(self) -> None:
        results = MatchingEngine().match(properties=[SAMPLE_PROPERTY], criteria={"budget_max": 400000})
        self.assertGreaterEqual(len(results), 1)

    def test_matching_engine_limit(self) -> None:
        props = [dict(SAMPLE_PROPERTY, id=i) for i in range(1, 6)]
        results = MatchingEngine().match(properties=props, criteria={"city": "Douala"}, limit=2)
        self.assertLessEqual(len(results), 2)

    def test_valuation_engine_estimate(self) -> None:
        estimate = ValuationEngine().estimate(property_row=SAMPLE_PROPERTY)
        self.assertGreater(int(estimate["amount"]), 0)
        self.assertEqual(estimate["currency"], "XAF")

    def test_valuation_engine_comparables(self) -> None:
        comps = [{"price_min": 280000}, {"price_min": 290000}]
        estimate = ValuationEngine().estimate(property_row=SAMPLE_PROPERTY, comparables=comps)
        self.assertGreater(int(estimate["amount"]), 0)

    def test_intelligence_engine_scores(self) -> None:
        scores = IntelligenceEngine().compute_scores(property_row=SAMPLE_PROPERTY, trust_score=80, listing_score=70)
        for key in INTELLIGENCE_SCORE_KEYS:
            self.assertIn(key, scores)
            self.assertGreaterEqual(scores[key], 0)

    def test_intelligence_engine_risk_inverse(self) -> None:
        scores = IntelligenceEngine().compute_scores(property_row=SAMPLE_PROPERTY, trust_score=90, listing_score=50)
        self.assertLessEqual(scores["risk"], scores["legal"])

    def test_listing_engine_published_score(self) -> None:
        score = ListingEngine().ai_listing_score(property_row=SAMPLE_PROPERTY, has_media=True)
        self.assertGreaterEqual(score, 50)

    def test_listing_engine_draft_score(self) -> None:
        draft = dict(SAMPLE_PROPERTY, status="draft", summary=None)
        draft.pop("latitude", None)
        score = ListingEngine().ai_listing_score(property_row=draft, has_media=False)
        self.assertLess(score, 60)

    def test_geo_engine_haversine(self) -> None:
        dist = GeoEngine().haversine_km(4.05, 9.7, 2.938, 9.907)
        self.assertGreater(dist, 100)

    def test_geo_engine_same_point(self) -> None:
        dist = GeoEngine().haversine_km(4.05, 9.7, 4.05, 9.7)
        self.assertEqual(dist, 0.0)

    def test_geo_engine_hash(self) -> None:
        h = GeoEngine().geo_hash(4.05, 9.7)
        self.assertEqual(len(h), 12)

    def test_search_engine_normalize(self) -> None:
        normalized = SearchEngine().normalize("  Bonanjo  City!!!  ")
        self.assertIn("bonanjo", normalized)

    def test_search_engine_build_index(self) -> None:
        index = SearchEngine().build_index(SAMPLE_PROPERTY)
        self.assertIn("douala", index)
        self.assertIn("bonanjo", index)

    def test_recommendation_engine_property(self) -> None:
        recs = RecommendationEngine().build_recommendations(
            matches=[{"property_id": 1, "score": 85, "reasons": ["city match"]}],
            intelligence={"investment": 60, "risk": 30},
            sources=["knowledge_platform"],
        )
        self.assertGreaterEqual(len(recs), 1)
        self.assertEqual(recs[0]["recommendation_type"], "property")

    def test_recommendation_engine_investment(self) -> None:
        recs = RecommendationEngine().build_recommendations(
            matches=[],
            intelligence={"investment": 80, "risk": 20},
            sources=["intelligent_core"],
        )
        types = {r["recommendation_type"] for r in recs}
        self.assertIn("investment", types)

    def test_recommendation_engine_risk_alert(self) -> None:
        recs = RecommendationEngine().build_recommendations(
            matches=[],
            intelligence={"investment": 50, "risk": 60},
            sources=["workflow_automation"],
        )
        types = {r["recommendation_type"] for r in recs}
        self.assertIn("risk", types)

    def test_platform_engine_sources(self) -> None:
        sources = RealEstatePlatformEngine().integration_sources()
        self.assertIn("knowledge_platform", sources)
        self.assertIn("workflow_automation", sources)

    def test_platform_engine_has_subengines(self) -> None:
        engine = RealEstatePlatformEngine()
        self.assertIsInstance(engine.verification, VerificationEngine)
        self.assertIsInstance(engine.matching, MatchingEngine)
        self.assertIsInstance(engine.search, SearchEngine)


class ReleaseProgramGRepositoryTests(LawimTestHarness):
    def _property_id(self) -> int:
        return int(self.repository.one("SELECT id FROM properties WHERE deleted_at IS NULL LIMIT 1")["id"])

    def test_list_rei_enriched_properties(self) -> None:
        rows = self.repository.list_rei_enriched_properties(limit=10)
        self.assertGreaterEqual(len(rows), 1)
        self.assertIn("property", rows[0])

    def test_get_rei_property_bundle(self) -> None:
        pid = self._property_id()
        bundle = self.repository.get_rei_property_bundle(pid)
        self.assertEqual(bundle["property"]["id"], pid)

    def test_list_rei_listings(self) -> None:
        listings = self.repository.list_rei_listings()
        self.assertGreaterEqual(len(listings), 1)

    def test_create_rei_listing(self) -> None:
        pid = self._property_id()
        listing = self.repository.create_rei_listing(property_id=pid, title="Repo test listing")
        self.assertEqual(listing["status"], "draft")

    def test_publish_rei_listing(self) -> None:
        pid = self._property_id()
        published = self.repository.publish_rei_listing(pid)
        self.assertEqual(published["status"], "published")

    def test_archive_rei_listing(self) -> None:
        pid = self._property_id()
        self.repository.publish_rei_listing(pid)
        archived = self.repository.archive_rei_listing(pid)
        self.assertEqual(archived["status"], "archived")

    def test_duplicate_rei_listing(self) -> None:
        pid = self._property_id()
        dup = self.repository.duplicate_rei_listing(pid)
        self.assertIn("copie", str(dup["title"]))

    def test_list_rei_owners(self) -> None:
        pid = self._property_id()
        owners = self.repository.list_rei_owners(pid)
        self.assertGreaterEqual(len(owners), 1)

    def test_add_rei_owner(self) -> None:
        pid = self._property_id()
        owner = self.repository.add_rei_owner(pid, owner_name="Test Owner")
        self.assertEqual(owner["owner_name"], "Test Owner")

    def test_list_rei_documents(self) -> None:
        pid = self._property_id()
        docs = self.repository.list_rei_documents(pid)
        self.assertIsInstance(docs, list)

    def test_add_rei_document(self) -> None:
        pid = self._property_id()
        doc = self.repository.add_rei_document(pid, title="Title deed", document_type="title")
        self.assertEqual(doc["document_type"], "title")

    def test_run_rei_verification(self) -> None:
        pid = self._property_id()
        score = self.repository.run_rei_verification(pid)
        self.assertIn("trust_score", score)

    def test_get_rei_valuation(self) -> None:
        pid = self._property_id()
        val = self.repository.get_rei_valuation(pid)
        self.assertGreater(int(val["amount"]), 0)

    def test_run_rei_matching(self) -> None:
        payload = self.repository.run_rei_matching(user_id=1, project_id=None, criteria={"city": "Douala"})
        self.assertIn("session_key", payload)
        self.assertIn("results", payload)

    def test_schedule_rei_visit(self) -> None:
        pid = self._property_id()
        scheduled_at = (datetime.now(timezone.utc) + timedelta(days=2)).replace(microsecond=0).isoformat()
        visit = self.repository.schedule_rei_visit(property_id=pid, user_id=1, scheduled_at=scheduled_at)
        self.assertEqual(visit["status"], "scheduled")

    def test_confirm_rei_visit(self) -> None:
        pid = self._property_id()
        scheduled_at = (datetime.now(timezone.utc) + timedelta(days=3)).replace(microsecond=0).isoformat()
        visit = self.repository.schedule_rei_visit(property_id=pid, user_id=1, scheduled_at=scheduled_at)
        confirmed = self.repository.confirm_rei_visit(int(visit["id"]))
        self.assertEqual(confirmed["status"], "confirmed")

    def test_cancel_rei_visit(self) -> None:
        pid = self._property_id()
        scheduled_at = (datetime.now(timezone.utc) + timedelta(days=4)).replace(microsecond=0).isoformat()
        visit = self.repository.schedule_rei_visit(property_id=pid, user_id=1, scheduled_at=scheduled_at)
        cancelled = self.repository.cancel_rei_visit(int(visit["id"]))
        self.assertEqual(cancelled["status"], "cancelled")

    def test_complete_rei_visit(self) -> None:
        pid = self._property_id()
        scheduled_at = (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat()
        visit = self.repository.schedule_rei_visit(property_id=pid, user_id=1, scheduled_at=scheduled_at)
        report = self.repository.complete_rei_visit(int(visit["id"]), summary="Good visit", rating=4)
        self.assertEqual(report["rating"], 4)

    def test_list_rei_visits(self) -> None:
        visits = self.repository.list_rei_visits()
        self.assertIsInstance(visits, list)

    def test_open_rei_negotiation(self) -> None:
        pid = self._property_id()
        neg = self.repository.open_rei_negotiation(property_id=pid, buyer_id=2)
        self.assertEqual(neg["status"], "open")

    def test_submit_rei_offer(self) -> None:
        pid = self._property_id()
        neg = self.repository.open_rei_negotiation(property_id=pid, buyer_id=2)
        offer = self.repository.submit_rei_offer(negotiation_id=int(neg["id"]), amount=240000)
        self.assertEqual(offer["status"], "submitted")

    def test_list_rei_negotiations(self) -> None:
        negs = self.repository.list_rei_negotiations()
        self.assertIsInstance(negs, list)

    def test_list_rei_offers(self) -> None:
        pid = self._property_id()
        neg = self.repository.open_rei_negotiation(property_id=pid, buyer_id=2)
        self.repository.submit_rei_offer(negotiation_id=int(neg["id"]), amount=200000)
        offers = self.repository.list_rei_offers(int(neg["id"]))
        self.assertGreaterEqual(len(offers), 1)

    def test_start_rei_transaction(self) -> None:
        pid = self._property_id()
        tx = self.repository.start_rei_transaction(property_id=pid, transaction_type="sale", buyer_id=2, amount=250000)
        self.assertEqual(tx["status"], "pending")

    def test_close_rei_transaction(self) -> None:
        pid = self._property_id()
        tx = self.repository.start_rei_transaction(property_id=pid, transaction_type="sale", buyer_id=2, amount=250000)
        closed = self.repository.close_rei_transaction(int(tx["id"]))
        self.assertEqual(closed["status"], "closed")

    def test_list_rei_transactions(self) -> None:
        txs = self.repository.list_rei_transactions()
        self.assertIsInstance(txs, list)

    def test_create_rei_reservation(self) -> None:
        pid = self._property_id()
        res = self.repository.create_rei_reservation(property_id=pid, user_id=2, days=5, amount=50000)
        self.assertEqual(res["status"], "pending")

    def test_build_rei_recommendations(self) -> None:
        recs = self.repository.build_rei_recommendations(user_id=2, project_id=None, criteria={"city": "Douala"})
        self.assertIsInstance(recs, list)

    def test_list_rei_recommendations(self) -> None:
        self.repository.build_rei_recommendations(user_id=2, project_id=None, criteria={"city": "Kribi"})
        recs = self.repository.list_rei_recommendations(user_id=2)
        self.assertIsInstance(recs, list)

    def test_list_rei_history(self) -> None:
        pid = self._property_id()
        history = self.repository.list_rei_history(pid)
        self.assertIsInstance(history, list)

    def test_rei_search(self) -> None:
        results = self.repository.rei_search(query="Douala")
        self.assertGreaterEqual(len(results), 1)

    def test_rei_map_properties(self) -> None:
        mapped = self.repository.rei_map_properties(city="Douala")
        self.assertGreaterEqual(len(mapped), 1)

    def test_rei_nearby(self) -> None:
        pid = self._property_id()
        nearby = self.repository.rei_nearby(pid)
        self.assertIsInstance(nearby, list)

    def test_rei_analytics(self) -> None:
        analytics = self.repository.rei_analytics()
        self.assertIn("properties", analytics)
        self.assertIn("published_listings", analytics)

    def test_rei_stats(self) -> None:
        stats = self.repository.rei_stats()
        self.assertIn("recommendations", stats)

    def test_generate_rei_report(self) -> None:
        pid = self._property_id()
        report = self.repository.generate_rei_report(pid, report_type="summary")
        self.assertEqual(report["report_type"], "summary")

    def test_compute_rei_intelligence_scores(self) -> None:
        pid = self._property_id()
        scores = self.repository.compute_rei_intelligence_scores(pid)
        for key in INTELLIGENCE_SCORE_KEYS:
            self.assertIn(key, scores)

    def test_snapshot_rei_analytics(self) -> None:
        snap = self.repository.snapshot_rei_analytics()
        self.assertIn("snapshot_key", snap)
        self.assertIn("metrics", snap)


class ReleaseProgramGApiTests(LawimTestHarness):
    def _property_id(self, token: str) -> int:
        payload = self.invoke("/api/v2/properties?limit=1", token=token).body_json()
        return int(payload["properties"][0]["property"]["id"])

    def _project_id(self, token: str) -> int:
        return int(self.invoke("/api/v2/projects?limit=1", token=token).body_json()["projects"][0]["id"])

    def test_properties_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/properties", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["properties"]), 1)

    def test_properties_detail_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("property", response.body_json())

    def test_properties_listings_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/properties/listings", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("listings", response.body_json())

    def test_properties_recommendations_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/properties/recommendations", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_visits_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/properties/visits", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_negotiations_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/properties/negotiations", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_transactions_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/properties/transactions", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_search_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/properties/search?q=Douala", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("results", response.body_json())

    def test_properties_map_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/properties/map?city=Douala", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_analytics_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/properties/analytics", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_stats_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/properties/stats", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("stats", response.body_json())

    def test_properties_owners_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/owners", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_documents_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/documents", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_verification_get_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/verification", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_valuation_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/valuation", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_history_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/history", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_nearby_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/nearby", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_media_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/media", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_intelligence_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/intelligence", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_scores_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/scores", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_reports_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/reports?type=summary", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_create_listing_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(
            "/api/v2/properties/listings",
            method="POST",
            token=token,
            body={"property_id": pid, "title": "API listing test"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_properties_matching_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke(
            "/api/v2/properties/matching",
            method="POST",
            token=token,
            body={"criteria": {"city": "Douala", "budget_max": 500000}},
        )
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("results", response.body_json())

    def test_properties_recommendations_post_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke(
            "/api/v2/properties/recommendations",
            method="POST",
            token=token,
            body={"criteria": {"city": "Douala"}},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_schedule_visit_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        scheduled_at = (datetime.now(timezone.utc) + timedelta(days=2)).replace(microsecond=0).isoformat()
        response = self.invoke(
            "/api/v2/properties/visits",
            method="POST",
            token=token,
            body={"property_id": pid, "scheduled_at": scheduled_at},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_properties_confirm_visit_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        scheduled_at = (datetime.now(timezone.utc) + timedelta(days=5)).replace(microsecond=0).isoformat()
        created = self.invoke(
            "/api/v2/properties/visits",
            method="POST",
            token=token,
            body={"property_id": pid, "scheduled_at": scheduled_at},
        )
        visit_id = int(created.body_json()["visit"]["id"])
        response = self.invoke(f"/api/v2/properties/visits/{visit_id}/confirm", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_cancel_visit_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        scheduled_at = (datetime.now(timezone.utc) + timedelta(days=6)).replace(microsecond=0).isoformat()
        created = self.invoke(
            "/api/v2/properties/visits",
            method="POST",
            token=token,
            body={"property_id": pid, "scheduled_at": scheduled_at},
        )
        visit_id = int(created.body_json()["visit"]["id"])
        response = self.invoke(f"/api/v2/properties/visits/{visit_id}/cancel", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_complete_visit_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        scheduled_at = (datetime.now(timezone.utc) + timedelta(days=1)).replace(microsecond=0).isoformat()
        created = self.invoke(
            "/api/v2/properties/visits",
            method="POST",
            token=token,
            body={"property_id": pid, "scheduled_at": scheduled_at},
        )
        visit_id = int(created.body_json()["visit"]["id"])
        response = self.invoke(
            f"/api/v2/properties/visits/{visit_id}/complete",
            method="POST",
            token=token,
            body={"summary": "Visit completed via API", "rating": 5},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_open_negotiation_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(
            "/api/v2/properties/negotiations",
            method="POST",
            token=token,
            body={"property_id": pid},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_properties_submit_offer_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        neg = self.invoke(
            "/api/v2/properties/negotiations",
            method="POST",
            token=token,
            body={"property_id": pid},
        )
        negotiation_id = int(neg.body_json()["negotiation"]["id"])
        response = self.invoke(
            "/api/v2/properties/offers",
            method="POST",
            token=token,
            body={"negotiation_id": negotiation_id, "amount": 230000},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_properties_negotiation_offers_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        neg = self.invoke(
            "/api/v2/properties/negotiations",
            method="POST",
            token=token,
            body={"property_id": pid},
        )
        negotiation_id = int(neg.body_json()["negotiation"]["id"])
        self.invoke(
            "/api/v2/properties/offers",
            method="POST",
            token=token,
            body={"negotiation_id": negotiation_id, "amount": 220000},
        )
        response = self.invoke(f"/api/v2/properties/negotiations/{negotiation_id}/offers", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_start_transaction_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(
            "/api/v2/properties/transactions",
            method="POST",
            token=token,
            body={"property_id": pid, "transaction_type": "sale", "amount": 260000},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_properties_close_transaction_api(self) -> None:
        admin = self.login(email="admin@lawim.local")
        agent = self.login(email="agent@lawim.local")
        pid = self._property_id(agent)
        created = self.invoke(
            "/api/v2/properties/transactions",
            method="POST",
            token=agent,
            body={"property_id": pid, "transaction_type": "sale", "amount": 270000},
        )
        tx_id = int(created.body_json()["transaction"]["id"])
        response = self.invoke(f"/api/v2/properties/transactions/{tx_id}/close", method="POST", token=admin, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_reservation_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(
            "/api/v2/properties/reservations",
            method="POST",
            token=token,
            body={"property_id": pid, "days": 7, "amount": 25000},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_properties_publish_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/publish", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_archive_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        pid = self._property_id(token)
        self.invoke(f"/api/v2/properties/{pid}/publish", method="POST", token=token, body={})
        response = self.invoke(f"/api/v2/properties/{pid}/archive", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_properties_duplicate_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/duplicate", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_properties_add_owner_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(
            f"/api/v2/properties/{pid}/owners",
            method="POST",
            token=token,
            body={"owner_name": "API Owner", "owner_type": "individual"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_properties_add_document_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(
            f"/api/v2/properties/{pid}/documents",
            method="POST",
            token=token,
            body={"title": "API diagnostic", "document_type": "diagnostic"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_properties_verification_post_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        response = self.invoke(f"/api/v2/properties/{pid}/verification", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)


class ReleaseProgramGUiTests(LawimTestHarness):
    def test_index_has_real_estate_intelligence_section(self) -> None:
        html = self.invoke("/")
        self.assertIn("Real Estate Intelligence", html.body_text())

    def test_app_js_references_rei_api(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/properties/stats", js.body_text())
        self.assertIn("refreshReiAdmin", js.body_text())


class ReleaseProgramGHealthTests(LawimTestHarness):
    def test_health_schema_v13(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.body_json()["database"]["schema_version"], 15)

    def test_migration_strategy_v13(self) -> None:
        self.assertEqual(migration_strategy_profile()["schema_version"], 15)

    def test_metrics_include_property_counters(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/properties?limit=1", token=token)
        admin = self.login(email="admin@lawim.local")
        metrics = self.invoke("/api/metrics", token=admin)
        snapshot = metrics.body_json()["metrics"]
        self.assertGreaterEqual(snapshot.get("property_list_total", 0), 1)


class ReleaseProgramGV13TableTests(LawimTestHarness):
    def _table_names(self) -> set[str]:
        return {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}

    def test_v13_table_rei_property_profiles(self) -> None:
        self.assertIn("rei_property_profiles", self._table_names())

    def test_v13_table_rei_listings(self) -> None:
        self.assertIn("rei_listings", self._table_names())

    def test_v13_table_rei_listing_publications(self) -> None:
        self.assertIn("rei_listing_publications", self._table_names())

    def test_v13_table_rei_listing_scores(self) -> None:
        self.assertIn("rei_listing_scores", self._table_names())

    def test_v13_table_rei_property_owners(self) -> None:
        self.assertIn("rei_property_owners", self._table_names())

    def test_v13_table_rei_property_documents(self) -> None:
        self.assertIn("rei_property_documents", self._table_names())

    def test_v13_table_rei_property_valuations(self) -> None:
        self.assertIn("rei_property_valuations", self._table_names())

    def test_v13_table_rei_verification_checks(self) -> None:
        self.assertIn("rei_verification_checks", self._table_names())

    def test_v13_table_rei_verification_scores(self) -> None:
        self.assertIn("rei_verification_scores", self._table_names())

    def test_v13_table_rei_matching_sessions(self) -> None:
        self.assertIn("rei_matching_sessions", self._table_names())

    def test_v13_table_rei_matching_results(self) -> None:
        self.assertIn("rei_matching_results", self._table_names())

    def test_v13_table_rei_visits(self) -> None:
        self.assertIn("rei_visits", self._table_names())

    def test_v13_table_rei_visit_reports(self) -> None:
        self.assertIn("rei_visit_reports", self._table_names())

    def test_v13_table_rei_negotiations(self) -> None:
        self.assertIn("rei_negotiations", self._table_names())

    def test_v13_table_rei_offers(self) -> None:
        self.assertIn("rei_offers", self._table_names())

    def test_v13_table_rei_transactions(self) -> None:
        self.assertIn("rei_transactions", self._table_names())

    def test_v13_table_rei_reservations(self) -> None:
        self.assertIn("rei_reservations", self._table_names())

    def test_v13_table_rei_property_history(self) -> None:
        self.assertIn("rei_property_history", self._table_names())

    def test_v13_table_rei_recommendations(self) -> None:
        self.assertIn("rei_recommendations", self._table_names())

    def test_v13_table_rei_intelligence_scores(self) -> None:
        self.assertIn("rei_intelligence_scores", self._table_names())

    def test_v13_table_rei_analytics_snapshots(self) -> None:
        self.assertIn("rei_analytics_snapshots", self._table_names())

    def test_v13_table_rei_search_index(self) -> None:
        self.assertIn("rei_search_index", self._table_names())

    def test_v13_table_rei_nearby_properties(self) -> None:
        self.assertIn("rei_nearby_properties", self._table_names())

    def test_v13_table_rei_property_reports(self) -> None:
        self.assertIn("rei_property_reports", self._table_names())


class ReleaseProgramGIntegrationTests(LawimTestHarness):
    def _property_id(self) -> int:
        return int(self.repository.one("SELECT id FROM properties WHERE deleted_at IS NULL LIMIT 1")["id"])

    def test_visit_scheduling_may_start_workflow(self) -> None:
        before = self.repository.scalar("SELECT COUNT(*) FROM automation_process_instances")
        pid = self._property_id()
        scheduled_at = (datetime.now(timezone.utc) + timedelta(days=2)).replace(microsecond=0).isoformat()
        self.repository.schedule_rei_visit(property_id=pid, user_id=1, scheduled_at=scheduled_at)
        after = self.repository.scalar("SELECT COUNT(*) FROM automation_process_instances")
        self.assertGreaterEqual(after, before)

    def test_negotiation_may_link_workflow(self) -> None:
        pid = self._property_id()
        neg = self.repository.open_rei_negotiation(property_id=pid, buyer_id=2)
        self.assertIn("workflow_instance_id", neg)

    def test_transaction_may_link_workflow(self) -> None:
        pid = self._property_id()
        tx = self.repository.start_rei_transaction(property_id=pid, transaction_type="sale", buyer_id=2, amount=250000)
        self.assertIn("workflow_instance_id", tx)

    def test_recommendations_include_platform_sources(self) -> None:
        recs = self.repository.build_rei_recommendations(
            user_id=2,
            project_id=None,
            criteria={"city": "Douala", "query": "achat immobilier"},
        )
        self.assertGreaterEqual(len(recs), 1)
        sources = RealEstatePlatformEngine().integration_sources()
        self.assertIn("knowledge_platform", sources)

    def test_recommendations_with_knowledge_query(self) -> None:
        recs = self.repository.build_rei_recommendations(
            user_id=2,
            project_id=None,
            criteria={"city": "Kribi", "query": "compromis de vente"},
        )
        self.assertIsInstance(recs, list)


class ReleaseProgramGObservabilityTests(LawimTestHarness):
    def _property_id(self, token: str) -> int:
        payload = self.invoke("/api/v2/properties?limit=1", token=token).body_json()
        return int(payload["properties"][0]["property"]["id"])

    def test_property_list_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/properties", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["property_list_total"], 1)

    def test_property_detail_counter(self) -> None:
        agent = self.login(email="agent@lawim.local")
        pid = self._property_id(agent)
        self.invoke(f"/api/v2/properties/{pid}", token=agent)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["property_detail_total"], 1)

    def test_property_search_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/properties/search?q=Douala", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["property_search_total"], 1)

    def test_listing_list_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/properties/listings", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["listing_list_total"], 1)

    def test_listing_created_counter(self) -> None:
        admin = self.login(email="admin@lawim.local")
        pid = self._property_id(admin)
        self.invoke(
            "/api/v2/properties/listings",
            method="POST",
            token=admin,
            body={"property_id": pid, "title": "Metrics listing"},
        )
        metrics = self.invoke("/api/metrics", token=admin)
        self.assertGreaterEqual(metrics.body_json()["metrics"]["listing_created_total"], 1)

    def test_verification_run_counter(self) -> None:
        agent = self.login(email="agent@lawim.local")
        pid = self._property_id(agent)
        self.invoke(f"/api/v2/properties/{pid}/verification", method="POST", token=agent, body={})
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["verification_run_total"], 1)

    def test_matching_run_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke(
            "/api/v2/properties/matching",
            method="POST",
            token=token,
            body={"criteria": {"city": "Douala"}},
        )
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["matching_run_total"], 1)

    def test_recommendation_generated_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke(
            "/api/v2/properties/recommendations",
            method="POST",
            token=token,
            body={"criteria": {"city": "Douala"}},
        )
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["recommendation_generated_total"], 1)

    def test_visit_scheduled_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        scheduled_at = (datetime.now(timezone.utc) + timedelta(days=3)).replace(microsecond=0).isoformat()
        self.invoke(
            "/api/v2/properties/visits",
            method="POST",
            token=token,
            body={"property_id": pid, "scheduled_at": scheduled_at},
        )
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["visit_scheduled_total"], 1)

    def test_transaction_started_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        self.invoke(
            "/api/v2/properties/transactions",
            method="POST",
            token=token,
            body={"property_id": pid, "transaction_type": "sale", "amount": 250000},
        )
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["transaction_started_total"], 1)

    def test_intelligence_computed_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        self.invoke(f"/api/v2/properties/{pid}/intelligence", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["intelligence_computed_total"], 1)

    def test_valuation_computed_counter(self) -> None:
        token = self.login(email="agent@lawim.local")
        pid = self._property_id(token)
        self.invoke(f"/api/v2/properties/{pid}/valuation", token=token)
        metrics = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertGreaterEqual(metrics.body_json()["metrics"]["valuation_computed_total"], 1)
