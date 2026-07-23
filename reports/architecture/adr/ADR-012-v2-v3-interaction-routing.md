# ADR-012: V2/V3 Interaction Routing

**Status:** Accepted
**Date:** 2026-07-23

## Context

V2 is in production with live users. V3 must coexist safely. A cutover risks downtime and user-facing regressions. Feature flags alone are insufficient for gradual, user-specific migration.

## Decision

InteractionModeRouter supports five modes: V2_ONLY, V3_SHADOW, V3_CANARY, V3_PRIMARY_WITH_V2_FALLBACK, and V3_ONLY. V3_SHADOW runs V3 in parallel with no external effects. V3_CANARY activates only for specific users, channels, or projects. Rollback is instant by flipping the mode.

## Consequences

- Zero-risk V3 deployment
- Per-user, per-channel, per-project canary testing
- Instant rollback per mode change
- Shadow mode proven by divergence analysis

## References

- ADR-007: V2->V3 Shadow Migration
