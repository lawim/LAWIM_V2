# LAWIM — Canonical Glossary (Architecture Terms)

**Version:** 3.0.0-alpha
**Last Updated:** 2026-07-22
**Status:** CANONICAL

---

## Terms

### LAWIM
- **Definition:** Intelligent real estate platform for Cameroon. LAWIM structures, qualifies, searches, matches, accompanies, and tracks real estate projects persistently.
- **Context:** Project name, platform identity, legal entity.
- **Aliases:** None.

### LROS (Lawim Runtime Operating System)
- **Definition:** Event-driven, project-centric kernel orchestrator for all V3 operations. LROS has zero knowledge of channels or LLM providers.
- **Context:** Architecture (V3), kernel layer.
- **Aliases:** Runtime, Runtime Kernel.

### ProjectProfile
- **Definition:** Single source of truth for all business data in V3. Holds structured, versioned fields with provenance, status, and confidence. Updated via ProfilePatch operations and resolved by the deterministic MergeEngine.
- **Context:** Program B, business truth layer.
- **Aliases:** Profile, Business Profile.

### ProjectBrain
- **Definition:** Qualification and decision authority. Composes QualificationEngine, DecisionEngine, and HumanHandoverEvaluator. Determines intent, state, and next action.
- **Context:** Program C, decision layer.
- **Aliases:** Brain, Decision Authority.

### ActionExecutionEngine
- **Definition:** Reliable execution authority for business actions. Provides idempotency, locking, leasing, retry, recovery, compensation, dead letter queue, and outbox pattern guarantees.
- **Context:** Program C.5, execution layer.
- **Aliases:** ExecutionEngine, Executor.

### Domain Runtime Engine
- **Definition:** Pluggable EngineBase implementation that executes business logic for a specific domain (matching, visits, CRM, notifications, documents, verification, transactions, payments).
- **Context:** Program D, domain layer.
- **Aliases:** Domain Engine, Engine.

### DecisionResult
- **Definition:** Action recommendation produced by ProjectBrain (DecisionEngine). Contains selected action, action category, priority, confidence, reasoning, and metadata.
- **Context:** Program C, decision output.
- **Aliases:** Action Recommendation, Decision.

### ActionHandler
- **Definition:** Contract for an executable business action. Defines validation, preparation, execution, verification, and optional compensation steps. Registered with ActionHandlerRegistry.
- **Context:** Program C.5, action contract.
- **Aliases:** Handler, Action Contract.

### ConversationState
- **Definition:** Session-level state for V2 conversation runtime. Tracks intent, extracted slots, language, conversation history, and handover status. Scoped to a single conversation, not a business project.
- **Context:** V2 runtime, conversation layer.
- **Aliases:** Session State, V2 State.

### Slot
- **Definition:** Extracted criterion from user message (e.g., city, budget, property type, bedrooms). Carries field name, value, confidence, provenance, and status.
- **Context:** V2 extraction, V3 qualification.
- **Aliases:** Criterion, Field, Extract.

### QualificationEngine
- **Definition:** Evaluates a ProjectProfile against registered requirements. Produces QualificationResult with score, qualification level, blockers, and warnings.
- **Context:** Program C, qualification layer.
- **Aliases:** Qualifier, Requirement Evaluator.

### Orchestrator
- **Definition:** AI provider orchestrator for V2 response generation. Manages provider selection, timeouts, retries, circuit breakers, and fallback across DeepSeek, OpenAI, and Gemini.
- **Context:** V2 conversation runtime, AI layer.
- **Aliases:** ProviderOrchestrator, AI Orchestrator.

### RuntimeDirector
- **Definition:** Central orchestrator of LROS. Every runtime event flows through RuntimeDirector.handle_event(). Coordinates persistence, timeline, audit, metrics, scheduler, and event publication.
- **Context:** Program A, LROS core.
- **Aliases:** Director.

### RuntimeRegistry
- **Definition:** Engine discovery and lifecycle management for LROS. Engines register by name and are resolved at runtime by the scheduler.
- **Context:** Program A, LROS core.
- **Aliases:** Registry.

### ResponsePlan
- **Definition:** Action plan produced by the V2 ConversationStateEngine. Defines the next response, maximum questions, required slots, and suggested action. Must be validated before provider delivery.
- **Context:** V2 conversation runtime.
- **Aliases:** Plan, Response Action Plan.

### ConversationResponseValidator
- **Definition:** Validates generated responses against the ResponsePlan. Checks for forbidden content, question count enforcement, and identity compliance. Replaces or blocks invalid responses.
- **Context:** V2 conversation runtime.
- **Aliases:** ResponseValidator, Validator.

### FeatureFlag
- **Definition:** Auditable activation switch for platform capabilities. Controls feature rollout, shadow mode, and provider selection without code deployment.
- **Context:** Platform infrastructure.
- **Aliases:** Feature Toggle, Flag.

### ShadowMode
- **Definition:** Safe execution mode where V3 engines process events without modifying production state or triggering real side effects. V2 remains the system of record during migration.
- **Context:** V2-to-V3 migration.
- **Aliases:** Observability Mode, Read-Only Mode.

### V2 Adapter
- **Definition:** Bridge between V2 production components and V3 LROS. Includes ConversationRuntimeAdapter (emits LROS events from V2 engine) and RuntimeFacade (simplified LROS access for V2 modules).
- **Context:** Migration, compatibility layer.
- **Aliases:** Adapter, Bridge.

### Program A
- **Definition:** LROS Foundation. Event-driven, project-centric kernel for V3. Implements RuntimeAPI, RuntimeDirector, RuntimeScheduler, RuntimeRegistry, RuntimeStateMachine, RuntimePersistence, Timeline, RuntimeAudit, RuntimeMetrics, EventBus, ProjectRuntime, EngineBase.
- **Context:** Completed programs.
- **Aliases:** LROS Foundation.

### Program B
- **Definition:** Project Profile and Field Registry. Implements ProjectProfile, FieldRegistry, FieldDefinitions, ProfilePatch, MergeEngine, ConflictResolution, HistorySnapshots, CompletenessCalculator, Normalizers, Validators.
- **Context:** Completed programs.
- **Aliases:** Project Profile.

### Program C
- **Definition:** Qualification and Decision Engine. Implements QualificationEngine, RequirementRegistry, DecisionEngine, ProjectBrain, HumanHandoverEvaluator, ActionRegistry, RuleEvaluator, Guards.
- **Context:** Completed programs.
- **Aliases:** Qualification and Decision.

### Program C.5
- **Definition:** Action Execution Engine. Implements ExecutionEngine, ExecutionDispatcher, ActionHandlerRegistry, IdempotencyManager, ActionLockManager, ActionLeaseManager, ExecutionVerifier, AuditTrail, EventCollector, MetricsCollector, ExecutionWorker, RetryPolicy, RecoveryManager, DeadLetterQueue, Outbox, Snapshots, Timeout, Compensation.
- **Context:** Completed programs (with baseline verification pending).
- **Aliases:** Action Execution.

### Program D
- **Definition:** Domain Runtime Engines. Pluggable EngineBase implementations for Matching, Visits, CRM, Notifications, Documents, Verification, Transactions, Payments.
- **Context:** In-progress programs.
- **Aliases:** Domain Engines.

### ADR (Architecture Decision Record)
- **Definition:** Documented architecture decision with context, options considered, decision rationale, and consequences. Stored in docs/adr/.
- **Context:** Governance, documentation.
- **Aliases:** Architecture Decision Record.

### L0-L8 Validation Levels
- **Definition:** Validation maturity scale from code presence (L0) to business certification (L8). Each level requires specific evidence. Forbidden equivalences are documented.
- **Context:** Quality assurance, acceptance.
- **Aliases:** Validation Levels, Maturity Levels.

### PREEXISTING_CONFIRMED
- **Definition:** Status for known test failures that existed before a program's changes. These failures are documented, reproduced, and accepted as pre-existing — not caused by the current work.
- **Context:** Testing, baseline verification.
- **Aliases:** Pre-existing Failure, Known Failure.

### SIMULATED_SUCCESS
- **Definition:** A test passes using simulated (mock) external dependencies. This proves code correctness but does NOT prove real integration.
- **Context:** Testing, quality assurance.
- **Aliases:** Mock Success, Simulated Pass.

### DOMAIN_RUNTIME_REQUIRED
- **Definition:** Status indicating that a domain-level engine (Program D) must be implemented before the action can be executed in production. The LROS and ActionExecutionEngine infrastructure is ready, but the specific domain handler is not yet registered.
- **Context:** Program C.5, execution planning.
- **Aliases:** Domain Pending, Engine Required.

### HANDLER_NOT_IMPLEMENTED
- **Definition:** Status indicating that a specific ActionHandler contract has been defined but the implementation does not yet exist in the ActionHandlerRegistry.
- **Context:** Program C.5, action registry.
- **Aliases:** Handler Missing, Not Implemented.

### DeadLetterQueue
- **Definition:** Persistent storage for actions that have exhausted all retry attempts. Actions in the DLQ require manual inspection and intervention.
- **Context:** Program C.5, reliability.
- **Aliases:** DLQ.

### IdempotencyKey
- **Definition:** Unique key derived from action type and input parameters. Guarantees that an action is executed at most once. Repeated submissions with the same key are safely ignored.
- **Context:** Program C.5, idempotency.
- **Aliases:** Idempotency Token, Dedup Key.

### CompensationEngine
- **Definition:** Executes compensation (rollback) actions for failed or cancelled executions. Maintains a compensation stack with ordered rollback steps.
- **Context:** Program C.5, reliability.
- **Aliases:** Compensator, Rollback Engine.

### ExecutionState Machine
- **Definition:** Deterministic state machine for action execution lifecycle. Statuses: PENDING, STARTED, VALIDATED, PREPARED, EXECUTING, COMPLETED, VERIFIED, FAILED, COMPENSATED, TIMEOUT, CANCELLED.
- **Context:** Program C.5, execution model.
- **Aliases:** Execution Status Machine.

### MATCH_FOUND
- **Definition:** Decision result indicating that one or more property matches satisfy the qualified criteria. Triggers the matching workflow.
- **Context:** Qualification, decision.
- **Aliases:** Match Success.

### NO_MATCH
- **Definition:** Decision result indicating that no properties satisfy the qualified criteria. Triggers criteria adjustment or alternative suggestions.
- **Context:** Qualification, decision.
- **Aliases:** No Results.

### INSUFFICIENT_DATA
- **Definition:** Decision result indicating that not enough criteria have been collected to perform a meaningful search or action. Triggers additional qualification questions.
- **Context:** Qualification, decision.
- **Aliases:** Needs More Info, Incomplete.

### PaymentIntent
- **Definition:** Financial operation record representing a planned or executed payment. Tracks amount, currency, provider, status, and reconciliation state.
- **Context:** Financial Core, payments.
- **Aliases:** Payment Record.

### Outbox
- **Definition:** Reliable event publication pattern. Events are written to an outbox table in the same transaction as state changes, then asynchronously published to the EventBus. Guarantees at-least-once delivery.
- **Context:** Program C.5, reliability.
- **Aliases:** Outbox Pattern, Event Outbox.
