# SEARCH QUERY CONTRACT — Contrat d'Exécution des Requêtes de Recherche

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** SEARCH_EXECUTION_ARCHITECTURE.md, MATCHING_MODEL.md, QUALIFICATION_MODEL.md, QUALIFICATION_MATRIX_CONTRACT.md

---

## 1. Contract Purpose

This document defines the formal contract between the Qualification Engine and the Search Engine. It specifies the input structure, processing pipeline, output structure, validation rules, and expansion rules for every search query execution.

---

## 2. Input Contract

### 2.1 Structured Query from Qualification

The Search Engine receives a fully qualified, validated payload from the Qualification Engine:

```typescript
interface SearchQueryInput {
  // === CORE INTENT (from Qualification Step 1) ===
  intent: "RENT" | "BUY" | "INVEST" | "SELL";
  intentConfidence: number; // 0.0 - 1.0, minimum 0.70 per CONFIDENCE_THRESHOLD

  // === PROPERTY TYPE (from Qualification Step 2) ===
  propertyType: PropertyType;
  propertyTypeFamily: PropertyTypeFamily; // computed: residential | commercial | land | etc.

  // === GEOGRAPHY (from Qualification Steps 3-4) ===
  city: string;
  cityNormalized: string; // canonical name from GEOGRAPHY_MODEL
  neighborhoods: string[]; // requested neighborhoods (unset = entire city)
  mobilityMode: "STRICT" | "FLEXIBLE" | "VERY_FLEXIBLE"; // default: FLEXIBLE

  // === BUDGET (from Qualification Step 5) ===
  budgetMin: number; // FCFA
  budgetMax: number; // FCFA
  budgetType: "PURCHASE" | "RENTAL" | "MONTHLY";
  currency: "XAF" | "EUR"; // default: XAF

  // === TEMPORAL (from Qualification Step 6) ===
  urgency: "URGENT" | "WITHIN_1_MONTH" | "WITHIN_3_MONTHS" | "FLEXIBLE";
  timeline: string | null; // free text if specified

  // === CONSTRAINTS (from Qualification Step 7) ===
  constraints: {
    surfaceMin: number | null;      // m²
    surfaceMax: number | null;      // m²
    roomsMin: number | null;
    bedroomsMin: number | null;
    floor: number | null;
    parking: boolean | null;
    furnished: boolean | null;
    bathroomsMin: number | null;
    condition: PropertyCondition | null; // NEW | GOOD | RENOVATED | FIXER
  };

  // === PREFERENCES (from Qualification Step 8) ===
  preferences: {
    exposure: string[] | null;       // north, south, east, west
    standing: "ECONOMY" | "STANDARD" | "PREMIUM" | "LUXURY" | null;
    petsAllowed: boolean | null;
    additionalFeatures: string[];   // pool, garden, borehole, security, etc.
  };

  // === PERMISSIONS (from User Profile + Role) ===
  permissions: {
    viewUnpublished: boolean;       // agents can see non-public listings
    viewPremiumOnly: boolean;       // premium user visibility
    viewAgentNetwork: boolean;      // professional search enabled
    viewFutureAvailability: boolean; // see pending/construction properties
  };

  // === DATA QUALITY (from CRM_MODEL Sec 9) ===
  minDataQualityScore: number;      // minimum quality score A/B/C/D (default: D = 0)
  // Quality Score = (Completeness × 0.6) + (Reliability × 0.4)

  // === SEARCH CONTEXT ===
  context: {
    dossierId: string;
    userId: string;
    sessionId: string;
    isRematching: boolean;          // true if this is a rematch execution
    previousSearchId: string | null; // linked to previous search for learning
    excludedPropertyIds: string[];  // blacklisted from previous refusals
    origin: "INITIAL" | "REMATCH" | "CONTINUOUS_SURVEILLANCE" | "MANUAL";
  };
}
```

### 2.2 PropertyType Enum

From MATCHING_MODEL §9 (16 types):

| Value | Family | Weight |
|-------|--------|--------|
| `APARTMENT` | Residential | Standard |
| `HOUSE` | Residential | Standard |
| `VILLA` | Residential | Standard |
| `STUDIO` | Residential | Standard |
| `DUPLEX` | Residential | Standard |
| `PENTHOUSE` | Residential | Standard |
| `ROOM` | Residential | Reduced |
| `LAND_RESIDENTIAL` | Land | Standard |
| `LAND_AGRICULTURAL` | Land | Reduced |
| `LAND_INDUSTRIAL` | Land | Reduced |
| `COMMERCIAL` | Commercial | Standard |
| `OFFICE` | Commercial | Standard |
| `BUILDING` | Commercial | Standard |
| `WAREHOUSE` | Industrial | Reduced |
| `FACTORY` | Industrial | Reduced |
| `FARM` | Agricultural | Reduced |
| `HOTEL` | Hospitality | Reduced |
| `OTHER` | Other | Minimal |

### 2.3 Property Condition Enum

| Value | Description |
|-------|-------------|
| `NEW` | Never occupied, newly built |
| `GOOD` | Well maintained, move-in ready |
| `RENOVATED` | Recently renovated |
| `FIXER` | Needs renovation work |

---

## 3. Processing Pipeline

```
┌──────────────────────────────────────────────────────────────────────────┐
│                       SEARCH QUERY PROCESSING                            │
│                                                                          │
│   SearchQueryInput                                                       │
│       │                                                                  │
│       ▼                                                                  │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │               PHASE 1: VALIDATION                                 │   │
│   │                                                                   │   │
│   │   1.1 Completeness Check ──→ are all required fields present?     │   │
│   │   1.2 Feasibility Check  ──→ does the query make logical sense?   │   │
│   │   1.3 Permission Check   ──→ does the user have rights?           │   │
│   │   1.4 Inventory Check    ──→ does city exist in inventory?        │   │
│   └──────────────────────────┬───────────────────────────────────────┘   │
│                              │                                           │
│                              ▼                                           │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │               PHASE 2: QUERY CONSTRUCTION                         │   │
│   │                                                                   │   │
│   │   2.1 Build Hard Filters ──→ status, city, type, budget, exclude  │   │
│   │   2.2 Build Soft Filters ──→ neighborhoods, constraints, pref     │   │
│   │   2.3 Apply Data Quality   ──→ minQualityScore filter             │   │
│   │   2.4 Set Expansion Params ──→ level=0, mobility mode             │   │
│   └──────────────────────────┬───────────────────────────────────────┘   │
│                              │                                           │
│                              ▼                                           │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │               PHASE 3: PRE-FILTERING                              │   │
│   │                                                                   │   │
│   │   3.1 Execute Hard Filter Query                                   │   │
│   │   3.2 Count Raw Results                                           │   │
│   │   3.3 If 0 → Enter Progressive Expansion                          │   │
│   │   3.4 If > 0 → Continue to Scoring                                │   │
│   └──────────────────────────┬───────────────────────────────────────┘   │
│                              │                                           │
│                              ▼                                           │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │               PHASE 4: SCORING & RANKING                          │   │
│   │                                                                   │   │
│   │   4.1 Calculate Geographical Score                                │   │
│   │   4.2 Calculate Budget Score                                      │   │
│   │   4.3 Calculate Property Score                                    │   │
│   │   4.4 Calculate Behavioral Score                                  │   │
│   │   4.5 Calculate Transaction Success Score                         │   │
│   │   4.6 Compute Composite Score (weighted sum + boosts)             │   │
│   │   4.7 Apply Freshness Multiplier                                  │   │
│   │   4.8 Apply Diversity Rule                                        │   │
│   │   4.9 Assign Star Rating                                          │   │
│   └──────────────────────────┬───────────────────────────────────────┘   │
│                              │                                           │
│                              ▼                                           │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │               PHASE 5: RESULTS ASSEMBLY                           │   │
│   │                                                                   │   │
│   │   5.1 Apply Minimum Threshold (60)                                │   │
│   │   5.2 Apply Top N Limit                                           │   │
│   │   5.3 Build Diagnostics (if threshold not met)                    │   │
│   │   5.4 Build Explanation for Top 3 Criteria                        │   │
│   │   5.5 Assemble SearchResults payload                              │   │
│   └──────────────────────────┬───────────────────────────────────────┘   │
│                              │                                           │
│                              ▼                                           │
│                       SearchResults Output                               │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Output Contract

### 4.1 SearchResults

```typescript
interface SearchResults {
  // === RESULTS ===
  results: ScoredProperty[];
  totalCount: number;          // total matching before top N limit
  bestScore: number;           // highest composite score in results
  worstScore: number;          // lowest composite score in results
  averageScore: number;        // average across all scored properties

  // === DIAGNOSTICS ===
  diagnostic: SearchDiagnostic | null;
  zeroResultReason: ZeroResultReason | null;

  // === EXPANSION STATE ===
  expansionState: {
    currentLevel: number;             // 0-8
    levelsAttempted: number[];
    userConsentObtained: boolean[];   // per level index
    relaxationsApplied: Relaxation[];
    nextAvailableLevel: number | null;
  };

  // === QUERY USED ===
  queryExecuted: SearchQuerySnapshot; // frozen snapshot of what was queried

  // === TIMING ===
  timing: {
    startedAt: string;   // ISO 8601
    completedAt: string;  // ISO 8601
    durationMs: number;
  };

  // === METADATA ===
  metadata: SearchMetadata;
}
```

### 4.2 ScoredProperty

```typescript
interface ScoredProperty {
  propertyId: string;
  title: string;
  location: {
    city: string;
    neighborhood: string;
    gps: { lat: number; lng: number } | null;
    proximityLevel: 1 | 2 | 3 | 4 | 5;  // from MATCHING_MODEL §21
  };
  price: number;          // FCFA
  pricePerSqm: number;    // FCFA/m²
  propertyType: PropertyType;
  surface: number;        // m²
  rooms: number;
  bedrooms: number;
  bathrooms: number;
  furnished: boolean;
  parking: boolean;

  // === SCORES ===
  scores: {
    composite: number;          // 0-100
    geographical: number;       // 0-100
    budget: number;             // 0-100
    property: number;           // 0-100
    behavioral: number;         // 0-100
    transactionSuccess: number; // 0-100
  };
  starRating: 1 | 2 | 3 | 4 | 5;
  rank: number;

  // === EXPLANATION (MATCH-033) ===
  explanation: {
    criteria: string[];     // top 3 matching criteria
    boosts: string[];      // priority boosts applied
  };

  // === STATUS ===
  status: PropertyStatus;
  availability: "AVAILABLE" | "RESERVED" | "PENDING" | "FUTURE";
  listingAge: number;      // days since publication
  dataQualityGrade: "A+" | "A" | "B" | "C" | "D";
}
```

### 4.3 PropertyStatus Enum

```
AVAILABLE        → active, can be contacted
RESERVED         → under option/compromise
PENDING          → awaiting confirmation
CONSTRUCTION     → being built (future availability)
SOLD             → sold (excluded from matching)
RENTED           → rented (excluded from matching)
ARCHIVED         → archived (excluded from matching)
INACTIVE         → owner unresponsive (excluded from matching)
```

### 4.4 SearchDiagnostic

```typescript
interface SearchDiagnostic {
  code: DiagnosticCode;
  message: string;              // user-facing message
  details: string;              // internal diagnostic details
  severity: "INFO" | "WARNING" | "BLOCKER";
  suggestedNextAction: string;  // what the engine recommends
  expansionRequired: boolean;
  userConsentRequired: boolean;
}

type DiagnosticCode =
  | "SUCCESS"                     // results found, no issues
  | "LOW_SCORE"                   // results < threshold but > 0
  | "NO_PROPERTIES_IN_CITY"
  | "NO_PROPERTIES_OF_TYPE"
  | "BUDGET_MISMATCH"
  | "NEIGHBORHOOD_TOO_NARROW"
  | "INVENTORY_EXHAUSTED"
  | "NO_MATCH_ABOVE_THRESHOLD"
  | "ALL_REJECTED"
  | "PENDING_AVAILABILITY"
  | "QUERY_INCOMPLETE"            // missing required field
  | "QUERY_INFEASIBLE"            // contradictory criteria
  | "PERMISSION_DENIED"
  | "INVENTORY_UNAVAILABLE";      // DB/cache error
```

### 4.5 ZeroResultReason

```typescript
type ZeroResultReason =
  | "NO_PROPERTIES"               // city has no properties at all
  | "TYPE_NOT_AVAILABLE"          // city has properties but not this type
  | "BUDGET_TOO_LOW"              // no property within budget in city
  | "NEIGHBORHOOD_EMPTY"          // neighborhood has 0 available properties
  | "ALL_FILTERED_OUT"            // hard filters removed everything
  | "ALL_BELOW_THRESHOLD"         // scored but all below 60
  | "ALL_REJECTED_BY_USER"        // user has rejected everything available
  | "INVENTORY_NOT_LOADED";       // data fetch failure
```

---

## 5. Query Validation

### 5.1 Completeness Check

| Field | Required For | Validation Rule |
|-------|-------------|----------------|
| `intent` | ALL | Must be one of RENT/BUY/INVEST/SELL. Confidence ≥ 0.70 |
| `propertyType` | ALL | Must be a valid PropertyType enum value |
| `city` | ALL | Must be in GEOGRAPHY_MODEL city inventory |
| `neighborhoods` | Only if STRICT mobility | Must be valid neighborhoods in the city |
| `budgetMin` | ALL | Must be > 0. Must be < budgetMax |
| `budgetMax` | ALL | Must be > 0. Must be > budgetMin |
| `budgetType` | ALL | Must match intent (RENT↔RENTAL, BUY↔PURCHASE) |
| `constraints` | Optional | No validation required if null |
| `preferences` | Optional | No validation required if null |

**Missing Field Response:**

```typescript
interface MissingFieldDiagnostic {
  missingFields: string[];
  message: string;
  code: "QUERY_INCOMPLETE";
  severity: "BLOCKER";
}
```

### 5.2 Feasibility Check

| Rule | Condition | Result |
|------|-----------|--------|
| Budget range too narrow | `budgetMax - budgetMin < 100000` (100k FCFA) | Warning: narrow range may limit results |
| Impossible budget for type | e.g., budget 5M for VILLA in Douala | Warning: unrealistic expectations |
| No inventory in city | city has 0 properties in DB | Blocker: cannot search this city |
| Contradictory criteria | e.g., studio + 4 bedrooms | Warning: contradictory constraints |
| Location + intent mismatch | e.g., BUY in neighborhood with only rentals | Warning: check inventory |
| Surface inconsistent with type | e.g., 500m² studio | Warning: unusual combination |

### 5.3 Permission Check

| Permission | Required For | Default |
|------------|-------------|---------|
| `viewUnpublished` | Searching non-public listings | false → filter out |
| `viewPremiumOnly` | Premium/promoted listings | true → include |
| `viewAgentNetwork` | Agent network (non-public inventory) | false → require explicit |
| `viewFutureAvailability` | Construction/pending properties | false → require explicit |

---

## 6. Query Expansion Rules

### 6.1 Automatic Expansions (No Consent Required)

| Situation | Expansion Applied | Level |
|-----------|-----------------|-------|
| No exact properties in neighborhood | Expand to entire city (remove neighborhood filter) | 0→1 |
| Surface too restrictive | ±5% surface range | 1 |
| Price slightly outside | ±5% price range (within tolerance) | 1 |

### 6.2 Consent-Required Expansions

| Expansion | User Message | Level |
|-----------|-------------|-------|
| Adjacent neighborhoods | "No properties in {neighborhood}. Would you like to search nearby areas?" | 2 |
| Budget tolerance | "No properties within your budget in {city}. Can I search slightly above?" | 3 |
| Similar property types | "No {type} available. Would you like to see {family} properties?" | 4 |
| Surrounding cities | "No {type} in {city}. Should I search in nearby cities?" | 5 |

### 6.3 Expansion Inheritance

Each expansion level inherits all relaxations from previous levels:

```
Level 0: strict budget, exact type, exact city, exact neighborhood
Level 1: ±5% surface, minor criteria relaxed
Level 2: L1 + neighborhood → city-wide + adjacent neighborhoods
Level 3: L2 + budget tolerance applied
Level 4: L3 + property type → family expansion
Level 5: L4 + city → surrounding cities
Level 6: L5 + continuous surveillance
Level 7: L6 + future properties included
Level 8: L7 + professional/agent network
```

### 6.4 Forbidden Expansions (Never Relaxed — from WORKFLOW §21)

| Criterion | Why Never Relaxed |
|-----------|------------------|
| Intent (RENT/BUY/SELL/INVEST) | Core business model — cannot mix rental and purchase |
| Transaction type | Incompatible operations cannot be merged |
| Critical fields (per PROPERTY_TYPE) | Per 02-PROPERTY-REFERENCE mandatory fields |
| Excluded/rejected properties | MATCH-017: definitively refused is never reproposed |
| Property status = SOLD/RENTED/ARCHIVED | Absolute exclusion rule MATCH-034 |

---

## 7. Contract Enforcement

### 7.1 Error Codes

| Code | HTTP-style Status | Meaning |
|------|------------------|---------|
| `QUERY_ACCEPTED` | 200 | Query validated, processing |
| `QUERY_INCOMPLETE` | 422 | Required fields missing |
| `QUERY_INFEASIBLE` | 422 | Logically contradictory criteria |
| `PERMISSION_DENIED` | 403 | User lacks required permissions |
| `INVENTORY_UNAVAILABLE` | 503 | Data source unavailable |
| `QUERY_TIMEOUT` | 408 | Processing exceeded time limit |
| `QUERY_REJECTED` | 400 | Malformed input |

### 7.2 Response Guarantees

| Guarantee | Detail |
|-----------|--------|
| **Idempotent** | Same input + same inventory → same results (within TTL) |
| **Deterministic scoring** | Same property always gets same score for same query |
| **Auditable** | Every query execution is logged with full snapshot |
| **Explainable** | Every result includes top 3 matching criteria (MATCH-033) |
| **Consent-tracked** | Every expansion requiring consent is recorded |
| **Bounded execution** | Max 9 levels, timeout after 10 seconds |

---

## 8. Contract Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-15 | Initial canonical contract — aligned with Heritage Gold MATCHING_MODEL |

---

*Canonical document — Search Query Contract for LAWIM V5. Defines the formal contract between Qualification Engine and Search Engine, including input/output types, validation rules, processing pipeline, and expansion rules.*
