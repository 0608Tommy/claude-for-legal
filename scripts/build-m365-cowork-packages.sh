#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Build reproducible, locally validated Microsoft 365 Cowork app packages.
set -euo pipefail

export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1
umask 022

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M365_ROOT="$ROOT/m365-cowork-ja"
TARGET="$M365_ROOT/cowork-packages"
DIST="$M365_ROOT/dist"
CACHE="$M365_ROOT/.cache"
CATALOG="$M365_ROOT/shared/package-catalog.json"
MIGRATION_MAP="$M365_ROOT/shared/migration-map.json"
NORMALIZER="$ROOT/scripts/normalize_m365_cowork_package.py"
ICON_VALIDATOR="$ROOT/scripts/validate_m365_cowork_icons.py"
ATK_VERSION="1.1.12"
MAX_PACKAGE_BYTES=$((10 * 1024 * 1024))
EXPECTED_PACKAGE_COUNT=12
SKILLS_REF_PYTHON="${SKILLS_REF_PYTHON:-$CACHE/skills-ref-venv/bin/python}"
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

command -v flock >/dev/null || {
  echo "requires flock" >&2
  exit 2
}
mkdir -p "$CACHE" "$CACHE/tmp"
export TMPDIR="$CACHE/tmp"

LOCK_FILE="$CACHE/package-build.lock"
if [[ "${M365_COWORK_LOCK_HELD:-}" != "1" ]]; then
  exec flock \
    --exclusive \
    --nonblock \
    --conflict-exit-code 75 \
    --close \
    "$LOCK_FILE" \
    env M365_COWORK_LOCK_HELD=1 bash "$0" "$@"
fi

RUN_ID="${BASHPID:-$$}"
FIRST_STAGE="$CACHE/package-build-first.$RUN_ID"
SECOND_STAGE="$CACHE/package-build-second.$RUN_ID"
DIST_BACKUP="$CACHE/dist-publication-backup"
FAILED_DIST="$CACHE/dist-publication-failed.$RUN_ID"
PAUSE_MARKER="$CACHE/package-build-paused.$RUN_ID"
PUBLICATION_PENDING=0

path_exists() {
  [[ -e "$1" || -L "$1" ]]
}

recover_interrupted_publication() {
  if ! path_exists "$DIST" && path_exists "$DIST_BACKUP"; then
    echo "restoring interrupted Cowork publication" >&2
    mv -T "$DIST_BACKUP" "$DIST"
  elif path_exists "$DIST" && path_exists "$DIST_BACKUP"; then
    rm -rf "$DIST_BACKUP"
  fi
}

cleanup_abandoned_builds() {
  local abandoned

  for abandoned in \
    "$CACHE"/package-build-first.* \
    "$CACHE"/package-build-second.* \
    "$CACHE"/dist-publication-failed.*; do
    [[ -d "$abandoned" ]] && rm -rf "$abandoned"
  done
  for abandoned in "$CACHE"/package-build-paused.*; do
    [[ -f "$abandoned" || -L "$abandoned" ]] && rm -f "$abandoned"
  done
  return 0
}

rollback_publication() {
  local moved_candidate=0

  ((PUBLICATION_PENDING == 1)) || return 0
  path_exists "$DIST_BACKUP" || return 0
  rm -rf "$FAILED_DIST"
  if path_exists "$DIST"; then
    mv -T "$DIST" "$FAILED_DIST"
    moved_candidate=1
  fi
  if mv -T "$DIST_BACKUP" "$DIST"; then
    rm -rf "$FAILED_DIST"
    PUBLICATION_PENDING=0
    return 0
  fi
  if ((moved_candidate == 1)); then
    mv -T "$FAILED_DIST" "$DIST" || true
  fi
  return 1
}

cleanup() {
  local status=$?

  trap - EXIT HUP INT TERM
  rollback_publication || status=1
  rm -rf "$FIRST_STAGE" "$SECOND_STAGE"
  rm -f "$PAUSE_MARKER"
  exit "$status"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

recover_interrupted_publication
cleanup_abandoned_builds

inject_failure() {
  local point="$1"

  if [[ "${M365_COWORK_BUILD_FAIL_AT:-}" == "$point" ]]; then
    echo "injected Cowork build failure at $point" >&2
    exit 86
  fi
}

pause_at() {
  local point="$1"

  if [[ "${M365_COWORK_BUILD_PAUSE_AT:-}" == "$point" ]]; then
    printf '%s\n' "$BASHPID" >"$PAUSE_MARKER"
    kill -STOP "$BASHPID"
    rm -f "$PAUSE_MARKER"
  fi
}

inject_failure "after-recovery"
mkdir "$FIRST_STAGE" "$SECOND_STAGE"

for tool in atk cmp cp diff find git jq mv sha256sum stat; do
  command -v "$tool" >/dev/null || {
    echo "requires $tool" >&2
    exit 2
  }
done
[[ -x "$SKILLS_REF_PYTHON" ]] || {
  echo "requires skills-ref 0.1.1 at $SKILLS_REF_PYTHON" >&2
  exit 2
}

actual_atk_version="$(atk --version)"
[[ "$actual_atk_version" == "$ATK_VERSION" ]] || {
  echo "requires atk $ATK_VERSION; found $actual_atk_version" >&2
  exit 2
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

mapfile -t eligible_slugs < <(
  jq -er '
    .packages
    | to_entries
    | map(select(.value.status == "draft-legal-review") | .key)
    | sort[]
  ' "$CATALOG"
)
mapfile -t source_slugs < <(
  find "$TARGET" \
    -mindepth 2 \
    -maxdepth 2 \
    -type f \
    -name manifest.json \
    -printf '%h\n' |
    while IFS= read -r package_dir; do basename "$package_dir"; done |
    sort
)

require_exact_slugs "catalog draft-legal-review packages" \
  "${eligible_slugs[@]}"
require_exact_slugs "source manifest package directories" \
  "${source_slugs[@]}"

blocked_status="$(
  jq -er '.packages["cocounsel-legal"].status' "$CATALOG"
)"
[[ "$blocked_status" == "blocked-vendor-approval" ]] || {
  echo "cocounsel-legal must remain blocked-vendor-approval" >&2
  exit 1
}
[[ ! -e "$TARGET/cocounsel-legal/manifest.json" ]] || {
  echo "blocked cocounsel-legal must not have a source package manifest" >&2
  exit 1
}

snapshot_sources() {
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
  done < <(
    git -C "$ROOT" ls-files -z -- \
      "m365-cowork-ja/cowork-packages"
  )
}

SOURCE_BEFORE="$FIRST_STAGE/source-before.tsv"
SOURCE_AFTER="$FIRST_STAGE/source-after.tsv"
snapshot_sources "$SOURCE_BEFORE"

# These validators are read-only. In particular, package builds never apply
# Apache notices to tracked source files.
python3 "$ROOT/scripts/validate_m365_cowork_target.py"
python3 "$ICON_VALIDATOR"

preflight_package() {
  local slug="$1"
  local package="$TARGET/$slug"
  local expected_app_id
  local actual_app_id
  local expected_manifest_version
  local actual_manifest_version
  local actual_language
  local skill_diff
  local source_skill_diff
  local unsafe_entry
  local folder

  for required in manifest.json m365agents.yml color.png outline.png \
    LICENSE NOTICE; do
    [[ -f "$package/$required" && ! -L "$package/$required" ]] || {
      echo "$slug: missing regular source file $required" >&2
      exit 1
    }
  done

  expected_app_id="$(
    jq -er --arg slug "$slug" '.packages[$slug].appId' "$CATALOG"
  )"
  actual_app_id="$(jq -er '.id' "$package/manifest.json")"
  [[ "$actual_app_id" == "$expected_app_id" ]] || {
    echo "$slug: manifest app ID does not match package catalog" >&2
    exit 1
  }

  expected_manifest_version="$(jq -er '.manifestVersion' "$CATALOG")"
  actual_manifest_version="$(
    jq -er '.manifestVersion' "$package/manifest.json"
  )"
  [[ "$actual_manifest_version" == "$expected_manifest_version" ]] || {
    echo "$slug: manifestVersion must be $expected_manifest_version" >&2
    exit 1
  }

  actual_language="$(
    jq -er '.localizationInfo.defaultLanguageTag' "$package/manifest.json"
  )"
  [[ "$actual_language" == "ja" ]] || {
    echo "$slug: defaultLanguageTag must be ja" >&2
    exit 1
  }

  skill_diff="$(
    comm -3 \
      <(
        jq -r --arg slug "$slug" \
          '.plugins[$slug] | [.direct[], .powerPlatform[], .admin[]] | .[]' \
          "$MIGRATION_MAP" |
          sort
      ) \
      <(
        jq -r '.agentSkills[].folder | sub("^./skills/"; "")' \
          "$package/manifest.json" |
          sort
      )
  )"
  [[ -z "$skill_diff" ]] || {
    echo "$slug: manifest skill set differs from migration map:" >&2
    echo "$skill_diff" >&2
    exit 1
  }

  source_skill_diff="$(
    comm -3 \
      <(
        jq -r '.agentSkills[].folder | sub("^./skills/"; "")' \
          "$package/manifest.json" |
          sort
      ) \
      <(
        find "$package/skills" \
          -mindepth 1 \
          -maxdepth 1 \
          -type d \
          -printf '%f\n' |
          sort
      )
  )"
  [[ -z "$source_skill_diff" ]] || {
    echo "$slug: source skill directories differ from manifest:" >&2
    echo "$source_skill_diff" >&2
    exit 1
  }

  unsafe_entry="$(
    find "$package/skills" \
      -mindepth 1 \
      ! -type d \
      ! -type f \
      -print \
      -quit
  )"
  [[ -z "$unsafe_entry" ]] || {
    echo "$slug: source skill tree contains a link or special file" >&2
    echo "$unsafe_entry" >&2
    exit 1
  }

  jq -e 'has("agentConnectors") | not' \
    "$package/manifest.json" >/dev/null || {
    echo "$slug: connector packaging is deferred; remove agentConnectors" >&2
    exit 1
  }

  while IFS= read -r folder; do
    folder="${folder#./}"
    "$SKILLS_REF_PYTHON" -m skills_ref.cli validate \
      "$package/$folder" >/dev/null
  done < <(jq -r '.agentSkills[].folder' "$package/manifest.json")
}

for slug in "${EXPECTED_SLUGS[@]}"; do
  preflight_package "$slug"
done

stage_package() {
  local slug="$1"
  local stage_root="$2"
  local source="$TARGET/$slug"
  local stage="$stage_root/packages/$slug"
  local icon
  local relative

  mkdir -p "$stage"
  cp -p "$source/manifest.json" "$source/m365agents.yml" "$stage/"
  cp -a "$source/skills" "$stage/"
  while IFS= read -r icon; do
    relative="${icon#./}"
    mkdir -p "$stage/$(dirname "$relative")"
    cp -p "$source/$relative" "$stage/$relative"
  done < <(jq -r '.icons.color, .icons.outline' "$source/manifest.json")
}

build_package() {
  local slug="$1"
  local stage_root="$2"
  local source="$TARGET/$slug"
  local stage="$stage_root/packages/$slug"
  local raw_zip="$stage/atk-output/$slug-ja.zip"
  local normalized="$stage_root/normalized/$slug-ja.zip"
  local result
  local result_slug
  local digest
  local package_bytes

  stage_package "$slug" "$stage_root"
  atk validate \
    --manifest-file "$stage/manifest.json" \
    --interactive false \
    --telemetry false >/dev/null
  (
    cd "$stage"
    atk package \
      --folder . \
      --manifest-file manifest.json \
      --output-folder atk-output \
      --output-package-file "atk-output/$slug-ja.zip" \
      --telemetry false >/dev/null
  )
  [[ -f "$raw_zip" ]] || {
    echo "$slug: ATK did not produce $raw_zip" >&2
    exit 1
  }

  result="$(
    python3 "$NORMALIZER" "$raw_zip" "$normalized" "$source"
  )"
  result_slug="${result%%$'\t'*}"
  digest="${result#*$'\t'}"
  [[ "$result_slug" == "$slug" && "$digest" =~ ^[0-9a-f]{64}$ ]] || {
    echo "$slug: invalid normalizer result: $result" >&2
    exit 1
  }

  package_bytes="$(stat -c '%s' "$normalized")"
  ((package_bytes <= MAX_PACKAGE_BYTES)) || {
    echo "$slug: package exceeds $MAX_PACKAGE_BYTES bytes" >&2
    exit 1
  }
  printf '%s\t%s\n' "$slug" "$digest" >>"$stage_root/hash-map.tsv"
  printf '  ✓ %-24s %8d bytes  %s\n' \
    "$slug" "$package_bytes" "${digest:0:12}"
}

build_pass() {
  local label="$1"
  local stage_root="$2"
  local slug

  mkdir -p "$stage_root/packages" "$stage_root/normalized"
  : >"$stage_root/hash-map.tsv"
  printf 'Cowork package build pass %s:\n' "$label"
  for slug in "${EXPECTED_SLUGS[@]}"; do
    build_package "$slug" "$stage_root"
  done
}

write_fleet_hash_map() {
  local fleet_root="$1"
  local output="$2"
  local slug
  local package_zip
  local digest_line

  : >"$output"
  for slug in "${EXPECTED_SLUGS[@]}"; do
    package_zip="$fleet_root/$slug/$slug-ja.zip"
    [[ -f "$package_zip" && ! -L "$package_zip" ]] || {
      echo "$slug: fleet ZIP is missing or not regular" >&2
      exit 1
    }
    digest_line="$(sha256sum "$package_zip")"
    printf '%s\t%s\n' "$slug" "${digest_line%% *}" >>"$output"
  done
}

build_pass "1/2" "$FIRST_STAGE"
build_pass "2/2" "$SECOND_STAGE"

snapshot_sources "$SOURCE_AFTER"
if ! cmp -s "$SOURCE_BEFORE" "$SOURCE_AFTER"; then
  echo "tracked package sources changed during the build" >&2
  diff -u "$SOURCE_BEFORE" "$SOURCE_AFTER" >&2 || true
  exit 1
fi

if ! cmp -s \
  "$FIRST_STAGE/hash-map.tsv" \
  "$SECOND_STAGE/hash-map.tsv"; then
  echo "independent package builds produced different hash maps" >&2
  diff -u \
    "$FIRST_STAGE/hash-map.tsv" \
    "$SECOND_STAGE/hash-map.tsv" >&2 || true
  exit 1
fi

PUBLISH="$FIRST_STAGE/publish"
mkdir "$PUBLISH"
for slug in "${EXPECTED_SLUGS[@]}"; do
  mkdir "$PUBLISH/$slug"
  cp -p \
    "$FIRST_STAGE/normalized/$slug-ja.zip" \
    "$PUBLISH/$slug/$slug-ja.zip"
done

CANDIDATE_HASHES="$SECOND_STAGE/candidate-hash-map.tsv"
write_fleet_hash_map "$PUBLISH" "$CANDIDATE_HASHES"
cmp -s "$FIRST_STAGE/hash-map.tsv" "$CANDIDATE_HASHES" || {
  echo "publication candidate hashes differ from validated build hashes" >&2
  exit 1
}

if path_exists "$DIST"; then
  path_exists "$DIST_BACKUP" && {
    echo "publication backup already exists: $DIST_BACKUP" >&2
    exit 1
  }
  mv -T "$DIST" "$DIST_BACKUP"
  PUBLICATION_PENDING=1
  inject_failure "after-dist-backup"
  pause_at "after-dist-backup"
fi
mv -T "$PUBLISH" "$DIST"

PUBLISHED_HASHES="$SECOND_STAGE/published-hash-map.tsv"
write_fleet_hash_map "$DIST" "$PUBLISHED_HASHES"
cmp -s "$FIRST_STAGE/hash-map.tsv" "$PUBLISHED_HASHES" || {
  echo "published package hashes differ from validated build hashes" >&2
  exit 1
}

PUBLICATION_PENDING=0
rm -rf "$DIST_BACKUP" "$FAILED_DIST"

printf 'Microsoft 365 Cowork package build: OK (%d deterministic ZIPs)\n' \
  "$EXPECTED_PACKAGE_COUNT"
