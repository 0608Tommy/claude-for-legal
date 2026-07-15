#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

VALID="$TMP/valid"
INVALID="$TMP/invalid"
mkdir -p "$VALID/example/skills/example/references"
mkdir -p "$INVALID/example/skills/example"

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

# 検証用スキル

[参照](references/details.md)を必要な場合だけ読みます。
EOF

cat >"$VALID/example/skills/example/references/details.md" <<'EOF'
# 詳細

検証用の参照ファイルです。
EOF

cat >"$INVALID/example/skills/example/SKILL.md" <<'EOF'
---
name: wrong-name
description: 検証に失敗するスキルです。
argument-hint: "[unsupported]"
---

# 無効なスキル
EOF

PYTHONPATH="$ROOT/scripts" python3 - "$VALID" "$INVALID" <<'PY'
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
)
for fragment in required_fragments:
    if not any(fragment in error for error in invalid_errors):
        raise SystemExit(
            f"invalid fixture did not report {fragment}: {invalid_errors}"
        )

print("m365 Cowork target validator: OK")
PY
