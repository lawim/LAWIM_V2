# Benchmark Details — LCIP A.1

## Scripts créés

### run_gold_benchmark.py

Orchestrateur du benchmark.

- Découvre automatiquement toutes les conversations dans `conversations/`
- Pour chaque conversation : valide les schémas, calcule les scores
- Produit : `reports/benchmark_results.json` et `reports/benchmark_report.md`
- Fonctionne même avec un corpus vide (avertissement, pas d'erreur)

### score.py

Moteur de scoring à 8 dimensions.

Scores :
- Conversation Score (conformité schémas)
- Memory Score (rétention des slots)
- Qualification Score (statut correct)
- Business Score (action métier correcte)
- Runtime Score (moteur et services)
- Language Score (langue et identité)
- Channel Score (canal correct)
- Intent Score (intention correcte)

Poids documentés dans le README.md. Score global = moyenne pondérée.
Seuil de succès : global ≥ 0.50

### report.py

Générateur de rapport formaté en Markdown.

- Tableau récapitulatif (total, PASS, FAIL, score moyen)
- Tableau détaillé par conversation (tous les scores)
- Poids du scoring

## Comportement corpus vide

Le benchmark fonctionne avec un corpus vide :

```bash
python tests/gold_corpus/benchmark/run_gold_benchmark.py --conversations-dir /tmp/empty/
```

Résultat : warning + rapport vide, pas d'erreur.

## Contrôle

BENCH-0001 : PASS
