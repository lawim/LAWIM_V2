# Matching Execution Architecture

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**Prerequisite:** Heritage Gold — `docs/lawim_heritage_gold/MATCHING_MODEL.md`, `docs/lawim_heritage_gold/RULE_INDEX.md` (MATCH-001 to MATCH-034)

---

## 1. Overview

The Matching Engine is the domain engine responsible for scoring, ranking, and selecting properties against a qualified dossier. It consumes all 34 MATCH rules from Heritage Gold and produces scored, ranked, explainable matching results with Next Best Action output.

```
Qualified Dossier (from Qualification Engine)
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│                        MATCHING ENGINE                                │
│                                                                       │
│  ┌─────────────────┐  ┌────────────────┐  ┌─────────────────────┐   │
│  │ Dimension        │  │ Constraint      │  │ Boost / Penalty     │   │
│  │ Evaluator        │  │ Enforcer        │  │ Applier             │   │
│  └────────┬────────┘  └───────┬────────┘  └──────────┬──────────┘   │
│           │                   │                       │              │
│           ▼                   ▼                       ▼              │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    Score Calculator                          │    │
│  │  aggregate dimension scores → compute family scores →       │    │
│  │  compute global score → apply boosts → apply penalties      │    │
│  └────────────────────────┬────────────────────────────────────┘    │
│                           │                                         │
│                           ▼                                         │
│  ┌─────────────────┐  ┌────────────────┐  ┌─────────────────────┐   │
│  │ Exclusion Engine │  │ Ranker          │  │ Explanation Builder │   │
│  │ (MATCH-022/023)  │  │ (MATCH-032)     │  │ (MATCH-033)         │   │
│  └────────┬────────┘  └───────┬────────┘  └──────────┬──────────┘   │
│           │                   │                       │              │
│           ▼                   ▼                       ▼              │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              Result Assembler + Decision Output              │    │
│  └─────────────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────────────┘
        │
        ▼
Decision Engine (NBA selection, next action)
```

---

## 2. Architecture Components

### 2.1 Dimension Evaluator

Evaluates all 5 score dimensions against the resource (property) and request (lead/dossier).

| Component | Responsibility | Heritage Rules |
|-----------|---------------|----------------|
| Geographical Dimension | City match, neighborhood match, affinity, GPS proximity, mobility mode | MATCH-001, GEO-001–GEO-011 |
| Budget Dimension | Budget range match, tolerance check per transaction type, flexibility test | MATCH-001, MATCH-003, MATCH-028 |
| Property Dimension | Property type match, title status, bedrooms, surface, critical characteristics | MATCH-001, MATCH-002, MATCH-012 |
| Behavioral Dimension | Urgency, visit intent, trust signals, message history, response time | MATCH-024 (Transaction Success sub-score), QUAL-012 |
| Transaction Success | Availability score, document score, holder reliability, freshness | MATCH-024, MATCH-025, MATCH-026, MATCH-027 |

**Geographical proximity levels** (GEO-011, MATCHING_MODEL §21):

| Level | Label | Score | Condition |
|-------|-------|-------|-----------|
| 1 | Exact neighborhood | Maximal | Property in exact requested neighborhood |
| 2 | Accepted alternative | High | Property in explicitly accepted alternative |
| 3 | Neighboring district | Medium | Property in neighboring district, same city |
| 4 | Same city distant | Low | Same city but far from requested zone |
| 5 | Incompatible zone | Minimal → Exclusion | Incompatible zone (unless multi-city request) |

**Mobility modes** (MATCH-025):

| Mode | Radius Boost | Behavior |
|------|-------------|----------|
| STRICT | 0 | Requested neighborhood only |
| FLEXIBLE | 0.5 | Alternative neighborhoods accepted |
| VERY_FLEXIBLE | 1.0 | Expanded zone |

### 2.2 Score Calculator

Aggregates dimension scores into family scores, then computes the global score with proper weighting.

**Score families** (MATCHING_MODEL §6, GE-MATCH-007):

| Family | Components | Weight |
|--------|-----------|--------|
| Geographical Score | City + Neighborhood + GPS + Affinity + Real distance | 26% |
| Budget Score | Budget range match + Tolerance check + Flexibility consideration | 20% |
| Property Score | Property type match + Title status + Critical characteristics + Comfort characteristics | 15% |
| Behavioral Score | Urgency + Visit intent + Trust signals + Lead engagement | 10% |
| Other Score | Freshness + Services + Agent fit + Availability + Document quality | 29% |

**Global score formula:**

```
global_score = (geographical_score × 0.26)
             + (budget_score × 0.20)
             + (property_score × 0.15)
             + (behavioral_score × 0.10)
             + (other_score × 0.29)

final_score = min(global_score + boost_total - penalty_total, 100)
final_score = max(final_score, 0)
```

### 2.3 Constraint Enforcer

Enforces hard constraints (MATCH-034). These are absolute rules that cannot be violated:

| Constraint | Condition | Action |
|-----------|-----------|--------|
| Incompatible property type | Property type does not match request type | Exclusion (no score calculated) |
| Sold/Rented/Archived property | Property status in unavailable set | Exclusion (MATCH-022) |
| Previously refused property | Property blacklisted for this requester | Exclusion (MATCH-017) |
| Different city (no multi-city) | City not in requested set | Exclusion (MATCH-022) |
| Operation incompatible | Buy vs. Rent vs. Invest mismatch | Exclusion (MATCH-023) |
| Budget outside tolerance | Price exceeds tolerance for transaction type | Exclusion (MATCH-003, MATCH-022) |

**Non-compensation principle** (MATCH-013): A critical field deficiency cannot be compensated by excellence in other fields. If a property fails a critical compatibility check (e.g., wrong city, incompatible type), the score is 0 regardless of other dimension scores.

### 2.4 Boost Applier

Applies priority boosts to the global score (MATCH-004 to MATCH-008, MATCH-020).

| Boost | Value | Trigger Condition | Rule |
|-------|-------|-------------------|------|
| Exact neighborhood match | +25 | Property in exact requested neighborhood | MATCH-004 |
| Exact city match | +20 | Property in exact requested city | MATCH-005 |
| Budget within range | +15 | Price falls within tolerance for transaction type | MATCH-006 |
| Title foncier (land title) | +10 | Property has valid land title | MATCH-007 |
| Diaspora investor | +20 | Lead identified as diaspora investor | MATCH-008 |
| Budget exact match (V5) | +50 | Difference = 0 | MATCH-020 |
| Budget < 10% diff (V5) | +35 | Difference < 10% | MATCH-020 |
| Budget < 30% diff (V5) | +20 | Difference < 30% | MATCH-020 |
| Budget < 50% diff (V5) | +10 | Difference < 50% | MATCH-020 |
| Location match (V5) | +40 | City match | MATCH-020 |
| Property type match (V5) | +10 | Type matches | MATCH-020 |

Boosts are additive. `boost_total` is the sum of all applicable boosts.

### 2.5 Penalty Applier

Applies penalties based on data quality or missing information.

| Penalty | Value | Trigger Condition | Rule |
|---------|-------|-------------------|------|
| Missing budget on lead | -10 | No budget information captured | QUAL-003 |
| Unclear location on lead | -10 | No city/neighborhood captured | QUAL-003 |
| Spam-like message | -50 | Spam patterns detected | QUAL-003 |
| Incomplete property data | -5 per missing field | Missing critical property fields | PROP-006 |

### 2.6 Exclusion Engine

Applies hard exclusion rules (MATCH-022, MATCH-023). Properties that match any exclusion criterion are removed from the candidate set before ranking.

| Exclusion | Trigger | Rule |
|-----------|---------|------|
| Property archived | `property.status = ARCHIVED` | MATCH-022 |
| Property sold | `property.status = SOLD` | MATCH-022 |
| Property rented | `property.status = RENTED` | MATCH-022 |
| Property inactive | `property.status = INACTIVE` | MATCH-022 |
| Previously rejected | Property in requester's blacklist | MATCH-017, MATCH-022 |
| Budget outside tolerance | Price exceeds tolerance for transaction type | MATCH-003, MATCH-022 |
| Different city (no multi-city) | Property city not in request cities | MATCH-022 |
| Incompatible operation | Buy/Rent/Invest mismatch | MATCH-023 |
| Incompatible type | Property type not compatible with request | MATCH-023 |
| Property unavailable | Status in SOLD/RENTED/ARCHIVED | MATCH-023 |

**Principle:** "Rank, don't filter" — properties should only be excluded for hard constraints. All others should be ranked with their score.

### 2.7 Ranker

Ranks surviving properties by `final_score` descending.

| Parameter | Value | Rule |
|-----------|-------|------|
| Minimum match score | 60/100 | MATCH-009 |
| Maximum results (V1) | 10 | MATCH-010 |
| Maximum results (first match) | 5 | MATCH-010 (DE reference) |
| Score range | 0–100 | MATCHING_MODEL §4 |
| Star rating threshold ≥80 | 5/5 | MATCH-019 |
| Star rating threshold ≥60 | 4/5 | MATCH-019 |
| Star rating threshold ≥40 | 3/5 | MATCH-019 |
| Star rating threshold ≥20 | 2/5 | MATCH-019 |
| Star rating threshold <20 | 1/5 | MATCH-019 |
| Score <60 | Never proposed | MATCH-011 |

**Diversity enforcement** (MATCH-032): The Ranker must avoid presenting near-identical properties. If 3 apartments in the same building match, only 1 is presented. Diversity is enforced after scoring but before final output:

```
diversity_check(candidates):
  group by building_id, property_type, price_range
  for each group: keep highest-scored, demote others
  re-rank with diversity adjustment
```

### 2.8 Explanation Builder

Builds human-readable explanations for each match proposition (MATCH-033).

**Top 3 criteria explanation:**
For each proposed property, the top 3 contributing criteria are identified:

```
explanation = top_3_criteria(candidate):
  1. "Located in your requested neighborhood of {neighborhood} (+{points})"
  2. "Within your {transaction_type} budget of {budget} FCFA (+{points})"
  3. "Matches your preferred property type: {type} (+{points})"
```

**Star rating display** (MATCH-019):
- ⭐⭐⭐⭐⭐ (5/5): "Excellent match" — ≥ 80
- ⭐⭐⭐⭐ (4/5): "Good match" — ≥ 60
- ⭐⭐⭐ (3/5): "Fair match" — ≥ 40
- ⭐⭐ (2/5): "Weak match" — ≥ 20
- ⭐ (1/5): "Poor match" — < 20

---

## 3. Heritage Gold Rule Consumption Matrix

### 3.1 MATCH-001 to MATCH-034 Mapping

| Rule ID | Domain | Consumed By | Behavior |
|---------|--------|-------------|----------|
| MATCH-001 | V1 Weights | Dimension Evaluator, Score Calculator | city=30%, neighborhood=25%, budget=25%, property_type=15%, title_status=5% |
| MATCH-002 | DE Weights | Dimension Evaluator, Score Calculator | type=25%, operation=20%, budget=15%, location=15%, critical=15%, recommended=10% |
| MATCH-003 | Budget Tolerances | Constraint Enforcer, Dimension Evaluator | rent=±20%, buy=±15%, invest=±25% |
| MATCH-004 | Boost: neighborhood | Boost Applier | exact_neighborhood_match=+25 |
| MATCH-005 | Boost: city | Boost Applier | exact_city_match=+20 |
| MATCH-006 | Boost: budget | Boost Applier | budget_within_range=+15 |
| MATCH-007 | Boost: title foncier | Boost Applier | title_foncier=+10 |
| MATCH-008 | Boost: diaspora | Boost Applier | diaspora_investor=+20 |
| MATCH-009 | Min score threshold | Ranker | minimum=60/100 |
| MATCH-010 | Max results | Ranker | max=10 (V1), max=5 (first match) |
| MATCH-011 | Score <60 rule | Ranker | score<60 = never proposed |
| MATCH-012 | 4 compatibility levels | Constraint Enforcer, Dimension Evaluator | Critical, Functional, Comfort, Preferential |
| MATCH-013 | Non-compensation | Constraint Enforcer | critical field deficiency = score 0 |
| MATCH-014 | Learning from refusals | Exclusion Engine, Rematching | 3 refusals → reprioritization |
| MATCH-015 | Rematching: never restart | Rematching Engine | preserve prior scores, only recalc affected |
| MATCH-016 | Rematching: only concerned | Rematching Engine | only recalc dossiers affected by change |
| MATCH-017 | Refused never reproposed | Exclusion Engine | blacklist property for this requester |
| MATCH-018 | Reproposition exceptions | Exclusion Engine, Rematching | price drop, major mod, need change, explicit request |
| MATCH-019 | Star rating | Ranker, Explanation Builder | ≥80=5★, ≥60=4★, ≥40=3★, ≥20=2★, <20=1★ |
| MATCH-020 | V5 scoring | Score Calculator, Boost Applier | location+40, budget tiers (+50/+35/+20/+10), type+10 |
| MATCH-021 | V4 filter | Constraint Enforcer | status='available', city+ budget correspondence |
| MATCH-022 | Exclusions | Exclusion Engine | archived, budget out, diff city, already sent |
| MATCH-023 | Exclusions | Exclusion Engine | incompatible operation, type, unavailable |
| MATCH-024 | Transaction Success Score | Score Calculator | 8 indicators with weights |
| MATCH-025 | Availability score | Dimension Evaluator | 100%=Available, 70%=Reservation, 30%=Pending, 0%=Sold/Rented/Archived |
| MATCH-026 | Document score | Dimension Evaluator | TF=100%, In progress=80%, Customary=60%, Unknown=40% |
| MATCH-027 | Holder reliability | Dimension Evaluator | response_time × acceptance × visits × transactions |
| MATCH-028 | Budget flexibility | Dimension Evaluator, Boost Applier | slight over-budget if other criteria excellent |
| MATCH-029 | Reasoning priority | Pipeline Orchestrator | intent > location > budget > property_type |
| MATCH-030 | 7 reasoning steps | Pipeline Orchestrator | detect_intent → detect_city → ... → rank_results |
| MATCH-031 | Confidence threshold | Pipeline Orchestrator | 0.70 minimum for auto-decisions |
| MATCH-032 | Diversity enforcement | Ranker | avoid near-identical properties |
| MATCH-033 | Explainability | Explanation Builder | top 3 criteria explained per proposition |
| MATCH-034 | Absolute rules | Constraint Enforcer | never incompatible, never sold, never twice after refusal |

### 3.2 Per-Type Weightings (MATCHING_MODEL §9)

| Property Type | Property Score Weight | Notes |
|---------------|----------------------|-------|
| Apartment / Appartement | 15% (Standard) | Default |
| House / Maison | 15% (Standard) | Default |
| Villa | 15% (Standard) | Default |
| Studio | 15% (Standard) | Default |
| Duplex | 15% (Standard) | Default |
| Land / Terrain | 15% (Standard) | Default |
| Commercial / Magasin | 15% (Standard) | Default |
| Office / Bureau | 15% (Standard) | Default |
| Room / Chambre | Reduced | Lower weight |
| Penthouse | 15% (Standard) | Default |
| Building / Immeuble | 15% (Standard) | Default |
| Factory / Usine | Reduced | Lower weight |
| Warehouse / Entrepôt | Reduced | Lower weight |
| Farm / Ferme | Reduced | Lower weight |
| Hotel | Reduced | Lower weight |
| Other | Minimal | Lowest default |

---

## 4. Scoring Pipeline

### 4.1 Full Pipeline

```
Input: (resource: Property, request: Dossier/Lead)
        │
        ▼
Step 1 — Constraint Enforcement (MATCH-034, MATCH-022, MATCH-023)
  │  Check absolute rules
  │  If any hard constraint violated → EXCLUDE → add to exclusion_reasons
  │  If excluded → skip to Result Assembly
  │
  ▼
Step 2 — Load Exclusions (MATCH-017, MATCH-018)
  │  Check requester's blacklist
  │  If blacklisted → EXCLUDE → add to exclusion_reasons
  │  Unless exception applies (MATCH-018)
  │
  ▼
Step 3 — Dimension Evaluation
  │  3a. Geographical Score (city + neighborhood + GPS + proximity)
  │  3b. Budget Score (range + tolerance + flexibility)
  │  3c. Property Score (type + title + characteristics)
  │  3d. Behavioral Score (urgency + visit + trust)
  │  3e. Transaction Success Score (availability + doc + holder + freshness)
  │
  ▼
Step 4 — Score Calculation (MATCH-001, MATCH-002)
  │  Compute family scores with weights
  │  Compute global score
  │  Check non-compensation (MATCH-013)
  │
  ▼
Step 5 — Apply Boosts (MATCH-004 to MATCH-008, MATCH-020)
  │  Apply all qualifying boosts
  │
  ▼
Step 6 — Apply Penalties
  │  Apply data quality / missing info penalties
  │
  ▼
Step 7 — Clamp & Threshold (MATCH-009, MATCH-011)
  │  final_score = clamp(score + boosts - penalties, 0, 100)
  │  If final_score < 60 → mark as below_threshold
  │
  ▼
Step 8 — Ranking (MATCH-010, MATCH-032)
  │  Sort by final_score descending
  │  Enforce diversity (MATCH-032)
  │  Apply star rating (MATCH-019)
  │  Limit to N results
  │
  ▼
Step 9 — Explanation Building (MATCH-033)
  │  Build top 3 criteria explanation per result
  │  Build overall summary
  │
  ▼
Step 10 — Result Assembly
  │  Package results with scores, explanations, exclusions, diagnostics
  │
  ▼
Output: MatchResult[] + Exclusions[] + Diagnostics
```

### 4.2 Score Families Weights (Decision Engine)

| Score Family | Weight | Components |
|-------------|--------|------------|
| Geographical | 26% | City match, neighborhood match, GPS proximity, real distance, travel time |
| Budget | 20% | Budget range match, tolerance compliance, flexibility |
| Property | 15% | Property type match, title status, critical characteristics, comfort |
| Behavioral | 10% | Urgency, visit intent, trust signals, message engagement |
| Other | 29% | Freshness, availability, document quality, holder reliability, services, agent fit |

### 4.3 Budget Tolerance per Transaction (MATCH-003)

| Transaction Type | Tolerance |
|-----------------|-----------|
| Rent | ±20% |
| Buy | ±15% |
| Invest | ±25% |

### 4.4 Availability Score (MATCH-025)

| Status | Score |
|--------|-------|
| Available (Disponible) | 100% |
| Reservation in progress | 70% |
| Owner response pending | 30% |
| Sold / Rented / Archived | 0% (excluded) |

### 4.5 Document Score (MATCH-026)

| Document Situation | Score |
|-------------------|-------|
| Titre foncier (Land title) | 100% |
| En cours d'immatriculation | 80% |
| Droit coutumier (Customary law) | 60% |
| Documents inconnus | 40% |

---

## 5. Integration with Decision Engine and NBA

### 5.1 Decision Engine Integration

The Matching Engine receives a qualified dossier from the Qualification Engine and returns scored results to the Decision Engine for NBA resolution.

```
Qualification Engine
        │
        ▼  QualifiedDossier { intent, location, budget, property_type, lead_score, lead_class }
        │
Matching Engine
        │
        ▼  MatchResult[] { properties, scores, explanations, exclusions }
        │
Decision Engine
        │
        ▼  NBA { action, priority, explanation }
```

### 5.2 NBA Actions after Matching

| Condition | NBA | Rule |
|-----------|-----|------|
| Matches found, WARM lead | `send_listings` | QUAL-009 |
| Matches found, HOT lead | `call_immediately` | QUAL-009 |
| No matches found | `suggest_alternatives` → Progressive Search Expansion | Decision Matrix |
| Match score < 60 (low) | `suggest_alternatives` | Decision Matrix |
| Visit intent detected | `schedule_visit` | Decision Matrix |
| All high-score results refused | `rematch` with learning | MATCH-014 |
| Inventory empty for dossier | `request_relaxation` (Progressive Search) | WORKFLOW §21 |

---

## 6. Error States and Fallbacks

| Error | Detection | Fallback |
|-------|-----------|----------|
| No properties in inventory | Inventory count = 0 | Return `inventory_empty` diagnostic → Progressive Search Expansion |
| All properties excluded | All candidates failed constraints | Return diagnostic with exclusion reasons |
| Dimension evaluation fails | Data missing for required dimension | Score dimension at 0, add warning |
| Score calculation overflow | Score > 100 | Clamp to 100 |
| No valid result after diversity | Single building dominates | Keep highest-scored variant only |

---

## 7. Audit and Traceability

Every matching execution produces audit_event entries:

1. Input snapshot: dossier fields used for matching
2. All evaluated properties with per-dimension scores
3. All exclusion decisions with reasons (rule ID, condition, value)
4. Boost/penalty application with rule references
5. Final ranking with explanations
6. NBA selected by Decision Engine
7. Full audit trail for MATCH rules consumed

---

## References

- Heritage Gold: `docs/lawim_heritage_gold/MATCHING_MODEL.md`
- Heritage Gold: `docs/lawim_heritage_gold/RULE_INDEX.md` (MATCH-001 to MATCH-034)
- Heritage Gold: `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` (§4 Matching Lifecycle, §20 NBA, §21 Progressive Search)
- Decision Engine: `docs/knowledge_execution/DECISION_ENGINE_ARCHITECTURE.md`
- Global Architecture: `docs/knowledge_execution/GLOBAL_EXECUTION_ARCHITECTURE.md`
- Score Contract: `docs/knowledge_execution/MATCHING_SCORE_CONTRACT.md`
