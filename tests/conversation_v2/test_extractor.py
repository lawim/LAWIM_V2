from __future__ import annotations

import unittest

from lawim_v2.conversation.understanding.extractor import extract_all


class TestExtractor(unittest.TestCase):
    def test_extract_property_location_budget_bedrooms(self):
        text = "Je cherche un appartement 3 chambres à Douala pour 50 millions"
        result = extract_all(text)
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("property_type", fields)
        self.assertIn("city", fields)
        self.assertIn("budget_max", fields)
        self.assertIn("bedroom_count", fields)

    def test_extract_appartement_type(self):
        result = extract_all("Je cherche un appartement")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("property_type", fields)

    def test_extract_maison_type(self):
        result = extract_all("maison a vendre")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("property_type", fields)

    def test_extract_transaction_type_acheter(self):
        result = extract_all("Je veux acheter")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("transaction_type", fields)

    def test_extract_transaction_type_louer(self):
        result = extract_all("Je veux louer")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("transaction_type", fields)

    def test_extract_city_douala(self):
        result = extract_all("Je cherche à Douala")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("city", fields)

    def test_extract_budget_with_acheter(self):
        result = extract_all("Je veux acheter pour 50 millions")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("budget_max", fields)
        budget_facts = [f for f in result["facts"] if f["field"] == "budget_max"]
        self.assertEqual(budget_facts[0]["normalized_value"], 50_000_000)

    def test_extract_budget_with_louer(self):
        result = extract_all("Je veux louer pour 50000")
        ambiguous_fields = {f["field"] for f in result["ambiguous"]}
        self.assertIn("budget", ambiguous_fields)

    def test_extract_neighborhood_implies_city(self):
        result = extract_all("Makepe")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("neighborhood", fields)
        self.assertIn("city", fields)

    def test_extract_bedroom_count(self):
        result = extract_all("3 chambres")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("bedroom_count", fields)
        bedroom = [f for f in result["facts"] if f["field"] == "bedroom_count"][0]
        self.assertEqual(bedroom["normalized_value"], 3)

    def test_extract_bedroom_count_t3(self):
        result = extract_all("T3")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("bedroom_count", fields)

    def test_extract_bathroom_count(self):
        result = extract_all("2 sdb")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("bathroom_count", fields)

    def test_extract_surface(self):
        result = extract_all("100 m2")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("surface_sqm", fields)

    def test_extract_surface_superficie(self):
        result = extract_all("superficie 200")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("surface_sqm", fields)

    def test_extract_date_deadline(self):
        result = extract_all("je cherche pour dans 1 mois")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("deadline", fields)

    def test_empty_text(self):
        result = extract_all("")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("property_type", fields)
        self.assertEqual(len(result["ambiguous"]), 2)

    def test_greeting_only(self):
        result = extract_all("Bonjour")
        self.assertEqual(len(result["facts"]), 0)

    def test_multiple_locations(self):
        result = extract_all("Makepe et Douala")
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("city", fields)

    def test_full_message_all_entities(self):
        text = "Je cherche un appartement 3 pièces à Douala Makepe pour 50 millions avec 100m2"
        result = extract_all(text)
        fields = {f["field"] for f in result["facts"]}
        self.assertIn("property_type", fields)
        self.assertIn("city", fields)
        self.assertIn("neighborhood", fields)
        self.assertIn("budget_max", fields)
        self.assertIn("bedroom_count", fields)
        self.assertIn("surface_sqm", fields)

    def test_ambiguous_budget_detected(self):
        result = extract_all("109 mil")
        ambiguous_fields = {f["field"] for f in result["ambiguous"]}
        self.assertIn("budget", ambiguous_fields)

    def test_no_false_positives(self):
        result = extract_all("Bonjour je voudrais de l'information")
        self.assertEqual(len(result["facts"]), 0)


if __name__ == "__main__":
    unittest.main()
