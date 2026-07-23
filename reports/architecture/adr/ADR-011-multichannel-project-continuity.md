# ADR-011: Multichannel Project Continuity

**Status:** Accepted
**Date:** 2026-07-23

## Context

Users start conversations on one channel (WhatsApp) and continue on another (Telegram, Web). Without cross-channel identity linking, each channel creates a separate project.

## Decision

IdentityResolver links channel identities to LAWIM user IDs. ProjectResolver finds the active project for a user regardless of channel. A session tracks the current channel but the project survives session expiry and channel switches. Cross-channel identity requires explicit linking (no automatic merge).

## Consequences

- One project can span multiple channels
- Identity linking requires explicit consent or verification
- Sessions are ephemeral; projects are persistent

## References

- ADR-001: Project-Centric Architecture
- ADR-007: V2->V3 Shadow Migration
