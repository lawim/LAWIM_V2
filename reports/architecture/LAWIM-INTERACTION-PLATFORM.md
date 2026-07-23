# LAWIM Interaction Platform

**Date:** 2026-07-23
**Status:** COMPLETE
**Programme:** E

## Overview

The Interaction Platform is the universal entry point for all user interactions across channels. It transforms every incoming message into a structured project update, orchestrates the business runtime, and delivers responses back to the originating channel.

## Architecture

```
Channel
  -> ChannelAdapter.parse_webhook()
  -> InteractionEnvelope
  -> InteractionGateway.validate()
  -> InteractionDeduplicator.check()
  -> MessageNormalizer.normalize()
  -> IdentityResolver.resolve()
  -> SessionManager.resume_or_create()
  -> ProjectResolver.resolve()
  -> InteractionContext
  -> [Extraction Handler] (Programme F)
  -> [ProjectProfile Patch]
  -> [ProjectBrain / DecisionEngine]
  -> [ActionExecutionEngine]
  -> [Domain Runtime]
  -> InteractionResponsePlan
  -> [ResponseWriter] (Programme F)
  -> ChannelAdapter.send()
  -> Channel Delivery
```

## Components

| Component | File | Responsibility |
|-----------|------|----------------|
| InteractionEnvelope | `envelope.py` | Immutable message envelope |
| InteractionContext | `context.py` | Turn context with resolved references |
| InteractionGateway | `gateway.py` | Validation and envelope preparation |
| MessageNormalizer | `normalization.py` | Channel-agnostic text normalization |
| InteractionDeduplicator | `deduplication.py` | Duplicate detection by ID and hash |
| CorrelationManager | `correlation.py` | End-to-end correlation IDs |
| IdentityResolver | `identity.py` | Multi-channel identity resolution |
| SessionManager | `session.py` | Session lifecycle management |
| ProjectResolver | `project_resolution.py` | Active project detection |
| InteractionOrchestrator | `orchestrator.py` | Full turn orchestration |
| InteractionResponsePlan | `response_plan.py` | Structured response from business decision |
| DeliveryManager | `delivery.py` | Message delivery with retry |
| InteractionModeRouter | `routing.py` | V2/V3 routing with shadow/canary |
| InteractionMetrics | `metrics.py` | Observability counters |
| InteractionAuditor | `audit.py` | Turn audit trail |

## Key Design Decisions

1. **No business logic in channels.** Adapters convert only; no decisions, no LLM calls.
2. **ProjectProfile is Source of Truth.** InteractionContext references, never replaces.
3. **Deterministic pipeline.** No LLM in identity, session, project resolution, or routing.
4. **Shadow-first migration.** V3 runs in parallel with V2 before any live traffic.

## Validation

- Unit tests: 64+ interaction tests
- Full LROS suite: 566 PASS
- V2 baseline: 3 preexisting failures (confirmed)
