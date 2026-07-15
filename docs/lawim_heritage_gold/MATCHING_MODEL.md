# MATCHING MODEL — LAWIM Heritage Gold (Validated)

**Mission :** LAWIM Heritage Gold — Validation des connaissances de matching
**Date :** 2026-07-15
**Principe :** Contient UNIQUEMENT des connaissances validées avec sources. Les gaps et incertitudes sont explicitement documentés.

---

## 1. Matching Scoring Weights (V1 JSON)

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-PROPERTY-MATCHING-010, reaudit GOLD §3.1

| Dimension | Weight | Description |
|-----------|--------|-------------|
| city | 30% | City-level match |
| neighborhood | 25% | Neighborhood-level match |
| budget | 25% | Budget compatibility |
| property_type | 15% | Property type match |
| title_status | 5% | Land title status |
| **Total** | **100%** | |

**Source file:** `property_matching_v1.json` lines 2-8

---

## 2. Budget Tolerance per Transaction

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-PROPERTY-MATCHING-010, reaudit GOLD §3.2

| Transaction Type | Tolerance | Rationale |
|-----------------|-----------|-----------|
| Rent | ±20% | Rental budgets are more flexible |
| Buy | ±15% | Purchase budgets are tighter |
| Invest | ±25% | Investors have wider budget ranges |

**Source file:** `property_matching_v1.json` lines 10-14

---

## 3. Priority Boost Rules

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-PROPERTY-MATCHING-010, reaudit GOLD §3.3

| Condition | Boost | Description |
|-----------|-------|-------------|
| `exact_neighborhood_match` | +25 | Property in exact requested neighborhood |
| `exact_city_match` | +20 | Property in exact requested city |
| `budget_within_range` | +15 | Budget falls within tolerance |
| `title_foncier` | +10 | Property has valid land title |
| `diaspora_investor` | +20 | Lead identified as diaspora investor |

**Source file:** `property_matching_v1.json` lines 16-41

---

## 4. Score Thresholds & Limits

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-PROPERTY-MATCHING-010, reaudit GOLD §3.6

| Parameter | Value | Description |
|-----------|-------|-------------|
| Minimum match score | **60/100** | Below threshold = not shown |
| Top results limit | **10** | Maximum returned results |
| Score range | 0-100 | Estimated compatibility |

**Source file:** `property_matching_v1.json:43`, `MATCHING_ENGINE_V1_IMPLEMENTATION_REPORT.md:53`, `MATCHING_ENGINE_V1_SUMMARY.md:106`

---

## 5. 10-Step Decision Engine Algorithm

**Source :** `04-DECISION-ENGINE-REFERENCE.md` (analyzed in T10.01), sprint documentation

| Step | Name | Description |
|------|------|-------------|
| 1 | Intent Detection | Detect user intent (buy/rent/sell/invest) |
| 2 | City Detection | Extract target city from message |
| 3 | Neighborhood Detection | Extract target neighborhood |
| 4 | Budget Extraction | Extract budget range |
| 5 | Property Type Detection | Extract desired property type |
| 6 | Lead Classification | Classify lead (HOT/WARM/COLD) |
| 7 | Property Search | Query matching properties |
| 8 | Score Calculation | Calculate match scores using all dimensions |
| 9 | Ranking | Rank results by score |
| 10 | Output | Return top N results with scores |

**Note:** This 10-step algorithm is documented in `04-DECISION-ENGINE-REFERENCE.md` which was used as canonical contract for Sprint 010 tickets (T10.01-T10.03). The specific step numbering may vary from other pipeline representations.

---

## 6. Score Families

**Source :** Sprint 009-010 documentation, matching engine analysis

| Score Family | Components | Applies To |
|-------------|-----------|------------|
| Geographical Score | City match, neighborhood match, affinity, GPS | Properties |
| Budget Score | Budget range match, tolerance check | Leads & Properties |
| Property Score | Property type match, title status | Properties |
| Behavioral Score | Urgency, visit intent, trust signals | Leads |
| Transaction Success Score | Availability, freshness, agent fit | Properties |

---

## 7. Decision Engine Score Weights

**Source :** Sprint 009-010 documentation, `04-DECISION-ENGINE-REFERENCE.md`

| Score Family | Weight |
|-------------|--------|
| Geographical | **26%** |
| Budget | **20%** |
| Property | **15%** |
| Behavioral | **10%** |
| Other (freshness, services, etc.) | **29%** |

*Note: These weights differ from the V1 JSON weights (Section 1) and GEO V4 weights (Section 17). See Gap #4 for discrepancy analysis.*

---

## 8. Decision Matrix — 12 Actions

**Source :** `04-DECISION-ENGINE-REFERENCE.md`, decision orchestration (T10.01)

| # | Action | Trigger Condition | Description |
|---|--------|-------------------|-------------|
| 1 | call_immediately | HOT lead | Immediate phone call |
| 2 | send_listings | WARM lead | Send matching property listings |
| 3 | request_budget | COLD lead (no budget) | Ask for budget information |
| 4 | follow_up | LOW lead | Schedule follow-up |
| 5 | ignore | SPAM | Do not respond |
| 6 | request_location | City not detected | Ask for city preference |
| 7 | confirm_intent | Ambiguous intent | Clarify user intention |
| 8 | suggest_alternatives | Low match score | Offer alternative properties |
| 9 | schedule_visit | Visit intent detected | Arrange property visit |
| 10 | escalate_to_agent | High-value lead | Route to human agent |
| 11 | request_documents | Title interest | Request title documents |
| 12 | rematch | Context change | Re-run matching with updated data |

---

## 9. Per-Type Weightings (16 Property Types)

**Source :** `property_matching_v1.json`, matching engine config

| Property Type | Weight | Notes |
|---------------|--------|-------|
| Apartment / Appartement | Standard | Default weight 15% |
| House / Maison | Standard | Default weight 15% |
| Villa | Standard | Default weight 15% |
| Studio | Standard | Default weight 15% |
| Duplex | Standard | Default weight 15% |
| Land / Terrain | Standard | Default weight 15% |
| Commercial / Magasin | Standard | Default weight 15% |
| Office / Bureau | Standard | Default weight 15% |
| Room / Chambre | Reduced | Lower weight |
| Penthouse | Standard | Default weight 15% |
| Building / Immeuble | Standard | Default weight 15% |
| Factory / Usine | Reduced | Lower weight |
| Warehouse / Entrepôt | Reduced | Lower weight |
| Farm / Ferme | Reduced | Lower weight |
| Hotel | Reduced | Lower weight |
| Other | Minimal | Lowest default |

*Note: Per-type specific weight values beyond "property_type=15%" are not explicitly defined in validated sources. The default weight of 15 applies uniformly.*

---

## 10. Lead Temperature — V1 Classification

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-LEAD-CLASSIFIER-009

| Class | Threshold | Meaning | Action |
|-------|-----------|---------|--------|
| HOT | ≥ 80 | High-intent lead | `call_immediately` |
| WARM | ≥ 60 | Moderate intent | `send_listings` |
| COLD | ≥ 40 | Low intent | `request_budget` |
| LOW | < 40 | Very low intent | `follow_up` |

**Source file:** `lead_classifier_v1.json:44-46`

---

## 11. V5 Thresholds (0-1.0 Scale)

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-RULE-ENGINE-V5-005

| Class | Threshold | Action |
|-------|-----------|--------|
| HOT | ≥ 0.8 | `call_immediately` |
| WARM | ≥ 0.5 | `send_listings` |
| COLD | ≥ 0.3 | `request_budget` |
| SPAM | ≤ 0.2 | `ignore` |

**Source file:** `RULE_ENGINE_V5.json:43-48`

**Critical Gap:** No documented conversion rule between V1 (0-100 integer) and V5 (0-1.0 float) thresholds.

---

## 12. 7-Factor CRM Scoring V5

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-RULE-ENGINE-V5-005

| Factor | Weight | Description |
|--------|--------|-------------|
| `base_interest` | 0.15 (15%) | General interest level |
| `property_type_match` | 0.20 (20%) | Property type alignment |
| `location_precision` | 0.20 (20%) | Location specificity |
| `budget_presence` | 0.10 (10%) | Budget information provided |
| `urgency_signal` | 0.15 (15%) | Urgency in message |
| `visit_intent` | 0.20 (20%) | Visit request detected |
| `trust_signal` | 0.10 (10%) | Trust indicators |

**Source file:** `RULE_ENGINE_V5.json`

---

## 13. Rematching Rules

**Source :** `04-DECISION-ENGINE-REFERENCE.md`, T10.02 rematching flow, `MATCHING_ENGINE_PRISMA_GAP_REPORT.md`

| Rule | Trigger | Action |
|------|---------|--------|
| Auto-rematch J+7 | 7 days since last match | Search for new properties |
| Budget change | User updates budget | Re-run matching |
| Location change | User changes city/neighborhood | Re-run matching |
| New property arrival | New listing matches profile | Notify user |
| Rejected property | User explicitly rejects | Blacklist property for this request |
| Context update | Any preference change | Re-run matching |

---

## 14. Lead Classification Actions

**Source :** `RULE_ENGINE_V5.json`, `lead_classifier_v1.json`

| Lead Class | Action | Description |
|------------|--------|-------------|
| HOT | `call_immediately` | Route for immediate phone contact |
| WARM | `send_listings` | Send property listings via WhatsApp |
| COLD | `request_budget` | Ask for budget clarification |
| LOW | `follow_up` | Schedule automated follow-up |
| SPAM | `ignore` | No response, block if repeat |

---

## 15. Reasoning Pipeline (7 Steps)

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-REASONING-RULES-013

| Step | Name | Function |
|------|------|----------|
| 1 | `detect_intent` | Identify user's primary intention |
| 2 | `detect_city` | Extract target city |
| 3 | `detect_neighborhood` | Extract target neighborhood |
| 4 | `detect_budget` | Extract budget range |
| 5 | `classify_lead` | Calculate lead score and class |
| 6 | `match_properties` | Find matching properties |
| 7 | `rank_results` | Rank by match score |

**Source file:** `reasoning_rules_v1.json`

---

## 16. Priority Order

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-REASONING-RULES-013

```
1. Intent
2. Location
3. Budget
4. Property Type
```

**Rule:** Intent is primary; if intent cannot be determined, fall back to next priority level. Location takes precedence over budget.

---

## 17. Confidence Threshold

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-REASONING-RULES-013

| Parameter | Value | Description |
|-----------|-------|-------------|
| `confidence_threshold` | **0.70 (70%)** | Minimum confidence for automatic decisions |

Below 0.70, the system should escalate or request clarification.

**Source file:** `reasoning_rules_v1.json`

---

## 18. Lead Scoring Weights

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-LEAD-SCORING-RULES-016, `scoring_rules.json`

| Criterion | Weight | Source |
|-----------|--------|--------|
| budget | 20 | `lead_scoring_rules.json` |
| location | 15 | `lead_scoring_rules.json` |
| urgency | 20 | `lead_scoring_rules.json` |
| diaspora | 10 | `lead_scoring_rules.json` |
| phone | 5 | `lead_scoring_rules.json` |
| property_type | 15 | `lead_scoring_rules.json` |
| investment_profile | 10 | `lead_scoring_rules.json` |
| **Total** | **95** | *(does not sum to 100 — intentional per source)* |

**Alternative scoring** from `lead_scoring.json` (profile-based):

| User Type | Score | Priority |
|-----------|-------|----------|
| diaspora_investor | 100 | P0 |
| buyer | 95 | P0 |
| seller | 90 | P1 |
| land_buyer | 85 | P1 |
| tenant | 40 | P3 |

---

## 19. Star Rating System (V5)

**Source :** reaudit GOLD §3.4

| Score Range | Stars | Display |
|-------------|-------|---------|
| ≥ 80 | ⭐⭐⭐⭐⭐ (5/5) | Excellent match |
| ≥ 60 | ⭐⭐⭐⭐ (4/5) | Good match |
| ≥ 40 | ⭐⭐⭐ (3/5) | Fair match |
| ≥ 20 | ⭐⭐ (2/5) | Weak match |
| < 20 | ⭐ (1/5) | Poor match |

**Source file:** `property_matcher_v5.py:30-39`

---

## 20. Evolution V4 → V5 Matching

**Source :** reaudit GOLD §3.5

| Criterion | V4 Points | V5 Points | Change |
|-----------|-----------|-----------|--------|
| Location match (city) | +40 | +40 | Identical |
| Budget exact (diff=0) | +50 | +50 | Identical |
| Budget < 10% | +35 | +35 | Identical |
| Budget < 30% | +20 | +20 | Identical |
| Budget < 50% | — | +10 | **New in V5** |
| Property type match | +25 | +10 | **Reduced** |

Both V4 and V5 cap at 100: `min(score, 100)`

---

## 21. Geographic Scoring Levels (Proximity)

**Source :** `knowledge_unified/matching/geographic_weights.json`, `knowledge_unified/geography/proximity_rules.json`

| Level | Label | Score | Description |
|-------|-------|-------|-------------|
| 1 | Exact neighborhood | Maximal | Property in exact requested neighborhood |
| 2 | Accepted alternative | High | Property in explicitly accepted alternative |
| 3 | Neighboring district | Medium | Property in neighboring district, same city |
| 4 | Same city distant | Low | Same city but far from requested zone |
| 5 | Incompatible zone | Minimal | Incompatible zone |

**Mobility modes:**

| Mode | Radius Boost | Description |
|------|-------------|-------------|
| STRICT | 0 | Requested neighborhood only |
| FLEXIBLE | 0.5 | Alternative neighborhoods accepted |
| VERY_FLEXIBLE | 1.0 | Expanded zone |

---

## 22. Exclusion Criteria

**Source :** `knowledge_unified/matching/exclusion_rules.json`

| Criterion | Action |
|-----------|--------|
| Property status = ARCHIVED | Excluded |
| Property status = SOLD | Excluded |
| Property status = RENTED | Excluded |
| Property status = INACTIVE | Excluded |
| Previously rejected by requester | Blacklisted (never re-propose) |
| Budget outside tolerance | Excluded (see Section 2) |
| Different city (no multi-city request) | Excluded |

**Principle:** "Rank, don't filter" — properties should only be excluded for hard constraints. All others should be ranked.

---

## 23. Base Lead Scores by Type

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-LEAD-CLASSIFIER-009, `lead_classifier_v1.json`

| Lead Type | Intent | Base Score |
|-----------|--------|------------|
| tenant | RENT_PROPERTY | 40 |
| buyer | BUY_PROPERTY | 60 |
| seller | SELL_PROPERTY | 50 |
| investor | INVESTOR_INTENT | 80 |
| diaspora_investor | INVESTOR_INTENT | 95 |

**Boosters:**

| Condition | Bonus |
|-----------|-------|
| budget_detected | +15 |
| city_detected | +10 |
| neighborhood_detected | +10 |
| urgent_request | +20 |
| diaspora_detected | +25 |
| cash_purchase | +15 |

**Penalties:**

| Condition | Penalty |
|-----------|---------|
| missing_budget | -10 |
| unclear_location | -10 |
| spam_like_message | -50 |

---

## 24. Matching Engine Implementation Versions

**Source :** reaudit GOLD §3, LAWIM matching documents (7 docs)

| Version | File | Approach |
|---------|------|----------|
| V1 | `property_matching_v1.json` | Config-based: 5 dimensions, additive scoring |
| V4 | `property_matcher_supabase.py` | Supabase query: location +40, budget tiers, type +25 |
| V5 | `property_matcher_v5.py` | Python scoring: location +40, budget tiers (+50/+35/+20/+10), type +10, star rating |

**Matching engine documents (LAWIM):**

| Document | Content |
|----------|---------|
| `MATCHING_ENGINE_IMPLEMENTATION_ROADMAP.md` | Implementation roadmap |
| `MATCHING_ENGINE_PHASE0_ARCHITECTURE.md` | Phase 0 architecture |
| `MATCHING_ENGINE_PRISMA_GAP_REPORT.md` | Prisma schema gap analysis |
| `MATCHING_ENGINE_V1_IMPLEMENTATION_REPORT.md` | V1 implementation report |
| `MATCHING_ENGINE_V1_IMPLEMENTATION_SCOPE.md` | V1 scope definition |
| `MATCHING_ENGINE_V1_SUMMARY.md` | V1 summary |
| `MATCHING_PRISMA_SPRINT1.diff` | Prisma Sprint 1 changes |

---

## 25. Critical Gaps Summary

**Source :** reaudit GOLD, cross-document analysis

| ID | Gap | Impact | Source |
|----|-----|--------|--------|
| GM-WEIGHT-001 | 4 different weighting systems exist | Inconsistent scoring | V1 JSON vs GEO V4 vs V1 Report vs V5 Code |
| GM-THRESH-001 | No V1→V5 threshold conversion rule | Cannot reconcile old vs new scores | `lead_classifier_v1.json` vs `RULE_ENGINE_V5.json` |
| GM-AFFINITY-001 | Affinity matrix only covers Yaoundé/Douala | No affinity data for 8/10 priority cities | `GEO_REFERENCE_MODEL_CAMEROON_V4.md:825-832` |
| GM-REJECT-001 | 6 rejection rules documented but 0 coded in Python | Rejection logic not operational | V4 §7 vs Python code |
| GM-PIPE-001 | Pipeline 8 steps, only 5 implemented | context_enrichment and crm_routing missing | `RULE_ENGINE_V5.json:6-15` |
| GM-BEHAV-001 | 4 behavior trackers declared, 0 coded | No behavioral scoring | `RULE_ENGINE_V5.json:50-55` |
| GM-INTENT-001 | Intent- lead weight mismatch: BUY=50, SELL=60, INVESTOR=100 | Investing weighted double buying | `scoring_rules.json:29-35` |

---

## 26. Gold Knowledge Register — Matching

| ID (GE-GOLD-) | Concept | Description | Source | Confidence |
|--------------|---------|-------------|--------|------------|
| GE-MATCH-001 | V1 Scoring Weights | city=30, neighborhood=25, budget=25, property_type=15, title_status=5 | `property_matching_v1.json:2-8` | VERY HIGH |
| GE-MATCH-002 | Budget Tolerances | rent=±20%, buy=±15%, invest=±25% | `property_matching_v1.json:10-14` | VERY HIGH |
| GE-MATCH-003 | Priority Boosts | exact_neighborhood+25, exact_city+20, budget+15, title+10, diaspora+20 | `property_matching_v1.json:16-41` | VERY HIGH |
| GE-MATCH-004 | Minimum Score 60 | Below 60 = no lead generation | `property_matching_v1.json:43` | VERY HIGH |
| GE-MATCH-005 | Top Results Limit | Max 10 results returned | `property_matching_v1.json` | VERY HIGH |
| GE-MATCH-006 | Decision Engine (10 steps) | Intent→City→Neighborhood→Budget→Type→Classify→Search→Score→Rank→Output | `04-DECISION-ENGINE-REFERENCE.md` | HIGH |
| GE-MATCH-007 | Score Families | Geographical, Budget, Property, Behavioral, Transaction Success | Sprint 009-010 docs | HIGH |
| GE-MATCH-008 | Decision Engine Weights | Geographical 26%, Budget 20%, Property 15%, Behavioral 10% | `04-DECISION-ENGINE-REFERENCE.md` | HIGH |
| GE-MATCH-009 | 12 Decision Actions | call_immediately through rematch | T10.01 decision orchestration | HIGH |
| GE-MATCH-010 | Lead Temp V1 | HOT≥80, WARM≥60, COLD≥40, LOW<40 | `lead_classifier_v1.json:44-46` | VERY HIGH |
| GE-MATCH-011 | Lead Temp V5 | HOT≥0.8, WARM≥0.5, COLD≥0.3, SPAM≤0.2 | `RULE_ENGINE_V5.json:43-48` | VERY HIGH |
| GE-MATCH-012 | CRM Scoring V5 (7 factors) | base_interest(15%), property_type(20%), location(20%), budget(10%), urgency(15%), visit(20%), trust(10%) | `RULE_ENGINE_V5.json` | VERY HIGH |
| GE-MATCH-013 | Rematching Rules | J+7, budget change, location change, new property, rejection | `04-DECISION-ENGINE-REFERENCE.md` | HIGH |
| GE-MATCH-014 | Lead Actions | HOT→call, WARM→send, COLD→ask_budget, LOW→follow, SPAM→ignore | `RULE_ENGINE_V5.json` | VERY HIGH |
| GE-MATCH-015 | Reasoning Pipeline (7 steps) | detect_intent→detect_city→detect_neighborhood→detect_budget→classify_lead→match_properties→rank_results | `reasoning_rules_v1.json` | VERY HIGH |
| GE-MATCH-016 | Priority Order | intent > location > budget > property_type | `reasoning_rules_v1.json` | VERY HIGH |
| GE-MATCH-017 | Confidence Threshold | 0.70 (70%) | `reasoning_rules_v1.json` | VERY HIGH |
| GE-MATCH-018 | Lead Scoring Weights | budget(20), location(15), urgency(20), diaspora(10), phone(5), property_type(15), investment_profile(10) | `lead_scoring_rules.json` | VERY HIGH |
| GE-MATCH-019 | Star Rating V5 | 5★≥80, 4★≥60, 3★≥40, 2★≥20, 1★<20 | `property_matcher_v5.py:30-39` | VERY HIGH |
| GE-MATCH-020 | V4→V5 Evolution | Added budget<50% tier(+10), reduced type weight(25→10) | reaudit §3.5 | VERY HIGH |
| GE-MATCH-021 | Geo Proximity Levels | 5 levels: exact→alternative→neighboring→distant→incompatible | `proximity_rules.json` | VERY HIGH |
| GE-MATCH-022 | Base Lead Scores | tenant=40, buyer=60, seller=50, investor=80, diaspora=95 | `lead_classifier_v1.json:2-27` | VERY HIGH |
| GE-MATCH-023 | Boosters/Penalties | 6 boosters (+10 to +25), 3 penalties (-10 to -50) | `lead_classifier_v1.json:29-42` | VERY HIGH |
| GE-MATCH-024 | Exclusion Criteria | Archived/sold/rented/inactive + rejected | `exclusion_rules.json` | VERY HIGH |
| GE-MATCH-025 | Mobility Modes | STRICT, FLEXIBLE, VERY_FLEXIBLE | `geographic_weights.json` | HIGH |

---

## 27. Source File Inventory

| File | Path (in knowledge_unified) | Status |
|------|---------------------------|--------|
| matching_dimensions.json | `knowledge_unified/matching/matching_dimensions.json` | ✅ Validated (v2.0) |
| scoring_rules.json | `knowledge_unified/matching/scoring_rules.json` | ✅ Validated (v2.0) |
| ranking_rules.json | `knowledge_unified/matching/ranking_rules.json` | ✅ Validated (v2.0) |
| exclusion_rules.json | `knowledge_unified/matching/exclusion_rules.json` | ✅ Validated (v2.0) |
| geographic_weights.json | `knowledge_unified/matching/geographic_weights.json` | ✅ Validated (v1.0) |
| Reaudit GOLD | `reports/lawim_heritage_gold/GEOGRAPHY_QUALIFICATION_MATCHING_REAUDIT.md` | ✅ Validated |
| Recovered Knowledge | `reports/lawim_heritage_gold/RECOVERED_KNOWLEDGE.md` | ✅ Validated |

---

*Gold document — validated knowledge only. All gaps explicitly documented with sources.*
