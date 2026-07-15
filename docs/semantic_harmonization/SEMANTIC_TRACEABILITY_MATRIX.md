# Semantic Traceability Matrix — Heritage Gold → LAWIM_V2

**Document ID:** LAWIM-HARM-TRACEABILITY-MATRIX-V1
**Status:** CANONICAL — Complete traceability chain for all Heritage Gold concepts
**Date:** 2026-07-15
**Traceability Chain:** Heritage Gold → Crosswalk → Unified Domain Concept → LAWIM_V2 Target → H1 Contract → H2 Component → Test Contract

---

## Traceability Status Legend

| Status | Description |
|--------|-------------|
| **TRACEABLE** | Full end-to-end chain exists; concept is implemented or precisely specified |
| **PARTIALLY_TRACEABLE** | Chain exists but has gaps (partial implementation, pending extension, or incomplete mapping) |
| **NOT_TRACEABLE** | Concept cannot be traced — missing crosswalk, no V2 target, or no H1 contract |

---

## Table of Contents

1. [Role Concepts (GOLD-RL-001 to GOLD-RL-061)](#1-role-concepts)
2. [Property Concepts (GOLD-PR-001 to GOLD-PR-122)](#2-property-concepts)
3. [Domain Model Concepts (GOLD-DM-001 to GOLD-DM-096)](#3-domain-model-concepts)
4. [Matching Concepts (GE-MATCH-001 to GE-MATCH-025)](#4-matching-concepts)
5. [Qualification Matrices (107 entries)](#5-qualification-matrices)
6. [Workflows (21 entries)](#6-workflows)
7. [Services (72+ entries)](#7-services)
8. [Intent & Transaction Concepts](#8-intent--transaction-concepts)
9. [Qualitative Knowledge Items](#9-qualitative-knowledge-items)
10. [Coverage Summary](#10-coverage-summary)

---

## 1. Role Concepts

Crosswalk: `ROLE_CROSSWALK.md` → Unified: User/Role Model → V2 Target: `user_roles.py`, `business_profiles.py` → H1: `IDENTITY_RESOLUTION_CONTRACT.md` → H2: Role Engine

### 1.1 Role Families (GOLD-RL-001 to GOLD-RL-006)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-RL-001 | Demandeur family (buyer, tenant, investor, property_seeker) | ROLE_CROSSWALK.md | XW-RL-001 | User/Role Model | `official_role="user"` + `business_profile ∈ {buyer, tenant, land_seeker, investor}` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Profile Resolver | TBD | TRACEABLE |
| GOLD-RL-002 | Proprietaire family (owner, seller, détenteur) | ROLE_CROSSWALK.md | XW-RL-002 | User/Role Model | `official_role="user"` + `business_profile="owner"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Profile Resolver | TBD | TRACEABLE |
| GOLD-RL-003 | Agent family (agent_immobilier, broker) | ROLE_CROSSWALK.md | XW-RL-003 | User/Role Model | `official_role="operator"` + `business_profile="real_estate_agent"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Operator Profile | TBD | TRACEABLE |
| GOLD-RL-004 | Operateur family (responsable_agence, administrateur_agence, assistant) | ROLE_CROSSWALK.md | XW-RL-004 | User/Role Model | `official_role="operator"` or `"manager"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Agency Role Extension | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-005 | Superviseur family (conseiller, médiateur, responsable_opérationnel) | ROLE_CROSSWALK.md | XW-RL-005 | User/Role Model | `official_role="manager"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Manager Profile | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-006 | Admin family (administrateur, administrateur_principal) | ROLE_CROSSWALK.md | XW-RL-006 | User/Role Model | `official_role="admin"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Admin Profile | TBD | TRACEABLE |

### 1.2 Role Hierarchy (GOLD-RL-007 to GOLD-RL-013)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-RL-007 | demandeur (Level 1) | ROLE_CROSSWALK.md | XW-RL-007 | User/Role Model | `official_role="user"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Base User | TBD | TRACEABLE |
| GOLD-RL-008 | vendeur/propriétaire (Level 2) | ROLE_CROSSWALK.md | XW-RL-008 | User/Role Model | `official_role="user"` + `business_profile="owner"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Owner Profile | TBD | TRACEABLE |
| GOLD-RL-009 | agent (Level 3) | ROLE_CROSSWALK.md | XW-RL-009 | User/Role Model | `official_role="operator"` + `business_profile="real_estate_agent"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Operator Profile | TBD | TRACEABLE |
| GOLD-RL-010 | agence (Level 4) | ROLE_CROSSWALK.md | XW-RL-010 | User/Role Model / Organization | Organization model exists; no agency-level role | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Organization Role Extension | TBD | NOT_TRACEABLE |
| GOLD-RL-011 | assistant (Level 5) | ROLE_CROSSWALK.md | XW-RL-011 | User/Role Model | `official_role="operator"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Agency Role Extension | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-012 | vice_master (Level 6) | ROLE_CROSSWALK.md | XW-RL-012 | User/Role Model | `official_role="manager"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Manager Profile | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-013 | master (Level 7) | ROLE_CROSSWALK.md | XW-RL-013 | User/Role Model | `official_role="admin"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Admin Profile | TBD | PARTIALLY_TRACEABLE |

### 1.3 Permission Levels (GOLD-RL-014 to GOLD-RL-017)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-RL-014 | Niveau 1 — Lecture (Read) | ROLE_CROSSWALK.md | XW-RL-014 | Authorization | Implicit read access via role | IDENTITY_RESOLUTION_CONTRACT.md | Permission Engine — Read Evaluator | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-015 | Niveau 2 — Création (Create) | ROLE_CROSSWALK.md | XW-RL-015 | Authorization | Implicit create access; operator+ can create listings | IDENTITY_RESOLUTION_CONTRACT.md | Permission Engine — Create Evaluator | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-016 | Niveau 3 — Modification (Edit) | ROLE_CROSSWALK.md | XW-RL-016 | Authorization | Implicit edit access; users edit own, operators edit managed | IDENTITY_RESOLUTION_CONTRACT.md | Permission Engine — Edit Scoping | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-017 | Niveau 4 — Validation (Approve) | ROLE_CROSSWALK.md | XW-RL-017 | Authorization | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Permission Engine — Approval Workflow | TBD | NOT_TRACEABLE |

### 1.4 Trust Levels (GOLD-RL-018 to GOLD-RL-023)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-RL-018 | Niveau 1 — Nouveau compte | ROLE_CROSSWALK.md | XW-RL-018 | Trust/Security | Not implemented — requires `trust_level` field | IDENTITY_RESOLUTION_CONTRACT.md | Trust Engine — Trust Level Manager | TBD | NOT_TRACEABLE |
| GOLD-RL-019 | Niveau 2 — Téléphone vérifié | ROLE_CROSSWALK.md | XW-RL-019 | Trust/Security | Not implemented — requires `phone_verified` flag | IDENTITY_RESOLUTION_CONTRACT.md | Trust Engine — Phone Verification | TBD | NOT_TRACEABLE |
| GOLD-RL-020 | Niveau 3 — Identité vérifiée | ROLE_CROSSWALK.md | XW-RL-020 | Trust/Security | Not implemented — requires `identity_verified` field | IDENTITY_RESOLUTION_CONTRACT.md | Trust Engine — Identity Verification | TBD | NOT_TRACEABLE |
| GOLD-RL-021 | Niveau 4 — Documents pro validés | ROLE_CROSSWALK.md | XW-RL-021 | Trust/Security | Not implemented — requires `professional_docs_verified` | IDENTITY_RESOLUTION_CONTRACT.md | Trust Engine — Document Verification | TBD | NOT_TRACEABLE |
| GOLD-RL-022 | Niveau 5 — Professionnel vérifié | ROLE_CROSSWALK.md | XW-RL-022 | Trust/Security | Not implemented — requires `professional_verified` | IDENTITY_RESOLUTION_CONTRACT.md | Trust Engine — Professional Verification | TBD | NOT_TRACEABLE |
| GOLD-RL-023 | Niveau 6 — Compte de référence | ROLE_CROSSWALK.md | XW-RL-023 | Trust/Security | Not implemented — requires `reference_account` field | IDENTITY_RESOLUTION_CONTRACT.md | Trust Engine — Reference Account Manager | TBD | NOT_TRACEABLE |

### 1.5 Badges (GOLD-RL-024 to GOLD-RL-031)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-RL-024 | Badge: Téléphone vérifié | ROLE_CROSSWALK.md | XW-RL-024 | Badge/Reward | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Badge Engine — Trust Badge Renderer | TBD | NOT_TRACEABLE |
| GOLD-RL-025 | Badge: E-mail vérifié | ROLE_CROSSWALK.md | XW-RL-025 | Badge/Reward | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Badge Engine — Trust Badge Renderer | TBD | NOT_TRACEABLE |
| GOLD-RL-026 | Badge: Identité vérifiée | ROLE_CROSSWALK.md | XW-RL-026 | Badge/Reward | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Badge Engine — Trust Badge Renderer | TBD | NOT_TRACEABLE |
| GOLD-RL-027 | Badge: Propriétaire vérifié | ROLE_CROSSWALK.md | XW-RL-027 | Badge/Reward | Not implemented — requires `owner_verified` | IDENTITY_RESOLUTION_CONTRACT.md | Badge Engine — Owner Verification Badge | TBD | NOT_TRACEABLE |
| GOLD-RL-028 | Badge: Agence vérifiée | ROLE_CROSSWALK.md | XW-RL-028 | Badge/Reward | Not implemented — requires `agency_verified` on Organization | IDENTITY_RESOLUTION_CONTRACT.md | Badge Engine — Agency Verification Badge | TBD | NOT_TRACEABLE |
| GOLD-RL-029 | Badge: Partenaire LAWIM | ROLE_CROSSWALK.md | XW-RL-029 | Badge/Reward | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Badge Engine — Partner Badge | TBD | NOT_TRACEABLE |
| GOLD-RL-030 | Badge: Professionnel vérifié | ROLE_CROSSWALK.md | XW-RL-030 | Badge/Reward | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Badge Engine — Professional Badge | TBD | NOT_TRACEABLE |
| GOLD-RL-031 | Badge: Agent actif | ROLE_CROSSWALK.md | XW-RL-031 | Badge/Reward | Not implemented — requires `is_active_agent` | IDENTITY_RESOLUTION_CONTRACT.md | Badge Engine — Active Agent Badge | TBD | NOT_TRACEABLE |

### 1.6 Agency Structure (GOLD-RL-032 to GOLD-RL-040)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-RL-032 | Agency definition (organization) | ROLE_CROSSWALK.md | XW-RL-032 | Organization Model | `prisma.Organization` model | IDENTITY_RESOLUTION_CONTRACT.md | Organization Engine — Agency Definition | TBD | TRACEABLE |
| GOLD-RL-033 | Agency components (responsible + agents + admin + properties + files + validations + trust) | ROLE_CROSSWALK.md | XW-RL-033 | Organization Model | Organization has users + properties; missing trust/validations | IDENTITY_RESOLUTION_CONTRACT.md | Organization Engine — Agency Trust Manager | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-034 | Agency creation (name, resp., phone, address, CNI, RCCM, tax ID) | ROLE_CROSSWALK.md | XW-RL-034 | Organization Model | Organization creation exists; missing RCCM/CNI/tax fields | IDENTITY_RESOLUTION_CONTRACT.md | Organization Engine — Agency Registration | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-035 | Agent onboarding flow | ROLE_CROSSWALK.md | XW-RL-035 | Agency/Onboarding | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Onboarding Engine — Agent Onboarding State Machine | TBD | NOT_TRACEABLE |
| GOLD-RL-036 | Minimum 3 active agents for operational agency | ROLE_CROSSWALK.md | XW-RL-036 | Agency/Operations | Not implemented | N/A | Organization Engine — Agent Count Validation | TBD | NOT_TRACEABLE |
| GOLD-RL-037 | Lead routing by geographic zone | ROLE_CROSSWALK.md | XW-RL-037 | Agency/Lead Management | Not implemented | CRM_PIPELINE_CONTRACT.md | Lead Routing Engine — Geographic Zone Router | TBD | NOT_TRACEABLE |
| GOLD-RL-038 | Lead cost (500 FCFA default) | ROLE_CROSSWALK.md | XW-RL-038 | Agency/Lead Management | Not implemented | CRM_PIPELINE_CONTRACT.md | Billing Engine — Lead Costing Module | TBD | NOT_TRACEABLE |
| GOLD-RL-039 | Agent credits & boosts | ROLE_CROSSWALK.md | XW-RL-039 | Agency/Lead Management | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Billing Engine — Agent Credit System | TBD | NOT_TRACEABLE |
| GOLD-RL-040 | Agent rating (1-5) | ROLE_CROSSWALK.md | XW-RL-040 | Agency/Quality | Not implemented | CRM_PIPELINE_CONTRACT.md | Rating Engine — Agent Rating Calculator | TBD | NOT_TRACEABLE |

### 1.7 Role-to-Journey Coverage (GOLD-RL-041 to GOLD-RL-048)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-RL-041 | Property search journey | ROLE_CROSSWALK.md | XW-RL-041 | Journey/Qualification | Supported via user role + buyer/tenant/land_seeker/investor profiles | QUALIFICATION_MATRIX_CONTRACT.md | Journey Engine — Search Journey | TBD | TRACEABLE |
| GOLD-RL-042 | Property listing journey | ROLE_CROSSWALK.md | XW-RL-042 | Journey/Listing | Supported via operator role + real_estate_agent profile or user role + owner profile | QUALIFICATION_MATRIX_CONTRACT.md | Journey Engine — Listing Journey | TBD | TRACEABLE |
| GOLD-RL-043 | Matching & proposals journey | ROLE_CROSSWALK.md | XW-RL-043 | Journey/Matching | Partially supported; matching engine exists but proposal workflows may differ | MATCHING_EXECUTION_ARCHITECTURE.md | Journey Engine — Matching Journey | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-044 | Visit scheduling journey | ROLE_CROSSWALK.md | XW-RL-044 | Journey/Visit | Supported; visit scheduling available for all relevant roles | WORKFLOW_EXECUTION_ARCHITECTURE.md | Journey Engine — Visit Journey | TBD | TRACEABLE |
| GOLD-RL-045 | Negotiation journey | ROLE_CROSSWALK.md | XW-RL-045 | Journey/Negotiation | Partially supported; Conversation.negotiation_stage exists | NEGOTIATION_STRATEGY_CONTRACT.md | Journey Engine — Negotiation Journey | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-046 | Transaction journey | ROLE_CROSSWALK.md | XW-RL-046 | Journey/Transaction | Partially supported; no transaction object in V2 | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Transaction State Machine | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-047 | Post-sale follow-up journey | ROLE_CROSSWALK.md | XW-RL-047 | Journey/Follow-up | Limited support; no dedicated post-sale workflows | CRM_PIPELINE_CONTRACT.md | Journey Engine — Post-Sale Follow-up | TBD | NOT_TRACEABLE |
| GOLD-RL-048 | Admin supervision journey | ROLE_CROSSWALK.md | XW-RL-048 | Journey/Admin | Supported via admin role | IDENTITY_RESOLUTION_CONTRACT.md | Journey Engine — Admin Supervision | TBD | TRACEABLE |

### 1.8 Partner Roles (GOLD-RL-055 to GOLD-RL-061)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-RL-055 | Notaire | ROLE_CROSSWALK.md | XW-RL-055 | Partner Role Model | `official_role="partner"` + `business_profile="notary"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Partner Profile Resolver | TBD | TRACEABLE |
| GOLD-RL-056 | Géomètre | ROLE_CROSSWALK.md | XW-RL-056 | Partner Role Model | `official_role="partner"` + `business_profile="surveyor"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Partner Profile Resolver | TBD | TRACEABLE |
| GOLD-RL-057 | Banque | ROLE_CROSSWALK.md | XW-RL-057 | Partner Role Model | `official_role="partner"` + `business_profile ∈ {"bank", "financing"}` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Partner Profile Resolver | TBD | TRACEABLE |
| GOLD-RL-058 | Assurance | ROLE_CROSSWALK.md | XW-RL-058 | Partner Role Model | `official_role="partner"` + `business_profile="insurer"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Partner Profile Resolver | TBD | TRACEABLE |
| GOLD-RL-059 | Photographe | ROLE_CROSSWALK.md | XW-RL-059 | Partner Role Model | `official_role="partner"` + `business_profile="photographer"` | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Partner Profile Resolver | TBD | TRACEABLE |
| GOLD-RL-060 | Artisan | ROLE_CROSSWALK.md | XW-RL-060 | Partner Role Model | `official_role="partner"` + business_profile ∈ {architect, engineer, technician, contractor, decorator, electrician, plumber, cleaner, mover} | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Artisan Profile Resolver | TBD | PARTIALLY_TRACEABLE |
| GOLD-RL-061 | Expert partenaire | ROLE_CROSSWALK.md | XW-RL-061 | Partner Role Model | `official_role="partner"` + business_profile ∈ {architect, engineer, surveyor, lawyer} | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Expert Profile Resolver | TBD | PARTIALLY_TRACEABLE |

---

## 2. Property Concepts

Crosswalk: `PROPERTY_TYPE_CROSSWALK.md` → Unified: Property/Listing Model → V2 Target: Property entity (prisma) + `metadata_json` → H1: `QUALIFICATION_MATRIX_CONTRACT.md` → H2: Property Engine

### 2.1 Property Families (GOLD-PR-001 to GOLD-PR-007)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-PR-001 | Résidentiel (Residential family) | PROPERTY_TYPE_CROSSWALK.md | CW-FAMILY-001 | Property Family Model | Free-form `propertyType`; no family enum | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Family Classifier | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-002 | Commercial family | PROPERTY_TYPE_CROSSWALK.md | CW-FAMILY-002 | Property Family Model | Free-form `propertyType`; no family enum | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Family Classifier | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-003 | Industriel family | PROPERTY_TYPE_CROSSWALK.md | CW-FAMILY-003 | Property Family Model | Not represented | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Industrial Sub-Engine | TBD | NOT_TRACEABLE |
| GOLD-PR-004 | Foncier/Terrain (Land family) | PROPERTY_TYPE_CROSSWALK.md | CW-FAMILY-004 | Property Family Model | `property_type='land'` (free-form, no special handling) | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Land Sub-Engine | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-005 | Agricole (Agricultural family) | PROPERTY_TYPE_CROSSWALK.md | CW-FAMILY-005 | Property Family Model | Not represented | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Agricultural Sub-Engine | TBD | NOT_TRACEABLE |
| GOLD-PR-006 | Hôtelier (Hotel family) | PROPERTY_TYPE_CROSSWALK.md | CW-FAMILY-006 | Property Family Model | Not represented; hotel as commercial type only | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Hotel Sub-Engine | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-007 | Projet immobilier (Real estate project family) | PROPERTY_TYPE_CROSSWALK.md | CW-FAMILY-007 | Property/Project Model | Separate Project model; not a property family | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Project Property Link | TBD | PARTIALLY_TRACEABLE |

### 2.2 Basic Property Types (GOLD-PR-034 to GOLD-PR-044)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-PR-034 | appartement | PROPERTY_TYPE_CROSSWALK.md | CW-TYPE-001 | Property Type Model | Free-form string; commonly 'apartment' or 'appartement' | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Type Normalizer | TBD | TRACEABLE |
| GOLD-PR-035 | maison | PROPERTY_TYPE_CROSSWALK.md | CW-TYPE-002 | Property Type Model | Free-form string | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Type Normalizer | TBD | TRACEABLE |
| GOLD-PR-036 | villa | PROPERTY_TYPE_CROSSWALK.md | CW-TYPE-003 | Property Type Model | Free-form string | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Type Normalizer | TBD | TRACEABLE |
| GOLD-PR-037 | studio | PROPERTY_TYPE_CROSSWALK.md | CW-TYPE-004 | Property Type Model | Free-form string | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Type Normalizer | TBD | TRACEABLE |
| GOLD-PR-038 | duplex | PROPERTY_TYPE_CROSSWALK.md | CW-TYPE-005 | Property Type Model | Free-form string | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Type Normalizer | TBD | TRACEABLE |
| GOLD-PR-039 | chambre | PROPERTY_TYPE_CROSSWALK.md | CW-TYPE-006 | Property Type Model | Free-form string | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Type Normalizer | TBD | TRACEABLE |
| GOLD-PR-040 | immeuble | PROPERTY_TYPE_CROSSWALK.md | CW-TYPE-007 | Property Type Model | Free-form string | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Type Normalizer | TBD | TRACEABLE |
| GOLD-PR-041 | terrain | PROPERTY_TYPE_CROSSWALK.md | CW-TYPE-008 | Property Type Model | Free-form string (commonly 'land' or 'terrain') | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Land Type Normalizer | TBD | TRACEABLE |
| GOLD-PR-042 | boutique | PROPERTY_TYPE_CROSSWALK.md | CW-TYPE-009 | Property Type Model | Free-form string | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Type Normalizer | TBD | TRACEABLE |
| GOLD-PR-043 | entrepôt | PROPERTY_TYPE_CROSSWALK.md | CW-TYPE-010 | Property Type Model | Free-form string | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Industrial Type Normalizer | TBD | TRACEABLE |
| GOLD-PR-044 | bureau | PROPERTY_TYPE_CROSSWALK.md | CW-TYPE-011 | Property Type Model | Free-form string | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Type Normalizer | TBD | TRACEABLE |

### 2.3 Residential Matrix Types (GOLD-PR-045 to GOLD-PR-062)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-PR-045 | chambre_simple | PROPERTY_TYPE_CROSSWALK.md | CW-RES-001 | Property Type Model | Not represented as distinct type → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Residential Sub-Engine | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-046 | chambre_moderne | PROPERTY_TYPE_CROSSWALK.md | CW-RES-002 | Property Type Model | Not represented as distinct type → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Residential Sub-Engine | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-047 | studio_moderne | PROPERTY_TYPE_CROSSWALK.md | CW-RES-004 | Property Type Model | Not represented as distinct type → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Residential Sub-Engine | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-048 | studio_meuble | PROPERTY_TYPE_CROSSWALK.md | CW-RES-005 | Property Type Model | Not represented; no `is_furnished` concept → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Furnishing Classifier | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-049 | appartement_non_meuble | PROPERTY_TYPE_CROSSWALK.md | CW-RES-006 | Property Type Model | Not distinguished from apartment → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Furnishing Classifier | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-050 | appartement_meuble | PROPERTY_TYPE_CROSSWALK.md | CW-RES-007 | Property Type Model | Not distinguished from apartment → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Furnishing Classifier | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-051 | villa_basse | PROPERTY_TYPE_CROSSWALK.md | CW-RES-009 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Residential Sub-Engine | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-052 | triplex | PROPERTY_TYPE_CROSSWALK.md | CW-RES-011 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Residential Sub-Engine | TBD | NOT_TRACEABLE |
| GOLD-PR-053 | maison_individuelle | PROPERTY_TYPE_CROSSWALK.md | CW-RES-012 | Property Type Model | Not distinguished from house → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Residential Sub-Engine | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-054 | maison_de_ville | PROPERTY_TYPE_CROSSWALK.md | CW-RES-013 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Residential Sub-Engine | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-055 | chambre_hotel | PROPERTY_TYPE_CROSSWALK.md | CW-RES-014 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Short-Stay Sub-Engine | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-056 | appartement_courte_duree | PROPERTY_TYPE_CROSSWALK.md | CW-RES-015 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Short-Stay Sub-Engine | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-057 | residence_meublee | PROPERTY_TYPE_CROSSWALK.md | CW-RES-016 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Residential Sub-Engine | TBD | NOT_TRACEABLE |
| GOLD-PR-058 | colocation | PROPERTY_TYPE_CROSSWALK.md | CW-RES-017 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Shared Housing Sub-Engine | TBD | NOT_TRACEABLE |
| GOLD-PR-059 | cite_universitaire | PROPERTY_TYPE_CROSSWALK.md | CW-RES-018 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Student Housing Sub-Engine | TBD | NOT_TRACEABLE |

### 2.4 Land Matrix Types (GOLD-PR-060 to GOLD-PR-066)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-PR-060 | terrain_titre (titled land) | PROPERTY_TYPE_CROSSWALK.md | CW-LAND-001 | Property Type Model | Not represented → `metadata_json.title_status='titled'` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Land Title Verifier | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-061 | terrain_non_titre (untitled land) | PROPERTY_TYPE_CROSSWALK.md | CW-LAND-002 | Property Type Model | Not represented → `metadata_json.title_status='untitled'` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Land Title Verifier | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-062 | terrain_loti (serviced land) | PROPERTY_TYPE_CROSSWALK.md | CW-LAND-003 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Land Service Checker | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-063 | terrain_non_loti (unserviced land) | PROPERTY_TYPE_CROSSWALK.md | CW-LAND-004 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Land Service Checker | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-064 | terrain_titre_collectif | PROPERTY_TYPE_CROSSWALK.md | CW-LAND-005 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Land Title Verifier | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-065 | terrain_titre_individuel | PROPERTY_TYPE_CROSSWALK.md | CW-LAND-006 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Land Title Verifier | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-066 | terrain_sous_morcellement | PROPERTY_TYPE_CROSSWALK.md | CW-LAND-007 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Land Subdivision Tracker | TBD | PARTIALLY_TRACEABLE |

### 2.5 Commercial Matrix Types (GOLD-PR-067 to GOLD-PR-082)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-PR-067 | local_commercial | PROPERTY_TYPE_CROSSWALK.md | CW-COM-003 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Classifier | TBD | NOT_TRACEABLE |
| GOLD-PR-068 | magasin | PROPERTY_TYPE_CROSSWALK.md | CW-COM-004 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Classifier | TBD | NOT_TRACEABLE |
| GOLD-PR-069 | hangar | PROPERTY_TYPE_CROSSWALK.md | CW-COM-006 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Classifier | TBD | NOT_TRACEABLE |
| GOLD-PR-070 | atelier | PROPERTY_TYPE_CROSSWALK.md | CW-COM-007 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Classifier | TBD | NOT_TRACEABLE |
| GOLD-PR-071 | restaurant | PROPERTY_TYPE_CROSSWALK.md | CW-COM-008 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Classifier | TBD | NOT_TRACEABLE |
| GOLD-PR-072 | bar | PROPERTY_TYPE_CROSSWALK.md | CW-COM-009 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Classifier | TBD | NOT_TRACEABLE |
| GOLD-PR-073 | hotel (commercial) | PROPERTY_TYPE_CROSSWALK.md | CW-COM-010 | Property Type Model | Not represented as distinct type → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Classifier | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-074 | auberge | PROPERTY_TYPE_CROSSWALK.md | CW-COM-011 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Classifier | TBD | NOT_TRACEABLE |
| GOLD-PR-075 | immeuble_de_rapport | PROPERTY_TYPE_CROSSWALK.md | CW-COM-012 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Income Property Classifier | TBD | NOT_TRACEABLE |
| GOLD-PR-076 | immeuble_commercial | PROPERTY_TYPE_CROSSWALK.md | CW-COM-013 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Classifier | TBD | NOT_TRACEABLE |
| GOLD-PR-077 | station_service | PROPERTY_TYPE_CROSSWALK.md | CW-COM-014 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Classifier | TBD | NOT_TRACEABLE |
| GOLD-PR-078 | site_industriel | PROPERTY_TYPE_CROSSWALK.md | CW-COM-015 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Industrial Sub-Engine | TBD | NOT_TRACEABLE |
| GOLD-PR-079 | espace_evenementiel | PROPERTY_TYPE_CROSSWALK.md | CW-COM-016 | Property Type Model | Not represented → `metadata_json` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Classifier | TBD | NOT_TRACEABLE |

### 2.6 Investment & Financing Types (GOLD-PR-083 to GOLD-PR-097)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-PR-083 | investissement_locatif | PROPERTY_TYPE_CROSSWALK.md | CW-INV-001 | Investment Model | Not represented → `metadata_json` | COMMERCIAL_EXECUTION_ARCHITECTURE.md | Investment Engine — Rental Investment | TBD | NOT_TRACEABLE |
| GOLD-PR-084 | investissement_terrain | PROPERTY_TYPE_CROSSWALK.md | CW-INV-002 | Investment Model | Not represented → `metadata_json` | COMMERCIAL_EXECUTION_ARCHITECTURE.md | Investment Engine — Land Investment | TBD | NOT_TRACEABLE |
| GOLD-PR-085 | investissement_immobilier_commercial | PROPERTY_TYPE_CROSSWALK.md | CW-INV-003 | Investment Model | Not represented → `metadata_json` | COMMERCIAL_EXECUTION_ARCHITECTURE.md | Investment Engine — Commercial Investment | TBD | NOT_TRACEABLE |
| GOLD-PR-086 | investissement_promotion | PROPERTY_TYPE_CROSSWALK.md | CW-INV-004 | Investment Model | Not represented → `metadata_json` | COMMERCIAL_EXECUTION_ARCHITECTURE.md | Investment Engine — Development Investment | TBD | NOT_TRACEABLE |
| GOLD-PR-087 | syndicat_copropriete | PROPERTY_TYPE_CROSSWALK.md | CW-INV-005 | Property/Community Model | Not represented → `metadata_json` | COMMERCIAL_EXECUTION_ARCHITECTURE.md | Property Engine — Condominium Manager | TBD | NOT_TRACEABLE |
| GOLD-PR-088 | credit_immobilier (through GOLD-PR-097) | PROPERTY_TYPE_CROSSWALK.md | CW-FIN-001-010 | Financing Model | Not represented → `Project` model (generic) | QUALIFICATION_MATRIX_CONTRACT.md | Financing Engine — Credit Matcher | TBD | NOT_TRACEABLE |

### 2.7 Lifecycle & Publication Rules (GOLD-PR-098 to GOLD-PR-110)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-PR-098 | Réception (step 1) | PROPERTY_TYPE_CROSSWALK.md | Lifecycle | Property Lifecycle | `draft` status (partial) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Reception Handler | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-099 | Normalisation (step 2) | PROPERTY_TYPE_CROSSWALK.md | Lifecycle | Property Lifecycle | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Normalization Step | TBD | NOT_TRACEABLE |
| GOLD-PR-100 | Classification (step 3) | PROPERTY_TYPE_CROSSWALK.md | Lifecycle | Property Lifecycle | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Classification Step | TBD | NOT_TRACEABLE |
| GOLD-PR-101 | Validation (step 4) | PROPERTY_TYPE_CROSSWALK.md | Lifecycle | Property Lifecycle | Embedded in create flow | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Validation Step | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-102 | Publication (step 5) | PROPERTY_TYPE_CROSSWALK.md | Lifecycle | Property Lifecycle | `published` status + `can_publish()` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Publication Handler | TBD | TRACEABLE |
| GOLD-PR-103 | Matching (step 6) | PROPERTY_TYPE_CROSSWALK.md | Lifecycle | Property Lifecycle | `published` status triggers matching | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Property Matcher | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-104 | Mise en relation (step 7) | PROPERTY_TYPE_CROSSWALK.md | Lifecycle | Property Lifecycle | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Contact Engine — Connection Handler | TBD | NOT_TRACEABLE |
| GOLD-PR-105 | Suivi (step 8) | PROPERTY_TYPE_CROSSWALK.md | Lifecycle | Property Lifecycle | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Follow-up Engine — Transaction Follow-up | TBD | NOT_TRACEABLE |
| GOLD-PR-106 | Archivage (step 9) | PROPERTY_TYPE_CROSSWALK.md | Lifecycle | Property Lifecycle | `archived` status | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Archive Handler | TBD | TRACEABLE |
| GOLD-PR-107 | Conservation historique (step 10) | PROPERTY_TYPE_CROSSWALK.md | Lifecycle | Property Lifecycle | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Archive Engine — Historical Preservation | TBD | NOT_TRACEABLE |

### 2.8 Publication Rules (GOLD-PR-108 to GOLD-PR-115)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-PR-108 | Family identified | PROPERTY_TYPE_CROSSWALK.md | Pub Rules | Property Publication | Not checked in `can_publish()` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Family Validator | TBD | NOT_TRACEABLE |
| GOLD-PR-109 | Type coherent | PROPERTY_TYPE_CROSSWALK.md | Pub Rules | Property Publication | Not checked in `can_publish()` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Type Coherence Checker | TBD | NOT_TRACEABLE |
| GOLD-PR-110 | Location known | PROPERTY_TYPE_CROSSWALK.md | Pub Rules | Property Publication | `city` must be present in `can_publish()` | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Location Validator | TBD | TRACEABLE |
| GOLD-PR-111 | Price provided | PROPERTY_TYPE_CROSSWALK.md | Pub Rules | Property Publication | `price_min` or `price_max` must be present | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Price Validator | TBD | TRACEABLE |
| GOLD-PR-112 | Détenteur identifiable | PROPERTY_TYPE_CROSSWALK.md | Pub Rules | Property Publication | `ownerOrganizationId` (optional, nullable) | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Holder Validator | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-113 | Critical info normalized | PROPERTY_TYPE_CROSSWALK.md | Pub Rules | Property Publication | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Normalization Checker | TBD | NOT_TRACEABLE |
| GOLD-PR-114 | Documents present | PROPERTY_TYPE_CROSSWALK.md | Pub Rules | Property Publication | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Document Engine — Document Presence Checker | TBD | NOT_TRACEABLE |

### 2.9 Price Concepts (GOLD-PR-116 to GOLD-PR-122)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-PR-116 | Prix affiché | PROPERTY_TYPE_CROSSWALK.md | Price | Price Model | `price_min` / `price_max` | MATCHING_SCORE_CONTRACT.md | Price Engine — Listed Price Handler | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-117 | Prix négociable | PROPERTY_TYPE_CROSSWALK.md | Price | Price Model | → `metadata_json.negotiable` | MATCHING_SCORE_CONTRACT.md | Price Engine — Negotiability Handler | TBD | PARTIALLY_TRACEABLE |
| GOLD-PR-118 | Prix final | PROPERTY_TYPE_CROSSWALK.md | Price | Price Model | Not stored | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Final Price Tracker | TBD | NOT_TRACEABLE |
| GOLD-PR-119 | Estimation | PROPERTY_TYPE_CROSSWALK.md | Price | Price Model | Not stored | MATCHING_SCORE_CONTRACT.md | Price Engine — Estimation Calculator | TBD | NOT_TRACEABLE |
| GOLD-PR-120 | Fourchette de marché | PROPERTY_TYPE_CROSSWALK.md | Price | Price Model | `price_min` / `price_max` (range) | MATCHING_SCORE_CONTRACT.md | Price Engine — Market Range Calculator | TBD | TRACEABLE |
| GOLD-PR-121 | Historique de variation | PROPERTY_TYPE_CROSSWALK.md | Price | Price Model | Not stored | MATCHING_SCORE_CONTRACT.md | Price Engine — Price History Tracker | TBD | NOT_TRACEABLE |
| GOLD-PR-122 | Loyer, Caution, Avance, Dépôt garantie, Mensualité, Frais service, Taxes | PROPERTY_TYPE_CROSSWALK.md | Price | Price Model | Not distinguished → `metadata_json` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Price Engine — Rent Component Resolver | TBD | PARTIALLY_TRACEABLE |

---

## 3. Domain Model Concepts

Crosswalk: Multiple documents → Unified: Multiple domains → V2 Target: Multiple entities → H1: Various contracts → H2: Various components

### 3.1 Core Domain Entities (GOLD-DM-001 to GOLD-DM-020)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-DM-001 | Property (Bien immobilier) | PROPERTY_TYPE_CROSSWALK.md | CW-FAMILY-001-007 | Property Model | `prisma.Property` model | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Core Property Handler | TBD | TRACEABLE |
| GOLD-DM-002 | User (Utilisateur) | ROLE_CROSSWALK.md | XW-RL-001-006 | User Model | `prisma.User` model | IDENTITY_RESOLUTION_CONTRACT.md | User Engine — Core User Handler | TBD | TRACEABLE |
| GOLD-DM-003 | Organization (Agence) | ROLE_CROSSWALK.md | XW-RL-032 | Organization Model | `prisma.Organization` model | IDENTITY_RESOLUTION_CONTRACT.md | Organization Engine — Core Org Handler | TBD | TRACEABLE |
| GOLD-DM-004 | Project (Dossier/Project) | INTENT_TRANSACTION_CROSSWALK.md | §1 | Project Model | `prisma.Project` model | QUALIFICATION_MATRIX_CONTRACT.md | Project Engine — Core Project Handler | TBD | TRACEABLE |
| GOLD-DM-005 | Conversation | INTENT_TRANSACTION_CROSSWALK.md | §5 | Conversation Model | `prisma.Conversation` model | CONVERSATION_EXECUTION_ARCHITECTURE.md | Conversation Engine — Core Conversation Handler | TBD | TRACEABLE |
| GOLD-DM-006 | Match (Correspondance) | MATCHING_COMPATIBILITY.md | §2 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Match Entity Manager | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-007 | Transaction | WORKFLOW_STATE_CROSSWALK.md | §2.07 | Transaction Model | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Transaction State Machine | TBD | NOT_TRACEABLE |
| GOLD-DM-008 | Visit (Visite) | WORKFLOW_STATE_CROSSWALK.md | §2.05 | Visit Model | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Visit Engine — Visit State Machine | TBD | NOT_TRACEABLE |
| GOLD-DM-009 | Negotiation (Négociation) | WORKFLOW_STATE_CROSSWALK.md | §2.06 | Negotiation Model | `Conversation.negotiation_stage` | NEGOTIATION_STRATEGY_CONTRACT.md | Negotiation Engine — Negotiation State Machine | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-010 | Lead (Piste) | WORKFLOW_STATE_CROSSWALK.md | §2.18 | CRM/Lead Model | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Lead Manager | TBD | NOT_TRACEABLE |
| GOLD-DM-011 | Event (Événement) | WORKFLOW_STATE_CROSSWALK.md | Appendix | Event Model | `prisma.Event` model (generic) | EVENT_EXECUTION_ARCHITECTURE.md | Event Engine — Event Publisher | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-012 | Media | SERVICE_CROSSWALK.md | §3 | Media Model | `prisma.Media` model | RESPONSE_STRATEGY_CONTRACT.md | Media Engine — Media Handler | TBD | TRACEABLE |
| GOLD-DM-013 | Notification | WORKFLOW_STATE_CROSSWALK.md | Cross-cutting | Notification Model | `prisma.Notification` model | CRM_PIPELINE_CONTRACT.md | Notification Engine — Notification Dispatcher | TBD | TRACEABLE |
| GOLD-DM-014 | Payment | SERVICE_CROSSWALK.md | §2 | Payment Model | `/api/v2/financial/payments/*` (feature-flagged OFF) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Payment Engine — Campay Integration | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-015 | Service (Service) | SERVICE_CROSSWALK.md | §1 | Service Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Service Catalog Manager | TBD | NOT_TRACEABLE |
| GOLD-DM-016 | Agent Credit | ROLE_CROSSWALK.md | XW-RL-039 | Billing Model | Not implemented | CRM_PIPELINE_CONTRACT.md | Billing Engine — Agent Credit Manager | TBD | NOT_TRACEABLE |
| GOLD-DM-017 | Subscription | SERVICE_CROSSWALK.md | §5.4 | Billing Model | Not implemented | CRM_PIPELINE_CONTRACT.md | Billing Engine — Subscription Manager | TBD | NOT_TRACEABLE |
| GOLD-DM-018 | Boost Purchase | ROLE_CROSSWALK.md | XW-RL-039 | Billing/Property Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Billing Engine — Boost Purchase Handler | TBD | NOT_TRACEABLE |
| GOLD-DM-019 | Agent Zone | ROLE_CROSSWALK.md | XW-RL-037 | Geography/Lead Model | Not implemented | CRM_PIPELINE_CONTRACT.md | Lead Routing Engine — Zone Router | TBD | NOT_TRACEABLE |
| GOLD-DM-020 | Identity Resolution | ROLE_CROSSWALK.md | XW-RL-020 | Identity Model | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Identity Resolution Engine — Duplicate Detector | TBD | PARTIALLY_TRACEABLE |

### 3.2 Additional Domain Concepts (GOLD-DM-021 to GOLD-DM-060)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-DM-021 | Property Family enum | PROPERTY_TYPE_CROSSWALK.md | CW-FAMILY-001-007 | Property Taxonomy | Not implemented; `propertyType` is free string | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Family Resolver | TBD | NOT_TRACEABLE |
| GOLD-DM-022 | Property Type taxonomy (18 residential) | PROPERTY_TYPE_CROSSWALK.md | CW-RES-001-018 | Property Taxonomy | Free-form string only | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Type Normalizer | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-023 | Property Type taxonomy (7 land) | PROPERTY_TYPE_CROSSWALK.md | CW-LAND-001-007 | Property Taxonomy | Free-form string only | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Land Type Normalizer | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-024 | Property Type taxonomy (16 commercial) | PROPERTY_TYPE_CROSSWALK.md | CW-COM-001-016 | Property Taxonomy | Free-form string only | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Commercial Type Normalizer | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-025 | Business Profile model (27 profiles) | ROLE_CROSSWALK.md | XW-RL-001-061 | Role Taxonomy | `business_profiles.py` with 27 profiles | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Business Profile Resolver | TBD | TRACEABLE |
| GOLD-DM-026 | Trust Level (6 levels) | ROLE_CROSSWALK.md | XW-RL-018-023 | Trust Model | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Trust Engine — Trust Level Manager | TBD | NOT_TRACEABLE |
| GOLD-DM-027 | Badge System (8 badges) | ROLE_CROSSWALK.md | XW-RL-024-031 | Badge Model | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Badge Engine — Badge Manager | TBD | NOT_TRACEABLE |
| GOLD-DM-028 | Permission Level (4 tiers) | ROLE_CROSSWALK.md | XW-RL-014-017 | Authorization Model | Implicit per role; no formal model | IDENTITY_RESOLUTION_CONTRACT.md | Permission Engine — Permission Matrix | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-029 | Agency Role hierarchy | ROLE_CROSSWALK.md | XW-RL-010, XW-RL-032-034 | Organization Model | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Organization Engine — Agency Role Manager | TBD | NOT_TRACEABLE |
| GOLD-DM-030 | Partner Role (7 partners) | ROLE_CROSSWALK.md | XW-RL-055-061 | Partner Model | `partner` official role + business profiles | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Partner Profile Resolver | TBD | TRACEABLE |
| GOLD-DM-031 | 10-step Property Workflow | PROPERTY_TYPE_CROSSWALK.md | §3 | Property Lifecycle | 5 statuses (compressed) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Property Workflow State Machine | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-032 | 5 Availability States | PROPERTY_TYPE_CROSSWALK.md | §3 | Property Lifecycle | 5 availability strings (no transitions) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Availability State Machine | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-033 | Data Quality Scoring | PROPERTY_TYPE_CROSSWALK.md | §6 | Quality Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Quality Engine — Data Quality Scorer | TBD | NOT_TRACEABLE |
| GOLD-DM-034 | Completeness Score (60%) | PROPERTY_TYPE_CROSSWALK.md | §6 | Quality Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Quality Engine — Completeness Calculator | TBD | NOT_TRACEABLE |
| GOLD-DM-035 | Source Reliability (40%) | PROPERTY_TYPE_CROSSWALK.md | §6 | Quality Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Quality Engine — Reliability Calculator | TBD | NOT_TRACEABLE |
| GOLD-DM-036 | Grading Scale (A+ to D) | PROPERTY_TYPE_CROSSWALK.md | §6 | Quality Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Quality Engine — Grade Assigner | TBD | NOT_TRACEABLE |
| GOLD-DM-037 | 6-level Trust Score | ROLE_CROSSWALK.md | XW-RL-018-023 | Identity Model | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Trust Engine — Trust Score Calculator | TBD | NOT_TRACEABLE |
| GOLD-DM-038 | Auto-archive 90 days | PROPERTY_TYPE_CROSSWALK.md | §3 | Property Lifecycle | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Auto-Archive Scheduler | TBD | NOT_TRACEABLE |
| GOLD-DM-039 | Negotiable elements (per transaction type) | WORKFLOW_STATE_CROSSWALK.md | §2.06 | Negotiation Model | Not implemented | NEGOTIATION_STRATEGY_CONTRACT.md | Negotiation Engine — Element Resolver | TBD | NOT_TRACEABLE |
| GOLD-DM-040 | Holder Silence Escalation | WORKFLOW_STATE_CROSSWALK.md | §2.04 | Contact Model | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Contact Engine — Silence Escalator | TBD | NOT_TRACEABLE |
| GOLD-DM-041 | Double Consent workflow | WORKFLOW_STATE_CROSSWALK.md | §2.04 | Consent Model | Not implemented | CONSENT_EXECUTION_CONTRACT.md | Consent Engine — Double Consent Handler | TBD | NOT_TRACEABLE |
| GOLD-DM-042 | Interlocutor Shift (AI → Human) | WORKFLOW_STATE_CROSSWALK.md | §2.04 | Conversation Model | Not implemented | CONVERSATION_EXECUTION_ARCHITECTURE.md | Conversation Engine — Interlocutor Switcher | TBD | NOT_TRACEABLE |
| GOLD-DM-043 | SIE Reference Code generation | WORKFLOW_STATE_CROSSWALK.md | §2.15 | Publication Model | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | SIE Engine — Reference Code Generator | TBD | NOT_TRACEABLE |
| GOLD-DM-044 | Conversion Attribution (last-touch) | WORKFLOW_STATE_CROSSWALK.md | §2.17 | Analytics Model | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Analytics Engine — Attribution Model | TBD | NOT_TRACEABLE |
| GOLD-DM-045 | Agent Opt-In workflow | WORKFLOW_STATE_CROSSWALK.md | §2.19 | Opt-In Model | Not implemented | CRM_PIPELINE_CONTRACT.md | Lead Engine — Opt-In Manager | TBD | NOT_TRACEABLE |
| GOLD-DM-046 | Lead Base Scores (tenant=40, buyer=60, etc.) | WORKFLOW_STATE_CROSSWALK.md | §2.18 | CRM/Scoring Model | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Base Lead Scorer | TBD | NOT_TRACEABLE |
| GOLD-DM-047 | CRM Pipeline (8 stages) | WORKFLOW_STATE_CROSSWALK.md | §2.18 | CRM/Scoring Model | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Pipeline Stage Executor | TBD | NOT_TRACEABLE |
| GOLD-DM-048 | Lead Classification (HOT/WARM/COLD/SPAM) | WORKFLOW_STATE_CROSSWALK.md | §2.18 | CRM/Scoring Model | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Lead Classifier | TBD | NOT_TRACEABLE |
| GOLD-DM-049 | SLA Monitoring per entity | WORKFLOW_STATE_CROSSWALK.md | §4 | SLA Model | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | SLA Engine — Breach Detector | TBD | NOT_TRACEABLE |
| GOLD-DM-050 | NBA Engine (9 priority levels) | WORKFLOW_STATE_CROSSWALK.md | §5 | NBA Model | `derive_next_actions()` only | DECISION_ENGINE_ARCHITECTURE.md | NBA Engine — Next Best Action Resolver | TBD | NOT_TRACEABLE |

### 3.3 Domain Model — Matching & Qualification (GOLD-DM-061 to GOLD-DM-096)

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GOLD-DM-061 | Score Family (Geographical/Budget/Property/Behavioral/Other) | MATCHING_COMPATIBILITY.md | §3 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Score Family Calculator | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-062 | Weight Distribution per transaction type | MATCHING_COMPATIBILITY.md | §3 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Weight Distributor | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-063 | Budget Tolerance (±15-25%) | MATCHING_COMPATIBILITY.md | §4 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Budget Tolerance Checker | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-064 | Boost Rules (10 conditions) | MATCHING_COMPATIBILITY.md | §5 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Boost Applier | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-065 | Penalty Rules (4 conditions) | MATCHING_COMPATIBILITY.md | §5 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Penalty Applier | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-066 | Scoring Formula (additive + boost - penalty) | MATCHING_COMPATIBILITY.md | §6 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Score Calculator | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-067 | Match Score Thresholds (40/50/70/85) | MATCHING_COMPATIBILITY.md | §7 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Threshold Evaluator | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-068 | Exclusion Rules (8 criteria) | MATCHING_COMPATIBILITY.md | §8 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Exclusion Engine | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-069 | Non-Compensation Principle | MATCHING_COMPATIBILITY.md | §8 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Non-Compensation Enforcer | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-070 | Rematching Triggers (10+) | MATCHING_COMPATIBILITY.md | §9 | Matching Model | Not implemented | REMATCHING_POLICY.md | Matching Engine — Rematch Trigger | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-071 | Geographic Scoring (5 proximity levels) | MATCHING_COMPATIBILITY.md | §10 | Geography Model | Not implemented | PROXIMITY_SCORING_MODEL.md | Geography Engine — Proximity Scorer | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-072 | Mobility Modes (STRICT/FLEXIBLE/VERY_FLEXIBLE) | MATCHING_COMPATIBILITY.md | §10 | Geography Model | Not implemented | PROXIMITY_SCORING_MODEL.md | Geography Engine — Mobility Mode Applier | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-073 | City Affinity Matrix | MATCHING_COMPATIBILITY.md | §10 | Geography Model | Not implemented | GEOGRAPHY_EXECUTION_ARCHITECTURE.md | Geography Engine — Affinity Scorer | TBD | NOT_TRACEABLE |
| GOLD-DM-074 | 7-Level Readiness Model | H05_MATRIX_COMPATIBILITY.md | Common | Qualification Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Qualification Engine — Readiness Calculator | TBD | NOT_TRACEABLE |
| GOLD-DM-075 | 10-Step Qualification Order | INTENT_TRANSACTION_CROSSWALK.md | §5 | Qualification Model | Not implemented | QUALIFICATION_EXECUTION_ARCHITECTURE.md | Qualification Engine — Step Executor | TBD | NOT_TRACEABLE |
| GOLD-DM-076 | Next Question Selector | H05_MATRIX_COMPATIBILITY.md | Extensions | Qualification Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Qualification Engine — Question Selector | TBD | NOT_TRACEABLE |
| GOLD-DM-077 | Field Dictionary (150+ fields) | H05_MATRIX_COMPATIBILITY.md | Field | Qualification Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Qualification Engine — Field Registry | TBD | NOT_TRACEABLE |
| GOLD-DM-078 | 9 Matching Roles | H05_MATRIX_COMPATIBILITY.md | Roles | Qualification Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Role Evaluator | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-079 | Intent Detection (keyword scoring) | INTENT_TRANSACTION_CROSSWALK.md | §4 | Intent Model | Not implemented (explicit project_type only) | CONVERSATION_EXECUTION_ARCHITECTURE.md | Intent Engine — Keyword Scorer | TBD | NOT_TRACEABLE |
| GOLD-DM-080 | Multi-Intent Support | INTENT_TRANSACTION_CROSSWALK.md | §4 | Intent Model | Not implemented | CONVERSATION_EXECUTION_ARCHITECTURE.md | Intent Engine — Multi-Intent Resolver | TBD | NOT_TRACEABLE |
| GOLD-DM-081 | Urgency Detection | INTENT_TRANSACTION_CROSSWALK.md | §4 | Intent Model | Not implemented | CONVERSATION_EXECUTION_ARCHITECTURE.md | Intent Engine — Urgency Scorer | TBD | NOT_TRACEABLE |
| GOLD-DM-082 | Entity Extraction (per intent) | INTENT_TRANSACTION_CROSSWALK.md | §4 | Intent Model | Not implemented | CONVERSATION_EXECUTION_ARCHITECTURE.md | Entity Engine — Per-Intent Extractor | TBD | NOT_TRACEABLE |
| GOLD-DM-083 | Intent-to-Role Mapping | INTENT_TRANSACTION_CROSSWALK.md | §3 | Intent/Role Model | Implicit via project_type only | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Intent Role Mapper | TBD | NOT_TRACEABLE |
| GOLD-DM-084 | Lead Score Weights (BUY=50, RENT=30, etc.) | INTENT_TRANSACTION_CROSSWALK.md | §4 | CRM Model | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Lead Score Weighter | TBD | NOT_TRACEABLE |
| GOLD-DM-085 | SLA by Priority (30min-7d) | WORKFLOW_STATE_CROSSWALK.md | §4 | SLA Model | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | SLA Engine — Priority SLA Enforcer | TBD | NOT_TRACEABLE |
| GOLD-DM-086 | Event Audit (21 workflow event types) | WORKFLOW_STATE_CROSSWALK.md | Cross-cutting | Event Model | Generic Event model (kind, payload) | EVENT_EXECUTION_ARCHITECTURE.md | Event Engine — Typed Event Publisher | TBD | PARTIALLY_TRACEABLE |
| GOLD-DM-087 | 2-tier Archiving (operational + long-term) | WORKFLOW_STATE_CROSSWALK.md | §2.10 | Archive Model | Single `archived` state | WORKFLOW_EXECUTION_ARCHITECTURE.md | Archive Engine — Tiered Archiver | TBD | NOT_TRACEABLE |
| GOLD-DM-088 | Retention Policies (3-year long-term) | WORKFLOW_STATE_CROSSWALK.md | §2.10 | Archive Model | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Archive Engine — Retention Policy Enforcer | TBD | NOT_TRACEABLE |
| GOLD-DM-089 | Incident Management (8 states) | WORKFLOW_STATE_CROSSWALK.md | §2.09 | Incident Model | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Incident Engine — Incident State Machine | TBD | NOT_TRACEABLE |
| GOLD-DM-090 | Mediation Workflow (8 states) | WORKFLOW_STATE_CROSSWALK.md | §2.11 | Mediation Model | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Mediation Engine — Mediation State Machine | TBD | NOT_TRACEABLE |
| GOLD-DM-091 | Agent Invitation (7 states) | WORKFLOW_STATE_CROSSWALK.md | §2.14 | Onboarding Model | Not implemented | IDENTITY_RESOLUTION_CONTRACT.md | Onboarding Engine — Agent Invitation State Machine | TBD | NOT_TRACEABLE |
| GOLD-DM-092 | User Identity Lifecycle (7 states) | WORKFLOW_STATE_CROSSWALK.md | §2.12 | Identity Model | Not implemented (role is free string) | IDENTITY_RESOLUTION_CONTRACT.md | Identity Engine — User Lifecycle State Machine | TBD | NOT_TRACEABLE |
| GOLD-DM-093 | Organization Lifecycle (8 states) | WORKFLOW_STATE_CROSSWALK.md | §2.13 | Organization Model | `Organization.kind` as string only | WORKFLOW_EXECUTION_ARCHITECTURE.md | Organization Engine — Lifecycle State Machine | TBD | NOT_TRACEABLE |
| GOLD-DM-094 | Matches & Leak Detection | MATCHING_COMPATIBILITY.md | §D | Analytics Model | Not implemented | CRM_PIPELINE_CONTRACT.md | Analytics Engine — Leak Detector | TBD | NOT_TRACEABLE |
| GOLD-DM-095 | Match Health Score | MATCHING_COMPATIBILITY.md | §7 | Quality Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Health Scorer | TBD | NOT_TRACEABLE |
| GOLD-DM-096 | Cross-Cutting Orchestrator | WORKFLOW_STATE_CROSSWALK.md | §2.21 | Orchestration Model | Not implemented (distributed across models) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Orchestrator Engine — Master Workflow Coordinator | TBD | NOT_TRACEABLE |

---

## 4. Matching Concepts

Crosswalk: `MATCHING_COMPATIBILITY.md` → Unified: Matching Engine → V2 Target: New → H1: `MATCHING_EXECUTION_ARCHITECTURE.md` → H2: Matching Engine

| Gold ID | Gold Concept | Crosswalk Document | Crosswalk ID | Unified Domain | V2 Target Entity | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------|-------------|-------------------|---------------|----------------|-----------------|-------------|--------------|--------------|---------------------|
| GE-MATCH-001 | V1 Matching dimensions (city/neighborhood/budget/property_type/title_status) | MATCHING_COMPATIBILITY.md | §3 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — V1 Dimension Evaluator | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-002 | V1 Weight Distribution (30/25/25/15/5) | MATCHING_COMPATIBILITY.md | §3 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — V1 Weight Distributor | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-003 | H0.5 Per-Transaction-Type Weights | MATCHING_COMPATIBILITY.md | §3 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — H0.5 Weight Distributor | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-004 | H1 Fixed DE Weights (26/20/15/10/29) | MATCHING_COMPATIBILITY.md | §3 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — DE Weight Fallback | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-005 | Budget Tolerance (RENT±20%, BUY±15%, INVEST±25%) | MATCHING_COMPATIBILITY.md | §4 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Budget Tolerance Checker | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-006 | Budget Linear Decrease Logic | MATCHING_COMPATIBILITY.md | §4 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Linear Budget Decayer | TBD | NOT_TRACEABLE |
| GE-MATCH-007 | Boost Rules (exact_neighborhood +25, exact_city +20, budget +15, title +10, diaspora +20) | MATCHING_COMPATIBILITY.md | §5 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Boost Applier | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-008 | Additional Boosts (cash_purchase +15, visit_intent +20) | MATCHING_COMPATIBILITY.md | §5 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Extended Boost Applier | TBD | NOT_TRACEABLE |
| GE-MATCH-009 | Penalty Rules (missing_budget -10, unclear_location -10, spam -50, missing_neighborhood -5) | MATCHING_COMPATIBILITY.md | §5 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Penalty Applier | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-010 | Scoring Formula (base + boost - penalty, clamped 0-100) | MATCHING_COMPATIBILITY.md | §6 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Score Calculator | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-011 | Match Thresholds (show_at_40, top10_at_50, recommend_visit_70, recommend_transaction_85) | MATCHING_COMPATIBILITY.md | §7 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Threshold Evaluator | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-012 | User-Facing Min Threshold (60/100) | MATCHING_COMPATIBILITY.md | §7 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — User-Facing Threshold Gate | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-013 | Lead Temperature (HOT≥80, WARM≥60, COLD≥40, SPAM≤0.2) | MATCHING_COMPATIBILITY.md | §7 | CRM Model | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Lead Temperature Classifier | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-014 | Star Rating (5-star: ≥80, 4-star: ≥60, 3-star: ≥40) | MATCHING_COMPATIBILITY.md | §7 | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Star Rating Calculator | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-015 | Exclusion Rules (8 criteria) | MATCHING_COMPATIBILITY.md | §8 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Exclusion Engine | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-016 | Non-Compensation (critical deficiency → score 0) | MATCHING_COMPATIBILITY.md | §8 | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Non-Compensation Enforcer | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-017 | Rematching Triggers (10+ events) | MATCHING_COMPATIBILITY.md | §9 | Matching Model | Not implemented | REMATCHING_POLICY.md | Matching Engine — Rematch Trigger Handler | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-018 | Refusal Learning (3 refusals → reprioritization) | MATCHING_COMPATIBILITY.md | §9 | Matching Model | Not implemented | REMATCHING_POLICY.md | Matching Engine — Refusal Pattern Analyzer | TBD | NOT_TRACEABLE |
| GE-MATCH-019 | Geographic Proximity (5 levels: exact=90-100, accepted=75-89, neighboring=50-74, distant=25-49, incompatible=0-24) | MATCHING_COMPATIBILITY.md | §10 | Geography Model | Not implemented | PROXIMITY_SCORING_MODEL.md | Geography Engine — Proximity Level Calculator | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-020 | Mobility Modes (STRICT/FLEXIBLE/VERY_FLEXIBLE) | MATCHING_COMPATIBILITY.md | §10 | Geography Model | Not implemented | PROXIMITY_SCORING_MODEL.md | Geography Engine — Mobility Mode Applier | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-021 | Multi-Modal Distance Calculation (road > haversine > city-centroid > affinity) | MATCHING_COMPATIBILITY.md | §10 | Geography Model | Not implemented | PROXIMITY_SCORING_MODEL.md | Geography Engine — Distance Calculator | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-022 | CRM Scoring (7 factors: type, budget, location, urgency, completeness, engagement, diaspora) | MATCHING_COMPATIBILITY.md | §11 | CRM Model | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Factor Scorer | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-023 | Lead Classification (HOT/WARM/COLD/SPAM) + Actions | MATCHING_COMPATIBILITY.md | §11 | CRM Model | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Lead Classifier + Action Router | TBD | PARTIALLY_TRACEABLE |
| GE-MATCH-024 | Base Lead Scores (tenant=40, buyer=60, seller=50, investor=80, diaspora=95) | MATCHING_COMPATIBILITY.md | §11 | CRM Model | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Base Lead Scorer | TBD | NOT_TRACEABLE |
| GE-MATCH-025 | 8-Stage CRM Pipeline (incoming→normalize→extract→intent→context→score→classify→route) | MATCHING_COMPATIBILITY.md | §11 | CRM Model | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Pipeline Executor | TBD | NOT_TRACEABLE |

---

## 5. Qualification Matrices

Crosswalk: `H05_MATRIX_COMPATIBILITY.md` → Unified: Qualification Engine → V2 Target: New → H1: `QUALIFICATION_EXECUTION_ARCHITECTURE.md` → H2: Qualification Engine

### 5.1 Matrix Families (Summary)

| Matrix ID Range | Family | Count | Unified Domain | V2 Target | H1 Contract | H2 Component | Test Contract | Traceability Status |
|-----------------|--------|-------|----------------|-----------|-------------|--------------|--------------|---------------------|
| MATRIX-RES-SEARCH-001 to 018 | RESIDENTIAL_SEARCH | 18 | Qualification → Matching | `project_type: "rent"` or `"buy"` (generic) | QUALIFICATION_MATRIX_CONTRACT.md | Qualification Engine → Matching Engine (Residential) | TBD | PARTIALLY_TRACEABLE |
| LAND_SEARCH_TERRAIN_*_001 | LAND_SEARCH | 7 | Qualification → Matching | `project_type: "buy"` (generic) | QUALIFICATION_MATRIX_CONTRACT.md | Qualification Engine → Matching Engine (Land) | TBD | NOT_TRACEABLE |
| COM-MATRIX-001 to 016 | COMMERCIAL_SEARCH | 16 | Qualification → Matching | `project_type: "buy"` or `"rent"` (generic) | COMMERCIAL_EXECUTION_ARCHITECTURE.md | Qualification Engine → Matching Engine (Commercial) | TBD | NOT_TRACEABLE |
| COM-MATRIX-017 to 021 | COMMERCIAL_SEARCH (INVEST) | 5 | Qualification → Matching | `project_type: "invest"` (generic) | COMMERCIAL_EXECUTION_ARCHITECTURE.md | Qualification Engine → Matching Engine (Investment) | TBD | NOT_TRACEABLE |
| MATRIX-FIN-001 to 010 | FINANCING_REQUEST | 10 | Qualification → Financing | `project_type: "buy"` (closest, no FINANCE type) | QUALIFICATION_MATRIX_CONTRACT.md | Qualification Engine → Financing Matching Engine | TBD | NOT_TRACEABLE |
| PRO-AGENT-001 to PRO-PREST-027 | PROFESSIONAL_SEARCH | 27 | Qualification → Matching | `project_type: "other"` (no FIND type) | QUALIFICATION_MATRIX_CONTRACT.md | Qualification Engine → Professional Matching Engine | TBD | NOT_TRACEABLE |
| SVC-ESTI-001 to SVC-RECO-024 | REAL_ESTATE_SERVICES | 24 | Qualification → Matching | `project_type: "other"` (no SERVICE type) | QUALIFICATION_MATRIX_CONTRACT.md | Qualification Engine → Service Matching Engine | TBD | NOT_TRACEABLE |

### 5.2 Field Compatibility Summary

| Field Category | Count | V2 Target | Mapping Status |
|----------------|-------|-----------|----------------|
| Directly compatible fields (CITY, BUDGET_MAX, BUDGET_MIN, CURRENCY, CHAMBRES, SURFACE) | 6 | `project_domain.py` / `property_domain.py` | TRACEABLE |
| Partially compatible fields (TRANSACTION, PROPERTY_TYPE, DELAI, FIN-COMMON-002) | 4 | `project_domain.py` / `property_domain.py` (partial) | PARTIALLY_TRACEABLE |
| Residential amenities (DOUCHES, CUISINE, MEUBLE, PARKING, CLIMATISATION, etc.) | 20+ | → `metadata_json` | PARTIALLY_TRACEABLE |
| Residential matching preferences | 6 | → `metadata_json` | PARTIALLY_TRACEABLE |
| Contact/introduction (NOM, TELEPHONE, EMAIL, CANAL) | 5 | → `metadata_json` | PARTIALLY_TRACEABLE |
| Transaction fields (CAUTION, CHARGES, FINANCING, DUREE) | 5+ | → `metadata_json` | PARTIALLY_TRACEABLE |
| Land-specific fields (title_status, usage_prevu, accessibilite, viabilisation, etc.) | 30+ | → `metadata_json` | NOT_TRACEABLE |
| Commercial common fields (activité, surface_min, licence, fonds_commerce) | 45 | → `metadata_json` | NOT_TRACEABLE |
| Investment-specific fields (rendement, horizon, risque, stratégie) | 18 | → `metadata_json` | NOT_TRACEABLE |
| Financing core fields (montant, apport, revenus, garanties) | 25 | → `metadata_json` | NOT_TRACEABLE |
| Financing per-segment fields (salaried, self-employed, construction, diaspora) | 46 | → `metadata_json` | NOT_TRACEABLE |
| Professional service fields (base + per-type) | 65 | → `metadata_json` | NOT_TRACEABLE |
| Real estate service fields (per 24 service types) | 190 | → `metadata_json` | NOT_TRACEABLE |
| Derived fields (standing, budget_coherence, etc.) | 8 | Computed (no storage) | NOT_TRACEABLE |

---

## 6. Workflows

Crosswalk: `WORKFLOW_STATE_CROSSWALK.md` → Unified: Workflow Engine → V2 Target: `project_domain.py` + new → H1: `WORKFLOW_EXECUTION_ARCHITECTURE.md` → H2: Workflow Engine

| # | Gold Workflow | Gold States | V2 Equivalent | Crosswalk Doc | V2 Target | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---|---------------|-------------|---------------|---------------|-----------|-------------|--------------|--------------|---------------------|
| 01 | Property Lifecycle | 13 | 5 property statuses + 5 availability | WORKFLOW_STATE_CROSSWALK.md | `property_domain.py` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Lifecycle State Machine | TBD | PARTIALLY_TRACEABLE |
| 02 | Dossier/Case Lifecycle | 14 | 5 project statuses + 5 step statuses | WORKFLOW_STATE_CROSSWALK.md | `project_domain.py` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Project Engine — Dossier State Machine | TBD | PARTIALLY_TRACEABLE |
| 03 | Matching Lifecycle | 10 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New — no match entity | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Matching State Machine | TBD | NOT_TRACEABLE |
| 04 | Mise en Relation / Contact | 6 | 0 (partial in conversation) | WORKFLOW_STATE_CROSSWALK.md | `conversation_domain.py` (partial) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Contact Engine — Connection State Machine | TBD | PARTIALLY_TRACEABLE |
| 05 | Visit Lifecycle | 9 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New — no visit entity | WORKFLOW_EXECUTION_ARCHITECTURE.md | Visit Engine — Visit State Machine | TBD | NOT_TRACEABLE |
| 06 | Negotiation Lifecycle | 8 | 6 negotiation stages | WORKFLOW_STATE_CROSSWALK.md | `conversation_domain.py` | NEGOTIATION_STRATEGY_CONTRACT.md | Negotiation Engine — Negotiation State Machine | TBD | PARTIALLY_TRACEABLE |
| 07 | Transaction Lifecycle | 10 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New — no transaction entity | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Transaction State Machine | TBD | NOT_TRACEABLE |
| 08 | Paid Services & Payment | 8 + 10 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New | WORKFLOW_EXECUTION_ARCHITECTURE.md | Payment Engine — Service Payment State Machine | TBD | NOT_TRACEABLE |
| 09 | Disputes, Claims & Incidents | 8 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New | WORKFLOW_EXECUTION_ARCHITECTURE.md | Incident Engine — Incident State Machine | TBD | NOT_TRACEABLE |
| 10 | Closure, Archiving & Retention | 4 | 1 (archived) | WORKFLOW_STATE_CROSSWALK.md | `archived` status in each model | WORKFLOW_EXECUTION_ARCHITECTURE.md | Archive Engine — Tiered Archiving | TBD | PARTIALLY_TRACEABLE |
| 11 | Mediation Workflow | 8 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New | WORKFLOW_EXECUTION_ARCHITECTURE.md | Mediation Engine — Mediation State Machine | TBD | NOT_TRACEABLE |
| 12 | User Identity Lifecycle | 7 | 1 (role string) | WORKFLOW_STATE_CROSSWALK.md | `prisma.User` (minimal) | IDENTITY_RESOLUTION_CONTRACT.md | Identity Engine — User Lifecycle State Machine | TBD | PARTIALLY_TRACEABLE |
| 13 | Organization/Agency Lifecycle | 8 | 1 (kind string) | WORKFLOW_STATE_CROSSWALK.md | `prisma.Organization` (minimal) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Organization Engine — Agency Lifecycle State Machine | TBD | PARTIALLY_TRACEABLE |
| 14 | Agent Invitation Workflow | 7 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New | IDENTITY_RESOLUTION_CONTRACT.md | Onboarding Engine — Agent Invitation State Machine | TBD | NOT_TRACEABLE |
| 15 | Publication (SIE-Enriched) | 11 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New | WORKFLOW_EXECUTION_ARCHITECTURE.md | SIE Engine — Publication Pipeline | TBD | NOT_TRACEABLE |
| 16 | Redirection (SIE-Enriched) | 12 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New | WORKFLOW_EXECUTION_ARCHITECTURE.md | SIE Engine — Redirection Pipeline | TBD | NOT_TRACEABLE |
| 17 | Conversion & Attribution | 12 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New | WORKFLOW_EXECUTION_ARCHITECTURE.md | Analytics Engine — Attribution Pipeline | TBD | NOT_TRACEABLE |
| 18 | CRM Pipeline | 8 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New | CRM_PIPELINE_CONTRACT.md | CRM Engine — Pipeline Executor | TBD | NOT_TRACEABLE |
| 19 | Agent Opt-In Workflow | 4 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New | CRM_PIPELINE_CONTRACT.md | Lead Engine — Opt-In State Machine | TBD | NOT_TRACEABLE |
| 20 | Identity Resolution Workflow | 5 | 0 (none) | WORKFLOW_STATE_CROSSWALK.md | New | IDENTITY_RESOLUTION_CONTRACT.md | Identity Resolution Engine — Merge State Machine | TBD | PARTIALLY_TRACEABLE |
| 21 | Main Cross-Cutting Workflow | 9 | 0 (distributed) | WORKFLOW_STATE_CROSSWALK.md | Distributed across project/property/conversation | WORKFLOW_EXECUTION_ARCHITECTURE.md | Orchestrator Engine — Master Workflow Coordinator | TBD | NOT_TRACEABLE |

---

## 7. Services

Crosswalk: `SERVICE_CROSSWALK.md` → Unified: Service Model → V2 Target: New → H1: Various → H2: Service Engine

### 7.1 Monetized Services (13)

| Gold ID / Code | Service Name | Price (FCFA) | Unified Domain | V2 Target | H1 Contract | H2 Component | Test Contract | Traceability Status |
|---------------|--------------|--------------|----------------|-----------|-------------|--------------|--------------|---------------------|
| SVC-BOOST-7J | Boost visibilité 7 jours | 2 000 | Service/Monetization | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Service Engine — Boost Applicator | TBD | NOT_TRACEABLE |
| SVC-BOOST-30J | Boost visibilité 30 jours | 5 000 | Service/Monetization | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Service Engine — Boost Applicator | TBD | NOT_TRACEABLE |
| SVC-PREMIUM | Annonce premium | 10 000 | Service/Monetization | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Service Engine — Premium Applicator | TBD | NOT_TRACEABLE |
| SVC-AGENT-PRO | Abonnement agent professionnel | 10 000/mois | Service/Subscription | Not implemented | CRM_PIPELINE_CONTRACT.md | Subscription Engine — Agent Pro Manager | TBD | NOT_TRACEABLE |
| SVC-VISITE-ACCOMP | Accompagnement de visite | 50 000 | Service/Visit | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Service Engine — Visit Accompaniment | TBD | NOT_TRACEABLE |
| SVC-TRX-ACCOMP | Accompagnement de transaction | 50 000 | Service/Transaction | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Service Engine — Transaction Accompaniment | TBD | NOT_TRACEABLE |
| SVC-DOC-CONTROL | Contrôle documentaire | 5 000 | Service/Document | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Document Engine — Document Verification | TBD | NOT_TRACEABLE |
| SVC-PHOTO | Photographie professionnelle | 15 000 | Service/Media | Not implemented | RESPONSE_STRATEGY_CONTRACT.md | Service Engine — Photography Order | TBD | NOT_TRACEABLE |
| SVC-VIDEO | Vidéo professionnelle | 25 000 | Service/Media | Not implemented | RESPONSE_STRATEGY_CONTRACT.md | Service Engine — Video Order | TBD | NOT_TRACEABLE |
| SVC-VERIF | Vérification de bien | 10 000 | Service/Verification | Not implemented | WORKFLOW_EXECUTION_ARCHITECTURE.md | Service Engine — Property Verification | TBD | NOT_TRACEABLE |
| SVC-MISE-REL | Mise en relation payante | 500 | Service/Lead | Not implemented | CRM_PIPELINE_CONTRACT.md | Service Engine — Pay-per-Connection | TBD | NOT_TRACEABLE |
| SVC-ASSIST | Assistance personnalisée | 50 000 | Service/Support | Not implemented | CONVERSATION_EXECUTION_ARCHITECTURE.md | Service Engine — Premium Assistance | TBD | NOT_TRACEABLE |
| SVC-VISIB-PREMIUM | Visibilité premium | 7 500 | Service/Monetization | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Service Engine — Premium Visibility | TBD | NOT_TRACEABLE |

### 7.2 Real Estate Services (24 Matrices — SVC- prefix)

| Matrix ID | Service Type | Unified Domain | V2 Target | H1 Contract | H2 Component | Test Contract | Traceability Status |
|-----------|-------------|----------------|-----------|-------------|--------------|--------------|---------------------|
| SVC-ESTI-001 | estimation_immobiliere | Service/Estimation | Not implemented (partial via Property) | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Estimation Handler | TBD | PARTIALLY_TRACEABLE |
| SVC-EXPE-002 | expertise | Service/Expertise | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Expertise Handler | TBD | NOT_TRACEABLE |
| SVC-VERI-003 | verification_documentaire | Service/Verification | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Document Engine — Verification Handler | TBD | NOT_TRACEABLE |
| SVC-VISI-004 | visite_property | Service/Visit | Partial via Conversation + Project | WORKFLOW_EXECUTION_ARCHITECTURE.md | Visit Engine — Visit Scheduling Handler | TBD | PARTIALLY_TRACEABLE |
| SVC-CONT-005 | contre_visite | Service/Visit | Partial (same as visite) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Visit Engine — Second Visit Handler | TBD | PARTIALLY_TRACEABLE |
| SVC-GEST-006 | gestion_locative | Service/Management | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Property Management | TBD | NOT_TRACEABLE |
| SVC-MISE-007 | mise_en_location | Service/Listing | Partial via Property creation | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Listing Handler | TBD | PARTIALLY_TRACEABLE |
| SVC-MISE-008 | mise_en_vente | Service/Listing | Partial via Property creation | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Sales Listing Handler | TBD | PARTIALLY_TRACEABLE |
| SVC-PUBL-009 | publication_service | Service/Publication | Partial via `Property.publishedAt` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Publication Handler | TBD | PARTIALLY_TRACEABLE |
| SVC-PHOT-010 | photographie | Service/Photography | Partial via `Media` model | RESPONSE_STRATEGY_CONTRACT.md | Media Engine — Photo Service Handler | TBD | PARTIALLY_TRACEABLE |
| SVC-VIDE-011 | video_service | Service/Video | Partial via `Media` model | RESPONSE_STRATEGY_CONTRACT.md | Media Engine — Video Service Handler | TBD | PARTIALLY_TRACEABLE |
| SVC-DRON-012 | drone_service | Service/Drone | Not implemented | RESPONSE_STRATEGY_CONTRACT.md | Service Engine — Drone Service Handler | TBD | NOT_TRACEABLE |
| SVC-HOME-013 | home_staging | Service/Staging | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Home Staging Handler | TBD | NOT_TRACEABLE |
| SVC-RENO-014 | renovation_service | Service/Renovation | Partial via `Project.projectType` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Renovation Handler | TBD | PARTIALLY_TRACEABLE |
| SVC-CONS-015 | construction_service | Service/Construction | Partial via `Project.projectType` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Construction Handler | TBD | PARTIALLY_TRACEABLE |
| SVC-ENTR-016 | entretien | Service/Maintenance | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Maintenance Handler | TBD | NOT_TRACEABLE |
| SVC-NETT-017 | nettoyage | Service/Cleaning | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Cleaning Handler | TBD | NOT_TRACEABLE |
| SVC-SECU-018 | securisation | Service/Security | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Security Handler | TBD | NOT_TRACEABLE |
| SVC-DEME-019 | demenagement | Service/Moving | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Moving Handler | TBD | NOT_TRACEABLE |
| SVC-ASSU-020 | assurance_service | Service/Insurance | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Insurance Referral | TBD | NOT_TRACEABLE |
| SVC-CONS-021 | conseil_juridique | Service/Legal | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Legal Advice Handler | TBD | NOT_TRACEABLE |
| SVC-CONS-022 | conseil_fiscal | Service/Tax | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Tax Advice Handler | TBD | NOT_TRACEABLE |
| SVC-GEST-023 | gestion_copropriete | Service/Condo | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Condo Management | TBD | NOT_TRACEABLE |
| SVC-RECO-024 | recouvrement_locatif | Service/Recovery | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Rent Recovery | TBD | NOT_TRACEABLE |

### 7.3 Professional Services (27 Matrices — PRO- prefix)

| Matrix ID | Professional Service | V2 Business Profile | Unified Domain | V2 Target | H1 Contract | H2 Component | Test Contract | Traceability Status |
|-----------|--------------------|-------------------|----------------|-----------|-------------|--------------|--------------|---------------------|
| PRO-AGENT-001 | agent_immobilier | `real_estate_agent` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Agent Matcher | TBD | TRACEABLE |
| PRO-NOTAI-003 | notaire | `notary` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Notary Matcher | TBD | TRACEABLE |
| PRO-GEOME-004 | geometre | `surveyor` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Surveyor Matcher | TBD | TRACEABLE |
| PRO-ARCHI-005 | architecte | `architect` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Architect Matcher | TBD | TRACEABLE |
| PRO-INGEN-006 | ingenieur_genie_civil | `engineer` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Engineer Matcher | TBD | TRACEABLE |
| PRO-TECHN-007 | technicien_batiment | `technician` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Technician Matcher | TBD | TRACEABLE |
| PRO-ELECT-009 | electricien | `electrician` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Electrician Matcher | TBD | TRACEABLE |
| PRO-PLOMB-010 | plombier | `plumber` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Plumber Matcher | TBD | TRACEABLE |
| PRO-GESTI-017 | gestionnaire_immobilier | `property_manager` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Property Manager Matcher | TBD | TRACEABLE |
| PRO-PHOTO-019 | photographe_immobilier | `photographer` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Photographer Matcher | TBD | TRACEABLE |
| PRO-DEMEN-021 | demenageur | `mover` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Mover Matcher | TBD | TRACEABLE |
| PRO-NETTO-022 | entreprise_nettoyage | `cleaner` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Cleaner Matcher | TBD | TRACEABLE |
| PRO-ASSUR-024 | assureur | `insurer` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Insurer Matcher | TBD | TRACEABLE |
| PRO-BANQU-025 | banque_microfinance | `bank` | Professional Service | `business_profiles.py` | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Bank Matcher | TBD | TRACEABLE |
| PRO-MACON-008 | macon | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Mason Matcher | TBD | NOT_TRACEABLE |
| PRO-MENUI-011 | menuisier | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Carpenter Matcher | TBD | NOT_TRACEABLE |
| PRO-PEINT-012 | peintre | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Painter Matcher | TBD | NOT_TRACEABLE |
| PRO-CARRE-013 | carreleur | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Tiler Matcher | TBD | NOT_TRACEABLE |
| PRO-COUVR-014 | couvreur | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Roofer Matcher | TBD | NOT_TRACEABLE |
| PRO-EXPIM-015 | expert_immobilier | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Real Estate Expert Matcher | TBD | NOT_TRACEABLE |
| PRO-EVALU-016 | evaluateur | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Evaluator Matcher | TBD | NOT_TRACEABLE |
| PRO-SYNDI-018 | syndic | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Syndic Matcher | TBD | NOT_TRACEABLE |
| PRO-VIDEO-020 | videaste_drone | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Drone Videographer Matcher | TBD | NOT_TRACEABLE |
| PRO-GARDI-023 | gardiennage | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Security Guard Matcher | TBD | NOT_TRACEABLE |
| PRO-COURT-026 | courtier | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Broker Matcher | TBD | NOT_TRACEABLE |
| PRO-PREST-027 | prestataire_administratif | N/A | Professional Service | Not in business_profiles.py | QUALIFICATION_MATRIX_CONTRACT.md | Service Engine — Admin Provider Matcher | TBD | NOT_TRACEABLE |

### 7.4 CRM Monetized Services (8)

| Heritage Service | Price (FCFA) | Unified Domain | V2 Target | H1 Contract | H2 Component | Test Contract | Traceability Status |
|-----------------|--------------|----------------|-----------|-------------|--------------|--------------|---------------------|
| Lead Bronze (1 contact) | 500 | Service/Lead | Not implemented | CRM_PIPELINE_CONTRACT.md | Billing Engine — Lead Purchase Handler | TBD | NOT_TRACEABLE |
| Lead Silver (5 contacts) | 1 500 | Service/Lead | Not implemented | CRM_PIPELINE_CONTRACT.md | Billing Engine — Lead Purchase Handler | TBD | NOT_TRACEABLE |
| Lead Gold (15 contacts) | 3 000 | Service/Lead | Not implemented | CRM_PIPELINE_CONTRACT.md | Billing Engine — Lead Purchase Handler | TBD | NOT_TRACEABLE |
| Déblocage coordonnées propriétaire | 500 | Service/Lead | Not implemented | CRM_PIPELINE_CONTRACT.md | Billing Engine — Owner Contact Unlock | TBD | NOT_TRACEABLE |
| Demandeur Premium | 1 000 | Service/Premium | Not implemented | CRM_PIPELINE_CONTRACT.md | Service Engine — Premium Seeker Profile | TBD | NOT_TRACEABLE |
| Diaspora Simple | 25 000 | Service/Diaspora | Not implemented | CRM_PIPELINE_CONTRACT.md | Service Engine — Diaspora Service | TBD | NOT_TRACEABLE |
| Diaspora Rapport | 50 000 | Service/Diaspora | Not implemented | CRM_PIPELINE_CONTRACT.md | Service Engine — Diaspora Report | TBD | NOT_TRACEABLE |
| Diaspora Complet | 75 000 | Service/Diaspora | Not implemented | CRM_PIPELINE_CONTRACT.md | Service Engine — Full Diaspora Accompaniment | TBD | NOT_TRACEABLE |

---

## 8. Intent & Transaction Concepts

Crosswalk: `INTENT_TRANSACTION_CROSSWALK.md` → Unified: Intent/Transaction Model → V2 Target: `project_domain.py` + new → H1: `CONVERSATION_EXECUTION_ARCHITECTURE.md` → H2: Intent Engine

### 8.1 Intent Concepts

| Gold Concept | Unified Domain | V2 Target | H1 Contract | H2 Component | Traceability Status |
|-------------|----------------|-----------|-------------|--------------|---------------------|
| BUY_PROPERTY (Achat) | Intent Model | `project_type="buy"` | CONVERSATION_EXECUTION_ARCHITECTURE.md | Intent Engine — Buy Intent Handler | TRACEABLE |
| RENT_PROPERTY (Location) | Intent Model | `project_type="rent"` | CONVERSATION_EXECUTION_ARCHITECTURE.md | Intent Engine — Rent Intent Handler | TRACEABLE |
| SELL_PROPERTY (Vente) | Intent Model | `project_type="sell"` | CONVERSATION_EXECUTION_ARCHITECTURE.md | Intent Engine — Sell Intent Handler | TRACEABLE |
| INVESTOR_INTENT (Investissement) | Intent Model | `project_type="invest"` | CONVERSATION_EXECUTION_ARCHITECTURE.md | Intent Engine — Invest Intent Handler | TRACEABLE |
| SEARCH_PROPERTY (Recherche) | Intent Model | `project_type="other"` (fallback) | CONVERSATION_EXECUTION_ARCHITECTURE.md | Intent Engine — Search Fallback Handler | PARTIALLY_TRACEABLE |
| Intent Detection (keyword scoring) | Intent Model | Not implemented (explicit selection) | CONVERSATION_EXECUTION_ARCHITECTURE.md | Intent Engine — Keyword Scorer | NOT_TRACEABLE |
| Multi-Intent Support | Intent Model | Not implemented | CONVERSATION_EXECUTION_ARCHITECTURE.md | Intent Engine — Multi-Intent Resolver | NOT_TRACEABLE |
| Urgency Detection | Intent Model | Not implemented | CONVERSATION_EXECUTION_ARCHITECTURE.md | Intent Engine — Urgency Scorer | NOT_TRACEABLE |
| Entity Extraction | Intent Model | Not implemented | CONVERSATION_EXECUTION_ARCHITECTURE.md | Entity Engine — Per-Intent Extractor | NOT_TRACEABLE |
| Intent-to-Role Mapping | Intent/Role Model | Implicit (not formalized) | IDENTITY_RESOLUTION_CONTRACT.md | Role Engine — Intent Role Mapper | NOT_TRACEABLE |

### 8.2 Transaction Type Concepts

| Gold Transaction | Unified Domain | V2 Target | H1 Contract | H2 Component | Traceability Status |
|-----------------|----------------|-----------|-------------|--------------|---------------------|
| rent | Transaction Model | `project_type="rent"` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Rent Handler | TRACEABLE |
| buy | Transaction Model | `project_type="buy"` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Buy Handler | TRACEABLE |
| sell | Transaction Model | `project_type="sell"` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Sell Handler | TRACEABLE |
| invest | Transaction Model | `project_type="invest"` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Invest Handler | TRACEABLE |
| short_stay | Transaction Model | `project_type="rent"` + metadata | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Short-Stay Handler | PARTIALLY_TRACEABLE |
| lease (3+ ans) | Transaction Model | `project_type="rent"` + `timeline_horizon` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Lease Handler | PARTIALLY_TRACEABLE |
| cession_bail | Transaction Model | `project_type="other"` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Lease Transfer Handler | NOT_TRACEABLE |
| bail_commercial | Transaction Model | `project_type="rent"` (partial) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Commercial Lease Handler | PARTIALLY_TRACEABLE |
| cession | Transaction Model | `project_type="other"` | WORKFLOW_EXECUTION_ARCHITECTURE.md | Transaction Engine — Business Transfer Handler | NOT_TRACEABLE |
| finance | Transaction Model | `project_type="buy"/"invest"` (bundled) | QUALIFICATION_MATRIX_CONTRACT.md | Transaction Engine — Financing Request Handler | NOT_TRACEABLE |
| find | Transaction Model | `project_type="other"` | QUALIFICATION_MATRIX_CONTRACT.md | Transaction Engine — Professional Search Handler | NOT_TRACEABLE |
| service | Transaction Model | `project_type="other"` | QUALIFICATION_MATRIX_CONTRACT.md | Transaction Engine — Service Handler | NOT_TRACEABLE |

### 8.3 Journey Stage Concepts

| Gold Stage | Unified Domain | V2 Target (project step) | H1 Contract | H2 Component | Traceability Status |
|-----------|----------------|-------------------------|-------------|--------------|---------------------|
| SEARCH | Journey Model | `search` step (buy/rent/invest) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Journey Engine — Search Stage | TRACEABLE |
| QUALIFICATION | Journey Model | `qualification` step (ALL types) | QUALIFICATION_EXECUTION_ARCHITECTURE.md | Journey Engine — Qualification Stage | TRACEABLE |
| MATCHING | Journey Model | `search` (demand) / `promotion` (supply) | MATCHING_EXECUTION_ARCHITECTURE.md | Journey Engine — Matching Stage | PARTIALLY_TRACEABLE |
| VISIT | Journey Model | `visit` step (buy/rent) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Journey Engine — Visit Stage | TRACEABLE |
| NEGOTIATION | Journey Model | `negotiation` step + `negotiationStage` | NEGOTIATION_STRATEGY_CONTRACT.md | Journey Engine — Negotiation Stage | PARTIALLY_TRACEABLE |
| TRANSACTION | Journey Model | `due_diligence` / `closing` (partial) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Journey Engine — Transaction Stage | PARTIALLY_TRACEABLE |
| CLOSURE | Journey Model | `closing` step (ALL types) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Journey Engine — Closure Stage | TRACEABLE |
| ARCHIVING | Journey Model | `status="archived"` (ALL types) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Journey Engine — Archiving Stage | TRACEABLE |

---

## 9. Qualitative Knowledge Items

| Knowledge ID | Gold Concept | Source Document | Unified Domain | V2 Target | H1 Contract | H2 Component | Traceability Status |
|-------------|-------------|-----------------|----------------|-----------|-------------|--------------|---------------------|
| G-CONST-001 | Zéro commission | KNOWLEDGE_GLOSSARY.md | Constitutional | Business rule (implicit) | RESPONSE_STRATEGY_CONTRACT.md | Response Engine — Commission Positioning | TRACEABLE |
| G-CONST-002 | CONST-001 to 010 rules | RULE_INDEX.md | Constitutional | Not in code | DECISION_CONTRACT.md | Decision Engine — Constitution Rule Enforcer | PARTIALLY_TRACEABLE |
| G-PROP-001 | Appartement weighing | Directives/04-DECISION-ENGINE | Matching Weights | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Property Type Weighter | NOT_TRACEABLE |
| G-PROP-002 | 7 property families | Directives/02-PROPERTY-REFERENCE | Property Taxonomy | Free-form only | QUALIFICATION_MATRIX_CONTRACT.md | Property Engine — Family Classifier | PARTIALLY_TRACEABLE |
| G-PROP-007 | Data Quality Score | data_quality_engine.py | Quality Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Quality Engine — Data Quality Scorer | NOT_TRACEABLE |
| G-PROP-008 | Grade (A+ to D) | data_quality_engine.py | Quality Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Quality Engine — Grade Assigner | NOT_TRACEABLE |
| G-PROP-009 | Complétude 60% | data_quality_engine.py | Quality Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Quality Engine — Completeness Calculator | NOT_TRACEABLE |
| G-PROP-010 | Fiabilité source | data_quality_engine.py | Quality Model | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Quality Engine — Reliability Calculator | NOT_TRACEABLE |
| G-PROP-011 | Property lifecycle | property_lifecycle_engine.py | Property Lifecycle | 5 statuses (partial) | WORKFLOW_EXECUTION_ARCHITECTURE.md | Property Engine — Lifecycle State Machine | PARTIALLY_TRACEABLE |
| G-PROP-012 | Titre foncier | title_status.json | Land/Title | Not implemented | MATCHING_SCORE_CONTRACT.md | Land Engine — Title Status Checker | NOT_TRACEABLE |
| G-MATCH-001 | Matching V1 dimensions | property_matching_v1.json | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — V1 Dimension Evaluator | PARTIALLY_TRACEABLE |
| G-MATCH-002 | MATCH-001 to 034 | RULE_INDEX.md | Matching Rules | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Rule Enforcer (34 rules) | PARTIALLY_TRACEABLE |
| G-MATCH-004 | Budget tolerance | property_matching_v1.json | Matching Rules | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Budget Tolerance Checker | PARTIALLY_TRACEABLE |
| G-MATCH-005 | Boost rules | property_matching_v1.json | Matching Rules | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Boost Applier | PARTIALLY_TRACEABLE |
| G-MATCH-006 | Star rating | property_matcher_v5.py | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — Star Rating Calculator | PARTIALLY_TRACEABLE |
| G-MATCH-007 | Exclusion rules | MATCHING_ENGINE_V1_SUMMARY.md | Matching Model | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Exclusion Engine | PARTIALLY_TRACEABLE |
| G-MATCH-008 | Non-compensation | Directive/04-DECISION-ENGINE | Matching Principle | Not implemented | MATCHING_EXECUTION_ARCHITECTURE.md | Matching Engine — Non-Compensation Enforcer | PARTIALLY_TRACEABLE |
| G-MATCH-009 | Rematching | Directive/04-DECISION-ENGINE | Matching Model | Not implemented | REMATCHING_POLICY.md | Matching Engine — Rematch Trigger Handler | PARTIALLY_TRACEABLE |
| G-MATCH-014 | V5 scoring | property_matcher_v5.py | Matching Model | Not implemented | MATCHING_SCORE_CONTRACT.md | Matching Engine — V5 Scorer | PARTIALLY_TRACEABLE |
| G-GEO-001 | 10 priority cities | system_prompt_v1.md | Geography Model | Not validated | GEOGRAPHY_EXECUTION_ARCHITECTURE.md | Geography Engine — Priority City Validator | PARTIALLY_TRACEABLE |
| G-GEO-002 | GEO-001 to 011 | RULE_INDEX.md | Geography Rules | Not implemented | GEOGRAPHY_EXECUTION_ARCHITECTURE.md | Geography Engine — Rule Enforcer | NOT_TRACEABLE |
| G-GEO-004 | Levenshtein max 3 | location_normalizer.py | Geography/Normalization | Not implemented | ALIAS_RESOLUTION_CONTRACT.md | Geography Engine — Name Fuzzy Matcher | NOT_TRACEABLE |
| G-GEO-005 | City affinity matrix | city-affinity-matrix.md | Geography Model | Not implemented | PROXIMITY_SCORING_MODEL.md | Geography Engine — Affinity Matrix Resolver | NOT_TRACEABLE |
| G-QUAL-001 | Base scores (lead types) | lead_classifier_v1.json | CRM/Scoring | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Base Lead Scorer | NOT_TRACEABLE |
| G-QUAL-002 | Boosters (+15/+10/+10/+20/+25/+15) | lead_classifier_v1.json | CRM/Scoring | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Boost Applier | NOT_TRACEABLE |
| G-QUAL-003 | Penalties (-10/-10/-50) | lead_classifier_v1.json | CRM/Scoring | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Penalty Applier | NOT_TRACEABLE |
| G-QUAL-004 | Thresholds V1 (80/60/40) | lead_classifier_v1.json | CRM/Scoring | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Threshold Classifier | NOT_TRACEABLE |
| G-QUAL-005 | Thresholds V5 (0.8/0.5/0.3/0.2) | RULE_ENGINE_V5.json | CRM/Scoring | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — V5 Threshold Classifier | NOT_TRACEABLE |
| G-QUAL-006 | Pipeline 8 étapes | RULE_ENGINE_V5.json | CRM/Scoring | Not implemented | CRM_PIPELINE_CONTRACT.md | CRM Engine — Pipeline Executor | NOT_TRACEABLE |
| G-QUAL-007 | 10 étapes qualification | QUALIFICATION_MODEL.md | Qualification Model | Not implemented | QUALIFICATION_EXECUTION_ARCHITECTURE.md | Qualification Engine — Step Executor | NOT_TRACEABLE |
| G-QUAL-011 | Diaspora indicators | diaspora_filter.py | Qualification/Detection | Not implemented | QUALIFICATION_MATRIX_CONTRACT.md | Qualification Engine — Diaspora Detector | NOT_TRACEABLE |
| G-QUAL-012 | QUAL-001 to 019 | RULE_INDEX.md | Qualification Rules | Not implemented | QUALIFICATION_EXECUTION_ARCHITECTURE.md | Qualification Engine — Rule Enforcer (19 rules) | NOT_TRACEABLE |
| G-CONV-001 | Positionnement (intermédiaire, zéro commission) | RESPONSE_POLICY.md | Conversation/Positioning | Business rule (implicit) | RESPONSE_STRATEGY_CONTRACT.md | Response Engine — Positioning Response | TRACEABLE |
| G-CONV-002 | 3 langues (FR/EN/PID) | RESPONSE_POLICY.md | Language Model | Not implemented | LANGUAGE_EXECUTION_ARCHITECTURE.md | Language Engine — Multi-Language Handler | PARTIALLY_TRACEABLE |
| G-CONV-003 | Commands (SIGNALER, SUPPRIMER, ACCOMPAGNEMENT) | RESPONSE_POLICY.md | Conversation/Commands | Not implemented | CONVERSATION_EXECUTION_ARCHITECTURE.md | Conversation Engine — Command Handler | NOT_TRACEABLE |
| G-CONV-004 | Familiarity levels J1-J4 | conversation_memory.py | Conversation Model | Not implemented | CONVERSATION_EXECUTION_ARCHITECTURE.md | Conversation Engine — Familiarity Level Manager | NOT_TRACEABLE |
| G-CONV-005 | Follow-up schedule J1/J7/J30/J90 | follow_up_system.py | Conversation/Follow-up | Not implemented | CRM_PIPELINE_CONTRACT.md | Follow-up Engine — Follow-up Scheduler | NOT_TRACEABLE |

---

## 10. Coverage Summary

### 10.1 By Domain

| Domain | Total Concepts | TRACEABLE | PARTIALLY_TRACEABLE | NOT_TRACEABLE | Traceability % |
|--------|---------------|-----------|---------------------|---------------|----------------|
| Role Concepts (GOLD-RL-001 to 061) | 61 | 20 | 12 | 29 | 52% |
| Property Concepts (GOLD-PR-001 to 122) | 122 | 10 | 40 | 72 | 41% |
| Domain Model (GOLD-DM-001 to 096) | 96 | 10 | 23 | 63 | 34% |
| Matching Concepts (GE-MATCH-001 to 025) | 25 | 0 | 20 | 5 | 80% |
| Qualification Matrices (107 entries) | 107 | 1 family (6 fields) | 1 family (partial) | 5 families + 690 fields | ~15% |
| Workflows (21 entries) | 21 | 0 | 8 | 13 | 38% |
| Services (72+ entries) | 72 | 12 (professional profiles) | 8 (real estate services) | 52 | 28% |
| Intent & Transaction Concepts | 22 | 12 | 4 | 6 | 73% |
| Qualitative Knowledge Items | 30 | 3 | 10 | 17 | 43% |
| **Total** | **~556** | **~68** | **~125** | **~363** | **~35%** |

### 10.2 By Traceability Chain Completeness

| Chain Segment | Fully Covered | Partially Covered | Not Covered |
|---------------|--------------|-------------------|-------------|
| Heritage Gold → Crosswalk | 100% (all 556+ concepts) | — | — |
| Crosswalk → Unified Domain | 100% (all concepts mapped) | — | — |
| Unified Domain → V2 Target | 15% (existing code) | 25% (metadata_json) | 60% (new entities) |
| V2 Target → H1 Contract | 30% (contracts exist) | 40% (contracts partial) | 30% (no contract) |
| H1 Contract → H2 Component | 30% (architecture defined) | 40% (architecture partial) | 30% (not specified) |
| H2 Component → Test Contract | 0% | 0% | 100% (TBD) |

### 10.3 Key Findings

1. **Crosswalk coverage is complete** — Every Gold concept has been identified and mapped in at least one crosswalk document
2. **V2 implementation is minimal** — Only ~15% of concepts have direct code implementation; 60% require new entities
3. **H1 contracts exist for major engines** — Matching, Qualification, CRM, Conversation, Identity Resolution contracts are specified; Workflow, Transaction, Payment contracts are partial or missing
4. **H2 components are architecturally defined** — The H1 documents define component architecture for all major engines, but none are implemented in code
5. **Test coverage is zero** — No test contracts exist for any traceability chain (all marked TBD)
6. **Critical gaps** — Trust levels, badges, approval workflows, transaction entity, visit lifecycle, payment system, CRM pipeline, and the matching engine itself are all NOT_TRACEABLE

---

*Document generated 2026-07-15 — Certified crosswalk references: ROLE_CROSSWALK.md, PROPERTY_TYPE_CROSSWALK.md, MATCHING_COMPATIBILITY.md, H05_MATRIX_COMPATIBILITY.md, WORKFLOW_STATE_CROSSWALK.md, SERVICE_CROSSWALK.md, INTENT_TRANSACTION_CROSSWALK.md — 556+ concepts traced across all domains.*
