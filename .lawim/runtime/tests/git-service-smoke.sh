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

run_expect_fail() {
  expected_text=$1
  shift
  output_file=$(mktemp)
  if "$@" >"$output_file" 2>&1; then
    cat "$output_file" >&2
    rm -f "$output_file"
    printf '%s\n' "expected failure but command succeeded: $*" >&2
    exit 1
  fi
  output=$(cat "$output_file")
  rm -f "$output_file"
  assert_contains "$output" "$expected_text"
}

TMP_ROOT=$(mktemp -d)
trap 'rm -rf "$TMP_ROOT"' EXIT INT HUP TERM

TEST_REPO="$TMP_ROOT/repo"
mkdir -p "$TEST_REPO/.lawim/runtime/bin"
cp "$BIN" "$TEST_REPO/.lawim/runtime/bin/lawim"
chmod +x "$TEST_REPO/.lawim/runtime/bin/lawim"

git -C "$TEST_REPO" init -q
git -C "$TEST_REPO" config user.name "LAWIM Runtime Test"
git -C "$TEST_REPO" config user.email "runtime-test@example.com"

printf '%s\n' "seed" > "$TEST_REPO/seed.txt"
git -C "$TEST_REPO" add -A
git -C "$TEST_REPO" commit -q -m "chore: isolated runtime test seed"

status_output=$("$TEST_REPO/.lawim/runtime/bin/lawim" git-sync --status)
assert_contains "$status_output" "LAWIM git-sync status"
assert_contains "$status_output" "Etat Git: propre"
assert_contains "$status_output" "Branche Git:"
assert_contains "$status_output" "Dernier commit:"
assert_contains "$status_output" "Dernier tag: aucun"
assert_contains "$status_output" "Derniers tags:"
assert_contains "$status_output" "Remote Git: absent"

run_expect_fail "Refus: message de commit vide." "$TEST_REPO/.lawim/runtime/bin/lawim" git-sync --commit ""
run_expect_fail "Refus: aucun changement a committer." "$TEST_REPO/.lawim/runtime/bin/lawim" git-sync --commit "isolated commit"
run_expect_fail "Refus: nom de tag vide." "$TEST_REPO/.lawim/runtime/bin/lawim" git-sync --tag ""

printf '%s\n' "change" > "$TEST_REPO/change.txt"
commit_output=$("$TEST_REPO/.lawim/runtime/bin/lawim" git-sync --commit "chore: isolated runtime commit")
assert_contains "$commit_output" "chore: isolated runtime commit"

tag_output=$("$TEST_REPO/.lawim/runtime/bin/lawim" git-sync --tag "lot-aios-003-smoke")
assert_contains "$tag_output" "Tag cree: lot-aios-003-smoke"

run_expect_fail "Refus: le tag existe deja." "$TEST_REPO/.lawim/runtime/bin/lawim" git-sync --tag "lot-aios-003-smoke"
run_expect_fail "Refus: aucun remote Git configure." "$TEST_REPO/.lawim/runtime/bin/lawim" git-sync --push

printf '%s\n' "runtime git-service smoke: PASS"
