#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Test the strict canonical-to-skill reference projection gate.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M365_ROOT="$ROOT/m365-cowork-ja"
PACKAGE_ROOT="$M365_ROOT/cowork-packages"
CONTRACT="$M365_ROOT/shared/reference-projection-contract.json"
VALIDATOR="$ROOT/scripts/validate_m365_reference_projection.py"
PYTHON_FILES=(
  "$ROOT/scripts/m365_reference_contract.py"
  "$ROOT/scripts/m365_reference_common_projection.py"
  "$ROOT/scripts/m365_reference_projection.py"
  "$ROOT/scripts/m365_reference_projection_types.py"
  "$VALIDATOR"
)
SCRATCH="$M365_ROOT/.cache/reference-projection-test.${BASHPID:-$$}"
MODE="${1:-}"

if [[ -n "$MODE" && "$MODE" != "--fixtures-only" ]]; then
  echo "usage: $0 [--fixtures-only]" >&2
  exit 2
fi

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
pyright --project \
  "$ROOT/scripts/pyrightconfig.m365-reference-projection.json"

python3 - "$SCRATCH" "$CONTRACT" "$PACKAGE_ROOT" <<'PY'
from __future__ import annotations

import json
import shutil
import sys
from collections.abc import Callable
from pathlib import Path, PurePosixPath

from m365_reference_projection import (
    load_contract,
    validate_projection,
)
from m365_reference_projection_types import (
    ProjectionContract,
    ProjectionError,
)

scratch = Path(sys.argv[1])
contract_path = Path(sys.argv[2])
source_root = Path(sys.argv[3])
valid_root = scratch / "valid"
contract = load_contract(contract_path)
package_map = {package.name: package for package in contract.packages}
transform_map = {
    (transform.package, transform.path): transform
    for transform in contract.transforms
}


def canonical_data(package: str, path: PurePosixPath) -> bytes:
    return (
        source_root
        / package
        / Path(*contract.canonical_root.parts)
        / Path(*path.parts)
    ).read_bytes()


def local_data(
    package: str,
    path: PurePosixPath,
    data: bytes,
) -> bytes:
    transform = transform_map.get((package, path))
    if transform is None:
        return data
    return data.replace(transform.source, transform.replacement)


def build_common_fixture(root: Path, rules: ProjectionContract) -> None:
    common = rules.common_projection
    for transform in common.transforms:
        source = (
            source_root
            / transform.package
            / Path(*common.canonical_root.parts)
            / Path(*transform.path.parts)
        ).read_bytes()
        canonical = (
            root
            / transform.package
            / Path(*common.canonical_root.parts)
            / Path(*transform.path.parts)
        )
        canonical.parent.mkdir(parents=True, exist_ok=True)
        canonical.write_bytes(source)
        expected = source.replace(
            transform.source,
            transform.replacement,
        )
        package = package_map[transform.package]
        for skill in package.registered_skills:
            local = (
                root
                / transform.package
                / "skills"
                / skill
                / Path(*common.local_root.parts)
                / Path(*transform.path.parts)
            )
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_bytes(expected)


def build_fixture(root: Path, rules: ProjectionContract) -> None:
    for package in rules.packages:
        package_dir = root / package.name
        manifest = {
            "agentSkills": [
                {"folder": f"./skills/{skill}"}
                for skill in package.registered_skills
            ],
        }
        package_dir.mkdir(parents=True)
        (package_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )
        canonical_root = package_dir.joinpath(*rules.canonical_root.parts)
        for path in package.canonical_files:
            data = canonical_data(package.name, path)
            canonical_path = canonical_root.joinpath(*path.parts)
            canonical_path.parent.mkdir(parents=True, exist_ok=True)
            canonical_path.write_bytes(data)
        for skill in package.registered_skills:
            skill_dir = package_dir / "skills" / skill
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                f"# {skill}\n",
                encoding="utf-8",
            )
            local_root = skill_dir.joinpath(*rules.local_root.parts)
            for path in package.canonical_files:
                data = canonical_data(package.name, path)
                local_path = local_root.joinpath(*path.parts)
                local_path.parent.mkdir(parents=True, exist_ok=True)
                local_path.write_bytes(local_data(package.name, path, data))
    build_common_fixture(root, rules)


def require_fragments(
    label: str,
    root: Path,
    fragments: tuple[str, ...],
) -> None:
    errors = validate_projection(root, contract).errors
    if not errors:
        raise AssertionError(f"{label}: invalid fixture passed")
    for fragment in fragments:
        if not any(fragment in error for error in errors):
            raise AssertionError(
                f"{label}: missing {fragment!r} in {errors}",
            )


def invalid_fixture(
    label: str,
    mutate: Callable[[Path], None],
    fragments: tuple[str, ...],
) -> None:
    root = scratch / label
    shutil.copytree(valid_root, root)
    mutate(root)
    require_fragments(label, root, fragments)
    shutil.rmtree(root)


def first_local(root: Path) -> Path:
    package = contract.packages[0]
    skill = package.registered_skills[0]
    path = package.canonical_files[0]
    return (
        root
        / package.name
        / "skills"
        / skill
        / Path(*contract.local_root.parts)
        / Path(*path.parts)
    )


def first_common_paths(root: Path) -> tuple[Path, Path]:
    transform = contract.common_projection.transforms[0]
    package = package_map[transform.package]
    canonical = (
        root
        / transform.package
        / Path(*contract.common_projection.canonical_root.parts)
        / Path(*transform.path.parts)
    )
    local = (
        root
        / transform.package
        / "skills"
        / package.registered_skills[0]
        / Path(*contract.common_projection.local_root.parts)
        / Path(*transform.path.parts)
    )
    return canonical, local


build_fixture(valid_root, contract)
valid_report = validate_projection(valid_root, contract)
if valid_report.errors:
    raise AssertionError(f"valid fixture failed: {valid_report.errors}")
if valid_report.observed_totals != contract.expected_totals:
    raise AssertionError(
        "valid fixture totals changed: "
        f"{valid_report.observed_totals}",
    )

invalid_fixture(
    "missing-local",
    lambda root: first_local(root).unlink(),
    ("file set mismatch", "observed projection totals mismatch"),
)
invalid_fixture(
    "changed-local",
    lambda root: first_local(root).write_bytes(b"changed\n"),
    ("SHA-256 mismatch", "projected bytes differ"),
)


def remove_common_copy(root: Path) -> None:
    _, local = first_common_paths(root)
    local.unlink()


invalid_fixture(
    "missing-common-transform",
    remove_common_copy,
    (
        "common transformed copy is missing",
        "common transformed copy total mismatch",
    ),
)


def write_stale_common_copy(root: Path) -> None:
    canonical, local = first_common_paths(root)
    local.write_bytes(canonical.read_bytes())


invalid_fixture(
    "wrong-common-transform",
    write_stale_common_copy,
    (
        "stale canonical path remains",
        "SHA-256 mismatch",
        "projected bytes differ",
    ),
)


def remove_common_canonical(root: Path) -> None:
    canonical, _ = first_common_paths(root)
    canonical.unlink()


invalid_fixture(
    "missing-common-canonical",
    remove_common_canonical,
    (
        "canonical common file is missing",
        "common transformed copy total mismatch",
    ),
)


def add_legacy(root: Path) -> None:
    package = contract.packages[0]
    skill = package.registered_skills[0]
    legacy = (
        root
        / package.name
        / "skills"
        / skill
        / Path(*contract.forbidden_local_root.parts)
    )
    legacy.mkdir(parents=True)


invalid_fixture(
    "legacy-root",
    add_legacy,
    ("forbidden legacy root exists",),
)


def add_unconfigured_legacy(root: Path) -> None:
    legacy = (
        root
        / "unconfigured-package"
        / "skills"
        / "unregistered"
        / Path(*contract.forbidden_local_root.parts)
    )
    legacy.mkdir(parents=True)


invalid_fixture(
    "unconfigured-legacy-root",
    add_unconfigured_legacy,
    ("unconfigured-package: forbidden legacy root exists",),
)


def add_collision(root: Path) -> None:
    package = contract.packages[0]
    canonical = (
        root
        / package.name
        / Path(*contract.canonical_root.parts)
        / "readme.md"
    )
    canonical.write_text("collision\n", encoding="utf-8")


invalid_fixture(
    "case-collision",
    add_collision,
    ("path collision", "file set mismatch"),
)


def break_transform(root: Path) -> None:
    transform = contract.transforms[0]
    canonical = (
        root
        / transform.package
        / Path(*contract.canonical_root.parts)
        / Path(*transform.path.parts)
    )
    local = (
        root
        / transform.package
        / "skills"
        / contract.packages[0].registered_skills[0]
        / Path(*contract.local_root.parts)
        / Path(*transform.path.parts)
    )
    local.write_bytes(canonical.read_bytes())


invalid_fixture(
    "missing-transform",
    break_transform,
    ("SHA-256 mismatch", "projected bytes differ"),
)


def duplicate_registration(root: Path) -> None:
    manifest_path = root / contract.packages[0].name / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["agentSkills"].append(manifest["agentSkills"][0])
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


invalid_fixture(
    "duplicate-registration",
    duplicate_registration,
    ("duplicate value", "manifest registrations mismatch"),
)


def unregistered_projection(root: Path) -> None:
    package = contract.packages[0]
    local = (
        root
        / package.name
        / "skills"
        / "unregistered"
        / Path(*contract.local_root.parts)
    )
    local.mkdir(parents=True)


invalid_fixture(
    "unregistered-projection",
    unregistered_projection,
    ("local projection exists for unregistered skills",),
)

duplicate_contract = scratch / "duplicate-contract.json"
contract_text = contract_path.read_text(encoding="utf-8")
duplicate_contract.write_text(
    contract_text.replace(
        "{\n",
        '{\n  "schemaVersion": 1,\n',
        1,
    ),
    encoding="utf-8",
)
try:
    load_contract(duplicate_contract)
except ProjectionError as error:
    if "duplicate JSON member" not in str(error):
        raise AssertionError(
            f"duplicate contract reported wrong error: {error}",
        ) from error
else:
    raise AssertionError("duplicate contract member was accepted")

print("Microsoft 365 reference projection fixtures: OK")
PY

python3 "$VALIDATOR" --check --root "$SCRATCH/valid" \
  --contract "$CONTRACT"

if [[ "$MODE" == "--fixtures-only" ]]; then
  exit 0
fi

python3 "$VALIDATOR" --check --root "$PACKAGE_ROOT" \
  --contract "$CONTRACT"
