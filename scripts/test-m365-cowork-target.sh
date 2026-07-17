#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRATCH="$ROOT/m365-cowork-ja/.cache/target-test.${BASHPID:-$$}"

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
mkdir -p "$VALID/example/skills/example/references"
mkdir -p "$INVALID/example/skills/example"
mkdir -p "$TOO_LONG/example/skills/too-long"
mkdir -p "$TOO_MANY/example/skills"
mkdir -p "$BACKTICK_ONLY/example/skills/example"
mkdir -p "$DEPTH_THREE" "$DEPTH_FOUR"

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

printf 'Apache License 2.0\n' >"$VALID/example/LICENSE"
printf 'Modified package\n' >"$VALID/example/NOTICE"
cp "$VALID/example/LICENSE" "$VALID/example/skills/example/LICENSE"
cp "$VALID/example/NOTICE" "$VALID/example/skills/example/NOTICE"

cp -R "$VALID/example" "$DEPTH_THREE/example"
mkdir -p \
  "$DEPTH_THREE/example/skills/example/references/common/ja-jp"
printf '{"depth": 3}\n' > \
  "$DEPTH_THREE/example/skills/example/references/common/ja-jp/data.json"

cp -R "$VALID/example" "$DEPTH_FOUR/example"
mkdir -p \
  "$DEPTH_FOUR/example/skills/example/references/common/jurisdictions/ja-jp"
printf '{"depth": 4}\n' > \
  "$DEPTH_FOUR/example/skills/example/references/common/jurisdictions/ja-jp/data.json"

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

python3 - "$TOO_LONG/example/skills/too-long/SKILL.md" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
header = """---
name: too-long
description: 文字数上限を検証するスキルです。
---

# 長すぎるスキル

"""
path.write_text(header + ("あ" * 20_001) + "\n", encoding="utf-8")
PY

for number in $(seq -w 1 21); do
  skill="skill-$number"
  mkdir -p "$TOO_MANY/example/skills/$skill"
  cat >"$TOO_MANY/example/skills/$skill/SKILL.md" <<EOF
---
name: $skill
description: パッケージ上限を検証するスキルです。
---

# パッケージ上限検証
EOF
done

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

PYTHONPATH="$ROOT/scripts" python3 - \
  "$VALID" "$INVALID" "$TOO_LONG" "$TOO_MANY" \
  "$BACKTICK_ONLY" "$DEPTH_THREE" "$DEPTH_FOUR" \
  "$ROOT/m365-cowork-ja/shared/toolchain-lock.json" <<'PY'
import json
import pathlib
import sys

from validate_m365_cowork_target import load_limits, validate_target

limits = load_limits()
if limits.maximum_file_nesting_depth != 3:
    raise SystemExit(
        "maximumFileNestingDepth contract was not loaded"
    )
toolchain_lock = json.loads(
    pathlib.Path(sys.argv[8]).read_text(encoding="utf-8")
)
if (
    toolchain_lock["limits"]["maximumFileNestingDepth"]
    != limits.maximum_file_nesting_depth
):
    raise SystemExit(
        "maximumFileNestingDepth machine contracts disagree"
    )

valid_errors, _ = validate_target(pathlib.Path(sys.argv[1]), limits)
if valid_errors:
    raise SystemExit(f"valid fixture failed: {valid_errors}")

invalid_errors, _ = validate_target(pathlib.Path(sys.argv[2]), limits)
required_fragments = (
    "unexpected frontmatter fields",
    "name must match folder",
    "reference escapes skill root",
    "absolute local reference is forbidden",
    "unsupported source runtime marker",
)
for fragment in required_fragments:
    if not any(fragment in error for error in invalid_errors):
        raise SystemExit(
            f"invalid fixture did not report {fragment}: {invalid_errors}"
        )

long_errors, _ = validate_target(pathlib.Path(sys.argv[3]), limits)
if not any("characters exceeds" in error for error in long_errors):
    raise SystemExit(
        f"character limit was not enforced: {long_errors}"
    )

many_errors, _ = validate_target(pathlib.Path(sys.argv[4]), limits)
if not any("skills exceeds" in error for error in many_errors):
    raise SystemExit(
        f"package skill limit was not enforced: {many_errors}"
    )

backtick_errors, _ = validate_target(pathlib.Path(sys.argv[5]), limits)
backtick_fragments = (
    "reference escapes skill root",
    "absolute local reference is forbidden",
)
for fragment in backtick_fragments:
    if not any(fragment in error for error in backtick_errors):
        raise SystemExit(
            f"backtick fixture did not report {fragment}: "
            f"{backtick_errors}"
        )

depth_three_errors, _ = validate_target(
    pathlib.Path(sys.argv[6]),
    limits,
)
if depth_three_errors:
    raise SystemExit(
        f"depth-3 fixture failed: {depth_three_errors}"
    )

depth_four_errors, _ = validate_target(
    pathlib.Path(sys.argv[7]),
    limits,
)
depth_four_fragment = (
    "references/common/jurisdictions/ja-jp/data.json: "
    "file nesting depth 4 exceeds maximum 3"
)
if not any(
    depth_four_fragment in error
    for error in depth_four_errors
):
    raise SystemExit(
        f"depth-4 fixture was accepted: {depth_four_errors}"
    )

print("m365 Cowork target validator: OK")
PY
