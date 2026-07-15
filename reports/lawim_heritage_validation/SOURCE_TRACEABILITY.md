# SOURCE TRACEABILITY — Traçabilité des Sources Patrimoine LAWIM

**Date :** 15 juillet 2026
**Statut :** Traçabilité partielle (sources primaires supprimées)

---

## 1. État des Sources

### Branches explorées selon HERITAGE_INDEX.md

| Branche | Chemin déclaré | Existence réelle | Traçabilité |
|---------|---------------|-----------------|-------------|
| **LAWIM** | `LAWIM_BACKUP/LAWIM/` | ✗ N'existe pas | Fichiers Directive/ disponibles dans `backup/pre-repository-cleanup-20260711-100549:docs/Directive/` (86 fichiers) |
| **LAWIMA** | `LAWIM_BACKUP/LAWIMA/` | ✗ N'existe pas | Aucune trace des fichiers 03_ENGINE/, 08_CONFIG/, 06_AI_MODELS/, 01_DATABASE/ |
| **ancienne_structure** | `LAWIM_BACKUP/ancienne_structure/` | ✗ N'existe pas | Décrit comme sous-ensemble de LAWIMA |

### Source alternative disponible

| Source | Chemin | Contenu |
|--------|--------|---------|
| Backup branch | `backup/pre-repository-cleanup-20260711-100549` | docs/Directive/ (86 fichiers), docs/ divers |
| knowledge_unified | `knowledge_unified/` | 50 fichiers consolidés depuis les sources legacy |
| SOURCE_INVENTORY | `knowledge_unified/sources/SOURCE_INVENTORY.md` | Inventaire de ~220 fichiers legacy |
| TRACEABILITY_MATRIX | `knowledge_unified/sources/TRACEABILITY_MATRIX.md` | Mapping legacy → knowledge_unified pour 73 entrées |
| QUALITY_REPORT | `knowledge_unified/validation/quality_report.md` | Rapport qualité du processus de consolidation |

---

## 2. Traçabilité des Fichiers Clés

### LAWIM — Fichiers Directive (vérifiés dans backup branch)

| Fichier déclaré (HERITAGE_INDEX.md §5) | Chemin réel (backup branch) | Statut |
|----------------------------------------|----------------------------|--------|
| `Directive/00-CONSTITUTION.md` | `docs/Directive/00-CONSTITUTION.md` | ✓ Présent (23 articles) |
| `Directive/02-PROPERTY-REFERENCE.md` | `docs/Directive/02-PROPERTY-REFERENCE.md` | ✓ Présent |
| `Directive/02A-RESIDENTIAL-REFERENCE.md` | `docs/Directive/02A-RESIDENTIAL-REFERENCE.md` | ✓ Présent |
| `Directive/02B-COMMERCIAL-REFERENCE.md` | `docs/Directive/02B-COMMERCIAL-REFERENCE.md` | ✓ Présent |
| `Directive/02C-INDUSTRIAL-REFERENCE.md` | `docs/Directive/02C-INDUSTRIAL-REFERENCE.md` | ✓ Présent |
| `Directive/02D-LAND-REFERENCE.md` | `docs/Directive/02D-LAND-REFERENCE.md` | ✓ Présent |
| `Directive/02E-AGRICULTURAL-REFERENCE.md` | `docs/Directive/02E-AGRICULTURAL-REFERENCE.md` | ✓ Présent |
| `Directive/02F-HOTEL-REFERENCE.md` | `docs/Directive/02F-HOTEL-REFERENCE.md` | ✓ Présent |
| `Directive/02G-PROJECT-REFERENCE.md` | `docs/Directive/02G-PROJECT-REFERENCE.md` | ✓ Présent |
| `Directive/02H-ATTRIBUTE-CATALOG.md` | `docs/Directive/02H-ATTRIBUTE-CATALOG.md` | ✓ Présent |
| `Directive/02I-PRICING-REFERENCE.md` | `docs/Directive/02I-PRICING-REFERENCE.md` | ✓ Présent |
| `Directive/03-CONVERSATION-REFERENCE.md` | `docs/Directive/03-CONVERSATION-REFERENCE.md` | ✓ Présent |
| `Directive/04-MATCHING-REFERENCE.md` | `docs/Directive/04-MATCHING-REFERENCE.md` | ✓ Présent |
| `Directive/04-DECISION-ENGINE-REFERENCE.md` | `docs/Directive/04-DECISION-ENGINE-REFERENCE.md` | ✓ Présent |
| `Directive/05-WORKFLOW-REFERENCE.md` | `docs/Directive/05-WORKFLOW-REFERENCE.md` | ✓ Présent |
| `Directive/06-DATABASE-REFERENCE.md` | `docs/Directive/06-DATABASE-REFERENCE.md` | ✓ Présent |
| `Directive/08-ROLE-REFERENCE.md` | `docs/Directive/08-ROLE-REFERENCE.md` | ✓ Présent |
| `Directive/09-GEOLOCATION-REFERENCE.md` | `docs/Directive/09-GEOLOCATION-REFERENCE.md` | ✓ Présent |
| `Directive/10-NOTIFICATION-REFERENCE.md` | `docs/Directive/10-NOTIFICATION-REFERENCE.md` | ✓ Présent |
| `Directive/15-SECURITY-REFERENCE.md` | `docs/Directive/15-SECURITY-REFERENCE.md` | ✓ Présent |
| `Directive/16-API-REFERENCE.md` | `docs/Directive/16-API-REFERENCE.md` | ✓ Présent |
| `Directive/18-LAWIM-AI-REFERENCE.md` | `docs/Directive/18-LAWIM-AI-REFERENCE.md` | ✓ Présent |
| `Directive/48-LAWIM-SALES-PLAYBOOK.md` | `docs/Directive/48-LAWIM-SALES-PLAYBOOK.md` | ✓ Présent |
| `Directive/LAWIM-BRAND-BOOK.md` | `docs/Directive/LAWIM-BRAND-BOOK.md` | ✓ Présent |
| `Directive/LAWIM-BUSINESS-PLAN.md` | `docs/Directive/LAWIM-BUSINESS-PLAN.md` | ✓ Présent |
| `Directive/LAWIM-OPERATIONS-MANUAL.md` | `docs/Directive/LAWIM-OPERATIONS-MANUAL.md` | ✓ Présent |
| `Directive/Plan_strategique_lancement.md` | `docs/Directive/Plan_strategique_lancement.md` | ✓ Présent |
| `Directive/Analyse *marché immobilier*.md` | `docs/Directive/Analyse __- marché immobilier camerounais_- groupe.md` | ✓ Présent |

### LAWIM — Fichiers Knowledge (documentés dans SOURCE_INVENTORY.md uniquement)

| Fichier déclaré | Source de vérification | Statut |
|----------------|----------------------|--------|
| `KNOWLEDGE/LAWIM_MASTER_DATASET.json` | SOURCE_INVENTORY.md (250KB) | ✓ Documenté |
| `KNOWLEDGE/geography/` (11 fichiers) | SOURCE_INVENTORY.md (11 fichiers listés) | ✓ Documenté |
| `KNOWLEDGE/neighborhoods/` (10 fichiers ville) | SOURCE_INVENTORY.md (11 fichiers listés) | ✓ Documenté |
| `KNOWLEDGE/intents/` (5 fichiers) | SOURCE_INVENTORY.md (5 fichiers listés) | ✓ Documenté |
| `KNOWLEDGE/whatsapp_language/` (7 fichiers) | SOURCE_INVENTORY.md (7 fichiers listés) | ✓ Documenté |
| `KNOWLEDGE/typo_database/` (5 fichiers) | SOURCE_INVENTORY.md (5 fichiers listés) | ✓ Documenté |
| `KNOWLEDGE/conversation-patterns.md` | SOURCE_INVENTORY.md (9.0KB, listé) | ✓ Documenté |
| `KNOWLEDGE/negotiation-patterns.md` | SOURCE_INVENTORY.md (4.8KB, listé) | ✓ Documenté |
| `KNOWLEDGE/qualification-implementation-backlog.md` | SOURCE_INVENTORY.md (14.3KB, listé) | ✓ Documenté |
| `KNOWLEDGE/master/` (15 docs) | SOURCE_INVENTORY.md (15 fichiers listés) | ✓ Documenté |
| `KNOWLEDGE/fraud-signals-and-verification.md` | SOURCE_INVENTORY.md (6.0KB, listé) | ✓ Documenté |
| `KNOWLEDGE/diaspora-behavior-model.md` | SOURCE_INVENTORY.md (4.8KB, listé) | ✓ Documenté |
| `KNOWLEDGE/city-affinity-matrix.md` | SOURCE_INVENTORY.md (1.3KB, listé) | ✓ Documenté |

### LAWIMA — Fichiers (aucune source disponible)

| Fichier déclaré | Source | Statut |
|----------------|--------|--------|
| `02_KNOWLEDGE/intents/*.json` | Aucune | ✗ Non vérifiable |
| `06_AI_MODELS/lead_classifier/` | Aucune | ✗ Non vérifiable |
| `08_CONFIG/rule_engine/RULE_ENGINE_V5.json` | Aucune | ✗ Non vérifiable |
| `08_CONFIG/features/FEATURE_FLAGS.json` | Aucune | ✗ Non vérifiable |
| `03_ENGINE/anti_spam.py` | Aucune | ✗ Non vérifiable |
| `05_AUTOMATIONS/scripts/implement_all.sql` | Aucune | ✗ Non vérifiable |
| `01_DATABASE/runtime/*.csv` | Aucune | ✗ Non vérifiable |
| `00_GLOBAL/rules/RESPONSE_POLICY.md` | Aucune | ✗ Non vérifiable |

---

## 3. Traçabilité des Concepts (TRACEABILITY_MATRIX.md → knowledge_unified/)

| Domaine | Entrées legacy tracées | Statut |
|---------|----------------------|--------|
| Géographie | GEO-001 à GEO-014 (14 entrées) | ✓ Toutes tracées vers geography/ |
| Qualification | QUAL-001 à QUAL-013 (13 entrées) | ✓ Toutes tracées vers qualification/ |
| Matching | MATCH-001 à MATCH-006 (6 entrées) | ✓ Toutes tracées vers matching/ |
| Langage | LANG-001 à LANG-014 (14 entrées) | ✓ Toutes tracées vers language/ |
| Commercial | COMM-001 à COMM-008 (8 entrées) | ✓ Toutes tracées vers commercial/ |
| Professionnels | PROF-001 à PROF-003 (3 entrées) | ✓ Toutes tracées vers professionals/ |
| Légal | LEGAL-001 à LEGAL-002 (2 entrées) | ✓ Toutes tracées vers legal_and_documents/ |
| Immobilier | RE-001 à RE-007 (7 entrées) | ✓ Toutes tracées vers real_estate/ |

**Total :** 73 entrées legacy tracées vers 50 fichiers consolidés.

---

## 4. Gaps de Traçabilité

| Connaissance | Raison de l'absence |
|-------------|---------------------|
| Feature flags | Pas dans le périmètre de TRACEABILITY_MATRIX.md |
| Anti-spam | Pas dans le périmètre de TRACEABILITY_MATRIX.md |
| SQL schemas (implement_all.sql) | Pas dans le périmètre de TRACEABILITY_MATRIX.md |
| CSV datasets | Pas dans le périmètre de TRACEABILITY_MATRIX.md |
| Configs IA (06_AI_MODELS) | Pas dans le périmètre de TRACEABILITY_MATRIX.md |
| Rule engine versions (08_CONFIG) | Pas dans le périmètre de TRACEABILITY_MATRIX.md |
| Architecture LAWIMA | Pas dans le périmètre de TRACEABILITY_MATRIX.md |
