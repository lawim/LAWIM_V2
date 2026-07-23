# Programme E — Interaction Platform, Channels & Conversation Orchestration

**Status:** IMPLEMENTED
**Branch:** feature/interaction-platform-multichannel-20260723
**Date:** 2026-07-23

## Purpose

Create the complete interaction layer between users, existing channels, and the LAWIM V3 business kernel. Transform every incoming interaction into a structured project update, then deliver the Runtime's decision back to the originating channel.

## Scope

- Interaction Gateway: envelope, validation, normalization, deduplication
- Identity Resolution: multi-channel identity linking
- Project Resolution: active project detection and creation
- Session Management: user session lifecycle across channels
- Correlation: end-to-end tracing of interactions
- Interaction Orchestrator: full turn processing pipeline
- Response Planning: structured response plans from business decisions
- Delivery Manager: reliable message delivery with idempotency
- Channel Adapters: contracts for WhatsApp, Telegram, Web/API
- V2/V3 Routing: safe migration mode router
- Divergence Analysis: V2 vs V3 comparison
- Event Publishing: domain runtime events via EventBus
- Metrics: interaction observability counters

## Non-Scope (deferred to Programme F)

- LLM extraction and response writing
- Semantic media analysis
- Natural language generation
- Provider orchestration and fallback
- RAG and linguistic memory

## D.5 Reservations Addressed

1. EventBus integration: DomainRuntime base now publishes events via `_publish_event()`
2. Metrics: InteractionMetrics defined with 22 counters
3. Visit transitions: Full state machine with 10 transitions, 3 new actions, 5 transition tests
4. Matching INSUFFICIENT_DATA: Detection with missing_fields, reason_codes, matching_not_started
5. V2 adapters: Wired through InteractionModeRouter with shadow/canary/primary modes

## Architecture

```
Channel (WhatsApp/Telegram/Web)
  → ChannelAdapter.parse_webhook()
  → InteractionEnvelope
  → InteractionGateway.validate()
  → InteractionDeduplicator.check()
  → MessageNormalizer.normalize()
  → IdentityResolver.resolve()
  → SessionManager.resume_or_create()
  → ProjectResolver.resolve()
  → InteractionOrchestrator.process()
  → InteractionResponsePlan
  → DeliveryManager.deliver()
  → ChannelAdapter.send()
```

## Feature Flags

All default to `false`:

- `interaction_gateway_enabled`
- `whatsapp_adapter_enabled`
- `telegram_adapter_enabled`
- `web_interaction_enabled`
- `api_interaction_enabled`
- `whatsapp_shadow_mode` (default `true`)
- `telegram_shadow_mode` (default `true`)

## Packages

- `lawim_runtime/interaction/` — 18 files (gateway, envelope, context, identity, project_resolution, session, normalization, deduplication, correlation, orchestrator, response_plan, delivery, routing, divergence, events, metrics, audit, adapters)
- `lawim_runtime/interaction/tests/` — 10 test files (64 tests)
- `lawim_runtime/interaction/persistence/` — repository abstraction
- `lawim_runtime/domains/base/runtime.py` — EventBus integration
- `lawim_runtime/domains/matching/runtime.py` — INSUFFICIENT_DATA handling
- `lawim_runtime/domains/visit/runtime.py` — state transition machine
