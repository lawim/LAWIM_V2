# Mission 13.2 - Lot 5 - Isolated Reconstruction Tests

## Objective

Run the rebuild flow in an isolated workspace, measure duration, and produce a
repeatable monthly recovery test report without touching production paths.

## Delivered Files

- `deployment/recovery/monthly-recovery-test.sh`
- `deployment/systemd/lawim-recovery-test.service`
- `deployment/systemd/lawim-recovery-test.timer`
- `tests/test_recovery_monthly_test.py`

## Implemented Behavior

The monthly recovery test now:

- selects the latest DRF bundle or honors an explicit bundle override;
- runs `rebuild-lawim.sh` in `--dry-run` mode inside an isolated workspace;
- measures execution time;
- writes machine-readable and Markdown reports to the recovery test report
  directory;
- keeps the runtime workspace separate from the production root.

The systemd timer schedules the recovery test monthly.

## Validation

Executed:

- `python3 -m unittest tests.test_recovery_monthly_test tests.test_disaster_recovery_validation tests.test_disaster_recovery_bundle tests.test_recovery_script tests.test_backup_api tests.test_backup_module`

Result:

- all targeted tests passed
- the monthly recovery test writes `latest-report.json` and `latest-report.md`
- repeated runs remain isolated and successful
- no production path is touched during the test harness

## Notes

- The report payload records bundle ID, exit code, run ID, timestamps, and the
  dry-run rebuild output.
- The isolated workspace uses a temporary root under the configured recovery
  test directory.
