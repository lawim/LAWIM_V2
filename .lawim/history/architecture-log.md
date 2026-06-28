# Architecture Log

Ce journal est append-only. Toute evolution architecturale doit laisser une trace.

| Date | ID | Topic | Decision | Impact | Owner | Reference |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-28 | ARCH-001 | Docker foundation | Shared base image plus development, staging and production overlays established | Deterministic Docker layering for Sprint 001 | DevOps | reports/sprint-001/T01.02-docker-foundation-report.md |
| 2026-06-28 | ARCH-002 | T01.02 architecture review | Valide avec reserves | Shared base and overlays are coherent; reproducibility reserve remains on mutable base image tag | Architecte Technique | reports/sprint-001/T01.02-architecture-review.md |
| 2026-06-28 | ARCH-003 | Docker Compose foundation | Shared base plus development, staging and production profile contracts established | Stable resource naming and extension path for Sprint 001 | DevOps | reports/sprint-001/T01.03-docker-compose-report.md |
