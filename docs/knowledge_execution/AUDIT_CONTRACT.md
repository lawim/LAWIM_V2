# Audit Contract

**Domain:** Audit and Compliance Infrastructure
**Version:** 1.0
**Status:** CANONICAL

---

## 1. Audit Mandate

The LAWIM Audit System provides an immutable, queryable, and privacy-protected record of every business-significant event in the system. The audit trail is the single source of truth for compliance, dispute resolution, performance analysis, and regulatory reporting.

**Constitutional principle:** Every decision, every state transition, every consent action, every data access, every permission change, and every payment MUST be audited. No business operation occurs outside the audit trail.

---

## 2. What Must Be Audited

### 2.1 Mandatory Audit Events

| Category | What Is Audited | Audit Event Type | Immutable |
|----------|----------------|------------------|-----------|
| **Decisions** | Every decision cycle, including rule selection, confidence, NBA, fallback | `decision.made`, `rule.conflict` | Yes |
| **State Transitions** | Every state machine transition in any of the 21 workflows | `state.transitioned` | Yes |
| **Consent Actions** | Every consent request, grant, refusal, and withdrawal | `consent.requested`, `consent.granted`, `consent.refused` | Yes |
| **Data Access** | Every access to high/critical privacy data | `access.granted`, `access.denied` | Yes |
| **Permission Changes** | Every role change, permission grant/revoke, trust level change | `permission.changed`, `role.changed` | Yes |
| **Payments** | Every payment attempt, success, failure, refund, dispute | All `payment.*` events | Yes |
| **Identity Actions** | Every identity resolution, user creation, merge | `identity.resolved`, `user.created` | Yes |
| **Fraud/Security** | Every fraud detection, security alert, handover | `fraud.detected`, `handover.requested` | Yes |
| **Relationship Events** | Every relationship creation, expiration, revocation | All `relationship.*` events | Yes |
| **NBA Actions** | Every action planned, executed, or failed | All `action.*` events | Yes |
| **SLA Events** | Every SLA breach and escalation | `SLA.breached` | Yes |

### 2.2 Exception: What Is NOT Audited

- **Read-only queries** on public data (property listings, published content).
- **Internal system health checks** and heartbeat signals.
- **Transient runtime metrics** (CPU, memory, connection pool) — these use a separate observability pipeline.
- **User-facing analytics events** (page views, button clicks) — these are captured by the analytics system, not the audit system.

---

## 3. Audit Record Structure

### 3.1 Canonical Audit Record

Every audit event conforms to this schema:

```json
{
  "audit_id": "aud_<ulid>",
  "event_id": "evt_<ulid>",
  "event_type": "state.transitioned",
  "timestamp": "2026-07-15T12:00:00.000Z",
  "actor": {
    "id": "agent_xyz789",
    "role": "agent",
    "trust_level": 4,
    "organization_id": "org_abc",
    "session_id": "sess_<ulid>"
  },
  "entity": {
    "type": "dossier",
    "id": "dossier_abc123",
    "previous_state": "Matching",
    "new_state": "Présentation"
  },
  "context": {
    "channel": "whatsapp",
    "ip_address": "196.xxx.xxx.xxx",
    "user_agent": "WhatsApp/2.24.10",
    "geo_location": { "city": "Douala", "region": "Littoral" },
    "correlation_id": "corr_<ulid>",
    "causation_id": "evt_<ulid>"
  },
  "decision": {
    "decision_id": "dec_<ulid>",
    "selected_rule": "MATCH-005",
    "confidence": 0.87,
    "nba": "PRESENT_PROPERTY"
  },
  "payload_snapshot": {
    "before": { /* entity state before event */ },
    "after": { /* entity state after event */ }
  },
  "privacy": {
    "level": "low",
    "masked_fields": [],
    "access_restriction": "none"
  },
  "hash": "sha256-<hex>",
  "previous_audit_hash": "sha256-<hex>"
}
```

### 3.2 Field Specifications

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `audit_id` | `string (ULID)` | Yes | Unique audit record identifier |
| `event_id` | `string (ULID)` | Yes | Reference to the original event |
| `event_type` | `string` | Yes | Canonical event type |
| `timestamp` | `string (ISO 8601)` | Yes | When the event occurred (UTC) |
| `actor.id` | `string` | Yes | Who/what caused the event |
| `actor.role` | `string` | Yes | Actor's role at time of event |
| `actor.trust_level` | `int` | Yes | Actor's trust level (1-6) |
| `actor.organization_id` | `string` | No | Actor's organization if applicable |
| `actor.session_id` | `string` | Yes | Authentication session ID |
| `entity.type` | `string` | Yes | Type of business entity |
| `entity.id` | `string` | Yes | Entity identifier |
| `entity.previous_state` | `string` | No | State before event |
| `entity.new_state` | `string` | No | State after event |
| `context.channel` | `string` | No | Interaction channel |
| `context.ip_address` | `string` | No | Actor IP (masked for privacy_level >= high) |
| `context.user_agent` | `string` | No | Client user agent |
| `context.geo_location` | `object` | No | Approximate location (city/region only) |
| `context.correlation_id` | `string` | Yes | Business transaction trace ID |
| `context.causation_id` | `string` | Yes | Direct cause event ID |
| `decision.decision_id` | `string` | No | Reference to Decision Engine decision |
| `decision.selected_rule` | `string` | No | Rule selected |
| `decision.confidence` | `float` | No | Decision confidence |
| `decision.nba` | `string` | No | Next Best Action determined |
| `payload_snapshot.before` | `object` | No | Entity state snapshot before event (masked) |
| `payload_snapshot.after` | `object` | No | Entity state snapshot after event (masked) |
| `privacy.level` | `enum` | Yes | `public`, `low`, `medium`, `high`, `critical` |
| `privacy.masked_fields` | `string[]` | No | Fields that were masked in this record |
| `privacy.access_restriction` | `enum` | No | `none`, `role_based`, `need_to_know`, `audit_only` |
| `hash` | `string` | Yes | SHA-256 hash of this record |
| `previous_audit_hash` | `string` | Yes | SHA-256 hash of previous record in chain |

### 3.3 Minimal Audit Record

For high-volume, low-sensitivity events (e.g., `state.transitioned` for system-internal states), a minimal record form MAY be used:

```json
{
  "audit_id": "aud_<ulid>",
  "event_id": "evt_<ulid>",
  "event_type": "state.transitioned",
  "timestamp": "2026-07-15T12:00:00.000Z",
  "actor": { "id": "system", "role": "system" },
  "entity": { "type": "property", "id": "prop_123" },
  "context": { "correlation_id": "corr_<ulid>" },
  "privacy": { "level": "low", "access_restriction": "none" },
  "hash": "sha256-<hex>",
  "previous_audit_hash": "sha256-<hex>"
}
```

### 3.4 Payload Snapshot Rules

| Event Category | Snapshot Required? | Detail Level |
|----------------|-------------------|--------------|
| State transition | Yes | Full before/after entity state |
| Consent action | Yes | Full consent record (masked PII) |
| Payment | Yes | Amount, status, provider ref (no full PAN) |
| Decision | Yes | All rule candidates, rejections, conflicts |
| Permission change | Yes | Full before/after permission set |
| Data access | Yes | Resource accessed, reason, authorization |
| Frau d detection | Yes | Indicators, confidence, actions taken |
| NBA action | No | action_id + status sufficient |
| System config | No | Key + before/after value only |

---

## 4. Immutable Audit Trail

### 4.1 Hash Chain

Every audit record contains a `previous_audit_hash` that links to the SHA-256 hash of the immediately preceding record. This creates a cryptographic chain that makes tampering detectable:

```
audit_001: { hash: H(audit_001), previous_audit_hash: null }
audit_002: { hash: H(audit_002), previous_audit_hash: H(audit_001) }
audit_003: { hash: H(audit_003), previous_audit_hash: H(audit_002) }
... chain continues indefinitely
```

If any record is modified, its hash changes, breaking the link to all subsequent records.

### 4.2 Integrity Verification

The system performs periodic integrity checks (default: every 6 hours):

```
for each partition:
  for i = 1..N:
    computed_hash = sha256(audit_records[i])
    stored_hash = audit_records[i].hash
    if computed_hash != stored_hash → CRITICAL ALERT
    
    expected_prev_hash = sha256(audit_records[i-1])
    if audit_records[i].previous_audit_hash != expected_prev_hash → CRITICAL ALERT
```

### 4.3 Immutability Guarantees

| Guarantee | Mechanism |
|-----------|-----------|
| No deletion | Records are marked as `excluded` but never physically deleted |
| No update | Audit records are append-only; no UPDATE statements execute on the audit store |
| No archival before retention | Cold storage preserves original hashes and chain continuity |
| Tamper detection | Hash chain verification + periodic integrity checks |
| Write-once storage | Underlying storage uses append-only files (WAL) |

---

## 5. Query Capabilities

### 5.1 Supported Query Patterns

| Query Pattern | Description | Example |
|--------------|-------------|---------|
| **By entity** | All events for a specific entity | `SELECT * WHERE entity.type = 'dossier' AND entity.id = 'dossier_abc'` |
| **By actor** | All events caused by a specific actor | `SELECT * WHERE actor.id = 'agent_xyz'` |
| **By time range** | Events within a time window | `SELECT * WHERE timestamp BETWEEN '2026-07-01' AND '2026-07-15'` |
| **By event type** | All events of a specific type | `SELECT * WHERE event_type = 'consent.granted'` |
| **By correlation_id** | Full trace of a business transaction | `SELECT * WHERE correlation_id = 'corr_abc' ORDER BY timestamp` |
| **By causation chain** | All descendants of an event | Recursive query on `causation_id` |
| **By decision_id** | All events related to a specific decision | `SELECT * WHERE decision.decision_id = 'dec_abc'` |
| **Composite** | Any combination of the above | `WHERE entity.type = 'dossier' AND timestamp > '2026-07-01' AND event_type = 'state.transitioned'` |
| **Entity state history** | Full state machine history of an entity | `SELECT entity.previous_state, entity.new_state, timestamp WHERE entity.id = 'dossier_abc' ORDER BY timestamp` |
| **Actor activity report** | All actions by an actor in a time range | `SELECT event_type, timestamp, entity WHERE actor.id = 'agent_xyz' AND timestamp > '2026-07-01' ORDER BY timestamp` |

### 5.2 Query Performance Targets

| Query Pattern | Hot Store (90 days) | Cold Store (full retention) |
|--------------|---------------------|------------------------------|
| By entity ID | < 100ms | < 2s |
| By actor ID | < 200ms | < 5s |
| By time range (1 day) | < 500ms | < 3s |
| By event type (1 day) | < 500ms | < 5s |
| By correlation_id | < 100ms | < 1s |
| Entity state history | < 100ms | < 2s |
| Actor activity report (30 days) | < 1s | < 10s |
| Composite (indexed fields) | < 2s | < 30s |

### 5.3 Query Indexes

| Index | Fields | Type |
|-------|--------|------|
| PK | `(audit_id)` | Primary |
| Entity lookup | `(entity.type, entity.id, timestamp)` | B-tree |
| Actor lookup | `(actor.id, timestamp)` | B-tree |
| Time range | `(timestamp)` | B-tree (partitioned) |
| Event type | `(event_type, timestamp)` | B-tree |
| Correlation | `(correlation_id)` | Hash |
| Decision | `(decision.decision_id)` | Hash |
| Causation | `(causation_id, timestamp)` | B-tree |

---

## 6. Retention Policy

### 6.1 Retention by Privacy Level

| Privacy Level | Hot Store | Cold Store | Total Retention | Deletion |
|---------------|-----------|------------|-----------------|----------|
| `public` | 90 days | 7 years | 7 years | After 7 years + legal hold check |
| `low` | 90 days | 7 years | 7 years | After 7 years + legal hold check |
| `medium` | 90 days | 5 years | 5 years | After 5 years + legal hold check |
| `high` | 30 days | 3 years | 3 years | After 3 years + legal hold check |
| `critical` | 7 days | 1 year | 1 year | After 1 year + legal hold check |

### 6.2 Legal Hold

Records under active legal or compliance hold are protected:

```
legal_holds:
  { hold_id, entity_type, entity_id, event_ids[], reason, 
    initiated_by, initiated_at, expires_at, status }
```

When a hold is active:
- Affected records are excluded from all deletion operations.
- The hold is visible in query results (field `legal_hold: true`).
- Expired holds are reviewed before records become eligible for deletion.

### 6.3 Deletion Process

1. **Review:** Monthly automated scan identifies records past retention + no legal hold.
2. **Verify:** Audit administrator reviews the deletion candidates.
3. **Anonymize:** Rather than delete, PII fields are irreversibly anonymized (replaced with `[REDACTED]` + hash).
4. **Retain structure:** Entity relationships, state transitions, and decision data are preserved even after PII redaction.
5. **Log:** Every anonymization is logged as an audit event.

---

## 7. Audit Visibility Levels

### 7.1 Level Definitions

| Level | Code | Description | Who Can Query |
|-------|------|-------------|---------------|
| **Public** | `public` | Visible to all authenticated users | All authenticated roles |
| **Internal** | `internal` | Visible to system operators and authorized roles | Agent, Agence, Assistant, Vice-Master, Master |
| **Confidential** | `confidential` | Sensitive business data, need-to-know only | Vice-Master, Master, Audit System |
| **Restricted** | `restricted` | Maximum sensitivity, audit-only | Master only, Audit System with justification |

### 7.2 Visibility Mapping by Event Category

| Event Category | Default Visibility | Rationale |
|----------------|-------------------|-----------|
| State transitions | `public` | Operational transparency |
| Property events | `public` | Property data is inherently public |
| Lead events | `internal` | Lead data is commercially sensitive |
| Consent events | `confidential` | Legal sensitivity |
| Payment events | `confidential` | Financial data protection |
| Permission changes | `restricted` | Security critical |
| Data access | `restricted` | Privacy critical |
| Fraud detection | `restricted` | Investigation integrity |
| Relationship events | `confidential` | Privacy of personal connections |

### 7.3 Query Restrictions by Visibility

| Visibility | Demandeur | Propriétaire | Agent | Agence | Assistant | Vice-Master | Master | Audit System |
|------------|:---------:|:------------:|:-----:|:------:|:---------:|:-----------:|:-----:|:------------:|
| `public` | Own only | Own only | All | All | All | All | All | All |
| `internal` | No | No | Assigned | Org | All | All | All | All |
| `confidential` | No | No | No | No | No | All | All | All |
| `restricted` | No | No | No | No | No | No | All | With reason |

---

## 8. Privacy Protection in Audit Records

### 8.1 Data Masking Rules

Audit records automatically mask PII and sensitive fields based on the event's `privacy_level` and the querying actor's role.

| Field | public | low | medium | high | critical |
|-------|--------|-----|--------|------|----------|
| `actor.id` | Full | Full | Full | Full | Full |
| `actor.role` | Full | Full | Full | Full | Full |
| `actor.trust_level` | Full | Full | Full | Full | Full |
| `entity.id` | Full | Full | Full | Full | Full |
| `entity.type` | Full | Full | Full | Full | Full |
| `phone` in payload | Full | Mask: +237XXXXX* | Mask: +237XXXXX** | Redacted | Redacted |
| `email` in payload | Full | Full | Mask: a***@d*.com | Redacted | Redacted |
| `name` in payload | Full | Full | First name only | Redacted | Redacted |
| `address` in payload | Full | Full | City only | Redacted | Redacted |
| `id_document` | Full | Full | Redacted | Redacted | Redacted |
| `payment_details` | Full | Full | Amount only | Amount + date | Redacted |
| `ip_address` | Mask: 196.xxx.xxx.xxx | Mask: 196.xxx.xxx.xxx | Mask: 196.xxx.x**.xxx | Redacted | Redacted |
| `geo_location` | Full | Full | City only | Region only | Redacted |
| `coordinates` | Full | Full | City level (5km) | Region level (50km) | Redacted |

### 8.2 Masking Implementation

- **Masking is applied at query time** based on the querying actor's role and the record's `privacy.level`.
- The underlying audit store ALWAYS stores the full unmasked data.
- Masking logic is centralized in the audit query service and is NOT bypassable.
- Every masked query is logged in the `audit.query_log` for compliance monitoring.

### 8.3 Unmasking Authorization

Unmasking of `high` and `critical` records requires:

1. A formal request with justification (compliance, dispute resolution, legal requirement).
2. Approval by Vice-Master or Master role.
3. The unmasking session is itself audited with full detail.

---

## 9. Integration with NBA for Audit-Triggered Actions

### 9.1 Audit Events That Trigger NBA Recalculation

| Audit Event | NBA Effect |
|-------------|------------|
| `state.transitioned` | NBA recalculated for the entity |
| `SLA.breached` | NBA recalculated, escalation level checked |
| `action.failed` | NBA recalculated, alternative action sought |
| `consent.refused` | NBA recalculated, path blocked |
| `fraud.detected` | NBA overridden to security_review |
| `permission.changed` | NBA recalculated for all entities the actor can influence |
| `payment.failed` | NBA recalculated, retry logic triggered |
| `handover.requested` | NBA paused, human intervention awaited |

### 9.2 Audit-Triggered NBA Flow

```
audit.event ──► Audit System ──► Audit Event Bus
                                      │
                                   (async)
                                      ▼
                              NBA Engine: recalculation
                                      │
                                      ▼
                              NBA Trigger: new action planned
                                      │
                          ┌───────────┴───────────┐
                          ▼                       ▼
                   action.executed          SLA Monitor watches
                                              for completion
```

### 9.3 Compliance NBA

Certain audit events trigger compliance-related NBAs that are separate from business NBAs:

| Audit Pattern | Compliance NBA |
|---------------|----------------|
| N consent.refused in 1 hour from same user | `compliance.consent_fatigue_check` |
| N permission.changed for same actor in 1 day | `compliance.permission_audit` |
| N fraud.detected for same entity in 1 day | `compliance.account_review` |
| Data access by actor without prior relationship | `compliance.access_review` |
| Payment disputed > X amount | `compliance.payment_investigation` |

---

## 10. Audit Reporting Requirements

### 10.1 Standard Reports

| Report | Frequency | Audience | Content |
|--------|-----------|----------|---------|
| **Daily Activity Summary** | Daily | Operations | Event counts by type, top actors, SLA breaches, failed actions |
| **Weekly Compliance Report** | Weekly | Compliance team | Consent actions, permission changes, data access patterns, fraud alerts |
| **Monthly Audit Summary** | Monthly | Management | Trend analysis, top event producers, anomaly detection, retention status |
| **Quarterly Security Report** | Quarterly | Security team | Access patterns, permission drift, fraud trends, incident summary |
| **Annual Compliance Report** | Annual | Regulators | Full audit trail summary, data retention verification, consent compliance |
| **Entity History Report** | On-demand | Authorized roles | Complete state machine history for a specific entity |
| **Actor Activity Report** | On-demand | Authorized roles | Complete action trail for a specific actor |
| **Decision Analysis Report** | On-demand | Decision Engineering | Decision patterns, rule performance, conflict frequency, NBA completion rate |

### 10.2 Report Data Sources

| Report | Primary Source | Secondary Source |
|--------|---------------|------------------|
| Activity Summary | `audit_store` (hot, 90 days) | Event counts from cold store for trends |
| Compliance | `audit_store` (full, filtered by `audit_visibility >= confidential`) | Legal holds table |
| Security | `audit_store` (filtered by `event_type IN (fraud, access, permission)`) | Security engine alerts |
| Entity History | `audit_store` (filtered by `entity.id`) | State machine definitions |
| Decision Analysis | `audit_store` (filtered by `event_type = decision.made`) | Knowledge registry rule data |

### 10.3 Report Distribution

| Report | Channel | Format | Security |
|--------|---------|--------|----------|
| Daily Activity | Dashboard + Email | HTML / PDF | Internal only |
| Weekly Compliance | Email (encrypted) | PDF (password-protected) | Confidential |
| Monthly Audit | Admin Dashboard | Interactive + CSV export | Internal |
| Quarterly Security | Email (encrypted) + Meeting | PDF with executive summary | Restricted |
| Annual Compliance | Formal submission | PDF + raw data export | Restricted |
| On-demand reports | Dashboard download | CSV, JSON, PDF | Per user role |

---

## 11. Audit System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          AUDIT SYSTEM                               │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Audit Ingestion Layer                     │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │ Event Bus│→│ Schema   │→│ Enrich   │→│ Write    │   │   │
│  │  │ Consumer │  │ Validator│  │ (actor,  │  │ to Store │   │   │
│  │  │          │  │          │  │ context) │  │          │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └────────────────────────────┬────────────────────────────────┘   │
│                               │                                     │
│                               ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     Audit Store Layer                        │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │              Append-Only Audit Log                    │   │   │
│  │  │  (hash chain, immutable, partitioned by month)       │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │              Queryable Indexes                       │   │   │
│  │  │  (entity, actor, time, event_type, correlation)     │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │              Cold Storage (Parquet)                   │   │   │
│  │  │  (monthly partitions, compressed, immutable)         │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └────────────────────────────┬────────────────────────────────┘   │
│                               │                                     │
│                               ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Audit Query Layer                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │ Query    │→│ Privacy  │→│ Access   │→│ Result   │   │   │
│  │  │ Parser   │  │ Mask     │  │ Control  │  │ Formatter│   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └────────────────────────────┬────────────────────────────────┘   │
│                               │                                     │
│                               ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Audit Reporting Layer                     │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │ Standard │  │ Custom   │  │ NBA      │  │ Alert    │   │   │
│  │  │ Reports  │  │ Queries  │  │ Triggers │  │ Engine   │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 12. Error Handling

| Scenario | Behavior |
|----------|----------|
| Audit write failure | Buffer to local queue, retry with backoff. Main flow is NEVER blocked by audit. |
| Hash chain violation | CRITICAL alert to security team. System continues operating but audit integrity is suspect. |
| Query on corrupted partition | Return partial results with corruption warning. Admin alert. |
| Retention job failure | Alert operations. Manual review required before next run. |
| Privacy mask failure | Return unmasked result is FORBIDDEN. Return error instead. |
| Legal hold violation attempt | Block deletion, alert compliance team, log attempt. |

---

## 13. Heritage Gold CRM-004 Alignment

CRM-004 defines 13 event types that map to audit requirements as follows:

| CRM-004 Event | Must Be Audited | Audit Record Detail | Retention |
|---------------|:--------------:|-------------------|-----------|
| `message.received` | Yes | Minimal (actor, channel, timestamp) | 7 years |
| `intent.detected` | Yes | Standard (decision context, confidence) | 7 years |
| `user.created` | Yes | Full (registration data, channel, IP) | 7 years |
| `property.created` | Yes | Full (owner, property data, timestamp) | 7 years |
| `lead.created` | Yes | Standard (score, source, person) | 7 years |
| `match.generated` | Yes | Standard (match score, entities) | 5 years |
| `payment.success` | Yes | Full (amount, service, provider ref) | 7 years |
| `subscription.renewed` | Yes | Full (user, subscription, payment) | 5 years |
| `boost.applied` | Yes | Standard (property, boost type, payment) | 5 years |
| `access.granted` | Yes | Full (actor, resource, permission, grantor) | 7 years |
| `user.state_changed` | Yes | Standard (previous state, new state) | 7 years |
| `feedback.submitted` | Yes | Standard (entity, rating, feedback text) | 3 years |
| `fraud.detected` | Yes | Full (indicators, confidence, actions) | 7 years |

All 13 CRM-004 events are audited. Every state transition across all 21 workflows (STATE_MACHINE_CATALOG.md) produces an audit event through the `state.transitioned` event type, ensuring complete workflow audit coverage.

---

## 14. Audit Coverage Matrix by Workflow

| Machine | Entity | States | Every Transition Audited | Audit Event(s) |
|---------|--------|-------|:------------------------:|----------------|
| 01 Property | property | 13 | Yes | `state.transitioned` + property-specific audit events |
| 02 Dossier | dossier | 14 | Yes | `state.transitioned` + dossier-specific audit events |
| 03 Matching | match | 10 | Yes | `matching.*`, `state.transitioned` |
| 04 Contact | contact | 6 | Yes | `consent.*`, `relationship.*` |
| 05 Visit | visit | 9 | Yes | `visit.*`, `state.transitioned` |
| 06 Negotiation | negotiation | 8 | Yes | `negotiation.*`, `state.transitioned` |
| 07 Transaction | transaction | 10 | Yes | `transaction.*`, `payment.*` |
| 08 Payment | paid_service | 18 | Yes | `payment.*`, `state.transitioned` |
| 09 Incidents | incident | 8 | Yes | `incident.created`, `state.transitioned` |
| 10 Archive | archived_object | 4 | Yes | `state.transitioned` |
| 11 Mediation | mediation | 8 | Yes | `incident.*`, `state.transitioned` |
| 12 User | user | 7 | Yes | `user.created`, `role.changed`, `state.transitioned` |
| 13 Organization | organization | 8 | Yes | `state.transitioned`, `permission.changed` |
| 14 Agent Invitation | agent_invitation | 7 | Yes | `state.transitioned`, `user.created` |
| 15 Publication | publication | 11 | Yes | `state.transitioned` |
| 16 Redirection | redirection | 12 | Yes | `state.transitioned` |
| 17 Conversion | conversion | 12 | Yes | `state.transitioned`, `payment.success` |
| 18 CRM Pipeline | lead | 8 | Yes | `lead.*`, `state.transitioned` |
| 19 Agent Opt-In | agent_opt_in | 4 | Yes | `consent.*` |
| 20 Identity Resolution | identity_resolution | 5 | Yes | `identity.resolved` |
| 21 Cross-cutting | real_estate_project | 9 | Yes | Delegates to sub-workflows |

**Total: 21 machines, 175+ states, every single transition audited.**
