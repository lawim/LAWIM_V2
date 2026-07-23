# LAWIM V3 — Changelog Release 1.0

**Date:** 2026-07-23
**HEAD:** 35af6958

---

## Programme A — LROS Foundation (cf633f5f)

- RuntimeAPI, RuntimeDirector, RuntimeScheduler, RuntimeRegistry
- RuntimeStateMachine, RuntimePersistence, Timeline
- RuntimeAudit, RuntimeMetrics, EventBus
- ProjectRuntime, EngineBase

## Programme B — Project Profile (46fbbc49)

- ProjectProfile, AbstractProjectProfile
- FieldRegistry, FieldDefinitions
- ProfilePatch, MergeEngine, ConflictResolution
- HistorySnapshots, CompletenessCalculator
- Normalizers, Validators
- 5 profile types (rental_search, purchase_search, sale_project, construction_project, land_project)

## Programme C — Qualification & Decision (86b449b9)

- QualificationEngine, RequirementRegistry
- DecisionEngine, ProjectBrain
- HumanHandoverEvaluator, ActionRegistry
- RuleEvaluator, Guards

## Programme C.5 — Action Execution (18de07d2)

- ExecutionEngine, ExecutionDispatcher
- ActionHandlerRegistry, IdempotencyManager
- ActionLockManager, ActionLeaseManager
- ExecutionVerifier, AuditTrail, EventCollector
- MetricsCollector, ExecutionWorker
- RetryPolicy, RecoveryManager, DeadLetterQueue
- Outbox, Snapshots, Timeout, Compensation

## Programme D — Domain Runtimes (8cf36b8a)

- MatchingRuntime, VisitRuntime, CRMRuntime
- NotificationRuntime, DocumentRuntime
- VerificationRuntime, TransactionRuntime, PaymentRuntime
- DomainRuntimeConfig (all disabled by default)
- DomainRegistration (shadow mode by default)
- V2 Adapters (8 domains)

## Programme E — Interaction Platform (c4e4efde + b5fd3814)

- InteractionEnvelope, InteractionContext
- IdentityResolver, ProjectResolver, SessionManager
- MessageNormalizer, InteractionDeduplicator
- CorrelationManager, InteractionOrchestrator
- InteractionResponsePlan, DeliveryManager
- InteractionModeRouter (V2/V3 routing)
- InteractionDivergenceAnalyzer
- InteractionMetrics, InteractionAuditor
- 3 channel adapters (WhatsApp, Telegram, Web/API)
- DeterministicResponseWriter
- Persistence repositories (InMemory)

## Programme E.5 — End-to-End Integration (beb986ab)

- 27 E2E scenario tests
- 26 resilience tests
- DeterministicExtractor
- Correlation traceability

## Programme F — AI Intelligence Platform (29af2767 + 812e13fb)

- AIIntelligenceGateway (6 modes)
- StructuredExtractionEngine
- ExtractionCandidate with provenance
- LLM Gateway / ProviderRegistry
- PromptRegistry / PromptRenderer / PromptInjectionDetector
- KnowledgeGateway
- AIResponseWriter with deterministic fallback
- ResponseValidator / ForbiddenClaimDetector
- DataClassification / RedactionPolicy
- AIEvaluator / AIMetrics
- AIIntegrationPolicy / CandidateUpdateFactory / AIDivergenceAnalyzer

## Programme G — Production Readiness (a337eda0)

- ProductionConfig with env validation
- OpenAIProvider, AnthropicProvider, DeepSeekProvider, GeminiProvider
- CircuitBreaker, RetryPolicy, RateLimiter
- SQLiteSessionStore, SQLiteProfileStore
- HealthChecker (liveness, readiness)
- Prometheus + Grafana configuration
- Docker Compose production (6 services)

## Programme G.5 — Production Deployment (da8ef6b7)

- deploy.sh, rollback.sh, backup.sh, restore.sh
- Migration engine (migrate.py, 4 migrations)
- load_test.py, disaster_recovery.py

## Programme G.6 — External Certification (35af6958)

- Pre-deployment checklist
- 7 evidence report templates (WhatsApp, Telegram, Campay, LLM, Load, DR, Backup)
- All L6: NOT VALIDATED (credentials non configurés)

## Statistiques

| Métrique | Valeur |
|----------|--------|
| Commits depuis Programme A | 18 |
| Fichiers | ~200+ |
| Tests LROS | 721 |
| Tests V2 baseline | 24 (3 preexisting) |
| Programmes | 14 (A → G.6) |
| Branches | 1 (release-1.0-20260723) |
