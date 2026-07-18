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
  "$ROOT/scripts/m365_cowork_path_policy.py"
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
export PYLINTHOME="$SCRATCH/pylint"
export TMPDIR="$SCRATCH/tmp"

cleanup() {
  rm -rf "$SCRATCH"
}
trap cleanup EXIT HUP INT TERM

mkdir -p "$TMPDIR"

ruff check --no-cache --select ALL "${PYTHON_FILES[@]}"
flake8 "${PYTHON_FILES[@]}"
mypy --strict --cache-dir "$SCRATCH/mypy" "${PYTHON_FILES[@]}"
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
maintainability="$(radon mi -s -n B "${PYTHON_FILES[@]}")"
[[ -z "$maintainability" ]] || {
  echo "radon requires maintainability grade A:" >&2
  echo "$maintainability" >&2
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
from validate_m365_cowork_target import load_limits

scratch = Path(sys.argv[1])
source_template = Path(sys.argv[2])
source = scratch / "fixture-source"
shutil.copytree(source_template, source)


def canonicalize_legal(source_root: Path) -> dict[str, bytes]:
    legal = {
        name: (source_root / name).read_bytes()
        for name in CANONICAL_LEGAL_FILES
    }
    for skill_dir in sorted((source_root / "skills").iterdir()):
        for distributed_name, canonical_name in DISTRIBUTED_LEGAL_FILES:
            (skill_dir / canonical_name).unlink(missing_ok=True)
            (skill_dir / distributed_name).write_bytes(
                legal[canonical_name],
            )
    return legal


canonical_legal = canonicalize_legal(source)
limits = load_limits()


def source_members(source_root: Path = source) -> dict[str, bytes]:
    manifest = json.loads(
        (source_root / "manifest.json").read_text(encoding="utf-8"),
    )
    names = {
        "manifest.json",
        manifest["icons"]["color"],
        manifest["icons"]["outline"],
    }
    names.update(
        path.relative_to(source_root).as_posix()
        for path in (source_root / "skills").rglob("*")
        if path.is_file()
    )
    return {name: (source_root / name).read_bytes() for name in names}


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


def write_raw_nul_archive(
    path: Path,
    members: list[tuple[str, bytes, bool]],
    raw_name: str,
) -> None:
    placeholder = raw_name.replace("\0", "X")
    if placeholder == raw_name:
        raise AssertionError("raw NUL fixture requires a NUL byte")
    write_archive(path, [*members, (placeholder, b"raw-nul", False)])
    archive_bytes = path.read_bytes()
    placeholder_bytes = placeholder.encode("ascii")
    raw_name_bytes = raw_name.encode("ascii")
    if archive_bytes.count(placeholder_bytes) != 2:
        raise AssertionError("raw NUL fixture did not find both ZIP headers")
    path.write_bytes(archive_bytes.replace(placeholder_bytes, raw_name_bytes))


def expect_failure(
    label: str,
    members: list[tuple[str, bytes, bool]],
    fragment: str,
    source_root: Path = source,
) -> None:
    raw = scratch / f"{label}.zip"
    output = scratch / f"{label}.normalized.zip"
    write_archive(raw, members)
    expect_archive_failure(label, raw, output, source_root, fragment)


def expect_archive_failure(
    label: str,
    raw: Path,
    output: Path,
    source_root: Path,
    fragment: str,
) -> None:
    try:
        normalize_package(raw, output, source_root)
    except PackageBuildError as error:
        if fragment not in str(error):
            raise AssertionError(
                f"{label}: expected {fragment!r}, got {error!s}",
            ) from error
    else:
        raise AssertionError(f"{label}: unsafe archive was accepted")


def expect_success(
    label: str,
    source_root: Path,
    members: list[tuple[str, bytes, bool]],
) -> None:
    raw = scratch / f"{label}.zip"
    output = scratch / f"{label}.normalized.zip"
    write_archive(raw, members)
    try:
        normalize_package(raw, output, source_root)
    except PackageBuildError as error:
        raise AssertionError(f"{label}: valid archive failed: {error}") from error


def clone_source(label: str) -> Path:
    destination = scratch / f"{label}-source"
    shutil.copytree(source, destination)
    return destination


def members_for(source_root: Path) -> list[tuple[str, bytes, bool]]:
    return [
        (name, data, False)
        for name, data in source_members(source_root).items()
    ]


COMPRESSIBLE_CHUNK = b"x" * 65_536


def write_compressible(path: Path, size: int) -> None:
    remaining = size
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as stream:
        while remaining:
            piece = COMPRESSIBLE_CHUNK[: min(remaining, len(COMPRESSIBLE_CHUNK))]
            stream.write(piece)
            remaining -= len(piece)


def companion_paths(source_root: Path, slug: str) -> list[Path]:
    skill_root = source_root / "skills" / slug
    entrypoint = skill_root / "SKILL.md"
    return [
        path
        for path in skill_root.rglob("*")
        if path.is_file() and path != entrypoint
    ]


def companion_total(source_root: Path, slug: str) -> int:
    return sum(path.stat().st_size for path in companion_paths(source_root, slug))


def fill_companion_total(
    source_root: Path,
    slug: str,
    target: int,
) -> tuple[Path, Path]:
    remaining = target - companion_total(source_root, slug)
    first_size = min(limits.maximum_companion_file_bytes, remaining)
    second_size = remaining - first_size
    references = source_root / "skills" / slug / "references"
    references.mkdir(parents=True, exist_ok=True)
    first = references / "total-a.txt"
    second = references / "total-b.txt"
    write_compressible(first, first_size)
    write_compressible(second, second_size)
    if companion_total(source_root, slug) != target:
        raise AssertionError("companion total fixture calculation failed")
    return first, second


def fill_companion_count(source_root: Path, slug: str, target: int) -> None:
    current = len(companion_paths(source_root, slug))
    if current > target:
        raise AssertionError("source already exceeds companion fixture target")
    references = source_root / "skills" / slug / "references"
    references.mkdir(parents=True, exist_ok=True)
    for number in range(target - current):
        (references / f"count-{number:02d}.txt").write_bytes(b"count")


def replace_member_data(
    members: list[tuple[str, bytes, bool]],
    target_name: str,
    replacement: bytes,
) -> list[tuple[str, bytes, bool]]:
    return [
        (
            name,
            replacement if name == target_name else data,
            symlink,
        )
        for name, data, symlink in members
    ]


def single_skill_source(
    label: str,
    template_slug: str,
    replacement_slug: str,
) -> Path:
    source_root = clone_source(label)
    skills_root = source_root / "skills"
    shutil.copytree(
        skills_root / template_slug,
        skills_root / replacement_slug,
    )
    for child in sorted(skills_root.iterdir()):
        if child.name != replacement_slug:
            shutil.rmtree(child)
    manifest_path = source_root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["agentSkills"] = [
        {"folder": f"./skills/{replacement_slug}"},
    ]
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return source_root


base = source_members()
base_members = [(name, data, False) for name, data in base.items()]
skill_name = next(
    name for name in sorted(base) if name.endswith("/SKILL.md")
)
skill_slug = skill_name.split("/")[1]
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
    "hidden-file",
    [
        *base_members,
        (f"skills/{skill_slug}/references/.hidden.txt", b"x", False),
    ],
    "hidden path segment is forbidden",
)
expect_failure(
    "hidden-directory",
    [
        *base_members,
        (f"skills/{skill_slug}/references/.hidden/note.txt", b"x", False),
    ],
    "hidden path segment is forbidden",
)
expect_failure(
    "reserved-con",
    [
        *base_members,
        (f"skills/{skill_slug}/references/CON.txt", b"x", False),
    ],
    "Windows reserved basename is forbidden",
)
expect_failure(
    "reserved-com1",
    [
        *base_members,
        (f"skills/{skill_slug}/references/com1.md", b"x", False),
    ],
    "Windows reserved basename is forbidden",
)
expect_failure(
    "backslash",
    [
        *base_members,
        (f"skills/{skill_slug}/references/bad\\name.txt", b"x", False),
    ],
    "backslash in path is forbidden",
)
expect_failure(
    "at-sign",
    [
        *base_members,
        (f"skills/{skill_slug}/references/bad@name.txt", b"x", False),
    ],
    "path segment contains unsafe characters",
)
expect_failure(
    "unicode",
    [
        *base_members,
        (f"skills/{skill_slug}/references/日本語.txt", b"x", False),
    ],
    "path segment contains unsafe characters",
)
expect_failure(
    "trailing-dot",
    [
        *base_members,
        (f"skills/{skill_slug}/references/trailing.", b"x", False),
    ],
    "path segment has a trailing dot or space",
)
expect_failure(
    "trailing-space",
    [
        *base_members,
        (f"skills/{skill_slug}/references/trailing.txt ", b"x", False),
    ],
    "path segment has a trailing dot or space",
)

safe_source = clone_source("safe-paths")
safe_root = safe_source / "skills" / skill_slug / "references" / "allowed dir!"
safe_root.mkdir(parents=True)
(safe_root / "note !.txt").write_bytes(b"safe path")
(safe_root / "COM10.md").write_bytes(b"COM10 is not reserved")
expect_success("safe-paths", safe_source, members_for(safe_source))

raw_nul = scratch / "raw-nul.zip"
raw_nul_output = scratch / "raw-nul.normalized.zip"
raw_nul_name = f"skills/{skill_slug}/references/raw-nul\0.txt"
write_raw_nul_archive(raw_nul, base_members, raw_nul_name)
expect_archive_failure(
    "raw-nul",
    raw_nul,
    raw_nul_output,
    source,
    "control character in path is forbidden",
)

source_hidden = clone_source("source-hidden")
(
    source_hidden
    / "skills"
    / skill_slug
    / "references"
    / ".hidden.txt"
).write_bytes(b"hidden")
expect_failure(
    "source-hidden",
    base_members,
    "unsafe source path",
    source_hidden,
)

count_source = clone_source("companion-count")
fill_companion_count(
    count_source,
    skill_slug,
    limits.maximum_companion_files,
)
count_members = members_for(count_source)
expect_success("companion-count-exact", count_source, count_members)
expect_failure(
    "companion-count-too-many",
    [
        *count_members,
        (
            f"skills/{skill_slug}/references/count-over.txt",
            b"count",
            False,
        ),
    ],
    (
        f"archive skill {skill_slug!r}: 21 companion files exceeds 20"
    ),
    count_source,
)

file_source = clone_source("companion-file-size")
file_path = (
    file_source
    / "skills"
    / skill_slug
    / "references"
    / "file-limit.txt"
)
write_compressible(file_path, limits.maximum_companion_file_bytes)
file_members = members_for(file_source)
expect_success("companion-file-size-exact", file_source, file_members)
file_name = file_path.relative_to(file_source).as_posix()
file_data = source_members(file_source)[file_name]
expect_failure(
    "companion-file-size-too-large",
    replace_member_data(file_members, file_name, file_data + b"x"),
    "companion file size 5242881 bytes exceeds 5242880",
    file_source,
)

source_file_too_large = clone_source("source-file-too-large")
write_compressible(
    source_file_too_large
    / "skills"
    / skill_slug
    / "references"
    / "file-limit.txt",
    limits.maximum_companion_file_bytes + 1,
)
expect_failure(
    "source-file-too-large",
    base_members,
    "companion file size 5242881 bytes exceeds 5242880",
    source_file_too_large,
)

total_source = clone_source("companion-total")
_, total_second = fill_companion_total(
    total_source,
    skill_slug,
    limits.maximum_companion_total_bytes,
)
total_members = members_for(total_source)
expect_success("companion-total-exact", total_source, total_members)
total_second_name = total_second.relative_to(total_source).as_posix()
total_second_data = source_members(total_source)[total_second_name]
expect_failure(
    "companion-total-too-large",
    replace_member_data(
        total_members,
        total_second_name,
        total_second_data + b"x",
    ),
    (
        f"archive skill {skill_slug!r}: companion total size "
        "10485761 bytes exceeds 10485760"
    ),
    total_source,
)

source_total_too_large = clone_source("source-total-too-large")
fill_companion_total(
    source_total_too_large,
    skill_slug,
    limits.maximum_companion_total_bytes + 1,
)
expect_failure(
    "source-total-too-large",
    base_members,
    (
        f"source skill {skill_slug!r}: companion total size "
        "10485761 bytes exceeds 10485760"
    ),
    source_total_too_large,
)

folder_prefix = "./skills/"
slug_at_limit = "a" * (
    limits.maximum_manifest_skill_folder_characters - len(folder_prefix)
)
slug_over_limit = f"{slug_at_limit}a"
folder_source_at_limit = single_skill_source(
    "folder-at-limit",
    skill_slug,
    slug_at_limit,
)
expect_success(
    "folder-at-limit",
    folder_source_at_limit,
    members_for(folder_source_at_limit),
)
folder_source_over_limit = single_skill_source(
    "folder-over-limit",
    skill_slug,
    slug_over_limit,
)
expect_failure(
    "folder-over-limit",
    members_for(folder_source_over_limit),
    "raw folder has 257 characters",
    folder_source_over_limit,
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
