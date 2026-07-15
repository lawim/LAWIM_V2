# COVERAGE SCORE — Score de Couverture du Patrimoine

**Date :** 15 juillet 2026
**Source de référence :** KNOWLEDGE_COVERAGE_MATRIX.md

---

## 1. Score Global

| Métrique | Valeur |
|----------|--------|
| **Couverture globale estimée** | ~60% |
| **Documents patrimoniaux créés** | 14/14 (100%) |
| **Connaissances tracées** | 73/73 (100%) dans TRACEABILITY_MATRIX.md |
| **Fichiers legacy vérifiables** | 86/86 (100%) Directive/ dans backup branch |
| **Fichiers legacy non vérifiables** | ~150+ (LAWIMA engine, config, IA, DB) |
| **Taux de vérification possible** | ~35% (principalement LAWIM Directive) |

---

## 2. Score par Domaine

Basé sur KNOWLEDGE_COVERAGE_MATRIX.md (matrice des ✓) :

| Domaine | Couverture Rapportée | Sources Vérifiables | Score de Confiance |
|---------|---------------------|--------------------|--------------------|
| Immobilier | ✓✓ Exhaustif | Oui (9 docs Directive/02*) | **90%** |
| Géographie | ✓✓ Exhaustif | Partiel (SOURCE_INVENTORY.md) | **70%** |
| Qualification | ✓✓ Exhaustif | Partiel | **60%** |
| Intentions | ✓✓ Exhaustif | Partiel | **75%** |
| Conversation | ✓✓ Exhaustif | Partiel | **65%** |
| Matching | ✓✓ Exhaustif | Partiel | **65%** |
| CRM / Rôles | ✓✓ Exhaustif | Partiel | **50%** |
| Négociation | ✓ Partiel | Partiel | **40%** |
| Langage | ✓✓ Exhaustif | Partiel | **75%** |
| Datasets | ✓✓ Exhaustif | Faible | **40%** |
| Règles métier | ✓✓ Exhaustif | Faible | **45%** |
| Workflows | ✓✓ Exhaustif | Partiel | **55%** |
| Fraude / Confiance | ✓ Partiel | Partiel | **35%** |
| Monétisation | ✓ Partiel | Faible | **20%** |

---

## 3. Score par Type de Source

| Type de Source | Présumé | Vérifié | Score |
|----------------|---------|---------|-------|
| LAWIM Directive/ | 18 fichiers clés | 27 fichiers dans backup branch | **100%** |
| LAWIM KNOWLEDGE/ geography/ | 11 fichiers | 11 fichiers listés | **80%** |
| LAWIM KNOWLEDGE/ neighborhoods/ | 10 fichiers | 11 fichiers listés | **80%** |
| LAWIM KNOWLEDGE/ intents/ | 5 fichiers | 5 fichiers listés | **80%** |
| LAWIM KNOWLEDGE/ whatsapp_language/ | 7 fichiers | 7 fichiers listés | **80%** |
| LAWIM KNOWLEDGE/ typo_database/ | 5 fichiers | 5 fichiers listés | **80%** |
| LAWIM KNOWLEDGE/ master/ | 15 fichiers | 15 fichiers listés | **80%** |
| LAWIMA 02_KNOWLEDGE/ | ~50+ fichiers | 0 vérifiables | **0%** |
| LAWIMA 03_ENGINE/ | 15 fichiers | 0 vérifiables | **0%** |
| LAWIMA 08_CONFIG/ | 7 fichiers | 0 vérifiables | **0%** |
| LAWIMA 06_AI_MODELS/ | 6 fichiers | 0 vérifiables | **0%** |
| LAWIMA 01_DATABASE/ | 20+ fichiers | 0 vérifiables | **0%** |
| LAWIMA 05_AUTOMATIONS/ | 2 fichiers | 0 vérifiables | **0%** |

---

## 4. Fiabilité des Documents Patrimoniaux

| Document | Fiabilité Estimée | Raison |
|----------|------------------|--------|
| HERITAGE_INDEX.md | **60%** | Partie LAWIM vérifiable, partie LAWIMA non vérifiable |
| DOMAIN_MODEL.md | **50%** | Modèle conceptuel cohérent, mais sources d'implémentation absentes |
| DATASETS.md | **30%** | Comptages contradictoires, sources absentes |
| KNOWLEDGE_COVERAGE_MATRIX.md | **55%** | Matrice cohérente avec quality_report.md mais LAWIMA non vérifiable |
| HERITAGE_GLOSSARY.md | **70%** | 95 termes présents, définitions cohérentes avec Constitution |

---

## 5. Score de Complétude par Exigence

| Exigence | Score |
|----------|-------|
| Exhaustivité des sources LAWIM | ✓ 86/86 fichiers Directive |
| Exhaustivité des sources LAWIMA | ✗ 0/N fichiers |
| Exhaustivité des sources ancienne_structure | ✗ 0/N fichiers |
| Exactitude des comptages | ⚠ 3 contradictions identifiées |
| Traçabilité des concepts | ✓ 73/73 entrées tracées |
| Couverture des domaines | ⚠ 14 domaines documentés, 5 gaps majeurs |
| Qualité des définitions | ✓ 95 termes, cohérence interne |
| Vérifiabilité des affirmations | ⚠ 6/55 validées, 30/55 partielles, 19/55 non validées |
