# ADR-001: Project-Centric Architecture

**Status:** Accepted
**Date:** 2026-07-22

## Context

LAWIM must manage persistent real estate projects spanning days or months. A chatbot-first approach loses state between sessions. Users expect continuity across channels (web, WhatsApp, Telegram) and over time without repeating previously shared information.

## Decision

ProjectProfile is the single source of truth. Conversations are transient sessions that read from and write to ProjectProfile. No business state lives exclusively in conversation memory.

## Justification

This design provides persistence, auditability, and cross-channel continuity. A user can start a search on WhatsApp, continue on web, and complete on Telegram without data loss. All business decisions reference the same authoritative profile.

## Positive Consequences

- State survives session boundaries and channel switches
- Full audit trail of all changes per project
- Cross-channel continuity without duplication
- Clear separation between transient conversation state and persistent business state

## Negative Consequences

- Every conversation turn requires a ProjectProfile load and save
- Increased storage cost per project over long time horizons
- Migration effort for existing V2 conversation data

## Rejected Alternatives

- **Chatbot-first state in memory**: Lost on session timeout, no cross-channel support
- **Database per channel**: Duplication, sync complexity, inconsistency risk

## Affected Components

- ConversationRuntime
- ProjectProfileService
- All channel adapters (WhatsApp, Telegram, Web)
- ConversationStateRepository

## Compliance Criteria

- Every user message triggers ProjectProfile load before processing
- Every response triggers ProjectProfile save after generation
- No business-critical data exists only in conversation memory
- Cross-channel test proves state continuity across two different channels

## References

- ADR-003: ProjectProfile as Source of Truth
- ADR-007: V2->V3 Shadow Migration
