# Test Details — LCIP A.3

## Test sur B000001 (exemple A.1/A.2)

```bash
python tests/gold_corpus/certification/engine/orchestrator.py \
    tests/gold_corpus/specification/tests/B000001/ \
    tests/gold_corpus/examples/B000001/ \
    --output-dir tests/gold_corpus/certification/output/
```

## Résultat

- **Verdict:** FAIL (attendu — BIZ-0001 échoue car l'exemple ne va pas jusqu'à la recherche)
- **Scores:** global 0.8125
- **1 violation** correctement identifiée :
  - BIZ-0001 : "Aucun objet metier n'a ete cree"
  - Tour 2, category business
  - Composant : ConversationJourneyOrchestrator (confiance 0.85)
  - Correction documentée
- **12 assertions** PASS
- **4 formats** de sortie générés

## Contrôle

TEST-0001 : PASS
