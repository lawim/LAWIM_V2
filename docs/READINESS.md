# Readiness

## Objective

Capture the readiness state for Release Program Y using a composite score over infrastructure, application, deployment, security, backup, documentation, and operational domains.

## Metrics

- Infrastructure
- Application
- Deployment
- Security
- Backup
- Documentation
- Operational
- Global readiness

## Use

- Evaluate production readiness before Go/No-Go decisions
- Surface warnings, blocking issues, and recommendations
- Support operational acceptance and release governance

## Implementation

Readiness is calculated in `deployment/acceptance/index.ts` with `ReadinessSummary.calculate()`.
