# LAWIM — Controlled Generation Architecture

- Author: LAWIM AI
- Date: 2026-07-21
- Status: IMPLEMENTED
- Chantier: 4 — Controlled Generation

## 1. Complete Generation Pipeline

```
Message
  → ConversationStateEngine
    → ActiveCaseResolver
      → QualificationPriorityRegistry
        → ProgressiveWizard
          → ConversationTurnDecision
            → ResponsePlan
              → DialoguePlan
                → MemoryContextBuilder
                  → ControlledGenerationRequest
                    → ProviderOrchestrator
                      → ControlledGenerationResponse
                        → Validation Pipeline
                          → RepairHandler
                            → InternalFallback
                              → ChannelRenderer
                                → Delivery
```

### Pipeline Stages

| Stage | Component | Responsibility |
|-------|-----------|----------------|
| 1 | ConversationStateEngine | Process incoming message, detect language, extract slots |
| 2 | ActiveCaseResolver | Resolve active case from conversation context |
| 3 | QualificationPriorityRegistry | Determine qualification priority and journey |
| 4 | ProgressiveWizard | Drive slot-by-slot qualification step |
| 5 | ConversationTurnDecision | Decide next action based on state and qualification |
| 6 | ResponsePlan | Define response constraints (type, max questions, forbidden content) |
| 7 | DialoguePlan | Define dialogue act, tone, facts, and formatting rules |
| 8 | MemoryContextBuilder | Build ProviderMemoryContext (limited view for LLM) |
| 9 | ControlledGenerationRequest | Unified request contract with all constraints |
| 10 | ProviderOrchestrator | Call provider chain with timeout, retry, circuit breaker |
| 11 | ControlledGenerationResponse | Unified response contract with validation metadata |
| 12 | Validation Pipeline | Structural → Business → Conversation validation |
| 13 | RepairHandler | Single repair attempt on invalid response |
| 14 | InternalFallback | Template/rule-based fallback when all providers fail |
| 15 | ChannelRenderer | Format response for channel (footer, parse mode) |
| 16 | Delivery | Send via provider adapter (Green API / Telegram) |

## 2. Key Components

### ControlledGenerationRequest

Defined in `contracts/generation.py:17-45`. Carries every constraint the LLM needs:

- request_id, conversation_id, case_id, state_version
- language, persona, intent, journey_code
- dialogue_act, facts_to_acknowledge, facts_not_to_repeat
- next_action, next_question_key, rendered_next_question
- allowed_content, forbidden_content, maximum_questions
- maximum_sentences, maximum_characters
- channel, provider_memory_context, response_schema_version
- user_message, known_facts, missing_required_facts
- handover_status, readiness_status

Built from ResponsePlan + DialoguePlan + ProviderMemoryContext via `build_request_from_plan()`.

### ControlledGenerationResponse

Defined in `contracts/generation.py:48-62`. Carries all output metadata:

- content, language, dialogue_act, question_count
- provider, model, latency_ms, finish_reason
- confidence, schema_version, valid, validation_errors

Built from provider raw response via `build_response_from_provider()`.

### ProviderOrchestrator

Defined in `orchestration/orchestrator.py:64-291`. Manages the full provider chain:

- Iterates through providers in configured order
- Applies timeout (total deadline), retry (max 1), and circuit breaker
- Records success/failure/timeout in ProviderRegistry
- Falls back to InternalReasoningEngine if all providers fail
- Returns GenerationResult with all attempts

### ProviderRegistry

Defined in `orchestration/provider_registry.py:63-167`. Manages provider health:

- Per-provider circuit breaker (3 failures → OPEN for 60s)
- Health tracking (error rate, latency, consecutive failures)
- Provider availability queries

### ProviderSelectionPolicy

Defined in `orchestration/selection.py:9-50`. Selects provider chain:

- Respects preferred provider, exclusion list
- Falls back through registry chain

## 3. Validation Pipeline

```
ControlledGenerationResponse
  → StructuralValidator (JSON schema, required fields, types, size)
    → BusinessValidator (dialogue act, question count, known facts)
      → ConversationValidator (forbidden content patterns)
        → RepairHandler (single repair attempt)
          → ResponseQualityEvaluator (quality scoring)
```

### Stages

| Stage | Component | Validation |
|-------|-----------|-----------|
| 1 | StructuralValidator | JSON validity, required fields (content, dialogue_act, language), type checks, empty content, language support, dialogue act validity, question count, max size |
| 2 | BusinessValidator | Question count ≤ 1, no re-asking known facts, no invented values, no intent change |
| 3 | ConversationValidator | Forbidden content: neutral assistant, external referrals, translation, grammar correction |
| 4 | RepairHandler | Single repair: JSON extraction from non-JSON, forbidden content stripping |
| 5 | ResponseQualityEvaluator | Continuous quality score (0.0-1.0): accuracy, relevance, conciseness, clarity, naturalness, tone, consistency, jargon |

## 4. Provider Chain

Default chain (configurable):

```
DeepSeek → OpenAI → Gemini Primary → Gemini Secondary → Internal
```

| Provider | Model | Role |
|----------|-------|------|
| DeepSeek | deepseek-chat | Primary LLM |
| OpenAI | gpt-4o-mini | Secondary LLM |
| Gemini Primary | gemini-2.0-flash | Gemini primary |
| Gemini Secondary | gemini-1.5-flash | Gemini secondary |
| Internal | InternalReasoningEngine + LawimInternalResponseEngine | Template/rule fallback |

## 5. Configuration Reference

Defined in `orchestration/config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| DEFAULT_CONNECT_TIMEOUT | 10.0s | Connection timeout per provider |
| DEFAULT_READ_TIMEOUT | 20.0s | Read timeout per provider |
| DEFAULT_TOTAL_TIMEOUT | 30.0s | Total deadline for all providers |
| DEFAULT_MAX_RETRIES | 1 | Max retries per provider |
| DEFAULT_BACKOFF_SECONDS | 1.0s | Backoff between retries |
| DEFAULT_CIRCUIT_BREAKER_THRESHOLD | 3 | Consecutive failures to open circuit |
| DEFAULT_CIRCUIT_BREAKER_RECOVERY_SECONDS | 60.0s | Circuit recovery time |
| DEFAULT_PROVIDER_CHAIN | ["deepseek", "openai", "gemini_primary", "gemini_secondary", "internal"] | Provider order |
