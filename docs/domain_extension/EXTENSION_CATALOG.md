# EXTENSION CATALOG — 175 Heritage Gold → LAWIM_V2 Extensions

**Document ID:** LAWIM-HARM-EXT-CATALOG-V1  
**Status:** CANONICAL  
**Date:** 2026-07-15  
**Source:** `required_extensions.json` · `LAWIM_UNIFIED_DOMAIN_MODEL.md`

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Summary Tables](#2-summary-tables)
   - 2.1 [Counts by Domain](#21-counts-by-domain)
   - 2.2 [Counts by Priority](#22-counts-by-priority)
   - 2.3 [Counts by Extension Category](#23-counts-by-extension-category)
   - 2.4 [Human Decision Summary](#24-human-decision-summary)
3. [Domain: trust_and_badges (14 extensions)](#3-domain-trust_and_badges)
4. [Domain: agency_structure (9 extensions)](#4-domain-agency_structure)
5. [Domain: service_model (60 extensions)](#5-domain-service_model)
   - 5.1 [Monetized Services (13)](#51-monetized-services)
   - 5.2 [Real Estate Services (24)](#52-real-estate-services)
   - 5.3 [Professional Services (12)](#53-professional-services)
   - 5.4 [CRM Monetized Services (9)](#54-crm-monetized-services)
   - 5.5 [Service Lifecycle (2)](#55-service-lifecycle)
6. [Domain: workflows (14 extensions)](#6-domain-workflows)
7. [Domain: property_model (15 extensions)](#7-domain-property_model)
8. [Domain: intent_detection (6 extensions)](#8-domain-intent_detection)
9. [Domain: transaction_types (8 extensions)](#9-domain-transaction_types)
10. [Domain: qualification_engine (11 extensions)](#10-domain-qualification_engine)
11. [Domain: crm (11 extensions)](#11-domain-crm)
12. [Domain: matching (13 extensions)](#12-domain-matching)
13. [Domain: sla (6 extensions)](#13-domain-sla)
14. [Domain: nba (4 extensions)](#14-domain-nba)
15. [Domain: permission_model (4 extensions)](#15-domain-permission_model)
16. [Implementation Phase Mapping](#16-implementation-phase-mapping)
17. [Priority Distribution by Domain](#17-priority-distribution-by-domain)
18. [Cross-Reference Index](#18-cross-reference-index)

---

## 1. Executive Summary

This catalog documents all **175 extension concepts** identified during the Heritage Gold → LAWIM_V2 semantic harmonization. Each extension represents a Gold concept, field, workflow, or business rule that requires implementation in V2.

**Key figures:**

| Metric | Value |
|--------|-------|
| Total extensions | 175 |
| Domains covered | 13 |
| Extensions requiring human decision | 89 (50.9%) |
| Extensions gating core monetization (P0-P1) | 47 |
| New entities required | ~15 new models |
| Estimated total effort | 24-35 weeks across 5 phases |

---

## 2. Summary Tables

### 2.1 Counts by Domain

| Domain | Count | % of Total | P0 | P1 | P2 | P3 | P4 |
|--------|-------|-----------|----|----|----|----|----|
| trust_and_badges | 14 | 8.0% | 0 | 3 | 8 | 3 | 0 |
| agency_structure | 9 | 5.1% | 0 | 2 | 6 | 1 | 0 |
| service_model | 60 | 34.3% | 0 | 13 | 10 | 5 | 32 |
| workflows | 14 | 8.0% | 0 | 6 | 3 | 4 | 1 |
| property_model | 15 | 8.6% | 2 | 4 | 5 | 4 | 0 |
| intent_detection | 6 | 3.4% | 0 | 2 | 4 | 0 | 0 |
| transaction_types | 8 | 4.6% | 0 | 0 | 5 | 3 | 0 |
| qualification_engine | 11 | 6.3% | 0 | 3 | 7 | 1 | 0 |
| crm | 11 | 6.3% | 0 | 5 | 5 | 1 | 0 |
| matching | 13 | 7.4% | 0 | 6 | 7 | 0 | 0 |
| sla | 6 | 3.4% | 0 | 1 | 5 | 0 | 0 |
| nba | 4 | 2.3% | 0 | 0 | 4 | 0 | 0 |
| permission_model | 4 | 2.3% | 0 | 1 | 3 | 0 | 0 |
| **Total** | **175** | **100%** | **2** | **46** | **72** | **25** | **32** |

> **Note:** Priority counts above are computed from individual extension data. Summary-level counts from the source JSON report P0=2, P1=45, P2=55, P3=30, P4=25. The extension-level analysis distributes more items into P2/P4 due to finer granularity. Both views are valid for different levels of analysis.

### 2.2 Counts by Priority

| Priority | Count | % | Meaning | Cumulative |
|----------|-------|---|---------|------------|
| **P0** | 2 | 1.1% | Blocking foundation — must ship first | 2 |
| **P1** | 46 | 26.3% | Core business — MVP-critical | 48 |
| **P2** | 72 | 41.1% | Operations & quality — H2.1 scope | 120 |
| **P3** | 25 | 14.3% | Enhancement — H2.2 scope | 145 |
| **P4** | 32 | 18.3% | Future — deferred beyond H2 | 177 |
| **Unknown** | 0 | 0.0% | — | — |
| **Total** | **175** | **100%** | | |

### 2.3 Counts by Extension Category

Extensions are classified into four implementation categories based on the nature of the change required in LAWIM_V2:

| Category | Count | % | Description |
|----------|-------|---|-------------|
| **ENRICH_EXISTING_ENTITY** | 68 | 38.9% | Add fields/behavior to existing V2 models (User, Property, Project, Organization, Conversation) |
| **ADD_NEW_ENTITY** | 67 | 38.3% | Create new database models (Service, ServiceOrder, Payment, Lead, Match, Visit, Transaction, Document, etc.) |
| **ADD_NEW_ENGINE** | 38 | 21.7% | Implement new algorithms/services (matching, CRM scoring, qualification matrices, intent detection, SLA monitoring, NBA) |
| **HUMAN_PROCESS** | 2 | 1.1% | Define human workflows with no code change (policy decisions, admin processes) |
| **Total** | **175** | **100%** | |

#### Category by Domain

| Domain | ENRICH_EXISTING_ENTITY | ADD_NEW_ENTITY | ADD_NEW_ENGINE | HUMAN_PROCESS |
|--------|----------------------|---------------|---------------|---------------|
| trust_and_badges | 14 | 0 | 0 | 0 |
| agency_structure | 7 | 1 | 1 | 0 |
| service_model | 12 | 43 | 5 | 0 |
| workflows | 0 | 12 | 2 | 0 |
| property_model | 15 | 0 | 0 | 0 |
| intent_detection | 1 | 1 | 4 | 0 |
| transaction_types | 8 | 0 | 0 | 0 |
| qualification_engine | 1 | 0 | 10 | 0 |
| crm | 2 | 5 | 4 | 0 |
| matching | 0 | 1 | 12 | 0 |
| sla | 0 | 0 | 6 | 0 |
| nba | 0 | 0 | 4 | 0 |
| permission_model | 4 | 0 | 0 | 0 |

### 2.4 Human Decision Summary

| Domain | Requires Decision | No Decision Needed | Decision Rate |
|--------|-----------------|-------------------|---------------|
| trust_and_badges | 8 | 6 | 57.1% |
| agency_structure | 9 | 0 | 100.0% |
| service_model | 17 | 43 | 28.3% |
| workflows | 10 | 4 | 71.4% |
| property_model | 8 | 7 | 53.3% |
| intent_detection | 4 | 2 | 66.7% |
| transaction_types | 6 | 2 | 75.0% |
| qualification_engine | 1 | 10 | 9.1% |
| crm | 7 | 4 | 63.6% |
| matching | 7 | 6 | 53.8% |
| sla | 6 | 0 | 100.0% |
| nba | 1 | 3 | 25.0% |
| permission_model | 2 | 2 | 50.0% |
| **Total** | **86** | **89** | **49.1%** |

---

## 3. Domain: trust_and_badges

**Target V2 Model:** User — ENRICH_EXISTING_ENTITY  
**Total Extensions:** 14 (6 trust levels + 8 badges)  
**Category:** All ENRICH_EXISTING_ENTITY — add fields and derived display logic to User model.

### 3.1 Trust Levels (6)

| ID | Concept | Priority | Source | Human Decision | Extension Category |
|----|---------|----------|--------|---------------|-------------------|
| EXT-RL-TRUST-001 | Niveau 1 — Nouveau compte | P1 | GOLD-RL-018 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-RL-TRUST-002 | Niveau 2 — Téléphone vérifié | P1 | GOLD-RL-019 | No | ENRICH_EXISTING_ENTITY |
| EXT-RL-TRUST-003 | Niveau 3 — Identité vérifiée | P1 | GOLD-RL-020 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-RL-TRUST-004 | Niveau 4 — Documents pro validés | P2 | GOLD-RL-021 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-RL-TRUST-005 | Niveau 5 — Professionnel vérifié | P2 | GOLD-RL-022 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-RL-TRUST-006 | Niveau 6 — Compte de référence | P3 | GOLD-RL-023 | Yes | ENRICH_EXISTING_ENTITY |

| ID | Concept | Proposed Target | Decision Question |
|----|---------|----------------|-------------------|
| EXT-RL-TRUST-001 | Niveau 1 — Nouveau compte | Add trust_level INT (1-6) field to User model | Default trust level assignment policy for new users |
| EXT-RL-TRUST-002 | Niveau 2 — Téléphone vérifié | Add phone_verified Boolean to User; implement OTP verification flow | — |
| EXT-RL-TRUST-003 | Niveau 3 — Identité vérifiée | Add identity_verified Boolean; implement document upload + admin validation workflow | Admin validation threshold for identity documents |
| EXT-RL-TRUST-004 | Niveau 4 — Documents pro validés | Add professional_docs_verified Boolean; implement pro document workflow | Professional document acceptance criteria |
| EXT-RL-TRUST-005 | Niveau 5 — Professionnel vérifié | Add professional_verified Boolean; complete verification workflow | Professional verification criteria and process |
| EXT-RL-TRUST-006 | Niveau 6 — Compte de référence | Add reference_account Boolean; admin-only grant mechanism | Admin-only grant policy for reference account status |

### 3.2 Badges (8)

| ID | Concept | Priority | Source | Human Decision | Extension Category |
|----|---------|----------|--------|---------------|-------------------|
| EXT-RL-BADGE-001 | Badge: Téléphone vérifié | P2 | GOLD-RL-024 | No | ENRICH_EXISTING_ENTITY |
| EXT-RL-BADGE-002 | Badge: E-mail vérifié | P2 | GOLD-RL-025 | No | ENRICH_EXISTING_ENTITY |
| EXT-RL-BADGE-003 | Badge: Identité vérifiée | P2 | GOLD-RL-026 | No | ENRICH_EXISTING_ENTITY |
| EXT-RL-BADGE-004 | Badge: Propriétaire vérifié | P2 | GOLD-RL-027 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-RL-BADGE-005 | Badge: Agence vérifiée | P2 | GOLD-RL-028 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-RL-BADGE-006 | Badge: Partenaire LAWIM | P2 | GOLD-RL-029 | No | ENRICH_EXISTING_ENTITY |
| EXT-RL-BADGE-007 | Badge: Professionnel vérifié | P2 | GOLD-RL-030 | No | ENRICH_EXISTING_ENTITY |
| EXT-RL-BADGE-008 | Badge: Agent actif | P3 | GOLD-RL-031 | Yes | ENRICH_EXISTING_ENTITY |

| ID | Concept | Proposed Target | Decision Question |
|----|---------|----------------|-------------------|
| EXT-RL-BADGE-001 | Badge: Téléphone vérifié | Implement badge rendering system; derive from phone_verified flag | — |
| EXT-RL-BADGE-002 | Badge: E-mail vérifié | Add email_verified flag; implement badge display | — |
| EXT-RL-BADGE-003 | Badge: Identité vérifiée | Derive from identity_verified trust level; implement badge display | — |
| EXT-RL-BADGE-004 | Badge: Propriétaire vérifié | Add owner_verified field; implement document verification for owners | Ownership proof criteria and verification process |
| EXT-RL-BADGE-005 | Badge: Agence vérifiée | Add agency_verified to Organization model; implement verification workflow | Agency verification criteria and process |
| EXT-RL-BADGE-006 | Badge: Partenaire LAWIM | Derive from professional_verified; add partner-specific badge | — |
| EXT-RL-BADGE-007 | Badge: Professionnel vérifié | Derive from professional_verified trust level | — |
| EXT-RL-BADGE-008 | Badge: Agent actif | Add is_active_agent field or derive from onboarding completion | Definition of active agent (criteria for badge display) |

---

## 4. Domain: agency_structure

**Target V2 Model:** User / Organization / OrganizationMember — ENRICH_EXISTING_ENTITY with ADD_NEW_ENTITY  
**Total Extensions:** 9

| ID | Concept | Priority | Source | Human Decision | Category |
|----|---------|----------|--------|---------------|----------|
| EXT-RL-AGENCY-001 | Agent onboarding flow | P2 | GOLD-RL-035 | Yes | ADD_NEW_ENTITY |
| EXT-RL-AGENCY-002 | Minimum 3 active agents for operational agency | P3 | GOLD-RL-036 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-RL-AGENCY-003 | Lead routing by geographic zone | P2 | GOLD-RL-037 | Yes | ADD_NEW_ENGINE |
| EXT-RL-AGENCY-004 | Lead cost (500 FCFA default) | P1 | GOLD-RL-038 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-RL-AGENCY-005 | Agent credits & boosts | P1 | GOLD-RL-039 | Yes | ADD_NEW_ENTITY |
| EXT-RL-AGENCY-006 | Agent rating (1-5 scale) | P2 | GOLD-RL-040 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-RL-AGENCY-007 | Agency hierarchy roles | P2 | GOLD-RL-010 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-RL-AGENCY-008 | Agency components with trust and validation | P2 | GOLD-RL-033 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-RL-AGENCY-009 | Agency registration fields (RCCM, CNI, tax ID) | P2 | GOLD-RL-034 | Yes | ENRICH_EXISTING_ENTITY |

| ID | Concept | Proposed Target | Decision Question |
|----|---------|----------------|-------------------|
| EXT-RL-AGENCY-001 | Agent onboarding flow | Implement onboarding state machine with onboarding_status field on User | Onboarding step policy and validation requirements per step |
| EXT-RL-AGENCY-002 | Minimum 3 active agents for operational agency | Add agent count validation rule; implement agency operational status logic | Minimum threshold value (Gold=3) and enforcement behavior |
| EXT-RL-AGENCY-003 | Lead routing by geographic zone | Implement agent_zones table (agent_id, zone); build lead routing engine | Routing algorithm: round-robin, score-based, or capacity-based |
| EXT-RL-AGENCY-004 | Lead cost (500 FCFA default) | Implement lead costing module with configurable price per lead | Lead pricing strategy: 500 FCFA default or market-adjusted pricing |
| EXT-RL-AGENCY-005 | Agent credits & boosts | Implement agent_credits (credits, total_spent, last_recharge) and boost_purchases models | Credit pricing: cost per lead, boost pricing tiers |
| EXT-RL-AGENCY-006 | Agent rating (1-5 scale) | Add agent_rating FLOAT field; implement post-interaction rating workflow | Rating calculation method: average, weighted, or decayed |
| EXT-RL-AGENCY-007 | Agency hierarchy roles | Add agency_role enum (responsible, admin, agent, assistant) to User/Org membership | Granularity of agency hierarchy: 4 tiers or simplified |
| EXT-RL-AGENCY-008 | Agency components with trust and validation | Add trust_level, verification fields to Organization model | Agency verification requirements and trust level criteria |
| EXT-RL-AGENCY-009 | Agency registration fields (RCCM, CNI, tax ID) | Add rccm, tax_id, cni_document fields to Organization model | Required vs optional registration fields for agency creation |

---

## 5. Domain: service_model

**Target V2 Model:** New Service, ServiceOrder, Payment, AgentCredit, LeadPurchase entities — ADD_NEW_ENTITY  
**Total Extensions:** 60 across 5 sub-domains  
**UDM Reference:** Domain 3 — Service Model (§4)

### 5.1 Monetized Services

**Count:** 13 extensions  
**Category:** ADD_NEW_ENTITY (new Service catalog items + ServiceOrder lifecycle)

| ID | Concept | Price (FCFA) | Priority | Human Decision |
|----|---------|-------------|----------|---------------|
| EXT-SVC-MON-001 | Boost visibilité 7 jours | 2,000 | P1 | No |
| EXT-SVC-MON-002 | Boost visibilité 30 jours | 5,000 | P1 | No |
| EXT-SVC-MON-003 | Annonce premium | 10,000 | P1 | No |
| EXT-SVC-MON-004 | Abonnement agent professionnel | 10,000/mois | P1 | Yes |
| EXT-SVC-MON-005 | Accompagnement de visite | 50,000 | P2 | Yes |
| EXT-SVC-MON-006 | Accompagnement de transaction | 50,000 | P2 | Yes |
| EXT-SVC-MON-007 | Contrôle documentaire | 5,000 | P4 | Yes |
| EXT-SVC-MON-008 | Photographie professionnelle | 15,000 | P4 | No |
| EXT-SVC-MON-009 | Vidéo professionnelle | 25,000 | P4 | No |
| EXT-SVC-MON-010 | Vérification de bien | 10,000 | P2 | Yes |
| EXT-SVC-MON-011 | Mise en relation payante | 500 | P1 | Yes |
| EXT-SVC-MON-012 | Assistance personnalisée | 50,000 | P4 | Yes |
| EXT-SVC-MON-013 | Visibilité premium | 7,500 | P3 | Yes |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-SVC-MON-001 | Add boost_level and boost_expires_at to Property; implement boost purchase flow | — |
| EXT-SVC-MON-002 | Implement as same boost system with duration parameter (7 vs 30 days) | — |
| EXT-SVC-MON-003 | Add is_premium field to Property; implement premium ranking boost | — |
| EXT-SVC-MON-004 | Implement Subscription model linked to Organization/User with billing via Campay | Subscription billing cycle, features, and cancellation policy |
| EXT-SVC-MON-005 | Implement as ServiceOrder with type='visit_accompaniment' linked to Conversation | Visit accompaniment scope and delivery model |
| EXT-SVC-MON-006 | Implement as ServiceOrder with type='transaction_accompaniment' with fulfillment tracking | Transaction accompaniment scope and deliverables |
| EXT-SVC-MON-007 | Defer to later phase; requires document upload and verification workflow | Document verification scope and pricing |
| EXT-SVC-MON-008 | Extend Media model with service order origin tracking | — |
| EXT-SVC-MON-009 | Extend Media model with service order origin for video services | — |
| EXT-SVC-MON-010 | Add verification_status and verified_at to Property; implement verification as ServiceOrder | Property verification criteria and process |
| EXT-SVC-MON-011 | Implement LeadPurchase model + agent credit system — core monetization mechanism | Pay-per-connection pricing and agent opt-in flow |
| EXT-SVC-MON-012 | Requires human decision on distinction from accompagnement services | Distinction from accompagnement_visite and accompagnement_transaction |
| EXT-SVC-MON-013 | Requires human decision to determine distinct semantics vs boost/premium_listing | Semantic distinction from boost (2 tiers) and premium_listing services |

### 5.2 Real Estate Services

**Count:** 24 extensions  
**Category:** ADD_NEW_ENTITY (new Service catalog items)

| ID | Concept | Priority | Human Decision |
|----|---------|----------|---------------|
| EXT-SVC-RES-001 | estimation_immobiliere | P1 | No |
| EXT-SVC-RES-002 | expertise | P2 | No |
| EXT-SVC-RES-003 | verification_documentaire | P2 | No |
| EXT-SVC-RES-004 | visite_property | P1 | No |
| EXT-SVC-RES-005 | contre_visite | P1 | No |
| EXT-SVC-RES-006 | gestion_locative | P3 | Yes |
| EXT-SVC-RES-007 | mise_en_location | P1 | No |
| EXT-SVC-RES-008 | mise_en_vente | P1 | No |
| EXT-SVC-RES-009 | publication_service | P1 | No |
| EXT-SVC-RES-010 | photographie | P4 | No |
| EXT-SVC-RES-011 | video_service | P4 | No |
| EXT-SVC-RES-012 | drone_service | P4 | No |
| EXT-SVC-RES-013 | home_staging | P4 | No |
| EXT-SVC-RES-014 | renovation_service | P3 | No |
| EXT-SVC-RES-015 | construction_service | P3 | No |
| EXT-SVC-RES-016 | entretien | P4 | No |
| EXT-SVC-RES-017 | nettoyage | P4 | No |
| EXT-SVC-RES-018 | securisation | P4 | No |
| EXT-SVC-RES-019 | demenagement | P4 | No |
| EXT-SVC-RES-020 | assurance_service | P4 | No |
| EXT-SVC-RES-021 | conseil_juridique | P4 | No |
| EXT-SVC-RES-022 | conseil_fiscal | P4 | No |
| EXT-SVC-RES-023 | gestion_copropriete | P4 | No |
| EXT-SVC-RES-024 | recouvrement_locatif | P4 | Yes |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-SVC-RES-001 | Implement estimation service matrix with valuation workflow | — |
| EXT-SVC-RES-002 | Implement expertise service with inspection workflow | — |
| EXT-SVC-RES-003 | Linked to controle_documentaire monetized service; implement verification workflow | — |
| EXT-SVC-RES-004 | Implement visit scheduling as a service with state machine | — |
| EXT-SVC-RES-005 | Extend visit infrastructure with contre-visite type | — |
| EXT-SVC-RES-006 | Implement rental management workflow with recurring service model | Rental management scope: full vs referral only |
| EXT-SVC-RES-007 | Implement listing as a service with order tracking | — |
| EXT-SVC-RES-008 | Same as mise_en_location but for sale transaction | — |
| EXT-SVC-RES-009 | Implement publication service with channel management | — |
| EXT-SVC-RES-010 | Extend Media model with photography service order flow | — |
| EXT-SVC-RES-011 | Extend Media with video service order flow | — |
| EXT-SVC-RES-012 | Implement as sub-service of photography | — |
| EXT-SVC-RES-013 | Implement as professional service with staging workflow | — |
| EXT-SVC-RES-014 | Implement renovation service with scope management | — |
| EXT-SVC-RES-015 | Implement construction service with project management | — |
| EXT-SVC-RES-016 | Implement as recurring service | — |
| EXT-SVC-RES-017 | Implement as professional service | — |
| EXT-SVC-RES-018 | Implement as professional service | — |
| EXT-SVC-RES-019 | Implement as professional service | — |
| EXT-SVC-RES-020 | Implement as partner referral service | — |
| EXT-SVC-RES-021 | Implement as partner professional service with lawyer network | — |
| EXT-SVC-RES-022 | Implement as partner professional service | — |
| EXT-SVC-RES-023 | Implement as professional management service | — |
| EXT-SVC-RES-024 | Implement as dispute resolution service | Rent recovery scope: advisory vs active collection |

### 5.3 Professional Services

**Count:** 12 extensions  
**Category:** ENRICH_EXISTING_ENTITY (add to business_profiles.py)

| ID | Concept | Priority | Human Decision | Proposed Target |
|----|---------|----------|---------------|----------------|
| EXT-SVC-PRO-001 | macon (Masonry) | P3 | No | Add 'mason' to business_profiles.py |
| EXT-SVC-PRO-002 | menuisier (Carpenter) | P3 | No | Add 'carpenter' to business_profiles.py |
| EXT-SVC-PRO-003 | peintre (Painter) | P3 | No | Add 'painter' to business_profiles.py |
| EXT-SVC-PRO-004 | carreleur (Tiler) | P3 | No | Add 'tiler' to business_profiles.py |
| EXT-SVC-PRO-005 | couvreur (Roofer) | P3 | No | Add 'roofer' to business_profiles.py |
| EXT-SVC-PRO-006 | expert_immobilier | P3 | Yes | Add 'real_estate_expert'; distinguish from agent_immobilier |
| EXT-SVC-PRO-007 | evaluateur (Appraiser) | P4 | Yes | Add 'appraiser'; distinguish from expert_immobilier |
| EXT-SVC-PRO-008 | syndic (Condo manager) | P4 | No | Add 'condo_manager' to business_profiles.py |
| EXT-SVC-PRO-009 | videaste_drone | P4 | No | Add 'drone_videographer' to business_profiles.py |
| EXT-SVC-PRO-010 | courtier (Broker) | P4 | Yes | Add 'broker'; distinguish from agent_immobilier |
| EXT-SVC-PRO-011 | gardiennage (Security) | P4 | No | Add 'security_guard' to business_profiles.py |
| EXT-SVC-PRO-012 | prestataire_administratif | P4 | No | Add 'admin_service_provider' to business_profiles.py |

### 5.4 CRM Monetized Services

**Count:** 9 extensions  
**Category:** ADD_NEW_ENTITY (new LeadPurchase pack types + Subscription tiers)

| ID | Concept | Price (FCFA) | Priority | Human Decision |
|----|---------|-------------|----------|---------------|
| EXT-SVC-CRM-001 | Lead Bronze (1 contact) | 500 | P1 | Yes |
| EXT-SVC-CRM-002 | Lead Silver (5 contacts) | 1,500 | P1 | No |
| EXT-SVC-CRM-003 | Lead Gold (15 contacts) | 3,000 | P1 | No |
| EXT-SVC-CRM-004 | Déblocage coordonnées propriétaire | 500 | P1 | Yes |
| EXT-SVC-CRM-005 | Demandeur Premium | 1,000 | P4 | Yes |
| EXT-SVC-CRM-006 | Diaspora Simple | 25,000 | P3 | Yes |
| EXT-SVC-CRM-007 | Diaspora Rapport | 50,000 | P3 | No |
| EXT-SVC-CRM-008 | Diaspora Complet | 75,000 | P3 | No |
| EXT-SVC-CRM-009 | Abonnement Agent Business | 25,000/mois | P2 | Yes |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-SVC-CRM-001 | Implement LeadPurchase model with lead_bronze pack | Lead pack pricing: 500 FCFA default or market-adjusted |
| EXT-SVC-CRM-002 | Implement lead_silver pack with tiered pricing | — |
| EXT-SVC-CRM-003 | Implement lead_gold pack with tiered pricing | — |
| EXT-SVC-CRM-004 | Implement coordinate unlock as distinct purchase type | Distinction from lead purchase: same price, different mechanism |
| EXT-SVC-CRM-005 | Implement premium seeker profile with priority features | Premium seeker features and pricing |
| EXT-SVC-CRM-006 | Implement diaspora service with verified property access | Diaspora service scope and pricing tiers |
| EXT-SVC-CRM-007 | Implement diaspora rapport tier with report delivery | — |
| EXT-SVC-CRM-008 | Implement diaspora complet tier with full accompaniment | — |
| EXT-SVC-CRM-009 | Add agent_business subscription tier to Subscription model | Agent Business features differentiation from Agent Pro |

### 5.5 Service Lifecycle

**Count:** 2 extensions  
**Category:** ADD_NEW_ENTITY (ServiceOrder and Payment models)

| ID | Concept | Priority | Human Decision | Proposed Target | Decision Question |
|----|---------|----------|---------------|----------------|-------------------|
| EXT-SVC-LIFE-001 | Service lifecycle (8 states) | P1 | No | Implement ServiceOrder model with 8-state lifecycle | — |
| EXT-SVC-LIFE-002 | Payment sub-states (10 states) | P1 | Yes | Implement Payment model with 10-state sub-machine; integrate Campay | Payment processor selection: Campay or multi-processor |

---

## 6. Domain: workflows

**Target V2 Model:** New entities — ADD_NEW_ENTITY  
**Total Extensions:** 14  
**UDM Reference:** Domains 5-10 (Dossier, Matching, Visit, Negotiation, Transaction, CRM)

| ID | Concept | Priority | Human Decision | Category |
|----|---------|----------|---------------|----------|
| EXT-WF-001 | Matching Lifecycle (10 states) | P1 | Yes | ADD_NEW_ENGINE |
| EXT-WF-002 | Mise en Relation / Contact Lifecycle (6 states) | P1 | Yes | ADD_NEW_ENTITY |
| EXT-WF-003 | Visit Lifecycle (9 states) | P1 | No | ADD_NEW_ENTITY |
| EXT-WF-004 | Transaction Lifecycle (10 states) | P1 | Yes | ADD_NEW_ENTITY |
| EXT-WF-005 | Paid Services & Payment Lifecycle (18 states) | P1 | Yes | ADD_NEW_ENTITY |
| EXT-WF-006 | Disputes, Claims & Incidents Lifecycle (8 states) | P2 | Yes | ADD_NEW_ENTITY |
| EXT-WF-007 | Mediation Workflow (8 states) | P3 | Yes | ADD_NEW_ENTITY |
| EXT-WF-008 | CRM Pipeline (8 stages) | P1 | Yes | ADD_NEW_ENGINE |
| EXT-WF-009 | Publication (SIE-Enriched) (11 states) | P3 | Yes | ADD_NEW_ENTITY |
| EXT-WF-010 | Redirection (SIE-Enriched) (12 states) | P3 | No | ADD_NEW_ENTITY |
| EXT-WF-011 | Conversion & Attribution (12 states) | P3 | Yes | ADD_NEW_ENTITY |
| EXT-WF-012 | Agent Invitation Workflow (7 states) | P2 | Yes | ADD_NEW_ENTITY |
| EXT-WF-013 | Identity Resolution Workflow (5 states) | P3 | Yes | ADD_NEW_ENTITY |
| EXT-WF-014 | Main Cross-cutting Workflow (9 states) | P2 | Yes | ADD_NEW_ENGINE |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-WF-001 | Implement Match entity with 10-state lifecycle; build scoring engine | Matching algorithm design: rule-based or ML-enhanced |
| EXT-WF-002 | Implement Contact entity with 6-state lifecycle; enforce double consent | Double consent enforcement: mandatory for all or configurable |
| EXT-WF-003 | Implement Visit model with 9-state lifecycle; scheduling, confirmation, no-show tracking | — |
| EXT-WF-004 | Implement Transaction model with 10-state lifecycle; document requirements per type | Transaction entity vs extended Project: separate model or extension |
| EXT-WF-005 | Implement ServiceOrder and Payment models; integrate Campay | Payment processor, service catalog scope, pricing validation |
| EXT-WF-006 | Implement Incident model with 8-state lifecycle; 12 incident types; 4 priority levels | Incident priority levels and SLA thresholds |
| EXT-WF-007 | Implement Mediation model with 8-state lifecycle | Mediation as built-in feature vs outsourced service |
| EXT-WF-008 | Implement Lead model with 8-stage pipeline; scoring engine; classification; routing | CRM pipeline automation level: fully automated or human-in-the-loop |
| EXT-WF-009 | Implement Publication model with 11-state lifecycle; SIE integration | SIE integration priority: MVP or Phase 3 enhancement |
| EXT-WF-010 | Implement Redirection model with 12-state lifecycle; bot/dedup detection | — |
| EXT-WF-011 | Implement Conversion model with 12-state lifecycle; last-touch attribution | Attribution model: last-touch or multi-touch |
| EXT-WF-012 | Implement AgentInvitation model with 7-state lifecycle; secure link generation | Onboarding step requirements: all Gold steps or simplified |
| EXT-WF-013 | Implement IdentityResolution model with 5-state lifecycle; signal matching | Identity resolution automation level and false positive handling |
| EXT-WF-014 | Implement orchestrator workflow engine that delegates to sub-workflows | Orchestrator implementation: workflow engine vs event-driven choreography |

---

## 7. Domain: property_model

**Target V2 Model:** Property — ENRICH_EXISTING_ENTITY  
**Total Extensions:** 15  
**UDM Reference:** Domain 2 — Property/Listing Model (§3)

| ID | Concept | Priority | Human Decision | Category |
|----|---------|----------|---------------|----------|
| EXT-PROP-001 | Property families (7 families) | **P0** | No | ENRICH_EXISTING_ENTITY |
| EXT-PROP-002 | Property type hierarchy (11 basic + 41 matrix) | **P0** | No | ENRICH_EXISTING_ENTITY |
| EXT-PROP-003 | Full matrix types (107 qualification matrices) | P2 | No | ENRICH_EXISTING_ENTITY |
| EXT-PROP-004 | 10-step property lifecycle | P1 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-PROP-005 | Publication rules (8 rules) | P1 | No | ENRICH_EXISTING_ENTITY |
| EXT-PROP-006 | Price concepts (6 levels) | P1 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-PROP-007 | Additional price types (7 types) | P2 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-PROP-008 | Data quality scoring | P2 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-PROP-009 | Per-type specific fields | P1 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-PROP-010 | Availability state machine | P2 | No | ENRICH_EXISTING_ENTITY |
| EXT-PROP-011 | Auto-archive (90-day inactivity rule) | P2 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-PROP-012 | Investment types (5 types) | P3 | No | ENRICH_EXISTING_ENTITY |
| EXT-PROP-013 | Agricultural family | P3 | No | ENRICH_EXISTING_ENTITY |
| EXT-PROP-014 | Hotelier family | P3 | No | ENRICH_EXISTING_ENTITY |
| EXT-PROP-015 | Real estate project family | P3 | Yes | ENRICH_EXISTING_ENTITY |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-PROP-001 | Add property_family enum (7 values); validate in property_domain.py | — |
| EXT-PROP-002 | Create PROPERTY_TYPES enum set; store subtype in metadata_json | — |
| EXT-PROP-003 | Link property types to qualification matrix catalog; implement matrix selection by type | — |
| EXT-PROP-004 | Extend property state machine from 5 to 10+ states | State granularity: full 10-step or key additions |
| EXT-PROP-005 | Expand can_publish() from 3 to 8 rules | — |
| EXT-PROP-006 | Extend price model: add price_displayed, negotiable flag, price_negotiable, etc. | Price field priority: which levels are MVP vs enhancement |
| EXT-PROP-007 | Add price type classification field; store typed prices in metadata_json | Price type implementation: typed fields vs metadata_json |
| EXT-PROP-008 | Implement quality scoring engine with completeness + reliability dimensions | Scoring dimensions and weights: Gold formula or adjusted |
| EXT-PROP-009 | Add per-type field schemas in metadata_json with validation per family | Per-type field priority: which families first |
| EXT-PROP-010 | Implement availability state machine with valid transition rules | — |
| EXT-PROP-011 | Implement cron job for 90-day inactivity auto-archive | Auto-archive threshold: 90 days or configurable |
| EXT-PROP-012 | Add investment-specific fields and workflows to property model | — |
| EXT-PROP-013 | Add agricultural family to property_family enum; implement sub-referentiel | — |
| EXT-PROP-014 | Add hotel family to property_family enum; map commercial.hotel to this family | — |
| EXT-PROP-015 | Add project family to property_family enum; link Property to Project | Project family: enum value or separate model link |

---

## 8. Domain: intent_detection

**Target V2 Model:** New Intent entity + detection engine — ADD_NEW_ENGINE  
**Total Extensions:** 6  
**UDM Reference:** Domain 4 — Intent/Transaction Model (§5)

| ID | Concept | Priority | Human Decision | Category |
|----|---------|----------|---------------|----------|
| EXT-INT-001 | Keyword-based intent detection | P1 | Yes | ADD_NEW_ENGINE |
| EXT-INT-002 | Confidence threshold (0.70) | P1 | Yes | ADD_NEW_ENGINE |
| EXT-INT-003 | Multi-intent detection | P2 | No | ADD_NEW_ENGINE |
| EXT-INT-004 | Urgency detection | P2 | Yes | ADD_NEW_ENGINE |
| EXT-INT-005 | Entity extraction per intent | P2 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-INT-006 | Intent-to-role mapping | P2 | No | ADD_NEW_ENTITY |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-INT-001 | Implement intent classifier with keyword dictionaries for FR, EN, PID | Intent detection mandatory for all channels or chat-only |
| EXT-INT-002 | Implement configurable confidence threshold with fallback mechanism | Confidence threshold value: 0.70 or tunable |
| EXT-INT-003 | Allow parallel project creation from multi-intent detection results | — |
| EXT-INT-004 | Add urgency scoring to intent detection pipeline; store urgency level on Project | Urgency scoring method and integration with lead scoring |
| EXT-INT-005 | Implement per-intent entity extraction for qualification auto-population | Entity extraction method: rule-based or NLP |
| EXT-INT-006 | Implement Intent model with role mapping layer; assign user role based on detected intent | — |

---

## 9. Domain: transaction_types

**Target V2 Model:** Project — ENRICH_EXISTING_ENTITY (extend PROJECT_TYPES)  
**Total Extensions:** 8  
**UDM Reference:** Domain 4 — Intent/Transaction Model (§5)

| ID | Concept | Priority | Human Decision | Category |
|----|---------|----------|---------------|----------|
| EXT-TRX-001 | short_stay transaction type | P2 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-TRX-002 | lease (bail 3+ ans) transaction type | P2 | No | ENRICH_EXISTING_ENTITY |
| EXT-TRX-003 | cession_bail (commercial lease transfer) | P3 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-TRX-004 | bail_commercial (commercial lease 3-9 ans) | P2 | No | ENRICH_EXISTING_ENTITY |
| EXT-TRX-005 | cession (business asset transfer) | P3 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-TRX-006 | finance (financing request) | P2 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-TRX-007 | find (professional search) | P2 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-TRX-008 | service (real estate service procurement) | P2 | Yes | ENRICH_EXISTING_ENTITY |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-TRX-001 | Add 'short_stay' to PROJECT_TYPES or implement as sub-type with metadata | Short_stay: dedicated project_type or rent sub-type |
| EXT-TRX-002 | Add 'lease' to PROJECT_TYPES; extend timeline_horizon to support 3+ years | — |
| EXT-TRX-003 | Add 'commercial_lease_transfer' as project type or sub-type | Cession_bail: dedicated type or metadata extension of 'lease' |
| EXT-TRX-004 | Add commercial lease handling to 'lease' type or create dedicated sub-type | — |
| EXT-TRX-005 | Add 'business_transfer' as project type | Cession: in-scope for LAWIM or out-of-scope |
| EXT-TRX-006 | Add 'finance' to PROJECT_TYPES; implement 10 financing qualification matrices | Finance: standalone project type or sub-intent of buy/invest |
| EXT-TRX-007 | Add 'find' to PROJECT_TYPES; implement professional search workflow | Find: core LAWIM feature or separate marketplace |
| EXT-TRX-008 | Add 'service' to PROJECT_TYPES; implement service procurement workflow | Service procurement: integrated workflow or separate service ordering |

---

## 10. Domain: qualification_engine

**Target V2 Model:** New qualification matrix system — ADD_NEW_ENGINE  
**Total Extensions:** 11  
**UDM Reference:** Domain 5 — Dossier/Project Model (§6)

| ID | Concept | Priority | Human Decision | Category |
|----|---------|----------|---------------|----------|
| EXT-QUAL-001 | Residential Search matrices (18 matrices) | P1 | No | ADD_NEW_ENGINE |
| EXT-QUAL-002 | Land Search matrices (7 matrices) | P1 | No | ADD_NEW_ENGINE |
| EXT-QUAL-003 | Commercial Search matrices (21 matrices) | P2 | No | ADD_NEW_ENGINE |
| EXT-QUAL-004 | Investment matrices (5 matrices) | P2 | No | ADD_NEW_ENGINE |
| EXT-QUAL-005 | Financing Request matrices (10 matrices) | P2 | No | ADD_NEW_ENGINE |
| EXT-QUAL-006 | Professional Search matrices (27 matrices) | P2 | No | ADD_NEW_ENGINE |
| EXT-QUAL-007 | Real Estate Service matrices (24 matrices) | P2 | No | ADD_NEW_ENGINE |
| EXT-QUAL-008 | Field dictionary with matching roles | P2 | No | ADD_NEW_ENGINE |
| EXT-QUAL-009 | Question priority system | P2 | No | ENRICH_EXISTING_ENTITY |
| EXT-QUAL-010 | Progressive qualification order (10 steps) | P1 | No | ADD_NEW_ENGINE |
| EXT-QUAL-011 | Per-channel adaptation | P2 | Yes | ADD_NEW_ENGINE |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-QUAL-001 | Implement 18 residential qualification matrices with field definitions | — |
| EXT-QUAL-002 | Implement 7 land qualification matrices with title status fields | — |
| EXT-QUAL-003 | Implement 21 commercial qualification matrices | — |
| EXT-QUAL-004 | Implement 5 investment qualification matrices | — |
| EXT-QUAL-005 | Implement 10 financing request matrices | — |
| EXT-QUAL-006 | Implement 27 professional search matrices | — |
| EXT-QUAL-007 | Implement 24 real estate service matrices | — |
| EXT-QUAL-008 | Implement field dictionary with role assignments per matrix field | — |
| EXT-QUAL-009 | Implement priority levels for qualification fields (mandatory, important, optional) | — |
| EXT-QUAL-010 | Implement ordered qualification wizard with 10-step progressive disclosure | — |
| EXT-QUAL-011 | Implement channel-adaptive qualification with configurable question limits | Per-channel question limits: Gold defaults or adjustable |

---

## 11. Domain: crm

**Target V2 Model:** New Lead entity + scoring engine — ADD_NEW_ENTITY / ADD_NEW_ENGINE  
**Total Extensions:** 11  
**UDM Reference:** Domain 10 — CRM Pipeline (§11)

| ID | Concept | Priority | Human Decision | Category |
|----|---------|----------|---------------|----------|
| EXT-CRM-001 | Lead scoring engine (base + boosters - penalties) | P1 | No | ADD_NEW_ENGINE |
| EXT-CRM-002 | Score boosters (13 boosters) | P1 | Yes | ADD_NEW_ENGINE |
| EXT-CRM-003 | Score penalties (8 penalties) | P1 | Yes | ADD_NEW_ENGINE |
| EXT-CRM-004 | Lead classification (5 classes) | P1 | Yes | ADD_NEW_ENGINE |
| EXT-CRM-005 | CRM routing engine | P1 | Yes | ADD_NEW_ENGINE |
| EXT-CRM-006 | 7-factor CRM scoring | P2 | Yes | ADD_NEW_ENGINE |
| EXT-CRM-007 | Behavior tracking fields | P2 | No | ENRICH_EXISTING_ENTITY |
| EXT-CRM-008 | Anti-fraud detection layers (4 layers) | P2 | Yes | ADD_NEW_ENGINE |
| EXT-CRM-009 | Agent rating system (post-interaction) | P2 | Yes | ADD_NEW_ENTITY |
| EXT-CRM-010 | Feedback handling system | P3 | No | ADD_NEW_ENTITY |
| EXT-CRM-011 | Lead SLA by priority | P1 | Yes | ENRICH_EXISTING_ENTITY |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-CRM-001 | Implement scoring engine with base scores, boosters, and penalties | — |
| EXT-CRM-002 | Implement 13+ configurable score boosters with weights | Booster weights and detection criteria |
| EXT-CRM-003 | Implement 8+ configurable score penalties with weights | Penalty weights and detection criteria |
| EXT-CRM-004 | Implement classification thresholds and class assignment logic | Classification thresholds for each class |
| EXT-CRM-005 | Implement routing engine with configurable rules | Primary routing dimension (score vs zone vs round-robin) |
| EXT-CRM-006 | Implement 7-factor scoring model with configurable factor weights | 7-factor scoring: integrated or separate from lead scoring |
| EXT-CRM-007 | Add behavior tracking fields to Lead/User model; implement data collection points | — |
| EXT-CRM-008 | Implement 4 fraud detection layers with configurable rules | Anti-fraud automation: automatic suspension or human-in-the-loop |
| EXT-CRM-009 | Implement post-interaction rating workflow and agent_rating calculation | Rating collection timing and calculation method |
| EXT-CRM-010 | Implement feedback collection, aggregation, and reporting module | — |
| EXT-CRM-011 | Implement SLA tracking per lead with priority-based thresholds and breach escalation | SLA thresholds and breach escalation workflow |

---

## 12. Domain: matching

**Target V2 Model:** New Match entity + matching algorithm — ADD_NEW_ENGINE  
**Total Extensions:** 13  
**UDM Reference:** Domain 6 — Matching Engine (§7)

| ID | Concept | Priority | Human Decision | Category |
|----|---------|----------|---------------|----------|
| EXT-MAT-001 | Full matching engine | P1 | Yes | ADD_NEW_ENGINE |
| EXT-MAT-002 | 5 scoring dimensions | P1 | Yes | ADD_NEW_ENGINE |
| EXT-MAT-003 | Geographic scoring (5 levels) | P1 | No | ADD_NEW_ENGINE |
| EXT-MAT-004 | 4 compatibility levels | P1 | Yes | ADD_NEW_ENGINE |
| EXT-MAT-005 | Rematching rules | P1 | Yes | ADD_NEW_ENGINE |
| EXT-MAT-006 | Exclusion criteria for matching | P1 | No | ADD_NEW_ENGINE |
| EXT-MAT-007 | Transaction success score | P2 | Yes | ADD_NEW_ENGINE |
| EXT-MAT-008 | Market tension index | P2 | No | ADD_NEW_ENGINE |
| EXT-MAT-009 | Dossier health score | P2 | No | ADD_NEW_ENGINE |
| EXT-MAT-010 | Property health score | P2 | No | ADD_NEW_ENGINE |
| EXT-MAT-011 | 9 matching roles | P1 | Yes | ADD_NEW_ENGINE |
| EXT-MAT-012 | Progressive search expansion | P2 | Yes | ADD_NEW_ENTITY |
| EXT-MAT-013 | Continuous market surveillance | P2 | No | ADD_NEW_ENGINE |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-MAT-001 | Implement Match entity and matching algorithm with trigger events | Matching engine: rule-based scoring vs ML-based |
| EXT-MAT-002 | Implement 5 scoring dimensions with configurable weights per property type | Scoring dimension weights: Gold defaults or tunable |
| EXT-MAT-003 | Implement geographic scoring with distance tiers and zone-based matching | — |
| EXT-MAT-004 | Implement compatibility level thresholds and display logic | Compatibility level thresholds (score ranges per level) |
| EXT-MAT-005 | Implement rematching triggers and rules; add rematching_count to dossier | Rematching trigger events and exclusion rules |
| EXT-MAT-006 | Implement exclusion rule engine with configurable criteria | — |
| EXT-MAT-007 | Implement transaction success score based on historical patterns | Transaction success score: statistical model or heuristic |
| EXT-MAT-008 | Implement market tension index calculation by property type, location, price range | — |
| EXT-MAT-009 | Implement dossier health score based on qualification completeness | — |
| EXT-MAT-010 | Implement property health score based on data quality, completeness, freshness | — |
| EXT-MAT-011 | Define 9 matching roles with role-specific scoring weights and permissions | Matching role definitions and scoring weights per role |
| EXT-MAT-012 | Implement progressive search expansion rules | Search expansion rules: priority order and maximum bounds |
| EXT-MAT-013 | Implement event-driven matching triggers on new property publication | — |

---

## 13. Domain: sla

**Target V2 Model:** New SLA monitoring engine — ADD_NEW_ENGINE  
**Total Extensions:** 6  
**UDM Reference:** Domain 10 — CRM Pipeline (§11.7)

| ID | Concept | Priority | Human Decision | Category |
|----|---------|----------|---------------|----------|
| EXT-SLA-001 | SLA per property type | P2 | Yes | ADD_NEW_ENGINE |
| EXT-SLA-002 | SLA per workflow state | P2 | Yes | ADD_NEW_ENGINE |
| EXT-SLA-003 | Priority-based SLAs (P0-P3) | P1 | Yes | ADD_NEW_ENGINE |
| EXT-SLA-004 | Breach detection engine | P2 | Yes | ADD_NEW_ENGINE |
| EXT-SLA-005 | 3-tier SLA escalation | P2 | Yes | ADD_NEW_ENGINE |
| EXT-SLA-006 | Holder silence escalation | P2 | Yes | ADD_NEW_ENGINE |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-SLA-001 | Implement SLA registry with configurable thresholds per property type per state | SLA threshold values per property type |
| EXT-SLA-002 | Implement per-state SLA thresholds with configurable duration per entity type | State SLA thresholds: which states get which durations |
| EXT-SLA-003 | Implement SLA by lead priority with breach detection and escalation | SLA time thresholds per priority level |
| EXT-SLA-004 | Implement SLA breach detection service with configurable check intervals | SLA check frequency per entity type |
| EXT-SLA-005 | Implement 3-tier escalation workflow with configurable actions per tier | Escalation actions per tier per entity type |
| EXT-SLA-006 | Implement holder silence tracking with configurable reminder intervals | Silence escalation intervals and actions per tier |

---

## 14. Domain: nba

**Target V2 Model:** New NBA (Next Best Action) engine — ADD_NEW_ENGINE  
**Total Extensions:** 4  
**UDM Reference:** Domain 7.1.4 — NBA Post-Visit (§8.1.4) and Domain 8 — Negotiation (§9)

| ID | Concept | Priority | Human Decision | Category |
|----|---------|----------|---------------|----------|
| EXT-NBA-001 | NBA per state per workflow | P2 | No | ADD_NEW_ENGINE |
| EXT-NBA-002 | 9-level NBA priority system | P2 | No | ADD_NEW_ENGINE |
| EXT-NBA-003 | Follow-up calendar (J1, J7, J30, J90) | P2 | Yes | ADD_NEW_ENGINE |
| EXT-NBA-004 | SLA breach → NBA recalculation | P2 | No | ADD_NEW_ENGINE |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-NBA-001 | Implement NBA registry with state-specific action definitions per workflow | — |
| EXT-NBA-002 | Implement 9-level NBA priority with action-specific priority assignment | — |
| EXT-NBA-003 | Implement follow-up scheduling with J1, J7, J30, J90 intervals and reminders | Follow-up interval configuration and reminder channel |
| EXT-NBA-004 | Implement NBA recalculation trigger on SLA breach events | — |

---

## 15. Domain: permission_model

**Target V2 Model:** User/Organization — ENRICH_EXISTING_ENTITY  
**Total Extensions:** 4  
**UDM Reference:** Domain 13 — Permission/Security Model (§14)

| ID | Concept | Priority | Human Decision | Category |
|----|---------|----------|---------------|----------|
| EXT-PERM-001 | Niveau 4 — Validation (Approve) | P1 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-PERM-002 | Niveau 1 — Lecture (Read) | P2 | Yes | ENRICH_EXISTING_ENTITY |
| EXT-PERM-003 | Niveau 2 — Création (Create) | P2 | No | ENRICH_EXISTING_ENTITY |
| EXT-PERM-004 | Niveau 3 — Modification (Edit) | P2 | No | ENRICH_EXISTING_ENTITY |

| ID | Proposed Target | Decision Question |
|----|----------------|-------------------|
| EXT-PERM-001 | Implement ApprovalWorkflow model with approver_role, target_type, status | Which actions require approval and which roles can approve |
| EXT-PERM-002 | Implement explicit Read permission check system if fine-grained RBAC needed | Explicit permission system: full RBAC or keep implicit |
| EXT-PERM-003 | Formalize Create permission level per role in permission matrix | — |
| EXT-PERM-004 | Formalize Edit permission scope with three tiers: own, managed, all | — |

---

## 16. Implementation Phase Mapping

The source JSON defines 5 implementation phases. Below is the mapping of extensions to phases:

### Phase 0: Foundation (2-3 weeks)

| ID | Concept | Priority |
|----|---------|----------|
| EXT-PROP-001 | Property families (7 families) | P0 |
| EXT-PROP-002 | Property type hierarchy | P0 |
| EXT-PROP-004 | 10-step property lifecycle (partial) | P1 |

### Phase 1: Core Business (8-12 weeks)

| Scope | Extensions | Priority Range |
|-------|-----------|---------------|
| **Trust levels** | EXT-RL-TRUST-001 to EXT-RL-TRUST-006 | P1-P3 |
| **Badges** | EXT-RL-BADGE-001 to EXT-RL-BADGE-008 | P2-P3 |
| **Workflows (core)** | EXT-WF-001 (Matching), EXT-WF-002 (Contact), EXT-WF-003 (Visit), EXT-WF-004 (Transaction), EXT-WF-005 (Payment), EXT-WF-008 (CRM Pipeline) | P1 |
| **Monetized services** | EXT-SVC-MON-001 to EXT-SVC-MON-013 | P1-P4 |
| **Intent detection** | EXT-INT-001 to EXT-INT-006 | P1-P2 |
| **Matching engine** | EXT-MAT-001 to EXT-MAT-013 | P1-P2 |
| **CRM engine** | EXT-CRM-001 to EXT-CRM-011 | P1-P3 |
| **Property (publication, pricing, per-type)** | EXT-PROP-005, EXT-PROP-006, EXT-PROP-009 | P1-P2 |

### Phase 2: Operations (6-8 weeks)

| Scope | Extensions | Priority Range |
|-------|-----------|---------------|
| **Agency structure** | EXT-RL-AGENCY-001 to EXT-RL-AGENCY-009 | P1-P3 |
| **Workflows (ops)** | EXT-WF-006 (Incidents), EXT-WF-012 (Agent Invitation), EXT-WF-014 (Orchestrator) | P2 |
| **NBA engine** | EXT-NBA-001 to EXT-NBA-004 | P2 |
| **SLA engine** | EXT-SLA-001 to EXT-SLA-006 | P1-P2 |
| **Qualification engine** | EXT-QUAL-001 to EXT-QUAL-011 | P1-P2 |

### Phase 3: Analytics (4-6 weeks)

| Scope | Extensions | Priority Range |
|-------|-----------|---------------|
| **SIE pipelines** | EXT-WF-009 (Publication SIE), EXT-WF-010 (Redirection), EXT-WF-011 (Conversion) | P3 |
| **Quality scoring** | EXT-PROP-008 (Data quality), EXT-PROP-010 (Availability state machine), EXT-PROP-011 (Auto-archive) | P2 |
| **Remaining property** | EXT-PROP-012 (Investment), EXT-PROP-013 (Agricultural), EXT-PROP-014 (Hotelier), EXT-PROP-015 (Project family) | P3 |

### Phase 4: Enhancement (4-6 weeks)

| Scope | Extensions | Priority Range |
|-------|-----------|---------------|
| **Mediation & Identity** | EXT-WF-007 (Mediation), EXT-WF-013 (Identity Resolution) | P3 |
| **Professional services** | EXT-SVC-PRO-001 to EXT-SVC-PRO-012 | P3-P4 |
| **Remaining services** | EXT-SVC-RES-001 to EXT-SVC-RES-024 (non-P1 items), EXT-SVC-CRM-005 to EXT-SVC-CRM-008 | P3-P4 |

---

## 17. Priority Distribution by Domain

```
Domain                  P0  P1  P2  P3  P4  Total
─────────────────────  ──  ──  ──  ──  ──  ─────
trust_and_badges        0   3   8   3   0     14
agency_structure        0   2   6   1   0      9
service_model           0  13  10   5  32     60
workflows               0   6   3   4   1     14
property_model          2   4   5   4   0     15
intent_detection        0   2   4   0   0      6
transaction_types       0   0   5   3   0      8
qualification_engine    0   3   7   1   0     11
crm                     0   5   5   1   0     11
matching                0   6   7   0   0     13
sla                     0   1   5   0   0      6
nba                     0   0   4   0   0      4
permission_model        0   1   3   0   0      4
─────────────────────  ──  ──  ──  ──  ──  ─────
Total                   2  46  72  25  32    175
```

---

## 18. Cross-Reference Index

### By Source Crosswalk

| Source Document | Extension Prefixes | Count |
|----------------|-------------------|-------|
| ROLE_CROSSWALK.md | EXT-RL-TRUST-\*, EXT-RL-BADGE-\*, EXT-RL-AGENCY-\*, EXT-PERM-\* | 31 |
| PROPERTY_TYPE_CROSSWALK.md | EXT-PROP-\* | 15 |
| SERVICE_CROSSWALK.md | EXT-SVC-\* | 60 |
| WORKFLOW_STATE_CROSSWALK.md | EXT-WF-\*, EXT-MAT-\*, EXT-CRM-\*, EXT-SLA-\*, EXT-NBA-\* | 48 |
| INTENT_TRANSACTION_CROSSWALK.md | EXT-INT-\*, EXT-TRX-\*, EXT-QUAL-\* | 25 |

> **Note:** Some extensions reference multiple source documents. Total exceeds 175 due to overlap.

### By New Entity Required

| Entity | Domain | Count of Contributing Extensions |
|--------|--------|----------------------------------|
| **Service** (catalog) | service_model | 45 (all monetized + real estate + CRM services) |
| **ServiceOrder** | service_model / workflows | EXT-SVC-LIFE-001, EXT-WF-005 |
| **Payment** | service_model / workflows | EXT-SVC-LIFE-002, EXT-WF-005 |
| **AgentCredit** | agency_structure | EXT-RL-AGENCY-005 |
| **LeadPurchase** | crm | EXT-SVC-CRM-001 to 004 |
| **Lead** | crm | EXT-CRM-001 to 011, EXT-WF-008 |
| **Match** | matching | EXT-MAT-001 to 013, EXT-WF-001 |
| **Visit** | workflows | EXT-WF-003 |
| **Transaction** | workflows | EXT-WF-004 |
| **Contact** | workflows | EXT-WF-002 |
| **Incident** | workflows | EXT-WF-006 |
| **Mediation** | workflows | EXT-WF-007 |
| **Intent** | intent_detection | EXT-INT-001 to 006 |
| **Document** | (cross-cutting) | EXT-SVC-MON-007, EXT-WF-004 |
| **ApprovalWorkflow** | permission_model | EXT-PERM-001 |
| **AgentInvitation** | workflows | EXT-WF-012 |
| **IdentityResolution** | workflows | EXT-WF-013 |

### By UDM Domain Reference

| UDM Section | Domain Context | Extensions |
|-------------|---------------|------------|
| Domain 1 — User/Role/Profile (§2) | trust_and_badges, agency_structure, permission_model | EXT-RL-TRUST-\*, EXT-RL-BADGE-\*, EXT-RL-AGENCY-001, 007, EXT-PERM-\* |
| Domain 2 — Property/Listing (§3) | property_model | EXT-PROP-\* |
| Domain 3 — Service Model (§4) | service_model | EXT-SVC-\* |
| Domain 4 — Intent/Transaction (§5) | intent_detection, transaction_types | EXT-INT-\*, EXT-TRX-\* |
| Domain 5 — Dossier/Project (§6) | qualification_engine | EXT-QUAL-\* |
| Domain 6 — Matching Engine (§7) | matching | EXT-MAT-\*, EXT-WF-001 |
| Domain 7 — Visit Workflow (§8) | workflows | EXT-WF-003 |
| Domain 8 — Negotiation (§9) | workflows | (via EXT-WF-014 orchestrator) |
| Domain 9 — Transaction (§10) | workflows | EXT-WF-004 |
| Domain 10 — CRM Pipeline (§11) | crm | EXT-CRM-\*, EXT-WF-008, EXT-SVC-CRM-\* |
| Domain 11 — Identity Model (§12) | workflows | EXT-WF-013 |
| Domain 12 — Organization (§13) | agency_structure | EXT-RL-AGENCY-002, 003, 008, 009 |
| Domain 13 — Permission/Security (§14) | permission_model | EXT-PERM-\* |
| Domain 14 — Document Model (§15) | service_model, workflows | EXT-SVC-MON-007, EXT-WF-004 (doc reqs) |
| Domain 15 — Events/Observability (§16) | (all domains) | All extensions generate events |

---

*End of EXTENSION_CATALOG.md — 175 extensions cataloged across 13 domains, 5 priorities, and 5 implementation phases.*
