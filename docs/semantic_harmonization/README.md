# LAWIM H1.2 — Semantic Harmonization

Patrimoine métier Heritage Gold → Modèle actuel LAWIM_V2.

## Documents

| Document | Description |
|----------|-------------|
| `LAWIM_UNIFIED_DOMAIN_MODEL.md` | Modèle cible unifié (indépendant du code) |
| `ROLE_CROSSWALK.md` | Correspondance des rôles, permissions, badges, confiance |
| `PROPERTY_TYPE_CROSSWALK.md` | Correspondance des familles, types, états, prix |
| `SERVICE_CROSSWALK.md` | Correspondance des services (24 RE, 27 PRO, 13 monétisés) |
| `INTENT_TRANSACTION_CROSSWALK.md` | Correspondance des intentions et transactions |
| `WORKFLOW_STATE_CROSSWALK.md` | Correspondance des 21 workflows Heritage Gold |
| `H05_MATRIX_COMPATIBILITY.md` | Compatibilité des 107 matrices de qualification H0.5 |
| `MATCHING_COMPATIBILITY.md` | Compatibilité des rôles de matching H0.5 → H1 |
| `REQUIRED_EXTENSIONS.md` | 175 concepts Heritage sans équivalent V2 |
| `SEMANTIC_CONFLICTS.md` | 13 conflits sémantiques documentés |
| `SEMANTIC_TRACEABILITY_MATRIX.md` | Traçabilité complète (436 entrées) |

## Fichiers JSON

| Fichier | Entrées |
|---------|---------|
| `role_crosswalk.json` | ~55 entrées |
| `property_type_crosswalk.json` | ~76 entrées |
| `service_crosswalk.json` | ~72 entrées |
| `intent_transaction_crosswalk.json` | ~40 entrées |
| `workflow_state_crosswalk.json` | ~21 workflows |
| `h05_matrix_compatibility.json` | ~107 matrices |
| `required_extensions.json` | ~175 extensions |

## Principes de préséance

| Domaine | Modèle prévalent |
|---------|-----------------|
| Architecture, identité, domaines, sécurité, permissions, consentement, persistance, API | LAWIM_V2 actuel |
| Richesse métier, matrices, matching, géographie, workflows, règles commerciales, scripts, langage, SLA, scoring | Heritage Gold |
| Concepts sans équivalent | EXTENSION_REQUIRED |
| Contradictions | HUMAN_DECISION_REQUIRED |

## Verdict

**Voir le rapport final :** `reports/semantic_harmonization/LAWIM_V2_Mission_H12_Semantic_Harmonization.md`
