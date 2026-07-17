#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Prove atomic fleet exchange survives concurrent reads and abrupt failure.
set -euo pipefail

export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M365_ROOT="$ROOT/m365-cowork-ja"
DIST="$M365_ROOT/dist"
TARGET="$M365_ROOT/cowork-packages"
CACHE="$M365_ROOT/.cache"
LEGACY_BACKUP="$CACHE/dist-publication-backup"
LOCK_FILE="$CACHE/package-build.lock"
BUILD_SCRIPT="$ROOT/scripts/build-m365-cowork-packages.sh"
SCRATCH="$CACHE/publication-test.${BASHPID:-$$}"
EXPECTED_PACKAGE_COUNT=12
launcher_pid=""
worker_pid=""
reader_pid=""

cleanup() {
  trap - EXIT HUP INT TERM
  if [[ -n "$worker_pid" ]] && kill -0 "$worker_pid" 2>/dev/null; then
    kill -KILL "$worker_pid" 2>/dev/null || true
  fi
  if [[ -n "$launcher_pid" ]] && kill -0 "$launcher_pid" 2>/dev/null; then
    kill -KILL "$launcher_pid" 2>/dev/null || true
  fi
  if [[ -n "$reader_pid" ]] && kill -0 "$reader_pid" 2>/dev/null; then
    kill -KILL "$reader_pid" 2>/dev/null || true
  fi
  if [[ -n "$launcher_pid" ]]; then
    wait "$launcher_pid" 2>/dev/null || true
  fi
  if [[ -n "$reader_pid" ]]; then
    wait "$reader_pid" 2>/dev/null || true
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
  local package_dir

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
  for package_dir in "$TARGET"/*; do
    [[ -d "$package_dir" && ! -L "$package_dir" ]] || continue
    for abandoned in \
      "$package_dir/build"/.m365-cowork-mirror-candidate.*.zip; do
      [[ ! -e "$abandoned" && ! -L "$abandoned" ]] || {
        echo "abandoned mirror candidate remains: $abandoned" >&2
        exit 1
      }
    done
  done
}

wait_for_pause() {
  local expected_point="$1"
  local pause_marker
  local paused_pid
  local paused_point

  for _ in $(seq 1 900); do
    for pause_marker in "$CACHE"/package-build-paused.*; do
      if [[ -f "$pause_marker" ]]; then
        IFS=$'\t' read -r paused_pid paused_point <"$pause_marker"
        if [[ "$paused_point" == "$expected_point" ]]; then
          worker_pid="$paused_pid"
          return 0
        fi
      fi
    done
    if ! kill -0 "$launcher_pid" 2>/dev/null; then
      wait "$launcher_pid" || true
      launcher_pid=""
      cat "$KILL_LOG" >&2
      echo "build exited before pause $expected_point" >&2
      exit 1
    fi
    sleep 1
  done
  cat "$KILL_LOG" >&2
  echo "timed out waiting for pause $expected_point" >&2
  exit 1
}

stop_reader() {
  : >"$READER_STOP"
  set +e
  wait "$reader_pid"
  reader_status=$?
  set -e
  reader_pid=""
  if ((reader_status != 0)) || [[ -s "$READER_FAILURE" ]]; then
    cat "$READER_FAILURE" >&2
    echo "concurrent dist reader observed an incomplete fleet" >&2
    exit 1
  fi
}

[[ -d "$DIST" && ! -L "$DIST" ]] || {
  echo "publication regression requires an existing dist directory" >&2
  exit 1
}
[[ ! -e "$LEGACY_BACKUP" && ! -L "$LEGACY_BACKUP" ]] || {
  echo "unexpected legacy publication backup: $LEGACY_BACKUP" >&2
  exit 1
}
assert_no_abandoned_builds
assert_lock_available

BEFORE="$SCRATCH/before.tsv"
BEFORE_EXCHANGE="$SCRATCH/before-exchange.tsv"
AFTER_EXCHANGE="$SCRATCH/after-exchange.tsv"
AFTER_RECOVERY="$SCRATCH/after-recovery.tsv"
KILL_LOG="$SCRATCH/abrupt-kill.log"
RECOVERY_LOG="$SCRATCH/recovery.log"
READER_STOP="$SCRATCH/reader.stop"
READER_FAILURE="$SCRATCH/reader.failure"
fleet_hash_map "$BEFORE"

python3 - "$DIST" "$READER_STOP" "$READER_FAILURE" <<'PY' &
from __future__ import annotations

import json
import sys
import time
import zipfile
from pathlib import Path

dist = Path(sys.argv[1])
stop = Path(sys.argv[2])
failure = Path(sys.argv[3])
slugs = (
    "ai-governance-legal",
    "commercial-legal",
    "corporate-legal",
    "employment-legal",
    "ip-legal",
    "law-student",
    "legal-builder-hub",
    "legal-clinic",
    "litigation-legal",
    "privacy-legal",
    "product-legal",
    "regulatory-legal",
)


def verify_fleet() -> None:
    """Require one complete old-or-new fleet at the consumer path."""
    actual = tuple(sorted(path.name for path in dist.iterdir()))
    if actual != slugs:
        raise RuntimeError(f"fleet directories differ: {actual!r}")
    for slug in slugs:
        archive_path = dist / slug / f"{slug}-ja.zip"
        if not archive_path.is_file() or archive_path.is_symlink():
            raise RuntimeError(f"missing regular ZIP: {archive_path}")
        with zipfile.ZipFile(archive_path) as archive:
            manifest = json.loads(archive.read("manifest.json"))
            if not isinstance(manifest, dict):
                raise RuntimeError(f"invalid manifest: {archive_path}")


try:
    while not stop.exists():
        verify_fleet()
        time.sleep(0.005)
except (
    KeyError,
    OSError,
    RuntimeError,
    ValueError,
    zipfile.BadZipFile,
) as error:
    failure.write_text(f"{type(error).__name__}: {error}\n", encoding="utf-8")
    raise
PY
reader_pid=$!

M365_COWORK_BUILD_PAUSE_AT=before-dist-exchange,after-dist-exchange \
  bash "$BUILD_SCRIPT" >"$KILL_LOG" 2>&1 &
launcher_pid=$!

wait_for_pause "before-dist-exchange"
[[ "$worker_pid" =~ ^[0-9]+$ ]] || {
  echo "invalid paused worker PID: $worker_pid" >&2
  exit 1
}
fleet_hash_map "$BEFORE_EXCHANGE"
cmp -s "$BEFORE" "$BEFORE_EXCHANGE" || {
  echo "fleet changed before the atomic exchange" >&2
  diff -u "$BEFORE" "$BEFORE_EXCHANGE" >&2 || true
  exit 1
}
kill -CONT "$worker_pid"

wait_for_pause "after-dist-exchange"
[[ "$worker_pid" =~ ^[0-9]+$ ]] || {
  echo "invalid post-exchange worker PID: $worker_pid" >&2
  exit 1
}
fleet_hash_map "$AFTER_EXCHANGE"
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

stop_reader
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
grep -F "injected Cowork build failure at after-recovery" \
  "$RECOVERY_LOG" >/dev/null || {
  cat "$RECOVERY_LOG" >&2
  echo "post-recovery failure marker is missing" >&2
  exit 1
}

fleet_hash_map "$AFTER_RECOVERY"
cmp -s "$AFTER_EXCHANGE" "$AFTER_RECOVERY" || {
  echo "post-SIGKILL recovery changed the exchanged fleet" >&2
  diff -u "$AFTER_EXCHANGE" "$AFTER_RECOVERY" >&2 || true
  exit 1
}
[[ ! -e "$LEGACY_BACKUP" && ! -L "$LEGACY_BACKUP" ]] || {
  echo "legacy publication backup remains after exchange" >&2
  exit 1
}
assert_no_abandoned_builds
assert_lock_available

printf 'Cowork atomic exchange/SIGKILL: OK (%d complete ZIPs)\n' \
  "$EXPECTED_PACKAGE_COUNT"
