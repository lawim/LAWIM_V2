from __future__ import annotations

import json
from http import HTTPStatus
from unittest import TestCase

from lawim_harness import LawimTestHarness
from lawim_v2.errors import ValidationError
from lawim_v2.geo_domain import build_geo_dto, normalize_city, normalize_region, validate_coordinates
from lawim_v2.geo_reference import (
    load_geo_reference_catalog,
    reference_city_coordinates,
    resolve_reference_location,
    search_reference_locations,
)
from lawim_v2.geocoding_provider import LocalGeocodingProvider
from lawim_v2.matching import haversine_km


class GeoReferenceCatalogTest(TestCase):
    def test_catalog_is_curated_and_secret_free(self) -> None:
        catalog = load_geo_reference_catalog()
        serialized = json.dumps(catalog, ensure_ascii=False).lower()
        self.assertEqual(catalog["country"], "Cameroon")
        self.assertGreaterEqual(len(catalog["cities"]), 5)
        self.assertGreaterEqual(len(catalog["neighborhoods"]), 5)
        for forbidden in ("secret", "password", "token", "api_key"):
            self.assertNotIn(forbidden, serialized)

    def test_alias_normalization_and_region_inference(self) -> None:
        self.assertEqual(normalize_city("  DLA "), "Douala")
        self.assertEqual(normalize_city("yde"), "Yaounde")
        self.assertEqual(normalize_region(None, city="dla"), "Littoral")
        self.assertEqual(normalize_region(None, city="YDE"), "Centre")

        dto = build_geo_dto(city="  yde ", country=" cameroun ", address_line="  bastos ")
        self.assertEqual(dto["city"], "Yaounde")
        self.assertEqual(dto["country"], "Cameroon")
        self.assertEqual(dto["region"], "Centre")

    def test_reference_search_and_resolution(self) -> None:
        bastos_hits = search_reference_locations(query="Bastos", limit=5)
        self.assertGreaterEqual(len(bastos_hits), 1)
        self.assertEqual(bastos_hits[0]["name"], "Bastos")

        douala_hits = search_reference_locations(query="Douala", limit=20)
        self.assertTrue(any(item["name"] == "Akwa" for item in douala_hits))

        resolved = resolve_reference_location(city="DLA", address_line="Akwa")
        self.assertIsNotNone(resolved)
        assert resolved is not None
        self.assertEqual(resolved["city"], "Douala")
        self.assertEqual(resolved["name"], "Akwa")

    def test_coordinates_validation_and_distance(self) -> None:
        with self.assertRaises(ValidationError):
            validate_coordinates(91.0, 0.0)
        with self.assertRaises(ValidationError):
            validate_coordinates(4.0, None)

        self.assertEqual(reference_city_coordinates("DLA"), (4.05, 9.7))
        self.assertAlmostEqual(haversine_km(4.05, 9.7, 4.05, 9.7), 0.0, places=6)
        self.assertGreater(haversine_km(4.05, 9.7, 3.867, 11.516), 100.0)

    def test_local_geocoder_prefers_reference_anchor(self) -> None:
        provider = LocalGeocodingProvider()
        first = provider.geocode(city="DLA", country="Cameroon", address_line="Akwa")
        second = provider.geocode(city="Douala", country="Cameroon", address_line="Akwa")

        self.assertEqual(first, second)
        self.assertEqual(first["provider"], "local")
        self.assertEqual(first["location"]["city"], "Douala")
        self.assertEqual(first["location"]["region"], "Littoral")
        self.assertEqual(first["reference"]["name"], "Akwa")
        self.assertEqual(first["reference"]["city"], "Douala")


class GeoReferenceApiTest(LawimTestHarness):
    def test_geo_search_exposes_curated_locations(self) -> None:
        response = self.invoke("/api/geo/search?q=Bastos")
        self.assertEqual(response.status, HTTPStatus.OK)
        locations = response.body_json()["locations"]
        self.assertTrue(any(item.get("name") == "Bastos" for item in locations))
        self.assertTrue(any(item.get("kind") == "neighborhood" for item in locations))

        douala = self.invoke("/api/geo/search?q=Douala")
        self.assertEqual(douala.status, HTTPStatus.OK)
        douala_locations = douala.body_json()["locations"]
        names = {item.get("name") for item in douala_locations}
        self.assertIn("Douala", names)
        self.assertTrue({"Akwa", "Bonanjo"}.intersection(names))
