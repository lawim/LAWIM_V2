# LAWIM Conversation Runtime – Call Graph Report

## Active Pipeline (what actually runs at runtime)

```
Green API Webhook ─┐
                   ├──→ process_green_api_webhook / process_telegram_webhook
Telegram Webhook ──┘                  │
                                      ▼
                              _generate_ai_reply
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                    greeting? ──→ _greeting_response
                         │
                         ▼
              AIOrchestrator.build_request
                         │
                         ▼
              AIOrchestrator.generate
                         │
                         ▼
            ┌────────────────────────────┐
            │  Provider chain            │
            │  (deepseek → openai →      │
            │   gemini_primary →          │
            │   gemini_secondary)         │
            │  with circuit breakers      │
            └────────┬───────────────────┘
                     │
             ┌───────┴───────┐
             ▼               ▼
      Provider.generate   All failed?
             │               │
             │               ▼
             │     InternalReasoningEngine.reason
             │               │
             ▼               ▼
         LLM call      Fallback response
```

### Key modules exercised

| Module | Path | Called? |
|--------|------|---------|
| `CommunicationService._generate_ai_reply` | `communication/service.py:575` | Yes |
| `CommunicationService._greeting_response` | `communication/service.py:629` | Yes |
| `CommunicationService._format_ai_footer` | `communication/service.py:618` | Yes |
| `AIOrchestrator.build_request` | `ai/orchestrator.py` | Yes |
| `AIOrchestrator.generate` | `ai/orchestrator.py` | Yes |
| `PromptReconstructionEngine.reconstruct` | `ai/prompt_reconstruction.py` | Yes |
| `MemoryOptimizer.load_for_conversation` | `ai/memory.py` | Yes |
| `InternalReasoningEngine.reason` | `ai/internal_reasoning.py` | Yes (fallback) |

---

## NOT WIRED (defined but never reached at runtime)

The following modules are fully implemented but **not invoked** by any active code path:

| Module | File | Reason |
|--------|------|--------|
| `ConversationService` (domain engine) | `conversation/service.py` | Bypassed; `_generate_ai_reply` goes directly to AIOrchestrator |
| `ProgressiveWizard` | `knowledge_runtime/engine/wizard.py` | No caller in webhook or AI reply path |
| `QualificationEngine` | `knowledge_runtime/engine/evaluator.py` | No caller in active pipeline |
| `ReadinessEvaluator` | `knowledge_runtime/engine/readiness.py` | Only used by ProgressiveWizard/QualificationEngine |
| `NextQuestionResolver` | `knowledge_runtime/engine/resolver.py` | Only used by ProgressiveWizard/QualificationEngine |
| `Planner` | `conversation/planning/planner.py` | ConversationService domain engine never instantiated |
| `QualificationEvaluator` | `conversation/qualification/evaluator.py` | ConversationService domain engine never instantiated |
| `GenerativeComposer` | `conversation/generation/composer.py` | ConversationService domain engine never instantiated |
| `MemoryService` | `conversation/memory/service.py` | ConversationService domain engine never instantiated |

---

## Call Flow Diagram (text)

```
incoming webhook
  │
  ├─ process_green_api_webhook (whatsapp)
  └─ process_telegram_webhook (telegram)
       │
       ▼
  _generate_ai_reply(raw_text, channel, conversation_key)
       │
       ├─ if greeting ──→ _greeting_response(channel)
       │
       └─ if not greeting:
              │
              ├─ AIOrchestrator.build_request(channel, text, conversation_key, language)
              │      │
              │      ├─ PromptReconstructionEngine.reconstruct(...)
              │      └─ MemoryOptimizer.load_for_conversation(...)
              │
              └─ AIOrchestrator.generate(request)
                     │
                     ├─ build_provider_chain(complexity)
                     ├─ for provider in chain:
                     │      ├─ circuit_breaker.allow(provider)?
                     │      ├─ provider.generate(request)
                     │      └─ if success → return response
                     │
                     └─ all providers failed:
                            └─ InternalReasoningEngine.reason(context)
                                   └─ return fallback text
```

---

## Summary

The active conversation pipeline is extremely thin: it consists of webhook normalization → greeting detection → raw AI orchestration. The full domain engine (`conversation/service.py` with its state machine, planner, qualification evaluator, composer, and memory service) is entirely bypassed. The `knowledge_runtime/engine/` wizard subsystem is also unused.

This means context tracking, multi-turn state management, progressive qualification, and structured fact extraction are **not operational** — every message is treated as an independent LLM call with no persistent session state.
