# Storage Resource Registry

The Storage Resource Registry is the canonical activation-ready registry for the ten Google Drive resources used by LAWIM_V2.

## Contract

- Each resource has a theoretical quota of `13 GB`
- No real Google Drive URL is stored in any business data
- No real token, client secret, or refresh token is stored in this release
- Media continue to resolve through `MediaID`
- Conversations continue to resolve through `ConversationID`
- Each resource records logical name, provider, category, state, health, last control, last access, API version, routing strategy, backup policy, and restore policy

## Thresholds

- Normal: `0-70%`
- Attention: `70-85%`
- Slowdown: `85-92%`
- Blocked: `>92%`

## Registry

| Drive | Logical name | Role | Category | Priority | Quota | Used | State | Health | Last control | Last access | API | Routing | Backup | Restore |
|---|---|---|---|---:|---:|---:|---|---|---|---|---|---|---|---|
| Drive 1 | `videos-a` | Videos A | Video | 1 | 13 GB | 3.2 GB | ready | healthy | `2026-07-05T10:00:00Z` | `2026-07-05T10:00:00Z` | v3 | official-priority-route | backup-center-activation | restore-center-activation |
| Drive 2 | `videos-b` | Videos B | Video | 2 | 13 GB | 4.1 GB | ready | healthy | `2026-07-05T10:00:00Z` | `2026-07-05T10:00:00Z` | v3 | official-priority-route | backup-center-activation | restore-center-activation |
| Drive 3 | `photos-audio` | Photos + Audio | Photo / Audio | 3 | 13 GB | 5.8 GB | ready | healthy | `2026-07-05T10:00:00Z` | `2026-07-05T10:00:00Z` | v3 | official-priority-route | backup-center-activation | restore-center-activation |
| Drive 4 | `documents` | Documents | Document | 4 | 13 GB | 6.4 GB | ready | healthy | `2026-07-05T10:00:00Z` | `2026-07-05T10:00:00Z` | v3 | official-priority-route | backup-center-activation | restore-center-activation |
| Drive 5 | `conversation-registry` | Conversation Registry | Conversation archive | 5 | 13 GB | 9.4 GB | watch | watch | `2026-07-05T10:00:00Z` | `2026-07-05T10:00:00Z` | v3 | official-priority-route | backup-center-activation | restore-center-activation |
| Drive 6 | `exports-reports-stats` | Exports / reports / statistics | Export / report | 6 | 13 GB | 10.5 GB | watch | watch | `2026-07-05T10:00:00Z` | `2026-07-05T10:00:00Z` | v3 | official-priority-route | backup-center-activation | restore-center-activation |
| Drive 7 | `application-backups` | Application backups | Backup applicatif | 7 | 13 GB | 11.9 GB | degraded | degraded | `2026-07-05T10:00:00Z` | `2026-07-05T10:00:00Z` | v3 | official-priority-route | backup-center-activation | restore-center-activation |
| Drive 8 | `replication-overflow` | Replication / overflow | Replication critique | 8 | 13 GB | 12.4 GB | blocked | blocked | `2026-07-05T10:00:00Z` | `2026-07-05T10:00:00Z` | v3 | official-priority-route | backup-center-activation | restore-center-activation |
| Drive 9 | `strategic-reserve` | Strategic reserve | Reserve | 9 | 13 GB | 1.3 GB | ready | healthy | `2026-07-05T10:00:00Z` | `2026-07-05T10:00:00Z` | v3 | official-priority-route | backup-center-activation | restore-center-activation |
| Drive 10 | `maintenance-migration` | Maintenance / migration | Maintenance / migration | 10 | 13 GB | 3.9 GB | ready | healthy | `2026-07-05T10:00:00Z` | `2026-07-05T10:00:00Z` | v3 | official-priority-route | backup-center-activation | restore-center-activation |

## Operational summary

- Available resources: Drive 1, Drive 2, Drive 3, Drive 4, Drive 5, Drive 6, Drive 7, Drive 9, Drive 10
- Blocked resources: Drive 8
- Alerts are generated when a resource leaves the normal band
- The registry is ready for the secure onboarding of the real Google credentials later

## Related documents

- `docs/GOOGLE_DRIVE_CONNECTOR.md`
- `docs/GOOGLE_DRIVE_ADMIN_CENTER.md`
- `docs/GOOGLE_DRIVE_OAUTH.md`
- `docs/GOOGLE_DRIVE_SETUP.md`
- `docs/GOOGLE_DRIVE_MONITORING.md`
- `docs/STORAGE_ROUTING_POLICY.md`
- `docs/GOOGLE_DRIVE_QUOTA_POLICY.md`
- `docs/STORAGE_SETUP_WIZARD.md`
