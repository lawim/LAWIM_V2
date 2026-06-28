# Risk History

Ce journal est append-only. Les risques evoluent avec leurs mitigations.

| Date | Risk ID | Risk | Impact | Probability | Mitigation | Owner | Status | Reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-28 | RISK-001 | Divergence between base and environment-specific Docker images | High | Medium | Promote the same digest, freeze tags and reuse the shared base | DevOps | Open | reports/sprint-001/T01.02-docker-foundation-report.md |
| 2026-06-28 | RISK-002 | Drift between Compose overlays and environment contracts | High | Medium | Keep resource names stable, externalize environment values and validate merged config | DevOps | Open | reports/sprint-001/T01.03-docker-compose-report.md |
| 2026-06-28 | RISK-003 | Nginx routing drift between the base proxy config and future virtual hosts | High | Medium | Keep the base server block minimal, isolate additions in conf.d and review routing before production | DevOps | Open | reports/sprint-001/T01.05-nginx-reverse-proxy-foundation-report.md |
| 2026-06-28 | RISK-004 | OVH host role drift between production, local relay and backup layers | High | Medium | Keep host roles documented, avoid real resource creation and align backup conventions with the storage reference | DevOps | Open | reports/sprint-001/T01.06-ovh-infrastructure-foundation-report.md |
| 2026-06-28 | RISK-005 | Secret template drift or leakage through env, Compose or CI/CD wiring | High | Medium | Keep secret values external, centralize the naming convention and review injection paths before use | Security | Open | reports/sprint-001/T01.07-secrets-management-foundation-report.md |
| 2026-06-28 | RISK-006 | Workflow drift, branch-policy mismatch or secret leakage through GitHub Actions wiring | High | Medium | Keep example workflows non-active, enforce minimal permissions, externalize secrets and validate branch mapping before activation | Security | Open | reports/sprint-001/T01.08-ci-cd-foundation-report.md |
| 2026-06-28 | RISK-007 | Logging drift, verbose output or sensitive data exposure through logs | High | Medium | Standardize levels, correlation identifiers, masking and retention rules before any collector is introduced | Security | Open | reports/sprint-001/T01.09-logging-foundation-report.md |
| 2026-06-28 | RISK-008 | Monitoring drift, non-actionable alerts or health-check blind spots | High | Medium | Define signal ownership, thresholds and escalation paths before any monitoring tool is activated | DevOps | Open | reports/sprint-001/T01.10-monitoring-foundation-report.md |
| 2026-06-28 | RISK-009 | T01.04 standalone report gap | Low | Low | Use `env/README.md` and the example environment files as the canonical coverage; the gap is non-blocking for Sprint 001 closure | PMO | Mitigated | reports/sprint-001/SPRINT-001-CLOSURE-REPORT.md |
| 2026-06-28 | RISK-010 | Mutable upstream base tag keeps the Docker baseline reproducibility reserve open | High | Medium | Keep the shared base documented, validate merged config and plan digest pinning in a later hardening ticket | DevOps | Open | reports/sprint-002/T02.01-docker-baseline-report.md |
