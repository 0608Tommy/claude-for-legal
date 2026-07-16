#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Prove abrupt publication failure preserves and recovers the prior fleet.
set -euo pipefail

export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M365_ROOT="$ROOT/m365-cowork-ja"
DIST="$M365_ROOT/dist"
CACHE="$M365_ROOT/.cache"
DIST_BACKUP="$CACHE/dist-publication-backup"
LOCK_FILE="$CACHE/package-build.lock"
BUILD_SCRIPT="$ROOT/scripts/build-m365-cowork-packages.sh"
SCRATCH="$CACHE/publication-test.${BASHPID:-$$}"
EXPECTED_PACKAGE_COUNT=12
launcher_pid=""
worker_pid=""

cleanup() {
  trap - EXIT HUP INT TERM
  if [[ -n "$worker_pid" ]] && kill -0 "$worker_pid" 2>/dev/null; then
    kill -KILL "$worker_pid" 2>/dev/null || true
  fi
  if [[ -n "$launcher_pid" ]] && kill -0 "$launcher_pid" 2>/dev/null; then
    kill -KILL "$launcher_pid" 2>/dev/null || true
  fi
  if [[ -n "$launcher_pid" ]]; then
    wait "$launcher_pid" 2>/dev/null || true
  fi
  rm -rf "$SCRATCH"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

mkdir -p "$SCRATCH/tmp"
export TMPDIR="$SCRATCH/tmp"

fleet_hash_map() {
  local output="$1"
  local package_dir
  local slug
  local package_zip
  local digest_line
  local count=0

  : >"$output"
  for package_dir in "$DIST"/*; do
    [[ -d "$package_dir" ]] || continue
    slug="$(basename "$package_dir")"
    package_zip="$package_dir/$slug-ja.zip"
    [[ -f "$package_zip" && ! -L "$package_zip" ]] || {
      echo "$slug: published ZIP is missing or not regular" >&2
      exit 1
    }
    digest_line="$(sha256sum "$package_zip")"
    printf '%s\t%s\n' "$slug" "${digest_line%% *}" >>"$output"
    ((count += 1))
  done
  ((count == EXPECTED_PACKAGE_COUNT)) || {
    echo "expected $EXPECTED_PACKAGE_COUNT published ZIPs, found $count" >&2
    exit 1
  }
}

assert_lock_available() {
  local lock_fd

  exec {lock_fd}>"$LOCK_FILE"
  flock --exclusive --nonblock "$lock_fd" || {
    exec {lock_fd}>&-
    echo "package build flock was not released" >&2
    exit 1
  }
  flock --unlock "$lock_fd"
  exec {lock_fd}>&-
}

assert_no_abandoned_builds() {
  local abandoned

  for abandoned in \
    "$CACHE"/package-build-first.* \
    "$CACHE"/package-build-second.* \
    "$CACHE"/package-build-paused.* \
    "$CACHE"/dist-publication-failed.*; do
    [[ ! -e "$abandoned" && ! -L "$abandoned" ]] || {
      echo "abandoned build path remains: $abandoned" >&2
      exit 1
    }
  done
}

[[ -d "$DIST" && ! -L "$DIST" ]] || {
  echo "publication regression requires an existing dist directory" >&2
  exit 1
}
[[ ! -e "$DIST_BACKUP" && ! -L "$DIST_BACKUP" ]] || {
  echo "unexpected stale publication backup: $DIST_BACKUP" >&2
  exit 1
}
assert_no_abandoned_builds
assert_lock_available

BEFORE="$SCRATCH/before.tsv"
AFTER="$SCRATCH/after.tsv"
KILL_LOG="$SCRATCH/abrupt-kill.log"
RECOVERY_LOG="$SCRATCH/recovery.log"
fleet_hash_map "$BEFORE"

M365_COWORK_BUILD_PAUSE_AT=after-dist-backup \
  bash "$BUILD_SCRIPT" >"$KILL_LOG" 2>&1 &
launcher_pid=$!

pause_marker=""
for _ in $(seq 1 900); do
  for candidate in "$CACHE"/package-build-paused.*; do
    if [[ -f "$candidate" ]]; then
      pause_marker="$candidate"
      break 2
    fi
  done
  if ! kill -0 "$launcher_pid" 2>/dev/null; then
    wait "$launcher_pid" || true
    launcher_pid=""
    cat "$KILL_LOG" >&2
    echo "build exited before reaching the publication pause" >&2
    exit 1
  fi
  sleep 1
done

[[ -n "$pause_marker" ]] || {
  cat "$KILL_LOG" >&2
  echo "timed out waiting for the publication pause" >&2
  exit 1
}
read -r worker_pid <"$pause_marker"
[[ "$worker_pid" =~ ^[0-9]+$ ]] || {
  echo "invalid paused worker PID: $worker_pid" >&2
  exit 1
}
[[ ! -e "$DIST" && ! -L "$DIST" ]] || {
  echo "dist still exists at the injected post-backup pause" >&2
  exit 1
}
[[ -d "$DIST_BACKUP" && ! -L "$DIST_BACKUP" ]] || {
  echo "publication backup is missing at the injected pause" >&2
  exit 1
}

kill -KILL "$worker_pid"
worker_pid=""
set +e
wait "$launcher_pid"
status=$?
set -e
launcher_pid=""
((status != 0)) || {
  echo "abruptly killed build unexpectedly succeeded" >&2
  exit 1
}

assert_lock_available

set +e
M365_COWORK_BUILD_FAIL_AT=after-recovery \
  bash "$BUILD_SCRIPT" >"$RECOVERY_LOG" 2>&1
status=$?
set -e
if ((status != 86)); then
  cat "$RECOVERY_LOG" >&2
  echo "expected post-recovery status 86, got $status" >&2
  exit 1
fi
grep -F "restoring interrupted Cowork publication" \
  "$RECOVERY_LOG" >/dev/null || {
  cat "$RECOVERY_LOG" >&2
  echo "interrupted publication was not restored" >&2
  exit 1
}
grep -F "injected Cowork build failure at after-recovery" \
  "$RECOVERY_LOG" >/dev/null || {
  cat "$RECOVERY_LOG" >&2
  echo "post-recovery failure marker is missing" >&2
  exit 1
}

fleet_hash_map "$AFTER"
cmp -s "$BEFORE" "$AFTER" || {
  echo "abrupt build failure changed the previously published fleet" >&2
  diff -u "$BEFORE" "$AFTER" >&2 || true
  exit 1
}
[[ ! -e "$DIST_BACKUP" && ! -L "$DIST_BACKUP" ]] || {
  echo "publication backup remains after recovery" >&2
  exit 1
}
assert_no_abandoned_builds
assert_lock_available

printf 'Cowork abrupt publication recovery: OK (%d preserved ZIPs)\n' \
  "$EXPECTED_PACKAGE_COUNT"
