#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/package/skills/example"

cat >"$TMP/package/skills/example/SKILL.md" <<'EOF'
---
name: example
description: 変更通知を検証します。
---

# スキル
EOF

cat >"$TMP/package/README.md" <<'EOF'
# パッケージ
EOF

PYTHONPATH="$ROOT/scripts" python3 - "$TMP" <<'PY'
import pathlib
import sys

from apply_m365_apache_notices import (
    NOTICE_MARKER,
    apply_notices,
)

target = pathlib.Path(sys.argv[1])
if apply_notices(target) != 2:
    raise SystemExit("expected two files to change")
if apply_notices(target) != 0:
    raise SystemExit("notice application must be idempotent")

skill = (target / "package/skills/example/SKILL.md").read_text(
    encoding="utf-8"
)
readme = (target / "package/README.md").read_text(encoding="utf-8")
if not skill.startswith("---\n"):
    raise SystemExit("skill frontmatter must remain first")
if NOTICE_MARKER not in skill or NOTICE_MARKER not in readme:
    raise SystemExit("change notice missing")

print("m365 Apache change notices: OK")
PY
