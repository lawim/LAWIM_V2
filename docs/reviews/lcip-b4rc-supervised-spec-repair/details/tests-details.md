# Tests Details — LCIP B.4R-C

## Test Suites

### Suite 1: Derivation Rule Tests (40 tests)

| Métrique | Valeur |
|----------|-------:|
| Total tests | 40 |
| PASS | 40 |
| FAIL | 0 |
| Durée | 0.17s |
| Commande | `python3 -m pytest tests/gold_corpus/specification/tests/test_expected_derivation_rules.py -q -ra` |

### Suite 2: Full Test Suite (104 tests)

| Métrique | Valeur |
|----------|-------:|
| Total tests | 104 |
| PASS | 104 |
| FAIL | 0 |
| Durée | 0.95s |
| Commande | `python3 -m pytest tests/gold_corpus/certification/tests/ tests/gold_corpus/specification/tests/ -q -ra` |

### JUnit Outputs

- Suite 1: `evidence/raw/tests/b4rc-tests.xml`
- Suite 2: `evidence/raw/tests/b4rc-tests-full.xml`

## Evidence

- JUnit XML: evidence/raw/tests/
- Normalized: evidence/normalized/
