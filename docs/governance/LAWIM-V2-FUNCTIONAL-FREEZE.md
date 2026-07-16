# LAWIM_V2 — FUNCTIONAL FREEZE

## Declaration
LAWIM_V2 is now functionally frozen as of 2026-07-16T19:00:00Z.

## Scope
All code under `code/`, `frontend/`, `tests/`, `scripts/`, `deployment/`, `docs/`.

## Frozen features
- All business features (H through T programs)
- All AI agents and fallback chains
- All communication channels
- All qualification, search, and matching logic
- All frontend surfaces
- All API contracts
- All database schemas
- All provider integrations
- All payment integrations (Campay remains disabled)
- All feature flags

## Permitted changes
- P0 (data loss, security critical, production unusable)
- P1 (core feature broken, high security)
- Security patches
- Translation corrections
- Data corrections (test data only)
- Deployment configuration
- Regression fixes
- Documentation

## Prohibited changes
- New features
- New agents
- New business modules
- New channels
- New workflows
- New taxonomies
- New interfaces
- New providers
- New API endpoints
- Schema changes without migration plan

## Change procedure
1. Classify the change (P0/P1/security/translation/docs/config)
2. Create a hotfix branch from `main`
3. Implement the fix
4. Run all tests
5. Peer review
6. Merge into `main`
7. Deploy to staging
8. Run smoke tests
9. Deploy to production

## Rollback
If a hotfix introduces a regression, revert the hotfix commit and deploy the previous version.

## Test phase
All future work beyond permitted changes belongs to the test phase:
- Functional testing
- User acceptance testing
- Linguistic testing
- Multi-channel testing
- Admin testing
- Agent testing
- Security testing
- Performance testing
- Load testing
- Recovery testing
- Acceptance certification
