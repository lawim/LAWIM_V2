# Decision Contract

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL

---

This document defines the formal input and output contracts for every decision cycle in LAWIM's execution pipeline. All components MUST adhere to these shapes. No component may extend, shrink, or bypass these contracts.

---

## 1. Input Contract

The input to a decision cycle is a complete snapshot of the current context. It is immutable for the duration of the cycle.

```json
{
  "actor": {
    "role": "buyer|seller|agent|investor|tenant|owner|broker|admin",
    "trust_level": "new|verified|elevated|high|revoked",
    "permissions": ["read_property", "create_lead", "send_message", ...]
  },
  "intent": {
    "type": "buy|rent|sell|invest|short_stay|lease",
    "confidence": 0.0,
    "extracted_facts": {
      "property_type": "apartment|house|villa|land|...",
      "city": "Douala",
      "neighborhood": "Bonanjo",
      "budget": 50000000,
      "urgency": "high|medium|low"
    }
  },
  "project": {
    "id": "proj_<uuid>",
    "type": "search|listing|investment",
    "state": "qualifying|matching|negotiating|closing|archived"
  },
  "dossier": {
    "id": "dos_<uuid>",
    "type": "buyer_profile|property_dossier|transaction_dossier",
    "state": "draft|complete|active|archived",
    "readiness": 0.0
  },
  "facts": {
    "property_type": { "value": "apartment", "confidence": 0.95, "source": "explicit" },
    "city": { "value": "Douala", "confidence": 1.0, "source": "explicit" },
    "budget": { "value": 50000000, "confidence": 0.8, "source": "inferred" },
    "diaspora": { "value": true, "confidence": 0.9, "source": "phone_prefix" }
  },
  "state": {
    "current_workflow": "lead_qualification",
    "current_step": "budget_collection",
    "previous_steps": ["intent_detection", "city_detection"]
  },
  "channel": "whatsapp|telegram|dashboard|api",
  "history": [
    {
      "decision_id": "dec_<uuid>",
      "action": "qualify.continue",
      "outcome": "budget_collected",
      "timestamp": "2026-07-14T18:00:00Z"
    }
  ],
  "permissions": {
    "can_view_property": true,
    "can_contact_owner": false,
    "can_receive_proposals": true
  },
  "consents": {
    "data_processing": true,
    "contact_by_agent": false,
    "share_with_partners": false
  },
  "search_results": [
    {
      "property_id": "prop_<uuid>",
      "match_score": 85,
      "explanation": { "city": "exact", "budget": "within_10pct", "type": "exact" }
    }
  ],
  "matches": [
    {
      "match_id": "match_<uuid>",
      "property_id": "prop_<uuid>",
      "score": 85,
      "status": "proposed|accepted|rejected|expired"
    }
  ],
  "relationship": {
    "with_agent": null,
    "with_owner": null,
    "consent_stage": "not_started|requested|granted|declined"
  },
  "time_context": {
    "current_time": "2026-07-15T14:30:00+01:00",
    "business_hours": true,
    "sla_status": "within_sla|approaching_sla|breached",
    "sla_deadline": "2026-07-15T18:00:00+01:00"
  },
  "geographic_context": {
    "country": "CM",
    "region": "Littoral",
    "city": "Douala",
    "neighborhood": "Bonanjo",
    "gps_coordinates": { "lat": 4.05, "lng": 9.70 }
  },
  "commercial_context": {
    "negotiation_stage": "none|initial|active|closing",
    "current_offer": null,
    "visit_scheduled": false,
    "visit_completed": false
  }
}
```

### Input field specification

| Field | Type | Required | Source |
|-------|------|----------|--------|
| `actor` | `Actor` | Yes | IAM/Role Engine |
| `intent` | `Intent` | Yes | Conversation Engine → Intent Detector |
| `project` | `Project` | Yes | Projects and Dossiers domain |
| `dossier` | `Dossier` | No | Projects and Dossiers domain |
| `facts` | `Map<string, Fact>` | Yes | Qualification Engine + Knowledge Builder |
| `state` | `WorkflowState` | Yes | Workflow Engine |
| `channel` | `Channel` | Yes | Channel adapter |
| `history` | `DecisionRef[]` | Yes | Audit store |
| `permissions` | `Permissions` | Yes | Role Engine |
| `consents` | `Consents` | Yes | Consent store |
| `search_results` | `SearchResult[]` | No | Search Engine |
| `matches` | `Match[]` | No | Matching Engine |
| `relationship` | `RelationshipState` | No | Relationship domain |
| `time_context` | `TimeContext` | Yes | System clock + SLA tracker |
| `geographic_context` | `GeoContext` | No | Geo Engine |
| `commercial_context` | `CommercialContext` | No | Commercial follow-up domain |

### Null/Empty handling

- **Missing optional field**: The field is `null`. The Decision Engine should note it in `required_data` if the field is needed.
- **Missing required field**: The engine MUST NOT proceed. Return `awaiting_data` as NBA with `required_data` listing the missing field.
- **Empty array**: Treated as "nothing to report" — not an error.

---

## 2. Output Contract

Every decision cycle produces exactly one `Decision` object.

```json
{
  "decision_id": "dec_<uuid>",
  "applicable_rules": [
    {
      "rule_id": "QUAL-002",
      "domain": "qualification",
      "matched_conditions": ["score >= 80", "intent == buy"],
      "priority_score": 0.85,
      "evaluation_status": "matched"
    },
    {
      "rule_id": "QUAL-009",
      "domain": "qualification",
      "matched_conditions": ["score >= 60"],
      "priority_score": 0.60,
      "evaluation_status": "matched"
    }
  ],
  "selected_rule": {
    "rule_id": "QUAL-002",
    "domain": "qualification",
    "knowledge_id": "GOLD-DM-020",
    "action": {
      "type": "call_immediately",
      "params": {
        "channel": "whatsapp",
        "template": "hot_lead_notification",
        "target_entity": "agent"
      },
      "target_engine": "conversation_engine"
    },
    "version": "1.0",
    "effective_date": "2026-06-01"
  },
  "rejected_rules": [
    {
      "rule_id": "QUAL-009",
      "domain": "qualification",
      "priority_score": 0.60,
      "reason": "lower_priority",
      "resolution": {
        "strategy": "priority",
        "winner": "QUAL-002",
        "winner_score": 0.85
      }
    }
  ],
  "reason": {
    "short": "Lead scored 85 (HOT) → call immediately.",
    "long": "Decision dec_abc123: Rule QUAL-002 matched with priority 0.85. 2 rules matched, 1 rejected (QUAL-009: lower_priority 0.60 < 0.85). Confidence: 0.85. Next action: call_immediately.",
    "structured": {
      "selected": "QUAL-002 (HOT lead → call_immediately, priority 0.85)",
      "rejected": ["QUAL-009 (call_immediately, priority 0.60) — lower priority"],
      "reasoning": "Highest priority rule selected. No conflicts detected."
    }
  },
  "next_action": {
    "action": "call_immediately",
    "target_entity": "agent_001",
    "params": {
      "template": "hot_lead_notification",
      "lead_id": "lead_<uuid>",
      "priority": "high"
    },
    "explanation": "HOT lead (score 85) requires immediate agent notification.",
    "priority_score": 0.92,
    "time_sensitivity": "urgent"
  },
  "required_data": [
    {
      "field": "facts.budget",
      "reason": "Matching cannot proceed without budget",
      "urgency": "high",
      "acquisition_strategy": "ask"
    }
  ],
  "state_transition": {
    "from": "lead_qualification.intent_detected",
    "to": "lead_qualification.budget_collected",
    "trigger": "data_collected"
  },
  "response_strategy": {
    "type": "proactive_notification",
    "channel": "whatsapp",
    "template": "hot_lead_alert",
    "language": "fr",
    "tone": "professional"
  },
  "business_action": {
    "type": "notify_agent",
    "engine": "conversation_engine",
    "payload": {
      "agent_id": "agent_001",
      "lead_id": "lead_<uuid>",
      "message": "Nouveau lead HOT: acheteur cherche appartement à Douala Bonanjo, budget 50M FCFA. Contactez immédiatement."
    }
  },
  "audit_events": [
    {
      "event_type": "decision.made",
      "severity": "info",
      "payload": { "decision_id": "dec_<uuid>", "selected_rule": "QUAL-002" }
    },
    {
      "event_type": "rule.rejected",
      "severity": "debug",
      "payload": { "rule_id": "QUAL-009", "reason": "lower_priority" }
    }
  ],
  "confidence": 0.85,
  "fallback_policy": {
    "if_action_fails": "retry_max_3",
    "if_no_match": "use_default_call_agent",
    "if_low_confidence": "escalate_to_admin",
    "escalation_contact": "admin_dashboard_alert"
  }
}
```

### Output field specification

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision_id` | `string` | Yes | Unique identifier: `dec_<uuid>` |
| `applicable_rules` | `RuleMatch[]` | Yes | All rules that matched conditions, with priority scores |
| `selected_rule` | `Rule` | Yes | The single winning rule |
| `rejected_rules` | `RuleRejection[]` | Yes | All matched rules that were not selected, with reasons |
| `reason` | `Explanation` | Yes | Human-readable explanation in short, long, and structured forms |
| `next_action` | `NextAction` | Yes | The single next action to execute |
| `required_data` | `DataRequirement[]` | No | What data is still needed (empty if complete) |
| `state_transition` | `StateTransition` | No | Workflow state change (null if no transition) |
| `response_strategy` | `ResponseStrategy` | Yes | How to communicate the decision |
| `business_action` | `BusinessAction` | Yes | The business operation to perform |
| `audit_events` | `AuditEvent[]` | Yes | Events to emit (at minimum one `decision.made` event) |
| `confidence` | `number` | Yes | 0.0–1.0 confidence in this decision |
| `fallback_policy` | `FallbackPolicy` | Yes | What to do if execution fails |

### Output invariants

1. **Every decision has exactly one `selected_rule`** — even if it's the `no_match` fallback rule.
2. **Every decision has a `next_action`** — even if it's `no_action_required`.
3. **`applicable_rules` is never empty** — at minimum the fallback rule is listed.
4. **`rejected_rules` includes ALL matched rules that were not selected** — no silent rejection.
5. **`confidence` is always set** — minimum 0.0 (no confidence) to 1.0 (absolute certainty).
6. **`audit_events` always includes `decision.made`** — traceability is mandatory.

---

## 3. Contract Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-15 | Initial canonical contract |

The input/output contracts are versioned independently of the execution architecture. A contract change requires an ADR and must be backward-compatible for at least one minor version.
