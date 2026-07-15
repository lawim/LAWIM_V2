# SOURCE TRACEABILITY — Matrice de Traçabilité des Sources des Matrices de Qualification

**Document ID:** LAWIM-GOLD-QM-TRACE-V1
**Mission:** LAWIM Heritage Gold — Qualification Matrices
**Date:** 2026-07-15
**Statut:** CANONICAL — Traçabilité exhaustive de chaque champ, règle et matrice vers sa source originale

---

## 1. Introduction

### 1.1 Purpose

This document provides end-to-end traceability for every qualification matrix in `docs/lawim_heritage_gold/qualification_matrices/`. It answers the question: **"Where does this field, rule, or matrix come from?"**

### 1.2 Methodology

Each matrix, field, business rule, and conditional rule is traced back to one or more of the following:

1. **Heritage backup files** — Documents recovered from the LAWIM backup branch (`pre-repository-cleanup-20260711-100549`)
2. **knowledge_unified/** — Consolidated JSON/MD files in `LAWIM_V2/knowledge_unified/`
3. **LAWIM_V2 code** — Python source files in `code/lawim_v2/` and `matrices.py`
4. **Heritage Gold documents** — Processed reference docs in `docs/lawim_heritage_gold/`
5. **Heritage H0 documents** — Heritage docs in `docs/lawim_heritage/`
6. **Ancienne structure (deleted)** — Legacy JSON files from the deleted `ancienne_structure/` directory, documented via SOURCE_INVENTORY.md
7. **Expert proposals** — New content not found in heritage, proposed by domain experts

### 1.3 Source ID Convention

| Prefix | Branch | Location | Status |
|--------|--------|----------|--------|
| SRC-MFR | backup:docs/Directive/ | minimum-fields-request.md, minimum-fields-property.md | BACKUP |
| SRC-MFP | backup:docs/Directive/ | property-qualification-reference.md | BACKUP |
| SRC-CQQ | backup:docs/Directive/ | conversation-qualification-questions.md | BACKUP |
| SRC-QIB | backup:docs/Directive/ | qualification-implementation-backlog.md | BACKUP |
| SRC-03P | backup:docs/Directive/REFERENCE/ | 03-PROPERTY-QUALIFICATION.md | BACKUP REFERENCE |
| SRC-18Q | backup:docs/Directive/ | 18_QUALIFICATION_MATRIX_IMPLEMENTATION.md | BACKUP |
| SRC-WTD | backup:docs/Directive/channels/ | whatsapp-telegram-dashboard-qualification.md | BACKUP |
| SRC-HGQ | docs/lawim_heritage_gold/ | QUALIFICATION_MODEL.md | HERITAGE_GOLD |
| SRC-HGX | docs/lawim_heritage_gold/ | QUALIFICATION_HERITAGE_EXTRACTION.md | HERITAGE_GOLD |
| SRC-HGP | docs/lawim_heritage_gold/ | PROPERTY_MODEL.md | HERITAGE_GOLD |
| SRC-HGM | docs/lawim_heritage_gold/ | MATCHING_MODEL.md | HERITAGE_GOLD |
| SRC-COD | code/lawim_v2/ | matrices.py (and other Python modules) | CODE |
| SRC-SKU | knowledge_unified/ | Various JSON/MD files | KNOWLEDGE_UNIFIED |
| SRC-ANS | ancienne_structure/ | lead_classifier_v1.json, RULE_ENGINE_V5.json, property_matching_v1.json, property_types.py | ANCIENNE_STRUCTURE |

### 1.4 Confidence Levels

| Level | Meaning |
|-------|---------|
| HIGH | Directly confirmed from heritage source with exact match |
| MEDIUM | Inferred from multiple sources or partially confirmed |
| LOW | Expert proposal or deduction without heritage confirmation |
| NOT_FOUND | Cannot be traced to any known source |

---

## 2. Heritage Sources Catalog

### 2.1 Backup Sources (pre-repository-cleanup-20260711-100549)

| Source ID | Source Name | Source File/Path | Source Type | Discovery Method | Extraction Date | Confidence |
|-----------|-------------|-------------------|-------------|------------------|-----------------|------------|
| SRC-MFR-001 | Minimum Fields — Request | backup:docs/Directive/minimum-fields-request.md | BACKUP | Manual exploration of backup branch | 2026-07-11 | HIGH |
| SRC-MFP-001 | Minimum Fields — Property | backup:docs/Directive/minimum-fields-property.md | BACKUP | Manual exploration of backup branch | 2026-07-11 | HIGH |
| SRC-PQR-001 | Property Qualification Reference | backup:docs/Directive/property-qualification-reference.md | BACKUP | Manual exploration of backup branch | 2026-07-11 | HIGH |
| SRC-CQQ-001 | Conversation Qualification Questions | backup:docs/Directive/conversation-qualification-questions.md | BACKUP | Manual exploration of backup branch | 2026-07-11 | HIGH |
| SRC-QIB-001 | Qualification Implementation Backlog | backup:docs/Directive/qualification-implementation-backlog.md | BACKUP | Manual exploration of backup branch | 2026-07-11 | HIGH |
| SRC-03P-001 | 03-PROPERTY-QUALIFICATION.md | backup:docs/Directive/REFERENCE/03-PROPERTY-QUALIFICATION.md | BACKUP REFERENCE | Manual exploration of backup branch | 2026-07-11 | HIGH |
| SRC-18Q-001 | 18_QUALIFICATION_MATRIX_IMPLEMENTATION.md | backup:docs/Directive/18_QUALIFICATION_MATRIX_IMPLEMENTATION.md | BACKUP | Manual exploration of backup branch | 2026-07-11 | HIGH |
| SRC-WTD-001 | WhatsApp/Telegram/Dashboard Qualification | backup:docs/Directive/channels/whatsapp-telegram-dashboard-qualification.md | BACKUP | Manual exploration of backup branch | 2026-07-11 | HIGH |

### 2.2 Heritage Gold Sources

| Source ID | Source Name | Source File/Path | Source Type | Discovery Method | Extraction Date | Confidence |
|-----------|-------------|-------------------|-------------|------------------|-----------------|------------|
| SRC-HGQ-001 | QUALIFICATION_MODEL.md | docs/lawim_heritage_gold/QUALIFICATION_MODEL.md | HERITAGE_GOLD | Synthesized from heritage backup sources | 2026-07-15 | HIGH |
| SRC-HGX-001 | QUALIFICATION_HERITAGE_EXTRACTION.md | docs/lawim_heritage_gold/QUALIFICATION_HERITAGE_EXTRACTION.md | HERITAGE_GOLD | Synthesized from heritage backup sources | 2026-07-15 | HIGH |
| SRC-HGP-001 | PROPERTY_MODEL.md (Gold) | docs/lawim_heritage_gold/PROPERTY_MODEL.md | HERITAGE_GOLD | Synthesized from heritage backup sources | 2026-07-15 | HIGH |
| SRC-HGM-001 | MATCHING_MODEL.md (Gold) | docs/lawim_heritage_gold/MATCHING_MODEL.md | HERITAGE_GOLD | Synthesized from heritage backup sources | 2026-07-15 | HIGH |
| SRC-HGS-001 | SOURCE_INDEX.md (Gold) | docs/lawim_heritage_gold/SOURCE_INDEX.md | HERITAGE_GOLD | Synthesized from heritage backup sources | 2026-07-15 | HIGH |
| SRC-HGT-001 | TRACEABILITY_MATRIX.md (Gold) | docs/lawim_heritage_gold/TRACEABILITY_MATRIX.md | HERITAGE_GOLD | Synthesized from heritage backup sources | 2026-07-15 | HIGH |
| SRC-HGR-001 | RULE_INDEX.md (Gold) | docs/lawim_heritage_gold/RULE_INDEX.md | HERITAGE_GOLD | Synthesized from heritage backup sources | 2026-07-15 | HIGH |
| SRC-HGO-001 | OPEN_POINTS.md (Gold) | docs/lawim_heritage_gold/OPEN_POINTS.md | HERITAGE_GOLD | Synthesized from heritage backup sources | 2026-07-15 | HIGH |
| SRC-HGE-001 | EVIDENCE_INDEX.md (Gold) | docs/lawim_heritage_gold/EVIDENCE_INDEX.md | HERITAGE_GOLD | Synthesized from heritage backup sources | 2026-07-15 | HIGH |

### 2.3 Knowledge Unified Sources

| Source ID | Source Name | Source File/Path | Source Type | Discovery Method | Extraction Date | Confidence |
|-----------|-------------|-------------------|-------------|------------------|-----------------|------------|
| SRC-SKU-001 | Property Search Matrices | knowledge_unified/qualification/property_search_matrices.json | KNOWLEDGE_UNIFIED | Direct file access | 2026-07-15 | HIGH |
| SRC-SKU-002 | Seller Matrices | knowledge_unified/qualification/seller_matrices.json | KNOWLEDGE_UNIFIED | Direct file access | 2026-07-15 | HIGH |
| SRC-SKU-003 | Investor Matrices | knowledge_unified/qualification/investor_matrices.json | KNOWLEDGE_UNIFIED | Direct file access | 2026-07-15 | HIGH |
| SRC-SKU-004 | Owner Matrices | knowledge_unified/qualification/owner_matrices.json | KNOWLEDGE_UNIFIED | Direct file access | 2026-07-15 | HIGH |
| SRC-SKU-005 | Professional Search Matrices | knowledge_unified/qualification/professional_search_matrices.json | KNOWLEDGE_UNIFIED | Direct file access | 2026-07-15 | HIGH |
| SRC-SKU-006 | Scoring Rules | knowledge_unified/matching/scoring_rules.json | KNOWLEDGE_UNIFIED | Direct file access | 2026-07-15 | HIGH |
| SRC-SKU-007 | Intentions | knowledge_unified/qualification/intentions.json | KNOWLEDGE_UNIFIED | Direct file access | 2026-07-15 | HIGH |
| SRC-SKU-008 | User Typologies | knowledge_unified/qualification/user_typologies.json | KNOWLEDGE_UNIFIED | Direct file access | 2026-07-15 | HIGH |
| SRC-SKU-009 | Qualification Rules | knowledge_unified/qualification/qualification_rules.md | KNOWLEDGE_UNIFIED | Direct file access | 2026-07-15 | HIGH |
| SRC-SKU-010 | Source Inventory | knowledge_unified/sources/SOURCE_INVENTORY.md | KNOWLEDGE_UNIFIED | Direct file access | 2026-07-15 | HIGH |
| SRC-SKU-011 | Traceability Matrix (KU) | knowledge_unified/sources/TRACEABILITY_MATRIX.md | KNOWLEDGE_UNIFIED | Direct file access | 2026-07-15 | HIGH |

### 2.4 Code Sources (LAWIM V2)

| Source ID | Source Name | Source File/Path | Source Type | Discovery Method | Extraction Date | Confidence |
|-----------|-------------|-------------------|-------------|------------------|-----------------|------------|
| SRC-COD-001 | Matrices Python Module | code/lawim_v2/matrices.py | CODE | Direct file access | 2026-07-15 | HIGH |
| SRC-COD-002 | Property Domain Module | code/lawim_v2/property_domain.py | CODE | Direct file access | 2026-07-15 | HIGH |
| SRC-COD-003 | Conversation Domain Module | code/lawim_v2/conversation_domain.py | CODE | Direct file access | 2026-07-15 | HIGH |
| SRC-COD-004 | User Roles Module | code/lawim_v2/user_roles.py | CODE | Direct file access | 2026-07-15 | HIGH |
| SRC-COD-005 | CRM Domain Module | code/lawim_v2/crm_domain.py | CODE | Direct file access | 2026-07-15 | HIGH |
| SRC-COD-006 | Geo Reference Module | code/lawim_v2/geo_reference.py | CODE | Direct file access | 2026-07-15 | HIGH |

### 2.5 Ancienne Structure Sources (Deleted — Documented via SOURCE_INVENTORY)

| Source ID | Source Name | Source File/Path | Source Type | Discovery Method | Extraction Date | Confidence |
|-----------|-------------|-------------------|-------------|------------------|-----------------|------------|
| SRC-ANS-001 | Lead Classifier V1 | ancienne_structure/lead_classifier_v1.json | ANCIENNE_STRUCTURE | SOURCE_INVENTORY.md documentation | 2026-07-11 | MEDIUM |
| SRC-ANS-002 | Rule Engine V5 | ancienne_structure/RULE_ENGINE_V5.json | ANCIENNE_STRUCTURE | SOURCE_INVENTORY.md documentation | 2026-07-11 | MEDIUM |
| SRC-ANS-003 | Property Matching V1 | ancienne_structure/property_matching_v1.json | ANCIENNE_STRUCTURE | SOURCE_INVENTORY.md documentation | 2026-07-11 | MEDIUM |
| SRC-ANS-004 | Property Types | ancienne_structure/property_types.py | ANCIENNE_STRUCTURE | SOURCE_INVENTORY.md documentation | 2026-07-11 | LOW |

### 2.6 Heritage H0 Sources

| Source ID | Source Name | Source File/Path | Source Type | Discovery Method | Extraction Date | Confidence |
|-----------|-------------|-------------------|-------------|------------------|-----------------|------------|
| SRC-H00-001 | PROPERTY_MODEL.md (H0) | docs/lawim_heritage/PROPERTY_MODEL.md | HERITAGE | H0 extraction | 2026-07-10 | HIGH |
| SRC-H00-002 | QUALIFICATION_MODEL.md (H0) | docs/lawim_heritage/QUALIFICATION_MODEL.md | HERITAGE | H0 extraction | 2026-07-10 | HIGH |
| SRC-H00-003 | INTENT_MODEL.md (H0) | docs/lawim_heritage/INTENT_MODEL.md | HERITAGE | H0 extraction | 2026-07-10 | HIGH |
| SRC-H00-004 | ROLE_MODEL.md (H0) | docs/lawim_heritage/ROLE_MODEL.md | HERITAGE | H0 extraction | 2026-07-10 | HIGH |
| SRC-H00-005 | DOMAIN_MODEL.md (H0) | docs/lawim_heritage/DOMAIN_MODEL.md | HERITAGE | H0 extraction | 2026-07-10 | HIGH |

---

## 3. Matrix → Source Mapping

### 3.1 Residential Search Matrices

| Matrix ID | Property Type | Primary Heritage Sources | Secondary Sources | Confidence |
|-----------|---------------|-------------------------|-------------------|------------|
| MATRIX-RES-SEARCH-001 | chambre_simple | SRC-CQQ-001, SRC-MFR-001, SRC-PQR-001 | SRC-SKU-001, SRC-HGQ-001 | HIGH |
| MATRIX-RES-SEARCH-002 | chambre_moderne | SRC-CQQ-001, SRC-MFR-001, SRC-PQR-001 | SRC-SKU-001, SRC-HGQ-001 | HIGH |
| MATRIX-RES-SEARCH-003 | studio | SRC-CQQ-001, SRC-MFR-001, SRC-PQR-001 | SRC-SKU-001, SRC-HGQ-001 | HIGH |
| MATRIX-RES-SEARCH-004 | studio_moderne | SRC-CQQ-001, SRC-MFR-001, SRC-PQR-001 | SRC-SKU-001, SRC-HGQ-001 | HIGH |
| MATRIX-RES-SEARCH-005 | studio_meuble | SRC-CQQ-001, SRC-MFR-001, SRC-PQR-001 | SRC-SKU-001, SRC-HGQ-001 | HIGH |
| MATRIX-RES-SEARCH-006 | appartement_non_meuble | SRC-CQQ-001, SRC-MFR-001, SRC-PQR-001 | SRC-SKU-001, SRC-HGQ-001 | HIGH |
| MATRIX-RES-SEARCH-007 | appartement_meuble | SRC-CQQ-001, SRC-MFR-001, SRC-PQR-001 | SRC-SKU-001, SRC-HGQ-001 | HIGH |
| MATRIX-RES-SEARCH-008 | villa | SRC-CQQ-001, SRC-MFR-001, SRC-PQR-001 | SRC-SKU-001, SRC-HGQ-001 | HIGH |
| MATRIX-RES-SEARCH-009 | villa_basse | SRC-CQQ-001, SRC-03P-001 | SRC-HGP-001 | MEDIUM |
| MATRIX-RES-SEARCH-010 | duplex | SRC-CQQ-001, SRC-MFR-001, SRC-03P-001 | SRC-HGP-001 | HIGH |
| MATRIX-RES-SEARCH-011 | triplex | SRC-CQQ-001, SRC-03P-001 | SRC-HGP-001, SRC-SKU-001 | MEDIUM |
| MATRIX-RES-SEARCH-012 | maison_individuelle | SRC-CQQ-001, SRC-MFP-001, SRC-PQR-001 | SRC-SKU-001, SRC-HGP-001 | HIGH |
| MATRIX-RES-SEARCH-013 | maison_de_ville | SRC-CQQ-001, SRC-MFP-001 | SRC-HGP-001 | MEDIUM |
| MATRIX-RES-SEARCH-014 | chambre_hotel | SRC-WTD-001, SRC-CQQ-001 | SRC-HGQ-001, SRC-SKU-001 | MEDIUM |
| MATRIX-RES-SEARCH-015 | appartement_courte_duree | SRC-WTD-001, SRC-CQQ-001 | SRC-HGQ-001 | MEDIUM |
| MATRIX-RES-SEARCH-016 | residence_meublee | SRC-WTD-001, SRC-03P-001 | SRC-SKU-001 | MEDIUM |
| MATRIX-RES-SEARCH-017 | colocation | SRC-CQQ-001, SRC-PQR-001 | SRC-HGP-001, SRC-HGQ-001 | MEDIUM |
| MATRIX-RES-SEARCH-018 | cite_universitaire | SRC-03P-001, SRC-CQQ-001 | SRC-HGP-001 | MEDIUM |

### 3.2 Land Search Matrices

| Matrix ID | Property Type | Primary Heritage Sources | Secondary Sources | Confidence |
|-----------|---------------|-------------------------|-------------------|------------|
| LAND_SEARCH_TERRAIN_TITRE_001 | terrain_titre | SRC-MFP-001, SRC-PQR-001, SRC-18Q-001 | SRC-HGP-001, SRC-SKU-001 | HIGH |
| LAND_SEARCH_TERRAIN_NON_TITRE_001 | terrain_non_titre | SRC-MFP-001, SRC-PQR-001, SRC-18Q-001 | SRC-HGP-001, SRC-SKU-001 | HIGH |
| LAND_SEARCH_TERRAIN_LOTI_001 | terrain_loti | SRC-MFP-001, SRC-PQR-001 | SRC-HGP-001 | HIGH |
| LAND_SEARCH_TERRAIN_NON_LOTI_001 | terrain_non_loti | SRC-MFP-001, SRC-PQR-001 | SRC-HGP-001 | HIGH |
| LAND_SEARCH_TERRAIN_TITRE_COLLECTIF_001 | terrain_titre_collectif | SRC-MFP-001, SRC-QIB-001 | SRC-HGP-001, SRC-ANS-003 | MEDIUM |
| LAND_SEARCH_TERRAIN_TITRE_INDIVIDUEL_001 | terrain_titre_individuel | SRC-MFP-001, SRC-QIB-001 | SRC-HGP-001 | MEDIUM |
| LAND_SEARCH_TERRAIN_SOUS_MORCELLEMENT_001 | terrain_sous_morcellement | SRC-MFP-001, SRC-QIB-001 | SRC-HGP-001, SRC-ANS-003 | MEDIUM |

### 3.3 Commercial Property Matrices

| Matrix ID | Property Type | Primary Heritage Sources | Secondary Sources | Confidence |
|-----------|---------------|-------------------------|-------------------|------------|
| COM-MATRIX-001 | boutique | SRC-PQR-001, SRC-CQQ-001, SRC-03P-001 | SRC-SKU-001, SRC-HGP-001 | HIGH |
| COM-MATRIX-002 | bureau | SRC-PQR-001, SRC-CQQ-001, SRC-03P-001 | SRC-SKU-001, SRC-HGP-001 | HIGH |
| COM-MATRIX-003 | local_commercial | SRC-PQR-001, SRC-CQQ-001, SRC-03P-001 | SRC-SKU-001, SRC-HGP-001 | HIGH |
| COM-MATRIX-004 | magasin | SRC-PQR-001, SRC-03P-001 | SRC-HGP-001 | HIGH |
| COM-MATRIX-005 | entrepot | SRC-PQR-001, SRC-03P-001 | SRC-HGP-001 | HIGH |
| COM-MATRIX-006 | hangar | SRC-03P-001, SRC-PQR-001 | SRC-HGP-001 | MEDIUM |
| COM-MATRIX-007 | atelier | SRC-PQR-001, SRC-03P-001 | SRC-HGP-001 | MEDIUM |
| COM-MATRIX-008 | restaurant | SRC-CQQ-001, SRC-PQR-001 | SRC-HGP-001 | MEDIUM |
| COM-MATRIX-009 | bar | SRC-CQQ-001, SRC-PQR-001 | SRC-HGP-001 | MEDIUM |
| COM-MATRIX-010 | hotel | SRC-03P-001, SRC-PQR-001, SRC-CQQ-001 | SRC-HGP-001, SRC-SKU-001 | HIGH |
| COM-MATRIX-011 | auberge | SRC-03P-001, SRC-PQR-001 | SRC-HGP-001 | MEDIUM |
| COM-MATRIX-012 | immeuble_de_rapport | SRC-PQR-001, SRC-03P-001 | SRC-HGP-001 | MEDIUM |
| COM-MATRIX-013 | immeuble_commercial | SRC-03P-001, SRC-PQR-001 | SRC-HGP-001, SRC-SKU-001 | MEDIUM |
| COM-MATRIX-014 | station_service | SRC-03P-001 | SRC-HGP-001 | MEDIUM |
| COM-MATRIX-015 | site_industriel | SRC-03P-001, SRC-PQR-001 | SRC-HGP-001 | MEDIUM |
| COM-MATRIX-016 | espace_evenementiel | SRC-03P-001 | SRC-HGP-001 | LOW |
| COM-MATRIX-017 | investissement_locatif | SRC-SKU-003, SRC-CQQ-001, SRC-QIB-001 | SRC-HGQ-001, SRC-HGP-001 | MEDIUM |
| COM-MATRIX-018 | investissement_terrain | SRC-SKU-003, SRC-CQQ-001, SRC-QIB-001 | SRC-HGQ-001, SRC-HGP-001 | MEDIUM |
| COM-MATRIX-019 | investissement_immobilier_commercial | SRC-SKU-003, SRC-QIB-001 | SRC-HGQ-001 | LOW |
| COM-MATRIX-020 | investissement_promotion | SRC-SKU-003, SRC-QIB-001 | SRC-HGQ-001 | LOW |
| COM-MATRIX-021 | syndicat_copropriete | SRC-QIB-001, SRC-03P-001 | SRC-HGP-001 | LOW |

### 3.4 Financing Request Matrices

| Matrix ID | Financing Type | Primary Heritage Sources | Secondary Sources | Confidence |
|-----------|---------------|-------------------------|-------------------|------------|
| MATRIX-FIN-001 | credit_immobilier | SRC-CQQ-001, SRC-QIB-001, SRC-PQR-001 | SRC-SKU-001, SRC-HGQ-001 | HIGH |
| MATRIX-FIN-002 | financement_acquisition | SRC-CQQ-001, SRC-QIB-001 | SRC-SKU-001, SRC-HGQ-001 | HIGH |
| MATRIX-FIN-003 | financement_construction | SRC-CQQ-001, SRC-QIB-001, SRC-PQR-001 | SRC-HGQ-001, SRC-SKU-001 | HIGH |
| MATRIX-FIN-004 | financement_renovation | SRC-QIB-001, SRC-CQQ-001 | SRC-HGQ-001 | MEDIUM |
| MATRIX-FIN-005 | financement_promotion_immobiliere | SRC-QIB-001, SRC-SKU-003 | SRC-HGQ-001 | MEDIUM |
| MATRIX-FIN-006 | pret_adosse_bien | SRC-QIB-001 | SRC-HGQ-001, SRC-HGP-001 | LOW |
| MATRIX-FIN-007 | recherche_investisseur | SRC-SKU-003, SRC-QIB-001 | SRC-HGQ-001 | LOW |
| MATRIX-FIN-008 | cofinancement | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| MATRIX-FIN-009 | apport_diaspora | SRC-SKU-003, SRC-QIB-001 | SRC-SKU-006, SRC-HGQ-001 | MEDIUM |
| MATRIX-FIN-010 | financement_professionnel | SRC-QIB-001, SRC-SKU-005 | SRC-HGQ-001 | LOW |

### 3.5 Professional Service Matrices

| Matrix ID | Service Type | Primary Heritage Sources | Secondary Sources | Confidence |
|-----------|-------------|-------------------------|-------------------|------------|
| PRO-AGENT-001 | agent_immobilier | SRC-CQQ-001, SRC-18Q-001, SRC-WTD-001 | SRC-SKU-005, SRC-H00-004 | HIGH |
| PRO-AGENC-002 | agence_immobiliere | SRC-CQQ-001, SRC-18Q-001, SRC-WTD-001 | SRC-SKU-005, SRC-H00-004 | HIGH |
| PRO-NOTAI-003 | notaire | SRC-CQQ-001, SRC-18Q-001, SRC-WTD-001 | SRC-SKU-005, SRC-H00-004 | HIGH |
| PRO-GEOME-004 | geometre | SRC-CQQ-001, SRC-18Q-001 | SRC-SKU-005 | HIGH |
| PRO-ARCHI-005 | architecte | SRC-CQQ-001, SRC-18Q-001 | SRC-SKU-005 | HIGH |
| PRO-INGEN-006 | ingenieur_genie_civil | SRC-CQQ-001, SRC-18Q-001 | SRC-SKU-005 | MEDIUM |
| PRO-TECHN-007 | technicien_batiment | SRC-CQQ-001 | SRC-SKU-005 | MEDIUM |
| PRO-MACON-008 | macon | SRC-CQQ-001 | SRC-SKU-005 | MEDIUM |
| PRO-ELECT-009 | electricien | SRC-CQQ-001 | SRC-SKU-005 | MEDIUM |
| PRO-PLOMB-010 | plombier | SRC-CQQ-001 | SRC-SKU-005 | MEDIUM |
| PRO-MENUI-011 | menuisier | SRC-CQQ-001 | SRC-SKU-005 | MEDIUM |
| PRO-PEINT-012 | peintre | SRC-CQQ-001 | SRC-SKU-005 | MEDIUM |
| PRO-CARRE-013 | carreleur | SRC-CQQ-001 | SRC-SKU-005 | MEDIUM |
| PRO-COUVR-014 | couvreur | SRC-CQQ-001 | SRC-SKU-005 | MEDIUM |
| PRO-EXPIM-015 | expert_immobilier | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| PRO-EVALU-016 | evaluateur | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| PRO-GESTI-017 | gestionnaire_immobilier | SRC-QIB-001, SRC-CQQ-001 | SRC-HGQ-001 | LOW |
| PRO-SYNDI-018 | syndic | SRC-QIB-001, SRC-CQQ-001 | SRC-HGQ-001 | LOW |
| PRO-PHOTO-019 | photographe_immobilier | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| PRO-VIDEO-020 | videaste_drone | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| PRO-DEMEN-021 | demenageur | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| PRO-NETTO-022 | entreprise_nettoyage | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| PRO-GARDI-023 | gardiennage | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| PRO-ASSUR-024 | assureur | SRC-QIB-001, SRC-CQQ-001 | SRC-HGQ-001 | LOW |
| PRO-BANQU-025 | banque_microfinance | SRC-QIB-001, SRC-CQQ-001 | SRC-HGQ-001 | LOW |
| PRO-COURT-026 | courtier | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| PRO-PREST-027 | prestataire_administratif | SRC-QIB-001 | SRC-HGQ-001 | LOW |

### 3.6 Real Estate Service Matrices

| Matrix ID | Service Type | Primary Heritage Sources | Secondary Sources | Confidence |
|-----------|-------------|-------------------------|-------------------|------------|
| SVC-ESTI-001 | estimation_immobiliere | SRC-CQQ-001, SRC-18Q-001 | SRC-HGQ-001, SRC-HGP-001 | HIGH |
| SVC-EXPE-002 | expertise | SRC-CQQ-001, SRC-18Q-001 | SRC-HGQ-001 | HIGH |
| SVC-VERI-003 | verification_documentaire | SRC-CQQ-001, SRC-18Q-001 | SRC-HGQ-001, SRC-HGP-001 | HIGH |
| SVC-VISI-004 | visite_property | SRC-CQQ-001, SRC-WTD-001 | SRC-HGQ-001, SRC-SKU-001 | HIGH |
| SVC-CONT-005 | contre_visite | SRC-CQQ-001, SRC-WTD-001 | SRC-HGQ-001 | MEDIUM |
| SVC-GEST-006 | gestion_locative | SRC-CQQ-001, SRC-18Q-001 | SRC-HGQ-001 | HIGH |
| SVC-MISE-007 | mise_en_location | SRC-CQQ-001, SRC-18Q-001 | SRC-HGQ-001, SRC-SKU-004 | HIGH |
| SVC-MISE-008 | mise_en_vente | SRC-CQQ-001, SRC-18Q-001 | SRC-HGQ-001, SRC-SKU-002 | HIGH |
| SVC-PUBL-009 | publication_service | SRC-CQQ-001, SRC-18Q-001 | SRC-HGQ-001 | MEDIUM |
| SVC-PHOT-010 | photographie | SRC-CQQ-001 | SRC-HGQ-001 | MEDIUM |
| SVC-VIDE-011 | video_service | SRC-CQQ-001 | SRC-HGQ-001 | MEDIUM |
| SVC-DRON-012 | drone_service | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| SVC-HOME-013 | home_staging | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| SVC-RENO-014 | renovation_service | SRC-CQQ-001, SRC-QIB-001 | SRC-HGQ-001 | MEDIUM |
| SVC-CONS-015 | construction_service | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| SVC-ENTR-016 | entretien | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| SVC-NETT-017 | nettoyage | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| SVC-SECU-018 | securisation | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| SVC-DEME-019 | demenagement | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| SVC-ASSU-020 | assurance_service | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| SVC-CONS-021 | conseil_juridique | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| SVC-CONS-022 | conseil_fiscal | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| SVC-GEST-023 | gestion_copropriete | SRC-QIB-001 | SRC-HGQ-001 | LOW |
| SVC-RECO-024 | recouvrement_locatif | SRC-QIB-001 | SRC-HGQ-001 | LOW |

---

## 4. Field → Source Mapping

### 4.1 Common Fields (Residential Search)

| Field ID | Label | Primary Source | Source Line(s) | Secondary Source(s) | Confidence |
|----------|-------|---------------|----------------|---------------------|------------|
| FLD-TRANSACTION | Transaction | SRC-CQQ-001 | General question bank | SRC-HGQ-001 §5 (step 1) | HIGH |
| FLD-INTENT | Intention | SRC-CQQ-001 | Intent detection section | SRC-SKU-007, SRC-HGQ-001 §1.2 | HIGH |
| FLD-PROPERTY_TYPE | Type de bien | SRC-MFR-001 | Required fields section | SRC-MFP-001, SRC-HGP-001 | HIGH |
| FLD-CITY | Ville | SRC-MFR-001 | Required fields section | SRC-CQQ-001 (step 3), SRC-HGQ-001 §5 (step 3) | HIGH |
| FLD-NEIGHBORHOOD | Quartier | SRC-MFR-001 | Recommended fields | SRC-CQQ-001 (step 4), SRC-HGQ-001 §5 (step 4) | HIGH |
| FLD-ZONE | Zone | SRC-MFP-001 | Land-specific fields | SRC-HGP-001 §3.2 | MEDIUM |
| FLD-BUDGET_MAX | Budget maximum | SRC-MFR-001 | Required fields section | SRC-CQQ-001 (step 5), SRC-HGQ-001 §5 (step 5) | HIGH |
| FLD-BUDGET_TYPE | Type de budget | SRC-CQQ-001 | Budget question variations | SRC-HGQ-001 §6.2 | HIGH |
| FLD-BUDGET_MENSUEL | Budget mensuel | SRC-MFR-001 | Tenant fields | SRC-HGQ-001 §6.2 | HIGH |
| FLD-DISPONIBILITE | Disponibilité | SRC-CQQ-001 | Timeline questions | SRC-HGQ-001 §5 (step 6) | HIGH |
| FLD-DELAI | Délai | SRC-CQQ-001 | Timeline questions | SRC-HGQ-001 §5 (step 6) | HIGH |
| FLD-NOM | Nom | SRC-CQQ-001 | Contact information | SRC-18Q-001, SRC-HGQ-001 §11.1 | HIGH |
| FLD-TELEPHONE | Téléphone | SRC-CQQ-001 | Contact information | SRC-18Q-001, SRC-HGQ-001 §11.1 | HIGH |
| FLD-CANAL_PREFERE | Canal préféré | SRC-WTD-001 | Channel adaptation | SRC-HGQ-001 §5 | HIGH |
| FLD-CHAMBRES | Chambres | SRC-CQQ-001 | Property criteria | SRC-MFR-001, SRC-SKU-001 | HIGH |
| FLD-DOUCHES | Douches | SRC-CQQ-001 | Property criteria | SRC-SKU-009 (Cameroon-specific) | HIGH |
| FLD-SALONS | Salons | SRC-CQQ-001 | Property criteria | SRC-SKU-009 (Cameroon-specific) | HIGH |
| FLD-SURFACE_MIN | Surface minimale | SRC-MFR-001 | Property criteria | SRC-PQR-001 | HIGH |
| FLD-SURFACE_MAX | Surface maximale | SRC-MFR-001 | Optional fields | SRC-PQR-001 | MEDIUM |
| FLD-MEUBLE | Meublé | SRC-CQQ-001 | Property criteria | SRC-MFR-001, SRC-SKU-001 | HIGH |
| FLD-ETAGE | Étage | SRC-CQQ-001 | Preference criteria | SRC-HGQ-001 §5 (step 8) | MEDIUM |
| FLD-PARKING | Parking | SRC-CQQ-001 | Optional criteria | SRC-SKU-001 (rent section) | MEDIUM |
| FLD-EXPOSITION | Exposition | SRC-CQQ-001 | Preference criteria | SRC-HGQ-001 §5 (step 8) | LOW |
| FLD-CLIMATISATION | Climatisation | SRC-CQQ-001 | Optional criteria | SRC-SKU-009 | MEDIUM |
| FLD-SECURITE | Sécurité | SRC-CQQ-001 | Optional criteria | SRC-SKU-009 | MEDIUM |
| FLD-CUISINE | Cuisine | SRC-CQQ-001 | Property criteria | SRC-SKU-009 | MEDIUM |
| FLD-CAUTION | Caution | SRC-CQQ-001 | Transaction fields | SRC-HGQ-001 §6.2 | MEDIUM |
| FLD-CHARGES | Charges | SRC-CQQ-001 | Transaction fields | SRC-SKU-001 (rent section) | MEDIUM |
| FLD-FINANCING | Financement | SRC-CQQ-001 | Transaction fields | SRC-HGQ-001 §6.1 | MEDIUM |
| FLD-EMAIL | Email | SRC-CQQ-001 | Contact information | SRC-18Q-001 | MEDIUM |
| FLD-PHOTOS | Photos | SRC-MFP-001 | Seller fields | SRC-HGQ-001 §6.3 | MEDIUM |
| FLD-DESCRIPTION | Description | SRC-MFP-001 | Seller fields | SRC-HGQ-001 §6.3 | MEDIUM |
| FLD-DOCUMENTS | Documents | SRC-MFP-001 | Property documents | SRC-HGP-001, SRC-SKU-002 | HIGH |
| FLD-TITRE_FONCIER | Titre foncier | SRC-MFP-001 | Land/Property fields | SRC-PQR-001, SRC-ANS-003 | HIGH |
| FLD-PRIX_DEMANDE | Prix demandé | SRC-MFP-001 | Seller fields | SRC-HGQ-001 §6.3 | HIGH |

### 4.2 Land-Specific Fields

| Field ID | Label | Primary Source | Source Line(s) | Secondary Source(s) | Confidence |
|----------|-------|---------------|----------------|---------------------|------------|
| FLD-SURFACE_TERRAIN | Surface terrain | SRC-MFP-001 | Land fields | SRC-PQR-001, SRC-HGP-001 §4 | HIGH |
| FLD-TYPE_TERRAIN | Type de terrain | SRC-MFP-001 | Land fields | SRC-PQR-001, SRC-03P-001 | HIGH |
| FLD-LOTI | Loti / Non loti | SRC-MFP-001 | Land fields | SRC-PQR-001, SRC-SKU-001 (land section) | HIGH |
| FLD-TITRE | Titre foncier | SRC-MFP-001 | Land fields | SRC-PQR-001, SRC-ANS-003 | HIGH |
| FLD-TYPE_TITRE | Type de titre | SRC-MFP-001 | Land fields | SRC-ANS-003 (property_matching_v1) | MEDIUM |
| FLD-TITRE_COLLECTIF | Titre collectif | SRC-MFP-001 | Land fields | SRC-HGP-001 §4.1 | MEDIUM |
| FLD-TITRE_INDIVIDUEL | Titre individuel | SRC-MFP-001 | Land fields | SRC-HGP-001 §4.1 | MEDIUM |
| FLD-ACCES_ROUTE | Accès route | SRC-CQQ-001 | Land criteria | SRC-SKU-001 (land section) | MEDIUM |
| FLD-DISTANCE_ROUTE | Distance route | SRC-CQQ-001 | Land criteria | SRC-SKU-001 (land section) | LOW |
| FLD-USAGE_TERRAIN | Usage terrain | SRC-CQQ-001 | Land criteria | SRC-HGQ-001 §6 | MEDIUM |
| FLD-MORCELLEMENT | Morcellement | SRC-QIB-001 | Land subdivision | SRC-HGP-001 §4.2 | LOW |
| FLD-VIABILITE | Viabilité | SRC-CQQ-001 | Land criteria | SRC-SKU-001 (land section) | MEDIUM |
| FLD-ELECTRICITE | Électricité | SRC-CQQ-001 | Land criteria | SRC-SKU-009 | MEDIUM |
| FLD-EAU | Eau | SRC-CQQ-001 | Land criteria | SRC-SKU-009 | MEDIUM |
| FLD-PROXIMITE_COMMERCE | Proximité commerce | SRC-CQQ-001 | Optional land criteria | SRC-SKU-001 | LOW |

### 4.3 Commercial Common Fields

| Field ID | Label | Primary Source | Source Line(s) | Secondary Source(s) | Confidence |
|----------|-------|---------------|----------------|---------------------|------------|
| COM-COMMON-001 | activite_commerciale | SRC-CQQ-001 | Commercial criteria | SRC-03P-001 | HIGH |
| COM-COMMON-002 | type_commerce | SRC-PQR-001 | Commercial types | SRC-03P-001 | HIGH |
| COM-COMMON-003 | surface_min | SRC-MFR-001 | Required fields | SRC-PQR-001 | HIGH |
| COM-COMMON-004 | surface_max | SRC-MFR-001 | Optional fields | SRC-PQR-001 | MEDIUM |
| COM-COMMON-005 | ville | SRC-MFR-001 | Required fields | SRC-CQQ-001 | HIGH |
| COM-COMMON-006 | quartier | SRC-MFR-001 | Required/recommended | SRC-CQQ-001 | HIGH |
| COM-COMMON-007 | budget_max | SRC-MFR-001 | Required fields | SRC-CQQ-001 | HIGH |
| COM-COMMON-008 | budget_min | SRC-MFR-001 | Optional fields | SRC-CQQ-001 | MEDIUM |
| COM-COMMON-009 | visibilite_route | SRC-CQQ-001 | Commercial criteria | SRC-SKU-001 (commercial section) | MEDIUM |
| COM-COMMON-010 | parking | SRC-CQQ-001 | Commercial criteria | SRC-SKU-001 | MEDIUM |
| COM-COMMON-011 | etat_local | SRC-CQQ-001 | Commercial criteria | SRC-PQR-001 | MEDIUM |
| COM-COMMON-012 | charges_incluses | SRC-CQQ-001 | Financial criteria | SRC-SKU-001 (rent section) | MEDIUM |
| COM-COMMON-013 | caution | SRC-CQQ-001 | Financial criteria | SRC-HGQ-001 | MEDIUM |
| COM-COMMON-014 | duree_bail | SRC-CQQ-001 | Commercial criteria | SRC-18Q-001 | MEDIUM |
| COM-COMMON-015 | type_bail | SRC-03P-001 | Commercial property | SRC-PQR-001 | MEDIUM |
| COM-COMMON-016 | hauteur_sous_plafond | SRC-CQQ-001 | Commercial criteria | SRC-03P-001 | LOW |
| COM-COMMON-017 | acces_camion | SRC-CQQ-001 | Industrial criteria | SRC-03P-001 | LOW |
| COM-COMMON-018 | normes_securite | SRC-QIB-001 | Commercial criteria | SRC-HGQ-001 | LOW |
| COM-COMMON-019 | rendement_attendu | SRC-SKU-003 | Investment criteria | SRC-HGQ-001 §6.4 | MEDIUM |
| COM-COMMON-020 | horizon_investissement | SRC-SKU-003 | Investment criteria | SRC-HGQ-001 §6.4 | MEDIUM |
| COM-COMMON-021 | type_investissement | SRC-SKU-003 | Investment types | SRC-HGQ-001 §6.4 | MEDIUM |
| COM-COMMON-022 | exposition | SRC-CQQ-001 | Commercial criteria | SRC-SKU-009 | LOW |
| COM-COMMON-023 | nombre_pieces | SRC-CQQ-001 | Property criteria | SRC-MFR-001 | HIGH |
| COM-COMMON-024 | mezzanine | SRC-03P-001 | Commercial criteria | SRC-PQR-001 | LOW |
| COM-COMMON-025 | climatisation | SRC-CQQ-001 | Comfort criteria | SRC-SKU-009 | MEDIUM |
| COM-COMMON-026 | groupe_electrogen | SRC-CQQ-001 | Service criteria | SRC-SKU-009 | LOW |
| COM-COMMON-027 | ascenseur | SRC-CQQ-001 | Building criteria | SRC-SKU-009 | LOW |
| COM-COMMON-028 | gardiennage | SRC-QIB-001 | Service criteria | SRC-HGQ-001 | LOW |
| COM-COMMON-029 | nb_station_service | SRC-03P-001 | Specific commercial | EXPERT_PROPOSAL | LOW |
| COM-COMMON-030 | cuivre_disponible | SRC-03P-001 | Industrial criteria | EXPERT_PROPOSAL | LOW |
| COM-COMMON-031 | nb_salles | SRC-CQQ-001 | Restaurant/bar criteria | SRC-03P-001 | LOW |
| COM-COMMON-032 | licence_alcool | SRC-03P-001 | Bar criteria | EXPERT_PROPOSAL | LOW |
| COM-COMMON-033 | terrasse | SRC-CQQ-001 | Commercial criteria | SRC-03P-001 | LOW |
| COM-COMMON-034 | transaction | SRC-MFR-001 | Required field | SRC-CQQ-001 | HIGH |
| COM-COMMON-035 | disponibilite | SRC-CQQ-001 | Timeline criteria | SRC-HGQ-001 §5 (step 6) | HIGH |
| COM-COMMON-036 | delai | SRC-CQQ-001 | Timeline criteria | SRC-HGQ-001 §5 (step 6) | HIGH |

### 4.4 Financing Common Fields

| Field ID | Label | Primary Source | Source Line(s) | Secondary Source(s) | Confidence |
|----------|-------|---------------|----------------|---------------------|------------|
| FIN-COMMON-001 | type_financement | SRC-CQQ-001 | Financing questions | SRC-18Q-001 | HIGH |
| FIN-COMMON-002 | montant_recherche | SRC-CQQ-001 | Financing questions | SRC-QIB-001 | HIGH |
| FIN-COMMON-003 | apport_personnel | SRC-CQQ-001 | Financing questions | SRC-HGQ-001 | HIGH |
| FIN-COMMON-004 | apport_disponible | SRC-CQQ-001 | Financing questions | SRC-QIB-001 | HIGH |
| FIN-COMMON-005 | duree_remboursement | SRC-CQQ-001 | Financing questions | SRC-18Q-001 | MEDIUM |
| FIN-COMMON-006 | mensualite_souhaitee | SRC-CQQ-001 | Financing questions | SRC-QIB-001 | MEDIUM |
| FIN-COMMON-007 | situation_professionnelle | SRC-CQQ-001 | Financing questions | SRC-PQR-001 | MEDIUM |
| FIN-COMMON-008 | type_bien_projet | SRC-CQQ-001 | Financing questions | SRC-HGP-001 | HIGH |
| FIN-COMMON-009 | revenus_mensuels | SRC-CQQ-001 | Financing questions | SRC-PQR-001 | MEDIUM |
| FIN-COMMON-010 | charges_existantes | SRC-CQQ-001 | Financing questions | SRC-QIB-001 | LOW |
| FIN-COMMON-011 | historique_bancaire | SRC-CQQ-001 | Financing questions | SRC-QIB-001 | LOW |
| FIN-COMMON-012 | taux_accepte | SRC-QIB-001 | Financing criteria | EXPERT_PROPOSAL | LOW |
| FIN-COMMON-013 | garantie_disponible | SRC-CQQ-001 | Financing questions | SRC-PQR-001 | MEDIUM |
| FIN-COMMON-014 | objet_financement | SRC-CQQ-001 | Financing questions | SRC-18Q-001 | HIGH |
| FIN-COMMON-015 | zone_projet | SRC-CQQ-001 | Financing questions | SRC-HGQ-001 | HIGH |
| FIN-COMMON-016 | statut_occupation | SRC-CQQ-001 | Financing questions | SRC-HGQ-001 §6.1 | MEDIUM |
| FIN-COMMON-017 | type_bien_existant | SRC-CQQ-001 | Financing questions | SRC-HGP-001 | HIGH |
| FIN-COMMON-018 | valeur_bien | SRC-CQQ-001 | Financing questions | SRC-PQR-001 | MEDIUM |
| FIN-COMMON-019 | estimation_besoin | SRC-CQQ-001 | Financing questions | SRC-18Q-001 | MEDIUM |
| FIN-COMMON-020 | delai_financement | SRC-CQQ-001 | Financing questions | SRC-QIB-001 | MEDIUM |
| FIN-COMMON-021 | finalite_projet | SRC-CQQ-001 | Financing questions | SRC-HGQ-001 | MEDIUM |
| FIN-COMMON-022 | ville_projet | SRC-CQQ-001 | Financing questions | SRC-HGQ-001 §5 (step 3) | HIGH |
| FIN-COMMON-023 | documents_disponibles | SRC-CQQ-001 | Financing questions | SRC-PQR-001 | HIGH |
| FIN-COMMON-024 | sources_remboursement | SRC-QIB-001 | Financing criteria | EXPERT_PROPOSAL | LOW |
| FIN-COMMON-025 | plan_affaires | SRC-QIB-001 | Business financing | EXPERT_PROPOSAL | LOW |

### 4.5 Professional Service Fields

| Field ID | Label | Primary Source | Source Line(s) | Secondary Source(s) | Confidence |
|----------|-------|---------------|----------------|---------------------|------------|
| PROF-CONTACT | Nom du professionnel | SRC-CQQ-001 | Professional search | SRC-18Q-001 | HIGH |
| PROF-IDENTITE | Identité professionnelle | SRC-CQQ-001 | Professional search | SRC-H00-004 | HIGH |
| PROF-SPECIALITE | Spécialité | SRC-CQQ-001 | Professional criteria | SRC-SKU-005 | HIGH |
| PROF-LOCALISATION | Localisation | SRC-CQQ-001 | Professional criteria | SRC-MFR-001 | HIGH |
| PROF-ZONE_INTERVENTION | Zone d'intervention | SRC-CQQ-001 | Professional criteria | SRC-SKU-005 | MEDIUM |
| PROF-TARIF | Tarif / Honoraires | SRC-CQQ-001 | Professional criteria | SRC-18Q-001 | MEDIUM |
| PROF-DISPO | Disponibilité | SRC-CQQ-001 | Professional criteria | SRC-WTD-001 | MEDIUM |
| PROF-REFERENCE | Référence | SRC-CQQ-001 | Professional criteria | SRC-PQR-001 | MEDIUM |
| PROF-ANNEE_EXP | Années d'expérience | SRC-CQQ-001 | Professional criteria | SRC-QIB-001 | LOW |
| PROF-CERTIFICATION | Certification | SRC-CQQ-001 | Professional criteria | SRC-18Q-001 | MEDIUM |
| PROF-LANGUE | Langue | SRC-CQQ-001 | Professional criteria | SRC-H00-005 | LOW |
| PROF-URGENCE | Niveau d'urgence | SRC-CQQ-001 | Professional criteria | SRC-HGQ-001 §2.1 | MEDIUM |

---

## 5. Rule → Source Mapping

### 5.1 Progressive Qualification Rules

| Rule ID | Rule Description | Source ID | Source Location | Confidence |
|---------|-----------------|-----------|-----------------|------------|
| QUAL-RULE-001 | Qualification order: Intention → Type → Ville → Quartier → Budget → Délai → Critères → Préférences → Confirmation → Escalade | SRC-HGQ-001 | §5 (10 steps) | HIGH |
| QUAL-RULE-002 | One question per message on WhatsApp | SRC-HGQ-001 | §8.1 | HIGH |
| QUAL-RULE-003 | 2-3 fields per message on Telegram | SRC-HGQ-001 | §8.1 | HIGH |
| QUAL-RULE-004 | Never re-ask a field already collected | SRC-HGQ-001 | §8.1 | HIGH |
| QUAL-RULE-005 | User correction overrides previous value | SRC-HGQ-001 | §8.1 | HIGH |
| QUAL-RULE-006 | Never restart qualification from beginning | SRC-HGQ-001 | §8.1 | HIGH |
| QUAL-RULE-007 | Stop if city not covered | SRC-HGQ-001 | §8.2 | HIGH |
| QUAL-RULE-008 | Stop if inventory empty for criteria | SRC-HGQ-001 | §8.2 | HIGH |
| QUAL-RULE-009 | Escalate immediately if user asks for human | SRC-HGQ-001 | §8.2, §10 | HIGH |
| QUAL-RULE-010 | Stop after 3 exchanges without progress | SRC-HGQ-001 | §8.2 | HIGH |
| QUAL-RULE-011 | Partial context reset if user changes intent | SRC-HGQ-001 | §8.2 | HIGH |
| QUAL-RULE-012 | Budget is blocking — no matching without budget | SRC-HGQ-001 | §2.2, §6 | HIGH |
| QUAL-RULE-013 | Never ask for `standing` explicitly — deduce from price/neighborhood/photos | SRC-SKU-009 | Cameroon-specific attributes | HIGH |
| QUAL-RULE-014 | Never use `nombre de pièces` — use `chambres` | SRC-SKU-009 | Cameroon-specific attributes | HIGH |
| QUAL-RULE-015 | Never propose a different city when requested is uncovered | SRC-SKU-009 | Forbidden rules | HIGH |
| QUAL-RULE-016 | Never pressure for budget on greetings only (History Gate) | SRC-SKU-009 | Forbidden rules | HIGH |
| QUAL-RULE-017 | Match early — launch search as soon as MINIMUM_SEARCH_READY achieved | SRC-HGQ-001 | §5 (cardinal rule) | HIGH |
| QUAL-RULE-018 | Deduce, don't ask — never ask what can be derived | SRC-HGQ-001 | §8.1 | HIGH |

### 5.2 Lead Scoring Rules

| Rule ID | Rule Description | Source ID | Source Location | Confidence |
|---------|-----------------|-----------|-----------------|------------|
| SCORE-RULE-001 | Base score for tenant: 40 | SRC-HGQ-001 | §1.1, SRC-ANS-001 | HIGH |
| SCORE-RULE-002 | Base score for buyer: 60 | SRC-HGQ-001 | §1.1, SRC-ANS-001 | HIGH |
| SCORE-RULE-003 | Base score for seller: 50 | SRC-HGQ-001 | §1.1, SRC-ANS-001 | HIGH |
| SCORE-RULE-004 | Base score for investor: 80 | SRC-HGQ-001 | §1.1, SRC-ANS-001 | HIGH |
| SCORE-RULE-005 | Base score for diaspora_investor: 95 | SRC-HGQ-001 | §1.1, SRC-ANS-001 | HIGH |
| SCORE-RULE-006 | budget_detected booster: +15 | SRC-HGQ-001 | §2.1, SRC-ANS-001 | HIGH |
| SCORE-RULE-007 | city_detected booster: +10 | SRC-HGQ-001 | §2.1, SRC-ANS-001 | HIGH |
| SCORE-RULE-008 | neighborhood_detected booster: +10 | SRC-HGQ-001 | §2.1, SRC-ANS-001 | HIGH |
| SCORE-RULE-009 | urgent_request booster: +20 | SRC-HGQ-001 | §2.1, SRC-ANS-001 | HIGH |
| SCORE-RULE-010 | diaspora_detected booster: +25 | SRC-HGQ-001 | §2.1, SRC-ANS-001 | HIGH |
| SCORE-RULE-011 | cash_purchase booster: +15 | SRC-HGQ-001 | §2.1, SRC-ANS-001 | HIGH |
| SCORE-RULE-012 | missing_budget penalty: -10 | SRC-HGQ-001 | §2.2, SRC-ANS-001 | HIGH |
| SCORE-RULE-013 | unclear_location penalty: -10 | SRC-HGQ-001 | §2.2, SRC-ANS-001 | HIGH |
| SCORE-RULE-014 | spam_like_message penalty: -50 | SRC-HGQ-001 | §2.2, SRC-ANS-001 | HIGH |
| SCORE-RULE-015 | HOT threshold V1: >= 80 | SRC-HGQ-001 | §2.3, SRC-ANS-001 | HIGH |
| SCORE-RULE-016 | WARM threshold V1: >= 60 | SRC-HGQ-001 | §2.3, SRC-ANS-001 | HIGH |
| SCORE-RULE-017 | COLD threshold V1: >= 40 | SRC-HGQ-001 | §2.3, SRC-ANS-001 | HIGH |
| SCORE-RULE-018 | LOW threshold V1: < 40 | SRC-HGQ-001 | §2.3, SRC-ANS-001 | HIGH |
| SCORE-RULE-019 | HOT threshold V5: >= 0.8 | SRC-HGQ-001 | §2.3, SRC-ANS-002 | HIGH |
| SCORE-RULE-020 | WARM threshold V5: >= 0.5 | SRC-HGQ-001 | §2.3, SRC-ANS-002 | HIGH |
| SCORE-RULE-021 | COLD threshold V5: >= 0.3 | SRC-HGQ-001 | §2.3, SRC-ANS-002 | HIGH |
| SCORE-RULE-022 | SPAM threshold V5: <= 0.2 | SRC-HGQ-001 | §2.3, SRC-ANS-002 | HIGH |
| SCORE-RULE-023 | Base_interest CRM weight: 0.15 | SRC-HGQ-001 | §4.1, SRC-ANS-002 | HIGH |
| SCORE-RULE-024 | Property_type_match CRM weight: 0.20 | SRC-HGQ-001 | §4.1, SRC-ANS-002 | HIGH |
| SCORE-RULE-025 | Location_precision CRM weight: 0.20 | SRC-HGQ-001 | §4.1, SRC-ANS-002 | HIGH |
| SCORE-RULE-026 | Budget_presence CRM weight: 0.10 | SRC-HGQ-001 | §4.1, SRC-ANS-002 | HIGH |
| SCORE-RULE-027 | Urgency_signal CRM weight: 0.15 | SRC-HGQ-001 | §4.1, SRC-ANS-002 | HIGH |
| SCORE-RULE-028 | Visit_intent CRM weight: 0.20 | SRC-HGQ-001 | §4.1, SRC-ANS-002 | HIGH |
| SCORE-RULE-029 | Trust_signal CRM weight: 0.10 | SRC-HGQ-001 | §4.1, SRC-ANS-002 | HIGH |

### 5.3 V5 Pipeline Rules

| Rule ID | Rule Description | Source ID | Source Location | Confidence |
|---------|-----------------|-----------|-----------------|------------|
| PIPE-RULE-001 | Step 1: normalize_text | SRC-HGQ-001 | §3, SRC-ANS-002 | HIGH |
| PIPE-RULE-002 | Step 2: extract_entities | SRC-HGQ-001 | §3, SRC-ANS-002 | HIGH |
| PIPE-RULE-003 | Step 3: detect_intent | SRC-HGQ-001 | §3, SRC-ANS-002 | HIGH |
| PIPE-RULE-004 | Step 4: context_enrichment (memory/preferences) | SRC-HGQ-001 | §3, SRC-ANS-002 | HIGH |
| PIPE-RULE-005 | Step 5: lead_scoring | SRC-HGQ-001 | §3, SRC-ANS-002 | HIGH |
| PIPE-RULE-006 | Step 6: lead_classification (HOT/WARM/COLD/SPAM) | SRC-HGQ-001 | §3, SRC-ANS-002 | HIGH |
| PIPE-RULE-007 | Step 7: crm_routing | SRC-HGQ-001 | §3, SRC-ANS-002 | HIGH |
| PIPE-RULE-008 | Step 8: response | SRC-HGQ-001 | §3, SRC-ANS-002 | HIGH |

### 5.4 Anti-Fraud Rules

| Rule ID | Rule Description | Source ID | Source Location | Confidence |
|---------|-----------------|-----------|-----------------|------------|
| FRAUD-RULE-001 | broker_spam detection: -50 penalty, manual flag | SRC-HGQ-001 | §9, SRC-ANS-002 | HIGH |
| FRAUD-RULE-002 | duplicate_listing detection: dedup, warning | SRC-HGQ-001 | §9, SRC-ANS-002 | HIGH |
| FRAUD-RULE-003 | fake_price detection: flag for manual verification | SRC-HGQ-001 | §9, SRC-ANS-002 | HIGH |
| FRAUD-RULE-004 | suspicious_urgency: reduce urgency_signal weight | SRC-HGQ-001 | §9, SRC-ANS-002 | HIGH |

### 5.5 Channel-Specific Rules

| Rule ID | Rule Description | Source ID | Source Location | Confidence |
|---------|-----------------|-----------|-----------------|------------|
| CHAN-RULE-001 | Qualification order on dashboard: complete form | SRC-WTD-001 | Dashboard qualification section | HIGH |
| CHAN-RULE-002 | WhatsApp pace: 1 question per message | SRC-WTD-001 | WhatsApp qualification section | HIGH |
| CHAN-RULE-003 | WhatsApp format: minimal, mobile-first | SRC-WTD-001 | WhatsApp qualification section | HIGH |
| CHAN-RULE-004 | Telegram pace: 2-3 fields per message | SRC-WTD-001 | Telegram qualification section | HIGH |
| CHAN-RULE-005 | Telegram format: structured with lists | SRC-WTD-001 | Telegram qualification section | HIGH |
| CHAN-RULE-006 | Dashboard: full form, complete and actionable | SRC-WTD-001 | Dashboard qualification section | HIGH |

### 5.6 Matching Rules

| Rule ID | Rule Description | Source ID | Source Location | Confidence |
|---------|-----------------|-----------|-----------------|------------|
| MATCH-RULE-001 | hard_constraint: must match exactly, otherwise excluded | SRC-HGM-001 | Matching role semantics | HIGH |
| MATCH-RULE-002 | soft_constraint: preference but flexible, penalized if not matched | SRC-HGM-001 | Matching role semantics | HIGH |
| MATCH-RULE-003 | ranking_preference: used to rank results only | SRC-HGM-001 | Matching role semantics | HIGH |
| MATCH-RULE-004 | exclusion: properties matching this are excluded | SRC-HGM-001 | Matching role semantics | HIGH |
| MATCH-RULE-005 | boost: score boost if matched (+10 to +25) | SRC-HGM-001 | Matching role semantics | HIGH |
| MATCH-RULE-006 | penalty: score penalty if not matched | SRC-HGM-001 | Matching role semantics | HIGH |
| MATCH-RULE-007 | informational_only: for display, does not affect score | SRC-HGM-001 | Matching role semantics | HIGH |
| MATCH-RULE-008 | verification_only: for transaction readiness only | SRC-HGM-001 | Matching role semantics | HIGH |
| MATCH-RULE-009 | transaction_blocker: must be resolved before transaction | SRC-HGM-001 | Matching role semantics | HIGH |

### 5.7 Escalation Rules

| Rule ID | Rule Description | Source ID | Source Location | Confidence |
|---------|-----------------|-----------|-----------------|------------|
| ESC-RULE-001 | Sale: HOT lead + confirmed budget + visit intent → Agent commercial | SRC-HGQ-001 | §10 | HIGH |
| ESC-RULE-002 | Legal: legal question, dispute, complaint → Support / Notaire | SRC-HGQ-001 | §10 | HIGH |
| ESC-RULE-003 | Human: explicit request or 3 failed qualification attempts → Conseiller | SRC-HGQ-001 | §10 | HIGH |
| ESC-RULE-004 | "Je veux parler à quelqu'un" → human escalation | SRC-SKU-009 | Human escalation triggers | HIGH |
| ESC-RULE-005 | "Je veux négocier" → human escalation | SRC-SKU-009 | Human escalation triggers | HIGH |
| ESC-RULE-006 | "Le titre n'est pas clair" → human escalation | SRC-SKU-009 | Human escalation triggers | HIGH |
| ESC-RULE-007 | "Le terrain n'est pas loti" → human escalation | SRC-SKU-009 | Human escalation triggers | HIGH |
| ESC-RULE-008 | "Il y a plusieurs propriétaires" → human escalation | SRC-SKU-009 | Human escalation triggers | HIGH |
| ESC-RULE-009 | "Il faut une décision rapide" → human escalation | SRC-SKU-009 | Human escalation triggers | HIGH |
| ESC-RULE-010 | Repeated fraud signals → human escalation | SRC-SKU-009 | Human escalation triggers | HIGH |

### 5.8 Field Matching Role Assignments

| Field ID | Matching Role | Source ID | Source Location | Confidence |
|----------|--------------|-----------|-----------------|------------|
| FLD-TRANSACTION | hard_constraint | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-PROPERTY_TYPE | hard_constraint | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-CITY | hard_constraint | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-NEIGHBORHOOD | soft_constraint | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-ZONE | soft_constraint | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-BUDGET_MAX | soft_constraint | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-BUDGET_TYPE | informational_only | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-DISPONIBILITE | soft_constraint | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-CHAMBRES | soft_constraint | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-DOUCHES | ranking_preference | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-SALONS | ranking_preference | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-SURFACE_MIN | soft_constraint | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-MEUBLE | ranking_preference | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-ETAGE | ranking_preference | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-PARKING | boost (+10 per parking) | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-CLIMATISATION | boost (+5) | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-SECURITE | boost (+5) | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-CUISINE | ranking_preference | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-NOM | informational_only | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-TELEPHONE | verification_only | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-CANAL_PREFERE | informational_only | SRC-HGM-001 | Matching semantics | HIGH |
| FLD-CAUTION | transaction_blocker | SRC-HGM-001 | Matching semantics | MEDIUM |
| FLD-CHARGES | informational_only | SRC-HGM-001 | Matching semantics | MEDIUM |

---

## 6. Gaps and Conflicts

### 6.1 Resolved Conflicts

| Conflict ID | Description | Sources Involved | Resolution | Resolution Source |
|-------------|-------------|------------------|------------|-------------------|
| CONF-001 | Matching threshold: 25% (Ch92) vs 60% (Ch26) | SRC-ANS-003, SRC-HGR-001 | Double threshold: 60% for proposal, 25% for absolute rejection | SRC-HGO-001 §C-004 |
| CONF-002 | Memory retention: 90 days vs 365 days | CONVERSATION_MODEL.md vs long_term_memory.py | 365 days is real value (code confirmed) | SRC-HGO-001 §C-005 |
| CONF-003 | Buyer fears: 12 vs 10 | CONVERSATION_MODEL.md vs trust-and-objection-patterns.md | 10 fears confirmed from source | SRC-HGO-001 §C-006 |
| CONF-004 | Camfranglais as 4th language | CONVERSATION_MODEL.md vs RESPONSE_POLICY.md | FR/EN/PID only; camfranglais is expressions only | SRC-HGO-001 §C-007 |
| CONF-005 | Qualification step count: 8 (V5 pipeline) vs 10 (qualification order) | SRC-ANS-002 vs SRC-HGQ-001 | These describe different processes: pipeline vs conversation order | SRC-HGQ-001 §3 vs §5 |
| CONF-006 | Score thresholds: integer V1 vs normalized V5 | SRC-ANS-001 vs SRC-ANS-002 | Both valid; V1 for legacy, V5 for current implementation | SRC-HGQ-001 §2.3 |
| CONF-007 | Diaspora indicators inconsistent across sources | SRC-HGQ-001 §12 vs SRC-SKU-006 | Diaspora_filter.py and scoring_rules.json define the authoritative list | SRC-HGQ-001 §12.1 |
| CONF-008 | Budget as hard vs soft constraint | SRC-HGM-001 vs SRC-SKU-006 | Budget is a preference, not absolute (scoring_rules.json) | SRC-SKU-006 §scoring_rules |

### 6.2 Unresolved Conflicts

| Conflict ID | Description | Sources Involved | Impact | Priority |
|-------------|-------------|------------------|--------|----------|
| CONF-009 | City priority order: 4 contradictory orderings | cities.json, system_prompt_v1.md, city-affinity-matrix.md | Affects search result ordering | MEDIUM |
| CONF-010 | Affinity matrix has data for only 2 of 10 priority cities | city-affinity-matrix.md | 8 cities have no affinity pairs | LOW |
| CONF-011 | Insurance requirements for different property types not consistently documented | SRC-QIB-001 vs SRC-CQQ-001 | May affect financing matrices | MEDIUM |
| CONF-012 | Land title status taxonomy differs between sources | SRC-MFP-001 vs SRC-ANS-003 vs SRC-SKU-001 | Affects land search matrices | HIGH |

### 6.3 Known Gaps

| Gap ID | Description | Impact | Workaround |
|--------|-------------|--------|------------|
| GAP-001 | No heritage source for short-term rental matrices (chambre_hotel, appartement_courte_duree) | Residential matrices 14-16 are partially speculative | Extrapolated from general rental matrices + WTD-001 |
| GAP-002 | No heritage source for 5 investment matrices (COM-MATRIX-017 to 021) | Investment matrices are EXPERT_PROPOSAL | Documented as HUMAN_VALIDATION_REQUIRED |
| GAP-003 | No heritage source for 13 professional service matrices (PRO-EXPIM-015 to PRO-PREST-027) | These matrices need expert validation | Marked as EXPERT_PROPOSAL |
| GAP-004 | No heritage source for 10 real estate service matrices (SVC-CONS-015 to SVC-RECO-024) | Service matrices need expert validation | Marked as EXPERT_PROPOSAL |
| GAP-005 | No heritage source for 5 financing matrices (FIN-006 to FIN-010) | Financing matrices need expert validation | Marked as EXPERT_PROPOSAL |
| GAP-006 | Missing insurance requirements in financing matrices | May need notaire/banque input | HUMAN_VALIDATION_REQUIRED |
| GAP-007 | Missing Cameroon-specific legal procedures for land transfer | Land matrices may be incomplete | HUMAN_VALIDATION_REQUIRED |
| GAP-008 | No heritage source for drone photography service matrix | SVC-DRON-012 is entirely EXPERT_PROPOSAL | Marked as HUMAN_VALIDATION_REQUIRED |

---

## 7. External Sources

No external (non-LAWIM) sources were consulted in the creation of these qualification matrices. All data originates from:

1. **LAWIM backup branch** (pre-repository-cleanup-20260711-100549) — 8 source documents
2. **LAWIM knowledge_unified/** — 11 JSON/MD files
3. **LAWIM code** — Python modules
4. **LAWIM Heritage Gold** — 9 processed reference docs
5. **LAWIM Heritage H0** — 5 heritage documents
6. **Ancienne structure (documented via SOURCE_INVENTORY)** — 4 JSON/Python files (deleted)

For a complete accounting of external sources consulted during the broader Heritage Gold mission (non-matrix-specific), see `EXTERNAL_COMPLEMENTS.md`.

---

## 8. Traceability Summary Statistics

| Metric | Count |
|--------|-------|
| Total source documents catalogued | 37 |
| Backup sources | 8 |
| Heritage Gold sources | 9 |
| Knowledge Unified sources | 11 |
| Code sources | 6 |
| Ancienne structure sources | 4 |
| Heritage H0 sources | 5 |
| Total matrices traced | 107 |
| Total fields traced | 100+ |
| Total business rules traced | 80+ |
| Conflicts resolved | 8 |
| Conflicts unresolved | 4 |
| Known gaps | 8 |
| HIGH confidence entries | 75% |
| MEDIUM confidence entries | 18% |
| LOW confidence entries | 7% |

---

**End of SOURCE_TRACEABILITY.md** — For corrections or updates, refer to the source documents listed in §2 or open an issue in the LAWIM documentation repository.
