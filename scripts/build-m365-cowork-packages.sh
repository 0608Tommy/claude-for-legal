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
TOOLCHAIN_LOCK="$M365_ROOT/shared/toolchain-lock.json"
NORMALIZER="$ROOT/scripts/normalize_m365_cowork_package.py"
ICON_VALIDATOR="$ROOT/scripts/validate_m365_cowork_icons.py"
ATK_VERSION="1.1.12"
SKILLS_REF_VERSION="0.1.1"
PYYAML_VERSION="6.0.3"
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
LEGACY_DIST_BACKUP="$CACHE/dist-publication-backup"
PAUSE_MARKER="$CACHE/package-build-paused.$RUN_ID"

path_exists() {
  [[ -e "$1" || -L "$1" ]]
}

mirror_candidate_path() {
  local slug="$1"

  printf '%s\n' \
    "$TARGET/$slug/build/.m365-cowork-mirror-candidate.$RUN_ID.zip"
}

recover_legacy_publication() {
  if ! path_exists "$DIST" && path_exists "$LEGACY_DIST_BACKUP"; then
    echo "restoring legacy interrupted Cowork publication" >&2
    mv --no-copy -T "$LEGACY_DIST_BACKUP" "$DIST"
  elif path_exists "$DIST" && path_exists "$LEGACY_DIST_BACKUP"; then
    rm -rf "$LEGACY_DIST_BACKUP"
  fi
}

cleanup_abandoned_builds() {
  local abandoned
  local mirror_dir
  local slug

  for abandoned in \
    "$CACHE"/package-build-first.* \
    "$CACHE"/package-build-second.* \
    "$CACHE"/dist-publication-failed.*; do
    [[ -d "$abandoned" ]] && rm -rf "$abandoned"
  done
  for abandoned in "$CACHE"/package-build-paused.*; do
    [[ -f "$abandoned" || -L "$abandoned" ]] && rm -f "$abandoned"
  done
  for slug in "${EXPECTED_SLUGS[@]}"; do
    mirror_dir="$TARGET/$slug/build"
    if path_exists "$mirror_dir"; then
      [[ -d "$mirror_dir" && ! -L "$mirror_dir" ]] || {
        echo "$slug: mirror build path must be a regular directory" >&2
        exit 1
      }
    else
      continue
    fi
    for abandoned in \
      "$mirror_dir"/.m365-cowork-mirror-candidate.*.zip; do
      if path_exists "$abandoned"; then
        [[ ! -d "$abandoned" || -L "$abandoned" ]] || {
          echo "$slug: abandoned mirror candidate is a directory" >&2
          exit 1
        }
        rm -f -- "$abandoned"
      fi
    done
  done
  return 0
}

cleanup() {
  local status=$?
  local candidate
  local slug

  trap - EXIT HUP INT TERM
  for slug in "${EXPECTED_SLUGS[@]}"; do
    candidate="$(mirror_candidate_path "$slug")"
    rm -f -- "$candidate" 2>/dev/null || true
  done
  rm -rf "$FIRST_STAGE" "$SECOND_STAGE"
  rm -f "$PAUSE_MARKER"
  exit "$status"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

recover_legacy_publication
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
  local requested=",${M365_COWORK_BUILD_PAUSE_AT:-},"

  if [[ "$requested" == *",$point,"* ]]; then
    printf '%s\t%s\n' "$BASHPID" "$point" >"$PAUSE_MARKER"
    kill -STOP "$BASHPID"
    rm -f "$PAUSE_MARKER"
  fi
}

inject_failure "after-recovery"
mkdir "$FIRST_STAGE" "$SECOND_STAGE"

for tool in atk cmp cp diff find git jq mv python3 sha256sum stat; do
  command -v "$tool" >/dev/null || {
    echo "requires $tool" >&2
    exit 2
  }
done
[[ -x "$SKILLS_REF_PYTHON" ]] || {
  echo "requires skills-ref $SKILLS_REF_VERSION at $SKILLS_REF_PYTHON" >&2
  exit 2
}

locked_skills_ref_version="$(
  jq -er '.tools.agentSkillsReference.version' "$TOOLCHAIN_LOCK"
)"
[[ "$locked_skills_ref_version" == "$SKILLS_REF_VERSION" ]] || {
  echo "toolchain must pin skills-ref $SKILLS_REF_VERSION" >&2
  exit 2
}
actual_skills_ref_version="$(
  "$SKILLS_REF_PYTHON" -c \
    'from importlib.metadata import version; print(version("skills-ref"))'
)"
[[ "$actual_skills_ref_version" == "$SKILLS_REF_VERSION" ]] || {
  echo "requires skills-ref $SKILLS_REF_VERSION; found $actual_skills_ref_version" >&2
  exit 2
}

locked_pyyaml_version="$(jq -er '.tools.pyYaml.version' "$TOOLCHAIN_LOCK")"
[[ "$locked_pyyaml_version" == "$PYYAML_VERSION" ]] || {
  echo "toolchain must pin PyYAML $PYYAML_VERSION" >&2
  exit 2
}
actual_pyyaml_version="$(
  python3 -c 'from importlib.metadata import version; print(version("PyYAML"))'
)"
[[ "$actual_pyyaml_version" == "$PYYAML_VERSION" ]] || {
  echo "requires PyYAML $PYYAML_VERSION; found $actual_pyyaml_version" >&2
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
  local label="$3"
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
  require_exact_hash_map "$label" "$output"
}

ensure_mirror_directory() {
  local slug="$1"
  local mirror_dir="$TARGET/$slug/build"

  if path_exists "$mirror_dir"; then
    [[ -d "$mirror_dir" && ! -L "$mirror_dir" ]] || {
      echo "$slug: mirror build path must be a regular directory" >&2
      exit 1
    }
  else
    mkdir -- "$mirror_dir"
  fi
}

build_mirror_candidates() {
  local output="$1"
  local slug
  local source
  local canonical
  local candidate
  local contract_copy
  local canonical_digest_line
  local candidate_digest_line
  local canonical_digest
  local candidate_digest
  local canonical_bytes
  local candidate_bytes
  local result
  local result_slug
  local contract_digest

  mkdir -p "$SECOND_STAGE/mirror-contract"
  : >"$output"
  for slug in "${EXPECTED_SLUGS[@]}"; do
    source="$TARGET/$slug"
    canonical="$DIST/$slug/$slug-ja.zip"
    ensure_mirror_directory "$slug"
    candidate="$(mirror_candidate_path "$slug")"
    contract_copy="$SECOND_STAGE/mirror-contract/$slug-ja.zip"
    ! path_exists "$candidate" || {
      echo "$slug: mirror candidate already exists" >&2
      exit 1
    }

    cp -p -- "$canonical" "$candidate"
    [[ -f "$candidate" && ! -L "$candidate" ]] || {
      echo "$slug: mirror candidate is not a regular file" >&2
      exit 1
    }
    cmp -s "$canonical" "$candidate" || {
      echo "$slug: mirror candidate bytes differ from canonical dist" >&2
      exit 1
    }
    canonical_bytes="$(stat -c '%s' "$canonical")"
    candidate_bytes="$(stat -c '%s' "$candidate")"
    [[ "$candidate_bytes" == "$canonical_bytes" ]] || {
      echo "$slug: mirror candidate size differs from canonical dist" >&2
      exit 1
    }

    result="$(
      python3 "$NORMALIZER" "$candidate" "$contract_copy" "$source"
    )"
    result_slug="${result%%$'\t'*}"
    contract_digest="${result#*$'\t'}"
    [[
      "$result_slug" == "$slug" &&
        "$contract_digest" =~ ^[0-9a-f]{64}$
    ]] || {
      echo "$slug: invalid mirror contract result: $result" >&2
      exit 1
    }
    cmp -s "$candidate" "$contract_copy" || {
      echo "$slug: mirror candidate violates normalized ZIP contract" >&2
      exit 1
    }

    canonical_digest_line="$(sha256sum "$canonical")"
    candidate_digest_line="$(sha256sum "$candidate")"
    canonical_digest="${canonical_digest_line%% *}"
    candidate_digest="${candidate_digest_line%% *}"
    [[
      "$candidate_digest" == "$canonical_digest" &&
        "$contract_digest" == "$canonical_digest"
    ]] || {
      echo "$slug: mirror candidate digest differs from canonical dist" >&2
      exit 1
    }
    printf '%s\t%s\n' "$slug" "$candidate_digest" >>"$output"
  done
  require_exact_hash_map "validated mirror candidate hash map" "$output"
}

write_mirror_hash_map() {
  local output="$1"
  local slug
  local canonical
  local mirror
  local digest_line

  : >"$output"
  for slug in "${EXPECTED_SLUGS[@]}"; do
    canonical="$DIST/$slug/$slug-ja.zip"
    mirror="$TARGET/$slug/build/$slug-ja.zip"
    [[ -f "$mirror" && ! -L "$mirror" ]] || {
      echo "$slug: package-local mirror ZIP is missing or not regular" >&2
      exit 1
    }
    cmp -s "$canonical" "$mirror" || {
      echo "$slug: package-local mirror bytes differ from canonical dist" >&2
      exit 1
    }
    digest_line="$(sha256sum "$mirror")"
    printf '%s\t%s\n' "$slug" "${digest_line%% *}" >>"$output"
  done
  require_exact_hash_map "published mirror hash map" "$output"
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
require_exact_hash_map \
  "validated deterministic build hash map" \
  "$FIRST_STAGE/hash-map.tsv"

PUBLISH="$FIRST_STAGE/publish"
mkdir "$PUBLISH"
for slug in "${EXPECTED_SLUGS[@]}"; do
  mkdir "$PUBLISH/$slug"
  cp -p \
    "$FIRST_STAGE/normalized/$slug-ja.zip" \
    "$PUBLISH/$slug/$slug-ja.zip"
done

CANDIDATE_HASHES="$SECOND_STAGE/candidate-hash-map.tsv"
write_fleet_hash_map \
  "$PUBLISH" \
  "$CANDIDATE_HASHES" \
  "dist publication candidate hash map"
cmp -s "$FIRST_STAGE/hash-map.tsv" "$CANDIDATE_HASHES" || {
  echo "publication candidate hashes differ from validated build hashes" >&2
  exit 1
}

if path_exists "$DIST"; then
  pause_at "before-dist-exchange"
  mv --exchange --no-copy -T "$PUBLISH" "$DIST"
  pause_at "after-dist-exchange"
else
  mv --no-copy -T "$PUBLISH" "$DIST"
fi

PUBLISHED_HASHES="$SECOND_STAGE/published-hash-map.tsv"
write_fleet_hash_map "$DIST" "$PUBLISHED_HASHES" "published dist hash map"
cmp -s "$FIRST_STAGE/hash-map.tsv" "$PUBLISHED_HASHES" || {
  echo "published package hashes differ from validated build hashes" >&2
  exit 1
}

MIRROR_CANDIDATE_HASHES="$SECOND_STAGE/mirror-candidate-hash-map.tsv"
build_mirror_candidates "$MIRROR_CANDIDATE_HASHES"
cmp -s "$FIRST_STAGE/hash-map.tsv" "$MIRROR_CANDIDATE_HASHES" || {
  echo "validated mirror candidate hashes differ from canonical dist" >&2
  exit 1
}

pause_at "before-mirror-renames"
inject_failure "before-mirror-renames"
for slug in "${EXPECTED_SLUGS[@]}"; do
  mirror_candidate="$(mirror_candidate_path "$slug")"
  mirror="$TARGET/$slug/build/$slug-ja.zip"
  mv --no-copy -T "$mirror_candidate" "$mirror"
  pause_at "after-mirror-rename-$slug"
  inject_failure "after-mirror-rename-$slug"
done

MIRROR_HASHES="$SECOND_STAGE/mirror-hash-map.tsv"
write_mirror_hash_map "$MIRROR_HASHES"
cmp -s "$FIRST_STAGE/hash-map.tsv" "$MIRROR_HASHES" || {
  echo "published mirror hashes differ from validated build hashes" >&2
  exit 1
}
cmp -s "$PUBLISHED_HASHES" "$MIRROR_HASHES" || {
  echo "published dist and mirror hash maps differ" >&2
  exit 1
}

printf \
  'Microsoft 365 Cowork package build: OK (%d deterministic ZIPs + mirrors)\n' \
  "$EXPECTED_PACKAGE_COUNT"
