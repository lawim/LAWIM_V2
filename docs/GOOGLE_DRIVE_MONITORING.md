# Google Drive Monitoring

The Google Drive monitoring view tracks the operational readiness of the distributed storage layer.

## Metrics

- Quota usage
- Available capacity
- Latency
- Throughput
- API status
- OAuth state
- Occupation
- Rotation
- Alerts
- Incidents

## Rotation model

- Video: Drive 1 -> Drive 2 -> Drive 8
- Photo: Drive 3 -> Drive 8
- Audio: Drive 3 -> Drive 8
- Document: Drive 4 -> Drive 8
- Conversation archive: Drive 5 -> Drive 8
- Backup: Drive 7 -> Drive 10
- Export: Drive 6 -> Drive 8
- Maintenance: Drive 10

## Alert policy

- Normal resources stay in the primary pool
- Attention and slowdown resources remain visible
- Blocked resources are retained in the registry but excluded from large-file routing

## Output contract

- Monitoring is exposed in the admin center
- Monitoring is also reused by the backup center and the setup wizard summaries
