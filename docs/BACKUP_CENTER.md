# Backup Center

This document describes the mock backup center architecture for LAWIM_V2. The implementation is additive and does not alter the existing media registry contract.

## Scope

- OVH VPS as the hot storage layer
- Backup center for orchestration and coordination
- Ten distributed Google Drive placeholders
- Weekly external disk sync placeholder
- Lifecycle-driven restoration and backup policies

## Guardrails

- No real Google Drive URL is stored in property, media, or conversation business entities
- Media entities continue to point to `MediaID`
- Conversations continue to point to `ConversationID`
- Sensitive values remain placeholders

## Configuration source

- `docs/BACKUP_CENTER_CONFIGURATION.md`
- `docs/STORAGE_RESOURCE_REGISTRY.md`
- `docs/STORAGE_ROUTING_POLICY.md`
