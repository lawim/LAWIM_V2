# LAWIM — Internal Fallback Engine

- Author: LAWIM AI
- Date: 2026-07-21
- Status: IMPLEMENTED
- Chantier: 4 — Controlled Generation

## 1. Overview

The internal fallback engine is the last resort in the provider chain. It activates when all external AI providers (DeepSeek, OpenAI, Gemini) have failed or are unavailable. It consists of two components:

| Component | File | Role |
|-----------|------|------|
| InternalReasoningEngine | `ai/internal_reasoning.py` | Intent detection + handler dispatch |
| LawimInternalResponseEngine | `conversation/policy/internal_engine.py` | Template-based dialogue act rendering |

## 2. Components

### InternalReasoningEngine

Defined in `ai/internal_reasoning.py:54-283`. Responsible for:

- Intent detection via keyword matching
- Handler dispatch per intent
- Knowledge runtime integration (when available)
- Default response escalation

**Intent detection** uses simple keyword-based classification:

| Intent | Keywords |
|--------|----------|
| greeting | bonjour, salut, hello, hi |
| farewell | au revoir, merci, bye |
| property_search | acheter, louer, recherche, bien, maison, appartement |
| qualification | qualification, évaluation, estimation, critère, besoin |
| matching | matching, correspond, similaire |
| financial | prix, coût, payer, campay, facture, budget |
| support | aide, support, problème, erreur, bug |
| scheduling | rendez-vous, visite, programmer, rencontre |
| general_inquiry | (fallback) |

**Handler methods:**

| Handler | Behavior |
|---------|----------|
| _handle_property_search | Formats criteria, searches property catalog, returns count + top 3 titles |
| _handle_qualification | Uses knowledge runtime wizard if available, else prompts for property type |
| _handle_matching | Formats matching results with scores |
| _handle_financial | Returns escalation (requires human) |
| _handle_support | Returns escalation (support request) |
| _handle_scheduling | Asks for availability |
| _handle_greeting | Returns canonical greeting in FR/EN/PCM |
| _handle_farewell | Standard farewell message |
| _handle_general | Shows known facts or capability list |
| _default_response | Escalation for unhandled requests |

### LawimInternalResponseEngine

Defined in `conversation/policy/internal_engine.py:16-173`. Responsible for rendering dialogue acts into natural language. Covers all 12 dialogue acts:

| Dialogue Act | Method | Description |
|-------------|--------|-------------|
| WELCOME | `_generate_welcome()` | Canonical greeting per language |
| HANDOVER | `_generate_handover()` | Handover message per language |
| REPHRASE_LAST_QUESTION | `_generate_rephrase()` | Rephrase with question per language |
| ACKNOWLEDGE_AND_ASK | `_generate_acknowledge_and_ask()` | Acknowledge facts + ask next question |
| CONFIRM_CORRECTION_AND_ASK | `_generate_correction()` | Confirm correction + ask next |
| CLARIFY_CURRENT_SLOT | `_generate_clarify()` | Ask for clarification |
| SEARCH_READY | `_generate_readiness()` | Announce search readiness |
| PUBLICATION_READY | `_generate_readiness()` | Announce publication readiness |
| VISIT_READY | `_generate_readiness()` | Announce visit readiness |
| TRANSACTION_READY | `_generate_readiness()` | Announce transaction readiness |
| SUMMARIZE_AND_CONFIRM | `_generate_summarize()` | Summarize facts + confirm |
| CONTROLLED_ERROR | `_generate_error()` | Error message per language |

## 3. Language Support

Both engines support three languages:

| Language | Code | InternalReasoningEngine | LawimInternalResponseEngine |
|----------|------|------------------------|------------------------------|
| French | fr | French responses | French templates |
| English | en | English responses | English templates |
| Pidgin (Cameroun) | pcm | French fallback + PCM-specific templates | PCM templates (e.g., "I don hammer", "Make I talk am well", "Dis information correct?") |

**Response quality by language:**

- French: Full coverage (all intents and acts)
- English: Full coverage (all intents and acts)
- Pidgin: All dialogue acts covered; intent detection uses French keywords with PCM-specific template responses

## 4. Integration with ResponsePlan and DialoguePlan

### Invocation Flow

```
ProviderOrchestrator._call_internal_fallback(request)
  → ReasoningContext built from ControlledGenerationRequest
    → InternalReasoningEngine.reason(ctx)
      → intent detection
        → handler dispatch
          → InternalResponse
            → GenerationResult (internal_fallback=True)
```

### Data Flow

The internal fallback receives a `ReasoningContext` built from `ControlledGenerationRequest`:

```python
ctx = ReasoningContext(
    user_text=request.text,
    conversation_key=request.conversation_key,
    language=request.language,
)
```

It does NOT receive the ResponsePlan or DialoguePlan — the internal engine generates its own response based on intent detection.

### LawimInternalResponseEngine Integration

The `LawimInternalResponseEngine` is used in the ConversationStateEngine for dialogue-act-based responses (non-AI path). It receives a `DialoguePlan` and renders the appropriate template per act. This path is used for:

- Non-AI responses (WELCOME, HANDOVER, etc.)
- When `generated_by_ai=False` in ResponsePlan
- As component of the fallback path

## 5. Fallback Chain Priority

```
1. ProviderOrchestrator tries external providers in order
2. If all external providers fail:
   a. InternalReasoningEngine.reason() is called
   b. If InternalReasoningEngine succeeds → return response
   c. If InternalReasoningEngine fails → AllProvidersFailedError
3. If AllProvidersFailedError → CommunicationService uses CONTROLLED_ERROR act
4. Error template rendered by LawimInternalResponseEngine
```

## 6. Limitations

- Intent detection is keyword-based, not semantic
- Property search requires KnowledgeRuntime integration
- Financial and support intents always require escalation
- No memory context is passed to InternalReasoningEngine (by design — it is a pure fallback)
- Pidgin responses use PCM templates but intent detection keywords are primarily French
