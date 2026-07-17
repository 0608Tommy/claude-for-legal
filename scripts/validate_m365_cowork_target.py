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
from typing import Final, NamedTuple, cast

from m365_cowork_frontmatter import (
    extract_frontmatter,
    frontmatter_fields,
    frontmatter_scalar,
    frontmatter_text,
)

ROOT: Final = Path(__file__).resolve().parent.parent
TARGET_ROOT: Final = ROOT / "m365-cowork-ja" / "cowork-packages"
CONTRACT_PATH: Final = (
    ROOT / "m365-cowork-ja" / "shared" / "target-contract.json"
)
TARGET_ID_RE: Final = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
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


class Limits(NamedTuple):
    """Validated target package limits."""

    allowed_fields: frozenset[str]
    character_limit: int
    description_limit: int
    maximum_skills: int
    maximum_companion_files: int
    maximum_file_nesting_depth: int
    recommended_lines: int


def _require_object(value: object, context: str) -> dict[str, object]:
    """Require a JSON object.

    Parameters
    ----------
    value:
        Candidate JSON value.
    context:
        Human-readable value location.

    Returns
    -------
    dict[str, object]
        Validated mapping.

    Raises
    ------
    TypeError
        If ``value`` is not a JSON object.

    """
    if not isinstance(value, dict):
        message = f"{context} must be an object"
        raise TypeError(message)
    return cast("dict[str, object]", value)


def _require_int(value: object, context: str) -> int:
    """Require a JSON integer.

    Parameters
    ----------
    value:
        Candidate JSON value.
    context:
        Human-readable value location.

    Returns
    -------
    int
        Validated integer.

    Raises
    ------
    TypeError
        If ``value`` is not an integer.

    """
    if not isinstance(value, int) or isinstance(value, bool):
        message = f"{context} must be an integer"
        raise TypeError(message)
    return value


def _require_strings(value: object, context: str) -> frozenset[str]:
    """Require a JSON array of strings.

    Parameters
    ----------
    value:
        Candidate JSON value.
    context:
        Human-readable value location.

    Returns
    -------
    frozenset[str]
        Validated strings.

    Raises
    ------
    TypeError
        If ``value`` is not an array of strings.

    """
    if not isinstance(value, list):
        message = f"{context} must be an array of strings"
        raise TypeError(message)
    items = cast("list[object]", value)
    if not all(isinstance(item, str) for item in items):
        message = f"{context} must be an array of strings"
        raise TypeError(message)
    return frozenset(cast("list[str]", items))


def load_limits(contract_path: Path = CONTRACT_PATH) -> Limits:
    """Load strict and recommended limits from the target contract.

    Parameters
    ----------
    contract_path:
        Path to ``target-contract.json``.

    Returns
    -------
    Limits
        Validated limits.

    """
    raw_contract: object = json.loads(
        contract_path.read_text(encoding="utf-8"),
    )
    contract = _require_object(raw_contract, "target contract")
    frontmatter = _require_object(
        contract.get("frontmatter"),
        "frontmatter",
    )
    skill = _require_object(contract.get("skill"), "skill")
    return Limits(
        allowed_fields=_require_strings(
            frontmatter.get("allowedFields"),
            "frontmatter.allowedFields",
        ),
        character_limit=_require_int(
            frontmatter.get("strictCharacterLimit"),
            "frontmatter.strictCharacterLimit",
        ),
        description_limit=_require_int(
            frontmatter.get("descriptionCharacterLimit"),
            "frontmatter.descriptionCharacterLimit",
        ),
        maximum_skills=_require_int(
            skill.get("maximumPerPackage"),
            "skill.maximumPerPackage",
        ),
        maximum_companion_files=_require_int(
            skill.get("maximumCompanionFiles"),
            "skill.maximumCompanionFiles",
        ),
        maximum_file_nesting_depth=_require_int(
            skill.get("maximumFileNestingDepth"),
            "skill.maximumFileNestingDepth",
        ),
        recommended_lines=_require_int(
            skill.get("recommendedMaximumLines"),
            "skill.recommendedMaximumLines",
        ),
    )


def _relative(path: Path, target_root: Path) -> str:
    """Return a target-root-relative path.

    Parameters
    ----------
    path:
        Target path.
    target_root:
        Target package root.

    Returns
    -------
    str
        POSIX path relative to ``target_root``.

    """
    return path.relative_to(target_root).as_posix()


def _contains_format_controls(text: str) -> bool:
    """Return whether text contains hidden Unicode format controls.

    Parameters
    ----------
    text:
        Candidate text.

    Returns
    -------
    bool
        ``True`` when a Unicode ``Cf`` character is present.

    """
    return any(unicodedata.category(character) == "Cf" for character in text)


def _companion_files(skill_path: Path) -> tuple[Path, ...]:
    """Return companion files shipped beside a skill.

    Parameters
    ----------
    skill_path:
        Path to ``SKILL.md``.

    Returns
    -------
    tuple[Path, ...]
        All other files under the skill directory.

    """
    return tuple(
        path
        for path in skill_path.parent.rglob("*")
        if path.is_file() and path != skill_path
    )


def _validate_local_references(
    skill_path: Path,
    target_root: Path,
) -> list[str]:
    """Validate local references without allowing skill-root escapes.

    Parameters
    ----------
    skill_path:
        Path to ``SKILL.md``.
    target_root:
        Target package root.

    Returns
    -------
    list[str]
        Link validation errors.

    """
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
    """Return validation errors for one local reference.

    Parameters
    ----------
    markdown_path:
        Markdown file containing the reference.
    raw_target:
        Link or backticked reference target.
    skill_root:
        Resolved skill directory.
    target_root:
        Target package root.

    Returns
    -------
    list[str]
        Reference errors.

    """
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
    """Validate one target skill.

    Parameters
    ----------
    skill_path:
        Path to ``SKILL.md``.
    limits:
        Target package limits.
    target_root:
        Target package root.

    Returns
    -------
    tuple[list[str], list[str]]
        Errors and warnings.

    """
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


def _unexpected_frontmatter_errors(
    fields: tuple[str, ...],
    limits: Limits,
    relative: str,
) -> list[str]:
    """Return errors for unsupported frontmatter fields."""
    unsupported = sorted(set(fields) - limits.allowed_fields)
    if unsupported:
        return [f"{relative}: unexpected frontmatter fields {unsupported}"]
    return []


def _name_errors(
    name: str | None,
    skill_path: Path,
    relative: str,
) -> list[str]:
    """Return target skill name errors."""
    expected_name = skill_path.parent.name
    errors: list[str] = []
    if name != expected_name:
        errors.append(f"{relative}: name must match folder {expected_name}")
    if name is None or TARGET_ID_RE.fullmatch(name) is None:
        errors.append(f"{relative}: invalid target skill name {name!r}")
    errors.extend(_hidden_control_errors(name, "name", relative))
    return errors


def _description_errors(
    description: str | None,
    limits: Limits,
    relative: str,
) -> list[str]:
    """Return target skill description errors."""
    if not description:
        return [f"{relative}: description is required"]
    errors: list[str] = []
    if len(description) > limits.description_limit:
        errors.append(
            f"{relative}: description has {len(description)} characters",
        )
    elif JAPANESE_CHARACTER_RE.search(description) is None:
        errors.append(f"{relative}: description must contain Japanese text")
    errors.extend(
        _hidden_control_errors(description, "description", relative),
    )
    return errors


def _frontmatter_errors(
    skill_path: Path,
    text: str,
    limits: Limits,
    relative: str,
) -> list[str]:
    """Return strict frontmatter errors.

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

    Returns
    -------
    list[str]
        Frontmatter errors.

    """
    errors: list[str] = []
    try:
        frontmatter = extract_frontmatter(text, skill_path)
    except ValueError as error:
        return [str(error)]
    fields = frontmatter_fields(frontmatter)
    name = frontmatter_scalar(frontmatter, "name")
    description = frontmatter_text(frontmatter, "description")
    errors.extend(_unexpected_frontmatter_errors(fields, limits, relative))
    errors.extend(_name_errors(name, skill_path, relative))
    errors.extend(_description_errors(description, limits, relative))
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


def _companion_count_errors(
    skill_path: Path,
    limits: Limits,
    relative: str,
) -> list[str]:
    """Return strict companion file count errors."""
    companion_count = len(_companion_files(skill_path))
    if companion_count <= limits.maximum_companion_files:
        return []
    return [
        f"{relative}: {companion_count} companion files exceeds "
        f"{limits.maximum_companion_files}",
    ]


def _file_nesting_errors(
    skill_path: Path,
    limits: Limits,
    target_root: Path,
) -> list[str]:
    """Return errors for files nested too deeply below a skill root.

    Depth is the count of parent directories relative to the skill root,
    excluding the filename itself.

    """
    errors: list[str] = []
    skill_root = skill_path.parent
    for file_path in sorted(skill_root.rglob("*")):
        if not file_path.is_file():
            continue
        depth = len(file_path.relative_to(skill_root).parts) - 1
        if depth > limits.maximum_file_nesting_depth:
            relative = _relative(file_path, target_root)
            errors.append(
                f"{relative}: file nesting depth {depth} exceeds maximum "
                f"{limits.maximum_file_nesting_depth}",
            )
    return errors


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
    errors.extend(
        _companion_count_errors(skill_path, limits, relative),
    )
    errors.extend(_file_nesting_errors(skill_path, limits, target_root))
    errors.extend(_text_format_errors(text, relative))
    errors.extend(_validate_local_references(skill_path, target_root))
    return errors


def _required_package_file_errors(
    package_path: Path,
    target_root: Path,
) -> list[str]:
    """Return errors for missing package-level legal files."""
    errors: list[str] = []
    for required_name in ("LICENSE", "NOTICE"):
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
    skill_paths: tuple[Path, ...],
    limits: Limits,
) -> list[str]:
    """Return package skill count errors."""
    skill_count = len(skill_paths)
    if skill_count <= limits.maximum_skills:
        return []
    return [
        f"{package_path.name}: {skill_count} skills exceeds "
        f"{limits.maximum_skills}",
    ]


def _required_skill_file_errors(
    skill_path: Path,
    target_root: Path,
) -> list[str]:
    """Return errors for missing skill-level legal files."""
    errors: list[str] = []
    for required_name in ("LICENSE", "NOTICE"):
        required_path = skill_path.parent / required_name
        if not required_path.is_file():
            relative = _relative(skill_path, target_root)
            errors.append(
                f"{relative}: missing companion {required_name}",
            )
    return errors


def _validate_package(
    package_path: Path,
    limits: Limits,
    target_root: Path,
) -> tuple[list[str], list[str]]:
    """Validate one Cowork package."""
    errors = _package_errors(package_path, target_root)
    warnings: list[str] = []
    skill_paths = tuple(
        sorted(package_path.glob("skills/*/SKILL.md")),
    )
    errors.extend(_skill_count_errors(package_path, skill_paths, limits))
    for skill_path in skill_paths:
        errors.extend(_required_skill_file_errors(skill_path, target_root))
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
