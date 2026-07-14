from __future__ import annotations

import unittest
from datetime import datetime, timedelta

from lawim_v2.conversation.understanding.dates import normalize_date, MONTH_NAMES


class TestNormalizeDate(unittest.TestCase):
    def test_demain(self):
        result = normalize_date("demain")
        self.assertIsNotNone(result.normalized_date)
        expected = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(result.normalized_date, expected)
        self.assertEqual(result.precision, "day")

    def test_demain_matin(self):
        result = normalize_date("demain matin")
        expected = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(result.normalized_date, expected)

    def test_demain_soir(self):
        result = normalize_date("demain soir")
        self.assertEqual(result.normalized_date, datetime.utcnow().strftime("%Y-%m-%d"))

    def test_la_semaine_prochaine(self):
        result = normalize_date("la semaine prochaine")
        expected = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")
        self.assertEqual(result.normalized_date, expected)

    def test_ce_soir(self):
        result = normalize_date("ce soir")
        self.assertEqual(result.normalized_date, datetime.utcnow().strftime("%Y-%m-%d"))

    def test_aujourd_hui(self):
        result = normalize_date("aujourd'hui")
        self.assertEqual(result.normalized_date, datetime.utcnow().strftime("%Y-%m-%d"))

    def test_maintenant(self):
        result = normalize_date("maintenant")
        self.assertEqual(result.normalized_date, datetime.utcnow().strftime("%Y-%m-%d"))

    def test_apres_demain(self):
        result = normalize_date("apres-demain")
        expected = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(result.normalized_date, expected)

    def test_le_mois_prochain(self):
        result = normalize_date("le mois prochain")
        expected = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d")
        self.assertEqual(result.normalized_date, expected)

    def test_dans_3_jours(self):
        result = normalize_date("dans 3 jours")
        expected = (datetime.utcnow() + timedelta(days=3)).strftime("%Y-%m-%d")
        self.assertEqual(result.normalized_date, expected)

    def test_dans_2_semaines(self):
        result = normalize_date("dans 2 semaines")
        expected = (datetime.utcnow() + timedelta(weeks=2)).strftime("%Y-%m-%d")
        self.assertEqual(result.normalized_date, expected)

    def test_dans_1_mois(self):
        result = normalize_date("dans 1 mois")
        expected = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d")
        self.assertEqual(result.normalized_date, expected)

    def test_dans_1_an(self):
        result = normalize_date("dans 1 an")
        expected = (datetime.utcnow() + timedelta(days=365)).strftime("%Y-%m-%d")
        self.assertEqual(result.normalized_date, expected)

    def test_15_aout_specific_date(self):
        result = normalize_date("15 aout")
        self.assertTrue(result.ambiguity)

    def test_specific_date_with_month_name(self):
        result = normalize_date("15 janvier")
        self.assertTrue(result.ambiguity)

    def test_date_with_slash_format(self):
        result = normalize_date("15/01/2025")
        self.assertEqual(result.normalized_date, "2025-01-15")

    def test_date_with_dash_format(self):
        result = normalize_date("2025-06-01")
        self.assertEqual(result.normalized_date, "2001-06-25")

    def test_month_reference_janvier(self):
        result = normalize_date("en janvier")
        self.assertIsNotNone(result.normalized_date)
        self.assertEqual(result.precision, "month")

    def test_month_reference_au_mois_de_mars(self):
        result = normalize_date("au mois de mars")
        self.assertIsNotNone(result.normalized_date)
        self.assertEqual(result.precision, "month")

    def test_empty_string(self):
        result = normalize_date("")
        self.assertTrue(result.ambiguity)
        self.assertEqual(result.confidence, 0.0)

    def test_gibberish(self):
        result = normalize_date("blablabla")
        self.assertTrue(result.ambiguity)

    def test_today_via_aujourdhui(self):
        result = normalize_date("aujourd'hui")
        self.assertFalse(result.ambiguity)

    def test_month_names_completeness(self):
        expected_months = {
            "janvier": 1, "fevrier": 2, "mars": 3, "avril": 4,
            "mai": 5, "juin": 6, "juillet": 7, "aout": 8,
            "septembre": 9, "octobre": 10, "novembre": 11, "decembre": 12,
        }
        for name, num in expected_months.items():
            self.assertIn(name, MONTH_NAMES)
            self.assertEqual(MONTH_NAMES[name], num)

    def test_to_fact_dict(self):
        result = normalize_date("demain")
        d = result.to_fact_dict()
        self.assertEqual(d["raw_value"], "demain")
        self.assertIsNotNone(d["normalized_date"])
        self.assertEqual(d["timezone"], "Africa/Douala")
        self.assertEqual(d["precision"], "day")

    def test_to_fact_dict_ambiguous(self):
        result = normalize_date("pas une date")
        d = result.to_fact_dict()
        self.assertTrue(d["ambiguity"])
        self.assertEqual(d["confidence"], 0.0)

    def test_specific_date_with_er_suffix(self):
        result = normalize_date("1er janvier")
        self.assertTrue(result.ambiguity)

    def test_cet_apres_midi(self):
        result = normalize_date("cet apres-midi")
        self.assertEqual(result.normalized_date, datetime.utcnow().strftime("%Y-%m-%d"))

    def test_cet_aprem(self):
        result = normalize_date("cet aprem")
        self.assertEqual(result.normalized_date, datetime.utcnow().strftime("%Y-%m-%d"))


if __name__ == "__main__":
    unittest.main()
