# RULE TEST CONTRACT — Heritage Gold Rule Testing Specification

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL

---

## 1. Contract Structure

Every Heritage Gold rule test MUST conform to this canonical contract:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `test_id` | `string` | Yes | Unique identifier: `T-{RULE_ID}-{TYPE}-{SEQ}` (e.g., `T-QUAL-001-NOM-001`) |
| `rule_id` | `string` | Yes | Rule identifier from RULE_INDEX.md (e.g., `QUAL-001`) |
| `rule_description` | `string` | Yes | Brief description of the rule under test |
| `test_type` | `enum` | Yes | One of: `nominal`, `negative`, `idempotence`, `audit` |
| `scenario` | `string` | Yes | Human-readable scenario description |
| `input` | `object` | Yes | Full context/input for the rule engine (RuleContext) |
| `expected_output` | `object` | Yes | Expected action or result from rule execution |
| `expected_events` | `array` | Yes | List of expected event(s) with payload schemas |
| `preconditions` | `object` | No | Required state before rule execution |
| `postconditions` | `object` | No | Expected state after rule execution |

### Test Type Definitions

| Test Type | Description | Assertions |
|-----------|-------------|------------|
| `nominal` | Rule triggers correctly when all conditions are met | Action matches expected; correct events emitted; correct state transitions |
| `negative` | Rule does NOT trigger when one or more conditions are not met | No action; no events; state unchanged |
| `idempotence` | Rule produces identical result when applied 1, 2, or N times | `apply^n(input) == apply^1(input)` for n ∈ {2, 3} |
| `audit` | Rule execution produces correct audit events | Audit event payload matches schema; all placeholders resolved |

---

## 2. Edge Case Tests Per Rule Type

| Rule Type | Edge Cases |
|-----------|------------|
| **Threshold** (scores, cutoffs) | Boundary at ±1 from threshold; negative values; zero; max int |
| **String match** (city, type, intent) | Case variants; whitespace; special chars; empty string; null; partial match |
| **Numeric range** (budget, price) | Exact boundary; just below minimum; just above maximum; zero; extreme values |
| **State machine** (lifecycle, transitions) | Every valid transition; every invalid transition; concurrent transitions |
| **Boolean flag** (diaspora, urgency) | True; false; null; undefined; conflicting flags |
| **Enumeration** (property type, role) | Every valid value; invalid value; null; empty array |
| **Temporal** (follow-up, auto-archive) | Just before deadline; just after deadline; timezone edge; leap year |
| **Format** (phone, price display) | Valid format; invalid format; incomplete; international; local |
| **Composition** (multiple conditions) | Only one condition met; all conditions met; none; contradictory conditions |

---

## 3. Test Contract Examples Per Domain

### 3.1 Constitution Domain

```json
{
  "test_id": "T-CONST-001-NOM-001",
  "rule_id": "CONST-001",
  "rule_description": "Zero commission on property transactions",
  "test_type": "nominal",
  "scenario": "Transaction event triggers zero-commission rule",
  "input": {
    "event_type": "transaction.created",
    "transaction": { "type": "sale", "amount": 50000000, "commission_included": false },
    "context": { "source": "whatsapp" }
  },
  "expected_output": {
    "action": { "type": "skip_commission", "params": { "reason": "zero_commission_policy" } }
  },
  "expected_events": [
    { "event_type": "transaction.created", "payload": { "commission": 0, "policy_applied": "CONST-001" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-CONST-001-NEG-001",
  "rule_id": "CONST-001",
  "rule_description": "Zero commission — negative: service transaction (not property)",
  "test_type": "negative",
  "scenario": "Service payment triggers commission logic (not blocked by CONST-001)",
  "input": {
    "event_type": "payment.pending",
    "transaction": { "type": "service", "amount": 50000, "service": "accompaniment" }
  },
  "expected_output": { "action": null },
  "expected_events": [],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-CONST-001-AUD-001",
  "rule_id": "CONST-001",
  "rule_description": "Zero commission — audit: correct event produced",
  "test_type": "audit",
  "scenario": "Audit trail records zero-commission application",
  "input": {
    "event_type": "transaction.created",
    "transaction": { "type": "sale", "amount": 50000000 },
    "context": { "source": "whatsapp" }
  },
  "expected_output": {
    "action": { "type": "skip_commission", "params": { "reason": "zero_commission_policy" } }
  },
  "expected_events": [
    {
      "event_type": "audit.rule_fired",
      "payload": {
        "rule_id": "CONST-001",
        "decision": "skip_commission",
        "transaction_id": "{{transaction.id}}",
        "timestamp": "{{$iso_timestamp}}"
      }
    }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

### 3.2 Property Domain

```json
{
  "test_id": "T-PROP-003-NOM-001",
  "rule_id": "PROP-003",
  "rule_description": "Property lifecycle: 5 states (available, pending, rented, sold, archived)",
  "test_type": "nominal",
  "scenario": "New property is created in available state",
  "input": {
    "property": { "id": "prop-001", "status": "available", "created_at": "2026-07-15T00:00:00Z" }
  },
  "expected_output": {
    "action": { "type": "transition_state", "params": { "from": null, "to": "available" } }
  },
  "expected_events": [
    { "event_type": "property.state_changed", "payload": { "property_id": "prop-001", "from": null, "to": "available" } }
  ],
  "preconditions": {},
  "postconditions": { "property.status": "available" }
}
```

```json
{
  "test_id": "T-PROP-003-NEG-001",
  "rule_id": "PROP-003",
  "rule_description": "Property lifecycle — negative: invalid state rejected",
  "test_type": "negative",
  "scenario": "Property created with invalid state 'reserved'",
  "input": {
    "property": { "id": "prop-002", "status": "reserved" }
  },
  "expected_output": { "action": { "type": "error", "params": { "message": "invalid_state" } } },
  "expected_events": [
    { "event_type": "property.state_rejected", "payload": { "property_id": "prop-002", "invalid_state": "reserved" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-PROP-005-NOM-001",
  "rule_id": "PROP-005",
  "rule_description": "Auto-archive after 90 days inactivity",
  "test_type": "nominal",
  "scenario": "Property inactive for 91 days triggers auto-archive",
  "input": {
    "property": { "id": "prop-003", "status": "available", "last_activity": "2026-04-14T00:00:00Z" },
    "current_date": "2026-07-15T00:00:00Z"
  },
  "expected_output": {
    "action": { "type": "transition_state", "params": { "from": "available", "to": "archived" } }
  },
  "expected_events": [
    { "event_type": "property.archived", "payload": { "property_id": "prop-003", "reason": "auto_archive_90d" } }
  ],
  "preconditions": { "property.status": "available" },
  "postconditions": { "property.status": "archived" }
}
```

```json
{
  "test_id": "T-PROP-005-NEG-001",
  "rule_id": "PROP-005",
  "rule_description": "Auto-archive — negative: 89 days does NOT trigger archive",
  "test_type": "negative",
  "scenario": "Property inactive for 89 days remains available",
  "input": {
    "property": { "id": "prop-004", "status": "available", "last_activity": "2026-04-17T00:00:00Z" },
    "current_date": "2026-07-15T00:00:00Z"
  },
  "expected_output": { "action": null },
  "expected_events": [],
  "preconditions": {},
  "postconditions": { "property.status": "available" }
}
```

```json
{
  "test_id": "T-PROP-006-NOM-001",
  "rule_id": "PROP-006",
  "rule_description": "Data Quality Score = completeness*0.6 + reliability*0.4",
  "test_type": "nominal",
  "scenario": "Complete property with agent source scores A+",
  "input": {
    "property": {
      "id": "prop-005",
      "title": "Villa à Douala",
      "description": "Belle villa 4 chambres",
      "price": 80000000,
      "city": "Douala",
      "type": "villa",
      "images": ["img1.jpg", "img2.jpg", "img3.jpg"],
      "source": "agent"
    }
  },
  "expected_output": {
    "action": { "type": "assign_quality_grade", "params": { "grade": "A+", "score": 94 } }
  },
  "expected_events": [
    { "event_type": "score.calculated", "payload": { "property_id": "prop-005", "grade": "A+", "score": 94 } }
  ],
  "preconditions": {},
  "postconditions": { "property.quality_grade": "A+" }
}
```

### 3.3 Matching Domain

```json
{
  "test_id": "T-MATCH-001-NOM-001",
  "rule_id": "MATCH-001",
  "rule_description": "V1 scoring dimensions: city=30%, neighborhood=25%, budget=25%, property_type=15%, title_status=5%",
  "test_type": "nominal",
  "scenario": "Property matches all V1 dimensions",
  "input": {
    "match_request": {
      "buyer_city": "Douala",
      "property_city": "Douala",
      "buyer_neighborhood": "Bonanjo",
      "property_neighborhood": "Bonanjo",
      "buyer_budget": 50000000,
      "property_price": 45000000,
      "buyer_type": "apartment",
      "property_type": "apartment",
      "property_title": "titré"
    }
  },
  "expected_output": {
    "action": { "type": "calculate_score", "params": { "score": 100, "breakdown": { "city": 30, "neighborhood": 25, "budget": 25, "type": 15, "title": 5 } } }
  },
  "expected_events": [
    { "event_type": "match.score_calculated", "payload": { "score": 100, "version": "V1" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-MATCH-009-NOM-001",
  "rule_id": "MATCH-009",
  "rule_description": "Minimum match score = 60/100",
  "test_type": "nominal",
  "scenario": "Score of 65 meets minimum threshold, proposal allowed",
  "input": {
    "match_result": { "property_id": "prop-010", "buyer_id": "user-005", "score": 65 }
  },
  "expected_output": {
    "action": { "type": "allow_proposal", "params": { "reason": "score_above_threshold" } }
  },
  "expected_events": [
    { "event_type": "match.proposal_allowed", "payload": { "property_id": "prop-010", "score": 65, "threshold": 60 } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-MATCH-009-NEG-001",
  "rule_id": "MATCH-009",
  "rule_description": "Minimum match score — negative: score 55 blocks proposal",
  "test_type": "negative",
  "scenario": "Score of 55 is below minimum threshold, proposal blocked",
  "input": {
    "match_result": { "property_id": "prop-011", "buyer_id": "user-005", "score": 55 }
  },
  "expected_output": {
    "action": { "type": "block_proposal", "params": { "reason": "score_below_threshold", "score": 55, "threshold": 60 } }
  },
  "expected_events": [
    { "event_type": "match.proposal_blocked", "payload": { "property_id": "prop-011", "score": 55, "threshold": 60 } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-MATCH-013-NOM-001",
  "rule_id": "MATCH-013",
  "rule_description": "Non-compensation: land does not compensate for villa",
  "test_type": "nominal",
  "scenario": "Buyer wants villa, land property is not proposed even if other criteria excel",
  "input": {
    "buyer_preference": { "property_type": "villa" },
    "property": { "id": "prop-012", "type": "land", "score": 85 }
  },
  "expected_output": {
    "action": { "type": "block_proposal", "params": { "reason": "non_compensation", "incompatible_type": "land" } }
  },
  "expected_events": [
    { "event_type": "match.non_compensation_applied", "payload": { "property_id": "prop-012", "buyer_type": "villa", "property_type": "land" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-MATCH-017-NOM-001",
  "rule_id": "MATCH-017",
  "rule_description": "Refused property never reproposed",
  "test_type": "nominal",
  "scenario": "Property previously refused is excluded from new match results",
  "input": {
    "match_request": { "buyer_id": "user-006" },
    "previous_refusals": ["prop-013", "prop-014"],
    "candidate_properties": ["prop-013", "prop-015", "prop-016"]
  },
  "expected_output": {
    "action": { "type": "filter_candidates", "params": { "excluded": ["prop-013", "prop-014"], "remaining": ["prop-015", "prop-016"] } }
  },
  "expected_events": [],
  "preconditions": { "buyer.refusals": ["prop-013", "prop-014"] },
  "postconditions": { "match.candidates": ["prop-015", "prop-016"] }
}
```

```json
{
  "test_id": "T-MATCH-033-NOM-001",
  "rule_id": "MATCH-033",
  "rule_description": "Explainability: top 3 criteria explained",
  "test_type": "nominal",
  "scenario": "Match result includes explanation for top 3 contributing criteria",
  "input": {
    "match_result": {
      "property_id": "prop-017",
      "score": 82,
      "breakdown": { "city": 30, "budget": 25, "type": 15, "neighborhood": 10, "title": 2 }
    }
  },
  "expected_output": {
    "action": {
      "type": "explain_match",
      "params": {
        "top_criteria": [
          { "criterion": "city", "weight": 30, "reason": "Même ville: Douala" },
          { "criterion": "budget", "weight": 25, "reason": "Budget correspondant: 45M FCFA dans la fourchette 40-60M" },
          { "criterion": "type", "weight": 15, "reason": "Type de bien correspondant: appartement" }
        ]
      }
    }
  },
  "expected_events": [
    { "event_type": "match.explanation_generated", "payload": { "property_id": "prop-017", "top_3": ["city", "budget", "type"] } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

### 3.4 Geography Domain

```json
{
  "test_id": "T-GEO-001-NOM-001",
  "rule_id": "GEO-001",
  "rule_description": "Territorial hierarchy: Pays→Région→Département→Arrondissement→Commune→Ville→District→Quartier",
  "test_type": "nominal",
  "scenario": "Location 'Douala-Bonanjo' resolves through full hierarchy",
  "input": {
    "location_raw": "Douala Bonanjo",
    "hierarchy": { "country": "Cameroun", "region": "Littoral", "department": "Wouri", "city": "Douala", "neighborhood": "Bonanjo" }
  },
  "expected_output": {
    "action": { "type": "resolve_location", "params": { "resolved": "Cameroun/Littoral/Wouri/Douala/Bonanjo", "levels": 5 } }
  },
  "expected_events": [
    { "event_type": "location.resolved", "payload": { "input": "Douala Bonanjo", "resolved": "Cameroun/Littoral/Wouri/Douala/Bonanjo" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-GEO-004-NOM-001",
  "rule_id": "GEO-004",
  "rule_description": "Levenshtein normalization with max threshold=3",
  "test_type": "nominal",
  "scenario": "Typo 'Duala' normalizes to 'Douala' (edit distance 1)",
  "input": {
    "input_name": "Duala",
    "reference": "Douala"
  },
  "expected_output": {
    "action": { "type": "normalize_name", "params": { "original": "Duala", "normalized": "Douala", "distance": 1, "threshold": 3 } }
  },
  "expected_events": [
    { "event_type": "name.normalized", "payload": { "original": "Duala", "normalized": "Douala", "distance": 1 } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-GEO-004-NEG-001",
  "rule_id": "GEO-004",
  "rule_description": "Levenshtein — negative: distance 4 exceeds threshold",
  "test_type": "negative",
  "scenario": "Typo 'Marseille' does NOT normalize to 'Douala' (distance > 3)",
  "input": {
    "input_name": "Marseille",
    "reference": "Douala"
  },
  "expected_output": {
    "action": { "type": "no_match", "params": { "reason": "distance_exceeds_threshold", "distance": 5, "threshold": 3 } }
  },
  "expected_events": [],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-GEO-009-NOM-001",
  "rule_id": "GEO-009",
  "rule_description": "Geographic prohibitions: Soa→Obala, Yaoundé→Soa",
  "test_type": "nominal",
  "scenario": "Buyer in Soa searching in Obala is rejected",
  "input": {
    "buyer_city": "Soa",
    "target_city": "Obala"
  },
  "expected_output": {
    "action": { "type": "block_cross_city", "params": { "reason": "geographic_prohibition", "from": "Soa", "to": "Obala" } }
  },
  "expected_events": [
    { "event_type": "geography.cross_city_blocked", "payload": { "from": "Soa", "to": "Obala" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

### 3.5 Qualification Domain

```json
{
  "test_id": "T-QUAL-001-NOM-001",
  "rule_id": "QUAL-001",
  "rule_description": "Base scores: tenant=40, buyer=60, seller=50, investor=80, diaspora_investor=95",
  "test_type": "nominal",
  "scenario": "Buyer intent assigns base score 60",
  "input": {
    "lead": { "message": "Je cherche un appartement à Douala", "intent": "BUY" }
  },
  "expected_output": {
    "action": { "type": "assign_base_score", "params": { "intent": "BUY", "base_score": 60 } }
  },
  "expected_events": [
    { "event_type": "lead.base_score_assigned", "payload": { "intent": "BUY", "base_score": 60 } }
  ],
  "preconditions": {},
  "postconditions": { "lead.base_score": 60 }
}
```

```json
{
  "test_id": "T-QUAL-001-NOM-002",
  "rule_id": "QUAL-001",
  "rule_description": "Base scores: diaspora_investor=95",
  "test_type": "nominal",
  "scenario": "Diaspora investor intent assigns base score 95",
  "input": {
    "lead": { "message": "Je vis en France, je veux investir au Cameroun", "intent": "INVESTOR", "diaspora_flag": true }
  },
  "expected_output": {
    "action": { "type": "assign_base_score", "params": { "intent": "INVESTOR", "base_score": 95 } }
  },
  "expected_events": [
    { "event_type": "lead.base_score_assigned", "payload": { "intent": "INVESTOR", "base_score": 95 } }
  ],
  "preconditions": {},
  "postconditions": { "lead.base_score": 95, "lead.diaspora_flag": true }
}
```

```json
{
  "test_id": "T-QUAL-004-NOM-001",
  "rule_id": "QUAL-004",
  "rule_description": "V1 thresholds: HOT≥80, WARM≥60, COLD≥40, LOW<40",
  "test_type": "nominal",
  "scenario": "Score 85 classifies as HOT",
  "input": {
    "lead": { "score": 85 }
  },
  "expected_output": {
    "action": { "type": "classify_lead", "params": { "score": 85, "class": "HOT", "threshold": "≥80" } }
  },
  "expected_events": [
    { "event_type": "lead.classified", "payload": { "score": 85, "class": "HOT" } }
  ],
  "preconditions": {},
  "postconditions": { "lead.classification": "HOT" }
}
```

```json
{
  "test_id": "T-QUAL-004-NEG-001",
  "rule_id": "QUAL-004",
  "rule_description": "V1 thresholds — negative: score 79 classifies as WARM (not HOT)",
  "test_type": "negative",
  "scenario": "Score 79 is below HOT threshold, classified as WARM",
  "input": {
    "lead": { "score": 79 }
  },
  "expected_output": {
    "action": { "type": "classify_lead", "params": { "score": 79, "class": "WARM", "threshold": "≥60" } }
  },
  "expected_events": [
    { "event_type": "lead.classified", "payload": { "score": 79, "class": "WARM" } }
  ],
  "preconditions": {},
  "postconditions": { "lead.classification": "WARM" }
}
```

```json
{
  "test_id": "T-QUAL-009-NOM-001",
  "rule_id": "QUAL-009",
  "rule_description": "Actions: call_immediately, send_listings, request_budget, follow_up, ignore",
  "test_type": "nominal",
  "scenario": "HOT lead triggers call_immediately action",
  "input": {
    "lead": { "classification": "HOT", "score": 85, "phone": "+237691234567" }
  },
  "expected_output": {
    "action": { "type": "call_immediately", "params": { "phone": "+237691234567", "priority": "P0" } }
  },
  "expected_events": [
    { "event_type": "lead.routed", "payload": { "action": "call_immediately", "classification": "HOT" } }
  ],
  "preconditions": {},
  "postconditions": { "lead.status": "routing_complete", "lead.action": "call_immediately" }
}
```

```json
{
  "test_id": "T-QUAL-016-NOM-001",
  "rule_id": "QUAL-016",
  "rule_description": "Diaspora indicators: 13 locations + 4 phone prefixes",
  "test_type": "nominal",
  "scenario": "User with French phone prefix and overseas mention flagged as diaspora",
  "input": {
    "user": { "phone": "+33612345678", "message": "Je vis à Paris" }
  },
  "expected_output": {
    "action": { "type": "set_diaspora_flag", "params": { "diaspora": true, "indicators": ["phone_prefix:+33", "location:Paris"] } }
  },
  "expected_events": [
    { "event_type": "diaspora.detected", "payload": { "diaspora": true, "reason": "phone_prefix+location" } }
  ],
  "preconditions": {},
  "postconditions": { "lead.diaspora_flag": true }
}
```

### 3.6 Conversation Domain

```json
{
  "test_id": "T-CONV-002-NOM-001",
  "rule_id": "CONV-002",
  "rule_description": "Professional tone, vouvoiement",
  "test_type": "nominal",
  "scenario": "User greeting triggers professional response with vouvoiement",
  "input": {
    "message": { "text": "Bonjour", "sender": "user-010" }
  },
  "expected_output": {
    "action": { "type": "generate_response", "params": { "tone": "professional", "vouvoiement": true, "template": "welcome" } }
  },
  "expected_events": [
    { "event_type": "conversation.response_generated", "payload": { "tone": "professional" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-CONV-004-NOM-001",
  "rule_id": "CONV-004",
  "rule_description": "Legal question → redirect to notary",
  "test_type": "nominal",
  "scenario": "User asks legal question, system redirects to notary",
  "input": {
    "message": { "text": "Quels sont les droits de succession pour un bien immobilier?" },
    "intent": "legal_question"
  },
  "expected_output": {
    "action": { "type": "escalate", "params": { "target": "notary", "reason": "legal_question" } }
  },
  "expected_events": [
    { "event_type": "escalation.triggered", "payload": { "reason": "legal_question", "target": "notary" } }
  ],
  "preconditions": {},
  "postconditions": { "conversation.escalated": true }
}
```

```json
{
  "test_id": "T-CONV-009-NOM-001",
  "rule_id": "CONV-009",
  "rule_description": "RGPD: SUPPRIMER MES DONNÉES within 7 days",
  "test_type": "nominal",
  "scenario": "User requests data deletion, anonymization scheduled within 7 days",
  "input": {
    "message": { "text": "SUPPRIMER MES DONNÉES", "sender": "user-011" }
  },
  "expected_output": {
    "action": { "type": "schedule_anonymization", "params": { "delay_days": 7, "user_id": "user-011" } }
  },
  "expected_events": [
    { "event_type": "anonymization.requested", "payload": { "user_id": "user-011", "delay_days": 7 } }
  ],
  "preconditions": {},
  "postconditions": { "user.privacy_status": "anonymization_scheduled" }
}
```

```json
{
  "test_id": "T-CONV-016-NOM-001",
  "rule_id": "CONV-016",
  "rule_description": "Follow-up schedule: J1(24h), J7(168h), J30(720h), J90(2160h)",
  "test_type": "nominal",
  "scenario": "New lead triggers follow-up schedule at all 4 intervals",
  "input": {
    "lead": { "id": "lead-020", "created_at": "2026-07-15T08:00:00Z" }
  },
  "expected_output": {
    "action": { "type": "schedule_followups", "params": {
      "intervals": [
        { "label": "J1", "delay_hours": 24 },
        { "label": "J7", "delay_hours": 168 },
        { "label": "J30", "delay_hours": 720 },
        { "label": "J90", "delay_hours": 2160 }
      ]
    } }
  },
  "expected_events": [
    { "event_type": "followup.scheduled", "payload": { "lead_id": "lead-020", "interval": "J1", "scheduled_at": "2026-07-16T08:00:00Z" } },
    { "event_type": "followup.scheduled", "payload": { "lead_id": "lead-020", "interval": "J7", "scheduled_at": "2026-07-22T08:00:00Z" } },
    { "event_type": "followup.scheduled", "payload": { "lead_id": "lead-020", "interval": "J30", "scheduled_at": "2026-08-14T08:00:00Z" } },
    { "event_type": "followup.scheduled", "payload": { "lead_id": "lead-020", "interval": "J90", "scheduled_at": "2026-10-13T08:00:00Z" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

### 3.7 Negotiation Domain

```json
{
  "test_id": "T-NEGO-001-NOM-001",
  "rule_id": "NEGO-001",
  "rule_description": "4 buyer profiles: national, diaspora, investor, jeune actif",
  "test_type": "nominal",
  "scenario": "Diaspora buyer profile correctly identified",
  "input": {
    "buyer": { "diaspora_flag": true, "budget": 80000000, "age": 35 }
  },
  "expected_output": {
    "action": { "type": "assign_buyer_profile", "params": { "profile": "diaspora" } }
  },
  "expected_events": [
    { "event_type": "negotiation.profile_assigned", "payload": { "profile": "diaspora", "type": "buyer" } }
  ],
  "preconditions": {},
  "postconditions": { "buyer.profile": "diaspora" }
}
```

```json
{
  "test_id": "T-NEGO-004-NOM-001",
  "rule_id": "NEGO-004",
  "rule_description": "8 seller fears documented and addressable",
  "test_type": "nominal",
  "scenario": "Seller expresses fear about price, system addresses with LAWIM arguments",
  "input": {
    "seller_expression": "J'ai peur de ne pas trouver le bon prix",
    "detected_fear": "prix_injuste"
  },
  "expected_output": {
    "action": { "type": "address_objection", "params": { "fear": "prix_injuste", "argument": "mise_en_relation", "response_template": "objection_price_seller" } }
  },
  "expected_events": [
    { "event_type": "negotiation.objection_addressed", "payload": { "fear": "prix_injuste", "argument_used": "mise_en_relation" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-NEGO-005-NOM-001",
  "rule_id": "NEGO-005",
  "rule_description": "6 LAWIM arguments: zero commission, matching, accompaniment, WhatsApp, agents",
  "test_type": "nominal",
  "scenario": "Objection about commission triggers zero-commission argument",
  "input": {
    "objection": { "type": "commission", "text": "Combien prenez-vous de commission?" }
  },
  "expected_output": {
    "action": { "type": "present_argument", "params": { "argument": "zero_commission", "details": "LAWIM ne prend aucune commission sur les transactions" } }
  },
  "expected_events": [
    { "event_type": "negotiation.argument_presented", "payload": { "argument": "zero_commission" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

### 3.8 CRM Domain

```json
{
  "test_id": "T-CRM-001-NOM-001",
  "rule_id": "CRM-001",
  "rule_description": "7 role levels 1-7: demandeur(1) through master(7)",
  "test_type": "nominal",
  "scenario": "New user registered as demandeur (level 1)",
  "input": {
    "user": { "phone": "+237691234567", "name": "Jean Dupont" }
  },
  "expected_output": {
    "action": { "type": "assign_role", "params": { "role": "demandeur", "level": 1 } }
  },
  "expected_events": [
    { "event_type": "user.created", "payload": { "role": "demandeur", "level": 1 } }
  ],
  "preconditions": {},
  "postconditions": { "user.role": "demandeur", "user.level": 1 }
}
```

```json
{
  "test_id": "T-CRM-002-NOM-001",
  "rule_id": "CRM-002",
  "rule_description": "7x7 permission matrix",
  "test_type": "nominal",
  "scenario": "Master (level 7) can access all resources",
  "input": {
    "user": { "role": "master", "level": 7 },
    "requested_action": "view_all_leads"
  },
  "expected_output": {
    "action": { "type": "grant_access", "params": { "permission": "view_all_leads", "granted": true } }
  },
  "expected_events": [
    { "event_type": "access.granted", "payload": { "role": "master", "permission": "view_all_leads" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-CRM-002-NEG-001",
  "rule_id": "CRM-002",
  "rule_description": "7x7 permission — negative: demandeur cannot view all leads",
  "test_type": "negative",
  "scenario": "Demandeur (level 1) access to view_all_leads denied",
  "input": {
    "user": { "role": "demandeur", "level": 1 },
    "requested_action": "view_all_leads"
  },
  "expected_output": {
    "action": { "type": "deny_access", "params": { "permission": "view_all_leads", "reason": "insufficient_permissions", "required_level": 5 } }
  },
  "expected_events": [
    { "event_type": "access.denied", "payload": { "role": "demandeur", "permission": "view_all_leads", "reason": "insufficient_permissions" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-CRM-008-NOM-001",
  "rule_id": "CRM-008",
  "rule_description": "Identity resolution: phone=100, email=95, name+phone≥40",
  "test_type": "nominal",
  "scenario": "Same phone number resolves as 100% match",
  "input": {
    "existing_user": { "phone": "+237691234567", "email": "jean@example.com", "name": "Jean Dupont" },
    "incoming_lead": { "phone": "+237691234567", "name": "Jean D." }
  },
  "expected_output": {
    "action": { "type": "resolve_identity", "params": { "match_score": 100, "match_type": "phone", "existing_user_id": "user-050" } }
  },
  "expected_events": [
    { "event_type": "identity.resolved", "payload": { "match_score": 100, "match_type": "phone" } }
  ],
  "preconditions": {},
  "postconditions": { "lead.resolved_user_id": "user-050" }
}
```

```json
{
  "test_id": "T-CRM-008-NEG-001",
  "rule_id": "CRM-008",
  "rule_description": "Identity resolution — negative: different phone and email, no match",
  "test_type": "negative",
  "scenario": "Completely different contact info yields no identity resolution",
  "input": {
    "existing_user": { "phone": "+237691234567", "email": "jean@example.com", "name": "Jean Dupont" },
    "incoming_lead": { "phone": "+237698765432", "name": "Marie Claire" }
  },
  "expected_output": {
    "action": { "type": "new_identity", "params": { "reason": "no_match_found" } }
  },
  "expected_events": [],
  "preconditions": {},
  "postconditions": { "lead.resolved_user_id": null }
}
```

### 3.9 Language Domain

```json
{
  "test_id": "T-LANG-001-NOM-001",
  "rule_id": "LANG-001",
  "rule_description": "Default language: French",
  "test_type": "nominal",
  "scenario": "New session without language preference defaults to French",
  "input": {
    "session": { "user_id": "user-060", "language_preference": null }
  },
  "expected_output": {
    "action": { "type": "set_language", "params": { "language": "fr", "reason": "default" } }
  },
  "expected_events": [
    { "event_type": "language.default_set", "payload": { "language": "fr" } }
  ],
  "preconditions": {},
  "postconditions": { "user.language": "fr" }
}
```

```json
{
  "test_id": "T-LANG-003-NOM-001",
  "rule_id": "LANG-003",
  "rule_description": "LANGUE command switches language with persistence",
  "test_type": "nominal",
  "scenario": "User sends LANGUE EN to switch to English",
  "input": {
    "message": { "text": "LANGUE EN", "sender": "user-061" },
    "current_language": "fr"
  },
  "expected_output": {
    "action": { "type": "set_user_language", "params": { "language": "en", "persist": true } }
  },
  "expected_events": [
    { "event_type": "language.changed", "payload": { "from": "fr", "to": "en", "user_id": "user-061" } }
  ],
  "preconditions": { "user.language": "fr" },
  "postconditions": { "user.language": "en" }
}
```

```json
{
  "test_id": "T-LANG-010-NOM-001",
  "rule_id": "LANG-010",
  "rule_description": "Cameroon phone format: 237 + 9 digits",
  "test_type": "nominal",
  "scenario": "Cameroonian phone number is correctly formatted",
  "input": {
    "raw_phone": "691234567"
  },
  "expected_output": {
    "action": { "type": "format_phone", "params": { "normalized": "+237691234567", "country": "CM", "valid": true } }
  },
  "expected_events": [
    { "event_type": "phone.formatted", "payload": { "normalized": "+237691234567" } }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-LANG-010-NEG-001",
  "rule_id": "LANG-010",
  "rule_description": "Cameroon phone format — negative: invalid digit count rejected",
  "test_type": "negative",
  "scenario": "Phone number with 8 digits (not 9) is rejected",
  "input": {
    "raw_phone": "69123456"
  },
  "expected_output": {
    "action": { "type": "format_phone", "params": { "normalized": null, "country": null, "valid": false, "reason": "invalid_digit_count" } }
  },
  "expected_events": [],
  "preconditions": {},
  "postconditions": {}
}
```

### 3.10 Security Domain

```json
{
  "test_id": "T-SEC-001-NOM-001",
  "rule_id": "SEC-001",
  "rule_description": "Anti-spam: max 10 messages/minute",
  "test_type": "nominal",
  "scenario": "User sends 10 messages within a minute, 11th is blocked",
  "input": {
    "user_id": "user-070",
    "message_count_last_minute": 10,
    "new_message": { "text": "spam message" }
  },
  "expected_output": {
    "action": { "type": "block_message", "params": { "reason": "rate_limit_exceeded", "limit": 10, "current": 10 } }
  },
  "expected_events": [
    { "event_type": "message.blocked", "payload": { "user_id": "user-070", "reason": "rate_limit_exceeded" } }
  ],
  "preconditions": {},
  "postconditions": { "user.blocked_until": "{{current_time + 60min}}" }
}
```

```json
{
  "test_id": "T-SEC-001-NEG-001",
  "rule_id": "SEC-001",
  "rule_description": "Anti-spam — negative: 9 messages within a minute is allowed",
  "test_type": "negative",
  "scenario": "User sends 9th message within a minute, not blocked",
  "input": {
    "user_id": "user-071",
    "message_count_last_minute": 9,
    "new_message": { "text": "normal message" }
  },
  "expected_output": {
    "action": { "type": "allow_message", "params": { "reason": "under_rate_limit", "count": 9, "limit": 10 } }
  },
  "expected_events": [],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-SEC-004-NOM-001",
  "rule_id": "SEC-004",
  "rule_description": "Anti-fraud 4 layers: broker_spam, duplicate_listing, fake_price, suspicious_urgency",
  "test_type": "nominal",
  "scenario": "Suspicious urgency detected on listing, flagged as fraud",
  "input": {
    "listing": { "title": "URGENT!!! SUPER OFFRE!!!", "price": 1000000, "city": "Douala" },
    "fraud_signals": { "suspicious_urgency": true, "fake_price": false, "duplicate": false, "broker_spam": false }
  },
  "expected_output": {
    "action": { "type": "flag_fraud", "params": { "layer": "suspicious_urgency", "confidence": "HIGH" } }
  },
  "expected_events": [
    { "event_type": "fraud.detected", "payload": { "listing_id": "listing-001", "layer": "suspicious_urgency", "confidence": "HIGH" } }
  ],
  "preconditions": {},
  "postconditions": { "listing.fraud_flagged": true }
}
```

```json
{
  "test_id": "T-SEC-005-NOM-001",
  "rule_id": "SEC-005",
  "rule_description": "Anonymisation RGPD within 7 days",
  "test_type": "nominal",
  "scenario": "User requests deletion, data anonymisation scheduled within 7d",
  "input": {
    "user": { "id": "user-080", "consent_status": "active" },
    "request": { "type": "delete_data", "received_at": "2026-07-15T10:00:00Z" }
  },
  "expected_output": {
    "action": { "type": "schedule_anonymization", "params": { "deadline": "2026-07-22T10:00:00Z", "user_id": "user-080" } }
  },
  "expected_events": [
    { "event_type": "anonymization.requested", "payload": { "user_id": "user-080", "deadline": "2026-07-22T10:00:00Z" } }
  ],
  "preconditions": {},
  "postconditions": { "user.anonymization_scheduled": true }
}
```

---

## 4. Idempotence Test Examples

```json
{
  "test_id": "T-CONST-006-IDP-001",
  "rule_id": "CONST-006",
  "rule_description": "Matching as core — idempotence: multiple lead qualifications produce same match behavior",
  "test_type": "idempotence",
  "scenario": "Apply matching rule 3 times to same qualified lead, same result each time",
  "input": {
    "lead": { "id": "lead-100", "qualified": true, "intent": "BUY" }
  },
  "expected_output": {
    "apply_1": { "action": { "type": "enable_matching", "params": {} } },
    "apply_2": { "action": { "type": "enable_matching", "params": {} } },
    "apply_3": { "action": { "type": "enable_matching", "params": {} } }
  },
  "expected_events": [
    { "apply_1": [{ "event_type": "match.enabled" }] },
    { "apply_2": [{ "event_type": "match.enabled" }] },
    { "apply_3": [{ "event_type": "match.enabled" }] }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-QUAL-004-IDP-001",
  "rule_id": "QUAL-004",
  "rule_description": "V1 thresholds — idempotence: same score produces same classification",
  "test_type": "idempotence",
  "scenario": "Classify same score 3 times, always HOT",
  "input": {
    "lead": { "score": 85 }
  },
  "expected_output": {
    "apply_1": { "action": { "type": "classify_lead", "params": { "class": "HOT" } } },
    "apply_2": { "action": { "type": "classify_lead", "params": { "class": "HOT" } } },
    "apply_3": { "action": { "type": "classify_lead", "params": { "class": "HOT" } } }
  },
  "expected_events": [
    { "apply_1": [{ "event_type": "lead.classified", "payload": { "class": "HOT" } }] },
    { "apply_2": [{ "event_type": "lead.classified", "payload": { "class": "HOT" } }] },
    { "apply_3": [{ "event_type": "lead.classified", "payload": { "class": "HOT" } }] }
  ],
  "preconditions": {},
  "postconditions": {}
}
```

```json
{
  "test_id": "T-PROP-005-IDP-001",
  "rule_id": "PROP-005",
  "rule_description": "Auto-archive — idempotence: already archived property stays archived",
  "test_type": "idempotence",
  "scenario": "Apply auto-archive to already archived property, no change",
  "input": {
    "property": { "status": "archived", "last_activity": "2026-01-01T00:00:00Z" },
    "current_date": "2026-07-15T00:00:00Z"
  },
  "expected_output": {
    "apply_1": { "action": null },
    "apply_2": { "action": null },
    "apply_3": { "action": null }
  },
  "expected_events": {
    "apply_1": [],
    "apply_2": [],
    "apply_3": []
  },
  "preconditions": { "property.status": "archived" },
  "postconditions": { "property.status": "archived" }
}
```

---

## 5. Contract Validation

Every test contract file MUST be validated against this JSON Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RuleTestContract",
  "type": "object",
  "required": ["test_id", "rule_id", "rule_description", "test_type", "scenario", "input", "expected_output", "expected_events"],
  "properties": {
    "test_id": { "type": "string", "pattern": "^T-[A-Z]+-\\d{3}-(NOM|NEG|IDP|AUD)-\\d{3}$" },
    "rule_id": { "type": "string", "pattern": "^[A-Z]+-\\d{3}$" },
    "rule_description": { "type": "string", "minLength": 1 },
    "test_type": { "type": "string", "enum": ["nominal", "negative", "idempotence", "audit"] },
    "scenario": { "type": "string", "minLength": 1 },
    "input": { "type": "object" },
    "expected_output": { "type": "object" },
    "expected_events": { "type": "array" },
    "preconditions": { "type": "object" },
    "postconditions": { "type": "object" }
  }
}
```

---

## 6. Generating Test Contracts

Each rule MUST have a test contract generated via:

1. **Identify rule type** (threshold, string match, numeric range, state machine, boolean, enumeration, temporal, format, composition).
2. **Select test types** per ACCEPTANCE_TEST_MATRIX.md criticality.
3. **Define input** that exercises the rule's condition_expression.
4. **Define expected output** matching the rule's action definition.
5. **Define expected events** matching the rule's audit_template.
6. **Add edge cases** per rule type (Section 2).
7. **Validate** contract against JSON schema.

### Minimum Contract Requirements Per Criticality

| Criticality | Nominal | Negative | Idempotence | Audit | Total |
|-------------|---------|----------|-------------|-------|-------|
| HIGH | 2 | 1 | 1 | 1 | 5 |
| MEDIUM | 1 | 1 | 0 | 0 | 2 |
| LOW | 1 | 0 | 0 | 0 | 1 |
