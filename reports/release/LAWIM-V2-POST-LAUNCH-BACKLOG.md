# LAWIM V2 — Post-Launch Backlog

**Date:** 2026-07-16
**Status:** TRACKED (separate from Go-Live scope)

---

## Register

| # | ID | Description | Priority | Risk | Owner | Target Date | Status |
|---|-----|-------------|----------|------|-------|-------------|--------|
| 1 | PL-001 | **Campay PROD activation** — Enable production payment processing after stabilization period | HIGH | Payment failure, financial loss | Operations | T+2 weeks | PENDING |
| 2 | PL-002 | **Performance baseline measurement** — Run load tests against production to establish p50/p95/p99 latency baselines | HIGH | Performance regression undetected | Engineering | T+1 week | PENDING |
| 3 | PL-003 | **Geo reference catalog fix** — Resolve `/app/lawim_v2/data/cameroon_locations.json` path resolution in container | MEDIUM | Location search fallback unavailable | Engineering | T+1 week | PENDING |
| 4 | PL-004 | **Facebook channel activation** — Enable Facebook Messenger and full publication workflow | LOW | Channel not available | Product | T+4 weeks | PENDING |
| 5 | PL-005 | **SMS channel activation** — Integrate SMS provider for notifications | LOW | Channel not available | Product | T+4 weeks | PENDING |
| 6 | PL-006 | **Published property onboarding** — Activate property owner workflow to publish listings | HIGH | No visible inventory | Operations | T+1 week | PENDING |
| 7 | PL-007 | **Sentry alert tuning** — Configure alert thresholds and notification channels for production | MEDIUM | Operational visibility gap | Engineering | T+1 week | PENDING |
| 8 | PL-008 | **Backup restoration drill** — Execute full restoration in isolated environment and validate data integrity | HIGH | Recovery not proven | Engineering | T+2 weeks | PENDING |
| 9 | PL-009 | **DNSSEC and email authentication** — Configure DKIM, SPF, DMARC for lawim.app domain | MEDIUM | Email deliverability risk | Operations | T+2 weeks | PENDING |
| 10 | PL-010 | **CDN integration** — Configure CDN for static assets (frontend, media) | LOW | Frontend load optimization | Engineering | T+4 weeks | PENDING |
| 11 | PL-011 | **API versioning documentation** — Publish API reference for v2 endpoints | LOW | Developer experience | Documentation | T+4 weeks | PENDING |
| 12 | PL-012 | **Weekly backup verification** — Automate weekly checksum verification and restoration drill | MEDIUM | Backup integrity assurance | Operations | T+2 weeks | PENDING |

---

## Reservations from PROGRAM T

All PROGRAM T reservations carried forward:

| Reservation | Original ID | Status |
|-------------|-------------|--------|
| Campay sandbox only | PROGRAM T-R1 | ✅ RESPECTED |
| Facebook out of scope | PROGRAM T-R2 | ✅ RESPECTED |
| SMS out of scope | PROGRAM T-R3 | ✅ RESPECTED |
| Performance baselines post-launch | PROGRAM T-R4 | 🔄 PL-002 |
| Ghost git objects | PROGRAM T-R5 | ✅ ACCEPTED (non-blocking) |

---

## Governance

- No backlog item may be implemented during Go-Live operations
- Each item requires separate planning, testing, and deployment cycle
- Priority reassessment after T+2 weeks of production stability
- All changes must pass through standard CI/CD pipeline
