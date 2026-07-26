# Test Results Details — A.3R-C

## Commande

```bash
python3 -m pytest tests/gold_corpus/certification/tests -q --tb=short \
  --junitxml=docs/reviews/lcip-a3r-completion/evidence/raw/tests/a3r-completion-junit.xml
```

## Résultat

```
38 passed in 0.81s
```

## Détail

| Suite | Tests | PASS |
|-------|:-----:|:----:|
| TestAssertionOperators | 12 | 12 |
| TestExpectedActualSeparation | 2 | 2 |
| TestNegativeCases | 5 | 5 |
| TestPositiveCases | 7 | 7 |
| TestNegativeCasesExtended | 2 | 2 |
| TestTautology | 1 | 1 |
| TestTautologyExtended | 5 | 5 |
| TestCategoryLanguageDefaults | 4 | 4 |
| TestRepositoryIsolation | 1 | 1 |
| **Total** | **38** | **38** |

## Fichiers

- JUnit XML : `evidence/raw/tests/a3r-completion-junit.xml`
- Tests source : `tests/gold_corpus/certification/tests/test_a3r_engine.py`

**Contrôle :** TEST-0001 : PASS
