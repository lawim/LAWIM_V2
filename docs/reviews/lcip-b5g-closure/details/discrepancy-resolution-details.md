# Discrepancy Resolution — LCIP B.5G-C

| ID | Severity | Old Value | New Value | File Corrected |
|----|----------|-----------|-----------|----------------|
| DISC-001 | LOW | FULLY_CERTIFIED=165 (unclear scope) | FULLY_CERTIFIED=185 (165 remaining + 20 pilot) | REPORT.md |
| DISC-002 | LOW | Language: FR=126, EN=27, PCM=27 (180 only) | FR=142, EN=29, PCM=29 (200 corpus) | REPORT.md |
| DISC-003 | MINOR | RUNTIME_VERDICT=LCIP_B5_PROVEN_RUNTIME_ERRORS_FOUND | LCIP_B5_NO_PROVEN_RUNTIME_ERRORS | REPORT.md |
| DISC-004 | MINOR | Idempotence: CREATION=200 + NO_ACTION=2 (overlap) | CREATION_EXPECTED=198, NO_ACTION_EXPECTED=2 | REPORT.md |
| DISC-005 | MINOR | SHA256SUMS not verifiable from evidence/ | Paths relative to evidence/, 18/18 PASS | evidence/SHA256SUMS |

All resolved without modifying any runtime, specifications, or individual conversation results.
