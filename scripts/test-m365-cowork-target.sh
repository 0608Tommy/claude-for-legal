#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRATCH="$ROOT/m365-cowork-ja/.cache/target-test.${BASHPID:-$$}"
TARGET_CONTRACT="$ROOT/m365-cowork-ja/shared/target-contract.json"
TOOLCHAIN_LOCK="$ROOT/m365-cowork-ja/shared/toolchain-lock.json"

cleanup() {
  rm -rf "$SCRATCH"
}
trap cleanup EXIT HUP INT TERM

VALID="$SCRATCH/valid"
INVALID="$SCRATCH/invalid"
TOO_LONG="$SCRATCH/too-long"
TOO_MANY="$SCRATCH/too-many"
BACKTICK_ONLY="$SCRATCH/backtick-only"
DEPTH_THREE="$SCRATCH/depth-three"
DEPTH_FOUR="$SCRATCH/depth-four"
NESTED_NO_EXTENSION="$SCRATCH/nested-no-extension"
UNSUPPORTED_EXTENSION="$SCRATCH/unsupported-extension"
UPPERCASE_EXTENSION="$SCRATCH/uppercase-extension"
OLD_LEGAL_NAMES="$SCRATCH/old-legal-names"
ALTERNATE_LEGAL_EXTENSIONS="$SCRATCH/alternate-legal-extensions"
LEGAL_CASE_VARIANTS="$SCRATCH/legal-case-variants"
MISSING_LEGAL_PAIR="$SCRATCH/missing-legal-pair"
LEGAL_CONTENT_MISMATCH="$SCRATCH/legal-content-mismatch"
CASE_COLLISION="$SCRATCH/case-collision"
ORPHAN_SHAPE="$SCRATCH/orphan-shape"

mkdir -p "$VALID/example/skills/example/references"

cat >"$VALID/example/skills/example/SKILL.md" <<'EOF'
---
name: example
description: >
  日本語の検証用スキルです。
license: Apache-2.0
compatibility: Microsoft 365 Copilot Cowork
metadata:
  locale: ja-JP
---

> **変更通知:** 検証用の派生ファイルです。

# 検証用スキル

[参照](references/details.md)を必要な場合だけ読みます。
EOF

cat >"$VALID/example/skills/example/references/details.md" <<'EOF'
> **変更通知:** 検証用の派生ファイルです。

# 詳細

検証用の参照ファイルです。
EOF

cat >"$VALID/example/skills/example/references/notes.txt" <<'EOF'
fleet converter compatibility text fixture
EOF

cat >"$VALID/example/skills/example/references/data.json" <<'EOF'
{
  "fixture": "fleet-converter-compatibility"
}
EOF

cat >"$VALID/example/skills/example/references/helper.py" <<'EOF'
"""Fleet converter compatibility fixture."""

VALUE = "fixture"
EOF

printf 'Apache License 2.0\n' >"$VALID/example/LICENSE"
printf 'Modified package\n' >"$VALID/example/NOTICE"
cp \
  "$VALID/example/LICENSE" \
  "$VALID/example/skills/example/LICENSE.txt"
cp \
  "$VALID/example/NOTICE" \
  "$VALID/example/skills/example/NOTICE.txt"

clone_valid() {
  local destination="$1"

  mkdir -p "$destination"
  cp -R "$VALID/example" "$destination/example"
}

clone_valid "$INVALID"
cat >"$INVALID/example/skills/example/SKILL.md" <<'EOF'
---
name: wrong-name
description: 検証に失敗するスキルです。
argument-hint: "[unsupported]"
---

# 無効なスキル

[outside](../../README.md)

[absolute](/etc/passwd)

`../../references/outside.md`

$ARGUMENTS
EOF

clone_valid "$TOO_LONG"
python3 - "$TOO_LONG/example/skills/example/SKILL.md" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
header = """---
name: example
description: 文字数上限を検証するスキルです。
---

> **変更通知:** 検証用の派生ファイルです。

# 長すぎるスキル

"""
path.write_text(header + ("あ" * 20_001) + "\n", encoding="utf-8")
PY

mkdir -p "$TOO_MANY/example/skills"
printf 'Apache License 2.0\n' >"$TOO_MANY/example/LICENSE"
printf 'Modified package\n' >"$TOO_MANY/example/NOTICE"
for number in $(seq -w 1 21); do
  skill="skill-$number"
  mkdir -p "$TOO_MANY/example/skills/$skill"
  cat >"$TOO_MANY/example/skills/$skill/SKILL.md" <<EOF
---
name: $skill
description: パッケージ上限を検証するスキルです。
---

> **変更通知:** 検証用の派生ファイルです。

# パッケージ上限検証
EOF
  cp \
    "$TOO_MANY/example/LICENSE" \
    "$TOO_MANY/example/skills/$skill/LICENSE.txt"
  cp \
    "$TOO_MANY/example/NOTICE" \
    "$TOO_MANY/example/skills/$skill/NOTICE.txt"
done

clone_valid "$BACKTICK_ONLY"
cat >"$BACKTICK_ONLY/example/skills/example/SKILL.md" <<'EOF'
---
name: example
description: backtick path containmentを検証します。
---

> **変更通知:** 検証用の派生ファイルです。

# Backtick path containment

`../../README.md`

`/etc/passwd`
EOF

clone_valid "$DEPTH_THREE"
mkdir -p \
  "$DEPTH_THREE/example/skills/example/references/common/ja-jp"
printf '{"depth": 3}\n' > \
  "$DEPTH_THREE/example/skills/example/references/common/ja-jp/data.json"

clone_valid "$DEPTH_FOUR"
mkdir -p \
  "$DEPTH_FOUR/example/skills/example/references/common/jurisdictions/ja-jp"
printf '{"depth": 4}\n' > \
  "$DEPTH_FOUR/example/skills/example/references/common/jurisdictions/ja-jp/data.json"

clone_valid "$NESTED_NO_EXTENSION"
mkdir -p \
  "$NESTED_NO_EXTENSION/example/skills/example/references/nested"
printf 'no extension\n' > \
  "$NESTED_NO_EXTENSION/example/skills/example/references/nested/README"

clone_valid "$UNSUPPORTED_EXTENSION"
printf 'fixture: unsupported\n' > \
  "$UNSUPPORTED_EXTENSION/example/skills/example/references/payload.yaml"

clone_valid "$UPPERCASE_EXTENSION"
printf '{"fixture": "uppercase"}\n' > \
  "$UPPERCASE_EXTENSION/example/skills/example/references/payload.JSON"

clone_valid "$OLD_LEGAL_NAMES"
rm \
  "$OLD_LEGAL_NAMES/example/skills/example/LICENSE.txt" \
  "$OLD_LEGAL_NAMES/example/skills/example/NOTICE.txt"
cp \
  "$OLD_LEGAL_NAMES/example/LICENSE" \
  "$OLD_LEGAL_NAMES/example/skills/example/LICENSE"
cp \
  "$OLD_LEGAL_NAMES/example/NOTICE" \
  "$OLD_LEGAL_NAMES/example/skills/example/NOTICE"

clone_valid "$ALTERNATE_LEGAL_EXTENSIONS"
printf '{"fixture": "alternate legal extension"}\n' > \
  "$ALTERNATE_LEGAL_EXTENSIONS/example/skills/example/LICENSE.json"
cat > \
  "$ALTERNATE_LEGAL_EXTENSIONS/example/skills/example/NOTICE.md" <<'EOF'
> **変更通知:** 検証用の派生ファイルです。

# 不正な通知名

別拡張子のlegal fileを拒否するfixtureです。
EOF

clone_valid "$LEGAL_CASE_VARIANTS"
printf 'lowercase license\n' > \
  "$LEGAL_CASE_VARIANTS/example/skills/example/license.txt"
printf 'mixed-case notice\n' > \
  "$LEGAL_CASE_VARIANTS/example/skills/example/Notice.txt"

clone_valid "$MISSING_LEGAL_PAIR"
rm \
  "$MISSING_LEGAL_PAIR/example/skills/example/LICENSE.txt" \
  "$MISSING_LEGAL_PAIR/example/skills/example/NOTICE.txt"

clone_valid "$LEGAL_CONTENT_MISMATCH"
printf 'different license\n' > \
  "$LEGAL_CONTENT_MISMATCH/example/skills/example/LICENSE.txt"
printf 'different notice\n' > \
  "$LEGAL_CONTENT_MISMATCH/example/skills/example/NOTICE.txt"

clone_valid "$CASE_COLLISION"
printf 'upper path\n' > \
  "$CASE_COLLISION/example/skills/example/references/Case.txt"
printf 'lower path\n' > \
  "$CASE_COLLISION/example/skills/example/references/case.txt"

clone_valid "$ORPHAN_SHAPE"
printf 'fixture: orphan\n' > \
  "$ORPHAN_SHAPE/example/skills/orphan.yaml"
mkdir -p "$ORPHAN_SHAPE/example/skills/undeclared"
printf 'orphan directory\n' > \
  "$ORPHAN_SHAPE/example/skills/undeclared/note.txt"

PYTHONPATH="$ROOT/scripts" python3 - \
  "$SCRATCH" "$TARGET_CONTRACT" "$TOOLCHAIN_LOCK" <<'PY'
from __future__ import annotations

import copy
import json
import pathlib
import sys

from validate_m365_cowork_target import load_limits, validate_target

scratch = pathlib.Path(sys.argv[1])
target_contract_path = pathlib.Path(sys.argv[2])
toolchain_lock_path = pathlib.Path(sys.argv[3])
expected_extensions = frozenset({".md", ".json", ".py", ".txt"})
limits = load_limits(target_contract_path, toolchain_lock_path)

if limits.maximum_file_nesting_depth != 3:
    raise SystemExit("maximumFileNestingDepth contract was not loaded")
if limits.fleet_converter_extensions != expected_extensions:
    raise SystemExit(
        "unexpected fleet/converter compatibility extension set: "
        f"{limits.fleet_converter_extensions}",
    )

target_contract = json.loads(
    target_contract_path.read_text(encoding="utf-8"),
)
toolchain_lock = json.loads(
    toolchain_lock_path.read_text(encoding="utf-8"),
)
target_compatibility = target_contract["skill"][
    "fleetConverterCompatibility"
]
toolchain_compatibility = toolchain_lock["cowork"][
    "fleetConverterCompatibility"
]
target_extensions = target_compatibility["fileExtensions"]
toolchain_extensions = toolchain_compatibility["fileExtensions"]
if target_extensions != toolchain_extensions:
    raise SystemExit("target/toolchain extension arrays are not identical")
if frozenset(target_extensions) != expected_extensions:
    raise SystemExit("target/toolchain extension set is incomplete")
for compatibility in (target_compatibility, toolchain_compatibility):
    if "not a universal Microsoft allowlist" not in compatibility["scope"]:
        raise SystemExit("compatibility extension scope is overbroad")

observation = toolchain_lock["tools"]["claudeToCoworkPlugin"]
expected_observation = {
    "command": "/claude-to-cowork-plugin",
    "observedAt": "2026-07-17",
    "noExtensionFileResult": "rejected",
    "version": None,
    "sha256": None,
}
for key, expected_value in expected_observation.items():
    if observation.get(key) != expected_value:
        raise SystemExit(
            f"converter observation {key} was not recorded exactly",
        )

mismatched_toolchain = copy.deepcopy(toolchain_lock)
mismatched_toolchain["cowork"]["fleetConverterCompatibility"][
    "fileExtensions"
].append(".yaml")
mismatched_path = scratch / "toolchain-mismatch.json"
mismatched_path.write_text(
    json.dumps(mismatched_toolchain, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
try:
    load_limits(target_contract_path, mismatched_path)
except ValueError as error:
    if "must match exactly" not in str(error):
        raise SystemExit(
            f"parity mismatch reported the wrong error: {error}",
        ) from error
else:
    raise SystemExit("target/toolchain extension mismatch was accepted")


def fixture_errors(name: str) -> list[str]:
    errors, _ = validate_target(scratch / name, limits)
    return errors


def require_clean(name: str) -> None:
    errors = fixture_errors(name)
    if errors:
        raise SystemExit(f"{name} fixture failed: {errors}")


def require_fragments(name: str, fragments: tuple[str, ...]) -> None:
    errors = fixture_errors(name)
    for fragment in fragments:
        if not any(fragment in error for error in errors):
            raise SystemExit(
                f"{name} fixture did not report {fragment}: {errors}",
            )


require_clean("valid")
require_clean("depth-three")

require_fragments(
    "invalid",
    (
        "unexpected frontmatter fields",
        "name must match folder",
        "reference escapes skill root",
        "absolute local reference is forbidden",
        "unsupported source runtime marker",
    ),
)
require_fragments("too-long", ("characters exceeds",))
require_fragments("too-many", ("skills exceeds",))
require_fragments(
    "backtick-only",
    (
        "reference escapes skill root",
        "absolute local reference is forbidden",
    ),
)
require_fragments(
    "depth-four",
    (
        "references/common/jurisdictions/ja-jp/data.json: "
        "file nesting depth 4 exceeds maximum 3",
    ),
)
require_fragments(
    "nested-no-extension",
    (
        "references/nested/README: file has no extension",
    ),
)
require_fragments(
    "unsupported-extension",
    (
        "payload.yaml: unsupported fleet/converter compatibility "
        "extension .yaml",
    ),
)
require_fragments(
    "uppercase-extension",
    (
        "payload.JSON: uppercase file extension is forbidden: .JSON",
    ),
)
require_fragments(
    "old-legal-names",
    (
        "skills/example/LICENSE: file has no extension",
        "skills/example/NOTICE: file has no extension",
        "required skill legal name is LICENSE.txt",
        "required skill legal name is NOTICE.txt",
    ),
)
require_fragments(
    "alternate-legal-extensions",
    (
        "LICENSE.json: skill legal filename must be exactly LICENSE.txt",
        "NOTICE.md: skill legal filename must be exactly NOTICE.txt",
    ),
)
require_fragments(
    "legal-case-variants",
    (
        "license.txt: skill legal filename must be exactly LICENSE.txt",
        "Notice.txt: skill legal filename must be exactly NOTICE.txt",
    ),
)
require_fragments(
    "missing-legal-pair",
    (
        "missing exact companion LICENSE.txt",
        "missing exact companion NOTICE.txt",
    ),
)
require_fragments(
    "legal-content-mismatch",
    (
        "LICENSE.txt: content does not byte-match package-root LICENSE",
        "NOTICE.txt: content does not byte-match package-root NOTICE",
    ),
)
require_fragments(
    "case-collision",
    ("case-insensitive path collision",),
)
require_fragments(
    "orphan-shape",
    (
        "skills/orphan.yaml: orphan file outside skills/<skill>/",
        "skills/orphan.yaml: unsupported fleet/converter compatibility "
        "extension .yaml",
        "skills/undeclared: orphan skill directory missing SKILL.md",
    ),
)

print("m365 Cowork target validator: OK")
PY
