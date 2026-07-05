# Storage Resource Registry

The Storage Resource Registry is the canonical mock registry for the ten Google Drive resources used by LAWIM_V2.

## Rules

- Each resource has a theoretical quota of `13 GB`
- No real Google Drive URL is stored in any business data
- No real token, client secret, or refresh token is stored in this release
- Media continue to resolve through `MediaID`
- Conversations continue to resolve through `ConversationID`

## Thresholds

- Normal: `0-70%`
- Attention: `70-85%`
- Slowdown: `85-92%`
- Blocked: `>92%`

## Registry

| Drive | Logical name | Role | Category | Priority | Quota | Mock band | Status | Health | Last test |
|---|---|---|---|---:|---:|---|---|---|---|
| Drive 1 | `videos-a` | Videos A | Video | 1 | 13 GB | Normal | ready | healthy | `mock-2026-07-05T10:00:00Z` |
| Drive 2 | `videos-b` | Videos B | Video | 2 | 13 GB | Normal | ready | healthy | `mock-2026-07-05T10:00:00Z` |
| Drive 3 | `photos-audio` | Photos + Audio | Photo / Audio | 3 | 13 GB | Normal | ready | healthy | `mock-2026-07-05T10:00:00Z` |
| Drive 4 | `documents` | Documents | Document | 4 | 13 GB | Normal | ready | healthy | `mock-2026-07-05T10:00:00Z` |
| Drive 5 | `conversation-registry` | Conversation Registry | Conversation archive | 5 | 13 GB | Attention | watch | watch | `mock-2026-07-05T10:00:00Z` |
| Drive 6 | `exports-reports-stats` | Exports / reports / statistics | Export / report | 6 | 13 GB | Attention | watch | watch | `mock-2026-07-05T10:00:00Z` |
| Drive 7 | `application-backups` | Application backups | Backup applicatif | 7 | 13 GB | Slowdown | degraded | degraded | `mock-2026-07-05T10:00:00Z` |
| Drive 8 | `replication-overflow` | Replication / overflow | Replication critique | 8 | 13 GB | Blocked | blocked | blocked | `mock-2026-07-05T10:00:00Z` |
| Drive 9 | `strategic-reserve` | Strategic reserve | Reserve | 9 | 13 GB | Normal | ready | healthy | `mock-2026-07-05T10:00:00Z` |
| Drive 10 | `maintenance-migration` | Maintenance / migration | Maintenance / migration | 10 | 13 GB | Normal | ready | healthy | `mock-2026-07-05T10:00:00Z` |

## Operational summary

- Available resources: Drive 1, Drive 2, Drive 3, Drive 4, Drive 5, Drive 6, Drive 7, Drive 9, Drive 10
- Blocked resources: Drive 8
- Alerts are generated when a resource leaves the normal band
- The registry is mock-safe and ready to accept the secure assistant phase for real Google credentials

## Related documents

- `docs/GOOGLE_DRIVE_FUNCTIONAL_CONFIGURATION.md`
- `docs/STORAGE_ROUTING_POLICY.md`
- `docs/GOOGLE_DRIVE_QUOTA_POLICY.md`
- `docs/STORAGE_SETUP_WIZARD.md`
