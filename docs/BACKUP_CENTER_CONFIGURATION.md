# Backup Center Configuration

The Backup Center is the operational layer that coordinates local backup, external disk backup, and the distributed Google Drive targets.

## Scope

- Local backup on OVH
- External disk backup
- Drive 7 for application backups
- Drive 8 for overflow and replication pressure
- Drive 9 for reserve
- Drive 10 for maintenance and migration

## Operating rules

- No real Google credentials are stored here
- No direct Google Drive URL is stored in business data
- Media continue to resolve through `MediaID`
- Conversations continue to resolve through `ConversationID`
- The Storage Orchestrator remains the decision maker for route selection

## Operational surfaces

- Global storage summary
- Alerts and blocked resources
- Last mock test timestamp
- Capacity remaining
- Backup status

## Related configuration

- `docs/STORAGE_RESOURCE_REGISTRY.md`
- `docs/STORAGE_ROUTING_POLICY.md`
- `docs/GOOGLE_DRIVE_QUOTA_POLICY.md`
