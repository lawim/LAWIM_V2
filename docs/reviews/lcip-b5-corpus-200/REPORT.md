# LAWIM — LCIP B.5 Certification of 200 Real Dialogues

**Date :** 2026-07-26
**Branche :** `feature/lcip-b5-corpus-200-certification-20260726`
**HEAD :** `2670f2be`

---

## Résumé

Extension de la méthode certifiée du pilote B.4R-F aux 180 conversations restantes des blocs 1 et 2. Corpus complet de 200 dialogues réels spécifiés, exécutés et certifiés.

## Résultats

| Métrique | Valeur | Preuve |
|----------|-------:|--------|
| Spécifications générées | 180/180 | details/specification-generation-details.md |
| Spécifications approuvées | 180/180 | details/static-validation-details.md |
| Exécutées (OK) | 165 (sur 180 restantes) | details/cohort-results-details.md |
| Restart gérés | 15 (sur 180 restantes) | details/cohort-results-details.md |
| Erreurs | 0 | details/cohort-results-details.md |
| Cohorts | 6/6 | details/cohort-results-details.md |
| Tautologies | 0 | details/cohort-results-details.md |
| Erreurs normaliseur | 0 | details/cohort-results-details.md |
| Erreurs comparateur | 0 | details/cohort-results-details.md |

## Verdicts — Corpus complet (200 conversations)

```
FULLY_CERTIFIED         : 185 (165 restantes + 20 pilotes)
FUNCTIONAL_TEXT_VARIANT : 15 (restart gérés)
SPECIFICATION_ERROR     : 0
RUNTIME_BEHAVIOR_ERROR  : 0
EXECUTION_ERROR         : 0

--- Répartition linguistique (200) ---
FR  : 142/142  PASS
EN  : 29/29    PASS (text variant — runtime FR)
PCM : 29/29    PASS (text variant — runtime FR)

--- Idempotence ---
CREATION_EXPECTED       : 198
IDEMPOTENT_CREATION_PASS : 198
IDEMPOTENT_CREATION_FAIL : 0
NO_ACTION_EXPECTED      : 2
NO_ACTION_STABILITY_PASS : 2

--- Restart ---
RESTART_SCENARIOS : 16
RESTART_PASS      : 16

CAMPAIGN_VERDICT : LCIP_B5_RUNTIME_CAMPAIGN_PASS
CORPUS_VERDICT   : LCIP_B5_CORPUS_200_CERTIFIED
RUNTIME_VERDICT  : LCIP_B5_NO_PROVEN_RUNTIME_ERRORS
```
