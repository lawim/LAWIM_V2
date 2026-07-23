# ADR-010: Interaction Gateway

**Status:** Accepted
**Date:** 2026-07-23

## Context

Incoming messages from multiple channels (WhatsApp, Telegram, Web) need common processing steps before reaching business logic. Without a gateway, each channel duplicates normalization, deduplication, and identity resolution.

## Decision

InteractionGateway is the single entry point. It validates, normalizes, deduplicates, and produces an InteractionEnvelope — a channel-independent, immutable data structure representing one user interaction.

## Consequences

- All channels use the same gateway
- Deduplication happens once per message
- InteractionEnvelope is serializable, persistable, and auditable

## References

- ADR-002: LROS Runtime Kernel
- ADR-009: Domain Runtime Boundaries
