# Procedures

## Operational checklist

1. Generate a fresh Recovery Bundle.
2. Confirm the latest validation snapshot is clean.
3. Verify the isolated recovery test report is present and passing.
4. Restore the approved secrets for the target environment.
5. Run the rebuild script on a blank server or an isolated test workspace.
6. Confirm LAWIM boots and the admin cockpit reports a healthy readiness
   state.

## Incident procedure

- If the primary host is lost, rebuild from Git, the restored secrets, and the
  latest valid bundle.
- If the bundle validation fails, regenerate the bundle before attempting a
  restore.
- If the monthly recovery test fails, treat the DRF as degraded until the test
  passes again.

## Operator guidance

- The Cockpit `Disaster Recovery` tab is the fastest operational entry point.
- Use the bundle download control to preserve a snapshot for offline recovery.
- Do not rely on undocumented manual steps.

## Maintenance cadence

- Daily: inspect the latest bundle and validation snapshot.
- Monthly: run the isolated recovery test.
- After a significant infrastructure change: regenerate the bundle and rerun
  validation.
