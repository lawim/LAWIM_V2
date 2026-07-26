# Violation Engine Details — LCIP A.3

## Fichier créé

`tests/gold_corpus/certification/diagnostics/violation_engine.py`

## Fonctionnalités

- **VIOLATION_EXPLANATIONS** : 31 explications documentées pour toutes les assertions
- `get_violation_detail()` : retourne l'explication et la correction pour une assertion
- `analyze_violation()` : produit analyse complète (assertion_id, category, turn, expected, actual, explication, correction, confidence)
- `analyze_all_violations()` : analyse toutes les violations d'un résultat de certification

## Format d'une violation

```json
{
  "assertion_id": "BIZ-0001",
  "category": "business",
  "turn_number": 2,
  "expected": "...",
  "actual": "...",
  "explanation": "Aucun objet metier n'a ete cree...",
  "expected_correction": "Verifier que l'action metier...",
  "confidence": 0.9
}
```

## Contrôle

VIO-0001 : PASS
