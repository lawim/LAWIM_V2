# Risk History

Ce journal est append-only. Les risques evoluent avec leurs mitigations.

| Date | Risk ID | Risk | Impact | Probability | Mitigation | Owner | Status | Reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-28 | RISK-001 | Divergence between base and environment-specific Docker images | High | Medium | Promote the same digest, freeze tags and reuse the shared base | DevOps | Open | reports/sprint-001/T01.02-docker-foundation-report.md |
| 2026-06-28 | RISK-002 | Drift between Compose overlays and environment contracts | High | Medium | Keep resource names stable, externalize environment values and validate merged config | DevOps | Open | reports/sprint-001/T01.03-docker-compose-report.md |
