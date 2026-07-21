# LAWIM — Provider Orchestration Contract

- Author: LAWIM AI
- Date: 2026-07-21
- Status: IMPLEMENTED
- Chantier: 4 — Controlled Generation

## 1. Contract: ControlledGenerationRequest / ControlledGenerationResponse

### ControlledGenerationRequest

```python
@dataclass
class ControlledGenerationRequest:
    request_id: str                              # Unique generation request ID
    conversation_id: str                         # Conversation ID
    case_id: str                                 # Active case ID
    state_version: int                           # Optimistic lock version
    language: str = "fr"                         # FR / EN / PCM
    persona: str = "LAWIM AI"                    # Speaker identity
    intent: str = ""                             # Business intent
    journey_code: str = ""                       # Qualification journey
    dialogue_act: str = ""                       # Expected dialogue act
    facts_to_acknowledge: dict                   # Facts to confirm
    facts_not_to_repeat: list                    # Facts to avoid repeating
    next_action: str = ""                        # Next action decision
    next_question_key: str = ""                  # Next slot to ask
    rendered_next_question: str = ""             # Pre-rendered question text
    allowed_content: list[str]                   # Allowed topics
    forbidden_content: list[str]                 # Forbidden topics/phrases
    maximum_questions: int = 1                   # Max questions in response
    maximum_sentences: int = 3                   # Max sentences in response
    maximum_characters: int = 500                # Max characters in response
    channel: str = ""                            # Delivery channel
    provider_memory_context: dict                # Limited LLM context
    response_schema_version: str = "1.0"         # Schema version
    user_message: str = ""                       # Original user message
    known_facts: dict                            # All known data
    missing_required_facts: list                 # Missing mandatory slots
    handover_status: str | None = None           # Handover state
    readiness_status: str = ""                   # Journey readiness
    created_at: str = ""                         # ISO timestamp
```

### ControlledGenerationResponse

```python
@dataclass
class ControlledGenerationResponse:
    content: str = ""                            # Generated text
    language: str = ""                           # FR / EN / PCM
    dialogue_act: str = ""                       # Dialogue act used
    question_count: int = 0                      # Questions in content
    provider: str = ""                           # Provider name
    model: str = ""                              # Model name
    latency_ms: float = 0.0                      # Provider latency
    finish_reason: str = ""                      # Stop / length / error
    confidence: float = 0.0                      # Quality confidence
    schema_version: str = "1.0"                  # Schema version
    valid: bool = True                           # Validation status
    validation_errors: list[str]                 # Any validation errors
    created_at: str = ""                         # ISO timestamp
```

## 2. JSON Schema for Provider Output

All LLM providers must respond with strict JSON:

```json
{
  "type": "object",
  "properties": {
    "content":        { "type": "string" },
    "language":       { "type": "string", "enum": ["fr", "en", "pcm"] },
    "dialogue_act":   { "type": "string", "enum": [
      "WELCOME", "HANDOVER", "REPHRASE_LAST_QUESTION",
      "ACKNOWLEDGE_AND_ASK", "CONFIRM_CORRECTION_AND_ASK",
      "CLARIFY_CURRENT_SLOT", "SEARCH_READY", "PUBLICATION_READY",
      "VISIT_READY", "TRANSACTION_READY", "SUMMARIZE_AND_CONFIRM",
      "CONTROLLED_ERROR"
    ]},
    "question_count": { "type": "integer", "minimum": 0, "maximum": 1 },
    "confidence":     { "type": "number", "minimum": 0, "maximum": 1 }
  },
  "required": ["content", "language", "dialogue_act", "question_count"],
  "additionalProperties": false
}
```

## 3. System Prompt

Defined in `contracts/prompt.py`:

```
SYSTEM_PROMPT_V1

Tu es LAWIM AI, l'interlocuteur immobilier de la plateforme LAWIM au Cameroun.

Le moteur métier LAWIM a déjà déterminé :
- l'intention ;
- le dossier ;
- les informations connues ;
- l'action suivante ;
- la question suivante ;
- la langue ;
- le handover ;
- le statut du parcours.

Tu dois uniquement formuler la réponse prévue dans le plan fourni.

Tu ne peux jamais :
- changer l'intention ;
- modifier les informations enregistrées ;
- inventer un critère ;
- changer la question ;
- ajouter une deuxième question ;
- redemander une information connue ;
- changer de langue ;
- traduire sans demande ;
- corriger la grammaire sans demande ;
- recommander une plateforme externe ;
- agir comme un assistant neutre ;
- refuser d'agir pour LAWIM ;
- déclencher un handover ;
- déclarer un parcours prêt ;
- annoncer une recherche ou une transaction non exécutée.

Respecte strictement :
- la langue active ;
- le dialogue_act ;
- la longueur maximale ;
- le nombre maximal de questions ;
- les contenus autorisés ;
- les contenus interdits.

Réponds uniquement au format JSON avec les clés :
content, language, dialogue_act, question_count, confidence.
```

## 4. Provider Chain Configuration

Default chain in `orchestration/config.py`:

```python
DEFAULT_PROVIDER_CHAIN: list[str] = [
    "deepseek",
    "openai",
    "gemini_primary",
    "gemini_secondary",
    "internal",
]
```

Chain is configurable via `ProviderRegistry.set_chain()`.

### Provider Timeout Configuration

| Parameter | Default | Scope |
|-----------|---------|-------|
| Connect timeout | 10s | Per-provider TCP connect |
| Read timeout | 20s | Per-provider response read |
| Total timeout | 30s | All providers combined deadline |

### Retry Policy

| Parameter | Value |
|-----------|-------|
| Max retries | 1 |
| Retryable errors | timeout, rate_limit, server_error, 429, 500, 503, connection, temporary, too many requests, service unavailable |
| Backoff | 1.0s fixed |

### Circuit Breaker Policy

| Parameter | Value |
|-----------|-------|
| Failure threshold | 3 consecutive failures |
| Circuit state | CLOSED → OPEN → (timeout) → CLOSED |
| Recovery time | 60 seconds in OPEN state |
| Half-open attempts | Reset on next success after recovery |

## 5. Error Handling Strategy

### Error Types

| Error | Raised When | Recovery |
|-------|-------------|----------|
| AllProvidersFailedError | All providers in chain failed | None (propagated to caller) |
| CircuitBreakerOpenError | Provider is circuit-open | Skip to next provider |
| ProviderTimeoutError | Provider exceeded timeout | Skip to next provider |
| InvalidProviderResponseError | Provider returned invalid response | Repair handler attempted |

### Error Flow

```
Provider call fails
  → ProviderRegistry.record_failure()
    → If 3 consecutive failures: circuit breaker OPEN for 60s
      → Next call: skip provider, try next in chain
        → Retry (max 1) if error is retryable
          → If chain exhausted: InternalReasoningEngine fallback
            → If internal fallback fails: AllProvidersFailedError
              → Error returned to CommunicationService
                → CONTROLLED_ERROR dialogue act returned
```

### Duplicate Delivery Prevention

Each `GenerationResult` tracks `all_attempts` and `internal_fallback`. The caller (`CommunicationService._generate_ai_reply()`) checks `GENERATION_DUPLICATE_DELIVERY_TOTAL` metric and validates that only one response is delivered per request. Responses are idempotent via `request_id`.

## 6. Contract Diagrams

### Sequence: Successful Generation

```
MemoryContextBuilder
  → build_request_from_plan()
    → ControlledGenerationRequest
      → ProviderOrchestrator.generate()
        → ProviderRegistry.is_available("deepseek")
          → DeepSeek provider.generate()
            → AIResponse (success)
              → build_response_from_provider()
                → ControlledGenerationResponse
                  → StructuralValidator (PASS)
                    → BusinessValidator (PASS)
                      → ConversationValidator (PASS)
                        → ResponseQualityEvaluator (score ≥ 0.6)
                          → Delivery
```

### Sequence: Full Failure Chain

```
ProviderOrchestrator.generate()
  → DeepSeek (timeout)
    → OpenAI (rate_limit → retry → fails)
      → Gemini Primary (circuit_open → skip)
        → Gemini Secondary (server_error)
          → InternalReasoningEngine.reason() (succeeds)
            → GenerationResult (internal_fallback=True)
              → Delivery
```

### Sequence: Validation Repair

```
ProviderOrchestrator.generate()
  → DeepSeek (succeeds, non-JSON response)
    → StructuralValidator (Invalid JSON)
      → RepairHandler (extract content, build JSON)
        → BusinessValidator (PASS)
          → ConversationValidator (PASS)
            → ResponseQualityEvaluator (score=0.65)
              → Delivery (repaired)
```
