# ADR-013: Channel Adapters — No Business Logic

**Status:** Accepted
**Date:** 2026-07-23

## Context

Channel-specific code historically mixed webhook parsing with business decisions. This made channels non-portable, untestable, and tightly coupled to specific providers.

## Decision

ChannelAdapters are strictly bi-directional format converters. Inbound: webhook payload → InteractionEnvelope. Outbound: ChannelDeliveryRequest → provider API call. Adapters NEVER make business decisions, call ProjectBrain, modify ProjectProfile, invoke LLMs, or orchestrate domain runtimes.

## Consequences

- Adapters are independently testable
- Adding a new channel requires only a new adapter
- Zero business logic duplication across channels
- All business decisions remain in the deterministic runtime

## References

- ADR-002: LROS Runtime Kernel
- ADR-004: LLM Is Not the Business Decision Maker
- ADR-009: Domain Runtime Boundaries
