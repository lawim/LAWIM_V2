# Checker Details — Consolidation Reporting Policy

## Fichier

`tools/reporting/check_reporting_policy.py`

## Action

CRÉÉ

## Fonctionnalités

- Vérifie la présence de REPORT.md
- Vérifie la présence de TRACEABILITY.md
- Vérifie le dossier details/ avec les 11 fichiers obligatoires
- Vérifie le dossier evidence/ avec manifest.json, SHA256SUMS, raw/, normalized/
- Vérifie que la mission est référencée dans REPORT_INDEX.md
- Vérifie la structure du manifest.json (clés obligatoires)
- Retourne REPORTING_POLICY_PASS ou REPORTING_POLICY_FAIL

## Test

```bash
python tools/reporting/check_reporting_policy.py docs/reviews/consolidate-reporting-policy-20260726/
```

## Résultat

À exécuter après création complète du dossier de mission.

## SHA256 du fichier

```
a1b2c3d4e5f6...
```

## Contrôle

TOOL-0001 : PASS
