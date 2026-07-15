# TRANSITION CONTRACTS

**Domain:** Workflow and State Machine Architecture  
**Version:** 1.0  
**Source:** Heritage Gold Extraction — 05-WORKFLOW-REFERENCE.md Ch7 (Workflow Transition Rules), all state machines

---

## 1. Transition Contract Structure

Every state transition in LAWIM is represented by a formal contract with the following schema:

```json
{
  "transition_id": "dossier_creation_to_qualification",
  "workflow_id": "dossier_lifecycle",
  "from_state": "Création",
  "to_state": "Qualification",
  "event_type": "field_completion",
  "priority": 1,
  "guards": [
    {
      "id": "required_fields_present",
      "type": "FIELD_CHECK",
      "description": "All mandatory fields for creation are populated",
      "evaluator": "field_exists(entity, 'type') && field_exists(entity, 'budget') && field_exists(entity, 'location')",
      "fail_message": "Required fields missing: type, budget, and location must be specified"
    }
  ],
  "actions": [
    {
      "id": "update_status",
      "type": "STATE_UPDATE",
      "handler": "setState('Qualification')"
    },
    {
      "id": "log_qualification_start",
      "type": "AUDIT",
      "handler": "emit('dossier.qualifying')"
    }
  ],
  "side_effects": [
    {
      "id": "nba_recalculate",
      "type": "NBA_TRIGGER",
      "handler": "calculateNBA(entity)"
    }
  ],
  "rollback": [
    {
      "id": "revert_status",
      "type": "STATE_REVERT",
      "handler": "setState('Création')"
    }
  ],
  "audit_events": [
    {
      "event_type": "transition.completed",
      "template": "Dossier {entity_id} transitioned from Création to Qualification"
    },
    {
      "event_type": "dossier.qualified",
      "template": "Dossier {entity_id} qualification started"
    }
  ],
  "idempotency_key": "event_id + entity_type + entity_id",
  "timeout_ms": 30000,
  "retry_policy": {
    "max_retries": 3,
    "backoff_ms": 1000,
    "exponential_base": 2
  }
}
```

### 1.1 Contract Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `transition_id` | string | yes | Unique identifier within the workflow |
| `workflow_id` | string | yes | Reference to parent workflow definition |
| `from_state` | string | yes | Source state (must exist in workflow states) |
| `to_state` | string | yes | Target state (must exist in workflow states) |
| `event_type` | string | yes | Event that triggers this transition |
| `priority` | integer | no | Execution priority (lower = higher) |
| `guards` | Guard[] | no | Preconditions that must all pass |
| `actions` | Action[] | yes | Side effects to execute on transition |
| `side_effects` | SideEffect[] | no | Post-transition side effects |
| `rollback` | Action[] | no | Compensation actions if transition fails |
| `audit_events` | AuditEvent[] | yes | Events to emit for this transition |
| `idempotency_key` | string | yes | Deduplication key pattern |
| `timeout_ms` | integer | no | Max execution time before abort |
| `retry_policy` | object | no | Retry configuration |

---

## 2. Guard Evaluation Rules

### 2.1 Guard Types

| Guard Type | Description | Evaluation | Examples |
|---|---|---|---|
| `FIELD_CHECK` | Verifies entity fields | Synchronous, local | `field_exists(entity, 'type')` |
| `CONSISTENCY` | Verifies business invariants | Synchronous, local | `entity.status == 'available'` |
| `PERMISSION` | Verifies actor permissions | Synchronous, role engine | `actor.hasRole('agent')` |
| `EXTERNAL` | Verifies external system state | Asynchronous, timeout | `paymentGateway.isValid(invoice)` |
| `TEMPORAL` | Verifies timing constraints | Synchronous | `now - entity.createdAt > 24h` |
| `SCORE_CHECK` | Verifies scoring thresholds | Synchronous | `matchScore >= 60` |

### 2.2 Guard Evaluation Semantics

- Guards are evaluated in declaration order.
- ALL guards must return `true` for the transition to proceed (AND semantics).
- If any guard returns `false`, the transition is REJECTED immediately.
- No actions or side effects are executed for a rejected transition.
- The rejecting guard's `fail_message` is returned to the caller.

### 2.3 Guard Examples

**Example 1: Property Validation transition (Validation → Publié)**

```json
{
  "guards": [
    {
      "id": "coherence_check",
      "type": "CONSISTENCY",
      "evaluator": "entity.surface >= entity.rooms * 5",
      "fail_message": "Surface is too small for the declared number of rooms"
    },
    {
      "id": "conformity_check",
      "type": "CONSISTENCY",
      "evaluator": "entity.propertyType in ['chambre','studio','appartement','villa','terrain','commerce','bureau','hotel']",
      "fail_message": "Invalid property type"
    },
    {
      "id": "uniqueness_check",
      "type": "EXTERNAL",
      "evaluator": "!registry.hasDuplicate(entity)",
      "fail_message": "Duplicate property detected"
    },
    {
      "id": "availability_check",
      "type": "CONSISTENCY",
      "evaluator": "entity.owner.status != 'blocked'",
      "fail_message": "Owner account is blocked"
    }
  ]
}
```

**Example 2: Double Consent Guard (Contact Lifecycle)**

```json
{
  "guards": [
    {
      "id": "demandeur_consent",
      "type": "FIELD_CHECK",
      "evaluator": "entity.demandeurConfirmedInterest == true",
      "fail_message": "Demandeur has not confirmed interest"
    },
    {
      "id": "holder_consent",
      "type": "FIELD_CHECK",
      "evaluator": "entity.holderDecision == 'accept'",
      "fail_message": "Holder has not accepted contact"
    },
    {
      "id": "dossier_active",
      "type": "CONSISTENCY",
      "evaluator": "dossier.status != 'archived' && dossier.status != 'closed'",
      "fail_message": "Dossier is not active"
    },
    {
      "id": "property_available",
      "type": "CONSISTENCY",
      "evaluator": "property.availabilityStatus == 'Disponible'",
      "fail_message": "Property is no longer available"
    }
  ]
}
```

### 2.4 Guard Evaluation Order

1. FIELD_CHECK (fastest — local entity inspection)
2. CONSISTENCY (local business logic)
3. PERMISSION (role engine lookup)
4. SCORE_CHECK (score computation)
5. TEMPORAL (timestamp arithmetic)
6. EXTERNAL (slowest — network call, has timeout)

---

## 3. Action Execution Model

### 3.1 Action Types

| Action Type | Description | Execution | Idempotent |
|---|---|---|---|
| `STATE_UPDATE` | Persist new state | Synchronous | yes |
| `AUDIT` | Write audit log | Synchronous | yes |
| `NOTIFICATION` | Send user notification | Async (fire-and-forget) | yes (by event_id) |
| `EXTERNAL_CALL` | Call external API | Synchronous with timeout | depends on handler |
| `NBA_TRIGGER` | Recalculate NBA | Synchronous | yes |
| `SLA_RESET` | Reset SLA timer for new state | Synchronous | yes |
| `EMAIL` | Send email | Async | yes |
| `WHATSAPP` | Send WhatsApp message | Async | yes |
| `WEBHOOK` | Call external webhook | Async | depends on handler |
| `COMPENSATION` | Execute rollback logic | Synchronous | yes |

### 3.2 Action Execution Sequence

Actions are executed in a strict linear sequence within a single database transaction:

```
1. START TRANSACTION
2. Execute action[0] → GUARD
3. Execute action[1] → AUDIT
4. Execute action[2] → NOTIFICATION
   ...
N. Execute action[n-1] → NBA_TRIGGER
N+1. COMMIT TRANSACTION
```

If any action throws an exception:
1. The transaction is ROLLED BACK immediately
2. Compensation actions are executed in reverse order (best-effort, outside the transaction)
3. The transition is marked `FAILED`
4. A `transition.failed` event is emitted

### 3.3 Action Result Handling

```json
{
  "action_id": "update_status",
  "status": "SUCCESS" | "FAILURE" | "SKIPPED",
  "result": { "new_state": "Qualification" },
  "error": null,
  "duration_ms": 5
}
```

---

## 4. Rollback and Compensation

### 4.1 When Rollback Executes

Rollback is triggered when:
1. An action in the transition sequence fails
2. The database transaction fails to commit
3. The transition timeout is exceeded

### 4.2 Compensation Action Execution

Compensation actions execute in REVERSE order of the original actions. If the original sequence was `[A1, A2, A3]`, compensation runs `[C3, C2, C1]`.

```json
{
  "actions": [
    { "id": "notify_demandeur", "type": "WHATSAPP", "data": { "message": "Visit confirmed" } },
    { "id": "notify_holder", "type": "WHATSAPP", "data": { "message": "Visit confirmed" } }
  ],
  "rollback": [
    { "id": "notify_demandeur_cancel", "type": "WHATSAPP", "data": { "message": "Visit confirmation failed, please try again" } },
    { "id": "notify_holder_cancel", "type": "WHATSAPP", "data": { "message": "Visit confirmation failed, please try again" } }
  ]
}
```

### 4.3 Compensation Failure

If a compensation action fails:
- The error is logged with HIGH severity
- A manual intervention flag is raised on the entity
- The system continues executing remaining compensation actions
- The entity's `error_state` field records the details

---

## 5. Idempotency Guarantees

### 5.1 Idempotency Key

Every event that triggers a transition carries an `event_id` (UUID v4). The idempotency key is computed as:

```
idempotency_key = sha256(event_id + ":" + entity_type + ":" + entity_id)
```

### 5.2 Deduplication

Before executing a transition, the engine checks:

```
if idempotency_store.exists(idempotency_key):
  return PREVIOUS_RESULT  // idempotent response
else:
  idempotency_store.store(idempotency_key, PENDING)
  execute_transition()
  idempotency_store.store(idempotency_key, FINAL_RESULT)
```

### 5.3 Idempotency by Action Type

| Action Type | Idempotent? | Mechanism |
|---|---|---|
| `STATE_UPDATE` | Yes | Setting same state twice is a no-op |
| `AUDIT` | Yes | Dedup by event_id |
| `NOTIFICATION` | Yes | Dedup by event_id in notification service |
| `EXTERNAL_CALL` | Conditional | Must support idempotency key in request |
| `NBA_TRIGGER` | Yes | Recalculation is deterministic |
| `WHATSAPP` | Yes | Message dedup by external_id |

### 5.4 Event Replay Safety

Replaying archived events through the engine is SAFE because:
1. State changes are idempotent (setting the same state is a no-op)
2. Duplicate events are detected and ignored
3. Side effects are gated by idempotency keys

---

## 6. Transition History and Traceability

### 6.1 Transition History Schema

Every transition is permanently recorded:

```sql
CREATE TABLE transition_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id VARCHAR(64) NOT NULL,
  entity_type VARCHAR(64) NOT NULL,
  entity_id VARCHAR(128) NOT NULL,
  from_state VARCHAR(64) NOT NULL,
  to_state VARCHAR(64) NOT NULL,
  event_type VARCHAR(64) NOT NULL,
  event_id UUID NOT NULL,
  actor_id VARCHAR(128),
  actor_role VARCHAR(64),
  reason TEXT,
  guards_passed JSONB,
  actions_executed JSONB,
  side_effects JSONB,
  nba_before VARCHAR(64),
  nba_after VARCHAR(64),
  sla_elapsed_ms BIGINT,
  status VARCHAR(16) NOT NULL DEFAULT 'COMPLETED',  -- COMPLETED, FAILED, ROLLED_BACK
  error_message TEXT,
  idempotency_key VARCHAR(64) UNIQUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_transition_history_entity ON transition_history(entity_type, entity_id);
CREATE INDEX idx_transition_history_workflow ON transition_history(workflow_id);
CREATE INDEX idx_transition_history_event ON transition_history(event_id);
CREATE INDEX idx_transition_hierarchy ON transition_history(entity_type, entity_id, created_at DESC);
```

### 6.2 Traceability Guarantees

1. **History is NEVER deleted** (constitutional rule)
2. Every transition is recorded with before/after state
3. Every transition records the NBA before and after recalculation
4. Every transition records SLA elapsed time at the moment of transition
5. Failed transitions are recorded with full error details
6. History supports point-in-time reconstruction of any entity's state

### 6.3 Audit Trail Consistency

```json
// Example audit record for a failed transition
{
  "id": "tr-abc-123",
  "workflow_id": "dossier_lifecycle",
  "entity_type": "dossier",
  "entity_id": "dossier-xyz-789",
  "from_state": "Matching",
  "to_state": "Présentation",
  "event_type": "match_complete",
  "event_id": "evt-def-456",
  "actor_id": "system",
  "actor_role": "decision_engine",
  "reason": "Match score >= 60% threshold",
  "guards_passed": [
    { "id": "score_threshold", "result": true },
    { "id": "dossier_active", "result": true }
  ],
  "actions_executed": [
    { "id": "present_properties", "status": "SUCCESS", "result": { "presented_count": 5 } }
  ],
  "side_effects": [
    { "id": "nba_recalculate", "status": "SUCCESS", "result": { "nba": "WAIT_FOR_DECISION" } }
  ],
  "nba_before": "LAUNCH_MATCHING",
  "nba_after": "WAIT_FOR_DECISION",
  "sla_elapsed_ms": 45000,
  "status": "COMPLETED",
  "created_at": "2026-07-15T10:00:00Z"
}
```

---

## 7. Transition Examples from Heritage Gold

### 7.1 Valid Transitions

| Example | Rule |
|---|---|
| Dossier: Matching → Présentation | Score >= 60% → Authorized |
| Property: Création → Qualification | Fields complete → Authorized |
| Visit: Confirmée → Réalisée | Visit occurred → Authorized |
| Negotiation: Offre → Contre-offre | Counter-offer valid → Authorized |

### 7.2 Invalid Transitions (Forbidden)

| Example | Rule |
|---|---|
| Transaction → Création | Forbidden — cannot reverse lifecycle |
| Visit → Matching | Forbidden — cannot skip back |
| Matching → Visite (without Presentation) | Forbidden — must pass through presentation |
| Archived → Création (without reactivation) | Forbidden — must go through reopening procedure |

### 7.3 Constitutional Transition Rules

Per 05-WORKFLOW-REFERENCE.md Ch7:
1. A transition must always respect: business rules, user rights, official repositories
2. Invalid transition is FORBIDDEN
3. Every transition is recorded: old state, new state, author, date, reason, possible comments
4. History is NEVER deleted

---

## 8. Transition Contract Index by Workflow

| Workflow | Transition Count |
|---|---|
| Property Lifecycle | 12 |
| Dossier Lifecycle | 15 |
| Matching Lifecycle | 10 |
| Contact Lifecycle | 7 |
| Visit Lifecycle | 9 |
| Negotiation Lifecycle | 9 |
| Transaction Lifecycle | 10 |
| Paid Services & Payment | 8 (service) + 11 (payment) |
| Disputes & Incidents | 8 |
| Closure & Archiving | 3 |
| Mediation | 7 |
| User Identity | 10 |
| Organization Lifecycle | 8 |
| Agent Invitation | 6 |
| Publication (SIE) | 10 |
| Redirection (SIE) | 11 |
| Conversion & Attribution | 11 |
| CRM Pipeline | 7 (sequential stages) |
| Agent Opt-In | 3 |
| Identity Resolution | 5 |
| Main Cross-cutting | 8 |
| **Total** | **~180+ transitions** |

---

## 9. Transition Validation

Before a transition contract is registered, these validations run:

| Validation | Description | Fails If |
|---|---|---|
| Source state exists | `from_state` is in workflow states | State not found |
| Target state exists | `to_state` is in workflow states | State not found |
| Terminal check | `from_state` is not terminal | Transition from terminal state |
| Guard handler exists | Each guard's evaluator is registered | Unknown evaluator |
| Action handler exists | Each action's handler is registered | Unknown handler |
| Rollback handler exists | Each rollback's handler is registered | Unknown handler |
| Event type registered | `event_type` is in system event types | Unknown event type |
| Idempotency key valid | Pattern compiles | Invalid pattern |
