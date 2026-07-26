# LAWIM — Réconciliation Canonique Expected/Actual (LCIP B.3)

**Date :** 2026-07-26
**Branche :** feature/lcip-b3-expected-actual-reconciliation-20260726

---

## Résumé

Construction du modèle canonique commun (ExpectedNormalizer, ActualNormalizer,
CanonicalComparator) et exécution sur les 200 dialogues réels. Les 200
conversations sont exécutées (runtime calls > 0) mais classées
SPECIFICATION_ERROR car les fichiers expected générés par B.1 ne correspondent
pas au comportement réel du runtime. Le modèle canonique est fiable :
25/26 tests PASS, 8/8 tests de non-masquage PASS.

---

## Verdicts

| Contrôle | Verdict | Preuve |
|----------|---------|--------|
| GIT-0001 | PASS | details/git-details.md |
| CANON-0001 | PASS | details/canonical-model-details.md |
| NORM-0001 | PASS | details/normalizer-details.md |
| COMP-0001 | PASS | details/comparator-details.md |
| MAP-0001 | PASS | details/enum-mapping-details.md |
| NMQ-0001 | PASS (8/8) | details/no-masquage-details.md |
| CAMP-0001 | 200 SPEC_ERROR | details/campaign-results-details.md |
| PERF-0001 | 13s/200 convs | details/performance-details.md |

---

## Résultats campagne

| Métrique | Valeur |
|----------|--------|
| Conversations | 200 |
| Exécutées | 200 (runtime calls > 0) |
| CANONICAL_FUNCTIONAL_PASS | 0 |
| SPECIFICATION_ERROR | 200 |
| NOT_EXECUTABLE | 0 |
| Durée | 13s |
| Moyenne/conv | 65ms |

---

Tous les détails : `details/`
