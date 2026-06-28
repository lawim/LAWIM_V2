#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BIN="$SCRIPT_DIR/../bin/lawim"

assert_contains() {
  haystack=$1
  needle=$2
  case "$haystack" in
    *"$needle"*) ;;
    *)
      printf '%s\n' "missing expected text: $needle" >&2
      exit 1
      ;;
  esac
}

help_output=$("$BIN" --help)
status_output=$("$BIN" status)
doctor_output=$("$BIN" doctor)

assert_contains "$help_output" "LAWIM runtime minimal executable"
assert_contains "$help_output" "lawim status"
assert_contains "$help_output" "lawim doctor"

assert_contains "$status_output" "Branche Git:"
assert_contains "$status_output" "Depot:"
assert_contains "$status_output" "Dernier commit:"
assert_contains "$status_output" "Dernier tag:"
assert_contains "$status_output" "Sprint actif:"
assert_contains "$status_output" "Etat programme:"
assert_contains "$status_output" "Remote Git:"

assert_contains "$doctor_output" "LAWIM doctor"
assert_contains "$doctor_output" "[OK] .lawim: present"
assert_contains "$doctor_output" "[OK] PCC: present"
assert_contains "$doctor_output" "[OK] Sprints: present"
assert_contains "$doctor_output" "[OK] Tickets: present"
assert_contains "$doctor_output" "[OK] Reports: present"
assert_contains "$doctor_output" "[OK] Git: present"
assert_contains "$doctor_output" "[OK] Git repo: present"
assert_contains "$doctor_output" "Etat depot:"
assert_contains "$doctor_output" "Remote Git:"
assert_contains "$doctor_output" "Tags recents:"

printf '%s\n' "runtime minimal smoke: PASS"
