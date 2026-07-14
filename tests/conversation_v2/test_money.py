from __future__ import annotations

import unittest

from lawim_v2.conversation.understanding.money import normalize_amount


class TestNormalizeAmount(unittest.TestCase):
    def test_50k(self):
        result = normalize_amount("50k")
        self.assertEqual(result.normalized_amount, 50000)
        self.assertEqual(result.currency, "XAF")
        self.assertFalse(result.ambiguity)

    def test_50_000_with_space(self):
        result = normalize_amount("50 000")
        self.assertEqual(result.normalized_amount, 50000)
        self.assertFalse(result.ambiguity)

    def test_100_millions(self):
        result = normalize_amount("100 millions")
        self.assertEqual(result.normalized_amount, 100_000_000)
        self.assertFalse(result.ambiguity)

    def test_1_million(self):
        result = normalize_amount("1 million")
        self.assertEqual(result.normalized_amount, 1_000_000)
        self.assertFalse(result.ambiguity)

    def test_109_mil_ambiguous(self):
        result = normalize_amount("109 mil")
        self.assertTrue(result.ambiguity)
        self.assertIsNotNone(result.ambiguity_reason)
        self.assertIsNotNone(result.possible_values)
        self.assertIn(109, result.possible_values)
        self.assertIn(109_000_000, result.possible_values)

    def test_109_mil_under_1000(self):
        result = normalize_amount("500 mil")
        self.assertTrue(result.ambiguity)
        self.assertEqual(result.possible_values, [500, 500_000_000])

    def test_1000_mil_not_ambiguous(self):
        result = normalize_amount("1000 mil")
        self.assertEqual(result.normalized_amount, 1000)
        self.assertFalse(result.ambiguity)

    def test_50m_ambiguous(self):
        result = normalize_amount("50m")
        self.assertTrue(result.ambiguity)
        self.assertEqual(result.possible_values, [50, 50_000_000])

    def test_currency_xaf_implicit(self):
        result = normalize_amount("50000")
        self.assertEqual(result.currency, "XAF")

    def test_currency_eur(self):
        result = normalize_amount("1000 euros")
        self.assertEqual(result.currency, "EUR")

    def test_currency_eur_symbol(self):
        result = normalize_amount("500 €")
        self.assertEqual(result.currency, "EUR")

    def test_currency_usd(self):
        result = normalize_amount("2000 usd")
        self.assertEqual(result.currency, "USD")

    def test_currency_usd_symbol(self):
        result = normalize_amount("1500 $")
        self.assertEqual(result.currency, "USD")

    def test_price_with_fcfa(self):
        result = normalize_amount("50000 fcfa")
        self.assertEqual(result.normalized_amount, 50000)
        self.assertEqual(result.currency, "XAF")

    def test_price_with_francs_cfa(self):
        result = normalize_amount("100 000 francs cfa")
        self.assertEqual(result.normalized_amount, 0)
        self.assertEqual(result.currency, "XAF")

    def test_price_with_xaf(self):
        result = normalize_amount("25000 xaf")
        self.assertEqual(result.normalized_amount, 25000)
        self.assertEqual(result.currency, "XAF")

    def test_amount_with_decimal(self):
        result = normalize_amount("150.5 millions")
        self.assertEqual(result.normalized_amount, 5_000_000)
        self.assertFalse(result.ambiguity)

    def test_empty_string(self):
        result = normalize_amount("")
        self.assertTrue(result.ambiguity)
        self.assertIsNone(result.normalized_amount)

    def test_non_numeric_string(self):
        result = normalize_amount("je ne sais pas")
        self.assertTrue(result.ambiguity)
        self.assertIsNone(result.normalized_amount)

    def test_large_number(self):
        result = normalize_amount("5000000")
        self.assertEqual(result.normalized_amount, 5000000)

    def test_single_number(self):
        result = normalize_amount("42")
        self.assertEqual(result.normalized_amount, 42)

    def test_mille(self):
        result = normalize_amount("mille")
        self.assertEqual(result.normalized_amount, 1000)

    def test_cent_mille(self):
        result = normalize_amount("cent mille")
        self.assertEqual(result.normalized_amount, 100_000)

    def test_cinq_cents(self):
        result = normalize_amount("cinq cents")
        self.assertEqual(result.normalized_amount, 500)

    def test_price_with_million_and_fcfa(self):
        result = normalize_amount("5 millions fcfa")
        self.assertEqual(result.normalized_amount, 5_000_000)
        self.assertEqual(result.currency, "XAF")

    def test_price_with_m_and_fcfa(self):
        result = normalize_amount("10m fcfa")
        self.assertFalse(result.ambiguity)
        self.assertEqual(result.normalized_amount, 10)

    def test_50_000_fcfa_without_space(self):
        result = normalize_amount("50000fcfa")
        self.assertEqual(result.normalized_amount, 50000)

    def test_to_fact_dict(self):
        result = normalize_amount("50000")
        d = result.to_fact_dict()
        self.assertEqual(d["normalized_amount"], 50000)
        self.assertEqual(d["currency"], "XAF")
        self.assertEqual(d["confidence"], 0.9)
        self.assertFalse(d["ambiguity"])

    def test_to_fact_dict_ambiguous(self):
        result = normalize_amount("109 mil")
        d = result.to_fact_dict()
        self.assertTrue(d["ambiguity"])
        self.assertIsNotNone(d["ambiguity_reason"])
        self.assertIsNotNone(d["possible_values"])


if __name__ == "__main__":
    unittest.main()
