# QUALIFICATION HERITAGE EXTRACTION — Qualification Historian Report H0.4

**Mission:** LAWIM Heritage Completion Mission H0.4
**Date:** 2026-07-15
**Statut:** Extraction exhaustive de toutes les sources patrimoniales
**Principe:** Connaissances métier uniquement (pas d'implémentation)

---

## TABLE OF CONTENTS

1. [Lead Profiles and Base Scores](#1-lead-profiles-and-base-scores)
2. [Qualification Pipeline](#2-qualification-pipeline)
3. [Scoring Rules (V1 and V5)](#3-scoring-rules)
4. [Boosters and Penalties](#4-boosters-and-penalties)
5. [Thresholds (Classifications HOT/WARM/COLD/LOW/SPAM)](#5-thresholds)
6. [Criteria and Questions Flow](#6-criteria-and-questions-flow)
7. [Minimum Requirements](#7-minimum-requirements)
8. [Exception Rules](#8-exception-rules)
9. [Priority Rules](#9-priority-rules)
10. [Diaspora Detection Rules](#10-diaspora-detection-rules)
11. [User Typologies](#11-user-typologies)
12. [Business Rules for Qualification](#12-business-rules-for-qualification)
13. [Source References](#13-source-references)

---

## 1. LEAD PROFILES AND BASE SCORES

### 1.1 Role-Based Base Scores (V1 Lead Classifier)

These are the canonical role-based scores defined in the gold standard model.

| Role | Base Score | Description | Intent Mapping |
|------|:----------:|-------------|----------------|
| tenant | **40** | Locataire potentiel | RENT_PROPERTY |
| buyer | **60** | Acheteur potentiel | BUY_PROPERTY |
| seller | **50** | Vendeur | SELL_PROPERTY |
| investor | **80** | Investisseur | INVESTOR_INTENT |
| diaspora_investor | **95** | Investisseur diaspora | INVESTOR_INTENT (diaspora detected) |

### 1.2 Intent-to-Role Mapping

| Intent | Target Role(s) |
|--------|----------------|
| `RENT_PROPERTY` | tenant |
| `BUY_PROPERTY` | buyer |
| `SELL_PROPERTY` | seller |
| `INVESTOR_INTENT` | investor, diaspora_investor |

### 1.3 Intent Lead Score Weights (Alternative Scoring System)

From `intentions.json` and `scoring_rules.json` — used for V5 intent-based scoring:

| Intent | Lead Score Weight | Priority | Budget Type |
|--------|:-----------------:|----------|-------------|
| BUY_PROPERTY | 50 | VERY_HIGH | global_price |
| RENT_PROPERTY | 30 | HIGH | monthly_rent |
| SELL_PROPERTY | 60 | VERY_HIGH | asking_price |
| INVESTOR_INTENT | 100 | P0 | (various) |
| SEARCH_PROPERTY | 25 | NORMAL | (none) |

### 1.4 Additional Types (V3 Extension)

From `RULE_ENGINE_V3.json` (QUAL-019):
- property_seeker
- agent
- owner
- broker

---

## 2. QUALIFICATION PIPELINE

### 2.1 V5 Pipeline — 8 Sequential Steps

| Step | Input | Output | Description |
|:----:|-------|--------|-------------|
| 1 | `incoming_message` | `normalize_text` | Cleaning, normalization, preparation of raw message |
| 2 | `normalize_text` | `extract_entities` | Entity extraction (city, neighborhood, budget, property type) |
| 3 | `extract_entities` | `detect_intent` | Intent detection (RENT/BUY/SELL/INVESTOR) |
| 4 | `detect_intent` | `context_enrichment` | Context enrichment (history, preferences, long-term memory) |
| 5 | `context_enrichment` | `lead_scoring` | Composite lead score calculation |
| 6 | `lead_scoring` | `lead_classification` | Classification (HOT/WARM/COLD/SPAM) |
| 7 | `lead_classification` | `crm_routing` | CRM routing (agent, queue, priority) |
| 8 | `crm_routing` | `response` | Final response generation |

### 2.2 Qualification Order — 10 Strict Steps

The strict qualification order to be respected in all conversations:

| Order | Step | Channel | Description |
|:-----:|------|---------|-------------|
| 1 | **Intention** | All | Determine need: rent, buy, sell, invest |
| 2 | **Type de bien** | All | Studio, apartment, house, villa, duplex, land, commercial |
| 3 | **Ville** | All | Main location |
| 4 | **Quartier** | WhatsApp/Telegram | Preferred neighborhood or zone |
| 5 | **Budget** | All | Maximum budget (buy) or monthly (rent) |
| 6 | **Délai** | All | Time horizon: urgent, 1 month, 3 months, no deadline |
| 7 | **Critères** | All | Surface, rooms, floor, parking, furnished, etc. |
| 8 | **Préférences** | WhatsApp/Telegram | Additional preferences (floor, exposure, standing) |
| 9 | **Confirmation** | All | Summary and validation of collected information |
| 10 | **Escalade** | All | Decision: results, appointments, human transfer |

### 2.3 Qualification Statuses

| Status | Meaning |
|--------|---------|
| `MISSING_CORE_FIELDS` | Core fields not yet collected |
| `DRAFT_CREATED` | Request draft created, qualification in progress |
| `QUALIFIED` | All required fields collected |
| `MATCH_READY` | Ready for matching engine |
| `WAITLISTED` | City not covered or no active inventory |
| `NO_ACTIVE_MATCH` | No active matches found |

### 2.4 Status Transitions (per property search type)

`MISSING_CORE_FIELDS` → `DRAFT_CREATED` → `QUALIFIED` → `MATCH_READY`

Stop transitions:
- From any state → `WAITLISTED` (when city_not_covered or inventory_empty)

### 2.5 Request Lifespan (by Property Type)

| Property Type | Default Lifespan |
|--------------|:----------------:|
| Chambre | 30 days |
| Studio | 30 days |
| Appartement | 90 days |
| Maison/Villa | 90 days |
| Bureau/Commerce | 90 days |
| Terrain | 365 days |

### 2.6 Seller Status Flow

1. Property details collected
2. Documents verified
3. Published
4. Matched with buyers

---

## 3. SCORING RULES

### 3.1 CRM V5 Scoring — 7 Weighted Factors

| Factor | Weight | Description |
|--------|:------:|-------------|
| `base_interest` | **0.15** | Base interest expressed by user |
| `property_type_match` | **0.20** | Match between desired property type and available offers |
| `location_precision` | **0.20** | Location precision (city + neighborhood) |
| `budget_presence` | **0.10** | Budget presence and clarity |
| `urgency_signal` | **0.15** | Urgency signal (explicit temporality) |
| `visit_intent` | **0.20** | Expressed visit intention |
| `trust_signal` | **0.10** | Trust signal (reference, recommendation, history) |

**Total:** 1.0 (100%)

### 3.2 Lead Scoring Weights (Alternative V1 or V5)

From `lead_scoring_rules.json`:

| Factor | Weight | Description |
|--------|:------:|-------------|
| budget | **20** | Budget presence and amount |
| location | **15** | Location specificity |
| urgency | **20** | Urgency level |
| diaspora | **10** | Diaspora signal |
| phone | **5** | Phone presence/verification |
| property_type | **15** | Property type match |
| investment_profile | **10** | Investment profile strength |

### 3.3 V1 Scoring — Integer-based

Score = base_role_score + boosters - penalties

Computed from `lead_classifier_v1.json`.

### 3.4 Freshness Bonus (Match Scoring)

| Age of Listing | Bonus |
|:--------------:|:-----:|
| 0-3 days | +15 |
| 4-7 days | +12 |
| 8-15 days | +8 |
| 16-30 days | +4 |
| Over 30 days | 0 |

### 3.5 Availability Confirmation Bonus/Malus

| Status | Adjustment |
|--------|:----------:|
| Confirmed available | +10 |
| Unconfirmed | -20 |

### 3.6 Composite Score Model (Property Level)

The global property score aggregates (from Decision Engine Ch.33):
- Score Immobilier (Property Score)
- Score Geographique (Geographic Score)
- Disponibilite (Availability)
- Documents (Document Score)
- Qualite (Quality)
- Fiabilite detenteur (Holder Reliability)
- Probabilite de transaction (Transaction Probability)

Score range: **0 to 100**

### 3.7 Transaction Success Score (8 Indicators)

| Indicator | Weight |
|-----------|:------:|
| Compatibilite immobilier | 30% |
| Compatibilite geographique | 15% |
| Disponibilite reelle | 10% |
| Situation documentaire | 10% |
| Reactivite du detenteur | 10% |
| Historique du demandeur | 10% |
| Faisabilite financiere | 10% |
| Probabilite de negociation | 5% |

### 3.8 Re-proposition Thresholds (Decision Engine Ch.92)

| Score | Decision |
|:-----:|----------|
| ≥ 98% | Present immediately |
| ≥ 82% | Present if no better property |
| ≥ 55% | Keep in waiting |
| < 25% or < 60% | Never propose |

---

## 4. BOOSTERS AND PENALTIES

### 4.1 Score Boosters (Lead Level)

| Signal | Bonus | Source |
|--------|:-----:|--------|
| `budget_detected` | **+15** | lead_classifier_v1.json |
| `city_detected` | **+10** | lead_classifier_v1.json |
| `neighborhood_detected` | **+10** | lead_classifier_v1.json |
| `urgent_request` | **+20** | lead_classifier_v1.json |
| `diaspora_detected` | **+25** | lead_classifier_v1.json |
| `cash_purchase` | **+15** | lead_classifier_v1.json |

### 4.2 Score Penalties (Lead Level)

| Signal | Malus | Source |
|--------|:-----:|--------|
| `missing_budget` | **-10** | lead_classifier_v1.json |
| `unclear_location` | **-10** | lead_classifier_v1.json |
| `spam_like_message` | **-50** | lead_classifier_v1.json |

### 4.3 Match-Level Boosters

| Condition | Bonus | Source |
|-----------|:-----:|--------|
| exact_neighborhood_match | +25 | property_matching_v1.json |
| exact_city_match | +20 | property_matching_v1.json |
| budget_within_range | +15 | property_matching_v1.json |
| title_foncier | +10 | property_matching_v1.json |
| diaspora_investor | +20 | property_matching_v1.json |

### 4.4 Match Bonuses by Age (Freshness)

See section 3.4 above.

### 4.5 Availability Boost/Malus

See section 3.5 above.

---

## 5. THRESHOLDS

### 5.1 V1 Thresholds (Integer Scale)

| Class | Threshold | Action |
|-------|:---------:|--------|
| **HOT** | ≥ **80** | call_immediately |
| **WARM** | ≥ **60** | send_listings |
| **COLD** | ≥ **40** | request_budget |
| **LOW** | < **40** | follow_up |

### 5.2 V5 Thresholds (Normalized Scale)

| Class | Threshold | Action |
|-------|:---------:|--------|
| **HOT** | ≥ **0.8** | call_immediately |
| **WARM** | ≥ **0.5** | send_listings |
| **COLD** | ≥ **0.3** | request_budget |
| **SPAM** | ≤ **0.2** | ignore |

Note: V5 replaces V1's `LOW` class with `SPAM` at the bottom end. The V5 scale is normalized 0.0-1.0.

### 5.3 Priority Levels (Lead Priority)

| Level | Score Range |
|:-----:|:-----------:|
| **P0** | 100-95 |
| **P1** | 90-85 |
| **P2** | 75-60 |
| **P3** | 40 |

### 5.4 CRM Priorities (Decision Engine Action Priority)

| Priority | Action |
|:--------:|--------|
| 1 | Correct an inconsistency |
| 2 | Complete a critical field |
| 3 | Matching |
| 4 | Present a property |
| 5 | Contact the holder |
| 6 | Organize a visit |
| 7 | Follow-up |
| 8 | Notifications |
| 9 | File optimization |

### 5.5 Match Minimum Threshold

- Minimum match score to propose: **60/100** (V1) or **60%** (DE)
- Max results at first matching: **5** (DE)
- Max results: **10** (V1)
- Score < 60%: **never proposed**

### 5.6 Confidence Threshold for Intent Detection

- SEARCH_PROPERTY confidence threshold: **0.70**
- Reasoning confidence threshold: **0.70**

---

## 6. CRITERIA AND QUESTIONS FLOW

### 6.1 General Qualification Questions (Progressive Extraction)

The engine automatically extracts from messages:
- property type (type de bien)
- property family (famille de bien)
- operation (operation)
- city (ville)
- neighborhood (quartier)
- budget
- constraints (contraintes)
- useful characteristics (caracteristiques utiles)
- legal information (informations juridiques pertinentes)

### 6.2 Buyer Qualification Questions

| Question | Purpose |
|----------|---------|
| "Vous achetez pour habiter ou pour investir ?" | Purpose (habitation/investment) |
| "Quel budget total ?" | Total budget |
| "Quel quartier vous interesse le plus ?" | Neighborhood preference |
| "Vous voulez combien de chambres, de douches ou de salons ?" | Rooms (Cameroon-specific: chambres/douches/salons) |
| "Vous avez besoin d'un titre foncier ou d'autres documents ?" | Title/document requirements |
| "L'etat du bien peut demander des travaux ou pas ?" | Condition/tolerance for work |

**Required fields:** city, neighborhood, budget_total, property_type
**Optional fields:** bedrooms, bathrooms, title_status, condition, purpose

### 6.3 Rent Qualification Questions

| Question | Purpose |
|----------|---------|
| "Dans quelle ville et quel quartier cherchez-vous ?" | Location |
| "Quel budget mensuel maximum ?" | Monthly budget |
| "Combien de chambres vous faut-il ?" | Bedrooms |
| "Combien de douches si c'est important ?" | Bathrooms (conditional) |
| "C'est meuble ou non meuble ?" | Furnished status |
| "A partir de quand vous voulez emmenager ?" | Move-in date |
| "Les charges doivent etre incluses ou non ?" | Charges included |

**Required fields:** city, neighborhood, budget_monthly, property_type
**Optional fields:** bedrooms, bathrooms, furnished, move_in_date, charges_included

### 6.4 Land Qualification Questions

| Question | Purpose |
|----------|---------|
| "Dans quelle ville ou sur quel axe cherchez-vous ?" | City or axis |
| "Quelle surface souhaitez-vous ?" | Surface area |
| "Quel budget ?" | Budget |
| "Le terrain doit etre titre et loti ?" | Title and servicing |
| "A quelle distance de la route principale peut-il se trouver ?" | Road distance |
| "Vous voulez quel usage : habitation, commerce, investissement ?" | Usage |

**Required fields:** city_or_axis, surface, budget
**Optional fields:** titled, serviced, usage, road_distance

### 6.5 Commercial Property Qualification Questions

| Question | Purpose |
|----------|---------|
| "Quel type d'activite va occuper le local ?" | Activity type |
| "Quelle surface minimale ?" | Minimum surface |
| "Quel budget ?" | Budget |
| "Le local doit etre visible depuis la route ?" | Road visibility |
| "Il faut du parking, de l'eau ou de l'electricite ?" | Utilities |
| "L'usage autorise doit-il etre confirme avant la suite ?" | Permitted use |

**Required fields:** activity_type, surface, budget, neighborhood
**Optional fields:** road_visibility, parking, water_electricity, permitted_use

### 6.6 Seller Qualification Questions

| Question | Purpose |
|----------|---------|
| "Quel est le type de bien ?" | Property type |
| "Dans quelle ville et quel quartier ?" | Location |
| "Quel prix demandez-vous ?" | Asking price |
| "Quels documents sont disponibles ?" | Available documents |
| "Quelle surface ou quels volumes ?" | Surface/volumes |
| "Le bien est vide, occupe ou libre ?" | Occupancy status |

**Required fields:** property_type, city, neighborhood, price, documents
**Optional fields:** surface, availability, condition, contact, title_status

**Seller signals:** proprio, titre foncier, vente urgente, dernier prix, prix negociable

### 6.7 Investor Qualification Questions

| Question | Purpose |
|----------|---------|
| "Vous cherchez du rendement ou une plus-value ?" | Yield vs capital gain |
| "Quel budget total ?" | Total budget |
| "Dans quelle ville ou zone ?" | City/zone |
| "Quel niveau de risque acceptez-vous ?" | Risk tolerance |
| "Vous visez la location, la revente ou un mix ?" | Strategy |
| "Vous voulez une estimation humaine avant d'avancer ?" | Human estimation needed |

**Diaspora contextual questions:**
- "Avez-vous un proche sur place pour visiter ou verifier ?"
- "Souhaitez-vous recevoir des documents complementaires ?"
- "Souhaitez-vous organiser une visite ou une verification ?"

**Required fields:** expected_return, budget, city, risk_tolerance
**Optional fields:** strategy, timeline, diaspora_country, exit_strategy, property_type

**Capital signals:** 10M, 20M, 50M, 100M, 200M, 500M FCFA

### 6.8 Owner (Rental Listing) Qualification Questions

| Question | Purpose |
|----------|---------|
| "Le bien est situe dans quelle ville et quel quartier ?" | Location |
| "Quel prix souhaitez-vous ?" | Price |
| "C'est meuble ou non meuble ?" | Furnished status |
| "Le bien est disponible a partir de quand ?" | Availability date |
| "Quels frais doivent etre mentionnes ?" | Fees |
| "Qui est le contact de suivi ?" | Follow-up contact |

**Required fields (rental):** city, neighborhood, price, availability_date, contact
**Required fields (sale):** property_type, city, neighborhood, price, documents

### 6.9 Professional Search (Agent/Agency/Manager)

**Agent Search:**
- Required: city, specialty, zone
- Questions: "Dans quelle ville cherchez-vous un agent ?", "Quel type de bien vous interesse ?", "Quelle zone specifiquement ?"

**Agency Search:**
- Required: city, service_type
- Questions: "Dans quelle ville ?", "Quel type de service recherchez-vous ?"

**Property Manager:**
- Required: city, property_type, service_scope
- Questions: "De quel type de bien s'agit-il ?", "Dans quelle ville ?", "Quel type de gestion souhaitez-vous ?"

### 6.10 Traced Behaviors (4 Types)

| Behavior | Description | Usage |
|----------|-------------|-------|
| `message_history` | Message exchange history | Consistency analysis, intent change detection |
| `response_time` | Average response time | Engagement measurement, prioritization |
| `budget_changes` | Budget declaration evolution | Indecision or update detection |
| `visit_requests` | Visit requests | Strong purchase intent signal |

### 6.11 Collected Lead Fields (10 Fields)

From RULE_INDEX QUAL-011:

| Field | Description |
|-------|-------------|
| `message` | Raw user message |
| `intent` | Detected intention |
| `budget` | Extracted budget |
| `location` | Extracted location |
| `property_type` | Extracted property type |
| `urgency` | Urgency level |
| `score` | Composite computed score |
| `status` | Qualification status |
| `priority` | Lead priority |
| `diaspora_flag` | Diaspora detection flag |

### 6.12 Extracted Fields (KnowledgeBuilder - 25 Categories)

| Category | Fields |
|----------|--------|
| Identite | nom, telephone, email |
| Localisation | ville, pays, quartier |
| Bien | type_bien, surface, pieces, etage |
| Budget | budget_min, budget_max, cash |
| Temporalite | urgence, delai, disponibilite |
| Intention | intent, source, satisfaction_precedente |
| Session | historique_recherche, message_count, session_id |

---

## 7. MINIMUM REQUIREMENTS

### 7.1 Minimum Fields by Profile

#### Buyer
| Level | Fields |
|-------|--------|
| **Mandatory** | type_de_bien, ville, budget_maximum |
| **Recommended** | quartier, delai, nombre_de_pieces, usage (residence principale / investissement) |
| **Optional** | source_financement, situation_actuelle (locataire / proprietaire) |

#### Tenant
| Level | Fields |
|-------|--------|
| **Mandatory** | type_de_bien, ville, budget_mensuel |
| **Recommended** | quartier, duree_souhaitee, nombre_de_pieces |
| **Optional** | meuble, animaux_acceptes, parking |

#### Seller
| Level | Fields |
|-------|--------|
| **Mandatory** | type_de_bien, ville, prix_souhaite |
| **Recommended** | titre_propriete, surface, description, photos |
| **Optional** | motif_vente, disponibilite, historique_bien |

#### Investor
| Level | Fields |
|-------|--------|
| **Mandatory** | budget, type_investissement (locatif / revente / terrain), ville |
| **Recommended** | rendement_attendu, horizon, zone_preferee |
| **Optional** | experience_immobiliere, autres_investissements |

### 7.2 Minimum Fields by Property Type

| Type de bien | Mandatory Fields |
|-------------|------------------|
| studio | ville, budget, surface_min |
| apartment | ville, budget, nombre_de_pieces |
| house | ville, budget, surface, nombre_de_chambres |
| villa | ville, budget, surface_terrain, nombre_de_chambres |
| duplex | ville, budget, surface, etage |
| land | ville, budget, surface, type_terrain (constructible/agricole) |
| commercial | ville, budget, surface, type_commerce |

### 7.3 Critical Fields for Matching

The critical fields (champs critiques) that allow matching to start:
- property type
- property family
- operation (transaction type)
- city
- neighborhood
- budget
- constraints

**Budget is mandatory before matching.**

### 7.4 Minimum Match Score

- Match must be ≥ **60/100** (or 60%) to be proposed
- Score < 60% = **never proposed**
- Max 5 properties at first matching

---

## 8. EXCEPTION RULES

### 8.1 Re-proposition Exceptions

A definitively refused property is **never re-proposed** — except:

| Exception | Condition |
|-----------|-----------|
| Price drop | Significant price reduction |
| Major modification | Property undergoes major change |
| Need change | User's need/requirements change |
| Explicit request | User explicitly asks to see it again |

### 8.2 Stop Conditions

| Condition | Action |
|-----------|--------|
| City not covered | Stop qualification, inform user |
| Empty inventory for criteria | Stop qualification, propose alternatives |
| User asks for human | Immediate escalation to advisor |
| Repetitive thread | Stop after 3 exchanges without progress |
| User changes intent | Partially reset context, resume at step 1 |

### 8.3 Human Escalation Triggers

| User Says | Action |
|-----------|--------|
| "Je veux parler a quelqu'un" | Escalate to human |
| "Je veux negocier" | Escalate to human |
| "Le titre n'est pas clair" | Escalate to human |
| "Le terrain n'est pas loti" | Escalate to human |
| "Il y a plusieurs proprietaires" | Escalate to human |
| "Il faut une decision rapide" | Escalate to human |
| Repeated fraud signals | Escalate to human |

### 8.4 Escalation Rules

| Type | Condition | Target |
|------|-----------|--------|
| **Sale** | Lead HOT + budget confirmed + visit intent | Commercial agent |
| **Request** | Legal question, dispute, complaint | Support / Notary |
| **Human** | Explicit request or 3 qualification failures | Available advisor |

### 8.5 Budget Flexibility

| Operation | Tolerance |
|-----------|:---------:|
| Rent | ±20% |
| Buy | ±15% |
| Invest | ±25% |

Rule: "Budget is a preference, not an absolute constraint. Slightly above/below is acceptable with penalty."

### 8.6 Urgency Score Rule

"Urgency level must NOT influence match score directly (users overestimate urgency)."

### 8.7 Non-Compensation Rule

Certain criteria cannot compensate a major incompatibility:
- A well-located land does NOT compensate a user looking for a villa
- A villa with pool does NOT compensate a completely incompatible budget
- A profitable hotel does NOT compensate the absence of availability for sale

### 8.8 Property-Specific Exceptions

- Apartment with >4 bedrooms: treated as atypical, proposed only if coherent with file
- Villa with <4 bedrooms: must be reclassified or flagged as atypical
- Duplex without confirmed "two levels": must propose reclassification to house/villa

---

## 9. PRIORITY RULES

### 9.1 Lead Priority Levels

| Level | Score Range | Handling |
|:-----:|:-----------:|----------|
| **P0** | 100-95 | Immediate attention |
| **P1** | 90-85 | High priority |
| **P2** | 75-60 | Standard |
| **P3** | 40 | Low priority / follow-up |

### 9.2 Intent Priority (from intentions.json)

| Intent | Priority |
|--------|----------|
| INVESTOR_INTENT | **P0** |
| BUY_PROPERTY | VERY_HIGH |
| SELL_PROPERTY | VERY_HIGH |
| RENT_PROPERTY | HIGH |
| SEARCH_PROPERTY | NORMAL |

### 9.3 CRM Action Priority (Decision Engine)

1. Correct an inconsistency
2. Complete a critical field
3. Matching
4. Present a property
5. Contact the holder
6. Organize a visit
7. Follow-up
8. Notifications
9. File optimization

### 9.4 Proposition Priority (for compatible properties)

1. Best transaction probability
2. Best compatibility
3. Best availability
4. Best documentation level
5. Best holder reactivity

### 9.5 Refusal Learning Rule

3 refusals of similar properties → automatic priority adjustment (MATCH-014).

### 9.6 Diversity Rule

Avoid proposing multiple nearly identical properties (e.g., 3 apartments in same building → present only 1 as priority).

---

## 10. DIASPORA DETECTION RULES

### 10.1 Location Indicators

| Type | Indicators |
|------|------------|
| **France** | france, paris, lyon |
| **USA** | etats-unis, usa |
| **Canada** | canada |
| **Germany** | allemagne |
| **Belgium** | belgique |
| **Switzerland** | suisse |
| **UK** | uk, londres |
| **Generic** | diaspora, international |

### 10.2 Phone Prefix Indicators

| Prefix | Region |
|:------:|--------|
| +33 | France |
| +1 | USA/Canada |
| +44 | UK |
| +49 | Germany |

### 10.3 Diaspora Countries (for investor context)

France, Canada, Belgique, USA, Allemagne, Italie, Royaume-Uni

### 10.4 Impact on Scoring

| Element | Value |
|---------|:-----:|
| Base score for diaspora_investor role | **95** (highest of all roles) |
| Diaspora detection bonus (lead scoring) | **+25** |
| Diaspora matching bonus | **+20** |
| Lead scoring weight for diaspora signal | **10** (out of 100 total weights) |

### 10.5 Diaspora Investor Investment Types

land banking, rental property, commercial property, development project, student housing, airbnb

### 10.6 Diaspora Capital Signals

10M, 20M, 50M, 100M, 200M, 500M (FCFA)

### 10.7 Diaspora-Specific Qualification Questions

- "Avez-vous un proche sur place pour visiter ou verifier ?"
- "Souhaitez-vous recevoir des documents complementaires ?"
- "Souhaitez-vous organiser une visite ou une verification ?"

---

## 11. USER TYPOLOGIES

### 11.1 Complete Typology Matrix

| ID | Label | Roles | Journey | Priority | Decision |
|:---|-------|-------|---------|:--------:|:--------:|
| **DEMANDEUR** | Demandeur (Requester) | VISITOR, USER, BUYER, RENTER | Create request → Qualify → Match → Follow-up | P1 | FUSIONNER |
| **PROPRIETAIRE** | Proprietaire (Owner) | OWNER | Publish property → Update availability → Documents → Follow-up | P1 | FUSIONNER |
| **AGENT_IMMOBILIER** | Agent Immobilier (Agent) | INTRODUCER | Queue → Assignment → Follow-up → Performance | P1 | ADAPTER |
| **OPERATEUR** | Operateur LAWIM (Operator) | MANAGER | Triage → Review → Assignment → Queue management | P0/P1 | CONSERVER + ADAPTER |
| **SUPERVISEUR** | Superviseur (Supervisor) | VICE_MANAGER, ADMIN | KPIs → Exceptions → Contestations → Audit | P0/P1 | FUSIONNER |
| **ADMINISTRATEUR** | Administrateur (Admin) | ADMIN | Users → Permissions → System health → Roles | P0 | CONSERVER |
| **INVESTISSEUR** | Investisseur (Investor) | persona | Investment-oriented request view | P2 | ADAPTER |

### 11.2 CRM Roles (Level 1-7)

From `implement_all.sql` / `user_roles.json`:

| Level | Role |
|:-----:|------|
| 1 | demandeur |
| 2 | vendeur |
| 3 | agent |
| 4 | agence |
| 5 | assistant |
| 6 | vice_master |
| 7 | master |

### 11.3 User States (7 States)

From `USER_STATES.json`:
1. NEW_USER
2. SEARCHING_PROPERTY
3. PROPERTY_OWNER
4. AGENT
5. LEAD_CREATED
6. PREMIUM_AGENT
7. INACTIVE

### 11.4 Buyer Profiles (Negotiation)

From `04-DECISION-ENGINE-REFERENCE.md` / Sales Playbook:
1. national
2. diaspora
3. investisseur
4. jeune actif

### 11.5 Seller Profiles (Negotiation)

From Sales Playbook:
1. particulier
2. promoteur
3. bailleur

### 11.6 Professional Qualification Requirements

| Profession | Required Docs | Min Exp | Trust Score Min |
|-----------|:-------------:|:-------:|:---------------:|
| AGENT_IMMOBILIER | carte_nationale, certificat_agent_immobilier, registre_de_commerce, casier_judiciaire, attestation_de_residence | 0 yrs | 3.0 |
| PROPRIETAIRE | carte_nationale, titre_foncier, justificatif_de_propriete | 0 yrs | 2.0 |
| PROMOTEUR | carte_nationale, registre_de_commerce, agrement_promoteur, casier_judiciaire, attestation_fiscale | 3 yrs | 3.5 |
| NOTAIRE | carte_professionnelle_notaire, inscription_ordre_notaires, casier_judiciaire, attestation_fiscale | 5 yrs | 4.0 |
| EXPERT_FONCIER | certificat_expert_foncier, carte_professionnelle, casier_judiciaire | 3 yrs | 3.5 |
| ARCHITECTE | diplome_architecte, inscription_ordre_architectes, carte_professionnelle, casier_judiciaire | 2 yrs | 3.0 |
| OPERATEUR | carte_nationale, contrat_de_travail, casier_judiciaire | 1 yr | 3.5 |

---

## 12. BUSINESS RULES FOR QUALIFICATION

### 12.1 General Qualification Rules

| Rule | Description |
|------|-------------|
| **Un message par question** | On WhatsApp: one question per message |
| **Limite de champs** | On Telegram: 2-3 fields maximum per message |
| **Pas de redemande** | Never re-ask for an already collected field |
| **Pas de redemarrage** | Never restart qualification from the beginning |
| **Correction prioritaire** | User correction always overrides obsolete context |
| **Budget obligatoire** | Budget is mandatory before matching |

### 12.2 Cameroon-Specific Attributes (Use These)

| Use This | Instead Of |
|----------|-----------|
| chambres (bedrooms) | nombre de pieces |
| douches (bathrooms) | salles de bain |
| salons (living rooms) | (no alternative) |
| meuble / non meuble | (standard) |
| bordure de route | (road frontage) |
| accessibilite | (accessibility) |
| titre foncier | (land title) |
| loti / non loti | (serviced land) |

**Standing is deduced** from: prix + quartier + photos + finitions — never asked explicitly.

### 12.3 Conversation Principles

- Understand before responding
- Never ask a useless question
- Never re-ask known information
- Never ask a question whose answer can be deduced from context
- Start matching as soon as possible
- Never wait for complete qualification to act
- Maintain a natural tone
- Adapt questions to context
- Never follow a fixed questionnaire
- Understand and normalize Cameroonian expressions

### 12.4 Anti-Fraud Layers

| Layer | Detection | Action |
|-------|-----------|--------|
| `broker_spam` | Unsolicited broker messages | Penalty -50, manual flag |
| `duplicate_listing` | Same property posted multiple times | Deduplication, warning |
| `fake_price` | Anomalously low or high price | Flag for manual verification |
| `suspicious_urgency` | Artificial urgency for pressure | Reduce urgency_signal weight |

### 12.5 Absolute Rules (Never Do)

| Rule | Description |
|------|-------------|
| No fixed questionnaire | Never transform conversation into a fixed form |
| No duplicate questions | Never ask the same information twice without reason |
| No ignoring corrections | Never ignore a user correction |
| No double consent bypass | Never bypass explicit consent from both parties |
| No standing question | Never ask for "standing" explicitly (deduce it) |
| No nombre de pieces | Never use "nombre de pieces" — use chambres instead |
| No wrong city proposal | Never propose a different city when requested city is uncovered |
| No budget pressure on greeting | Never pressure for budget on greetings only (History Gate) |

### 12.6 Double Consent Rule

No relationship can be established without explicit consent from both parties. The process must remain traceable and timestamped.

### 12.7 Anonymity Rules

- Requester remains anonymous until the holder accepts the relationship
- Minimum necessary principle always applies
- Never disclose: exact address before authorization, sensitive documents, confidential information not required, data from non-concerned actors

### 12.8 Holders

The property holder can be:
- the owner (proprietaire)
- an agency (agence)
- a mandated agent (agent mandaté)
- a manager (gestionnaire)
- an authorized introducer (introducer autorise)

### 12.9 Matching Start Rule

Matching begins as soon as critical fields are available. Conversation continues after matching. Never wait for complete qualification.

### 12.10 Rematching Triggers

**Requester side:**
- Budget modification
- City change
- Neighborhood change
- Property type change
- New criterion added
- Criterion removed
- Property refusal
- Visit abandoned
- New preference expressed

**Property side:**
- Publication
- Modification
- Price drop/increase
- Availability change
- Photos added
- GPS coordinates added
- Documents added
- Qualification improvement

**Holder side:**
- Acceptance
- Refusal
- No response
- Temporary unavailability
- Return to availability

**System side:**
- New business rule
- Periodic recalculation
- Global learning
- Data correction

### 12.11 Follow-up Schedule

| Relance | Delay |
|:-------:|:-----:|
| J1 | 24h |
| J7 | 168h |
| J30 | 720h |
| J90 | 2160h |

### 12.12 Long-Term Memory Rule

- Long-term retention: 365 days
- Lead >12 months: re-contactable
- Previous satisfaction consulted (check_previous_property_satisfaction)

### 12.13 Familiarity Levels

| Level | Duration |
|:-----:|:--------:|
| J1 | 1 day |
| J2 | ≤7 days |
| J3 | ≤30 days |
| J4 | >30 days |

### 12.14 Forbidden Items in Scoring

- Land scoring: never use chambres, douches, salon, pieces, standing
- Commercial/industrial scoring: residential criteria are forbidden
- Urgency must NOT influence match score directly

### 12.15 Qualification Question Source Files

The following legacy files contain the question banks:
- `conversation-qualification-questions.md` (6.4KB) — Core qualification question bank
- `minimum-fields-request.md` (6.8KB) — Minimum fields for request qualification
- `property-qualification-reference.md` (5.3KB) — Property qualification reference
- `qualification-implementation-backlog.md` (14.3KB) — Implementation backlog (not fully migrated)

---

## 13. SOURCE REFERENCES

### 13.1 Primary Sources (Direct Knowledge Extracted)

| Source | Path | Type | Confidence |
|--------|------|------|:-----------:|
| Gold Qualification Model | `docs/lawim_heritage_gold/QUALIFICATION_MODEL.md` | Markdown | **HIGH** |
| Gold Rule Index | `docs/lawim_heritage_gold/RULE_INDEX.md` | Markdown | **HIGH** |
| Conversation Reference | `git:backup/.../03-CONVERSATION-REFERENCE.md` | Markdown | **HIGH** |
| Decision Engine Reference | `git:backup/.../04-DECISION-ENGINE-REFERENCE.md` | Markdown | **HIGH** |
| Matching Reference | `git:backup/.../04-MATCHING-REFERENCE.md` | Markdown | **HIGH** |
| Intentions | `knowledge_unified/qualification/intentions.json` | JSON | **HIGH** |
| Investor Matrices | `knowledge_unified/qualification/investor_matrices.json` | JSON | **HIGH** |
| Owner Matrices | `knowledge_unified/qualification/owner_matrices.json` | JSON | **HIGH** |
| Professional Search Matrices | `knowledge_unified/qualification/professional_search_matrices.json` | JSON | **HIGH** |
| Property Search Matrices | `knowledge_unified/qualification/property_search_matrices.json` | JSON | **HIGH** |
| Qualification Rules | `knowledge_unified/qualification/qualification_rules.md` | Markdown | **HIGH** |
| Seller Matrices | `knowledge_unified/qualification/seller_matrices.json` | JSON | **HIGH** |
| User Typologies | `knowledge_unified/qualification/user_typologies.json` | JSON | **HIGH** |
| Scoring Rules | `knowledge_unified/matching/scoring_rules.json` | JSON | **HIGH** |
| Professional Qualification | `knowledge_unified/professionals/professional_qualification.json` | JSON | **MEDIUM** |
| Source Inventory | `knowledge_unified/sources/SOURCE_INVENTORY.md` | Markdown | **HIGH** |
| Quality Report | `knowledge_unified/validation/quality_report.md` | Markdown | **HIGH** |

### 13.2 Legacy Sources Referenced (Not Directly Read)

| Source | Description | Confidence |
|--------|-------------|:-----------:|
| `lead_classifier_v1.json` | Base scores, boosters, penalties, V1 thresholds | **HIGH** |
| `RULE_ENGINE_V5.json` | V5 thresholds, pipeline, 7 CRM factors, anti-fraud | **HIGH** |
| `RULE_ENGINE_V3.json` | Additional user types | **MEDIUM** |
| `lead_scoring_rules.json` | Lead scoring weights (7 factors) | **HIGH** |
| `lead_scoring.json` | Priority levels P0-P3 | **MEDIUM** |
| `diaspora_filter.py` | Diaspora indicators (13 locations + 4 prefixes) | **HIGH** |
| `conversation-qualification-questions.md` | Question banks (6.4KB) | **HIGH** |
| `minimum-fields-request.md` | Minimum fields per request type (6.8KB) | **HIGH** |
| `minimum-fields-property.md` | Minimum fields for property (6.7KB) | **HIGH** |
| `property-qualification-reference.md` | Property qualification (5.3KB) | **HIGH** |
| `qualification-implementation-backlog.md` | Backlog items (14.3KB) | **MEDIUM** |
| `channels/whatsapp-telegram-dashboard-qualification.md` | Channel-specific qualification | **MEDIUM** |
| `diaspora-behavior-model.md` | Diaspora behavior patterns (4.8KB) | **MEDIUM** |
| `lead_scoring_v1.json` (archive) | V1 scoring archive | **LOW** |
| `knowledge_builder.py` | 25 user fields, 10 lead fields | **MEDIUM** |
| `conversation-patterns.md` | Core conversation patterns (9.0KB) | **MEDIUM** |
| `roles-matrix.md` | Roles matrix (4.2KB) | **MEDIUM** |

### 13.3 Sprint Documentation

| Source | Description | Confidence |
|--------|-------------|:-----------:|
| `.lawim/tickets/sprint-009/T09.02-qualification-scoring.md` | Ticket definition | **MEDIUM** |
| `reports/sprint-009/T09.02-qualification-scoring-report.md` | Execution report | **MEDIUM** |

---

*End of Qualification Heritage Extraction — Mission H0.4 complete.*
*Document patrimonial — Toute reconstruction doit respecter ce savoir extrait.*
