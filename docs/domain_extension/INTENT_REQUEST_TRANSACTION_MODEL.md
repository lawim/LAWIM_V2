# INTENT, REQUEST & TRANSACTION EXTENSION MODEL

**Document ID:** LAWIM-H13-INTENT-TRX-V1
**Status:** CANONICAL DOMAIN EXTENSION
**Date:** 2026-07-15
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §5 (Intent/Transaction Model), §8 (Negotiation Workflow), §9 (Transaction Workflow)
**Source Crosswalks:** INTENT_TRANSACTION_CROSSWALK.md, required_extensions.json (intent_detection, transaction_types)

---

## Table of Contents

1. [Conceptual Architecture](#1-conceptual-architecture)
2. [Entity: Intent](#2-entity-intent)
3. [Entity: ServiceRequest](#3-entity-servicerequest)
4. [Entity: Transaction](#4-entity-transaction)
5. [Intent Detection Pipeline](#5-intent-detection-pipeline)
6. [Multi-Intent Detection & Parallel Project Creation](#6-multi-intent-detection--parallel-project-creation)
7. [Urgency Detection](#7-urgency-detection)
8. [Entity Extraction Per Intent](#8-entity-extraction-per-intent)
9. [Intent-to-Role Mapping](#9-intent-to-role-mapping)
10. [Transaction Type Catalog](#10-transaction-type-catalog)
11. [Transaction 7-State Lifecycle](#11-transaction-7-state-lifecycle)
12. [Negotiation Workflow](#12-negotiation-workflow)
13. [Document Requirements Per Transaction Type](#13-document-requirements-per-transaction-type)
14. [Journey Stages & Business Actions](#14-journey-stages--business-actions)
15. [Complete Extension Mapping Table](#15-complete-extension-mapping-table)
16. [Extension Mapping: INT Extensions](#16-extension-mapping-int-extensions)
17. [Extension Mapping: TRX Extensions](#17-extension-mapping-trx-extensions)

---

## 1. Conceptual Architecture

The LAWIM_V2 extension model distinguishes six layered concepts that together describe the full lifecycle from user expression to deal closure:

### 1.1 Concept Hierarchy

```
INTENT (what the user wants to do)
  ↓ maps to
PROJECT_GOAL (the concrete objective the platform helps achieve)
  ↓ realized through
TRANSACTION_TYPE (the legal/financial instrument used)
  ↓ executed as
SERVICE_REQUEST (a specific ask to the platform or an agent)
  ↓ guided by
JOURNEY_STAGE (where the user is in the funnel)
  ↓ triggered by
BUSINESS_ACTION (a specific system operation)
```

### 1.2 Examples

| Concept | Example 1 | Example 2 | Example 3 |
|---------|-----------|-----------|-----------|
| **Intent** | `chercher un terrain` | `louer un appartement` | `trouver un notaire` |
| **Project Goal** | `construire une maison` | `se loger en centre-ville` | `authentifier un acte` |
| **Transaction Type** | `achat (buy)` | `location (rent)` | `service` |
| **Service Request** | `recherche de parcelle titrée` | `recherche T3 meublé` | `recherche notaire spécialisé` |
| **Business Action** | `lancer Search (matching)` | `lancer Search (matching)` | `lancer FindProfessional` |
| **Journey Stage** | `qualification` | `qualification` | `qualification` |

### 1.3 Layer Responsibilities

| Layer | Entity | Responsibility | Persistence |
|-------|--------|---------------|-------------|
| **Intent** | `Intent` | Raw detected user intention from NLP/keyword pipeline | Transient/logged |
| **Project Goal** | `Project.project_type` | User-facing objective the platform commits to helping with | Persistent on Project |
| **Transaction Type** | `Transaction.transaction_type` | Legal/financial framework for the deal | Persistent on Transaction |
| **Service Request** | `ServiceRequest` | A specific ask (search, quote, document) directed at the platform or an agent | Persistent |
| **Journey Stage** | `Project.journey_stage` | Current step in the progressive qualification/discovery funnel | Enum on Project |
| **Business Action** | (engine/service) | System operation triggered by state/event | Triggered |

---

## 2. Entity: Intent

Represents a raw detected user intention. Created by the intent detection pipeline from natural language input.

### 2.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `source_text` | Text | Original user utterance |
| `language` | Enum | `fr \| en \| pid` |
| `primary_intent` | Enum | `buy \| rent \| sell \| invest \| search_property \| find_professional \| service \| finance \| other` |
| `confidence` | Float | Detection confidence (0.0-1.0) |
| `threshold` | Float | Configurable threshold (default 0.70) |
| `is_multi_intent` | Boolean | Multiple intents detected |
| `sub_intents` | JSON[] | Array of {intent, confidence, entities} objects |
| `urgency_score` | Float | Detected urgency (0.0-1.0) |
| `urgency_level` | Enum | `low \| medium \| high \| urgent` |
| `extracted_entities` | JSON | Budget, location, property type, timeline, persons |
| `detection_method` | Enum | `keyword \| explicit_selection \| hybrid` |
| `keyword_scores` | JSON | Per-keyword contribution map |
| `project_type_mapping` | Enum | Mapped to `Project.project_type` |
| `detected_at` | DateTime | Detection timestamp |
| `session_id` | String | Chat session identifier |
| `source_channel` | Enum | `whatsapp \| telegram \| dashboard \| api` |

### 2.2 Intent Enum Definition

| Intent Code | Label (FR) | Label (EN) | Base Weight | Default Project Type |
|-------------|------------|------------|-------------|---------------------|
| `buy` | Acheter | Buy | 50 | buy |
| `rent` | Louer | Rent | 30 | rent |
| `sell` | Vendre | Sell | 60 | sell |
| `invest` | Investir | Invest | 100 | invest |
| `search_property` | Chercher un bien | Search property | 25 | buy/rent |
| `find_professional` | Trouver un professionnel | Find professional | 35 | find |
| `service` | Commander un service | Order service | 40 | service |
| `finance` | Financer | Finance | 70 | finance |
| `other` | Autre | Other | 10 | other |

### 2.3 Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | 0:1 | Optional link to created project |
| User (creator) | N:1 | User who expressed the intent |
| ServiceRequest | 0:N | May spawn service requests |
| Transaction | 0:1 | May lead to transaction |

---

## 3. Entity: ServiceRequest

Represents a specific service ask from a user — a request to the platform or an agent to perform an action.

### 3.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `user_id` | UUID | Requesting user |
| `intent_id` | UUID? | Source intent (if detected) |
| `project_id` | UUID? | Parent project |
| `request_type` | Enum | `search \| quote \| document \| visit \| expertise \| estimation \| legal \| other` |
| `status` | Enum | `open \| in_progress \| fulfilled \| cancelled \| expired` |
| `description` | Text | Free-text request description |
| `assigned_to_id` | UUID? | Agent assigned to fulfill |
| `deadline` | DateTime? | Requested completion date |
| `fulfilled_at` | DateTime? | When fulfilled |
| `created_at` | DateTime | Creation timestamp |

### 3.2 ServiceRequest Types

| Request Type | Example | Typical Fulfiller |
|-------------|---------|-------------------|
| `search` | "Trouve-moi un terrain à Bastos" | Matching engine / agent |
| `quote` | "Combien coûte l'estimation de ma villa?" | Agent / service |
| `document` | "J'ai besoin d'un modèle de bail" | Platform / document service |
| `visit` | "Je veux visiter le bien RF-2024-089" | Agent / holder |
| `expertise` | "Expertise structurelle de l'immeuble" | Expert professional |
| `estimation` | "Estimez mon terrain de 500m2 à Mvog-Mbi" | Evaluateur |
| `legal` | "Besoin d'un conseil fiscal pour vente" | Legal professional |

---

## 4. Entity: Transaction

The legal/financial deal-closing entity. Created after successful negotiation between demandeur and holder.

### 4.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID? | Originating project |
| `property_id` | UUID | Property being transacted |
| `transaction_type` | Enum | `sale \| rental \| short_stay \| lease \| cession_bail \| bail_commercial \| cession \| finance \| find \| service` |
| `status` | Enum | 7-state lifecycle |
| `demandeur_id` | UUID | Buyer/tenant/demandeur |
| `holder_id` | UUID | Seller/owner/holder |
| `agent_id` | UUID? | Managing agent |
| `notaire_id` | UUID? | Notary (if applicable) |
| `price_agreed` | Decimal | Agreed transaction price |
| `currency` | String | Currency (default: XAF) |
| `payment_milestones` | JSON[] | Array of milestone objects |
| `negotiation_id` | UUID? | Link to negotiation record |
| `signature_demandeur_at` | DateTime? | Demandeur signature |
| `signature_holder_at` | DateTime? | Holder signature |
| `handover_at` | DateTime? | Key handover / possession |
| `completed_at` | DateTime? | Completion |
| `failed_at` | DateTime? | Failure timestamp |
| `failure_reason` | String? | Reason for failure |
| `follow_up_at` | DateTime? | Post-completion follow-up |
| `created_at` | DateTime | Creation |

### 4.2 Transaction Type Enum (Extended)

See [§10 Transaction Type Catalog](#10-transaction-type-catalog) for full definitions.

### 4.3 Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | 0..1:1 | Project that led to this transaction |
| Property | N:1 | Property being transacted |
| Negotiation | 0:1 | Preceding negotiation |
| User (demandeur) | N:1 | Primary buyer/tenant |
| User (holder) | N:1 | Seller/owner |
| User (agent) | N:1 | Managing agent |
| User (notaire) | N:1 | Notary |
| Document | 1:N | Transaction documents |

---

## 5. Intent Detection Pipeline

### 5.1 Pipeline Stages

```
Raw Utterance (FR/EN/PID)
  → Language Detection
    → Tokenization & Normalization
      → Keyword Scoring (per intent dictionary)
        → Confidence Calculation
          → Threshold Check (0.70)
            → Multi-Intent Split (if applicable)
              → Entity Extraction (per sub-intent)
                → Urgency Scoring
                  → Intent-to-Role Mapping
                    → Project Goal Assignment
                      → Project Creation / Routing
```

### 5.2 Language Support

| Language | Code | Tokenizer | Normalization |
|----------|------|-----------|---------------|
| French | `fr` | Standard + French-specific contractions (au→à le, du→de le) | Unicode NFKD, lowercase, accent stripping for matching, accent preservation for display |
| English | `en` | Standard | Unicode NFKD, lowercase |
| Pidgin | `pid` | Custom tokenizer (Camfranglais dictionary, compound word splitting) | Custom normalization (mon/ma→my, chop→eat/eat→buy) |

### 5.3 Keyword Dictionaries — FR (Partial)

#### BUY Keywords

| Keyword | Weight | Category |
|---------|--------|----------|
| acheter | 50 | primary |
| achat | 50 | primary |
| cherche un terrain | 60 | specific |
| cherche une maison | 55 | specific |
| veux acquérir | 50 | primary |
| veux devenir propriétaire | 45 | aspirational |
| je veux un bien | 40 | general |
| parcelle | 55 | land-specific |
| villa | 50 | property-specific |
| appartement à vendre | 55 | listing |

#### RENT Keywords

| Keyword | Weight | Category |
|---------|--------|----------|
| louer | 30 | primary |
| location | 30 | primary |
| cherche un appart | 35 | specific |
| studio | 30 | property-specific |
| meublé | 25 | modifier |
| colocation | 30 | specific |
| bail | 25 | legal |
| loyer | 20 | price-related |

#### SELL Keywords

| Keyword | Weight | Category |
|---------|--------|----------|
| vendre | 60 | primary |
| vente | 60 | primary |
| mise en vente | 60 | primary |
| je veux vendre | 65 | primary |
| estimer mon bien | 40 | related |
| proprio vend | 55 | specific |

#### INVEST Keywords

| Keyword | Weight | Category |
|---------|--------|----------|
| investir | 100 | primary |
| investissement | 100 | primary |
| placement | 90 | primary |
| rentabilité | 85 | specific |
| rendement | 85 | specific |
| cash purchase | 95 | diaspora-specific |
| diaspora | 80 | diaspora-specific |
| invest locatif | 100 | specific |

#### FIND_PROFESSIONAL Keywords

| Keyword | Weight | Category |
|---------|--------|----------|
| cherche un agent | 35 | primary |
| trouver un notaire | 40 | specific |
| besoin d'un géomètre | 40 | specific |
| architecte | 35 | professional |
| avocat | 35 | professional |
| expert immobilier | 40 | professional |
| évaluateur | 40 | professional |
| courtier | 35 | professional |
| constructeur | 35 | professional |

### 5.4 English Keyword Dictionary (Partial)

| Keyword | Intent | Weight |
|---------|--------|--------|
| buy | buy | 50 |
| purchase | buy | 50 |
| looking for land | buy | 60 |
| looking for house | buy | 55 |
| rent | rent | 30 |
| rental | rent | 30 |
| apartment for rent | rent | 35 |
| sell | sell | 60 |
| selling my property | sell | 65 |
| invest | invest | 100 |
| investment | invest | 100 |
| find an agent | find_professional | 35 |
| need a notary | find_professional | 40 |
| finance | finance | 70 |
| loan | finance | 65 |
| mortgage | finance | 65 |

### 5.5 Pidgin Keyword Dictionary (Partial)

| Keyword | Intent | Weight | Standard Form |
|---------|--------|--------|---------------|
| wan buy | buy | 55 | want to buy |
| wan rent | rent | 35 | want to rent |
| wan sell | sell | 65 | want to sell |
| wan put for sale | sell | 60 | want to list for sale |
| dey find house | search_property | 30 | looking for house |
| dey find land | search_property | 35 | looking for land |
| how much | search_property | 20 | price inquiry |
| I get property | sell | 55 | I have property to sell |
| wan invest | invest | 100 | want to invest |
| need lawyer | find_professional | 35 | need lawyer |
| need contractor | find_professional | 35 | need contractor |
| chop credit | finance | 70 | get financing |

### 5.6 Scoring Algorithm

```
For each intent I in {buy, rent, sell, invest, search_property, find_professional, service, finance}:
  raw_score(I) = sum(keyword_weight for each matched keyword in dictionary[language][I])
  normalized_score(I) = raw_score(I) / max_possible_score(I)
  boost(I) = 1.0 + (0.1 × count(specific_matches) / count(total_matches))
  final_score(I) = normalized_score(I) × boost(I)

primary_intent = argmax(final_score)
confidence = final_score(primary_intent) / sum(final_score(all intents))

if confidence >= threshold (0.70):
  assign primary_intent
elif confidence >= 0.50:
  flag for human disambiguation
else:
  fallback to "other" or explicit selection prompt
```

### 5.7 Confidence Threshold Configuration

| Context | Threshold | Behavior Below Threshold |
|---------|-----------|-------------------------|
| WhatsApp inbound | 0.70 | Prompt user to select from top 2-3 options |
| Telegram inbound | 0.70 | Same as WhatsApp |
| Dashboard form | 0.50 | Pre-fill suggestion (user confirms) |
| API inbound | 0.80 | Reject with "unclear intent" error |
| Agent manual entry | 0.40 | Agent overrides threshold |

### 5.8 Detection Method

| Method | Description | When Used |
|--------|-------------|-----------|
| `keyword` | Automatic pipeline with keyword matching | Chat/API inbound |
| `explicit_selection` | User picks from a list | Dashboard form, agent-assisted |
| `hybrid` | Keyword detection with user confirmation | WhatsApp/Telegram with disambiguation |

---

## 6. Multi-Intent Detection & Parallel Project Creation

### 6.1 Detection

When multiple intents score above threshold in a single utterance:

```
Input: "Je cherche un terrain à Bastos pour construire, et aussi un notaire pour la paperasse"
Analysis:
  Intent 1: buy (terrain) — confidence 0.82
  Intent 2: find_professional (notaire) — confidence 0.75
  Combined: is_multi_intent = true
```

Multi-intent is triggered when:
- At least 2 intent scores >= threshold (0.70)
- OR total score >= 1.40 with at least 2 distinct intents
- Semantic distance between intents > 0.3 (non-overlapping)

### 6.2 Parallel Project Creation

Each validated sub-intent spawns an independent project:

| Sub-Intent | Project Type | Title | Independent? |
|------------|-------------|-------|--------------|
| buy (terrain) | buy | "Recherche terrain Bastos" | Yes |
| find_professional (notaire) | find | "Recherche notaire" | Yes |

Multi-intent projects are linked via `multi_intent_group_id` for cross-project coordination.

### 6.3 Multi-Intent Storage

| Field | Type | Description |
|-------|------|-------------|
| `is_multi_intent` | Boolean | Whether the source utterance had multiple intents |
| `sub_intents` | JSON[] | `[{intent, confidence, entities, assigned_project_id}]` |
| `multi_intent_group_id` | UUID | Shared group ID across all spawned projects |

---

## 7. Urgency Detection

### 7.1 Urgency Score Calculation

Extracted from temporal keywords and sentence structure:

| Signal | Weight | Examples |
|--------|--------|----------|
| Temporal urgency adverb | 0.30 | `urgent`, `vite`, `rapidement`, `asap`, `now`, `quickly` |
| Specific deadline | 0.35 | `cette semaine`, `avant vendredi`, `this week`, `by Monday` |
| Negative consequence | 0.20 | `sinon je perds`, `offre expire`, `offer expires`, `owner selling to someone` |
| Repetition/emphasis | 0.10 | Multiple messages, all caps (`URGENT`), repeated `!!` |
| Diaspora premium | 0.05 | Diaspora user with short timeline |

### 7.2 Urgency Levels

| Level | Score Range | SLA Target | Routing |
|-------|-------------|------------|---------|
| `low` | 0.00 - 0.25 | P2 (< 24h) | Standard routing |
| `medium` | 0.26 - 0.50 | P1 (< 2h) | Priority routing |
| `high` | 0.51 - 0.75 | P0 (< 30min) | Immediate routing + agent notification |
| `urgent` | 0.76 - 1.00 | P0 (< 15min) | Immediate routing + escalation to responsible |

### 7.3 Storage on Project

| Field | Type | Description |
|-------|------|-------------|
| `urgency_score` | Float | 0.0 - 1.0 |
| `urgency_level` | Enum | `low \| medium \| high \| urgent` |
| `urgency_detected_at` | DateTime | When urgency was assessed |
| `urgency_keywords` | String[] | Which keywords triggered urgency |

---

## 8. Entity Extraction Per Intent

### 8.1 Extraction Rules Per Intent Type

#### BUY / SEARCH_PROPERTY

| Entity | Extraction Method | Example |
|--------|-------------------|---------|
| `budget_min` | Price pattern: `budget de X`, `max X`, `entre X et Y` | "budget 50 millions" → 50,000,000 |
| `budget_max` | Price pattern + range | "entre 30 et 50 millions" → 50,000,000 |
| `city` | Gazetteer lookup | "Bastos", "Yaoundé", "Douala" |
| `neighborhood` | Gazetteer lookup | "Mvog-Mbi", "Bonanjo" |
| `property_type` | Type dictionary | "terrain", "villa", "appartement", "studio" |
| `surface_min` | Surface pattern | "au moins 500m2" |
| `bedrooms` | Number + room pattern | "3 chambres" |
| `furnished` | Binary pattern | "meublé", "non meublé" |
| `timeline` | Temporal pattern | "dans 3 mois", "avant décembre" |

#### RENT

| Entity | Extraction Method | Example |
|--------|-------------------|---------|
| `budget_max` | Price + "loyer" | "loyer max 200 000" |
| `city` | Gazetteer | "Douala" |
| `neighborhood` | Gazetteer | "Bonapriso" |
| `property_type` | Type dictionary | "appartement", "studio", "maison" |
| `bedrooms` | Number + room | "2 chambres" |
| `furnished` | Binary | "meublé" |
| `lease_duration` | Duration pattern | "pour 1 an", "long terme" |
| `move_in_date` | Temporal | "disponible maintenant" |

#### SELL

| Entity | Extraction Method | Example |
|--------|-------------------|---------|
| `property_type` | Type dictionary | "villa duplex" |
| `city` | Gazetteer | "Yaoundé" |
| `neighborhood` | Gazetteer | "Mvolyé" |
| `asking_price` | Price pattern | "je veux 80 millions" |
| `surface` | Surface pattern | "500 m2" |
| `title_status` | Document keyword | "titre foncier", "sans titre" |
| `urgency` | Temporal | "vends urgemment" |

#### INVEST

| Entity | Extraction Method | Example |
|--------|-------------------|---------|
| `budget_range` | Price pattern | "investir 100 millions" |
| `investment_type` | Type dictionary | "locatif", "terrain", "commercial" |
| `target_roi` | Percentage pattern | "rendement 8%" |
| `city` | Gazetteer | "Douala" |
| `is_diaspora` | Geo-IP / keyword | "je suis à l'étranger" |
| `cash_purchase` | Keyword | "cash", "comptant" |

#### FIND_PROFESSIONAL

| Entity | Extraction Method | Example |
|--------|-------------------|---------|
| `profession` | Professional dictionary | "notaire", "géomètre", "architecte" |
| `city` | Gazetteer | "Yaoundé" |
| `specialization` | Keyword | "spécialiste en droit foncier" |
| `mission` | Free text | "pour authentifier un acte de vente" |

### 8.2 Extracted Entity Storage

Extracted entities are stored per intent as a normalized JSON object:

```json
{
  "budget_min": 30000000,
  "budget_max": 50000000,
  "city": "Yaoundé",
  "neighborhood": "Bastos",
  "property_type": "terrain",
  "surface_min": 300,
  "timeline": "6 months",
  "is_diaspora": false,
  "cash_purchase": null
}
```

Entities are used to:
1. Pre-populate qualification fields on the created Project
2. Provide initial matching criteria
3. Improve lead scoring (boosters for detected entities)

---

## 9. Intent-to-Role Mapping

### 9.1 Mapping Table

| Detected Intent | Business Role | User Typology | Transaction Participant Role |
|----------------|--------------|---------------|------------------------------|
| `buy` | `buyer` | `particular` | `buyer` (achèteur) |
| `rent` | `tenant` | `particular` | `lessee` (preneur) |
| `sell` | `seller` | `particular / professional` | `seller` (vendeur) |
| `invest` | `investor` | `particular / diaspora` | `buyer` (investor variant) |
| `search_property` | `visitor` | `particular` | — (undetermined) |
| `find_professional` | `client` | `particular / professional` | — (service client) |
| `service` | `client` | `particular / professional` | — (service client) |
| `finance` | `investor` | `particular` | `borrower` (emprunteur) |
| `other` | `visitor` | `particular` | — |

### 9.2 Role Assignment Rules

- **Single match**: Role is directly assigned from detected intent.
- **Multi-intent**: User gets the primary role from the highest-confidence intent. Secondary roles are stored on sub-projects.
- **Explicit override**: User can manually change their role after intent detection.
- **Role affects**: Qualification matrix selection, matching strategy, recommended services, CRM segmentation.

### 9.3 Role-Dependent Qualification

| Role | Qualification Matrix Family | Example Question |
|------|---------------------------|------------------|
| buyer | Residential Search (18 matrices) | "Quel type de propriété cherchez-vous?" |
| tenant | Residential Search (rental variant) | "Quel est votre budget loyer max?" |
| seller | Sales Listing (8 matrices) | "Quel est le prix de vente souhaité?" |
| investor | Investment (5 matrices) | "Quel rendement annuel visez-vous?" |
| client (find) | Professional Search (27 matrices) | "Quel type de professionnel cherchez-vous?" |
| client (service) | Real Estate Service (24 matrices) | "Quel service souhaitez-vous commander?" |

---

## 10. Transaction Type Catalog

### 10.1 Complete Transaction Types

| # | Transaction Type | Code | Category | Duration | Legal Framework | UDM Mapping |
|---|-----------------|------|----------|----------|----------------|-------------|
| 1 | Sale | `sale` | Transfer of ownership | Permanent | Civil code (vente) | `project_type: buy` |
| 2 | Rental | `rental` | Bail for habitation | < 3 years | OHADA / Civil code | `project_type: rent` |
| 3 | Short Stay | `short_stay` | Location courte durée | < 90 days | Specific contract | `project_type: rent` (sub-type) |
| 4 | Lease (3+ years) | `lease` | Bail à long terme | 3+ years | Civil code (bail 3+ ans) | `project_type: rent` (extended) |
| 5 | Commercial Lease | `bail_commercial` | Bail commercial | 3-9 years | OHADA commercial code | `project_type: rent` (sub-type) |
| 6 | Commercial Lease Transfer | `cession_bail` | Cession de droit au bail | Transfer of remaining term | OHADA / civil code | `project_type: other` |
| 7 | Business Asset Transfer | `cession` | Cession de fonds de commerce | Permanent | Commercial code | `project_type: other` |
| 8 | Financing | `finance` | Demande de financement | Variable | Banking / credit | `project_type: finance` |
| 9 | Professional Search | `find` | Recherche de professionnel | Per engagement | Service contract | `project_type: find` |
| 10 | Service Procurement | `service` | Prestation de service | Per engagement | Service contract | `project_type: service` |

### 10.2 Detailed Type Definitions

#### 10.2.1 short_stay

| Property | Value |
|----------|-------|
| **Code** | `short_stay` |
| **Duration** | 1 to 89 days |
| **Keywords** | `court séjour`, `weekend`, `chambre d'hôte`, `airbnb`, `vacances`, `short stay` |
| **Qualification Matrices** | Hotel/Tourism sub-referentiel |
| **Specific Fields** | Check-in/check-out dates, number of guests, amenities |
| **Payment** | Full or partial upfront |
| **Required Documents** | ID copy, short-stay contract, deposit receipt |
| **Legal Notes** | No tenant rights; no lease renewal |

#### 10.2.2 lease (bail 3+ ans)

| Property | Value |
|----------|-------|
| **Code** | `lease` |
| **Duration** | 3 to 99 years |
| **Keywords** | `bail longue durée`, `lease`, `long terme`, `bail emphytéotique` |
| **Qualification Matrices** | Residential or Commercial (long-term) |
| **Specific Fields** | Lease duration, renewal options, indexation clause |
| **Payment** | Monthly rent + deposit (typically 3-6 months) |
| **Required Documents** | Lease contract (notarized), ID copies, tax clearance |
| **Legal Notes** | Must be registered; tenant may have right to renew |

#### 10.2.3 cession_bail (commercial lease transfer)

| Property | Value |
|----------|-------|
| **Code** | `cession_bail` |
| **Duration** | Transfer of remaining lease term |
| **Keywords** | `cession de bail`, `transfert de bail`, `reprise de bail commercial` |
| **Qualification Matrices** | Commercial sub-referentiel |
| **Specific Fields** | Original lease terms, remaining duration, transfer price |
| **Payment** | Transfer fee + ongoing rent |
| **Required Documents** | Original lease, landlord consent, RCCM, tax ID |
| **Legal Notes** | Landlord approval required; rights and obligations transfer |

#### 10.2.4 bail_commercial (commercial lease 3-9 ans)

| Property | Value |
|----------|-------|
| **Code** | `bail_commercial` |
| **Duration** | 3 to 9 years (renewable) |
| **Keywords** | `bail commercial`, `local commercial`, `boutique`, `magasin` |
| **Qualification Matrices** | Commercial sub-referentiel |
| **Specific Fields** | Business type, renovation responsibility, signage rights |
| **Payment** | Commercial rent + deposit (typically 6-12 months) |
| **Required Documents** | Commercial lease contract, company RCCM, tax ID, business license |
| **Legal Notes** | OHASA uniform act; tenant has right to renew; 3-2-3-2 formula common |

#### 10.2.5 cession (business asset transfer)

| Property | Value |
|----------|-------|
| **Code** | `cession` |
| **Duration** | Permanent |
| **Keywords** | `cession`, `fonds de commerce`, `reprise d'entreprise`, `business transfer` |
| **Qualification Matrices** | Business transfer sub-referentiel |
| **Specific Fields** | Business valuation, inventory, client list, goodwill |
| **Payment** | Lump sum or structured payment |
| **Required Documents** | Business registration (RCCM), tax clearance, financial statements, lease, licenses |
| **Legal Notes** | Publication required; right of first refusal; registration with tax authorities |

#### 10.2.6 finance (financing request)

| Property | Value |
|----------|-------|
| **Code** | `finance` |
| **Duration** | Variable (loan term) |
| **Keywords** | `financement`, `crédit`, `prêt`, `hypothèque`, `financing`, `loan`, `mortgage` |
| **Qualification Matrices** | 10 financing matrices |
| **Specific Fields** | Loan amount, purpose, income, existing commitments, collateral |
| **Payment** | Monthly installments |
| **Required Documents** | ID, proof of income, property documents, bank statements |
| **Legal Notes** | Partner bank integration; credit assessment |

#### 10.2.7 find (professional search)

| Property | Value |
|----------|-------|
| **Code** | `find` |
| **Duration** | Per engagement |
| **Keywords** | `trouver`, `recherche professionnel`, `find`, `need`, `agent`, `notaire` |
| **Qualification Matrices** | 27 professional search matrices |
| **Specific Fields** | Profession, specialization, location, mission |
| **Payment** | Free or premium (lead purchase for contact) |
| **Required Documents** | None (service discovery) |
| **Legal Notes** | Professional verification recommended |

#### 10.2.8 service (real estate service procurement)

| Property | Value |
|----------|-------|
| **Code** | `service` |
| **Duration** | Per engagement |
| **Keywords** | `estimation`, `expertise`, `photographie`, `service`, `besoin d'un service` |
| **Qualification Matrices** | 24 real estate service matrices |
| **Specific Fields** | Service type, scope, location, timeline |
| **Payment** | Service price (fixed, per Service catalog) |
| **Required Documents** | Property documents (if applicable) |
| **Legal Notes** | Service contract; linked to ServiceOrder |

---

## 11. Transaction 7-State Lifecycle

### 11.1 State Machine

```
          ┌────────────────────────────────────────────┐
          │                                            │
          v                                            │
AGREEMENT ──→ PREPARATION ──→ DOCUMENTS ──→ PAYMENT ──→ SIGNATURE ──→ HANDOVER ──→ COMPLETED
   │            │               │             │            │              │
   │            │               │             │            │              │
   └──→ FAILED ←┴───────────────┴─────────────┴────────────┴──────────────┴──→ ARCHIVED
```

### 11.2 State Definitions

| State | Entry Condition | Responsible | Actions | Max Duration | Exit |
|-------|----------------|-------------|---------|-------------|------|
| `agreement` | Negotiation accepted | Both parties | Document accepted price, set milestones, assign agent/notaire | 7 days | Both confirm |
| `preparation` | Agreement confirmed | Agent / both | Gather required docs, verify property title, prepare contract draft | 14 days | Docs collected |
| `documents` | Preparation complete | Both parties | Upload/verify all transaction documents, admin validation | 14 days | All docs validated |
| `payment` | Documents validated | Demandeur / agent | Pay deposit/partial, set payment schedule | 30 days | Payment confirmed |
| `signature` | Payment stage OK | Both + notaire | Sign final contract, notarize if required | 7 days | Both signed |
| `handover` | All signatures done | Holder | Key handover, possession transfer, final inspection | 3 days | Handover confirmed |
| `completed` | Handover confirmed | System | Mark complete, trigger follow-up scheduling, update property availability | — | Archived or followed up |

### 11.3 Failure States

| State | Failure Reason | Recovery |
|-------|---------------|----------|
| Any | Party withdraws | Negotiate or abandon |
| `documents` | Missing/invalid documents | Request new documents or abort |
| `payment` | Payment failure | Retry payment, renegotiate terms |
| `signature` | Party refuses to sign | Mediation or failure |
| Any | `failure_reason` captured | NBA: rematch or new transaction |

If transaction stays in any state beyond configured max duration, it auto-escalates:

| Layer | Escalation | Action |
|-------|-----------|--------|
| 1 | 24h before expiry | Reminder to responsible party |
| 2 | At expiry | Escalate to agent/notaire |
| 3 | 7d past expiry | Escalate to platform admin |

---

## 12. Negotiation Workflow

### 12.1 Negotiation States

```
not_started
  → [Demandeur makes offer]
demandeur_proposes
  → [Holder responds]
holder_responds → counter_offer → demandeur_proposes (cycle)
                → accepted → NEGOTIATION_SUCCESSFUL
                → rejected → NEGOTIATION_FAILED
                → silent   → [reminder cycle] → failed (silence)
```

### 12.2 State Definitions

| State | Description | Next States |
|-------|-------------|-------------|
| `not_started` | No offer made yet | `demandeur_proposes` |
| `demandeur_proposes` | Demandeur has submitted an offer | `holder_responds` |
| `holder_responds` | Holder has acknowledged and responded | `counter_offer`, `accepted`, `rejected`, `silent` |
| `counter_offer` | Counter-offer made by either party | `demandeur_proposes` (if holder counters), `holder_responds` (if demandeur counters) |
| `accepted` | Offer accepted by both parties | Transaction `agreement` state |
| `rejected` | Offer rejected by either party | Failure diagnostic |
| `silent` | No response within 48h | Reminder cycle |
| `failed` | Negotiation failed (rejection or silence) | NBA: rematch or close |
| `escalated` | Escalated to agent/admin | Mediation or assisted negotiation |

### 12.3 Negotiable Elements Per Transaction Type

| Transaction Type | Negotiable Elements |
|-----------------|-------------------|
| `sale` | Price, payment schedule (lump sum vs installments), closing date, inclusions (furniture, appliances), condition precedents |
| `rental` | Monthly rent, deposit amount, lease duration, maintenance responsibility, notice period |
| `short_stay` | Daily rate, cleaning fee, check-in/out flexibility, cancellation policy |
| `lease` | Rent (annual indexation), deposit, responsibility for major repairs, renewal options |
| `bail_commercial` | Rent, deposit (typically 6-12 months), renovation/signage rights, duration, renewal terms |
| `cession_bail` | Transfer fee, remaining duration acceptance, condition of premises |
| `cession` | Price, payment structure, inventory inclusion, handover date, training period |
| `finance` | Interest rate, loan duration, grace period, collateral terms |

### 12.4 Offer/Counter-Offer Tracking

Each negotiation records a full offer history:

| Field | Type | Description |
|-------|------|-------------|
| `offer_id` | UUID | Unique offer identifier |
| `negotiation_id` | UUID | Parent negotiation |
| `offered_by` | UUID | User who made this offer |
| `offer_type` | Enum | `initial \| counter \| acceptance \| rejection` |
| `amount` | Decimal | Offered amount |
| `terms` | JSON | Negotiable elements values at this point |
| `message` | Text | Accompanying message |
| `made_at` | DateTime | Timestamp |
| `responded_at` | DateTime? | When the other party responded |
| `response` | Enum? | `accepted \| countered \| rejected \| no_response` |

### 12.5 Reminder System on Silence

| Day | Action |
|-----|--------|
| 48h silence (T+48) | First reminder: "Do you have a response to the offer?" |
| 96h silence (T+96) | Second reminder: "We haven't heard from you. Would you like to counter-offer?" |
| 168h silence (7d) | Final reminder: "Without response, negotiation will close." |
| 240h silence (10d) | Auto-close negotiation as "failed (silence)" |

### 12.6 Post-Failure Diagnostic

When a negotiation fails, a structured diagnostic is captured:

| Field | Type | Description |
|-------|------|-------------|
| `failure_reason` | Enum | `price_disagreement \| terms_disagreement \| silence \| third_party \| other` |
| `price_gap_percentage` | Float | (last_offer - asking_price) / asking_price |
| `last_offer_by` | UUID | Who made the last offer |
| `stuck_state_duration` | Int | Hours spent in current state |
| `reminders_sent` | Int | Total reminders sent before failure |
| `suggested_nba` | Enum | `new_match \| price_review \| agent_assist \| mediation` |

---

## 13. Document Requirements Per Transaction Type

### 13.1 Required Documents Matrix

| Transaction Type | Essential Documents | Optional Documents | Verification Required |
|-----------------|-------------------|-------------------|---------------------|
| `sale` | Land title, seller ID, buyer ID | Power of attorney, tax clearance, cadastral plan, building permit | Land title (notary verification) |
| `rental` | Lease contract, ID copies (both), deposit receipt | Inventory of fixtures, utility contracts, insurance cert | ID verification |
| `short_stay` | Short-term contract, ID copy, payment receipt | Insurance, guest list | ID verification |
| `lease` | Notarized lease contract, ID copies, tax clearance (if commercial) | Property title, building permit, inspection report | Notarization required |
| `bail_commercial` | Commercial lease contract, RCCM (business), tax ID, ID copies | Financial statements, business license, previous lease | RCCM verification |
| `cession_bail` | Original lease, landlord consent letter, transfer agreement, RCCM | Inventory, condition report, financial statements | Landlord consent verification |
| `cession` | Business registration (RCCM), tax clearance, financial statements, lease, licenses, ID | Client list, supplier contracts, employee records | Publication in newspaper required |
| `finance` | ID, proof of income, property documents, bank statements (3 months) | Business plan, collateral documents, guarantor docs | Income verification |
| `find` | None (service discovery) | — | — |
| `service` | Service order, property documents (if applicable) | — | Per service type |

### 13.2 Document State Machine

```
not_required
  → [Transaction type assigned]
required → pending → [Uploaded]
  uploaded → pending_validation → [Admin/notary validates]
    validated
    rejected → [Resubmit] → uploaded
```

### 13.3 Document Type Enum

| Document Type | Applies To |
|--------------|------------|
| `land_title` | sale, lease |
| `national_id` | All transaction types |
| `passport` | All (alternative to ID) |
| `lease_contract` | rental, lease, bail_commercial |
| `commercial_lease_contract` | bail_commercial, cession_bail |
| `sale_agreement` | sale, cession |
| `power_of_attorney` | sale (if representative) |
| `tax_clearance` | sale, cession, lease |
| `rccm` | bail_commercial, cession, cession_bail |
| `tax_id` | bail_commercial, cession |
| `proof_of_income` | finance |
| `bank_statement` | finance |
| `inventory_of_fixtures` | rental, lease |
| `deposit_receipt` | rental, short_stay |
| `financial_statement` | cession, finance |
| `business_license` | bail_commercial, cession |
| `insurance_cert` | rental, short_stay (optional) |
| `building_permit` | sale (optional) |
| `cadastral_plan` | sale (optional) |
| `landlord_consent` | cession_bail |

---

## 14. Journey Stages & Business Actions

### 14.1 Journey Stages

| Stage | Code | Description | Entry From | Exit To |
|-------|------|-------------|------------|---------|
| Discovery | `discovery` | User first arrives on platform | Inbound message / signup | Intent detection |
| Qualification | `qualification` | User intent is clarified and criteria collected | Intent detected | Qualification complete |
| Matching | `matching` | Property/professional matching in progress | Criteria set | Match proposed |
| Presentation | `presentation` | Matches shown to user | Match found | User selects / user rejects |
| Contact | `contact` | User requests contact with holder/professional | User selects match | Contact established |
| Visit | `visit` | Property visit scheduled/in progress | Contact established | Visit completed |
| Negotiation | `negotiation` | Offer/counter-offer in progress | Visit completed (or direct) | Agreement reached |
| Transaction | `transaction` | Deal closing in progress | Agreement reached | Deal closed |
| Completed | `completed` | Deal closed, follow-up stage | Transaction completed | — |

### 14.2 Business Actions

| Action | Code | Triggered By | System Effect |
|--------|------|-------------|---------------|
| Create Project | `create_project` | Intent detected or explicit form | Create Project entity |
| Start Qualification | `start_qualification` | Project created | Send first qualification question |
| Launch Search | `launch_search` | Qualification complete | Trigger matching engine |
| Propose Match | `propose_match` | Match score >= 60 | Send match proposal to user |
| Request Contact | `request_contact` | User selects match | Initiate double consent flow |
| Establish Contact | `establish_contact` | Double consent obtained | Reveal contact info |
| Schedule Visit | `schedule_visit` | Contact established | Create Visit entity |
| Complete Visit | `complete_visit` | Visit confirmed as done | Trigger post-visit NBA |
| Open Negotiation | `open_negotiation` | Visit satisfactory or direct offer | Create Negotiation |
| Make Offer | `make_offer` | User submits price/terms | Record offer, notify counter-party |
| Accept Offer | `accept_offer` | Counter-party accepts | Create Transaction |
| Reject Offer | `reject_offer` | Counter-party rejects | Offer rejected, offer rematch |
| Create Transaction | `create_transaction` | Offer accepted | Create Transaction entity |
| Request Document | `request_document` | Transaction state requires doc | Generate document request |
| Validate Document | `validate_document` | Doc uploaded | Move to next state |
| Complete Transaction | `complete_transaction` | All states completed | Archive, update property |
| Archive Project | `archive_project` | Completed / abandoned | Freeze project |

### 14.3 Journey Stage × Business Action Matrix

| Stage | Entry Action | During-Stage Action | Exit Action |
|-------|-------------|--------------------|-------------|
| Discovery | `receive_message` | `detect_intent`, `suggest_options` | `create_project` |
| Qualification | `start_qualification` | `ask_question`, `collect_answer` | `launch_search` |
| Matching | `launch_search` | `score_matches`, `recalculate` | `propose_match` |
| Presentation | `propose_match` | `show_details`, `show_comparison` | `request_contact` / `request_rematch` |
| Contact | `request_contact` | `double_consent`, `reveal_info` | `establish_contact` |
| Visit | `schedule_visit` | `send_reminder`, `log_attendance` | `complete_visit` |
| Negotiation | `open_negotiation` | `record_offer`, `send_counter` | `accept_offer` / `reject_offer` |
| Transaction | `create_transaction` | `request_document`, `process_payment` | `complete_transaction` / `archive` |

---

## 15. Complete Extension Mapping Table

### 15.1 Intent Detection Extensions (INT)

| Extension ID | Concept | Proposed Entity | Target Fields | Priority |
|-------------|---------|----------------|--------------|----------|
| EXT-INT-001 | Keyword-based intent detection | Intent + IntentEngine | `source_text`, `detected_intent`, `confidence`, `threshold`, `language` | P1 |
| EXT-INT-002 | Confidence threshold (0.70) | IntentEngine (config) | `threshold` (global config, per-channel override) | P1 |
| EXT-INT-003 | Multi-intent detection | Intent | `is_multi_intent`, `sub_intents`, `multi_intent_group_id` | P2 |
| EXT-INT-004 | Urgency detection | Intent + Project | `urgency_score`, `urgency_level` on Project | P2 |
| EXT-INT-005 | Entity extraction per intent | Intent | `extracted_entities` (JSON), qualified fields auto-populated on Project | P2 |
| EXT-INT-006 | Intent-to-role mapping | Intent + Project + User | `project_type_mapping`, role derived from intent | P2 |

### 15.2 Transaction Type Extensions (TRX)

| Extension ID | Concept | Proposed Entity | Target Fields | Priority |
|-------------|---------|----------------|--------------|----------|
| EXT-TRX-001 | short_stay transaction type | Transaction | `transaction_type` includes `short_stay` | P2 |
| EXT-TRX-002 | lease (bail 3+ ans) | Transaction | `transaction_type` includes `lease`, timeline extended | P2 |
| EXT-TRX-003 | cession_bail | Transaction | `transaction_type` includes `cession_bail` | P3 |
| EXT-TRX-004 | bail_commercial | Transaction | `transaction_type` includes `bail_commercial` | P2 |
| EXT-TRX-005 | cession (business asset transfer) | Transaction | `transaction_type` includes `cession` | P3 |
| EXT-TRX-006 | finance (financing request) | Transaction + Project | `transaction_type` includes `finance` | P2 |
| EXT-TRX-007 | find (professional search) | Transaction + Project | `transaction_type` includes `find` | P2 |
| EXT-TRX-008 | service (real estate service procurement) | Transaction + Project | `transaction_type` includes `service` | P2 |

### 15.3 Transaction Workflow Extensions (WF-related)

| Extension ID | Concept | Proposed Entity | Target Fields | Priority |
|-------------|---------|----------------|--------------|----------|
| EXT-WF-004 | Transaction Lifecycle (10 states) | Transaction | `status` (7 pure states), payment_milestones, signatures | P1 |
| EXT-WF-005 | Paid Services & Payment Lifecycle | ServiceOrder, Payment | payment_milestones, ServiceOrder linkage | P1 |

---

## 16. Extension Mapping: INT Extensions

### 16.1 EXT-INT-001 — Keyword-based intent detection

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-INT-001 |
| **Concept** | Keyword-based intent detection from natural language input |
| **Business Reason** | Automatically detect user intent from FR/EN/PID keyword dictionaries |
| **Source** | INTENT_MODEL.md (Gold) |
| **Current Limitation** | V2 has no intent detection — users explicitly select project_type from form |
| **Proposed Target** | Implement Intent entity + IntentEngine service with keyword dictionaries for FR, EN, PID |
| **Required Fields** | `Intent.source_text: Text`, `Intent.detected_intent: Enum`, `Intent.confidence: Float`, `Intent.language: Enum`, `Intent.keyword_scores: JSON` |
| **Required Events** | `intent.detected (payload: {intent_id, detected_intent, confidence, language})` |
| **Required States** | `Intent.detected_intent ∈ {buy, rent, sell, invest, search_property, find_professional, service, finance, other}` |
| **Priority** | P1 |
| **Implementation Wave** | Wave 1 — Foundation |
| **Human Decision** | Y — Intent detection mandatory for all channels or chat-only |

### 16.2 EXT-INT-002 — Confidence threshold (0.70)

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-INT-002 |
| **Concept** | Configurable confidence threshold for intent assignment |
| **Business Reason** | Minimum confidence score (default 0.70) gates automatic intent assignment |
| **Source** | INTENT_MODEL.md (Gold) |
| **Current Limitation** | No confidence scoring or threshold concept in V2 |
| **Proposed Target** | Add `threshold` field to IntentEngine config; per-channel override support |
| **Required Fields** | `IntentEngineConfig.default_threshold: Float (0.70)`, `IntentEngineConfig.channel_overrides: JSON` |
| **Required Events** | `intent.below_threshold (payload: {intent_id, highest_confidence, threshold, fallback_action})` |
| **Required States** | `Intent.confidence >= 0.70 → auto-assign`, `0.50 <= confidence < 0.70 → prompt_user`, `confidence < 0.50 → fallback` |
| **Priority** | P1 |
| **Implementation Wave** | Wave 1 — Foundation |
| **Human Decision** | Y — Confidence threshold value: 0.70 (Gold) or tunable |

### 16.3 EXT-INT-003 — Multi-intent detection

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-INT-003 |
| **Concept** | Support multiple parallel intents in a single utterance |
| **Business Reason** | Users often express compound needs in one message |
| **Source** | INTENT_MODEL.md (Gold) |
| **Current Limitation** | V2 supports single project_type per user; no parallel intent handling |
| **Proposed Target** | Add `is_multi_intent`, `sub_intents`, `multi_intent_group_id` to Intent; spawn parallel projects |
| **Required Fields** | `Intent.is_multi_intent: Boolean`, `Intent.sub_intents: JSON[]` (array of sub-intent objects), `Project.multi_intent_group_id: UUID?` |
| **Required Events** | `intent.multi_detected (payload: {source_text, sub_intents: [{intent, confidence, project_id}]})` |
| **Required States** | `Intent.is_multi_intent ∈ {true, false}` |
| **Priority** | P2 |
| **Implementation Wave** | Wave 2 — Intent Enhancement |
| **Human Decision** | N |

### 16.4 EXT-INT-004 — Urgency detection

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-INT-004 |
| **Concept** | Detect urgency from temporal keywords in user input |
| **Business Reason** | Urgency score drives lead prioritization, SLA routing, agent assignment |
| **Source** | INTENT_MODEL.md (Gold) |
| **Current Limitation** | No urgency detection mechanism in V2 |
| **Proposed Target** | Add `urgency_score`, `urgency_level` fields to Project; urgency scoring in Intent pipeline |
| **Required Fields** | `Intent.urgency_score: Float`, `Project.urgency_score: Float`, `Project.urgency_level: Enum (low | medium | high | urgent)` |
| **Required Events** | `project.urgency_updated (payload: {project_id, old_level, new_level})` |
| **Required States** | `Project.urgency_level ∈ {low, medium, high, urgent}` |
| **Priority** | P2 |
| **Implementation Wave** | Wave 2 — Intent Enhancement |
| **Human Decision** | Y — Urgency scoring method and integration with lead scoring |

### 16.5 EXT-INT-005 — Entity extraction per intent

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-INT-005 |
| **Concept** | Extract budget, location, property type, timeline per detected intent |
| **Business Reason** | Automatically pre-populate qualification fields, reduce user friction |
| **Source** | INTENT_MODEL.md (Gold) |
| **Current Limitation** | No structured entity extraction in V2 |
| **Proposed Target** | Add `extracted_entities` to Intent; auto-populate Project qualification fields from entities |
| **Required Fields** | `Intent.extracted_entities: JSON`, `Project` qualification fields pre-filled from entities |
| **Required Events** | `project.qualification_prefilled (payload: {project_id, source_intent_id, entity_fields: [...]})` |
| **Priority** | P2 |
| **Implementation Wave** | Wave 2 — Intent Enhancement |
| **Human Decision** | Y — Entity extraction method: rule-based (Gold) or NLP |

### 16.6 EXT-INT-006 — Intent-to-role mapping

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-INT-006 |
| **Concept** | Map detected intent to platform role (buyer/tenant/seller/investor/visitor) |
| **Business Reason** | Role-based personalization of user journey, qualification, and matching |
| **Source** | INTENT_TRANSACTION_CROSSWALK.md §3 |
| **Current Limitation** | No formal role mapping or user role abstraction exists in V2 |
| **Proposed Target** | Add `project_type_mapping` to Intent; implement role assignment service; assign business_role on Project |
| **Required Fields** | `Intent.project_type_mapping: Enum`, `Project.business_role: Enum (buyer | seller | tenant | investor | visitor | client)` |
| **Required Events** | `project.role_assigned (payload: {project_id, user_id, role, source_intent_id})` |
| **Required States** | `Project.business_role ∈ {buyer, seller, tenant, investor, visitor, client}` |
| **Priority** | P2 |
| **Implementation Wave** | Wave 2 — Intent Enhancement |
| **Human Decision** | N |

---

## 17. Extension Mapping: TRX Extensions

### 17.1 EXT-TRX-001 — short_stay transaction type

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-TRX-001 |
| **Concept** | Short-term rental (chambre_hotel, appartement_courte_duree) |
| **Business Reason** | Distinguish short-stay from standard rent; different legal/document regime |
| **Source** | INTENT_TRANSACTION_CROSSWALK.md §2 |
| **Current Limitation** | Subsumed by 'rent' project_type; no dedicated short_stay handling |
| **Proposed Target** | Add `short_stay` to `Transaction.transaction_type` enum and `Project.project_type` (or sub-type) |
| **Required Fields** | `Transaction.transaction_type` includes `short_stay`, `Project.project_type` includes `short_stay` or metadata flag |
| **Required Documents** | Short-term contract, ID copy, payment receipt |
| **Qualification Impact** | Hotel/Tourism sub-referentiel matrices |
| **Priority** | P2 |
| **Implementation Wave** | Wave 2 — Transaction Expansion |
| **Human Decision** | Y — short_stay: dedicated project_type or rent sub-type with metadata |

### 17.2 EXT-TRX-002 — lease (bail 3+ ans)

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-TRX-002 |
| **Concept** | Long-term lease (3+ years) with distinct legal requirements |
| **Business Reason** | Different legal regime from standard rental; requires notarization |
| **Source** | INTENT_TRANSACTION_CROSSWALK.md §2 |
| **Current Limitation** | Subsumed by 'rent' with timeline_horizon maxing at 2 years |
| **Proposed Target** | Add `lease` to `Transaction.transaction_type`; extend timeline_horizon to 99 years |
| **Required Fields** | `Transaction.transaction_type` includes `lease`, `Project.timeline_horizon` extended |
| **Required Documents** | Notarized lease contract, ID copies, tax clearance |
| **Priority** | P2 |
| **Implementation Wave** | Wave 2 — Transaction Expansion |
| **Human Decision** | N |

### 17.3 EXT-TRX-003 — cession_bail (commercial lease transfer)

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-TRX-003 |
| **Concept** | Transfer of commercial lease rights |
| **Business Reason** | Distinct legal transaction requiring landlord consent |
| **Source** | INTENT_TRANSACTION_CROSSWALK.md §2 |
| **Current Limitation** | No equivalent; mapped to 'other' in V2 |
| **Proposed Target** | Add `cession_bail` to `Transaction.transaction_type` enum |
| **Required Fields** | `Transaction.transaction_type` includes `cession_bail` |
| **Required Documents** | Original lease, landlord consent letter, transfer agreement, RCCM |
| **Priority** | P3 |
| **Implementation Wave** | Wave 3 — Niche Transaction Types |
| **Human Decision** | Y — cession_bail: dedicated type or metadata extension of 'lease' |

### 17.4 EXT-TRX-004 — bail_commercial (commercial lease 3-9 ans)

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-TRX-004 |
| **Concept** | Commercial lease with 3-9 year terms |
| **Business Reason** | Specific OHADA legal framework; distinct from residential rental |
| **Source** | INTENT_TRANSACTION_CROSSWALK.md §2 |
| **Current Limitation** | Subsumed by generic 'rent' with no commercial lease handling |
| **Proposed Target** | Add `bail_commercial` to `Transaction.transaction_type`; implement commercial-specific fields |
| **Required Fields** | `Transaction.transaction_type` includes `bail_commercial` |
| **Required Documents** | Commercial lease contract, RCCM, tax ID, business license |
| **Qualification Impact** | Commercial sub-referentiel matrices |
| **Priority** | P2 |
| **Implementation Wave** | Wave 2 — Transaction Expansion |
| **Human Decision** | N |

### 17.5 EXT-TRX-005 — cession (business asset transfer)

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-TRX-005 |
| **Concept** | Transfer of business assets (fonds de commerce) |
| **Business Reason** | Not pure real estate; distinct legal process with publication requirement |
| **Source** | INTENT_TRANSACTION_CROSSWALK.md §2 |
| **Current Limitation** | No equivalent; mapped to 'other' in V2 |
| **Proposed Target** | Add `cession` to `Transaction.transaction_type`; implement business transfer workflow |
| **Required Fields** | `Transaction.transaction_type` includes `cession` |
| **Required Documents** | RCCM, tax clearance, financial statements, lease, licenses |
| **Priority** | P3 |
| **Implementation Wave** | Wave 3 — Niche Transaction Types |
| **Human Decision** | Y — cession: in-scope for LAWIM or out-of-scope |

### 17.6 EXT-TRX-006 — finance (financing request)

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-TRX-006 |
| **Concept** | Standalone financing request with 10 qualification matrices |
| **Business Reason** | Users need mortgage/loan discovery; partner bank integration |
| **Source** | INTENT_TRANSACTION_CROSSWALK.md §2 |
| **Current Limitation** | Implicitly bundled into buy/invest projects; no standalone financing |
| **Proposed Target** | Add `finance` to `Transaction.transaction_type`; implement 10 financing qualification matrices |
| **Required Fields** | `Transaction.transaction_type` includes `finance` |
| **Required Documents** | ID, proof of income, property documents, bank statements |
| **Qualification Impact** | 10 financing matrices |
| **Priority** | P2 |
| **Implementation Wave** | Wave 2 — Transaction Expansion |
| **Human Decision** | Y — finance: standalone project type or sub-intent of buy/invest |

### 17.7 EXT-TRX-007 — find (professional search)

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-TRX-007 |
| **Concept** | Professional service discovery (find agent, notary, architect, etc.) |
| **Business Reason** | Professional ecosystem: 27 qualification matrices, no legal document requirement |
| **Source** | INTENT_TRANSACTION_CROSSWALK.md §2 |
| **Current Limitation** | No equivalent; mapped to 'other' in V2 |
| **Proposed Target** | Add `find` to `Transaction.transaction_type`; implement professional search workflow and ServiceRequest linkage |
| **Required Fields** | `Transaction.transaction_type` includes `find` |
| **Required Documents** | None (service discovery) |
| **Qualification Impact** | 27 professional search matrices |
| **Priority** | P2 |
| **Implementation Wave** | Wave 2 — Professional Ecosystem |
| **Human Decision** | Y — find: core LAWIM feature or separate marketplace |

### 17.8 EXT-TRX-008 — service (real estate service procurement)

| Aspect | Detail |
|--------|--------|
| **Extension ID** | EXT-TRX-008 |
| **Concept** | Procurement of real estate services (estimation, expertise, photography) |
| **Business Reason** | Service marketplace: 24 matrices, linked to ServiceOrder |
| **Source** | INTENT_TRANSACTION_CROSSWALK.md §2 |
| **Current Limitation** | No equivalent; mapped to 'other' in V2 |
| **Proposed Target** | Add `service` to `Transaction.transaction_type`; implement service procurement workflow linked to ServiceOrder |
| **Required Fields** | `Transaction.transaction_type` includes `service` |
| **Required Documents** | Service order, property documents (if applicable) |
| **Qualification Impact** | 24 real estate service matrices |
| **Priority** | P2 |
| **Implementation Wave** | Wave 2 — Professional Ecosystem |
| **Human Decision** | Y — service procurement: integrated workflow or separate service ordering |

---

*End of INTENT_REQUEST_TRANSACTION_MODEL.md — 6 intent detection extensions mapped, 8 transaction type extensions mapped, 10 transaction types defined, 6 concept layers distinguished, 7-state transaction lifecycle defined.*
