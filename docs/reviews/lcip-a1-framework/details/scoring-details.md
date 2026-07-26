# Scoring Details — LCIP A.1

## Moteur de scoring

Fichier : `tests/gold_corpus/benchmark/score.py`

## Catégories et poids

| Catégorie | Poids | Fonction |
|-----------|-------|----------|
| conversation | 0.15 | compute_conversation_score() |
| memory | 0.15 | compute_memory_score() |
| qualification | 0.15 | compute_qualification_score() |
| business | 0.15 | compute_business_score() |
| runtime | 0.15 | compute_runtime_score() |
| language | 0.10 | compute_language_score() |
| channel | 0.05 | compute_channel_score() |
| intent | 0.10 | compute_intent_score() |

## Calcul

Chaque score est un float dans [0.0, 1.0].

Le score global est la moyenne pondérée :

```
global = Σ(weight_i × score_i) / Σ(weight_i)
```

## Seuil

Un score global ≥ 0.50 est requis pour le succès d'une conversation dans le
benchmark.

## Documentation

Le calcul est documenté dans :
- `tests/gold_corpus/README.md` (section Scoring)
- `tests/gold_corpus/benchmark/score.py` (docstrings)

## Contrôle

SCORE-0001 : PASS
