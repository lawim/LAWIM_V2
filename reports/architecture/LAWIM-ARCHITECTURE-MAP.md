# LAWIM — Architecture Map

**Version:** 3.0.0-alpha
**Last Updated:** 2026-07-22
**Status:** CANONICAL

---

## 1. End-to-End Flow

```
Channel (WhatsApp/Telegram/Web)
  -> InteractionGateway (normalize, authenticate, route)
    -> ExtractionEngine (LLM-based: intent, slots, language)
      -> CandidateUpdate / ProfilePatch
        -> ProjectProfile (single source of business truth)
          -> QualificationEngine (validate criteria, score readiness)
            -> ProjectBrain / DecisionEngine (select next action)
              -> DecisionResult (action recommendation)
                -> ActionExecutionEngine (execute with idempotency)
                  -> Domain Runtime Engine (domain business logic)
                    -> Runtime Events (timeline, audit, metrics)
                      -> ProjectBrain Re-evaluation (state-dependent)
                        -> ResponsePlan (plan the response)
                          -> ResponseWriter (LLM formulates)
                            -> Channel (deliver to user)
```

---

## 2. Layer Breakdown

### 2.1 Channel Layer

**Responsibilities:**
- Message reception and delivery (WhatsApp via Green API, Telegram via Bot API, Web via HTTP)
- Webhook authentication and idempotency
- Message normalization into internal format
- Channel-specific formatting (markdown, HTML, plain text)

**Key classes:**
- `CommunicationService` (V2)
- `WhatsAppAdapter`, `TelegramAdapter`, `WebAdapter`
- Channel-specific webhook handlers

**Constraints:**
- Channels MUST NOT contain business logic
- Channels MUST NOT call LLMs directly
- Channels MUST NOT persist state
- Webhooks MUST be idempotent
- Footer appended only for WhatsApp and Telegram (not Web)

---

### 2.2 InteractionGateway

**Responsibilities:**
- Actor resolution (User lookup or provisional profile)
- Conversation resolution (existing or new conversation)
- Cross-channel identity resolution (same user across channels)
- Message normalization (language detection, content cleaning)
- Correlation ID generation and propagation

**Key classes:**
- `ConversationResolver`
- `CrossChannelIdentityResolver`
- `ConversationStateRepository`

**Constraints:**
- Every message MUST have a `correlation_id`
- Unknown actors get a provisional profile
- Cross-channel identity requires explicit consent (PENDING -> GRANTED)

---

### 2.3 ExtractionEngine (LLM-based)

**Responsibilities:**
- Intent classification from natural language
- Slot/criterion extraction (city, budget, property type, etc.)
- Language detection
- Re-phrasing and greeting detection
- Handover detection

**Key classes:**
- `IntentDetector`
- `SlotExtractor`
- `LanguageDetector`
- `HandoverEvaluator`

**Constraints:**
- LLM performs extraction ONLY — no business decisions
- Extraction output is a `CandidateUpdate` — never written directly to profile
- Single foreign word does NOT change conversation language

---

### 2.4 CandidateUpdate / ProfilePatch

**Responsibilities:**
- Merge extracted candidates into ProjectProfile via deterministic MergeEngine
- Track provenance, confidence, and status (CANDIDATE, CONFIRMED, REJECTED, SUPERSEDED, CONFLICTED, UNKNOWN)
- Detect and flag conflicts
- Update completeness score

**Key classes:**
- `CandidateUpdate`
- `ProfilePatch`
- `MergeEngine`
- `ConflictResolution`
- `CompletenessCalculator`

**Constraints:**
- Profile is the single source of truth — no parallel business state
- Every update records a history snapshot
- Conflicts require resolution before progression

---

### 2.5 ProjectProfile

**Responsibilities:**
- Single source of business truth
- Structured versioned fields with type, value, normalized value, confidence, provenance, status
- Field registry enforcement (types, requirements, constraints)
- Completeness scoring

**Key classes:**
- `ProjectProfile`
- `FieldRegistry`
- `FieldDefinitions`
- `HistorySnapshots`

**Constraints:**
- No component other than ProjectProfile owns authoritative business state
- Profile is typed per project type (rental_search, purchase_search, sale_project, etc.)

---

### 2.6 QualificationEngine

**Responsibilities:**
- Evaluate ProjectProfile against registered requirements
- Produce QualificationResult: score, level, blockers, warnings
- Determine qualification readiness

**Key classes:**
- `QualificationEngine`
- `RequirementRegistry`
- `RuleEvaluator`

**Constraints:**
- Qualification level must be computed, not LLM-assigned
- Blockers prevent progression until resolved
- Qualification level drives decision selection

---

### 2.7 ProjectBrain / DecisionEngine

**Responsibilities:**
- Consume QualificationResult
- Select next action category: COLLECTION, QUALIFICATION, CONFIRMATION, MATCHING, HANDOVER, WAIT
- Set next_action on ProjectRuntime
- Evaluate human handover requirements

**Key classes:**
- `ProjectBrain`
- `DecisionEngine`
- `HumanHandoverEvaluator`
- `ActionRegistry`
- `Guards`

**Constraints:**
- Decision is deterministic — same profile, same decision
- Handover requires persistent handover_id and valid reason
- No handover triggered by greetings or ordinary requests

---

### 2.8 DecisionResult

**Responsibilities:**
- Carry the decision from ProjectBrain to ActionExecutionEngine
- Include action, category, priority, confidence, reasoning, metadata

**Key classes:**
- `DecisionResult`

**Constraints:**
- Every DecisionResult must map to a registered ActionHandler or be recorded as HANDLER_NOT_IMPLEMENTED

---

### 2.9 ActionExecutionEngine

**Responsibilities:**
- Execute business actions with full reliability guarantees
- Idempotency management (at-most-once execution)
- Locking and leasing (prevent concurrent execution)
- Retry with configurable policy and backoff
- Recovery for stalled/failed executions
- Dead letter queue for persistently failing actions
- Compensation for rollback on failure
- Outbox pattern for reliable event publication

**Key classes:**
- `ExecutionEngine`
- `ExecutionDispatcher`
- `ActionHandlerRegistry`
- `IdempotencyManager`
- `ActionLockManager`
- `ActionLeaseManager`
- `RetryPolicy`
- `RecoveryManager`
- `DeadLetterQueue`
- `CompensationEngine`
- `Outbox`

**Execution states:**
PENDING -> STARTED -> VALIDATED -> PREPARED -> EXECUTING -> COMPLETED -> VERIFIED
                                                    |-> FAILED -> COMPENSATED
                                                    |-> TIMEOUT -> CANCELLED

**Constraints:**
- Every action MUST have an IdempotencyKey
- Execution MUST be audited per attempt
- Shadow mode MUST be supported (no real side effects)
- DOMAIN_RUNTIME_REQUIRED status when handler needs a Domain Runtime Engine

---

### 2.10 Domain Runtime Engine

**Responsibilities:**
- Execute domain-specific business logic
- Implement EngineBase contract for LROS integration
- Manage domain state machine, validation, event contracts

**Planned engines:**
| Engine | Domain |
|--------|--------|
| MatchingEngine | Score and rank properties against criteria |
| VisitEngine | Plan, confirm, and track property visits |
| CRMEngine | Contact management, lead pipeline, follow-up |
| NotificationEngine | Template-based message delivery |
| DocumentEngine | Document lifecycle and GED integration |
| VerificationEngine | Identity, property, document verification |
| TransactionEngine | Transaction step tracking |
| PaymentEngine | Payment processing via Financial Core + Campay |

**Constraints:**
- Each engine extends EngineBase
- Each engine registers with RuntimeRegistry
- Engines execute within RuntimeScheduler ordering
- Engines are channel-independent and LLM-independent

---

### 2.11 LROS Runtime (Kernel)

**Responsibilities:**
- Event processing and routing (RuntimeAPI -> RuntimeDirector)
- Ordered engine execution (RuntimeScheduler)
- Engine lifecycle management (RuntimeRegistry)
- State machine enforcement (RuntimeStateMachine)
- Persistence abstraction (RuntimePersistence)
- Timeline recording
- Audit trail (before/after snapshots)
- Metrics collection
- EventBus pub/sub

**Key classes:**
- `RuntimeAPI`
- `RuntimeDirector`
- `RuntimeScheduler`
- `RuntimeRegistry`
- `RuntimeStateMachine`
- `RuntimePersistence`
- `Timeline`
- `RuntimeAudit`
- `RuntimeMetrics`
- `EventBus`
- `ProjectRuntime`

**Constraints:**
- LROS has zero knowledge of channels (WhatsApp, Telegram, Web)
- LROS does not import or reference any LLM provider
- LROS is deterministic — same events produce same state
- All state changes are immutable and audited

---

### 2.12 ResponsePlan / ResponseWriter

**Responsibilities:**
- Produce a ResponsePlan from engine output (V2) or decision result (V3)
- Define next question text, maximum questions, required slots
- Generate natural language response via LLM
- Validate response against ResponsePlan (forbidden content, question count)
- Append canonical footer

**Key classes:**
- `ResponsePlan`
- `AIOrchestrator`
- `ConversationResponseValidator`
- `ControlledGenerationRequest`

**Constraints:**
- Maximum one question per response
- Footer max 10 words (FR: verifiez infos importantes)
- Footer error must NEVER block main response
- Response must pass validator before delivery

---

## 3. V2 Compatibility Layer

```
V2 Pipeline (current production):
Channel -> CommunicationService -> ConversationStateEngine -> AIOrchestrator -> Response

V2 Adapter (shadow migration):
V2 ConversationStateEngine -> ConversationRuntimeAdapter -> LROS EventBus
                                                              LROS records events, no effect on V2

V3 Pipeline (target):
Channel -> RuntimeAPI -> RuntimeDirector -> EngineBase[N] -> ProjectRuntime -> ResponsePlan -> Response
```

### V2 Adapter Components

| Component | Role |
|-----------|------|
| ConversationRuntimeAdapter | Emits LROS events when V2 detects messages, intents, slots, qualification readiness |
| RuntimeFacade | Simplified LROS access for V2 modules |

### Shadow Migration Path

```
Phase 1 (Current) — Coexistence:
  V2 operates unchanged. LROS is write-only, recording events in parallel.
  V2 does not read from LROS. Risk: None.

Phase 2 — Adoption:
  New features built as LROS EngineBase. V2 reads qualification from LROS.

Phase 3 — Cutover:
  Channel adapters call RuntimeAPI directly. V2 engine becomes an LROS EngineBase.

Phase 4 — Optimization:
  PostgreSQL persistence, parallel execution, circuit breakers, observability stack.
```

---

## 4. Key Architecture Diagrams

### Program Dependencies

```
Program A (LROS Foundation)
  |
  v
Program B (ProjectProfile)
  |
  v
Program C (Qualification + Decision)
  |
  v
Program C.5 (Action Execution)
  |
  v
Program D (Domain Runtime Engines)
  |
  v
Programs E-N (Future)
```

### Data Flow (V3 Target)

```
User Message
  |
  v
RuntimeEvent (event_type, project_id, actor, payload)
  |
  v
RuntimeAPI.handle_event()
  |
  v
RuntimeDirector.handle_event()
  |-- load ProjectRuntime
  |-- capture before-state
  |-- RuntimeScheduler.execute(engines)
  |-- capture after-state
  |-- persist project + event
  |-- record timeline + audit
  |-- publish to EventBus
  |
  v
ResponsePlan -> ResponseWriter -> Channel
```
