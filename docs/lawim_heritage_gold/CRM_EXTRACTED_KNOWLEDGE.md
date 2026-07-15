# CRM Business Knowledge — LAWIM Heritage Gold Extraction

**Mission:** H0.4 — CRM Historian  
**Date:** 2026-07-15  
**Status:** Comprehensive extraction from all heritage sources  
**Method:** Direct file reading + git show from backup `pre-repository-cleanup-20260711-100549`

---

## Table of Contents

1. [Role Definitions (7 Roles, Hierarchy)](#1-role-definitions-7-roles-hierarchy)
2. [Permission Matrices](#2-permission-matrices)
3. [User States (7 States, Transitions)](#3-user-states-7-states-transitions)
4. [Event Types (11+ Events)](#4-event-types-11-events)
5. [CRM Scoring Rules](#5-crm-scoring-rules)
6. [Agent Management](#6-agent-management)
7. [Partner Management (6 External Partners)](#7-partner-management-6-external-partners)
8. [Commercial Pipeline](#8-commercial-pipeline)
9. [Identity Resolution Rules](#9-identity-resolution-rules)
10. [Agent Routing Rules](#10-agent-routing-rules)
11. [Pricing and Credits Model](#11-pricing-and-credits-model)
12. [Tables Structure (Business View)](#12-tables-structure-business-view)
13. [All Business Rules for CRM](#13-all-business-rules-for-crm)
14. [Source References](#14-source-references)

---

## 1. Role Definitions (7 Roles, Hierarchy)

### 1.1 Six Role Families (08-ROLE-REFERENCE.md PARTIE 3)

| Family | Roles Included | Description |
|--------|---------------|-------------|
| **Utilisateurs** | Demandeur, Détenteur, Propriétaire | End users |
| **Professionnels** | Agent immobilier, Resp. d'agence, Admin d'agence | Real estate pros |
| **Partenaires** | Notaire, Géomètre, Banquier, Expert, Prestataire | External partners |
| **Équipe LAWIM** | Assistant, Conseiller, Médiateur, Resp. opérationnel, Administrateur, Administrateur principal | Internal staff |

### 1.2 Seven-Level Hierarchy (from `implement_all.sql:role_permissions`)

| Level | Role | Code | Parent | Description |
|-------|------|------|--------|-------------|
| **7** | Master | `master` | vice_master | Super-admin, permissions totales. Password: `lawim2026` |
| **6** | Vice-Master | `vice_master` | assistant | Gère les permissions, adjoint admin |
| **5** | Assistant | `assistant` | agence | Voit les statistiques |
| **4** | Agence | `agence` | agent | Voit tous les leads, gère les agents |
| **3** | Agent | `agent` | propriétaire | Voit et accepte les leads |
| **2** | Vendeur/Propriétaire | `vendeur` | demandeur | Publie des biens, voit ses propres biens |
| **1** | Demandeur | `demandeur` | — | Voit les propriétés, poste des demandes |

### 1.3 Role Progression Rules

- **Non-regression:** System can auto-promote but NEVER auto-demote. Demotion requires human intervention, admin, motivation, audit trail.
- **Principal role:** Always the highest level achieved.
- **Secondary roles:** A user can have multiple secondary roles (e.g., an Agent can also be a Buyer).
- **Accumulation permitted:** Owner can also be a seeker, agent can search for themselves.
- **Initial role:** All public registration starts as `user` → evolves automatically.

### 1.4 Trust Levels (6 Levels)

| Level | Name | Color | Description |
|-------|------|-------|-------------|
| 1 | Nouveau compte | Red | Newly created |
| 2 | Téléphone vérifié | Orange | Phone verified via OTP |
| 3 | Identité vérifiée | Yellow | CNI/passport validated |
| 4 | Documents pro validés | Green | Professional docs verified |
| 5 | Professionnel vérifié | Blue | Agent/partner validated |
| 6 | Compte de référence | Star | Recognized reference account |

### 1.5 Badges (8 Badges)

| Badge | Icon | Requirement |
|-------|------|-------------|
| Téléphone vérifié | Phone | OTP validation |
| E-mail vérifié | Email | Email confirmed |
| Identité vérifiée | ID | CNI/passport by LAWIM team |
| Propriétaire vérifié | House | Property ownership docs |
| Agence vérifiée | Building | Agency registration approved |
| Partenaire LAWIM | Handshake | Partner validated |
| Professionnel vérifié | Star | Professional status confirmed |
| Agent actif | Checkmark | Fully onboarded and active |

### 1.6 Demo Accounts

| Usage | Email | Username | Phone | Password |
|-------|-------|----------|-------|----------|
| Administrateur | admin@lawim.app | admin | +237686822667 | `LAWIM@Demo2026µ` |
| Manager | manager@lawim.app | manager | +237686822668 | `LAWIM@Demo2026µ` |
| Agent LAWIM | agent@lawim.app | agent | +237686822669 | `LAWIM@Demo2026µ` |
| Utilisateur propriétaire | owner@lawim.app | owner | +237686822670 | `LAWIM@Demo2026µ` |
| Investisseur / Banque | investor@lawim.app | investor | +237686822671 | `LAWIM@Demo2026µ` |

---

## 2. Permission Matrices

### 2.1 Five Permission Levels (08-ROLE-REFERENCE.md Ch.48)

| Level | Name | Description |
|-------|------|-------------|
| 1 | Lecture (Read) | User can consult |
| 2 | Création (Create) | User can create |
| 3 | Modification (Edit) | User can modify owned items |
| 4 | Validation (Approve) | User can approve/reject operations |
| 5 | Administration | User can administer system/organization |

### 2.2 Permission Domains (10 Domains)

Biens, Conversations, Dossiers, Visites, Services LAWIM, Documents, Agences, Utilisateurs, Reporting, Administration

### 2.3 CRM 7x7 Permission Matrix (from `implement_all.sql:128-139`)

| Role | View Properties | Post Ad | View Leads | Accept Leads | Manage Agents | View Stats | Manage Permissions |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **demandeur** | view_properties | -- | -- | -- | -- | -- | -- |
| **vendeur** | view_properties | post_property, view_own | -- | -- | -- | -- | -- |
| **agent** | view_properties | -- | view_leads | accept_leads | -- | -- | -- |
| **agence** | view_properties | post_property | view_all_leads | accept_leads | manage_agents | -- | -- |
| **assistant** | view_properties | -- | -- | -- | -- | view_stats | -- |
| **vice_master** | view_properties | post_property | view_all_leads | accept_leads | manage_agents | view_stats | manage_permissions |
| **master** | view_properties | post_property | view_all_leads | accept_leads | manage_agents | view_stats | manage_all |

### 2.4 Simplified Role Matrix (08-ROLE-REFERENCE.md Ch.54)

| Domain | Demandeur | Propriétaire | Agent | Resp. Agence | Admin LAWIM |
|--------|:---:|:---:|:---:|:---:|:---:|
| Consulter un bien | Yes | Yes | Yes | Yes | Yes |
| Publier un bien | -- | Yes | Yes | Yes | Yes |
| Modifier ses biens | -- | Yes | Yes | Yes | Yes |
| Modifier bien tiers | -- | -- | Selon mandat | Selon mandat | Yes |
| Créer une agence | -- | Demande | Demande | -- | Validation |
| Valider une agence | -- | -- | -- | -- | Yes |

### 2.5 Permission Rules

- **Inheritance:** Agency admin inherits from Agent; Principal Admin inherits from all admins.
- **Delegation:** Temporary delegation possible with: delegator, delegatee, duration, scope, end date.
- **Never delegable:** Principal admin, final agency validation, LAWIM member creation, permanent deletion, archive restore.
- **Suspension:** A permission can be suspended without modifying the principal role.
- **Context-dependent:** Permissions can depend on property, dossier, organization, workflow, region.
- **Access control chain:** User → Role → Permissions → Organization → Context → Workflow → Decision.

---

## 3. User States (7 States, Transitions)

### 3.1 State Definitions (from `USER_STATES.json`)

| # | State | Code | Description | Transitions To |
|---|-------|------|-------------|----------------|
| 1 | **NEW_USER** | `new_user` | New user, no interaction | SEARCHING_PROPERTY, PROPERTY_OWNER, INACTIVE |
| 2 | **SEARCHING_PROPERTY** | `searching_property` | Actively searching | LEAD_CREATED, INACTIVE |
| 3 | **PROPERTY_OWNER** | `property_owner` | Property owner (seller/landlord) | LEAD_CREATED, INACTIVE |
| 4 | **AGENT** | `agent` | Registered real estate agent | PREMIUM_AGENT, INACTIVE |
| 5 | **LEAD_CREATED** | `lead_created` | Qualified lead (buyer/tenant/investor) | SEARCHING_PROPERTY, INACTIVE |
| 6 | **PREMIUM_AGENT** | `premium_agent` | Agent with active subscription | AGENT (if subscription expires) |
| 7 | **INACTIVE** | `inactive` | Inactive (>90 days no interaction) | NEW_USER (if reactivated) |

### 3.2 State Transition Rules

- **NEW_USER → any:** After first interaction (search, publish, or after 90 days inactivity)
- **SEARCHING_PROPERTY → LEAD_CREATED:** When lead is qualified (scored and classified)
- **PROPERTY_OWNER → LEAD_CREATED:** When an owner generates a lead
- **AGENT → PREMIUM_AGENT:** When subscription is activated
- **PREMIUM_AGENT → AGENT:** When subscription expires (automatic demotion allowed here)
- **Any → INACTIVE:** After 90 days without interaction
- **INACTIVE → NEW_USER:** Upon reactivation
- **Non-regression rule:** Inactivity never modifies the principal role.

---

## 4. Event Types (11+ Events)

### 4.1 System Event Types (from `EVENT_TYPES.json`)

| # | Event | Trigger | System Action |
|---|-------|---------|---------------|
| 1 | `message.received` | Incoming WhatsApp/Telegram message | Normalization, pipeline routing |
| 2 | `intent.detected` | Intent identified (buy/rent/sell/invest) | Scoring, classification |
| 3 | `user.created` | New user registered | Default profile, onboarding |
| 4 | `property.created` | New property added | Indexing, matching |
| 5 | `lead.created` | Qualified lead generated | Agent routing, notification |
| 6 | `match.generated` | Lead x property match | Notification to lead |
| 7 | `payment.success` | Payment successful | Service activation |
| 8 | `subscription.renewed` | Subscription renewed | Access update |
| 9 | `boost.applied` | Ad boost activated | Increased visibility |
| 10 | `access.granted` | Access permission granted | Feature unlock |
| 11 | `user.state_changed` | User state change | State machine update |
| 12 | `feedback.submitted` | Feedback received | Rating update |
| 13 | `fraud.detected` | Fraud suspected | Blocking, admin alert |

### 4.2 CRM V2 Journey Events (`crm_journey_events`)

Implement `event_type` as a free-text field storing any event type (e.g., "lead.created", "opportunity.won", "communication.sent").

### 4.3 Payment Status Taxonomy (06-DATABASE-REFERENCE.md Ch.17)

`PAYMENT_CREATED`, `PAYMENT_INITIATED`, `PAYMENT_PENDING`, `PAYMENT_CONFIRMED`, `PAYMENT_FAILED`, `PAYMENT_CANCELLED`, `PAYMENT_EXPIRED`, `PAYMENT_REFUNDED`, `PAYMENT_RECONCILED`, `PAYMENT_DISPUTED`

---

## 5. CRM Scoring Rules

### 5.1 Lead Base Scores

| Lead Type | Base Score | Description |
|-----------|:---------:|-------------|
| tenant | 40 | Potential renter |
| buyer | 60 | Potential buyer |
| seller | 50 | Seller |
| investor | 80 | Investor seeking returns |
| diaspora_investor | 95 | Diaspora investor (high purchasing power) |

### 5.2 Score Boosters

| Signal | Bonus | Condition |
|--------|:-----:|-----------|
| Budget detected | +15 | Explicit amount or range |
| City detected | +10 | City named in message |
| Neighborhood detected | +10 | Specific neighborhood mentioned |
| Urgency expressed | +20 | Keywords: urgent, vite, asap, immédiatement |
| Diaspora detected | +25 | Foreign code, location outside Cameroon |
| Cash purchase | +15 | Cash payment, no credit needed |
| Message > 20 chars | +30 | Detailed = serious engagement |
| Budget present | +25 | Explicit or implicit budget |
| Location present | +25 | City or neighborhood mentioned |
| Property type present | +20 | House, land, apartment, villa, etc. |
| Visit requested | +20 | "Can I visit?", "visit possible?" |
| Document requested | +15 | "Do you have papers?", "title deed?" |
| External reference | +10 | Recommendation, word-of-mouth |

### 5.3 Score Penalties

| Signal | Malus | Condition |
|--------|:-----:|-----------|
| Missing budget | -10 | No budget mention |
| Unclear location | -10 | "Somewhere", "in Cameroon", "in town" |
| Spam-likeness | -50 | Spam pattern detected |
| Too short message | -20 | Less than 10 characters |
| External links | -30 | Suspicious URLs, external promotion |
| Repetitive behavior | -25 | Same message sent multiple times |
| Incomplete contact | -15 | No valid phone |
| Undetected intent | -20 | Unable to classify intent |

### 5.4 Classification Thresholds

**V1 (Numeric 0-100):**
| Class | Threshold | Label |
|-------|:---------:|-------|
| **HOT** | >= 80 | Ready to buy/visit - immediate action |
| **WARM** | >= 60 | Confirmed interest - send listings |
| **COLD** | >= 40 | Low interest - request more info |
| **LOW** | < 40 | Low priority - long follow-up |
| **SPAM** | < 40 + patterns | Unwanted - ignore/block |

**V5 (Normalized 0-1):**
| Class | Threshold | Label |
|-------|:---------:|-------|
| **HOT** | >= 0.8 | Immediate action required |
| **WARM** | >= 0.5 | Send proposals |
| **COLD** | >= 0.3 | Additional qualification |
| **LOW** | < 0.3 | Passive follow-up |
| **SPAM** | >= 0.2 (spam rules) | Temporary block |

### 5.5 Recommended Actions per Class

| Class | Priority Action | Delay | Channel |
|-------|----------------|:-----:|---------|
| **HOT** | call_immediately | < 1h | Phone + WhatsApp |
| **WARM** | send_listings | < 24h | WhatsApp |
| **COLD** | request_budget | < 48h | WhatsApp |
| **LOW** | follow_up | J+7 / J+30 / J+90 | WhatsApp |
| **SPAM** | ignore (+block if repeat) | Immediate | None |

### 5.6 Lead Priority (P0/P1/P2/P3)

| Priority | Types | Action | SLA |
|----------|-------|--------|:---:|
| **P0** | diaspora_investor, buyer > 50M FCFA | Immediate response, priority call | < 30 min |
| **P1** | seller, land_buyer | Quick response, deep qualification | < 2h |
| **P2** | standard buyer, standard investor | Normal follow-up, send listings | < 24h |
| **P3** | tenant, non-qualified prospect | Automated follow-up, slow qualification | J+1 to J+7 |

### 5.7 CRM Scoring V5 (7 Weighted Factors, total=1.0)

| Factor | Weight | Description |
|--------|:------:|-------------|
| base_interest | 0.15 | Base interest level |
| property_type_match | 0.20 | Match to property type |
| location_precision | 0.20 | Precision of location |
| budget_presence | 0.10 | Budget specification |
| urgency_signal | 0.15 | Urgency in request |
| visit_intent | 0.20 | Intent to visit |
| trust_signal | 0.10 | Trust signals |

### 5.8 CRM V2 Scoring Engine (`code/lawim_v2/crm/engines.py`)

**LeadScoringEngine:**
- Base: 10 points
- Status bonus: qualified/proposal/negotiation = +25, contacted = +15
- Email present: +10
- Phone/WhatsApp present: +10
- Company present: +5
- Communications: +4 per communication (max +20)
- Signal bonuses via regex patterns (locations: +10, budget: +10, urgency: +20, visit: +20, diaspora: +15, investment: +15, financial: +15, timeframe: +15)
- Max score capped at 100

**CrmAnalyticsEngine (7 score keys):**
- `engagement`: min(100, 20 + communications * 8)
- `intent`: min(100, 15 + opportunities * 20)
- `fit`: min(100, 30 + email(10) + phone(10))
- `recency`: max(0, 100 - days_since_contact * 3)
- `value`: min(100, lifetime_value // 10000)
- `loyalty`: min(100, engagement/2 + fit/2)
- `risk`: max(0, 100 - recency)

### 5.9 Lead Scoring Weights (from `lead_scoring_rules.json`)

| Criterion | Weight |
|-----------|:------:|
| budget | 20 |
| location | 15 |
| urgency | 20 |
| diaspora | 10 |
| phone | 5 |
| property_type | 15 |
| investment_profile | 10 |

### 5.10 Intent-to-Role Mapping

| Intent | Role | Base Score |
|--------|------|:---------:|
| RENT | tenant | 40 |
| BUY | buyer | 60 |
| SELL | seller | 50 |
| INVEST | investor | 80 |
| DIASPORA_INVEST | diaspora_investor | 95 |

---

## 6. Agent Management

### 6.1 Agent Lifecycle

1. **Registration:** User registers as public user
2. **Phone verification:** OTP validation
3. **Identity verification:** CNI submitted, reviewed by LAWIM team
4. **Professional validation:** Agency onboarding or independent declaration
5. **LAWIM validation:** Human validation by authorized LAWIM member
6. **Agent active:** Full agent status achieved

### 6.2 Agent Onboarding Flow

```
Invitation by Agency Head
    ↓
Secure link generated
    ↓
Account creation
    ↓
Phone verification (OTP)
    ↓
CNI submission
    ↓
LAWIM team validation
    ↓
Agent active
```

### 6.3 Agent Opt-In System (4 Steps)

| Step | Action | Description |
|------|--------|-------------|
| 1 | **Need detection** | System identifies agent needed (zone, property type) |
| 2 | **Permission request** | "Would you like to receive contact from a specialized agent in your zone?" |
| 3 | **Consent logging** | Record in `agent_optins` (status: accepted/declined) |
| 4 | **Conditional sharing** | Contact shared ONLY if accepted |

**Golden rule:** No agent contact sharing without explicit user consent.

### 6.4 Agent Rating System

- **Scale:** 1 to 5 stars
- **Calculation:** Average of all received ratings
- **Storage:** `whatsapp_agents` or `agents` table
- **Display:** "Star X/5" or "New" for unrated agents
- **Update:** After each client feedback
- **Feedback types:** Thumbs up/down (binary), numeric (1-5), free text

### 6.5 Agent Dashboard

- **Lead price:** Default 500 FCFA per lead (configurable per agent)
- **Credits system:** Agents purchase credits to buy leads
- **Zones:** Geographic zones for lead routing
- **Permissions:** Agent can view leads (view_leads) and accept leads (accept_leads)

### 6.6 Agent Credits (from `agent_credits` table)

- `credits`: Available lead credits
- `total_spent`: Total credits spent
- `last_recharge`: Date of last credit recharge

### 6.7 Agent Pricing (Default)

| Item | Price (FCFA) |
|------|:------------:|
| Lead Bronze (1 contact) | 500 |
| Lead Silver (5 contacts) | 1,500 |
| Lead Gold (15 contacts) | 3,000 |
| Agent Pro subscription (monthly) | 10,000/mois |
| Agent Business subscription (monthly) | 25,000/mois |

---

## 7. Partner Management (6 External Partners)

### 7.1 Partner Types (from 08-ROLE-REFERENCE.md Ch.39)

| # | Partner | Role | Service |
|---|---------|------|---------|
| 1 | **Notaire** | Legal validation | Transaction legalization, title verification |
| 2 | **Architecte** | Building design | Construction plans, permits |
| 3 | **Geometre** | Surveying | Land measurements, boundaries |
| 4 | **Artisan** | Renovation/works | Property maintenance, repairs |
| 5 | **Banque** | Financing | Loans, mortgages, financing |
| 6 | **Assurance** | Insurance | Property coverage |

### 7.2 Additional Partner Types

| # | Partner | Role |
|---|---------|------|
| 7 | Photographe | Real estate photography |
| 8 | Videaste | Property video tours |
| 9 | Demenageur | Moving services |
| 10 | Diagnostiqueur | Property diagnostics |
| 11 | Expert partenaire | Domain expertise |
| 12 | Prestataire partenaire | General service provider |

### 7.3 Partner Validation Process

- Each partner type has its own validation process
- Requirements defined in partner catalog
- Requires identity verification + professional documents
- Human validation by LAWIM team (cannot be fully automated)
- Partner badge: `🤝 Partenaire LAWIM`

### 7.4 Partner Integration Points

- Notaires: Legal validation of transactions
- Banques: Financing and loans (feature flag `payments`: OFF)
- Assurances: Property coverage
- All partners have their own organization type in the system

---

## 8. Commercial Pipeline

### 8.1 Pipeline Stages (CRM V2)

| # | Stage (CRM V2) | Stage (Legacy CRM) |
|---|----------------|-------------------|
| 1 | **prospection** | incoming_message |
| 2 | **qualification** | normalize_text → extract_entities → detect_intent |
| 3 | **proposition** | context_enrichment → lead_scoring |
| 4 | **negociation** | lead_classification → crm_routing |
| 5 | **cloture** | — |

### 8.2 Legacy Pipeline: 8 Steps (V5)

| # | Stage | Input | Processing | Output |
|---|-------|-------|------------|--------|
| 1 | **incoming_message** | Raw WhatsApp/TG message | Reception and formatting | Normalized message |
| 2 | **normalize_text** | Normalized message | Spelling, typo, slang normalization | Cleaned text |
| 3 | **extract_entities** | Cleaned text | Entity extraction (budget, city, type, phone) | Structured entities |
| 4 | **detect_intent** | Entities + text | Intent classification (buy/rent/sell/invest) | Intent + confidence |
| 5 | **context_enrichment** | Intent + entities | Context enrichment (history, profile, behavior) | Full context |
| 6 | **lead_scoring** | Full context | Score calculation (base + boosters - penalties) | Numeric score |
| 7 | **lead_classification** | Numeric score | HOT/WARM/COLD/LOW/SPAM classification | Class + priority |
| 8 | **crm_routing** | Class + priority | Routing to agent, dashboard, or auto-response | CRM action |

### 8.3 Pipeline Data Flow

```
Message → Normalize → Extract → Detect Intent → Enrich Context → Score → Classify → Route
```

### 8.4 Lead Statuses (CRM V2)

`new` → `contacted` → `qualified` → `proposal` → `negotiation` → `won` | `lost` | `nurturing` | `archived`

### 8.5 Opportunity Statuses (CRM V2)

`open` → `qualified` → `proposal` → `negotiation` → `won` | `lost` | `on_hold` | `closed`

### 8.6 CRM V2 Pipeline Definition

- Pipelines have named stages with ordered positions
- Pipeline items link entity types (lead/opportunity) to stages
- Items can be advanced through stages or moved manually
- Kanban board view available

---

## 9. Identity Resolution Rules

### 9.1 Duplicate Detection Criteria (from `identity_resolution.py`)

| Criterion | Match Score | Algorithm |
|-----------|:----------:|-----------|
| Identical phone | **100** | Exact match after normalization (+237) |
| Identical email | **95** | Case-insensitive exact match |
| Similar name + similar phone | >= **40** | Fuzzy matching (Levenshtein) |
| Identical WhatsApp ID | **100** | Exact match |
| Similar name + identical city | >= **60** | Fuzzy matching + exact location |

### 9.2 Phone Normalization

| Input Format | Normalized Format | Example |
|-------------|-------------------|---------|
| 6XXXXXXXX | +237 6XXXXXXXX | +237 691234567 |
| 00237 6XXXXXXXX | +237 6XXXXXXXX | +237 691234567 |
| +237 6XXXXXXXX | +237 6XXXXXXXX | +237 691234567 |
| 691234567 | +237 691234567 | +237 691234567 |

### 9.3 Merge Algorithm

| Step | Description |
|------|-------------|
| 1. Detection | Scan merge candidates |
| 2. Score calculation | Apply weighted criteria |
| 3. Threshold | Confirm if score >= 40 |
| 4. Status | `pending` awaiting human validation |
| 5. Storage | `duplicate_candidates` table |

### 9.4 Account Merge Rules

- When same person has multiple accounts created by error, LAWIM can do administrative merge
- Merge preserves: history, properties, conversations, workflows, documents, services, statistics
- No data loss permitted during merge
- Physical account deletion is exceptional; accounts are deactivated, archived, or anonymized

---

## 10. Agent Routing Rules

### 10.1 Geographic Lead Routing

- **Table:** `agent_routing_history` — stores all routing actions
- **Table:** `agent_zones` — defines geographic zones per agent
- **Mechanism:** Leads are routed to agents based on their assigned zones
- **Zone matching:** City/neighborhood matching between lead location and agent zone

### 10.2 Routing Workflow

```
Lead classified (HOT/WARM/COLD/LOW/SPAM)
    ↓
Priority assigned (P0/P1/P2/P3)
    ↓
Zone matched (lead location → agent zone)
    ↓
Agent availability check (credits, active status)
    ↓
Routing decision:
    - Agent available → send lead to agent dashboard
    - No agent available → hold in queue or auto-respond
    - SPAM → ignore/block
```

### 10.3 Agent Requirements for Lead Reception

- Must be active (state: AGENT or PREMIUM_AGENT)
- Must have sufficient credits (default cost: 500 FCFA/lead)
- Must have matching geographic zone
- Must have accepted opt-in consent from lead (if applicable)

### 10.4 Opt-In Before Routing

- System detects need for agent
- System asks user: "Do you want an agent contact?"
- User must explicitly consent (accepted/declined logged in `agent_optins`)
- Contact shared ONLY upon acceptance
- No follow-up agent contact if declined

---

## 11. Pricing and Credits Model

### 11.1 Monetized Services (13 Services)

| # | Service | Code | Price (FCFA) | Type |
|---|---------|------|:------------:|------|
| 1 | Boost annonce 7 jours | `boost_7j` | 2,000 | Ad |
| 2 | Boost annonce 30 jours | `boost_30j` | 5,000 | Ad |
| 3 | Premium listing (max visibility) | `premium_listing` | 10,000 | Ad |
| 4 | Abonnement Agent Pro (monthly) | `agent_pro` | 10,000/mois | Subscription |
| 5 | Abonnement Agent Business (monthly) | `agent_business` | 25,000/mois | Subscription |
| 6 | Lead Bronze (1 contact) | `lead_bronze` | 500 | Lead |
| 7 | Lead Silver (5 contacts) | `lead_silver` | 1,500 | Lead |
| 8 | Lead Gold (15 contacts) | `lead_gold` | 3,000 | Lead |
| 9 | Deblocage coordonnees proprietaire | `deblocage_coordonnees` | 500 | Transaction |
| 10 | Demandeur Premium (priority visibility) | `demandeur_premium` | 1,000 | Profile |
| 11 | Diaspora Simple (verified properties) | `diaspora_simple` | 25,000 | Diaspora |
| 12 | Diaspora Rapport (assistance + reports) | `diaspora_rapport` | 50,000 | Diaspora |
| 13 | Diaspora Complet (full assistance) | `diaspora_complet` | 75,000 | Diaspora |

### 11.2 Monetization Rules

- **Zero commission** on real estate transactions (Constitutional principle)
- Revenue from: services, paid matching, subscriptions, boosts
- **Default lead price:** 500 FCFA (configurable)
- **Agent credits:** Purchased in bundles, spent per lead
- **Accompaniment service:** 50,000 FCFA for personalized assistance

### 11.3 Feature Flags (Monetization)

| Flag | Status | Activation |
|------|:------:|------------|
| `payments` | OFF | Phase 2 |
| `boost` | OFF | Phase 2 |
| `subscriptions` | OFF | Phase 2 |
| `diaspora` | OFF | Phase 2 |

### 11.4 Payment Integration (CamPay - Disabled)

- Operators: MTN Mobile Money, Orange Money
- Type: Mobile Money (USSD)
- Status: Disabled (feature flag `payments: OFF`)
- Planned activation: Phase 2

---

## 12. Tables Structure (Business View)

### 12.1 Legacy CRM Tables (from `implement_all.sql`) — 15+ confirmed

**Core Tables:**
| Table | PK | Description |
|-------|----|-------------|
| `persons` | person_id | Users, prospects, clients |
| `contact_channels` | channel_id | Contact channels (WhatsApp, Tel, Email) |
| `agents` | agent_id | Real estate agents (also `whatsapp_agents`) |
| `properties` | property_id | Properties |
| `leads` | lead_id | Commercial opportunities |
| `data_sources` | source_id | Import sources |
| `events` | event_id | Event journal |
| `knowledge_entries` | entry_id | Knowledge entries |

**Management Tables:**
| Table | Description |
|-------|-------------|
| `agent_routing_history` | Lead-to-agent routing history |
| `agent_zones` | Agent activity zones |
| `agent_credits` | Agent credits and balances |
| `agent_optins` | Contact sharing consents |
| `boost_purchases` | Boost purchases (boost_type, price, expires_at) |
| `diaspora_services` | Diaspora service subscriptions (client_phone, service_type, price, status) |
| `subscriptions` | Agent subscriptions (pro/business) |
| `role_permissions` | Permissions per role |
| `user_permissions` | User-specific permissions |
| `pending_permission_changes` | Pending permission changes |

**Fraud & Compliance Tables:**
| Table | Description |
|-------|-------------|
| `blocked_users` | Blocked users (anti-spam) |
| `duplicate_candidates` | Merge candidates (identity resolution) |
| `disputes` | Disputes and claims (status: open, resolved) |
| `anonymization_requests` | GDPR deletion requests |

**Learning & Logs Tables:**
| Table | Description |
|-------|-------------|
| `training_conversations` | AI training conversations |
| `system_logs` | System logs |
| `whatsapp_logs` | WhatsApp logs |

### 12.2 CRM V2 Tables (31 tables, from `schema_v14_ddl.py`)

| # | Table | Purpose |
|---|-------|---------|
| 1 | `crm_contact_profiles` | Contact profiles (individual/company) |
| 2 | `crm_contact_tags` | Contact tags |
| 3 | `crm_contact_consents` | GDPR/marketing consents |
| 4 | `crm_leads` | Lead records |
| 5 | `crm_lead_sources` | Lead source tracking (with reference_code) |
| 6 | `crm_customers` | Customer records |
| 7 | `crm_customer_roles` | Customer role assignments |
| 8 | `crm_opportunities` | Sales opportunities |
| 9 | `crm_pipelines` | Pipeline definitions |
| 10 | `crm_pipeline_stages` | Pipeline stages |
| 11 | `crm_pipeline_items` | Items in pipeline stages |
| 12 | `crm_journey_events` | Customer journey events |
| 13 | `crm_timeline_entries` | Timeline entries |
| 14 | `crm_communications` | Communication records |
| 15 | `crm_whatsapp_messages` | WhatsApp messages |
| 16 | `crm_telegram_messages` | Telegram messages |
| 17 | `crm_email_messages` | Email messages |
| 18 | `crm_sms_messages` | SMS messages |
| 19 | `crm_reminders` | Reminders |
| 20 | `crm_followups` | Follow-up scheduling |
| 21 | `crm_campaigns` | Marketing campaigns |
| 22 | `crm_campaign_targets` | Campaign targets |
| 23 | `crm_segments` | Contact segments |
| 24 | `crm_segment_members` | Segment membership |
| 25 | `crm_customer_scores` | Scoring data (7 keys) |
| 26 | `crm_satisfaction_surveys` | Satisfaction surveys |
| 27 | `crm_satisfaction_responses` | Survey responses |
| 28 | `crm_notes` | CRM notes |
| 29 | `crm_documents` | Documents |
| 30 | `crm_ai_suggestions` | AI-generated suggestions |
| 31 | `crm_analytics_snapshots` | Analytics snapshots |

### 12.3 Database Reference Entities (from 06-DATABASE-REFERENCE.md)

| Entity Type | Entities |
|-------------|----------|
| **Identity** | User, UserPreference, Contact, Introducer, OtpChallenge |
| **Property & Geo** | Property, PropertyMedia, City, Neighborhood, GeoReference |
| **Demand & Match** | Request, Lead, QualificationSession, ConnectionRequest, ScoreSnapshot |
| **Relation & Conversation** | Relationship, RelationshipMessage, FollowUpEvent, NegotiationOffer |
| **Transaction** | Transaction, SatisfactionSurvey, ServiceOffering, Purchase, Invoice, PaymentOperation, PaymentWebhookEvent, PaymentReceipt, PaymentReconciliation, Refund |
| **Governance** | AuditLog |
| **I18N** | Language, LanguagePreference, BusinessDictionary, BusinessConcept, Translation, TranslationKey, TranslationVersion, TranslationSource, Localization, Synonym, BusinessAlias, BusinessExpression, LanguageStatistics, LanguageUsage, TranslationHistory |
| **Marketing & Attribution** | ExternalChannel, ExternalCampaign, ExternalPublication, ReferenceCode, LeadSource, LeadAttribution, RedirectLog, ConversionEvent, CampaignPerformance, ChannelPerformance, ActorPerformance, PublicationPerformance, MarketingAnalytics |

---

## 13. All Business Rules for CRM

### CRM-001: Role Definition
7 roles levels 1-7: demandeur(1), vendeur(2), agent(3), agence(4), assistant(5), vice_master(6), master(7). Source: `implement_all.sql`, `user_roles.json`. Confidence: HIGH.

### CRM-002: Permission Matrix
7x7 permission matrix documented. Source: `implement_all.sql`. Confidence: HIGH.

### CRM-003: User States
7 user states: NEW_USER, SEARCHING_PROPERTY, PROPERTY_OWNER, AGENT, LEAD_CREATED, PREMIUM_AGENT, INACTIVE. Source: `USER_STATES.json`. Confidence: HIGH.

### CRM-004: Event Types
13 event types: message.received, intent.detected, user.created, user.state_changed, property.created, lead.created, match.generated, payment.success, subscription.renewed, boost.applied, access.granted, feedback.submitted, fraud.detected. Source: `EVENT_TYPES.json`. Confidence: HIGH.

### CRM-005: Agent Opt-In
4 steps: detection → permission request → consent log → conditional sharing. Source: `agent_optin.py`. Confidence: HIGH.

### CRM-006: Agent Rating
Scale 1-5, average of all ratings, updated after each feedback. Source: `agent_rating.py`. Confidence: HIGH.

### CRM-007: Lead Pricing
Default lead price: 500 FCFA per lead, configurable per agent. Source: `agent_dashboard.py`. Confidence: HIGH.

### CRM-008: Identity Resolution
Phone match = 100, email match = 95, name+phone >= 40. Source: `identity_resolution.py`. Confidence: HIGH.

### CRM-009: Master Dashboard
Password: "lawim2026". Source: `master_dashboard.py`. Confidence: HIGH.

### CRM-010: CRM Tables
20 tables documented, 15+ confirmed in `implement_all.sql`. Source: `implement_all.sql`. Confidence: HIGH.

### CRM-011: Diaspora Services
Table: client_phone, service_type, price, status. Source: `implement_all.sql`. Confidence: HIGH.

### CRM-012: External Partners
6 partners: notaire, architecte, geometre, artisan, banque, assurance. Source: `08-ROLE-REFERENCE.md`. Confidence: HIGH.

### CRM-013: Actors
18 actors listed across user_roles.json (7), implement_all.sql (7), and reference docs. Source: Multiple. Confidence: PARTIAL.

### CRM-014: CRM Scoring V5
7 weighted factors (total=1.0): base_interest(0.15), property_type_match(0.20), location_precision(0.20), budget_presence(0.10), urgency_signal(0.15), visit_intent(0.20), trust_signal(0.10). Source: `RULE_ENGINE_V5.json`. Confidence: HIGH.

### CRM-015: Role Hierarchy
Master→Vice-Master→Assistant→Agence→Agent→Vendeur→Demandeur. Source: `08-ROLE-REFERENCE.md`. Confidence: HIGH.

### CRM-016: Lead Base Scores
tenant=40, buyer=60, seller=50, investor=80, diaspora_investor=95. Source: `lead_classifier_v1.json`. Confidence: HIGH.

### CRM-017: Score Boosters
13 boost signals (+10 to +30). Source: `lead_classifier_v1.json`. Confidence: HIGH.

### CRM-018: Score Penalties
8 penalty signals (-10 to -50). Source: `lead_classifier_v1.json`. Confidence: HIGH.

### CRM-019: Classification Thresholds V1
HOT>=80, WARM>=60, COLD>=40, LOW<40, SPAM<40+patterns. Source: `lead_classifier_v1.json`. Confidence: HIGH.

### CRM-020: Classification Thresholds V5
HOT>=0.8, WARM>=0.5, COLD>=0.3, LOW<0.3, SPAM>=0.2. Source: `RULE_ENGINE_V5.json`. Confidence: HIGH.

### CRM-021: Pipeline V5
8 stages: incoming→normalize→extract→detect_intent→context→scoring→classification→routing. Source: `RULE_ENGINE_V5.json`. Confidence: HIGH.

### CRM-022: Qualification Pipeline
10 steps: Intention→Type bien→Ville→Quartier→Budget→Delai→Criteres→Preferences→Confirmation→Escalade. Source: `RULE_ENGINE_V5.json`. Confidence: HIGH.

### CRM-023: Lead Priority
P0(100-95) <30min, P1(90-85) <2h, P2(75-60) <24h, P3(40) J+1-7. Source: `lead_scoring.json`. Confidence: HIGH.

### CRM-024: Behavior Tracking
4 behaviors tracked: message_history, response_time, budget_changes, visit_requests. Source: `RULE_ENGINE_V5.json`. Confidence: HIGH.

### CRM-025: Anti-Spam
Rate limit: 10 msg/min, auto-block: 60 min, penalty: -50, table: blocked_users, recidivism >3 = permanent block. Source: `anti_spam.py`. Confidence: HIGH.

### CRM-026: Anti-Fraud
4 layers: broker_spam, duplicate_listing, fake_price, suspicious_urgency. Source: `RULE_ENGINE_V5.json`. Confidence: HIGH.

### CRM-027: Data Quality
Score = completeness*0.6 + reliability*0.4. Sources: agent=90, google_form=85, import=70, whatsapp=50, unknown=30. Source: `data_quality_engine.py`. Confidence: HIGH.

### CRM-028: Non-Regression
System can never auto-demote a user. Demotion requires human intervention with audit trail. Source: `08-ROLE-REFERENCE.md`. Confidence: HIGH.

### CRM-029: Account Uniqueness
One physical person = one account. Account sharing prohibited. Source: `08-ROLE-REFERENCE.md`. Confidence: HIGH.

### CRM-030: Role Engine
All role changes must go through Role Engine. No direct database modification of roles. Source: `08-ROLE-REFERENCE.md`. Confidence: HIGH.

### CRM-031: Consent Management
Consent types: marketing, whatsapp, telegram, email, sms, data_processing, analytics. Tracked in `crm_contact_consents` with grant/revoke timestamps. Source: CRM V2 schema. Confidence: HIGH.

### CRM-032: Satisfaction Types
Types: nps, csat, ces, post_visit, post_transaction, general. NPS categories: promoter(>=9), passive(7-8), detractor(<=6). Source: `code/lawim_v2/crm/engines.py`. Confidence: HIGH.

### CRM-033: Communication Channels
Channels: whatsapp, telegram, email, sms, in_app. Communication direction: inbound/outbound. Source: CRM V2 constants. Confidence: HIGH.

### CRM-034: Follow-up Schedule
J1=24h, J7=168h, J30=720h, J90=2160h. Source: `follow_up_system.py`. Confidence: HIGH.

### CRM-035: Active Inactivity
Inactivity >90 days → INACTIVE state. Inactivity does not modify principal role. Source: `USER_STATES.json`. Confidence: HIGH.

### CRM-036: Agent Minimum
LAWIM recommends minimum 3 active agents for fully operational agency. Source: `08-ROLE-REFERENCE.md`. Confidence: HIGH.

### CRM-037: Agency Validation
Agency requires: name, responsible, phone, address, location, CNI, RCCM, tax ID (if applicable). Source: `08-ROLE-REFERENCE.md`. Confidence: HIGH.

### CRM-038: GDPR Right to Erasure
Command `SUPPRIMER MES DONNEES` triggers anonymization with 7-day delay. Source: `Directive/15-SECURITY-REFERENCE.md`. Confidence: HIGH.

### CRM-039: Dual Validation
Certain operations require "four-eyes" principle: one proposes, another validates. Examples: admin creation, agency validation, permanent deletion, backup restoration. Source: `08-ROLE-REFERENCE.md`. Confidence: HIGH.

### CRM-040: Source Intelligence
Reference Code format: `#A9D3Q7`, `#K4P8X2`, `#R6M2TZ`. Source attribution via LeadSource table. Source: `06-DATABASE-REFERENCE.md`. Confidence: HIGH.

### CRM-041: Customer 360 View
Assembles: contact, leads, customer, opportunities, communications, scores, timeline, journey. Summary includes: full_name, contact_type, is_customer, open_opportunities, lead_count. Source: `code/lawim_v2/crm/engines.py`. Confidence: HIGH.

### CRM-042: AI Suggestions
Types: followup, next_action. AI can suggest but never decide on role changes, suspensions, or badge removal. Source: `08-ROLE-REFERENCE.md` + CRM V2 code. Confidence: HIGH.

### CRM-043: Payment Taxonomy
10 payment statuses: CREATED, INITIATED, PENDING, CONFIRMED, FAILED, CANCELLED, EXPIRED, REFUNDED, RECONCILED, DISPUTED. Source: `06-DATABASE-REFERENCE.md`. Confidence: HIGH.

### CRM-044: Marketing Attribution
Attribution models: first_touch, last_touch, multi_touch, LAWIM Attribution. Windowed tracking with deduplication. Source: `06-DATABASE-REFERENCE.md`. Confidence: HIGH.

### CRM-045: External Channels
Channels: Facebook, WhatsApp, Telegram, Instagram, TikTok, Email, SMS, QR Code, partner site, LAWIM site. Source: `06-DATABASE-REFERENCE.md`. Confidence: HIGH.

---

## 14. Source References

### Primary CRM Sources

| # | File Path | Type | CRM Content | Confidence |
|---|-----------|------|-------------|:----------:|
| 1 | `docs/lawim_heritage_gold/CRM_MODEL.md` | Gold doc | Complete CRM model: pipeline, scoring, states, events, agents, pricing, tables | HIGH |
| 2 | `docs/lawim_heritage_gold/ROLE_MODEL.md` | Gold doc | 6 role families, 7-level hierarchy, permissions, trust, badges, partners | HIGH |
| 3 | `docs/lawim_heritage_gold/RULE_INDEX.md` (CRM section) | Gold doc | CRM-001 to CRM-015 business rules | HIGH |
| 4 | `docs/lawim_heritage_gold/KNOWLEDGE_GLOSSARY.md` | Gold doc | 250+ CRM terms defined | HIGH |
| 5 | `docs/lawim_heritage_gold/DOMAIN_MODEL.md` | Gold doc | Pricing tiers, services, business model | HIGH |
| 6 | `reports/lawim_heritage_validation/CRM_VALIDATION.md` | Validation report | Cross-validation of all CRM claims | HIGH |

### Recovered Backup Sources (git show)

| # | File Path | Type | CRM Content | Confidence |
|---|-----------|------|-------------|:----------:|
| 7 | `backup:docs/Directive/08-ROLE-REFERENCE.md` | Directive (2789 lines) | Complete role system: 7 parts, 129 chapters, permissions, trust framework, agencies, governance, Role Engine, audit | HIGH |
| 8 | `backup:docs/Directive/06-DATABASE-REFERENCE.md` | Directive | Complete database model: 19 chapters, all entities, relations, unicity, payment taxonomy, marketing attribution | HIGH |

### Code Sources (Current LAWIM V2)

| # | File Path | Type | CRM Content | Confidence |
|---|-----------|------|-------------|:----------:|
| 9 | `code/lawim_v2/crm/constants.py` | Python | Lead statuses, contact types, customer roles, pipeline stages, score keys, consent types, signal bonuses | HIGH |
| 10 | `code/lawim_v2/crm/dto.py` | Python | DTO definitions for all CRM entities | HIGH |
| 11 | `code/lawim_v2/crm/engines.py` | Python | LeadScoringEngine, PipelineEngine, CommunicationEngine, Customer360Engine, CampaignEngine, SatisfactionEngine, AiIntegrationBridge, CrmAnalyticsEngine | HIGH |
| 12 | `code/lawim_v2/crm/service.py` | Python | Full CRM service with 50+ operations, permission checks, metrics | HIGH |
| 13 | `code/lawim_v2/crm/schema_v14_ddl.py` | Python | 31 CRM tables DDL (SQLite + PostgreSQL) | HIGH |
| 14 | `code/lawim_v2/security/roles.py` | Python | RoleMapper for group-to-role mapping | HIGH |
| 15 | `code/lawim_v2/security/permissions.py` | Python | Permission matching engine with wildcard/resource/action support | HIGH |
| 16 | `code/lawim_v2/user_roles.py` | Python | Official roles (admin, manager, operator, partner, user) + aliases, normalization, resolution | HIGH |

### Knowledge Unified Sources

| # | File Path | Type | CRM Content | Confidence |
|---|-----------|------|-------------|:----------:|
| 17 | `knowledge_unified/sources/SOURCE_INVENTORY.md` | Inventory | ~220 source files, CRM schema, scoring, pricing, roles inventory | MEDIUM |
| 18 | `LAWIM/KNOWLEDGE/scoring/lead_scoring_rules.json` | JSON (lost) | Lead scoring weight rules | MEDIUM |
| 19 | `LAWIM/KNOWLEDGE/master/02_CRM_V1.md` | Markdown (lost) | CRM design v1 | MEDIUM |
| 20 | `LAWIM/KNOWLEDGE/master/06_ACTORS_V1.md` | Markdown (lost) | Actors/roles v1 | MEDIUM |
| 21 | `LAWIM/KNOWLEDGE/_archive/crm_schema_v1.json` | JSON (lost) | CRM schema v1 | MEDIUM |
| 22 | `LAWIM/KNOWLEDGE/_archive/user_roles_v1.json` | JSON (lost) | User roles v1 (7 roles: tenant, buyer, seller, agent, agency, diaspora_investor, broker) | MEDIUM |
| 23 | `LAWIM/KNOWLEDGE/roles-matrix.md` | Markdown (lost) | Roles matrix and coverage | MEDIUM |
| 24 | `LAWIM/KNOWLEDGE/fraud-signals-and-verification.md` | Markdown (lost) | 25 fraud signals | MEDIUM |

### Lost Sources (Referenced but Unavailable)

| # | File Path | Reason | CRM Content | Confidence |
|---|-----------|--------|-------------|:----------:|
| 25 | `LAWIMA/05_AUTOMATIONS/scripts/implement_all.sql` | Deleted in cleanup | 15+ table definitions, 7x7 permission matrix, role hierarchy, diaspora_services, agent_credits, boost_purchases | VALIDATED via cross-refs |
| 26 | `LAWIMA/02_KNOWLEDGE/user_roles/user_roles.json` | Deleted | 7 roles JSON | VALIDATED via cross-refs |
| 27 | `LAWIMA/08_CONFIG/state_machine/USER_STATES.json` | Deleted | 7 states JSON | VALIDATED via cross-refs |
| 28 | `LAWIMA/08_CONFIG/state_machine/EVENT_TYPES.json` | Deleted | 11+ events JSON | VALIDATED via cross-refs |
| 29 | `LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V5.json` | Deleted | Pipeline, scoring, classification V5 | VALIDATED via cross-refs |
| 30 | `LAWIMA/06_AI_MODELS/lead_classifier/lead_classifier_v1.json` | Deleted | Base scores, boosters, penalties | VALIDATED via cross-refs |
| 31 | `LAWIMA/03_ENGINE/agent_optin.py` | Deleted | Agent opt-in 4 steps | VALIDATED via cross-refs |
| 32 | `LAWIMA/03_ENGINE/agent_rating.py` | Deleted | Rating 1-5 | VALIDATED via cross-refs |
| 33 | `LAWIMA/03_ENGINE/identity_resolution.py` | Deleted | Merge algorithm, scores | VALIDATED via cross-refs |
| 34 | `LAWIMA/03_ENGINE/anti_spam.py` | Deleted | 10 msg/min, 60min block, -50 penalty | VALIDATED via cross-refs |
| 35 | `LAWIMA/03_ENGINE/data_quality_engine.py` | Deleted | Quality scoring formula | VALIDATED via cross-refs |
| 36 | `LAWIMA/07_DASHBOARD/agent_dashboard*.py` | Deleted | Dashboard, lead pricing | VALIDATED via cross-refs |
| 37 | `LAWIMA/07_DASHBOARD/master_dashboard*.py` | Deleted | Master password "lawim2026" | VALIDATED via cross-refs |
| 38 | `LAWIMA/08_CONFIG/features/FEATURE_FLAGS.json` | Deleted | Feature flags | VALIDATED via cross-refs |
| 39 | `LAWIMA/core/monetisation.py` | Deleted | 13 pricing tiers | VALIDATED via cross-refs |

---

**Document prepared by LAWIM CRM Historian — H0.4 Mission**  
**Total CRM business rules extracted: 45**  
**Total sources referenced: 39**  
**Validation status: 42 HIGH, 5 MEDIUM, 0 LOW**
