# LAWIM V2 → V3 Migration Guide

**Last Updated:** 2026-07-22
**Target:** LROS 3.0.0-alpha

---

## 1. Current State (V2 — Conversation-Centric)

The V2 architecture is organized around the `ConversationStateEngine`, which tightly couples:

- Message reception (channel adapters)
- Intent detection (LLM prompt classification)
- Slot extraction (LLM parameter extraction)
- State management (`ConversationState` with slot map)
- Response generation (LLM prompt formulation)
- Handover detection (LLM business decision)

### V2 Pipeline

```
Channel (WhatsApp/Telegram/Web)
  → CommunicationService
    → ConversationStateEngine
      → LLM Provider (OpenAI/DeepSeek/Gemini)
        → Response
```

### V2 Limitations

| Issue | Impact |
|-------|--------|
| **Conversation-scoped state** | No cross-conversation business project tracking |
| **No explicit state machine** | Status is implicit, transitions are ad-hoc |
| **No audit trail** | Cannot reconstruct what happened or why |
| **No telemetry** | No latency, error rates, or throughput visibility |
| **LLM-centric** | Business logic mixed with LLM prompts |
| **No event sourcing** | State is ephemeral, no replay capability |
| **No pluggable engines** | All logic in a single engine class |

---

## 2. Target State (V3 — Project-Centric)

The V3 LROS architecture is organized around the `ProjectRuntime` aggregate, with clear separation of concerns:

- **Events** — immutable, typed, correlated
- **Engines** — pluggable business logic units
- **State machine** — deterministic, enforced transitions
- **Persistence** — abstract storage backend
- **Telemetry** — metrics, audit, timeline
- **API** — single entry point (`RuntimeAPI`)

### V3 Pipeline

```
Channel (WhatsApp/Telegram/Web)
  → RuntimeAPI
    → RuntimeDirector
      → RuntimeScheduler
        → EngineBase[N] (pluggable business logic)
          → ProjectRuntime (state aggregate)
      → Timeline (history)
      → Audit (before/after trail)
      → Metrics (counters, latency)
      → EventBus (pub/sub)
    → Response
```

---

## 3. Migration Phases

### Phase 1: Coexistence (Current — Deployed)

**Goal:** LROS exists alongside V2 with zero impact on existing behavior.

**Actions:**

1. Deploy `lawim_runtime` as a parallel package
2. Wire `ConversationRuntimeAdapter` to the V2 `ConversationStateEngine`
3. V2 publishes events to LROS but does not read from it
4. LROS records all events and builds project state independently
5. Timeline and audit run as shadow observability

**Verification:**

- All existing V2 tests pass unchanged
- V2 responses are identical with or without LROS present
- LROS events are recorded for every message, intent, slot, and qualification
- LROS project state is consistent with V2 conversation state

**Risk:** None. LROS is write-only in this phase.

### Phase 2: Adoption (Build on LROS)

**Goal:** New features are implemented as LROS engines. V2 modules begin consuming LROS data.

**Actions:**

1. All new business logic is written as `EngineBase` implementations
2. `RuntimeFacade` provides V2 modules access to LROS project state
3. V2 reads qualification criteria from LROS instead of its own state
4. Timeline replaces V2 debug logging
5. Engines are registered in `RuntimeRegistry` and ordered via `RuntimeScheduler`

**Verification:**

- New engine tests pass in isolation
- V2 modules using `RuntimeFacade` produce identical results
- Timeline entries match V2 expected state transitions
- Metrics are visible and accurate

**Risk:** Medium. V2 modules must be carefully adapted to read from LROS without breaking existing behavior.

### Phase 3: Cutover

**Goal:** `RuntimeAPI` becomes the primary entry point. V2 pipeline is a downstream consumer of LROS events.

**Actions:**

1. Channel adapters (WhatsApp, Telegram, Web) call `RuntimeAPI.handle_event()` directly
2. V2 `ConversationStateEngine` is refactored into an LROS `EngineBase`
3. V2 response generation is triggered by LROS events, not by direct channel input
4. V2 conversation state rebuilt from LROS event replay
5. Old V2 entry points are deprecated

**Verification:**

- Channel messages produce identical responses through V3 pipeline
- V2 `ConversationStateEngine` produces identical output as an LROS engine
- Event replay from LROS reconstructs identical conversation state
- All V2 tests pass when routed through LROS

**Risk:** High. Requires full regression testing on all channels.

### Phase 4: Optimization

**Goal:** Fully leverage LROS capabilities for performance, reliability, and observability.

**Actions:**

1. `RuntimePersistence` backed by PostgreSQL (replaces in-memory)
2. Event sourcing with periodic `Snapshot` for fast project rebuild
3. Parallel engine execution in `RuntimeScheduler`
4. Circuit breakers for engine failures
5. Engine retry with configurable `Task.retry_count`
6. `RuntimeMetrics` hooks into Prometheus/Grafana
7. `RuntimeAudit` backs up to long-term storage

**Verification:**

- Event replay from PostgreSQL reconstructs project state correctly
- Snapshot-based rebuild is O(1) vs O(n) from full replay
- Parallel engine execution reduces latency proportionally
- Circuit breakers isolate failing engines
- Metrics visible in production dashboards

**Risk:** Medium. Database migration and parallel execution require careful testing.

---

## 4. Adapter Usage

### ConversationRuntimeAdapter

Use when you need to emit LROS events from existing V2 code without modifying it.

```python
from lawim_runtime.events.bus import EventBus
from lawim_runtime.services.conversation_adapter import ConversationRuntimeAdapter

bus = EventBus()
adapter = ConversationRuntimeAdapter(bus)

# Inside V2 engine, after receiving a message:
adapter.on_message_received(
    project_id="abc123",
    actor="user_42",
    message="Je cherche un appartement",
    channel="whatsapp",
)

# After detecting intent:
adapter.on_intent_detected(
    project_id="abc123",
    actor="user_42",
    intent="rental_search",
    confidence=0.95,
)

# After extracting a slot:
adapter.on_slot_updated(
    project_id="abc123",
    actor="user_42",
    field="city",
    value="Douala",
)

# After qualification is complete:
adapter.on_qualification_ready(
    project_id="abc123",
    actor="user_42",
    qualification={"budget": 180000, "bedrooms": 2, "city": "Douala"},
)
```

### RuntimeFacade

Use when V2 modules need to interact with LROS without constructing `RuntimeEvent` objects.

```python
from lawim_runtime import (
    RuntimeDirector, RuntimeAPI, RuntimeFacade,
    EventBus, RuntimeRegistry, RuntimeScheduler,
    RuntimePersistence, RuntimeMetrics, RuntimeAudit,
)
from lawim_runtime.project.timeline import Timeline

# Build the LROS stack
bus = EventBus()
registry = RuntimeRegistry()
scheduler = RuntimeScheduler()
persistence = _YourPersistenceImplementation()
timeline = Timeline()
audit = RuntimeAudit()
metrics = RuntimeMetrics()

director = RuntimeDirector(bus, registry, scheduler, persistence, timeline, audit, metrics)
facade = RuntimeFacade(director)

# Create a project from V2 code
result = facade.process_event(
    "PROJECT_CREATED",
    project_id="",
    actor="v2_adapter",
    project_type="RENT",
    owner="user_42",
)

# Check health
health = facade.health()
```

---

## 5. Backward Compatibility Guarantees

### Data Compatibility

| Item | Guarantee |
|------|-----------|
| V2 conversation state | Unchanged. LROS reads only, never writes V2 state |
| V2 event schema | Same `RuntimeEvent` can be used across V2 and V3 |
| V2 projections | Timeline and audit are additive, never destructive |

### API Compatibility

| LROS API | Backward Compat? | Notes |
|----------|-----------------|-------|
| `RuntimeEvent` | Yes | Extends V2 event concept, same field naming |
| `EventBus` | Yes | New. V2 never used pub/sub |
| `RuntimeDirector` | N/A | New component |
| `RuntimeScheduler` | N/A | New component |
| `RuntimeRegistry` | N/A | New component |
| `RuntimeAPI` | N/A | New entry point |
| `RuntimeFacade` | N/A | Bridge for V2 → V3 |
| `ConversationRuntimeAdapter` | Yes | Emits events only, no V2 dependency |

### Behavioral Guarantees

1. **V2 responses are identical** with or without LROS in the write-only phase
2. **LROS does not modify V2 state** — it builds its own `ProjectRuntime` from events
3. **LROS does not call LLMs** — no prompt costs from LROS alone
4. **LROS event publishing is synchronous** — no async race conditions with V2
5. **LROS errors are isolated** — `RuntimeDirector` wraps engine failures; V2 continues unaffected

---

## 6. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| V2 regression | Low | High | Write-only phase. LROS does not modify V2 state. Full V2 test suite passes |
| Performance overhead | Low | Medium | LROS adds ~1ms per event in-memory. Pluggable persistence can add latency |
| Event flooding | Low | Medium | `EventBus` is synchronous. Consider async dispatch in Phase 4 |
| LLM cost duplication | Low | High | LROS does not call LLMs. Only V2 pipeline triggers LLM costs |
| State divergence | Medium | High | Phase 1 validates LROS project state matches V2 conversation state continuously |
| Data loss on restart | Medium | High | In-memory persistence loses state. SQL persistence planned in Phase 4 |
| Engine circular dependency | Low | Medium | `RuntimeScheduler` is single-pass ordered. Engines cannot recurse |
| Migration incomplete | Low | High | Each phase has a clear verification gate. Rollback documented for each phase |

---

## 7. Rollback Plan

### Rollback from Phase 1 (Coexistence)

- Remove `ConversationRuntimeAdapter` wiring from V2 engine
- Remove `lawim_runtime` from deployment
- V2 pipeline operates unchanged
- No data loss (LROS was write-only)

### Rollback from Phase 2 (Adoption)

- Revert V2 modules to read from their own state instead of `RuntimeFacade`
- Disable new `EngineBase` implementations
- Timeline and audit data is preserved but not actively used

### Rollback from Phase 3 (Cutover)

- Restore V2 channel adapters as primary entry points
- Demote `RuntimeAPI` to advisory
- V2 `ConversationStateEngine` resumes direct processing
- LROS continues as shadow pipeline for re-validation

### Rollback from Phase 4 (Optimization)

- Switch `RuntimePersistence` back to in-memory
- Revert to sequential engine execution
- Disable circuit breakers and retry

---

## 8. Verification Checklist

### Phase 1

- [ ] All V2 tests pass (519 tests, 0 failed)
- [ ] LROS 38 tests pass (0 failed)
- [ ] `ConversationRuntimeAdapter` emits correct events
- [ ] Timeline entries match V2 expected state
- [ ] Audit entries capture before/after correctly

### Phase 2

- [ ] New `EngineBase` implementations pass unit tests
- [ ] V2 modules receive correct data from `RuntimeFacade`
- [ ] Metrics counters match expected values
- [ ] Engine execution order matches `RuntimeScheduler.set_order()`

### Phase 3

- [ ] Channel messages produce identical responses via `RuntimeAPI`
- [ ] V2 `ConversationStateEngine` as LROS engine produces identical output
- [ ] Event replay reconstructs identical project state
- [ ] All 519 V2 tests pass through LROS pipeline

### Phase 4

- [ ] PostgreSQL persistence passes all load/save/replay tests
- [ ] Snapshot rebuild is O(1) for any event count
- [ ] Parallel engine execution reduces latency
- [ ] Circuit breakers trigger on configured failure threshold
- [ ] Metrics visible in production dashboard
