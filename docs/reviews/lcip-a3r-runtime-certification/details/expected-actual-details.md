# Expected/Actual Details — A.3R

## Séparation stricte

- **ExpectedSpecLoader** charge depuis les fichiers du corpus (expected_*.json)
- **RuntimeExecutor** exécute contre le runtime réel (ProgramFEngineAdapter)
- Aucune fonction commune ne retourne les deux

## Vérification de tautologie

La fonction `check_tautology()` dans runtime_comparator.py vérifie :
1. `actual_run.call_count > 0` — le runtime a-t-il été appelé ?
2. Les sources expected/actual sont-elles différentes ?

Si `call_count == 0` → `CERTIFICATION_TAUTOLOGY_DETECTED`

## Test

`test_tautology_detected_if_no_runtime` : PASS

## Contrôle

EA-0001 : PASS
TAUT-0001 : PASS
