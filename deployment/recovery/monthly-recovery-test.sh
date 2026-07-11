#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REBUILD_SCRIPT="$SCRIPT_DIR/rebuild-lawim.sh"

RECOVERY_TEST_ROOT="${LAWIM_RECOVERY_TEST_ROOT:-/var/lib/lawim-backup/recovery-tests}"
RECOVERY_REPORT_DIR="${LAWIM_RECOVERY_REPORT_DIR:-$RECOVERY_TEST_ROOT/reports}"
RECOVERY_RUN_DIR="${LAWIM_RECOVERY_RUN_DIR:-$RECOVERY_TEST_ROOT/runs}"
RECOVERY_WORK_DIR="${LAWIM_RECOVERY_WORK_DIR:-$RECOVERY_TEST_ROOT/work}"
RECOVERY_BUNDLE_ROOT="${LAWIM_RECOVERY_BUNDLE_ROOT:-/var/lib/lawim-backup/recovery-bundles}"
RECOVERY_BUNDLE="${LAWIM_RECOVERY_BUNDLE:-}"

log() {
  printf '[monthly-recovery-test] %s\n' "$*"
}

die() {
  printf '[monthly-recovery-test] ERROR: %s\n' "$*" >&2
  exit 1
}

manifest_value() {
  local manifest_path="$1"
  local key="$2"
  python3 - "$manifest_path" "$key" <<'PY'
import json
import sys

manifest_path = sys.argv[1]
key = sys.argv[2]

with open(manifest_path, "r", encoding="utf-8") as handle:
    payload = json.load(handle)

value = payload.get(key, "")
if value is None:
    print("")
elif isinstance(value, (dict, list)):
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))
else:
    print(value)
PY
}

latest_bundle_dir() {
  if [[ -n "$RECOVERY_BUNDLE" ]]; then
    printf '%s\n' "$RECOVERY_BUNDLE"
    return 0
  fi

  if [[ ! -d "$RECOVERY_BUNDLE_ROOT" ]]; then
    return 0
  fi

  find "$RECOVERY_BUNDLE_ROOT" -mindepth 1 -maxdepth 1 -type d -name 'LAWIM-DRF-*' | sort | tail -n 1
}

load_bundle() {
  local bundle_dir
  bundle_dir="$(latest_bundle_dir)"
  if [[ -z "${bundle_dir:-}" || ! -d "$bundle_dir" ]]; then
    die "recovery bundle not found; set LAWIM_RECOVERY_BUNDLE or populate $RECOVERY_BUNDLE_ROOT"
  fi
  [[ -f "$bundle_dir/manifest.json" ]] || die "missing manifest.json in $bundle_dir"
  [[ -f "$bundle_dir/database/postgresql.dump.sql" ]] || die "missing database dump in $bundle_dir"
  printf '%s\n' "$bundle_dir"
}

write_report() {
  local report_json="$1"
  local report_md="$2"
  local bundle_dir="$3"
  local bundle_id="$4"
  local run_id="$5"
  local started_at="$6"
  local completed_at="$7"
  local duration_seconds="$8"
  local exit_code="$9"
  local rebuild_output="${10}"

  export RECOVERY_BUNDLE_DIR="$bundle_dir"
  export RECOVERY_BUNDLE_ID="$bundle_id"
  export RECOVERY_RUN_ID="$run_id"
  export RECOVERY_STARTED_AT="$started_at"
  export RECOVERY_COMPLETED_AT="$completed_at"
  export RECOVERY_DURATION_SECONDS="$duration_seconds"
  export RECOVERY_EXIT_CODE="$exit_code"
  export RECOVERY_OUTPUT="$rebuild_output"

  python3 - "$report_json" "$report_md" <<'PY'
import json
import os
import pathlib
import sys

report_json = pathlib.Path(sys.argv[1])
report_md = pathlib.Path(sys.argv[2])

output_lines = [line for line in os.environ.get("RECOVERY_OUTPUT", "").splitlines() if line.strip()]
payload = {
    "bundle_id": os.environ.get("RECOVERY_BUNDLE_ID", ""),
    "bundle_path": os.environ.get("RECOVERY_BUNDLE_DIR", ""),
    "completed_at": os.environ.get("RECOVERY_COMPLETED_AT", ""),
    "duration_seconds": float(os.environ.get("RECOVERY_DURATION_SECONDS", "0") or 0),
    "exit_code": int(os.environ.get("RECOVERY_EXIT_CODE", "0") or 0),
    "run_id": os.environ.get("RECOVERY_RUN_ID", ""),
    "started_at": os.environ.get("RECOVERY_STARTED_AT", ""),
    "status": "PASS" if int(os.environ.get("RECOVERY_EXIT_CODE", "0") or 0) == 0 else "FAIL",
    "stdout": output_lines,
}
report_json.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

markdown = [
    "# Monthly Recovery Test",
    "",
    f"- Run ID: `{payload['run_id']}`",
    f"- Bundle: `{payload['bundle_id']}`",
    f"- Bundle path: `{payload['bundle_path']}`",
    f"- Started at: `{payload['started_at']}`",
    f"- Completed at: `{payload['completed_at']}`",
    f"- Duration: `{payload['duration_seconds']:.3f}` seconds",
    f"- Exit code: `{payload['exit_code']}`",
    f"- Status: `{payload['status']}`",
    "",
    "## Rebuild Output",
]
for line in output_lines:
    markdown.append(f"- {line}")
report_md.write_text("\n".join(markdown) + "\n", encoding="utf-8")
PY
}

main() {
  local bundle_dir
  local bundle_id
  local run_id
  local run_dir
  local report_dir
  local report_json
  local report_md
  local started_at
  local completed_at
  local start_ns
  local end_ns
  local duration_seconds
  local rebuild_output
  local rebuild_status=0

  bundle_dir="$(load_bundle)"
  bundle_id="$(manifest_value "$bundle_dir/manifest.json" bundle_id)"
  if [[ -z "$bundle_id" ]]; then
    bundle_id="$(basename "$bundle_dir")"
  fi

  started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  start_ns="$(date +%s%N)"
  run_id="LAWIM-DRF-TEST-$(date -u +%Y%m%d-%H%M%S)"
  run_dir="$RECOVERY_RUN_DIR/$run_id"
  report_dir="$RECOVERY_REPORT_DIR"
  report_json="$report_dir/latest-report.json"
  report_md="$report_dir/latest-report.md"

  mkdir -p "$run_dir" "$report_dir" "$RECOVERY_WORK_DIR"

  log "starting isolated recovery test for bundle $bundle_id"
  if rebuild_output="$(
    DRY_RUN=1 \
    LAWIM_ROOT="$run_dir/current" \
    LAWIM_RELEASES_ROOT="$run_dir/releases" \
    LAWIM_MEDIA_STORAGE_PATH="$run_dir/media" \
    LAWIM_RECOVERY_BUNDLE="$bundle_dir" \
    LAWIM_RECOVERY_BUNDLE_ROOT="$RECOVERY_BUNDLE_ROOT" \
    LAWIM_GIT_REMOTE="" \
    LAWIM_DATABASE_URL="" \
    DATABASE_URL="" \
    "$REBUILD_SCRIPT" --dry-run 2>&1
  )"; then
    rebuild_status=0
  else
    rebuild_status=$?
  fi

  completed_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  end_ns="$(date +%s%N)"
  duration_seconds="$(python3 - "$start_ns" "$end_ns" <<'PY'
import sys

start = int(sys.argv[1])
end = int(sys.argv[2])
elapsed = max(0, end - start) / 1_000_000_000
print(f"{elapsed:.3f}")
PY
)"

  write_report "$report_json" "$report_md" "$bundle_dir" "$bundle_id" "$run_id" "$started_at" "$completed_at" "$duration_seconds" "$rebuild_status" "$rebuild_output"

  log "isolated recovery report written to $report_json"
  log "isolated recovery markdown written to $report_md"

  if [[ "$rebuild_status" -ne 0 ]]; then
    printf '%s\n' "$rebuild_output" >&2
    die "isolated recovery test failed"
  fi

  log "isolated recovery test completed successfully in ${duration_seconds}s"
}

main "$@"
