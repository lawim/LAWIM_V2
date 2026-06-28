# Architecture Log

Ce journal est append-only. Toute evolution architecturale doit laisser une trace.

| Date | ID | Topic | Decision | Impact | Owner | Reference |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-28 | ARCH-001 | Docker foundation | Shared base image plus development, staging and production overlays established | Deterministic Docker layering for Sprint 001 | DevOps | reports/sprint-001/T01.02-docker-foundation-report.md |
| 2026-06-28 | ARCH-002 | T01.02 architecture review | Valide avec reserves | Shared base and overlays are coherent; reproducibility reserve remains on mutable base image tag | Architecte Technique | reports/sprint-001/T01.02-architecture-review.md |
| 2026-06-28 | ARCH-003 | Docker Compose foundation | Shared base plus development, staging and production profile contracts established | Stable resource naming and extension path for Sprint 001 | DevOps | reports/sprint-001/T01.03-docker-compose-report.md |
| 2026-06-28 | ARCH-004 | Nginx reverse proxy foundation | Base server block, future virtual host split, reusable snippets and external certificate policy established | Stable reverse proxy contract for Compose and production preparation | DevOps | reports/sprint-001/T01.05-nginx-reverse-proxy-foundation-report.md |
| 2026-06-28 | ARCH-005 | OVH infrastructure foundation | Target host roles, network prerequisites, DNS concept, storage hierarchy and automation skeletons established | Operational OVH preparation without real deployment | DevOps | reports/sprint-001/T01.06-ovh-infrastructure-foundation-report.md |
| 2026-06-28 | ARCH-006 | Secrets management foundation | Environment-separated templates, secret naming convention and external injection contract established | Controlled secret handling path for Compose, OVH and CI/CD preparation | DevOps | reports/sprint-001/T01.07-secrets-management-foundation-report.md |
