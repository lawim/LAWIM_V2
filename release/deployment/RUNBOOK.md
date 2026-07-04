# RUNBOOK

## Scope

Release-only operational steps for a controlled OVH deployment.

## Pre-flight

- confirm the snapshot id and checksum set
- confirm that no migration is being launched
- confirm that secrets are supplied externally
- confirm that the payload matches `manifests/DEPLOYMENT_MANIFEST.md`

## Deploy

- validate the compose configuration
- start the production stack with the approved launch script
- ensure that runtime configuration comes from example templates and external environment values
- record the release snapshot id and the checksum set

## Verify

- check `/healthz`
- check `/readyz`
- check `/api/health`
- validate service-specific health endpoints from the deployment compose files

## Rollback

- stop the current stack
- restore the previous known-good release payload
- restore the matching backup set if data rollback is required
- re-run the health checks before reopening traffic

