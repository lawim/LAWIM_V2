# SEARCH EXECUTION ARCHITECTURE — Moteur de Recherche LAWIM V5

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** MATCHING_MODEL.md, WORKFLOW_EXTRACTION_COMPLETE.md (Sec 21-22), DECISION_ENGINE_ARCHITECTURE.md, QUALIFICATION_EXECUTION_ARCHITECTURE.md

---

## 1. Overview

The Search Engine is the core property-finding subsystem of LAWIM. It consumes the structured query produced by Qualification, executes multi-phase matching against the property inventory, scores and ranks results, and produces a results payload consumable by the Decision Engine and NBA resolver.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SEARCH ENGINE                               │
│                                                                     │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐    │
│  │ Qualified     │──→│ Query        │──→│ Query Validator      │    │
│  │ Fields        │   │ Constructor  │   │ (completeness,       │    │
│  │ (from Qualif) │   │              │   │  feasibility)        │    │
│  └──────────────┘   └──────┬───────┘   └──────────┬───────────┘    │
│                            │                       │                │
│                            ▼                       ▼                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   Search Phase Controller                     │   │
│  │                                                               │   │
│  │  Level 0: Exact Search                                        │   │
│  │  Level 1: Strict Compatible Search                            │   │
│  │  Level 2: Nearby Search                                       │   │
│  │  Level 3: Budget Tolerance Search                             │   │
│  │  Level 4: Property-Type Relaxation                            │   │
│  │  Level 5: Location Expansion                                  │   │
│  │  Level 6: Continuous Surveillance                             │   │
│  │  Level 7: Future Availability                                 │   │
│  │  Level 8: Professional Search                                 │   │
│  └─────────────────────────┬───────────────────────────────────┘  │
│                            │                                       │
│                            ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │               Scoring & Ranking Pipeline                      │   │
│  │                                                               │   │
│  │  Pre-filter → Score Families → Composite Score → Star Rating │   │
│  └─────────────────────────┬───────────────────────────────────┘  │
│                            │                                       │
│                            ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │               Results Assembler                               │   │
│  │  top N properties + diagnostics + zero-result handler        │   │
│  └─────────────────────────┬───────────────────────────────────┘  │
│                            │                                       │
│                            ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Decision Engine ← Results → NBA Resolver → Follow-up      │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Search Phase Definitions

Execution proceeds through ordered levels. Each level relaxes specific constraints from the previous one. The engine always starts at Level 0 and escalates only when results are insufficient (below threshold or zero).

### 2.1 Phase Inventory

| Level | Name | Relaxation | Trigger | Max Results |
|-------|------|-----------|---------|-------------|
| 0 | Exact Search | None — all criteria strict | Initial search | 10 |
| 1 | Strict Compatible Search | Minor criteria (floor, orientation, surface ±5%) | 0 results at L0 | 10 |
| 2 | Nearby Search | Neighborhood → adjacent neighborhoods | < 3 results at L1 | 10 |
| 3 | Budget Tolerance Search | Budget ± tolerance (rent ±20%, buy ±15%, invest ±25%) | < 3 results at L2 | 10 |
| 4 | Property-Type Relaxation | Property type → parent family (e.g., apartment ← studio/duplex) | < 3 results at L3 | 10 |
| 5 | Location Expansion | City → neighboring cities / same department | < 3 results at L4 | 10 |
| 6 | Continuous Surveillance | Ongoing monitoring of new listings, price drops, status changes | Auto post-L5, J+7 recheck | N/A |
| 7 | Future Availability Search | Properties with pending/construction status, estimated availability | Explicit user request | 5 |
| 8 | Professional Search | Agent network listings, non-public inventory | Explicit user request + permissions | 5 |

### 2.2 Phase Entry Conditions

| Level | Entry Condition | User Consent Required |
|-------|----------------|----------------------|
| 0 | Always (initial search) | No |
| 1 | L0 returns < threshold result count | No |
| 2 | L1 returns < threshold | Yes — propose adjacent neighborhoods |
| 3 | L2 returns < threshold | Yes — explain tolerance impact |
| 4 | L3 returns < threshold | Yes — explain type family expansion |
| 5 | L4 returns < threshold | Yes — explain location expansion |
| 6 | L5 returns < threshold OR dossier is active | Yes (opt-in at dossier creation) |
| 7 | User explicitly asks for future/upcoming | Yes |
| 8 | User is professional (agent/investor) | Yes |

### 2.3 Threshold Result Count

| Context | Minimum Results Before Escalation |
|---------|----------------------------------|
| First matching | 3 properties |
| Rematching (J+7) | 2 new properties since last check |
| Post-visit rematching | 1 new property matching rejected criteria |
| Continuous surveillance | 1 new property = notify immediately |

---

## 3. Search Query Construction

### 3.1 Input Fields (from Qualification)

The Search Engine consumes the structured qualification payload:

| Field | Type | Source (Qualification Step) | Required |
|-------|------|----------------------------|----------|
| `intent` | Enum (RENT/BUY/SELL/INVESTOR) | Step 1 — Intention | YES |
| `property_type` | Enum (16 types) | Step 2 — Type bien | YES |
| `city` | String | Step 3 — Ville | YES |
| `neighborhood` | String | Step 4 — Quartier | NO |
| `budget_min` | Integer (FCFA) | Step 5 — Budget | YES |
| `budget_max` | Integer (FCFA) | Step 5 — Budget | YES |
| `budget_type` | Enum (purchase/rental/monthly) | Step 5 — Budget | YES |
| `urgency` | Enum (urgent/1month/3months/flexible) | Step 6 — Délai | NO |
| `surface_min` | Integer (m²) | Step 7 — Critères | NO |
| `rooms_min` | Integer | Step 7 — Critères | NO |
| `bedrooms_min` | Integer | Step 7 — Critères | NO |
| `floor` | Integer | Step 7 — Critères | NO |
| `parking` | Boolean | Step 7 — Critères | NO |
| `furnished` | Boolean | Step 7 — Critères | NO |
| `preferences` | Map (exposure, standing, animals, features) | Step 8 — Préférences | NO |
| `mobility_mode` | Enum (STRICT/FLEXIBLE/VERY_FLEXIBLE) | Derived from user behavior | Default: FLEXIBLE |
| `excluded_properties` | UUID[] | Blacklist from previous refusals | NO |

### 3.2 Query Construction Process

```
Raw Fields
    │
    ├── 1. Validate required fields (intent, property_type, city, budget)
    │        └── Missing → return diagnostics + which field is missing
    │
    ├── 2. Build hard filters (pre-filter layer)
    │        ├── intent → operation_type filter
    │        ├── property_type → type filter
    │        ├── city → city filter
    │        ├── budget → [min - tolerance, max + tolerance]
    │        ├── excluded_properties → NOT IN
    │        └── status → Disponible ONLY (see MATCH-034)
    │
    ├── 3. Build soft filters (scoring layer)
    │        ├── neighborhood → boost if match
    │        ├── surface, rooms, bedrooms → score bands
    │        ├── parking, furnished, floor → score increments
    │        └── preferences → score boosts
    │
    ├── 4. Build expansion params
    │        ├── current_level (0-8)
    │        ├── relaxations applied (which criteria loosened)
    │        └── mobility_mode
    │
    └── 5. Output: SearchQuery object
```

### 3.3 SearchQuery Object

```typescript
interface SearchQuery {
  // Hard constraints (pre-filter)
  hardFilters: {
    transactionType: "RENT" | "BUY" | "INVEST";
    propertyTypes: PropertyType[];
    cities: string[];
    minPrice: number;
    maxPrice: number;
    excludedPropertyIds: string[];
    allowedStatuses: string[];
  };

  // Soft constraints (scoring weights)
  softFilters: {
    neighborhoods: string[];
    minSurface: number;
    maxSurface: number;
    minRooms: number;
    minBedrooms: number;
    parking: boolean | null;
    furnished: boolean | null;
    preferences: Record<string, any>;
  };

  // Expansion state
  expansion: {
    currentLevel: number;
    relaxationsApplied: Relaxation[];
    mobilityMode: "STRICT" | "FLEXIBLE" | "VERY_FLEXIBLE";
  };

  // Metadata
  metadata: {
    dossierId: string;
    userId: string;
    searchId: string; // unique per search execution
    timestamp: string;
    origin: "INITIAL" | "REMATCH" | "SURVEILLANCE" | "EXPLICIT";
  };
}
```

---

## 4. Pre-Filtering (Hard Constraints)

### 4.1 Exclusion Rules (from MATCHING_MODEL §22)

| Criterion | Action |
|-----------|--------|
| Property status = ARCHIVED | Excluded |
| Property status = SOLD | Excluded |
| Property status = RENTED | Excluded |
| Property status = INACTIVE | Excluded |
| Previously rejected by requester | Blacklisted (never re-propose) |
| Budget outside tolerance + expansion | Excluded |
| Different city (no multi-city request, no expansion) | Excluded |
| Incompatible property type (MATCH-013: non-compensation) | Excluded |

### 4.2 Inclusion by Search Level

| Level | Hard Filters Active |
|-------|-------------------|
| 0 (Exact) | All hard filters at strict values |
| 1 (Compatible) | Same as L0 + surface ±5% |
| 2 (Nearby) | L1 filters + neighborhood expanded to adjacent |
| 3 (Budget Tolerance) | L2 filters + budget range expanded by tolerance % |
| 4 (Type Relaxation) | L3 filters + property_type expanded to parent family |
| 5 (Location Expansion) | L4 filters + city expanded to neighboring cities |
| 6 (Surveillance) | Same as L5 filters (ongoing) |
| 7 (Future Availability) | status IN (PENDING_CONSTRUCTION, RESERVED) |
| 8 (Professional Search) | visibility IN (PUBLIC, AGENT_NETWORK, PREMIUM) |

---

## 5. Scoring & Ranking Pipeline

### 5.1 Score Families

From MATCHING_MODEL §6-7 with validated weights:

| Score Family | Weight | Components |
|-------------|--------|------------|
| **Geographical Score** | 26% | city_match, neighborhood_match, proximity_level, mobility_mode boost |
| **Budget Score** | 20% | budget_within_range, tolerance_tier, price_position |
| **Property Score** | 15% | property_type_match, title_status, surface_match, room_match |
| **Behavioral Score** | 10% | user_profile_affinity, past_preferences, visit_history |
| **Transaction Success Score** | 29% | availability, freshness, holder_reliability, document_score |

### 5.2 Geographical Score Calculation

From MATCHING_MODEL §21 (Proximity Levels):

| Level | Label | Score Contribution |
|-------|-------|-------------------|
| 1 | Exact neighborhood | 100% of geo weight |
| 2 | Accepted alternative | 85% of geo weight |
| 3 | Neighboring district | 65% of geo weight |
| 4 | Same city distant | 40% of geo weight |
| 5 | Incompatible zone | 0% (excluded) |

**Mobility Mode Boost:**

| Mode | Radius Boost | Score Multiplier |
|------|-------------|-----------------|
| STRICT | 0 | 1.0x (neighborhood only) |
| FLEXIBLE | 0.5 | 1.2x for alternative |
| VERY_FLEXIBLE | 1.0 | 1.4x for expanded zone |

### 5.3 Budget Score Calculation

From MATCHING_MODEL §2, §20:

| Budget Diff | Score Contribution |
|-------------|-------------------|
| Exact match (diff = 0) | 100% of budget weight |
| < 10% of budget range | 70% of budget weight |
| < 30% of budget range | 40% of budget weight |
| < 50% of budget range | 20% of budget weight |
| Outside tolerance | 0% (excluded unless expanded) |

**Transaction Budget Tolerances:**

| Transaction Type | Tolerance |
|-----------------|-----------|
| Rent | ±20% |
| Buy | ±15% |
| Invest | ±25% |

### 5.4 Property Score Calculation

| Dimension | Score Contribution |
|-----------|-------------------|
| Property type exact match | 100% of type weight |
| Property type family match | 60% of type weight |
| Surface within ±10% | +5 bonus |
| Rooms match | +5 bonus |
| Bedrooms match | +5 bonus |
| Title foncier (land title) | +10 (from MATCH-003 priority boost) |

### 5.5 Behavioral Score Calculation

| Signal | Score Boost |
|--------|-------------|
| exact_neighborhood_match | +25 (MATCH-003) |
| exact_city_match | +20 (MATCH-003) |
| budget_within_range | +15 (MATCH-003) |
| title_foncier | +10 (MATCH-003) |
| diaspora_investor | +20 (MATCH-003) |
| Past visit to similar property | +15 |
| Previously expressed interest in type | +10 |

### 5.6 Composite Score Formula

```
CompositeScore = Σ(score_family_i × weight_i) + priority_boosts

Where:
  - score_family_i ∈ [0, 100]
  - weight_i ∈ [0, 1], Σ weights = 1
  - priority_boosts ∈ [0, 100]
  - CompositeScore ∈ [0, 100]
  - min(CompositeScore, 100) → final score
```

### 5.7 Star Rating (from MATCHING_MODEL §19)

| Score Range | Stars | Display |
|-------------|-------|---------|
| ≥ 80 | ⭐⭐⭐⭐⭐ (5/5) | Excellent match |
| ≥ 60 | ⭐⭐⭐⭐ (4/5) | Good match |
| ≥ 40 | ⭐⭐⭐ (3/5) | Fair match |
| ≥ 20 | ⭐⭐ (2/5) | Weak match |
| < 20 | ⭐ (1/5) | Poor match |

### 5.8 Minimum Threshold (from MATCH-009)

| Parameter | Value |
|-----------|-------|
| Minimum match score | **60/100** |
| Below threshold | Not shown (zero-result diagnostic) |
| Exception | Explicit expansion search may show ≥ 50 |

### 5.9 Top Results Limit (from MATCH-010)

| Context | Max Results |
|---------|-------------|
| First matching | **5** (DE rule MATCH-010) |
| Rematching | **10** (V1 rule) |
| Continuous surveillance notification | **3** (top new matches) |
| Professional search | **5** |

---

## 6. Ranking Algorithm

### 6.1 Primary Sort

```
ORDER BY composite_score DESC, freshness_score DESC
```

### 6.2 Diversity Rule (MATCH-032)

> Avoid near-identical properties: maximum 1 property per same building/complex in top 5.

Implementation:
```
1. Score and rank all properties
2. Group by building/complex ID
3. If >1 property from same group in top 5:
     keep highest-scored, remove others
     promote next property from different group
4. Repeat until top N has ≤1 per group
```

### 6.3 Freshness Boost

| Listing Age | Freshness Multiplier |
|-------------|---------------------|
| < 24 hours | 1.2x |
| < 7 days | 1.1x |
| < 30 days | 1.0x |
| < 90 days | 0.9x |
| > 90 days | 0.8x |

---

## 7. Zero-Result Handling & Diagnostics

### 7.1 Diagnostic Categories

When a search phase returns zero results, the engine produces a structured diagnostic:

| Diagnostic | Meaning | System Action |
|-----------|---------|---------------|
| `NO_PROPERTIES_IN_CITY` | No inventory in requested city | → Level 5 (Location Expansion) |
| `NO_PROPERTIES_OF_TYPE` | City has properties but not this type | → Level 4 (Type Relaxation) |
| `BUDGET_MISMATCH` | Properties exist but budget too low | → Level 3 (Budget Tolerance) |
| `NEIGHBORHOOD_TOO_NARROW` | Only other neighborhoods available | → Level 2 (Nearby) |
| `INVENTORY_EXHAUSTED` | All properties in city already visited/rejected | → Level 6 (Surveillance) + follow-up |
| `NO_MATCH_ABOVE_THRESHOLD` | Properties found but all score < 60 | → Progressive expansion + explain |
| `ALL_REJECTED` | User rejected all available options | → Ask for new criteria |
| `PENDING_AVAILABILITY` | Only future/pending properties match | → Level 7 (Future Availability) |

### 7.2 Zero-Result Response Template

```
Diagnostic: {diagnostic_code}
Score: {best_score}/100
Properties found: {total_raw}
After filtering: {after_hard_filters}
After threshold: {after_min_score}
Expansion level reached: {current_level}
Suggested next level: {next_level}
User consent required: {true/false}
```

### 7.3 Escalation Flow

```
     ┌──────────────────────────────┐
     │   Search Phase returns 0     │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │   Build diagnostic           │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │   Can expand to next level?  │
     │   yes ───────────→ User consent needed? ──yes──→ Ask user
     │   no                            │ no                │
     └──────────────┬───────────────┘   │                  │
                    │                   ▼                  │
                    ▼            ┌─────────────┐          │
     ┌────────────────────┐      │ Execute next │←────────┘
     │ Activate Continuous │      │ level       │
     │ Surveillance        │      └──────┬──────┘
     └────────────────────┘             │
                                        ▼
                               ┌────────────────┐
                               │ Results ≥       │
                               │ threshold?      │
                               │ yes → return    │
                               │ no  → expand    │
                               └────────────────┘
```

---

## 8. Search History & Learning

### 8.1 What Is Recorded

| Event | Data Stored | Used For |
|-------|------------|----------|
| Search executed | Full SearchQuery, timestamp, level | Audit, re-execution |
| Property presented | Property ID, score, rank, search_id | Performance tracking |
| Property viewed | Property ID, user_id, timestamp | Behavioral scoring |
| Property rejected | Property ID, reason, timestamp | Blacklist (MATCH-017) |
| Property accepted | Property ID, timestamp | Affinity learning |
| Visit requested | Property ID, timestamp | High-intent signal |
| Budget change | Old range → new range, timestamp | Rematch trigger |
| Location change | Old location → new location, timestamp | Rematch trigger |

### 8.2 Learning Signals

| Signal | Impact | Update Frequency |
|--------|--------|-----------------|
| Repeated rejection of property type | Reduce type weight for user | After 3 rejections (MATCH-014) |
| Repeated acceptance of neighborhood | Boost neighborhood weight | After 2 acceptances |
| Price range drift over time | Adjust budget tolerance dynamically | Per search session |
| Mobility mode inferred from behavior | STRICT → FLEXIBLE shift if user accepts alternatives | After 2 alternative acceptances |
| Preferred features from view history | Auto-add preferences to future queries | Per dossier |

### 8.3 Blacklist Management (MATCH-017, MATCH-018)

| Rule | Action |
|------|--------|
| Property definitively refused | Add to `excluded_properties[]` — never repropose |
| Exception: price decrease ≥ 10% | Remove from blacklist, notify user |
| Exception: major modification | Remove from blacklist, notify user |
| Exception: user changed need | Clear blacklist, notify user |
| Exception: explicit user request | Clear blacklist for specific property |
| 3 refusals of same type | → Prioritization signal (MATCH-014) |

---

## 9. Integration with Decision Engine & NBA

### 9.1 Search Results → Decision Engine Contract

```typescript
interface SearchResults {
  results: ScoredProperty[];
  totalCount: number;
  bestScore: number;
  diagnostic: SearchDiagnostic | null;
  expansionState: {
    currentLevel: number;
    levelsAttempted: number[];
    userConsentObtained: boolean[];
  };
  metadata: SearchMetadata;
}

interface ScoredProperty {
  propertyId: string;
  scores: {
    composite: number;    // 0-100
    geographical: number;
    budget: number;
    property: number;
    behavioral: number;
    transactionSuccess: number;
  };
  starRating: 1 | 2 | 3 | 4 | 5;
  rank: number;
  explanation: string[]; // top 3 criteria (MATCH-033)
}
```

### 9.2 Decision Engine Input

The Decision Engine receives `SearchResults` and decides:

| Decision | Condition | NBA |
|----------|-----------|-----|
| `send_listings` | Results ≥ threshold (score ≥ 60) & count ≥ 1 | Present properties to user |
| `suggest_alternatives` | Results < threshold but > 0 | Show best available, suggest expansion |
| `request_budget` | Zero results due to budget mismatch | Ask for budget adjustment |
| `request_location` | Zero results due to location | Ask for location flexibility |
| `suggest_alternatives` + expansion | Zero results, expansion possible | Ask consent, execute expansion |
| `follow_up` | Zero results, no expansion possible | Schedule J+7 rematch |
| `rematch` | Any criteria change or J+7 expiry | Execute rematch |
| `schedule_visit` | User accepts property | Organize visit |
| `call_immediately` | HOT lead + property match | Escalate to agent |

### 9.3 Decision Engine Priority (from WORKFLOW §4, Ch88)

| Priority | Action |
|----------|--------|
| 1 | Correct an incoherence |
| 2 | Complete a critical field |
| 3 | **Matching** |
| 4 | Present a property |
| 5 | Contact the holder |
| 6 | Organize a visit |
| 7 | Follow up |
| 8 | Notifications |
| 9 | Dossier optimization |

### 9.4 NBA Resolution After Search

```
SearchResults
    │
    ├── results.length > 0 AND bestScore >= 60
    │       ↓
    │   NBA = PRESENT_PROPERTIES
    │   Explanation: "Found {n} matching properties. Best match: {property} ({score}/100)"
    │
    ├── results.length > 0 AND bestScore < 60
    │       ↓
    │   NBA = SUGGEST_ALTERNATIVES + propose expansion
    │   Explanation: "Properties found but match quality is low. Consider expanding criteria."
    │
    ├── results.length === 0 AND expansionAvailable
    │       ↓
    │   NBA = PROPOSE_EXPANSION
    │   Explanation: "No exact matches. Would you like to search in nearby areas?"
    │
    └── results.length === 0 AND NOT expansionAvailable
            ↓
        NBA = ACTIVATE_SURVEILLANCE + FOLLOW_UP
        Explanation: "No current matches. I'll monitor the market and notify you."
```

---

## 10. Execution Flow (Complete)

```
Qualification
    │
    ├──→ Qualified fields
    │
    ├──→ SearchQuery Constructor
    │       │
    │       ├──→ Query Validator
    │       │       ├── fields complete? → yes: continue
    │       │       │                     no: return MISSING_FIELD diagnostic
    │       │       └── feasible? → yes: continue
    │       │                       no: return INFEASIBLE diagnostic
    │       │
    │       └──→ Phase Controller (start Level 0)
    │               │
    │               ├──→ Pre-filter (hard constraints)
    │               ├──→ Execute query
    │               ├──→ Score properties
    │               ├──→ Rank + apply diversity
    │               ├──→ Check threshold
    │               │       ├── ≥ threshold → return results
    │               │       └── < threshold → check next level
    │               │
    │               └──→ [Recurse until threshold met or max level reached]
    │
    ├──→ Decision Engine receives SearchResults
    │       │
    │       ├──→ Resolve NBA from results
    │       ├──→ Build explanation
    │       └──→ Write audit trail
    │
    └──→ User response → Learning → Next turn
```

---

## 11. Edge Cases & Error Handling

| Scenario | Detection | Handling |
|----------|-----------|----------|
| All properties in city exhausted | Every property in inventory has been viewed/rejected | Activate surveillance, ask user to adjust criteria |
| Budget range too narrow for any property | No property within ±tolerance in city | Diagnostic: BUDGET_MISMATCH, propose alternatives |
| Property type not available in city | City inventory has 0 of requested type | Expand to parent type family immediately (no consent needed for cross-family) |
| User rejects all presented properties (3 consecutive) | 3 refusals with no acceptance | Enter diagnostic mode: ask what's wrong, adjust criteria |
| Search timeout (inventory large) | > 5s execution | Return partial results, continue async, notify when complete |
| Network/cache failure | Property database unavailable | Return CACHED results with `stale: true` flag |
| Inconsistent user criteria | e.g., budget 10M for apartment in Douala center | Soft warning, execute anyway, note in diagnostic |
| Multi-city search | User requests multiple cities | Create parallel searches per city, merge ranked results |

---

## 12. SLA Compliance (from WORKFLOW §24)

| Property Type | First Matching SLA | First Rematching SLA |
|---------------|-------------------|---------------------|
| Chambre / Studio | Immediate | 24-48 h |
| Appartement | Immediate | 72 h |
| Maison / Villa | Immediate | 5-7 days |
| Terrain | Immediate | 10-15 days |
| Commerce / Bureau | Immediate | 7-10 days |
| Hôtel / Immeuble | Immediate | 30 days |

---

## 13. Gold Knowledge Register — Search Execution

| ID (SE-) | Concept | Description | Source | Confidence |
|---------|---------|-------------|--------|------------|
| SE-001 | 9 Search Phases | Exact → Compatible → Nearby → Budget → Type → Location → Surveillance → Future → Professional | Derived from MATCHING_MODEL + WORKFLOW_EXTRACTION §21-22 | HIGH |
| SE-002 | Scoring Weights | Geo 26%, Budget 20%, Property 15%, Behavioral 10%, Transaction 29% | MATCHING_MODEL §7 | HIGH |
| SE-003 | Budget Tolerances | Rent ±20%, Buy ±15%, Invest ±25% | MATCHING_MODEL §2 | VERY HIGH |
| SE-004 | Minimum Threshold | 60/100 | MATCH-009 | VERY HIGH |
| SE-005 | Priority Boosts | neighborhood +25, city +20, budget +15, title +10, diaspora +20 | MATCHING_MODEL §3 | VERY HIGH |
| SE-006 | Exclusion Rules | Archived/Sold/Rented/Inactive/Rejected | MATCHING_MODEL §22 | VERY HIGH |
| SE-007 | Diversity Rule | Max 1 per building in top 5 | MATCH-032 | HIGH |
| SE-008 | Star Rating | 5★≥80, 4★≥60, 3★≥40, 2★≥20, 1★<20 | MATCHING_MODEL §19 | VERY HIGH |
| SE-009 | Blacklist Management | Never repropose refused property (exceptions apply) | MATCH-017, MATCH-018 | VERY HIGH |
| SE-010 | Learning from Refusals | 3 refusals → prioritization | MATCH-014 | HIGH |
| SE-011 | Explainer | Top 3 criteria explained for each proposition | MATCH-033 | HIGH |

---

*Canonical document — Search Execution Architecture for LAWIM V5. All weights and rules aligned with Heritage Gold MATCHING_MODEL and WORKFLOW_EXTRACTION_COMPLETE.*
