# PROGRESSIVE SEARCH EXPANSION — Extension Progressive de la Recherche LAWIM V5

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** WORKFLOW_EXTRACTION_COMPLETE.md §21 (Progressive Search Expansion Rules), MATCHING_MODEL.md, SEARCH_EXECUTION_ARCHITECTURE.md

---

## 1. Overview

Progressive Search Expansion defines the automatic escalation path when an initial search returns zero or insufficient results. It implements the Heritage Gold principle:

> **Core Rule (WORKFLOW §21):** Critical fields are NEVER modified without demandeur agreement. The proposal must ALWAYS be explained.

The expansion follows a strict level hierarchy. Each level relaxes specific criteria while preserving others. The engine progresses through levels until a minimum result threshold is met or all levels are exhausted.

```
Recherche normale → Recherche élargie → Recherche intelligente → Recherche continue → Notification → Relance auto
(Normal Search)     (Expanded Search)   (Intelligent Search)   (Continuous Search)  (Notification)  (Auto Follow-up)
```

---

## 2. Level Definitions

### 2.1 Level 0: Exact Search (Recherche Normale)

| Aspect | Detail |
|--------|--------|
| **Name** | Exact match — recherche exacte |
| **Entry condition** | Always — initial search |
| **Intent** | Preserved (exact) |
| **Property type** | Preserved (exact) |
| **City** | Preserved (exact) |
| **Neighborhood** | Preserved (if specified, exact match; if not, city-wide) |
| **Budget** | Preserved (within declared range) |
| **Constraints** | Preserved (all strict) |
| **Preferences** | Preserved (all applied) |
| **Permissions** | Standard visibility only |
| **Status filter** | `Disponible` only |
| **User consent required** | No |
| **Exit condition** | ≥ 3 results with score ≥ 60 → return results; else → Level 1 |

### 2.2 Level 1: Strict Compatible Search (Recherche Compatible)

| Aspect | Detail |
|--------|--------|
| **Name** | Strict compatible — compatible strict |
| **Entry condition** | L0 returns < 3 results OR best score < 60 |
| **Criteria PRESERVED** | Intent, property type, city, budget range, neighborhood, status |
| **Criteria RELAXED** | Surface ±5%, rooms ±1, bedrooms ±1, floor removed, parking requirement removed, furnished requirement removed |
| **Criteria FORBIDDEN to relax** | Intent, transaction type, status, property type |
| **User consent required** | No |
| **Explanation** | "I found similar properties with slightly different specifications." |
| **Exit condition** | ≥ 3 results with score ≥ 60 → return results; else → Level 2 |

### 2.3 Level 2: Nearby Search (Recherche Voisinage)

| Aspect | Detail |
|--------|--------|
| **Name** | Nearby — quartiers adjacents |
| **Entry condition** | L1 returns < 3 results |
| **Criteria PRESERVED** | Intent, property type, city, budget range, status |
| **Criteria RELAXED** | **Neighborhood** → expanded to adjacent neighborhoods with similar characteristics (WORKFLOW §21: "propose neighboring districts with similar characteristics"), surface ±10% |
| **Criteria FORBIDDEN to relax** | Intent, transaction type, status, property type |
| **User consent required** | **YES** — "No properties in {neighborhood}. Would you like to see nearby areas like {adjacent1}, {adjacent2}?" |
| **Geographic expansion** | Adjacent neighborhoods only (same city), proximity level ≤ 3 |
| **Explanation** | "Expanding to nearby neighborhoods: {list}. These areas have similar characteristics." |
| **Exit condition** | ≥ 3 results with score ≥ 60 → return results; else → Level 3 |

### 2.4 Level 3: Budget Tolerance Search (Recherche Budget Tolérance)

| Aspect | Detail |
|--------|--------|
| **Name** | Budget tolerance — tolérance budgétaire |
| **Entry condition** | L2 returns < 3 results OR best score < 60 |
| **Criteria PRESERVED** | Intent, property type, city, neighborhood (expanded), status |
| **Criteria RELAXED** | **Budget** → expanded by tolerance (Rent ±20%, Buy ±15%, Invest ±25% — from MATCHING_MODEL §2), surface ±15% |
| **Criteria FORBIDDEN to relax** | Intent, transaction type, status, property type |
| **User consent required** | **YES** — "No properties within your budget range. Can I search slightly above (up to {tolerance}%)?" |
| **Constraint** | Budget increase ONLY if other criteria are excellent OR user has already accepted comparable properties (WORKFLOW §21) |
| **Explanation** | "I've extended the budget range by {tolerance}% to find more options." |
| **Exit condition** | ≥ 3 results with score ≥ 60 → return results; else → Level 4 |

### 2.5 Level 4: Property-Type Relaxation (Recherche Type Élargi)

| Aspect | Detail |
|--------|--------|
| **Name** | Type relaxation — élargissement type de bien |
| **Entry condition** | L3 returns < 3 results |
| **Criteria PRESERVED** | Intent, city, budget (expanded), status |
| **Criteria RELAXED** | **Property type** → expanded to family (e.g., Apartment → Studio, Duplex, Penthouse; House → Villa; Land → all land subtypes) |
| **Criteria FORBIDDEN to relax** | Intent, transaction type, status, non-compensation principle (MATCH-013: terrain does not compensate villa) |
| **Family mapping** | See §7 — Property Type Families |
| **User consent required** | **YES** — "There are few {type} available. Would you like to see {family} properties?" |
| **Explanation** | "Showing {family} properties which share similar characteristics with {type}." |
| **Exit condition** | ≥ 3 results with score ≥ 60 → return results; else → Level 5 |

### 2.6 Level 5: Location Expansion (Recherche Localisation Élargie)

| Aspect | Detail |
|--------|--------|
| **Name** | Location expansion — extension géographique |
| **Entry condition** | L4 returns < 3 results |
| **Criteria PRESERVED** | Intent, budget (expanded), type (expanded), status |
| **Criteria RELAXED** | **City** → neighboring cities / same department / same region (ordered by distance and similarity score) |
| **Criteria FORBIDDEN to relax** | Intent, transaction type, status |
| **User consent required** | **YES** — "No {type} available in {city}. Should I search in nearby cities like {city1}, {city2}?" |
| **Geographic expansion** | Distance-ordered: adjacent cities first, then same department, then same region |
| **Explanation** | "Expanding search to {city_list}. These cities are within reasonable distance." |
| **Exit condition** | ≥ 3 results with score ≥ 60 → return results; else → Level 6 |

### 2.7 Level 6: Continuous Surveillance Activation

| Aspect | Detail |
|--------|--------|
| **Name** | Continuous surveillance — surveillance continue |
| **Entry condition** | L5 returns < 3 results OR user agrees to monitoring |
| **What happens** | Search is saved as a surveillance profile. Engine monitors new listings, price drops, status changes |
| **User consent required** | **YES** — "I'll notify you when matching properties become available. Would you like me to monitor the market?" |
| **Follow-up schedule** | J+7 / J+30 / J+90 (from WORKFLOW §24) |
| **Exit condition** | New property found → notify user. Dossier closed → stop surveillance. 90 days inactivity → archive |

### 2.8 Level 7: Future Availability Search

| Aspect | Detail |
|--------|--------|
| **Name** | Future availability — disponibilité future |
| **Entry condition** | Explicit user request OR system recommendation |
| **Criteria PRESERVED** | Intent, property type, budget (expanded), city (expanded), status |
| **Criteria RELAXED** | **Status** → includes PENDING_CONSTRUCTION, RESERVED, UNDER_NEGOTIATION |
| **User consent required** | **YES** — "Some properties match but aren't available yet. Would you like to see upcoming options?" |
| **Explanation** | "These properties match your criteria but are not immediately available." |
| **Results** | Max 5, scored with availability penalty (-20 on transaction success score) |

### 2.9 Level 8: Professional Search

| Aspect | Detail |
|--------|--------|
| **Name** | Professional search — recherche professionnelle |
| **Entry condition** | Explicit user request + user has agent/investor permissions |
| **Criteria PRESERVED** | Intent, property type, budget (expanded), city (expanded) |
| **Criteria RELAXED** | **Visibility** → includes AGENT_NETWORK, PREMIUM, UNPUBLISHED |
| **User consent required** | **YES** — "As a professional, you can access additional listings. Search the agent network?" |
| **Results** | Max 5, includes agent commission notes if applicable |

---

## 3. Level Transition Diagram

```
                    ┌─────────────────────────────────────────────┐
                    │              SEARCH START                    │
                    │        (Qualification Complete)              │
                    └───────────────────┬─────────────────────────┘
                                        │
                                        ▼
              ┌─────────────────────────────────────────┐
              │   LEVEL 0: EXACT SEARCH                  │
              │   All criteria strict, status=Disponible │
              └──────────┬──────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │ Results ≥ 3 & ≥60?  │───YES──→ Return Results
              └──────────┬──────────┘
                         │ NO
                         ▼
              ┌─────────────────────────────────────────┐
              │   LEVEL 1: STRICT COMPATIBLE             │
              │   Relax: surface ±5%, rooms, floor, etc │
              └──────────┬──────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │ Results ≥ 3 & ≥60?  │───YES──→ Return Results
              └──────────┬──────────┘
                         │ NO
                         ▼
              ┌─────────────────────────────────────────┐
              │   LEVEL 2: NEARBY SEARCH                 │
              │   Relax: adjacent neighborhoods          │
              │   ⚠ User consent required               │
              └──────────┬──────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │ Results ≥ 3 & ≥60?  │───YES──→ Return Results
              └──────────┬──────────┘
                         │ NO
                         ▼
              ┌─────────────────────────────────────────┐
              │   LEVEL 3: BUDGET TOLERANCE              │
              │   Relax: ± tolerance (rent 20/buy 15/inv 25)│
              │   ⚠ User consent required               │
              └──────────┬──────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │ Results ≥ 3 & ≥60?  │───YES──→ Return Results
              └──────────┬──────────┘
                         │ NO
                         ▼
              ┌─────────────────────────────────────────┐
              │   LEVEL 4: PROPERTY-TYPE RELAXATION      │
              │   Relax: type → family                   │
              │   ⚠ User consent required               │
              └──────────┬──────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │ Results ≥ 3 & ≥60?  │───YES──→ Return Results
              └──────────┬──────────┘
                         │ NO
                         ▼
              ┌─────────────────────────────────────────┐
              │   LEVEL 5: LOCATION EXPANSION            │
              │   Relax: city → surrounding cities       │
              │   ⚠ User consent required               │
              └──────────┬──────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │ Results ≥ 3 & ≥60?  │───YES──→ Return Results
              └──────────┬──────────┘
                         │ NO
                         ▼
              ┌─────────────────────────────────────────┐
              │   LEVEL 6: CONTINUOUS SURVEILLANCE       │
              │   Monitor new listings, price drops      │
              │   ⚠ User consent required               │
              └──────────┬──────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────────────────────────┐
              │   LEVEL 7: FUTURE AVAILABILITY           │
              │   Include pending/construction           │
              │   (Only if user explicitly requests)     │
              └──────────┬──────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────────────────────────┐
              │   LEVEL 8: PROFESSIONAL SEARCH           │
              │   Agent network, non-public              │
              │   (Only if user has permissions)         │
              └─────────────────────────────────────────┘
```

---

## 4. Criteria Management Per Level

### 4.1 Criteria Preserved Across All Levels

| Criterion | Rationale |
|-----------|-----------|
| **Intent** | Core business model — cannot mix RENT/BUY/INVEST/SELL (MATCH-013) |
| **Transaction type** | Operation type is fundamental (MATCH-002: Operation=20% weight) |
| **Property status** | Cannot show SOLD/RENTED/ARCHIVED (MATCH-034: absolute rule) |
| **Excluded properties** | User blacklist is absolute (MATCH-017) |
| **Non-compensation** | A terrain does not compensate a villa (MATCH-013) |

### 4.2 Criteria That May Be Relaxed (with Stages)

| Criterion | L0 | L1 | L2 | L3 | L4 | L5 |
|-----------|:--:|:--:|:--:|:--:|:--:|:--:|
| Surface | Strict | ±5% | ±5% | ±15% | ±15% | ±15% |
| Rooms | Strict | ±1 | ±1 | ±1 | ±1 | ±1 |
| Bedrooms | Strict | ±1 | ±1 | ±1 | ±1 | ±1 |
| Floor | Strict | Removed | Removed | Removed | Removed | Removed |
| Parking | Strict | Removed | Removed | Removed | Removed | Removed |
| Furnished | Strict | Removed | Removed | Removed | Removed | Removed |
| Neighborhood | Strict | Strict | Adjacent | Adjacent | Adjacent | Adjacent |
| Budget | Strict | Strict | Strict | ±Tol | ±Tol | ±Tol |
| Property type | Strict | Strict | Strict | Strict | Family | Family |
| City | Strict | Strict | Strict | Strict | Strict | Surrounding |

### 4.3 Criteria Forbidden To Relax

| Criterion | Rule Reference | Consequence If Relaxed |
|-----------|---------------|----------------------|
| Intent | MATCH-013, QUAL-008 | Wrong user journey, broken business model |
| Transaction type | MATCH-002 | Scoring weights would be misapplied |
| Property SOLD/RENTED/ARCHIVED | MATCH-034, MATCH-024 | Legal/commercial risk |
| Property blacklisted by user | MATCH-017 | User trust violation |
| Non-compensation | MATCH-013 | False expectations |

---

## 5. User Consent Protocol

### 5.1 Consent Requirement Per Level

| Level | Consent Required | Consent Model |
|-------|:---------------:|--------------|
| L0: Exact | No | Automatic |
| L1: Compatible | No | Automatic (minor relaxations, no material impact) |
| L2: Nearby | **Yes** | Explicit — propose specific adjacent neighborhoods |
| L3: Budget Tolerance | **Yes** | Explicit — explain tolerance % and impact |
| L4: Type Relaxation | **Yes** | Explicit — show family mapping |
| L5: Location Expansion | **Yes** | Explicit — list candidate cities |
| L6: Surveillance | **Yes** | Opt-in at dossier creation or on suggestion |
| L7: Future | **Yes** | Explicit — explain availability delay |
| L8: Professional | **Yes** | Explicit — requires role check |

### 5.2 Consent Message Template

```
When consent is required, the engine produces:

{
  "type": "EXPANSION_CONSENT_REQUEST",
  "currentLevel": 2,
  "nextLevel": 3,
  "reason": "No properties found within original budget range",
  "whatWillChange": "Budget tolerance of ±{tolerance}% will be applied",
  "whatWontChange": "City ({city}), property type ({type}), neighborhood ({neighborhood})",
  "userMessage": "I couldn't find properties within XAF {min}-{max} in {neighborhood}. "
               + "Can I search up to XAF {newMax}? This would give us {estimatedCount} more options.",
  "consentRequired": true,
  "consentExpiry": "2026-07-15T12:00:00Z"  // 24h timeout
}
```

### 5.3 User Response Handling

| User Response | Action |
|---------------|--------|
| `ACCEPT` | Execute next level, record consent in audit trail |
| `REJECT` | Stay at current level, return best-effort results, propose surveillance |
| `MODIFY` | Present modified criteria, ask for specific input |
| `TIMEOUT` (no response in 24h) | Stay at current level, auto-activate surveillance |

---

## 6. Results Produced Per Level

| Level | Max Results | Min Score Threshold | Expected Quality |
|-------|:-----------:|:-------------------:|:----------------:|
| 0: Exact | 10 | 60 | High precision |
| 1: Compatible | 10 | 60 | High precision |
| 2: Nearby | 10 | 55 | Medium-high (location relaxed) |
| 3: Budget Tolerance | 10 | 50 | Medium (budget relaxed) |
| 4: Type Relaxation | 10 | 50 | Medium (type broader) |
| 5: Location Expansion | 10 | 45 | Lower (location broader) |
| 6: Surveillance | N/A | 60 (notify threshold) | High (new listings only) |
| 7: Future | 5 | 40 | Lower (availability uncertain) |
| 8: Professional | 5 | 40 | Variable (network-dependent) |

At each level, results are scored and ranked with the standard scoring pipeline. Only results meeting the min score threshold are returned.

---

## 7. Property Type Families

Family mapping used at Level 4 expansion:

| Family | Includes |
|--------|----------|
| **Residential** | Apartment, House, Villa, Studio, Duplex, Penthouse, Room |
| **Land** | Land Residential, Land Agricultural, Land Industrial |
| **Commercial** | Commercial, Office, Building |
| **Industrial** | Warehouse, Factory |
| **Agricultural** | Farm |
| **Hospitality** | Hotel |

Family expansion rules:
- A Residential type can expand to any other Residential type
- A Land type can expand to any other Land type
- Cross-family expansion is NEVER automatic (MATCH-013: non-compensation)
- Cross-family requires explicit user request and diagnostic explanation

---

## 8. Audit Trail

### 8.1 Audit Record Per Expansion Step

```typescript
interface ExpansionAuditRecord {
  id: string;
  searchId: string;
  dossierId: string;
  userId: string;

  // Expansion details
  fromLevel: number;
  toLevel: number;
  timestamp: string;

  // Relaxations applied
  relaxations: {
    criterion: string;       // e.g., "neighborhood", "budget", "type"
    oldValue: any;
    newValue: any;
    reason: string;
  }[];

  // Consent tracking
  consent: {
    required: boolean;
    obtained: boolean;
    obtainedAt: string | null;
    method: "AUTO" | "USER_ACCEPT" | "USER_REJECT" | "TIMEOUT";
  };

  // Results
  resultsBeforeExpansion: number;
  resultsAfterExpansion: number;

  // Decision
  outcome: "SUCCESS" | "INSUFFICIENT" | "MAXED_OUT";
}
```

### 8.2 Audit Storage

| Requirement | Detail |
|-------------|--------|
| **Storage** | Immutable event log (append-only) |
| **Retention** | Duration of dossier lifecycle + 3 years (per WORKFLOW §11) |
| **Queryable by** | searchId, dossierId, userId, level |
| **Use cases** | Debugging, optimization, learning, user history |

---

## 9. Exit Conditions

### 9.1 When to Stop Expanding

| Condition | Action |
|-----------|--------|
| Results ≥ threshold (3) AND best score ≥ 60 | Stop expansion, return results |
| All 9 levels exhausted | Stop, activate surveillance |
| User explicitly rejects all expansions | Stop, save best-effort results |
| Dossier closed or user inactive | Stop all expansion |
| 90 days without user interaction | Archive dossier, stop expansion |

### 9.2 Result Threshold by Context

| Context | Threshold | Rationale |
|---------|:---------:|-----------|
| Initial search | 3 results | Minimum viable choice set |
| Rematching (J+7) | 2 new results | At least some progress |
| Continuous surveillance | 1 new result | Worth notifying |
| Post-rejection rematching | 1 new result | At least one fresh option |

---

## 10. Edge Cases

| Scenario | Handling |
|----------|----------|
| User accepts L2 (nearby) but still 0 results | Continue to L3 automatically (since consent chain is established) |
| User rejects L2 consent | Stay at L1 results. Offer surveillance. Record preference. |
| L3 budget expansion still returns 0 | Skip to L5 (location) — no point in type relaxation if budget was the issue |
| L4 type family empty in city | Skip directly to L5 (location expansion) — diagnostic: "type family not available in city" |
| Every expansion level exhausted | Activate surveillance. Follow-up message: "I am actively pursuing your search. Since our last exchange, no property exactly matches your criteria. Would you like to maintain your search as-is or explore some alternatives?" (WORKFLOW §22) |
| User keeps rejecting results across expansions | After 3 total rejections → rematch diagnostic mode (MATCH-014) |
| Property becomes available at a higher expansion level | Re-score at current level. If score ≥ 60, promote to top. |

---

## 11. Gold Knowledge Register — Progressive Search Expansion

| ID (PSE-) | Concept | Description | Source | Confidence |
|-----------|---------|-------------|--------|------------|
| PSE-001 | 6-Stage Expansion | Normal → Expanded → Intelligent → Continuous → Notification → Auto Follow-up | WORKFLOW §21 | HIGH |
| PSE-002 | Progressive Dimensions | Neighborhood, distance, GPS, compatible variants, flexible criteria | WORKFLOW §21 | HIGH |
| PSE-003 | Critical Fields Never Modified | No modification without demandeur agreement | WORKFLOW §21 | VERY HIGH |
| PSE-004 | Budget Increase Constraint | Only if other criteria excellent OR user accepted comparable | WORKFLOW §21 | HIGH |
| PSE-005 | Location Fallback | Propose neighboring districts with similar characteristics | WORKFLOW §21 | HIGH |
| PSE-006 | Always Explain | Every proposal must be explained | WORKFLOW §21 | VERY HIGH |
| PSE-007 | Refused Property Exceptions | Price decrease, major modification, changed need, explicit request | WORKFLOW §21, MATCH-018 | VERY HIGH |

---

*Canonical document — Progressive Search Expansion for LAWIM V5. Defines the 9-level expansion hierarchy, criteria management rules, user consent protocol, and audit trail requirements. Fully aligned with Heritage Gold WORKFLOW_EXTRACTION_COMPLETE §21.*
