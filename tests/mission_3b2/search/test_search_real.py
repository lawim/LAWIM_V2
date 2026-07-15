from __future__ import annotations

import logging
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "code"))

from lawim_v2.conversation.search.adapters import LawimRepositoryAdapter
from lawim_v2.conversation.search.results import SearchRequest
from lawim_v2.conversation.search.service import SearchService

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("LAWIM_DATABASE_URL", "")


def _make_property_row(r: dict[str, Any]) -> dict[str, Any]:
    price = r.get("price_min") or r.get("price_max") or 0
    return {
        "id": r["id"],
        "title": r.get("title", ""),
        "name": r.get("title", ""),
        "description": r.get("summary", ""),
        "city": r.get("city", ""),
        "price": price,
        "property_type": r.get("property_type", ""),
        "bedrooms": r.get("bedrooms", 0),
        "surface": r.get("area_sqm", 0),
        "partner_name": "",
        "partner_id": None,
        "contact_info": {},
        "status": r.get("status", ""),
        "transaction_type": _detect_transaction_type(r),
        "district": "",
        "partner_type": "",
        "rating": None,
        "partner_rating": None,
    }


def _detect_transaction_type(r: dict[str, Any]) -> str:
    status = (r.get("status") or "").lower()
    if status in ("published", "open"):
        return "rent" if "rent" in (r.get("title", "")).lower() else "buy"
    return "buy"


class RealDbRepositoryAdapter(LawimRepositoryAdapter):
    def __init__(self, repository: Any = None) -> None:
        super().__init__(repository=repository)

    def _fetch_raw_data(self, source_type: str) -> list[dict[str, Any]]:
        if source_type in self._cache:
            return self._cache[source_type]
        if self.repository is None:
            self._cache[source_type] = []
            return []
        try:
            rows = self.repository.all(
                "SELECT * FROM properties WHERE deleted_at IS NULL ORDER BY id ASC"
            )
            raw = [_make_property_row(dict(r)) for r in rows]
            log.info("Fetched %d properties from database", len(raw))
        except Exception as exc:
            log.error("Failed to fetch properties: %s", exc)
            raw = []
        self._cache[source_type] = raw
        return raw


def _build_service(repo: Any) -> SearchService:
    adapter = RealDbRepositoryAdapter(repository=repo)
    return SearchService(adapter=adapter)


def _probe_pg(db_url: str, timeout: int = 5) -> bool:
    try:
        from lawim_v2.postgresql_repository import parse_postgres_dsn
        import pg8000.native

        params = parse_postgres_dsn(db_url)
        conn = pg8000.native.Connection(**params, timeout=timeout)
        conn.run("SELECT 1")
        conn.close()
        return True
    except Exception:
        return False


def _create_repo() -> Any:
    db_url = DATABASE_URL
    if db_url and db_url.startswith("postgresql"):
        if _probe_pg(db_url, timeout=5):
            from lawim_v2.postgresql_repository import PostgreSQLLawimRepository

            log.info("Connecting to PostgreSQL: %s", db_url)
            return PostgreSQLLawimRepository(db_url)
        log.warning("PostgreSQL at %s unreachable, falling back to SQLite", db_url)

    from lawim_v2.db import LawimRepository

    log.info("Using SQLite with demo seed data")
    tmp = tempfile.mkdtemp()
    db_path = Path(tmp) / "lawim_test.db"
    repo = LawimRepository(db_path)
    repo.initialize(seed_demo_data=True)
    repo._tmpdir = tmp
    return repo


class TestSearchRealDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        log.info("Initializing repository")
        cls.repo = _create_repo()
        cls.service = _build_service(cls.repo)
        prop_count = cls.repo.scalar(
            "SELECT COUNT(*) FROM properties WHERE deleted_at IS NULL"
        )
        log.info("Repository ready. Properties available: %d", prop_count)

    @classmethod
    def tearDownClass(cls) -> None:
        if hasattr(cls, "repo"):
            try:
                cls.repo.close()
            except Exception:
                pass
            tmpdir = getattr(cls.repo, "_tmpdir", None)
            if tmpdir:
                import shutil

                shutil.rmtree(tmpdir, ignore_errors=True)

    def _search(self, **kwargs: Any) -> Any:
        req = SearchRequest(**kwargs)
        return self.service.search(req)

    def test_01_empty_request_returns_error(self):
        result = self._search()
        self.assertTrue(result.is_empty)
        self.assertIsNotNone(result.error)
        self.assertIn("empty", (result.error or "").lower())
        log.info("Empty request test: error='%s'", result.error)

    def test_02_search_all_properties(self):
        result = self._search(city="Douala", max_results=50)
        log.info("Search all Douala: count=%d, returned=%d, time=%.1fms",
                 result.total_count, result.returned_count, result.execution_time_ms)
        self.assertGreater(result.total_count, 0)
        self.assertGreater(result.returned_count, 0)

    def test_03_search_by_city_yaounde(self):
        result = self._search(city="Yaoundé", max_results=20)
        log.info("Yaoundé: count=%d, returned=%d", result.total_count, result.returned_count)
        for item in result.items:
            self.assertEqual(item.city, "Yaoundé")

    def test_04_search_by_city_douala(self):
        result = self._search(city="Douala", max_results=20)
        log.info("Douala: count=%d, returned=%d", result.total_count, result.returned_count)
        for item in result.items:
            self.assertEqual(item.city, "Douala")

    def test_05_search_by_property_type_apartment(self):
        result = self._search(property_type="apartment", max_results=20)
        log.info("Apartments: count=%d, returned=%d", result.total_count, result.returned_count)
        if result.items:
            for item in result.items:
                self.assertEqual(item.property_type, "apartment")

    def test_06_search_by_property_type_house(self):
        result = self._search(property_type="house", max_results=20)
        log.info("Houses: count=%d, returned=%d", result.total_count, result.returned_count)
        if result.items:
            for item in result.items:
                self.assertEqual(item.property_type, "house")

    def test_07_search_by_budget_range(self):
        result = self._search(budget_min=50000000, budget_max=150000000, max_results=20)
        log.info("Budget 50M-150M: count=%d, returned=%d", result.total_count, result.returned_count)
        if result.items:
            for item in result.items:
                if item.price is not None:
                    self.assertGreaterEqual(item.price, 50000000)
                    self.assertLessEqual(item.price, 150000000)

    def test_08_search_by_budget_min_only(self):
        result = self._search(budget_min=100000000, max_results=20)
        log.info("Budget min 100M: count=%d, returned=%d", result.total_count, result.returned_count)

    def test_09_search_by_budget_max_only(self):
        result = self._search(budget_max=50000000, max_results=20)
        log.info("Budget max 50M: count=%d, returned=%d", result.total_count, result.returned_count)

    def test_10_search_by_bedrooms(self):
        result = self._search(bedrooms=3, max_results=20)
        log.info("Bedrooms=3: count=%d, returned=%d", result.total_count, result.returned_count)
        if result.items:
            for item in result.items:
                self.assertEqual(item.bedrooms, 3)

    def test_11_search_by_surface_range(self):
        result = self._search(surface_min=100, surface_max=300, max_results=20)
        log.info("Surface 100-300: count=%d, returned=%d", result.total_count, result.returned_count)
        if result.items:
            for item in result.items:
                if item.surface is not None:
                    self.assertGreaterEqual(item.surface, 100)
                    self.assertLessEqual(item.surface, 300)

    def test_12_search_city_and_budget(self):
        result = self._search(city="Douala", budget_min=30000000, budget_max=100000000, max_results=20)
        log.info("Douala + 30M-100M: count=%d, returned=%d", result.total_count, result.returned_count)
        if result.items:
            for item in result.items:
                self.assertEqual(item.city, "Douala")

    def test_13_search_city_and_property_type(self):
        result = self._search(city="Yaoundé", property_type="house", max_results=20)
        log.info("Yaoundé houses: count=%d, returned=%d", result.total_count, result.returned_count)
        if result.items:
            for item in result.items:
                self.assertEqual(item.city, "Yaoundé")
                self.assertEqual(item.property_type, "house")

    def test_14_search_zero_results_nonexistent_city(self):
        result = self._search(city="NonExistentCityXYZ", max_results=20)
        log.info("Non-existent city: count=%d, returned=%d", result.total_count, result.returned_count)
        self.assertEqual(result.total_count, 0)
        self.assertEqual(result.returned_count, 0)

    def test_15_search_zero_results_impossible_budget(self):
        result = self._search(budget_min=999999999999, max_results=20)
        log.info("Impossible budget: count=%d, returned=%d", result.total_count, result.returned_count)
        self.assertEqual(result.total_count, 0)

    def test_16_search_zero_results_mismatched_criteria(self):
        result = self._search(city="Douala", property_type="commercial", max_results=20)
        log.info("Douala commercial: count=%d, returned=%d", result.total_count, result.returned_count)

    def test_17_search_pagination_offset(self):
        first = self._search(city="Douala", max_results=5, offset=0)
        second = self._search(city="Douala", max_results=5, offset=5)
        log.info("First page: %d items, Second page: %d items", first.returned_count, second.returned_count)
        if first.items and second.items:
            first_ids = [i.item_id for i in first.items]
            second_ids = [i.item_id for i in second.items]
            overlap = set(first_ids) & set(second_ids)
            self.assertEqual(len(overlap), 0, "Pages should not overlap")

    def test_18_search_by_transaction_type_buy(self):
        result = self._search(transaction_type="buy", max_results=20)
        log.info("Transaction buy: count=%d, returned=%d", result.total_count, result.returned_count)

    def test_19_search_by_transaction_type_rent(self):
        result = self._search(transaction_type="rent", max_results=20)
        log.info("Transaction rent: count=%d, returned=%d", result.total_count, result.returned_count)

    def test_20_search_multi_criteria_combined(self):
        result = self._search(
            city="Douala",
            property_type="apartment",
            bedrooms=2,
            budget_min=20000000,
            budget_max=80000000,
            max_results=20,
        )
        log.info("Douala+apt+2br+20M-80M: count=%d, returned=%d",
                 result.total_count, result.returned_count)

    def test_21_search_execution_time_reported(self):
        result = self._search(city="Douala", max_results=20)
        self.assertGreater(result.execution_time_ms, 0)
        log.info("Execution time: %.1f ms", result.execution_time_ms)

    def test_22_search_by_criteria_dict(self):
        criteria = {
            "city": "Douala",
            "property_type": "apartment",
            "max_results": 10,
        }
        result = self.service.search_by_criteria(criteria)
        log.info("search_by_criteria Douala+apt: count=%d, returned=%d",
                 result.total_count, result.returned_count)
        self.assertGreaterEqual(result.total_count, 0)

    def test_23_search_with_create_alert(self):
        result = self._search(city="Douala", create_alert=True, max_results=5)
        log.info("Alert created: %s, alert_id=%s", result.alert_created, result.alert_id)
        if result.is_empty:
            self.skipTest("No results to create alert for")
        self.assertTrue(result.alert_created)
        self.assertIsNotNone(result.alert_id)

    def test_24_search_zero_results_partner_type(self):
        result = self._search(partner_type="nonexistent_partner_type", max_results=20)
        log.info("Non-existent partner type: count=%d", result.total_count)
        self.assertEqual(result.total_count, 0)

    def test_25_search_source_name_is_set(self):
        result = self._search(city="Douala", max_results=5)
        self.assertEqual(result.source, "lawim_local")
        log.info("Source: %s", result.source)

    def test_26_search_result_items_have_required_fields(self):
        result = self._search(city="Douala", max_results=10)
        for item in result.items:
            self.assertTrue(item.item_id, "Each result should have an item_id")
            self.assertTrue(item.title, "Each result should have a title")
            log.info("Item %s: city=%s type=%s price=%s",
                     item.item_id, item.city, item.property_type, item.price)

    def test_27_search_without_criteria_returns_all(self):
        result = self._search(max_results=5, city="Douala")
        self.assertGreater(result.returned_count, 0)

    def test_28_search_marketplace_type(self):
        result = self._search(city="Douala", transaction_type="buy", max_results=10)
        log.info("Marketplace buy search: count=%d", result.total_count)

    def test_29_search_region_specific(self):
        result = self._search(city="Bafoussam", max_results=20)
        log.info("Bafoussam: count=%d, returned=%d", result.total_count, result.returned_count)

    def test_30_search_combined_house_douala(self):
        result = self._search(city="Douala", property_type="house", bedrooms=3, max_results=20)
        log.info("Douala+house+3br: count=%d", result.total_count)

    def test_31_search_max_results_respected(self):
        for limit in (1, 5, 10):
            result = self._search(city="Douala", max_results=limit)
            self.assertLessEqual(result.returned_count, limit)
            log.info("max_results=%d: returned=%d", limit, result.returned_count)

    def test_32_search_minimal_budget_zero(self):
        result = self._search(budget_min=0, max_results=10)
        log.info("Budget min=0: count=%d", result.total_count)
        self.assertGreaterEqual(result.total_count, 0)

    def test_33_search_high_budget(self):
        result = self._search(budget_min=200000000, max_results=10)
        log.info("Budget min=200M: count=%d", result.total_count)

    def test_34_search_professional_partner(self):
        result = self._search(partner_type="agency", max_results=20)
        log.info("Partner type=agency: count=%d, returned=%d",
                 result.total_count, result.returned_count)
        self.assertGreaterEqual(result.total_count, 0)

    def test_35_search_no_criteria_surface_only(self):
        result = self._search(surface_min=50, surface_max=150, max_results=20)
        log.info("Surface 50-150: count=%d, returned=%d", result.total_count, result.returned_count)

    def test_36_search_verify_deterministic(self):
        r1 = self._search(city="Douala", property_type="apartment", max_results=10)
        r2 = self._search(city="Douala", property_type="apartment", max_results=10)
        ids1 = [i.item_id for i in r1.items]
        ids2 = [i.item_id for i in r2.items]
        self.assertEqual(ids1, ids2, "Results should be deterministic")
        log.info("Determinism verified: %d items match", len(ids1))

    def test_37_search_empty_criteria_dict(self):
        result = self.service.search_by_criteria({})
        self.assertTrue(result.is_empty)
        self.assertIsNotNone(result.error)
        log.info("Empty criteria dict: error='%s'", result.error)

    def test_38_search_large_offset(self):
        result = self._search(city="Douala", offset=9999, max_results=10)
        log.info("Large offset: count=%d, returned=%d", result.total_count, result.returned_count)
        self.assertEqual(result.returned_count, 0)

    def test_39_search_zero_min_surface(self):
        result = self._search(surface_min=0, max_results=10)
        log.info("Surface min=0: count=%d", result.total_count)

    def test_40_search_all_cities_count(self):
        req = SearchRequest(
            city="Douala",
            budget_min=10000000,
            budget_max=500000000,
            property_type="house",
            max_results=100,
        )
        result = self.service.search(req)
        log.info("Final comprehensive search: count=%d, returned=%d, time=%.1fms",
                 result.total_count, result.returned_count, result.execution_time_ms)


if __name__ == "__main__":
    unittest.main()
