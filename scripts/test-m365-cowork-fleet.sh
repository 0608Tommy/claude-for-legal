#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Run every local-only Microsoft 365 Cowork migration gate.
set -euo pipefail

export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M365_ROOT="$ROOT/m365-cowork-ja"
TARGET="$M365_ROOT/cowork-packages"
DIST="$M365_ROOT/dist"
SCRATCH="$M365_ROOT/.cache/fleet-test.${BASHPID:-$$}"
CLINIC_REFERENCES="$M365_ROOT/cowork-packages/legal-clinic/references"
CLINIC_VALIDATOR="$CLINIC_REFERENCES/validate_clinic_state_payloads.py"
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
SHARED_ENVELOPE_PACKAGES=(
  corporate-legal
  employment-legal
  ip-legal
  legal-builder-hub
  litigation-legal
)

for tool in cmp diff find git sha256sum sort; do
  command -v "$tool" >/dev/null || {
    echo "requires $tool" >&2
    exit 2
  }
done

export TMPDIR="$SCRATCH/tmp"

cleanup() {
  rm -rf "$SCRATCH"
}
trap cleanup EXIT HUP INT TERM

mkdir -p "$TMPDIR"

snapshot_tracked_files() {
  local output="$1"
  local path
  local digest

  : >"$output"
  while IFS= read -r -d '' path; do
    if [[ -e "$ROOT/$path" || -L "$ROOT/$path" ]]; then
      digest="$(git -C "$ROOT" hash-object -- "$path")"
    else
      digest="MISSING"
    fi
    printf '%s\t%s\n' "$digest" "$path" >>"$output"
  done < <(git -C "$ROOT" ls-files -z)
}

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
    cmp -s "$DIST/$slug/$slug-ja.zip" "$mirror" || {
      echo "$slug: package-local mirror differs from canonical dist" >&2
      exit 1
    }
    digest_line="$(sha256sum "$mirror")"
    printf '%s\t%s\n' "$slug" "${digest_line%% *}" >>"$output"
  done
  require_exact_hash_map "package-local mirror hash map" "$output"
}

TRACKED_BEFORE="$SCRATCH/tracked-before.tsv"
TRACKED_AFTER="$SCRATCH/tracked-after.tsv"
FIRST_HASHES="$SCRATCH/first-build-hashes.tsv"
SECOND_HASHES="$SCRATCH/second-build-hashes.tsv"
FIRST_MIRROR_HASHES="$SCRATCH/first-mirror-hashes.tsv"
SECOND_MIRROR_HASHES="$SCRATCH/second-mirror-hashes.tsv"
snapshot_tracked_files "$TRACKED_BEFORE"

bash "$ROOT/scripts/test-m365-cowork-inventory.sh"
bash "$ROOT/scripts/test-m365-apache-notices.sh"
bash "$ROOT/scripts/test-m365-cowork-target.sh"
bash "$ROOT/scripts/test-m365-cowork-icons.sh"
bash "$ROOT/scripts/test-m365-reference-projection.sh"
bash "$ROOT/scripts/test-m365-cowork-package-build.sh"
bash "$ROOT/scripts/test-sharepoint-state-contracts.sh"
bash "$ROOT/scripts/test-m365-connector-matrix.sh"
bash "$ROOT/scripts/test-power-platform-contracts.sh"
bash "$ROOT/scripts/test-m365-artifacts.sh"

(
  cd "$M365_ROOT/cowork-packages/regulatory-legal"
  python3 -m fixtures.validate_regulatory_fixtures
)
python3 "$CLINIC_VALIDATOR"
for package in "${SHARED_ENVELOPE_PACKAGES[@]}"; do
  envelope_validator="$M365_ROOT/cowork-packages/$package/references"
  python3 "$envelope_validator/validate_shared_envelope_examples.py"
done

bash "$ROOT/scripts/build-m365-cowork-packages.sh"
dist_hash_map "$FIRST_HASHES"
mirror_hash_map "$FIRST_MIRROR_HASHES"
cmp -s "$FIRST_HASHES" "$FIRST_MIRROR_HASHES" || {
  echo "first canonical dist and mirror hash maps differ" >&2
  diff -u "$FIRST_HASHES" "$FIRST_MIRROR_HASHES" >&2 || true
  exit 1
}
bash "$ROOT/scripts/test-m365-cowork-publication.sh"
bash "$ROOT/scripts/test-m365-cowork-package-mirrors.sh"
dist_hash_map "$SECOND_HASHES"
mirror_hash_map "$SECOND_MIRROR_HASHES"

if ! cmp -s "$FIRST_HASHES" "$SECOND_HASHES"; then
  echo "consecutive fleet builds produced different package hashes" >&2
  diff -u "$FIRST_HASHES" "$SECOND_HASHES" >&2 || true
  exit 1
fi
if ! cmp -s "$SECOND_HASHES" "$SECOND_MIRROR_HASHES"; then
  echo "final canonical dist and mirror hash maps differ" >&2
  diff -u "$SECOND_HASHES" "$SECOND_MIRROR_HASHES" >&2 || true
  exit 1
fi

python3 -c "
import glob,json
[json.load(open(path, encoding='utf-8')) for path in glob.glob(
    '$M365_ROOT/**/*.json',
    recursive=True,
)]
"

snapshot_tracked_files "$TRACKED_AFTER"
if ! cmp -s "$TRACKED_BEFORE" "$TRACKED_AFTER"; then
  echo "fleet validation changed tracked source files" >&2
  diff -u "$TRACKED_BEFORE" "$TRACKED_AFTER" >&2 || true
  exit 1
fi

git -C "$ROOT" --no-pager diff --check
printf 'Microsoft 365 Cowork fleet validation: OK\n'
