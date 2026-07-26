# Certification Engine Details — LCIP A.2

## Fichier créé

`tests/gold_corpus/specification/engine/certification_engine.py`

## Fonctionnalités

- Chargement de la spécification (turn_spec + expected_*)
- Chargement des résultats réels (conversation.json + actual_*)
- Évaluation des assertions par path résolu
- Évaluation par tour avec assertions individuelles
- Calcul des scores par dimension (8 catégories + global)
- Détermination du verdict (PASS / FAIL / PARTIAL)
- Rapport JSON complet

## Commandes

```bash
python tests/gold_corpus/specification/engine/certification_engine.py \
    tests/gold_corpus/specification/tests/B000001/ \
    tests/gold_corpus/examples/B000001/
```

## Contrôle

ENGINE-0001 : PASS
