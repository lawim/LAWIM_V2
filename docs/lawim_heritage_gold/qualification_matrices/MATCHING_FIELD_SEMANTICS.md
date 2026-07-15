# MATCHING FIELD SEMANTICS — Matching Roles, Scoring, and Behavior

**Document ID:** LAWIM-GOLD-QM-MATCHING-V1
**Status:** CANONICAL — Complete reference for all matching role definitions and scoring rules
**Date:** 2026-07-15

---

## Table of Contents

1. [Matching Role Definitions](#1-matching-role-definitions)
2. [Matching Score Framework](#2-matching-score-framework)
3. [Mapping Tables](#3-mapping-tables)
4. [Priority Boost Rules](#4-priority-boost-rules)
5. [Scoring Examples](#5-scoring-examples)
6. [Implementation Guide](#6-implementation-guide)
7. [Per-Property-Type Matching Semantics](#7-per-property-type-matching-semantics)
8. [Budget Tolerance by Transaction Type](#8-budget-tolerance-by-transaction-type)
9. [Role Interaction Rules](#9-role-interaction-rules)
10. [Appendix: Complete Field-to-Role Mapping](#10-appendix-complete-field-to-role-mapping)

---

## 1. Matching Role Definitions

Each field in the qualification matrices is assigned a matching role that defines how it behaves in the matching engine. There are nine distinct roles:

### 1.1 hard_constraint

| Attribute | Description |
|-----------|-------------|
| **Definition** | A field that MUST match exactly between the user's request and the property. If it does not match, the property is excluded from results. |
| **Behavior** | Binary filter: pass or exclude. No partial credit. If the property doesn't satisfy the constraint, it is removed from the candidate set entirely before scoring. |
| **Scoring Impact** | 0 or 100 (pass/fail). Failed constraints are not scored — the property is removed. |
| **Examples** | transaction (can't show buy results to a renter), city (wrong city = wrong city), property_type (studio ≠ 2-bedroom apartment), usage_prevu (commercial ≠ residential land) |
| **Channel Handling** | On WhatsApp: confirm hard constraints early. On Dashboard: enforce at form level. |
| **Priority** | Evaluated FIRST, before any other matching logic. |

**When to use**: Fields where mismatch fundamentally breaks the match intent.

### 1.2 soft_constraint

| Attribute | Description |
|-----------|-------------|
| **Definition** | A field that represents a strong preference. Properties that don't match are NOT excluded but receive a score penalty. |
| **Behavior** | Continuous scoring factor. Missing or mismatched values reduce the match score proportionally. |
| **Scoring Impact** | 0-100% of the field's weight. If budget tolerance ±15%: within range = 100% score, outside = score decreases linearly to 0%. |
| **Examples** | budget (±20% rent, ±15% buy), neighborhood (nearby quartiers score 70%), chambres (2 vs 3 → partial score) |
| **Typical Weights** | 10-25% of total match score. |

**When to use**: Fields where the user has a preference but would consider alternatives.

### 1.3 ranking_preference

| Attribute | Description |
|-----------|-------------|
| **Definition** | A field that is used ONLY to rank results, never to filter. Properties with this feature matching rank higher than those without. |
| **Behavior** | Tie-breaker/ranking signal. Does not exclude. Adds a bonus to the base match score. |
| **Scoring Impact** | +0 to +N points (typically +5 to +15 depending on importance). |
| **Examples** | etage (preferred floor), balcon (nice to have), parking (preferred but not required), flux_passage (for boutique), visibilité (for shop) |
| **When to Collect** | Only after search results are shown and user wants refinement. |

**When to use**: Amenities, preferences, and nice-to-haves that should influence ordering but never exclusion.

### 1.4 exclusion

| Attribute | Description |
|-----------|-------------|
| **Definition** | Properties matching this criterion are explicitly excluded from results. The opposite of a requirement — it's a "do not show" signal. |
| **Behavior** | If property matches the exclusion criteria → score = 0, property removed from results. |
| **Scoring Impact** | Binary: excluded or not excluded. |
| **Examples** | Previously rejected properties (user said "no" to this property), properties the user has already visited and declined, neighborhoods the user explicitly ruled out |
| **Lifecycle** | Typically comes from user feedback AFTER seeing results, not from initial qualification. |

**When to use**: User rejection feedback, negative preferences. Not for initial criteria.

### 1.5 boost

| Attribute | Description |
|-----------|-------------|
| **Definition** | A field that, when matched, applies a fixed score boost above the base matching score. |
| **Behavior** | Additive bonus to match score. Does not exclude non-matching properties. |
| **Scoring Impact** | Fixed values: +25, +20, +15, +10 (defined per field). |
| **Examples** | exact_neighborhood_match (+25), exact_city_match (+20), budget_within_range (+15), title_foncier (+10), diaspora_investor (+20) |
| **Stacking** | Multiple boosts can apply simultaneously. a property in exact neighborhood + exact city + budget within range = +25+20+15 = +60 boost. |
| **Cap** | Total boost is capped at +50 to prevent over-scoring. |

**When to use**: Specific high-value matches that should be strongly preferred.

### 1.6 penalty

| Attribute | Description |
|-----------|-------------|
| **Definition** | A field that, when missing or mismatched, applies a fixed score penalty. |
| **Behavior** | Subtractive from match score. Does not exclude (unless penalty is large enough to drop score below threshold). |
| **Scoring Impact** | Fixed values: -20, -10, -5 (defined per field). |
| **Examples** | missing_budget (-10), unclear_location (-10), spam_like_message (-50), missing_neighborhood (-5), missed_visit (-25), incomplete_documents (-30) |
| **Cumulative** | Multiple penalties cumulate. A lead with missing_budget (-10) and unclear_location (-10) starts at 80 before any positive scoring. |
| **Floor** | Score cannot go below 0 regardless of penalties. |

**When to use**: Missing critical information, negative signals, undesirable behaviors.

### 1.7 informational_only

| Attribute | Description |
|-----------|-------------|
| **Definition** | A field that is collected for display, context, or CRM purposes. It does NOT affect match score in any way. |
| **Behavior** | Stored in the lead profile. May be shown to agents or property holders. Never used in scoring algorithms. |
| **Scoring Impact** | 0 (no effect). |
| **Examples** | FLD-NOM (name — informational only for introduction), FLD-EMAIL (for follow-up), FLD-LANGUE (language preference), FLD-ZONE (zone description), derived standing |
| **When to Collect** | When needed for the introduction or transaction stage. Never before search. |

**When to use**: Demographic, contact, descriptive, and derived fields that don't influence property matching.

### 1.8 verification_only

| Attribute | Description |
|-----------|-------------|
| **Definition** | A field that is used ONLY for verification purposes at transaction time. It does NOT affect matching. |
| **Behavior** | Verified at transaction stage. If verification fails, transaction is blocked. |
| **Scoring Impact** | 0 (no effect on match score). |
| **Examples** | FLD-TELEPHONE (verify before contact), FLD-NUM_TITRE (verify title validity), FLD-BORNAGE (verify boundary survey), FLD-CERTIFICAT_URBANISME (verify planning permission) |
| **Transaction Blocking** | If verification_only field fails validation, the transaction level cannot be reached. |

**When to use**: Legal, documentary, and identity fields that must be verified but don't affect matching.

### 1.9 transaction_blocker

| Attribute | Description |
|-----------|-------------|
| **Definition** | A field that must be resolved before a transaction can proceed. These are not matching fields but transaction-readiness gates. |
| **Behavior** | If unresolved, the system cannot advance to TRANSACTION_READY. Must be collected and validated at transaction stage. |
| **Scoring Impact** | 0 (no effect on match score). However, properties that cannot satisfy transaction blockers may be deprioritized. |
| **Examples** | FLD-CAUTION (security deposit — must be agreed), FLD-FINANCING (financing must be secured), FLD-LITIGES_CONNUS (known disputes must be resolved), FLD-HYPOTHEQUE (mortgage must be cleared) |
| **Resolution** | Requires action from user, property holder, or third party (notary, bank). |

**When to use**: Financial, legal, and documentary requirements that are preconditions for closing.

---

## 2. Matching Score Framework

### Base Score Calculation

```python
total_score = match_score + boost_total - penalty_total

match_score = Σ(field_weight_i * field_match_i) for all matching fields
boost_total = Σ(boost_values) capped at +50
penalty_total = Σ(penalty_values) floored at 0
```

### Weight Distribution by Field Category

| Category | Weight | Fields |
|----------|--------|--------|
| Geographical | 30-55% | CITY, NEIGHBORHOOD, ZONE |
| Budget | 20-25% | BUDGET_MAX, BUDGET_TYPE, BUDGET_NEGOTIABLE |
| Property Type | 10-15% | PROPERTY_TYPE, CHAMBRES, DOUCHES, SURFACE |
| Amenities | 5-15% | PARKING, CLIMATISATION, INTERNET, etc. |
| Title/Legal | 0-10% | TITLE_STATUS, DOCUMENTS |

### Weight Distribution by Transaction Type

| Transaction | Geographical | Budget | Property | Amenities | Legal |
|-------------|-------------|--------|----------|-----------|-------|
| RENT | 35% | 30% | 25% | 10% | 0% |
| BUY | 30% | 25% | 25% | 10% | 10% |
| INVEST | 25% | 30% | 20% | 10% | 15% |
| LAND_BUY | 30% | 25% | 15% | 5% | 25% |
| FINANCE | 20% | 35% | 20% | 0% | 25% |

### Normalized Score Formula

```python
def calculate_match(lead, property):
    # Base score from weighted dimensions
    score = 0
    
    # 1. Geographical score (max 30-55% depending on type)
    geo_score = 0
    if lead.city == property.city:
        geo_score += 0.30  # city weight
    if lead.neighborhood == property.neighborhood:
        geo_score += 0.25  # neighborhood weight
    elif lead.neighborhood in property.nearby_neighborhoods:
        geo_score += 0.15  # nearby neighborhood (partial)
    score += geo_score * 100
    
    # 2. Budget score (max 20-30%)
    budget_tolerance = get_budget_tolerance(lead.transaction)
    budget_ratio = min(lead.budget_max / property.price,
                       property.price / lead.budget_max)
    if budget_ratio >= (1 - budget_tolerance):
        budget_score = 1.0
    else:
        budget_score = budget_ratio / (1 - budget_tolerance)
    score += budget_score * 25  # budget weight
    
    # 3. Property type score (max 10-25%)
    if lead.property_type == property.property_type:
        score += 15
    elif lead.property_type in property.alternative_types:
        score += 8
    
    # 4. Amenities score
    amenity_matches = count_matching(lead.amenities, property.amenities)
    amenity_score = (amenity_matches / len(lead.amenities)) * 10
    score += amenity_score
    
    # 5. Apply boosts
    score += calculate_boosts(lead, property)
    
    # 6. Apply penalties
    score -= calculate_penalties(lead, property)
    
    return max(0, min(100, score))
```

---

## 3. Mapping Tables

### 3.1 Field → Typical Matching Role by Property Type

| Field | Residential | Land | Commercial | Financing |
|-------|-------------|------|------------|-----------|
| transaction | hard_constraint | hard_constraint | hard_constraint | hard_constraint |
| property_type | hard_constraint | hard_constraint | hard_constraint | hard_constraint |
| city | hard_constraint | hard_constraint | hard_constraint | hard_constraint |
| neighborhood | soft_constraint | hard_constraint | soft_constraint | soft_constraint |
| budget | hard_constraint | hard_constraint | hard_constraint | hard_constraint |
| chambres | soft_constraint | N/A | N/A | N/A |
| douches | soft_constraint | N/A | N/A | N/A |
| cuisine | soft_constraint | N/A | soft_constraint | N/A |
| meublé | soft_constraint | N/A | soft_constraint | N/A |
| surface | ranking_preference | soft_constraint | hard_constraint | N/A |
| surface_terrain | ranking_preference | soft_constraint | N/A | N/A |
| etage | ranking_preference | N/A | soft_constraint | N/A |
| parking | soft_constraint | N/A | soft_constraint | N/A |
| climatisation | ranking_preference | N/A | ranking_preference | N/A |
| internet | ranking_preference | N/A | soft_constraint | N/A |
| usage_prevu | informational_only | hard_constraint | informational_only | N/A |
| titre_foncier | informational_only | hard_constraint | informational_only | verification_only |
| activité_prévue | N/A | N/A | hard_constraint | N/A |
| montant_recherche | N/A | N/A | N/A | hard_constraint |
| revenus | N/A | N/A | N/A | soft_constraint |
| garanties | N/A | N/A | N/A | soft_constraint |

### 3.2 Field → Budget Tolerance by Transaction Type

| Field | Rent | Buy | Invest | Notes |
|-------|------|-----|--------|-------|
| BUDGET_MAX | ±20% | ±15% | ±25% | Core budget tolerance |
| BUDGET_MIN | ±20% | ±15% | ±25% | Same tolerance as max |
| BUDGET_NEGOTIABLE | +10% extra | +5% extra | +15% extra | Extra flexibility if negotiable |
| CAUTION | ±0% (exact) | N/A | N/A | Security deposit is exact |
| CHARGES | Included/Not | N/A | N/A | Binary, no tolerance |
| RENDEMENT_ATTENDU | N/A | N/A | ±2% | Yield tolerance |
| MONTANT_RECHERCHE | N/A | N/A | N/A | ±10% (financing) |
| APPORT | N/A | ±10% | ±10% | Down payment flexibility |

### 3.3 Privacy Level to Matching Role Mapping

| Privacy Level | Allowed Matching Roles | Restrictions |
|---------------|----------------------|--------------|
| public | All roles | No restrictions on matching usage |
| private | informational_only, verification_only, soft_constraint | Must not be shared with unauthorized parties |
| sensitive | informational_only, verification_only | Cannot be used in scoring exposed to holder |
| confidential | verification_only, transaction_blocker | Only used for legal/transactional verification |

---

## 4. Priority Boost Rules

### Boost Definitions

| Condition | Boost | Applies To | Source |
|-----------|-------|------------|--------|
| exact_neighborhood_match | +25 | All residential, land | MATCHING_MODEL.md §3 |
| exact_city_match | +20 | All types | MATCHING_MODEL.md §3 |
| budget_within_range | +15 | All types | MATCHING_MODEL.md §3 |
| title_foncier (land title available) | +10 | Land, residential buy | MATCHING_MODEL.md §3 |
| diaspora_investor | +20 | Investment | MATCHING_MODEL.md §3 |
| urgent_request | +15 | All types | QUALIFICATION_MODEL.md §2 |
| cash_purchase | +15 | Buy transactions | QUALIFICATION_MODEL.md §2 |
| budget_detected (early signal) | +15 | All types | QUALIFICATION_MODEL.md §2 |
| city_detected (early signal) | +10 | All types | QUALIFICATION_MODEL.md §2 |
| neighborhood_detected (early) | +10 | All types | QUALIFICATION_MODEL.md §2 |
| matching_amenity (+per amenity) | +5 | Residential | EXPERT_PROPOSAL |
| multiple_positive_feedback | +10 | All types | EXPERT_PROPOSAL |
| professional_recommendation | +15 | Professional services | EXPERT_PROPOSAL |
| quick_response_time | +10 | All types | QUALIFICATION_MODEL.md |
| visit_intent confirmed | +20 | All types | QUALIFICATION_MODEL.md |

### Boost Stacking Rules

```
Maximum total boost: +50
Boosts from same category: non-cumulative (only highest applies)
Exact neighborhood (+25) and exact city (+20): BOTH apply = +45 total
Diaspora (+20) + budget_within_range (+15) = +35 total
Cap at +50: diaspora(+20) + exact_neighborhood(+25) + budget(+15) = +60 → capped to +50
```

### Boost Application Order

1. hard_constraint check (pass/fail) → excludes non-matching
2. base score calculation (weighted averages)
3. boost application (additive, capped)
4. penalty application (subtractive, floored)
5. threshold check (min 60/100 to show)

---

## 5. Scoring Examples

### Example 1: Perfect Match — Residential Rent

```
Lead: 2-bed apartment in Douala Bonapriso, max 150k/month
Property: 2-bed apartment in Douala Bonapriso, 140k/month

Geographical: city=Douala(30) + neighborhood=Bonapriso(25) = 55
Budget: 140k within ±20% of 150k → 25 points
Property type: apartment = 15 points
Amenities: (assume 2/3 match) = 6.7 points
Boosts: exact_neighborhood(+25) + exact_city(+20) + budget_within(+15) = +50(capped)

Total = 55 + 25 + 15 + 6.7 + 50 = 100+ (capped at 100)
Result: SHOW (score = 100)
```

### Example 2: Partial Match — Different Neighborhood

```
Lead: 2-bed apartment in Douala Bonapriso, max 150k/month
Property: 2-bed apartment in Douala Makepe, 130k/month

Geographical: city=Douala(30) + nearby_neighborhood=Makepe(15) = 45
Budget: 130k within ±20% → 25 points
Property type: apartment = 15 points
Amenities: (assume 2/3 match) = 6.7 points
Boosts: exact_city(+20) + budget_within(+15) = +35

Total = 45 + 25 + 15 + 6.7 + 35 = 126.7
Capped at 100.
Result: SHOW (score = 100, but ranked below Bonapriso properties)
```

### Example 3: Budget Mismatch — Below Minimum

```
Lead: 2-bed apartment in Douala Bonapriso, max 100k/month
Property: 2-bed apartment in Douala Bonapriso, 200k/month

Geographical: city=Douala(30) + neighborhood=Bonapriso(25) = 55
Budget: 200k is 100% over 100k → 25 * 0.5 = 12.5 points (linearly decreasing)
Property type: 15 points
Boosts: exact_neighborhood(+25) + exact_city(+20) = +45

Total = 55 + 12.5 + 15 + 0 + 45 = 127.5 → capped at 100
Result: SHOW but with warning "Budget may be insufficient for this property"
```

### Example 4: Hard Constraint Failure

```
Lead: 2-bed apartment in Douala, max 150k/month (RENT)
Property: 2-bed apartment for SALE in Douala, 15M

Hard constraint: transaction = RENT != BUY → FAIL
Result: NOT SHOWN (excluded by hard constraint)
```

### Example 5: Land with Title Preference

```
Lead: Terrain in Yaounde, 500m2, 10M, needs titre foncier
Property 1: Terrain in Yaounde, 450m2, 9.5M, with titre
Property 2: Terrain in Yaounde, 550m2, 9M, without titre

Property 1:
  Geographical: city=30 + neighborhood=25 = 55
  Budget: 9.5M within ±15% of 10M = 25
  Surface: 450 vs 500 → soft match (90%) = 13.5
  Title: titre foncier = hard constraint match = no exclusion
  Boosts: exact_city(+20) + title_foncier(+10) + budget(+15) = +45
  Total = 55 + 25 + 13.5 + 0 + 45 = 100+ → 100

Property 2:
  Title: no titre → hard constraint FAIL since user requires it
  → NOT SHOWN
```

---

## 6. Implementation Guide

### Matching Engine Flow

```
1. COLLECT user criteria (from qualification)
2. FILTER inventory by hard_constraints
3. SCORE remaining properties
4. APPLY boosts and penalties
5. RANK by total score
6. RETURN top N (max 10)
7. PRESENT to user with scores
8. COLLECT feedback (exclusions, refinements)
9. RE-RANK based on feedback
10. REPEAT from step 2 if new criteria added
```

### Role Evaluation Priority

```python
def evaluate_match(lead, property):
    # Phase 1: Hard constraints (binary pass/fail)
    for field in hard_constraint_fields:
        if not hard_match(lead[field], property[field]):
            return None  # Excluded
    
    # Phase 2: Hard matching for transaction_blocker
    for field in transaction_blocker_fields:
        if lead[field] and not verify_blocker(lead[field], property[field]):
            mark_as_blocked(property)
    
    # Phase 3: Soft constraints (scored)
    score = 0
    for field in soft_constraint_fields:
        match_ratio = soft_match(lead[field], property[field])
        score += match_ratio * field.weight
    
    # Phase 4: Ranking preferences (additive)
    for field in ranking_preference_fields:
        if preference_match(lead[field], property[field]):
            score += field.rank_bonus
    
    # Phase 5: Boosts
    boost = calculate_boosts(lead, property)
    score += min(boost, 50)
    
    # Phase 6: Penalties
    penalty = calculate_penalties(lead, property)
    score = max(0, score - penalty)
    
    return min(100, score)
```

### Threshold Enforcement

```python
def should_show_score(score):
    return score >= 60  # Minimum threshold from MATCHING_MODEL.md §4

def get_top_results(properties, limit=10):
    scored = [p for p in properties if p.score >= 60]
    return sorted(scored, key=lambda p: p.score, reverse=True)[:limit]
```

---

## 7. Per-Property-Type Matching Semantics

### Residential

| Property Type | Key hard_constraints | Key soft_constraints | Key boost triggers |
|---------------|---------------------|---------------------|-------------------|
| chambre_simple | city, budget | neighborhood, douche, cuisine | exact_neighborhood, budget_within |
| chambre_moderne | city, budget | neighborhood, cuisine | exact_neighborhood, budget_within |
| studio | city, budget | neighborhood, cuisine, meublé | exact_neighborhood |
| studio_moderne | city, budget | neighborhood, cuisine, etage | exact_neighborhood, exact_city |
| studio_meuble | city, budget | neighborhood, cuisine | exact_neighborhood |
| appartement_non_meuble | city, budget | chambres, douches, salons, cuisine | exact_neighborhood, exact_city |
| appartement_meuble | city, budget | chambres, douches, salons, cuisine | exact_neighborhood |
| villa | city, budget | chambres, douches, surface_terrain | exact_neighborhood, parking |
| colocation | city, budget | chambres, nombre_colocataires | exact_neighborhood |
| cite_universitaire | city, université | type_chambre | exact_university, budget_within |

### Land

| Land Type | Key hard_constraints | Key soft_constraints | Key boost/penalty |
|-----------|---------------------|---------------------|-------------------|
| terrain_titre | city, budget, usage, titre | surface, accessibilité | title_foncier(+10), exact_city(+20) |
| terrain_non_titre | city, budget, usage | surface, type_document | exact_city(+20), missing_title(-10) |
| terrain_loti | city, budget, usage | surface, lotissement | construction_ready(+15) |
| terrain_non_loti | city, budget, usage | surface, accessibilité | lower_price_advantage |
| titre_collectif | city, budget, usage | surface, signataires | exact_city(+20) |
| titre_individuel | city, budget, usage | surface, titre_verification | title_foncier(+10), exact_city(+20) |
| sous_morcellement | city, budget, usage | surface, avancement | subdivision_progress(+15) |

### Commercial

| Commercial Type | Key hard_constraints | Key soft_constraints | Key boost triggers |
|----------------|---------------------|---------------------|-------------------|
| boutique | activité, surface, ville, budget | quartier, zone, visibilité, flux | exact_city, exact_quartier, high_visibility |
| bureau | surface, ville, budget | quartier, étage, accès_pmr, employés | exact_city, parking, PMR |
| local_commercial | activité, surface, ville, budget | quartier, hauteur, visibilité | exact_city, high_traffic |
| magasin | activité, surface, ville, budget | quartier, visibilité, parking | exact_city, high_foot_traffic |
| restaurant | activité, surface, ville, budget | quartier, flux, licence, terrasse | high_visibility, parking, licence |
| entrepot | surface, ville, budget, accès | hauteur, quai_chargement | vehicle_access, ceiling_height |

---

## 8. Budget Tolerance by Transaction Type

### Core Tolerances

| Transaction Type | Tolerance | Behavior |
|-----------------|-----------|----------|
| RENT | ±20% | Monthly rent. Property within ±20% of max budget = full score. Beyond ±20% = linear decrease. |
| BUY | ±15% | Total price. Property within ±15% of max budget = full score. Beyond = decrease. |
| INVEST | ±25% | Investment budget. Wider range acceptable for opportunistic investors. |
| LAND_BUY | ±15% | Same as BUY for land. |
| FINANCE | ±10% | Financing amount; lenders have stricter criteria. |

### Tolerance Application Rules

```
Within tolerance → budget_score = 1.0
At tolerance boundary → budget_score = 1.0
Beyond tolerance → budget_score decreases linearly:
  For rent: over 20% → score = max(0, 1 - (excess/20%))
  For buy: over 15% → score = max(0, 1 - (excess/15%))
  For invest: over 25% → score = max(0, 1 - (excess/25%))
```

### Edge Cases

| Scenario | Handling |
|----------|----------|
| No budget provided | Penalty: missing_budget(-10); search not launched |
| Budget is range (min-max) | Use max for hard constraint, min for soft scoring |
| Budget is "no limit" | Score budget at 1.0; no penalty |
| Currency mismatch | Convert to XAF; apply tolerance |
| Budget negotiable=True | Add +5% effective tolerance |

---

## 9. Role Interaction Rules

### Conflict Resolution

When a field could have multiple roles depending on context:

```yaml
priority_order:
  1. hard_constraint       # Most restrictive, evaluated first
  2. transaction_blocker    # Blocks transaction, not matching
  3. exclusion             # Explicit negative preference
  4. soft_constraint       # Strong preference
  5. boost                 # Positive signal
  6. penalty               # Negative signal
  7. ranking_preference    # Tie-breaker
  8. verification_only     # Transaction verification
  9. informational_only    # No scoring impact
```

### Role Combination Rules

| Combination | Result | Example |
|-------------|--------|---------|
| hard_constraint + boost | Both apply: field filters AND boosts when matched | city: hard_constraint for filtering + exact_city boost for scoring |
| soft_constraint + penalty | Both apply: mismatch penalizes, match rewards | budget: soft match + missing_budget penalty |
| informational_only + anything | informational_only overrides | Standing: informational_only even if budget suggests it |
| verification_only + transaction_blocker | Both apply: verify AND block if fails | num_titre: verify validity + block if invalid |

---

## 10. Appendix: Complete Field-to-Role Mapping

### Residential Search Fields

| FIELD-ID | Default Role | Rent Role | Buy Role | Notes |
|----------|-------------|-----------|----------|-------|
| FLD-TRANSACTION | hard_constraint | hard_constraint | hard_constraint | Different transactions can't match |
| FLD-INTENT | informational_only | informational_only | informational_only | Used for lead classification |
| FLD-PROPERTY_TYPE | hard_constraint | hard_constraint | hard_constraint | Type mismatch = no match |
| FLD-CITY | hard_constraint | hard_constraint | hard_constraint | City mismatch = no match |
| FLD-NEIGHBORHOOD | soft_constraint | soft_constraint | soft_constraint | Nearby neighborhoods partial credit |
| FLD-ZONE | informational_only | informational_only | informational_only | Free text zone description |
| FLD-BUDGET_MAX | hard_constraint | hard_constraint (±20%) | hard_constraint (±15%) | Budget tolerance applies |
| FLD-BUDGET_MIN | soft_constraint | soft_constraint | soft_constraint | Lower bound of range |
| FLD-BUDGET_TYPE | informational_only | informational_only | informational_only | Derived, no scoring |
| FLD-BUDGET_NEGOTIABLE | soft_constraint | soft_constraint | soft_constraint | Adds effective tolerance |
| FLD-CHAMBRES | soft_constraint | soft_constraint | soft_constraint | Closest match if not exact |
| FLD-DOUCHES | soft_constraint | soft_constraint | soft_constraint | |
| FLD-SALONS | ranking_preference | ranking_preference | ranking_preference | |
| FLD-CUISINE | soft_constraint | soft_constraint | soft_constraint | |
| FLD-MEUBLE | soft_constraint | soft_constraint | soft_constraint | |
| FLD-SURFACE | ranking_preference | ranking_preference | soft_constraint | More important for buy |
| FLD-SURFACE_TERRAIN | ranking_preference | N/A | ranking_preference | Villa/land only |
| FLD-ETAGE | ranking_preference | ranking_preference | ranking_preference | |
| FLD-ASCENSEUR | ranking_preference | ranking_preference | ranking_preference | Conditional on etage |
| FLD-PARKING | soft_constraint | soft_constraint | soft_constraint | |
| FLD-COUR | ranking_preference | ranking_preference | ranking_preference | |
| FLD-CLOTURE | soft_constraint | soft_constraint | soft_constraint | |
| FLD-BALCON | ranking_preference | ranking_preference | ranking_preference | |
| FLD-JARDIN | ranking_preference | ranking_preference | ranking_preference | |
| FLD-PISCINE | ranking_preference | ranking_preference | ranking_preference | Luxury segment |
| FLD-CLIMATISATION | ranking_preference | ranking_preference | ranking_preference | Conditional on climate |
| FLD-GROUPE_ELECTROGENE | boost (+10) | boost (+10) | boost (+10) | |
| FLD-FORAGE | boost (+10) | boost (+10) | boost (+10) | |
| FLD-INTERNET | ranking_preference | ranking_preference | ranking_preference | |
| FLD-SECURITE | soft_constraint | soft_constraint | soft_constraint | |
| FLD-GARDIENNAGE | boost (+10) | boost (+10) | boost (+10) | |
| FLD-EAU | soft_constraint | soft_constraint | soft_constraint | |
| FLD-ELECTRICITE | soft_constraint | soft_constraint | soft_constraint | |
| FLD-ACCES_ROUTE | ranking_preference | ranking_preference | ranking_preference | |
| FLD-DISPONIBILITE | soft_constraint | soft_constraint | soft_constraint | |
| FLD-DELAI | ranking_preference | ranking_preference | ranking_preference | |
| FLD-URGENCE | ranking_preference | ranking_preference | ranking_preference | |
| FLD-CAUTION | transaction_blocker | transaction_blocker | N/A | Rent only |
| FLD-CHARGES | soft_constraint | soft_constraint | N/A | Rent only |
| FLD-FINANCING | transaction_blocker | N/A | transaction_blocker | Buy only |
| FLD-NOM | informational_only | informational_only | informational_only | |
| FLD-TELEPHONE | verification_only | verification_only | verification_only | |
| FLD-EMAIL | informational_only | informational_only | informational_only | |
| FLD-CANAL_PREFERE | informational_only | informational_only | informational_only | |
| FLD-LANGUE | informational_only | informational_only | informational_only | |
| FLD-PROXIMITY_PREFERENCES | ranking_preference | ranking_preference | ranking_preference | |
| FLD-MOBILITY | soft_constraint | soft_constraint | soft_constraint | |

### Land Search Fields

| FIELD-ID | Role | Notes |
|----------|------|-------|
| ville | hard_constraint | City is required |
| quartier | hard_constraint | Neighborhood is required for land |
| surface | soft_constraint | ±30% tolerance |
| budget_total | hard_constraint | ±15% tolerance |
| usage_prevu | hard_constraint | Must match intended use |
| titre_requis | hard_constraint | If user requires it, must match |
| type_document | soft_constraint | Some documents better than none |
| num_titre | verification_only | Verified at transaction |
| accessibilite | ranking_preference | Better access = higher rank |
| viabilisation_eau | soft_constraint | Preferred |
| viabilisation_electricite | soft_constraint | Preferred |
| topographie | soft_constraint | Flat preferred |
| inondable | soft_constraint | Non-inondable preferred |
| occupation_actuelle | informational_only | Informational |
| litiges_connus | transaction_blocker | Blocks transaction if present |
| hypotheque | transaction_blocker | Blocks transaction if present |

---

**End of MATCHING_FIELD_SEMANTICS.md**
