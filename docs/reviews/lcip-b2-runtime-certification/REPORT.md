# LAWIM — Certification Runtime des 200 Dialogues Réels (LCIP B.2)

**Date :** 2026-07-26
**HEAD :** 303f9ae6

---

## Résumé

Campagne runtime complète des 200 dialogues réels (blocs 1-2). 200/200
exécutées contre ProgramFEngineAdapter en 18.6s. Toutes détectent des écarts
entre les spécifications auto-générées (B.1 migration) et le comportement
runtime réel. La campagne est valide ; les écarts sont documentés.

---

## Verdicts

| Contrôle | Verdict | Preuve |
|----------|---------|--------|
| GIT-0001 | PASS | details/git-details.md |
| SCOPE-0001 | PASS (200) | details/corpus-scope-details.md |
| FID-0001 | PASS (200/200) | details/migration-fidelity-details.md |
| RUN-0001 | PASS (200 exec) | details/runtime-execution-details.md |
| CLASS-0001 | 200 BEHAVIOR_ERROR | details/block-results-details.md |
| PERF-0001 | 18.6s, 88.2ms/conv | details/performance-details.md |
| TEST-0001 | 38/38 PASS | details/test-results-details.md |

---

## Résultats

| Métrique | Valeur |
|----------|--------|
| Conversations sélectionnées | 200 |
| FIDELITY_PASS | 200 |
| Exécutées | 200 |
| Appels runtime | 1 016 |
| Durée totale | 18.6s |
| Moyenne/conversation | 88.2ms |
| p50 | 80ms |
| p95 | 162ms |
| p99 | 257ms |
| RUNTIME_BEHAVIOR_ERROR | 200 |

---

Tous les détails : `details/`
Preuves : `evidence/`
