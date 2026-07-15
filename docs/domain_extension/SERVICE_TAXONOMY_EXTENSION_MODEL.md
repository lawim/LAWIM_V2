# SERVICE TAXONOMY EXTENSION MODEL

**Document ID:** LAWIM-H13-SERVICE-TAXONOMY-V1
**Status:** CANONICAL — Extension target for H2 implementation
**Date:** 2026-07-15
**Source Documents:** `SERVICE_CROSSWALK.md`, `required_extensions.json` (§monetized_services, §real_estate_services, §professional_services, §crm_monetized_services, §service_lifecycle), `LAWIM_UNIFIED_DOMAIN_MODEL.md` (§4)

---

## Table of Contents

1. [Service Taxonomy Overview](#1-service-taxonomy-overview)
2. [Service Model](#2-service-model)
3. [Complete Service Catalog (72 Services)](#3-complete-service-catalog-72-services)
4. [ServiceOrder Entity — 8-State Lifecycle](#4-serviceorder-entity--8-state-lifecycle)
5. [Payment Entity — 10-State Sub-Machine](#5-payment-entity--10-state-sub-machine)
6. [AgentCredit Entity](#6-agentcredit-entity)
7. [LeadPurchase Entity](#7-leadpurchase-entity)
8. [Full Pricing Tables for Monetized Services](#8-full-pricing-tables-for-monetized-services)
9. [CRM Lead Services (Bronze, Silver, Gold Packs)](#9-crm-lead-services-bronze-silver-gold-packs)
10. [Diaspora Service Tiers](#10-diaspora-service-tiers)
11. [Complete Extension Mapping Table](#11-complete-extension-mapping-table)

---

## 1. Service Taxonomy Overview

The LAWIM service taxonomy is organized into 11 service families that span the full real estate ecosystem. Each service belongs to exactly one family and carries classification attributes that determine provider requirements, pricing model, and fulfillment workflow.

### 1.1 Service Families (11)

| # | Family | Code | Description | Service Count |
|---|--------|------|-------------|---------------|
| 1 | Immobilier | `immobilier` | Core real estate services: valuation, visits, listings, transactions | 12 |
| 2 | Juridique | `juridique` | Legal services: notary, legal advice, transaction accompaniment | 4 |
| 3 | Technique | `technique` | Skilled trades: masonry, carpentry, painting, tiling, roofing, plumbing, electrical | 9 |
| 4 | Financier | `financier` | Financial services: tax advice, insurance, valuation, financing | 5 |
| 5 | Documentaire | `documentaire` | Document services: verification, document control, title checks | 3 |
| 6 | Commercial | `commercial` | Marketing & media: photography, videography, drone, staging, publication | 7 |
| 7 | Gestion | `gestion` | Management services: rental management, condo management, syndicate | 5 |
| 8 | Construction | `construction` | Construction and development services | 2 |
| 9 | Renovation | `renovation` | Renovation, maintenance, and cleaning services | 4 |
| 10 | Securite | `securite` | Security and surveillance services | 2 |
| 11 | Mobilite | `mobilite` | Mobility and relocation services | 1 |

### 1.2 Taxonomy Dimensions

Each service is classified across these dimensions:

| Dimension | Values | Description |
|-----------|--------|-------------|
| **service_family** | 11 families from §1.1 | Primary classification |
| **category** | `monetized \| real_estate \| professional \| crm` | Economic category (4 types) |
| **provider_type** | `agent \| partner \| platform \| professional` | Who provides the service |
| **pricing_model** | `fixed \| recurring \| per_use \| tiered \| free` | How the service is priced |
| **fulfillment_type** | `automatic \| manual \| hybrid` | How the service is fulfilled |
| **geographic_scope** | `local \| regional \| national \| diaspora` | Geographic availability |
| **requires_verification** | Boolean | Whether provider verification is required |
| **is_monetized** | Boolean | Whether the service generates platform revenue |

---

## 2. Service Model

### 2.1 Entity: Service

The `Service` entity defines a monetized catalog item with fixed price, type classification, and lifecycle state.

#### Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `code` | String | Unique service code (e.g., `boost_7j`, `lead_bronze`) |
| `name` | String | Display name |
| `description` | Text | Service description |
| `service_family` | Enum | Taxonomy family from §1.1 |
| `category` | Enum | `monetized \| real_estate \| professional \| crm` |
| `price_fcfa` | Int | Fixed price in FCFA |
| `currency` | String | Currency (default: XAF) |
| `is_active` | Boolean | Whether service is currently offered |
| `duration_days` | Int | Service duration (for time-based services) |
| `provider_categories` | String[] | Required provider professional categories |
| `requester_categories` | String[] | Eligible requester categories |
| `qualification_matrix_id` | UUID? | Optional qualification matrix for this service |
| `required_documents` | String[] | Documents required to fulfill this service |
| `required_verifications` | String[] | Verifications required before fulfillment |
| `pricing_model` | Enum | `fixed \| recurring \| per_use \| tiered \| free` |
| `geographic_scope` | Enum | `local \| regional \| national \| diaspora` |
| `sla_hours` | Int? | Service level agreement in hours |
| `workflow_id` | UUID? | Associated fulfillment workflow |
| `consent_requirements` | JSON[] | Required consents before service activation |
| `matching_requirements` | JSON[] | Matching criteria for provider assignment |
| `lifecycle_state` | Enum | `creation \| proposition \| acceptation \| paiement \| activation \| utilisation \| expiration \| archivage` |

### 2.2 Service Lifecycle (8 states)

```
creation
  → proposition
    → acceptation
      → paiement
        → activation
          → utilisation
            → expiration
              → archivage
```

| State | Description | Entry Condition |
|-------|-------------|-----------------|
| `creation` | Service record created in catalog | Admin creates service definition |
| `proposition` | Service proposed to customer | Customer initiates order |
| `acceptation` | Customer accepts terms | Customer confirms order |
| `paiement` | Payment processed | Customer completes payment |
| `activation` | Service becomes active | Payment confirmed |
| `utilisation` | Service is being delivered | Service delivery in progress |
| `expiration` | Service period ends | Duration expires or delivery completes |
| `archivage` | Service record archived | Final state |

---

## 3. Complete Service Catalog (72 Services)

### 3.1 Monetized Services (13)

| # | Code | Name | Price (FCFA) | Service Family |
|---|------|------|-------------|----------------|
| 1 | `boost_7j` | Boost visibilité 7 jours | 2,000 | Immobilier |
| 2 | `boost_30j` | Boost visibilité 30 jours | 5,000 | Immobilier |
| 3 | `premium_listing` | Annonce premium | 10,000 | Immobilier |
| 4 | `agent_pro` | Abonnement agent professionnel | 10,000/mois | Immobilier |
| 5 | `accompagnement_visite` | Accompagnement de visite | 50,000 | Immobilier |
| 6 | `accompagnement_transaction` | Accompagnement de transaction | 50,000 | Juridique |
| 7 | `controle_documentaire` | Contrôle documentaire | 5,000 | Documentaire |
| 8 | `photographie_pro` | Photographie professionnelle | 15,000 | Commercial |
| 9 | `video_pro` | Vidéo professionnelle | 25,000 | Commercial |
| 10 | `verification_bien` | Vérification de bien | 10,000 | Documentaire |
| 11 | `mise_en_relation` | Mise en relation payante | 500 | Immobilier |
| 12 | `assistance_personnalisee` | Assistance personnalisée | 50,000 | Immobilier |
| 13 | `visibilite_premium` | Visibilité premium | 7,500 | Immobilier |

### 3.2 CRM Lead Services (9)

| # | Code | Name | Price (FCFA) | Service Family |
|---|------|------|-------------|----------------|
| 14 | `lead_bronze` | Lead Bronze (1 contact) | 500 | Commercial |
| 15 | `lead_silver` | Lead Silver (5 contacts) | 1,500 | Commercial |
| 16 | `lead_gold` | Lead Gold (15 contacts) | 3,000 | Commercial |
| 17 | `deblocage_coordonnees` | Déblocage coordonnées propriétaire | 500 | Immobilier |
| 18 | `demandeur_premium` | Demandeur Premium | 1,000 | Immobilier |
| 19 | `diaspora_simple` | Diaspora Simple | 25,000 | Immobilier |
| 20 | `diaspora_rapport` | Diaspora Rapport | 50,000 | Immobilier |
| 21 | `diaspora_complet` | Diaspora Complet | 75,000 | Immobilier |
| 22 | `agent_business` | Abonnement Agent Business | 25,000/mois | Gestion |

### 3.3 Real Estate Services (24)

| # | Code | Name | Price (FCFA) | Service Family |
|---|------|------|-------------|----------------|
| 23 | `estimation_immobiliere` | Estimation immobilière | 15,000 | Financier |
| 24 | `expertise_immobiliere` | Expertise immobilière | 25,000 | Immobilier |
| 25 | `verification_documentaire` | Vérification documentaire | 10,000 | Documentaire |
| 26 | `visite_property` | Visite de propriété | 5,000 | Immobilier |
| 27 | `contre_visite` | Contre-visite | 5,000 | Immobilier |
| 28 | `gestion_locative` | Gestion locative | 10,000/mois | Gestion |
| 29 | `mise_en_location` | Mise en location | 20,000 | Immobilier |
| 30 | `mise_en_vente` | Mise en vente | 25,000 | Immobilier |
| 31 | `publication_service` | Service de publication | 5,000 | Commercial |
| 32 | `photographie_immobiliere` | Photographie immobilière | 15,000 | Commercial |
| 33 | `video_immobiliere` | Vidéo immobilière | 25,000 | Commercial |
| 34 | `drone_service` | Service drone | 35,000 | Commercial |
| 35 | `home_staging` | Home staging | 30,000 | Commercial |
| 36 | `renovation_service` | Service rénovation | — | Renovation |
| 37 | `construction_service` | Service construction | — | Construction |
| 38 | `entretien_property` | Entretien de propriété | — | Renovation |
| 39 | `nettoyage_property` | Nettoyage de propriété | — | Renovation |
| 40 | `securisation_property` | Sécurisation de propriété | — | Securite |
| 41 | `demenagement` | Déménagement | — | Mobilite |
| 42 | `assurance_service` | Service d'assurance | — | Financier |
| 43 | `conseil_juridique_immobilier` | Conseil juridique immobilier | — | Juridique |
| 44 | `conseil_fiscal_immobilier` | Conseil fiscal immobilier | — | Financier |
| 45 | `gestion_copropriete` | Gestion de copropriété | — | Gestion |
| 46 | `recouvrement_locatif` | Recouvrement locatif | — | Gestion |

### 3.4 Professional Services (27)

| # | Code | Name | Service Family | In V2? | Extension Needed? |
|---|------|------|----------------|--------|-------------------|
| 47 | `agent_immobilier` | Agent immobilier | Immobilier | Yes | No |
| 48 | `notaire` | Notaire | Juridique | Yes | No |
| 49 | `geometre` | Géomètre | Immobilier | Yes | No |
| 50 | `expert_immobilier` | Expert immobilier | Immobilier | No | Yes |
| 51 | `evaluateur` | Évaluateur | Financier | No | Yes |
| 52 | `architecte` | Architecte | Construction | Yes | No |
| 53 | `courtier` | Courtier | Immobilier | No | Yes |
| 54 | `macon` | Maçon | Technique | No | Yes |
| 55 | `menuisier` | Menuisier | Technique | No | Yes |
| 56 | `peintre` | Peintre | Technique | No | Yes |
| 57 | `carreleur` | Carreleur | Technique | No | Yes |
| 58 | `couvreur` | Couvreur | Technique | No | Yes |
| 59 | `plombier` | Plombier | Technique | Yes | No |
| 60 | `electricien` | Électricien | Technique | Yes | No |
| 61 | `syndic` | Syndic | Gestion | No | Yes |
| 62 | `gardiennage_securite` | Gardiennage / Sécurité | Securite | No | Yes |
| 63 | `prestataire_administratif` | Prestataire administratif | Gestion | No | Yes |
| 64 | `videaste_drone` | Vidéaste / Drone | Commercial | No | Yes |
| 65 | `photographe` | Photographe | Commercial | Yes | No |
| 66 | `agent_nettoyage` | Agent de nettoyage | Renovation | Yes | No |
| 67 | `agent_entretien` | Agent d'entretien | Renovation | Yes | No |
| 68 | `demenageur` | Déménageur | Mobilite | Yes | No |
| 69 | `conseiller_juridique` | Conseiller juridique | Juridique | Yes | No |
| 70 | `conseiller_fiscal` | Conseiller fiscal | Financier | Yes | No |
| 71 | `assureur` | Assureur | Financier | Yes | No |
| 72 | `banque_institution` | Banque / Institution financière | Financier | Yes | No |
| 73 | `promoteur_immobilier` | Promoteur immobilier | Construction | Yes | No |

> **Note:** 15 of the 27 professional services already exist in V2 `business_profiles.py`. The 12 new additions (marked "Yes" under Extension Needed) require `business_profiles` updates. The 27 professional services correspond to the 27 professional search qualification matrices.

---

## 4. ServiceOrder Entity — 8-State Lifecycle

Represents a customer's purchase of a service. Tracks the order lifecycle from proposition through payment to activation and usage.

### 4.1 Key Attributes

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

### 4.2 8-State ServiceOrder Lifecycle

```
created → proposed → accepted → payment_pending → paid → activated → in_use → expired
                                                                          → archived
                                                                          → cancelled
```

| State | Description | Transitions To |
|-------|-------------|----------------|
| `created` | Order record created | `proposed` |
| `proposed` | Service proposed to buyer | `accepted`, `cancelled` |
| `accepted` | Buyer accepted terms | `payment_pending`, `cancelled` |
| `payment_pending` | Awaiting payment confirmation | `paid`, `cancelled` |
| `paid` | Payment received | `activated`, `cancelled` |
| `activated` | Service activated and available | `in_use`, `expired` |
| `in_use` | Service being delivered/consumed | `expired`, `archived` |
| `expired` | Service duration expired | `archived` |
| `archived` | Final archived state | — |
| `cancelled` | Order cancelled (any stage) | — |

### 4.3 Transition Rules

| From | To | Condition | Action |
|------|----|-----------|--------|
| `created` | `proposed` | Service selected and order initialized | Send proposal to buyer |
| `proposed` | `accepted` | Buyer explicitly accepts | Lock price, prepare payment |
| `proposed` | `cancelled` | Buyer declines or timeout | Release hold |
| `accepted` | `payment_pending` | Payment initiated | Initiate payment with provider |
| `accepted` | `cancelled` | Buyer cancels before payment | Release hold |
| `payment_pending` | `paid` | Payment provider confirms | Credit AgentCredit if applicable |
| `payment_pending` | `cancelled` | Payment fails or timeout | Notify buyer |
| `paid` | `activated` | Service activation conditions met | Set `activated_at` |
| `paid` | `cancelled` | Refund issued | Process refund |
| `activated` | `in_use` | Service delivery started | Track usage |
| `activated` | `expired` | Duration elapsed without usage | Auto-expire |
| `in_use` | `expired` | Service delivery completed | Set `expires_at` |
| `in_use` | `archived` | Manual archive | Set archive flag |
| `expired` | `archived` | Archival period reached | Final state |

---

## 5. Payment Entity — 10-State Sub-Machine

Tracks payment lifecycle for service orders. Integrates with Campay for mobile money processing.

### 5.1 Key Attributes

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

### 5.2 10-State Payment Sub-Machine

```
created → initiated → pending → confirmed → reconciled
                                → failed → (retry)
                                → cancelled
                                → expired
                                → disputed → refunded
confirmed → refunded
```

| State | Description | Transitions To |
|-------|-------------|----------------|
| `created` | Payment record created | `initiated` |
| `initiated` | Payment request sent to provider | `pending`, `failed` |
| `pending` | Awaiting provider callback | `confirmed`, `failed`, `cancelled`, `expired` |
| `confirmed` | Provider confirmed payment | `reconciled`, `disputed`, `refunded` |
| `failed` | Payment processing failed | `initiated` (retry) |
| `cancelled` | Payment cancelled by user/system | — |
| `expired` | Payment request expired (timeout) | — |
| `refunded` | Payment refunded | — |
| `reconciled` | Payment reconciled with ledger | — |
| `disputed` | Payment disputed by user | `refunded` |

### 5.3 Transition Rules

| From | To | Condition | Action |
|------|----|-----------|--------|
| `created` | `initiated` | API call to Campay initiated | Log `initiated_at` |
| `initiated` | `pending` | Waiting for USSD response | Set timeout (5 min) |
| `initiated` | `failed` | API error | Log `failure_reason` |
| `pending` | `confirmed` | Campay callback received | Log `confirmed_at`, trigger ServiceOrder.paid |
| `pending` | `failed` | Payment declined or error | Log `failure_reason`, `failed_at` |
| `pending` | `cancelled` | User cancels USSD | Log cancellation |
| `pending` | `expired` | Timeout (5 min) | Auto-expire |
| `confirmed` | `reconciled` | End-of-day reconciliation | Mark reconciled |
| `confirmed` | `disputed` | User files dispute | Log `dispute_reason`, `disputed_at` |
| `confirmed` | `refunded` | Admin-initiated refund | Process reversal, log `refunded_at` |
| `disputed` | `refunded` | Dispute resolved in favor of user | Process reversal |

---

## 6. AgentCredit Entity

Tracks agent credit balance and transactions. Credits are consumed for lead purchases and boost activations.

### 6.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `agent_id` | UUID | Reference to User (agent) |
| `balance` | Int | Current credit balance |
| `total_purchased` | Int | Lifetime credits purchased |
| `total_consumed` | Int | Lifetime credits consumed |
| `last_recharge_at` | DateTime | Last recharge timestamp |
| `last_recharge_amount` | Int | Last recharge amount |

### 6.2 Credit Operations

| Operation | Effect | Trigger |
|-----------|--------|---------|
| **Recharge** | `balance += amount`, `total_purchased += amount` | Agent purchases credits via payment |
| **Consume (lead)** | `balance -= cost`, `total_consumed += cost` | Agent purchases a lead |
| **Consume (boost)** | `balance -= cost`, `total_consumed += cost` | Agent activates a boost |
| **Refund** | `balance += amount` | Lead/boost cancelled and refunded |
| **Admin adjust** | `balance ±= amount` | Admin correction |

---

## 7. LeadPurchase Entity

Tracks when an agent purchases a lead (contact information for a demandeur or property owner).

### 7.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `agent_id` | UUID | Purchasing agent |
| `lead_id` | UUID | Reference to Lead |
| `service_order_id` | UUID | Reference to ServiceOrder |
| `credits_spent` | Int | Credits consumed |
| `purchased_at` | DateTime | Purchase timestamp |
| `contact_revealed` | Boolean | Whether contact was revealed |

### 7.2 Lead Purchase Flow

```
Agent selects lead → Credit balance checked → Sufficient? → Yes → Deduct credits
                                                              → No → Prompt recharge
→ Create LeadPurchase record → Reveal contact information → Log event
```

---

## 8. Full Pricing Tables for Monetized Services

### 8.1 Visibility & Boost Services

| Service | Code | Price (FCFA) | Duration | Discount vs Unit |
|---------|------|-------------|----------|------------------|
| Boost 7 jours | `boost_7j` | 2,000 | 7 days | 286/jour |
| Boost 30 jours | `boost_30j` | 5,000 | 30 days | 167/jour (42% vs 7j) |
| Annonce premium | `premium_listing` | 10,000 | Until sold/rented | — |
| Visibilité premium | `visibilite_premium` | 7,500 | 30 days | 250/jour |

### 8.2 Accompaniment Services

| Service | Code | Price (FCFA) | Includes |
|---------|------|-------------|----------|
| Accompagnement de visite | `accompagnement_visite` | 50,000 | Agent accompanies visit, transport, initial negotiation |
| Accompagnement de transaction | `accompagnement_transaction` | 50,000 | Full transaction support: offer→signature |
| Assistance personnalisée | `assistance_personnalisee` | 50,000 | Premium concierge: all of above + ongoing support |

### 8.3 Media Services

| Service | Code | Price (FCFA) | Deliverables |
|---------|------|-------------|--------------|
| Photographie professionnelle | `photographie_pro` | 15,000 | 10-15 edited photos |
| Vidéo professionnelle | `video_pro` | 25,000 | 2-3 min edited video |
| Service drone | `drone_service` | 35,000 | Aerial photos + video |

### 8.4 Verification & Document Services

| Service | Code | Price (FCFA) | Description |
|---------|------|-------------|-------------|
| Contrôle documentaire | `controle_documentaire` | 5,000 | Document compliance check |
| Vérification de bien | `verification_bien` | 10,000 | On-site property verification |

### 8.5 Agent Subscriptions

| Service | Code | Price (FCFA/mois) | Features |
|---------|------|-------------------|----------|
| Agent Professionnel | `agent_pro` | 10,000 | Professional listing tools, basic analytics |
| Agent Business | `agent_business` | 25,000 | All Pro features + priority leads, CRM access |

### 8.6 Pay-Per-Use

| Service | Code | Price (FCFA) | Description |
|---------|------|-------------|-------------|
| Mise en relation payante | `mise_en_relation` | 500 | Per-connection fee |

---

## 9. CRM Lead Services (Bronze, Silver, Gold Packs)

### 9.1 Lead Pack Comparison

| Feature | Lead Bronze | Lead Silver | Lead Gold |
|---------|-------------|-------------|-----------|
| **Price** | 500 FCFA | 1,500 FCFA | 3,000 FCFA |
| **Contacts** | 1 | 5 | 15 |
| **Cost per lead** | 500 FCFA | 300 FCFA | 200 FCFA |
| **Discount vs Bronze** | — | 40% | 60% |
| **Best for** | Single test purchase | Occasional leads | High-volume agents |

### 9.2 Lead Purchase Options

| Code | Name | Price (FCFA) | Description |
|------|------|-------------|-------------|
| `lead_bronze` | Lead Bronze | 500 | Single lead purchase |
| `lead_silver` | Lead Silver | 1,500 | 5-lead pack |
| `lead_gold` | Lead Gold | 3,000 | 15-lead pack |
| `deblocage_coordonnees` | Déblocage coordonnées | 500 | Unlock owner contact details |
| `demandeur_premium` | Demandeur Premium | 1,000 | Premium seeker profile |

### 9.3 Agent Business Subscription Features

| Feature | Agent Pro (10,000/mois) | Agent Business (25,000/mois) |
|---------|------------------------|-----------------------------|
| Property listing | Unlimited | Unlimited |
| Boost eligibility | Yes | Yes |
| Lead purchasing | Yes (pay per lead) | Yes (included allocation) |
| Lead allocation | — | 50 leads/month included |
| CRM dashboard | Basic | Full |
| Priority routing | — | Yes |
| Analytics | Basic | Advanced |
| API access | — | Yes |

---

## 10. Diaspora Service Tiers

### 10.1 Tier Comparison

| Feature | Diaspora Simple | Diaspora Rapport | Diaspora Complet |
|---------|----------------|------------------|------------------|
| **Price** | 25,000 FCFA | 50,000 FCFA | 75,000 FCFA |
| **Property search** | Self-service | Guided | Full concierge |
| **Property report** | — | Detailed report | Detailed report + comparison |
| **Visit arrangement** | — | Up to 3 visits | Up to 10 visits |
| **Video tour** | Pre-recorded | On-demand | Live + on-demand |
| **Negotiation support** | — | — | Full support |
| **Transaction accompaniment** | — | — | Included |
| **Legal support** | — | — | Included |
| **Document assistance** | — | — | Full assistance |
| **Duration** | 30 days | 60 days | 90 days |
| **Target segment** | Budget-conscious diaspora | Mid-range diaspora | Premium diaspora investors |

### 10.2 Diaspora Service Fulfillment

```
Diaspora user signs up → Selects tier → Payment →
  → Onboarding with dedicated diaspora agent →
  → Property matching (verified properties) →
  → Remote visits / video tours →
  → Negotiation (Complet only) →
  → Transaction support (Complet only)
```

### 10.3 Diaspora Premium Treatment

| Signal | Value |
|--------|-------|
| Lead score base | 95 (highest of all lead types) |
| Score booster | +25 diaspora indicator |
| SLA priority | P0 (< 30 min) |
| Agent requirement | Certified diaspora-specialist agent |

---

## 11. Complete Extension Mapping Table

All 60 service extensions from `required_extensions.json` mapped to proposed entities.

### 11.1 Monetized Service Extensions (13)

| Extension ID | Concept | Proposed Entity | Target Fields | Priority |
|-------------|---------|----------------|--------------|----------|
| EXT-SVC-MON-001 | Boost visibilité 7 jours | Property | `boost_level`, `boost_expires_at` | P1 |
| EXT-SVC-MON-002 | Boost visibilité 30 jours | Property | `boost_level`, `boost_expires_at` | P1 |
| EXT-SVC-MON-003 | Annonce premium | Property | `is_premium` | P1 |
| EXT-SVC-MON-004 | Abonnement agent professionnel | ServiceOrder | Subscription model → Organization/User | P1 |
| EXT-SVC-MON-005 | Accompagnement de visite | ServiceOrder | Type=`visit_accompaniment` | P2 |
| EXT-SVC-MON-006 | Accompagnement de transaction | ServiceOrder | Type=`transaction_accompaniment` | P2 |
| EXT-SVC-MON-007 | Contrôle documentaire | ServiceOrder | Document verification workflow | P4 |
| EXT-SVC-MON-008 | Photographie professionnelle | Media | Service order origin tracking | P4 |
| EXT-SVC-MON-009 | Vidéo professionnelle | Media | Service order origin tracking | P4 |
| EXT-SVC-MON-010 | Vérification de bien | Property | `verification_status`, `verified_at` | P2 |
| EXT-SVC-MON-011 | Mise en relation payante | LeadPurchase | Agent credit system + pay-per-connection | P1 |
| EXT-SVC-MON-012 | Assistance personnalisée | ServiceOrder | Premium assistance workflow | P4 |
| EXT-SVC-MON-013 | Visibilité premium | Service | Distinct from boost/premium listing | P3 |

### 11.2 Real Estate Service Extensions (24)

| Extension ID | Concept | Proposed Entity | Target Fields | Priority |
|-------------|---------|----------------|--------------|----------|
| EXT-SVC-RES-001 | Estimation immobilière | ServiceOrder | Estimation workflow with valuation matrix | P1 |
| EXT-SVC-RES-002 | Expertise | ServiceOrder | Inspection and expertise workflow | P2 |
| EXT-SVC-RES-003 | Vérification documentaire | ServiceOrder | Document verification workflow | P2 |
| EXT-SVC-RES-004 | Visite property | Visit | Visit scheduling state machine | P1 |
| EXT-SVC-RES-005 | Contre-visite | Visit | Extended visit with `contre_visite` type | P1 |
| EXT-SVC-RES-006 | Gestion locative | ServiceOrder | Recurring rental management workflow | P3 |
| EXT-SVC-RES-007 | Mise en location | ServiceOrder | Rental listing as a service | P1 |
| EXT-SVC-RES-008 | Mise en vente | ServiceOrder | Sales listing as a service | P1 |
| EXT-SVC-RES-009 | Publication service | ServiceOrder | Publication channel management | P1 |
| EXT-SVC-RES-010 | Photographie (real estate) | Media | Photography service order flow | P4 |
| EXT-SVC-RES-011 | Video service | Media | Videography service order flow | P4 |
| EXT-SVC-RES-012 | Drone service | Media | Drone sub-service of photography | P4 |
| EXT-SVC-RES-013 | Home staging | ServiceOrder | Staging workflow | P4 |
| EXT-SVC-RES-014 | Renovation service | ServiceOrder | Renovation scope management | P3 |
| EXT-SVC-RES-015 | Construction service | ServiceOrder | Construction project management | P3 |
| EXT-SVC-RES-016 | Entretien (maintenance) | ServiceOrder | Recurring maintenance service | P4 |
| EXT-SVC-RES-017 | Nettoyage (cleaning) | ServiceOrder | Professional cleaning service | P4 |
| EXT-SVC-RES-018 | Sécurisation (security) | ServiceOrder | Property security service | P4 |
| EXT-SVC-RES-019 | Déménagement (moving) | ServiceOrder | Moving/relocation service | P4 |
| EXT-SVC-RES-020 | Assurance service | ServiceOrder | Partner referral insurance service | P4 |
| EXT-SVC-RES-021 | Conseil juridique | ServiceOrder | Partner legal advisory service | P4 |
| EXT-SVC-RES-022 | Conseil fiscal | ServiceOrder | Partner tax advisory service | P4 |
| EXT-SVC-RES-023 | Gestion copropriété | ServiceOrder | Condominium management service | P4 |
| EXT-SVC-RES-024 | Recouvrement locatif | ServiceOrder | Rent recovery service | P4 |

### 11.3 Professional Service Extensions (12)

| Extension ID | Concept | Proposed Entity | Target Fields | Priority |
|-------------|---------|----------------|--------------|----------|
| EXT-SVC-PRO-001 | Maçon (Masonry) | User.business_profiles | Add `mason` to `business_profiles` | P3 |
| EXT-SVC-PRO-002 | Menuisier (Carpenter) | User.business_profiles | Add `carpenter` to `business_profiles` | P3 |
| EXT-SVC-PRO-003 | Peintre (Painter) | User.business_profiles | Add `painter` to `business_profiles` | P3 |
| EXT-SVC-PRO-004 | Carreleur (Tiler) | User.business_profiles | Add `tiler` to `business_profiles` | P3 |
| EXT-SVC-PRO-005 | Couvreur (Roofer) | User.business_profiles | Add `roofer` to `business_profiles` | P3 |
| EXT-SVC-PRO-006 | Expert immobilier | User.business_profiles | Add `real_estate_expert` | P3 |
| EXT-SVC-PRO-007 | Évaluateur (Appraiser) | User.business_profiles | Add `appraiser` | P4 |
| EXT-SVC-PRO-008 | Syndic (Condo manager) | User.business_profiles | Add `condo_manager` | P4 |
| EXT-SVC-PRO-009 | Vidéaste drone | User.business_profiles | Add `drone_videographer` | P4 |
| EXT-SVC-PRO-010 | Courtier (Broker) | User.business_profiles | Add `broker` | P4 |
| EXT-SVC-PRO-011 | Gardiennage (Security) | User.business_profiles | Add `security_guard` | P4 |
| EXT-SVC-PRO-012 | Prestataire administratif | User.business_profiles | Add `admin_service_provider` | P4 |

### 11.4 CRM Monetized Service Extensions (9)

| Extension ID | Concept | Proposed Entity | Target Fields | Priority |
|-------------|---------|----------------|--------------|----------|
| EXT-SVC-CRM-001 | Lead Bronze (1 contact, 500 FCFA) | LeadPurchase | LeadPurchase model with `lead_bronze` pack | P1 |
| EXT-SVC-CRM-002 | Lead Silver (5 contacts, 1,500 FCFA) | LeadPurchase | `lead_silver` pack with tiered pricing | P1 |
| EXT-SVC-CRM-003 | Lead Gold (15 contacts, 3,000 FCFA) | LeadPurchase | `lead_gold` pack with tiered pricing | P1 |
| EXT-SVC-CRM-004 | Déblocage coordonnées propriétaire | LeadPurchase | Coordinate unlock purchase type | P1 |
| EXT-SVC-CRM-005 | Demandeur Premium | User/ServiceOrder | Premium seeker profile features | P4 |
| EXT-SVC-CRM-006 | Diaspora Simple (25,000 FCFA) | ServiceOrder | Diaspora verified property access | P3 |
| EXT-SVC-CRM-007 | Diaspora Rapport (50,000 FCFA) | ServiceOrder | Diaspora accompaniment + reports | P3 |
| EXT-SVC-CRM-008 | Diaspora Complet (75,000 FCFA) | ServiceOrder | Diaspora full accompaniment | P3 |
| EXT-SVC-CRM-009 | Abonnement Agent Business | ServiceOrder | Premium agent subscription tier | P2 |

### 11.5 Service Lifecycle Extensions (2)

| Extension ID | Concept | Proposed Entity | Target Fields | Priority |
|-------------|---------|----------------|--------------|----------|
| EXT-SVC-LIFE-001 | Service lifecycle (8 states) | ServiceOrder | `status` enum with 8-state lifecycle | P1 |
| EXT-SVC-LIFE-002 | Payment sub-states (10 states) | Payment | `status` enum with 10-state sub-machine | P1 |

---

*End of SERVICE_TAXONOMY_EXTENSION_MODEL.md — 60 service extensions mapped, 72 services cataloged, 11 service families defined.*
