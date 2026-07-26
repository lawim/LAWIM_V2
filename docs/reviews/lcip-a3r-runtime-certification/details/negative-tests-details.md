# Negative Tests Details — A.3R

## Cas testés

| Test | Défaut | Résultat |
|------|--------|:--------:|
| NEG-0001 | Budget erroné (999999) | PASS |
| NEG-0002 | Zone perdue (district absent) | PASS |
| NEG-0003 | Action métier NONE vs search | PASS |
| NEG-0005 | Langue en vs fr | PASS |
| NEG-0007 | Qualification complète sans critères | PASS |

## Résultat

```
NEGATIVE_TESTS=5
NEGATIVE_TESTS_DETECTED=5
FALSE_NEGATIVES=0
```

Chaque test vérifie `assertions_failed > 0` après exécution runtime.

## Contrôle

NEG-0001 : PASS (5/5 négatifs détectés)
