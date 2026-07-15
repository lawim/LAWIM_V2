# SLA EXECUTION MODEL

**Domain:** Workflow and State Machine Architecture  
**Version:** 1.0  
**Source:** Heritage Gold Extraction — 05-WORKFLOW-REFERENCE.md Ch20-33 (SLA & Proactive Management), Ch22 (SLA tables), CRM_MODEL.md Sec 5 (Lead Priority SLAs)

---

## 1. SLA Registry

The SLA Registry stores the canonical SLA definitions for every entity type and state combination.

```json
{
  "sla_id": "sla_property_available_villa",
  "entity_type": "property",
  "property_type": "villa",
  "state": "Disponible",
  "metric": "time_in_state",
  "threshold_ms": 7776000000,  // 90 days (3 months)
  "direction": "MAX",          // breach when elapsed > threshold
  "severity": "WARNING",
  "action": {
    "type": "DIAGNOSTIC",
    "handler": "diagnostic_engine.analyze(property)",
    "parameters": {
      "checks": ["price", "photo_quality", "description", "availability", "owner_activity", "match_count", "visit_count", "refusal_count"]
    }
  },
  "escalation": {
    "first_breach": "NOTIFY_OWNER",
    "second_breach": "NBA_RECALCULATE",
    "third_breach": "ESCALATE_TO_LAWIM"
  },
  "notify_roles": ["owner", "agent"]
}
```

### 1.1 SLA Registry Schema

| Field | Type | Description |
|---|---|---|
| `sla_id` | string | Unique identifier |
| `entity_type` | string | Business entity (property, dossier, user, etc.) |
| `property_type` | string | Optional — property sub-type filter |
| `state` | string | State in which this SLA applies |
| `metric` | string | What is measured (time_in_state, response_time, count) |
| `threshold_ms` | integer | Threshold in milliseconds |
| `direction` | `MAX` or `MIN` | `MAX` = breach if exceeded, `MIN` = breach if below |
| `severity` | `INFO`, `WARNING`, `CRITICAL` | Breach severity level |
| `action` | ActionConfig | Action to take on breach |
| `escalation` | EscalationConfig | Escalation steps for repeated breaches |
| `notify_roles` | string[] | Roles to notify on breach |

> **ARCHITECTURE_DECISION:** SLA threshold values (e.g., 90-day auto-archive, market rotation durations per property type) are architecture-defined defaults sourced from Heritage Gold (PROP-005). Actual values must be validated against current market conditions during implementation.

---

## 2. Market Rotation SLA per Property Type

From Heritage Gold Ch22 — these are the reference normal rotation durations:

### 2.1 Property Type Rotation Expectations

| Property Type | Normal Rotation | Threshold (days) | Threshold (ms) |
|---|---|---|---|
| Chambre | 1-4 weeks | 28 days | 2,419,200,000 |
| Studio | 2-8 weeks | 56 days | 4,838,400,000 |
| Appartement | 1-4 months | 120 days | 10,368,000,000 |
| Villa | 3-12 months | 365 days | 31,536,000,000 |
| Terrain résidentiel | 3-18 months | 540 days | 46,656,000,000 |
| Terrain agricole | 6-36 months | 1095 days | 94,608,000,000 |
| Commerce | 1-6 months | 180 days | 15,552,000,000 |
| Bureau | 2-8 months | 240 days | 20,736,000,000 |
| Hôtel | 6-36 months | 1095 days | 94,608,000,000 |

### 2.2 SLA by Property Type (First Matching, Rematching, Follow-up)

From Heritage Gold SLA Tables:

| Property Type | First Matching | First Rematching | First Follow-up |
|---|---|---|---|
| Chambre | Immediate | 24h | 48h |
| Chambre moderne | Immediate | 24h | 48h |
| Studio | Immediate | 48h | 72h |
| Appartement | Immediate | 72h | 5 days |
| Maison | Immediate | 5 days | 7 days |
| Villa | Immediate | 7 days | 10 days |
| Duplex | Immediate | 7 days | 10 days |
| Terrain résidentiel | Immediate | 10 days | 15 days |
| Terrain agricole | Immediate | 15 days | 20 days |
| Terrain industriel | Immediate | 20 days | 30 days |
| Commerce | Immediate | 7 days | 10 days |
| Bureau | Immediate | 10 days | 15 days |
| Entrepôt | Immediate | 15 days | 20 days |
| Hôtel | Immediate | 30 days | 45 days |
| Immeuble | Immediate | 30 days | 45 days |

### 2.3 Example: Villa SLA Behavior

```json
{
  "entity": "property-villa-001",
  "type": "villa",
  "state": "Disponible",
  "entered_state_at": "2026-07-01T00:00:00Z",
  "sla": {
    "first_matching": { "threshold": "Immediate", "status": "COMPLETED" },
    "first_rematching": { "threshold_ms": 604800000, "deadline": "2026-07-08T00:00:00Z", "status": "PENDING" },
    "first_followup": { "threshold_ms": 864000000, "deadline": "2026-07-11T00:00:00Z", "status": "PENDING" },
    "rotation": { "threshold_ms": 31536000000, "deadline": "2027-07-01T00:00:00Z", "status": "OK" }
  }
}
```

---

## 3. Lead Priority SLAs

From Heritage Gold CRM_MODEL Sec 5:

| Priority | Types | SLA | Threshold |
|---|---|---|---|
| P0 | diaspora_investor, buyer > 50M FCFA | < 30 min | 1,800,000 ms |
| P1 | seller, land_buyer | < 2h | 7,200,000 ms |
| P2 | standard buyer, standard investor | < 24h | 86,400,000 ms |
| P3 | tenant, non-qualified prospect | J+1 to J+7 | 604,800,000 ms |

Lead Class Action SLAs:

| Class | Delay | Action |
|---|---|---|
| HOT | < 1h | call_immediately (Phone + WhatsApp) |
| WARM | < 24h | send_listings (WhatsApp) |
| COLD | < 48h | request_budget (WhatsApp) |
| LOW | J+7 / J+30 / J+90 | follow_up (WhatsApp) |
| SPAM | Immediate | ignore + block if persistent |

---

## 4. Incident Priority SLAs

From Heritage Gold:

| Priority | Handling Delay | Threshold |
|---|---|---|
| 🔴 Critique | Immediate | 0 ms |
| 🟠 Élevée | < 24h | 86,400,000 ms |
| 🟡 Normale | < 72h | 259,200,000 ms |
| 🟢 Faible | Per support availability | Configurable |

---

## 5. Follow-up Intervals (Commercial)

| Priority | Interval | Channel | Threshold |
|---|---|---|---|
| URGENT | Within hours | WhatsApp/Telegram | 3,600,000 ms |
| HIGH | Daily | WhatsApp | 86,400,000 ms |
| NORMAL | Every 3 days | WhatsApp/Telegram | 259,200,000 ms |
| LOW | Weekly | Telegram | 604,800,000 ms |

### 5.1 Long-term Follow-up Cadence

| Milestone | Delay | Use Case |
|---|---|---|
| J1 | 24h | Post-qualification follow-up |
| J7 | 168h | Post-presentation check-in |
| J30 | 720h | Monthly re-engagement |
| J90 | 2160h | Quarterly review |

---

## 6. Dossier Health SLA

> A dossier must never remain without significant event beyond the applicable SLA. If exceeded, system MUST: launch rematching, follow up a party, propose an adjustment, or escalate to LAWIM collaborator.

The SLA Monitor evaluates every active dossier against its state-specific SLA. If no event has occurred within the threshold, the system escalates:

```
Dossier in "Attente décision demandeur" for > 48h
  → NBA recalculates to FOLLOW_UP
  → First reminder sent
  → If no response for another 48h → Second reminder
  → If no response for another 72h → Last reminder
  → If no response → Mark as LOW priority, period follow-up (J7/J30/J90)
```

---

## 7. SLA Monitoring

### 7.1 Check Frequency

| SLA Category | Check Frequency |
|---|---|
| Market rotation (property) | Every 24h |
| First matching | Immediate (event-triggered) |
| Lead priority (P0-P3) | Every 1 min |
| Lead class (HOT/WARM) | Every 5 min |
| Incident (Critique) | Continuous (event-triggered) |
| Incident (Élevée/Normale) | Every 30 min |
| Follow-up intervals | Every 1h |
| Dossier health | Every 1h |
| Visit reminders | Every 15 min |

### 7.2 Evaluation Algorithm

```
function evaluateSLA(entity, slaDefinition):
    elapsed = now() - entity.lastStateChangeAt
    if slaDefinition.direction == 'MAX':
        return elapsed > slaDefinition.threshold_ms ? BREACHED : OK
    else:  // MIN
        return elapsed < slaDefinition.threshold_ms ? BREACHED : OK

function monitorTick():
    for each (entityType, state) in slaRegistry.getActiveSLAs():
        entities = stateManager.getEntitiesInState(entityType, state)
        for entity in entities:
            slaDef = slaRegistry.get(entityType, entity.state, entity.propertyType)
            if slaDef == null: continue
            status = evaluateSLA(entity, slaDef)
            if status == BREACHED:
                handleBreach(entity, slaDef)
```

### 7.3 Breach Detection Event

```json
{
  "event_type": "sla.breach",
  "entity_type": "property",
  "entity_id": "property-abc-123",
  "state": "Disponible",
  "sla_id": "sla_property_available_villa",
  "threshold_ms": 31536000000,
  "elapsed_ms": 32000000000,
  "severity": "WARNING",
  "breach_count": 1,
  "timestamp": "2026-07-15T10:00:00Z"
}
```

---

## 8. Breach Handling

### 8.1 Breach Response Flow

```
SLA BREACH DETECTED
    │
    ├──→ Increment breach counter on entity
    │
    ├──→ Execute breach action (from SLA definition)
    │       │
    │       ├──→ type=DIAGNOSTIC: Run diagnostic engine
    │       ├──→ type=NOTIFY: Send notification to notify_roles
    │       ├──→ type=NBA_RECALCULATE: Trigger NBA recalculation
    │       ├──→ type=ESCALATE: Flag for LAWIM collaborator
    │       └──→ type=AUTO_ARCHIVE: Archive entity automatically
    │
    ├──→ Emit sla.breach event → EventBus
    │
    ├──→ Apply escalation rules (if repeated breach)
    │       │
    │       ├──→ 1st breach: NOTIFY
    │       ├──→ 2nd breach: NBA_RECALCULATE + NOTIFY
    │       └──→ 3rd+ breach: ESCALATE_LAWIM + SUSPEND/CONFIGURE
    │
    └──→ Log to SLA breach history
```

### 8.2 Breach Notifications

| SLA Entity | Notify Roles | Channel |
|---|---|---|
| Property rotation | Owner, Agent | WhatsApp, Email |
| Lead priority (P0) | Agent, Agency admin | Phone, WhatsApp |
| Lead priority (P1-P3) | Agent | WhatsApp |
| Incident (Critique) | LAWIM admin | Phone, WhatsApp, Email |
| Incident (Élevée) | LAWIM support | WhatsApp, Email |
| Dossier health | LAWIM AI (auto-action) | System internal |

### 8.3 Automatic Actions on Breach

| SLA | First Breach | Second Breach | Third Breach |
|---|---|---|---|
| Property rotation exceeded | Diagnostic + notify owner | Suggest price reduction + premium visibility | Auto-archive proposal |
| Dossier no event | First reminder | Second reminder | Escalate to LAWIM collaborator |
| Lead P0 not contacted | Agent alert + reassign | Escalate to agency admin | Escalate to LAWIM |
| Incident not handled | Priority escalation | Assign additional resources | LAWIM admin notified |
| Visit reminder | 24h reminder | 2h reminder | None (visit near) |

---

## 9. NBA Engine Integration

### 9.1 How SLA Breaches Trigger NBA Recalculation

Every SLA breach event triggers a full NBA recalculation. The NBA may produce a different action than before:

```
SLA Breach: Property rotation exceeded for property-abc-123
    ↓
NBA Recalculation:
    1. Correct incoherence? No
    2. Complete critical field? No (fields complete)
    3. Matching? Already done, no new matches
    4. Present property? Already presented
    5. Contact holder? → YES (Confirm availability)
    6. Organize visit? No
    7. Follow up? No
    8. Notifications? No
    9. Optimize dossier? Maybe later
    
    Result: CONTACT_HOLDER (recalculate)
    ↓
Action: System contacts holder to confirm availability
```

### 9.2 NBA Priority After SLA Breach

SLA breaches elevate the NBA priority. The system escalates the action:

```
Normal:      NBA = LAUNCH_MATCHING (priority 3)
After SLA:   NBA = CONTACT_HOLDER  (priority 5 — still within normal range)
After 2x:    NBA = FOLLOW_UP        (priority 7 — manual follow-up needed)
After 3x+:   NBA = NOTIFICATIONS    (priority 8 — LAWIM admin alerted)
```

### 9.3 NBA-SLA Mapping

| SLA Breach Type | New NBA | Rationale |
|---|---|---|
| Property unavailable too long | Confirm availability | Ensure accurate status |
| Property rotation exceeded | Price reduction / Premium visibility | Improve listing performance |
| Dossier no matching progress | Launch matching | Restart matching with expanded criteria |
| Dossier waiting too long | Follow up / Rematch | Re-engage demandeur |
| Lead not contacted within SLA | Contact immediately | Re-prioritize lead |
| Visit not confirmed | Confirm visit (reminder) | Ensure visit happens |
| Negotiation silence | Follow up / Remind | Unblock negotiation |
| Incident not handled | Escalate / Reassign | Ensure resolution |

---

## 10. SLA by Entity Type — Complete Reference

### 10.1 Property SLA

| State | Metric | Threshold | Breach Action |
|---|---|---|---|
| `Création` | Time to qualify | 24h | Reminder to complete fields |
| `Qualification` | Time to validate | 48h | Reminder to enrich data |
| `Validation` | Time to publish | 24h | Reminder to validate |
| `Disponible` | Time in market | Per type (see §2.1) | Diagnostic + NBA recalculation |
| `Matching` | Time to match | Immediate | System auto-triggers |
| `Visites` | Time before first visit | Per property type | Follow-up with demandeur |
| `Négociation` | Time in negotiation | 30 days (default) | Negotiation follow-up |
| `Indisponible` | Auto-archival | 90 days inactivity | Auto-archive |

### 10.2 Dossier SLA

| State | Metric | Threshold | Breach Action |
|---|---|---|---|
| `Création` | Time to qualify | 24h | Ask qualifying questions |
| `Qualification` | Time to critical fields | 48h | Ask specific missing fields |
| `Matching` | Matching trigger | Immediate | Auto-trigger on field completion |
| `Présentation` | Time to decision | 72h (default) | Follow up with demandeur |
| `Attente décision demandeur` | Response time | By urgency level | Reminder chain |
| `Attente décision détenteur` | Response time | By property type | Holder silence workflow |
| `Visite` | Time to visit | 7 days (default) | Follow-up with both parties |
| `Négociation` | Time to outcome | 30 days | Reminder chain, auto-close |
| `Transaction` | Time to complete | 60 days | Follow-up on pending items |
| Any non-terminal | Significant event gap | Per property type SLA | Rematch, follow up, or escalate |

### 10.3 Lead SLA

| Class | Metric | Threshold | Breach Action |
|---|---|---|---|
| HOT | Time to contact | < 1h | Agent alert, reassign if no response |
| WARM | Time to send listings | < 24h | Agent reminder |
| COLD | Time to budget request | < 48h | Agent reminder |
| LOW | Time to follow-up | J+7 / J+30 / J+90 | System auto-follow-up |
| P0 | Time to first action | < 30 min | Escalate to agency admin |
| P1 | Time to first action | < 2h | Agent alert |
| P2 | Time to first action | < 24h | Agent reminder |
| P3 | Time to first action | J+1 to J+7 | Periodic reminder |

### 10.4 Incident SLA

| Priority | Metric | Threshold | Breach Action |
|---|---|---|---|
| 🔴 Critique | Time to respond | Immediate | LAWIM admin phone alert |
| 🟠 Élevée | Time to respond | < 24h | Daily check, escalate if missed |
| 🟡 Normale | Time to respond | < 72h | Reminder at 48h |
| 🟢 Faible | Time to respond | As available | No automatic escalation |

### 10.5 Visit SLA

| Event | Metric | Threshold | Breach Action |
|---|---|---|---|
| Pre-visit reminder | Time before visit | 24h before | Send reminder to both parties |
| Pre-visit reminder | Time before visit | 2h before | Send reminder to both parties |
| Post-visit follow-up | Time after visit | 24h | Request satisfaction feedback |

### 10.6 User Identity SLA

| State | Metric | Threshold | Breach Action |
|---|---|---|---|
| `NEW_USER` | Time to first action | 7 days | Welcome reminder |
| `INACTIVE` | Time since last activity | 90 days | Reactivation campaign |
| Phone verification | Time to verify | 24h | Reminder |
| Identity verification | Time to verify | 72h | Reminder + support offer |
| Professional validation | Time to verify | 7 days | Agent follow-up |

---

## 11. SLA Breach History

```sql
CREATE TABLE sla_breach_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sla_id VARCHAR(64) NOT NULL,
  entity_type VARCHAR(64) NOT NULL,
  entity_id VARCHAR(128) NOT NULL,
  state VARCHAR(64) NOT NULL,
  threshold_ms BIGINT NOT NULL,
  elapsed_ms BIGINT NOT NULL,
  severity VARCHAR(16) NOT NULL,
  breach_count INTEGER NOT NULL DEFAULT 1,
  action_taken VARCHAR(64),
  action_result JSONB,
  nba_before VARCHAR(64),
  nba_after VARCHAR(64),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_sla_breach_entity ON sla_breach_history(entity_type, entity_id);
CREATE INDEX idx_sla_breach_time ON sla_breach_history(created_at DESC);
```

---

## 12. SLA Configuration per Entity Type

### 12.1 Default Values

Most SLAs have configurable thresholds. The defaults are based on Heritage Gold reference values and can be overridden per:
- Property type (for property rotation)
- Urgency level (for dossier response times)
- Lead priority (for lead handling)
- Incident priority (for incident handling)
- Organization settings (for agency-level customizations)

### 12.2 Override Priority

```
System default < Property type default < Entity instance override < Manual override
```

Higher priority overrides take precedence. If no override exists at a level, the next lower level is used.

---

## 13. Example: Complete SLA Lifecycle for a Property

```json
// Property created
{
  "entity": "property-001",
  "type": "appartement",
  "state": "Création",
  "sla": { "threshold": "24h", "remaining": "24h", "status": "OK" }
}

// 30 hours later — SLA BREACH
→ Breach: "Property in Création for 30h, threshold 24h"
→ Action: Send reminder to owner to complete fields
→ NBA: COMPLETE_CRITICAL_FIELD

// Fields completed, moves to Disponible
{
  "entity": "property-001",
  "type": "appartement",
  "state": "Disponible",
  "sla": { "threshold": "120 days", "remaining": "120 days", "status": "OK" }
}

// 130 days later — SLA BREACH
→ Breach: "Property in Disponible for 130d, threshold 120d"
→ Action: Run diagnostic (price, photos, description, availability, owner activity, matches, visits, refusals)
→ NBA: Based on diagnostic — suggest price reduction or premium visibility

// If 90 days after breach with no improvement
→ Second breach escalation
→ Action: Propose auto-archival to owner
```

---

## 14. Constitutional SLA Rules

From Heritage Gold:

1. **No active dossier, no published property, no transaction shall remain without action beyond the applicable SLA.**
2. **If exceeded, LAWIM MUST trigger an appropriate action.**
3. **Inaction is considered an operational anomaly.**
4. **A workflow without a next action is considered defective.**
