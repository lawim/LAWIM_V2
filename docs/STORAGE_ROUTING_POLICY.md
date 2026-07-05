# Storage Routing Policy

The Storage Orchestrator chooses the first available resource on the ordered route for each content class.

## Official routes

- Video: Drive 1 -> Drive 2 -> Drive 8
- Photo: Drive 3 -> Drive 8
- Audio: Drive 3 -> Drive 8
- Document: Drive 4 -> Drive 8
- Conversation archive: Drive 5 -> Drive 8
- Export / report / statistics: Drive 6 -> Drive 8
- Application backup: Drive 7 -> Drive 10
- Critical replication: Drive 8 -> Drive 10
- Reserve: Drive 9
- Maintenance / migration: Drive 10

## Selection rule

1. Normalize the requested category
2. Resolve the ordered route
3. Pick the first resource that is not blocked and still has available quota
4. If every candidate is constrained, keep the final fallback visible in the trace

## Band handling

- Normal resources are preferred
- Attention and slowdown resources remain selectable for fallback routing
- Blocked resources are not used for large-file routing

## Storage Orchestrator contract

- Media requests route by media class
- Conversation archives route to Drive 5 first and Drive 8 as overflow
- The route is traceable and documented in the admin dashboard

## Related documents

- `docs/STORAGE_RESOURCE_REGISTRY.md`
- `docs/GOOGLE_DRIVE_QUOTA_POLICY.md`
- `docs/STORAGE_SETUP_WIZARD.md`
