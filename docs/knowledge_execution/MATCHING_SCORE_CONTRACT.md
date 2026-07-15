# Matching Score Contract

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**Prerequisite:** Heritage Gold — `docs/lawim_heritage_gold/MATCHING_MODEL.md`, `docs/lawim_heritage_gold/RULE_INDEX.md` (MATCH-001 to MATCH-034)

---

## 1. Purpose

Defines the formal input/output contract for the Matching Engine scoring pipeline. Every matching execution produces a standardized `MatchScore` result that is consumed by the Ranker, Explanation Builder, Decision Engine, and Audit system.

---

## 2. Input Contract

### 2.1 Resource (Property Data)

```json
{
  "resource": {
    "id": "prop_<uuid>",
    "property_type": "appartement",
    "transaction_type": "rent",
    "city": "douala",
    "neighborhood": "bonanjo",
    "price": 250000,
    "currency": "XAF",
    "status": "available",
    "title_status": "titre_foncier",
    "bedrooms": 3,
    "surface": 120,
    "gps_coordinates": { "lat": 4.0511, "lng": 9.7679 },
    "description": "Bel appartement meublé à Bonanjo",
    "images": ["url1.jpg", "url2.jpg"],
    "holder_id": "usr_<uuid>",
    "created_at": "2026-06-01T00:00:00Z",
    "data_quality_score": 85,
    "document_score": 100,
    "availability_score": 100,
    "holder_reliability_score": 0.85,
    "last_match_date": null,
    "building_id": "bld_<uuid>",
    "features": {
      "parking": true,
      "balcony": true,
      "garden": false,
      "pool": false,
      "furnished": true,
      "gps_available": true
    }
  }
}
```

### 2.2 Request (Lead/Dossier Data with Qualification)

```json
{
  "request": {
    "id": "dossier_<uuid>",
    "lead_id": "lead_<uuid>",
    "intent": "rent",
    "transaction_type": "rent",
    "city": "douala",
    "neighborhood": "bonanjo",
    "alternative_neighborhoods": ["bonapriso", "akwa"],
    "budget_min": 150000,
    "budget_max": 300000,
    "property_type": "appartement",
    "critical_criteria": ["parking", "furnished"],
    "comfort_criteria": ["balcony", "garden"],
    "preferential_criteria": ["pool"],
    "lead_score": 75,
    "lead_class": "WARM",
    "lead_type": "tenant",
    "lead_priority": "P2",
    "diaspora_flag": false,
    "urgency_flag": false,
    "visit_intent_flag": false,
    "budget_detected": true,
    "city_detected": true,
    "neighborhood_detected": true,
    "requester_id": "usr_<uuid>",
    "refused_property_ids": ["prop_abc", "prop_def"],
    "mobility_mode": "FLEXIBLE"
  }
}
```

### 2.3 Context (Cross-cutting State)

```json
{
  "context": {
    "matching_run_id": "match_run_<uuid>",
    "timestamp": "2026-07-15T14:30:00Z",
    "is_rematch": false,
    "rematch_reason": null,
    "progressive_search_level": 1,
    "source": "user_request",
    "available_inventory_size": 45,
    "system_rules_version": "v1.0"
  }
}
```

---

## 3. Output Contract

### 3.1 Top-Level Structure

```json
{
  "match_result": {
    "matching_run_id": "match_run_<uuid>",
    "request_id": "dossier_<uuid>",
    "resource_id": "prop_<uuid>",
    "global_score": 82,
    "star_rating": 4,
    "rank": 1,
    "total_candidates": 12,
    "above_threshold_count": 5,
    "threshold": 60,
    "excluded": false,
    "exclusion_reason": null,
    "conflicts": [],
    "warnings": [],
    "dimension_scores": {},
    "family_scores": {},
    "boosts": [],
    "penalties": [],
    "explanation": {},
    "recommended_action": "send_listings",
    "progressive_search_available": true,
    "audit_trail": []
  }
}
```

### 3.2 Dimension Scores

Each dimension evaluated produces a raw value, weight, score, and contribution.

```json
{
  "dimension_scores": {
    "geographical": {
      "raw": {
        "city_match": "exact",
        "neighborhood_match": "exact",
        "gps_distance_km": 0.5,
        "proximity_level": 1,
        "mobility_mode": "FLEXIBLE",
        "affinity_applicable": false
      },
      "weight": 0.26,
      "score": 92,
      "contribution": 23.92,
      "breakdown": [
        { "criterion": "exact_city_match", "points": 40 },
        { "criterion": "exact_neighborhood_match", "points": 35 },
        { "criterion": "gps_proximity", "points": 17 }
      ]
    },
    "budget": {
      "raw": {
        "requested_min": 150000,
        "requested_max": 300000,
        "property_price": 250000,
        "difference_pct": 0,
        "within_tolerance": true,
        "tolerance_pct": 20,
        "transaction_type": "rent",
        "flexible_applied": false
      },
      "weight": 0.20,
      "score": 100,
      "contribution": 20.00,
      "breakdown": [
        { "criterion": "budget_exact_match", "points": 50 },
        { "criterion": "within_tolerance", "points": 50 }
      ]
    },
    "property": {
      "raw": {
        "property_type_match": "exact",
        "title_status": "titre_foncier",
        "critical_criteria_met": ["parking", "furnished"],
        "critical_criteria_missed": [],
        "comfort_criteria_met": ["balcony"],
        "comfort_criteria_missed": ["garden"],
        "preferential_criteria_met": [],
        "data_quality_score": 85
      },
      "weight": 0.15,
      "score": 78,
      "contribution": 11.70,
      "breakdown": [
        { "criterion": "property_type_match", "points": 25 },
        { "criterion": "title_foncier", "points": 20 },
        { "criterion": "critical_criteria_score", "points": 33 }
      ]
    },
    "behavioral": {
      "raw": {
        "lead_score": 75,
        "lead_class": "WARM",
        "urgency_flag": false,
        "visit_intent_flag": false,
        "diaspora_flag": false,
        "message_engagement": "moderate",
        "budget_detected": true,
        "city_detected": true,
        "neighborhood_detected": true
      },
      "weight": 0.10,
      "score": 65,
      "contribution": 6.50,
      "breakdown": [
        { "criterion": "lead_class_weight", "points": 30 },
        { "criterion": "completeness_score", "points": 35 }
      ]
    },
    "other": {
      "raw": {
        "availability_score": 100,
        "document_score": 100,
        "holder_reliability_score": 0.85,
        "freshness_days": 45,
        "service_boost_applicable": false
      },
      "weight": 0.29,
      "score": 85,
      "contribution": 24.65,
      "breakdown": [
        { "criterion": "availability", "points": 30 },
        { "criterion": "document_score", "points": 25 },
        { "criterion": "holder_reliability", "points": 20 },
        { "criterion": "freshness", "points": 10 }
      ]
    }
  }
}
```

### 3.3 Family Scores

```json
{
  "family_scores": {
    "geographical_score": {
      "raw_score": 92,
      "weight": 0.26,
      "weighted_contribution": 23.92
    },
    "budget_score": {
      "raw_score": 100,
      "weight": 0.20,
      "weighted_contribution": 20.00
    },
    "property_score": {
      "raw_score": 78,
      "weight": 0.15,
      "weighted_contribution": 11.70
    },
    "behavioral_score": {
      "raw_score": 65,
      "weight": 0.10,
      "weighted_contribution": 6.50
    },
    "other_score": {
      "raw_score": 85,
      "weight": 0.29,
      "weighted_contribution": 24.65
    }
  }
}
```

### 3.4 Global Score Calculation

```json
{
  "global_score": {
    "base_score": 86.77,
    "boost_total": 25,
    "penalty_total": 0,
    "final_score": 82,
    "calculation": "round(clamp(86.77 + 25 - 0, 0, 100))",
    "non_compensation_applied": false,
    "non_compensation_reason": null,
    "below_threshold": false
  }
}
```

**Formula:**
```
base_score = (geo_contribution + budget_contribution + prop_contribution + behav_contribution + other_contribution)
boost_total = sum of all applicable boosts
penalty_total = sum of all applicable penalties
final_score = clamp(base_score + boost_total - penalty_total, 0, 100)
```

### 3.5 Boosts

```json
{
  "boosts": [
    {
      "rule_id": "MATCH-004",
      "name": "exact_neighborhood_match",
      "value": 25,
      "trigger": "Property in exact requested neighborhood (bonanjo)",
      "applied": true
    },
    {
      "rule_id": "MATCH-005",
      "name": "exact_city_match",
      "value": 20,
      "trigger": "Property in exact requested city (douala)",
      "applied": false,
      "reason": "Already applied neighborhood boost (non-stacking per policy)"
    },
    {
      "rule_id": "MATCH-006",
      "name": "budget_within_range",
      "value": 15,
      "trigger": "Price (250000) within tolerance for rent (±20%, range: 120000-360000)",
      "applied": true
    },
    {
      "rule_id": "MATCH-007",
      "name": "title_foncier",
      "value": 10,
      "trigger": "Property has valid land title (titre_foncier)",
      "applied": true
    },
    {
      "rule_id": "MATCH-008",
      "name": "diaspora_investor",
      "value": 20,
      "trigger": "Lead identified as diaspora investor",
      "applied": false,
      "reason": "diaspora_flag is false"
    }
  ]
}
```

### 3.6 Penalties

```json
{
  "penalties": [
    {
      "rule_id": "QUAL-003",
      "name": "missing_budget",
      "value": -10,
      "trigger": "Budget not detected on lead",
      "applied": false
    },
    {
      "rule_id": "QUAL-003",
      "name": "unclear_location",
      "value": -10,
      "trigger": "Location not clearly detected",
      "applied": false
    },
    {
      "rule_id": "QUAL-003",
      "name": "spam_like_message",
      "value": -50,
      "trigger": "Message matches spam patterns",
      "applied": false
    },
    {
      "rule_id": "PROP-006",
      "name": "incomplete_property_data",
      "value": -5,
      "trigger": "Missing critical property field",
      "applied": false,
      "detail": "All critical fields present (data_quality_score: 85)"
    }
  ]
}
```

### 3.7 Exclusions

```json
{
  "exclusions": {
    "excluded": false,
    "reason": null,
    "excluded_by_rules": [],
    "blacklist_check": {
      "property_blacklisted": false,
      "blacklist_rule": "MATCH-017",
      "property_refused_before": false,
      "exception_applies": null,
      "exception_rule": "MATCH-018"
    },
    "hard_constraint_check": {
      "status_available": true,
      "operation_compatible": true,
      "type_compatible": true,
      "city_compatible": true,
      "budget_compatible": true
    }
  }
}
```

### 3.8 Conflicts

```json
{
  "conflicts": [
    {
      "type": "weight_discrepancy",
      "detail": "V1 JSON weights (city=30%) differ from DE weights (Geographical=26%)",
      "source": "GM-WEIGHT-001",
      "resolution": "Using DE weights (26%) for this matching run",
      "severity": "info"
    }
  ]
}
```

### 3.9 Warnings

```json
{
  "warnings": [
    {
      "code": "DATA_QUALITY",
      "message": "Property data quality score (85) is below A+ threshold (≥90)",
      "field": "data_quality_score",
      "value": 85,
      "threshold": 90,
      "severity": "low"
    },
    {
      "code": "MISSING_GPS",
      "message": "GPS coordinates not available for this property; proximity scored on neighborhood only",
      "field": "gps_coordinates",
      "value": null,
      "severity": "medium"
    },
    {
      "code": "LEAD_COMPLETENESS",
      "message": "No comfort criteria specified; property scored on critical criteria only",
      "field": "request.comfort_criteria",
      "value": [],
      "severity": "low"
    }
  ]
}
```

### 3.10 Rank

```json
{
  "rank": {
    "position": 1,
    "total_results": 5,
    "above_threshold": 5,
    "below_threshold_count": 7,
    "diversity_applied": true,
    "diversity_original_position": 1,
    "diversity_note": "Original rank 1; no diversity demotion needed"
  }
}
```

### 3.11 Explanation (MATCH-033)

```json
{
  "explanation": {
    "summary": "Excellent match (82/100) for your rental search in Douala Bonanjo.",
    "top_3_criteria": [
      {
        "rank": 1,
        "criterion": "Location",
        "detail": "Located in your exact requested neighborhood: Bonanjo",
        "contribution": 23.92,
        "percentage": 29.2
      },
      {
        "rank": 2,
        "criterion": "Budget",
        "detail": "Price 250,000 FCFA is within your rental budget range (150,000 - 300,000 FCFA)",
        "contribution": 20.00,
        "percentage": 24.4
      },
      {
        "rank": 3,
        "criterion": "Availability & Documentation",
        "detail": "Property is available with valid land title (titre foncier)",
        "contribution": 17.65,
        "percentage": 21.5
      }
    ],
    "star_rating_text": "⭐⭐⭐⭐ (4/5) — Good match",
    "compatibility_level": "Functional",
    "compatibility_met": ["Critical", "Functional"],
    "compatibility_missed": ["Comfort", "Preferential"]
  }
}
```

### 3.12 Recommended Action

```json
{
  "recommended_action": {
    "action": "send_listings",
    "reason": "WARM lead with qualified matching results (5 properties above threshold)",
    "confidence": 0.85,
    "rule_id": "QUAL-009",
    "nba_priority": 3,
    "alternatives": [
      {
        "action": "suggest_alternatives",
        "trigger": "If user rejects all 5 proposed properties"
      },
      {
        "action": "schedule_visit",
        "trigger": "If user expresses visit intent for any property"
      }
    ],
    "sla": {
      "delay": "< 24h",
      "channel": "WhatsApp"
    }
  }
}
```

### 3.13 Audit Trail

```json
{
  "audit_trail": [
    {
      "step": 1,
      "component": "ConstraintEnforcer",
      "action": "Hard constraint check",
      "rules_applied": ["MATCH-034", "MATCH-022", "MATCH-023"],
      "result": "passed",
      "detail": "All hard constraints satisfied"
    },
    {
      "step": 2,
      "component": "ExclusionEngine",
      "action": "Blacklist check",
      "rules_applied": ["MATCH-017"],
      "result": "passed",
      "detail": "Property not in requester blacklist"
    },
    {
      "step": 3,
      "component": "DimensionEvaluator",
      "action": "Geographical dimension evaluation",
      "rules_applied": ["MATCH-001", "GEO-011"],
      "result": "score=92",
      "detail": "Exact neighborhood match in FLEXIBLE mode"
    },
    {
      "step": 4,
      "component": "ScoreCalculator",
      "action": "Global score computation",
      "rules_applied": ["MATCH-001", "MATCH-002", "MATCH-020"],
      "result": "base_score=86.77",
      "detail": "DE weights used (26/20/15/10/29)"
    },
    {
      "step": 5,
      "component": "BoostApplier",
      "action": "Boost application",
      "rules_applied": ["MATCH-004", "MATCH-006", "MATCH-007"],
      "result": "boost_total=50",
      "detail": "Neighborhood (+25), Budget (+15), Title (+10)"
    },
    {
      "step": 6,
      "component": "PenaltyApplier",
      "action": "Penalty evaluation",
      "rules_applied": [],
      "result": "penalty_total=0",
      "detail": "No penalties applied"
    },
    {
      "step": 7,
      "component": "ScoreCalculator",
      "action": "Score clamping and threshold check",
      "rules_applied": ["MATCH-009", "MATCH-011"],
      "result": "final_score=82, above_threshold=true",
      "detail": "82 >= 60 threshold, passed"
    },
    {
      "step": 8,
      "component": "Ranker",
      "action": "Ranking and diversity check",
      "rules_applied": ["MATCH-010", "MATCH-032"],
      "result": "ranked #1 of 5",
      "detail": "Diversity enforced, 1 building-group demoted"
    },
    {
      "step": 9,
      "component": "ExplanationBuilder",
      "action": "Explanation generation",
      "rules_applied": ["MATCH-033"],
      "result": "3 criteria explained",
      "detail": "Location (29.2%), Budget (24.4%), Availability & Documentation (21.5%)"
    }
  ]
}
```

---

## 4. Score Thresholds and Limits

| Parameter | Value | Rule | Applied In |
|-----------|-------|------|------------|
| Minimum match score | 60/100 | MATCH-009 | Ranker |
| Score < 60 behavior | Never proposed | MATCH-011 | Ranker |
| Max results (V1) | 10 | MATCH-010 | Ranker |
| Max results (first match) | 5 | MATCH-010 (DE) | Ranker |
| Score range | 0–100 | MATCHING_MODEL §4 | Score Calculator |
| Star rating 5★ | ≥ 80 | MATCH-019 | Explanation Builder |
| Star rating 4★ | ≥ 60 | MATCH-019 | Explanation Builder |
| Star rating 3★ | ≥ 40 | MATCH-019 | Explanation Builder |
| Star rating 2★ | ≥ 20 | MATCH-019 | Explanation Builder |
| Star rating 1★ | < 20 | MATCH-019 | Explanation Builder |

---

## 5. Error States

| Error Condition | Output Signal | Fallback |
|----------------|---------------|----------|
| Resource data incomplete | `warnings` with missing fields | Score dimension at 0 |
| Request missing critical field | `exclusions` with reason | Return empty results |
| Score calculation exception | `global_score.error` | Score = 0, audit log |
| Non-compensation triggered | `non_compensation_applied: true` | global_score = 0 |
| All candidates excluded | `exclusions` with full reasons | Return empty result set |

---

## References

- Heritage Gold: `docs/lawim_heritage_gold/MATCHING_MODEL.md`
- Heritage Gold: `docs/lawim_heritage_gold/RULE_INDEX.md` (MATCH-001 to MATCH-034)
- Matching Architecture: `docs/knowledge_execution/MATCHING_EXECUTION_ARCHITECTURE.md`
- Decision Contract: `docs/knowledge_execution/DECISION_CONTRACT.md`
