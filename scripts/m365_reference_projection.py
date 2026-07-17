#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Validate canonical Japanese references projected into Cowork skills."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path, PurePosixPath
from typing import Final

from m365_reference_common_projection import (
    compare_file_bytes,
    file_record,
    parse_common_projection,
    transformed_bytes,
    validate_common_projection,
)
from m365_reference_contract import (
    parse_byte_transform as _parse_byte_transform,
)
from m365_reference_contract import (
    require_exact_fields as _require_exact_fields,
)
from m365_reference_contract import (
    require_identifier as _require_identifier,
)
from m365_reference_contract import (
    require_list as _require_list,
)
from m365_reference_contract import (
    require_object as _require_object,
)
from m365_reference_contract import (
    require_positive_int as _require_positive_int,
)
from m365_reference_contract import (
    require_relative_path as _require_relative_path,
)
from m365_reference_contract import (
    require_text as _require_text,
)
from m365_reference_projection_types import (
    FileRecord,
    PackageContract,
    PackageOutcome,
    ProjectionContract,
    ProjectionError,
    ProjectionTotals,
    ProjectionTransform,
    TreeSnapshot,
    ValidationReport,
)

ROOT: Final = Path(__file__).resolve().parent.parent
DEFAULT_PACKAGE_ROOT: Final = ROOT / "m365-cowork-ja" / "cowork-packages"
DEFAULT_CONTRACT_PATH: Final = (
    ROOT / "m365-cowork-ja/shared/reference-projection-contract.json"
)
SCHEMA_VERSION: Final = 1
REQUIRED_CANONICAL_ROOT: Final = PurePosixPath(
    "references/jurisdictions/ja-jp",
)
REQUIRED_LOCAL_ROOT: Final = PurePosixPath("references/common/ja-jp")
REQUIRED_FORBIDDEN_ROOT: Final = PurePosixPath(
    "references/common/jurisdictions",
)
REQUIRED_TOTALS: Final = ProjectionTotals(10, 119, 79, 928)
REQUIRED_TRANSFORM: Final = ProjectionTransform(
    package="ai-governance-legal",
    path=PurePosixPath("README.md"),
    source=b"../../original-jurisdiction-logic.md",
    replacement=b"../original-jurisdiction-logic.md",
    expected_occurrences=1,
)
SKILL_FOLDER_RE: Final = re.compile(
    r"^\./skills/([a-z0-9][a-z0-9-]{1,63})$",
)
TOP_LEVEL_FIELDS: Final = frozenset({
    "schemaVersion", "canonicalRoot", "localRoot", "forbiddenLocalRoot",
    "expectedTotals", "commonFileProjection", "packages", "transforms",
})
TOTAL_FIELDS: Final = frozenset({
    "packageCount", "registeredSkillCount", "canonicalFileCount",
    "projectedFileCount",
})
PACKAGE_FIELDS: Final = frozenset({
    "expectedSkillCount", "expectedFilesPerSkill",
    "expectedProjectedFileCount", "registeredSkills", "canonicalFiles",
})
TRANSFORM_FIELDS: Final = frozenset({
    "package", "path", "from", "to", "expectedOccurrences",
})


def _reject_duplicate_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    """Build a JSON object while rejecting duplicate member names."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            message = f"duplicate JSON member {key!r}"
            raise ProjectionError(message)
        result[key] = value
    return result


def _load_json_object(path: Path) -> dict[str, object]:
    """Load a regular UTF-8 JSON object with duplicate-key rejection."""
    if not path.is_file() or path.is_symlink():
        message = f"{path}: must be a regular file"
        raise ProjectionError(message)
    try:
        raw: object = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except ProjectionError as error:
        message = f"{path}: {error}"
        raise ProjectionError(message) from error
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        message = f"{path}: invalid JSON: {error}"
        raise ProjectionError(message) from error
    return _require_object(raw, path.as_posix())


def _collision_key(value: str) -> str:
    """Return a Unicode-normalized case-insensitive path key."""
    return unicodedata.normalize("NFC", value).casefold()


def _validate_ordered_unique(
    values: tuple[str, ...],
    context: str,
) -> None:
    """Require sorted, exact, and collision-free strings."""
    seen: set[str] = set()
    collision_keys: dict[str, str] = {}
    for value in values:
        if value in seen:
            message = f"{context} contains duplicate value {value!r}"
            raise ProjectionError(message)
        key = _collision_key(value)
        previous = collision_keys.get(key)
        if previous is not None:
            message = (
                f"{context} contains colliding values "
                f"{previous!r} and {value!r}"
            )
            raise ProjectionError(message)
        seen.add(value)
        collision_keys[key] = value
    if values != tuple(sorted(values)):
        message = f"{context} must be sorted"
        raise ProjectionError(message)


def _identifier_list(value: object, context: str) -> tuple[str, ...]:
    """Parse a sorted collision-free identifier array."""
    items = _require_list(value, context)
    result = tuple(
        _require_identifier(item, f"{context}[{index}]")
        for index, item in enumerate(items)
    )
    _validate_ordered_unique(result, context)
    return result


def _path_list(value: object, context: str) -> tuple[PurePosixPath, ...]:
    """Parse a sorted collision-free relative-path array."""
    items = _require_list(value, context)
    paths = tuple(
        _require_relative_path(item, f"{context}[{index}]")
        for index, item in enumerate(items)
    )
    texts = tuple(path.as_posix() for path in paths)
    _validate_ordered_unique(texts, context)
    return paths


def _parse_totals(value: object) -> ProjectionTotals:
    """Parse and pin the fleet-wide count floor."""
    totals = _require_object(value, "expectedTotals")
    _require_exact_fields(totals, TOTAL_FIELDS, "expectedTotals")
    result = ProjectionTotals(
        package_count=_require_positive_int(
            totals.get("packageCount"),
            "expectedTotals.packageCount",
        ),
        registered_skill_count=_require_positive_int(
            totals.get("registeredSkillCount"),
            "expectedTotals.registeredSkillCount",
        ),
        canonical_file_count=_require_positive_int(
            totals.get("canonicalFileCount"),
            "expectedTotals.canonicalFileCount",
        ),
        projected_file_count=_require_positive_int(
            totals.get("projectedFileCount"),
            "expectedTotals.projectedFileCount",
        ),
    )
    if result != REQUIRED_TOTALS:
        message = (
            "expectedTotals must remain "
            f"{REQUIRED_TOTALS}, got {result}"
        )
        raise ProjectionError(message)
    return result


def _parse_package(name: str, value: object) -> PackageContract:
    """Parse one package projection declaration."""
    package = _require_object(value, f"packages.{name}")
    _require_exact_fields(package, PACKAGE_FIELDS, f"packages.{name}")
    skills = _identifier_list(
        package.get("registeredSkills"),
        f"packages.{name}.registeredSkills",
    )
    files = _path_list(
        package.get("canonicalFiles"),
        f"packages.{name}.canonicalFiles",
    )
    expected_skill_count = _require_positive_int(
        package.get("expectedSkillCount"),
        f"packages.{name}.expectedSkillCount",
    )
    expected_files_per_skill = _require_positive_int(
        package.get("expectedFilesPerSkill"),
        f"packages.{name}.expectedFilesPerSkill",
    )
    expected_projected_file_count = _require_positive_int(
        package.get("expectedProjectedFileCount"),
        f"packages.{name}.expectedProjectedFileCount",
    )
    if expected_skill_count != len(skills):
        message = f"packages.{name}: expectedSkillCount does not match skills"
        raise ProjectionError(message)
    if expected_files_per_skill != len(files):
        message = (
            f"packages.{name}: expectedFilesPerSkill does not match files"
        )
        raise ProjectionError(message)
    if expected_projected_file_count != len(skills) * len(files):
        message = (
            f"packages.{name}: expectedProjectedFileCount is not "
            "skills times files"
        )
        raise ProjectionError(message)
    return PackageContract(
        name=name,
        expected_skill_count=expected_skill_count,
        expected_files_per_skill=expected_files_per_skill,
        expected_projected_file_count=expected_projected_file_count,
        registered_skills=skills,
        canonical_files=files,
    )


def _parse_packages(value: object) -> tuple[PackageContract, ...]:
    """Parse the exact sorted package map."""
    package_map = _require_object(value, "packages")
    names = tuple(package_map)
    for index, name in enumerate(names):
        _require_identifier(name, f"packages key {index}")
    _validate_ordered_unique(names, "packages")
    return tuple(
        _parse_package(name, package_map[name])
        for name in names
    )


def _parse_transform(
    value: object,
    index: int,
) -> ProjectionTransform:
    """Parse one explicit byte replacement."""
    context = f"transforms[{index}]"
    _, fields = _parse_byte_transform(
        value,
        context,
        TRANSFORM_FIELDS,
    )
    return fields


def _parse_transforms(value: object) -> tuple[ProjectionTransform, ...]:
    """Parse and pin the sole allowed local transform."""
    items = _require_list(value, "transforms")
    transforms = tuple(
        _parse_transform(item, index)
        for index, item in enumerate(items)
    )
    if transforms != (REQUIRED_TRANSFORM,):
        message = (
            "transforms must contain only the explicit "
            "ai-governance-legal README path rewrite"
        )
        raise ProjectionError(message)
    return transforms


def _derived_totals(
    packages: tuple[PackageContract, ...],
) -> ProjectionTotals:
    """Calculate count floors from exact package declarations."""
    return ProjectionTotals(
        package_count=len(packages),
        registered_skill_count=sum(
            len(package.registered_skills)
            for package in packages
        ),
        canonical_file_count=sum(
            len(package.canonical_files)
            for package in packages
        ),
        projected_file_count=sum(
            package.expected_projected_file_count
            for package in packages
        ),
    )


def _validate_transform_targets(
    packages: tuple[PackageContract, ...],
    transforms: tuple[ProjectionTransform, ...],
) -> None:
    """Require every transform to target one declared canonical file."""
    declared = {
        (package.name, path)
        for package in packages
        for path in package.canonical_files
    }
    for transform in transforms:
        if (transform.package, transform.path) not in declared:
            message = (
                "transform targets undeclared canonical file "
                f"{transform.package}/{transform.path}"
            )
            raise ProjectionError(message)


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> ProjectionContract:
    """Load and strictly validate the reference projection contract."""
    raw = _load_json_object(path)
    _require_exact_fields(raw, TOP_LEVEL_FIELDS, "projection contract")
    version = _require_positive_int(
        raw.get("schemaVersion"),
        "schemaVersion",
    )
    if version != SCHEMA_VERSION:
        message = f"schemaVersion must be {SCHEMA_VERSION}, got {version}"
        raise ProjectionError(message)
    canonical_root = _require_relative_path(
        raw.get("canonicalRoot"),
        "canonicalRoot",
    )
    local_root = _require_relative_path(
        raw.get("localRoot"),
        "localRoot",
    )
    forbidden_root = _require_relative_path(
        raw.get("forbiddenLocalRoot"),
        "forbiddenLocalRoot",
    )
    roots = (canonical_root, local_root, forbidden_root)
    required_roots = (
        REQUIRED_CANONICAL_ROOT,
        REQUIRED_LOCAL_ROOT,
        REQUIRED_FORBIDDEN_ROOT,
    )
    if roots != required_roots:
        message = f"projection roots must remain {required_roots}, got {roots}"
        raise ProjectionError(message)
    totals = _parse_totals(raw.get("expectedTotals"))
    packages = _parse_packages(raw.get("packages"))
    common_projection = parse_common_projection(
        raw.get("commonFileProjection"),
        packages,
    )
    transforms = _parse_transforms(raw.get("transforms"))
    derived = _derived_totals(packages)
    if derived != totals:
        message = f"package declarations total {derived}, expected {totals}"
        raise ProjectionError(message)
    _validate_transform_targets(packages, transforms)
    return ProjectionContract(
        canonical_root=canonical_root,
        local_root=local_root,
        forbidden_local_root=forbidden_root,
        common_projection=common_projection,
        expected_totals=totals,
        packages=packages,
        transforms=transforms,
    )


def _path_exists(path: Path) -> bool:
    """Return whether a path or broken symbolic link exists."""
    return path.exists() or path.is_symlink()


def _is_regular_directory(path: Path) -> bool:
    """Return whether a path is a non-symlink directory."""
    return path.is_dir() and not path.is_symlink()


def _is_regular_file(path: Path) -> bool:
    """Return whether a path is a non-symlink regular file."""
    return path.is_file() and not path.is_symlink()


def _directory_entry_has_path(
    directory: Path,
    relative: PurePosixPath,
) -> bool:
    """Return whether a directory entry contains a relative path."""
    is_directory_entry = directory.is_dir() or directory.is_symlink()
    return (
        is_directory_entry
        and _path_exists(directory.joinpath(*relative.parts))
    )


def _collision_errors(
    relative_text: str,
    collision_keys: dict[str, str],
    context: str,
) -> tuple[str, ...]:
    """Record one path key and report a normalized collision."""
    key = _collision_key(relative_text)
    previous = collision_keys.get(key)
    if previous is None:
        collision_keys[key] = relative_text
        return ()
    if previous != relative_text:
        return (
            f"{context}: path collision {previous!r} / {relative_text!r}",
        )
    return ()


def _snapshot_entry(
    entry: Path,
    relative: PurePosixPath,
    context: str,
) -> tuple[FileRecord | None, tuple[str, ...]]:
    """Read one regular tree entry or return its structural error."""
    if entry.is_symlink():
        return None, (f"{context}/{relative}: symlink is forbidden",)
    if entry.is_dir():
        return None, ()
    if not entry.is_file():
        return None, (
            f"{context}/{relative}: non-regular entry is forbidden",
        )
    try:
        return file_record(entry.read_bytes()), ()
    except OSError as error:
        return None, (f"{context}/{relative}: cannot read: {error}",)


def _snapshot_tree(root: Path, context: str) -> TreeSnapshot:
    """Read a regular, collision-free file tree."""
    if not _path_exists(root):
        return TreeSnapshot({}, (f"{context}: root is missing",))
    if not _is_regular_directory(root):
        return TreeSnapshot(
            {},
            (f"{context}: root must be a regular directory",),
        )
    files: dict[PurePosixPath, FileRecord] = {}
    errors: list[str] = []
    collision_keys: dict[str, str] = {}
    entries = sorted(
        root.rglob("*"),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    for entry in entries:
        relative = PurePosixPath(entry.relative_to(root).as_posix())
        relative_text = relative.as_posix()
        errors.extend(
            _collision_errors(relative_text, collision_keys, context),
        )
        record, entry_errors = _snapshot_entry(entry, relative, context)
        errors.extend(entry_errors)
        if record is not None:
            files[relative] = record
    return TreeSnapshot(files, tuple(errors))


def _file_set_errors(
    actual: dict[PurePosixPath, FileRecord],
    expected: tuple[PurePosixPath, ...],
    context: str,
) -> tuple[str, ...]:
    """Return one exact file-set mismatch, if present."""
    actual_paths = set(actual)
    expected_paths = set(expected)
    if actual_paths == expected_paths:
        return ()
    missing = sorted(path.as_posix() for path in expected_paths - actual_paths)
    extra = sorted(path.as_posix() for path in actual_paths - expected_paths)
    return (
        f"{context}: file set mismatch; missing={missing}, extra={extra}",
    )


def _manifest_skills(manifest_path: Path) -> tuple[str, ...]:
    """Return sorted, collision-free manifest skill registrations."""
    manifest = _load_json_object(manifest_path)
    entries = _require_list(
        manifest.get("agentSkills"),
        f"{manifest_path}.agentSkills",
    )
    skills: list[str] = []
    for index, value in enumerate(entries):
        context = f"{manifest_path}.agentSkills[{index}]"
        entry = _require_object(value, context)
        _require_exact_fields(entry, frozenset({"folder"}), context)
        folder = _require_text(entry.get("folder"), f"{context}.folder")
        match = SKILL_FOLDER_RE.fullmatch(folder)
        if match is None:
            message = f"{context}.folder is invalid: {folder!r}"
            raise ProjectionError(message)
        skills.append(match.group(1))
    result = tuple(skills)
    _validate_ordered_unique(result, f"{manifest_path}.agentSkills")
    return result


def _skill_names_with_path(
    package_dir: Path,
    relative: PurePosixPath,
) -> tuple[str, ...]:
    """Return direct skill names containing a given relative path."""
    skills_root = package_dir / "skills"
    if not _is_regular_directory(skills_root):
        return ()
    names = [
        skill_dir.name
        for skill_dir in skills_root.iterdir()
        if _directory_entry_has_path(skill_dir, relative)
    ]
    return tuple(sorted(names))


def _registered_skill_error(
    package_dir: Path,
    package_name: str,
    skill: str,
) -> str | None:
    """Return one registered-skill structure error, if present."""
    skill_dir = package_dir / "skills" / skill
    if not _is_regular_directory(skill_dir):
        return f"{package_name}/{skill}: registered skill directory missing"
    if not _is_regular_file(skill_dir / "SKILL.md"):
        return f"{package_name}/{skill}: SKILL.md must be a regular file"
    return None


def _registered_skill_errors(
    package_dir: Path,
    package: PackageContract,
) -> tuple[str, ...]:
    """Require every registered skill directory and SKILL.md file."""
    results = (
        _registered_skill_error(package_dir, package.name, skill)
        for skill in package.registered_skills
    )
    return tuple(error for error in results if error is not None)


def _apply_transform(
    record: FileRecord,
    transform: ProjectionTransform | None,
    context: str,
) -> bytes:
    """Apply a count-checked explicit transform, if declared."""
    if transform is None:
        return record.data
    return transformed_bytes(
        record,
        transform.source,
        transform.replacement,
        transform.expected_occurrences,
        context,
    )


def _validate_local_tree(
    local_root: Path,
    package: PackageContract,
    skill: str,
    canonical: dict[PurePosixPath, FileRecord],
    transforms: dict[tuple[str, PurePosixPath], ProjectionTransform],
) -> tuple[tuple[str, ...], int]:
    """Validate one skill's exact local projection."""
    context = f"{package.name}/{skill}/{REQUIRED_LOCAL_ROOT}"
    snapshot = _snapshot_tree(local_root, context)
    errors = [
        *snapshot.errors,
        *_file_set_errors(
            snapshot.files,
            package.canonical_files,
            context,
        ),
    ]
    for path in package.canonical_files:
        source = canonical.get(path)
        local = snapshot.files.get(path)
        if source is None or local is None:
            continue
        try:
            expected_data = _apply_transform(
                source,
                transforms.get((package.name, path)),
                f"{package.name}/{REQUIRED_CANONICAL_ROOT}/{path}",
            )
        except ProjectionError as error:
            errors.append(str(error))
            continue
        errors.extend(
            compare_file_bytes(
                local,
                expected_data,
                f"{context}/{path}",
            ),
        )
    return tuple(errors), len(snapshot.files)


def _projection_presence_errors(
    package_dir: Path,
    package: PackageContract,
    contract: ProjectionContract,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Validate required and unregistered local projection roots."""
    projected = _skill_names_with_path(package_dir, contract.local_root)
    required = set(package.registered_skills)
    present = set(projected)
    errors: list[str] = []
    missing = sorted(required - present)
    extra = sorted(present - required)
    if missing:
        errors.append(
            f"{package.name}: local projection root missing for skills "
            f"{missing}",
        )
    if extra:
        errors.append(
            f"{package.name}: local projection exists for unregistered "
            f"skills {extra}",
        )
    return tuple(errors), projected


def _legacy_root_errors(
    package_root: Path,
    forbidden_root: PurePosixPath,
) -> tuple[str, ...]:
    """Reject the old local jurisdiction root in every package."""
    errors: list[str] = []
    for package_dir in sorted(package_root.iterdir()):
        if not _is_regular_directory(package_dir):
            continue
        skills = _skill_names_with_path(package_dir, forbidden_root)
        if skills:
            errors.append(
                f"{package_dir.name}: forbidden legacy root exists for "
                f"skills {list(skills)}",
            )
    return tuple(errors)


def _manifest_validation(
    package_dir: Path,
    package: PackageContract,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Validate manifest registrations and return observed skills."""
    errors: list[str] = []
    try:
        skills = _manifest_skills(package_dir / "manifest.json")
    except ProjectionError as error:
        errors.append(str(error))
        skills = ()
    if skills != package.registered_skills:
        errors.append(
            f"{package.name}: manifest registrations mismatch; "
            f"expected={list(package.registered_skills)}, "
            f"actual={list(skills)}",
        )
    return skills, tuple(errors)


def _validate_package(
    package_root: Path,
    package: PackageContract,
    contract: ProjectionContract,
    transforms: dict[tuple[str, PurePosixPath], ProjectionTransform],
) -> PackageOutcome:
    """Validate one package's manifest, canonical files, and projections."""
    package_dir = package_root / package.name
    if not _is_regular_directory(package_dir):
        return PackageOutcome(
            (f"{package.name}: package directory is missing",),
            0,
            0,
            0,
        )
    manifest_skills, manifest_errors = _manifest_validation(
        package_dir,
        package,
    )
    errors = list(manifest_errors)
    errors.extend(_registered_skill_errors(package_dir, package))
    canonical = _snapshot_tree(
        package_dir.joinpath(*contract.canonical_root.parts),
        f"{package.name}/{contract.canonical_root}",
    )
    errors.extend(canonical.errors)
    errors.extend(
        _file_set_errors(
            canonical.files,
            package.canonical_files,
            f"{package.name}/{contract.canonical_root}",
        ),
    )
    presence_errors, projected_skills = _projection_presence_errors(
        package_dir,
        package,
        contract,
    )
    errors.extend(presence_errors)
    projected_count = 0
    for skill in projected_skills:
        if skill not in package.registered_skills:
            continue
        local_errors, local_count = _validate_local_tree(
            package_dir
            / "skills"
            / skill
            / Path(*contract.local_root.parts),
            package,
            skill,
            canonical.files,
            transforms,
        )
        errors.extend(local_errors)
        projected_count += local_count
    return PackageOutcome(
        errors=tuple(errors),
        registered_skill_count=len(manifest_skills),
        canonical_file_count=len(canonical.files),
        projected_file_count=projected_count,
    )


def _packages_with_canonical_root(
    package_root: Path,
    canonical_root: PurePosixPath,
) -> tuple[str, ...]:
    """Return packages containing a canonical projection root."""
    if not _is_regular_directory(package_root):
        return ()
    names = [
        package_dir.name
        for package_dir in package_root.iterdir()
        if _directory_entry_has_path(package_dir, canonical_root)
    ]
    return tuple(sorted(names))


def _canonical_package_errors(
    actual: tuple[str, ...],
    expected: tuple[str, ...],
) -> tuple[str, ...]:
    """Require the exact ten packages to own canonical roots."""
    if actual == expected:
        return ()
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    return (
        "canonical projection package set mismatch; "
        f"missing={missing}, extra={extra}",
    )


def _transform_map(
    contract: ProjectionContract,
) -> dict[tuple[str, PurePosixPath], ProjectionTransform]:
    """Index explicit transforms by package and canonical path."""
    return {
        (transform.package, transform.path): transform
        for transform in contract.transforms
    }


def _contract_package_names(
    contract: ProjectionContract,
) -> tuple[str, ...]:
    """Return the contract's ordered package names."""
    return tuple(package.name for package in contract.packages)


def _package_outcomes(
    package_root: Path,
    contract: ProjectionContract,
) -> tuple[PackageOutcome, ...]:
    """Validate every package declared by the contract."""
    transforms = _transform_map(contract)
    return tuple(
        _validate_package(package_root, package, contract, transforms)
        for package in contract.packages
    )


def _outcome_errors(
    outcomes: tuple[PackageOutcome, ...],
) -> tuple[str, ...]:
    """Flatten package validation errors."""
    errors: list[str] = []
    for outcome in outcomes:
        errors.extend(outcome.errors)
    return tuple(errors)


def _observed_totals(
    actual_packages: tuple[str, ...],
    outcomes: tuple[PackageOutcome, ...],
) -> ProjectionTotals:
    """Calculate independent counts from filesystem observations."""
    return ProjectionTotals(
        package_count=len(actual_packages),
        registered_skill_count=sum(
            outcome.registered_skill_count
            for outcome in outcomes
        ),
        canonical_file_count=sum(
            outcome.canonical_file_count
            for outcome in outcomes
        ),
        projected_file_count=sum(
            outcome.projected_file_count
            for outcome in outcomes
        ),
    )


def validate_projection(
    package_root: Path,
    contract: ProjectionContract,
) -> ValidationReport:
    """Validate the exact canonical-to-skill reference projection."""
    if not _is_regular_directory(package_root):
        totals = ProjectionTotals(0, 0, 0, 0)
        return ValidationReport(
            (f"{package_root}: package root must be a directory",),
            totals,
        )
    actual_packages = _packages_with_canonical_root(
        package_root,
        contract.canonical_root,
    )
    errors = list(
        _canonical_package_errors(
            actual_packages,
            _contract_package_names(contract),
        ),
    )
    errors.extend(
        _legacy_root_errors(package_root, contract.forbidden_local_root),
    )
    outcomes = _package_outcomes(package_root, contract)
    errors.extend(_outcome_errors(outcomes))
    common_report = validate_common_projection(
        package_root,
        contract.common_projection,
        contract.packages,
    )
    errors.extend(common_report.errors)
    observed = _observed_totals(actual_packages, outcomes)
    if observed != contract.expected_totals:
        errors.append(
            "observed projection totals mismatch; "
            f"expected={contract.expected_totals}, actual={observed}",
        )
    return ValidationReport(tuple(errors), observed)
