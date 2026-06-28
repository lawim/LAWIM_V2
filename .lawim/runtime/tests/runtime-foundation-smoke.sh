#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../../.." && pwd)

required_paths="
.lawim/runtime/README.md
.lawim/runtime/bin/lawim
.lawim/runtime/src/core/README.md
.lawim/runtime/src/core/runtime-contract.md
.lawim/runtime/src/core/dispatch-model.md
.lawim/runtime/src/commands/README.md
.lawim/runtime/src/services/README.md
.lawim/runtime/src/policies/README.md
.lawim/runtime/src/commands/status.md
.lawim/runtime/src/commands/doctor.md
.lawim/runtime/src/commands/run.md
.lawim/runtime/src/commands/batch-run.md
.lawim/runtime/src/commands/review.md
.lawim/runtime/src/commands/close-sprint.md
.lawim/runtime/src/commands/git-sync.md
.lawim/runtime/src/services/workflow-service.md
.lawim/runtime/src/services/policy-service.md
.lawim/runtime/src/services/execution-service.md
.lawim/runtime/src/services/review-service.md
.lawim/runtime/src/services/git-service.md
.lawim/runtime/src/services/pcc-service.md
.lawim/runtime/src/services/planning-service.md
.lawim/runtime/src/services/report-service.md
.lawim/runtime/docs/RUNTIME-ARCHITECTURE.md
.lawim/runtime/docs/COMMANDS.md
.lawim/runtime/docs/SERVICES.md
.lawim/runtime/docs/POLICIES.md
.lawim/runtime/docs/ROADMAP.md
reports/runtime/LOT-AIOS-001-RUNTIME-FOUNDATION-REPORT.md
"

missing=0
for path in $required_paths; do
  if [ ! -e "$REPO_ROOT/$path" ]; then
    printf '%s\n' "missing: $path" >&2
    missing=1
  fi
done

if [ "$missing" -ne 0 ]; then
  exit 1
fi

printf '%s\n' "runtime foundation smoke: PASS"
