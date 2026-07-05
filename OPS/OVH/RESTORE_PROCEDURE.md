# Restore Procedure

## Release rollback

1. stop the application stack;
2. repoint `/opt/lawim/current` to the previous release;
3. restart the stack;
4. verify `/healthz`, `/readyz` and `/api/health`.

## Data restore

1. stop PostgreSQL and the application;
2. restore the most recent validated database dump;
3. restore media or shared files only if the incident requires it;
4. restart PostgreSQL, Redis and the application;
5. re-run the healthchecks.

## Restore discipline

- never restore over an unverified backup;
- never restore production data without a prior backup of the current state;
- keep the restore logs with the backup bundle.
