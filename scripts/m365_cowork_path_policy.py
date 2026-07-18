#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Share strict Cowork companion path validation."""

from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath
from typing import Final, NamedTuple, cast

ROOT: Final = Path(__file__).resolve().parent.parent
CONTRACT_PATH: Final = (
    ROOT / "m365-cowork-ja" / "shared" / "target-contract.json"
)
TOOLCHAIN_LOCK_PATH: Final = (
    ROOT / "m365-cowork-ja" / "shared" / "toolchain-lock.json"
)
SAFE_SEGMENT_RE: Final = re.compile(r"^[A-Za-z0-9._! -]+$")
FILE_EXTENSION_RE: Final = re.compile(r"^\.[a-z0-9]+$")
CONTROL_CODE_LIMIT: Final = 0x20
DELETE_CODE: Final = 0x7F
SKILL_FOLDER_PART_COUNT: Final = 2
WINDOWS_RESERVED_BASENAMES: Final = frozenset(
    {
        "aux",
        "con",
        "nul",
        "prn",
        *(f"com{number}" for number in range(1, 10)),
        *(f"lpt{number}" for number in range(1, 10)),
    },
)


class CoworkPathError(ValueError):
    """Report one unsafe Cowork package path."""


class CompanionPolicy(NamedTuple):
    """Hold statically enforced per-skill companion limits."""

    maximum_files: int
    maximum_file_bytes: int
    maximum_total_bytes: int
    maximum_depth: int


class CompanionItem(NamedTuple):
    """Describe one companion path and its uncompressed size."""

    name: str
    size: int
    depth: int


class Limits(NamedTuple):
    """Hold validated target package limits."""

    allowed_fields: frozenset[str]
    character_limit: int
    description_limit: int
    maximum_skills: int
    maximum_companion_files: int
    maximum_companion_file_bytes: int
    maximum_companion_total_bytes: int
    maximum_file_nesting_depth: int
    maximum_manifest_skill_folder_characters: int
    companion_download_timeout_seconds: int
    recommended_lines: int
    fleet_converter_extensions: frozenset[str]


def _error(detail: str) -> CoworkPathError:
    """Build one path-policy exception."""
    return CoworkPathError(detail)


def _require_object(value: object, context: str) -> dict[str, object]:
    """Require a JSON object."""
    if not isinstance(value, dict):
        message = f"{context} must be an object"
        raise TypeError(message)
    return cast("dict[str, object]", value)


def _require_int(value: object, context: str) -> int:
    """Require a JSON integer."""
    if not isinstance(value, int) or isinstance(value, bool):
        message = f"{context} must be an integer"
        raise TypeError(message)
    return value


def _require_false(value: object, context: str) -> None:
    """Require an explicitly disabled static enforcement flag."""
    if value is not False:
        message = f"{context} must be false"
        raise ValueError(message)


def _require_strings(value: object, context: str) -> frozenset[str]:
    """Require a JSON array of strings."""
    if not isinstance(value, list):
        message = f"{context} must be an array of strings"
        raise TypeError(message)
    items = cast("list[object]", value)
    if not all(isinstance(item, str) for item in items):
        message = f"{context} must be an array of strings"
        raise TypeError(message)
    return frozenset(cast("list[str]", items))


def _invalid_extensions(extensions: frozenset[str]) -> list[str]:
    """Return extensions that are not normalized lowercase suffixes."""
    return sorted(
        extension
        for extension in extensions
        if FILE_EXTENSION_RE.fullmatch(extension) is None
    )


def _require_extension_set(
    value: object,
    context: str,
) -> frozenset[str]:
    """Require a nonempty set of normalized file extensions."""
    extensions = _require_strings(value, context)
    raw_items = cast("list[object]", value)
    if not extensions:
        message = f"{context} must not be empty"
        raise ValueError(message)
    if len(raw_items) != len(extensions):
        message = f"{context} must not contain duplicates"
        raise ValueError(message)
    invalid = _invalid_extensions(extensions)
    if invalid:
        message = f"{context} has invalid extensions {invalid}"
        raise ValueError(message)
    return extensions


def load_json_object(path: Path, context: str) -> dict[str, object]:
    """Load one JSON document and require an object root."""
    raw_document: object = json.loads(path.read_text(encoding="utf-8"))
    return _require_object(raw_document, context)


def _compatibility_extensions(
    document: dict[str, object],
    section_name: str,
    context: str,
) -> frozenset[str]:
    """Load the scoped fleet and converter compatibility extensions."""
    section = _require_object(
        document.get(section_name),
        f"{context}.{section_name}",
    )
    compatibility = _require_object(
        section.get("fleetConverterCompatibility"),
        f"{context}.{section_name}.fleetConverterCompatibility",
    )
    return _require_extension_set(
        compatibility.get("fileExtensions"),
        (
            f"{context}.{section_name}.fleetConverterCompatibility."
            "fileExtensions"
        ),
    )


def _matching_limit(
    target_value: object,
    target_context: str,
    toolchain_value: object,
    toolchain_context: str,
) -> int:
    """Require one target limit to match its toolchain lock value."""
    target_limit = _require_int(target_value, target_context)
    toolchain_limit = _require_int(toolchain_value, toolchain_context)
    if target_limit != toolchain_limit:
        message = (
            f"{target_context} and {toolchain_context} must match exactly"
        )
        raise ValueError(message)
    return target_limit


def load_limits(
    contract_path: Path = CONTRACT_PATH,
    toolchain_lock_path: Path = TOOLCHAIN_LOCK_PATH,
) -> Limits:
    """Load strict and recommended target and toolchain contracts."""
    contract = load_json_object(contract_path, "target contract")
    toolchain_lock = load_json_object(toolchain_lock_path, "toolchain lock")
    frontmatter = _require_object(
        contract.get("frontmatter"),
        "frontmatter",
    )
    skill = _require_object(contract.get("skill"), "skill")
    toolchain_limits = _require_object(
        toolchain_lock.get("limits"),
        "toolchain lock.limits",
    )
    target_extensions = _compatibility_extensions(
        contract,
        "skill",
        "target contract",
    )
    toolchain_extensions = _compatibility_extensions(
        toolchain_lock,
        "cowork",
        "toolchain lock",
    )
    if target_extensions != toolchain_extensions:
        message = (
            "target contract and toolchain lock fleet/converter "
            "compatibility extension sets must match exactly"
        )
        raise ValueError(message)
    _require_false(
        skill.get("companionDownloadTimeoutStaticEnforcement"),
        "skill.companionDownloadTimeoutStaticEnforcement",
    )
    limits = Limits(
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
        maximum_skills=_matching_limit(
            skill.get("maximumPerPackage"),
            "skill.maximumPerPackage",
            toolchain_limits.get("skillsPerPackage"),
            "toolchain lock.limits.skillsPerPackage",
        ),
        maximum_companion_files=_matching_limit(
            skill.get("maximumCompanionFiles"),
            "skill.maximumCompanionFiles",
            toolchain_limits.get("companionsPerSkill"),
            "toolchain lock.limits.companionsPerSkill",
        ),
        maximum_companion_file_bytes=_matching_limit(
            skill.get("maximumCompanionFileBytes"),
            "skill.maximumCompanionFileBytes",
            toolchain_limits.get("companionFileBytes"),
            "toolchain lock.limits.companionFileBytes",
        ),
        maximum_companion_total_bytes=_matching_limit(
            skill.get("maximumCompanionTotalBytes"),
            "skill.maximumCompanionTotalBytes",
            toolchain_limits.get("companionTotalBytes"),
            "toolchain lock.limits.companionTotalBytes",
        ),
        maximum_file_nesting_depth=_matching_limit(
            skill.get("maximumFileNestingDepth"),
            "skill.maximumFileNestingDepth",
            toolchain_limits.get("maximumFileNestingDepth"),
            "toolchain lock.limits.maximumFileNestingDepth",
        ),
        maximum_manifest_skill_folder_characters=_matching_limit(
            skill.get("maximumManifestSkillFolderCharacters"),
            "skill.maximumManifestSkillFolderCharacters",
            toolchain_limits.get("skillFolderPathCharacters"),
            "toolchain lock.limits.skillFolderPathCharacters",
        ),
        companion_download_timeout_seconds=_matching_limit(
            skill.get("companionDownloadTimeoutSeconds"),
            "skill.companionDownloadTimeoutSeconds",
            toolchain_limits.get("companionDownloadTimeoutSeconds"),
            "toolchain lock.limits.companionDownloadTimeoutSeconds",
        ),
        recommended_lines=_require_int(
            skill.get("recommendedMaximumLines"),
            "skill.recommendedMaximumLines",
        ),
        fleet_converter_extensions=target_extensions,
    )
    if limits.companion_download_timeout_seconds <= 0:
        message = "companion download timeout must be positive"
        raise ValueError(message)
    return limits


def _has_control_character(value: str) -> bool:
    """Return whether a path contains an ASCII control character."""
    return any(
        ord(character) < CONTROL_CODE_LIMIT
        or ord(character) == DELETE_CODE
        for character in value
    )


def _reserved_basename(segment: str) -> str:
    """Return a Windows-comparison basename for one path segment."""
    basename = segment.partition(".")[0]
    return basename.rstrip(" .").casefold()


def _segment_shape_error(segment: str) -> str | None:
    """Return a structural segment error."""
    if not segment:
        return "empty path segment is forbidden"
    if segment.startswith("."):
        return f"hidden path segment is forbidden: {segment!r}"
    if segment.endswith((" ", ".")):
        return f"path segment has a trailing dot or space: {segment!r}"
    return None


def _segment_name_error(segment: str) -> str | None:
    """Return a reserved-name or unsafe-character segment error."""
    if _reserved_basename(segment) in WINDOWS_RESERVED_BASENAMES:
        return f"Windows reserved basename is forbidden: {segment!r}"
    if SAFE_SEGMENT_RE.fullmatch(segment) is None:
        return f"path segment contains unsafe characters: {segment!r}"
    return None


def _validate_segment(segment: str) -> None:
    """Validate one explicit ASCII Cowork path segment."""
    for detail in (
        _segment_shape_error(segment),
        _segment_name_error(segment),
    ):
        if detail is not None:
            raise _error(detail)


def _path_shape_error(value: str) -> str | None:
    """Return a whole-path structural error."""
    if not value:
        return "path must not be empty"
    if _has_control_character(value):
        return "control character in path is forbidden"
    if "\\" in value:
        return "backslash in path is forbidden"
    if value.startswith("/"):
        return "absolute path is forbidden"
    return None


def validate_cowork_relative_path(value: str) -> PurePosixPath:
    """Validate and return one slash-separated relative Cowork path.

    Parameters
    ----------
    value:
        Raw package-relative path.

    Returns
    -------
    pathlib.PurePosixPath
        Validated relative path.

    Raises
    ------
    CoworkPathError
        If the path violates the shared source and ZIP policy.

    """
    detail = _path_shape_error(value)
    if detail is not None:
        raise _error(detail)
    segments = value.split("/")
    for segment in segments:
        _validate_segment(segment)
    return PurePosixPath(*segments)


def validate_manifest_skill_folder(
    value: str,
    maximum_characters: int,
) -> PurePosixPath:
    """Validate one raw ``agentSkills[].folder`` value.

    Parameters
    ----------
    value:
        Raw manifest value, including its required ``./`` prefix.
    maximum_characters:
        Maximum raw character count.

    Returns
    -------
    pathlib.PurePosixPath
        Validated package-relative path without the ``./`` prefix.

    Raises
    ------
    CoworkPathError
        If the raw folder is too long or violates the shared path policy.

    """
    if len(value) > maximum_characters:
        detail = (
            f"raw folder has {len(value)} characters; maximum is "
            f"{maximum_characters}"
        )
        raise _error(detail)
    if not value.startswith("./"):
        detail = "skill folder must start with './'"
        raise _error(detail)
    return validate_cowork_relative_path(value.removeprefix("./"))


def _manifest_folder_value(value: object, index: int) -> str:
    """Return one raw manifest folder value."""
    context = f"agentSkills[{index}].folder"
    if not isinstance(value, dict):
        detail = f"{context}: entry must be an object"
        raise _error(detail)
    item = cast("dict[str, object]", value)
    folder = item.get("folder")
    if not isinstance(folder, str) or not folder:
        detail = f"{context}: folder must be a nonempty string"
        raise _error(detail)
    return folder


def _direct_skill_slug(path: PurePosixPath, index: int) -> str:
    """Return a slug from one canonical direct ``skills`` child."""
    if (
        len(path.parts) != SKILL_FOLDER_PART_COUNT
        or path.parts[0] != "skills"
    ):
        detail = f"agentSkills[{index}].folder must match ./skills/<slug>"
        raise _error(detail)
    return path.parts[1]


def _manifest_skill_slugs(
    values: list[object],
    maximum_characters: int,
) -> list[str]:
    """Validate and collect manifest skill folder slugs."""
    slugs: list[str] = []
    for index, value in enumerate(values):
        raw_folder = _manifest_folder_value(value, index)
        path = validate_manifest_skill_folder(raw_folder, maximum_characters)
        slugs.append(_direct_skill_slug(path, index))
    return slugs


def _validate_unique_slugs(slugs: list[str]) -> None:
    """Reject duplicate and case-insensitive manifest folder collisions."""
    if len(slugs) != len(set(slugs)):
        detail = "agentSkills contains duplicate folders"
        raise _error(detail)
    collision_keys = {cowork_path_collision_key(slug) for slug in slugs}
    if len(slugs) != len(collision_keys):
        detail = "agentSkills contains case-colliding folders"
        raise _error(detail)


def manifest_skill_slugs(
    value: object,
    maximum_characters: int,
) -> tuple[str, ...]:
    """Return the sorted, validated ``agentSkills`` folder slugs.

    Parameters
    ----------
    value:
        Raw ``agentSkills`` manifest value.
    maximum_characters:
        Maximum raw ``folder`` character count.

    Returns
    -------
    tuple[str, ...]
        Sorted, unique direct skill directory names.

    Raises
    ------
    CoworkPathError
        If the array or any folder violates the shared policy.

    """
    if not isinstance(value, list) or not value:
        detail = "agentSkills must be a nonempty array"
        raise _error(detail)
    slugs = _manifest_skill_slugs(
        cast("list[object]", value),
        maximum_characters,
    )
    _validate_unique_slugs(slugs)
    return tuple(sorted(slugs))


def _companion_count_errors(
    items: tuple[CompanionItem, ...],
    policy: CompanionPolicy,
    skill_label: str,
) -> tuple[str, ...]:
    """Return a per-skill companion count error."""
    count = len(items)
    if count <= policy.maximum_files:
        return ()
    return (
        f"{skill_label}: {count} companion files exceeds "
        f"{policy.maximum_files}",
    )


def _companion_file_size_errors(
    items: tuple[CompanionItem, ...],
    policy: CompanionPolicy,
) -> tuple[str, ...]:
    """Return oversized individual companion errors."""
    return tuple(
        f"{item.name}: companion file size {item.size} bytes exceeds "
        f"{policy.maximum_file_bytes}"
        for item in items
        if item.size > policy.maximum_file_bytes
    )


def _companion_total_size_errors(
    items: tuple[CompanionItem, ...],
    policy: CompanionPolicy,
    skill_label: str,
) -> tuple[str, ...]:
    """Return a per-skill aggregate companion size error."""
    total_size = sum(item.size for item in items)
    if total_size <= policy.maximum_total_bytes:
        return ()
    return (
        f"{skill_label}: companion total size {total_size} bytes exceeds "
        f"{policy.maximum_total_bytes}",
    )


def _companion_depth_errors(
    items: tuple[CompanionItem, ...],
    policy: CompanionPolicy,
) -> tuple[str, ...]:
    """Return conservative nesting-depth errors."""
    return tuple(
        f"{item.name}: file nesting depth {item.depth} exceeds maximum "
        f"{policy.maximum_depth}"
        for item in items
        if item.depth > policy.maximum_depth
    )


def companion_limit_errors(
    items: tuple[CompanionItem, ...],
    policy: CompanionPolicy,
    skill_label: str,
) -> tuple[str, ...]:
    """Return all static count, byte, and depth errors for one skill."""
    return (
        *_companion_count_errors(items, policy, skill_label),
        *_companion_file_size_errors(items, policy),
        *_companion_total_size_errors(items, policy, skill_label),
        *_companion_depth_errors(items, policy),
    )


def companion_policy(limits: Limits) -> CompanionPolicy:
    """Return the shared static companion policy from loaded limits."""
    return CompanionPolicy(
        maximum_files=limits.maximum_companion_files,
        maximum_file_bytes=limits.maximum_companion_file_bytes,
        maximum_total_bytes=limits.maximum_companion_total_bytes,
        maximum_depth=limits.maximum_file_nesting_depth,
    )


def cowork_path_collision_key(value: str) -> str:
    """Return the case-insensitive collision key for a validated path."""
    return value.casefold()
