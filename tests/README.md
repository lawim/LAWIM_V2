# Tests

Suite `unittest` pour LAWIM_V2 (64 tests au 2026-06-29).

## Lancer les tests

```bash
./scripts/run-tests.sh
```

Le script exécute :

- vérification syntaxe `app.js` (si Node.js est disponible)
- `python3 -m unittest discover -s tests -v`
- `scripts/validate_prisma_manifest.py`
- `scripts/smoke_runtime.py`

## Structure

| Fichier | Rôle |
|---------|------|
| `lawim_harness.py` | Harness partagé (`DummyHandler`, `LawimTestHarness`, fixtures média) |
| `test_lawim_v2.py` | Baseline exécutable, persistence, RBAC, mutations |
| `test_user_journeys.py` | Parcours utilisateur bout-en-bout |
| `test_product_depth.py` | Profondeur produit (matching, conversations, médias) |
| `test_mvp_stabilization.py` | Stabilisation MVP (health, pagination, erreurs) |
| `test_beta_candidate.py` | Critères beta (sécurité, validation, redaction) |
| `test_release_candidate.py` | Durcissement release candidate |
| `test_runtime_smoke.py` | Smoke runtime et validation config |

## Configuration de test

Les tests utilisent `AppConfig.for_test()` avec une base SQLite temporaire et des données demo seedées.
