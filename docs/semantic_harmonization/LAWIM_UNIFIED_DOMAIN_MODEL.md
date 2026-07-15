# LAWIM UNIFIED DOMAIN MODEL (H2 Target)

**Document ID:** LAWIM-HARM-UDM-V1
**Status:** APPROVED — Target model for H2 implementation phase
**Date:** 2026-07-15

---

## Table of Contents

1. [Purpose & Scope](#1-purpose--scope)
2. [Domain 1: User/Role/Profile Model](#2-domain-1-userroleprofile-model)
3. [Domain 2: Property/Listing Model](#3-domain-2-propertylisting-model)
4. [Domain 3: Service Model](#4-domain-3-service-model)
5. [Domain 4: Intent/Transaction Model](#5-domain-4-intenttransaction-model)
6. [Domain 5: Dossier/Project Model](#6-domain-5-dossierproject-model)
7. [Domain 6: Matching Engine](#7-domain-6-matching-engine)
8. [Domain 7: Visit Workflow](#8-domain-7-visit-workflow)
9. [Domain 8: Negotiation Workflow](#9-domain-8-negotiation-workflow)
10. [Domain 9: Transaction Workflow](#10-domain-9-transaction-workflow)
11. [Domain 10: CRM Pipeline](#11-domain-10-crm-pipeline)
12. [Domain 11: Identity Model](#12-domain-11-identity-model)
13. [Domain 12: Organization Model](#13-domain-12-organization-model)
14. [Domain 13: Permission/Security Model](#14-domain-13-permissionsecurity-model)
15. [Domain 14: Document Model](#15-domain-14-document-model)
16. [Domain 15: Events/Observability](#16-domain-15-eventsobservability)
17. [Entity Relationship Summary](#17-entity-relationship-summary)
18. [Legacy Compatibility Layer](#18-legacy-compatibility-layer)

---

## 1. Purpose & Scope

This document defines the **TARGET unified domain model** that reconciles Heritage Gold (legacy LAWIM) with current LAWIM_V2. It is code-independent and represents the semantic target for H2 implementation.

### 1.1 Status Legend

| Status | Meaning |
|--------|---------|
| **RETAIN_CURRENT** | Keep current V2 model as-is; no changes needed |
| **ENRICH_CURRENT** | Extend current V2 model with Heritage Gold concepts |
| **EXTEND_CURRENT** | Create new entities/engine based on Heritage Gold (no current equivalent) |
| **REPLACE_CURRENT_CONCEPT** | Replace current V2 concept with Heritage Gold equivalent |
| **HUMAN_DECISION_REQUIRED** | Cannot reconcile without product/domain decision |

### 1.2 Source Documents

- `ROLE_CROSSWALK.md` — Role, badge, trust, agency reconciliation
- `PROPERTY_TYPE_CROSSWALK.md` — Property taxonomy reconciliation
- `SERVICE_CROSSWALK.md` — Service catalog reconciliation
- `WORKFLOW_STATE_CROSSWALK.md` — State machine reconciliation
- `INTENT_TRANSACTION_CROSSWALK.md` — Intent/project reconciliation
- `SEMANTIC_CONFLICTS.md` — 13 identified semantic conflicts
- `REQUIRED_EXTENSIONS.md` — 175 extension concepts cataloged

---

## 2. Domain 1: User/Role/Profile Model

**Status:** ENRICH_CURRENT

### 2.1 Entity: User (Core Identity)

| Aspect | Detail |
|--------|--------|
| **Status** | ENRICH_CURRENT |
| **Gold Source** | `user` (Heritage Gold) with 7-level hierarchy, trust levels, badges |
| **Current V2** | `User` model with 5 official roles, 27 business profiles, flat structure |
| **Unified Target** | Keep V2's 5 official roles as permission-bearing structure. Add trust levels, badges, and agency role as enriched fields. Role hierarchy from Gold is mapped via lookup table, not inheritance chain. |

#### Key Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `id` | UUID | V2 | Primary identifier |
| `email` | String | V2 | Email address (unique) |
| `phone` | String | V2 | Phone number |
| `role` | Enum | V2 | `admin \| manager \| operator \| partner \| user` |
| `business_profiles` | String[] | V2 | 27 business profile labels |
| `trust_level` | Int (1-6) | **ENRICH** | Trust graduation: 1=New, 2=PhoneVerified, 3=IdentityVerified, 4=ProDocsValidated, 5=VerifiedPro, 6=Reference |
| `badges` | JSON[] | **ENRICH** | Derived badges: phone_verified, email_verified, identity_verified, owner_verified, agency_verified, partner_lawim, professional_verified, agent_active |
| `phone_verified` | Boolean | **ENRICH** | Phone verified via OTP |
| `email_verified` | Boolean | **ENRICH** | Email verified |
| `identity_verified` | Boolean | **ENRICH** | Identity doc verified |
| `professional_docs_verified` | Boolean | **ENRICH** | Professional credentials verified |
| `professional_verified` | Boolean | **ENRICH** | Full professional verification |
| `owner_verified` | Boolean | **ENRICH** | Property ownership verified |
| `is_active_agent` | Boolean | **ENRICH** | Fully onboarded active agent |
| `agency_role` | Enum | **ENRICH** | `responsible \| admin \| agent \| assistant` (scoped by organization_id) |
| `reference_account` | Boolean | **ENRICH** | Admin-granted reference status |
| `onboarding_status` | Enum | **ENRICH** | `invited \| account_created \| phone_verified \| cni_uploaded \| validated \| active` |
| `agent_rating` | Float | **ENRICH** | 1-5 post-interaction rating |
| `agent_credits` | Int | **ENRICH** | Current agent credit balance |
| `total_credits_spent` | Int | **ENRICH** | Lifetime credits spent |
| `last_credit_recharge` | DateTime | **ENRICH** | Last credit recharge timestamp |

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Organization | N:1 | User belongs to an organization (agency) |
| Project | 1:N | User creates/manages projects |
| Property | 1:N | User owns/list properties |
| Visit | 1:N | User participates in visits |
| Transaction | 1:N | User is party to transactions |
| Lead | 1:N | User is tracked as lead or assigned as agent |
| Document | 1:N | User uploads documents |

---

## 3. Domain 2: Property/Listing Model

**Status:** ENRICH_CURRENT (with EXTEND)

### 3.1 Entity: Property

| Aspect | Detail |
|--------|--------|
| **Status** | ENRICH_CURRENT |
| **Gold Source** | `property` with 7 families, 11+ types, 107 qualification matrices, 10-step lifecycle, 6 price levels |
| **Current V2** | `Property` model with free-form type, 5 statuses, price_min/price_max, metadata_json |
| **Unified Target** | Keep current Property entity as core. Add property_family enum, property_type taxonomy (reference data), 10-step lifecycle, publication rules engine, multilevel pricing, data quality scoring. |

#### Key Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `id` | UUID | V2 | Primary identifier |
| `title` | String | V2 | Property title |
| `description` | Text | V2 | Property description |
| `property_family` | Enum | **ENRICH** | `residential \| commercial \| industrial \| land \| agricultural \| hotel \| project` |
| `property_type` | String (ref) | **ENRICH** | Reference data key into PROPERTY_TYPES taxonomy |
| `property_subtype` | String | **ENRICH** | Sub-referentiel type per family (metadata_json) |
| `status` | Enum | **ENRICH** | Enriched lifecycle: `creation \| normalization \| classification \| validation \| published \| matching \| visit \| negotiation \| transaction \| archived \| conserved` |
| `availability` | Enum | **ENRICH** | `available \| pending \| rented \| sold \| archived` |
| `price_displayed` | Decimal | **ENRICH** | Single displayed price (primary price) |
| `price_negotiable` | Decimal | **ENRICH** | Negotiable price (if different from displayed) |
| `price_final` | Decimal | **ENRICH** | Final transaction price |
| `price_estimation` | Decimal | **ENRICH** | Estimated value |
| `price_min` | Decimal | V2 | Minimum price range (retained) |
| `price_max` | Decimal | V2 | Maximum price range (retained) |
| `negotiable` | Boolean | **ENRICH** | Whether price is negotiable |
| `price_type` | Enum | **ENRICH** | `rent \| sale \| deposit \| caution \| monthly \| fees \| taxes` |
| `surface` | Decimal | V2 | Surface area |
| `bedrooms` | Int | V2 | Number of bedrooms |
| `bathrooms` | Int | V2 | Number of bathrooms |
| `location` | JSON | V2 | Location data (city, neighborhood, coordinates) |
| `metadata_json` | JSON | V2 | Extensible per-type specific fields |
| `owner_id` | UUID | V2 | Reference to User (owner/detenteur) |
| `quality_score` | Float | **ENRICH** | Data quality score (0-100) |
| `quality_grade` | String | **ENRICH** | A+, A, B, C, D grade |
| `boost_level` | Enum | **ENRICH** | `none \| boost_7d \| boost_30d \| premium` |
| `boost_expires_at` | DateTime | **ENRICH** | Boost expiration |
| `is_premium` | Boolean | **ENRICH** | Premium listing flag |
| `verification_status` | Enum | **ENRICH** | `unverified \| pending \| verified \| rejected` |
| `published_at` | DateTime | V2 | Publication date |
| `expires_at` | DateTime | **ENRICH** | Auto-archive date (90d from last activity) |
| `last_activity_at` | DateTime | **ENRICH** | Last activity timestamp |

#### Publication Rules Engine (8 rules)

| Rule | Description |
|------|-------------|
| 1. Family check | property_family must be set |
| 2. Type check | property_type must be valid per family |
| 3. Location check | city + neighborhood required |
| 4. Price check | At least price_displayed must be > 0 |
| 5. Holder check | owner_id must be a verified user |
| 6. Normalization check | Fields must pass normalization |
| 7. Documents check | Required documents per type must be uploaded |
| 8. Reference code check | SIE reference code must be generated |

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| User (owner) | N:1 | Property owner/detenteur |
| User (agent) | N:1 | Managing agent |
| Organization | N:1 | Managing agency |
| Media | 1:N | Property photos/videos |
| Document | 1:N | Property documents (title, permits) |
| Visit | 1:N | Scheduled visits |
| Match | 1:N | Match scores with demandeurs |
| Transaction | 0:1 | Completed transaction |

---

## 4. Domain 3: Service Model

**Status:** EXTEND_CURRENT (new entity)

### 4.1 Entity: Service

| Aspect | Detail |
|--------|--------|
| **Status** | EXTEND_CURRENT |
| **Gold Source** | 72 services (13 monetized, 24 real estate, 27 professional, 8 CRM), fixed pricing, payment lifecycle |
| **Current V2** | No service model — no catalog, no pricing, no payment processing |
| **Unified Target** | Create Service entity as a monetized catalog item with fixed price, type classification, and lifecycle state. Link to ServiceOrder for customer purchases and Payment for processing. |

#### Key Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `id` | UUID | **NEW** | Primary identifier |
| `code` | String | **NEW** | Unique service code (e.g., `boost_7j`, `lead_bronze`) |
| `name` | String | **NEW** | Display name |
| `description` | Text | **NEW** | Service description |
| `category` | Enum | **NEW** | `monetized \| real_estate \| professional \| crm` |
| `price_fcfa` | Int | **NEW** | Fixed price in FCFA |
| `currency` | String | **NEW** | Currency (default: XAF) |
| `is_active` | Boolean | **NEW** | Whether service is currently offered |
| `duration_days` | Int | **NEW** | Service duration (for time-based services) |
| `lifecycle_state` | Enum | **NEW** | `creation \| proposition \| acceptation \| paiement \| activation \| utilisation \| expiration \| archivage` |

#### 4.1.1 Monetized Service Catalog (13)

| Code | Name | Price (FCFA) | Category |
|------|------|-------------|----------|
| `boost_7j` | Boost visibilité 7 jours | 2 000 | monetized |
| `boost_30j` | Boost visibilité 30 jours | 5 000 | monetized |
| `premium_listing` | Annonce premium | 10 000 | monetized |
| `agent_pro` | Abonnement agent professionnel | 10 000/mois | monetized |
| `accompagnement_visite` | Accompagnement de visite | 50 000 | monetized |
| `accompagnement_transaction` | Accompagnement de transaction | 50 000 | monetized |
| `controle_documentaire` | Contrôle documentaire | 5 000 | monetized |
| `photographie` | Photographie professionnelle | 15 000 | monetized |
| `video` | Vidéo professionnelle | 25 000 | monetized |
| `verification` | Vérification de bien | 10 000 | monetized |
| `mise_en_relation` | Mise en relation payante | 500 | monetized |
| `assistance` | Assistance personnalisée | 50 000 | monetized |
| `visibilite_premium` | Visibilité premium | 7 500 | monetized |

#### 4.1.2 CRM Lead Services

| Code | Name | Price (FCFA) | Details |
|------|------|-------------|---------|
| `lead_bronze` | Lead Bronze | 500 | 1 contact |
| `lead_silver` | Lead Silver | 1 500 | 5 contacts |
| `lead_gold` | Lead Gold | 3 000 | 15 contacts |
| `deblocage_coordonnees` | Déblocage coordonnées propriétaire | 500 | — |
| `demandeur_premium` | Demandeur Premium | 1 000 | — |
| `diaspora_simple` | Diaspora Simple | 25 000 | — |
| `diaspora_rapport` | Diaspora Rapport | 50 000 | — |
| `diaspora_complet` | Diaspora Complet | 75 000 | — |
| `agent_business` | Abonnement Agent Business | 25 000/mois | — |

### 4.2 Entity: ServiceOrder

| Aspect | Detail |
|--------|--------|
| **Status** | EXTEND_CURRENT |
| **Gold Source** | Service ordering and payment lifecycle |
| **Current V2** | None |
| **Unified Target** | Represents a customer's purchase of a service. Tracks the order lifecycle from proposition through payment to activation and usage. |

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `service_id` | UUID | Reference to Service |
| `buyer_id` | UUID | Reference to User (buyer) |
| `property_id` | UUID? | Optional property context |
| `project_id` | UUID? | Optional project context |
| `price_paid` | Decimal | Actual price paid |
| `currency` | String | Transaction currency |
| `status` | Enum | `created \| proposed \| accepted \| payment_pending \| paid \| activated \| in_use \| expired \| archived \| cancelled` |
| `activated_at` | DateTime | When service was activated |
| `expires_at` | DateTime | When service expires |
| `cancelled_at` | DateTime | When cancelled |
| `cancellation_reason` | String | Reason for cancellation |

### 4.3 Entity: Payment

| Aspect | Detail |
|--------|--------|
| **Status** | EXTEND_CURRENT |
| **Gold Source** | Campay Mobile Money integration, 10 payment sub-states |
| **Current V2** | Feature flag payments=OFF; no payment processing |
| **Unified Target** | Tracks payment lifecycle for service orders. Integrates with Campay for mobile money processing. |

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `service_order_id` | UUID | Reference to ServiceOrder |
| `amount` | Decimal | Payment amount |
| `currency` | String | Currency (XAF) |
| `provider` | String | Payment processor (campay) |
| `provider_reference` | String | External payment reference |
| `phone_number` | String | Payer phone number |
| `status` | Enum | `created \| initiated \| pending \| confirmed \| failed \| cancelled \| expired \| refunded \| reconciled \| disputed` |
| `initiated_at` | DateTime | Payment initiation time |
| `confirmed_at` | DateTime | Payment confirmation time |
| `failed_at` | DateTime | Payment failure time |
| `failure_reason` | String | Failure reason |
| `refunded_at` | DateTime | Refund time |
| `disputed_at` | DateTime | Dispute time |
| `dispute_reason` | String | Dispute reason |

### 4.4 Entity: AgentCredit

| Aspect | Detail |
|--------|--------|
| **Status** | EXTEND_CURRENT |
| **Gold Source** | Agent credit system with boost purchases, lead purchasing |
| **Current V2** | None |
| **Unified Target** | Tracks agent credit balance and transactions. Credits are consumed for lead purchases and boost activations. |

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `agent_id` | UUID | Reference to User (agent) |
| `balance` | Int | Current credit balance |
| `total_purchased` | Int | Lifetime credits purchased |
| `total_consumed` | Int | Lifetime credits consumed |
| `last_recharge_at` | DateTime | Last recharge timestamp |
| `last_recharge_amount` | Int | Last recharge amount |

### 4.5 Entity: LeadPurchase

| Aspect | Detail |
|--------|--------|
| **Status** | EXTEND_CURRENT |
| **Gold Source** | Lead purchasing (mise en relation payante) |
| **Current V2** | None |
| **Unified Target** | Tracks when an agent purchases a lead (contact information for a demandeur or property owner). |

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `agent_id` | UUID | Purchasing agent |
| `lead_id` | UUID | Reference to Lead |
| `service_order_id` | UUID | Reference to ServiceOrder |
| `credits_spent` | Int | Credits consumed |
| `purchased_at` | DateTime | Purchase timestamp |
| `contact_revealed` | Boolean | Whether contact was revealed |

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| ServiceOrder | N:1 | Links payment to service purchase |
| Payment | 1:1 | Payment for service order |
| AgentCredit | 1:N | Agent credit transactions |
| LeadPurchase | 1:N | Lead purchases from credits |
| Property (boost) | N:1 | Boost/premium applied to property |
| User (subscription) | N:1 | Agent subscription to User |

---

## 5. Domain 4: Intent/Transaction Model

**Status:** ENRICH_CURRENT

### 5.1 Entity: Intent (new concept, integrated with Project)

| Aspect | Detail |
|--------|--------|
| **Status** | ENRICH_CURRENT |
| **Gold Source** | Intent detection pipeline with keyword scoring, 0.70 threshold, FR/EN/PID, multi-intent, urgency detection |
| **Current V2** | No intent detection; users explicitly select project_type |
| **Unified Target** | Add intent detection as an optional layer on top of explicit project_type selection. Support chat-based (WhatsApp/Telegram) and form-based (dashboard) interaction paradigms. |

#### Key Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `id` | UUID | **NEW** | Primary identifier |
| `source_text` | Text | **NEW** | Original user utterance |
| `language` | Enum | **NEW** | `fr \| en \| pid` |
| `detected_intent` | Enum | **NEW** | `buy \| rent \| sell \| invest \| search_property \| find_professional \| service \| finance \| other` |
| `confidence` | Float | **NEW** | Detection confidence (0.0-1.0) |
| `threshold` | Float | **NEW** | Configurable threshold (default 0.70) |
| `is_multi_intent` | Boolean | **NEW** | Multiple intents detected |
| `sub_intents` | JSON[] | **NEW** | Array of sub-intent objects |
| `urgency_score` | Float | **NEW** | Detected urgency (0.0-1.0) |
| `extracted_entities` | JSON | **NEW** | Budget, location, property type, timeline |
| `detection_method` | Enum | **NEW** | `keyword \| explicit_selection \| hybrid` |
| `project_type_mapping` | Enum | **NEW** | Mapped to V2 project_type |
| `created_at` | DateTime | **NEW** | Detection timestamp |

#### 5.1.1 Intent-to-Project_Type Mapping

| Detected Intent | Project Type | Roles Implied |
|----------------|-------------|---------------|
| `buy` | buy | buyer |
| `rent` | rent | tenant |
| `sell` | sell | seller |
| `invest` | invest | investor |
| `search_property` | buy/rent | visitor |
| `find_professional` | find | client |
| `service` | service | client |
| `finance` | invest | investor |
| `other` | other | visitor |
| `multi` | (multiple projects) | per sub-intent |

#### 5.1.2 Intent Score Weights

| Intent | Base Weight | Description |
|--------|------------|-------------|
| BUY | 50 | Purchase intent |
| RENT | 30 | Rental intent |
| SELL | 60 | Selling intent |
| INVEST | 100 | Investment intent (highest) |
| SEARCH_PROPERTY | 25 | Exploratory search (lowest) |

### 5.2 Entity: Project (retained as user journey tracker)

Keep current `Project` entity. The Project model remains the user-facing journey tracker. Intent detection feeds into project creation by auto-populating project_type and initial qualification data.

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| All existing V2 fields | — | V2 | Current project model retained |
| `intent_id` | UUID? | **ENRICH** | Optional link to detected intent |
| `detected_intent` | Enum? | **ENRICH** | Original detected intent for audit |

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Intent | 1:1 | Project originated from intent detection |
| Project | 1:0..1 | May have associated transaction |
| User | N:1 | Project creator |
| Property | N:M | Properties matched/associated |

---

## 6. Domain 5: Dossier/Project Model

**Status:** ENRICH_CURRENT

### 6.1 Entity: Project (as Dossier equivalent)

| Aspect | Detail |
|--------|--------|
| **Status** | ENRICH_CURRENT |
| **Gold Source** | `dossier` with 14 states, matching lifecycle, double consent, holder decision chain, rematching |
| **Current V2** | `Project` with 5 statuses, journey steps, no matching/consent logic |
| **Unified Target** | Keep `Project` as the entity name (no breaking API change). Add dossier-specific states, double consent workflow, holder decision tracking, and automatic rematching. |

#### Enriched Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `id` | UUID | V2 | Primary identifier |
| `title` | String | V2 | Project title |
| `project_type` | Enum | V2 | `buy \| rent \| sell \| invest \| find \| service \| other` |
| `status` | Enum | V2 | Retained for backward compatibility |
| `dossier_state` | Enum | **ENRICH** | `creation \| qualification \| matching \| presentation \| wait_demandeur \| wait_holder \| mise_en_relation \| visit \| negotiation \| agreement \| transaction \| closure \| archive` |
| `matching_status` | Enum | **ENRICH** | `not_started \| in_progress \| completed \| rematching \| failed` |
| `double_consent_status` | Enum | **ENRICH** | `not_started \| demandeur_interested \| holder_contacted \| holder_favorable \| consent_obtained \| refused \| expired` |
| `rematching_count` | Int | **ENRICH** | Number of rematching cycles |
| `max_rematches` | Int | **ENRICH** | Maximum allowed rematches (default 3) |
| `holder_id` | UUID? | **ENRICH** | Current holder being negotiated with |
| `matched_property_id` | UUID? | **ENRICH** | Currently matched property |
| `decision_deadline` | DateTime | **ENRICH** | Deadline for current decision |
| `qualification_step` | Int | **ENRICH** | Current step in 10-step qualification order |

#### 6.1.1 Qualification Order (10 steps)

| Step | Action | Description |
|------|--------|-------------|
| 1 | Intention | Determine primary intent (buy/rent/sell/invest) |
| 2 | Type | Property type classification |
| 3 | Ville | City selection |
| 4 | Quartier | Neighborhood preference |
| 5 | Budget | Budget range |
| 6 | Délai | Timeline |
| 7 | Critères | Specific criteria (bedrooms, surface, features) |
| 8 | Préférences | Preferences (furnished, floor, parking) |
| 9 | Confirmation | Qualification summary confirmation |
| 10 | Escalade | Escalate to agent if incomplete |

#### 6.1.2 Double Consent Workflow

```
Matching Complete
    → Demandeur Interested (consent 1/2)
        → Holder Contacted
            → Holder Favorable (consent 2/2)
                → Double Consent Obtained → Mise en Relation Established
            → Holder Refuses → Rematching
            → Holder Silence (72h) → Reminder 1 → Reminder 2 → Last Reminder → Property "to confirm" → Rematching
```

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| User (creator) | N:1 | Project owner (demandeur) |
| User (holder) | N:1 | Current property holder |
| Property | N:M | Matched properties |
| Match | 1:N | Match scores |
| Visit | 0:N | Scheduled visits |
| Transaction | 0:1 | Completed transaction |
| Intent | 0:1 | Source intent detection |

---

## 7. Domain 6: Matching Engine

**Status:** EXTEND_CURRENT (new engine)

### 7.1 Entity: Match

| Aspect | Detail |
|--------|--------|
| **Status** | EXTEND_CURRENT |
| **Gold Source** | Full algorithmic matching engine: 5 score families, 9 matching roles, 4 compatibility levels, geographic scoring, boost/penalty rules, rematching engine |
| **Current V2** | No matching engine — properties listed, users search/contact manually |
| **Unified Target** | Implement full matching engine with 5 scoring dimensions, 9 matching roles, H0.5 weight distribution, geographic scoring with 5 levels and 3 mobility modes, 4 compatibility levels, rematching engine, minimum score 60/100, top 10 results. |

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to Project (demandeur dossier) |
| `property_id` | UUID | Reference to Property |
| `agent_id` | UUID? | Reference to assigned agent |
| `overall_score` | Float | Composite score (0-100) |
| `compatibility_level` | Enum | `excellent \| good \| average \| low` |
| `rank` | Int | Ranking position for this project |
| `is_active` | Boolean | Whether match is currently active |
| `is_proposed` | Boolean | Whether match has been proposed to demandeur |
| `demandeur_decision` | Enum? | `pending \| interested \| not_interested` |
| `holder_decision` | Enum? | `pending \| favorable \| refused` |
| `rematch_count` | Int | Number of rematches for this pair |
| `created_at` | DateTime | Match creation timestamp |
| `expires_at` | DateTime | Match expiration (auto-recalculate) |

### 7.2 Score Dimensions

#### 7.2.1 Five Score Families

| Family | Sub-dimensions | Weight (H0.5) | Description |
|--------|---------------|---------------|-------------|
| **Geographical** | Location proximity, zone preference | H0.5 × 0.25 | Distance-based scoring with 5 levels |
| **Budget** | Price alignment, negotiability | H0.5 × 0.20 | Budget range compatibility |
| **Property** | Type match, surface, bedrooms, features | H0.5 × 0.20 | Property characteristics alignment |
| **Behavioral** | Response time, profile completeness | H0.5 × 0.15 | User behavior signals |
| **Other** | Documentation, trust level | H0.5 × 0.10 | Secondary factors |
| **Transaction Success** | Predicted success probability | H0.5 × 0.10 | Historical success prediction |

#### 7.2.2 Geographic Scoring (5 levels)

| Level | Distance | Score (base) | Description |
|-------|----------|-------------|-------------|
| L1 | Same neighborhood | 100 | Exact location match |
| L2 | Same city, diff neighborhood | 75 | City-level match |
| L3 | Same region, diff city | 50 | Regional match |
| L4 | Same country, diff region | 25 | Country-level match |
| L5 | Different country | 0 | No geographic match |

#### 7.2.3 Mobility Modes

| Mode | Radius | Decay Function |
|------|--------|---------------|
| Low mobility | 5 km | Steep linear decay |
| Medium mobility | 20 km | Gradual decay |
| High mobility | 50+ km | Shallow decay |

### 7.3 Matching Roles (9)

| Role | Type | Description |
|------|------|-------------|
| `hard_constraint` | Filter | Binary pass/fail (e.g., budget range entirely disjoint) |
| `strong_preference` | Weighted | Strongly weighted scoring factor |
| `weak_preference` | Weighted | Lightly weighted scoring factor |
| `nice_to_have` | Boost | Bonus if present, no penalty if absent |
| `deal_breaker` | Filter | Any mismatch → match rejected |
| `tie_breaker` | Rank | Used only when scores are equal |
| `exclusion` | Filter | Presence explicitly excludes |
| `boost` | Modifier | Applied after base scoring |
| `transaction_blocker` | Filter | Blocks transaction if conditions not met |

### 7.4 Compatibility Levels

| Level | Score Range | Action |
|-------|-------------|--------|
| Excellent | 85-100 | Auto-propose to demandeur |
| Good | 70-84 | Propose with qualification note |
| Average | 60-69 | Propose only if no better matches |
| Low | < 60 | Not proposed; held for progressive expansion |

### 7.5 Rematching Engine

| Trigger | Action |
|---------|--------|
| Demandeur refuses match | Exclude property, recalculate, propose next |
| Holder refuses contact | Exclude property, recalculate, propose next |
| Visit fails (no-show) | Offer rematch with same property or new |
| Negotiation fails | Offer rematch with new property |
| Match expires (30d) | Recalculate score, re-propose if still valid |
| New property listed | Evaluate against all active dossiers |
| Dossier updated | Recalculate all matches |

#### 7.5.1 Boost/Penalty Rules

| Type | Rule | Value | Caps |
|------|------|-------|------|
| Boost | Premium listing | +10 | Max total boost: +50 |
| Boost | Agent pro subscription | +15 | Max total boost: +50 |
| Boost | Complete dossier | +10 | Max total boost: +50 |
| Boost | Verified identity | +5 | Max total boost: +50 |
| Boost | Urgent demandeur | +20 | Max total boost: +50 |
| Penalty | Incomplete dossier | -10 | Min total: 0 |
| Penalty | Unverified phone | -15 | Min total: 0 |
| Penalty | Spam-like behavior | -50 | Min total: 0 |

### 7.6 Minimum Match Score

- **Minimum score to propose:** 60/100
- **Maximum results per proposal:** Top 10

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | N:1 | Demandeur dossier being matched |
| Property | N:1 | Property being matched |
| User (agent) | N:1 | Assigned agent |

---

## 8. Domain 7: Visit Workflow

**Status:** EXTEND_CURRENT (new entity)

### 8.1 Entity: Visit

| Aspect | Detail |
|--------|--------|
| **Status** | EXTEND_CURRENT |
| **Gold Source** | Visit lifecycle: 9 states, automatic reminders, satisfaction tracking, absence handling |
| **Current V2** | No Visit entity — visits handled ad-hoc via Conversation messages |
| **Unified Target** | Create Visit entity with 9-state lifecycle, automatic reminder system (24h and 2h before), post-visit satisfaction tracking, absence/no-show handling with business rules. |

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to Project |
| `property_id` | UUID | Reference to Property |
| `demandeur_id` | UUID | Visiting demandeur |
| `holder_id` | UUID | Property holder/host |
| `agent_id` | UUID? | Accompanying agent (if accompagnement_visite service) |
| `scheduled_at` | DateTime | Scheduled visit datetime |
| `status` | Enum | `requested \| awaiting_confirmation \| confirmed \| rescheduled \| cancelled \| completed \| refused \| absent_demandeur \| absent_holder` |
| `confirmation_deadline` | DateTime | Deadline for holder to confirm |
| `cancellation_reason` | String? | Reason if cancelled |
| `rescheduled_to` | DateTime? | New datetime if rescheduled |
| `satisfaction_demandeur` | Int? | 1-5 demandeur satisfaction |
| `satisfaction_holder` | Int? | 1-5 holder satisfaction |
| `absence_type` | Enum? | `demandeur_no_show \| holder_no_show` |
| `reminder_24h_sent` | Boolean | 24h reminder sent |
| `reminder_2h_sent` | Boolean | 2h reminder sent |
| `notes` | Text | Visit notes |
| `created_at` | DateTime | Visit creation |
| `completed_at` | DateTime | Visit completion |

#### 8.1.1 Visit States

```
Requested → Awaiting Confirmation → Confirmed → Completed
                                     → Rescheduled
                                     → Cancelled
                                     → Refused
                                     → Absent (demandeur)
                                     → Absent (holder)
```

#### 8.1.2 Reminder System

| Timing | Channel | Action |
|--------|---------|--------|
| 24h before | WhatsApp/Telegram | Remind both parties of scheduled visit |
| 2h before | WhatsApp/Telegram | Final reminder with address/contact |
| 30min after scheduled | WhatsApp/Telegram | Confirm visit occurred; handle absence |
| Post-visit (1h) | WhatsApp/Telegram | Collect satisfaction rating |

#### 8.1.3 Absence Handling

| Scenario | Action |
|----------|--------|
| Demandeur no-show | Log absence, notify holder, offer reschedule |
| Holder no-show | Log absence, notify demandeur, offer reschedule or rematch |
| Both absent | Log both absences, escalate to agent |
| 3rd demandeur no-show | Flag demandeur account, reduce trust level |
| 3rd holder no-show | Flag property, reduce holder reliability score |

#### 8.1.4 NBA Post-Visit

| Satisfaction | Next Best Action |
|-------------|------------------|
| Très satisfait (4-5) | Open negotiation |
| Mitigé (3) | Propose second visit |
| Insatisfait (1-2) | Propose another property / rematch |

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | N:1 | Visit belongs to project |
| Property | N:1 | Property being visited |
| User (demandeur) | N:1 | Visiting user |
| User (holder) | N:1 | Hosting user |
| User (agent) | N:1 | Accompanying agent |

---

## 9. Domain 8: Negotiation Workflow

**Status:** ENRICH_CURRENT

### 9.1 Conversation Domain (Negotiation)

| Aspect | Detail |
|--------|--------|
| **Status** | ENRICH_CURRENT |
| **Gold Source** | Negotiation stages with offer/counter-offer tracking, negotiable elements per transaction type, reminder system on silence, post-failure diagnostic |
| **Current V2** | `conversation_domain` with negotiation stages (interest → negotiation → agreement → closed) |
| **Unified Target** | Keep current conversation negotiation stages. Enrich with offer/counter-offer tracking, negotiable elements per transaction type, silent-reminder system, and post-failure diagnostic. |

#### Enriched Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `negotiation_status` | Enum | V2+ | `not_started \| demandeur_proposes \| holder_responds \| counter_offer \| accepted \| rejected \| silent \| failed \| escalated` |
| `current_offer_amount` | Decimal | **ENRICH** | Current offer on the table |
| `current_offer_by` | UUID | **ENRICH** | User who made current offer |
| `offer_history` | JSON[] | **ENRICH** | Array of {amount, by, at, message} |
| `negotiable_elements` | JSON | **ENRICH** | Per transaction type negotiable items |
| `silence_started_at` | DateTime | **ENRICH** | When silence period started |
| `reminder_count` | Int | **ENRICH** | Number of reminders sent |
| `last_reminder_at` | DateTime | **ENRICH** | Last reminder timestamp |
| `failure_reason` | Enum? | **ENRICH** | `price_disagreement \| terms_disagreement \| silence \| third_party \| other` |
| `failure_diagnostic` | JSON | **ENRICH** | Structured failure analysis |

#### 9.1.1 Negotiables Per Transaction Type

| Transaction Type | Negotiables |
|-----------------|-------------|
| Vente (Sale) | Price, payment schedule, closing date, inclusions |
| Location (Rental) | Rent, deposit, lease duration, maintenance responsibility |
| Bail commercial | Rent, deposit, renovation responsibility, duration |
| Investissement | Price, ROI terms, management, exit strategy |

#### 9.1.2 Reminder System on Silence

| Day | Action |
|-----|--------|
| 48h silence | First reminder: "Do you have a response to the offer?" |
| 96h silence | Second reminder: "We haven't heard from you. Would you like to counter-offer?" |
| 168h silence (7d) | Final reminder: "Without response, negotiation will close." |
| 240h silence (10d) | Auto-close negotiation as "failed (silence)" |

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | 1:1 | Negotiation belongs to project |
| User (demandeur) | N:1 | Demandeur participant |
| User (holder) | N:1 | Holder participant |
| Visit | 0:1 | Preceding visit |

---

## 10. Domain 9: Transaction Workflow

**Status:** EXTEND_CURRENT (new entity)

### 10.1 Entity: Transaction

| Aspect | Detail |
|--------|--------|
| **Status** | EXTEND_CURRENT |
| **Gold Source** | Transaction entity with 10 states, type-specific document requirements, party roles, payment integration, 6 transaction types |
| **Current V2** | No dedicated transaction entity; Project serves as deal tracker |
| **Unified Target** | Create Transaction entity as the legal/financial deal-closing entity. Link to Project (0..1:1). Implement 7-state lifecycle, per-type document requirements, party involvement tracking, payment milestones. |

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to originating Project |
| `property_id` | UUID | Reference to Property |
| `transaction_type` | Enum | `sale \| rental \| lease \| commercial_lease \| seasonal_rental \| investment` |
| `status` | Enum | `agreement \| preparation \| documents \| payment \| signature \| handover \| completed \| failed \| archived` |
| `demandeur_id` | UUID | Primary demandeur/buyer/tenant |
| `holder_id` | UUID | Property holder/seller/owner |
| `agent_id` | UUID? | Managing agent |
| `notaire_id` | UUID? | Notary (if applicable) |
| `price_agreed` | Decimal | Agreed transaction price |
| `currency` | String | Currency |
| `payment_milestones` | JSON[] | Array of milestone {description, amount, due_date, paid_at} |
| `signature_demandeur_at` | DateTime? | Demandeur signature timestamp |
| `signature_holder_at` | DateTime? | Holder signature timestamp |
| `handover_at` | DateTime? | Key handover / possession date |
| `completed_at` | DateTime? | Transaction completion |
| `failed_at` | DateTime? | Transaction failure |
| `failure_reason` | String? | Reason for failure |
| `follow_up_at` | DateTime? | Post-transaction follow-up date |
| `follow_up_notes` | Text? | Follow-up outcome |
| `created_at` | DateTime | Transaction creation |

#### 10.1.1 Transaction States

```
Agreement → Preparation → Documents → Payment → Signature → Handover → Completed
                                                                        → Failed
                                                                        → Archived
```

#### 10.1.2 Document Requirements Per Type

| Transaction Type | Required Documents |
|-----------------|-------------------|
| Sale | Land title, seller ID, buyer ID, power of attorney (if applicable), tax clearance |
| Rental | Lease contract, deposit receipt, inventory of fixtures, ID copies |
| Commercial Lease | Commercial lease contract, company registration (RCCM), tax ID |
| Seasonal Rental | Short-term rental contract, ID copy, deposit |
| Investment | Investment agreement, property title, financial documents |

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | 0..1:1 | Originating project (optional for direct transactions) |
| Property | N:1 | Property being transacted |
| User (demandeur) | N:1 | Buyer/tenant |
| User (holder) | N:1 | Seller/owner |
| User (agent) | N:1 | Managing agent |
| User (notaire) | N:1 | Notary |
| Document | 1:N | Transaction documents |

---

## 11. Domain 10: CRM Pipeline

**Status:** EXTEND_CURRENT

### 11.1 Entity: Lead

| Aspect | Detail |
|--------|--------|
| **Status** | EXTEND_CURRENT |
| **Gold Source** | 8-stage CRM pipeline, lead scoring (base + boosters - penalties), 5 classification levels, CRM routing, 7-factor scoring, 8 tracked behaviors, 4 anti-fraud layers |
| **Current V2** | No CRM model — basic User + Organization only |
| **Unified Target** | Create Lead entity as the central CRM concept. Implement 8-stage pipeline from incoming message through routing. Scoring engine with base score + boosters - penalties. Classification into HOT/WARM/COLD/LOW/SPAM. Geographic routing engine. 4-layer anti-fraud. |

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `source_channel` | Enum | `whatsapp \| telegram \| dashboard \| api \| referral` |
| `source_text` | Text | Original incoming message |
| `normalized_text` | Text | Normalized text (lowercase, unicode normalized) |
| `language` | Enum | `fr \| en \| pid` |
| `pipeline_stage` | Enum | `incoming \| normalized \| extracted \| intent_detected \| enriched \| scored \| classified \| routed` |
| `detected_intent` | Enum? | Detected primary intent |
| `intent_confidence` | Float? | Intent detection confidence |
| `lead_type` | Enum? | `tenant \| buyer \| seller \| investor \| diaspora_investor` |
| `base_score` | Int | Base score by lead type |
| `boosters_applied` | JSON[] | Array of booster {type, value} |
| `penalties_applied` | JSON[] | Array of penalty {type, value} |
| `total_boost` | Int | Sum of all boosters |
| `total_penalty` | Int | Sum of all penalties |
| `final_score` | Int | base_score + total_boost - total_penalty |
| `classification` | Enum | `hot \| warm \| cold \| low \| spam` |
| `routed_to_agent_id` | UUID? | Assigned agent |
| `routed_at` | DateTime? | Route assignment timestamp |
| `routing_method` | Enum? | `zone \| availability \| score \| manual` |
| `is_fraud` | Boolean | Flagged as potential fraud |
| `fraud_layers_triggered` | String[] | Which anti-fraud layers fired |
| `fraud_action_taken` | Enum? | `none \| flag \| temporary_suspend \| block` |
| `user_id` | UUID? | Linked to existing User if identified |
| `phone` | String | Contact phone |
| `email` | String? | Contact email |
| `name` | String | Contact name |
| `city` | String? | Detected city |
| `neighborhood` | String? | Detected neighborhood |
| `budget_min` | Decimal? | Detected budget range |
| `budget_max` | Decimal? | |
| `urgency` | Enum? | `low \| medium \| high \| urgent` |
| `is_diaspora` | Boolean | Diaspora indicator |
| `cash_purchase` | Boolean | Cash purchase indicator |
| `sla_priority` | Enum | `p0 \| p1 \| p2 \| p3` |
| `sla_deadline` | DateTime | SLA response deadline |
| `first_response_at` | DateTime? | First agent response |
| `sla_breached` | Boolean | Whether SLA was breached |
| `converted_to_project` | Boolean | Whether lead converted to project |
| `converted_project_id` | UUID? | Reference to converted Project |
| `acquisition_cost` | Decimal? | Lead acquisition cost (if purchased) |
| `created_at` | DateTime | Lead creation |
| `assigned_at` | DateTime | Agent assignment |
| `resolved_at` | DateTime? | Lead resolution |

#### 11.1.1 CRM Pipeline (8 stages)

```
incoming_message
    → normalize_text
        → extract_entities
            → detect_intent
                → context_enrichment
                    → lead_scoring
                        → lead_classification
                            → crm_routing
```

### 11.2 Lead Scoring Engine

#### 11.2.1 Base Scores by Lead Type

| Lead Type | Base Score | Description |
|-----------|-----------|-------------|
| tenant | 40 | Rental seeker |
| buyer | 60 | Property buyer |
| seller | 50 | Property seller |
| investor | 80 | Real estate investor |
| diaspora_investor | 95 | Diaspora investor (highest) |

#### 11.2.2 Score Boosters (13)

| Booster | Value | Condition |
|---------|-------|-----------|
| budget_detected | +15 | Budget range provided |
| city_detected | +10 | City specified |
| neighborhood_detected | +10 | Neighborhood specified |
| urgency_detected | +20 | Urgency keywords found |
| diaspora | +25 | Diaspora indicator |
| cash_purchase | +15 | Cash purchase stated |
| property_type_specified | +5 | Property type specified |
| timeline_specified | +10 | Timeline provided |
| multiple_criteria | +10 | 3+ criteria specified |
| professional | +15 | Professional profile |
| referral | +10 | Referred by existing user |
| complete_profile | +10 | Full contact info provided |
| verified_phone | +10 | Phone number verified |

#### 11.2.3 Score Penalties (8)

| Penalty | Value | Condition |
|---------|-------|-----------|
| missing_budget | -10 | No budget information |
| unclear_location | -10 | No location specified |
| spam_like | -50 | Spam patterns detected |
| too_short | -20 | Message < 10 characters |
| external_links | -30 | Contains external URLs |
| duplicate_message | -20 | Same message sent repeatedly |
| aggressive_language | -30 | Aggressive or abusive language |
| impossible_request | -40 | Request contradicts reality |

### 11.3 Lead Classification Thresholds

| Classification | Score Range | Action |
|---------------|-------------|--------|
| HOT | 80-100+ | Route immediately (P0: < 30min) |
| WARM | 60-79 | Route within 2h (P1) |
| COLD | 40-59 | Route within 24h (P2) |
| LOW | 20-39 | Route within 7d (P3) |
| SPAM | < 20 | Block/quarantine |

### 11.4 CRM Routing

| Method | Description |
|--------|-------------|
| Zone-based | Route to agent assigned to lead's geographic zone |
| Availability-based | Route to least-loaded agent in zone |
| Score-based | Route to highest-rated agent in zone |
| Manual | Admin/manager manually assigns |

### 11.5 Anti-Fraud Layers (4)

| Layer | Detection | Action |
|-------|-----------|--------|
| 1. Broker spam | Same phone/email submitting > 5 leads in 1h | Flag, rate-limit |
| 2. Duplicate listing | Same property details from multiple accounts | Flag, merge investigation |
| 3. Fake price | Price deviates > 300% from market avg | Flag, require verification |
| 4. Suspicious urgency | Aggressive language + no details + external links | Flag, temporary suspension |

### 11.6 Behavior Tracking (8 behaviors)

| Behavior | Tracking |
|----------|----------|
| message_history | All messages, timestamps, channels |
| response_time | Time to first agent response |
| response_rate | Percentage of messages responded to |
| budget_changes | Budget modifications over time |
| visit_requests | Number of visit requests |
| visit_completion | Percentage of visits completed |
| negotiation_history | Offer patterns |
| complaint_history | Number and type of complaints |

### 11.7 SLA by Priority

| Priority | Target Response | Classification |
|----------|----------------|---------------|
| P0 | < 30 minutes | HOT |
| P1 | < 2 hours | WARM |
| P2 | < 24 hours | COLD |
| P3 | J+1 to J+7 | LOW |

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| User (lead) | 0:1 | Existing user if identified |
| User (agent) | N:1 | Assigned agent |
| Project | 0:1 | Converted project |
| Organization | N:1 | Target organization |
| LeadPurchase | 0:1 | If lead was purchased |

---

## 12. Domain 11: Identity Model

**Status:** ENRICH_CURRENT

### 12.1 Entity: User (Identity)

| Aspect | Detail |
|--------|--------|
| **Status** | ENRICH_CURRENT |
| **Gold Source** | Identity resolution with duplicate detection, merge algorithm, phone normalization, trust score calculation, GDPR deletion workflow |
| **Current V2** | Basic User model with email, phone, name; no duplicate detection or merge capability |
| **Unified Target** | Keep current User entity. Enrich with identity resolution service (duplicate detection via phone/email/name matching), merge algorithm, phone normalization (international format), trust score calculation, GDPR-compliant deletion workflow. |

#### Enriched Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `id` | UUID | V2 | Primary identifier |
| All existing V2 fields | — | V2 | Retained |
| `phone_normalized` | String | **ENRICH** | E.164 normalized phone |
| `phone_country_code` | String | **ENRICH** | Country code (e.g., +237) |
| `identity_confidence` | Float | **ENRICH** | Identity resolution confidence score |
| `merged_into_id` | UUID? | **ENRICH** | If merged, points to surviving account |
| `merge_history` | JSON[] | **ENRICH** | Array of merge records |
| `gdpr_deletion_requested_at` | DateTime? | **ENRICH** | When GDPR deletion was requested |
| `gdpr_deletion_completed_at` | DateTime? | **ENRICH** | When deletion was completed |
| `gdpr_deletion_status` | Enum | **ENRICH** | `none \| requested \| processing \| completed` |
| `anonymized_at` | DateTime? | **ENRICH** | When data was anonymized |
| `trust_score` | Float | **ENRICH** | Computed trust score (0-100) |
| `trust_score_factors` | JSON | **ENRICH** | Contributing factors |

### 12.2 Identity Resolution Service

#### 12.2.1 Duplicate Detection Signals

| Signal | Weight | Description |
|--------|--------|-------------|
| Phone match | 0.40 | Same normalized phone |
| Email match | 0.35 | Same email address |
| Name similarity | 0.15 | Fuzzy name matching |
| Device fingerprint | 0.10 | Same device ID |

#### 12.2.2 Merge Algorithm

```
1. Detect potential matches (score > 0.70)
2. Flag for human review (score 0.70-0.90)
3. Auto-merge (score > 0.90 with phone match)
4. On merge:
   a. Choose survivor (most recent active account)
   b. Merge properties, projects, conversations
   c. Link merged_into_id on consumed account
   d. Preserve audit trail on both accounts
```

#### 12.2.3 GDPR Deletion Workflow

```
Request Received → Identity Verification → Data Anonymization
    → Account Deactivation → Data Deletion (except legal holds)
    → Confirmation to User → Completion Record
```

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| User (merged) | 1:1 | Self-referential merge link |
| IdentityLog | 1:N | Identity resolution audit trail |

---

## 13. Domain 12: Organization Model

**Status:** ENRICH_CURRENT

### 13.1 Entity: Organization

| Aspect | Detail |
|--------|--------|
| **Status** | ENRICH_CURRENT |
| **Gold Source** | Agency-specific fields (RCCM, tax ID, verification), agent zone routing, minimum agent requirements, organization lifecycle |
| **Current V2** | Organization model with basic fields, user membership |
| **Unified Target** | Keep current Organization entity. Enrich with agency-specific registration fields, agent zone assignment, minimum agent validation rules, organization lifecycle states. |

#### Enriched Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `id` | UUID | V2 | Primary identifier |
| `name` | String | V2 | Organization name |
| All existing V2 fields | — | V2 | Retained |
| `rccm` | String | **ENRICH** | Trade register number (Registre du Commerce et du Crédit Mobilier) |
| `tax_id` | String | **ENRICH** | Tax identification number |
| `cni_document_id` | UUID? | **ENRICH** | CNI/passport document reference |
| `registration_document_id` | UUID? | **ENRICH** | Business registration document |
| `lifecycle_state` | Enum | **ENRICH** | `creation \| validation \| active \| suspended \| dissolution \| archived` |
| `verification_status` | Enum | **ENRICH** | `unverified \| pending \| verified \| rejected` |
| `verified_at` | DateTime? | **ENRICH** | Verification completion |
| `trust_level` | Int (1-6) | **ENRICH** | Agency-level trust level |
| `agency_verified` | Boolean | **ENRICH** | Agency verification badge |
| `min_agents_required` | Int | **ENRICH** | Minimum agents for operational status (default 3) |
| `is_operational` | Boolean | **ENRICH** | Meets minimum agent requirement |
| `agent_count` | Int | **ENRICH** | Current active agent count |
| `zones` | JSON[] | **ENRICH** | Geographic zones served |
| `lead_capacity` | Int | **ENRICH** | Maximum concurrent leads |
| `lead_count` | Int | **ENRICH** | Current active lead count |

#### 13.1.1 Organization Lifecycle

```
Creation → Validation → Active → Suspension → Dissolution → Archived
```

| State | Description |
|-------|-------------|
| Creation | Agency registration initiated; basic info collected |
| Validation | Documents under review by LAWIM admin |
| Active | Fully verified and operational |
| Suspended | Temporarily suspended (compliance, fraud investigation) |
| Dissolution | Agency closing process |
| Archived | Agency closed, data preserved |

### 13.2 Entity: OrganizationMember (extended)

| Aspect | Detail |
|--------|--------|
| **Status** | ENRICH_CURRENT |
| **Gold Source** | Agency hierarchy roles, zone assignment |
| **Current V2** | Basic user-organization membership |
| **Unified Target** | Extend membership with agency role, zone assignment, credit limit. |

#### Enriched Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `user_id` | UUID | V2 | Member user |
| `organization_id` | UUID | V2 | Organization |
| `agency_role` | Enum | **ENRICH** | `responsible \| admin \| agent \| assistant` |
| `zones` | String[] | **ENRICH** | Assigned geographic zones |
| `max_leads` | Int | **ENRICH** | Per-agent lead limit |
| `current_leads` | Int | **ENRICH** | Current active leads |
| `joined_at` | DateTime | V2 | Membership start |
| `left_at` | DateTime? | V2+ | Membership end |

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| User | 1:N | Organization members |
| OrganizationMember | N:M | User membership with role |
| Lead (zone) | 1:N | Leads routed by zone |

---

## 14. Domain 13: Permission/Security Model

**Status:** ENRICH_CURRENT

### 14.1 Permission Model

| Aspect | Detail |
|--------|--------|
| **Status** | ENRICH_CURRENT |
| **Gold Source** | 4 explicit permission levels (Read, Create, Edit, Approve), permission matrix per role, approval workflows, permission scope (own/managed/org/all) |
| **Current V2** | Implicit permissions via role checks (isAdmin, isOperator), no formal permission model, no approval workflow |
| **Unified Target** | Keep current role-based approach as foundation. Add explicit 4-level permission matrix mapped to official roles. Implement approval workflow model. Add permission scope awareness (own vs. managed vs. org vs. all). |

### 14.2 Permission Levels (4)

| Level | Code | Description |
|-------|------|-------------|
| Read | R | View/can access the resource |
| Create | C | Create new instances of the resource |
| Edit | E | Modify existing instances |
| Approve | A | Approve/reject actions on the resource |

### 14.3 Permission Matrix (Role × Resource)

| Resource \ Role | admin | manager | operator | partner | user |
|-----------------|-------|---------|----------|---------|------|
| Property (own) | RCEA | RCEA | RCEA | RCE | RCE |
| Property (org) | RCEA | RCEA | RCEA | R | — |
| Property (all) | RCEA | R | — | — | — |
| Project (own) | RCEA | RCEA | RCEA | RCEA | RCEA |
| Project (org) | RCEA | RCEA | RCEA | R | — |
| Transaction | RCEA | RCEA | RCE | R | — |
| User (org) | RCEA | RCEA | R | R | — |
| Organization | RCEA | RCE | — | — | — |
| Service | RCEA | RCEA | RCEA | RCE | R |
| Payment | RCEA | RCEA | R | — | — |
| Lead | RCEA | RCEA | RCE | RCE | — |
| Document | RCEA | RCE | RCE | RCE | RCE |
| CRM settings | RCEA | RA | — | — | — |
| System config | A | — | — | — | — |

### 14.4 Entity: ApprovalWorkflow

| Aspect | Detail |
|--------|--------|
| **Status** | ENRICH_CURRENT |
| **Gold Source** | Approval workflow for agency creation, listing validation, professional verification |
| **Current V2** | No approval workflow |
| **Unified Target** | Create generic ApprovalWorkflow model for actions requiring approval. |

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `approval_type` | Enum | `agency_creation \| listing_validation \| professional_verification \| organization_validation \| refund_approval \| account_suspension` |
| `target_type` | String | Entity type being approved |
| `target_id` | UUID | Entity ID being approved |
| `requested_by` | UUID | User requesting approval |
| `assigned_to` | UUID | Approver user |
| `status` | Enum | `pending \| approved \| rejected \| cancelled` |
| `reviewed_by` | UUID? | Reviewer who acted |
| `reviewed_at` | DateTime? | Review timestamp |
| `approval_notes` | Text? | Approver notes |
| `rejection_reason` | String? | Reason if rejected |
| `escalated_to` | UUID? | Escalated approver |
| `created_at` | DateTime | Creation timestamp |

### 14.5 Consent Management

| Concept | Description |
|---------|-------------|
| Agent opt-in | Agent must consent to receive routed leads |
| Data sharing | User must consent to data sharing for matching |
| Double consent | Both parties must consent before contact (see Dossier model) |
| GDPR consent | Explicit consent for data processing |
| Marketing opt-in | Separate consent for marketing communications |

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| ApprovalWorkflow | N:1 (by target) | Links to entity being approved |
| User (approver) | N:1 | User with Approve permission |
| Permission matrix | — | Configurable lookup table |

---

## 15. Domain 14: Document Model

**Status:** EXTEND_CURRENT

### 15.1 Entity: Document

| Aspect | Detail |
|--------|--------|
| **Status** | EXTEND_CURRENT |
| **Gold Source** | Document types per transaction, verification workflow, mandatory documents per transaction type |
| **Current V2** | Media entity handles file uploads; no specific Document entity with type, verification, or lifecycle |
| **Unified Target** | Create Document entity as a typed, verifiable document with lifecycle. Support per-transaction-type document requirements. Implement verification workflow (upload → validate → approve → reject). |

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `document_type` | Enum | `land_title \| national_id \| passport \| power_of_attorney \| tax_clearance \| lease_contract \| deposit_receipt \| inventory \| company_registration \| tax_id \| professional_cert \| property_title \| survey_plan \| building_permit \| other` |
| `file_url` | String | Storage URL |
| `file_name` | String | Original filename |
| `file_size` | Int | File size in bytes |
| `mime_type` | String | MIME type |
| `uploaded_by` | UUID | User who uploaded |
| `verification_status` | Enum | `pending \| validated \| rejected` |
| `validated_by` | UUID? | Verifier user |
| `validated_at` | DateTime? | Verification timestamp |
| `rejection_reason` | String? | Reason if rejected |
| `is_mandatory` | Boolean | Whether document is mandatory for transaction type |
| `expires_at` | DateTime? | Document expiration (e.g., ID card) |
| `reference_entity_type` | String | Entity this document belongs to |
| `reference_entity_id` | UUID | Entity ID (Property, Transaction, User) |
| `created_at` | DateTime | Upload timestamp |

#### 15.1.1 Document Verification Workflow

```
Upload → Pending → Validated (by admin/operator)
                → Rejected (with reason)
```

#### 15.1.2 Mandatory Documents Per Transaction Type

| Transaction Type | Mandatory Documents |
|-----------------|-------------------|
| Sale | land_title, seller_id, buyer_id |
| Rental | lease_contract, deposit_receipt, inventory |
| Commercial Lease | commercial_lease, company_registration, tax_id |
| Agent Verification | national_id, professional_cert |
| Organization Validation | company_registration, tax_id, national_id (for responsible) |

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| User | N:1 | Uploader/owner |
| Transaction | N:1 | Transaction documents |
| Property | N:1 | Property documents |
| Organization | N:1 | Organization documents |

---

## 16. Domain 15: Events/Observability

**Status:** ENRICH_CURRENT

### 16.1 Entity: Event

| Aspect | Detail |
|--------|--------|
| **Status** | ENRICH_CURRENT |
| **Gold Source** | 12+ typed audit events per workflow, state transition audit trail |
| **Current V2** | Generic Event model with `kind` (string) and `payload` (JSON) |
| **Unified Target** | Keep current Event entity as generic base. Enrich with typed event catalog, formal state transition audit events, domain-specific event types with structured payloads. |

#### Enriched Attributes

| Attribute | Type | Source | Description |
|-----------|------|--------|-------------|
| `id` | UUID | V2 | Primary identifier |
| `kind` | String | V2 | Event type (now typed from catalog below) |
| `payload` | JSON | V2 | Event payload |
| `entity_type` | String | **ENRICH** | Type of entity that generated the event |
| `entity_id` | UUID | **ENRICH** | Entity ID |
| `actor_id` | UUID? | **ENRICH** | User who triggered the event |
| `previous_state` | String? | **ENRICH** | Previous state (for state transitions) |
| `new_state` | String? | **ENRICH** | New state (for state transitions) |
| `transition` | String? | **ENRICH** | Transition name (e.g., "publish", "validate") |
| `source` | String | **ENRICH** | Event source (system, user, webhook, cron) |
| `correlation_id` | UUID? | **ENRICH** | Correlation ID for event chains |
| `severity` | Enum | **ENRICH** | `debug \| info \| warning \| error \| critical` |
| `created_at` | DateTime | V2 | Event timestamp |

### 16.2 Typed Event Catalog (13+ categories)

| Category | Event Kinds | Description |
|----------|-------------|-------------|
| **User Events** | `user.created`, `user.updated`, `user.deleted`, `user.login`, `user.logout`, `user.verified`, `user.merged`, `user.gdpr_deletion_requested` | User lifecycle events |
| **Role/Trust Events** | `user.trust_level_changed`, `user.badge_awarded`, `user.role_changed`, `user.agency_role_changed` | Role and trust events |
| **Property Events** | `property.created`, `property.updated`, `property.published`, `property.archived`, `property.verified`, `property.boosted`, `property.status_changed` | Property lifecycle |
| **Project/Dossier Events** | `project.created`, `project.matching_started`, `project.match_found`, `project.double_consent_updated`, `project.rematched`, `project.qualification_step_completed` | Project lifecycle |
| **Matching Events** | `match.created`, `match.score_calculated`, `match.proposed`, `match.accepted`, `match.rejected`, `match.expired`, `match.rematched` | Matching engine events |
| **Visit Events** | `visit.requested`, `visit.confirmed`, `visit.rescheduled`, `visit.cancelled`, `visit.completed`, `visit.absence_reported`, `visit.satisfaction_recorded` | Visit workflow |
| **Negotiation Events** | `negotiation.started`, `negotiation.offer_made`, `negotiation.counter_offer`, `negotiation.accepted`, `negotiation.rejected`, `negotiation.silence_reminder`, `negotiation.failed` | Negotiation events |
| **Transaction Events** | `transaction.created`, `transaction.documents_submitted`, `transaction.payment_milestone`, `transaction.signed`, `transaction.completed`, `transaction.failed` | Transaction lifecycle |
| **Payment Events** | `payment.created`, `payment.initiated`, `payment.confirmed`, `payment.failed`, `payment.refunded`, `payment.disputed` | Payment processing |
| **CRM Events** | `lead.created`, `lead.scored`, `lead.classified`, `lead.routed`, `lead.converted`, `lead.fraud_flagged`, `lead.sla_breached` | CRM pipeline |
| **Organization Events** | `org.created`, `org.validated`, `org.member_added`, `org.member_removed`, `org.suspended`, `org.dissolved` | Organization lifecycle |
| **Approval Events** | `approval.requested`, `approval.approved`, `approval.rejected`, `approval.escalated` | Approval workflow |
| **System Events** | `system.sla_breach_detected`, `system.nba_recalculated`, `system.cron_executed`, `system.error`, `system.warning` | System observability |

### 16.3 Audit Trail

All state transitions MUST generate an audit event with:

- `entity_type` + `entity_id` (identifies the entity)
- `previous_state` (state before transition)
- `new_state` (state after transition)
- `transition` (name of the transition)
- `actor_id` (who performed it)
- `created_at` (when it happened)

#### Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Any entity | N:1 | Events reference any entity by type + ID |
| User (actor) | N:1 | User who triggered event |

---

## 17. Entity Relationship Summary

```
User (identity)
  ├─ Organization (via OrganizationMember with agency_role)
  ├─ Project (as creator/owner)
  │    ├─ Intent (source detection)
  │    ├─ Property (N:M via Match)
  │    ├─ Match (score and proposal)
  │    ├─ Visit (scheduled visits)
  │    ├─ Negotiation (offer exchange)
  │    └─ Transaction (deal closing)
  ├─ Property (as owner or agent)
  │    ├─ Media (photos/videos)
  │    ├─ Document (title, permits)
  │    ├─ Visit (property visits)
  │    └─ Transaction (property sale/rental)
  ├─ Lead (as source or assigned agent)
  │    └─ LeadPurchase (if purchased)
  ├─ ServiceOrder (as buyer)
  │    └─ Payment (payment processing)
  ├─ AgentCredit (credit balance)
  ├─ Document (uploaded documents)
  └─ Event (audit trail)

Organization
  └─ OrganizationMember (users with agency_role)

Project
  ├─ Intent → Intent detection pipeline
  ├─ Match (scores for N properties)
  ├─ Visit (scheduled visits)
  ├─ Conversation → Negotiation
  └─ Transaction (deal closing)

Property
  ├─ Match (scores for N projects)
  ├─ Visit (scheduled visits)
  └─ Transaction (deal closing)

Service
  └─ ServiceOrder → Payment

Lead
  └─ CRM Pipeline → Project conversion
```

### 17.1 Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Project vs Dossier | Keep "Project" name | Avoid breaking API surface; add dossier semantics as enriched fields |
| Transaction as separate entity | Yes | Distinct lifecycle, document requirements, and party structure from Project |
| Roles: hierarchy vs flat | Flat (V2) + enrichment | Gold hierarchy mapped via lookup table, not inheritance |
| Property types: enum vs free | Enum + metadata fallback | Validation for core types, flexibility for edge cases |
| State machine approach | Hybrid (Gold states + V2 mapping) | Full Gold states internally, simplified V2 map for API consumers |
| Data model philosophy | Hybrid (typed + JSON) | Core fields typed, per-family fields in documented metadata_json |
| Service model | Full Gold catalog | 72 services with fixed pricing, Campay integration |
| Permission model | Explicit matrix | 4 levels × roles with scope awareness |

---

## 18. Legacy Compatibility Layer

To ensure backward compatibility during H2 transition:

### 18.1 State Mapping

| V2 Status | Unified State(s) |
|-----------|------------------|
| property: draft | creation / normalization / classification |
| property: open | validation / published / matching |
| property: closed | archived |
| property: published | published |
| property: archived | archived |
| project: draft | creation / qualification |
| project: active | matching / presentation / wait_demandeur / wait_holder / mise_en_relation |
| project: paused | paused (retained) |
| project: completed | closure |
| project: archived | archive |

### 18.2 Role Mapping

| Gold Level | V2 Role |
|------------|---------|
| L1 (demandeur) | user |
| L2 (visiteur) | user |
| L3 (membre) | user |
| L4 (agent) | partner (or operator if agency) |
| L5 (professionnel) | partner |
| L6 (expert) | operator / manager |
| L7 (master) | admin |

### 18.3 Property Type Migration

```
Free-form string → validated enum with fallback:
  - If value matches known PROPERTY_TYPE → use validated type
  - If value is unknown → map to 'other' with original value preserved in metadata_json
  - Family is inferred from type where possible, else 'other'
```

### 18.4 API Compatibility

- All existing API endpoints preserved during transition
- New fields return `null`/empty until data is migrated
- State field returns simplified V2-compatible value in API; full state available via extended endpoint (e.g., `GET /properties/:id/state`)
- New entities (Service, Transaction, Visit, Lead, Match, Document) behind feature flags

---

*End of LAWIM_UNIFIED_DOMAIN_MODEL.md — 15 domains defined, 18 new/enriched entities specified, legacy compatibility mapped.*
