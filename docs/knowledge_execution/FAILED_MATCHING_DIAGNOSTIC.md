# Failed Matching Diagnostic

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**Prerequisite:** Heritage Gold — `docs/lawim_heritage_gold/RULE_INDEX.md` (MATCH-009, MATCH-011), `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` (§21 Progressive Search Expansion)

---

## 1. Overview

When matching produces zero results (no property scores ≥ 60), the system must diagnose the root cause, produce a user-facing explanation, and determine the next action. This document defines the diagnostic framework, failure modes, remedies, and escalation paths.

```
Matching Engine → Zero Results
        │
        ▼
┌───────────────────────────────┐
│   Failed Matching Diagnostic  │
│                               │
│   1. Classify failure mode    │
│   2. Build user explanation   │
│   3. Suggest remedy           │
│   4. Determine NBA            │
│   5. Escalate if needed       │
└───────────────────────────────┘
        │
        ▼
Decision Engine → NBA
```

---

## 2. Diagnostic Dimensions

### 2.1 Failure Mode Classification

When matching returns zero results, the system evaluates each diagnostic dimension to identify the root cause:

| # | Diagnostic Dimension | Detection | Condition |
|---|---------------------|-----------|-----------|
| 1 | Inventory empty | No available properties in the system for this city | `count_available(city) = 0` |
| 2 | Criteria too strict | Properties exist but all fail constraints or score < 60 | `count_available(city) > 0` AND `count_matching = 0` |
| 3 | Location not covered | City is not in LAWIM's priority city list | `city NOT IN priority_cities` |
| 4 | Budget mismatch | Properties exist but none within budget tolerance | `count_in_budget_range = 0` AND `count_in_city > 0` |
| 5 | Type mismatch | Properties exist in city+ budget but wrong type | `count_by_type = 0` AND `count_by_city_budget > 0` |
| 6 | All excluded | Properties matched criteria but all excluded by hard constraints | `count_candidates > 0` AND `count_excluded = count_candidates` |
| 7 | All below threshold | Properties scored but none ≥ 60 | `count_scored > 0` AND `max_score < 60` |

### 2.2 Diagnostic Pipeline

```
diagnose_failed_match(dossier, inventory):
  1. Check inventory_empty(dossier.city)
     → If true: DIAG_INVENTORY_EMPTY
     → Stop: no further diagnosis possible

  2. Check location_covered(dossier.city)
     → If false: DIAG_LOCATION_NOT_COVERED
     → Stop: city not in LAWIM coverage

  3. Check budget_mismatch(dossier, inventory)
     → If true AND count_available > 0: DIAG_BUDGET_MISMATCH
     → Continue: may also have type mismatch

  4. Check type_mismatch(dossier, inventory)
     → If true AND count_city_budget > 0: DIAG_TYPE_MISMATCH
     → Continue: may be combined with budget

  5. Check all_excluded(dossier, candidates)
     → If true: DIAG_ALL_EXCLUDED
     → Attach exclusion reasons

  6. Check all_below_threshold(candidates)
     → If true: DIAG_ALL_BELOW_THRESHOLD
     → Attach max_score, min_score

  7. If none of the above → DIAG_CRITERIA_TOO_STRICT
     → General case: properties exist but don't match dossier criteria
```

### 2.3 Diagnostic Output Contract

```json
{
  "diagnostic": {
    "matching_run_id": "match_run_<uuid>",
    "dossier_id": "dossier_<uuid>",
    "result_count": 0,
    "failure_modes": [
      {
        "primary": true,
        "mode": "budget_mismatch",
        "confidence": 0.85,
        "detail": "No properties found within budget range 100000-200000 for rent (±20%) in Douala",
        "supporting_data": {
          "available_in_city": 23,
          "in_budget_range": 0,
          "budget_range": { "min": 100000, "max": 200000 },
          "tolerance_applied": 20,
          "effective_range": { "min": 80000, "max": 240000 },
          "cheapest_available": 250000
        }
      },
      {
        "primary": false,
        "mode": "type_mismatch",
        "confidence": 0.30,
        "detail": "Available properties in Douala are mostly houses; requested type is apartment",
        "supporting_data": {
          "available_types": { "house": 15, "villa": 5, "land": 3 },
          "requested_type": "appartement",
          "type_match_count": 0
        }
      }
    ],
    "inventory_summary": {
      "total_available": 45,
      "in_city": 23,
      "after_constraints": 0,
      "after_scoring": 0
    },
    "progressive_search_available": true,
    "progressive_search_level": 1,
    "remedies": [],
    "human_escalation_required": false,
    "human_escalation_reason": null
  }
}
```

---

## 3. Failure Modes Detail

### 3.1 DIAG_INVENTORY_EMPTY

**Detection:** `count_available(dossier.city) = 0`

**User-facing explanation (FR):**
> "Désolé, nous n'avons actuellement aucun bien disponible à {city}. LAWIM couvre 10 villes prioritaires au Cameroun."

**User-facing explanation (EN):**
> "Sorry, we currently have no properties available in {city}. LAWIM covers 10 priority cities in Cameroon."

**Suggested remedies:**
1. Expand search to neighboring cities (if applicable)
2. Check back later (new listings are added regularly)
3. Request notification when properties become available in this city
4. Ask agent to source properties in this area

**NBA:** `suggest_alternatives` → request city change or notify on new listing

**Progressive Search:** Not applicable (no inventory to expand)

### 3.2 DIAG_LOCATION_NOT_COVERED

**Detection:** `city NOT IN priority_cities = [Douala, Yaoundé, Bafoussam, Bamenda, Buea, Limbe, Kribi, Nkongsamba, Garoua, Maroua]`

**User-facing explanation (FR):**
> "Malheureusement, {city} ne fait pas encore partie de nos villes couvertes. Nous opérons actuellement dans 10 villes au Cameroun : Douala, Yaoundé, Bafoussam, Bamenda, Buea, Limbe, Kribi, Nkongsamba, Garoua et Maroua."

**User-facing explanation (EN):**
> "Unfortunately, {city} is not yet one of our covered cities. We currently operate in 10 cities in Cameroon: Douala, Yaoundé, Bafoussam, Bamenda, Buea, Limbe, Kribi, Nkongsamba, Garoua, and Maroua."

**Suggested remedies:**
1. Ask if user is interested in any of the covered cities
2. Notify user when coverage expands to their city
3. Suggest nearest covered city with similar characteristics

**NBA:** `request_location` → ask for alternative city

**Human escalation:** Not required unless user insists

### 3.3 DIAG_BUDGET_MISMATCH

**Detection:** `count_available(dossier.city) > 0` AND `count_in_budget_range(dossier) = 0`

**User-facing explanation (FR):**
> "Nous avons des biens à {city}, mais aucun ne correspond à votre budget de {budget_min} - {budget_max} FCFA. Le bien le moins cher disponible est à {cheapest} FCFA."

**User-facing explanation (EN):**
> "We have properties in {city}, but none match your budget of {budget_min} - {budget_max} FCFA. The cheapest available property is {cheapest} FCFA."

**Suggested remedies:**
1. Increase budget: "Would you like to see properties up to {suggested_max} FCFA?"
2. Different transaction type: rent vs. buy vs. invest tolerances differ (MATCH-003)
3. Different neighborhood: some neighborhoods have lower prices
4. Wait for new listings that match budget

**NBA:** `request_budget` → suggest revised budget range

**Progressive Search:** Apply flexible budget (MATCH-028): slight increase if other criteria excellent. Expand to next budget tier.

### 3.4 DIAG_TYPE_MISMATCH

**Detection:** `count_by_city_budget(dossier) > 0` AND `count_by_type(dossier) = 0`

**User-facing explanation (FR):**
> "À {city}, les biens disponibles dans votre budget sont principalement des {available_types}. Nous n'avons pas de {requested_type} correspondant actuellement."

**User-facing explanation (EN):**
> "In {city}, available properties in your budget are mainly {available_types}. We currently have no matching {requested_type}."

**Suggested remedies:**
1. Suggest alternative property types available in the same budget
2. Ask if user is open to other property types
3. Show similar types (e.g., studio instead of apartment)
4. Notify when requested type becomes available

**NBA:** `suggest_alternatives` → propose available types

**Progressive Search:** Expand property type to compatible alternatives (MATCH-013 non-compensation: do NOT substitute unrelated types).

### 3.5 DIAG_ALL_EXCLUDED

**Detection:** `count_candidates > 0` AND `count_excluded = count_candidates`

**User-facing explanation (FR):**
> "Des biens correspondent à vos critères mais sont actuellement indisponibles (vendus, loués ou archivés)."

**User-facing explanation (EN):**
> "Some properties match your criteria but are currently unavailable (sold, rented, or archived)."

**Exclusion breakdown:**
| Exclusion Reason | Count | Action |
|-----------------|-------|--------|
| Sold/Rented/Archived | N | Notify if returns to availability |
| Budget outside tolerance | N | Suggest budget adjustment |
| Previously refused | N | Respect refusal; suggest alternatives |
| City different | N | Confirm city preference |

**Suggested remedies:**
1. Notify when unavailable properties become available again
2. Suggest similar properties in same area
3. Relax one constraint (budget, location, type)
4. Check holder response status for pending properties

**NBA:** `suggest_alternatives` OR `continuous_surveillance`

### 3.6 DIAG_ALL_BELOW_THRESHOLD

**Detection:** `count_scored > 0` AND `max_score < 60`

**User-facing explanation (FR):**
> "Nous avons trouvé {count} bien(s) qui se rapprochent de vos critères, mais aucun n'atteint le score minimum de 60/100. Le meilleur score est de {max_score}/100."

**User-facing explanation (EN):**
> "We found {count} properties close to your criteria, but none reach the minimum score of 60/100. The best score is {max_score}/100."

**Scoring breakdown for best candidate:**
| Dimension | Score | Why Low |
|-----------|-------|---------|
| Geographical | X | Distance from requested neighborhood |
| Budget | X | Price above tolerance |
| Property | X | Type mismatch or missing features |
| Behavioral | X | Low lead score |
| Other | X | Low availability or document score |

**Suggested remedies:**
1. Relax neighborhood criteria (expand to neighboring districts)
2. Increase budget tolerance
3. Consider different property type
4. Improve lead data quality (add missing fields)

**NBA:** `suggest_alternatives` → propose relaxing the weakest-scoring dimension

### 3.7 DIAG_CRITERIA_TOO_STRICT (Default)

**Detection:** None of the above specific modes matched

**User-facing explanation (FR):**
> "Aucun bien ne correspond exactement à vos critères actuels. Nous pouvons élargir la recherche ou ajuster certains critères."

**User-facing explanation (EN):**
> "No properties exactly match your current criteria. We can expand the search or adjust some criteria."

**Suggested remedies:**
1. Systematic relaxation: try each relaxation dimension independently
2. Ask user which criterion they are most flexible on
3. Show "almost matching" properties with their scores and gaps

**NBA:** `suggest_alternatives` → Progressive Search Expansion

---

## 4. Remedies and Relaxation Order

### 4.1 Progressive Relaxation Order

When no results are found, the system progressively relaxes criteria in this order:

```
Level 1: Broaden neighborhood (same city, adjacent districts)
Level 2: Relax budget tolerance (next tier)
Level 3: Consider alternative property types
Level 4: Expand to neighboring cities (if affinity exists)
Level 5: Remove comfort criteria
Level 6: Remove preferential criteria
```

**Critical fields are NEVER modified** without demandeur agreement (WORKFLOW_EXTRACTION_COMPLETE §21).

### 4.2 Progressive Search Expansion (WORKFLOW_EXTRACTION_COMPLETE §21)

```
┌────────────────────┐
│  Level 1: Normal   │  ← Current failed match
│  Search            │
└─────────┬──────────┘
          │ (no results)
          ▼
┌────────────────────┐
│  Level 2: Expanded │  Broaden neighborhood, slightly relax budget
│  Search            │
└─────────┬──────────┘
          │ (no results)
          ▼
┌────────────────────┐
│  Level 3: Smart    │  AI-driven alternative suggestions
│  Search            │
└─────────┬──────────┘
          │ (no results)
          ▼
┌────────────────────┐
│  Level 4:          │  Continuous surveillance
│  Continuous        │  (new listings, price drops, availability)
│  Search            │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Level 5: Notify   │  "I'm watching for new listings..."
│  Demandeur         │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  Level 6: Auto     │  Periodic follow-up per SLA
│  Follow-up         │
└────────────────────┘
```

### 4.3 Suggested Remedy Contract

```json
{
  "remedies": [
    {
      "id": "remedy_001",
      "type": "expand_neighborhood",
      "label": "Expand to neighboring districts",
      "description": "Search in Akwa and Bonapriso (neighboring districts to Bonanjo)",
      "expected_impact": "+8 potential properties",
      "user_question": "Would you like to see properties in nearby neighborhoods?",
      "progressive_level": 2
    },
    {
      "id": "remedy_002",
      "type": "relax_budget",
      "label": "Increase budget slightly",
      "description": "Increase max budget from 200,000 to 250,000 FCFA (+25%)",
      "expected_impact": "+3 potential properties",
      "user_question": "Would you like to consider properties up to 250,000 FCFA?",
      "progressive_level": 2
    },
    {
      "id": "remedy_003",
      "type": "change_type",
      "label": "Consider studios",
      "description": "Studios in your budget range are available in Douala",
      "expected_impact": "+5 potential properties",
      "user_question": "Would you like to see studios instead of apartments?",
      "progressive_level": 3
    },
    {
      "id": "remedy_004",
      "type": "continuous_search",
      "label": "Monitor for new listings",
      "description": "I'll watch for new properties matching your criteria",
      "expected_impact": "Notification when new listings appear",
      "user_question": "Shall I notify you when new matching properties become available?",
      "progressive_level": 4
    }
  ]
}
```

---

## 5. Integration with Qualification Engine

### 5.1 Requesting Missing/Relaxed Criteria

When matching fails due to insufficient qualification data, the system requests the Qualification Engine to collect missing criteria:

| Missing Data | Impact | Qualification Request | Priority |
|-------------|--------|---------------------|----------|
| No budget | Cannot evaluate budget dimension | "What is your budget range?" | HIGH |
| No city | Cannot evaluate geographical dimension | "Which city are you interested in?" | HIGH |
| No property type | Cannot evaluate property dimension | "What type of property are you looking for?" | HIGH |
| No neighborhood | Reduced geographical score | "Do you have a preferred neighborhood?" | MEDIUM |
| No transaction type | Cannot determine tolerance | "Are you looking to rent, buy, or invest?" | HIGH |
| Missing comfort criteria | Lower property score | "Any specific features you need?" | LOW |

### 5.2 Relaxed Criteria Flow

```
Matching → Zero Results
        │
        ▼
Diagnose Failure Mode
        │
        ▼
Identify most relaxable criterion
        │
        ▼
┌───────────────────────────────────────┐
│ Ask user:                             │
│ "No properties match exactly. Would   │
│ you like to try [suggested remedy]?"  │
└───────────────┬───────────────────────┘
                │
        ┌───────┴───────┐
        │               │
     (yes)           (no)
        │               │
        ▼               ▼
Apply relaxation   Try next remedy
and rematch        or continuous search
        │               │
        ▼               ▼
   Results?         Ask if they'd
        │           like to be
   ┌────┴───┐       notified
   │        │
 (yes)    (no)
   │        │
   ▼        ▼
Present   Try next
results   remedy
```

---

## 6. Human Escalation

### 6.1 When to Escalate

| Condition | Reason | Escalation Target |
|-----------|--------|-------------------|
| Location not covered and user insists | System cannot help | Agent for manual sourcing |
| All remedies tried, user refuses all | No automated path forward | Agent for personalized assistance |
| High-value lead (P0, diaspora) + no results | Opportunity requires human touch | Agent (immediate) |
| 3+ failed matching attempts | Persistent failure | Agent + diagnostic report |
| User explicitly requests human | User preference | Agent |
| Complex multi-city/multi-type request | Beyond automated matching | Agent |

### 6.2 Escalation Contract

```json
{
  "escalation": {
    "required": true,
    "reason": "high_value_lead_no_results",
    "priority": "P0",
    "agent_note": "Diaspora investor (score: 95) searching in Limbe with budget 50M+. No properties found. All 4 remedy suggestions refused. Requires agent intervention.",
    "diagnostic_attached": true,
    "diagnostic_id": "diag_<uuid>",
    "suggested_agent_action": "Manually source properties in Limbe, contact partner agents, check off-market listings",
    "user_message": "I've noted your preferences and will have a specialized agent contact you shortly to find the perfect property."
  }
}
```

### 6.3 Escalation Levels

| Level | Trigger | Action | SLA |
|-------|---------|--------|-----|
| L1 | City not covered | Suggest covered cities | Immediate |
| L2 | All remedies exhausted | Route to agent dashboard | < 1h |
| L3 | High-value lead + no results | Route to senior agent | < 30 min |
| L4 | User insists on uncovered city | Route to business development | < 24h |

---

## 7. Diagnostic Summary for Dashboard

When matching fails, a summarized diagnostic is displayed on the agent/dashboard:

```
MATCHING DIAGNOSTIC — Dossier #12345
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status:  ZERO RESULTS
Primary failure: Budget mismatch
Confidence: 85%

Inventory in Douala: 23 properties
In budget range: 0 (range: 100k-200k)
Cheapest available: 250k

Suggested remedy: Increase budget to 250k (+3 properties)

Progressive search: Level 2 available
Human escalation: Not required

Rules applied: MATCH-009, MATCH-011, MATCH-022, MATCH-023
```

---

## References

- Heritage Gold: `docs/lawim_heritage_gold/RULE_INDEX.md` (MATCH-009, MATCH-011, MATCH-022, MATCH-023)
- Heritage Gold: `docs/lawim_heritage_gold/MATCHING_MODEL.md` (§2 Budget Tolerance, §5 10-Step Decision Engine)
- Heritage Gold: `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` (§4 Matching Lifecycle, §21 Progressive Search Expansion, §22 Continuous Market Surveillance)
- Matching Architecture: `docs/knowledge_execution/MATCHING_EXECUTION_ARCHITECTURE.md`
- Rematching Policy: `docs/knowledge_execution/REMATCHING_POLICY.md`
- Score Contract: `docs/knowledge_execution/MATCHING_SCORE_CONTRACT.md`
- Global Architecture: `docs/knowledge_execution/GLOBAL_EXECUTION_ARCHITECTURE.md`
