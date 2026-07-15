# SERVICE CROSSWALK — Heritage Gold → LAWIM V2

**Document ID:** LAWIM-SEM-SERVICE-CROSSWALK-V1
**Status:** CANONICAL — Semantic harmonization of service models
**Date:** 2026-07-15
**Mapping Statuses:** EXACT_MATCH, NORMALIZED_MATCH, ONE_TO_MANY, MANY_TO_ONE, PARTIAL_MATCH, EXTENSION_REQUIRED, OBSOLETE, CONFLICT, HUMAN_DECISION_REQUIRED, UNMAPPED

---

## Table of Contents

1. [Service Family Overview](#1-service-family-overview)
2. [Monetized Services Mapping (Revenue Model)](#2-monetized-services-mapping-revenue-model)
3. [Real Estate Services Mapping](#3-real-estate-services-mapping)
4. [Professional Services Mapping](#4-professional-services-mapping)
5. [CRM Monetized Services Mapping](#5-crm-monetized-services-mapping)
6. [Service Lifecycle Comparison](#6-service-lifecycle-comparison)
7. [Gap Analysis](#7-gap-analysis)

---

## 1. Service Family Overview

### Heritage Gold Service Universe

| Family | Count | Source Document | Description |
|--------|-------|-----------------|-------------|
| Monetized Services (Revenue) | 13 | DOMAIN_MODEL.md §9 | Paid services with fixed FCFA prices |
| Real Estate Service Matrices | 24 | MATRIX_CATALOG.md §7 | Qualification matrices for service requests |
| Professional Service Matrices | 27 | MATRIX_CATALOG.md §6 | FIND-type professional search matrices |
| CRM Monetized Services | 8 | CRM_MODEL.md §14 | Lead packs, diaspora services, premium profiles |
| **Total Heritage Services** | **72** | | |

### LAWIM V2 Service Coverage

| Family | Count | Status | Description |
|--------|-------|--------|-------------|
| Prisma Service Model | 0 | NOT_IMPLEMENTED | No `Service`, `ServiceOrder`, or `ServiceCatalog` models |
| Payment System | 0 | FEATURE_FLAG_OFF | `/api/v2/financial/payments/*` endpoints exist but `payments=OFF` |
| Business Profiles | 27 | IMPLEMENTED | `business_profiles.py` — professional role definitions (not services) |
| Project Service Tracking | partial | IMPLEMENTED | `Project` model with steps, not service orders |
| **Total V2 Service Coverage** | **0 / 72** | **EXTENSION_REQUIRED** | |

### Key Finding

All 72 Heritage Gold service concepts are status **EXTENSION_REQUIRED** in LAWIM V2. The V2 codebase has no service catalog, no service order lifecycle, no payment processing, and no monetization logic. The Heritage Gold business model (zero commission + paid services) is documented but unimplemented.

---

## 2. Monetized Services Mapping (Revenue Model)

**Source:** Heritage Gold DOMAIN_MODEL.md §9 — 13 pricing tiers

| Heritage Gold Code | Heritage Gold Service Name | Price (FCFA) | V2 Status | V2 Equivalent | Mapping Status | Priority |
|---|---|---|---|---|---|---|
| boost_7j | Boost visibilité 7 jours | 2 000 | Service model required | `Property.boost_level` exists in LAWIMA heritage but not in V2 Prisma | EXTENSION_REQUIRED | HIGH |
| boost_30j | Boost visibilité 30 jours | 5 000 | Service model required | Same as boost_7j, different duration | EXTENSION_REQUIRED | HIGH |
| premium_listing | Annonce premium | 10 000 | Service model required | No `Property.premium` field in V2 Prisma | EXTENSION_REQUIRED | HIGH |
| agent_pro | Abonnement agent professionnel | 10 000/mois | Service model required | `Organization` model exists but no subscription system | EXTENSION_REQUIRED | HIGH |
| accompagnement_visite | Accompagnement de visite | 50 000 | Service model required | No visit accompaniment service model | EXTENSION_REQUIRED | MEDIUM |
| accompagnement_transaction | Accompagnement de transaction | 50 000 | Service model required | Transaction flow exists in canonical docs, no paid accompaniment | EXTENSION_REQUIRED | MEDIUM |
| controle_documentaire | Contrôle documentaire | 5 000 | Service model required | No document verification service | EXTENSION_REQUIRED | LOW |
| photographie | Photographie professionnelle | 15 000 | Service model required | `Media` model exists but no photography service ordering | EXTENSION_REQUIRED | LOW |
| video | Vidéo professionnelle | 25 000 | Service model required | `Media` model supports video but no service ordering | EXTENSION_REQUIRED | LOW |
| verification | Vérification de bien | 10 000 | Service model required | `Property.verification_status` in heritage but not V2 | EXTENSION_REQUIRED | MEDIUM |
| mise_en_relation | Mise en relation payante | 500 | Service model required | Agent opt-in exists in heritage but no pay-per-connection | EXTENSION_REQUIRED | HIGH |
| assistance | Assistance personnalisée | 50 000 | Service model required | No premium assistant service | EXTENSION_REQUIRED | LOW |
| visibilite_premium | Visibilité premium | 7 500 | Service model required | Distinct from boost, combines multiple visibility features | EXTENSION_REQUIRED | LOW |

### Mapping Notes

- All 13 services map to **EXTENSION_REQUIRED** — no equivalent exists in V2
- `boost_7j` and `boost_30j` share the same concept (visibility boost) differentiated only by duration → future V2 model should use a service configuration with duration parameter
- `photographie` and `video` relate to the existing `Media` model but require a service order flow
- `mise_en_relation` (pay-per-connection) is the core LAWIM monetization model — highest priority
- `accompagnement_visite` and `accompagnement_transaction` are the two premium accompaniment paths at identical price points

---

## 3. Real Estate Services Mapping

**Source:** Heritage Gold MATRIX_CATALOG.md §7 — 24 real estate service matrices (SVC- prefix)

### 3.1 Documented Service Matrices (SVC-)

| Matrix ID | Service Type | Transaction Type | V2 Status | V2 Equivalent | Mapping Status | Priority |
|---|---|---|---|---|---|---|
| SVC-ESTI-001 | estimation_immobiliere | SERVICE | Not implemented | `Project.project_type` could accept "estimation" | EXTENSION_REQUIRED | HIGH |
| SVC-EXPE-002 | expertise | SERVICE | Not implemented | No expertise service model | EXTENSION_REQUIRED | MEDIUM |
| SVC-VERI-003 | verification_documentaire | SERVICE | Not implemented | Document verification absent | EXTENSION_REQUIRED | MEDIUM |
| SVC-VISI-004 | visite_property | SERVICE | PARTIAL | `Conversation` + `Project` could track visits | PARTIAL_MATCH | HIGH |
| SVC-CONT-005 | contre_visite | SERVICE | PARTIAL | Second visit, same infrastructure as visite | PARTIAL_MATCH | HIGH |
| SVC-GEST-006 | gestion_locative | SERVICE | Not implemented | Property management not in V2 scope | EXTENSION_REQUIRED | LOW |
| SVC-MISE-007 | mise_en_location | SERVICE | PARTIAL | `Property` creation flow covers listing | PARTIAL_MATCH | HIGH |
| SVC-MISE-008 | mise_en_vente | SERVICE | PARTIAL | `Property` creation flow covers listing | PARTIAL_MATCH | HIGH |
| SVC-PUBL-009 | publication_service | SERVICE | PARTIAL | `Property.publishedAt` exists | PARTIAL_MATCH | HIGH |
| SVC-PHOT-010 | photographie | SERVICE | PARTIAL | `Media` model supports photo upload | PARTIAL_MATCH | LOW |
| SVC-VIDE-011 | video_service | SERVICE | PARTIAL | `Media` model supports video upload | PARTIAL_MATCH | LOW |
| SVC-DRON-012 | drone_service | SERVICE | Not implemented | No drone service capability | EXTENSION_REQUIRED | LOW |
| SVC-HOME-013 | home_staging | SERVICE | Not implemented | No staging service model | EXTENSION_REQUIRED | LOW |
| SVC-RENO-014 | renovation_service | SERVICE | PARTIAL | `Project.projectType` could cover renovation | PARTIAL_MATCH | MEDIUM |
| SVC-CONS-015 | construction_service | SERVICE | PARTIAL | `Project.projectType` could cover construction | PARTIAL_MATCH | MEDIUM |
| SVC-ENTR-016 | entretien | SERVICE | Not implemented | No maintenance service | EXTENSION_REQUIRED | LOW |
| SVC-NETT-017 | nettoyage | SERVICE | Not implemented | No cleaning service | EXTENSION_REQUIRED | LOW |
| SVC-SECU-018 | securisation | SERVICE | Not implemented | No security service | EXTENSION_REQUIRED | LOW |
| SVC-DEME-019 | demenagement | SERVICE | Not implemented | Moving service not in V2 | EXTENSION_REQUIRED | LOW |
| SVC-ASSU-020 | assurance_service | SERVICE | Not implemented | Insurance referral not in V2 | EXTENSION_REQUIRED | LOW |
| SVC-CONS-021 | conseil_juridique | SERVICE | Not implemented | Legal advice not in V2 | EXTENSION_REQUIRED | LOW |
| SVC-CONS-022 | conseil_fiscal | SERVICE | Not implemented | Tax advice not in V2 | EXTENSION_REQUIRED | LOW |
| SVC-GEST-023 | gestion_copropriete | SERVICE | Not implemented | Condo management not in V2 | EXTENSION_REQUIRED | LOW |
| SVC-RECO-024 | recouvrement_locatif | SERVICE | Not implemented | Rent recovery not in V2 | EXTENSION_REQUIRED | LOW |

### 3.2 Mapping Notes

- **PARTIAL_MATCH** services (8 of 24) have indirect V2 equivalents via `Property` or `Project` models, but no dedicated service flow
- **EXTENSION_REQUIRED** services (16 of 24) have no V2 equivalent at all
- The highest-value services for V2 are: `visite_property`, `contre_visite`, `mise_en_location`, `mise_en_vente`, `publication`, `estimation_immobiliere`
- `estimation_immobiliere` (SVC-ESTI-001) should be prioritized as it directly feeds the matching pipeline

---

## 4. Professional Services Mapping

**Source:** Heritage Gold MATRIX_CATALOG.md §6 — 27 professional service matrices (PRO- prefix, transaction_type: FIND)

### 4.1 Mapping to LAWIM V2 Business Profiles

| Matrix ID | Professional Service | V2 Business Profile | Matching Role | Mapping Status | Confidence |
|---|---|---|---|---|---|
| PRO-AGENT-001 | agent_immobilier | `real_estate_agent` | EXACT | NORMALIZED_MATCH | HIGH |
| PRO-AGENC-002 | agence_immobiliere | `real_estate_agent` | MANY_TO_ONE | NORMALIZED_MATCH | HIGH |
| PRO-NOTAI-003 | notaire | `notary` | EXACT | NORMALIZED_MATCH | HIGH |
| PRO-GEOME-004 | geometre | `surveyor` | EXACT | NORMALIZED_MATCH | HIGH |
| PRO-ARCHI-005 | architecte | `architect` | EXACT | NORMALIZED_MATCH | HIGH |
| PRO-INGEN-006 | ingenieur_genie_civil | `engineer` | EXACT | NORMALIZED_MATCH | HIGH |
| PRO-TECHN-007 | technicien_batiment | `technician` | EXACT | NORMALIZED_MATCH | HIGH |
| PRO-MACON-008 | macon | N/A | UNMAPPED | EXTENSION_REQUIRED | — |
| PRO-ELECT-009 | electricien | `electrician` | EXACT | NORMALIZED_MATCH | HIGH |
| PRO-PLOMB-010 | plombier | `plumber` | EXACT | NORMALIZED_MATCH | HIGH |
| PRO-MENUI-011 | menuisier | N/A | UNMAPPED | EXTENSION_REQUIRED | — |
| PRO-PEINT-012 | peintre | N/A | UNMAPPED | EXTENSION_REQUIRED | — |
| PRO-CARRE-013 | carreleur | N/A | UNMAPPED | EXTENSION_REQUIRED | — |
| PRO-COUVR-014 | couvreur | N/A | UNMAPPED | EXTENSION_REQUIRED | — |
| PRO-EXPIM-015 | expert_immobilier | N/A | UNMAPPED | EXTENSION_REQUIRED | — |
| PRO-EVALU-016 | evaluateur | N/A | UNMAPPED | EXTENSION_REQUIRED | — |
| PRO-GESTI-017 | gestionnaire_immobilier | `property_manager` | EXACT | NORMALIZED_MATCH | HIGH |
| PRO-SYNDI-018 | syndic | N/A | UNMAPPED | EXTENSION_REQUIRED | — |
| PRO-PHOTO-019 | photographe_immobilier | `photographer` | EXACT | NORMALIZED_MATCH | HIGH |
| PRO-VIDEO-020 | videaste_drone | N/A | UNMAPPED | EXTENSION_REQUIRED | — |
| PRO-DEMEN-021 | demenageur | `mover` | NORMALIZED | NORMALIZED_MATCH | HIGH |
| PRO-NETTO-022 | entreprise_nettoyage | `cleaner` | NORMALIZED | NORMALIZED_MATCH | HIGH |
| PRO-GARDI-023 | gardiennage | N/A | UNMAPPED | EXTENSION_REQUIRED | — |
| PRO-ASSUR-024 | assureur | `insurer` | EXACT | NORMALIZED_MATCH | HIGH |
| PRO-BANQU-025 | banque_microfinance | `bank` | NORMALIZED | NORMALIZED_MATCH | HIGH |
| PRO-COURT-026 | courtier | N/A | UNMAPPED | EXTENSION_REQUIRED | — |
| PRO-PREST-027 | prestataire_administratif | N/A | UNMAPPED | EXTENSION_REQUIRED | — |

### 4.2 Analysis

- **17 of 27** professional services map to existing `business_profiles.py` roles (NORMALIZED_MATCH)
- **10 of 27** have no V2 equivalent (EXTENSION_REQUIRED): macon, menuisier, peintre, carreleur, couvreur, expert_immobilier, evaluateur, syndic, videaste_drone, gardiennage, courtier, prestataire_administratif
- **CRITICAL DISTINCTION:** Heritage Gold treats these as FIND-type service matrices with full qualification pipelines (intake → search → matching → introduction → execution). V2 `business_profiles.py` treats them as **user role labels only** — no qualification matrix, no matching criteria, no service execution flow.

### 4.3 Nomenclature Differences

| Heritage Gold | LAWIM V2 | Notes |
|---|---|---|
| agent_immobilier | real_estate_agent | Different snake_case convention |
| notaire | notary | French vs English label |
| geometre | surveyor | Semantic equivalent |
| agence_immobiliere | real_estate_agent (merged) | Heritage distinguishes agent vs agency; V2 uses one role |
| demenageur | mover | Different naming convention |
| banque_microfinance | bank | Heritage specific; V2 generic |
| entreprise_nettoyage | cleaner | Heritage specific; V2 generic |

---

## 5. CRM Monetized Services Mapping

**Source:** Heritage Gold CRM_MODEL.md §14 + §14 legacy

### 5.1 Lead Packs

| Heritage Service | Code | Price (FCFA) | V2 Status | Mapping Status | Priority |
|---|---|---|---|---|---|
| Lead Bronze (1 contact) | lead_bronze | 500 | Agent credit system exists in heritage; not in V2 | EXTENSION_REQUIRED | HIGH |
| Lead Silver (5 contacts) | lead_silver | 1 500 | Bulk discount variant of lead_bronze | EXTENSION_REQUIRED | HIGH |
| Lead Gold (15 contacts) | lead_gold | 3 000 | Bulk discount variant of lead_bronze | EXTENSION_REQUIRED | HIGH |

### 5.2 Transaction Services

| Heritage Service | Code | Price (FCFA) | V2 Status | Mapping Status | Priority |
|---|---|---|---|---|---|
| Déblocage coordonnées propriétaire | deblocage_coordonnees | 500 | No owner contact unlock mechanism | EXTENSION_REQUIRED | HIGH |
| Demandeur Premium | demandeur_premium | 1 000 | No premium seeker profile | EXTENSION_REQUIRED | LOW |

### 5.3 Diaspora Services

| Heritage Service | Code | Price (FCFA) | V2 Status | Mapping Status | Priority |
|---|---|---|---|---|---|
| Diaspora Simple | diaspora_simple | 25 000 | Diaspora detection exists in qualification; no paid service | EXTENSION_REQUIRED | MEDIUM |
| Diaspora Rapport | diaspora_rapport | 50 000 | No diaspora-specific report service | EXTENSION_REQUIRED | MEDIUM |
| Diaspora Complet | diaspora_complet | 75 000 | No full diaspora accompaniment | EXTENSION_REQUIRED | MEDIUM |

### 5.4 Agent Business Subscription

| Heritage Service | Code | Price (FCFA) | V2 Status | Mapping Status | Priority |
|---|---|---|---|---|---|
| Abonnement Agent Business | agent_business | 25 000/mois | No subscription system | EXTENSION_REQUIRED | HIGH |

---

## 6. Service Lifecycle Comparison

### Heritage Gold Service Lifecycle

```
Discovery → Qualification → Quotation → Payment → Fulfillment → Completion → Review
```

| Stage | Heritage Gold Implementation | V2 Implementation |
|---|---|---|
| **Catalog/Browsing** | MATRIX_CATALOG.md with 107 matrices across 6 families | No service catalog |
| **Qualification** | Matrix-specific minimum_intake_fields for each service | Generic `Project` with `project_type` field |
| **Quotation/Pricing** | Fixed prices in DOMAIN_MODEL.md §9 + CRM_MODEL.md §14 | No pricing model |
| **Payment** | Campay Mobile Money integration (`payments=OFF`) | `/api/v2/financial/payments/*` endpoints exist but `payments_enabled=True` |
| **Fulfillment** | Matrix-specific execution fields (contrat_service, conditions_paiement, etc.) | No service fulfillment |
| **Completion** | Event types: `payment.success`, `boost.applied`, `subscription.renewed` | `Event` model exists with generic payload |
| **Review/Rating** | Agent rating (1-5 stars), customer satisfaction tracking | `Notification` model exists; no feedback loop |

### LAWIM V2 Lifecycle (Current)

```
Project Creation → Step Tracking → Completion
```

V2 uses `Project` → `ProjectStep` → `ProjectStepHistory` for generic project management, with no service-specific semantics.

### Gap Summary

| Lifecycle Stage | Heritage Gold | LAWIM V2 | Gap |
|---|---|---|---|
| Service Definition | Full catalog (72 items) | None | EXTENSION_REQUIRED |
| Classification | 6 families × service-specific matrices | `Project.project_type` (string) | MAJOR |
| Pricing | Fixed prices, tiers, subscriptions | None | EXTENSION_REQUIRED |
| Payment | Campay, Mobile Money, credits | API exists, feature flag OFF | PARTIAL_MATCH |
| Agent Credits | `agent_credits` table | None | EXTENSION_REQUIRED |
| Service Routing | Zone-based agent routing | No routing | EXTENSION_REQUIRED |
| Fulfillment | Matrix-specific execution fields | `ProjectStep` (generic) | MAJOR |
| Rating/Review | 1-5 stars after service | None | EXTENSION_REQUIRED |

---

## 7. Gap Analysis

### 7.1 Critical Gaps (Must Address for V2 Service Implementation)

| Gap ID | Description | Heritage Reference | V2 Impact | Suggested Approach |
|---|---|---|---|---|
| GAP-SVC-001 | No `Service` or `ServiceCatalog` Prisma model | DOMAIN_MODEL.md §9 | Cannot store, price, or order services | Add `Service` and `ServiceOrder` models |
| GAP-SVC-002 | No payment processing active | CRM_MODEL.md §16, GOLD-DM-088 | Feature flag `payments=OFF` | Enable Campay integration, activate payments |
| GAP-SVC-003 | No agent credit/lead purchase system | CRM_MODEL.md §14.1, GOLD-RL-038 | No monetization of core matching | Implement `AgentCredit` + `LeadPurchase` |
| GAP-SVC-004 | No service order lifecycle | MATRIX_CATALOG.md full pipeline | No fulfillment tracking | Extend `Project` with service semantics |
| GAP-SVC-005 | No boost/premium listing system | GOLD-DM-062/063/064 | No paid visibility for properties | Add `boost_level` + `premium` to `Property` |

### 7.2 Moderate Gaps

| Gap ID | Description | Heritage Reference | Priority |
|---|---|---|---|
| GAP-SVC-006 | Missing 10 professional roles in business_profiles.py | MATRIX_CATALOG.md §6 | MEDIUM |
| GAP-SVC-007 | No diaspora service fulfillment | CRM_MODEL.md §14.3 | LOW (feature flag OFF) |
| GAP-SVC-008 | No service-specific qualification matrices | 24 SVC- matrices | MEDIUM |
| GAP-SVC-009 | No subscription management for agents | GOLD-DM-065 agent_pro | MEDIUM |

### 7.3 Minor Gaps

| Gap ID | Description | Heritage Reference | Priority |
|---|---|---|---|
| GAP-SVC-010 | No photography/video service ordering | SVC-PHOT-010, SVC-VIDE-011 | LOW |
| GAP-SVC-011 | No rating/review after service fulfillment | CRM_MODEL.md §13 | LOW |
| GAP-SVC-012 | Missing document verification service | GOLD-DM-068 controle_documentaire | LOW |

### 7.4 Aggregated Statistics

| Category | Count | Percentage |
|---|---|---|
| Total Heritage Services | 72 | 100% |
| EXACT_MATCH | 0 | 0% |
| NORMALIZED_MATCH | 17 | 23.6% |
| ONE_TO_MANY | 0 | 0% |
| MANY_TO_ONE | 1 | 1.4% |
| PARTIAL_MATCH | 8 | 11.1% |
| EXTENSION_REQUIRED | 46 | 63.9% |
| OBSOLETE | 0 | 0% |
| CONFLICT | 0 | 0% |
| HUMAN_DECISION_REQUIRED | 0 | 0% |
| UNMAPPED | 0 | 0% |

### 7.5 Priority Recommendations

1. **Phase 1 (IMMEDIATE):** Implement `Service` + `ServiceOrder` Prisma models to close GAP-SVC-001
2. **Phase 1 (IMMEDIATE):** Activate `payments` feature flag + enable Campay integration (GAP-SVC-002)
3. **Phase 1 (IMMEDIATE):** Implement agent credit system (GAP-SVC-003) — core to LAWIM monetization model
4. **Phase 2 (SHORT-TERM):** Add boost/premium to Property model (GAP-SVC-005) — quick revenue win
5. **Phase 2 (SHORT-TERM):** Extend `Project` to support service order lifecycle (GAP-SVC-004)
6. **Phase 3 (MEDIUM-TERM):** Add 10 missing professional roles to business_profiles.py (GAP-SVC-006)
7. **Phase 3 (MEDIUM-TERM):** Implement top 4 real estate service matrices (visite, contre-visite, mise_en_location, estimation) (GAP-SVC-008)
8. **Phase 4 (LONG-TERM):** Full diaspora service suite, subscriptions, rating system

---

*End of SERVICE_CROSSWALK.md*
