# Production Runbook

## Purpose

This runbook provides the controlled operational package for a real-server deployment of LAWIM V2 without executing any live migration.

## Scope

- Prepare host, users, files, services, networking, SSL, and backups
- Validate environment and deployment prerequisites
- Execute migration in dry-run and verification-only mode
- Preserve rollback and incident procedures

## Safety

- Backend remains frozen
- No real deployment is executed by this package
- All actions are documented for controlled execution on a real server
