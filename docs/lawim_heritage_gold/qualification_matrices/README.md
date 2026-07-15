# LAWIM Qualification Matrices — Heritage Gold

**Document ID:** LAWIM-GOLD-QM-README-V1
**Domain:** Qualification Matrices Framework
**Status:** CANONICAL — Framework reference for all matrix documentation
**Date:** 2026-07-15

---

## Table of Contents

1. [Purpose](#purpose)
2. [Overview of the Matrix Catalog](#overview-of-the-matrix-catalog)
3. [How to Navigate the Files](#how-to-navigate-the-files)
4. [How Matrices Are Organized](#how-matrices-are-organized)
5. [How to Add New Matrices](#how-to-add-new-matrices)
6. [Status of This Documentation](#status-of-this-documentation)
7. [Related Documentation](#related-documentation)
8. [Matrix File Index](#matrix-file-index)

---

## Purpose

The qualification matrices are the canonical reference for every property type, service type, and financing request that LAWIM can handle. Each matrix defines the exact fields required at each stage of qualification, from initial intake through to transaction readiness.

### Why Matrices Exist

- **Consistency**: Every property type has a predictable, documented qualification path
- **Completeness**: No field is collected by accident; every field has a source, confidence level, and matching role
- **Reusability**: The framework supports adding new property types without redesigning the qualification engine
- **Traceability**: Every field is sourced from heritage documents, external confirmation, or expert proposal
- **Progressive qualification**: The readiness-level system ensures the user is never asked more than necessary before actionable results can be delivered

### What Matrices Cover

| Domain | File | Transaction Types | Count |
|--------|------|-------------------|-------|
| Residential Search | `residential_search_matrices.md` | RENT, BUY | 18 matrices |
| Land Search | `land_search_matrices.md` | BUY | 7 matrices |
| Commercial Property | `commercial_property_matrices.md` | RENT, BUY, CESSION, BAIL | 21 matrices |
| Financing Request | `financing_request_matrices.md` | FINANCE | 10 matrices |
| Professional Service | `professional_service_matrices.md` | FIND | 27 matrices |
| Real Estate Service | `real_estate_service_matrices.md` | SERVICE | 24 matrices |

**Total: 107 qualification matrices**

---

## Overview of the Matrix Catalog

The matrix catalog covers six request families:

### 1. RESIDENTIAL_SEARCH (18 matrices)
All residential property types from basic rooms (chambre_simple) to university residences (cite_universitaire). Each matrix defines fields for rent or buy transactions with property-type-specific rules.

### 2. LAND_SEARCH (7 matrices)
Land with title (titre), without title, serviced (loti), unserviced (non_loti), collective title, individual title, and land undergoing subdivision. Each land type has distinct legal and documentary requirements.

### 3. COMMERCIAL_SEARCH (21 matrices)
Sixteen commercial property types (boutique, bureau, local_commercial, magasin, entrepot, hangar, atelier, restaurant, bar, hotel, auberge, immeuble_de_rapport, immeuble_commercial, station_service, site_industriel, espace_evenementiel) plus five investment types (investissement_locatif, investissement_terrain, investissement_immobilier_commercial, investissement_promotion, syndicat_copropriete).

### 4. FINANCING_REQUEST (10 matrices)
Credit immobilier, acquisition financing, construction financing, renovation financing, development financing, property-backed loan, investor search, co-financing, diaspora contribution, professional/business financing.

### 5. PROFESSIONAL_SEARCH (27 matrices)
All professional service providers: agent immobilier, agence immobiliere, notaire, geometre, architecte, ingenieur genie civil, technicien batiment, macon, electricien, plombier, menuisier, peintre, carreleur, couvreur, expert immobilier, evaluateur, gestionnaire immobilier, syndic, photographe immobilier, videaste drone, demenageur, entreprise nettoyage, gardiennage, assureur, banque microfinance, courtier, prestataire administratif.

### 6. REAL_ESTATE_SERVICES (24 matrices)
Real estate service offerings: estimation immobiliere, expertise, verification documentaire, visite property, contre visite, gestion locative, mise en location, mise en vente, publication service, photographie, video service, drone service, home staging, renovation service, construction service, entretien, nettoyage, securisation, demenagement, assurance service, conseil juridique, conseil fiscal, gestion copropriete, recouvrement locatif.

---

## How to Navigate the Files

### File Structure

```
qualification_matrices/
├── README.md                           ← This file
├── MATRIX_CATALOG.md                   ← Complete catalog of all matrices
├── COMMON_FIELD_DICTIONARY.md          ← Dictionary of all common fields
├── READINESS_LEVELS.md                 ← Readiness level definitions
├── QUESTION_PRIORITY_POLICY.md         ← Dynamic question ordering policy
├── CONDITIONAL_QUESTION_RULES.md       ← Conditional question rules
├── MATCHING_FIELD_SEMANTICS.md         ← Matching role definitions
├── PRIVACY_AND_SENSITIVE_FIELDS.md     ← Privacy levels and sensitive fields
├── residential_search_matrices.md      ← Residential property matrices
├── land_search_matrices.md             ← Land property matrices
├── commercial_property_matrices.md     ← Commercial property matrices
├── financing_request_matrices.md       ← Financing request matrices
├── professional_service_matrices.md    ← Professional service matrices
└── real_estate_service_matrices.md     ← Real estate service matrices
```

### Quick Navigation Guide

| If you need to... | Start here |
|-------------------|------------|
| Find a specific matrix | `MATRIX_CATALOG.md` — search by matrix_id or property type |
| Understand a field's definition | `COMMON_FIELD_DICTIONARY.md` — lookup by field_id |
| Know what questions to ask when | `QUESTION_PRIORITY_POLICY.md` + `CONDITIONAL_QUESTION_RULES.md` |
| Know readiness thresholds | `READINESS_LEVELS.md` |
| Understand matching behavior | `MATCHING_FIELD_SEMANTICS.md` |
| Handle sensitive data | `PRIVACY_AND_SENSITIVE_FIELDS.md` |
| Read a specific matrix | Direct matrix file by domain |

### Cross-Reference Convention

Throughout the matrix files, references use the following conventions:

- `QUALIFICATION_MODEL.md §N` — Section N of the qualification model
- `CONVERSATION_MODEL.md §N` — Section N of the conversation model
- `MATCHING_MODEL.md §N` — Section N of the matching model
- `DOMAIN_MODEL.md §N` — Section N of the domain model
- `FLD-XXXXX` — Field identifier used across matrices
- `MATRIX-XXX-XXX` — Matrix identifier
- `COM-COMMON-NNN` — Commercial common field identifier
- `FIN-COMMON-NNN` — Financing common field identifier

---

## How Matrices Are Organized

### Matrix Structure (Per Matrix)

Each matrix follows a standard structure:

```yaml
matrix_id: Unique identifier (e.g., MATRIX-RES-SEARCH-001)
canonical_name: Human-readable name
request_family: Domain family (RESIDENTIAL_SEARCH, LAND_SEARCH, etc.)
transaction_type: Supported transaction types
property_or_service_type: The specific property or service type
requester_typology: Who typically makes this request
journey_stage: SEARCH, SERVICE, or FINANCE
description: Brief description

// Field sections (threshold-based):
minimum_intake_fields:    // Always collected first
minimum_search_fields:    // Required before search
minimum_matching_fields:  // Required for matching
minimum_introduction_fields: // Contact/intro before introduction
minimum_visit_fields:     // Required before visit
minimum_transaction_fields: // Required before transaction
recommended_fields:       // Nice to have
optional_fields:          // Full set of optional fields
conditional_fields:       // Shown only under conditions
sensitive_fields:         // Privacy-handled fields
derived_fields:           // System-computed fields
forbidden_questions:      // Never ask these
```

### Field Specification (Per Field)

Each field in a matrix carries:

| Attribute | Description |
|-----------|-------------|
| FIELD-ID | Unique field identifier |
| label | Human-readable label (French) |
| data_type | string, integer, float, boolean, enum, date |
| allowed_values | For enums: the permitted values |
| mandatory_when | Condition under which the field is mandatory |
| question_template | Suggested question wording |
| question_priority | Numeric priority (lower = asked earlier) |
| matching_role | How the field affects matching |
| privacy_level | public, private, sensitive, confidential |
| source | Where the field definition originates |
| confidence | HIGH, MEDIUM, LOW |

### Readiness Levels

Every field belongs to a readiness level bucket. The levels are:

| Level | Meaning | Example Fields |
|-------|---------|----------------|
| INTENT_IDENTIFIED | Basic intent and property type known | FLD-TRANSACTION, FLD-PROPERTY_TYPE |
| MINIMUM_INTAKE_READY | Core identification complete | FLD-CITY, FLD-BUDGET_MAX |
| MINIMUM_SEARCH_READY | Can launch first search | FLD-NEIGHBORHOOD, budget |
| MINIMUM_MATCHING_READY | Can rank and match results | FLD-DOUCHES, FLD-CUISINE |
| INTRODUCTION_READY | Can introduce parties | FLD-NOM, FLD-TELEPHONE, FLD-CANAL_PREFERE |
| VISIT_READY | Can organise visits | FLD-CLIMATISATION, FLD-SECURITE |
| TRANSACTION_READY | Can proceed to transaction | FLD-CAUTION, FLD-CHARGES, FLD-FINANCING |

The **cardinal rule**: As soon as MINIMUM_SEARCH_READY is reached, LAWIM launches a first search. It is forbidden to continue collecting recommended or optional fields before presenting initial results.

---

## How to Add New Matrices

### Adding a New Property Type

1. **Identify the family**: Determine which request family the property belongs to (RESIDENTIAL_SEARCH, LAND_SEARCH, COMMERCIAL_SEARCH, FINANCING_REQUEST, PROFESSIONAL_SEARCH, or REAL_ESTATE_SERVICES)

2. **Copy the template**: Use an existing matrix of the same family as a template

3. **Assign a matrix_id**: Follow the existing numbering convention (e.g., MATRIX-RES-SEARCH-019 for a new residential type)

4. **Define fields per readiness level**:
   - Start with the common fields inherited from the family
   - Add property-type-specific fields
   - Specify mandatory_when conditions
   - Assign matching roles
   - Define derived fields
   - List forbidden questions

5. **Update the catalog**: Add the new matrix to `MATRIX_CATALOG.md`

6. **Update common fields**: If adding new fields, add them to `COMMON_FIELD_DICTIONARY.md`

### Adding a New Field

1. **Assign a FIELD-ID**: Follow the existing naming convention
2. **Add to COMMON_FIELD_DICTIONARY.md**: Full definition with all attributes
3. **Add to relevant matrices**: Reference the FIELD-ID in each matrix's field sections
4. **Consider sensitivity**: Add to PRIVACY_AND_SENSITIVE_FIELDS.md if needed

### Quality Checklist

- [ ] matrix_id follows naming convention
- [ ] All field sections populated (minimum empty sections can be omitted)
- [ ] Every field has a source and confidence level
- [ ] Forbidden questions updated
- [ ] Derived fields specified
- [ ] Matching roles assigned
- [ ] Privacy levels set
- [ ] mandatory_when conditions documented
- [ ] CATALOG updated
- [ ] COMMON_FIELD_DICTIONARY updated (if new fields)

---

## Status of This Documentation

| Component | Status | Last Updated |
|-----------|--------|-------------|
| Residential Search Matrices | CANONICAL — 18 matrices, fully sourced | 2026-07-15 |
| Land Search Matrices | CANONICAL — 7 land types, Cameroon-specific | 2026-07-15 |
| Commercial Property Matrices | CANONICAL — 21 commercial/investment types | 2026-07-15 |
| Financing Request Matrices | GOLD VALIDATED — 10 financing types | 2026-07-15 |
| Professional Service Matrices | GOLD VALIDATED — 27 professional types | 2026-07-15 |
| Real Estate Service Matrices | GOLD VALIDATED — 24 service types | 2026-07-15 |
| MATRIX_CATALOG.md | CANONICAL — Complete cross-reference | 2026-07-15 |
| COMMON_FIELD_DICTIONARY.md | CANONICAL — 100+ field definitions | 2026-07-15 |
| READINESS_LEVELS.md | CANONICAL — 7-level readiness system | 2026-07-15 |
| QUESTION_PRIORITY_POLICY.md | CANONICAL — Priority calculation rules | 2026-07-15 |
| CONDITIONAL_QUESTION_RULES.md | CANONICAL — Conditional rules with examples | 2026-07-15 |
| MATCHING_FIELD_SEMANTICS.md | CANONICAL — All 9 matching roles defined | 2026-07-15 |
| PRIVACY_AND_SENSITIVE_FIELDS.md | CANONICAL — 4 privacy levels | 2026-07-15 |

### Status Definitions

| Status | Meaning |
|--------|---------|
| CANONICAL | Approved reference document for architecture H1 |
| GOLD VALIDATED | Validated against heritage sources |
| DRAFT | Initial version, awaiting review |
| HUMAN_VALIDATION_REQUIRED | Needs expert review before use |

---

## Related Documentation

### Main Heritage Gold Docs

- [Main README](../README.md) — LAWIM Heritage Gold overview
- [QUALIFICATION_MODEL.md](../QUALIFICATION_MODEL.md) — Core qualification model, pipeline, scoring
- [MATCHING_MODEL.md](../MATCHING_MODEL.md) — Matching scoring weights, decision engine
- [CONVERSATION_MODEL.md](../CONVERSATION_MODEL.md) — Conversation flow, channel adaptation, double consent
- [DOMAIN_MODEL.md](../DOMAIN_MODEL.md) — Domain concepts, entities, relationships
- [PROPERTY_MODEL.md](../PROPERTY_MODEL.md) — Property taxonomy, attribute definitions
- [INTENT_MODEL.md](../INTENT_MODEL.md) — Intent detection, user goal modeling
- [ROLE_MODEL.md](../ROLE_MODEL.md) — User roles, permissions, typologies
- [GEOGRAPHY_MODEL.md](../GEOGRAPHY_MODEL.md) — City, neighborhood, zone definitions
- [LANGUAGE_MODEL.md](../LANGUAGE_MODEL.md) — Multilingual support, terminology
- [KNOWLEDGE_GLOSSARY.md](../KNOWLEDGE_GLOSSARY.md) — Business glossary of terms
- [TRACEABILITY_MATRIX.md](../TRACEABILITY_MATRIX.md) — Source traceability

### Final Report

The final extraction report is available at:
- [KNOWLEDGE_RECOVERY_REPORT_H0.4.md](../KNOWLEDGE_RECOVERY_REPORT_H0.4.md) — Comprehensive recovery report covering all heritage knowledge domains
- [WORKFLOW_EXTRACTION_COMPLETE.md](../WORKFLOW_EXTRACTION_COMPLETE.md) — Workflow extraction completion status
- [COVERAGE_REPORT.md](../COVERAGE_REPORT.md) — Coverage analysis and gap identification

---

## Matrix File Index

### Residential Search (18 matrices)

| # | Matrix | File | Lines |
|---|--------|------|-------|
| 1 | MATRIX-RES-SEARCH-001 | `residential_search_matrices.md` | 220-352 |
| 2 | MATRIX-RES-SEARCH-002 | `residential_search_matrices.md` | 354-487 |
| 3 | MATRIX-RES-SEARCH-003 | `residential_search_matrices.md` | 489-623 |
| 4 | MATRIX-RES-SEARCH-004 | `residential_search_matrices.md` | 625-759 |
| 5 | MATRIX-RES-SEARCH-005 | `residential_search_matrices.md` | 761-897 |
| 6 | MATRIX-RES-SEARCH-006 | `residential_search_matrices.md` | 899-1049 |
| 7 | MATRIX-RES-SEARCH-007 | `residential_search_matrices.md` | 1051-1200+ |
| 8 | MATRIX-RES-SEARCH-008 | `residential_search_matrices.md` | — |
| 9 | MATRIX-RES-SEARCH-009 | `residential_search_matrices.md` | — |
| 10 | MATRIX-RES-SEARCH-010 | `residential_search_matrices.md` | — |
| 11 | MATRIX-RES-SEARCH-011 | `residential_search_matrices.md` | — |
| 12 | MATRIX-RES-SEARCH-012 | `residential_search_matrices.md` | — |
| 13 | MATRIX-RES-SEARCH-013 | `residential_search_matrices.md` | — |
| 14 | MATRIX-RES-SEARCH-014 | `residential_search_matrices.md` | — |
| 15 | MATRIX-RES-SEARCH-015 | `residential_search_matrices.md` | — |
| 16 | MATRIX-RES-SEARCH-016 | `residential_search_matrices.md` | — |
| 17 | MATRIX-RES-SEARCH-017 | `residential_search_matrices.md` | — |
| 18 | MATRIX-RES-SEARCH-018 | `residential_search_matrices.md` | — |

### Land Search (7 matrices)

| # | Matrix | File | Lines |
|---|--------|------|-------|
| 1 | LAND_SEARCH_TERRAIN_TITRE_001 | `land_search_matrices.md` | 108-244 |
| 2 | LAND_SEARCH_TERRAIN_NON_TITRE_001 | `land_search_matrices.md` | 247-384 |
| 3 | LAND_SEARCH_TERRAIN_LOTI_001 | `land_search_matrices.md` | 387-505 |
| 4 | LAND_SEARCH_TERRAIN_NON_LOTI_001 | `land_search_matrices.md` | 508-633 |
| 5 | LAND_SEARCH_TERRAIN_TITRE_COLLECTIF_001 | `land_search_matrices.md` | 636-765 |
| 6 | LAND_SEARCH_TERRAIN_TITRE_INDIVIDUEL_001 | `land_search_matrices.md` | 768-894 |
| 7 | LAND_SEARCH_TERRAIN_SOUS_MORCELLEMENT_001 | `land_search_matrices.md` | 897-950+ |

### Commercial Property (21 matrices)

| # | Matrix | File | Lines |
|---|--------|------|-------|
| 1 | COM-MATRIX-001 | `commercial_property_matrices.md` | 132-258 |
| 2 | COM-MATRIX-002 | `commercial_property_matrices.md` | 260-389 |
| 3 | COM-MATRIX-003 | `commercial_property_matrices.md` | 391-516 |
| 4 | COM-MATRIX-004 | `commercial_property_matrices.md` | 519-620+ |
| 5-21 | (remaining commercial types) | `commercial_property_matrices.md` | — |

### Financing Request (10 matrices)

| # | Matrix | File | Lines |
|---|--------|------|-------|
| 1 | MATRIX-FIN-001 | `financing_request_matrices.md` | 134-295 |
| 2 | MATRIX-FIN-002 | `financing_request_matrices.md` | 297-435 |
| 3 | MATRIX-FIN-003 | `financing_request_matrices.md` | 437-597 |
| 4 | MATRIX-FIN-004 | `financing_request_matrices.md` | 600-724 |
| 5-10 | (remaining financing types) | `financing_request_matrices.md` | — |

### Professional Service (27 matrices)

| # | Matrix | File | Lines |
|---|--------|------|-------|
| 1 | PRO-AGENT-001 | `professional_service_matrices.md` | 284-382 |
| 2 | PRO-AGENC-002 | `professional_service_matrices.md` | 385-506 |
| 3 | PRO-NOTAI-003 | `professional_service_matrices.md` | 509-652 |
| 4 | PRO-GEOME-004 | `professional_service_matrices.md` | 655-790 |
| 5 | PRO-ARCHI-005 | `professional_service_matrices.md` | 793-948 |
| 6 | PRO-INGEN-006 | `professional_service_matrices.md` | 951-1094 |
| 7 | PRO-TECHN-007 | `professional_service_matrices.md` | 1097-1231 |
| 8 | PRO-MACON-008 | `professional_service_matrices.md` | 1234-1370 |
| 9 | PRO-ELECT-009 | `professional_service_matrices.md` | 1373-1519 |
| 10 | PRO-PLOMB-010 | `professional_service_matrices.md` | 1522-1659 |
| 11 | PRO-MENUI-011 | `professional_service_matrices.md` | 1662-1809 |
| 12 | PRO-PEINT-012 | `professional_service_matrices.md` | 1812-1955 |
| 13 | PRO-CARRE-013 | `professional_service_matrices.md` | 1958-2000+ |
| 14-27 | (remaining professional types) | `professional_service_matrices.md` | — |

### Real Estate Service (24 matrices)

| # | Matrix | File | Lines |
|---|--------|------|-------|
| 1 | SVC-ESTI-001 | `real_estate_service_matrices.md` | 50-219 |
| 2 | SVC-EXPE-002 | `real_estate_service_matrices.md` | 222-381 |
| 3 | SVC-VERI-003 | `real_estate_service_matrices.md` | 384-509 |
| 4 | SVC-VISI-004 | `real_estate_service_matrices.md` | 512-635 |
| 5 | SVC-CONT-005 | `real_estate_service_matrices.md` | 638-749 |
| 6 | SVC-GEST-006 | `real_estate_service_matrices.md` | 752-930 |
| 7 | SVC-MISE-007 | `real_estate_service_matrices.md` | 933-1072 |
| 8 | SVC-MISE-008 | `real_estate_service_matrices.md` | 1075-1213 |
| 9 | SVC-PUBL-009 | `real_estate_service_matrices.md` | 1216-1354 |
| 10 | SVC-PHOT-010 | `real_estate_service_matrices.md` | 1357-1485 |
| 11 | SVC-VIDE-011 | `real_estate_service_matrices.md` | 1488-1618 |
| 12 | SVC-DRON-012 | `real_estate_service_matrices.md` | 1621-1752 |
| 13 | SVC-HOME-013 | `real_estate_service_matrices.md` | 1755-1891 |
| 14 | SVC-RENO-014 | `real_estate_service_matrices.md` | 1894-2000+ |
| 15-24 | (remaining service types) | `real_estate_service_matrices.md` | — |

---

**End of README.md** — For questions or corrections, refer to the main heritage gold documentation or open an issue in the LAWIM documentation repository.
