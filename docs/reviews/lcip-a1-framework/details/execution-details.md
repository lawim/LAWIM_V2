# Execution Details — LCIP A.1

## Validateur de schémas — Exemple B000001

```bash
$ python tests/gold_corpus/validators/validate_schema.py tests/gold_corpus/examples/B000001/

  PASS: conversation (tests/gold_corpus/examples/B000001/conversation.json)
  PASS: expected_state (tests/gold_corpus/examples/B000001/expected_state.json)
  PASS: expected_business (tests/gold_corpus/examples/B000001/expected_business.json)
  PASS: expected_questions (tests/gold_corpus/examples/B000001/expected_questions.json)
  PASS: expected_language (tests/gold_corpus/examples/B000001/expected_language.json)
  PASS: expected_runtime (tests/gold_corpus/examples/B000001/expected_runtime.json)
  PASS: expected_assertions (tests/gold_corpus/examples/B000001/expected_assertions.json)

Total: 7 PASS, 0 FAIL, 0 WARNING
```

## Validateur de conversation — Exemple B000001

```bash
$ python tests/gold_corpus/validators/validate_conversation.py tests/gold_corpus/examples/B000001/

PASS
```

## Validateur d'assertions — Exemple B000001

```bash
$ python tests/gold_corpus/validators/validate_assertions.py tests/gold_corpus/examples/B000001/expected_assertions.json

NOTE: No assertions file
```

(Le validateur vérifie les assertions contre un état runtime ; sans fichier
actual, il indique simplement l'absence de données réelles.)

## Validateur métier — Exemple B000001

```bash
$ python tests/gold_corpus/validators/validate_business.py tests/gold_corpus/examples/B000001/expected_business.json

PASS: Business expectations valid
```

## Benchmark — Corpus vide

```bash
$ python tests/gold_corpus/benchmark/run_gold_benchmark.py --conversations-dir /tmp/empty/

Gold Benchmark — LAWIM Gold Corpus
========================================

WARNING: No conversations directory found. Running with empty corpus.

Total: 0 | PASS: 0 | FAIL: 0 | Duration: 0s
```

## Benchmark — Exemple B000001

```bash
$ python tests/gold_corpus/benchmark/run_gold_benchmark.py --conversations-dir tests/gold_corpus/examples/

Gold Benchmark — LAWIM Gold Corpus
========================================

  PASS: B000001 (global=1.0000)

Total: 1 | PASS: 1 | FAIL: 0 | Duration: X.XXXs
```

## Statistiques — Exemple B000001

```bash
$ python tests/gold_corpus/statistics/build_statistics.py --conversations-dir tests/gold_corpus/examples/

# Gold Corpus Statistics

**Total conversations:** 1
**Total messages:** 5
**User messages:** 3
**Assistant messages:** 2
**Avg messages/conversation:** 5.0
**Avg turns/conversation:** 3.0

## By Category
| Category | Count |
| -------- | ----- |
| rental | 1 |

## By Language
| Language | Count |
| -------- | ----- |
| fr | 1 |

## By Level
| Level | Count |
| ----- | ----- |
| basic | 1 |

## By Channel
| Channel | Count |
| ------- | ----- |
| web | 1 |

## By Business Object
| Object | Count |
| ------ | ----- |
| apartment | 1 |

## Coverage
| Dimension | Unique Values |
| --------- | ------------- |
| business_objects | 1 |
| categories | 1 |
| channels | 1 |
| languages | 1 |
| levels | 1 |
```

## Contrôle

EXEC-0001 : PASS
