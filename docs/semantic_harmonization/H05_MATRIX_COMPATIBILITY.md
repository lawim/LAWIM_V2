# H05 — MATRIX COMPATIBILITY: Qualification Matrices × Current LAWIM V2 Model

**Document ID:** LAWIM-H05-MATRIX-COMPATIBILITY-V1
**Status:** CANONICAL — Crosswalk between 107 heritage qualification matrices and current code model
**Date:** 2026-07-15
**Prerequisites:** MATRIX_CATALOG.md, QUALIFICATION_MATRIX_CONTRACT.md, MATCHING_EXECUTION_ARCHITECTURE.md

---

## Executive Summary

The LAWIM Heritage Gold qualification matrices define **107 canonical matrices** across 7 request families, specifying **700+ field-level requirements** organized across 6 readiness levels (intake → transaction). The current LAWIM V2 codebase contains **zero direct implementation** of these matrices.

| Metric | Value |
|--------|-------|
| Total matrices in catalog | 107 |
| Matrices with direct code implementation | **0 (0%)** |
| Matrices with H1 architecture contract mapping | 107 (100%) |
| Matrices requiring extension for H2 implementation | **107 (100%)** |
| Current model fields usable without extension | 9 (project + property fields) |
| Matrix-specific fields with no model equivalent | 690+ (→ `metadata_json`) |
| Matching roles defined in matrices | 9 |
| Matching roles implemented in code | **0** |
| INTENT_FAMILY × PROPERTY_SERVICE_TYPE combinations | 107 (1:1 per matrix) |
| Combinations mappable to current project_domain types | ~7 (buy, rent, sell, invest, build, other) |

**Core finding:** The matrices are a complete, validated specification for the qualification engine defined in H1 contracts (QUALIFICATION_EXECUTION_ARCHITECTURE.md, QUALIFICATION_MATRIX_CONTRACT.md, MATCHING_EXECUTION_ARCHITECTURE.md). The current code implements the project/CRUD skeleton but not the qualification engine. All 107 matrices require H2 implementation as extensions.

---

## Matrix Family Overview Table

| # | Family | File | Matrices | Transaction Types | Current Code Support | Extensions Required |
|---|--------|------|----------|-------------------|---------------------|---------------------|
| 1 | RESIDENTIAL_SEARCH | `residential_search_matrices.md` | 18 | RENT, BUY | project_domain (generic) | 18/18 |
| 2 | LAND_SEARCH | `land_search_matrices.md` | 7 | BUY | project_domain (generic) | 7/7 |
| 3 | COMMERCIAL_SEARCH | `commercial_property_matrices.md` | 16 | RENT, BUY, CESSION_BAIL | project_domain (generic) | 16/16 |
| 4 | COMMERCIAL_SEARCH (INVEST) | `commercial_property_matrices.md` | 5 | INVEST | project_domain (invest) | 5/5 |
| 5 | FINANCING_REQUEST | `financing_request_matrices.md` | 10 | FINANCE | project_domain (generic) | 10/10 |
| 6 | PROFESSIONAL_SEARCH | `professional_service_matrices.md` | 27 | FIND | project_domain (generic) | 27/27 |
| 7 | REAL_ESTATE_SERVICES | `real_estate_service_matrices.md` | 24 | SERVICE | project_domain (generic) | 24/24 |

---

## Per-Family Compatibility Analysis

### 1. RESIDENTIAL_SEARCH (18 matrices)

**Matrix IDs:** MATRIX-RES-SEARCH-001 through MATRIX-RES-SEARCH-018
**Current model mapping:** `project_domain.py` — `project_type: "rent"` or `"buy"`
**Fields in current model:** title, objective, budget_min, budget_max, currency, location_city, location_region, timeline_horizon, metadata_json
**Fields in matrices:** 70+ unique field IDs (FLD-TRANSACTION, FLD-PROPERTY_TYPE, FLD-CITY, FLD-NEIGHBORHOOD, FLD-BUDGET_MAX, FLD-CHAMBRES, FLD-DOUCHES, FLD-CUISINE, FLD-MEUBLE, FLD-SURFACE, FLD-ETAGE, FLD-PARKING, FLD-CLIMATISATION, etc.)
**Fields without model target:** 60+ (all amenity, preference, and matching fields) → `metadata_json`
**Matching roles used:** hard_constraint, soft_constraint, ranking_preference, boost, penalty, informational_only, verification_only, transaction_blocker
**Consumer engine:** Qualification Engine → Matching Engine (H1)

#### Common Readiness Level Structure (per matrix)

| Level | Fields per matrix | Current model coverage |
|-------|------------------|----------------------|
| minimum_intake | 3 (TRANSACTION, PROPERTY_TYPE, CITY) | Partial — project_type, location_city exist |
| minimum_search | 2 (NEIGHBORHOOD, BUDGET_MAX) | Partial — budget_max exists |
| minimum_matching | 2-5 (type-specific: DOUCHES, CUISINE, CHAMBRES) | None → metadata_json |
| minimum_introduction | 4-5 (NOM, TELEPHONE, CANAL_PREFERE, DISPONIBILITE) | None → metadata_json |
| minimum_visit | 1-3 (CLIMATISATION, EAU, ELECTRICITE) | None → metadata_json |
| minimum_transaction | 2 (CAUTION, CHARGES) | None → metadata_json |

### 2. LAND_SEARCH (7 matrices)

**Matrix IDs:** LAND_SEARCH_TERRAIN_TITRE_001 through LAND_SEARCH_TERRAIN_SOUS_MORCELLEMENT_001
**Current model mapping:** `project_domain.py` — `project_type: "buy"`
**Fields in matrices:** 50+ unique field IDs (ville, quartier, surface, budget_total, usage_prevu, titre_requis, type_document, num_titre, accessibilite, viabilisation_eau, topographie, inondable, litiges_connus, hypotheque, etc.)
**Fields without model target:** 45+ → `metadata_json`
**Key specificity:** Land has unique legal/document fields (titre foncier, bornage, certificat_urbanisme) with no current model equivalent
**Consumer engine:** Qualification Engine → Matching Engine, with legal verification sub-engine

### 3. COMMERCIAL_SEARCH (16 matrices)

**Matrix IDs:** COM-MATRIX-001 through COM-MATRIX-016
**Current model mapping:** `project_domain.py` — `project_type: "buy"` or `"rent"`
**Fields in matrices:** 45 common fields (COM-COMMON-001 through COM-COMMON-045) + per-matrix specific fields
**Fields without model target:** 40+ → `metadata_json`
**Key specificity:** activité_prévue (hard_constraint), surface_min (hard_constraint), licence_exploitation (hard_constraint), fonds_commerce, chiffre_affaires
**Consumer engine:** Qualification Engine → Matching Engine (commercial variant)

### 4. COMMERCIAL_SEARCH — INVEST (5 matrices)

**Matrix IDs:** COM-MATRIX-017 through COM-MATRIX-021
**Current model mapping:** `project_domain.py` — `project_type: "invest"`
**Fields in matrices:** 18 common investment fields (INV-COMMON-001 through INV-COMMON-018)
**Fields without model target:** 16+ → `metadata_json`
**Key specificity:** rendement_cible (hard_constraint), horizon_investissement, risque_accepté, stratégie_investissement, source_financement
**Consumer engine:** Qualification Engine → Matching Engine (investment variant)

### 5. FINANCING_REQUEST (10 matrices)

**Matrix IDs:** MATRIX-FIN-001 through MATRIX-FIN-010
**Current model mapping:** `project_domain.py` — `project_type: "buy"` (closest), no explicit FINANCE type
**Fields in matrices:** 80+ unique field IDs (FIN-COMMON-001 through FIN-COMMON-025, FIN-SAL-001 through FIN-SAL-008, FIN-SE-001 through FIN-SE-012, FIN-CONS-001 through FIN-CONS-020, FIN-DIA-001 through FIN-DIA-006)
**Fields without model target:** 75+ → `metadata_json`
**Key specificity:** Financial profile (revenus, garanties, capacité_remboursement), employment details, business financials, construction project details, diaspora-specific fields
**Consumer engine:** Qualification Engine → Financing Matching Engine (financing-specific)

### 6. PROFESSIONAL_SEARCH (27 matrices)

**Matrix IDs:** PRO-AGENT-001 through PRO-PREST-027
**Current model mapping:** `project_domain.py` — `project_type: "other"` (no FIND type)
**Fields in matrices:** 40+ base fields (type_prestation, localisation, description_besoin, urgence, budget_fourchette, date_souhaitee) + per-profession-specific fields
**Fields without model target:** 35+ → `metadata_json`
**Key specificity:** Service-oriented fields (type_prestation, urgence levels specific to services), per-profession qualification criteria
**Consumer engine:** Qualification Engine → Professional Matching Engine

### 7. REAL_ESTATE_SERVICES (24 matrices)

**Matrix IDs:** SVC-ESTI-001 through SVC-RECO-024
**Current model mapping:** `project_domain.py` — `project_type: "other"` (no SERVICE type)
**Fields in matrices:** 200+ unique fields across all service types (highest of any family)
**Fields without model target:** 190+ → `metadata_json`
**Key specificity:** Service-specific progression (service_ready → provider_matching_ready → quote_ready → execution_ready), document uploads, provider qualification
**Consumer engine:** Qualification Engine → Service Matching Engine

---

## Field-Level Compatibility: Common Fields × Current Model

The following table maps the most frequently used matrix fields to the current LAWIM V2 code model:

| Matrix Field ID | Matrix Label | Current Model Field | Model File | Compatible? | Notes |
|----------------|--------------|-------------------|------------|-------------|-------|
| FLD-TRANSACTION | Transaction | `project_type` | project_domain.py | PARTIAL | Matrix values: RENT/BUY; model: buy/rent/sell/invest/build/other. Missing FINANCE, FIND, SERVICE |
| FLD-PROPERTY_TYPE | Type de bien | `property_type` | property_domain.py | PARTIAL | Matrix has 18 residential + 7 land + 16 commercial types; model is free-text with no enum |
| FLD-CITY | Ville | `location_city` | project_domain.py | YES | Direct mapping |
| FLD-NEIGHBORHOOD | Quartier | (none) | — | NO | Not in project or property model |
| FLD-BUDGET_MAX | Budget maximum | `budget_max` | project_domain.py | YES | Direct mapping |
| FLD-BUDGET_MIN | Budget minimum | `budget_min` | project_domain.py | YES | Direct mapping |
| FLD-BUDGET_TYPE | Type de budget | (none) | — | NO | Budget type (MONTHLY_RENT vs TOTAL_PRICE) not modeled |
| FLD-BUDGET_CURRENCY | Devise | `currency` | project_domain.py | YES | Direct mapping |
| FLD-DISPONIBILITE | Disponibilité | (none) | — | NO | Availability date not in model |
| FLD-DELAI | Délai | `timeline_horizon` | project_domain.py | PARTIAL | Different enum values |
| FLD-URGENCE | Urgence | (none) | — | NO | Urgency not modeled |
| FLD-CHAMBRES | Chambres | `bedrooms` | property_domain.py | YES | In property model |
| FLD-DOUCHES | Douches | (none) | — | NO | Bathroom count (`bathrooms` exists in property model but maps to FLD-SALLES_BAIN, not douches) |
| FLD-SURFACE | Surface habitable | `area_sqm` | property_domain.py | YES | Direct mapping |
| FLD-NOM | Nom | (none) | — | NO | Contact name not in project model |
| FLD-TELEPHONE | Téléphone | (none) | — | NO | Phone not in project model |
| FLD-EMAIL | Email | (none) | — | NO | Email not in project model |
| FLD-CANAL_PREFERE | Canal préféré | (none) | — | NO | Communication channel not modeled |
| FLD-PARKING | Parking | (none) | — | NO | → metadata_json |
| FLD-CUISINE | Cuisine | (none) | — | NO | → metadata_json |
| FLD-MEUBLE | Meublé | (none) | — | NO | → metadata_json |
| FLD-CLIMATISATION | Climatisation | (none) | — | NO | → metadata_json |
| FLD-SECURITE | Sécurité | (none) | — | NO | → metadata_json |
| FLD-ETAGE | Étage | (none) | — | NO | → metadata_json |
| FLD-CAUTION | Caution | (none) | — | NO | → metadata_json |
| FLD-CHARGES | Charges | (none) | — | NO | → metadata_json |
| FLD-FINANCING | Financement | (none) | — | NO | → metadata_json |
| COM-COMMON-001 | activité_prévue | (none) | — | NO | → metadata_json |
| COM-COMMON-003 | surface_min | (none) | — | NO | → metadata_json |
| COM-COMMON-005 | ville | `location_city` | project_domain.py | YES | Direct mapping |
| COM-COMMON-034 | transaction | `project_type` | project_domain.py | PARTIAL | Different enum values |
| FIN-COMMON-002 | montant_recherche | `budget_max` | project_domain.py | PARTIAL | Financing-specific semantics |
| FIN-COMMON-004 | apport_disponible | (none) | — | NO | → metadata_json |
| FIN-COMMON-008 | type_bien_projet | `property_type` | property_domain.py | PARTIAL | Different taxonomy |
| FIN-COMMON-010 | profil_demandeur | (none) | — | NO | → metadata_json |
| FIN-COMMON-013 | revenus_mensuels | (none) | — | NO | → metadata_json |
| FIN-COMMON-018 | garanties_disponibles | (none) | — | NO | → metadata_json |

**Directly compatible fields:** 6 (FLD-CITY, FLD-BUDGET_MAX, FLD-BUDGET_MIN, FLD-BUDGET_CURRENCY, FLD-CHAMBRES/bedrooms, FLD-SURFACE/area_sqm)
**Partially compatible fields:** 4 (FLD-TRANSACTION/project_type, FLD-PROPERTY_TYPE/property_type, FLD-DELAI/timeline_horizon, FIN-COMMON-002/budget_max)
**Incompatible / absent fields:** 690+ (→ `metadata_json`)

---

## Matching Role Compatibility: Matrix Roles × H1 Matching Engine

The 9 matching roles defined in `MATCHING_FIELD_SEMANTICS.md` and used across all 107 matrices map to the H1 `MATCHING_EXECUTION_ARCHITECTURE.md`:

| Matrix Role | H1 Matching Engine Component | H1 Status | Current Code Status | Implementation Gap |
|-------------|------------------------------|-----------|-------------------|-------------------|
| `hard_constraint` | Constraint Enforcer (§0.2) | ARCHITECTURE_DEFINED | NOT_IMPLEMENTED | No constraint enforcement in current code |
| `soft_constraint` | Dimension Evaluator (§2.1) | ARCHITECTURE_DEFINED | NOT_IMPLEMENTED | No weighted scoring in current code |
| `ranking_preference` | Score Calculator (§2.2) | ARCHITECTURE_DEFINED | NOT_IMPLEMENTED | No ranking bonuses in current code |
| `boost` | Boost Applier (§2.4) | ARCHITECTURE_DEFINED | NOT_IMPLEMENTED | Boost rules defined, not coded |
| `penalty` | Penalty Applier (§2.5) | ARCHITECTURE_DEFINED | NOT_IMPLEMENTED | Penalty rules defined, not coded |
| `exclusion` | Exclusion Engine (§2.6) | ARCHITECTURE_DEFINED | NOT_IMPLEMENTED | Exclusion logic not implemented |
| `informational_only` | Explanation Builder (§2.8) | ARCHITECTURE_DEFINED | NOT_IMPLEMENTED | No explanation layer in code |
| `verification_only` | Audit / Transaction Engine | ARCHITECTURE_DEFINED | NOT_IMPLEMENTED | No verification engine |
| `transaction_blocker` | Transaction Readiness Gate | ARCHITECTURE_DEFINED | NOT_IMPLEMENTED | No readiness gate in code |

**All 9 matching roles:** ARCHITECTURE_DEFINED in H1 contracts but **NOT_IMPLEMENTED** in current code.

---

## Engine Consumer Identification

Each matrix family is consumed by a specific engine component defined in H1:

| Matrix Family | Primary Consumer Engine | H1 Contract Reference | Current Status |
|--------------|------------------------|----------------------|----------------|
| RESIDENTIAL_SEARCH | Qualification Engine → Matching Engine (Residential) | QUALIFICATION_EXECUTION_ARCHITECTURE.md, MATCHING_EXECUTION_ARCHITECTURE.md | NOT_IMPLEMENTED |
| LAND_SEARCH | Qualification Engine → Matching Engine (Land) | QUALIFICATION_EXECUTION_ARCHITECTURE.md, MATCHING_EXECUTION_ARCHITECTURE.md | NOT_IMPLEMENTED |
| COMMERCIAL_SEARCH | Qualification Engine → Matching Engine (Commercial) | COMMERCIAL_EXECUTION_ARCHITECTURE.md | NOT_IMPLEMENTED |
| COMMERCIAL_SEARCH (INVEST) | Qualification Engine → Matching Engine (Investment) | COMMERCIAL_EXECUTION_ARCHITECTURE.md | NOT_IMPLEMENTED |
| FINANCING_REQUEST | Qualification Engine → Financing Matching Engine | QUALIFICATION_MATRIX_CONTRACT.md | NOT_IMPLEMENTED |
| PROFESSIONAL_SEARCH | Qualification Engine → Professional Matching Engine | QUALIFICATION_MATRIX_CONTRACT.md | NOT_IMPLEMENTED |
| REAL_ESTATE_SERVICES | Qualification Engine → Service Matching Engine | QUALIFICATION_MATRIX_CONTRACT.md | NOT_IMPLEMENTED |

**Secondary consumers (downstream):**
- `CRM_EXECUTION_ARCHITECTURE.md` — Lead scoring and routing (consumes qualification output)
- `DECISION_ENGINE_ARCHITECTURE.md` — NBA selection (consumes matching results)
- `CONVERSATION_EXECUTION_ARCHITECTURE.md` — Question priority and next-question selection

---

## Fields Without Target in Current Model

All fields that do not map to `project_domain.py` or `property_domain.py` must be stored in `metadata_json`. The breakdown by category:

| Category | Example Fields | Count (est.) | Storage Strategy |
|----------|---------------|-------------|-----------------|
| Residential amenities | FLD-DOUCHES, FLD-CUISINE, FLD-MEUBLE, FLD-PARKING, FLD-CLIMATISATION, FLD-SECURITE, FLD-INTERNET, FLD-BALCON, FLD-JARDIN, FLD-PISCINE, FLD-GROUPE_ELECTROGENE, FLD-FORAGE, FLD-GARDIENNAGE, FLD-EAU, FLD-ELECTRICITE, FLD-COUR, FLD-CLOTURE, FLD-DEPENDANCES, FLD-ASCENSEUR | 20+ | metadata_json |
| Residential matching | FLD-SALONS, FLD-SURFACE_TERRAIN, FLD-ETAGE, FLD-PROXIMITY_PREFERENCES, FLD-MOBILITY, FLD-USAGE | 6+ | metadata_json |
| Contact / introduction | FLD-NOM, FLD-TELEPHONE, FLD-EMAIL, FLD-CANAL_PREFERE, FLD-LANGUE | 5 | metadata_json |
| Transaction | FLD-CAUTION, FLD-CHARGES, FLD-FINANCING, FLD-DUREE_LOCATION, FLD-DUREE_SEJOUR | 5+ | metadata_json |
| Colocation-specific | FLD-NOMBRE_COLOCATAIRES, FLD-ESPACES_PARTAGES, FLD-GENRE_PREFERENCE, FLD-AGE_RANGE, FLD-REGLEMENT_INTERIEUR | 5 | metadata_json |
| University-specific | FLD-UNIVERSITE, FLD-TYPE_CHAMBRE_UNIV, FLD-ANNEE_ETUDES, FLD-RESTAURATION, FLD-BOURSE | 5 | metadata_json |
| Short-stay specific | FLD-NOMBRE_PERSONNES, FLD-PETIT_DEJEUNER, FLD-MENAGE, FLD-SERVICES_INCLUS, FLD-LINGE, FLD-DATE_ARRIVEE, FLD-DATE_DEPART | 7 | metadata_json |
| Land-specific | quartier, axe, village, repere, surface, budget_par_m2, usage_prevu, titre_requis, type_titre, num_titre, type_document, certificat_propriete, plan_bornage, lotissement, terrain_loti, terrain_constructible, accessibilite, distance_route, qualite_acces, viabilisation_eau, viabilisation_electricite, topographie, inondable, occupation_actuelle, servitudes, litiges_connus, hypotheque, succession, indivision, procuration, bornage, pv_bornage, certificat_urbanisme | 30+ | metadata_json |
| Commercial common | COM-COMMON-001 through COM-COMMON-045 (activité, surface, hauteur, accès, visibilité, façade, flux, parking, stockage, électricité, eau, licence, nuisances, voisinage, fonds_commerce, chiffre_affaires, zone, documents_juridiques, bail, dépôt_garantie, accès_pmr, climatisation, état, étage, standing, délai, contact, urgence, employés, ouverture, horaires) | 45 | metadata_json |
| Investment-specific | INV-COMMON-001 through INV-COMMON-018 (budget_investissement, rendement_cible, horizon, risque, stratégie, ville, zone, expérience, source_financement, accompagnement, diaspora_flag, proche_sur_place, estimation_humaine, documents) | 18 | metadata_json |
| Financing core | FIN-COMMON-001 through FIN-COMMON-025 (objet_financement, montant, apport, revenus, garanties, documents, etc.) | 25 | metadata_json |
| Financing salaried | FIN-SAL-001 through FIN-SAL-008 (employeur, ancienneté, contrat, etc.) | 8 | metadata_json |
| Financing self-employed | FIN-SE-001 through FIN-SE-012 (activité, CA, formalisation, RCCM, etc.) | 12 | metadata_json |
| Financing construction | FIN-CONS-001 through FIN-CONS-020 (terrain, statut, plans, permis, devis, calendrier, etc.) | 20 | metadata_json |
| Financing diaspora | FIN-DIA-001 through FIN-DIA-006 (pays_résidence, statut, relay_local, etc.) | 6 | metadata_json |
| Professional service base | type_prestation, localisation (structured fields), description_besoin, urgence, budget_fourchette, date_souhaitee, type_bien_concerne, surface, besoin_details, qualification_requise, certifications, references, etc. | 15+ | metadata_json |
| Professional per-type | Per-profession specific fields (spécialité, années_expérience, diplôme, assurance_professionnelle, langue, etc.) | 50+ | metadata_json |
| Real estate service fields | Service-specific fields per 24 service types (type_estimation, specialite_evaluateur, methode_evaluation, rapport_estimation, type_visite, duree_gestion, type_mandat, support_publication, type_photographie, type_video, type_drone, type_staging, type_renovation, etc.) | 190+ | metadata_json |
| Derived fields | FLD-DERIVED-STANDING, FLD-DERIVED-BUDGET_COHERENCE, FLD-DERIVED-URGENCE_REELLE, FLD-DERIVED-PROFIL_ACHETEUR, FLD-DERIVED-PRIX_M2_ESTIME, FLD-DERIVED-COMPATIBILITE, FLD-DERIVED-URBANISATION, FLD-DERIVED-PROFIL | 8 | Computed (no storage needed) |

**Total fields without model target: ~690+** (all stored as `metadata_json` key-value pairs)

---

## Incompatible Values

| Matrix Concept | Current Model Value | Incompatibility | Action Required |
|---------------|-------------------|-----------------|-----------------|
| transaction: RENT, BUY | `project_type`: rent, buy | Matrix also uses FINANCE, FIND, SERVICE | Add project_type values |
| transaction: CESSION_BAIL | `project_type`: buy | No cession concept | Add or → metadata_json |
| transaction: FINANCE | `project_type`: buy (mapped) | Semantically different | Add FINANCE type |
| transaction: FIND | `project_type`: other | Professional service search | Add FIND type |
| transaction: SERVICE | `project_type`: other | Real estate service request | Add SERVICE type |
| property_type: 18 residential types | `property_type`: free-text string | Matrix uses canonical enum | Add enum in property model |
| property_type: 7 land types | `property_type`: free-text string | Land types not distinguished | Add land enum values |
| property_type: 16 commercial types | `property_type`: free-text string | Commercial types not distinguished | Add commercial enum values |
| financement: montant_recherche | `budget_max` | Financing amount ≠ budget | Separate field needed |
| budget_type: MONTHLY_RENT | (none) | No distinction rent vs buy budget | Distinguish in model |
| matching_role: 9 roles | (none) | No matching engine exists | Implement H1 matching engine |
| question_priority: 10-97 | (none) | No question selector exists | Implement next-question engine |
| readiness_level: 7 levels | (none) | No readiness calculator exists | Implement readiness engine |

---

## Extensions Required for Each Family

### ALL 107 MATRICES → H2 EXTENSION REQUIRED

The following extensions must be implemented before any matrix can be consumed by the engine:

#### Core Engine Extensions (Required by All Families)

| Extension | H1 Reference | Priority | Description |
|-----------|-------------|----------|-------------|
| Qualification Engine | QUALIFICATION_EXECUTION_ARCHITECTURE.md | CRITICAL | 8-step pipeline (normalize → extract → intent → context → score → classify → route) |
| Matrix Selector | QUALIFICATION_MATRIX_CONTRACT.md §0.1 | CRITICAL | Resolve matrix by (family, transaction, property_type) |
| Field Dictionary | QUALIFICATION_MATRIX_CONTRACT.md §0.3 | CRITICAL | 100+ field definitions with validation, normalization, templates |
| Matching Engine | MATCHING_EXECUTION_ARCHITECTURE.md | CRITICAL | 9-step pipeline with constraint enforcement, scoring, ranking |
| Matching Role Evaluator | MATCHING_EXECUTION_ARCHITECTURE.md §0.2 | CRITICAL | Evaluate hard_constraint, soft_constraint, ranking_preference, boost, penalty |
| Next Question Selector | QUALIFICATION_MATRIX_CONTRACT.md §0.5 | HIGH | Dynamic question ordering per matrix |
| Readiness Calculator | QUALIFICATION_MATRIX_CONTRACT.md §0.4 | HIGH | Compute readiness stage per matrix field completion |
| Question Priority Engine | QUESTION_PRIORITY_POLICY.md | HIGH | Priority formula with context awareness |

#### Family-Specific Extensions

| Family | Extension | Priority | Description |
|--------|-----------|----------|-------------|
| RESIDENTIAL_SEARCH | Residential Property Type Taxonomy | HIGH | 18 canonical residential types with hierarchical relationships |
| RESIDENTIAL_SEARCH | Amenity Matching Model | HIGH | Douches, cuisine, meuble, parking, climatisation, etc. matching semantics |
| LAND_SEARCH | Land Legal Verification Engine | HIGH | Title verification, document validation, Cameroon-specific land rules |
| LAND_SEARCH | Land Matching Semantics | HIGH | Surface tolerance (±30%), usage hard_constraint, access ranking |
| COMMERCIAL_SEARCH | Commercial Activity Taxonomy | HIGH | Activity type matching, zoning constraints |
| COMMERCIAL_SEARCH | Commercial Matching Semantics | HIGH | Surface hard_constraint, flux/visibilité ranking, licence matching |
| COMMERCIAL_SEARCH (INVEST) | Investment Profile Engine | HIGH | Yield calculation, risk assessment, horizon matching |
| COMMERCIAL_SEARCH (INVEST) | Diaspora Investor Module | MEDIUM | Diaspora detection, local representative handling |
| FINANCING_REQUEST | Financial Profile Engine | HIGH | Income verification, repayment capacity, guarantee assessment |
| FINANCING_REQUEST | Lender Matching Engine | HIGH | Match requests to financing products by profile |
| FINANCING_REQUEST | Document Collection Pipeline | MEDIUM | Collect and verify financial documents |
| FINANCING_REQUEST | Construction Financing Module | MEDIUM | Construction-specific fields (plans, permits, tranches) |
| FINANCING_REQUEST | Diaspora Financing Module | MEDIUM | Diaspora-specific fields and document handling |
| PROFESSIONAL_SEARCH | Professional Profile Engine | HIGH | Qualification matching, certification verification |
| PROFESSIONAL_SEARCH | Professional Matching Semantics | HIGH | Service type matching, location radius, urgency handling |
| PROFESSIONAL_SEARCH | Per-Profession-Specific Matrices | MEDIUM | 27 distinct qualification profiles |
| REAL_ESTATE_SERVICES | Service Profile Engine | HIGH | Service offering matching to provider capabilities |
| REAL_ESTATE_SERVICES | Service Progression Model | MEDIUM | 4-stage progression (service → matching → quote → execution) |
| REAL_ESTATE_SERVICES | Per-Service-Specific Matrices | MEDIUM | 24 distinct service matrices with unique fields |

---

## Overall Statistics

| Category | Count |
|----------|-------|
| **Total matrices** | **107** |
| — RESIDENTIAL_SEARCH | 18 |
| — LAND_SEARCH | 7 |
| — COMMERCIAL_SEARCH | 16 |
| — COMMERCIAL_SEARCH (INVEST) | 5 |
| — FINANCING_REQUEST | 10 |
| — PROFESSIONAL_SEARCH | 27 |
| — REAL_ESTATE_SERVICES | 24 |
| **Implementation status** | |
| Directly implemented in code | 0 (0%) |
| H1 architecture contract defined | 107 (100%) |
| Requires H2 extension | 107 (100%) |
| **Current model fields usable** | |
| Directly compatible | 6 |
| Partially compatible | 4 |
| Without model target (→ metadata_json) | 690+ |
| **Matching roles** | |
| Defined in H0.5 matrices | 9 |
| Implemented in current code | 0 (0%) |
| **Matrix families × engine components** | 7 distinct engines |
| **INTENT_FAMILY × PROPERTY_SERVICE_TYPE combinations** | 107 (1 per matrix) |
| **Source status** | |
| HERITAGE_VALIDATED | ~75 (70%) |
| EXPERT_PROPOSAL | ~21 (20%) |
| HERITAGE_NORMALIZED | ~11 (10%) |
| **Confidence levels** | |
| HIGH | ~80 (75%) |
| MEDIUM | ~21 (20%) |
| LOW | ~6 (5%) |

---

## Conclusion

The 107 qualification matrices constitute the **complete specification** for the H2 qualification engine implementation. They are:

1. **Architecturally mapped** — Every matrix, field, and matching role is defined in H1 contracts
2. **Not implemented** — Zero lines of qualification/matching engine code exist in the current codebase
3. **Semantically consistent** — The 9 matching roles from matrices map 1:1 to H1 matching engine components
4. **Field-incomplete in current model** — 690+ matrix-specific fields require `metadata_json` or model extensions
5. **Uniformly requiring H2 extension** — All 107 matrices require engine implementation before they can be consumed

**Recommendation:** Implement the Qualification Engine, Matrix Selector, and Next Question Selector as the foundational H2 extensions. These are the minimal set that unblocks all 107 matrices. Follow with the Matching Engine and family-specific extensions in priority order: Residential → Land → Commercial → Financing → Professional → Services.
