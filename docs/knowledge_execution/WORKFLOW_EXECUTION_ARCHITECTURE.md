# WORKFLOW EXECUTION ARCHITECTURE

**Domain:** Workflow and State Machine Architecture  
**Version:** 1.0  
**Source:** Heritage Gold Extraction — LAWIM Workflow Reference (05-WORKFLOW-REFERENCE.md, 04-DECISION-ENGINE-REFERENCE.md, CRM_MODEL.md, 08-ROLE-REFERENCE.md)

---

## 1. Workflow Engine Architecture

The LAWIM Workflow Engine is composed of seven core subsystems that together manage the lifecycle of all business workflows.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      WORKFLOW ENGINE                                │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────────┐   │
│  │  Workflow    │  │   State     │  │   Transition Resolver    │   │
│  │  Registry    │  │  Manager    │  │  (authorized transitions)│   │
│  └──────┬───────┘  └──────┬───────┘  └───────────┬─────────────┘   │
│         │                 │                      │                  │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌───────────┴─────────────┐   │
│  │   Guard      │  │   Action     │  │      SLA Monitor        │   │
│  │  Evaluator   │  │  Executor    │  │  (timer-based checks)   │   │
│  └──────┬───────┘  └──────┬───────┘  └───────────┬─────────────┘   │
│         │                 │                      │                  │
│  ┌──────┴─────────────────┴──────────────────────┴─────────────┐   │
│  │                      NBA Trigger                              │   │
│  │  (recalculates NBA after every transition or SLA event)      │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.1 Workflow Registry

**Responsibility:** Stores the canonical definition of every workflow.

| Component | Description |
|---|---|
| `workflow_id` | Unique identifier (e.g., `property_lifecycle`, `dossier_lifecycle`) |
| `entity_type` | The business object the workflow governs (e.g., `property`, `dossier`) |
| `initial_state` | Starting state of the machine |
| `terminal_states` | Set of absorbing/end states |
| `states` | Complete list of states with metadata |
| `transitions` | Authorized transition table |
| `sla_rules` | SLA definitions keyed by state |
| `nba_rules` | NBA candidates keyed by state |
| `version` | Schema version for migration support |

**Loading:** On engine startup, all workflow definitions are loaded from the Registry into an in-memory cache. Definitions are immutable at runtime.

### 1.2 State Manager

**Responsibility:** Tracks the current state of every entity instance.

```
StateManager {
  getCurrentState(entityType, entityId) → State
  setState(entityType, entityId, newState, metadata) → void
  getHistory(entityType, entityId) → List<TransitionRecord>
  isInTerminalState(entityType, entityId) → boolean
}
```

The State Manager persists every state change to the `transition_history` table (see TRANSITION_CONTRACTS.md). History is never deleted.

### 1.3 Transition Resolver

**Responsibility:** Given a current state and an event, determine the valid target state(s).

```
TransitionResolver {
  resolve(entityType, currentState, event) → Transition | null
  getAllowedTransitions(entityType, currentState) → List<Transition>
}
```

The resolver returns `null` (forbidden) if no transition matches. The engine MUST reject invalid transitions per the constitutional rule: *"Invalid transition is FORBIDDEN"*.

### 1.4 Guard Evaluator

**Responsibility:** Execute preconditions before a transition is committed.

Each transition declares zero or more guard functions. All guards must pass for the transition to proceed.

Guard types:
- **Field guards:** Verify required fields are populated
- **Consistency guards:** Verify business invariants (e.g., "property still available")
- **Permission guards:** Verify actor has the right role/permission
- **External guards:** Verify conditions in external systems (e.g., payment gateway)

Guard evaluation is atomic: if any guard fails, the entire transition is rejected and NO state change occurs.

### 1.5 Action Executor

**Responsibility:** Execute the side effects declared on a transition.

Actions are executed AFTER guards pass and BEFORE the state change is committed. Actions can be:
- **Internal:** Update entity fields, trigger matching, send notifications
- **External:** Call payment gateway, send WhatsApp message, update CRM

Action execution follows a linear sequence. If an action fails:
1. All previously executed actions in the same transition are rolled back (compensation)
2. The transition is marked as `FAILED`
3. An error event is emitted

### 1.6 SLA Monitor

**Responsibility:** Detect SLA breaches and trigger NBA recalculation.

The SLA Monitor runs on a configurable tick interval (default: 1 minute). For every active entity:

```
for each (entityType, state) in activeEntities:
  sla = registry.get(entityType, state)
  if sla == null: continue
  elapsed = now - entity.lastStateChangeAt
  if elapsed > sla.threshold:
    emit SLA_BREACH(event)
    NBA_Trigger.recalculate(entity)
```

### 1.7 NBA Trigger

**Responsibility:** Recalculate the Next Best Action after every event.

The NBA Trigger is invoked after:
- Every successful state transition
- Every SLA breach detection
- Every external event that matches the Decision Engine reaction events

The NBA recalculation uses the strict priority order defined in the Decision Engine:

```
1. Correct an incoherence
2. Complete a critical field
3. Matching
4. Present a property
5. Contact the holder
6. Organize a visit
7. Follow up (relance)
8. Notifications
9. Dossier optimization
```

The result is stored as `current_nba` on the entity and is available for querying.

---

## 2. Workflow Lifecycle: Load → Instantiate → Execute

### 2.1 Loading

```
WorkflowDefinition def = WorkflowRegistry.load("dossier_lifecycle");
// Validates: all states reachable?, all terminal states absorbing?, no orphan states?
def.validate();
```

Validation checks:
- Every state is reachable from initial state
- No dangling transitions (target state must exist)
- Terminal states have no outgoing transitions (absorbing)
- SLA rules reference valid states
- NBA rules reference valid states

### 2.2 Instantiation

When a new business entity is created (e.g., a new dossier):

```
WorkflowInstance instance = new WorkflowInstance(
  workflowId = "dossier_lifecycle",
  entityType = "dossier",
  entityId = "dossier-abc-123",
  currentState = "Création",    // initial state
  createdAt = now(),
  metadata = { source: "whatsapp", priority: "P2" }
);
```

The instance is persisted and the initial NBA is calculated.

### 2.3 Execution

Execution is event-driven. An event arrives at the engine:

```
Event: { type: "field_completion", entityType: "dossier", entityId: "dossier-abc-123", data: {...} }
```

The engine processes through these steps:

```
1. Validate event is well-formed
2. Load workflow instance
3. TransitionResolver.resolve(dossier_lifecycle, Création, field_completion)
   → Transition { from: "Création", to: "Qualification", guard: "fields_complete?" }
4. GuardEvaluator.evaluate(guard, instance, event)
   → PASS
5. ActionExecutor.execute(actions, instance, event)
   → [update status, log event, trigger NBA]
6. StateManager.setState(dossier, dossier-abc-123, "Qualification", { transitionedAt: now() })
7. NBA_Trigger.recalculate(dossier-abc-123)
8. EventBus.emit(TransitionEvent { ... })
```

All steps 4-8 are executed within a single transaction. If any step fails, the transaction is rolled back entirely.

---

## 3. Decision Engine and NBA Engine Integration

The Decision Engine and NBA Engine are not separate runtime components but rather **rule evaluators** invoked by the Workflow Engine at specific points.

### 3.1 Integration Points

| Trigger Point | Integration |
|---|---|
| After state transition | NBA recalculated via priority chain |
| SLA breach detected | NBA recalculated, may suggest escalation |
| External reaction event | NBA recalculated (e.g., holder responds) |
| Periodic timer | Continuous market surveillance triggers rematching |

### 3.2 Decision Engine Priority Chain

The Decision Engine evaluates the entity and produces the single highest-priority action:

```
function calculateNBA(entity):
  if entity.hasIncoherence(): return CORRECT_INCOHERENCE
  if entity.hasMissingCriticalField(): return COMPLETE_CRITICAL_FIELD
  if entity.canMatch(): return LAUNCH_MATCHING
  if entity.hasPropertyToPresent(): return PRESENT_PROPERTY
  if entity.shouldContactHolder(): return CONTACT_HOLDER
  if entity.canOrganizeVisit(): return ORGANIZE_VISIT
  if entity.needsFollowUp(): return FOLLOW_UP
  if entity.hasNotifications(): return SEND_NOTIFICATIONS
  return OPTIMIZE_DOSSIER
```

### 3.3 NBA Persistence

Every entity carries a `current_nba` field. This is visible to:
- The frontend (displays NBA badge to agents)
- The SLA Monitor (silence exceeding NBA threshold triggers alert)
- The notification system (sends NBA reminder)

The NBA history is stored for analytics (NBA changes over time, NBA completion rate).

---

## 4. Error Handling

### 4.1 Failed Transitions

| Failure Point | Behavior | Compensation |
|---|---|---|
| Guard evaluation fails | Transition rejected, no state change | None needed (no side effects executed) |
| Action execution fails mid-sequence | Execute rollback for completed actions | Compensation actions in reverse order |
| Persistence fails | Full transaction rollback | Database rollback |
| External system unavailable | Retry with exponential backoff (max 3) | Circuit breaker after max retries |

### 4.2 Transition Error Event

On any transition failure, the engine emits:

```json
{
  "event_type": "transition.failed",
  "entity_type": "dossier",
  "entity_id": "dossier-abc-123",
  "from_state": "Matching",
  "to_state": "Présentation",
  "reason": "GUARD_FAILED: property no longer available",
  "timestamp": "2026-07-15T10:00:00Z"
}
```

### 4.3 Compensation Actions

Each transition can declare a `rollback` array — a list of compensation actions to undo side effects:

```json
{
  "actions": [
    { "type": "notify_holder", "data": { "message": "..." } }
  ],
  "rollback": [
    { "type": "notify_holder", "data": { "message": "..." } }
  ]
}
```

Rollback actions execute in reverse order of the original actions. They are best-effort — if a rollback fails, the error is logged and manual intervention is flagged.

### 4.4 Idempotency

Every event carries an `event_id` (UUID). The engine deduplicates by `(event_id, entity_type, entity_id)` — if the same event is received twice, the second is silently ignored (idempotent).

---

## 5. Event Generation

Every successful transition generates a structured event:

```json
{
  "event_id": "evt-xxx",
  "event_type": "transition.completed",
  "workflow_id": "dossier_lifecycle",
  "entity_type": "dossier",
  "entity_id": "dossier-abc-123",
  "from_state": "Matching",
  "to_state": "Présentation",
  "trigger": {
    "event": "match_complete",
    "actor": "system",
    "reason": "Top match score > 80%"
  },
  "sla": {
    "elapsed_in_state_ms": 5000,
    "threshold_ms": 86400000,
    "breached": false
  },
  "nba": {
    "action": "PRESENT_PROPERTY",
    "priority": 4
  },
  "timestamp": "2026-07-15T10:00:00Z"
}
```

Events are published to the EventBus and consumed by:
- **Audit system** — permanent record
- **SLA Monitor** — reset state timer
- **NBA Trigger** — recalculate NBA
- **Notification system** — send user-facing alerts
- **Continuous Learning** — update models (refusals, preferences, scores)
- **Reporting** — update dashboards

---

## 6. Parallel Workflow Execution

Cross-cutting workflows run in **parallel** to main workflows. They share entity references but maintain independent state machines.

### 6.1 Parallelism Model

```
Main:          Dossier Lifecycle (Création → ... → Archivage)
                    │
Parallel:      ┌────┼────┐
               │    │    │
               ▼    ▼    ▼
          Visit   Nego-   Transaction
          Life-   tiation Lifecycle
          cycle   Life-
                  cycle
```

Each parallel workflow:
- Has its own state machine instance
- Has its own SLA rules
- Has its own NBA
- Shares the parent entity's `entity_id` via a `parent_workflow_id` reference

### 6.2 Coordination Rules

| Event | Effect on Parallel Workflows |
|---|---|
| Main workflow archived | All parallel workflows archived |
| Visit completed | May trigger Negotiation workflow |
| Negotiation completed | May trigger Transaction workflow |
| Main workflow fails | Parallel workflows notified but not automatically terminated |

### 6.3 Cross-Cutting Workflow

The Main Cross-cutting Workflow (21 workflows) orchestrates the entire lifecycle from "Real Estate Project" to "Archiving". It launches sub-workflows at specific states:

```
Projet immobilier
    → Création du dossier (launches Dossier Lifecycle)
    → Qualification
    → Matching (launches Matching Lifecycle)
    → Mise en relation (launches Contact Lifecycle)
    → Visite (launches Visit Lifecycle)
    → Négociation (launches Negotiation Lifecycle)
    → Transaction (launches Transaction Lifecycle)
    → Clôture
    → Archivage
```

---

## 7. Workflow Hierarchy

### 7.1 Main Workflows

| ID | Name | Parent |
|---|---|---|
| `property_lifecycle` | Property Lifecycle | Cross-cutting |
| `dossier_lifecycle` | Dossier/Case Lifecycle | Cross-cutting |
| `user_identity` | User Identity Lifecycle | None (standalone) |
| `organization_lifecycle` | Organization/Agency Lifecycle | None (standalone) |
| `crm_pipeline` | CRM Pipeline (8 stages) | None (standalone) |

### 7.2 Sub-Workflows (launched by Main Workflows)

| ID | Name | Launched By | Launch State |
|---|---|---|---|
| `matching_lifecycle` | Matching Lifecycle | Dossier Lifecycle | Matching |
| `contact_lifecycle` | Mise en Relation / Contact | Dossier Lifecycle | Mise en relation |
| `visit_lifecycle` | Visit Lifecycle | Dossier Lifecycle | Visite |
| `negotiation_lifecycle` | Negotiation Lifecycle | Dossier Lifecycle | Négociation |
| `transaction_lifecycle` | Transaction Lifecycle | Dossier Lifecycle | Transaction |
| `mediation_workflow` | Mediation Workflow | Disputes Lifecycle | Décision |
| `publication_workflow` | Publication (SIE) | Property Lifecycle | Publié |
| `redirection_workflow` | Redirection (SIE) | Publication | Clic |
| `conversion_attribution` | Conversion & Attribution | Redirection | Session |
| `agent_invitation` | Agent Invitation | Organization Lifecycle | Demande |
| `agent_opt_in` | Agent Opt-In | CRM Pipeline | lead_classification |
| `identity_resolution` | Identity Resolution | CRM Pipeline / User Identity | async |

### 7.3 Support Workflows (cross-cutting, run in parallel)

| ID | Name | Trigger |
|---|---|---|
| `paid_services_payment` | Paid Services & Payment | Any service purchase |
| `disputes_claims_incidents` | Disputes, Claims & Incidents | Any incident report |
| `closure_archiving_retention` | Closure, Archiving & Retention | Any terminal state |
| `crm_pipeline` | CRM Pipeline (8 stages) | Incoming message |

---

## 8. State Machine Validation Rules

Before a workflow definition is accepted into the Registry, the following validations must pass:

| Rule | Description |
|---|---|
| Reachability | Every state reachable from initial state via valid transitions |
| Absorbing terminal | Terminal states have zero outgoing transitions |
| No dead ends | Every non-terminal state has at least one outgoing transition |
| Guard consistency | Every guard references valid fields/rules |
| Action consistency | Every action references a valid handler |
| SLA consistency | SLA metric must be measurable (time-based or count-based) |
| NBA consistency | Each NBA must be a valid Decision Engine action |
| Event consistency | Trigger event must be a registered system event type |

---

## 9. Integration with External Systems

| System | Integration Point | Protocol |
|---|---|---|
| WhatsApp/Telegram | Event source (incoming messages trigger CRM Pipeline) | Webhook → EventBus |
| Campay (Payment) | Payment confirmation triggers service activation | Callback → EventBus |
| DeepSeek | NBA explanation, matching score calculation | API call (Action Executor) |
| SIE | Publication, redirection, conversion tracking | EventBus → SIE adapter |
| Notification Service | Reminders, alerts, NBA notifications | EventBus → notifier |

---

## 10. System Event Types (trigger events)

These are the canonical events that can trigger a state transition, per the Heritage Gold extraction:

| Event | Triggers Workflow |
|---|---|
| `message.received` | CRM Pipeline |
| `intent.detected` | CRM Pipeline |
| `user.created` | User Identity Lifecycle |
| `property.created` | Property Lifecycle |
| `lead.created` | CRM Pipeline |
| `match.generated` | Matching Lifecycle |
| `payment.success` | Paid Services & Payment |
| `subscription.renewed` | User Identity (Agent) |
| `boost.applied` | Paid Services |
| `access.granted` | Paid Services |
| `user.state_changed` | User Identity Lifecycle |
| `feedback.submitted` | Visit Lifecycle / Transaction |
| `fraud.detected` | Disputes Lifecycle |
| `sla.breach` | All workflows (monitoring) |
| `transition.failed` | All workflows (error handling) |
| `nba.recalculated` | All workflows |
