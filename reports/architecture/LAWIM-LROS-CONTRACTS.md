# LAWIM Runtime Operating System (LROS) — Public Interface Contracts

**Version:** 3.0.0-alpha
**Status:** IMPLEMENTED
**Last Updated:** 2026-07-22

---

## 1. RuntimeEvent

**Module:** `lawim_runtime.events.base`
**Class:** `RuntimeEvent` (frozen dataclass)

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `event_id` | `str` | `uuid4().hex[:16]` | Unique event identifier (16 hex chars) |
| `event_type` | `str` | `""` | Event discriminator for routing and filtering |
| `project_id` | `str` | `""` | Target project ID. Empty string means new project |
| `timestamp` | `str` | `datetime.now(timezone.utc).isoformat()` | UTC ISO-8601 timestamp of event creation |
| `actor` | `str` | `"system"` | Entity that triggered the event (user ID, "system", "agent") |
| `source` | `str` | `""` | Channel or origin ("api", "whatsapp", "telegram", "web") |
| `payload` | `dict[str, Any]` | `{}` | Event-type-specific business data |
| `metadata` | `dict[str, Any]` | `{}` | Cross-cutting concerns (tracing tokens, feature flags) |
| `correlation_id` | `str` | `""` | End-to-end trace identifier preserved across event chains |
| `causation_id` | `str` | `""` | `event_id` of the event that caused this one |
| `version` | `int` | `1` | Schema version for forward compatibility |

### Constraints

- **Immutable**: The dataclass is `frozen=True`. Any attempt to modify a field after creation raises `FrozenInstanceError`
- **event_id** is auto-generated but can be overridden for deterministic testing
- **project_id** = `""` signals a new project (Director auto-creates a `ProjectRuntime`)

---

## 2. Typed Event Classes

All inherit from `RuntimeEvent` and set a default `event_type`. All are frozen dataclasses.

| Class | Module | Default `event_type` |
|-------|--------|---------------------|
| `ProjectEvent` | `lawim_runtime.events.project` | `"PROJECT"` |
| `ConversationEvent` | `lawim_runtime.events.conversation` | `"CONVERSATION"` |
| `QualificationEvent` | `lawim_runtime.events.qualification` | `"QUALIFICATION"` |
| `MatchingEvent` | `lawim_runtime.events.matching` | `"MATCHING"` |
| `VisitEvent` | `lawim_runtime.events.visit` | `"VISIT"` |
| `DocumentEvent` | `lawim_runtime.events.document` | `"DOCUMENT"` |
| `PaymentEvent` | `lawim_runtime.events.payment` | `"PAYMENT"` |
| `NotificationEvent` | `lawim_runtime.events.notification` | `"NOTIFICATION"` |
| `AnalyticsEvent` | `lawim_runtime.events.analytics` | `"ANALYTICS"` |

Each typed event exposes the same field set as `RuntimeEvent`. Override `event_type` at construction for granular routing:

```python
event = ConversationEvent(
    event_type="CONVERSATION_MESSAGE_RECEIVED",
    project_id="p1",
    payload={"message": "Bonjour", "channel": "whatsapp"},
)
```

---

## 3. EventBus

**Module:** `lawim_runtime.events.bus`

### `subscribe(event_type: str, handler: EventHandler) -> None`

Register a callable to receive events of the specified type.

- `event_type`: string discriminator to filter events
- `handler: Callable[[RuntimeEvent], None]`: callback invoked for each matching event
- Multiple handlers can subscribe to the same event_type
- The same handler can subscribe to multiple event_types

### `unsubscribe(event_type: str, handler: EventHandler) -> None`

Remove a previously registered handler.

- `handler`: the exact callable reference passed to `subscribe`
- No-op if the handler was not registered

### `publish(event: RuntimeEvent) -> None`

Append the event to the internal history and notify all handlers registered for `event.event_type`.

- Handlers are called synchronously in registration order
- An exception in one handler does not prevent other handlers from being called

### `replay(from_index: int = 0) -> list[RuntimeEvent]`

Return all events from `from_index` to the end of history.

- `from_index=0` returns the full history
- Index is the append order (0-based)
- Returns a copy of the slice (immutable events)

### `clear() -> None`

Remove all handlers and clear event history.

---

## 4. RuntimeDirector

**Module:** `lawim_runtime.runtime.director`

### Constructor

```python
RuntimeDirector(
    bus: EventBus,
    registry: RuntimeRegistry,
    scheduler: RuntimeScheduler,
    persistence: RuntimePersistence,
    timeline: Timeline,
    audit: RuntimeAudit,
    metrics: RuntimeMetrics,
)
```

All dependencies are injected. No default construction.

### `handle_event(event: RuntimeEvent) -> dict[str, Any]`

Process a runtime event through the full pipeline.

**Returns:**
```python
{
    "project": dict,   # ProjectRuntime.to_dict() after processing
    "event": RuntimeEvent,  # The processed event
}
```

**Pipeline stages (in order):**
1. `metrics.record_event_received(event.event_type)`
2. `metrics.measure(event.event_type)` context manager
3. `_load_project(event.project_id)` — returns existing project or creates new `ProjectRuntime()` if `project_id == ""`
4. `_scheduler.execute(project, event, registry)` — ordered engine execution
5. `_persist(project, event)` — save project state and event
6. `_record_timeline(project, event, before, after)` — before/after state snapshot
7. `_audit.record(event, before, after)` — audit trail
8. `_bus.publish(event)` — notify subscribers

**Edge cases:**
- Empty `project_id` → new `ProjectRuntime` created, returned as `None`-safe
- `project` is `None` after engine execution → empty dict returned in result

---

## 5. RuntimeStateMachine

**Module:** `lawim_runtime.runtime.state_machine`

### `transition(current: ProjectStatus, target: ProjectStatus) -> ProjectStatus`

Validate and execute a status transition.

- Returns `target` on success
- Raises `InvalidTransitionError` if `target` is not in `VALID_TRANSITIONS[current]`

### `can_transition(current: ProjectStatus, target: ProjectStatus) -> bool`

Pure predicate. Returns `True` if the transition is allowed, `False` otherwise.

### `next_statuses(current: ProjectStatus) -> list[ProjectStatus]`

Return sorted list of valid next statuses from `current`.

---

## 6. RuntimeScheduler

**Module:** `lawim_runtime.scheduler.scheduler`

### `set_order(order: list[str]) -> None`

Define the execution order of engines by name. Engines not in the order list are appended at the end (preserving their discovery order in the registry).

### `execute(project: ProjectRuntime | None, event: RuntimeEvent, registry: RuntimeRegistry) -> ProjectRuntime | None`

Resolve matching engines from the registry (via `can_handle(event)`), order them according to `_engine_order`, and execute each engine sequentially.

- Each engine receives `(project, event)` and returns `(project | None)`
- The output of engine N is the input of engine N+1
- If any engine raises, execution stops and `RuntimeError` is raised with the engine name
- Returns the final project state

### `_resolve_engines(event, registry) -> list[EngineBase]`

Internal. Returns engines whose `can_handle(event)` returns `True`, ordered by `_engine_order` first, then by insertion order.

---

## 7. RuntimeRegistry

**Module:** `lawim_runtime.registry.registry`

### `register(name: str, engine: Any) -> None`

Register an engine by name. Overwrites any existing engine with the same name.

### `unregister(name: str) -> None`

Remove an engine from the registry. No-op if name does not exist.

### `get(name: str) -> Any`

Retrieve an engine by name.

- Returns the registered engine object
- Raises `EngineNotFoundError` if `name` is not registered

### `list() -> list[str]`

Return a list of all registered engine names.

### `get_all() -> list[Any]`

Return a list of all registered engine objects (in insertion order).

### `clear() -> None`

Remove all registered engines.

---

## 8. EngineBase (ABC)

**Module:** `lawim_runtime.registry.engine`

### Abstract Methods

```python
class EngineBase(ABC):

    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def can_handle(self, event: RuntimeEvent) -> bool: ...

    @abstractmethod
    def execute(self, project: ProjectRuntime | None, event: RuntimeEvent) -> ProjectRuntime | None: ...
```

| Method | Returns | Description |
|--------|---------|-------------|
| `name()` | `str` | Engine identifier, used for ordering and metrics |
| `can_handle(event)` | `bool` | Predicate: should this engine process the given event? |
| `execute(project, event)` | `ProjectRuntime \| None` | Mutate project state based on event. Return `None` to signal deletion/no-project |

### Contract
- `execute` must be idempotent when possible
- `execute` may mutate the project in place or return a new instance
- `execute` should not raise on unrecognized events (use `can_handle` for routing)
- `project` may be `None` — engine must handle this gracefully

---

## 9. RuntimePersistence (ABC)

**Module:** `lawim_runtime.persistence.persistence`

### Abstract Methods

```python
class RuntimePersistence(ABC):

    @abstractmethod
    def save_project(self, project: ProjectRuntime) -> None: ...

    @abstractmethod
    def load_project(self, project_id: str) -> ProjectRuntime | None: ...

    @abstractmethod
    def save_event(self, event: RuntimeEvent) -> None: ...

    @abstractmethod
    def load_events(self, project_id: str) -> list[RuntimeEvent]: ...

    @abstractmethod
    def save_timeline_entry(self, entry: TimelineEntry) -> None: ...
```

| Method | Returns | Description |
|--------|---------|-------------|
| `save_project(project)` | `None` | Persist or update project state |
| `load_project(project_id)` | `ProjectRuntime \| None` | Load project by ID, or `None` if not found |
| `save_event(event)` | `None` | Append event to event store |
| `load_events(project_id)` | `list[RuntimeEvent]` | Load all events for a project (chronological order) |
| `save_timeline_entry(entry)` | `None` | Persist a timeline entry |

### Known Implementations
- `_MemoryPersistence` (in-memory dict — used in tests)

---

## 10. RuntimeMetrics

**Module:** `lawim_runtime.telemetry.metrics`

### Fields (dataclass)

| Field | Type | Description |
|-------|------|-------------|
| `events_received` | `dict[str, int]` | Event type → count |
| `engines_executed` | `dict[str, int]` | Engine name → count |
| `transitions_count` | `int` | Total state machine transitions |
| `errors_count` | `int` | Total errors encountered |
| `total_latency_ms` | `float` | Cumulative latency across all operations |
| `engine_latency` | `dict[str, list[float]]` | Engine name → list of latencies (ms) |
| `event_latency` | `dict[str, list[float]]` | Event type → list of latencies (ms) |

### Methods

| Method | Description |
|--------|-------------|
| `record_event_received(event_type)` | Increment event type counter |
| `record_engine_executed(engine_name)` | Increment engine execution counter |
| `record_transition()` | Increment transition counter |
| `record_error()` | Increment error counter |
| `record_latency(engine, latency_ms)` | Record a per-engine latency measurement |
| `measure(event_type)` | Context manager — records elapsed time in `event_latency` |
| `get_summary() -> dict` | Return aggregate summary (total events, by type, transitions, errors, total latency) |

---

## 11. RuntimeAudit

**Module:** `lawim_runtime.telemetry.audit`

### `record(event: RuntimeEvent, before: dict, after: dict) -> None`

Create and store an `AuditEntry` capturing the before/after state of a project for the given event.

- `before`: project state dict before event processing
- `after`: project state dict after event processing

### `get_entries(project_id: str | None = None) -> list[AuditEntry]`

Return audit entries. If `project_id` is provided, filter to that project. Otherwise return all entries.

### `clear() -> None`

Remove all audit entries.

### AuditEntry Fields

| Field | Type | Description |
|-------|------|-------------|
| `entry_id` | `str` | Auto-generated unique ID |
| `event_id` | `str` | ID of the triggering event |
| `event_type` | `str` | Event type discriminator |
| `project_id` | `str` | Target project |
| `actor` | `str` | Event actor |
| `before` | `dict` | Project state before processing |
| `after` | `dict` | Project state after processing |
| `timestamp` | `str` | UTC ISO-8601 |

---

## 12. Timeline

**Module:** `lawim_runtime.project.timeline`

### `append(entry: TimelineEntry) -> None`

Add a timeline entry to the project history.

### `get_entries(project_id: str | None = None) -> list[TimelineEntry]`

Return all entries, optionally filtered by project_id.

### `replay(project_id: str, from_index: int = 0) -> list[TimelineEntry]`

Replay timeline entries for a project from a given index. Used for event sourcing reconstruction.

### `clear() -> None`

Remove all entries.

### TimelineEntry Fields

| Field | Type | Description |
|-------|------|-------------|
| `entry_id` | `str` | Auto-generated unique ID |
| `project_id` | `str` | Target project |
| `event_type` | `str` | Event type discriminator |
| `before_state` | `dict` | Project state before processing |
| `after_state` | `dict` | Project state after processing |
| `actor` | `str` | Event actor |
| `source` | `str` | Event source/channel |
| `correlation_id` | `str` | End-to-end trace ID |
| `timestamp` | `str` | UTC ISO-8601 |

---

## 13. RuntimeAPI

**Module:** `lawim_runtime.api.api`

### Constructor

```python
RuntimeAPI(director: RuntimeDirector)
```

### `handle_event(event: RuntimeEvent) -> dict[str, Any]`

Delegates directly to `RuntimeDirector.handle_event(event)`. Returns the same result dict.

### `create_project(project_type: str, owner: str) -> dict[str, Any]`

Convenience method that constructs a `RuntimeEvent` with:
- `event_type = "PROJECT_CREATED"`
- `project_id = ""` (signals new project)
- `actor = owner`
- `source = "api"`
- `payload = {"project_type": project_type, "owner": owner}`

Returns the result of `handle_event()`.

---

## 14. ProjectRuntime

**Module:** `lawim_runtime.project.model`

### Fields (dataclass, mutable)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `project_id` | `str` | `uuid4().hex[:16]` | Unique project identifier |
| `project_type` | `ProjectType` | `ProjectType.OTHER` | Business type (BUY, RENT, SELL, etc.) |
| `status` | `ProjectStatus` | `ProjectStatus.DRAFT` | Current project status |
| `owner` | `str` | `""` | Owner/user identifier |
| `profile` | `dict` | `{}` | User profile data (name, contact, preferences) |
| `qualification` | `dict` | `{}` | Qualification criteria (budget, bedrooms, location, etc.) |
| `current_step` | `str` | `""` | Current workflow step identifier |
| `current_stage` | `ProjectStage` | `ProjectStage.INITIAL` | Computed stage (derived from status) |
| `next_action` | `str` | `""` | Suggested next action for the user/agent |
| `risk_level` | `str` | `"LOW"` | Risk assessment: LOW, MEDIUM, HIGH |
| `priority` | `int` | `0` | Priority (0 = highest) |
| `metadata` | `dict` | `{}` | Extensible metadata |
| `created_at` | `str` | UTC ISO-8601 | Creation timestamp |
| `updated_at` | `str` | UTC ISO-8601 | Last update timestamp |
| `version` | `int` | `1` | Optimistic locking version |

### Property

| Name | Returns | Description |
|------|---------|-------------|
| `stage` | `ProjectStage` | Computed from `status` via `STAGE_MAP` |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `to_dict()` | `dict[str, Any]` | Serialize all fields (enum values as strings) |

### ProjectStatus Enum Values

`DRAFT`, `ACTIVE`, `QUALIFYING`, `MATCHING`, `VISIT_PENDING`, `NEGOTIATING`, `TRANSACTION_PENDING`, `COMPLETED`, `CANCELLED`, `ARCHIVED`

### ProjectType Enum Values

`BUY`, `RENT`, `SELL`, `LIST`, `PUBLISH`, `DOCUMENT_REQUEST`, `COMPLAINT`, `CONSTRUCTION`, `PROFESSIONAL_SERVICE`, `OTHER`

### ProjectStage Enum Values

`INITIAL`, `QUALIFICATION`, `SEARCH`, `VISIT`, `NEGOTIATION`, `TRANSACTION`, `POST_TRANSACTION`, `CLOSED`

---

## 15. Task (Scheduler)

**Module:** `lawim_runtime.scheduler.task`

### TaskPriority Enum Values

| Name | Value | Description |
|------|-------|-------------|
| `CRITICAL` | `0` | Must execute before all others |
| `HIGH` | `1` | High priority |
| `MEDIUM` | `2` | Default priority |
| `LOW` | `3` | Low priority |

### Task Fields (dataclass)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `task_id` | `str` | `""` | Unique task identifier |
| `engine_name` | `str` | `""` | Target engine name |
| `priority` | `TaskPriority` | `MEDIUM` | Execution priority |
| `dependencies` | `list[str]` | `[]` | Task IDs that must complete first |
| `timeout_seconds` | `float` | `30.0` | Maximum execution time |
| `retry_count` | `int` | `0` | Number of retries on failure |
| `metadata` | `dict` | `{}` | Extensible metadata |

---

## 16. Snapshot

**Module:** `lawim_runtime.persistence.snapshot`

### Fields (dataclass)

| Field | Type | Description |
|-------|------|-------------|
| `snapshot_id` | `str` | Auto-generated unique ID |
| `project_id` | `str` | Target project |
| `state` | `dict` | Full project state at snapshot point |
| `version` | `int` | Project version at snapshot |
| `timestamp` | `str` | UTC ISO-8601 |

---

## 17. Error Hierarchy

**Module:** `lawim_runtime.runtime.errors`

| Exception | Parent | Description |
|-----------|--------|-------------|
| `RuntimeError` | `Exception` | Base runtime exception |
| `EventError` | `RuntimeError` | Event processing error |
| `TransitionError` | `RuntimeError` | State transition error |
| `InvalidTransitionError` | `TransitionError` | Disallowed status transition |
| `ProjectNotFoundError` | `RuntimeError` | Project not found in persistence |
| `EngineNotFoundError` | `RuntimeError` | Engine not found in registry |
| `ValidationError` | `RuntimeError` | Data validation failure |
| `PersistenceError` | `RuntimeError` | Storage backend failure |
| `ConcurrencyError` | `RuntimeError` | Optimistic locking conflict |

---

## 18. ConversationRuntimeAdapter

**Module:** `lawim_runtime.services.conversation_adapter`

### Constructor

```python
ConversationRuntimeAdapter(bus: EventBus)
```

### Methods

| Method | Event Emitted | Payload |
|--------|---------------|---------|
| `on_message_received(project_id, actor, message, channel)` | `CONVERSATION_MESSAGE_RECEIVED` | `{"message": ..., "channel": ...}` |
| `on_intent_detected(project_id, actor, intent, confidence)` | `CONVERSATION_INTENT_DETECTED` | `{"intent": ..., "confidence": ...}` |
| `on_slot_updated(project_id, actor, field, value)` | `CONVERSATION_SLOT_UPDATED` | `{"field": ..., "value": ...}` |
| `on_qualification_ready(project_id, actor, qualification)` | `QUALIFICATION_READY` | `qualification` dict directly |

Each method constructs a `RuntimeEvent` and publishes it to the bus. Returns the event.

---

## 19. RuntimeFacade

**Module:** `lawim_runtime.services.runtime_facade`

### Constructor

```python
RuntimeFacade(director: RuntimeDirector)
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `process_event(event_type, project_id, actor, **payload)` | `dict` | Construct a `RuntimeEvent` and delegate to `director.handle_event()` |
| `get_project(project_id)` | `ProjectRuntime \| None` | Retrieve project state (currently returns `None`) |
| `health()` | `dict` | Return `{"status": "ok", "runtime": "LROS", "version": "3.0.0-alpha"}` |

---

## 20. Package Exports

**File:** `lawim_runtime/__init__.py`

```python
__all__ = [
    "RuntimeDirector",
    "RuntimeEvent",
    "ProjectRuntime",
    "RuntimeAPI",
    "EventBus",
    "RuntimeRegistry",
    "RuntimeScheduler",
    "RuntimeStateMachine",
    "RuntimeMetrics",
    "RuntimeAudit",
    "RuntimePersistence",
]
```

All public API components are exported at the package root.
