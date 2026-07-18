#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Validate Japanese Microsoft 365 Copilot Cowork skill content."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Final

from m365_cowork_frontmatter import (
    FrontmatterError,
    frontmatter_validation_errors,
    parse_frontmatter,
)
from m365_cowork_path_policy import (
    CompanionItem,
    CoworkPathError,
    Limits,
    companion_limit_errors,
    companion_policy,
    cowork_path_collision_key,
    load_json_object,
    load_limits,
    manifest_skill_slugs,
    validate_cowork_relative_path,
)

ROOT: Final = Path(__file__).resolve().parent.parent
TARGET_ROOT: Final = ROOT / "m365-cowork-ja" / "cowork-packages"
MARKDOWN_LINK_RE: Final = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BACKTICK_PATH_RE: Final = re.compile(
    r"`((?:(?:/|\./|\.\./)[^`\n]+|references/[A-Za-z0-9_./-]+))`",
)
SLASH_COMMAND_RE: Final = re.compile(
    r"^/[a-z0-9-]+:[a-z0-9-]+(?:\s.*)?$",
)
JAPANESE_CHARACTER_RE: Final = re.compile(
    r"[\u3040-\u30ff\u3400-\u9fff]",
)
CHANGE_NOTICE_MARKER: Final = "> **変更通知:**"
FORBIDDEN_RUNTIME_MARKERS: Final = ("~/.claude/", "$ARGUMENTS")
SKILL_ENTRYPOINT_NAME: Final = "SKILL.md"
MANIFEST_NAME: Final = "manifest.json"
PACKAGE_LEGAL_FILE_NAMES: Final = ("LICENSE", "NOTICE")
SKILL_LEGAL_FILE_PAIRS: Final = (
    ("LICENSE.txt", "LICENSE"),
    ("NOTICE.txt", "NOTICE"),
)
SKILL_LEGAL_NAMES_BY_STEM: Final = {
    "license": "LICENSE.txt",
    "notice": "NOTICE.txt",
}


def _relative(path: Path, target_root: Path) -> str:
    """Return a target-root-relative POSIX path."""
    return path.relative_to(target_root).as_posix()


def _contains_format_controls(text: str) -> bool:
    """Return whether text contains hidden Unicode format controls."""
    return any(unicodedata.category(character) == "Cf" for character in text)


def _declared_skill_paths(
    skills_root: Path,
    declared: tuple[str, ...],
) -> tuple[Path, ...]:
    """Return exact ``skills/<skill>/SKILL.md`` entrypoints."""
    return tuple(
        skill_path
        for slug in declared
        if (skill_path := skills_root / slug / SKILL_ENTRYPOINT_NAME).is_file()
    )


def _manifest_declared_skills(
    package_path: Path,
    limits: Limits,
    target_root: Path,
) -> tuple[tuple[str, ...], list[str]]:
    """Load the exact skill folder set declared by one package manifest."""
    manifest_path = package_path / MANIFEST_NAME
    relative = _relative(manifest_path, target_root)
    try:
        manifest = load_json_object(manifest_path, relative)
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError) as error:
        return (), [f"{relative}: invalid manifest: {error}"]
    try:
        declared = manifest_skill_slugs(
            manifest.get("agentSkills"),
            limits.maximum_manifest_skill_folder_characters,
            limits.maximum_skills,
        )
    except CoworkPathError as error:
        return (), [f"{relative}: {error}"]
    return declared, []


def _source_skill_slugs(skills_root: Path) -> tuple[str, ...]:
    """Return every direct source skill directory name."""
    return tuple(
        child.name for child in sorted(skills_root.iterdir()) if child.is_dir()
    )


def _declared_source_set_errors(
    skills_root: Path,
    declared: tuple[str, ...],
    target_root: Path,
) -> list[str]:
    """Require exact equality between manifest and source skill folders."""
    source = _source_skill_slugs(skills_root)
    if source == declared:
        return []
    relative = _relative(skills_root, target_root)
    return [
        f"{relative}: declared skills {declared!r} differ from "
        f"source skills {source!r}",
    ]


def _top_level_skill_shape_errors(
    skills_root: Path,
    target_root: Path,
) -> list[str]:
    """Return errors for invalid direct children of ``skills``."""
    errors: list[str] = []
    for child in sorted(skills_root.iterdir()):
        relative = _relative(child, target_root)
        if child.is_file():
            errors.append(
                f"{relative}: orphan file outside skills/<skill>/",
            )
        elif child.is_dir() and not (
            child / SKILL_ENTRYPOINT_NAME
        ).is_file():
            errors.append(
                f"{relative}: orphan skill directory missing "
                f"{SKILL_ENTRYPOINT_NAME}",
            )
    return errors


def _misplaced_entrypoint_errors(
    skills_root: Path,
    target_root: Path,
) -> list[str]:
    """Return errors for nested or root-level skill entrypoints."""
    return [
        (
            f"{_relative(entrypoint, target_root)}: skill entrypoint is "
            "outside skills/<skill>/SKILL.md"
        )
        for entrypoint in sorted(skills_root.rglob(SKILL_ENTRYPOINT_NAME))
        if entrypoint.parent.parent != skills_root
    ]


def _case_collision_errors(
    skills_root: Path,
    target_root: Path,
) -> list[str]:
    """Return case-insensitive collisions across the complete skills tree."""
    errors: list[str] = []
    observed: dict[str, Path] = {}
    for path in sorted(skills_root.rglob("*")):
        skill_relative = path.relative_to(skills_root).as_posix()
        collision_key = cowork_path_collision_key(skill_relative)
        previous = observed.get(collision_key)
        if previous is not None:
            relative = _relative(path, target_root)
            previous_relative = _relative(previous, target_root)
            errors.append(
                f"{relative}: case-insensitive path collision with "
                f"{previous_relative}",
            )
        else:
            observed[collision_key] = path
    return errors


def _path_policy_errors(
    package_path: Path,
    skills_root: Path,
    target_root: Path,
) -> list[str]:
    """Validate every directory and file path in the skills tree."""
    errors: list[str] = []
    for path in sorted(skills_root.rglob("*")):
        package_relative = path.relative_to(package_path).as_posix()
        try:
            validate_cowork_relative_path(package_relative)
        except CoworkPathError as error:
            relative = _relative(path, target_root)
            errors.append(f"{relative}: unsafe Cowork path: {error}")
    return errors


def _file_extension_error(
    file_path: Path,
    allowed_extensions: frozenset[str],
    target_root: Path,
) -> str | None:
    """Return one fleet/converter compatibility extension error."""
    relative = _relative(file_path, target_root)
    extension = file_path.suffix
    if not extension:
        if file_path.name in PACKAGE_LEGAL_FILE_NAMES:
            return (
                f"{relative}: file has no extension; required skill "
                f"legal name is {file_path.name}.txt"
            )
        return (
            f"{relative}: file has no extension; fleet/converter "
            "compatibility requires a declared extension"
        )
    if extension != extension.lower():
        return (
            f"{relative}: uppercase file extension is forbidden: "
            f"{extension}"
        )
    if extension not in allowed_extensions:
        return (
            f"{relative}: unsupported fleet/converter compatibility "
            f"extension {extension}"
        )
    return None


def _file_extension_errors(
    skills_root: Path,
    allowed_extensions: frozenset[str],
    target_root: Path,
) -> list[str]:
    """Validate every file extension under the complete skills tree."""
    errors: list[str] = []
    for file_path in sorted(skills_root.rglob("*")):
        if not file_path.is_file():
            continue
        error = _file_extension_error(
            file_path,
            allowed_extensions,
            target_root,
        )
        if error is not None:
            errors.append(error)
    return errors


def _scan_skill_tree(
    package_path: Path,
    declared: tuple[str, ...],
    limits: Limits,
    target_root: Path,
) -> tuple[tuple[Path, ...], list[str]]:
    """Discover declared skills and validate the complete skills tree."""
    skills_root = package_path / "skills"
    if not skills_root.is_dir():
        relative = _relative(package_path, target_root)
        return (), [f"{relative}: missing skills directory"]
    errors = _top_level_skill_shape_errors(skills_root, target_root)
    errors.extend(
        _declared_source_set_errors(skills_root, declared, target_root),
    )
    errors.extend(_misplaced_entrypoint_errors(skills_root, target_root))
    errors.extend(_path_policy_errors(package_path, skills_root, target_root))
    errors.extend(_case_collision_errors(skills_root, target_root))
    errors.extend(
        _file_extension_errors(
            skills_root,
            limits.fleet_converter_extensions,
            target_root,
        ),
    )
    return _declared_skill_paths(skills_root, declared), errors


def _validate_local_references(
    skill_path: Path,
    target_root: Path,
) -> list[str]:
    """Validate local references without allowing skill-root escapes."""
    errors: list[str] = []
    skill_root = skill_path.parent.resolve()
    for markdown_path in skill_path.parent.rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        raw_targets = [
            *MARKDOWN_LINK_RE.findall(text),
            *BACKTICK_PATH_RE.findall(text),
        ]
        for raw_target in raw_targets:
            errors.extend(
                _reference_errors(
                    markdown_path,
                    raw_target,
                    skill_root,
                    target_root,
                ),
            )
    return errors


def _is_nonlocal_reference(target: str) -> bool:
    """Return whether a reference does not resolve to a local file."""
    return target.startswith(
        ("http://", "https://", "mailto:", "#"),
    ) or SLASH_COMMAND_RE.fullmatch(target) is not None


def _local_reference_error(
    markdown_path: Path,
    target: str,
    skill_root: Path,
    target_root: Path,
) -> str | None:
    """Return an error for an invalid local reference."""
    relative = _relative(markdown_path, target_root)
    if target.startswith("/"):
        return f"{relative}: absolute local reference is forbidden: {target}"
    path_without_anchor = target.split("#", maxsplit=1)[0]
    if not path_without_anchor:
        return None
    resolved = (markdown_path.parent / path_without_anchor).resolve()
    if not resolved.is_relative_to(skill_root):
        return f"{relative}: reference escapes skill root: {target}"
    if not resolved.exists():
        return f"{relative}: missing local reference target {target}"
    return None


def _reference_errors(
    markdown_path: Path,
    raw_target: str,
    skill_root: Path,
    target_root: Path,
) -> list[str]:
    """Return validation errors for one local reference."""
    target = raw_target.strip().strip("<>")
    if _is_nonlocal_reference(target):
        return []
    error = _local_reference_error(
        markdown_path,
        target,
        skill_root,
        target_root,
    )
    return [error] if error is not None else []


def _validate_skill(
    skill_path: Path,
    limits: Limits,
    target_root: Path,
) -> tuple[list[str], list[str]]:
    """Validate one target skill."""
    text = skill_path.read_text(encoding="utf-8")
    relative = _relative(skill_path, target_root)
    errors = _frontmatter_errors(skill_path, text, limits, relative)
    errors.extend(
        _content_errors(
            skill_path,
            text,
            limits,
            relative,
            target_root,
        ),
    )
    warnings = _content_warnings(text, limits, relative)
    return errors, warnings


def _hidden_control_errors(
    value: str | None,
    field: str,
    relative: str,
) -> list[str]:
    """Return hidden Unicode control errors for one field."""
    if value is None:
        return []
    if _contains_format_controls(value):
        return [f"{relative}: {field} contains hidden Unicode controls"]
    return []


def _string_value(
    document: dict[str, object],
    field: str,
) -> str | None:
    """Return one parsed string field when its YAML type is correct."""
    value = document.get(field)
    return value if isinstance(value, str) else None


def _frontmatter_errors(
    skill_path: Path,
    text: str,
    limits: Limits,
    relative: str,
) -> list[str]:
    """Return strict frontmatter errors."""
    try:
        document = parse_frontmatter(text, skill_path)
    except FrontmatterError as error:
        return [str(error)]
    errors = [
        f"{relative}: {detail}"
        for detail in frontmatter_validation_errors(
            document,
            skill_path.parent.name,
            limits.frontmatter_policy(),
        )
    ]
    name = _string_value(document, "name")
    description = _string_value(document, "description")
    errors.extend(_hidden_control_errors(name, "name", relative))
    errors.extend(_hidden_control_errors(description, "description", relative))
    if (
        description is not None
        and JAPANESE_CHARACTER_RE.search(description) is None
    ):
        errors.append(f"{relative}: description must contain Japanese text")
    return errors


def _source_contract_errors(text: str, relative: str) -> list[str]:
    """Return source attribution and runtime marker errors."""
    errors: list[str] = []
    if CHANGE_NOTICE_MARKER not in text:
        errors.append(f"{relative}: Apache change notice is required")
    errors.extend(
        f"{relative}: unsupported source runtime marker {marker}"
        for marker in FORBIDDEN_RUNTIME_MARKERS
        if marker in text
    )
    return errors


def _storage_contract_errors(
    skill_path: Path,
    text: str,
    relative: str,
) -> list[str]:
    """Return errors for a missing required storage contract."""
    if "storage contract required" not in text:
        return []
    runtime_contract = (
        skill_path.parent
        / "references"
        / "common"
        / "cowork-runtime-contract.md"
    )
    if runtime_contract.is_file():
        return []
    return [f"{relative}: storage contract companion is required"]


def _character_limit_errors(
    text: str,
    limits: Limits,
    relative: str,
) -> list[str]:
    """Return strict skill character limit errors."""
    if len(text) <= limits.character_limit:
        return []
    return [
        f"{relative}: {len(text)} characters exceeds "
        f"{limits.character_limit}",
    ]


def _companion_items(
    skill_path: Path,
    target_root: Path,
) -> tuple[CompanionItem, ...]:
    """Return shared-policy records for one declared skill."""
    skill_root = skill_path.parent
    return tuple(
        CompanionItem(
            name=_relative(file_path, target_root),
            size=file_path.stat().st_size,
            depth=len(file_path.relative_to(skill_root).parts) - 1,
        )
        for file_path in sorted(skill_root.rglob("*"))
        if file_path.is_file() and file_path != skill_path
    )


def _companion_errors(
    skill_path: Path,
    limits: Limits,
    relative: str,
    target_root: Path,
) -> list[str]:
    """Return all shared static companion policy errors."""
    return list(
        companion_limit_errors(
            _companion_items(skill_path, target_root),
            companion_policy(limits),
            relative,
        ),
    )


def _text_format_errors(text: str, relative: str) -> list[str]:
    """Return final newline and trailing whitespace errors."""
    errors: list[str] = []
    if not text.endswith("\n"):
        errors.append(f"{relative}: missing final newline")
    if any(line.rstrip() != line for line in text.splitlines()):
        errors.append(f"{relative}: trailing whitespace")
    return errors


def _content_errors(
    skill_path: Path,
    text: str,
    limits: Limits,
    relative: str,
    target_root: Path,
) -> list[str]:
    """Return content size, hygiene, and link errors.

    Parameters
    ----------
    skill_path:
        Path to ``SKILL.md``.
    text:
        Skill Markdown text.
    limits:
        Target package limits.
    relative:
        Target-root-relative path.
    target_root:
        Target package root.

    Returns
    -------
    list[str]
        Content errors.

    """
    errors = _source_contract_errors(text, relative)
    errors.extend(
        _storage_contract_errors(skill_path, text, relative),
    )
    errors.extend(_character_limit_errors(text, limits, relative))
    errors.extend(_text_format_errors(text, relative))
    errors.extend(_validate_local_references(skill_path, target_root))
    return errors


def _required_package_file_errors(
    package_path: Path,
    target_root: Path,
) -> list[str]:
    """Return errors for missing package-level legal files."""
    errors: list[str] = []
    for required_name in PACKAGE_LEGAL_FILE_NAMES:
        required_path = package_path / required_name
        if not required_path.is_file():
            relative = _relative(package_path, target_root)
            errors.append(f"{relative}: missing {required_name}")
    return errors


def _package_markdown_errors(
    markdown_path: Path,
    target_root: Path,
) -> list[str]:
    """Return source and localization errors for package Markdown."""
    text = markdown_path.read_text(encoding="utf-8")
    relative = _relative(markdown_path, target_root)
    errors: list[str] = []
    if CHANGE_NOTICE_MARKER not in text:
        errors.append(f"{relative}: Apache change notice is required")
    if JAPANESE_CHARACTER_RE.search(text) is None:
        errors.append(f"{relative}: Japanese content is required")
    errors.extend(
        f"{relative}: unsupported source runtime marker {marker}"
        for marker in FORBIDDEN_RUNTIME_MARKERS
        if marker in text
    )
    return errors


def _package_errors(
    package_path: Path,
    target_root: Path,
) -> list[str]:
    """Return package-level license and notice errors.

    Parameters
    ----------
    package_path:
        Cowork package source directory.
    target_root:
        Target package root.

    Returns
    -------
    list[str]
        Package-level errors.

    """
    errors = _required_package_file_errors(package_path, target_root)
    for markdown_path in package_path.rglob("*.md"):
        errors.extend(
            _package_markdown_errors(markdown_path, target_root),
        )
    return errors


def _content_warnings(
    text: str,
    limits: Limits,
    relative: str,
) -> list[str]:
    """Return advisory content warnings.

    Parameters
    ----------
    text:
        Skill Markdown text.
    limits:
        Target package limits.
    relative:
        Target-root-relative path.

    Returns
    -------
    list[str]
        Advisory warnings.

    """
    line_count = len(text.splitlines())
    if line_count <= limits.recommended_lines:
        return []
    return [
        f"{relative}: {line_count} lines exceeds the recommended "
        f"{limits.recommended_lines}",
    ]


def _skill_count_errors(
    package_path: Path,
    declared: tuple[str, ...],
    limits: Limits,
) -> list[str]:
    """Return package skill count errors."""
    skill_count = len(declared)
    if skill_count <= limits.maximum_skills:
        return []
    return [
        f"{package_path.name}: {skill_count} skills exceeds "
        f"{limits.maximum_skills}",
    ]


def _declared_companion_errors(
    package_path: Path,
    declared: tuple[str, ...],
    limits: Limits,
    target_root: Path,
) -> list[str]:
    """Validate companions for every declared source skill directory."""
    errors: list[str] = []
    for slug in declared:
        skill_path = package_path / "skills" / slug / SKILL_ENTRYPOINT_NAME
        if skill_path.parent.is_dir():
            relative = _relative(skill_path, target_root)
            errors.extend(
                _companion_errors(
                    skill_path,
                    limits,
                    relative,
                    target_root,
                ),
            )
    return errors


def _required_skill_file_errors(
    skill_path: Path,
    package_path: Path,
    target_root: Path,
) -> list[str]:
    """Return errors for missing or divergent skill-level legal files."""
    errors: list[str] = []
    relative = _relative(skill_path, target_root)
    for skill_name, package_name in SKILL_LEGAL_FILE_PAIRS:
        skill_legal_path = skill_path.parent / skill_name
        if not skill_legal_path.is_file():
            errors.extend(
                _missing_skill_legal_errors(
                    skill_path,
                    skill_name,
                    package_name,
                    relative,
                ),
            )
            continue
        package_legal_path = package_path / package_name
        if (
            package_legal_path.is_file()
            and skill_legal_path.read_bytes()
            != package_legal_path.read_bytes()
        ):
            skill_relative = _relative(skill_legal_path, target_root)
            errors.append(
                f"{skill_relative}: content does not byte-match "
                f"package-root {package_name}",
            )
    return errors


def _missing_skill_legal_errors(
    skill_path: Path,
    skill_name: str,
    package_name: str,
    relative: str,
) -> list[str]:
    """Return a missing error unless a rejected legacy file explains it."""
    if (skill_path.parent / package_name).is_file():
        return []
    return [f"{relative}: missing exact companion {skill_name}"]


def _skill_legal_name_error(
    file_path: Path,
    target_root: Path,
) -> str | None:
    """Reject noncanonical legal-like filenames at a skill root."""
    if not file_path.is_file():
        return None
    if file_path.name in PACKAGE_LEGAL_FILE_NAMES:
        return None
    stem = file_path.name.partition(".")[0].casefold()
    expected_name = SKILL_LEGAL_NAMES_BY_STEM.get(stem)
    if expected_name is None or file_path.name == expected_name:
        return None
    relative = _relative(file_path, target_root)
    return (
        f"{relative}: skill legal filename must be exactly "
        f"{expected_name}"
    )


def _skill_legal_name_errors(
    skill_path: Path,
    target_root: Path,
) -> list[str]:
    """Return noncanonical skill-root legal filename errors."""
    errors: list[str] = []
    for file_path in sorted(skill_path.parent.iterdir()):
        error = _skill_legal_name_error(file_path, target_root)
        if error is not None:
            errors.append(error)
    return errors


def _validate_package(
    package_path: Path,
    limits: Limits,
    target_root: Path,
) -> tuple[list[str], list[str]]:
    """Validate one Cowork package."""
    errors = _package_errors(package_path, target_root)
    warnings: list[str] = []
    declared, manifest_errors = _manifest_declared_skills(
        package_path,
        limits,
        target_root,
    )
    errors.extend(manifest_errors)
    skill_paths, skill_tree_errors = _scan_skill_tree(
        package_path,
        declared,
        limits,
        target_root,
    )
    errors.extend(skill_tree_errors)
    errors.extend(_skill_count_errors(package_path, declared, limits))
    errors.extend(
        _declared_companion_errors(
            package_path,
            declared,
            limits,
            target_root,
        ),
    )
    for skill_path in skill_paths:
        errors.extend(_skill_legal_name_errors(skill_path, target_root))
        errors.extend(
            _required_skill_file_errors(
                skill_path,
                package_path,
                target_root,
            ),
        )
        skill_errors, skill_warnings = _validate_skill(
            skill_path,
            limits,
            target_root,
        )
        errors.extend(skill_errors)
        warnings.extend(skill_warnings)
    return errors, warnings


def _package_directories(target_root: Path) -> tuple[Path, ...]:
    """Return sorted package directories below the target root."""
    return tuple(
        path for path in sorted(target_root.glob("*")) if path.is_dir()
    )


def validate_target(
    target_root: Path = TARGET_ROOT,
    limits: Limits | None = None,
) -> tuple[list[str], list[str]]:
    """Validate every package under a target root.

    Parameters
    ----------
    target_root:
        Directory containing package directories.
    limits:
        Optional preloaded limits.

    Returns
    -------
    tuple[list[str], list[str]]
        Errors and warnings.

    """
    active_limits = load_limits() if limits is None else limits
    errors: list[str] = []
    warnings: list[str] = []
    package_paths = _package_directories(target_root)
    if not package_paths:
        return [f"{target_root.as_posix()}: no packages found"], warnings
    for package_path in package_paths:
        package_errors, package_warnings = _validate_package(
            package_path,
            active_limits,
            target_root,
        )
        errors.extend(package_errors)
        warnings.extend(package_warnings)
    return errors, warnings


def main() -> int:
    """Validate the default target root and return a process status.

    Returns
    -------
    int
        Zero when no validation errors are found.

    """
    errors, warnings = validate_target()
    for warning in warnings:
        sys.stderr.write(f"WARNING: {warning}\n")
    if errors:
        for error in errors:
            sys.stderr.write(f"ERROR: {error}\n")
        return 1
    sys.stdout.write("Microsoft 365 Cowork target validation: OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
