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
MANIFEST_MISMATCH="$SCRATCH/manifest-mismatch"
COMPANION_COUNT_EXACT="$SCRATCH/companion-count-exact"
COMPANION_COUNT_TOO_MANY="$SCRATCH/companion-count-too-many"
FILE_SIZE_EXACT="$SCRATCH/file-size-exact"
FILE_SIZE_TOO_LARGE="$SCRATCH/file-size-too-large"
TOTAL_SIZE_EXACT="$SCRATCH/total-size-exact"
TOTAL_SIZE_TOO_LARGE="$SCRATCH/total-size-too-large"
SAFE_PATHS="$SCRATCH/safe-paths"
HIDDEN_FILE="$SCRATCH/hidden-file"
HIDDEN_DIRECTORY="$SCRATCH/hidden-directory"
RESERVED_CON="$SCRATCH/reserved-con"
RESERVED_COM1="$SCRATCH/reserved-com1"
BACKSLASH_PATH="$SCRATCH/backslash-path"
AT_PATH="$SCRATCH/at-path"
UNICODE_PATH="$SCRATCH/unicode-path"
TRAILING_DOT="$SCRATCH/trailing-dot"
TRAILING_SPACE="$SCRATCH/trailing-space"
NAME_ONE="$SCRATCH/name-one"
NAME_64="$SCRATCH/name-64"
NAME_65="$SCRATCH/name-65"
NAME_LEADING_HYPHEN="$SCRATCH/name-leading-hyphen"
NAME_TRAILING_HYPHEN="$SCRATCH/name-trailing-hyphen"
NAME_CONSECUTIVE_HYPHENS="$SCRATCH/name-consecutive-hyphens"
NAME_UPPERCASE="$SCRATCH/name-uppercase"
NAME_UNDERSCORE="$SCRATCH/name-underscore"
NAME_PLAIN_TRUE="$SCRATCH/name-plain-true"
NAME_PLAIN_NULL="$SCRATCH/name-plain-null"
NAME_PLAIN_INTEGER="$SCRATCH/name-plain-integer"
NAME_YAML_12_ON="$SCRATCH/name-yaml-12-on"
NAME_YAML_12_OFF="$SCRATCH/name-yaml-12-off"
NAME_YAML_12_YES="$SCRATCH/name-yaml-12-yes"
NAME_YAML_12_DATE="$SCRATCH/name-yaml-12-date"
MALFORMED_YAML="$SCRATCH/malformed-yaml"
DUPLICATE_YAML="$SCRATCH/duplicate-yaml"
EXPLICIT_STR_TAG="$SCRATCH/explicit-str-tag"
EXPLICIT_BOOL_TAG="$SCRATCH/explicit-bool-tag"
EXPLICIT_TIMESTAMP_TAG="$SCRATCH/explicit-timestamp-tag"
UNSUPPORTED_YAML_TAG="$SCRATCH/unsupported-yaml-tag"
NON_MAPPING_YAML="$SCRATCH/non-mapping-yaml"
NON_STRING_NAME="$SCRATCH/non-string-name"
NON_STRING_DESCRIPTION="$SCRATCH/non-string-description"
DESCRIPTION_ONE="$SCRATCH/description-one"
DESCRIPTION_1024="$SCRATCH/description-1024"
DESCRIPTION_1025="$SCRATCH/description-1025"
CTA_ENGLISH="$SCRATCH/cta-english"
CTA_JAPANESE="$SCRATCH/cta-japanese"
CTA_NEUTRAL="$SCRATCH/cta-neutral"

mkdir -p "$VALID/example/skills/example/references"

cat >"$VALID/example/manifest.json" <<'EOF'
{
  "agentSkills": [
    {
      "folder": "./skills/example"
    }
  ]
}
EOF

cat >"$VALID/example/skills/example/SKILL.md" <<'EOF'
---
name: example
description: >
  日本語の検証用スキルです。
license: Apache-2.0
compatibility: Microsoft 365 Copilot Cowork
metadata:
  locale: ja-JP
  plain-values:
    - true
    - null
    - 123
    - 2026-01-01
    - on
  nested:
    enabled: false
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

clone_named_valid() {
  local destination="$1"
  local name="$2"

  clone_valid "$destination"
  python3 - "$destination/example" "$name" <<'PY'
from __future__ import annotations

import json
import pathlib
import sys

package = pathlib.Path(sys.argv[1])
name = sys.argv[2]
old_skill = package / "skills" / "example"
new_skill = package / "skills" / name
old_skill.rename(new_skill)
skill_path = new_skill / "SKILL.md"
skill_path.write_text(
    skill_path.read_text(encoding="utf-8").replace(
        "name: example",
        f"name: {name}",
        1,
    ),
    encoding="utf-8",
)
manifest_path = package / "manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["agentSkills"] = [{"folder": f"./skills/{name}"}]
manifest_path.write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY
}

clone_description_valid() {
  local destination="$1"
  local character_count="$2"

  clone_valid "$destination"
  python3 - \
    "$destination/example/skills/example/SKILL.md" \
    "$character_count" <<'PY'
from __future__ import annotations

import pathlib
import sys

path = pathlib.Path(sys.argv[1])
description = "あ" * int(sys.argv[2])
path.write_text(
    (
        "---\n"
        "name: example\n"
        f"description: {description}\n"
        "license: Apache-2.0\n"
        "---\n\n"
        "> **変更通知:** 検証用の派生ファイルです。\n\n"
        "# description boundary\n"
    ),
    encoding="utf-8",
)
PY
}

name_64="$(python3 -c 'print("a" * 64)')"
name_65="$(python3 -c 'print("a" * 65)')"
clone_named_valid "$NAME_ONE" "a"
clone_named_valid "$NAME_64" "$name_64"
clone_named_valid "$NAME_65" "$name_65"
clone_named_valid "$NAME_LEADING_HYPHEN" "-example"
clone_named_valid "$NAME_TRAILING_HYPHEN" "example-"
clone_named_valid "$NAME_CONSECUTIVE_HYPHENS" "example--skill"
clone_named_valid "$NAME_UPPERCASE" "Example"
clone_named_valid "$NAME_UNDERSCORE" "example_skill"
clone_named_valid "$NAME_PLAIN_TRUE" "true"
clone_named_valid "$NAME_PLAIN_NULL" "null"
clone_named_valid "$NAME_PLAIN_INTEGER" "123"
clone_named_valid "$NAME_YAML_12_ON" "on"
clone_named_valid "$NAME_YAML_12_OFF" "off"
clone_named_valid "$NAME_YAML_12_YES" "yes"
clone_named_valid "$NAME_YAML_12_DATE" "2026-01-01"

clone_description_valid "$DESCRIPTION_ONE" 1
clone_description_valid "$DESCRIPTION_1024" 1024
clone_description_valid "$DESCRIPTION_1025" 1025

clone_valid "$MALFORMED_YAML"
cat >"$MALFORMED_YAML/example/skills/example/SKILL.md" <<'EOF'
---
name: example
description: [malformed
---

> **変更通知:** 検証用の派生ファイルです。
EOF

clone_valid "$DUPLICATE_YAML"
cat >"$DUPLICATE_YAML/example/skills/example/SKILL.md" <<'EOF'
---
name: example
name: duplicate
description: 日本語の重複key検証です。
---

> **変更通知:** 検証用の派生ファイルです。
EOF

clone_valid "$EXPLICIT_STR_TAG"
cat >"$EXPLICIT_STR_TAG/example/skills/example/SKILL.md" <<'EOF'
---
name: !!str example
description: 日本語の明示str tag検証です。
---

> **変更通知:** 検証用の派生ファイルです。
EOF

clone_valid "$EXPLICIT_BOOL_TAG"
cat >"$EXPLICIT_BOOL_TAG/example/skills/example/SKILL.md" <<'EOF'
---
name: !!bool true
description: 日本語の明示bool tag検証です。
---

> **変更通知:** 検証用の派生ファイルです。
EOF

clone_valid "$EXPLICIT_TIMESTAMP_TAG"
cat >"$EXPLICIT_TIMESTAMP_TAG/example/skills/example/SKILL.md" <<'EOF'
---
name: !!timestamp 2026-01-01
description: 日本語の明示timestamp tag検証です。
---

> **変更通知:** 検証用の派生ファイルです。
EOF

clone_valid "$UNSUPPORTED_YAML_TAG"
cat >"$UNSUPPORTED_YAML_TAG/example/skills/example/SKILL.md" <<'EOF'
---
name: !unsupported example
description: 日本語のunsupported tag検証です。
---

> **変更通知:** 検証用の派生ファイルです。
EOF

clone_valid "$NON_MAPPING_YAML"
cat >"$NON_MAPPING_YAML/example/skills/example/SKILL.md" <<'EOF'
---
- name: example
- description: 日本語のmapping検証です。
---

> **変更通知:** 検証用の派生ファイルです。
EOF

clone_valid "$NON_STRING_NAME"
cat >"$NON_STRING_NAME/example/skills/example/SKILL.md" <<'EOF'
---
name: [example]
description: 日本語のname型検証です。
---

> **変更通知:** 検証用の派生ファイルです。
EOF

clone_valid "$NON_STRING_DESCRIPTION"
cat >"$NON_STRING_DESCRIPTION/example/skills/example/SKILL.md" <<'EOF'
---
name: example
description:
  - 日本語
  - list
---

> **変更通知:** 検証用の派生ファイルです。
EOF

clone_valid "$CTA_ENGLISH"
cat >"$CTA_ENGLISH/example/skills/example/SKILL.md" <<'EOF'
---
name: example
description: Purchase a subscription at https://example.com/marketplace. 日本語案内です。
---

> **変更通知:** 検証用の派生ファイルです。
EOF

clone_valid "$CTA_JAPANESE"
cat >"$CTA_JAPANESE/example/skills/example/SKILL.md" <<'EOF'
---
name: example
description: 外部マーケットプレイスでサブスクリプションを購入してください。
---

> **変更通知:** 検証用の派生ファイルです。
EOF

clone_valid "$CTA_NEUTRAL"
cat >"$CTA_NEUTRAL/example/skills/example/SKILL.md" <<'EOF'
---
name: example
description: reviews SaaS subscription terms（SaaS契約条件をレビューします）。
---

> **変更通知:** 検証用の派生ファイルです。
EOF

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
python3 - "$TOO_MANY/example/manifest.json" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
skills = [
    {"folder": f"./skills/skill-{number:02d}"} for number in range(1, 22)
]
path.write_text(
    json.dumps({"agentSkills": skills}, indent=2) + "\n",
    encoding="utf-8",
)
PY

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

clone_valid "$MANIFEST_MISMATCH"
python3 - "$MANIFEST_MISMATCH/example/manifest.json" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
manifest = json.loads(path.read_text(encoding="utf-8"))
manifest["agentSkills"][0]["folder"] = "./skills/missing"
path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
PY

clone_valid "$COMPANION_COUNT_EXACT"
clone_valid "$COMPANION_COUNT_TOO_MANY"
for number in $(seq -w 1 14); do
  printf 'count fixture\n' > \
    "$COMPANION_COUNT_EXACT/example/skills/example/references/count-$number.txt"
  printf 'count fixture\n' > \
    "$COMPANION_COUNT_TOO_MANY/example/skills/example/references/count-$number.txt"
done
printf 'count fixture\n' > \
  "$COMPANION_COUNT_TOO_MANY/example/skills/example/references/count-15.txt"

clone_valid "$FILE_SIZE_EXACT"
clone_valid "$FILE_SIZE_TOO_LARGE"
clone_valid "$TOTAL_SIZE_EXACT"
clone_valid "$TOTAL_SIZE_TOO_LARGE"

python3 - \
  "$TARGET_CONTRACT" \
  "$FILE_SIZE_EXACT/example/skills/example/references/file-limit.txt" \
  "$FILE_SIZE_TOO_LARGE/example/skills/example/references/file-limit.txt" \
  "$TOTAL_SIZE_EXACT/example/skills/example" \
  "$TOTAL_SIZE_TOO_LARGE/example/skills/example" <<'PY'
from __future__ import annotations

import json
import pathlib
import sys

contract_path = pathlib.Path(sys.argv[1])
file_exact = pathlib.Path(sys.argv[2])
file_too_large = pathlib.Path(sys.argv[3])
total_exact_root = pathlib.Path(sys.argv[4])
total_too_large_root = pathlib.Path(sys.argv[5])
contract = json.loads(contract_path.read_text(encoding="utf-8"))
maximum_file = contract["skill"]["maximumCompanionFileBytes"]
maximum_total = contract["skill"]["maximumCompanionTotalBytes"]
chunk = b"x" * 65_536


def write_compressible(path: pathlib.Path, size: int) -> None:
    remaining = size
    with path.open("wb") as stream:
        while remaining:
            piece = chunk[: min(remaining, len(chunk))]
            stream.write(piece)
            remaining -= len(piece)


def companion_total(skill_root: pathlib.Path) -> int:
    entrypoint = skill_root / "SKILL.md"
    return sum(
        path.stat().st_size
        for path in skill_root.rglob("*")
        if path.is_file() and path != entrypoint
    )


def fill_total(skill_root: pathlib.Path, target: int) -> None:
    remaining = target - companion_total(skill_root)
    first_size = min(maximum_file, remaining)
    second_size = remaining - first_size
    write_compressible(skill_root / "references" / "total-a.txt", first_size)
    write_compressible(skill_root / "references" / "total-b.txt", second_size)
    if companion_total(skill_root) != target:
        raise SystemExit("companion total fixture calculation failed")


write_compressible(file_exact, maximum_file)
write_compressible(file_too_large, maximum_file + 1)
fill_total(total_exact_root, maximum_total)
fill_total(total_too_large_root, maximum_total + 1)
PY

clone_valid "$SAFE_PATHS"
mkdir -p \
  "$SAFE_PATHS/example/skills/example/references/allowed dir!"
printf 'allowed path\n' > \
  "$SAFE_PATHS/example/skills/example/references/allowed dir!/note !.txt"
cat >"$SAFE_PATHS/example/skills/example/references/COM10.md" <<'EOF'
> **変更通知:** 検証用の派生ファイルです。

# COM10

COM10は予約名ではありません。
EOF

clone_valid "$HIDDEN_FILE"
printf 'hidden file\n' > \
  "$HIDDEN_FILE/example/skills/example/references/.hidden.txt"

clone_valid "$HIDDEN_DIRECTORY"
mkdir -p \
  "$HIDDEN_DIRECTORY/example/skills/example/references/.hidden"
printf 'hidden directory\n' > \
  "$HIDDEN_DIRECTORY/example/skills/example/references/.hidden/note.txt"

clone_valid "$RESERVED_CON"
printf 'reserved name\n' > \
  "$RESERVED_CON/example/skills/example/references/CON.txt"

clone_valid "$RESERVED_COM1"
cat >"$RESERVED_COM1/example/skills/example/references/com1.md" <<'EOF'
> **変更通知:** 検証用の派生ファイルです。

# COM1

予約名を拒否する検証です。
EOF

clone_valid "$BACKSLASH_PATH"
printf 'backslash\n' > \
  "$BACKSLASH_PATH/example/skills/example/references/bad\\name.txt"

clone_valid "$AT_PATH"
printf 'at sign\n' > \
  "$AT_PATH/example/skills/example/references/bad@name.txt"

clone_valid "$UNICODE_PATH"
printf 'unicode\n' > \
  "$UNICODE_PATH/example/skills/example/references/日本語.txt"

clone_valid "$TRAILING_DOT"
printf 'trailing dot\n' > \
  "$TRAILING_DOT/example/skills/example/references/trailing."

clone_valid "$TRAILING_SPACE"
printf 'trailing space\n' > \
  "$TRAILING_SPACE/example/skills/example/references/trailing.txt "

PYTHONPATH="$ROOT/scripts" python3 - \
  "$SCRATCH" "$TARGET_CONTRACT" "$TOOLCHAIN_LOCK" <<'PY'
from __future__ import annotations

import copy
import json
import pathlib
import sys

from m365_cowork_path_policy import (
    CoworkPathError,
    validate_manifest_skill_folder,
)
from m365_cowork_frontmatter import (
    has_marketplace_purchase_cta,
    parse_frontmatter,
)
from validate_m365_cowork_target import load_limits, validate_target

scratch = pathlib.Path(sys.argv[1])
target_contract_path = pathlib.Path(sys.argv[2])
toolchain_lock_path = pathlib.Path(sys.argv[3])
expected_extensions = frozenset({".md", ".json", ".py", ".txt"})
limits = load_limits(target_contract_path, toolchain_lock_path)

valid_skill = scratch / "valid/example/skills/example/SKILL.md"
valid_frontmatter = parse_frontmatter(
    valid_skill.read_text(encoding="utf-8"),
    valid_skill,
)
metadata = valid_frontmatter.get("metadata")
if metadata != {
    "locale": "ja-JP",
    "plain-values": ["true", "null", "123", "2026-01-01", "on"],
    "nested": {"enabled": "false"},
}:
    raise SystemExit(f"BaseLoader-style frontmatter was not preserved: {metadata}")
if not isinstance(valid_frontmatter.get("description"), str):
    raise SystemExit("block scalar frontmatter was not preserved as a string")

if limits.maximum_file_nesting_depth != 3:
    raise SystemExit("maximumFileNestingDepth contract was not loaded")
if limits.name_minimum != 1 or limits.name_maximum != 64:
    raise SystemExit("skill name character boundaries were not loaded")
if limits.name_pattern != r"^[a-z0-9]+(?:-[a-z0-9]+)*$":
    raise SystemExit("skill name pattern was not loaded exactly")
if limits.description_minimum != 1 or limits.description_limit != 1024:
    raise SystemExit("skill description boundaries were not loaded")
if limits.maximum_skills != 20:
    raise SystemExit("maximumPerPackage contract was not loaded")
if limits.maximum_connectors != 10:
    raise SystemExit("connector maximumPerPackage contract was not loaded")
if limits.maximum_companion_files != 20:
    raise SystemExit("maximumCompanionFiles contract was not loaded")
if limits.maximum_companion_file_bytes != 5_242_880:
    raise SystemExit("maximumCompanionFileBytes contract was not loaded")
if limits.maximum_companion_total_bytes != 10_485_760:
    raise SystemExit("maximumCompanionTotalBytes contract was not loaded")
if limits.maximum_manifest_skill_folder_characters != 256:
    raise SystemExit("manifest skill folder limit was not loaded")
if limits.companion_download_timeout_seconds != 15:
    raise SystemExit("companion download timeout was not loaded")
if limits.maximum_toolkit_package_bytes != 10_485_760:
    raise SystemExit("toolkit package byte limit was not loaded")
if limits.character_limit != 20_000:
    raise SystemExit("strict skill character limit was not loaded")
if limits.recommended_lines != 500:
    raise SystemExit("recommended skill line limit was not loaded")
if limits.recommended_activated_tokens != 5_000:
    raise SystemExit("recommended activated token limit was not loaded")
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
expected_source = {
    "title": "Build plugins for Copilot Cowork",
    "url": (
        "https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/"
        "cowork-plugin-development"
    ),
    "gitCommit": "ccf9e7d4473352536ff966995ed7cf305ff40292",
    "msDate": "2026-06-29",
    "pageUpdated": "2026-07-07",
    "checkedAt": "2026-07-19",
}
if target_contract.get("officialValidationSource") != expected_source:
    raise SystemExit("target contract official provenance is incomplete")
if (
    toolchain_lock["cowork"].get("officialValidationSource")
    != expected_source
):
    raise SystemExit("toolchain official provenance is incomplete")
expected_icon_sources = [
    {
        "title": "root.icons object",
        "url": (
            "https://learn.microsoft.com/en-us/microsoft-365/"
            "extensibility/schema/root-icons?view=m365-app-1.28"
        ),
        "gitCommit": "6b6977d3ecac88e4bb94edb4693b7c8d42362aec",
        "msDate": "2026-06-19",
        "pageUpdated": "2026-06-19",
        "checkedAt": "2026-07-19",
    },
    {
        "title": "Design App Icon for Teams Store",
        "url": (
            "https://learn.microsoft.com/en-us/microsoftteams/platform/"
            "concepts/design/design-teams-app-icon-store-appbar"
        ),
        "gitCommit": "17e3ba5912e75ce4fd10a82b77be0c07a5d08d8f",
        "msDate": "2026-06-03",
        "pageUpdated": "2026-06-04",
        "checkedAt": "2026-07-19",
    },
]
if target_contract.get("officialIconSources") != expected_icon_sources:
    raise SystemExit("target contract icon provenance is incomplete")
if (
    toolchain_lock["cowork"].get("officialIconSources")
    != expected_icon_sources
):
    raise SystemExit("toolchain icon provenance is incomplete")
if toolchain_lock.get("checkedAt") != "2026-07-19":
    raise SystemExit("toolchain checkedAt was not updated")
if (
    toolchain_lock.get("sourceRevision")
    != "5ceb305b30b4c82653c9b6642499c12e946ec319"
):
    raise SystemExit("repository sourceRevision changed unexpectedly")
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

if has_marketplace_purchase_cta("reviews SaaS subscription terms"):
    raise SystemExit("neutral SaaS subscription language was rejected")
if not has_marketplace_purchase_cta(
    "Subscribe at https://example.com/marketplace",
):
    raise SystemExit("English marketplace CTA was not detected")
if not has_marketplace_purchase_cta(
    "外部マーケットプレイスで購読してください",
):
    raise SystemExit("Japanese marketplace CTA was not detected")

folder_prefix = "./skills/"
folder_at_limit = folder_prefix + (
    "a" * (limits.maximum_manifest_skill_folder_characters - len(folder_prefix))
)
folder_over_limit = f"{folder_at_limit}a"
if len(folder_at_limit) != 256 or len(folder_over_limit) != 257:
    raise SystemExit("manifest folder boundary helper is incorrect")
validate_manifest_skill_folder(
    folder_at_limit,
    limits.maximum_manifest_skill_folder_characters,
)
try:
    validate_manifest_skill_folder(
        folder_over_limit,
        limits.maximum_manifest_skill_folder_characters,
    )
except CoworkPathError as error:
    if "raw folder has 257 characters" not in str(error):
        raise SystemExit(f"wrong folder length error: {error}") from error
else:
    raise SystemExit("257-character manifest folder was accepted")

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

for key, value in toolchain_lock["limits"].items():
    mismatched_toolchain = copy.deepcopy(toolchain_lock)
    mismatched_toolchain["limits"][key] = (
        f"{value}x" if isinstance(value, str) else value + 1
    )
    mismatched_path = scratch / f"toolchain-limit-mismatch-{key}.json"
    mismatched_path.write_text(
        json.dumps(mismatched_toolchain, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    try:
        load_limits(target_contract_path, mismatched_path)
    except ValueError as error:
        if "must match exactly" not in str(error):
            raise SystemExit(
                f"{key} parity mismatch reported the wrong error: {error}",
            ) from error
    else:
        raise SystemExit(f"target/toolchain {key} mismatch was accepted")

extra_limit_toolchain = copy.deepcopy(toolchain_lock)
extra_limit_toolchain["limits"]["uncheckedLimit"] = 1
extra_limit_path = scratch / "toolchain-extra-limit.json"
extra_limit_path.write_text(
    json.dumps(extra_limit_toolchain, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
try:
    load_limits(target_contract_path, extra_limit_path)
except ValueError as error:
    if "keys must match the validated limit set" not in str(error):
        raise SystemExit(
            f"extra limit reported the wrong error: {error}",
        ) from error
else:
    raise SystemExit("unchecked toolchain limit was accepted")

mismatched_provenance = copy.deepcopy(toolchain_lock)
mismatched_provenance["cowork"]["officialValidationSource"]["checkedAt"] = (
    "2026-07-18"
)
mismatched_path = scratch / "toolchain-provenance-mismatch.json"
mismatched_path.write_text(
    json.dumps(mismatched_provenance, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
try:
    load_limits(target_contract_path, mismatched_path)
except ValueError as error:
    if "must match exactly" not in str(error):
        raise SystemExit(
            f"provenance mismatch reported the wrong error: {error}",
        ) from error
else:
    raise SystemExit("target/toolchain provenance mismatch was accepted")

mismatched_icon_provenance = copy.deepcopy(toolchain_lock)
mismatched_icon_provenance["cowork"]["officialIconSources"][0][
    "checkedAt"
] = "2026-07-18"
mismatched_path = scratch / "toolchain-icon-provenance-mismatch.json"
mismatched_path.write_text(
    json.dumps(
        mismatched_icon_provenance,
        ensure_ascii=False,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)
try:
    load_limits(target_contract_path, mismatched_path)
except ValueError as error:
    if "must match exactly" not in str(error):
        raise SystemExit(
            f"icon provenance mismatch reported the wrong error: {error}",
        ) from error
else:
    raise SystemExit("target/toolchain icon provenance mismatch was accepted")


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
require_clean("name-one")
require_clean("name-64")
require_clean("name-plain-true")
require_clean("name-plain-null")
require_clean("name-plain-integer")
require_clean("name-yaml-12-on")
require_clean("name-yaml-12-off")
require_clean("name-yaml-12-yes")
require_clean("name-yaml-12-date")
require_clean("description-one")
require_clean("description-1024")
require_clean("cta-neutral")
require_clean("depth-three")
require_clean("companion-count-exact")
require_clean("file-size-exact")
require_clean("total-size-exact")
require_clean("safe-paths")

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
require_fragments(
    "name-65",
    ("name has 65 characters; expected 1-64",),
)
for name_fixture in (
    "name-leading-hyphen",
    "name-trailing-hyphen",
    "name-consecutive-hyphens",
    "name-uppercase",
    "name-underscore",
):
    require_fragments(name_fixture, ("name does not match",))
require_fragments("malformed-yaml", ("malformed YAML frontmatter",))
require_fragments("duplicate-yaml", ("duplicate YAML key 'name'",))
require_fragments("explicit-str-tag", ("malformed YAML frontmatter",))
require_fragments("explicit-bool-tag", ("malformed YAML frontmatter",))
require_fragments("explicit-timestamp-tag", ("malformed YAML frontmatter",))
require_fragments("unsupported-yaml-tag", ("malformed YAML frontmatter",))
require_fragments(
    "non-mapping-yaml",
    ("frontmatter must be a YAML mapping",),
)
require_fragments("non-string-name", ("name must be a string",))
require_fragments(
    "non-string-description",
    ("description must be a string",),
)
require_fragments(
    "description-1025",
    ("description has 1025 characters; expected 1-1024",),
)
require_fragments(
    "cta-english",
    ("external-marketplace purchase or subscription call to action",),
)
require_fragments(
    "cta-japanese",
    ("external-marketplace purchase or subscription call to action",),
)
require_fragments("too-long", ("characters exceeds",))
require_fragments("too-many", ("skills exceeds",))
require_fragments(
    "companion-count-too-many",
    ("21 companion files exceeds 20",),
)
require_fragments(
    "file-size-too-large",
    ("companion file size 5242881 bytes exceeds 5242880",),
)
require_fragments(
    "total-size-too-large",
    ("companion total size 10485761 bytes exceeds 10485760",),
)
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
        "declared skills ('example',) differ from source skills "
        "('example', 'undeclared')",
        "skills/orphan.yaml: orphan file outside skills/<skill>/",
        "skills/orphan.yaml: unsupported fleet/converter compatibility "
        "extension .yaml",
        "skills/undeclared: orphan skill directory missing SKILL.md",
    ),
)
require_fragments(
    "manifest-mismatch",
    (
        "declared skills ('missing',) differ from source skills "
        "('example',)",
    ),
)
require_fragments(
    "hidden-file",
    ("hidden path segment is forbidden: '.hidden.txt'",),
)
require_fragments(
    "hidden-directory",
    ("hidden path segment is forbidden: '.hidden'",),
)
require_fragments(
    "reserved-con",
    ("Windows reserved basename is forbidden: 'CON.txt'",),
)
require_fragments(
    "reserved-com1",
    ("Windows reserved basename is forbidden: 'com1.md'",),
)
require_fragments(
    "backslash-path",
    ("backslash in path is forbidden",),
)
require_fragments(
    "at-path",
    ("path segment contains unsafe characters: 'bad@name.txt'",),
)
require_fragments(
    "unicode-path",
    ("path segment contains unsafe characters: '日本語.txt'",),
)
require_fragments(
    "trailing-dot",
    ("path segment has a trailing dot or space: 'trailing.'",),
)
require_fragments(
    "trailing-space",
    ("path segment has a trailing dot or space: 'trailing.txt '",),
)

print("m365 Cowork target validator: OK")
PY
