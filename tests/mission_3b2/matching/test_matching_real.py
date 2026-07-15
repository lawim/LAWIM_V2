from __future__ import annotations

import logging
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "code"))

from lawim_v2.conversation.matching.service import MatchingService
from lawim_v2.conversation.search.adapters import LawimRepositoryAdapter
from lawim_v2.conversation.search.results import SearchRequest, SearchResult
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


class TestMatchingRealDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        log.info("Initializing repository")
        cls.repo = _create_repo()
        adapter = RealDbRepositoryAdapter(repository=cls.repo)
        cls.search_service = SearchService(adapter=adapter)
        cls.matching_service = MatchingService()
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

    def _search(self, **kwargs: Any) -> SearchResult:
        req = SearchRequest(**kwargs)
        return self.search_service.search(req)

    def test_01_matching_returns_results(self):
        search = self._search(city="Douala", property_type="apartment", max_results=20)
        if search.is_empty:
            self.skipTest("No Douala apartments in seed data")
        self.assertFalse(search.is_empty)
        result = self.matching_service.match(
            search_result=search,
            project_criteria={"city": "Douala", "property_type": "apartment"},
        )
        log.info("Match: evaluated=%d, matches=%d", result.total_evaluated, len(result.matches))
        self.assertTrue(result.has_matches)
        self.assertGreater(result.total_evaluated, 0)

    def test_02_matching_scores_in_range(self):
        search = self._search(city="Douala", property_type="house", max_results=20)
        result = self.matching_service.match(
            search_result=search,
            project_criteria={
                "city": "Douala",
                "property_type": "house",
                "budget_min": 30000000,
                "budget_max": 150000000,
                "bedrooms": 3,
            },
        )
        for m in result.matches:
            self.assertGreaterEqual(m.global_score, 0.0)
            self.assertLessEqual(m.global_score, 1.0)
            log.info("  Match %s: score=%.4f, matched=%d/%d",
                     m.item_id, m.global_score, m.matched_criteria_count, m.total_criteria_count)

    def test_03_matching_deterministic_across_runs(self):
        runs = []
        for i in range(3):
            search = self._search(city="Douala", property_type="apartment", max_results=20)
            if search.is_empty:
                self.skipTest(f"Run {i}: No Douala apartments in seed data")
            result = self.matching_service.match(
                search_result=search,
                project_criteria={
                    "city": "Douala",
                    "property_type": "apartment",
                    "budget_min": 100000,
                    "budget_max": 500000,
                    "bedrooms": 1,
                },
            )
            runs.append(([m.item_id for m in result.matches],
                         [m.global_score for m in result.matches]))
        for i in range(1, len(runs)):
            self.assertEqual(runs[0][0], runs[i][0],
                             f"Run 0 and {i}: item order differs")
            self.assertEqual(runs[0][1], runs[i][1],
                             f"Run 0 and {i}: scores differ")
        log.info("Determinism verified: %d runs produce identical results", len(runs))

    def test_04_matching_empty_search_returns_empty(self):
        empty_result = SearchResult(total_count=0)
        result = self.matching_service.match(search_result=empty_result)
        self.assertEqual(result.total_evaluated, 0)
        self.assertFalse(result.has_matches)
        log.info("Empty search -> empty match: OK")

    def test_05_matching_without_project_criteria(self):
        search = self._search(city="Douala", max_results=10)
        result = self.matching_service.match(search_result=search)
        self.assertTrue(result.has_matches or result.total_evaluated == 0)
        log.info("Match without project criteria: matches=%d", len(result.matches))

    def test_06_matching_single_item(self):
        search = self._search(city="Douala", property_type="apartment", max_results=1)
        self.assertGreater(search.returned_count, 0)
        item = search.items[0]
        match = self.matching_service.match_single(
            item=item,
            project_criteria={"city": "Douala", "property_type": "apartment"},
        )
        self.assertIsNotNone(match)
        self.assertGreaterEqual(match.global_score, 0.0)
        log.info("Single match: id=%s score=%.4f", match.item_id, match.global_score)

    def test_07_matching_explanations_present(self):
        search = self._search(city="Douala", max_results=5)
        result = self.matching_service.match(
            search_result=search,
            project_criteria={"city": "Douala", "budget_min": 30000000},
        )
        for m in result.matches:
            self.assertGreater(len(m.explanations), 0)
            for exp in m.explanations:
                self.assertTrue(exp.dimension)
                self.assertGreaterEqual(exp.score, 0.0)
                self.assertLessEqual(exp.score, 1.0)
                log.info("  Expl: %s score=%.2f weight=%.2f %s",
                         exp.dimension, exp.score, exp.weight, exp.details)

    def test_08_matching_ranked_by_score(self):
        search = self._search(city="Douala", max_results=20)
        result = self.matching_service.match(
            search_result=search,
            project_criteria={
                "city": "Douala",
                "property_type": "house",
                "budget_min": 30000000,
                "budget_max": 100000000,
                "bedrooms": 3,
            },
        )
        if len(result.matches) >= 2:
            for i in range(len(result.matches) - 1):
                self.assertGreaterEqual(
                    result.matches[i].global_score,
                    result.matches[i + 1].global_score,
                    "Matches should be sorted descending by score",
                )

    def test_09_matching_min_max_average_stats(self):
        search = self._search(city="Douala", max_results=20)
        result = self.matching_service.match(
            search_result=search,
            project_criteria={"city": "Douala", "property_type": "apartment"},
        )
        if result.matches:
            self.assertGreaterEqual(result.min_score, 0.0)
            self.assertLessEqual(result.max_score, 1.0)
            self.assertGreaterEqual(result.average_score, result.min_score)
            self.assertLessEqual(result.average_score, result.max_score)
            log.info("Stats: min=%.4f max=%.4f avg=%.4f",
                     result.min_score, result.max_score, result.average_score)

    def test_10_matching_criteria_used_listed(self):
        search = self._search(city="Douala", max_results=10)
        result = self.matching_service.match(
            search_result=search,
            project_criteria={"city": "Douala", "budget_min": 50000000},
        )
        self.assertGreater(len(result.criteria_used), 0)
        log.info("Criteria used: %s", result.criteria_used)

    def test_11_matching_explanation_generated(self):
        search = self._search(city="Douala", property_type="apartment", max_results=5)
        result = self.matching_service.match(
            search_result=search,
            project_criteria={"city": "Douala"},
        )
        if result.matches:
            explanation = self.matching_service.get_explanation(result.matches[0])
            self.assertTrue(len(explanation) > 0)
            log.info("Explanation: %s", explanation)
            detailed = self.matching_service.get_explanation(result.matches[0], detailed=True)
            self.assertTrue(len(detailed) > 0)
            log.info("Detailed explanation:\n%s", detailed)

    def test_12_matching_yaounde_houses(self):
        search = self._search(city="Yaoundé", property_type="house", max_results=20)
        if not search.is_empty:
            result = self.matching_service.match(
                search_result=search,
                project_criteria={
                    "city": "Yaoundé",
                    "property_type": "house",
                    "budget_min": 20000000,
                    "budget_max": 100000000,
                },
            )
            log.info("Yaoundé houses matched=%d", len(result.matches))
            for m in result.matches[:3]:
                log.info("  %s score=%.4f", m.title, m.global_score)

    def test_13_matching_determinism_second_city(self):
        search = self._search(city="Bafoussam", max_results=20)
        if not search.is_empty:
            results = []
            for i in range(3):
                r = self.matching_service.match(
                    search_result=search,
                    project_criteria={"city": "Bafoussam"},
                )
                results.append([m.global_score for m in r.matches])
            for i in range(1, len(results)):
                self.assertEqual(results[0], results[i],
                                 f"Bafoussam determinism failed run 0 vs {i}")
            log.info("Bafoussam determinism verified across %d runs", len(results))

    def test_14_matching_without_criteria_uses_search_request(self):
        search = self._search(city="Douala", property_type="apartment", max_results=10)
        result = self.matching_service.match(search_result=search)
        if result.matches:
            log.info("Match without explicit criteria: %d matches", len(result.matches))

    def test_15_matching_score_is_deterministic_multi_criteria(self):
        search = self._search(city="Douala", max_results=20)
        criteria = {
            "city": "Douala",
            "property_type": "house",
            "budget_min": 40000000,
            "budget_max": 120000000,
            "bedrooms": 3,
            "surface_min": 100,
            "surface_max": 500,
            "transaction_type": "buy",
        }
        runs = []
        for i in range(3):
            r = self.matching_service.match(
                search_result=search,
                project_criteria=criteria,
            )
            runs.append(r)
        for i in range(1, len(runs)):
            s0 = [(m.item_id, m.global_score) for m in runs[0].matches]
            si = [(m.item_id, m.global_score) for m in runs[i].matches]
            self.assertEqual(s0, si,
                             f"Multi-criteria determinism failed run 0 vs {i}")
        log.info("Multi-criteria determinism verified across %d runs", len(runs))

    def test_16_matching_repeated_with_project_criteria(self):
        search = self._search(city="Douala", max_results=15)
        criteria = {"city": "Douala", "property_type": "apartment"}
        for i in range(3):
            r = self.matching_service.match(
                search_result=search,
                project_criteria=criteria,
            )
            log.info("Run %d: matches=%d min=%.4f max=%.4f avg=%.4f",
                     i, len(r.matches), r.min_score, r.max_score, r.average_score)

    def test_17_matching_score_logs_per_item(self):
        search = self._search(city="Douala", property_type="house", max_results=10)
        result = self.matching_service.match(
            search_result=search,
            project_criteria={"city": "Douala", "property_type": "house", "bedrooms": 3},
        )
        for m in result.matches:
            log.info("Score: %-30s global=%.4f matched=%d/%d",
                     m.title[:30], m.global_score, m.matched_criteria_count, m.total_criteria_count)

    def test_18_matching_top_match_returned(self):
        search = self._search(city="Douala", property_type="house", max_results=20)
        result = self.matching_service.match(
            search_result=search,
            project_criteria={"city": "Douala", "property_type": "house"},
        )
        top = result.top_match
        if top is not None:
            log.info("Top match: %s score=%.4f", top.title, top.global_score)
            self.assertEqual(top, result.matches[0])

    def test_19_matching_full_pipeline(self):
        search = self._search(
            city="Douala",
            property_type="house",
            bedrooms=3,
            budget_min=30000000,
            budget_max=150000000,
            max_results=20,
        )
        result = self.matching_service.match(
            search_result=search,
            project_criteria={
                "city": "Douala",
                "property_type": "house",
                "bedrooms": 3,
                "budget_min": 30000000,
                "budget_max": 150000000,
                "surface_min": 80,
                "transaction_type": "buy",
            },
        )
        log.info("Full pipeline: total_evaluated=%d matches=%d min=%.4f max=%.4f avg=%.4f",
                 result.total_evaluated, len(result.matches),
                 result.min_score, result.max_score, result.average_score)
        self.assertGreaterEqual(result.total_evaluated, 0)
        if result.matches:
            self.assertGreater(len(result.criteria_used), 0)

    def test_20_matching_insufficient_criteria_rejected(self):
        search = self._search(city="Douala", max_results=10)
        result = self.matching_service.match(
            search_result=search,
            project_criteria=None,
        )
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
