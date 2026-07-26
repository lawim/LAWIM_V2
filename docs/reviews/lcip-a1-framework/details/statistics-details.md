# Statistics Details — LCIP A.1

## Script créé

Fichier : `tests/gold_corpus/statistics/build_statistics.py`

## Fonctionnalités

- Parcourt automatiquement toutes les conversations
- Calcule les distributions par :
  - Catégorie
  - Langue
  - Niveau
  - Canal
  - Objet métier
- Calcule les statistiques globales :
  - Nombre total de conversations
  - Nombre total de messages (user, assistant)
  - Moyenne messages/conversation
  - Moyenne tours/conversation
- Calcule la couverture (valeurs uniques par dimension)

## Sortie

- Sortie terminale formatée en Markdown
- Export JSON optionnel via `--output`

## Test

```bash
python tests/gold_corpus/statistics/build_statistics.py --conversations-dir tests/gold_corpus/examples/
```

Résultats : voir details/execution-details.md

## Contrôle

STAT-0001 : PASS
