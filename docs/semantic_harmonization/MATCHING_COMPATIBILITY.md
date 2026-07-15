# Matching Compatibility — H0.5 → H1 → Heritage Gold

**Document:** Semantic Harmonization — Matching Model Compatibility Analysis
**Date:** 2026-07-15
**Status:** CANONICAL
**Sources:**
- `docs/lawim_heritage_gold/MATCHING_MODEL.md` (Heritage Gold — validated matching knowledge)
- `docs/knowledge_execution/MATCHING_EXECUTION_ARCHITECTURE.md` (H1 Matching Engine architecture)
- `docs/knowledge_execution/MATCHING_SCORE_CONTRACT.md` (H1 scoring contract with H0.5 integration)
- `docs/knowledge_execution/MATCHING_SCORE_CONTRACT.md` (H0.5 integration sections §0.1–§0.7)
- `docs/knowledge_execution/REMATCHING_POLICY.md` (H1 rematching policy)
- `docs/knowledge_execution/PROXIMITY_SCORING_MODEL.md` (H1 geographic scoring)
- `docs/knowledge_execution/CRM_PIPELINE_CONTRACT.md` (H1 CRM pipeline)

---

## 1. Overview

This document verifies compatibility between three layers of the LAWIM matching model:

- **H0.5** — Semantic field roles (`matching_semantics.json`, `field_dictionary.json`, `MATCHING_FIELD_SEMANTICS.md`). Defines per-field matching roles, weight distributions per transaction type, budget tolerances, boost/penalty rules, and thresholds.
- **H1** — Knowledge Execution Architecture (`MATCHING_EXECUTION_ARCHITECTURE.md`, `MATCHING_SCORE_CONTRACT.md`, `REMATCHING_POLICY.md`, `PROXIMITY_SCORING_MODEL.md`, `CRM_PIPELINE_CONTRACT.md`). Defines engine components, scoring pipeline, rematching, geographic scoring, and CRM pipeline.
- **Heritage Gold** — Validated legacy knowledge (`docs/lawim_heritage_gold/MATCHING_MODEL.md`). The Gold standard for matching rules extracted from legacy JSON/config files.

The analysis covers role mapping, weight distribution, budget tolerance, boost/penalty rules, scoring formula, thresholds, exclusion rules, rematching, geographic scoring, CRM scoring, and gap analysis.

**Current LAWIM_V2 codebase status:** No matching engine is implemented in code. All matching architecture exists only in H1 documents. This compatibility analysis validates that the H1 documents can serve as a complete specification for implementation.

---

## 2. H0.5 Matching Role → H1 Engine Component Mapping

### 2.1 Mapping Table

| H0.5 Matching Role | H1 Engine Component | Behavior in H1 | Mapping Status |
|---------------------|---------------------|----------------|----------------|
| `hard_constraint` | Constraint Enforcer (§2.3) | Binary pass/fail before scoring. Excluded if violated. | ✅ **FULL** |
| `soft_constraint` | Dimension Evaluator (§2.1) | Score contribution 0–100% of field weight. Weighted scoring within dimension. | ✅ **FULL** |
| `ranking_preference` | Score Calculator (§2.2) — Bonus | +5 to +15 additive bonus to dimension score. | ⚠️ **PARTIAL** — H1 documents +5 to +15 range, but H0.5 does not specify per-field bonus values for ranking_preference; these must be defined per field in `matching_semantics.json` field_mappings. |
| `boost` | Boost Applier (§2.4) | Fixed additive +10 to +25, capped at +50 total. Exact values match per condition. | ✅ **FULL** |
| `penalty` | Penalty Applier (§2.5) | Fixed subtractive -5 to -50. Values: -10 (missing budget), -10 (unclear location), -50 (spam), -5 (missing neighborhood). | ✅ **FULL** |
| `exclusion` | Exclusion Engine (§2.6) | Properties matching exclusion criteria removed before ranking. | ✅ **FULL** |
| `informational_only` | Explanation Builder (§2.8) | No scoring impact. Used only for display/recommendation. | ✅ **FULL** |
| `verification_only` | Audit / Transaction Engine (not in scope) | No scoring. Verified at transaction readiness time. | ✅ **FULL** (delegated to transaction engine) |
| `transaction_blocker` | Transaction readiness gate (readiness model) | Blocks TRANSACTION_READY if unresolved. | ✅ **FULL** (delegated to readiness/transaction engine) |

### 2.2 Mapping Details

**hard_constraint → Constraint Enforcer:**
- H0.5 fields marked as `hard_constraint` (e.g., `transaction_type`, `property_type`, `city`, `budget_max` with tolerance) are enforced by the Constraint Enforcer (MATCH-034).
- Violation = exclusion with no score calculation.
- Non-compensation principle (MATCH-013) applies: a critical field deficiency cannot be compensated.

**soft_constraint → Dimension Evaluator:**
- H0.5 fields marked as `soft_constraint` (e.g., `neighborhood`, `budget_min`, `chambres`, `douches`, `cuisine`, `meuble`, `parking`) are evaluated by the Dimension Evaluator within their respective score families.
- These contribute 0–100% of their field weight based on match quality.

**ranking_preference → Score Calculator (bonus):**
- H0.5 fields marked as `ranking_preference` (e.g., `etage`, `surface`) add a +5 to +15 bonus to the property dimension score.
- These influence ranking but not exclusion.

**boost → Boost Applier:**
- H0.5 fields with explicit boost conditions (exact_neighborhood_match, exact_city_match, budget_within_range, title_foncier, diaspora_investor, cash_purchase, visit_intent) map directly to the Boost Applier.
- Boost cap of +50 from H0.5 is enforced in H1 (§0.5).

**penalty → Penalty Applier:**
- H0.5 penaly factors (missing_budget, unclear_location, spam_like, missing_neighborhood) map to the Penalty Applier.
- Values match: -10, -10, -50, -5.

**exclusion → Exclusion Engine:**
- The `exclusion` role from H0.5 (properties matching this are excluded) is handled by the H1 Exclusion Engine which checks status, blacklist, budget, city, operation compatibility, and type compatibility.

**informational_only → Explanation Builder:**
- H0.5 `informational_only` fields (e.g., `intent`) contribute to explanation context.
- No score impact.

**verification_only → Audit / Transaction Engine:**
- H0.5 `verification_only` fields are not evaluated during matching. They are verified at transaction readiness time by the Transaction Engine.
- No matching engine component modification needed.

**transaction_blocker → Transaction Readiness Gate:**
- H0.5 fields marked `transaction_blocker` (e.g., `financing`) prevent the TRANSACTION_READY state transition.
- The matching engine passes these through without evaluation; the readiness model enforces the gate.

### 2.3 Verification: All 9 H0.5 Roles Have H1 Representation

| H0.5 Role | H1 Representation | Verified |
|-----------|-------------------|----------|
| `hard_constraint` | Constraint Enforcer (§2.3) | ✅ |
| `soft_constraint` | Dimension Evaluator (§2.1) | ✅ |
| `ranking_preference` | Score Calculator — Bonus (§2.2) | ✅ |
| `exclusion` | Exclusion Engine (§2.6) | ✅ |
| `boost` | Boost Applier (§2.4) | ✅ |
| `penalty` | Penalty Applier (§2.5) | ✅ |
| `informational_only` | Explanation Builder (§2.8) | ✅ |
| `verification_only` | Audit / Transaction Engine (delegated) | ✅ |
| `transaction_blocker` | Transaction Readiness Gate (delegated) | ✅ |

**Verdict:** All 9 H0.5 matching roles have a corresponding representation in the H1 architecture. Roles either map directly to an engine component (Constraint Enforcer, Dimension Evaluator, Boost Applier, Penalty Applier, Exclusion Engine, Explanation Builder) or are delegated to external subsystems (Transaction Engine for verification_only and transaction_blocker).

---

## 3. Weight Distribution Compatibility

### 3.1 Three Competing Weight Systems

Three different weight distributions coexist across H0.5, H1, and Heritage Gold:

**System A — H0.5 Per-Transaction-Type Weights** (from `matching_semantics.json` weight_distribution):

| Transaction Type | Geographical | Budget | Property | Amenities | Legal |
|-----------------|-------------|--------|----------|-----------|-------|
| RENT | 35% | 30% | 25% | 10% | 0% |
| BUY | 30% | 25% | 25% | 10% | 10% |
| INVEST | 25% | 30% | 20% | 10% | 15% |
| LAND_BUY | 30% | 25% | 15% | 5% | 25% |
| FINANCE | 20% | 35% | 20% | 0% | 25% |

**System B — H1 Fixed Decision Engine Weights** (from MATCHING_EXECUTION_ARCHITECTURE.md §2.2):

| Score Family | Weight |
|-------------|--------|
| Geographical | 26% |
| Budget | 20% |
| Property | 15% |
| Behavioral | 10% |
| Other (freshness, services, etc.) | 29% |

**System C — V1 JSON Weights** (Heritage Gold §1, MATCH-001):

| Dimension | Weight |
|-----------|--------|
| city | 30% |
| neighborhood | 25% |
| budget | 25% |
| property_type | 15% |
| title_status | 5% |

### 3.2 H0.5 → H1 Mapping

The H1 architecture (§0.3) defines the mapping from H0.5 weight distribution to H1 score families:

```
Geographical Score  ← Geographical weight (e.g., 35% for RENT)
Budget Score         ← Budget weight (e.g., 30% for RENT)
Property Score       ← Property weight (e.g., 25% for RENT)
Behavioral Score     ← Derived from urgency + visit intent (not in H0.5 weights → fixed at 10%)
Other Score          ← Amenities + Legal weight (e.g., 10% + 0% = 10% for RENT)
```

The MATCHING_SCORE_CONTRACT (§0.3) confirms this mapping with:

```
function get_weight_distribution(transaction_type):
    weights = matching_semantics.weight_distribution[transaction_type]
    return {
        geographical: weights.geographical,
        budget: weights.budget,
        property: weights.property,
        behavioral: 0.10,  // H1 fixed, not in H0.5
        other: 1 - weights.geographical - weights.budget
              - weights.property - 0.10  // remaining is amenity + legal
    }
```

### 3.3 Compatibility Matrix

| Aspect | H0.5 | H1 | Heritage Gold (V1) | Compatible? | Resolution |
|--------|------|----|--------------------|-------------|------------|
| Weight source | Per-transaction-type dynamic | Fixed 26/20/15/10/29 | Fixed city=30/neighborhood=25/budget=25/type=15/title=5 | ⚠️ **INCOMPATIBLE** | H1 supersedes V1 per MATCHING_EXECUTION_ARCHITECTURE §0.8: **RESOLVED_BY_H05** — H0.5 dynamic weights supersede H1 fixed DE weights. |
| Behavioral weight | Not in H0.5 | 10% fixed | Not in V1 | ✅ **COMPATIBLE** | H0.5 does not define behavioral weight; H1 adds a fixed 10% behavioral component derived from urgency/visit intent signals. |
| Other weight | Amenities + Legal (varies by type: 0–25%) | 29% fixed | Not in V1 | ⚠️ **PARTIAL** | When H0.5 weights are active (RESOLVED_BY_H05), the "Other" weight = 1 − (geo + budget + property + 0.10). This produces values like 10% for RENT, 15% for BUY, 25% for INVEST — which differ from the H1 fixed 29%. |
| V1 legacy weights | City 30% = Geographical component, Neighborhood 25% = Geographical component | Geographical = 26% | City 30% + Neighborhood 25% = 55% geographical | ❌ **INCOMPATIBLE** | The V1 model splits geographical into city and neighborhood separately, while H1 aggregates them into a single Geographical family at 26%. See GM-WEIGHT-001. |

### 3.4 Verdict

- **H0.5 → H1 weight mapping is structurally compatible** via the `get_weight_distribution()` adapter function defined in MATCHING_SCORE_CONTRACT §0.3.
- **H1 fixed weights (26/20/15/10/29) are superseded** when H0.5 per-transaction-type weights are available (RESOLVED_BY_H05 per §0.8).
- **Heritage Gold V1 weights (30/25/25/15/5) are an older representation** that does not align with either H0.5 or H1. The V1 weights should be treated as deprecated once H0.5 weight distribution is fully live.
- **Gap GM-WEIGHT-001** (4 different weighting systems exist) is partially resolved by the RESOLVED_BY_H05 rule, but the coexistence of V1, DE, V5, and H0.5 weights creates confusion.

---

## 4. Budget Tolerance Compatibility

### 4.1 Tolerance Values

| Transaction Type | H0.5 Tolerance | H1 (Heritage Gold MATCH-003) | Heritage Gold V1 | Compatible? |
|-----------------|----------------|------------------------------|------------------|-------------|
| RENT | ±20% | ±20% | ±20% | ✅ **FULL** |
| BUY | ±15% | ±15% | ±15% | ✅ **FULL** |
| INVEST | ±25% | ±25% | ±25% | ✅ **FULL** |
| LAND_BUY | ±15% | Not defined | Not defined | ⚠️ **H1 MISSING** — H0.5 extends to LAND_BUY; H1 has no documented tolerance |
| FINANCE | ±10% | Not defined | Not defined | ⚠️ **H1 MISSING** — H0.5 extends to FINANCE; H1 has no documented tolerance |

### 4.2 Tolerance Application Logic

**H0.5** (from MATCHING_SCORE_CONTRACT §0.6):

```
is_within_tolerance(request, property):
    tolerance = matching_semantics.field_mappings.budget_max.tolerance[request.transaction_type]
    ratio = property.price / request.budget_max
    if ratio <= (1 + tolerance):
        return true  // Within or below max + tolerance
    // Above tolerance → linear decrease to 0 at 2× tolerance
    score_ratio = max(0, 1 - (ratio - (1 + tolerance)) / tolerance)
    return score_ratio  // Partial score
```

**H1** (from MATCHING_EXECUTION_ARCHITECTURE.md §4.3):

The budget dimension evaluates budget range match, tolerance check per transaction type, and flexibility test. The Constraint Enforcer (§2.3) excludes properties where "Budget outside tolerance (MATCH-003, MATCH-022)."

**Heritage Gold** (§2): Simple ±% tolerance per transaction type.

### 4.3 Compatibility Analysis

| Aspect | Compatible? | Notes |
|--------|-------------|-------|
| Core tolerance values (RENT/BUY/INVEST) | ✅ **FULL** | All three sources agree: RENT=±20%, BUY=±15%, INVEST=±25% |
| Extended transaction types (LAND_BUY, FINANCE) | ⚠️ **H1 GAP** | H1 must be updated to include LAND_BUY (±15%) and FINANCE (±10%) tolerances |
| Linear decrease above tolerance | ⚠️ **H1 NOT IMPLEMENTED** | H0.5 defines a linear decrease from 1× to 2× tolerance; H1 currently treats budget as binary pass/fail in Constraint Enforcer |
| Hard constraint vs flexible budget | ⚠️ **PARTIAL** | H0.5 marks budget_max as hard_constraint (with tolerance), budget_min as soft_constraint. H1 enforces budget in both Constraint Enforcer (binary) and Budget Dimension (scored). This dual treatment is compatible but must be coordinated. |

### 4.4 Verdict

Budget tolerances are **fully compatible for the core transaction types** (RENT, BUY, INVEST) across all three layers. H1 needs to be extended to document LAND_BUY and FINANCE tolerances from H0.5. The linear decrease logic (H0.5 §0.6) is an H1 implementation gap that must be coded.

---

## 5. Boost/Penalty Rule Compatibility

### 5.1 Boost Rules

| Boost Condition | H0.5 Value | H1 Value (MATCH-004 to MATCH-008) | Heritage Gold | Compatible? |
|----------------|-----------|-----------------------------------|---------------|-------------|
| exact_neighborhood_match | +25 | +25 ($2.4) | +25 ($3) | ✅ **FULL** |
| exact_city_match | +20 | +20 ($2.4) | +20 ($3) | ✅ **FULL** |
| budget_within_range | +15 | +15 ($2.4) | +15 ($3) | ✅ **FULL** |
| title_foncier_available | +10 | +10 ($2.4) | +10 ($3) | ✅ **FULL** |
| diaspora_investor | +20 | +20 ($2.4) | +20 ($3) | ✅ **FULL** |
| cash_purchase | +15 | Not in Boost Applier (§2.4) | Not in Gold | ⚠️ **H1 MISSING** — H0.5 lists cash_purchase (+15); H1 §2.4 does not include it. H1 is a subset; needs addition. |
| visit_intent_confirmed | +20 | Not in Boost Applier (§2.4) | Not in Gold | ⚠️ **H1 MISSING** — H0.5 lists visit_intent_confirmed (+20) for ALL. Must be added to H1 Boost Applier. |
| construction-ready_land | +15 | Not in Boost Applier (§2.4) | Not in Gold | ⚠️ **H1 MISSING** — H0.5 boost for LAND_SEARCH. Must be added. |
| high_visibility_commercial | +10 | Not in Boost Applier (§2.4) | Not in Gold | ⚠️ **H1 MISSING** — H0.5 boost for COMMERCIAL_SEARCH. Must be added. |
| V5 budget exact match | Not in H0.5 | +50 (MATCH-020) | +50 ($20) | ⚠️ **H0.5 MISSING** — V5 budget tiers are not in H0.5 boost_rules. Pre-dates this model. |
| V5 location match | Not in H0.5 | +40 (MATCH-020) | +40 ($20) | ⚠️ **H0.5 MISSING** — V5 location boost not in H0.5. |
| V5 property type match | Not in H0.5 | +10 (MATCH-020) | +10 ($20) | ⚠️ **H0.5 MISSING** — V5 type boost not in H0.5. |

### 5.2 Boost Cap

| Source | Cap Value | Compatible? |
|--------|-----------|-------------|
| H0.5 | +50 (`matching_semantics.json` `boost_cap`) | ✅ **FULL** — MATCHING_SCORE_CONTRACT §0.4 confirms H0.5 cap applies |
| H1 (§0.5) | +50 (from `matching_semantics.json` `boost_cap`) | ✅ |
| H1 (§2.4) | No explicit cap; boosts are additive | ⚠️ **IMPLICIT** — The final_score clamp to 100 provides an implicit cap |
| Heritage Gold | Not specified | — |

### 5.3 Penalty Rules

| Penalty Condition | H0.5 Value | H1 Value (§2.5) | Heritage Gold | Compatible? |
|------------------|-----------|-----------------|---------------|-------------|
| missing_budget | -10 | -10 (QUAL-003) | -10 ($23) | ✅ **FULL** |
| unclear_location | -10 | -10 (QUAL-003) | -10 ($23) | ✅ **FULL** |
| spam_like_message | -50 | -50 (QUAL-003) | -50 ($23) | ✅ **FULL** |
| missing_neighborhood (post-MINIMUM_INTAKE_READY) | -5 | Not in Penalty Applier (§2.5) | Not in Gold | ⚠️ **H1 MISSING** — H0.5 lists missing_neighborhood (-5); H1 §2.5 does not include it. |
| incomplete_property_data | Not in H0.5 | -5 per field (PROP-006) | Not in Gold | ⚠️ **H0.5 MISSING** — H1 adds this penalty not present in H0.5 |

### 5.4 Verdict

**Boosts:** Core boosts (neighborhood, city, budget, title, diaspora) are fully compatible across all three layers. H0.5 extends the boost list with 4 additional conditions (cash_purchase, visit_intent, construction-ready_land, high_visibility_commercial) not yet documented in H1 §2.4. V5 budget tier boosts (MATCH-020) are in H1 but not in H0.5 — these are legacy artifacts that should be reconciled.

**Penalties:** Core penalties (missing_budget, unclear_location, spam) are fully compatible. H0.5 adds missing_neighborhood (-5); H1 adds incomplete_property_data (-5). Both additions are minor and compatible in principle.

**Boost cap:** The +50 cap from H0.5 applies per architecture decision (MATCHING_EXECUTION_ARCHITECTURE §0.8). H1 must explicitly document this cap in §2.4 rather than relying on the implicit final_score clamp.

---

## 6. Scoring Formula Compatibility

### 6.1 Formula Comparison

**H0.5 Formula** (from `matching_semantics.json` `scoring_formula`):

```
total_score = match_score + boost_total - penalty_total
match_score = Σ(field_weight_i × field_match_i) for all matching fields
boost_total = min(Σ boost_values, 50)
penalty_total = max(Σ penalty_values, 0)
final_score = clamp(total_score, 0, 100)
```

**H1 Formula** (from MATCHING_EXECUTION_ARCHITECTURE.md §2.2):

```
global_score = (geographical_score × 0.26)
             + (budget_score × 0.20)
             + (property_score × 0.15)
             + (behavioral_score × 0.10)
             + (other_score × 0.29)

final_score = min(global_score + boost_total - penalty_total, 100)
final_score = max(final_score, 0)
```

**H1 Formula** (from MATCHING_SCORE_CONTRACT §3.4):

```
base_score = Σ(family_weight_i × family_score_i)
boost_total = Σ applicable_boosts
penalty_total = Σ applicable_penalties
final_score = clamp(base_score + boost_total - penalty_total, 0, 100)
```

### 6.2 Structural Compatibility

| Component | H0.5 | H1 | Compatible? |
|-----------|------|----|-------------|
| Base score computation | Σ(field_weight × field_match) — per-field aggregation | Σ(family_weight × family_score) — per-family aggregation | ✅ **FUNCTIONALLY EQUIVALENT** — Field-level scores aggregate into family scores; the formula is the same at different granularity. |
| Boost addition | + boost_total (capped at 50) | + boost_total (implicit cap at 100) | ✅ **COMPATIBLE** — Same addition. H0.5 cap explicit at 50; H1 cap implicit at 100 via clamp. |
| Penalty subtraction | − penalty_total | − penalty_total | ✅ **COMPATIBLE** |
| Clamping | clamp to [0, 100] | clamp to [0, 100] | ✅ **FULL** |
| Non-compensation | Not explicit in formula | global_score = 0 if critical violation | ⚠️ **PARTIAL** — H0.5 does not include non-compensation in scoring_formula; H1 enforces it in Constraint Enforcer before scoring. Compatible in practice (non-compensation prevents scoring entirely). |

### 6.3 Verdict

The scoring formulas are **fully compatible**. Both use an additive model:
```
final = clamp(base_score + boosts − penalties, 0, 100)
```

The difference in granularity (H0.5 per-field vs H1 per-family) is an implementation detail, not a semantic incompatibility. The H1 family-level aggregation is the correct architectural decomposition.

---

## 7. Threshold Compatibility

### 7.1 Match Score Thresholds

| Threshold | H0.5 | H1 (Heritage Gold) | Compatible? |
|-----------|------|--------------------|-------------|
| Minimum match score | 40/100 (show_in_results) | 60/100 (MATCH-009) | ⚠️ **CONTRADICTION** |
| Show in top 10 | 50/100 (show_in_top_10) | V1: max 10 results (MATCH-010), DE: max 5 first match | ⚠️ **DIFFERENT SEMANTICS** |
| Recommend for visit | 70/100 (recommend_for_visit) | Not explicitly in Gold/H1 thresholds | ⚠️ **H1 MISSING** |
| Recommend for transaction | 85/100 (recommend_for_transaction) | Not explicitly in Gold/H1 thresholds | ⚠️ **H1 MISSING** |
| Score < 60 behavior | Not defined (show at 40) | Never proposed (MATCH-011) | ⚠️ **CONTRADICTION** |

**Resolution** (from MATCHING_EXECUTION_ARCHITECTURE §0.8):

| H0.5 Rule | H1 Rule | Resolution |
|-----------|---------|------------|
| Score threshold: show at 40, recommend visit at 70 | Minimum threshold: 60/100 | **ARCHITECTURE_DECISION_RETAINED** — The 60/100 minimum applies for user-facing propositions; H0.5 >40 thresholds apply for internal ranking |

This means:
- Internal ranking uses H0.5 thresholds: show at 40, top 10 at 50, recommend visit at 70, recommend transaction at 85.
- User-facing propositions use H1 threshold: minimum 60/100.
- Properties with score 40–59 are visible internally (dashboard, agent view) but never proposed to the user.

### 7.2 Lead Temperature Thresholds

| Class | H0.5 | H1 (Heritage Gold V1) | H1 (Heritage Gold V5) | Compatible? |
|-------|------|-----------------------|-----------------------|-------------|
| HOT | Not defined in H0.5 matching | ≥ 80 | ≥ 0.8 | ✅ **MATCH** (different scale, same semantics) |
| WARM | Not defined in H0.5 matching | ≥ 60 | ≥ 0.5 | ✅ **MATCH** |
| COLD | Not defined in H0.5 matching | ≥ 40 | ≥ 0.3 | ✅ **MATCH** |
| LOW | Not defined in H0.5 matching | < 40 | — | ⚠️ **V5 LOW removed** |
| SPAM | Not defined in H0.5 matching | — | ≤ 0.2 | ⚠️ **V1 SPAM missing** |

**Critical Gap** (GM-THRESH-001): No documented conversion rule between V1 (0–100 integer) and V5 (0–1.0 float) thresholds.

### 7.3 Star Rating Thresholds

| Stars | Heritage Gold (V5) | H1 (MATCH-019) | Compatible? |
|-------|-------------------|-----------------|-------------|
| ⭐⭐⭐⭐⭐ (5/5) | ≥ 80 | ≥ 80 | ✅ **FULL** |
| ⭐⭐⭐⭐ (4/5) | ≥ 60 | ≥ 60 | ✅ **FULL** |
| ⭐⭐⭐ (3/5) | ≥ 40 | ≥ 40 | ✅ **FULL** |
| ⭐⭐ (2/5) | ≥ 20 | ≥ 20 | ✅ **FULL** |
| ⭐ (1/5) | < 20 | < 20 | ✅ **FULL** |

Star rating thresholds are **fully compatible** between Heritage Gold and H1. H0.5 does not define star ratings (pre-dates this model).

### 7.4 Other Thresholds

| Threshold | H0.5 | H1 | Heritage Gold | Compatible? |
|-----------|------|----|---------------|-------------|
| Top results limit | Not defined | 10 (MATCH-010) | 10 ($4) | ✅ **FULL** |
| First match max results | Not defined | 5 (MATCH-010) | — | ⚠️ **H0.5 NOT DEFINED** |
| Confidence threshold | Not defined | 0.70 (MATCH-031) | 0.70 ($17) | ✅ **FULL** (H1 = Gold) |

### 7.5 Verdict

Threshold compatibility is **partial** — the H0.5 multi-tier thresholds (show_at_40, top_10_at_50, recommend_visit_at_70, recommend_transaction_at_85) and H1's flat 60/100 minimum serve different purposes. The architecture decision (§0.8) correctly resolves this by applying H0.5 thresholds for internal ranking and H1's 60 for user-facing propositions. Lead temperature thresholds are compatible across V1 and V5 scales but lack a documented conversion rule. Star rating thresholds are fully compatible.

---

## 8. Exclusion Rule Compatibility

### 8.1 Exclusion Criteria

| Exclusion Criterion | H0.5 Source | H1 Exclusion Engine (§2.6) | Heritage Gold (§22) | Compatible? |
|--------------------|-------------|---------------------------|---------------------|-------------|
| Archived property | hard_constraint → status check | `property.status = ARCHIVED` | Property status = ARCHIVED | ✅ **FULL** |
| Sold property | hard_constraint → status check | `property.status = SOLD` | Property status = SOLD | ✅ **FULL** |
| Rented property | hard_constraint → status check | `property.status = RENTED` | Property status = RENTED | ✅ **FULL** |
| Inactive property | hard_constraint → status check | `property.status = INACTIVE` | Property status = INACTIVE | ✅ **FULL** |
| Previously rejected | exclusion role | Property in requester's blacklist (MATCH-017) | Previously rejected by requester | ✅ **FULL** |
| Budget outside tolerance | hard_constraint (budget_max) | Price exceeds tolerance (MATCH-003) | Budget outside tolerance | ✅ **FULL** |
| Different city (no multi-city) | hard_constraint (city) | City not in requested set (MATCH-022) | Different city (no multi-city request) | ✅ **FULL** |
| Incompatible operation | hard_constraint (transaction_type) | Buy/Rent/Invest mismatch (MATCH-023) | Not in Gold §22 (implied by budget tolerance) | ⚠️ **GOLD MISSING** — Heritage Gold §22 does not explicitly list operation incompatibility, but it's implied |
| Incompatible property type | hard_constraint (property_type) | Type not compatible with request (MATCH-023) | Not in Gold §22 | ⚠️ **GOLD MISSING** — Heritage Gold §22 does not list type incompatibility |

### 8.2 Exclusion Principle

Heritage Gold (§22) states: **"Rank, don't filter"** — properties should only be excluded for hard constraints. All others should be ranked. H1 (§2.6) repeats this principle verbatim.

### 8.3 Non-Compensation Principle (MATCH-013)

| Aspect | H1 | Heritage Gold | Compatible? |
|--------|----|---------------|-------------|
| Non-compensation | Critical field deficiency → score 0 regardless of other dimensions (MATCH-013) | Not explicitly in Gold §22 but documented in MATCH-013 | ✅ **FULL** (both reference MATCH-013) |
| Application | Applied before scoring | — | — |

### 8.4 Verdict

Exclusion rules are **fully compatible** between H0.5 (via hard_constraint and exclusion roles), H1 (Exclusion Engine), and Heritage Gold. Two Heritage Gold omissions (operation incompatibility, type incompatibility) are covered by H1's MATCH-023 and are minor documentation gaps, not logical contradictions.

---

## 9. Rematching Rule Compatibility

### 9.1 Rematching Triggers

| Trigger | Heritage Gold (§13) | H1 (REMATCHING_POLICY.md §2) | H0.5 | Compatible? |
|---------|-------------------|------------------------------|------|-------------|
| Auto-rematch J+7 | 7 days since last match | Per SLA table (24h–30d by property type, §2.5) | Not defined | ⚠️ **PARTIAL** — Gold says fixed J+7; H1 has SLA table per type. H1 supersedes with refined SLA. |
| Budget change | User updates budget | Budget modification (§2.1) | Not defined | ✅ **COMPATIBLE** (H1 includes Gold trigger) |
| Location change | User changes city/neighborhood | City change / Neighborhood change (§2.1) | Not defined | ✅ **COMPATIBLE** (H1 includes Gold trigger) |
| New property arrival | New listing matches profile | New publication (§2.2) | Not defined | ✅ **COMPATIBLE** (H1 includes Gold trigger) |
| Rejected property | User explicitly rejects | Property refusal / Definitely refused properties (§4) | Not defined | ✅ **COMPATIBLE** (H1 expands Gold trigger) |
| Context update | Any preference change | Property type change, new criterion, criterion removed, new preference (§2.1) | Not defined | ✅ **COMPATIBLE** (H1 expands Gold trigger) |
| Visit abandonment | Not in Gold | Visit abandonment (§2.1) | Not defined | ⚠️ **GOLD MISSING** |
| Price decrease | Not in Gold | Price decrease (§2.2) with MATCH-018 exception | Not defined | ⚠️ **GOLD MISSING** |
| Property modification | Not in Gold | Property details updated (§2.2) | Not defined | ⚠️ **GOLD MISSING** |
| Availability change | Not in Gold | Available/unavailable (§2.2) | Not defined | ⚠️ **GOLD MISSING** |
| Holder response | Not in Gold | Acceptance/Refusal/No response (§2.3) | Not defined | ⚠️ **GOLD MISSING** |

### 9.2 Rematching Algorithm

| Principle | Heritage Gold | H1 | Compatible? |
|-----------|---------------|----|-------------|
| Never restart from zero (MATCH-015) | Implied (rematching preserves context) | Explicit: preserve previous scores, only recalc affected dimensions (§3.1) | ✅ **FULL** |
| Only concerned dossiers (MATCH-016) | Implied | Explicit: only dossiers matching change scope (§3.2) | ✅ **FULL** |
| Refused never reproposed (MATCH-017) | Explicit | Explicit with 4 exceptions (§4.2) | ✅ **FULL** (H1 adds documented exceptions) |
| Learning from refusals (MATCH-014) | 3 refusals → reprioritization | 3 refusals → reprioritization with pattern analysis (§5) | ✅ **FULL** (H1 expands with pattern detection) |

### 9.3 Verdict

Rematching rules are **fully compatible** between Heritage Gold and H1. H1 (REMATCHING_POLICY.md) is a **superset** of the Heritage Gold rules, adding:
- SLA-tiered rematching cadence (24h–30d) instead of fixed J+7
- Property-side triggers (price change, modification, availability)
- Holder-side triggers (acceptance, refusal)
- Detailed refusal management with 4 documented exceptions (MATCH-018)
- Refusal pattern analysis

H0.5 does not define rematching rules — these are entirely in the H1 domain. No contradiction exists.

---

## 10. Geographic Scoring Compatibility

### 10.1 Proximity Levels

| Level | Label | Heritage Gold (§21) | H1 PROXIMITY_SCORING_MODEL (§2.5) | H1 MATCHING_EXECUTION_ARCHITECTURE (§2.1) | Compatible? |
|-------|-------|--------------------|------------------------------------|-------------------------------------------|-------------|
| 1 | Exact neighborhood | Maximal | 90–100 | Maximal | ✅ **FULL** |
| 2 | Accepted alternative | High | 75–89 | High | ✅ **FULL** |
| 3 | Neighboring district | Medium | 50–74 | Medium | ✅ **FULL** |
| 4 | Same city distant | Low | 25–49 | Low | ✅ **FULL** |
| 5 | Incompatible zone | Minimal | 0–24 | Minimal → Exclusion | ✅ **FULL** (H1 adds exclusion for strict incompatibility) |

### 10.2 Mobility Modes

| Mode | Heritage Gold (§21) | H1 PROXIMITY_SCORING_MODEL (§7) | H1 MATCHING_EXECUTION_ARCHITECTURE (§2.1) | Compatible? |
|------|--------------------|----------------------------------|-------------------------------------------|-------------|
| STRICT | Radius Boost: 0 | Requested neighborhood only (score unmodified) | Radius Boost: 0 | ✅ **FULL** |
| FLEXIBLE | Radius Boost: 0.5 | Alternative neighborhoods accepted (score × 0.95) | Radius Boost: 0.5 | ✅ **FULL** |
| VERY_FLEXIBLE | Radius Boost: 1.0 | Expanded zone (score × 0.85) | Radius Boost: 1.0 | ✅ **FULL** |

### 10.3 Score Components

| Component | Heritage Gold | H1 PROXIMITY_SCORING_MODEL | Compatible? |
|-----------|---------------|---------------------------|-------------|
| City score | Not in geographic scoring §21 (listed in V1 weights as 30%) | 30% (same city = 100, same region diff city = 50, different region = 0) | ✅ **COMPATIBLE** — Gold §21 focuses on proximity levels; city match is in V1 weights |
| Neighborhood score | Not separately weighted in geographic scoring §21 (V1 = 25%) | 25% (exact = 100, compatible = 75, same city diff = 50, incompatible = 0) | ✅ **COMPATIBLE** |
| GPS proximity | Not in §21 | 20% (normalized distance) | ⚠️ **GOLD NOT DEFINED** |
| Real distance score | Not in §21 | 15% (distance label factor × 100) | ⚠️ **GOLD NOT DEFINED** |
| Travel time score | Not in §21 | 10% (<15 min = 100, >60 min = 25) | ⚠️ **GOLD NOT DEFINED** |
| Affinity | §21 mentions (Yaoundé/Douala only) | §3.1 affinity scoring (exact=100, strong=85, same region=60, low=30, prohibited=0) | ✅ **COMPATIBLE** (H1 formalizes Gold's affinity concept) |

### 10.4 Verdict

Geographic scoring is **fully compatible** between Heritage Gold and H1. H1 (PROXIMITY_SCORING_MODEL.md) is a **superset** that formalizes all Gold geographic concepts:
- Same 5 proximity levels
- Same 3 mobility modes (STRICT, FLEXIBLE, VERY_FLEXIBLE)
- Same affinity matrix concept (Gold limitation: only Yaoundé/Douala — tracked as GM-AFFINITY-001)
- Adds detailed distance calculation methods (road > haversine > city-centroid > affinity)
- Adds travel time scoring

H0.5 does not define geographic scoring independently — it maps the `city` and `neighborhood` fields to the Geographical score family via the weight distribution.

---

## 11. CRM Scoring Compatibility

### 11.1 V5 CRM Scoring Factors

| Factor | Heritage Gold V5 (§12) | H1 CRM_PIPELINE_CONTRACT | Compatible? |
|--------|----------------------|--------------------------|-------------|
| base_interest (15%) | Factor 1: 0.15 (15%) | Not explicitly in CRM pipeline as separate factor | ⚠️ **NAME INCONSISTENCY** |
| property_type_match (20%) | Factor 2: 0.20 (20%) | factor `type_score` in scoring stage | ✅ **COMPATIBLE** (different naming, same semantics) |
| location_precision (20%) | Factor 3: 0.20 (20%) | factor `location_score` in scoring stage | ✅ **COMPATIBLE** |
| budget_presence (10%) | Factor 4: 0.10 (10%) | factor `budget_score` in scoring stage | ✅ **COMPATIBLE** |
| urgency_signal (15%) | Factor 5: 0.15 (15%) | factor `urgency_score` in scoring stage | ✅ **COMPATIBLE** |
| visit_intent (20%) | Factor 6: 0.20 (20%) | Not explicitly as separate factor | ⚠️ **PARTIAL** — Visit intent is detected but may be part of `engagement_score` |
| trust_signal (10%) | Factor 7: 0.10 (10%) | Not explicitly as separate factor | ⚠️ **PARTIAL** — Trust signals may feed into diaspora_score or engagement_score |

**H1 CRM Pipeline (§1, Stage 6 — scoring):**

```
factors: { type_score, budget_score, location_score, urgency_score,
           completeness_score, engagement_score, diaspora_score }
```

### 11.2 Factor Name Normalization

| Gold V5 Factor | H1 Pipeline Factor | Normalized Name | Status |
|---------------|-------------------|-----------------|--------|
| base_interest (15%) | completeness_score (?) | engagement_quality | ⚠️ Needs alignment |
| property_type_match (20%) | type_score | property_type_match | ✅ Direct match |
| location_precision (20%) | location_score | location_precision | ✅ Direct match |
| budget_presence (10%) | budget_score | budget_presence | ✅ Direct match |
| urgency_signal (15%) | urgency_score | urgency_signal | ✅ Direct match |
| visit_intent (20%) | engagement_score | visit_intent | ⚠️ Needs alignment |
| trust_signal (10%) | diaspora_score | trust_signal | ⚠️ Needs alignment |

### 11.3 Lead Classification

| Class | Heritage Gold V5 (§11) | H1 CRM Pipeline (§1, Stage 7) | Compatible? |
|-------|----------------------|-------------------------------|-------------|
| HOT | ≥ 0.8 | ≥ 0.8 (threshold mapping) | ✅ **FULL** |
| WARM | ≥ 0.5 | ≥ 0.5 | ✅ **FULL** |
| COLD | ≥ 0.3 | ≥ 0.3 | ✅ **FULL** |
| SPAM | ≤ 0.2 | ≤ 0.2 | ✅ **FULL** |

### 11.4 Lead Actions

| Class | Heritage Gold (§14) | H1 CRM Pipeline (§1, Stage 8 — routing) | Compatible? |
|-------|--------------------|----------------------------------------|-------------|
| HOT | `call_immediately` | call_immediately | ✅ **FULL** |
| WARM | `send_listings` | send_listings | ✅ **FULL** |
| COLD | `request_budget` | request_budget | ✅ **FULL** |
| LOW | `follow_up` | follow_up | ✅ **FULL** |
| SPAM | `ignore` | ignore | ✅ **FULL** |

### 11.5 Base Lead Scores

| Lead Type | Heritage Gold (§23) | H1 | Compatible? |
|-----------|--------------------|----|-------------|
| tenant | 40 | Not in H1 score contract | ⚠️ **H1 NOT DEFINED** |
| buyer | 60 | Not in H1 score contract | ⚠️ **H1 NOT DEFINED** |
| seller | 50 | Not in H1 score contract | ⚠️ **H1 NOT DEFINED** |
| investor | 80 | Not in H1 score contract | ⚠️ **H1 NOT DEFINED** |
| diaspora_investor | 95 | Not in H1 score contract | ⚠️ **H1 NOT DEFINED** |

### 11.6 Verdict

CRM scoring is **partially compatible**. The 7-factor V5 structure exists in both Heritage Gold and H1, but factor names differ and the mapping is not exact. The lead classification thresholds and actions are fully compatible. Base lead scores from Gold (§23) are not documented in H1 — these should be added to the CRM pipeline contract or the matching score contract.

---

## 12. Gap Analysis

### 12.1 Identified Gaps

| ID | Gap | Source | Impact | Layer | Severity |
|----|-----|--------|--------|-------|----------|
| MC-WEIGHT-001 | 3 weight systems coexist (H0.5 per-type, H1 fixed 26/20/15/10/29, V1 30/25/25/15/5) without clear deprecation path | §3 | Scoring inconsistency between old and new data | All | **HIGH** |
| MC-THRESH-001 | H0.5 thresholds (40/50/70/85) vs H1 60/100 for user-facing propositions — resolved by ARCHITECTURE_DECISION_RETAINED but implementation must enforce both | §7 | Complexity in dual-threshold system | H0.5→H1 | **MEDIUM** |
| MC-BOOST-001 | H0.5 lists 4 boosts not in H1 Boost Applier: cash_purchase (+15), visit_intent (+20), construction-ready_land (+15), high_visibility_commercial (+10) | §5.1 | Incomplete boost coverage | H0.5→H1 | **MEDIUM** |
| MC-BOOST-002 | V5 budget tiers (+50/+35/+20/+10) and V5 location (+40) and type (+10) boosts are in H1 but not in H0.5 | §5.1 | Legacy boosts not represented in modern model | H1→H0.5 | **LOW** |
| MC-PENALTY-001 | H0.5 lists missing_neighborhood (-5) not in H1 Penalty Applier | §5.3 | Incomplete penalty coverage | H0.5→H1 | **LOW** |
| MC-PENALTY-002 | H1 incomplete_property_data (-5) not in H0.5 | §5.3 | H1 penalty not in H0.5 | H1→H0.5 | **LOW** |
| MC-BUDGET-001 | H0.5 adds LAND_BUY (±15%) and FINANCE (±10%) tolerances not in H1 | §4 | Incomplete budget tolerance coverage | H0.5→H1 | **MEDIUM** |
| MC-BUDGET-002 | H0.5 linear decrease logic (1× to 2× tolerance) not implemented in H1 binary pass/fail | §4.2 | H1 currently treats budget as binary | H0.5→H1 | **MEDIUM** |
| MC-THRESH-V5 | No documented conversion rule between V1 (0–100) and V5 (0–1.0) lead scoring scales | §7.2 | Cannot reconcile lead scores across versions | Heritage Gold | **HIGH** (GM-THRESH-001 carryover) |
| MC-AFFINITY-001 | Affinity matrix only covers Yaoundé/Douala; no data for 8/10 priority cities | §10 | Geographic scoring incomplete for most cities | Heritage Gold | **HIGH** (GM-AFFINITY-001 carryover) |
| MC-CRM-001 | H1 CRM pipeline factors (completeness, engagement, diaspora) do not exactly match Gold V5 factors (base_interest, visit_intent, trust_signal) | §11.2 | Factor names need normalization | H1 | **MEDIUM** |
| MC-CRM-002 | Base lead scores (tenant=40, buyer=60, seller=50, investor=80, diaspora=95) from Gold §23 not documented in H1 | §11.5 | Base scores could be lost in transition | H1 | **MEDIUM** |
| MC-CODE-001 | Exclusion rules fully documented in H1, but 6 rejection rules documented vs 0 coded in legacy Python | §8 | Legacy code gap (GM-REJECT-001 carryover) | Heritage Gold | **HIGH** |
| MC-BEHAV-001 | Behavioral scoring dimension in H1 (urgency, visit intent, trust signals) has 4 behavior trackers declared, 0 coded | §6 | Behavioral scoring is specified but no implementation exists | H1 | **HIGH** (GM-BEHAV-001 carryover) |
| MC-PIPELINE-001 | 8-stage CRM pipeline in H1, only 5 implemented in legacy; context_enrichment and crm_routing stages missing | §11 | Pipeline incompleteness (GM-PIPE-001 carryover) | H1 | **MEDIUM** |
| MC-BOOST-CAP-001 | H1 §2.4 does not explicitly document the +50 boost cap; relies on implicit final_score clamp | §5.2 | Boost stacking could exceed intended cap without explicit rule | H1 | **LOW** |

### 12.2 Gap Severity Summary

| Severity | Count | Key Items |
|----------|-------|-----------|
| **HIGH** | 5 | MC-WEIGHT-001, MC-THRESH-V5, MC-AFFINITY-001, MC-CODE-001, MC-BEHAV-001 |
| **MEDIUM** | 7 | MC-THRESH-001, MC-BOOST-001, MC-BUDGET-001, MC-BUDGET-002, MC-CRM-001, MC-CRM-002, MC-PIPELINE-001 |
| **LOW** | 4 | MC-BOOST-002, MC-PENALTY-001, MC-PENALTY-002, MC-BOOST-CAP-001 |

### 12.3 Gap Resolution Recommendations

| ID | Recommendation | Effort | Priority |
|----|---------------|--------|----------|
| MC-WEIGHT-001 | Document weight deprecation policy: V1 = deprecated, H1 fixed = fallback, H0.5 per-type = active. Remove V1 weights from active use. | Low | High |
| MC-THRESH-001 | Implement dual-threshold pipeline: internal ranking at 40+, user-facing proposition at 60+. Add configuration flag. | Medium | High |
| MC-BOOST-001 | Add 4 missing boosts to H1 MATCHING_EXECUTION_ARCHITECTURE §2.4: cash_purchase (+15), visit_intent (+20), construction-ready_land (+15), high_visibility_commercial (+10). | Low | Medium |
| MC-BOOST-002 | Add V5 budget tiers to H0.5 matching_semantics.json boost_rules as legacy compatibility entries. | Low | Low |
| MC-PENALTY-001 | Add missing_neighborhood (-5) to H1 Penalty Applier §2.5. | Low | Low |
| MC-PENALTY-002 | Add incomplete_property_data (-5) to H0.5 penalty rules. | Low | Low |
| MC-BUDGET-001 | Add LAND_BUY (±15%) and FINANCE (±10%) tolerances to H1 MATCHING_EXECUTION_ARCHITECTURE §4.3. | Low | Medium |
| MC-BUDGET-002 | Implement H0.5 linear decrease logic in budget tolerance checking. | Medium | Medium |
| MC-THRESH-V5 | Create canonical V1→V5 conversion function: `v5_score = v1_score / 100`. Document in Heritage Gold. | Low | High |
| MC-AFFINITY-001 | Expand affinity matrix to cover all 10 priority cities. Requires domain expert input. | High | High |
| MC-CRM-001 | Normalize CRM factor names between Gold V5 and H1. Use Gold factor names as canonical, map to H1 pipeline names. | Low | Medium |
| MC-CRM-002 | Add base lead scores to H1 CRM_PIPELINE_CONTRACT or MATCHING_SCORE_CONTRACT. | Low | Medium |
| MC-BOOST-CAP-001 | Add explicit +50 boost cap documentation to H1 MATCHING_EXECUTION_ARCHITECTURE §2.4. | Low | Low |

---

## 13. H0.5 Matching Role Representation Verification

### 13.1 Per-Role Verification

| H0.5 Role | Defined in H0.5 | Mapped in H1 | Represented in H1 Component | Implementable from H1 Docs? |
|-----------|----------------|--------------|----------------------------|----------------------------|
| `hard_constraint` | ✅ `field_dictionary.json` | ✅ §0.2 | Constraint Enforcer | ✅ — Fully specified in MATCHING_EXECUTION_ARCHITECTURE §2.3, MATCHING_SCORE_CONTRACT §2 |
| `soft_constraint` | ✅ `field_dictionary.json` | ✅ §0.2 | Dimension Evaluator | ✅ — Fully specified in MATCHING_EXECUTION_ARCHITECTURE §2.1 |
| `ranking_preference` | ✅ `field_dictionary.json` | ⚠️ §0.2 | Score Calculator (bonus) | ⚠️ — Range documented (+5 to +15) but per-field values must come from field_mappings; H1 does not define default values |
| `boost` | ✅ `matching_semantics.json` `boost_rules` | ✅ §0.5 | Boost Applier | ✅ — Boost values and conditions fully specified; 4 conditions from H0.5 not yet in H1 (see MC-BOOST-001) |
| `penalty` | ✅ `matching_semantics.json` penalty role | ✅ §0.5 | Penalty Applier | ✅ — Penalty values fully specified; 1 missing penalty (see MC-PENALTY-001) |
| `exclusion` | ✅ `matching_semantics.json` exclusion role | ✅ (via Constraint Enforcer + Exclusion Engine) | Exclusion Engine | ✅ — Fully specified in MATCHING_EXECUTION_ARCHITECTURE §2.6 |
| `informational_only` | ✅ `field_dictionary.json` | ✅ §0.2 | Explanation Builder | ✅ — No scoring impact; documented as explanation-only |
| `verification_only` | ✅ `field_dictionary.json` | ✅ §0.2 | Audit / Transaction Engine | ✅ — Delegated to transaction engine; no matching engine changes needed |
| `transaction_blocker` | ✅ `field_dictionary.json` | ✅ §0.2 | Transaction readiness gate | ✅ — Delegated to readiness model; no matching engine changes needed |

### 13.2 Verification Summary

| Metric | Count |
|--------|-------|
| Total H0.5 matching roles | 9 |
| Fully verified in H1 | 7 (hard_constraint, soft_constraint, boost, penalty, exclusion, informational_only, verification_only) |
| Partially verified in H1 | 2 (ranking_preference — per-field values not defaulted; transaction_blocker — delegated to external engine) |
| Not represented in H1 | 0 |

**Verdict:** All 9 H0.5 matching roles have a representation in the H1 architecture. Seven roles are fully specified and implementable from H1 documents alone. Two roles (ranking_preference, transaction_blocker) require cross-reference with H0.5 field_mappings or external engine specifications but are structurally defined.

### 13.3 Current Model Verification

Beyond H1 architecture, each H0.5 role also maps to the current LAWIM_V2 codebase status:

| H0.5 Role | Current LAWIM_V2 Code State | Verification |
|-----------|---------------------------|-------------|
| `hard_constraint` | ❌ Not implemented (no matching engine in code) | Defined in H1 docs only |
| `soft_constraint` | ❌ Not implemented | Defined in H1 docs only |
| `ranking_preference` | ❌ Not implemented | Defined in H1 docs only |
| `boost` | ❌ Not implemented | Defined in H1 docs only |
| `penalty` | ❌ Not implemented | Defined in H1 docs only |
| `exclusion` | ❌ Not implemented | Defined in H1 docs only |
| `informational_only` | ❌ Not implemented | Defined in H1 docs only |
| `verification_only` | ❌ Not implemented | Defined in H1 docs only |
| `transaction_blocker` | ❌ Not implemented | Defined in H0.5 field semantics only |

**Current code state:** No matching engine is implemented in code. All 9 roles exist only in documentation (H0.5 semantics files + H1 architecture documents). The H1 documents provide a complete specification for implementation; no role is missing from the specification.

---

## 14. Overall Compatibility Verdict

| Domain | Compatibility Status | Key Finding |
|--------|---------------------|-------------|
| **Role Mapping** (§2) | ✅ **FULL** — 9/9 roles mapped | All H0.5 roles have H1 representation |
| **Weight Distribution** (§3) | ⚠️ **PARTIAL** — 3 weight systems coexist | H0.5 per-type weights supersede H1 fixed weights per RESOLVED_BY_H05 |
| **Budget Tolerance** (§4) | ⚠️ **PARTIAL** — Core types match, extensions missing | LAND_BUY/FINANCE tolerances need H1 update |
| **Boost/Penalty** (§5) | ⚠️ **PARTIAL** — Core rules match, 4 boosts missing | H0.5 extensions not in H1 Boost Applier |
| **Scoring Formula** (§6) | ✅ **FULL** — Identical formula structure | Same additive model at different granularity |
| **Thresholds** (§7) | ⚠️ **PARTIAL** — Dual-threshold system | ARCHITECTURE_DECISION_RETAINED resolution in place |
| **Exclusion Rules** (§8) | ✅ **FULL** — All criteria match | H1 superset of Gold |
| **Rematching** (§9) | ✅ **FULL** — H1 superset of Gold | SLA-based cadence replaces fixed J+7 |
| **Geographic Scoring** (§10) | ✅ **FULL** — Complete alignment | H1 formalizes all Gold concepts |
| **CRM Scoring** (§11) | ⚠️ **PARTIAL** — Factor names need normalization | V5 7-factor structure exists, names differ |
| **Gap Resolution** (§12) | ⚠️ **16 gaps identified** | 5 HIGH, 7 MEDIUM, 4 LOW severity |

**Overall Score: 7/10** — The H0.5 → H1 → Heritage Gold compatibility is strong but has documented gaps that must be resolved before implementation. No fundamental architectural contradiction exists; all gaps are resolvable through documentation updates and implementation decisions.

---

## References

- `docs/lawim_heritage_gold/MATCHING_MODEL.md` — Heritage Gold matching knowledge (all sections)
- `docs/knowledge_execution/MATCHING_EXECUTION_ARCHITECTURE.md` — H1 Matching Engine architecture (§0–§7)
- `docs/knowledge_execution/MATCHING_SCORE_CONTRACT.md` — H1 scoring contract (§0–§5)
- `docs/knowledge_execution/REMATCHING_POLICY.md` — H1 rematching policy (§1–§8)
- `docs/knowledge_execution/PROXIMITY_SCORING_MODEL.md` — H1 geographic scoring (§1–§9)
- `docs/knowledge_execution/CRM_PIPELINE_CONTRACT.md` — H1 CRM pipeline (§1–§9)
- `docs/semantic_harmonization/ROLE_CROSSWALK.md` — H0.5 role crosswalk
- `docs/semantic_harmonization/INTENT_TRANSACTION_CROSSWALK.md` — H0.5 intent/transaction crosswalk
