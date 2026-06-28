# Decision Log

Ce journal est append-only. Toute nouvelle decision cree une nouvelle entree.

| Date | ID | Decision | Owner | Scope | Status | Reference |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-28 | DEC-001 | Pin a shared Docker base image and derive environment overlays from it | DevOps | Docker foundation | Active | reports/sprint-001/T01.02-docker-foundation-report.md |
| 2026-06-28 | DEC-002 | Adopt a shared Compose base with development, staging and production profile overlays | DevOps | Docker Compose foundation | Active | reports/sprint-001/T01.03-docker-compose-report.md |
| 2026-06-28 | DEC-003 | Adopt a shared Nginx reverse proxy foundation with default.conf, conf.d, snippets and external certificates | DevOps | Nginx foundation | Active | reports/sprint-001/T01.05-nginx-reverse-proxy-foundation-report.md |
| 2026-06-28 | DEC-004 | Adopt an OVH infrastructure foundation with conceptual DNS, backup and administration conventions | DevOps | OVH foundation | Active | reports/sprint-001/T01.06-ovh-infrastructure-foundation-report.md |
| 2026-06-28 | DEC-005 | Adopt a secrets management foundation with environment-separated templates and external injection | DevOps | Secrets foundation | Active | reports/sprint-001/T01.07-secrets-management-foundation-report.md |
| 2026-06-28 | DEC-006 | Adopt a split CI/CD foundation with branch-gated validation, digest promotion and external secrets | DevOps | CI/CD foundation | Active | reports/sprint-001/T01.08-ci-cd-foundation-report.md |
| 2026-06-28 | DEC-007 | Adopt the DG-0026 orchestrator orientation and freeze governance until Sprint 001 closes | Directeur General | Architecture backlog / Sprint 001 freeze | Active | .lawim/architecture-backlog/DG-0026-ORIENTATION-STRATEGIQUE.md |
| 2026-06-28 | DEC-008 | Adopt a logging foundation with documented strategy, levels, rotation, masking and monitoring preparation | DevOps | Logging foundation | Active | reports/sprint-001/T01.09-logging-foundation-report.md |
| 2026-06-28 | DEC-009 | Adopt a monitoring foundation with technical metrics, availability, alerting and health checks | DevOps | Monitoring foundation | Active | reports/sprint-001/T01.10-monitoring-foundation-report.md |
| 2026-06-28 | DEC-010 | Sprint 001 closure proposal and freeze of further sprint openings | Directeur General | Sprint 001 closure / no Sprint 002 | Proposed | reports/sprint-001/SPRINT-001-CLOSURE-REPORT.md |
| 2026-06-28 | DEC-011 | Docker baseline, Compose contract and Nginx/environment baseline confirmed for LAWIM_V2 | DevOps | T02.01 / Docker baseline | Active | reports/sprint-002/T02.01-docker-baseline-report.md |
| 2026-06-28 | DEC-012 | Runtime observability, logging conventions and health-check contract confirmed for LAWIM_V2 | DevOps | T02.02 / Runtime observability | Active | reports/sprint-002/T02.02-runtime-observability-report.md |
| 2026-06-28 | DEC-013 | CI skeleton, branch gates and external-secret conventions confirmed for LAWIM_V2 | DevOps | T02.03 / CI skeleton | Active | reports/sprint-002/T02.03-ci-skeleton-report.md |
| 2026-06-28 | DEC-014 | Sprint 002 closure proposal and no Sprint 003 opening | Directeur General | Sprint 002 closure / no Sprint 003 | Proposed | reports/sprint-002/SPRINT-002-CLOSURE-REPORT.md |
| 2026-06-28 | DEC-015 | Sprint 003 opening and database/storage plan confirmed | Directeur General | Sprint 003 / base de donnees et stockage | Active | reports/sprint-003/SPRINT-003-PLANNING-REPORT.md |
| 2026-06-28 | DEC-016 | PostgreSQL foundation, connection baseline and constraint contract confirmed | Database | T03.01 / PostgreSQL foundation | Active | reports/sprint-003/T03.01-postgresql-foundation-report.md |
| 2026-06-28 | DEC-017 | Prisma baseline, schema mapping and migration conventions confirmed | Database | T03.02 / Prisma baseline | Active | reports/sprint-003/T03.02-prisma-baseline-report.md |
| 2026-06-28 | DEC-018 | Backup primitives, checksum contract and restore conventions confirmed | DevOps | T03.03 / Backup primitives | Active | reports/sprint-003/T03.03-backup-primitives-report.md |
| 2026-06-28 | DEC-019 | Sprint 003 closure proposal and no Sprint 004 opening | Directeur General | Sprint 003 closure / no Sprint 004 | Proposed | reports/sprint-003/SPRINT-003-CLOSURE-REPORT.md |
| 2026-06-28 | DEC-020 | Sprint 004 opening and authentication/identity plan confirmed | Directeur General | Sprint 004 / authentification et identite | Active | reports/sprint-004/SPRINT-004-PLANNING-REPORT.md |
| 2026-06-28 | DEC-021 | Auth service, login/logout and session contract confirmed | Security | T04.01 / Auth service | Active | reports/sprint-004/T04.01-auth-service-report.md |
| 2026-06-28 | DEC-022 | Token strategy, JWT refresh and session storage confirmed | Security | T04.02 / Token strategy | Active | reports/sprint-004/T04.02-token-strategy-report.md |
| 2026-06-28 | DEC-023 | MFA gate, recovery and access policy confirmed | Security | T04.03 / MFA gate | Active | reports/sprint-004/T04.03-mfa-gate-report.md |
| 2026-06-28 | DEC-024 | Sprint 004 closure proposal and no Sprint 005 opening | Directeur General | Sprint 004 closure / no Sprint 005 | Proposed | reports/sprint-004/SPRINT-004-CLOSURE-REPORT.md |
| 2026-06-28 | DEC-025 | Sprint 005 opening and users/roles/organizations plan confirmed | Directeur General | Sprint 005 / users, roles et organisations | Active | reports/sprint-005/SPRINT-005-PLANNING-REPORT.md |
| 2026-06-28 | DEC-026 | User lifecycle, single-account and status contract confirmed | Security | T05.01 / User lifecycle | Active | reports/sprint-005/T05.01-user-lifecycle-report.md |
| 2026-06-28 | DEC-027 | Organization model, hierarchy and attachment contract confirmed | Administration | T05.02 / Organization model | Active | reports/sprint-005/T05.02-organization-model-report.md |
| 2026-06-28 | DEC-028 | Permissions matrix, inheritance and delegation contract confirmed | Security | T05.03 / Permissions matrix | Active | reports/sprint-005/T05.03-permissions-matrix-report.md |
| 2026-06-28 | DEC-029 | Sprint 005 closure proposal and no Sprint 006 opening | Directeur General | Sprint 005 closure / no Sprint 006 | Proposed | reports/sprint-005/SPRINT-005-CLOSURE-REPORT.md |
| 2026-06-28 | DEC-030 | Sprint 006 opening and core immobilier plan confirmed | Directeur General | Sprint 006 / coeur immobilier | Active | reports/sprint-006/SPRINT-006-PLANNING-REPORT.md |
| 2026-06-28 | DEC-031 | Property domain schema, status model and attribute normalization confirmed | Architecture | T06.01 / Property domain schema | Active | reports/sprint-006/T06.01-property-domain-schema-report.md |
| 2026-06-28 | DEC-032 | Pricing alignment, currency contract and variation history confirmed | Reporting | T06.02 / Pricing alignment | Active | reports/sprint-006/T06.02-pricing-alignment-report.md |
| 2026-06-28 | DEC-033 | Publication guardrails, status transitions and validation gates confirmed | Workflow | T06.03 / Publication guardrails | Active | reports/sprint-006/T06.03-publication-guardrails-report.md |
| 2026-06-28 | DEC-034 | Sprint 006 closure proposal and no Sprint 007 opening | Directeur General | Sprint 006 closure / no Sprint 007 | Proposed | reports/sprint-006/SPRINT-006-CLOSURE-REPORT.md |
| 2026-06-28 | DEC-035 | Sprint 007 opening and media/document/geo plan confirmed | Directeur General | Sprint 007 / medias, documents et geolocalisation | Active | reports/sprint-007/SPRINT-007-PLANNING-REPORT.md |
| 2026-06-28 | DEC-036 | Media pipeline, storage and thumbnail contract confirmed | Architecture | T07.01 / Media pipeline | Active | reports/sprint-007/T07.01-media-pipeline-report.md |
| 2026-06-28 | DEC-037 | Document pipeline, verification and archive contract confirmed | Security | T07.02 / Document pipeline | Active | reports/sprint-007/T07.02-document-pipeline-report.md |
| 2026-06-28 | DEC-038 | Geo integration, locality and traceability contract confirmed | Architecture | T07.03 / Geo integration | Active | reports/sprint-007/T07.03-geo-integration-report.md |
| 2026-06-28 | DEC-039 | Sprint 007 closure proposal and no Sprint 008 opening | Directeur General | Sprint 007 closure / no Sprint 008 | Proposed | reports/sprint-007/SPRINT-007-CLOSURE-REPORT.md |
| 2026-06-28 | DEC-040 | Sprint 008 opening and conversation plan confirmed | Directeur General | Sprint 008 / conversation engine | Active | reports/sprint-008/SPRINT-008-PLANNING-REPORT.md |
| 2026-06-28 | DEC-041 | Conversation model, thread and participant contract confirmed | Architecture | T08.01 / Conversation model | Active | reports/sprint-008/T08.01-conversation-model-report.md |
| 2026-06-28 | DEC-042 | Messaging flow, delivery and read-state contract confirmed | Integration | T08.02 / Messaging flow | Active | reports/sprint-008/T08.02-messaging-flow-report.md |
| 2026-06-28 | DEC-043 | Sprint 008 closure proposal and no Sprint 009 opening | Directeur General | Sprint 008 closure / no Sprint 009 | Proposed | reports/sprint-008/SPRINT-008-CLOSURE-REPORT.md |
| 2026-06-28 | DEC-044 | Sprint 009 opening and matching plan confirmed | Directeur General | Sprint 009 / matching foundation | Active | reports/sprint-009/SPRINT-009-PLANNING-REPORT.md |
| 2026-06-28 | DEC-045 | Search and ranking, relevance and pricing contract confirmed | Architecture | T09.01 / Search and ranking | Active | reports/sprint-009/T09.01-search-ranking-report.md |
| 2026-06-28 | DEC-046 | Qualification, scoring and explainability contract confirmed | Architecture | T09.02 / Qualification and scoring | Active | reports/sprint-009/T09.02-qualification-scoring-report.md |
| 2026-06-28 | DEC-047 | Availability, preferences and location filters contract confirmed | Architecture | T09.03 / Availability and preferences | Active | reports/sprint-009/T09.03-availability-preferences-report.md |
| 2026-06-28 | DEC-048 | Sprint 009 closure proposal and no Sprint 010 opening | Directeur General | Sprint 009 closure / no Sprint 010 | Proposed | reports/sprint-009/SPRINT-009-CLOSURE-REPORT.md |
| 2026-06-28 | DEC-001 | Sprint 010 opening and decision engine et rematching plan confirmed | Directeur General | Sprint 010 / decision engine et rematching | Active | reports/sprint-010/SPRINT-010-PLANNING-REPORT.md |
| 2026-06-28 | DEC-002 | Decision orchestration, contract confirmed for Sprint 010 | Architecture | T10.01 / Decision orchestration | Active | reports/sprint-010/T10.01-decision-orchestration-report.md |
| 2026-06-28 | DEC-003 | Rematching flow, contract confirmed for Sprint 010 | Architecture | T10.02 / Rematching flow | Active | reports/sprint-010/T10.02-rematching-flow-report.md |
