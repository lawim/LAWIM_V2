# Classification Details — Audit B.1R

## Classification B.1 (à rejeter)

| Catégorie | Nombre | Statut réel |
|-----------|:------:|-------------|
| GOLD CERTIFIED | 990 | INVALIDE — pas de runtime |
| REPAIRABLE | 0 | — |
| REJECTED | 0 | — |
| ERRORS | 0 | — |

## Classification réelle

| Statut | Nombre | Justification |
|--------|:------:|---------------|
| STATIC_SCHEMA_VALID | 990 | Les fichiers respectent les schémas JSON |
| RUNTIME_GOLD_CERTIFIED | 0 | Aucune exécution runtime |
| GOLD_REPAIRABLE | 0 | Pas de test runtime |
| SCENARIO_TEMPLATE | 0 | Aucun placeholder trouvé |
| DUPLICATE | 0 | Pas de doublon |
| INVALID_SCHEMA | 0 | Tous les schémas sont valides |
| RUNTIME_FAIL | 0 | Pas de test runtime |
| NOT_EXECUTED | 990 | Aucune conversation testée contre le runtime |

## Conclusion

```
RUNTIME_GOLD_CERTIFIED : 0
STATIC_SCHEMA_VALID    : 990
NOT_EXECUTED           : 990
```

Aucune conversation n'est réellement certifiée GOLD.

## Contrôle

CLASS-0001 : FAIL (GOLD attribué sans certification runtime)
