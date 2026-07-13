# Feature Management Architecture

This document describes the canonical feature-management model for LAWIM_V2.

## Principles

- One central registry for modules, features, flags, dependencies, and scopes.
- A flag never grants permission by itself.
- A disabled feature must fail closed.
- Kill switches are always evaluated before feature flags.
- The backend is the source of truth; the frontend only consumes the capability manifest.

## Evaluation order

1. Global kill switch
2. Environment
3. Module status
4. Feature status
5. Dependency availability
6. Scope checks
7. Permission checks
8. Consent checks
9. Default fallback

## Scopes

- GLOBAL
- ENVIRONMENT
- ORGANIZATION
- AGENCY
- ROLE
- USER
- SUBSCRIPTION_PLAN
- COUNTRY
- REGION
- PERCENTAGE
- DATE_RANGE

## Operational expectations

- Every change is audited.
- Sensitive changes require confirmation and justification.
- Feature evaluation must be deterministic and reproducible.
- `GET /api/capabilities` exposes the safe runtime manifest.

