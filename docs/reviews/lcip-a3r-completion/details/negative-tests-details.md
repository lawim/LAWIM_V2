# Negative Tests Details — A.3R-C

## 7 tests négatifs obligatoires

| ID | Défaut | Fichier test | Runtime appelé | Résultat |
|----|--------|-------------|:--------------:|:--------:|
| NEG-001 | Budget erroné (999999) | test_budget_erronne | OUI | PASS |
| NEG-002 | Zone perdue (district absent) | test_zone_perdue | OUI | PASS |
| NEG-003 | Action métier NONE vs search | test_action_manquante | OUI | PASS |
| NEG-004 | Double création métier | test_double_creation_metier | OUI | PASS |
| NEG-005 | Mauvaise langue (en vs fr) | test_mauvaise_langue | OUI | PASS |
| NEG-006 | pending_user_action incorrect | test_pending_user_action_incorrect | OUI | PASS |
| NEG-007 | Confirmation prématurée | test_confirmation_prematuree | OUI | PASS |

## Résultat

```
NEGATIVE_TESTS=7
NEGATIVE_TESTS_DETECTED=7
NEGATIVE_FALSE_NEGATIVES=0
```

Chaque test vérifie `assertions_failed > 0` et chaque échec est produit par
le RuntimeComparator après exécution réelle via ProgramFEngineAdapter.

**Contrôle :** NEG-0001 : PASS
