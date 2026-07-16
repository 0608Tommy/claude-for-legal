#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Run every local-only Microsoft 365 Cowork migration gate.
set -euo pipefail

export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M365_ROOT="$ROOT/m365-cowork-ja"
DIST="$M365_ROOT/dist"
SCRATCH="$M365_ROOT/.cache/fleet-test.${BASHPID:-$$}"
CLINIC_REFERENCES="$M365_ROOT/cowork-packages/legal-clinic/references"
CLINIC_VALIDATOR="$CLINIC_REFERENCES/validate_clinic_state_payloads.py"
EXPECTED_PACKAGE_COUNT=12
SHARED_ENVELOPE_PACKAGES=(
  corporate-legal
  employment-legal
  ip-legal
  legal-builder-hub
  litigation-legal
)

for tool in cmp diff git sha256sum; do
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

dist_hash_map() {
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
      echo "$slug: deterministic fleet ZIP is missing" >&2
      exit 1
    }
    digest_line="$(sha256sum "$package_zip")"
    printf '%s\t%s\n' "$slug" "${digest_line%% *}" >>"$output"
    ((count += 1))
  done
  ((count == EXPECTED_PACKAGE_COUNT)) || {
    echo "expected $EXPECTED_PACKAGE_COUNT fleet ZIPs, found $count" >&2
    exit 1
  }
}

TRACKED_BEFORE="$SCRATCH/tracked-before.tsv"
TRACKED_AFTER="$SCRATCH/tracked-after.tsv"
FIRST_HASHES="$SCRATCH/first-build-hashes.tsv"
SECOND_HASHES="$SCRATCH/second-build-hashes.tsv"
snapshot_tracked_files "$TRACKED_BEFORE"

bash "$ROOT/scripts/test-m365-cowork-inventory.sh"
bash "$ROOT/scripts/test-m365-apache-notices.sh"
bash "$ROOT/scripts/test-m365-cowork-target.sh"
bash "$ROOT/scripts/test-m365-cowork-icons.sh"
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
bash "$ROOT/scripts/test-m365-cowork-publication.sh"
bash "$ROOT/scripts/build-m365-cowork-packages.sh"
dist_hash_map "$SECOND_HASHES"

if ! cmp -s "$FIRST_HASHES" "$SECOND_HASHES"; then
  echo "consecutive fleet builds produced different package hashes" >&2
  diff -u "$FIRST_HASHES" "$SECOND_HASHES" >&2 || true
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
