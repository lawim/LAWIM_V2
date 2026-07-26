# Architecture Details — A.3R

## Pipeline

```
ExpectedSpecLoader (tests/gold_corpus/certification/runtime/expected_loader.py)
  → expected (depuis expected_*.json)

RuntimeExecutor (tests/gold_corpus/certification/runtime/executor.py)
  → actual (via ProgramFEngineAdapter + ConversationJourneyOrchestrator réels)

RuntimeComparator (tests/gold_corpus/certification/engine/runtime_comparator.py)
  → différences, violations, score

A3ROrchestrator (tests/gold_corpus/certification/engine/a3r_orchestrator.py)
  → certification.json, violations.json, runtime-trace.json, summary.md
```

## Fichiers créés

| Fichier | Rôle |
|---------|------|
| certification/runtime/models.py | ActualConversationRun, ActualTurn |
| certification/runtime/executor.py | RuntimeExecutor |
| certification/runtime/expected_loader.py | ExpectedSpecLoader |
| certification/engine/runtime_comparator.py | AssertionOperator, RuntimeComparator, check_tautology |
| certification/engine/a3r_orchestrator.py | A3ROrchestrator |
| certification/tests/test_a3r_engine.py | 25 tests |

## Contrôle

ARC-0001 : PASS
