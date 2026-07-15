#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Build locally validated, skills-only Microsoft 365 Cowork app packages.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="$ROOT/m365-cowork-ja/cowork-packages"
DIST="$ROOT/m365-cowork-ja/dist"
ATK_VERSION="1.1.12"
MAX_PACKAGE_BYTES=$((10 * 1024 * 1024))
SKILLS_REF_PYTHON="${SKILLS_REF_PYTHON:-$ROOT/m365-cowork-ja/.cache/skills-ref-venv/bin/python}"

command -v atk >/dev/null || {
  echo "requires @microsoft/m365agentstoolkit-cli@$ATK_VERSION" >&2
  exit 2
}
command -v jq >/dev/null || {
  echo "requires jq" >&2
  exit 2
}
command -v unzip >/dev/null || {
  echo "requires unzip" >&2
  exit 2
}
[[ -x "$SKILLS_REF_PYTHON" ]] || {
  echo "requires skills-ref 0.1.1 at $SKILLS_REF_PYTHON" >&2
  exit 2
}

actual_atk_version="$(atk --version)"
[[ "$actual_atk_version" == "$ATK_VERSION" ]] || {
  echo "requires atk $ATK_VERSION; found $actual_atk_version" >&2
  exit 2
}

python3 "$ROOT/scripts/apply_m365_apache_notices.py" >/dev/null
python3 "$ROOT/scripts/validate_m365_cowork_target.py"

found=0
for package in "$TARGET"/*; do
  [[ -d "$package" && -f "$package/manifest.json" ]] || continue
  found=1
  slug="$(basename "$package")"
  package_dist="$DIST/$slug"
  package_zip="$package_dist/$slug-ja.zip"

  jq -e 'has("agentConnectors") | not' "$package/manifest.json" >/dev/null || {
    echo "$slug: connector packaging is deferred; remove agentConnectors" >&2
    exit 1
  }

  while IFS= read -r skill; do
    "$SKILLS_REF_PYTHON" -m skills_ref.cli validate "$skill" >/dev/null
  done < <(find "$package/skills" -mindepth 1 -maxdepth 1 -type d | sort)

  atk validate \
    --manifest-file "$package/manifest.json" \
    --interactive false \
    --telemetry false >/dev/null

  rm -rf "$package/build"
  (
    cd "$package"
    atk package \
      --folder . \
      --manifest-file manifest.json \
      --output-folder build \
      --output-package-file "build/$slug-ja.zip" \
      --telemetry false >/dev/null
  )

  mkdir -p "$package_dist"
  cp "$package/build/$slug-ja.zip" "$package_zip"
  unzip -t "$package_zip" >/dev/null

  package_bytes="$(stat -c '%s' "$package_zip")"
  ((package_bytes <= MAX_PACKAGE_BYTES)) || {
    echo "$slug: package exceeds $MAX_PACKAGE_BYTES bytes" >&2
    exit 1
  }

  python3 - "$package_zip" "$package/manifest.json" <<'PY'
import json
import pathlib
import sys
import zipfile

archive_path = pathlib.Path(sys.argv[1])
manifest_path = pathlib.Path(sys.argv[2])
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
skill_folders = [
    entry["folder"].removeprefix("./")
    for entry in manifest["agentSkills"]
]
with zipfile.ZipFile(archive_path) as archive:
    archive_names = set(archive.namelist())

missing = [
    required
    for folder in skill_folders
    for required in (f"{folder}/LICENSE", f"{folder}/NOTICE")
    if required not in archive_names
]
if missing:
    raise SystemExit(f"packaged license notices are missing: {missing}")
PY

  printf '  ✓ %-24s %8d bytes\n' "$slug" "$package_bytes"
done

((found == 1)) || {
  echo "no Cowork packages with manifest.json found under $TARGET" >&2
  exit 1
}
