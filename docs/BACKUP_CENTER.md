# Backup Center

This document describes the mock backup center architecture for AAC-B2. The implementation is additive and does not alter the existing media registry contract.

## Scope

- OVH VPS as the hot storage layer
- Backup center for orchestration and coordination
- Ten distributed Google Drive placeholders
- Weekly external disk sync placeholder
- Lifecycle-driven restoration and backup policies

## Guardrails

- No real Google Drive URLs are stored in property or media business entities.
- Media entities continue to point to MediaID and the local registry resolves provider access.
- Sensitive values remain placeholders.
