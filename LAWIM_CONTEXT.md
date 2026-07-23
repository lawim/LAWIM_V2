# LAWIM Context — Comprehensive Project Reference

**Version:** 3.0.0-alpha
**Last Updated:** 2026-07-23
**HEAD:** 8cf36b8a
**Branch:** feature/action-execution-engine-20260722
**Repository:** git@github-lawim:lawim/LAWIM_V2.git

---

## 1. Identity

LAWIM is an intelligent real estate platform for Cameroon. It is NOT a chatbot. LAWIM understands, structures, qualifies, searches, matches, accompanies, and tracks real estate projects persistently.

LAWIM n'est pas un chatbot. LAWIM est une plateforme immobiliere intelligente et operationnelle pour le Cameroun.

LAWIM handles requests directly: buying, selling, renting, listing, publishing, searching, qualifying, matching, planning visits, preparing transactions, managing documents, explaining payments, handling claims, and providing follow-up.

LAWIM does not redirect users to external platforms. All real estate needs within its scope are processed using its own properties, services, search engine, matching engine, CRM, agents, workflows, and document resources.

---

## 2. Business Vision

LAWIM transforms informal real estate requests into manageable, persistent projects. Every interaction feeds a structured project profile with verified criteria, traceable decisions, explicit consent, and operational follow-up.

The platform manages the full lifecycle:
- Prospect discovery and qualification
- Property search and matching
- Visit scheduling and transaction preparation
- Document management and payment processing
- Post-transaction follow-up and claims

A conversation does not constitute a project. A project is the persistent business entity. Conversations are ephemeral transport channels that feed into projects.

---

## 3. Problems Solved

| Problem | Solution |
|---------|----------|
| Lack of trust in real estate transactions | Structured project profiles, verified criteria, audit trail |
| No persistent follow-up | Project-centric model with state machines and timeline |
| Informal requests lost across channels | Cross-channel identity resolution, persistent project state |
| LLM deciding business logic | Separation: LLM extracts/formulates, engine decides |
| No traceability | Immutable events, before/after audit, timeline |
| Channel lock-in | Channel-independent runtime, adapters are transport only |
| Fragmented data | Single source of truth: ProjectProfile |
| No execution reliability | ActionExecutionEngine with idempotency, recovery, retry |

---

## 4. Actors

| Actor | Description |
|-------|-------------|
| Visitor | Unauthenticated person consulting or initiating a request |
| User | Authenticated LAWIM identity |
| Client | User engaged in a tracked project |
| Owner | Property holder or authorized representative |
| Seller | Actor offering a property for sale |
| Landlord | Actor offering a property for rent |
| Buyer | Client seeking to purchase |
| Tenant | Client seeking to rent |
| Investor | Client seeking returns, land, buildings, or opportunities |
| LAWIM Agent | Internal authorized staff for follow-up, arbitration, escalation |
| Real Estate Agent | External verified professional or partner |
| Agency | Organization of agents and mandates |
| Partner | Organization or person referenced by LAWIM |
| Professional | Architect, engineer, technician, notary, or other service provider |
| Notary | External legal officer — LAWIM never substitutes for a notary |

---

## 5. Architectural Principles

1. **Project-centric, not conversation-centric.** Conversations are ephemeral; projects are persistent.
2. **Event-driven.** Every operation is triggered by an immutable, typed, correlated event.
3. **Channel-independent.** The runtime (LROS) has zero knowledge of WhatsApp, Telegram, or Web transport. Channels are adapters.
4. **LLM as formatter only.** The LLM performs extraction, classification, reformulation, and response writing. It NEVER makes business decisions.
5. **Deterministic state machine.** Given the same events, the system produces the same state. No LLM path-dependent state drift.
6. **Pluggable engines.** Business logic lives in EngineBase implementations registered at runtime.
7. **Auditable.** Every state change is recorded with before/after snapshots.
8. **No silent failures.** Every error must be logged (without secrets) and handled.
9. **Separation of concerns.** The business engine determines intent, state, and next action. The LLM only formulates the response.
10. **Single source of truth.** ProjectProfile is the authoritative business state.

---

## 6. Architecture V2 (Current Production)

The V2 architecture is conversation-centric. It couples message reception, intent detection, slot extraction, state management, response generation, and handover detection into a single pipeline.

### V2 Pipeline
```
Channel (WhatsApp/Telegram/Web)
  -> CommunicationService
    -> ConversationStateEngine
      -> LLM Provider (OpenAI/DeepSeek/Gemini)
        -> Response
```

### V2 Limitations
- Conversation-scoped state — no cross-conversation business project tracking
- No explicit state machine — status is implicit, transitions are ad-hoc
- No audit trail — cannot reconstruct what happened or why
- No telemetry — no latency, error rates, or throughput visibility
- LLM-centric — business logic mixed with LLM prompts
- No event sourcing — state is ephemeral, no replay capability
- No pluggable engines — all logic in a single engine class

V2 remains operational during the V3 shadow migration. V3 does not modify V2 state.

---

## 7. Architecture V3 (Target with LROS)

The V3 architecture is project-centric and event-driven, built on the LAWIM Runtime Operating System (LROS).

### V3 Pipeline
```
Channel (WhatsApp/Telegram/Web)
  -> RuntimeAPI
    -> RuntimeDirector
      -> RuntimeScheduler
        -> EngineBase[N] (pluggable business logic)
          -> ProjectRuntime (state aggregate)
      -> Timeline (history)
      -> Audit (before/after trail)
      -> Metrics (counters, latency)
      -> EventBus (pub/sub)
    -> Response
```

### Core LROS Components

| Component | Role |
|-----------|------|
| RuntimeAPI | Single entry point for external callers |
| RuntimeDirector | Central orchestrator for all event processing |
| RuntimeScheduler | Orders and executes registered engines |
| RuntimeRegistry | Engine discovery and lifecycle management |
| RuntimeStateMachine | Deterministic state machine for project transitions |
| RuntimePersistence | Abstract storage backend (in-memory, PostgreSQL planned) |
| Timeline | Project historical truth with before/after snapshots |
| RuntimeAudit | Complete before/after audit trail |
| RuntimeMetrics | Telemetry counters and latency measurement |
| EventBus | Pub/sub with history replay capability |
| ProjectRuntime | Central state aggregate for each project |

### Project Statuses
DRAFT, ACTIVE, QUALIFYING, MATCHING, VISIT_PENDING, NEGOTIATING, TRANSACTION_PENDING, COMPLETED, CANCELLED, ARCHIVED

### Project Types
BUY, RENT, SELL, LIST, PUBLISH, DOCUMENT_REQUEST, COMPLAINT, CONSTRUCTION, PROFESSIONAL_SERVICE, OTHER

### Project Stages
INITIAL, QUALIFICATION, SEARCH, VISIT, NEGOTIATION, TRANSACTION, POST_TRANSACTION, CLOSED

---

## 8. Sources of Truth

The single source of truth for all LAWIM V3 operations is the **ProjectProfile**.

- ProjectProfile holds structured, versioned business fields with provenance and status
- FieldRegistry defines all valid fields, their types, requirements, and constraints
- The deterministic merge engine resolves concurrent updates with conflict detection
- History snapshots preserve the evolution of every profile
- No other component owns authoritative business state

Additional authoritative sources:
- RuntimeAudit — immutable before/after trail of all state changes
- Timeline — project historical truth with event replay capability
- EventBus event history — append-only record of all events

---

## 9. Role of LLM

The LLM (OpenAI, DeepSeek, Gemini) is a linguistic capability, NOT a business decision-maker.

### Allowed
- Linguistic extraction (intent, slots, criteria from natural language)
- Reformulation and summarization
- Response drafting and natural language generation
- Intent classification
- Translation
- Explainability assistance

### Forbidden
- Possessing business rules
- Writing directly to canonical memory
- Making business decisions
- Creating relationships
- Authorizing payments
- Sharing private data
- Bypassing feature flags
- Determining conversation state or project status
- Choosing the next business action

A message does not constitute a decision. A decision does not constitute an execution. The engine decides, the LLM formulates.

---

## 10. Role of Channels

Channels (WhatsApp, Telegram, Web, Email) are **transport adapters only**.

### Rules
- A channel possesses NO business logic, decision authority, memory, qualification, matching, relationship, or autonomous response capability
- Channel identity is linked to a User or provisional profile
- Channel verification is required before sensitive actions
- Webhooks are idempotent
- Incoming messages are normalized before processing
- Cross-channel continuity preserves state without loss
- Human handover is coherent across channels

### Supported Channels
- Web (React SPA)
- WhatsApp (Green API)
- Telegram (Bot API)
- Mobile (React Native — planned)
- API REST

---

## 11. Role of LROS (Kernel Orchestrator)

The LAWIM Runtime Operating System (LROS) is the kernel orchestrator for all V3 operations.

### Responsibilities
- Event processing and routing via RuntimeDirector
- Ordered engine execution via RuntimeScheduler
- Engine lifecycle management via RuntimeRegistry
- Deterministic state machine enforcement via RuntimeStateMachine
- Event sourcing, timeline, and audit trail
- Metrics collection and telemetry
- Pub/sub event distribution via EventBus
- Project lifecycle management via ProjectRuntime

### Non-responsibilities
- LROS has zero knowledge of WhatsApp, Telegram, or Web transport
- LROS does not import or reference OpenAI, DeepSeek, or Gemini
- LROS does not make business decisions (delegated to engines)
- LROS does not generate natural language responses

---

## 12. Role of ProjectProfile (Structured Business Truth)

ProjectProfile is the single source of truth for all business data in V3.

### Features
- Structured fields with type, value, normalized value, confidence, provenance, and status
- FieldValueStatus: CANDIDATE, CONFIRMED, REJECTED, SUPERSEDED, CONFLICTED, UNKNOWN
- Deterministic merge engine with conflict detection and resolution strategies
- Field registry defining all valid fields with requirements, types, and constraints
- Field definitions for each project type (rental_search, purchase_search, sale_project, construction_project, land_project)
- Completeness scoring based on requirement weights
- History snapshots at configurable intervals
- Profile patch operations for incremental updates
- Normalizers for value standardization
- Validators for business rule enforcement

---

## 13. Role of ProjectBrain (Qualification + Decision Authority)

ProjectBrain is the qualification and decision authority in V3.

### Components
- **QualificationEngine** — evaluates a ProjectProfile against requirements and produces a QualificationResult with score, level, blockers, warnings
- **DecisionEngine** — consumes QualificationResult and selects the next action (ASK_MISSING_FIELD, START_MATCHING, RESOLVE_CONFLICT, INSUFFICIENT_DATA, WAIT)
- **HumanHandoverEvaluator** — determines if human intervention is required based on profile state and user message

### Qualification Levels
UNQUALIFIED, MINIMAL, PARTIAL, SUBSTANTIAL, QUALIFIED, ACTION_READY

### Decision Categories
COLLECTION, QUALIFICATION, CONFIRMATION, MATCHING, HANDOVER, WAIT

ProjectBrain determines intent, state, and next action. The LLM only formulates the response.

---

## 14. Role of ActionExecutionEngine (Reliable Execution)

ActionExecutionEngine provides reliable execution of business actions with idempotency, recovery, and retry.

### Features
- Action execution with validation, preparation, execution, verification, and optional compensation
- Idempotency management to prevent duplicate execution
- Action locking with distributed lock support
- Action leasing with timeout-based lease management
- Execution state machine with defined transitions
- Audit trail for every execution attempt
- Metrics collection for execution duration, success/failure counts
- Event publishing for execution lifecycle events
- Retry policy with configurable max attempts and backoff
- Recovery mechanism for stalled or failed executions
- Dead letter queue for persistently failing actions
- Outbox pattern for reliable event publication
- Snapshot management for execution state persistence
- Timeout enforcement per action
- Verification hooks for post-execution validation
- Compensation support for failure rollback
- Shadow mode for safe execution without real side effects

### Execution Statuses
PENDING, STARTED, VALIDATED, PREPARED, EXECUTING, COMPLETED, VERIFIED, FAILED, COMPENSATED, TIMEOUT, CANCELLED

---

## 15. Role of Domain Runtime Engines (Program D)

Domain Runtime Engines are pluggable EngineBase implementations that execute business logic for specific domains.

### Planned Domain Engines
| Engine | Domain | Purpose |
|--------|--------|---------|
| Matching Engine | Matching | Score and rank properties against criteria |
| Visit Engine | Visits | Plan, confirm, and track property visits |
| CRM Engine | CRM | Contact management, lead pipeline, follow-up |
| Notification Engine | Notifications | Template-based message delivery |
| Document Engine | Documents | Document lifecycle, GED integration |
| Verification Engine | Verification | Identity, property, and document verification |
| Transaction Engine | Transactions | Transaction step tracking |
| Payment Engine | Payments | Payment processing via Financial Core and Campay |

Each engine extends EngineBase, registers with RuntimeRegistry, and executes within RuntimeScheduler ordering.

---

## 16. Migration V2 to V3 (Shadow Mode)

Migration follows four phases, with V2 remaining operational throughout.

### Phase 1: Coexistence (Current)
- LROS exists alongside V2 as a parallel package
- ConversationRuntimeAdapter wires events from V2 to LROS
- V2 publishes events to LROS but V2 does not read from LROS
- LROS records all events and builds project state independently
- Timeline and audit run as shadow observability
- V2 responses are identical with or without LROS
- Risk: None. LROS is write-only in this phase.

### Phase 2: Adoption
- New business logic written as EngineBase implementations
- RuntimeFacade provides V2 modules access to LROS project state
- V2 reads qualification criteria from LROS
- Timeline replaces V2 debug logging
- Risk: Medium. V2 modules must be adapted without breakage.

### Phase 3: Cutover
- Channel adapters call RuntimeAPI.handle_event() directly
- V2 ConversationStateEngine refactored into an LROS EngineBase
- V2 response generation triggered by LROS events
- V2 conversation state rebuilt from LROS event replay
- Risk: High. Full regression testing required on all channels.

### Phase 4: Optimization
- RuntimePersistence backed by PostgreSQL
- Event sourcing with periodic snapshots
- Parallel engine execution
- Circuit breakers and retry
- Prometheus/Grafana integration
- Risk: Medium. Database migration requires careful testing.

---

## 17. Completed Programs

### Program A — LROS Foundation
- **Commit:** cf633f5f
- **Description:** Event-driven, project-centric kernel for V3
- **Components:** RuntimeAPI, RuntimeDirector, RuntimeScheduler, RuntimeRegistry, RuntimeStateMachine, RuntimePersistence, Timeline, RuntimeAudit, RuntimeMetrics, EventBus, ProjectRuntime, EngineBase

### Program B — Project Profile & Field Registry
- **Commit:** 46fbbc49
- **Tag:** lawim-v3-program-b-project-profile-complete
- **Description:** Project profile, field registry, deterministic merge engine
- **Components:** ProjectProfile, AbstractProjectProfile, FieldRegistry, FieldDefinitions, ProfilePatch, MergeEngine, ConflictResolution, HistorySnapshots, CompletenessCalculator, Normalizers, Validators, Profile types

### Program C — Qualification & Decision Engine
- **Commit:** 86b449b9
- **Tag:** lawim-v3-program-c-qualification-decision-complete
- **Description:** Qualification engine, decision engine, project brain
- **Components:** QualificationEngine, RequirementRegistry, DecisionEngine, ProjectBrain, HumanHandoverEvaluator, ActionRegistry, RuleEvaluator, Guards

### Program C.5 — Action Execution Engine
- **Commit:** 18de07d2
- **Description:** Reliable action execution with idempotency, recovery, retry
- **Components:** ExecutionEngine, ExecutionDispatcher, ActionHandlerRegistry, IdempotencyManager, ActionLockManager, ActionLeaseManager, ExecutionVerifier, AuditTrail, EventCollector, MetricsCollector, ExecutionWorker, RetryPolicy, RecoveryManager, DeadLetterQueue, Outbox, Snapshots, Timeout, Compensation
- **Tests:** 276 C.5 tests PASS, 434 A+B+C+C.5 tests PASS
- **Status:** complete_with_baseline_verification_pending

---

## 18. Current Program

### Program D — Domain Runtime Engines
- **Status:** certified_with_reservations (Programme D.5 review: 2026-07-23)
- **Commit:** 8cf36b8a
- **Description:** Domain-specific execution engines for matching, visits, CRM, notifications, documents, verification, transactions, payments
- Each engine extends DomainRuntime base contract and registers with DomainRuntimeRegistry
- Engines are wrapped in ActionHandlers for ActionExecutionEngine integration
- Each engine has its own validation, logic, verification, models, events, metrics, and policies
- **Components:** MatchingRuntime, VisitRuntime, CRMRuntime, NotificationRuntime, DocumentRuntime, VerificationRuntime, TransactionRuntime, PaymentRuntime, DomainRuntimeConfig, DomainRegistration, V2Adapters
- **Tests:** 68 domain tests PASS, 502 total LROS tests PASS

---

### Program E — Interaction Platform & Channels
- **Status:** complete
- **Description:** Interaction gateway, identity resolution, session management, project resolution, message normalization, deduplication, correlation, interaction orchestrator, response planning, delivery management, V2/V3 routing, divergence analysis
- **Components:** InteractionEnvelope, IdentityResolver, ProjectResolver, SessionManager, MessageNormalizer, InteractionDeduplicator, CorrelationManager, InteractionOrchestrator, InteractionResponsePlan, DeliveryManager, InteractionModeRouter, InteractionDivergenceAnalyzer
- **Feature flags:** interaction_gateway_enabled=false, whatsapp_adapter_enabled=false, telegram_adapter_enabled=false (all disabled by default)
- **Components:** InteractionEnvelope, InteractionGateway, IdentityResolver, ProjectResolver, SessionManager, MessageNormalizer, InteractionDeduplicator, CorrelationManager, InteractionOrchestrator, InteractionResponsePlan, ResponseWriter, DeliveryManager, InteractionModeRouter, InteractionDivergenceAnalyzer, InteractionMetrics, InteractionAuditor, WhatsAppAdapter, TelegramAdapter, WebAPIAdapter, SessionRepository, ChannelIdentityRepository, DeduplicationRepository, DeliveryRepository
- **Tests:** 92 interaction tests PASS, 595 total LROS tests PASS
- **Reservations D.5 addressed:** EventBus integration, metrics, visit transitions, matching INSUFFICIENT_DATA, V2 adapters wiring

---

## 19. Future Programs

| Program | Focus | Status |
|---------|-------|--------|
| E | Cross-Channel Continuity & Full Omnichannel | planned |
| F | Advanced Search & Hybrid Matching | planned |
| G | Transaction Pipeline & Payment Integration | planned |
| H | Document Intelligence & GED Automation | planned |
| I | Admin Cockpits & Dashboard Suite | planned |
| J | Analytics, Observability & Alerting | planned |
| K | Learning & Knowledge Engine | planned |
| L | AI Agent Integration & Multi-Provider Governance | planned |
| M | Production Readiness & Performance Optimization | planned |
| N | Operations Industrialization | planned |
| O | Ecosystem & Partner Integration | planned |

---

## 20. Non-Negotiable Constraints

1. PROJECT_CENTRIC — Every operation revolves around the ProjectProfile. No conversation-scoped business state.
2. EVENT_DRIVEN — Every state change originates from an immutable, typed event. No ad-hoc mutations.
3. CHANNEL_INDEPENDENT — Channels are transport only. No business logic in adapters.
4. LLM_AS_FORMATTER — LLM extracts and formulates. The engine decides, executes, and persists.
5. AUDIT_EVERYTHING — Every state change has a before/after audit entry.
6. NO_SILENT_FAILURES — Every error is logged and handled. No bare except:pass.
7. NO_SECRETS_IN_CODE — Secrets come from environment or vault. Never commit secrets.
8. IDEMPOTENCY — Every action must be safely repeatable.
9. SINGLE_SOURCE_OF_TRUTH — ProjectProfile is authoritative. No parallel business state.
10. DETERMINISTIC — Given same events, same state. No LLM-dependent state drift.
11. V2_MUST_REMAIN_OPERATIONAL — V2 continues serving users during shadow migration.
12. EVIDENCE_REQUIRED — No LIVE/VERIFIED/COMPLETE without real runtime proof.
13. NO_HANDOVER_WITHOUT_REASON — Every handover requires persistent handover_id and valid reason.
14. ONE_QUESTION_PER_RESPONSE — Each LAWIM response asks at most one useful question.
15. CANONICAL_FOOTER — Every automated message includes the LAWIM AI footer (max 10 words).

---

## 21. Validation Levels

| Level | Definition | Evidence Required |
|-------|------------|-------------------|
| L0 | Not implemented | None |
| L1 | Code written | Source files in repository |
| L2 | Unit tested | Test suite passes |
| L3 | Integration tested | Cross-component tests pass |
| L4 | Shadow validated | LROS events match V2 state |
| L5 | Channel tested | Real message through pipeline |
| L6 | User accepted | Real user validates on terminal |
| L7 | Production deployed | Deployed on OVH |
| L8 | Runtime validated | Full real-world journey complete |

### Non-Evidence
The following do NOT constitute proof of production readiness:
- Code present in the repository
- Successful unit tests
- Successful build or container healthy
- healthz/readyz returning 200
- Webhook configured in the API
- Simulated payload accepted by endpoint
- Green API returns authorized
- Telegram getMe returns ok
- Git tag created
- Report written

Un test unitaire ne prouve pas une integration reelle.
Un commit ne prouve pas un deploiement.
Un service sain ne prouve pas le fonctionnement du parcours metier.

---

## 22. Known Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| State divergence between V2 and V3 | Medium | Phase 1 write-only; continuous validation |
| LLM cost duplication during migration | Low | LROS does not call LLMs; only V2 triggers costs |
| V2 regression from LROS adapter | Low | Write-only phase; LROS does not modify V2 state |
| Event flooding | Low | Synchronous EventBus; async dispatch in Phase 4 |
| Data loss on restart | Medium | In-memory persistence; SQL persistence in Phase 4 |
| Migration incomplete | Low | Clear verification gates per phase; documented rollback |
| Engine circular dependency | Low | Scheduler is single-pass; engines cannot recurse |
| Performance overhead | Low | LROS adds ~1ms per event in-memory |

---

## 23. Modification Rules

Before ANY modification, an agent MUST:

1. Read LAWIM_CONTEXT.md, AGENTS.md, lawim_program_status.yaml, applicable ADRs, and program specification
2. Verify Git state (branch, HEAD, dirty files)
3. Read canonical documents from docs/canonical/
4. Inspect existing code for the component to be modified
5. Search for similar components or patterns
6. Identify public contracts (APIs, events, models)
7. Execute reference tests to establish baseline
8. Summarize understanding of the change
9. Signal any contradictions found in the codebase
10. Identify risks of the proposed change

### Testing requirements
- Reproduce the defect before any correction
- Create a failing test before modifying code
- Run linting and type checking after changes
- Verify all existing tests still pass
- Document rollback procedure before deployment

---

## 24. References

| Document | Location |
|----------|----------|
| Project context | LAWIM_CONTEXT.md (this file) |
| Agent rules | AGENTS.md |
| Program status | lawim_program_status.yaml |
| Project glossary | docs/canonical/24_GLOSSARY.md |
| Vision and scope | docs/canonical/00_LAWIM_VISION_AND_SCOPE.md |
| Principles and governance | docs/canonical/01_PRINCIPLES_AND_GOVERNANCE.md |
| Domain boundaries | docs/canonical/03_DOMAIN_BOUNDARIES.md |
| Users, roles, actors | docs/canonical/02_USERS_ROLES_AND_ACTORS.md |
| Projects and dossiers | docs/canonical/05_PROJECTS_AND_DOSSIERS.md |
| Conversation specification | docs/canonical/07_CONVERSATION_TARGET_SPECIFICATION.md |
| AI governance | docs/canonical/15_AI_GOVERNANCE.md |
| Channels and omnichannel | docs/canonical/14_CHANNELS_AND_OMNICHANNEL.md |
| Testing and acceptance | docs/canonical/20_TESTING_AND_ACCEPTANCE_STANDARD.md |
| LROS architecture | reports/architecture/LAWIM-LROS-ARCHITECTURE.md |
| LROS contracts | reports/architecture/LAWIM-LROS-CONTRACTS.md |
| LROS migration guide | reports/architecture/LAWIM-LROS-MIGRATION-GUIDE.md |
| AI context (conversation) | docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md |
| AI context (scope) | docs/ai-context/LAWIM_CANONICAL_SCOPE.md |
| AI context (rules) | docs/ai-context/LAWIM_ENGINEERING_RULES.md |
| AI context (evidence) | docs/ai-context/LAWIM_PRODUCTION_EVIDENCE_POLICY.md |
| AI context (secrets) | docs/ai-context/LAWIM_SECRET_MANAGEMENT_POLICY.md |
| AI context (current state) | docs/ai-context/LAWIM_CURRENT_STATE.md |
| ADR index | docs/adr/ |
| Domain extensions | docs/domain_extension/ |
| Knowledge execution | docs/knowledge_execution/ |
| Semantic harmonization | docs/semantic_harmonization/ |
| Operations | docs/operations/ |
| Deployment | docs/deployment/ |

---

## Appendix: Canonical Statements

- LAWIM n'est pas un chatbot. LAWIM est une plateforme immobiliere intelligente et operationnelle.
- Une conversation ne constitue pas un projet. Un projet est une entite metier persistante.
- Un message ne constitue pas une decision. La decision est prise par le moteur metier.
- Une decision ne constitue pas une execution. L'execution est realisee par ActionExecutionEngine.
- Une execution automatisee ne constitue pas necessairement une preuve reelle. La preuve reelle necessite un test de bout en bout sur canal reel.
- Un test unitaire ne prouve pas une integration reelle. L'integration reelle necessite des tests cross-composant et cross-canal.
- Un commit ne prouve pas un deploiement. Le deploiement necessite un environnement cible operationnel.
- Un service sain ne prouve pas le fonctionnement du parcours metier. Le parcours metier necessite une validation de bout en bout.
