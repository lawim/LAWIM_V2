# Release Activation Runbook

## Before release

- Verify git status.
- Verify no secret is present in tracked files.
- Run the relevant test suite.
- Build the frontend when the UI is touched.

## Release steps

- Create the release commit.
- Deploy the approved artifact.
- Apply migrations if required.
- Restart the necessary services only.
- Check health endpoints and logs.

## Rollback

- Revert to the previous known-good release.
- Do not delete persisted conversation or audit data.
- Record the incident and root cause.

