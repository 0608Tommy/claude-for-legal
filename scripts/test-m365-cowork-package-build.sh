#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Test deterministic Cowork ZIP normalization and its Python quality gates.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M365_ROOT="$ROOT/m365-cowork-ja"
SOURCE="$M365_ROOT/cowork-packages/legal-clinic"
SCRATCH="$M365_ROOT/.cache/package-build-test.${BASHPID:-$$}"
PYTHON_FILES=(
  "$ROOT/scripts/normalize_m365_cowork_package.py"
  "$ROOT/scripts/validate_m365_cowork_icons.py"
  "$ROOT/scripts/validate_m365_cowork_target.py"
)

for tool in bandit flake8 mypy pydocstyle pylint pyright radon ruff \
  vulture; do
  command -v "$tool" >/dev/null || {
    echo "requires $tool" >&2
    exit 2
  }
done

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT/scripts"
export TMPDIR="$SCRATCH/tmp"

cleanup() {
  rm -rf "$SCRATCH"
}
trap cleanup EXIT HUP INT TERM

mkdir -p "$TMPDIR"

ruff check --select ALL "${PYTHON_FILES[@]}"
flake8 "${PYTHON_FILES[@]}"
mypy --strict "${PYTHON_FILES[@]}"
pylint --fail-under=10 "${PYTHON_FILES[@]}"
bandit -q "${PYTHON_FILES[@]}"
pydocstyle --convention=numpy "${PYTHON_FILES[@]}"
vulture "${PYTHON_FILES[@]}"
complexity="$(radon cc -s -n B "${PYTHON_FILES[@]}")"
[[ -z "$complexity" ]] || {
  echo "radon requires complexity grade A:" >&2
  echo "$complexity" >&2
  exit 1
}
pyright --project "$ROOT/scripts/pyrightconfig.m365-build.json"

python3 - "$SCRATCH" "$SOURCE" <<'PY'
from __future__ import annotations

import json
import shutil
import stat
import sys
import warnings
import zipfile
from pathlib import Path

from normalize_m365_cowork_package import (
    CANONICAL_LEGAL_FILES,
    DOS_EPOCH,
    DISTRIBUTED_LEGAL_FILES,
    FIXED_EXTERNAL_ATTR,
    PackageBuildError,
    normalize_package,
)

scratch = Path(sys.argv[1])
source_template = Path(sys.argv[2])
source = scratch / "fixture-source"
shutil.copytree(source_template, source)
canonical_legal = {
    name: (source / name).read_bytes() for name in CANONICAL_LEGAL_FILES
}
for skill_dir in sorted((source / "skills").iterdir()):
    for distributed_name, canonical_name in DISTRIBUTED_LEGAL_FILES:
        (skill_dir / canonical_name).unlink(missing_ok=True)
        (skill_dir / distributed_name).write_bytes(
            canonical_legal[canonical_name],
        )


def source_members() -> dict[str, bytes]:
    manifest = json.loads(
        (source / "manifest.json").read_text(encoding="utf-8"),
    )
    names = {
        "manifest.json",
        manifest["icons"]["color"],
        manifest["icons"]["outline"],
    }
    names.update(
        path.relative_to(source).as_posix()
        for path in (source / "skills").rglob("*")
        if path.is_file()
    )
    return {name: (source / name).read_bytes() for name in names}


def info(
    name: str,
    *,
    timestamp: tuple[int, int, int, int, int, int],
    symlink: bool = False,
) -> zipfile.ZipInfo:
    value = zipfile.ZipInfo(name, date_time=timestamp)
    value.create_system = 3
    mode = stat.S_IFLNK | 0o777 if symlink else stat.S_IFREG | 0o600
    value.external_attr = mode << 16
    value.compress_type = zipfile.ZIP_DEFLATED
    value.extra = b"\xfe\xca\x00\x00"
    value.comment = b"raw-member-comment"
    return value


def write_archive(
    path: Path,
    members: list[tuple[str, bytes, bool]],
    *,
    reverse: bool = False,
) -> None:
    ordered = list(reversed(members)) if reverse else members
    timestamp = (2026, 7, 17, 1, 2, 4) if reverse else (2025, 1, 2, 3, 4, 6)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(
            path,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=1 if reverse else 6,
        ) as archive:
            archive.comment = b"raw-archive-comment"
            for name, data, symlink in ordered:
                archive.writestr(
                    info(name, timestamp=timestamp, symlink=symlink),
                    data,
                )


def expect_failure(
    label: str,
    members: list[tuple[str, bytes, bool]],
    fragment: str,
) -> None:
    raw = scratch / f"{label}.zip"
    output = scratch / f"{label}.normalized.zip"
    write_archive(raw, members)
    try:
        normalize_package(raw, output, source)
    except PackageBuildError as error:
        if fragment not in str(error):
            raise AssertionError(
                f"{label}: expected {fragment!r}, got {error!s}",
            ) from error
    else:
        raise AssertionError(f"{label}: unsafe archive was accepted")


base = source_members()
base_members = [(name, data, False) for name, data in base.items()]
skill_name = next(
    name for name in sorted(base) if name.endswith("/SKILL.md")
)
license_name = next(
    name for name in sorted(base) if name.endswith("/LICENSE.txt")
)
notice_name = next(
    name for name in sorted(base) if name.endswith("/NOTICE.txt")
)
license_names = sorted(
    name for name in base if name.endswith("/LICENSE.txt")
)
notice_names = sorted(
    name for name in base if name.endswith("/NOTICE.txt")
)
raw_one = scratch / "raw-one.zip"
raw_two = scratch / "raw-two.zip"
normalized_one = scratch / "normalized-one.zip"
normalized_two = scratch / "normalized-two.zip"
normalized_three = scratch / "normalized-three.zip"
write_archive(raw_one, base_members)
write_archive(raw_two, base_members, reverse=True)

digest_one = normalize_package(raw_one, normalized_one, source)
digest_two = normalize_package(raw_two, normalized_two, source)
if digest_one != digest_two:
    raise AssertionError("normalized digests differ")
if normalized_one.read_bytes() != normalized_two.read_bytes():
    raise AssertionError("normalized ZIP bytes differ")
digest_three = normalize_package(normalized_one, normalized_three, source)
if digest_three != digest_one:
    raise AssertionError("normalized ZIP contract is not digest-idempotent")
if normalized_three.read_bytes() != normalized_one.read_bytes():
    raise AssertionError("normalized ZIP contract is not byte-idempotent")

with zipfile.ZipFile(normalized_one) as archive:
    infos = archive.infolist()
    archive_names = [item.filename for item in infos]
    if archive_names != sorted(base):
        raise AssertionError("normalized members are not sorted")
    if any(name in archive_names for name in CANONICAL_LEGAL_FILES):
        raise AssertionError("package-root canonical legal file was archived")
    if any(
        name.endswith(("/LICENSE", "/NOTICE")) for name in archive_names
    ):
        raise AssertionError("legacy extensionless legal member was archived")
    if archive.comment:
        raise AssertionError("normalized archive comment remains")
    for item in infos:
        if item.date_time != DOS_EPOCH:
            raise AssertionError(f"timestamp remains on {item.filename}")
        if item.external_attr != FIXED_EXTERNAL_ATTR:
            raise AssertionError(f"permissions differ on {item.filename}")
        if item.compress_type != zipfile.ZIP_DEFLATED:
            raise AssertionError(f"compression differs on {item.filename}")
        if item.extra or item.comment:
            raise AssertionError(f"metadata remains on {item.filename}")
        if archive.read(item) != base[item.filename]:
            raise AssertionError(f"member bytes changed: {item.filename}")
    for name in license_names:
        if archive.read(name) != canonical_legal["LICENSE"]:
            raise AssertionError(f"license bytes differ: {name}")
    for name in notice_names:
        if archive.read(name) != canonical_legal["NOTICE"]:
            raise AssertionError(f"notice bytes differ: {name}")

color_name = "color.png"
manifest_name = "manifest.json"

expect_failure(
    "duplicate",
    [*base_members, (manifest_name, base[manifest_name], False)],
    "duplicate ZIP member",
)
expect_failure(
    "case-collision",
    [*base_members, ("Color.png", base[color_name], False)],
    "case-colliding ZIP member",
)
expect_failure(
    "traversal",
    [*base_members, ("../escape", b"x", False)],
    "unsafe ZIP member path",
)
expect_failure(
    "windows-drive",
    [*base_members, ("C:/escape", b"x", False)],
    "unsafe ZIP member path",
)
expect_failure(
    "symlink",
    [*base_members, ("link", b"target", True)],
    "symlink member",
)
expect_failure(
    "connector-draft",
    [*base_members, ("connectors.draft.json", b"{}", False)],
    "connector draft",
)

missing_license = [
    member for member in base_members if member[0] != license_name
]
expect_failure(
    "missing-license",
    missing_license,
    f"required archived file missing or empty: {license_name}",
)
missing_notice = [
    member for member in base_members if member[0] != notice_name
]
expect_failure(
    "missing-notice",
    missing_notice,
    f"required archived file missing or empty: {notice_name}",
)

changed_license = [
    (
        name,
        data + b"\nchanged" if name == license_name else data,
        symlink,
    )
    for name, data, symlink in base_members
]
expect_failure(
    "changed-license",
    changed_license,
    "archived legal file differs from package-root LICENSE",
)
changed_notice = [
    (
        name,
        data + b"\nchanged" if name == notice_name else data,
        symlink,
    )
    for name, data, symlink in base_members
]
expect_failure(
    "changed-notice",
    changed_notice,
    "archived legal file differs from package-root NOTICE",
)

legacy_license_name = license_name.removesuffix(".txt")
expect_failure(
    "legacy-legal-member",
    [
        *base_members,
        (legacy_license_name, canonical_legal["LICENSE"], False),
    ],
    "legacy extensionless legal member",
)
expect_failure(
    "unsupported-extension",
    [
        *base_members,
        (f"{legacy_license_name}.md", canonical_legal["LICENSE"], False),
    ],
    "unsupported legal-file extension",
)
expect_failure(
    "legal-case-collision",
    [
        *base_members,
        (f"{legacy_license_name}.TXT", canonical_legal["LICENSE"], False),
    ],
    "case-colliding ZIP member",
)

changed_manifest = json.loads(base[manifest_name])
changed_manifest["version"] = "9.9.9"
changed_manifest_bytes = json.dumps(changed_manifest).encode()
semantic_members = [
    (
        name,
        changed_manifest_bytes if name == manifest_name else data,
        symlink,
    )
    for name, data, symlink in base_members
]
expect_failure(
    "semantic-manifest",
    semantic_members,
    "differs semantically",
)

changed_skill = [
    (
        name,
        data + b"\nchanged" if name == skill_name else data,
        symlink,
    )
    for name, data, symlink in base_members
]
expect_failure("changed-skill", changed_skill, "skill bytes changed")

print("m365 Cowork deterministic package normalizer: OK")
PY
