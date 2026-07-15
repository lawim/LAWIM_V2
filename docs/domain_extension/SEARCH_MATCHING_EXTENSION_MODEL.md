# SEARCH & MATCHING EXTENSION MODEL

**Document ID:** LAWIM-H13-MATCHING-EXT-V1
**Status:** CANONICAL DOMAIN EXTENSION
**Date:** 2026-07-15
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §6 (Matching Engine)
**Source Crosswalks:** required_extensions.json (matching section), MATCHING_MODEL.md (Gold), WORKFLOW_03 (Gold)

---

## Table of Contents

1. [Decision Framework](#1-decision-framework)
2. [Match Entity](#2-match-entity)
3. [Scoring Dimensions](#3-scoring-dimensions)
4. [Geographic Scoring](#4-geographic-scoring)
5. [Compatibility Levels](#5-compatibility-levels)
6. [Matching Roles](#6-matching-roles)
7. [Constraint System](#7-constraint-system)
8. [Boost & Penalty Rules](#8-boost--penalty-rules)
9. [Rematching Engine](#9-rematching-engine)
10. [Progressive Search Expansion](#10-progressive-search-expansion)
11. [Continuous Market Surveillance](#11-continuous-market-surveillance)
12. [Market Tension Index](#12-market-tension-index)
13. [Dossier Health Score](#13-dossier-health-score)
14. [Property Health Score](#14-property-health-score)
15. [Failed Matching Diagnostics](#15-failed-matching-diagnostics)
16. [Verification-Only Fields](#16-verification-only-fields)
17. [Transaction Blockers](#17-transaction-blockers)
18. [Complete Extension Mapping Table](#18-complete-extension-mapping-table)

---

## 1. Decision Framework

Each matching concept is assessed against five possible decisions:

| Decision | Meaning | Used When |
|----------|---------|-----------|
| **CREATE_NEW_ENTITY** | Build a new entity with dedicated attributes | No V2 equivalent; domain-specific semantics |
| **ENRICH_CURRENT** | Extend existing V2 entity with additional fields | V2 has base model but missing attributes |
| **CREATE_NEW_ENGINE** | Build a new algorithmic engine | No V2 equivalent; computational logic |
| **CONFIGURE_EXISTING** | Parameterize existing system | V2 has capability but needs configuration |
| **HUMAN_DECISION_REQUIRED** | Cannot finalize without product/domain authority | Unresolved design question |

### 1.1 Matching Decision Summary

| # | Concept | Decision | Rationale |
|---|---------|----------|-----------|
| 1 | Match Entity | CREATE_NEW_ENTITY | No matching entity exists in V2 |
| 2 | Scoring Engine | CREATE_NEW_ENGINE | No algorithmic scoring exists in V2 |
| 3 | Geographic Scoring | CREATE_NEW_ENGINE | Distance-based scoring with 5 levels |
| 4 | Compatibility Levels | CONFIGURE_EXISTING | Threshold-based classification on score |
| 5 | Matching Roles | CONFIGURE_EXISTING | Role-based scoring weight configuration |
| 6 | Hard Constraints | CONFIGURE_EXISTING | Binary pass/fail filter rules |
| 7 | Soft Constraints | CONFIGURE_EXISTING | Weighted scoring factors |
| 8 | Boost/Penalty Rules | CREATE_NEW_ENGINE | Post-scoring modifiers with caps |
| 9 | Rematching Engine | CREATE_NEW_ENGINE | Event-driven rematching with cycle limits |
| 10 | Progressive Search Expansion | CREATE_NEW_ENGINE | Automatic criteria broadening |
| 11 | Continuous Market Surveillance | CREATE_NEW_ENGINE | Event-driven match triggers on new listings |
| 12 | Market Tension Index | CREATE_NEW_ENGINE | Supply/demand ratio computation |
| 13 | Dossier Health Score | CREATE_NEW_ENGINE | Quality/completeness score for projects |
| 14 | Property Health Score | CREATE_NEW_ENGINE | Quality/freshness score for properties |
| 15 | Failed Matching Diagnostics | CREATE_NEW_ENGINE | Structured failure analysis |
| 16 | Verification-Only Fields | CONFIGURE_EXISTING | Fields that inform but do not score |
| 17 | Transaction Blockers | CONFIGURE_EXISTING | Conditions that block transaction progression |

---

## 2. Match Entity

**Extension ID:** EXT-MAT-001
**Decision:** CREATE_NEW_ENTITY

### 2.1 Core Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to Project (demandeur dossier) |
| `property_id` | UUID | Reference to Property |
| `agent_id` | UUID? | Reference to assigned agent |
| `overall_score` | Float | Composite score (0-100) |
| `compatibility_level` | Enum | `excellent \| good \| average \| low` |
| `rank` | Int | Ranking position for this project |
| `is_active` | Boolean | Whether match is currently active |
| `is_proposed` | Boolean | Whether match has been proposed to demandeur |
| `demandeur_decision` | Enum? | `pending \| interested \| not_interested` |
| `holder_decision` | Enum? | `pending \| favorable \| refused` |
| `decision_deadline` | DateTime? | Deadline for current decision |
| `rematch_count` | Int | Number of rematches for this pair |
| `rematch_reason` | String? | Reason for rematch trigger |
| `match_pool` | Enum | `primary \| expansion_geo \| expansion_budget \| expansion_type` |
| `created_at` | DateTime | Match creation timestamp |
| `expires_at` | DateTime | Match expiration |
| `proposed_at` | DateTime? | When match was proposed |
| `demandeur_decided_at` | DateTime? | When demandeur decided |
| `holder_decided_at` | DateTime? | When holder decided |
| `score_breakdown` | JSON | Detailed per-dimension scores |

### 2.2 Score Breakdown Structure

```json
{
  "geographic": { "score": 75.0, "weight": 0.25, "level": "L2", "distance_km": 3.2 },
  "budget": { "score": 90.0, "weight": 0.20, "overlap_pct": 85.0 },
  "property": { "score": 65.0, "weight": 0.20, "alignment_pct": 70.0 },
  "behavioral": { "score": 80.0, "weight": 0.15, "signals": ["profile_complete", "responsive"] },
  "document_trust": { "score": 70.0, "weight": 0.10, "trust_level": 4 },
  "transaction_success": { "score": 75.0, "weight": 0.10, "probability": 0.75 },
  "boosts_applied": [{"type": "premium_listing", "value": 10}],
  "penalties_applied": [],
  "total_boost": 10,
  "total_penalty": 0,
  "composite_raw": 75.0,
  "composite_final": 77.5,
  "compatibility_level": "good"
}
```

### 2.3 Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Project | N:1 | Demandeur dossier being matched |
| Property | N:1 | Property being matched |
| User (agent) | N:1 | Assigned agent |
| Contact | 0:1 | Established contact if consent obtained |
| Visit | 0:N | Scheduled visits from this match |

---

## 3. Scoring Dimensions

**Extension ID:** EXT-MAT-002
**Decision:** CREATE_NEW_ENGINE

### 3.1 Five Score Families

| # | Family | Sub-dimensions | Weight | Description |
|---|--------|---------------|--------|-------------|
| 1 | **Geographic** | Location proximity, zone preference, mobility mode | 0.25 | Distance-based scoring with 5 levels |
| 2 | **Budget** | Price alignment, negotiability, budget tolerance | 0.20 | Budget range compatibility |
| 3 | **Property** | Type match, surface, bedrooms, features, amenities | 0.20 | Property characteristics alignment |
| 4 | **Behavioral** | Response time, profile completeness, activity recency | 0.15 | User behavior signals |
| 5 | **Document/Trust** | Documentation completeness, trust level, verification | 0.10 | Secondary trust factors |
| 6 | **Transaction Success** | Predicted success probability, historical conversion | 0.10 | Historical success prediction |

### 3.2 Scoring Algorithm

```
For each dimension d:
  raw_score_d = compute_dimension_score(d)
  weighted_score_d = raw_score_d × weight_d

composite_raw = SUM(weighted_score_d for d in dimensions)
composite_final = CLAMP(composite_raw + total_boost - total_penalty, 0, 100)

compatibility_level = classify(composite_final)
  where 85-100 → excellent
        70-84  → good
        60-69  → average
        < 60   → low
```

### 3.3 Budget Scoring

| Overlap % | Score | Description |
|-----------|-------|-------------|
| 100% (full overlap) | 100 | Price fully within budget |
| >= 80% | 90 | High overlap |
| >= 60% | 75 | Moderate overlap |
| >= 40% | 50 | Partial overlap |
| >= 20% | 25 | Low overlap |
| < 20% | 0 | Minimal/no overlap (hard constraint) |
| Negotiable flag on property | +10 bonus | Price marked negotiable |
| Budget tolerance applied | +5 per level | Up to +20 for progressive expansion |

### 3.4 Property Scoring

| Factor | Score Contribution | Description |
|--------|-------------------|-------------|
| Type match | 0-40 | Exact type match = 40, family match = 20, different = 0 |
| Surface alignment | 0-20 | Within ±20% = 20, ±50% = 10, beyond = 0 |
| Bedrooms match | 0-20 | Exact = 20, ±1 = 10, beyond = 0 |
| Feature match rate | 0-20 | % of requested features present |
| Quality score bonus | +0 to +5 | Property quality grade contribution |

### 3.5 Behavioral Scoring

| Signal | Score | Condition |
|--------|-------|-----------|
| Profile complete | 20 | All required fields filled |
| Phone verified | 15 | phone_verified = true |
| Email verified | 10 | email_verified = true |
| Identity verified | 15 | identity_verified = true |
| Activity within 7d | 15 | last_activity within 7 days |
| Activity within 30d | 10 | last_activity within 30 days |
| Activity > 30d | 5 | last_activity > 30 days ago |
| Response rate > 80% | 10 | Historical response rate |
| No-show count = 0 | +10 | No missed visits |
| No-show count > 3 | -30 | Frequent no-shows |

### 3.6 Document/Trust Scoring

| Factor | Score | Condition |
|--------|-------|-----------|
| Trust level 5-6 | 40 | Verified professional or reference |
| Trust level 4 | 30 | Pro docs validated |
| Trust level 3 | 20 | Identity verified |
| Trust level 2 | 10 | Phone verified |
| Trust level 1 | 0 | New account |
| Required docs uploaded | 30 | All required documents present |
| Partial docs | 15 | Some documents present |
| No documents | 0 | No documents uploaded |
| Agency verified | 20 | holder belongs to verified agency |
| Badge count bonus | +5 per badge | Up to +15 |

### 3.7 Transaction Success Scoring

| Factor | Score | Condition |
|--------|-------|-----------|
| Historical success rate | 0-40 | % of past matches → transaction |
| Demandeur intent strength | 0-20 | buy=20, rent=15, invest=15, sell=10 |
| Holder reliability | 0-20 | Based on past holder behavior |
| Property market demand | 0-10 | High/medium/low demand segment |
| Agent involvement | 0-10 | Agent-pro subscription = 10 |

---

## 4. Geographic Scoring

**Extension ID:** EXT-MAT-003
**Decision:** CREATE_NEW_ENGINE

### 4.1 Five Geographic Levels

| Level | Distance | Score (base) | Description |
|-------|----------|-------------|-------------|
| L1 | Same neighborhood | 100 | Exact location match |
| L2 | Same city, diff neighborhood | 75 | City-level match |
| L3 | Same region (département), diff city | 50 | Regional match |
| L4 | Same country, diff region | 25 | Country-level match |
| L5 | Different country | 0 | No geographic match |

### 4.2 Mobility Modes

| Mode | Radius | Decay Function | Typical Profile |
|------|--------|---------------|-----------------|
| Low mobility | 5 km | Steep linear: score = 100 × max(0, 1 - d/5) | Elderly, no vehicle, family constraint |
| Medium mobility | 20 km | Gradual: score = 100 × max(0, 1 - d/20) | Average professional, has transport |
| High mobility | 50+ km | Shallow: score = 100 × max(0, 1 - d/50) | Investor, diaspora, corporate |

### 4.3 Zone Preference Scoring

| Zone Match | Bonus | Description |
|------------|-------|-------------|
| Exact neighborhood | +10 | Both in same neighborhood list |
| Nearby zone (≤3 km) | +5 | Adjacent zone |
| Same city zone | 0 | Within same city |
| Outside city | -10 | Different city entirely |

### 4.4 Geographic Expansion

When insufficient matches exist at current level, geographic expansion follows this order:

| Expansion Step | From | To | Score Impact |
|----------------|------|----|-------------|
| 1 | L1 (neighborhood) | L2 (city) | Drops L1→L2 weighting |
| 2 | L2 (city) | L3 (region) | Applies regional penalty |
| 3 | L3 (region) | L4 (country) | Country-level with -15 penalty |
| 4 | L4 (country) | L5 (any) | Only if no matches exist |

---

## 5. Compatibility Levels

**Extension ID:** EXT-MAT-004
**Decision:** CONFIGURE_EXISTING

### 5.1 Compatibility Classification

| Level | Score Range | Label | Action |
|-------|-------------|-------|--------|
| Excellent | 85-100 | Excellent | Auto-propose to demandeur; push notification; highlight as "Best Match" |
| Good | 70-84 | Good | Propose with qualification note; standard notification |
| Average | 60-69 | Average | Propose only if no Excellent/Good matches exist; with caveats |
| Low | < 60 | Low | Not proposed; held for progressive expansion or dossier improvement |

### 5.2 Presentation Rules

| Level | Display | Action |
|-------|---------|--------|
| Excellent | Green badge, "Excellent Match" label, score breakdown shown | Immediate proposal |
| Good | Blue badge, "Good Match" label | Standard proposal flow |
| Average | Yellow badge, "Average Match" with improvement suggestions | Conditional proposal |
| Low | Gray badge, "Below Threshold" | Hidden from default view; shown in "expand search" |

---

## 6. Matching Roles

**Extension ID:** EXT-MAT-011
**Decision:** CONFIGURE_EXISTING

### 6.1 Nine Matching Roles

| # | Role | Type | Description | Score Impact |
|---|------|------|-------------|-------------|
| 1 | `demandeur` | Primary | Property seeker (buyer/tenant) | All dimensions apply |
| 2 | `holder` | Primary | Property owner/seller | All dimensions apply (weighted differently) |
| 3 | `agent` | Facilitator | Managing agent for owner | Behavioral + Trust dimensions only |
| 4 | `notaire` | Professional | Notary for transaction | Document/Trust dimension only |
| 5 | `investor` | Specialized | Investment buyer | Budget + Transaction Success weighted higher |
| 6 | `diaspora` | Specialized | Diaspora seeker | Geographic weighted lower; Trust + Document higher |
| 7 | `professional` | Service | Professional service provider | Behavioral + Document/Trust only |
| 8 | `guarantor` | Secondary | Guarantor for rental | Trust dimension only |
| 9 | `co_demandeur` | Secondary | Co-buyer/co-tenant | Same as demandeur, averaged |

### 6.2 Role-Specific Weight Configurations

| Role | Geographic | Budget | Property | Behavioral | Doc/Trust | Transaction |
|------|-----------|--------|----------|------------|-----------|-------------|
| demandeur | 0.25 | 0.20 | 0.20 | 0.15 | 0.10 | 0.10 |
| holder | 0.15 | 0.25 | 0.25 | 0.10 | 0.15 | 0.10 |
| agent | 0.00 | 0.00 | 0.00 | 0.40 | 0.40 | 0.20 |
| notaire | 0.00 | 0.00 | 0.00 | 0.00 | 0.80 | 0.20 |
| investor | 0.15 | 0.30 | 0.15 | 0.10 | 0.10 | 0.20 |
| diaspora | 0.10 | 0.25 | 0.20 | 0.10 | 0.25 | 0.10 |
| professional | 0.25 | 0.00 | 0.00 | 0.35 | 0.40 | 0.00 |
| guarantor | 0.00 | 0.25 | 0.00 | 0.00 | 0.75 | 0.00 |
| co_demandeur | 0.25 | 0.20 | 0.20 | 0.15 | 0.10 | 0.10 |

---

## 7. Constraint System

**Extension IDs:** EXT-MAT-006
**Decision:** CONFIGURE_EXISTING

### 7.1 Hard Constraints (Binary Pass/Fail)

Hard constraints produce immediate exclusion — score = 0, match not created.

| # | Constraint | Evaluation | Behavior |
|---|------------|-----------|----------|
| 1 | Budget disjoint | demandeur.max < property.min OR demandeur.min > property.max | Exclude (unless negotiable flag) |
| 2 | Property type mismatch | demandeur.type ≠ property.type AND no family match | Exclude |
| 3 | Location country mismatch | demandeur.country ≠ property.country | Exclude |
| 4 | Transaction type mismatch | demandeur.project_type incompatible with property.availability | Exclude (buy vs rent) |
| 5 | Availability blocked | property.availability = sold/rented/archived | Exclude |
| 6 | Holder blacklisted | holder.trust_level < 2 OR holder.blacklisted | Exclude |

### 7.2 Soft Constraints (Weighted Scoring)

Soft constraints reduce score proportionally rather than excluding.

| # | Constraint | Score Impact | Evaluation |
|---|------------|-------------|------------|
| 1 | Budget partial overlap | 0-50 reduction | Based on overlap percentage |
| 2 | Property subtype mismatch | -20 | Different subtype within same family |
| 3 | Location neighborhood mismatch | -25 | Same city, different neighborhood |
| 4 | Missing required features | -10 per missing feature | Up to -50 |
| 5 | Bedroom mismatch | -15 per bedroom difference | Max -45 |
| 6 | Surface mismatch > 30% | -20 | Surface > 30% off from target |

### 7.3 Ranking Preferences (Tie-Breakers)

Applied when scores are equal (within ±1 point).

| # | Preference | Priority | Description |
|---|------------|----------|-------------|
| 1 | Premium listing | 1st | is_premium = true ranks higher |
| 2 | Boosted listing | 2nd | boost_level > none ranks higher |
| 3 | Recent activity | 3rd | More recent last_activity_at |
| 4 | Trust level | 4th | Higher demandeur trust_level |
| 5 | Newer listing | 5th | Earlier published_at |
| 6 | Agent rating | 6th | Higher agent_rating |

### 7.4 Exclusions

| # | Exclusion Rule | Reason | Behavior |
|---|----------------|--------|----------|
| 1 | Previously refused by same demandeur | Historical refusal | Permanent exclusion for this pair |
| 2 | Previously refused by same holder | Holder refused contact | Permanent exclusion for this pair |
| 3 | Already in active negotiation | Ongoing process | Exclude until negotiation concludes |
| 4 | Rematch max exceeded for pair | rematch_count >= 3 | Block further rematching |
| 5 | Property in maintenance/suspension | status = maintenance | Exclude until reactivated |
| 6 | Demandeur blacklisted | Fraud detected | Exclude all matches |

---

## 8. Boost & Penalty Rules

**Extension ID:** EXT-MAT-001 (integrated in Match entity)
**Decision:** CREATE_NEW_ENGINE

### 8.1 Boost Rules

| # | Boost | Value | Condition | Cap |
|---|-------|-------|-----------|-----|
| 1 | Premium listing | +10 | property.is_premium = true | +50 |
| 2 | Agent pro subscription | +15 | agent has active agent_pro subscription | +50 |
| 3 | Complete dossier | +10 | All qualification steps completed | +50 |
| 4 | Verified identity | +5 | demandeur.identity_verified = true | +50 |
| 5 | Urgent demandeur | +20 | demandeur urgency = high/urgent | +50 |
| 6 | Boost 7d active | +8 | property.boost_level = boost_7d | +50 |
| 7 | Boost 30d active | +12 | property.boost_level = boost_30d | +50 |
| 8 | Property verified | +5 | property.verification_status = verified | +50 |
| 9 | Agency verified | +10 | holder.agency_verified = true | +50 |
| 10 | Cash purchase | +15 | demandeur.cash_purchase = true | +50 |

### 8.2 Penalty Rules

| # | Penalty | Value | Condition | Floor |
|---|---------|-------|-----------|-------|
| 1 | Incomplete dossier | -10 | Qualification < 80% complete | 0 |
| 2 | Unverified phone | -15 | demandeur.phone_verified = false | 0 |
| 3 | Spam-like behavior | -50 | Fraud layers triggered | 0 |
| 4 | No-show history | -20 | no_show_count > 2 | 0 |
| 5 | Incomplete property listing | -10 | Property quality_score < 40 | 0 |
| 6 | Low agent rating | -10 | agent_rating < 3.0 | 0 |
| 7 | No documents uploaded | -15 | Document count = 0 | 0 |
| 8 | Inactive > 90d | -10 | last_activity > 90d ago | 0 |

### 8.3 Cap Enforcement

```
total_boost = SUM(boost_values)
total_boost = MIN(total_boost, 50)  // Cap at +50

total_penalty = SUM(penalty_values)
composite_raw = MAX(0, composite_raw - total_penalty)  // Floor at 0

composite_final = composite_raw + total_boost
composite_final = MIN(MAX(composite_final, 0), 100)  // Clamp [0, 100]
```

---

## 9. Rematching Engine

**Extension ID:** EXT-MAT-005
**Decision:** CREATE_NEW_ENGINE

### 9.1 Rematching Triggers

| # | Trigger | Source | Action | Max Cycles |
|---|---------|--------|--------|------------|
| 1 | Demandeur refuses match | demandeur_decision = not_interested | Exclude property, recalculate, propose next | 3 |
| 2 | Holder refuses contact | holder_decision = refused | Exclude property, recalculate, propose next | 3 |
| 3 | Visit fails (no-show) | absence_type set | Offer rematch with same property (reschedule) or new | 3 |
| 4 | Visit fails (holder no-show) | absence_type = holder_no_show | Offer rematch with new property | 3 |
| 5 | Negotiation fails | failure_reason set | Offer rematch with new property | 3 |
| 6 | Match expires (30d) | expires_at passed | Recalculate score, re-propose if still valid | 3 |
| 7 | New property listed | property.published event | Evaluate against all active dossiers | N/A |
| 8 | Dossier updated | project.qualification changed | Recalculate all active matches for project | N/A |
| 9 | Holder silence (72h) | holder_decision = pending > 72h | Send reminders, then auto-exclude | 2 |

### 9.2 Rematching Flow

```
1. Trigger event detected
2. Check rematch_count < max_rematches (default 3)
3. If yes:
   a. Exclude current property from pool (if refusal/failure)
   b. Set rematch_reason on original match
   c. Increment rematch_count on project
   d. Recalculate scores against remaining pool
   e. Propose next best match (top remaining)
4. If no (max reached):
   a. Mark project matching_status = failed
   b. Generate failed matching diagnostic
   c. Notify agent/admin for manual intervention
```

### 9.3 Rematch Exclusion Rules

| Condition | Exclude? | Duration |
|-----------|----------|----------|
| Demandeur refused this property | Yes | Permanent for this dossier |
| Holder refused this demandeur | Yes | Permanent for this dossier |
| Visit no-show (demandeur) | No | Offer reschedule, then exclude after 3rd |
| Visit no-show (holder) | No | Offer new property match |
| Negotiation failed on price | Yes | Exclude property, suggest alternatives |
| Match expired naturally | No | Recalculate and re-propose |
| Holder silence > 72h | Yes | Exclude property for this cycle |

---

## 10. Progressive Search Expansion

**Extension ID:** EXT-MAT-012
**Decision:** CREATE_NEW_ENGINE

### 10.1 Expansion Levels

| Level | Condition | Expansion Action | Score Impact |
|-------|-----------|-----------------|-------------|
| 0 | Initial search | As per original criteria | Full scoring |
| 1 | Top 10 matches, all < 85 | Expand budget tolerance ±10% | Budget score -5 |
| 2 | Still < 5 matches >= 70 | Expand to nearby neighborhoods | Geographic -10 |
| 3 | Still < 3 matches >= 60 | Expand budget tolerance ±20% | Budget score -10 |
| 4 | Still < 3 matches >= 60 | Expand to city-level (L2) | Geographic -25 |
| 5 | No matches >= 60 | Expand to region-level (L3) | Geographic -50 |
| 6 | No matches >= 60 | Expand property type (family match) | Property -20 |
| 7 | No matches at all | Expand country-level (L4) + max budget ±30% | Geographic -75, Budget -15 |

### 10.2 Expansion Prioritization

```
Expansion order:
  1. Geographic (neighborhood → city → region → country)
  2. Budget (±10% → ±20% → ±30%)
  3. Property type (exact → family → any)
  4. Surface (±20% → ±40%)
  5. Bedrooms (±1 → ±2)
```

### 10.3 Match Pool Naming

| Pool | Description | Display |
|------|-------------|---------|
| `primary` | Original criteria match | "Primary Matches" |
| `expansion_geo` | Expanded geographic criteria | "Nearby Properties" |
| `expansion_budget` | Expanded budget tolerance | "Extended Budget Matches" |
| `expansion_type` | Expanded property type | "Similar Properties" |

---

## 11. Continuous Market Surveillance

**Extension ID:** EXT-MAT-013
**Decision:** CREATE_NEW_ENGINE

### 11.1 Surveillance Events

| # | Event | Trigger | Action |
|---|-------|---------|--------|
| 1 | New property published | property.status → published | Score against all active dossiers |
| 2 | Property availability changes | availability → available/pending | Re-score for matched dossiers |
| 3 | Property price changes | price_displayed updated | Re-score for matched dossiers |
| 4 | Property boost activated | boost_level changes | Re-score (boost value update) |
| 5 | Property verification completes | verification_status → verified | Re-score (trust update) |
| 6 | Dossier criteria updated | project.qualification changed | Re-score all matches for project |
| 7 | User trust level changes | trust_level updated | Re-score affected matches |
| 8 | New property in same neighborhood | property.published, same zone | Score against zone-interested dossiers |

### 11.2 Surveillance Execution

```
On each event:
  1. Identify affected dossiers (by criteria match)
  2. For each dossier, compute match score
  3. If score >= 60 AND score >= dossier.current_best - 10:
     a. Create new match record
     b. Add to match pool
     c. Notify demandeur (if score >= 70)
  4. If score >= 85 (excellent):
     a. Immediate push notification to demandeur
     b. Flag for agent review
```

### 11.3 Batch Processing Schedule

| Frequency | Scope | Action |
|-----------|-------|--------|
| Real-time (event-driven) | New publications | Immediate scoring |
| Every 15 min | Price/availability changes | Batch re-score |
| Every 1 hour | Boost/verification changes | Batch re-score |
| Every 24 hours | Full dossier re-evaluation | Re-score all active matches |
| On demand | Manual trigger | Full re-score |

---

## 12. Market Tension Index

**Extension ID:** EXT-MAT-008
**Decision:** CREATE_NEW_ENGINE

### 12.1 Definition

The Market Tension Index (MTI) measures supply/demand equilibrium per market segment.

```
MTI = number_of_active_dossiers / number_of_active_properties

Stratified by:
  - Property type (residential.buy, residential.rent, commercial, land, etc.)
  - City / Zone
  - Price range (low: < 25M, mid: 25-75M, high: 75-150M, premium: > 150M FCFA)
```

### 12.2 Tension Levels

| MTI Range | Label | Market Condition | Matching Strategy |
|-----------|-------|-----------------|-------------------|
| MTI < 0.5 | Oversupply | More properties than seekers | Relaxed matching; promote properties |
| 0.5 <= MTI < 1.0 | Balanced | Equilibrium | Standard matching |
| 1.0 <= MTI < 2.0 | Tension | More seekers than properties | Competitive matching; faster proposals |
| 2.0 <= MTI < 5.0 | High Tension | Significant shortage | Prioritize excellent matches only |
| MTI >= 5.0 | Critical | Extreme shortage | VIP allocation; waitlist system |

### 12.3 MTI Impact on Matching

| Tension Level | Score Threshold Adjust | Max Proposals | Proposal Speed |
|---------------|----------------------|---------------|----------------|
| Oversupply | Lower minimum to 50 | Top 15 | Standard |
| Balanced | Standard (60) | Top 10 | Standard |
| Tension | Raise minimum to 65 | Top 7 | Expedited |
| High Tension | Raise minimum to 70 | Top 5 | Immediate |
| Critical | Raise minimum to 75 | Top 3 | VIP immediate |

---

## 13. Dossier Health Score

**Extension ID:** EXT-MAT-009
**Decision:** CREATE_NEW_ENGINE

### 13.1 Definition

The Dossier Health Score (DHS) measures a demandeur dossier's readiness for successful matching.

```
DHS = completeness_score × 0.50 + data_quality_score × 0.30 + freshness_score × 0.20
```

### 13.2 Scoring Components

| Component | Weight | Factors |
|-----------|--------|---------|
| Completeness | 0.50 | Qualification steps completed (10 max), criteria defined (budget, location, type, features), documents uploaded |
| Data Quality | 0.30 | Budget specificity (range vs exact), location precision (neighborhood vs city), criteria detail level |
| Freshness | 0.20 | Last updated within 7d = 100, within 30d = 70, within 90d = 40, > 90d = 10 |

### 13.3 Health Levels

| Score Range | Label | Meaning | Action |
|-------------|-------|---------|--------|
| 85-100 | Excellent | Ready for matching | Full matching enabled |
| 70-84 | Good | Minor improvements needed | Matching active, improvement suggestions |
| 50-69 | Average | Requires more data | Matching limited, prompt for completion |
| < 50 | Poor | Not match-ready | Matching blocked, dossier incomplete |

---

## 14. Property Health Score

**Extension ID:** EXT-MAT-010
**Decision:** CREATE_NEW_ENGINE

### 14.1 Definition

The Property Health Score (PHS) measures a property listing's quality and match readiness.

```
PHS = completeness_score × 0.40 + quality_score × 0.30 + freshness_score × 0.20 + verification_score × 0.10
```

### 14.2 Scoring Components

| Component | Weight | Factors |
|-----------|--------|---------|
| Completeness | 0.40 | All required fields filled, photos uploaded (min 3), documents attached, price set, location precise |
| Quality | 0.30 | Data quality grade (A+ through D), professional photos, detailed description, amenities listed |
| Freshness | 0.20 | Published within 7d = 100, within 30d = 80, within 90d = 50, > 90d = 10 |
| Verification | 0.10 | verification_status: verified = 100, pending = 50, unverified = 0, rejected = 0 |

### 14.3 Health Levels

| Score Range | Label | Meaning | Action |
|-------------|-------|---------|--------|
| 85-100 | Excellent | Premium listing quality | Boost in matching; "Verified" badge |
| 70-84 | Good | High quality | Standard matching; "Quality Listing" badge |
| 50-69 | Average | Needs improvement | Lower match priority; improvement prompts |
| < 50 | Poor | Incomplete | Reduced visibility; publication warnings |

---

## 15. Failed Matching Diagnostics

**Extension ID:** EXT-MAT-001 (integrated)
**Decision:** CREATE_NEW_ENGINE

### 15.1 Diagnostic Record Structure

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary identifier |
| `project_id` | UUID | Reference to failed project |
| `failure_mode` | Enum | `no_properties \| all_below_threshold \| all_refused \| max_rematches \| dossier_incomplete \| market_insufficient` |
| `rematch_count` | Int | Rematching cycles attempted |
| `total_properties_evaluated` | Int | Total properties scored |
| `properties_above_threshold` | Int | Properties scoring >= 60 |
| `properties_proposed` | Int | Properties actually proposed |
| `refusal_reasons` | JSON[] | Array of refusal records |
| `expansion_level_reached` | Enum | `none \| geo \| budget \| type \| max` |
| `market_tension_at_failure` | Float | MTI at time of failure |
| `diagnostic_summary` | String | Human-readable summary |
| `recommended_actions` | JSON[] | Array of suggested next actions |
| `created_at` | DateTime | Diagnostic timestamp |

### 15.2 Failure Modes & Recommended Actions

| Failure Mode | Description | Recommended Actions |
|-------------|-------------|-------------------|
| `no_properties` | No properties at all match criteria | Widen geographic range, adjust budget, change property type |
| `all_below_threshold` | Properties exist but all score < 60 | Improve dossier completeness, verify identity, expand criteria |
| `all_refused` | Properties proposed but all refused | Review refusal patterns, adjust criteria, consult agent |
| `max_rematches` | Rematching limit reached (3 cycles) | Manual agent intervention, dossier review |
| `dossier_incomplete` | Dossier not ready for matching | Complete qualification steps, upload documents |
| `market_insufficient` | Market tension index insufficient | Notify agent, set up market alert, schedule follow-up |

---

## 16. Verification-Only Fields

**Extension ID:** EXT-MAT-006 (integrated)
**Decision:** CONFIGURE_EXISTING

These fields are collected during qualification and used for informational purposes. They are stored on the match record but do NOT directly influence scoring.

| Field | Context | Purpose |
|-------|---------|---------|
| `holder_occupation` | Holder profile | Informational context |
| `demandeur_occupation` | Demandeur profile | Informational context |
| `property_construction_year` | Property details | Age reference only |
| `property_last_renovation` | Property details | Renovation reference only |
| `property_floor_number` | Property details | Preference check |
| `property_total_floors` | Building details | Reference only |
| `property_orientation` | Property details | Preference check |
| `heating_type` | Property details | Preference check |
| `parking_type` | Property details | Preference check |
| `furnished_status` | Property details | Preference check |
| `pet_policy` | Building rules | Informational only |
| `hoa_fees` | Building costs | Informational only |
| `property_taxes` | Property costs | Informational only |

---

## 17. Transaction Blockers

**Extension ID:** EXT-MAT-007 (integrated)
**Decision:** CONFIGURE_EXISTING

### 17.1 Blocker Definition

Transaction blockers are conditions that prevent a match from progressing to transaction even when scoring is otherwise acceptable.

| # | Blocker | Checked At | Description |
|---|---------|------------|-------------|
| 1 | Trust level insufficient | Transaction initiation | demandeur.trust_level < 3 OR holder.trust_level < 3 |
| 2 | Property verification incomplete | Transaction initiation | property.verification_status != verified |
| 3 | Required documents missing | Transaction preparation | Per transaction type document requirements |
| 4 | Holder consent not obtained | Transaction initiation | holder_decision != favorable |
| 5 | Demandeur consent not obtained | Transaction initiation | demandeur_decision != interested |
| 6 | Agent not assigned | Transaction initiation | No active agent on match |
| 7 | Payment not completed (if paid service) | Transaction preparation | service_order.status != paid |
| 8 | Identity not verified for both parties | Transaction signing | Both parties must have identity_verified |
| 9 | Price mismatch > agreed tolerance | Transaction agreement | price_agreed != price_negotiable AND > 5% deviation |
| 10 | Legal hold on property | Transaction preparation | property flagged with legal issue |

### 17.2 Blocker Resolution

| Blocker | Resolution | Responsible |
|---------|-----------|-------------|
| Trust level insufficient | Complete verification steps | User |
| Property verification incomplete | Purchase verification service | Holder/Agent |
| Required documents missing | Upload documents | Both parties |
| Holder consent not obtained | Contact holder | Agent/System |
| Demandeur consent not obtained | Follow up with demandeur | Agent/System |
| Agent not assigned | Assign agent | System/Admin |
| Payment not completed | Process payment | User |
| Identity not verified | Complete identity verification | User |
| Price mismatch > agreed tolerance | Renegotiate | Both parties |
| Legal hold on property | Resolve legal issue | Holder/Notaire |

---

## 18. Complete Extension Mapping Table

| Extension ID | Concept | Decision | Entity | Priority |
|-------------|---------|----------|--------|----------|
| EXT-MAT-001 | Full matching engine | CREATE_NEW_ENGINE | Match + ScoringEngine | P1 |
| EXT-MAT-002 | 5 scoring dimensions | CREATE_NEW_ENGINE | ScoringEngine | P1 |
| EXT-MAT-003 | Geographic scoring | CREATE_NEW_ENGINE | ScoringEngine.Geographic | P1 |
| EXT-MAT-004 | 4 compatibility levels | CONFIGURE_EXISTING | Match | P1 |
| EXT-MAT-005 | Rematching rules | CREATE_NEW_ENGINE | RematchingEngine | P1 |
| EXT-MAT-006 | Exclusion criteria | CONFIGURE_EXISTING | MatchingEngine | P1 |
| EXT-MAT-007 | Transaction success score | CREATE_NEW_ENGINE | ScoringEngine.Transaction | P2 |
| EXT-MAT-008 | Market tension index | CREATE_NEW_ENGINE | MarketAnalysis | P2 |
| EXT-MAT-009 | Dossier health score | CREATE_NEW_ENGINE | DossierHealth | P2 |
| EXT-MAT-010 | Property health score | CREATE_NEW_ENGINE | PropertyHealth | P2 |
| EXT-MAT-011 | 9 matching roles | CONFIGURE_EXISTING | MatchingEngine | P1 |
| EXT-MAT-012 | Progressive search expansion | CREATE_NEW_ENGINE | SearchExpansion | P2 |
| EXT-MAT-013 | Continuous market surveillance | CREATE_NEW_ENGINE | MarketSurveillance | P2 |
