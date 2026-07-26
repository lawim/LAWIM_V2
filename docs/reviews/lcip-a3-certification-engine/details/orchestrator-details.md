# Orchestrator Details — LCIP A.3

## Fichier créé

`tests/gold_corpus/certification/engine/orchestrator.py`

## Pipeline de certification

1. **CertificationEngine.certify()** (A.2) → scores + assertions
2. **analyze_all_violations()** → violations détaillées
3. **analyze_root_causes()** → causes racines + composants
4. **_write_outputs()** → 4 formats de sortie

## Sorties

| Fichier | Contenu |
|---------|---------|
| certification.json | Résultat complet (verdict, scores, assertions, violations, root causes) |
| violations.json | Liste des violations avec explications |
| diagnostics.json | Causes racines et résumé par composant |
| summary.md | Résumé lisible en Markdown |

## Usage

```bash
python tests/gold_corpus/certification/engine/orchestrator.py \
    tests/gold_corpus/specification/tests/B000001/ \
    tests/gold_corpus/examples/B000001/ \
    --output-dir tests/gold_corpus/certification/output/
```

## Contrôle

ORCH-0001 : PASS
