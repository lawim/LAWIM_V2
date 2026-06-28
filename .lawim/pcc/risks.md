# Risks PCC

| ID | Risk | Impact | Probability | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | Backlog canonique non totalement verifie | Medium | Medium | Verifier le backlog avant les tickets metier | Directeur General | Open |
| R-002 | Derive de secret ou de configuration | High | Medium | Appliquer les regles de securite et de traceabilite | Securite | Open |
| R-003 | Ambiguite d'infrastructure entre environnements | High | Medium | Formaliser les conventions d'environnement et de deploiement | DevOps | Open |
| R-004 | Derive entre la base Docker et les overlays environnementaux | High | Medium | Promouvoir le meme digest, figer les tags et reutiliser la base commune | DevOps | Open |
| R-005 | Drift between Compose overlays and environment contracts | High | Medium | Keep resource names stable, externalize environment values and validate merged config | DevOps | Open |
| R-006 | Nginx routing drift between default.conf and future virtual hosts | High | Medium | Keep the base server block minimal and isolate additions in conf.d with explicit review | DevOps | Open |
| R-007 | OVH host role drift between production, local relay and backup layers | High | Medium | Keep host roles documented, avoid real resource creation and align backup conventions with the storage reference | DevOps | Open |
| R-008 | Secret template drift or leakage through env, Compose or CI/CD wiring | High | Medium | Keep secret values external, centralize the naming convention and review injection paths before use | Security | Open |
| R-009 | Workflow drift, branch-policy mismatch or secret leakage through GitHub Actions wiring | High | Medium | Keep example workflows non-active, enforce minimal permissions, externalize secrets and validate branch mapping before activation | Security | Open |
| R-010 | Logging drift, verbose output or sensitive data exposure through logs | High | Medium | Standardize levels, correlation identifiers, masking and retention rules before any collector is introduced | Security | Open |
| R-011 | Monitoring drift, non-actionable alerts or health-check blind spots | High | Medium | Define signal ownership, thresholds and escalation paths before any monitoring tool is activated | DevOps | Open |
| R-012 | Sprint 002 opened before DG opening decision is traced | High | Low | Record the DG opening decision in the execution trace and keep ticket states synchronized | PMO | Mitigated |
| R-013 | Docker baseline drifts from the inherited runtime contract | High | Medium | Reuse the shared base, keep overlays deterministic and validate merged config before use | DevOps | Open |
| R-014 | CI skeleton or observability exposes secrets or masks failures | High | Medium | Keep secrets external, validate log masking and health checks before activation | Security | Mitigated |
