# OPERATIONS

## Purpose

Operational notes for a release that is already packaged for OVH.

## Runtime directories

- application data: `/srv/lawim`
- shared data: `/opt/lawim/shared`
- logs: `/var/log/lawim`
- PostgreSQL data when self-hosted: `/var/lib/postgresql`

## Common actions

- start the approved production compose stack
- check container health and service logs
- rotate or archive logs externally
- keep permissions limited to the service account and the operator group

## Configuration

- use example files only in the repository
- inject real values from an external secret provider
- keep development, staging, and production values separate

