# EVENT & AUDIT EXTENSION MODEL

**Document ID:** LAWIM-H16-EVT-V1
**Status:** CANONICAL DOMAIN EXTENSION
**Date:** 2026-07-15
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §16 (Events/Observability)
**Source Crosswalks:** required_extensions.json (event_audit), Event model (Gold)

---

## Table of Contents

1. [Enriched Event Entity Model](#1-enriched-event-entity-model)
2. [Typed Event Catalog](#2-typed-event-catalog)
3. [Audit Trail Requirements](#3-audit-trail-requirements)
4. [Retention Policy Per Event Type](#4-retention-policy-per-event-type)
5. [Privacy Levels Per Event Type](#5-privacy-levels-per-event-type)
6. [Event Consumers](#6-event-consumers)
7. [Correlation ID for Event Chains](#7-correlation-id-for-event-chains)
8. [Event Sourcing Considerations](#8-event-sourcing-considerations)
9. [Complete Extension Mapping Table](#9-complete-extension-mapping-table)

---

## 1. Enriched Event Entity Model

### 1.1 Core Event Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `event_type` | String | Typed event kind from catalog (e.g., `user.created`, `property.published`) |
| `entity_type` | String | Type of entity that generated the event |
| `entity_id` | UUID | Entity ID |
| `actor_id` | UUID? | User who triggered the event (null for system events) |
| `previous_state` | String? | State before transition (for state transition events) |
| `new_state` | String? | State after transition (for state transition events) |
| `transition` | String? | Transition name (e.g., `publish`, `validate`, `archive`) |
| `source` | Enum | `system \| user \| webhook \| cron \| integration` |
| `correlation_id` | UUID? | Links events in the same chain/transaction |
| `severity` | Enum | `debug \| info \| warning \| error \| critical` |
| `privacy_level` | Enum | `public \| internal \| restricted \| confidential` |
| `payload` | JSON | Event payload (typed per event_type) |
| `metadata` | JSON? | Additional context (request_id, ip_address, user_agent, geo) |
| `retention_days` | Int | Days to retain this event before archival/purge |
| `created_at` | DateTime | Event timestamp |

### 1.2 Event Entity Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| Any entity | N:1 | Events reference any entity by entity_type + entity_id |
| User (actor) | N:1 | User who triggered the event |
| Event (parent) | N:1 | Parent event in a chain (linked via correlation_id) |

---

## 2. Typed Event Catalog

### 2.1 User Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `user.created` | User registration completes | `{user_id, email, signup_channel, referral_code?}` | info | internal |
| `user.updated` | Profile field changed | `{user_id, changed_fields, previous_values, new_values}` | info | internal |
| `user.deleted` | Account deletion | `{user_id, deletion_reason, account_age_days}` | warning | confidential |
| `user.login` | Successful authentication | `{user_id, ip_address, device_fingerprint, auth_method}` | info | internal |
| `user.logout` | Session termination | `{user_id, session_duration_seconds}` | debug | internal |
| `user.verified` | Identity verification completed | `{user_id, verification_method, verified_at}` | info | internal |
| `user.merged` | Duplicate accounts merged | `{target_user_id, source_user_id, merged_fields}` | warning | confidential |
| `user.gdpr_deletion_requested` | GDPR data deletion request | `{user_id, request_id, scope}` | critical | confidential |
| `user.password_changed` | Password reset or change | `{user_id, method (reset\|change)}` | warning | internal |
| `user.account_suspended` | Account suspended | `{user_id, reason, suspended_by, duration}` | warning | restricted |
| `user.account_reactivated` | Suspension lifted | `{user_id, reactivated_by}` | info | restricted |

### 2.2 Role/Trust Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `user.trust_level_changed` | Trust score recalculated | `{user_id, previous_level, new_level, reason}` | info | internal |
| `user.badge_awarded` | Badge earned | `{user_id, badge_type, badge_id, awarded_at}` | info | public |
| `user.role_changed` | Platform role changed | `{user_id, previous_role, new_role, changed_by}` | warning | restricted |
| `user.agency_role_changed` | Agency membership role changed | `{user_id, organization_id, previous_agency_role, new_agency_role, changed_by}` | info | internal |
| `user.permissions_updated` | Permission set modified | `{user_id, added_permissions, removed_permissions, changed_by}` | warning | restricted |

### 2.3 Property Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `property.created` | New property listing created | `{property_id, owner_id, property_type, city}` | info | internal |
| `property.updated` | Property fields changed | `{property_id, changed_fields, previous_values, new_values}` | info | internal |
| `property.published` | Property goes live | `{property_id, published_at, visibility}` | info | public |
| `property.archived` | Property taken offline | `{property_id, archive_reason}` | info | internal |
| `property.verified` | Property verification completed | `{property_id, verification_status, verified_by}` | info | public |
| `property.boosted` | Property promoted in search | `{property_id, boost_type, boost_expires_at}` | info | internal |
| `property.status_changed` | State machine transition | `{property_id, previous_status, new_status, transition}` | info | internal |
| `property.media_added` | Photo/video uploaded | `{property_id, media_type, media_count}` | debug | internal |
| `property.media_removed` | Media deleted | `{property_id, media_type, reason}` | debug | internal |
| `property.claim_requested` | Ownership claim submitted | `{property_id, claimant_id, evidence_document_ids}` | warning | restricted |
| `property.claim_resolved` | Claim approved or rejected | `{property_id, claimant_id, resolution, resolved_by}` | info | restricted |

### 2.4 Project/Dossier Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `project.created` | New project created | `{project_id, creator_id, project_type, intent_id?}` | info | internal |
| `project.matching_started` | Matching engine initiated | `{project_id, match_criteria}` | info | internal |
| `project.match_found` | Match discovered by engine | `{project_id, match_id, score}` | info | internal |
| `project.double_consent_updated` | Both parties consented | `{project_id, demandeur_consented, holder_consented}` | info | internal |
| `project.rematched` | Project re-entered matching | `{project_id, previous_match_id, reason}` | info | internal |
| `project.qualification_step_completed` | Qualification stage passed | `{project_id, step_name, completed_by}` | info | internal |
| `project.paused` | Project paused | `{project_id, reason, paused_by}` | info | internal |
| `project.resumed` | Project resumed | `{project_id, resumed_by}` | info | internal |
| `project.archived` | Project archived | `{project_id, reason}` | info | internal |

### 2.5 Matching Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `match.created` | Match record created | `{match_id, project_id, property_id, algorithm_version}` | info | internal |
| `match.score_calculated` | Match score computed | `{match_id, score, score_factors, confidence}` | info | internal |
| `match.proposed` | Match proposed to parties | `{match_id, proposed_to_demandeur_at, proposed_to_holder_at}` | info | internal |
| `match.accepted` | Party accepted match | `{match_id, accepted_by (demandeur\|holder), accepted_at}` | info | internal |
| `match.rejected` | Party rejected match | `{match_id, rejected_by, reason}` | info | internal |
| `match.expired` | Match proposal timed out | `{match_id, expired_at, notification_sent}` | info | internal |
| `match.rematched` | Match replaced by new match | `{match_id, new_match_id, reason}` | info | internal |

### 2.6 Visit Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `visit.requested` | Visit scheduled | `{visit_id, project_id, property_id, requested_by, requested_date}` | info | internal |
| `visit.confirmed` | Visit confirmed by both parties | `{visit_id, confirmed_at, confirmed_by}` | info | internal |
| `visit.rescheduled` | Visit date/time changed | `{visit_id, previous_date, new_date, initiator}` | info | internal |
| `visit.cancelled` | Visit cancelled | `{visit_id, reason, cancelled_by}` | info | internal |
| `visit.completed` | Visit occurred | `{visit_id, completed_at, duration_minutes}` | info | internal |
| `visit.absence_reported` | Party did not show | `{visit_id, absent_party (demandeur\|holder\|both)}` | warning | internal |
| `visit.satisfaction_recorded` | Post-visit rating | `{visit_id, rating, feedback}` | info | internal |

### 2.7 Negotiation Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `negotiation.started` | Negotiation initiated | `{negotiation_id, project_id, initiator_id}` | info | internal |
| `negotiation.offer_made` | Offer submitted | `{negotiation_id, offer_id, offer_amount, offer_terms, offered_by}` | info | restricted |
| `negotiation.counter_offer` | Counter-offer submitted | `{negotiation_id, offer_id, counter_amount, counter_terms, offered_by}` | info | restricted |
| `negotiation.accepted` | Offer accepted | `{negotiation_id, offer_id, accepted_by}` | info | internal |
| `negotiation.rejected` | Offer rejected | `{negotiation_id, offer_id, reason}` | info | internal |
| `negotiation.silence_reminder` | No response within SLA | `{negotiation_id, silence_duration_hours, last_action_at}` | warning | internal |
| `negotiation.failed` | Negotiation terminated without agreement | `{negotiation_id, reason, duration_days, offer_count}` | info | internal |

### 2.8 Transaction Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `transaction.created` | Transaction record created | `{transaction_id, project_id, property_id, transaction_type, amount}` | info | restricted |
| `transaction.documents_submitted` | Required documents uploaded | `{transaction_id, document_type, document_id, submitted_by}` | info | restricted |
| `transaction.payment_milestone` | Payment milestone reached | `{transaction_id, milestone_name, percentage, amount}` | info | restricted |
| `transaction.signed` | Contract signed | `{transaction_id, signed_by_party, signing_method}` | info | restricted |
| `transaction.completed` | Transaction closed | `{transaction_id, completed_at, final_amount}` | info | internal |
| `transaction.failed` | Transaction aborted | `{transaction_id, reason, stage}` | warning | restricted |
| `transaction.disputed` | Transaction disputed | `{transaction_id, disputing_party, reason}` | warning | restricted |
| `transaction.dispute_resolved` | Dispute resolved | `{transaction_id, resolution, resolved_by}` | info | restricted |

### 2.9 Payment Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `payment.created` | Payment record created | `{payment_id, service_order_id, amount, currency, payment_method}` | info | restricted |
| `payment.initiated` | Payment sent to gateway | `{payment_id, gateway, gateway_transaction_id}` | info | restricted |
| `payment.confirmed` | Payment successful | `{payment_id, gateway_confirmations, fee_amount}` | info | internal |
| `payment.failed` | Payment declined/error | `{payment_id, gateway_error_code, reason}` | warning | restricted |
| `payment.refunded` | Payment reversed | `{payment_id, refund_amount, reason, refunded_by}` | warning | restricted |
| `payment.disputed` | Payment disputed by user | `{payment_id, dispute_reason, evidence_provided}` | warning | restricted |
| `payment.retried` | Failed payment retry attempt | `{payment_id, retry_count, gateway}` | info | restricted |

### 2.10 CRM Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `lead.created` | Lead record created | `{lead_id, source_channel, lead_type, base_score}` | info | internal |
| `lead.scored` | Lead score computed | `{lead_id, final_score, total_boost, total_penalty}` | info | internal |
| `lead.classified` | Lead class assigned | `{lead_id, classification, sla_priority, sla_deadline}` | info | internal |
| `lead.routed` | Lead assigned to agent | `{lead_id, agent_id, routing_method}` | info | internal |
| `lead.converted` | Lead converted to project | `{lead_id, project_id}` | info | internal |
| `lead.fraud_flagged` | Fraud detected | `{lead_id, layers_triggered, action_taken}` | warning | restricted |
| `lead.sla_breached` | SLA deadline missed | `{lead_id, sla_priority, sla_deadline, assigned_agent_id}` | warning | internal |

### 2.11 Organization Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `org.created` | Organization registered | `{org_id, name, org_type, created_by}` | info | public |
| `org.validated` | Organization verified | `{org_id, validated_by, validation_document}` | info | internal |
| `org.member_added` | User joined organization | `{org_id, user_id, role, invited_by}` | info | internal |
| `org.member_removed` | User removed from organization | `{org_id, user_id, reason, removed_by}` | warning | internal |
| `org.suspended` | Organization suspended | `{org_id, reason, suspended_by}` | critical | restricted |
| `org.dissolved` | Organization dissolved | `{org_id, reason, assets_transferred_to}` | critical | public |
| `org.settings_updated` | Organization configuration changed | `{org_id, changed_settings, changed_by}` | info | internal |

### 2.12 Approval Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `approval.requested` | Approval workflow initiated | `{approval_id, entity_type, entity_id, requested_by, approval_type}` | info | internal |
| `approval.approved` | Request approved | `{approval_id, approved_by, approved_at, comments}` | info | internal |
| `approval.rejected` | Request rejected | `{approval_id, rejected_by, reason}` | info | internal |
| `approval.escalated` | Request escalated to higher authority | `{approval_id, escalated_by, escalated_to, reason}` | warning | internal |
| `approval.expired` | Approval request timed out | `{approval_id, expiry_reason}` | info | internal |

### 2.13 System Events

| Event Type | Trigger | Payload Schema | Severity | Privacy |
|-----------|---------|---------------|----------|---------|
| `system.sla_breach_detected` | Cron detects SLA breach | `{entity_type, entity_id, sla_priority, deadline}` | warning | internal |
| `system.nba_recalculated` | NBA scores recomputed | `{batch_id, properties_recalculated, duration_ms}` | debug | internal |
| `system.cron_executed` | Scheduled job ran | `{job_name, started_at, completed_at, records_processed, success}` | debug | internal |
| `system.error` | Application error | `{error_code, service, message, stack_trace?}` | error | internal |
| `system.warning` | Non-critical anomaly | `{warning_code, service, message}` | warning | internal |
| `system.database_migration` | Schema migration executed | `{migration_name, direction (up\|down), duration_ms}` | info | internal |
| `system.config_changed` | Runtime configuration updated | `{config_key, previous_value, new_value, changed_by}` | warning | internal |
| `system.integration_health` | External integration status | `{integration_name, status (up\|down\|degraded), latency_ms, last_success_at}` | warning | internal |

---

## 3. Audit Trail Requirements

### 3.1 Mandatory Audit Events

All state transitions across every domain MUST generate an audit event with:

- `event_type`: `{entity_type}.status_changed` or specific transition event
- `entity_type` + `entity_id`: identifies the entity
- `previous_state`: state before transition
- `new_state`: state after transition
- `transition`: name of the transition (e.g., `publish`, `validate`, `archive`)
- `actor_id`: who performed it
- `correlation_id`: chain identifier if part of a multi-step workflow
- `created_at`: when it happened

### 3.2 State Transition Matrix

| Entity | State Machine | Transition Events | Audit Granularity |
|--------|--------------|-------------------|-------------------|
| Property | `draft → normalization → classification → validation → published → matching → archived` | `property.status_changed` with transition name | Every status change |
| Project | `draft → qualification → matching → presentation → mise_en_relation → negotiation → closure → archive` | `project.status_changed` or `project.*` specific | Every status change |
| Visit | `requested → confirmed → completed \| cancelled \| rescheduled \| absence_reported` | `visit.*` specific events | Every status change |
| Negotiation | `started → offer_made → counter_offer → accepted \| rejected \| failed` | `negotiation.*` specific | Every offer/response |
| Transaction | `created → documents_submitted → payment_milestones → signed → completed \| failed` | `transaction.*` specific | Every milestone |
| Lead | `incoming → normalized → extracted → intent_detected → enriched → scored → classified → routed` | `lead.*` specific | Every pipeline stage change |
| User | `active → suspended → active \| deactivated → deleted` | `user.account_suspended`, `user.deleted` | Every status change |
| Organization | `active → suspended → dissolved` | `org.*` specific | Every status change |

### 3.3 Audit Event Naming Convention

```
{entity_type}.{action}
  e.g., property.published, user.role_changed, match.accepted
```

State transition events use the pattern:
```
{entity_type}.status_changed
  payload: { previous_status, new_status, transition }
```

### 3.4 Audit Trail Integrity

| Requirement | Implementation |
|-------------|----------------|
| Immutability | Events are append-only; no UPDATE or DELETE on events |
| Ordering | `created_at` + sequence_number for same-timestamp events |
| Non-repudiation | `actor_id` recorded on all user-initiated events |
| Completeness | Every state transition fires exactly one audit event |
| Traceability | `correlation_id` links events across entities in a workflow |

---

## 4. Retention Policy Per Event Type

### 4.1 Retention Tiers

| Tier | Duration | Storage | Applies To |
|------|----------|---------|------------|
| **Real-time** | 7 days | Hot (primary DB) | `debug` severity events |
| **Short-term** | 30 days | Hot (primary DB) | `info` severity events (most events) |
| **Medium-term** | 90 days | Warm (primary DB + index) | `warning` severity events |
| **Long-term** | 365 days | Cold (archive table / object store) | `error` + `critical` severity events |
| **Compliance** | 5 years | Cold (encrypted archive) | GDPR deletion requests, financial transactions, legal holds |

### 4.2 Retention by Event Category

| Event Category | Default Retention | Archive After | Purge After | Rationale |
|---------------|-------------------|---------------|-------------|-----------|
| User Events | 365 days | 365 days | 5 years | Account lifecycle, GDPR compliance |
| Role/Trust Events | 365 days | 365 days | 5 years | Audit trail for permission changes |
| Property Events | 90 days | 90 days | 365 days | Property lifecycle tracking |
| Project/Dossier Events | 90 days | 90 days | 365 days | Project workflow audit |
| Matching Events | 90 days | 90 days | 365 days | Matching algorithm traceability |
| Visit Events | 90 days | 90 days | 365 days | Visit history |
| Negotiation Events | 365 days | 365 days | 5 years | Commercial record |
| Transaction Events | 365 days | 365 days | 5 years | Financial/legal record |
| Payment Events | 365 days | 365 days | 5 years | Financial audit trail |
| CRM Events | 90 days | 90 days | 365 days | CRM pipeline tracking |
| Organization Events | 365 days | 365 days | 5 years | Org lifecycle, compliance |
| Approval Events | 365 days | 365 days | 5 years | Authorization trail |
| System Events | 30 days | 30 days | 90 days | Operational monitoring |

### 4.3 Archival Strategy

| Tier | Storage | Access Pattern | Indexing |
|------|---------|---------------|----------|
| Hot (0-90d) | PostgreSQL events table | Real-time query, dashboard, alerting | entity_type + entity_id, created_at, correlation_id |
| Warm (91-365d) | PostgreSQL + TimescaleDB (if available) | Reporting, analytics, audit lookup | entity_type + entity_id, created_at |
| Cold (1-5y) | Object store (S3/MinIO) in Parquet/JSON | Compliance, legal hold, data export | Partitioned by year/month, indexed by event_type |

### 4.4 Purge Criteria

Events are purged when:
- Retention period expires AND no legal hold is active AND no open investigation references the entity
- GDPR deletion request is fulfilled (user events only, anonymized before purge)
- System events with `debug` severity exceed 7 days

---

## 5. Privacy Levels Per Event Type

### 5.1 Privacy Level Definitions

| Level | Visibility | Example | Access Control |
|-------|-----------|---------|----------------|
| **public** | Visible to all authenticated users | Property published, badge awarded, org created | No restrictions |
| **internal** | Visible within the platform (staff/system) | User login, visit requested, match scored | Authenticated users with "audit:read:internal" permission |
| **restricted** | Visible to involved parties + admin | Offer amount, payment amount, transaction details | Involved users + admin/manager roles |
| **confidential** | Visible to admin/system only | GDPR request, account suspension details, fraud flags | Admin only + audit log access control |

### 5.2 Privacy by Event Category

| Event Category | Default Privacy Level | Exceptions |
|---------------|----------------------|------------|
| User Events | `internal` | `user.deleted` → confidential; `user.gdpr_deletion_requested` → confidential; `user.account_suspended` → restricted |
| Role/Trust Events | `internal` | `user.badge_awarded` → public; `user.role_changed` → restricted; `user.permissions_updated` → restricted |
| Property Events | `internal` | `property.published` → public; `property.verified` → public; `property.claim_*` → restricted |
| Project/Dossier Events | `internal` | All default internal |
| Matching Events | `internal` | All default internal |
| Visit Events | `internal` | All default internal |
| Negotiation Events | `restricted` | `negotiation.offer_made`, `negotiation.counter_offer` contain financial data |
| Transaction Events | `restricted` | All restricted (financial/legal data) |
| Payment Events | `restricted` | All restricted (financial data) |
| CRM Events | `internal` | `lead.fraud_flagged` → restricted |
| Organization Events | `internal` | `org.created` → public; `org.dissolved` → public; `org.suspended` → restricted |
| Approval Events | `internal` | All default internal |
| System Events | `internal` | All default internal |

### 5.3 Privacy Enforcement

| Mechanism | Description |
|-----------|-------------|
| API filter | Events API filters payload by privacy_level + user permission |
| Payload masking | Confidential events omit sensitive payload fields in non-admin responses |
| Audit log access | `audit:read:{privacy_level}` permission required to query events |
| Data export | GDPR export excludes restricted/confidential events involving other users |

---

## 6. Event Consumers

### 6.1 Consumer Matrix

| Event Category | Consumers | Delivery Method | SLA |
|---------------|-----------|----------------|-----|
| User Events | Auth service, notification service, analytics, GDPR compliance | Queue + webhook | Real-time |
| Role/Trust Events | Permission service, notification service, scoring engine | Queue | Real-time |
| Property Events | Search index, matching engine, notification service, analytics | Queue + CDC (change data capture) | Near real-time |
| Project/Dossier Events | Matching engine, notification service, workflow engine | Queue | Real-time |
| Matching Events | Notification service, project service, analytics | Queue | Real-time |
| Visit Events | Notification service, calendar service, CRM scoring | Queue | Real-time |
| Negotiation Events | Notification service, transaction service, analytics | Queue | Near real-time |
| Transaction Events | Document service, payment service, notification, compliance | Queue + webhook | Real-time |
| Payment Events | Billing service, notification, ledger, compliance | Queue + webhook | Real-time |
| CRM Events | Routing engine, notification, analytics, fraud detection | Queue | Real-time |
| Organization Events | Auth service, billing, notification | Queue | Near real-time |
| Approval Events | Notification, workflow engine, audit | Queue | Real-time |
| System Events | Monitoring, alerting, ops dashboard, SRE | Queue + direct | Real-time |

### 6.2 Consumer Delivery Guarantees

| Guarantee | Implementation |
|-----------|----------------|
| At-least-once delivery | Consumer acks after processing; retry queue on failure |
| Ordered delivery (per entity) | Partition by entity_type + entity_id |
| Dead letter queue | Events that fail after 3 retries routed to DLQ for manual inspection |
| Backpressure | Queue backlog monitoring; consumer autoscaling |
| Eventual consistency | Consumers process asynchronously; no transactional dependency on event creation |

### 6.3 Consumer Registration

| Consumer Type | Registration | Example |
|--------------|-------------|---------|
| Internal service | Hardcoded subscription | NotificationService subscribes to `user.*`, `property.*`, `visit.*` |
| Webhook (external) | Admin-configurable endpoint | External CRM subscribes to `lead.created`, `lead.converted` |
| Analytics pipeline | Batch ETL from event store | Data warehouse ingests all events daily |

---

## 7. Correlation ID for Event Chains

### 7.1 Correlation ID Generation

| Scope | Generated By | Format | Example |
|-------|-------------|--------|---------|
| Request (HTTP) | API Gateway / middleware | `req_{uuid}` | `req_a1b2c3d4-...` |
| Workflow | Workflow engine | `wf_{uuid}` | `wf_e5f6g7h8-...` |
| Business transaction | Transaction service | `tx_{uuid}` | `tx_i9j0k1l2-...` |
| Batch process | Cron / scheduler | `batch_{uuid}` | `batch_m3n4o5p6-...` |

### 7.2 Propagation Rules

| Rule | Description |
|------|-------------|
| **Inheritance** | Child events inherit `correlation_id` from parent context |
| **Chaining** | Events triggered as a consequence of another event carry the same `correlation_id` |
| **Root correlation** | First event in a chain generates a new `correlation_id` |
| **Cross-entity** | Events across different entity types can share a `correlation_id` (e.g., `project.match_found` → `visit.requested` → `visit.confirmed`) |
| **Idempotency** | `correlation_id` used for idempotent event processing (deduplication) |

### 7.3 Example Event Chains

**Property Publishing Chain:**
```
correlation_id = req_{uuid}
  1. property.updated (draft → normalization)
  2. property.updated (normalization → classification)
  3. property.updated (classification → validation)
  4. property.verified
  5. property.published (validation → published)
  6. match.created (matching engine triggered)
```

**Lead-to-Transaction Chain:**
```
correlation_id = wf_{uuid}
  1. lead.created
  2. lead.scored
  3. lead.classified
  4. lead.routed
  5. lead.converted → project.created (same correlation_id)
  6. match.created
  7. visit.requested
  8. negotiation.started
  9. transaction.created
  10. payment.initiated
  11. payment.confirmed
  12. transaction.completed
```

### 7.4 Querying by Correlation ID

| Use Case | Query | Example |
|----------|-------|---------|
| Trace workflow | `SELECT * FROM events WHERE correlation_id = :cid ORDER BY created_at` | Debug a failed transaction |
| Replay chain | `SELECT * FROM events WHERE correlation_id = :cid ORDER BY created_at ASC` | Reproduce state |
| Chain metrics | `SELECT COUNT(DISTINCT correlation_id), AVG(duration) FROM event_chains` | Workflow performance |
| Identify orphan events | `SELECT * FROM events WHERE correlation_id IS NOT NULL AND parent_event_id IS NULL` | Missing chain starts |

---

## 8. Event Sourcing Considerations

### 8.1 Event Store Design

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Storage | Append-only events table + materialized snapshots | Audit immutability + query performance |
| Snapshot frequency | Every 100 events per aggregate or daily | Rebuild state without replaying full event stream |
| Event versioning | `event_schema_version` field on each event | Schema evolution without breaking existing events |
| Serialization | JSON for payload; Avro/Protobuf for internal streaming | Human-readable storage + efficient streaming |

### 8.2 State Reconstruction

| Method | Description | When Used |
|--------|-------------|-----------|
| **Full replay** | Replay all events for an entity from start | Bootstrap, data correction |
| **Snapshot + incremental** | Load latest snapshot, then replay events after snapshot | Normal read path |
| **Projection** | Pre-built read model updated by event stream | Query optimization |

### 8.3 Event Sourcing vs Audit Log

| Aspect | Event Sourcing | Audit Log (this model) |
|--------|---------------|----------------------|
| Source of truth | Events ARE the state | State is in entity tables; events record changes |
| State reconstruction | Required; no state tables | Not required; entity tables are source of truth |
| Query pattern | Replay event stream | Direct entity queries + event lookup |
| Complexity | High (event versioning, snapshots, projections) | Moderate (append-only log) |
| Use case | Systems where full auditability + temporal query is primary | LAWIM_V2: events as audit trail + observability |

### 8.4 Recommended Approach for LAWIM_V2

**Hybrid model**: Entity tables as source of truth + enriched audit events as immutable log.

- Entities maintain current state in relational tables
- Events capture every state transition with full context
- Snapshot tables (materialized views) for performance-critical queries
- Event streams for async consumers (notifications, analytics, search indexing)
- Migration path: current generic Event model → typed event catalog described here

### 8.5 Schema Evolution

| Scenario | Strategy |
|----------|----------|
| New event type added | Add to event catalog; no migration needed |
| Payload field added | `event_schema_version` incremented; old events remain valid |
| Payload field removed | Deprecated field optional; consumers ignore unknown fields |
| Event type deprecated | Kept in catalog as `DEPRECATED`; no new events created |
| Event type removed | Events remain in store; type removed from catalog after retention expiry |

---

## 9. Complete Extension Mapping Table

### 9.1 Event & Audit Extensions

| Extension ID | Source Concept | Target Entity | Proposed Structure | Priority | Human Decision |
|-------------|---------------|---------------|-------------------|----------|----------------|
| EXT-EVT-001 | Enriched Event entity (13 enriched attributes) | Event | Extend Event with entity_type, entity_id, actor_id, previous_state, new_state, transition, source, correlation_id, severity, privacy_level, retention_days, metadata | P1 | N |
| EXT-EVT-002 | Typed event catalog (13 categories) | Event | Typed event_type enum from catalog; event_type validation; per-event payload schemas | P1 | Y — catalog completeness |
| EXT-EVT-003 | Audit trail — all state transitions | Event | Mandatory audit event on every state transition across all entities; event naming convention | P1 | N |
| EXT-EVT-004 | Retention policy per event type | Event | Retention tiers (7d/30d/90d/365d/5y); archival strategy; purge criteria | P2 | Y — retention durations |
| EXT-EVT-005 | Privacy levels per event type | Event | Privacy level enum (public/internal/restricted/confidential); per-event-type defaults; enforcement | P2 | Y — privacy classification |
| EXT-EVT-006 | Event consumers | Event | Consumer matrix; delivery guarantees; webhook registration | P2 | N |
| EXT-EVT-007 | Correlation ID for event chains | Event | Correlation ID generation; propagation rules; cross-entity chaining; idempotency | P2 | N |
| EXT-EVT-008 | Event sourcing considerations | Event | Hybrid model (entity tables + audit events); snapshot strategy; schema evolution | P3 | Y — event sourcing adoption |
| EXT-EVT-009 | Severity classification | Event | Severity enum (debug/info/warning/error/critical); per-event-type defaults | P1 | N |
| EXT-EVT-010 | Source attribution | Event | Source enum (system/user/webhook/cron/integration); actor tracking | P1 | N |

### 9.2 All Event-* Fields Extension Table

| Field | Entity | Type | Extension Source | Description |
|-------|--------|------|------------------|-------------|
| `event_type` | Event | String | EXT-EVT-001 | Typed event kind from catalog |
| `entity_type` | Event | String | EXT-EVT-001 | Type of entity that generated the event |
| `entity_id` | Event | UUID | EXT-EVT-001 | Entity ID |
| `actor_id` | Event | UUID? | EXT-EVT-001 | User who triggered the event |
| `previous_state` | Event | String? | EXT-EVT-001 | State before transition |
| `new_state` | Event | String? | EXT-EVT-001 | State after transition |
| `transition` | Event | String? | EXT-EVT-001 | Transition name |
| `source` | Event | Enum | EXT-EVT-001 | system/user/webhook/cron/integration |
| `correlation_id` | Event | UUID? | EXT-EVT-007 | Correlation ID for event chains |
| `severity` | Event | Enum | EXT-EVT-009 | debug/info/warning/error/critical |
| `privacy_level` | Event | Enum | EXT-EVT-005 | public/internal/restricted/confidential |
| `retention_days` | Event | Int | EXT-EVT-004 | Retention duration in days |
| `metadata` | Event | JSON? | EXT-EVT-001 | Additional context metadata |
| `event_schema_version` | Event | Int | EXT-EVT-008 | Schema version for event evolution |

---

*End of EVENT_AUDIT_EXTENSION_MODEL.md — 9 sections, 10 event/audit extensions, 14 enriched fields defined.*
