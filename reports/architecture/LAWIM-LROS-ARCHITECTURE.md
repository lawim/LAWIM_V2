# LAWIM Runtime Operating System (LROS) — Architecture

**Version:** 3.0.0-alpha
**Status:** IMPLEMENTED
**Last Updated:** 2026-07-22

---

## 1. Architecture Overview

LROS is the LAWIM Runtime Operating System. It is the single source of truth for all LAWIM V3 operations. LROS replaces the V2 conversation-centric pipeline with a project-centric, event-driven runtime.

### Design Principles

| Principle | Description |
|-----------|-------------|
| **No channel dependency** | LROS has zero knowledge of WhatsApp, Telegram, or Web transport |
| **No LLM dependency** | LROS does not import or reference OpenAI, DeepSeek, or Gemini |
| **Event-driven** | Every operation is triggered by an immutable event |
| **Project-centric** | The `ProjectRuntime` is the central state aggregate |
| **Deterministic** | Given the same events, LROS produces the same state |
| **Auditable** | Every state change is recorded with before/after snapshots |
| **Pluggable engines** | Business logic lives in `EngineBase` implementations registered at runtime |

### Architecture Diagram (Conceptual)

```
┌─────────────────────────────────────────────────────┐
│                    RuntimeAPI                        │
│              (single entry point)                    │
└──────────┬──────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│                 RuntimeDirector                      │
│           (orchestrates all operations)              │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Timeline  │  │  Audit   │  │    Metrics       │   │
│  │ (history) │  │ (before/ │  │ (counters,       │   │
│  │           │  │  after)  │  │  latency, errors)│   │
│  └──────────┘  └──────────┘  └──────────────────┘   │
└──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│                RuntimeScheduler                      │
│      (ordered engine execution)                      │
│                                                      │
│  Engine[0] → Engine[1] → Engine[2] → ...            │
└──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│                RuntimeRegistry                       │
│           (engine discovery by name)                 │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │Qualifier │  │  Matcher │  │  Conversation    │   │
│  │ Engine   │  │  Engine  │  │  Engine          │   │
│  └──────────┘  └──────────┘  └──────────────────┘   │
└──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│              RuntimePersistence                      │
│      (storage — in-memory / PostgreSQL / etc.)       │
└──────────────────────────────────────────────────────┘
```

### Event Flow

```
External trigger → RuntimeEvent → RuntimeAPI → RuntimeDirector
  → RuntimeScheduler → EngineBase[N] ... → ProjectRuntime mutated
  → Timeline.entry() → Audit.record() → Metrics.count()
  → EventBus.publish() → response
```

---

## 2. Core Components

### 2.1 RuntimeDirector

The central orchestrator. Every event flows through `RuntimeDirector.handle_event()`. It coordinates persistence, timeline recording, auditing, metrics, and event publication.

**File:** `lawim_runtime/runtime/director.py`

```
handle_event(event)
  ├── metrics.record_event_received(event.event_type)
  ├── metrics.measure(event.event_type):
  │   ├── _load_project(event.project_id)
  │   ├── scheduler.execute(project, event, registry)
  │   ├── _persist(project, event)
  │   ├── _record_timeline(project, event, before, after)
  │   ├── audit.record(event, before, after)
  │   └── bus.publish(event)
  └── return {project, event}
```

### 2.2 EventBus

Pub/sub event bus with history replay. Decouples event producers from consumers. Maintains an append-only event history for replay.

**File:** `lawim_runtime/events/bus.py`

- `subscribe(event_type, handler)` — register a handler for an event type
- `unsubscribe(event_type, handler)` — remove a handler
- `publish(event)` — append to history, notify all subscribers
- `replay(from_index=0)` — return all events from a given index

### 2.3 RuntimeStateMachine

Deterministic state machine enforcing valid project status transitions. Pure functions with no side effects.

**File:** `lawim_runtime/runtime/state_machine.py`

- `transition(current, target)` — validate and execute transition
- `can_transition(current, target)` — predicate check
- `next_statuses(current)` — list valid next statuses

### 2.4 RuntimeScheduler

Orders and executes engines registered in the RuntimeRegistry. Supports explicit ordering and automatic fallback for unlisted engines.

**File:** `lawim_runtime/scheduler/scheduler.py`

- `set_order(order)` — define engine execution order by name
- `execute(project, event, registry)` — resolve and execute matching engines

### 2.5 RuntimeRegistry

Engine discovery and lifecycle management. Engines are registered by name and resolved at runtime.

**File:** `lawim_runtime/registry/registry.py`

- `register(name, engine)` — register an engine
- `unregister(name)` — remove an engine
- `get(name)` — retrieve engine by name (raises `EngineNotFoundError`)
- `list()` — list registered engine names
- `get_all()` — return all registered engines

### 2.6 RuntimePersistence

Abstract base class for storage backends. Defines the contract for project and event persistence.

**File:** `lawim_runtime/persistence/persistence.py`

- `save_project(project)` — persist project state
- `load_project(project_id)` — load project by ID
- `save_event(event)` — persist event
- `load_events(project_id)` — load all events for a project
- `save_timeline_entry(entry)` — persist timeline entry

### 2.7 RuntimeMetrics

Telemetry counters and latency measurement. Tracks events received, engines executed, transitions, errors, and per-engine/per-event latency.

**File:** `lawim_runtime/telemetry/metrics.py`

- `record_event_received(event_type)`
- `record_engine_executed(engine_name)`
- `record_transition()`
- `record_error()`
- `record_latency(engine, latency_ms)`
- `measure(event_type)` — context manager for latency
- `get_summary()` — aggregate metrics

### 2.8 RuntimeAudit

Complete before/after audit trail for every state change. Immutable record of every event's impact on project state.

**File:** `lawim_runtime/telemetry/audit.py`

- `record(event, before, after)` — create an audit entry
- `get_entries(project_id=None)` — retrieve audit trail

### 2.9 Timeline

Project historical truth. Every event that affects a project produces a `TimelineEntry` with before/after snapshots.

**File:** `lawim_runtime/project/timeline.py`

- `append(entry)` — add a timeline entry
- `get_entries(project_id=None)` — retrieve entries (filtered or all)
- `replay(project_id, from_index=0)` — replay from a given index

### 2.10 RuntimeAPI

Single entry point for external callers. Accepts `RuntimeEvent` and delegates to `RuntimeDirector`.

**File:** `lawim_runtime/api/api.py`

- `handle_event(event)` — process a runtime event
- `create_project(project_type, owner)` — convenience method to create a new project

---

## 3. Event Model

### 3.1 RuntimeEvent (Base)

```python
@dataclass(frozen=True)
class RuntimeEvent:
    event_id: str        # auto-generated UUID hex (16 chars)
    event_type: str      # event discriminator (e.g. "PROJECT_CREATED")
    project_id: str      # target project (empty = new project)
    timestamp: str       # UTC ISO-8601
    actor: str           # who triggered the event ("system", user ID, etc.)
    source: str          # origin ("api", "whatsapp", "telegram", etc.)
    payload: dict        # event-specific data
    metadata: dict       # cross-cutting concerns (tracing, etc.)
    correlation_id: str  # end-to-end correlation
    causation_id: str    # parent event ID for causality chain
    version: int         # schema version (default 1)
```

### 3.2 Typed Event Types

| Class | Default `event_type` | Business Domain |
|-------|---------------------|-----------------|
| `ProjectEvent` | `PROJECT` | Project lifecycle (create, update, transition) |
| `ConversationEvent` | `CONVERSATION` | Message received, intent detected, slot updated |
| `QualificationEvent` | `QUALIFICATION` | Qualification data (budget, criteria, needs) |
| `MatchingEvent` | `MATCHING` | Property matching results |
| `VisitEvent` | `VISIT` | Visit scheduling and feedback |
| `DocumentEvent` | `DOCUMENT` | Document upload, verification, expiry |
| `PaymentEvent` | `PAYMENT` | Payment initiation, confirmation, failure |
| `NotificationEvent` | `NOTIFICATION` | Outbound notifications |
| `AnalyticsEvent` | `ANALYTICS` | Analytics and tracking |

All typed events extend `RuntimeEvent` and inherit its immutability contract.

### 3.3 Event Correlation

- `correlation_id` — end-to-end trace ID, preserved across event chains
- `causation_id` — the `event_id` of the event that caused this one (enables full causality DAG reconstruction)
- `version` — schema versioning for forward compatibility

### 3.4 Event Handling Lifecycle

```
1. RuntimeAPI.handle_event(event)
2. RuntimeDirector.handle_event(event)
   a. Load project (or create default)
   b. Capture before-state snapshot
   c. Execute registered engines via RuntimeScheduler
   d. Capture after-state snapshot
   e. Persist project + event
   f. Record timeline entry (before → after)
   g. Record audit entry (before → after)
   h. Publish event to EventBus subscribers
   i. Return {project, event}
```

---

## 4. Project Model

### 4.1 ProjectRuntime

```python
@dataclass
class ProjectRuntime:
    project_id: str                    # UUID hex (16 chars)
    project_type: ProjectType          # BUY, RENT, SELL, LIST, etc.
    status: ProjectStatus              # DRAFT, ACTIVE, QUALIFYING, etc.
    owner: str                         # owner/user identifier
    profile: dict                      # user profile data
    qualification: dict                # qualification criteria
    current_step: str                  # current workflow step
    current_stage: ProjectStage        # computed stage
    next_action: str                   # suggested next action
    risk_level: str                    # LOW, MEDIUM, HIGH
    priority: int                      # 0 = highest
    metadata: dict                     # extensible metadata
    created_at: str                    # UTC ISO-8601
    updated_at: str                    # UTC ISO-8601
    version: int                       # optimistic locking version
```

### 4.2 ProjectType

```
BUY, RENT, SELL, LIST, PUBLISH,
DOCUMENT_REQUEST, COMPLAINT,
CONSTRUCTION, PROFESSIONAL_SERVICE, OTHER
```

### 4.3 ProjectStatus (9 statuses)

| Status | Stage | Description |
|--------|-------|-------------|
| `DRAFT` | INITIAL | Project created, not yet active |
| `ACTIVE` | QUALIFICATION | User engaged, qualification in progress |
| `QUALIFYING` | QUALIFICATION | Collecting criteria and needs |
| `MATCHING` | SEARCH | Searching/matching properties |
| `VISIT_PENDING` | VISIT | Visit scheduled or pending |
| `NEGOTIATING` | NEGOTIATION | Price/terms negotiation |
| `TRANSACTION_PENDING` | TRANSACTION | Payment/document processing |
| `COMPLETED` | POST_TRANSACTION | Transaction completed |
| `CANCELLED` | CLOSED | Project cancelled (terminal) |
| `ARCHIVED` | CLOSED | Project archived (terminal) |

### 4.4 Valid Transitions

```
DRAFT ──────────► ACTIVE ──► QUALIFYING ──► MATCHING ──► VISIT_PENDING
  │                  │            │              │              │
  │                  │            │              │              │
  └──► CANCELLED ◄──┘◄──────────┘◄─────────────┘◄─────────────┘
                                        │
                                        ▼
                               NEGOTIATING ──► TRANSACTION_PENDING ──► COMPLETED ──► ARCHIVED
                                     │                  │
                                     │                  │
                                     └──► CANCELLED ◄───┘
```

### 4.5 Stage Map

| Status | Stage |
|--------|-------|
| DRAFT | INITIAL |
| ACTIVE | QUALIFICATION |
| QUALIFYING | QUALIFICATION |
| MATCHING | SEARCH |
| VISIT_PENDING | VISIT |
| NEGOTIATING | NEGOTIATION |
| TRANSACTION_PENDING | TRANSACTION |
| COMPLETED | POST_TRANSACTION |
| CANCELLED | CLOSED |
| ARCHIVED | CLOSED |

---

## 5. State Machine

The `RuntimeStateMachine` enforces deterministic transitions using the `VALID_TRANSITIONS` map.

### Rules

1. Every transition must be explicitly allowed in `VALID_TRANSITIONS`
2. `CANCELLED` is reachable from any non-terminal status except `COMPLETED`
3. `COMPLETED` can only transition to `ARCHIVED`
4. `CANCELLED` and `ARCHIVED` are terminal (no outgoing transitions)
5. Backward transitions are allowed (e.g., `QUALIFYING → ACTIVE`, `MATCHING → QUALIFYING`) to support re-qualification

### Exceptions

- `InvalidTransitionError` — raised when a disallowed transition is attempted
- Defined in `lawim_runtime/runtime/errors.py` — part of the `TransitionError` hierarchy

---

## 6. Data Flow

### Old (V2 — Conversation-Centric)

```
Message → ConversationStateEngine → Response
           (intent, state, generation all coupled)
```

### New (V3 — Project-Centric)

```
Message → RuntimeEvent → RuntimeAPI → RuntimeDirector
  → RuntimeScheduler → EngineBase[N] → ProjectRuntime mutated
  → Timeline → Audit → Metrics → EventBus.publish
  → ResponsePlan → Response
```

### Key Differences

| Aspect | V2 | V3 |
|--------|----|----|
| Central concept | Conversation | Project |
| State | ConversationState (chat-focused) | ProjectRuntime (business-focused) |
| Events | Implicit inside engine | First-class RuntimeEvent |
| Extensibility | Modify engine | Register new EngineBase |
| Audit | None | Complete before/after trail |
| Telemetry | None | Counters, latency, errors |
| Determinism | Not guaranteed | Enforced by state machine |

---

## 7. V2 Adapters

### 7.1 ConversationRuntimeAdapter

Bridges the V2 `ConversationStateEngine` to the LROS event system. The adapter publishes runtime events when the V2 engine detects messages, intents, slot updates, or qualification readiness — no modification to the V2 engine required.

**File:** `lawim_runtime/services/conversation_adapter.py`

| Method | Event Type Emitted |
|--------|-------------------|
| `on_message_received(project_id, actor, message, channel)` | `CONVERSATION_MESSAGE_RECEIVED` |
| `on_intent_detected(project_id, actor, intent, confidence)` | `CONVERSATION_INTENT_DETECTED` |
| `on_slot_updated(project_id, actor, field, value)` | `CONVERSATION_SLOT_UPDATED` |
| `on_qualification_ready(project_id, actor, qualification)` | `QUALIFICATION_READY` |

### 7.2 RuntimeFacade

Simplified facade for V2 modules that need to interact with LROS without constructing `RuntimeEvent` objects directly. Provides `process_event()`, `get_project()`, and `health()` methods.

**File:** `lawim_runtime/services/runtime_facade.py`

---

## 8. Directory Structure

```
lawim_runtime/
├── __init__.py                     # Public API exports
├── api/
│   ├── __init__.py
│   └── api.py                      # RuntimeAPI (single entry point)
├── events/
│   ├── __init__.py                 # All event type exports
│   ├── base.py                     # RuntimeEvent (frozen dataclass)
│   ├── bus.py                      # EventBus (pub/sub + replay)
│   ├── analytics.py                # AnalyticsEvent
│   ├── conversation.py             # ConversationEvent
│   ├── document.py                 # DocumentEvent
│   ├── matching.py                 # MatchingEvent
│   ├── notification.py             # NotificationEvent
│   ├── payment.py                  # PaymentEvent
│   ├── project.py                  # ProjectEvent
│   ├── qualification.py            # QualificationEvent
│   └── visit.py                    # VisitEvent
├── persistence/
│   ├── __init__.py
│   ├── persistence.py              # RuntimePersistence ABC
│   └── snapshot.py                 # Snapshot dataclass
├── project/
│   ├── __init__.py
│   ├── model.py                    # ProjectRuntime dataclass
│   ├── status.py                   # ProjectStatus, ProjectType, ProjectStage, VALID_TRANSITIONS, STAGE_MAP
│   └── timeline.py                 # Timeline, TimelineEntry
├── registry/
│   ├── __init__.py
│   ├── engine.py                   # EngineBase ABC
│   └── registry.py                 # RuntimeRegistry
├── runtime/
│   ├── __init__.py
│   ├── director.py                 # RuntimeDirector
│   ├── errors.py                   # Error hierarchy
│   └── state_machine.py            # RuntimeStateMachine
├── scheduler/
│   ├── __init__.py
│   ├── scheduler.py                # RuntimeScheduler
│   └── task.py                     # Task, TaskPriority
├── services/
│   ├── __init__.py
│   ├── conversation_adapter.py     # ConversationRuntimeAdapter
│   └── runtime_facade.py           # RuntimeFacade
├── telemetry/
│   ├── __init__.py
│   ├── audit.py                    # RuntimeAudit, AuditEntry
│   └── metrics.py                  # RuntimeMetrics
└── tests/
    ├── __init__.py
    ├── test_audit.py               # 2 tests
    ├── test_events.py              # 6 tests
    ├── test_integration.py         # 7 tests
    ├── test_metrics.py             # 3 tests
    ├── test_project.py             # 4 tests
    ├── test_registry.py            # 3 tests
    ├── test_scheduler.py           # 2 tests
    ├── test_state_machine.py       # 7 tests
    └── test_timeline.py            # 3 tests
```

---

## 9. Test Coverage

**Total: 38 tests — 0 FAILED, 0 ERROR, 0 XFAIL, 0 XPASS**

| Test File | Count | Coverage |
|-----------|-------|----------|
| `test_state_machine.py` | 7 | All status transitions, `can_transition`, `next_statuses`, full journey, cancellation, stage map consistency |
| `test_integration.py` | 7 | Full pipeline, event replay, metrics tracking, conversation adapter, runtime facade, multi-engine pipeline |
| `test_events.py` | 6 | Event creation, immutability, pub/sub, unsubscribe, replay, typed events |
| `test_project.py` | 4 | Creation, to_dict, profile, stage updates |
| `test_registry.py` | 3 | Register/get, not found, list |
| `test_timeline.py` | 3 | Append, filter, replay |
| `test_metrics.py` | 3 | Counters, measurement, summary |
| `test_scheduler.py` | 2 | Execution order, skip unregistered |
| `test_audit.py` | 2 | Record, filter |
| **Total** | **38** | **All deterministic** |

All tests are deterministic — no mocks, no network, no randomness in assertions.

---

## 10. Migration Path V2 → V3

### Phase 1: Coexistence (Current)
- `ConversationRuntimeAdapter` bridges V2 events into LROS
- `RuntimeFacade` provides V2 modules with LROS access
- Both V2 and V3 pipelines operate in parallel
- LROS records all events without affecting V2 behavior

### Phase 2: Adoption
- New features are built as `EngineBase` implementations in LROS
- V2 engines are gradually wrapped as LROS engines
- Timeline and audit replace V2 debug logging

### Phase 3: Cutover
- RuntimeAPI becomes the primary entry point
- V2 ConversationStateEngine becomes a downstream consumer of LROS events
- V2 pipeline is deprecated and removed

### Phase 4: Optimization
- RuntimePersistence backed by PostgreSQL (instead of in-memory)
- Event sourcing with Snapshot for fast rebuild
- Parallel engine execution in RuntimeScheduler
- Circuit breakers for engine failures

---

## Appendix: Error Hierarchy

```
RuntimeError (base)
├── EventError
├── TransitionError
│   └── InvalidTransitionError
├── ProjectNotFoundError
├── EngineNotFoundError
├── ValidationError
├── PersistenceError
└── ConcurrencyError
```
