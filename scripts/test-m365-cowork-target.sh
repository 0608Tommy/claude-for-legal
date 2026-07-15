#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

VALID="$TMP/valid"
INVALID="$TMP/invalid"
TOO_LONG="$TMP/too-long"
TOO_MANY="$TMP/too-many"
BACKTICK_ONLY="$TMP/backtick-only"
mkdir -p "$VALID/example/skills/example/references"
mkdir -p "$INVALID/example/skills/example"
mkdir -p "$TOO_LONG/example/skills/too-long"
mkdir -p "$TOO_MANY/example/skills"
mkdir -p "$BACKTICK_ONLY/example/skills/example"

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
  "$BACKTICK_ONLY" <<'PY'
import pathlib
import sys

from validate_m365_cowork_target import load_limits, validate_target

limits = load_limits()
valid_errors, _ = validate_target(pathlib.Path(sys.argv[1]), limits)
if valid_errors:
    raise SystemExit(f"valid fixture failed: {valid_errors}")

invalid_errors, _ = validate_target(pathlib.Path(sys.argv[2]), limits)
required_fragments = (
    "unexpected frontmatter fields",
    "name must match folder",
    "reference escapes skill root",
    "absolute local reference is forbidden",
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

print("m365 Cowork target validator: OK")
PY
