from __future__ import annotations

import unittest

from lawim_v2.conversation.understanding.geography import (
    KNOWN_NEIGHBORHOODS,
    KNOWN_CITIES,
    NEIGHBORHOOD_TO_CITY,
    CITY_TO_REGION,
    normalize_location,
    GeoResult,
)


class TestKnownData(unittest.TestCase):
    def test_known_cities_contains_douala(self):
        self.assertIn("douala", KNOWN_CITIES)
        self.assertEqual(KNOWN_CITIES["douala"], "Douala")

    def test_known_cities_contains_yaounde(self):
        self.assertIn("yaounde", KNOWN_CITIES)
        self.assertEqual(KNOWN_CITIES["yaounde"], "Yaoundé")

    def test_known_neighborhoods_contains_makepe(self):
        self.assertIn("makepe", KNOWN_NEIGHBORHOODS)
        self.assertEqual(KNOWN_NEIGHBORHOODS["makepe"], "Makepe")

    def test_neighborhood_to_city_makepe_to_douala(self):
        self.assertEqual(NEIGHBORHOOD_TO_CITY["makepe"], "Douala")

    def test_neighborhood_to_city_odza_to_yaounde(self):
        self.assertEqual(NEIGHBORHOOD_TO_CITY["odza"], "Yaoundé")

    def test_city_to_region_douala(self):
        self.assertEqual(CITY_TO_REGION["Douala"], "Littoral")

    def test_city_to_region_yaounde(self):
        self.assertEqual(CITY_TO_REGION["Yaoundé"], "Centre")


class TestNormalizeLocation(unittest.TestCase):
    def test_normalize_douala_city(self):
        result = normalize_location("Douala")
        self.assertEqual(result.normalized_value, "Douala")
        self.assertEqual(result.match_type, "city")
        self.assertEqual(result.city, "Douala")
        self.assertEqual(result.region, "Littoral")
        self.assertEqual(result.confidence, 1.0)
        self.assertFalse(result.ambiguity)

    def test_normalize_yaounde_city(self):
        result = normalize_location("yaounde")
        self.assertEqual(result.normalized_value, "Yaoundé")
        self.assertEqual(result.match_type, "city")
        self.assertEqual(result.city, "Yaoundé")
        self.assertEqual(result.region, "Centre")

    def test_normalize_lowercase_city(self):
        result = normalize_location("douala")
        self.assertEqual(result.normalized_value, "Douala")
        self.assertEqual(result.match_type, "city")

    def test_normalize_neighborhood(self):
        result = normalize_location("Makepe")
        self.assertEqual(result.normalized_value, "Makepe")
        self.assertEqual(result.match_type, "neighborhood")
        self.assertEqual(result.city, "Douala")
        self.assertEqual(result.region, "Littoral")
        self.assertEqual(result.confidence, 0.9)

    def test_normalize_neighborhood_bonamoussadi(self):
        result = normalize_location("bonamoussadi")
        self.assertEqual(result.normalized_value, "Bonamoussadi")
        self.assertEqual(result.match_type, "neighborhood")
        self.assertEqual(result.city, "Douala")

    def test_normalize_neighborhood_odza(self):
        result = normalize_location("Odza")
        self.assertEqual(result.normalized_value, "Odza")
        self.assertEqual(result.match_type, "neighborhood")
        self.assertEqual(result.city, "Yaoundé")
        self.assertEqual(result.region, "Centre")

    def test_normalize_unknown_location(self):
        result = normalize_location("Paris")
        self.assertEqual(result.match_type, "unknown")
        self.assertEqual(result.confidence, 0.0)
        self.assertTrue(result.ambiguity)
        self.assertIsNone(result.normalized_value)

    def test_normalize_empty_string(self):
        result = normalize_location("")
        self.assertEqual(result.match_type, "unknown")
        self.assertTrue(result.ambiguity)

    def test_normalize_strips_whitespace(self):
        result = normalize_location("  Douala  ")
        self.assertEqual(result.normalized_value, "Douala")
        self.assertEqual(result.match_type, "city")

    def test_foreign_location(self):
        result = normalize_location("New York")
        self.assertEqual(result.match_type, "unknown")
        self.assertTrue(result.ambiguity)
        self.assertFalse(result.is_foreign)

    def test_garoua_city(self):
        result = normalize_location("Garoua")
        self.assertEqual(result.normalized_value, "Garoua")
        self.assertEqual(result.match_type, "city")
        self.assertEqual(result.region, "Nord")

    def test_to_fact_dict_structure(self):
        result = normalize_location("Douala")
        d = result.to_fact_dict()
        self.assertEqual(d["normalized_value"], "Douala")
        self.assertEqual(d["match_type"], "city")
        self.assertEqual(d["city"], "Douala")
        self.assertEqual(d["region"], "Littoral")
        self.assertEqual(d["country"], "Cameroun")
        self.assertEqual(d["confidence"], 1.0)
        self.assertFalse(d["is_foreign"])

    def test_to_fact_dict_unknown(self):
        result = normalize_location("Mars")
        d = result.to_fact_dict()
        self.assertIsNone(d["normalized_value"])
        self.assertEqual(d["match_type"], "unknown")
        self.assertEqual(d["country"], "Cameroun")

    def test_bafoussam_city(self):
        result = normalize_location("Bafoussam")
        self.assertEqual(result.normalized_value, "Bafoussam")
        self.assertEqual(result.region, "Ouest")

    def test_bamenda_city(self):
        result = normalize_location("Bamenda")
        self.assertEqual(result.normalized_value, "Bamenda")
        self.assertEqual(result.region, "Nord-Ouest")

    def test_limbe_city(self):
        result = normalize_location("Limbe")
        self.assertEqual(result.normalized_value, "Limbe")
        self.assertEqual(result.region, "Sud-Ouest")

    def test_kribi_city(self):
        result = normalize_location("Kribi")
        self.assertEqual(result.normalized_value, "Kribi")
        self.assertEqual(result.match_type, "city")

    def test_new_bell_neighborhood(self):
        result = normalize_location("new bell")
        self.assertEqual(result.normalized_value, "New Bell")
        self.assertEqual(result.match_type, "neighborhood")
        self.assertEqual(result.city, "Douala")


class TestNormalizeLocationEdgeCases(unittest.TestCase):
    def test_location_case_insensitive(self):
        r1 = normalize_location("DOUALA")
        r2 = normalize_location("douala")
        self.assertEqual(r1.normalized_value, r2.normalized_value)

    def test_known_cities_list_douala(self):
        self.assertIn("douala", KNOWN_CITIES)

    def test_city_to_region_nkongsamba(self):
        self.assertEqual(CITY_TO_REGION.get("Nkongsamba"), "Littoral")

    def test_all_neighborhoods_have_city_mapping(self):
        for hood in KNOWN_NEIGHBORHOODS:
            self.assertIn(hood, NEIGHBORHOOD_TO_CITY, f"{hood} missing from NEIGHBORHOOD_TO_CITY")

    def test_geo_result_defaults(self):
        r = GeoResult(raw_value="test")
        self.assertEqual(r.country, "Cameroun")
        self.assertFalse(r.is_foreign)
        self.assertFalse(r.ambiguity)
        self.assertEqual(r.confidence, 0.0)


if __name__ == "__main__":
    unittest.main()
