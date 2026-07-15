# READINESS LEVELS — LAWIM Qualification Progress Model

**Document ID:** LAWIM-GOLD-QM-READINESS-V1
**Status:** CANONICAL — Definitive reference for all readiness level definitions
**Date:** 2026-07-15

---

## Table of Contents

1. [The Readiness Level Model](#1-the-readiness-level-model)
2. [Level Definitions](#2-level-definitions)
3. [Level Transitions](#3-level-transitions)
4. [The Fundamental Rule](#4-the-fundamental-rule)
5. [Implementation Rules](#5-implementation-rules)
6. [Threshold Scores](#6-threshold-scores)
7. [Residential Example Walkthrough](#7-residential-example-walkthrough)
8. [Land Example Walkthrough](#8-land-example-walkthrough)
9. [Commercial Example Walkthrough](#9-commercial-example-walkthrough)
10. [Financing Example Walkthrough](#10-financing-example-walkthrough)
11. [Professional Service Example](#11-professional-service-example)

---

## 1. The Readiness Level Model

The readiness level model defines seven progressive stages through which any qualification request progresses. Each level unlocks specific actions and determines what fields must (and must not) be collected.

### Model Principles

- **Progressive disclosure**: Ask only what is needed for the current readiness level
- **Early search**: Launch search as soon as MINIMUM_SEARCH_READY is achieved
- **No blocking**: Missing recommended/optional fields never block progression
- **Forward-only**: Readiness levels only advance; never regress
- **Recovery**: If a user corrects information, re-validate at current level without restarting

### Level Overview

```
Level 1: INTENT_IDENTIFIED
    ↓ (transaction + property type known)
Level 2: MINIMUM_INTAKE_READY
    ↓ (city + budget known)
Level 3: MINIMUM_SEARCH_READY  ← FIRST SEARCH LAUNCHED HERE
    ↓ (neighborhood + basic criteria)
Level 4: MINIMUM_MATCHING_READY
    ↓ (field-specific criteria for ranking)
Level 5: INTRODUCTION_READY
    ↓ (contact info + willingness to connect)
Level 6: VISIT_READY
    ↓ (visit logistics confirmed)
Level 7: TRANSACTION_READY
    ↓ (legal/financial requirements met)
```

### Readiness Level vs. Journey Stage

| Readiness Level | Journey Stage | Typical Channel |
|----------------|---------------|-----------------|
| INTENT_IDENTIFIED | DISCOVERY | WhatsApp/Telegram |
| MINIMUM_INTAKE_READY | QUALIFICATION | WhatsApp/Telegram |
| MINIMUM_SEARCH_READY | SEARCH | WhatsApp/Telegram/Dashboard |
| MINIMUM_MATCHING_READY | MATCHING | Dashboard/System |
| INTRODUCTION_READY | INTRODUCTION | WhatsApp/Telegram |
| VISIT_READY | VISIT | WhatsApp/Phone |
| TRANSACTION_READY | TRANSACTION | Dashboard/Notary |

---

## 2. Level Definitions

### 2.1 INTENT_IDENTIFIED

**Definition**: The system has established what the user wants to do and what type of property/service they need.

**Required Fields (Summary)**:

| Requirement | Description | Examples |
|-------------|-------------|----------|
| Transaction type | Buy, rent, sell, finance, find, service | FLD-TRANSACTION, FLD-INTENT |
| Property/service type | What specific type | FLD-PROPERTY_TYPE |

**Conditional Requirements**: None at this level.

**Blocking Conditions**:
- User intention is ambiguous or contradictory
- Property type is not supported by LAWIM
- Transaction type is incompatible with property type
- User explicitly refuses to clarify intent after 3 attempts

**Non-Blocking Missing Fields**: All other fields are non-blocking at this level.

**Allowed Actions**:
- ✓ Detect and confirm intent
- ✓ Detect and confirm property type
- ✓ Ask follow-up to clarify ambiguous intent
- ✓ Route to human agent if intent unsupported
- ✗ Launch search (too early)
- ✗ Ask for contact details (premature)
- ✗ Ask for detailed property criteria (premature)

**Threshold Score**: N/A — this level is binary (intent identified or not)

---

### 2.2 MINIMUM_INTAKE_READY

**Definition**: The system has enough information to begin locating properties — city and budget are established.

**Required Fields (Summary)**:

| Requirement | Description | Examples |
|-------------|-------------|----------|
| City | Target city known | FLD-CITY, ville |
| Budget | Maximum budget or range | FLD-BUDGET_MAX, budget_total |

**Conditional Requirements**:
- Land: surface + usage_prevu also required
- Commercial: activité_prévue + surface_min also required
- Financing: montant_recherche + apport_disponible also required

**Blocking Conditions**:
- City not covered by LAWIM's active workflow
- Budget below minimum viable threshold for the property type
- Budget missing after explicit question (3 attempts)
- City missing after explicit question (3 attempts)
- User gives contradictory budget information after clarification

**Non-Blocking Missing Fields**:
- Neighborhood (will be asked at search level)
- Contact info (not needed yet)
- Property details (chambres, douches, surface, etc.)
- Timing (disponibilité, délai)

**Allowed Actions**:
- ✓ Confirm city and budget
- ✓ Ask for neighborhood
- ✓ Begin matching engine initialization
- ✗ Launch full search (need neighborhood)
- ✗ Ask for contact details
- ✗ Introduce to property holders

---

### 2.3 MINIMUM_SEARCH_READY

**Definition**: The system has the minimum criteria to launch a first property search. **This is the critical threshold** — once reached, LAWIM MUST launch a search. It is forbidden to continue asking recommended or optional fields before presenting results.

**Required Fields (Summary)**:

| Requirement | Description | Examples |
|-------------|-------------|----------|
| City | Target city | FLD-CITY |
| Budget | Budget range | FLD-BUDGET_MAX |
| Neighborhood | At least one neighborhood or zone | FLD-NEIGHBORHOOD |
| Property type | Specific property type | FLD-PROPERTY_TYPE |
| Transaction | Buy/rent/etc | FLD-TRANSACTION |

**Conditional Requirements**:
- Land: surface_min also required
- Commercial: activité_prévue + surface_min also required
- Financing: montant_recherche + apport_disponible + type_bien_projet + ville_projet
- Professional: localisation + description_besoin + type_prestation

**Blocking Conditions**:
- City + neighborhood combination returns zero inventory
- Budget is too low for any property of this type in this city
- Property type has zero inventory in the city
- User refuses to provide neighborhood (offer zone as alternative first)

**Non-Blocking Missing Fields**:
- Number of bedrooms (soft constraint — can be refined after first results)
- Property condition (ranking preference)
- Specific amenities (balcony, parking, etc.)
- Contact information (collected at introduction level)
- Timing/disponibilité (collected at introduction level)

**Allowed Actions**:
- ✓ ✓ ✓ **LAUNCH FIRST SEARCH** (MANDATORY)
- ✓ Present top results to user
- ✓ Ask if user wants to refine criteria
- ✓ Ask if user wants to see details of specific properties
- ✓ Offer to collect more criteria for refined search
- ✗ Continue asking recommended/optional fields before search (FORBIDDEN)
- ✗ Withhold results while collecting non-essential fields
- ✗ Ask for contact details before presenting results

**Threshold Score**: When all required fields are present and no blocking conditions exist, the system MUST transition to MINIMUM_SEARCH_READY and launch search immediately.

---

### 2.4 MINIMUM_MATCHING_READY

**Definition**: The system has enough detailed criteria to rank and score matches with precision.

**Required Fields (Summary)**:

| Requirement | Description | Per-Matrix |
|-------------|-------------|------------|
| Room count | chambres/douches/salons | Multi-room properties |
| Kitchen type | Cuisine preference | All residential |
| Furnished | Meublé preference | Residential |
| Usage | Intended use | Buy transactions |
| Budget type | Monthly/total | Derived from transaction |

**Conditional Requirements**:
- Appartement/villa: chambres, douches, salons
- Studio: cuisine, meublé (chambres=0 by definition)
- Chambre: douches (interne/externe), cuisine
- Land: surface, usage_prevu, type_document
- Commercial: matching fields per matrix (M-sections)
- Financing: matching fields per matrix

**Blocking Conditions**: None — matching is progressive; missing criteria simply reduce match precision.

**Non-Blocking Missing Fields**:
- Visit preferences
- Contact preferences
- Timing details (disponibilité)
- Amenities (climatisation, internet, etc.)
- Condition (état)
- Floor level (étage)

**Allowed Actions**:
- ✓ Re-rank results with improved criteria
- ✓ Filter results more precisely
- ✓ Show match scores with breakdown
- ✓ Ask if user wants to see top N results
- ✓ Begin collecting introduction fields
- ✗ Block search results while collecting matching fields
- ✗ Replace already-show results without user request

---

### 2.5 INTRODUCTION_READY

**Definition**: The system has the user's consent and contact information to facilitate an introduction between parties.

**Required Fields (Summary)**:

| Requirement | Description | Examples |
|-------------|-------------|----------|
| Name | User's full name | FLD-NOM |
| Phone | Contact phone number | FLD-TELEPHONE |
| Channel | Preferred contact channel | FLD-CANAL_PREFERE |
| Availability | When user is available | FLD-DISPONIBILITE, FLD-DELAI |
| Consent | Agreement to be introduced | Implicit from continued conversation |

**Conditional Requirements**:
- Email: for diaspora or specific follow-up scenarios
- Language: if not yet auto-detected
- Preferred contact time: if not yet provided

**Blocking Conditions**:
- User refuses to provide name after 2 attempts (offer anonymous option)
- User refuses to provide phone number (offer alternative channel)
- User explicitly says they are not ready to be introduced
- No suitable match found at previous level

**Non-Blocking Missing Fields**:
- Email address (optional unless diaspora)
- Specific visit preferences
- Preferred agent type
- Detailed feedback on shown properties

**Allowed Actions**:
- ✓ ✓ **INTRODUCE PARTIES** (with double consent)
- ✓ Share property details with user
- ✓ Contact property holder on user's behalf
- ✓ Schedule introduction call
- ✓ Ask for visit preferences
- ✗ Share contact info without double consent (FORBIDDEN)
- ✗ Force introduction if user is not ready

---

### 2.6 VISIT_READY

**Definition**: All conditions are met to organise a physical visit to the property.

**Required Fields (Summary)**:

| Requirement | Description | Examples |
|-------------|-------------|----------|
| Visit logistics | Date, time, participants | FLD-HORAIRE_VISITE, nombre_visiteurs |
| Property access | Access arrangements confirmed | FLD-ACCES_INSTRUCTIONS |
| Accompaniment | Whether agent accompanies | accompanateur |
| Visit type | Individual, group, virtual | type_visite |

**Conditional Requirements**:
- Land: GPS coordinates shared, geometre availability if needed
- Commercial: access hours, PMR requirements, parking
- Specific amenity verification: climatisation, sécurité, eau for certain types
- Transport: vehicle availability for agent if accompanying

**Blocking Conditions**:
- Property is not available for visit
- Owner refuses visit
- User cannot make any proposed time slots
- Access instructions are not obtainable
- Safety concerns for agent (for specific neighborhoods/times)

**Non-Blocking Missing Fields**:
- Specific questions about property condition
- Negotiation preferences
- Financing details

**Allowed Actions**:
- ✓ Schedule and confirm visit
- ✓ Send visit confirmation with details
- ✓ Ask for feedback after visit
- ✓ Request additional documents if needed
- ✓ Prepare visit report
- ✗ Share exact address without user consent (FORBIDDEN)

---

### 2.7 TRANSACTION_READY

**Definition**: The user is ready to proceed to transaction stage. All legal, financial, and documentary requirements are met or in progress.

**Required Fields (Summary)**:

| Requirement | Description | Examples |
|-------------|-------------|----------|
| Financing | Payment method confirmed | FLD-FINANCING, FLD-SOURCE_FINANCEMENT |
| Guarantees | Caution/deposit agreed | FLD-CAUTION, FLD-CHARGES |
| Documents | Required documents available | pièce_identité, registre |
| Legal checks | Title/ownership verified | FLD-NUM_TITRE, litiges |
| Professional review | Notary/geometer identified | besoin_notaire, besoin_geometre |

**Conditional Requirements**:
- Land title: num_titre, identite_signataires, verifications
- Rent: caution, charges, bail
- Buy: financing, notaire, titre
- Professional: contrat_service, conditions_paiement signed
- Financing: all income/guarantee documents verified

**Blocking Conditions**:
- Financing not secured (unable to proceed)
- Title dispute or legal issue
- Missing mandatory documents
- Party withdraws consent
- Professional review required but not obtained
- Any transaction_blocker field is unresolved

**Non-Blocking Missing Fields**:
- Decorative preferences
- Move-in date (can be flexible)
- Secondary preferences
- Long-term plans

**Allowed Actions**:
- ✓ Proceed to formal transaction
- ✓ Engage notary/legal professional
- ✓ Facilitate document exchange
- ✓ Coordinate payment
- ✓ Generate final contract
- ✗ Proceed without resolving transaction_blocker fields
- ✗ Skip legal verification
- ✗ Share confidential documents without explicit consent

---

## 3. Level Transitions

### Transition Rules

| From | To | Required Action | Auto or Manual |
|------|----|-----------------|----------------|
| INTENT_IDENTIFIED | MINIMUM_INTAKE_READY | Collect city + budget | Auto (ask questions) |
| MINIMUM_INTAKE_READY | MINIMUM_SEARCH_READY | Collect neighborhood + validate criteria | Auto (ask + search) |
| MINIMUM_SEARCH_READY | MINIMUM_MATCHING_READY | Collect property-specific criteria | Auto (post-search refinement) |
| MINIMUM_MATCHING_READY | INTRODUCTION_READY | Collect contact + confirm interest | Auto (ask + confirm) |
| INTRODUCTION_READY | VISIT_READY | Schedule visit + confirm access | Manual (coordination) |
| VISIT_READY | TRANSACTION_READY | Verify documents + legal + financing | Manual (with professionals) |

### Transition Guards

Each transition must pass these checks:

```
can_transition(from, to) {
    // All required fields for 'to' are present
    if missing_required_fields(to) return false
    
    // No blocking conditions exist
    if blocking_conditions_exist(from, to) return false
    
    // User has not explicitly rejected progression
    if user_rejected_progression return false
    
    return true
}
```

### Automatic vs. Manual Transitions

| Levels | Type | Trigger |
|--------|------|---------|
| 1→2→3→4 | Automatic | Field collection + system validation |
| 4→5 | Semi-automatic | User interest confirmation needed |
| 5→6 | Manual | Coordination with property holder |
| 6→7 | Manual | Professional verification needed |

---

## 4. The Fundamental Rule

**THE CARDINAL RULE OF QUALIFICATION:**

> **As soon as MINIMUM_SEARCH_READY is reached, LAWIM can launch a first search. It is forbidden to continue a long questionnaire only to fill recommended or optional fields.**

### What This Means in Practice

1. **Search first, refine later**: The first search may return broad results. That is acceptable. Refinement happens after results are seen.

2. **No withholding**: Never say "I need a few more details before I can show you results" when minimum search criteria are already met.

3. **Progressive matching**: Matching scores improve as more fields are collected. A score of 60/100 on first pass is acceptable. Collection continues after showing results.

4. **Channel awareness**: On WhatsApp, this rule is even stricter — one question at a time, launch search at minimum, collect remaining fields during follow-up.

5. **Exception**: If the first search returns zero results, it is acceptable to collect additional criteria before a second search. Do not ask for more criteria before the first search.

### Enforcement

```
correct_behavior:
  - collect transaction, property_type, city, budget, neighborhood
  - LAUNCH SEARCH immediately
  - present results
  - ask: "Would you like to refine? I can also ask about..."
  - collect additional criteria if user agrees

incorrect_behavior:
  - collect transaction, property_type, city, budget, neighborhood
  - ask about chambres, douches, cuisine, etage, parking, ... (15 questions)
  - "Let me now search..."
  - THIS IS WRONG. Search should have happened after step 1.
```

---

## 5. Implementation Rules

### Field Collection Order

1. Always collect in readiness-level order
2. Within a level, collect by priority (lower question_priority first)
3. Skip fields already known from context or previous conversation
4. Skip fields that are irrelevant for the property type
5. Never re-ask a field that has been confirmed

### Priority Calculation

Within each readiness level, fields are ordered by:

```
priority = base_priority - (impact_filtering * 10)
         + (sensitivity * 5)
         - (ambiguity * 3)
```

Where:
- `impact_filtering` = 0.0-1.0 (how much this field narrows results)
- `sensitivity` = 0-3 (0=public, 3=confidential — higher = ask later)
- `ambiguity` = 0-1 (0=clear, 1=ambiguous — higher = ask later)

### Timeout Rules

| Level | Max Time to Collect | Notes |
|-------|--------------------|-------|
| INTENT_IDENTIFIED | 2 exchanges | Clarify quickly or handoff |
| MINIMUM_INTAKE_READY | 4 exchanges | City + budget priority |
| MINIMUM_SEARCH_READY | 6 exchanges | Include search launch |
| MINIMUM_MATCHING_READY | 4 exchanges post-search | |
| INTRODUCTION_READY | 2 exchanges | |
| VISIT_READY | 3 exchanges | |
| TRANSACTION_READY | Ongoing | With professional support |

### Rollback Protection

If a user corrects information at a higher readiness level:
1. Re-validate the specific field
2. Check if blocking conditions still clear
3. Check if current level's required fields still satisfied
4. If yes → stay at current level
5. If no → drop to highest level that IS satisfied (never below MINIMUM_INTAKE_READY once achieved)

---

## 6. Threshold Scores

### Match Score by Readiness Level

| Readiness Level | Expected Match Score Range | Notes |
|-----------------|---------------------------|-------|
| INTENT_IDENTIFIED | N/A | Cannot compute match score yet |
| MINIMUM_INTAKE_READY | 20-40 | Rough estimate based on city + budget |
| MINIMUM_SEARCH_READY | 40-60 | Basic match with neighborhood + property type |
| MINIMUM_MATCHING_READY | 60-80 | Detailed match with specific criteria |
| INTRODUCTION_READY | 70-85 | Refined with contact context |
| VISIT_READY | 80-95 | Highly refined match |
| TRANSACTION_READY | 90-100 | Best possible match for the user |

### Minimum Match Score for Action

| Action | Minimum Score |
|--------|---------------|
| Show in search results | 40/100 |
| Show in top 10 | 50/100 |
| Recommend for visit | 70/100 |
| Recommend for transaction | 85/100 |

### Boost Factors by Level

| Level | Boost Factors Available |
|-------|------------------------|
| INTENT_IDENTIFIED | None |
| MINIMUM_INTAKE_READY | city_match (+20), budget_within_range (+15) |
| MINIMUM_SEARCH_READY | exact_neighborhood (+25), diaspora (+20) |
| MINIMUM_MATCHING_READY | property_type_match (+15), amenities_match (+10) |
| INTRODUCTION_READY | urgency (+15), trust_signal (+10) |
| VISIT_READY | visit_intent (+20) |
| TRANSACTION_READY | financing_secured (+15), documents_ready (+10) |

### Penalty Factors by Level

| Level | Penalty Factors |
|-------|-----------------|
| INTENT_IDENTIFIED | None |
| MINIMUM_INTAKE_READY | missing_budget (-10), unclear_location (-10) |
| MINIMUM_SEARCH_READY | missing_neighborhood (-5), spam_like (-50) |
| MINIMUM_MATCHING_READY | contradictory_criteria (-15) |
| INTRODUCTION_READY | refused_contact (-20) |
| VISIT_READY | missed_visit (-25) |
| TRANSACTION_READY | incomplete_documents (-30) |

---

## 7. Residential Example Walkthrough

### User: Looking for a 2-bedroom apartment in Douala

| Step | Readiness Level | Fields Collected | Action |
|------|-----------------|------------------|--------|
| 1 | INTENT_IDENTIFIED | TRANSACTION=RENT, PROPERTY_TYPE=appartement_non_meuble | Confirm: "Looking to rent an apartment?" |
| 2 | MINIMUM_INTAKE_READY | CITY=Douala | "In which city?" → Douala |
| 3 | MINIMUM_INTAKE_READY | BUDGET_MAX=150000 | "Maximum budget?" → 150,000 FCFA |
| 4 | MINIMUM_SEARCH_READY | NEIGHBORHOOD=Bonapriso | "Which neighborhood?" → Bonapriso |
| 5 | **SEARCH LAUNCHED** | — | System finds 5 apartments in Bonapriso ≤150k FCFA |
| 6 | MINIMUM_MATCHING_READY | CHAMBRES=2, DOUCHES=1 | "How many bedrooms?" → 2. Results re-ranked. |
| 7 | INTRODUCTION_READY | NOM, TELEPHONE, DISPONIBILITE | "Your name and phone?" → Collected |
| 8 | VISIT_READY | HORAIRE_VISITE | "When would you like to visit?" |
| 9 | TRANSACTION_READY | CAUTION, CHARGES | Security deposit and charges confirmed |

### What NOT to do:

```
WRONG: Ask all 20 questions before showing any results
RIGHT: Launch search at step 5, refine post-search
```

---

## 8. Land Example Walkthrough

### User: Looking for titled land in Yaounde

| Step | Readiness Level | Fields Collected | Action |
|------|-----------------|------------------|--------|
| 1 | INTENT_IDENTIFIED | TRANSACTION=BUY, PROPERTY_TYPE=terrain_titre | Confirm land purchase intent |
| 2 | MINIMUM_INTAKE_READY | CITY=Yaounde, SURFACE=500, BUDGET=10M | City, surface, budget |
| 3 | MINIMUM_SEARCH_READY | NEIGHBORHOOD=Mvog-Mbi, USAGE=habitation | Neighborhood + usage |
| 4 | **SEARCH LAUNCHED** | — | 3 parcels in Mvog-Mbi area |
| 5 | MINIMUM_MATCHING_READY | ACCESSIBILITE, TOPOGRAPHIE | Refine with access + topography |
| 6 | INTRODUCTION_READY | NOM, TELEPHONE | Contact info |
| 7 | VISIT_READY | GPS, VISITE_SOUHAITEE, BESOIN_GEOMETRE | Visit logistics |
| 8 | TRANSACTION_READY | NUM_TITRE, IDENTITE_SIGNATAIRES, NOTAIRE | Legal verification |

---

## 9. Commercial Example Walkthrough

### User: Looking for a boutique in Douala centre-ville

| Step | Readiness Level | Fields Collected | Action |
|------|-----------------|------------------|--------|
| 1 | INTENT_IDENTIFIED | TRANSACTION=boutique, TRANSACTION=location | Confirm commercial lease |
| 2 | MINIMUM_INTAKE_READY | VILLE=Douala, SURFACE_MIN=20, BUDGET=500k | City, surface, budget |
| 3 | MINIMUM_SEARCH_READY | QUARTIER=Bonanjo, ACTIVITE=vetements | Neighborhood + activity |
| 4 | **SEARCH LAUNCHED** | — | 3 boutiques found |
| 5 | MINIMUM_MATCHING_READY | VISIBILITE, FLUX | Refine with visibility + foot traffic |
| 6 | INTRODUCTION_READY | CONTACT_NOM, CONTACT_TELEPHONE | Contact info |
| 7 | VISIT_READY | DISPONIBILITE, ACCOMPAGNEMENT | Schedule visit |
| 8 | TRANSACTION_READY | PIECE_IDENTITE, REGISTRE, GARANTIE | Business registration + guarantee |

---

## 10. Financing Example Walkthrough

### User: Looking for a mortgage

| Step | Readiness Level | Fields Collected | Action |
|------|-----------------|------------------|--------|
| 1 | INTENT_IDENTIFIED | OBJET_FINANCEMENT=credit_immobilier | Confirm mortgage intent |
| 2 | MINIMUM_INTAKE_READY | MONTANT=15M, APPORT=5M, VILLE=Douala | Amount, down payment, city |
| 3 | MINIMUM_SEARCH_READY | TYPE_BIEN=appartement, PROFIL=salarie | Property type, profile |
| 4 | **SEARCH LAUNCHED** | — | Match with 3 lenders |
| 5 | MINIMUM_MATCHING_READY | REVENUS, GARANTIES, DUREE | Income, guarantees, duration |
| 6 | INTRODUCTION_READY | EMAIL, TELEPHONE | Contact for lender intro |
| 7 | TRANSACTION_READY | EMPLOYEUR, ANCIENNETE, DOCUMENTS | Full documentation |

---

## 11. Professional Service Example

### User: Looking for a plumber in Yaounde

| Step | Readiness Level | Fields Collected | Action |
|------|-----------------|------------------|--------|
| 1 | INTENT_IDENTIFIED | TYPE_PRESTATION=recherche_professionnel, SERVICE=plombier | Confirm service type |
| 2 | MINIMUM_INTAKE_READY | LOCALISATION=Yaounde | City |
| 3 | MINIMUM_SEARCH_READY | DESCRIPTION_BESOIN=fuite_eau, URGENCE=urgent_48h, DATE=demain | Description, urgency, date |
| 4 | **SEARCH LAUNCHED** | — | Match with 5 plumbers |
| 5 | MINIMUM_MATCHING_READY | TYPE_TRAVAUX, QUALIFICATION | Specific work + certification |
| 6 | INTRODUCTION_READY | NOM, TELEPHONE | User contact |
| 7 | TRANSACTION_READY | CONTRAT, DEVIS, PAIEMENT | Contract + quote + payment |

---

## Appendix A: Readiness Level Field Requirements by Matrix Family

### Residential Search (All 18 types)

| Level | Required |
|-------|----------|
| INTENT_IDENTIFIED | FLD-TRANSACTION, FLD-PROPERTY_TYPE |
| MINIMUM_INTAKE_READY | FLD-CITY, FLD-BUDGET_MAX |
| MINIMUM_SEARCH_READY | FLD-NEIGHBORHOOD, FLD-BUDGET_TYPE |
| MINIMUM_MATCHING_READY | Per-matrix: chambres, douches, cuisine, meublé |
| INTRODUCTION_READY | FLD-NOM, FLD-TELEPHONE, FLD-DISPONIBILITE, FLD-CANAL_PREFERE |
| VISIT_READY | Per-matrix: climatisation, sécurité, eau |
| TRANSACTION_READY | FLD-CAUTION, FLD-CHARGES (rent), FLD-FINANCING (buy) |

### Land Search (All 7 types)

| Level | Required |
|-------|----------|
| INTENT_IDENTIFIED | TRANSACTION, PROPERTY_TYPE |
| MINIMUM_INTAKE_READY | ville, surface, budget_total, usage_prevu |
| MINIMUM_SEARCH_READY | quartier, surface_min, loti/non-loti |
| MINIMUM_MATCHING_READY | type_document, accessibilite, topographie |
| INTRODUCTION_READY | contact_nom, contact_telephone |
| VISIT_READY | visite_souhaitee, disponibilite, coordonnees_gps |
| TRANSACTION_READY | num_titre, identite_signataires, besoin_notaire, source_financement |

### Commercial Property (All 21 types)

| Level | Required |
|-------|----------|
| INTENT_IDENTIFIED | transaction, type_bien |
| MINIMUM_INTAKE_READY | ville, surface_min, budget, activité_prévue |
| MINIMUM_SEARCH_READY | quartier, zone_commerciale |
| MINIMUM_MATCHING_READY | Per-matrix matching fields |
| INTRODUCTION_READY | contact_nom, contact_téléphone |
| VISIT_READY | disponibilité, accompagnement |
| TRANSACTION_READY | pièce_identité, registre, garantie |

### Financing Request (All 10 types)

| Level | Required |
|-------|----------|
| INTENT_IDENTIFIED | objet_financement |
| MINIMUM_INTAKE_READY | montant_recherche, apport_disponible, ville_projet, type_bien_projet |
| MINIMUM_SEARCH_READY | duree_souhaitee, statut_acquisition, profil_demandeur |
| MINIMUM_MATCHING_READY | revenus, garanties, cout_total_projet |
| INTRODUCTION_READY | email_contact, telephone_contact |
| VISIT_READY | (not typically applicable for financing) |
| TRANSACTION_READY | employeur/activité, documents, type_contrat |

### Professional Service (All 27 types)

| Level | Required |
|-------|----------|
| INTENT_IDENTIFIED | type_prestation, profession_type |
| MINIMUM_INTAKE_READY | localisation |
| MINIMUM_SEARCH_READY | description_besoin, urgence, date_souhaitee |
| MINIMUM_MATCHING_READY | Per-service matching criteria |
| INTRODUCTION_READY | identite_professionnel, contact |
| VISIT_READY | disponibilite, acces |
| TRANSACTION_READY | contrat_service, conditions_paiement |

### Real Estate Service (All 24 types)

| Level | Required |
|-------|----------|
| INTENT_IDENTIFIED | service_type |
| MINIMUM_INTAKE_READY | localisation, type_bien |
| MINIMUM_SEARCH_READY | description, urgence, date_souhaitee |
| MINIMUM_MATCHING_READY | Per-service matching criteria |
| INTRODUCTION_READY | contact_nom, contact_telephone |
| VISIT_READY | (per service type) |
| TRANSACTION_READY | contrat_signe, conditions_paiement |

---

**End of READINESS_LEVELS.md**
