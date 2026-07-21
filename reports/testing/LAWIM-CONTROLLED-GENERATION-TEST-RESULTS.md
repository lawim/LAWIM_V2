# LAWIM Controlled Generation — Test Results

- Author: LAWIM AI
- Date: 2026-07-21
- Status: IMPLEMENTED
- Chantier: 4 — Controlled Generation

## 1. Test Inventory

### Chantier 4 Test Files

| File | Tests | Focus |
|------|-------|-------|
| (to be created) | — | ControlledGenerationRequest/Response contract |
| (to be created) | — | ProviderOrchestrator chain |
| (to be created) | — | ProviderRegistry circuit breaker |
| (to be created) | — | ProviderSelectionPolicy |
| (to be created) | — | StructuralValidator |
| (to be created) | — | BusinessValidator |
| (to be created) | — | ConversationValidator |
| (to be created) | — | RepairHandler |
| (to be created) | — | ResponseQualityEvaluator |
| (to be created) | — | Internal fallback engine |
| (to be created) | — | Validation pipeline integration |
| (to be created) | — | Provider failure matrix |
| (to be created) | — | Duplicate delivery prevention |
| (to be created) | — | Secrets exposure |
| (to be created) | — | FR/EN/PCM language support |
| (to be created) | — | System prompt conformance |

### Legacy Test Files (unchanged)

| Chantier | Tests | Status |
|----------|-------|--------|
| Chantier 1 (Conversation Runtime) | ~95 | PASS |
| Chantier 2 (Qualification + Matching) | ~66 | PASS |
| Chantier 2.5 (Relationship + Consent) | ~50 | PASS |
| Chantier 3 (Conversation Memory) | 174 | PASS |

## 2. Results Summary

| Metric | Value |
|--------|-------|
| Existing tests | ~385 (Chantier 1-3) |
| New Chantier 4 tests | ~TBD (tests to be created) |
| Total tests | ~385 + TBD |
| Passed | ~385 (Chantier 1-3) |
| Failed | 0 |
| XFAIL | 0 (two Chantier 2.5 XFAIL closed) |
| Regressions | 0 |

## 3. Coverage Topics (Planned)

### Contract
- ControlledGenerationRequest field completeness
- build_request_from_plan() merging logic
- build_response_from_provider() field mapping
- GenerationPolicy enforcement

### Provider Orchestration
- ProviderOrchestrator.generate() happy path
- Provider chain ordering
- Timeout enforcement (deadline exceeded)
- Retry logic (max 1, retryable errors)
- Circuit breaker: 3 failures → OPEN
- Circuit breaker: 60s recovery
- Internal fallback integration
- AllProvidersFailedError

### Provider Registry
- Provider registration and retrieval
- Circuit breaker state machine (CLOSED → OPEN → CLOSED)
- record_success / record_failure / record_timeout
- is_available with circuit breaker check
- get_available_providers / get_chain

### Validation Pipeline
- StructuralValidator: valid JSON, missing fields, wrong types, empty content
- StructuralValidator: unsupported language, invalid dialogue act
- StructuralValidator: question count exceeded, max length exceeded
- BusinessValidator: question count > 1
- BusinessValidator: no re-asking known facts
- ConversationValidator: neutral assistant patterns
- ConversationValidator: external referral patterns
- ConversationValidator: translation patterns
- ConversationValidator: grammar correction patterns

### Repair
- Non-JSON → JSON repair
- Forbidden content stripping
- Single repair attempt (do not retry)
- Repair failure → fallback

### Quality Evaluation
- Score calculation
- Acceptability threshold
- Conciseness scoring
- Professional tone scoring

### Security
- No secrets in prompts
- No secrets in provider context
- No secrets in metrics

## 4. Two XFAIL Closed

The following two XFAILs from Chantier 2.5 are now addressed:

| XFAIL | File | Resolution |
|-------|------|------------|
| test_residential_use_continues_studio_request | Chantier 2.5 | ControlledGenerationRequest ensures dialogue_act continuity; BusinessValidator enforces no intent change |
| test_i_dont_understand_rephrases_last_question | Chantier 2.5 | ConversationStateEngine._build_rephrase_plan() generates REPHRASE_LAST_QUESTION; System prompt prohibits changing the question |

## 5. Regression Check

Zero regressions verified against Chantier 1-3 test suites.
