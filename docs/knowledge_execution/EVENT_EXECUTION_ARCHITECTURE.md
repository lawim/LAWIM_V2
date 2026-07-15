# Event Execution Architecture

**Domain:** Event Engine and Audit Infrastructure
**Version:** 1.0
**Status:** CANONICAL

---

## 1. Event Engine Overview

The Event Engine is the central nervous system of LAWIM. Every business action, state transition, decision, and system operation emits a structured event. Events flow through a publish–route–persist–notify bus and are consumed by audit, NBA, notification, and learning subsystems.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EVENT ENGINE                                │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     EVENT PRODUCERS                          │   │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │   │
│  │  │Decision│Conv. │ │Qualif│ │Search│ │Match │ │Geo   │ ... │   │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘    │   │
│  └─────────────────────────┬───────────────────────────────────┘   │
│                            │                                        │
│                            ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     EVENT BUS                                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │   │
│  │  │  Publish  │→│   Route  │→│  Persist │→│  Notify  │    │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │   │
│  └─────────────────────────┬───────────────────────────────────┘   │
│                            │                                        │
│                            ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    EVENT CONSUMERS                           │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │   │
│  │  │  Audit   │ │   NBA   │ │   Notif  │ │ Learning │  ...   │   │
│  │  │  System  │ │  Engine  │ │  System  │ │  Engine  │       │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Event Producers

Every LAWIM engine is an event producer. Engines emit events when they perform work, make decisions, detect state changes, or encounter errors.

| # | Engine | Events Emitted | Domain |
|---|--------|---------------|--------|
| 1 | **Decision Engine** | `decision.made`, `rule.conflict`, `confidence.low`, `fallback.activated` | Meta-orchestrator |
| 2 | **Conversation Engine** | `message.received`, `message.sent`, `intent.detected`, `fact.extracted`, `question.selected`, `response.received` | Conversation |
| 3 | **Qualification Engine** | `qualification.updated`, `readiness.changed`, `field.completed`, `critical.field.identified` | Qualification |
| 4 | **Search Engine** | `search.started`, `search.completed`, `search.expanded`, `result.selected` | Search |
| 5 | **Matching Engine** | `matching.started`, `matching.completed`, `match.generated`, `match.rejected`, `score.calculated` | Matching |
| 6 | **Geography Engine** | `geo.resolved`, `geo.proximity.calculated`, `geo.normalized` | Geography |
| 7 | **CRM Engine** | `lead.created`, `lead.scored`, `lead.classified`, `lead.routed`, `identity.resolved` | CRM |
| 8 | **Relationship Engine** | `relationship.created`, `relationship.expired`, `relationship.revoked`, `consent.requested`, `consent.granted`, `consent.refused` | Relationship |
| 9 | **Negotiation Engine** | `negotiation.started`, `negotiation.accepted`, `negotiation.rejected`, `proposal.created`, `price.updated` | Negotiation |
| 10 | **Language Engine** | `language.detected`, `text.normalized`, `translation.completed` | Language |
| 11 | **Workflow Engine** | `state.transitioned`, `action.planned`, `action.executed`, `action.failed`, `follow.up.scheduled`, `SLA.breached`, `incident.created` | Workflow |
| 12 | **Notification Engine** | `notification.sent`, `notification.delivered`, `notification.failed` | Notifications |
| 13 | **Payment Engine (Campay)** | `payment.requested`, `payment.success`, `payment.failed`, `payment.refunded`, `payment.disputed` | Payments |
| 14 | **Security Engine** | `access.granted`, `access.denied`, `permission.changed`, `fraud.detected`, `handover.requested` | Security |
| 15 | **Continuous Learning Engine** | `learning.signal`, `model.updated`, `confidence.recalibrated` | Learning |
| 16 | **Administration Engine** | `user.created`, `role.changed`, `feature.flag.changed`, `system.config.updated` | Admin |
| 17 | **Visit Engine** | `visit.scheduled`, `visit.completed`, `visit.cancelled`, `visit.rescheduled` | Visits |

---

## 3. Event Bus Architecture

The bus follows a **publish → route → persist → notify** pipeline.

### 3.1 Pipeline Stages

```
Producer ──► Publish ──► Route ──► Persist ──► Notify ──► Consumer
                │           │           │           │
                │           │           │           └── Async delivery to subscribers
                │           │           │
                │           │           └── Write to event_store (immutable)
                │           │
                │           └── Determine subscribers by event_type + routing rules
                │
                └── Accept event, validate schema, assign event_id + timestamp
```

### 3.2 Publish

**Schema validation:** Every event must conform to the canonical event schema before acceptance. Malformed events are rejected with a validation error.

**Idempotency key:** Producers supply an `idempotency_key` (typically event_id). The bus deduplicates by `(event_type, entity_type, entity_id, idempotency_key)` within a 5-minute window.

**Guarantees:** At-least-once delivery. Events are persisted before any consumer notification.

### 3.3 Route

The router determines which consumers receive the event based on:

- **Exact match:** `event_type` → subscriber list
- **Pattern match:** Wildcard subscriptions (e.g., `payment.*` subscribes to all payment events)
- **Entity filter:** Subscribe to events for a specific entity_id
- **Domain filter:** Subscribe to all events from a producer engine

**Routing table** is loaded at startup and updated via configuration events at runtime.

### 3.4 Persist

Events are written to the immutable `event_store` before consumer delivery. The persist step guarantees:

- **Ordering:** Events for the same `(entity_type, entity_id)` are stored in sequence with a monotonic sequence number.
- **Partitioning:** By `entity_type` for horizontal scaling.
- **Replication:** Synchronous replication to at least 2 nodes before acknowledgment.

### 3.5 Notify

Consumers are notified asynchronously via:

- **In-process channel:** For latency-sensitive consumers (NBA, SLA Monitor)
- **Message queue:** For durable, retry-capable delivery (notifications, webhooks)
- **Change data capture:** For analytics and reporting consumers

Consumer acknowledgment is expected. Unacknowledged events are retried with exponential backoff (3 retries), then sent to a dead-letter queue.

---

## 4. Event Schema

Every event in the system conforms to this canonical schema:

```json
{
  "event_id": "evt_<ulid>",
  "event_type": "state.transitioned",
  "entity_type": "dossier",
  "entity_id": "dossier_abc123",
  "actor_id": "agent_xyz789",
  "channel": "whatsapp",
  "timestamp": "2026-07-15T12:00:00.000Z",
  "correlation_id": "corr_<ulid>",
  "causation_id": "evt_<ulid>",
  "payload": {
    "from_state": "Matching",
    "to_state": "Présentation",
    "transition_event": "match_complete"
  },
  "knowledge_rules_used": ["MATCH-005", "MATCH-012", "QUAL-002"],
  "decision_id": "dec_<ulid>",
  "previous_state": "Matching",
  "new_state": "Présentation",
  "audit_visibility": "internal",
  "privacy_level": "confidential"
}
```

### Field Specifications

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `event_id` | `string (ULID)` | Yes | Globally unique event identifier, sortable by time |
| `event_type` | `string` | Yes | Canonical event type name (see EVENT_CATALOG.md) |
| `entity_type` | `string` | Yes | Type of business entity (dossier, property, user, lead, etc.) |
| `entity_id` | `string` | Yes | Unique identifier of the entity |
| `actor_id` | `string` | Yes | Identifier of the actor who caused the event (user_id, system, rule_id) |
| `channel` | `string` | No | Channel through which the event originated (whatsapp, telegram, api, system, dashboard) |
| `timestamp` | `string (ISO 8601)` | Yes | Time the event was produced (UTC) |
| `correlation_id` | `string (ULID)` | Yes | Ties together all events belonging to a single business transaction |
| `causation_id` | `string (ULID)` | Yes | Identifies the direct cause event (for causation chain) |
| `payload` | `object` | Yes | Type-specific business data (minimal, no PII in top-level payload) |
| `knowledge_rules_used` | `string[]` | No | List of rule IDs that were evaluated/triggered for this event |
| `decision_id` | `string` | No | Links to the decision that produced this event |
| `previous_state` | `string` | No | Entity state before the event (for state transitions) |
| `new_state` | `string` | No | Entity state after the event (for state transitions) |
| `audit_visibility` | `enum` | Yes | Visibility level for audit: `public`, `internal`, `confidential`, `restricted` |
| `privacy_level` | `enum` | Yes | Data sensitivity: `public`, `low`, `medium`, `high`, `critical` |

---

## 5. Correlation ID Propagation

### 5.1 Purpose

The `correlation_id` ties all events belonging to a single **business transaction** into a single trace. This enables end-to-end visibility of a user interaction, a matching cycle, or a negotiation flow.

### 5.2 Generation and Propagation Rules

| Rule | Description |
|------|-------------|
| **Creation** | A new `correlation_id` is generated when the system receives an external stimulus (message, webhook, API call) that is not itself an event. |
| **Propagation** | Every event emitted during processing of that stimulus MUST carry the same `correlation_id`. |
| **Downstream calls** | If processing triggers a new external interaction (API call, message send), the `correlation_id` is included in the outbound request headers. |
| **Sub-events** | If the processing spawns new asynchronous work (e.g., scheduled follow-up), the new work receives a new `correlation_id`, with the original `correlation_id` recorded as `parent_correlation_id`. |
| **Boundary** | A `correlation_id` never crosses between independent business transactions. |

### 5.3 Example Trace

```
message.received          (corr_A, causation: null)
    └── intent.detected   (corr_A, causation: evt_msg)
        └── lead.created  (corr_A, causation: evt_intent)
            └── search.started       (corr_A, causation: evt_lead)
                └── search.completed  (corr_A, causation: evt_search)
                    └── match.generated (corr_A, causation: evt_search_complete)
```

---

## 6. Causation Chain Tracking

### 6.1 Purpose

While `correlation_id` provides horizontal traceability across parallel events, the `causation_id` provides a vertical chain showing exactly which event caused which. Every event (except root events) has a `causation_id` pointing to its immediate parent.

### 6.2 Rules

| Rule | Description |
|------|-------------|
| **Root events** | Events that are direct responses to external stimuli have `causation_id = null`. |
| **Chain events** | Every event produced as a direct consequence of another event MUST set `causation_id` to the parent `event_id`. |
| **Fan-out** | If one event causes N child events, each child carries the same `causation_id`. |
| **Fan-in** | If a processing step awaits multiple prior events, the emitted event's `causation_id` points to the latest trigger; the `payload` MAY list all contributing event_ids. |
| **Integrity** | Causation chains MUST be acyclic. Cycles are detected and rejected by the Event Bus. |

### 6.3 Causation Chain Example

```
evt_001: message.received       (causation_id: null)
evt_002: intent.detected        (causation_id: evt_001)
evt_003: fact.extracted         (causation_id: evt_002)
evt_004: lead.created           (causation_id: evt_003)
evt_005: search.started         (causation_id: evt_004)
evt_006: search.completed       (causation_id: evt_005)
evt_007: match.generated        (causation_id: evt_006)
```

Full chain query: `SELECT * FROM events WHERE correlation_id = 'corr_A' ORDER BY timestamp` returns all 7 events in order.

---

## 7. Event Persistence and Retention

### 7.1 Storage Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        EVENT STORE                                  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     Write-Ahead Log (WAL)                     │   │
│  │  Append-only, immutable, ordered by (entity_type, seq_no)    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                  │                                   │
│                                  ▼                                   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                  Queryable Index                              │   │
│  │  event_id │ event_type │ entity_type │ entity_id │ actor_id  │   │
│  │  correlation_id │ timestamp │ audit_visibility │ privacy    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                  │                                   │
│                                  ▼                                   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                  Cold Storage (Parquet/AVRO)                  │   │
│  │  Monthly partitions, compressed, immutable                   │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 Retention Periods

| Privacy Level | Hot Store (Queryable) | Cold Store (Analytics) | Total Retention |
|---------------|----------------------|------------------------|-----------------|
| `public` | 90 days | 7 years | 7 years |
| `low` | 90 days | 7 years | 7 years |
| `medium` | 90 days | 5 years | 5 years |
| `high` | 30 days | 3 years | 3 years |
| `critical` | 7 days | 1 year | 1 year |

- **Hot store:** Primary database (PostgreSQL/TimescaleDB) for operational queries.
- **Cold store:** Object storage (S3-compatible) with Parquet format for analytics, audit reporting, and compliance.
- **Audit override:** Events with `audit_visibility = public` or `internal` have a minimum retention of 7 years regardless of privacy level.
- **Legal hold:** Events under active legal or compliance hold are excluded from deletion. The hold is managed via the `event_store.legal_holds` table.

> **ARCHITECTURE_DECISION:** Retention durations (7d public, 30d internal, 1y confidential, 7y restricted) are architecture-defined defaults. Actual retention must comply with applicable data protection regulations.

### 7.3 Immutability Guarantees

- Events are **append-only**. No event is ever modified, deleted, or overwritten.
- The WAL uses a hash chain: each event record includes the hash of the previous event in the partition, enabling tamper detection.
- Deletion policy is implemented via **exclusion from query results**, not physical deletion. Physical deletion only occurs after the retention period expires AND a verification pass confirms no legal hold applies.

---

## 8. Event Consumption

### 8.1 Consumer Map

| Consumer | Events Consumed | Delivery Mode | SLA |
|----------|----------------|---------------|-----|
| **Audit System** | ALL events | Async (batch) | < 5s to persist |
| **NBA Engine** | `state.transitioned`, `action.executed`, `SLA.breached`, `follow.up.scheduled`, `decision.made` | Sync (in-process) | < 100ms |
| **Notification System** | `notification.sent`, `action.failed`, `SLA.breached`, `handover.requested`, `incident.created` | Async (queue) | < 30s |
| **Continuous Learning** | `action.executed`, `action.failed`, `match.rejected`, `consent.refused`, `notification.failed`, `payment.failed` | Async (batch) | < 5min |
| **SLA Monitor** | `state.transitioned`, `SLA.breached` | Sync (in-process) | < 50ms |
| **Dashboard/Reporting** | ALL events (aggregated) | Async (CDC) | < 1min |
| **Security Engine** | `access.denied`, `fraud.detected`, `permission.changed`, `handover.requested` | Sync (alert) | < 1s |

### 8.2 NBA Engine Consumption

The NBA Engine subscribes to state transition events and SLA breach events to recalculate the Next Best Action for the affected entity.

```
state.transitioned ──► NBA Engine ──► recalculate NBA ──► nba.recalculated
                            ▲
SLA.breached ───────────────┘
```

The NBA Engine also consumes `action.executed` to verify that the suggested NBA was actually performed, and `action.failed` to re-evaluate if the NBA should change.

### 8.3 Audit System Consumption

The Audit System consumes **every** event. It maintains its own immutable store separate from the Event Store, optimized for compliance query patterns:

- **Append-only log:** All events in chronological order.
- **Entity journal:** All events grouped by entity_id for per-entity audit trail.
- **Actor journal:** All events grouped by actor_id for per-actor activity trail.

Audit events are enriched with:
- **Geo-location** of the actor at event time (if available)
- **Session ID** from the authentication system
- **IP address** and user agent
- **Data snapshot** of the entity before and after the event

---

## 9. Privacy and Access Control for Events

### 9.1 Privacy Level Definitions

| Level | Definition | Examples | Masking Required |
|-------|------------|----------|-----------------|
| `public` | No sensitive data, visible to all authenticated users | Property published, visit scheduled | No |
| `low` | Low sensitivity, visible to entity participants | Lead scored, match generated | No |
| `medium` | Moderately sensitive, visible to assigned roles | Qualification updated, negotiation started | Partial (phone, email masked) |
| `high` | Highly sensitive, need-to-know only | Payment success, identity resolved | Full PII masking |
| `critical` | Maximum sensitivity, audit-only, restricted access | Consent granted, fraud detected, permission changed | Full masking, access logged |

### 9.2 Access Control Rules

| Role | public | low | medium | high | critical |
|------|--------|-----|--------|------|----------|
| Demandeur | Read own | Read own | Read own | No | No |
| Propriétaire | Read own | Read own | Read own | No | No |
| Agent | Read | Read+assign | Read assigned | No | No |
| Agence | Read | Read | Read org | Read org | No |
| Assistant | Read | Read | Read | Read | No |
| Vice-Master | Read | Read | Read | Read | Read |
| Master | Read | Read | Read | Read | Read |
| Audit System | Full | Full | Full | Full | Full |

### 9.3 Payload Masking

Events with `privacy_level >= medium` MUST have sensitive fields masked in the payload before delivery to consumers that do not have explicit access.

| Field | Medium | High | Critical |
|-------|--------|------|----------|
| `phone` | Mask last 4 digits | Mask all but last 2 | Fully masked |
| `email` | Mask domain after @ | Fully masked | Fully masked |
| `name` | Full | First name only | First initial only |
| `address` | City only | City only | Region only |
| `id_document` | Not included | Not included | Not included |
| `payment_details` | Amount only | Amount only | Not included |
| `exact_location` | Neighborhood | City | Region |

### 9.4 Audit Trail of Access

Every access to a `high` or `critical` event is itself recorded as an audit event:

```
audit.event_access {
  event_id: "evt_accessed",
  accessed_event_id: "evt_original",
  actor_id: "agent_xyz",
  access_time: "...",
  access_reason: "compliance_query",
  granted_by: "system_policy"
}
```

---

## 10. Event Volume Estimation and Scaling

### 10.1 Volume Estimates

| Event Category | Events/Day (Est.) | Peak EPS | Growth Rate |
|----------------|-------------------|----------|-------------|
| Conversation | 50,000 | 50 | 50%/yr |
| Qualification | 10,000 | 20 | 50%/yr |
| Search & Matching | 30,000 | 40 | 60%/yr |
| State Transitions | 100,000 | 80 | 40%/yr |
| Payments | 5,000 | 10 | 100%/yr |
| SLA Monitor | 500,000 | 200 | 30%/yr |
| System/Admin | 20,000 | 30 | 20%/yr |
| **Total** | **~715,000** | **~430** | **40%/yr** |

### 10.2 Scaling Strategy

| Concern | Approach |
|---------|----------|
| **Throughput** | Partition event store by `entity_type`. Each partition is an independent write target. |
| **Storage** | Hot: TimescaleDB hypertable partitioned by day. Cold: Parquet files in S3, partitioned by month. |
| **Read capacity** | Queryable index uses a separate read replica. Full-text search on payload via elasticsearch for audit queries. |
| **Consumer backpressure** | Each consumer has a dedicated queue. If a consumer falls behind, events remain in the queue (persistent, not lost). |
| **Dead-letter queue** | Events that cannot be delivered after 3 retries go to DLQ for manual inspection. DLQ alert triggers within 5 minutes. |
| **Burst handling** | Write buffer with configurable flush interval (default 100ms or 1000 events, whichever first). |
| **Multi-region** | Active-active per region. Events carry a `region` tag for origin tracking. Cross-region replication via CDC. |

### 10.3 Capacity Dimensions

| Dimension | Year 1 | Year 2 | Year 3 |
|-----------|--------|--------|--------|
| Daily events | 715K | 1M | 1.4M |
| Monthly events | 21M | 30M | 42M |
| Hot storage | 200 GB | 300 GB | 450 GB |
| Cold storage | 2 TB | 3 TB | 4.5 TB |
| Peak EPS | 430 | 600 | 850 |
| Index size | 50 GB | 75 GB | 110 GB |

---

## 11. Event Schema Evolution

### 11.1 Backward Compatibility

- New fields are always optional (nullable).
- Existing fields never change type or semantics.
- Deprecated fields are marked with a `_deprecated` suffix and removed after two release cycles.

### 11.2 Schema Registry

Every event_type has a registered schema in the Schema Registry. Validation occurs at publish time:

```
publish(event) → SchemaRegistry.validate(event_type, event) → PASS/FAIL
```

Schemas are versioned (`event_schema_version` field in payload). Consumers declare which schema version they support.

---

## 12. Error Handling

| Scenario | Behavior |
|----------|----------|
| Schema validation failure | Event rejected, producer gets 400 error |
| Persistence failure | Event is buffered, retried with backoff (max 3) |
| Consumer failure | Event stays in queue, retried with backoff (max 3), then DLQ |
| Duplicate event | Idempotency key check — silently acknowledged |
| Corrupted event | Validation checksum fails → dead-letter queue + admin alert |
| Partition unavailable | Writes routed to replica, rebalanced when partition recovers |
