#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Prove package-local Cowork mirrors are validated and atomically replaced.
set -euo pipefail

export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M365_ROOT="$ROOT/m365-cowork-ja"
TARGET="$M365_ROOT/cowork-packages"
DIST="$M365_ROOT/dist"
CACHE="$M365_ROOT/.cache"
LOCK_FILE="$CACHE/package-build.lock"
BUILD_SCRIPT="$ROOT/scripts/build-m365-cowork-packages.sh"
NORMALIZER="$ROOT/scripts/normalize_m365_cowork_package.py"
SCRATCH="$CACHE/mirror-test.${BASHPID:-$$}"
EXPECTED_PACKAGE_COUNT=12
EXPECTED_SLUGS=(
  ai-governance-legal
  commercial-legal
  corporate-legal
  employment-legal
  ip-legal
  law-student
  legal-builder-hub
  legal-clinic
  litigation-legal
  privacy-legal
  product-legal
  regulatory-legal
)
launcher_pid=""
worker_pid=""
reader_pid=""

path_exists() {
  [[ -e "$1" || -L "$1" ]]
}

cleanup() {
  local slug

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
  for slug in "${EXPECTED_SLUGS[@]}"; do
    rm -f \
      "$TARGET/$slug/build/.m365-cowork-mirror-test-sentinel."*.zip \
      2>/dev/null || true
  done
  rm -rf "$SCRATCH"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

mkdir -p "$SCRATCH/tmp"
export TMPDIR="$SCRATCH/tmp"

array_text() {
  printf '%s\n' "$@"
}

require_exact_slugs() {
  local label="$1"
  shift
  local actual=("$@")
  local expected_text
  local actual_text

  expected_text="$(array_text "${EXPECTED_SLUGS[@]}")"
  actual_text="$(array_text "${actual[@]}")"
  if ((${#actual[@]} != EXPECTED_PACKAGE_COUNT)) ||
    [[ "$actual_text" != "$expected_text" ]]; then
    echo "$label must equal the exact $EXPECTED_PACKAGE_COUNT-package set" >&2
    diff -u \
      <(printf '%s\n' "$expected_text") \
      <(printf '%s\n' "$actual_text") >&2 || true
    exit 1
  fi
}

require_exact_hash_map() {
  local label="$1"
  local hash_map="$2"
  local slug
  local digest
  local extra
  local actual=()

  while IFS=$'\t' read -r slug digest extra; do
    [[ -n "$slug" && "$digest" =~ ^[0-9a-f]{64}$ && -z "$extra" ]] || {
      echo "$label contains an invalid hash-map row" >&2
      exit 1
    }
    actual+=("$slug")
  done <"$hash_map"
  require_exact_slugs "$label" "${actual[@]}"
}

dist_hash_map() {
  local output="$1"
  local slug
  local package_zip
  local digest_line
  local actual=()

  mapfile -t actual < <(
    find "$DIST" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort
  )
  require_exact_slugs "canonical dist directories" "${actual[@]}"
  : >"$output"
  for slug in "${EXPECTED_SLUGS[@]}"; do
    package_zip="$DIST/$slug/$slug-ja.zip"
    [[ -f "$package_zip" && ! -L "$package_zip" ]] || {
      echo "$slug: canonical dist ZIP is missing or not regular" >&2
      exit 1
    }
    digest_line="$(sha256sum "$package_zip")"
    printf '%s\t%s\n' "$slug" "${digest_line%% *}" >>"$output"
  done
  require_exact_hash_map "canonical dist hash map" "$output"
}

mirror_hash_map() {
  local output="$1"
  local slug
  local mirror
  local digest_line

  : >"$output"
  for slug in "${EXPECTED_SLUGS[@]}"; do
    mirror="$TARGET/$slug/build/$slug-ja.zip"
    [[ -f "$mirror" && ! -L "$mirror" ]] || {
      echo "$slug: package-local mirror is missing or not regular" >&2
      exit 1
    }
    digest_line="$(sha256sum "$mirror")"
    printf '%s\t%s\n' "$slug" "${digest_line%% *}" >>"$output"
  done
  require_exact_hash_map "package-local mirror hash map" "$output"
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
  local slug

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
  for slug in "${EXPECTED_SLUGS[@]}"; do
    for abandoned in \
      "$TARGET/$slug/build"/.m365-cowork-mirror-candidate.*.zip; do
      [[ ! -e "$abandoned" && ! -L "$abandoned" ]] || {
        echo "abandoned mirror candidate remains: $abandoned" >&2
        exit 1
      }
    done
  done
}

prepare_sentinel_mirrors() {
  local slug
  local mirror_dir
  local mirror
  local sentinel
  local temporary

  mkdir "$SCRATCH/sentinels"
  for slug in "${EXPECTED_SLUGS[@]}"; do
    mirror_dir="$TARGET/$slug/build"
    if path_exists "$mirror_dir"; then
      [[ -d "$mirror_dir" && ! -L "$mirror_dir" ]] || {
        echo "$slug: mirror build path must be a regular directory" >&2
        exit 1
      }
    else
      mkdir -- "$mirror_dir"
    fi
    mirror="$mirror_dir/$slug-ja.zip"
    if path_exists "$mirror"; then
      [[ -f "$mirror" && ! -L "$mirror" ]] || {
        echo "$slug: existing mirror must be a regular file" >&2
        exit 1
      }
    fi
    sentinel="$SCRATCH/sentinels/$slug-ja.zip"
    temporary="$mirror_dir/.m365-cowork-mirror-test-sentinel.$$.$slug.zip"
    printf 'stale Cowork mirror sentinel: %s\n' "$slug" >"$sentinel"
    cp -p -- "$sentinel" "$temporary"
    mv --no-copy -T "$temporary" "$mirror"
  done
}

assert_sentinel_mirrors() {
  local slug
  local mirror
  local sentinel

  for slug in "${EXPECTED_SLUGS[@]}"; do
    mirror="$TARGET/$slug/build/$slug-ja.zip"
    sentinel="$SCRATCH/sentinels/$slug-ja.zip"
    [[ -f "$mirror" && ! -L "$mirror" ]] || {
      echo "$slug: sentinel mirror is missing or not regular" >&2
      exit 1
    }
    cmp -s "$sentinel" "$mirror" || {
      echo "$slug: mirror changed before an atomic rename" >&2
      exit 1
    }
  done
}

assert_partial_mirrors() {
  local first="${EXPECTED_SLUGS[0]}"
  local slug
  local mirror

  mirror="$TARGET/$first/build/$first-ja.zip"
  cmp -s "$DIST/$first/$first-ja.zip" "$mirror" || {
    echo "$first: first atomic mirror rename was not published" >&2
    exit 1
  }
  for slug in "${EXPECTED_SLUGS[@]:1}"; do
    mirror="$TARGET/$slug/build/$slug-ja.zip"
    cmp -s "$SCRATCH/sentinels/$slug-ja.zip" "$mirror" || {
      echo "$slug: mirror changed before its atomic rename" >&2
      exit 1
    }
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
      cat "$PARTIAL_LOG" >&2
      echo "build exited before pause $expected_point" >&2
      exit 1
    fi
    sleep 1
  done
  cat "$PARTIAL_LOG" >&2
  echo "timed out waiting for pause $expected_point" >&2
  exit 1
}

start_atomic_reader() {
  python3 - \
    "$DIST" \
    "$TARGET" \
    "$MIRROR_READER_STOP" \
    "$MIRROR_READER_FAILURE" <<'PY' &
from __future__ import annotations

import sys
import time
from pathlib import Path

dist = Path(sys.argv[1])
target = Path(sys.argv[2])
stop = Path(sys.argv[3])
failure = Path(sys.argv[4])
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
old = {
    slug: (target / slug / "build" / f"{slug}-ja.zip").read_bytes()
    for slug in slugs
}
canonical = {
    slug: (dist / slug / f"{slug}-ja.zip").read_bytes() for slug in slugs
}


def verify_mirrors() -> None:
    """Require every mirror read to be one complete old-or-new file."""
    for slug in slugs:
        path = target / slug / "build" / f"{slug}-ja.zip"
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"missing regular mirror: {path}")
        data = path.read_bytes()
        if data not in (old[slug], canonical[slug]):
            raise RuntimeError(f"partial or unexpected mirror bytes: {path}")


try:
    while not stop.exists():
        verify_mirrors()
        time.sleep(0.005)
except (OSError, RuntimeError) as error:
    failure.write_text(f"{type(error).__name__}: {error}\n", encoding="utf-8")
    raise
PY
  reader_pid=$!
}

stop_atomic_reader() {
  local reader_status

  : >"$MIRROR_READER_STOP"
  set +e
  wait "$reader_pid"
  reader_status=$?
  set -e
  reader_pid=""
  if ((reader_status != 0)) || [[ -s "$MIRROR_READER_FAILURE" ]]; then
    cat "$MIRROR_READER_FAILURE" >&2
    echo "concurrent mirror reader observed partial bytes" >&2
    exit 1
  fi
}

assert_final_mirrors() {
  local dist_hashes="$SCRATCH/final-dist-hashes.tsv"
  local mirror_hashes="$SCRATCH/final-mirror-hashes.tsv"
  local contract_root="$SCRATCH/final-contract"
  local slug
  local canonical
  local mirror
  local contract_copy
  local digest_line
  local digest
  local result

  dist_hash_map "$dist_hashes"
  mirror_hash_map "$mirror_hashes"
  if ! cmp -s "$dist_hashes" "$mirror_hashes"; then
    echo "canonical dist and mirror hash maps differ" >&2
    diff -u "$dist_hashes" "$mirror_hashes" >&2 || true
    exit 1
  fi

  mkdir "$contract_root"
  for slug in "${EXPECTED_SLUGS[@]}"; do
    canonical="$DIST/$slug/$slug-ja.zip"
    mirror="$TARGET/$slug/build/$slug-ja.zip"
    contract_copy="$contract_root/$slug-ja.zip"
    cmp -s "$canonical" "$mirror" || {
      echo "$slug: final mirror bytes differ from canonical dist" >&2
      exit 1
    }
    [[ "$(stat -c '%s' "$canonical")" == "$(stat -c '%s' "$mirror")" ]] || {
      echo "$slug: final mirror size differs from canonical dist" >&2
      exit 1
    }
    digest_line="$(sha256sum "$canonical")"
    digest="${digest_line%% *}"
    result="$(
      python3 "$NORMALIZER" \
        "$mirror" \
        "$contract_copy" \
        "$TARGET/$slug"
    )"
    [[ "$result" == "$slug"$'\t'"$digest" ]] || {
      echo "$slug: final mirror failed normalized contract: $result" >&2
      exit 1
    }
    cmp -s "$mirror" "$contract_copy" || {
      echo "$slug: final mirror is not byte-canonical after normalization" >&2
      exit 1
    }
  done

  python3 - "$TARGET" <<'PY'
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

target = Path(sys.argv[1])
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
for slug in slugs:
    path = target / slug / "build" / f"{slug}-ja.zip"
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read("manifest.json"))
        folders = [
            item["folder"].removeprefix("./") for item in manifest["agentSkills"]
        ]
        required = {
            f"{folder}/{filename}"
            for folder in folders
            for filename in ("LICENSE.txt", "NOTICE.txt")
        }
        forbidden = {
            f"{folder}/{filename}"
            for folder in folders
            for filename in ("LICENSE", "NOTICE")
        }
        missing = sorted(required - names)
        legacy = sorted(forbidden & names)
        corrupt = archive.testzip()
    if missing:
        raise AssertionError(f"{slug}: missing legal files: {missing}")
    if legacy:
        raise AssertionError(f"{slug}: legacy legal files remain: {legacy}")
    if corrupt is not None:
        raise AssertionError(f"{slug}: corrupt ZIP member: {corrupt}")
PY
}

for tool in cmp diff find flock mv sha256sum sort stat; do
  command -v "$tool" >/dev/null || {
    echo "requires $tool" >&2
    exit 2
  }
done
[[ -d "$DIST" && ! -L "$DIST" ]] || {
  echo "mirror regression requires an existing canonical dist directory" >&2
  exit 1
}
assert_lock_available

BEFORE_DIST="$SCRATCH/before-dist.tsv"
AFTER_FAILURE_DIST="$SCRATCH/after-failure-dist.tsv"
AFTER_REPAIR_DIST="$SCRATCH/after-repair-dist.tsv"
FAILURE_LOG="$SCRATCH/before-rename-failure.log"
PARTIAL_LOG="$SCRATCH/partial-update.log"
REPAIR_LOG="$SCRATCH/repair.log"
MIRROR_READER_STOP="$SCRATCH/mirror-reader.stop"
MIRROR_READER_FAILURE="$SCRATCH/mirror-reader.failure"
dist_hash_map "$BEFORE_DIST"
prepare_sentinel_mirrors

set +e
M365_COWORK_BUILD_FAIL_AT=before-mirror-renames \
  bash "$BUILD_SCRIPT" >"$FAILURE_LOG" 2>&1
status=$?
set -e
if ((status != 86)); then
  cat "$FAILURE_LOG" >&2
  echo "expected pre-mirror-rename status 86, got $status" >&2
  exit 1
fi
grep -F "injected Cowork build failure at before-mirror-renames" \
  "$FAILURE_LOG" >/dev/null || {
  cat "$FAILURE_LOG" >&2
  echo "pre-mirror-rename failure marker is missing" >&2
  exit 1
}
assert_sentinel_mirrors
assert_no_abandoned_builds
assert_lock_available
dist_hash_map "$AFTER_FAILURE_DIST"
cmp -s "$BEFORE_DIST" "$AFTER_FAILURE_DIST" || {
  echo "deterministic dist changed during mirror failure test" >&2
  diff -u "$BEFORE_DIST" "$AFTER_FAILURE_DIST" >&2 || true
  exit 1
}

start_atomic_reader
first_slug="${EXPECTED_SLUGS[0]}"
pause_point="after-mirror-rename-$first_slug"
M365_COWORK_BUILD_PAUSE_AT="$pause_point" \
  bash "$BUILD_SCRIPT" >"$PARTIAL_LOG" 2>&1 &
launcher_pid=$!
wait_for_pause "$pause_point"
[[ "$worker_pid" =~ ^[0-9]+$ ]] || {
  echo "invalid paused worker PID: $worker_pid" >&2
  exit 1
}
assert_partial_mirrors
killed_worker_pid="$worker_pid"
kill -KILL "$worker_pid"
worker_pid=""
set +e
wait "$launcher_pid"
status=$?
set -e
launcher_pid=""
((status != 0)) || {
  echo "abruptly killed mirror build unexpectedly succeeded" >&2
  exit 1
}
stop_atomic_reader
assert_partial_mirrors
assert_lock_available

for slug in "${EXPECTED_SLUGS[@]:1}"; do
  candidate="$TARGET/$slug/build/"
  candidate+=".m365-cowork-mirror-candidate.$killed_worker_pid.zip"
  [[ -f "$candidate" && ! -L "$candidate" ]] || {
    echo "$slug: interrupted mirror candidate is missing" >&2
    exit 1
  }
done

bash "$BUILD_SCRIPT" >"$REPAIR_LOG" 2>&1
assert_no_abandoned_builds
assert_lock_available
assert_final_mirrors
dist_hash_map "$AFTER_REPAIR_DIST"
cmp -s "$BEFORE_DIST" "$AFTER_REPAIR_DIST" || {
  echo "deterministic dist changed during mirror repair test" >&2
  diff -u "$BEFORE_DIST" "$AFTER_REPAIR_DIST" >&2 || true
  exit 1
}

printf 'Cowork package-local mirror publication: OK (%d exact ZIPs)\n' \
  "$EXPECTED_PACKAGE_COUNT"
