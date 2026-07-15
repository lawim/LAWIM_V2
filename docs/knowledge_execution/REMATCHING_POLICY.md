# Rematching Policy

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**Prerequisite:** Heritage Gold — `docs/lawim_heritage_gold/RULE_INDEX.md` (MATCH-014 to MATCH-018)

---

## 1. Overview

Rematching is the process of re-running the matching pipeline for an existing dossier in response to a context change. It follows strict rules to avoid redundant computation, ensure fairness, and learn from past outcomes.

**Core principles:**
- Never restart from zero (MATCH-015)
- Only recalc concerned dossiers (MATCH-016)
- Definitely refused properties are never reproposed (MATCH-017), with explicit exceptions (MATCH-018)
- Learning from refusals: 3 refusals → reprioritization (MATCH-014)

---

## 2. Rematching Triggers

### 2.1 Demandeur-Side Triggers

| Trigger | Description | Rematch Scope | Rule |
|---------|-------------|---------------|------|
| Budget modification | User changes budget range | Full recalc on budget dimension for all candidates | MATCH-016 |
| City change | User changes target city | Full recalc on geographical dimension | MATCH-016 |
| Neighborhood change | User changes target neighborhood | Full recalc on geographical dimension | MATCH-016 |
| Property type change | User changes desired property type | Full recalc on property dimension | MATCH-016 |
| New criterion added | User adds critical/comfort/preferential criterion | Partial recalc: property dimension updated | MATCH-016 |
| Criterion removed | User removes a criterion | Partial recalc: property dimension updated | MATCH-016 |
| Property refusal | User explicitly rejects a proposed property | Blacklist property, re-rank remaining | MATCH-017, MATCH-014 |
| Visit abandonment | User abandons scheduled visit | Flag dossier for rematch | — |
| New preference | User expresses new preference | Apply preference to scoring | — |
| Confirmation of interest | User confirms interest in a property | No rematch needed; advance to contact | — |

### 2.2 Property-Side Triggers

| Trigger | Description | Rematch Scope | Rule |
|---------|-------------|---------------|------|
| New publication | New property matching dossier criteria | Add new candidate, score, and rank | — |
| Property modification | Property details updated | Re-score this property | — |
| Price decrease | Price reduced | Re-evaluate budget dimension | MATCH-018 |
| Price increase | Price increased | Re-evaluate budget dimension | — |
| Availability change | Property becomes available/unavailable | Update availability score or exclude | — |
| Photo addition | New photos added | Data quality score update | — |
| GPS addition | GPS coordinates added | Geographical score update | — |
| Document addition | Title/document added | Document score update | — |
| Qualification improvement | Data quality score improves | Re-score property dimension | — |

### 2.3 Holder-Side Triggers

| Trigger | Description | Rematch Scope |
|---------|-------------|---------------|
| Acceptance | Holder accepts contact request | Advance to mise en relation |
| Refusal | Holder refuses contact | Re-rank remaining candidates |
| No response | Holder does not respond | Trigger holder silence workflow |
| Temporary unavailability | Holder marks property unavailable | Exclude property temporarily |
| Return to availability | Holder marks property available again | Re-include property |

### 2.4 System-Side Triggers

| Trigger | Description | Frequency | Rule |
|---------|-------------|-----------|------|
| New business rule | System configuration updated | On deploy | — |
| Periodic recalculation | Scheduled recalc for stale dossiers | Per SLA by property type | MATCH-016 |
| Global learning | Model/weight update from aggregated data | Batch | — |
| Data correction | System data error corrected | On correction | — |
| Auto-rematch J+7 | 7 days since last match | Per SLA table | MATCHING_MODEL §13 |

### 2.5 SLA for First Rematching by Property Type

| Property Type | First Rematching SLA |
|---------------|---------------------|
| Chambre | 24 h |
| Studio | 48 h |
| Appartement | 72 h |
| Maison | 5 days |
| Villa | 7 days |
| Duplex | 7 days |
| Terrain résidentiel | 10 days |
| Terrain agricole | 15 days |
| Terrain industriel | 20 days |
| Commerce | 7 days |
| Bureau | 10 days |
| Entrepôt | 15 days |
| Hôtel | 30 days |
| Immeuble | 30 days |

---

## 3. Rematching Algorithm

### 3.1 Core Principle: Never Restart from Zero (MATCH-015)

When rematching is triggered, the system MUST NOT discard previous scores and recalculate from scratch. Instead:

```
rematch(dossier, trigger_event):
  1. Load previous matching state:
     - previous_candidates[] with scores
     - blacklisted_property_ids[]
     - refusal_history[] with counts
     - previously_proposed_ids[]
     - last_matching_timestamp

  2. Identify scope of change from trigger_event:
     - If budget_change → only recalculate budget dimension
     - If location_change → only recalculate geographical dimension
     - If type_change → only recalculate property dimension
     - If new_property → only score the new property
     - If price_change → only recalculate budget dimension for affected
     - If refusal → only update blacklist and re-rank
     - If system_recalc → full recalc (but preserve refusal history)

  3. Apply changes:
     - Update only affected dimensions
     - Preserve all unaffected dimension scores from previous run
     - Recompute global score only for affected properties

  4. Apply learning (MATCH-014):
     - If refusal_count >= 3 for any property → reprioritization

  5. Re-rank:
     - Sort by new final_scores
     - Re-apply diversity (MATCH-032)
     - Re-check diversity (new properties may change groups)

  6. Audit:
     - Record rematch_reason, scope, previous_scores_snapshot, new_scores
```

**Rationale:** Computing all 5 dimensions for every property on every rematch is expensive and unnecessary. Only the dimensions affected by the trigger event need recalculation.

### 3.2 Only Concerned Dossiers (MATCH-016)

When a property-side or system-side event occurs, only dossiers whose criteria match the change scope are recalculated:

```
identify_concerned_dossiers(event):
  - If new_property → only dossiers with matching city + type + budget
  - If price_change → only dossiers whose budget range covers the price
  - If availability_change → only dossiers that had this property in candidates
  - If system_recalc → only dossiers with stale scores (> SLA age)
```

### 3.3 Rematching Flow

```
┌──────────────────────────────┐
│     Context Change Event     │
│  (demandeur/property/holder/ │
│   system)                    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Identify Trigger Type        │
│ & Affected Dossiers          │
│ (MATCH-016)                  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Load Previous Matching State │
│ Preserve unaffected scores   │
│ (MATCH-015)                  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Apply Scope-Based Recalc     │
│ - Only affected dimensions   │
│ - Only affected properties   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Apply Refusal Learning       │
│ 3 refusals → reprioritize    │
│ (MATCH-014)                  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Re-rank & Re-apply Diversity │
│ (MATCH-032)                  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Build Result + Audit Trail   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Decision Engine → NBA        │
└──────────────────────────────┘
```

---

## 4. Definitely Refused Properties (MATCH-017, MATCH-018)

### 4.1 General Rule (MATCH-017)

A property that has been definitively refused by the demandeur is NEVER reproposed.

```
on_refusal(dossier_id, property_id):
  blacklist.add(property_id, dossier_id, reason="explicit_refusal")
  property.refusal_count += 1
  if property.refusal_count >= 3 for this dossier:
    trigger_reprioritization(dossier_id, property_id)
```

### 4.2 Exceptions (MATCH-018)

A refused property MAY be reproposed ONLY if one of the following conditions is met:

| Exception | Condition | Validation Required |
|-----------|-----------|-------------------|
| Significant price decrease | Price reduced by ≥ 10% from last proposition | Compare current price vs price at refusal time |
| Major modification | Property modified: new photos, updated description, GPS added, documents added | Verify at least 2 property fields changed |
| Changed need | Demandeur's criteria changed significantly enough that the property is now a better match | Re-score with new criteria; score must increase by ≥ 15 points |
| Explicit request | Demandeur asks to see the property again | No validation needed; user request overrides |

**All four exceptions require re-scoring the property with current criteria before reproposing.** The re-scored result must meet the minimum threshold (≥ 60, MATCH-009).

```
can_repropose(dossier_id, property_id):
  exceptions = check_exceptions(property_id, dossier_id)
  
  if exceptions.contains("price_decrease") AND price_drop >= 10%:
    new_score = recalculate_score(property_id, dossier_id)
    return new_score >= 60
  
  if exceptions.contains("major_modification") AND fields_changed >= 2:
    new_score = recalculate_score(property_id, dossier_id)
    return new_score >= 60
  
  if exceptions.contains("changed_need") AND score_increase >= 15:
    new_score = recalculate_score(property_id, dossier_id)
    return new_score >= 60
  
  if exceptions.contains("explicit_request"):
    new_score = recalculate_score(property_id, dossier_id)
    return new_score >= 60
  
  return false
```

### 4.3 Blacklist Management

| Operation | Description | Retention |
|-----------|-------------|-----------|
| Add to blacklist | Property refused → add to dossier's blacklist | Until exception applies or dossier closed |
| Remove from blacklist | Exception triggered → remove from blacklist | After reproposition (re-add if refused again) |
| Clear blacklist | Dossier closed → blacklist archived with dossier | Permanent in audit |
| Global blacklist | Property refused by 10+ users → flagged for holder | Holder notification |

---

## 5. Learning from Refusals (MATCH-014)

### 5.1 Reprioritization on 3 Refusals

When a property has been refused 3 times by the same demandeur:

```
trigger_reprioritization(dossier_id, property_id):
  1. Mark property as "reprioritized" for this dossier
  2. Reduce property's score by 20 points on future matching runs
  3. If property type is refused 3+ times across different properties:
     - Reduce property_type weight for this dossier
     - Boost alternative property types
  4. If neighborhood is refused:
     - Reduce neighborhood affinity score
     - Boost alternative neighborhoods
```

### 5.2 Refusal Pattern Analysis

The system analyzes refusal patterns to detect:

| Pattern | Detection | Action |
|---------|-----------|--------|
| Same type refused 3x | 3 refusals on appartements | Reduce type weight, boost other types |
| Same neighborhood refused 3x | 3 refusals in bonanjo | Reduce neighborhood weight, suggest alternatives |
| Same price range refused 3x | 3 refusals at 250k-300k | Suggest different budget tier |
| Same holder refused 3x | 3 refusals from same holder | Reduce holder reliability score |

### 5.3 Refusal Types

| Refusal Type | Description | Score Impact | Rematch Behavior |
|-------------|-------------|-------------|------------------|
| explicit_refusal | User says "no" or "not interested" | Blacklist property | Re-rank without property |
| silent_refusal | User ignores proposition for > SLA | Score -= 10 | Re-rank with penalty |
| visit_abandonment | User schedules but abandons visit | Score -= 15 | Re-rank with penalty |
| negotiation_failure | User enters negotiation but fails | Score -= 5 | Re-rank with penalty |

---

## 6. Audit Trail for Rematching Decisions

Every rematching operation produces an immutable audit record:

```json
{
  "rematch_audit": {
    "rematch_id": "rematch_<uuid>",
    "dossier_id": "dossier_<uuid>",
    "trigger": {
      "type": "budget_modification",
      "event": "User changed budget from 150000-300000 to 200000-400000",
      "timestamp": "2026-07-15T15:00:00Z",
      "source": "user_input"
    },
    "previous_state": {
      "matching_run_id": "match_run_abc",
      "timestamp": "2026-07-14T10:00:00Z",
      "result_count": 5,
      "top_score": 82,
      "candidate_count": 12
    },
    "rematch_scope": {
      "dimensions_recalculated": ["budget"],
      "properties_added": ["prop_new_001"],
      "properties_removed": [],
      "properties_blacklisted": [],
      "properties_reprioritized": []
    },
    "new_state": {
      "matching_run_id": "match_run_def",
      "timestamp": "2026-07-15T15:00:05Z",
      "result_count": 6,
      "top_score": 88,
      "candidate_count": 13
    },
    "rules_applied": [
      "MATCH-015",
      "MATCH-016",
      "MATCH-017"
    ]
  }
}
```

---

## 7. Integration with NBA

### 7.1 NBA Actions after Rematching

| Rematch Result | NBA | Description |
|---------------|-----|-------------|
| New results found, count > 0 | `present_properties` | Show new/updated matching results |
| New results found, count = 0 | `suggest_alternatives` | Suggest search expansion |
| Same results, same scores | `notify_no_change` | Inform user no new properties found |
| Price decrease detected | `notify_price_drop` | Inform user of price reduction on matched property |
| New property in criteria | `notify_new_listing` | Alert user about new matching property |
| 3 refusals accumulated | `suggest_alternatives` | Propose different property types or neighborhoods |

### 7.2 Rematching NBA Priority

| Priority | Action | When |
|----------|--------|------|
| 1 | `present_properties` | New results available after rematch |
| 2 | `notify_price_drop` | Price decreased on existing match |
| 3 | `notify_new_listing` | New property matching criteria |
| 4 | `suggest_alternatives` | No new results, pattern detected |
| 5 | `notify_no_change` | No improvement from rematch |

---

## 8. Continuous Market Surveillance

Even without user interaction, the system continuously monitors for rematch-worthy events (WORKFLOW_EXTRACTION_COMPLETE §22):

- New publications matching open dossiers
- Price decreases
- Returns to availability
- Holder responses
- SLA-triggered periodic rematch

When a relevant event is detected, the system performs a targeted rematch on only the affected dossiers and determines the appropriate NBA.

---

## References

- Heritage Gold: `docs/lawim_heritage_gold/RULE_INDEX.md` (MATCH-014 to MATCH-018)
- Heritage Gold: `docs/lawim_heritage_gold/MATCHING_MODEL.md` (§13 Rematching Rules)
- Heritage Gold: `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` (§4 Matching Lifecycle, §22 Continuous Market Surveillance)
- Matching Architecture: `docs/knowledge_execution/MATCHING_EXECUTION_ARCHITECTURE.md`
- Global Architecture: `docs/knowledge_execution/GLOBAL_EXECUTION_ARCHITECTURE.md`
