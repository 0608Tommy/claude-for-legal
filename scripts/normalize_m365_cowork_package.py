#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Validate and deterministically normalize one Cowork ATK package."""

from __future__ import annotations

import hashlib
import json
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Final, NamedTuple, cast

from m365_cowork_path_policy import (
    CompanionItem,
    CoworkPathError,
    Limits,
    companion_limit_errors,
    companion_policy,
    cowork_path_collision_key,
    load_limits,
    manifest_skill_slugs,
    validate_cowork_relative_path,
)
from validate_m365_cowork_icons import (
    EXPECTED_DIMENSIONS,
    IconValidationError,
    validate_png_bytes,
)

DOS_EPOCH: Final = (1980, 1, 1, 0, 0, 0)
FIXED_MODE: Final = stat.S_IFREG | 0o644
FIXED_EXTERNAL_ATTR: Final = FIXED_MODE << 16
UNIX_CREATE_SYSTEM: Final = 3
SKILL_PATH_PART_COUNT: Final = 2
CLI_ARGUMENT_COUNT: Final = 4
MAX_UNCOMPRESSED_BYTES: Final = 100 * 1024 * 1024
MAX_MEMBER_BYTES: Final = 20 * 1024 * 1024
REQUIRED_SKILL_FILES: Final = ("SKILL.md", "LICENSE.txt", "NOTICE.txt")
CANONICAL_LEGAL_FILES: Final = ("LICENSE", "NOTICE")
DISTRIBUTED_LEGAL_FILES: Final = (
    ("LICENSE.txt", "LICENSE"),
    ("NOTICE.txt", "NOTICE"),
)
LEGAL_FILE_STEMS: Final = frozenset({"license", "notice"})
CONNECTOR_DRAFT_NAME: Final = "connectors.draft.json"


class PackageBuildError(ValueError):
    """Report an unsafe or semantically invalid package archive."""


class ArchiveEntry(NamedTuple):
    """Hold one validated archive member and its original bytes."""

    name: str
    data: bytes


def _error(context: str, detail: str) -> PackageBuildError:
    """Build a consistently contextualized package error."""
    return PackageBuildError(f"{context}: {detail}")


def _require_regular_file(path: Path, context: str) -> None:
    """Require a non-symlink regular file."""
    if not path.is_file() or path.is_symlink():
        raise _error(context, "must be a regular file")


def _require_object(value: object, context: str) -> dict[str, object]:
    """Require a JSON object."""
    if not isinstance(value, dict):
        raise _error(context, "must be a JSON object")
    return cast("dict[str, object]", value)


def _load_json_bytes(data: bytes, context: str) -> dict[str, object]:
    """Decode a UTF-8 JSON object."""
    try:
        value: object = json.loads(data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise _error(context, f"invalid JSON: {error}") from error
    return _require_object(value, context)


def _load_json_path(path: Path) -> dict[str, object]:
    """Load a regular UTF-8 JSON object from disk."""
    _require_regular_file(path, path.as_posix())
    try:
        return _load_json_bytes(path.read_bytes(), path.as_posix())
    except OSError as error:
        raise _error(path.as_posix(), f"cannot read file: {error}") from error


def _member_path(name: str, context: str) -> PurePosixPath:
    """Validate and return one canonical ZIP member path."""
    try:
        return validate_cowork_relative_path(name)
    except CoworkPathError as error:
        raise _error(
            context,
            f"unsafe ZIP member path {name!r}: {error}",
        ) from error


def _member_mode(info: zipfile.ZipInfo) -> int:
    """Return the Unix mode encoded in a ZIP member."""
    return info.external_attr >> 16


def _validate_member_type(
    info: zipfile.ZipInfo,
    context: str,
) -> None:
    """Reject directories, links, devices, and encrypted members."""
    if info.is_dir():
        raise _error(
            context,
            f"directory member is forbidden: {info.filename}",
        )
    mode = _member_mode(info)
    if stat.S_ISLNK(mode):
        raise _error(context, f"symlink member is forbidden: {info.filename}")
    file_type = stat.S_IFMT(mode)
    if file_type not in {0, stat.S_IFREG}:
        raise _error(
            context,
            f"non-regular member is forbidden: {info.filename}",
        )
    if info.flag_bits & 1:
        raise _error(
            context,
            f"encrypted member is forbidden: {info.filename}",
        )


def _validate_unique_name(
    name: str,
    names: set[str],
    collision_keys: set[str],
    context: str,
) -> None:
    """Reject duplicate and case-colliding archive member names."""
    if name in names:
        raise _error(context, f"duplicate ZIP member {name!r}")
    key = cowork_path_collision_key(name)
    if key in collision_keys:
        raise _error(context, f"case-colliding ZIP member {name!r}")
    names.add(name)
    collision_keys.add(key)


def _validated_member_data(
    archive: zipfile.ZipFile,
    info: zipfile.ZipInfo,
    context: str,
) -> bytes:
    """Read one bounded member while verifying its ZIP CRC."""
    if info.file_size > MAX_MEMBER_BYTES:
        raise _error(context, f"ZIP member is too large: {info.filename}")
    try:
        data = archive.read(info)
    except (RuntimeError, NotImplementedError, zipfile.BadZipFile) as error:
        raise _error(
            context,
            f"cannot decode ZIP member {info.filename!r}: {error}",
        ) from error
    if len(data) != info.file_size:
        raise _error(context, f"ZIP member size mismatch: {info.filename}")
    return data


def _raw_member_name(info: zipfile.ZipInfo, context: str) -> str:
    """Validate a raw central-directory name before ZIP sanitization."""
    raw_name = info.orig_filename
    _member_path(raw_name, context)
    if raw_name != info.filename:
        raise _error(
            context,
            f"ZIP member name was sanitized: {raw_name!r}",
        )
    return raw_name


def _read_archive_entries(archive_path: Path) -> list[ArchiveEntry]:
    """Read and safety-check every raw ATK archive member."""
    context = archive_path.as_posix()
    _require_regular_file(archive_path, context)
    names: set[str] = set()
    collision_keys: set[str] = set()
    entries: list[ArchiveEntry] = []
    total_size = 0
    try:
        with zipfile.ZipFile(archive_path) as archive:
            for info in archive.infolist():
                raw_name = _raw_member_name(info, context)
                _validate_member_type(info, context)
                _validate_unique_name(
                    raw_name,
                    names,
                    collision_keys,
                    context,
                )
                data = _validated_member_data(archive, info, context)
                total_size += len(data)
                if total_size > MAX_UNCOMPRESSED_BYTES:
                    raise _error(context, "ZIP expands beyond the size limit")
                entries.append(ArchiveEntry(raw_name, data))
    except zipfile.BadZipFile as error:
        raise _error(context, f"invalid ZIP archive: {error}") from error
    if not entries:
        raise _error(context, "ZIP archive must not be empty")
    return entries


def _manifest_relative_path(
    value: object,
    context: str,
) -> PurePosixPath:
    """Validate a package-relative path from the manifest."""
    if not isinstance(value, str) or not value:
        raise _error(context, "manifest path must be a nonempty string")
    normalized = value.removeprefix("./")
    try:
        return validate_cowork_relative_path(normalized)
    except CoworkPathError as error:
        detail = f"unsafe manifest path {value!r}: {error}"
        raise _error(context, detail) from error


def _manifest_icons(
    manifest: dict[str, object],
    context: str,
) -> dict[str, PurePosixPath]:
    """Return the manifest's exact color and outline icon paths."""
    icons = _require_object(manifest.get("icons"), f"{context} icons")
    if set(icons) != set(EXPECTED_DIMENSIONS):
        raise _error(context, "icons must declare exactly color and outline")
    return {
        name: _manifest_relative_path(
            icons.get(name),
            f"{context} icons.{name}",
        )
        for name in EXPECTED_DIMENSIONS
    }


def _declared_skills(
    manifest: dict[str, object],
    limits: Limits,
    context: str,
) -> tuple[str, ...]:
    """Return sorted, unique skill slugs declared by the manifest."""
    try:
        return manifest_skill_slugs(
            manifest.get("agentSkills"),
            limits.maximum_manifest_skill_folder_characters,
        )
    except CoworkPathError as error:
        raise _error(context, str(error)) from error


def _require_regular_directory(path: Path, context: str) -> None:
    """Require a non-symlink directory."""
    if not path.is_dir() or path.is_symlink():
        raise _error(context, f"must be a regular directory: {path}")


def _validate_source_path(name: str, context: str) -> None:
    """Apply the shared Cowork path policy to one source-tree path."""
    try:
        validate_cowork_relative_path(name)
    except CoworkPathError as error:
        raise _error(
            context,
            f"unsafe source path {name!r}: {error}",
        ) from error


def _source_skill_slugs(source_dir: Path, context: str) -> tuple[str, ...]:
    """Return the exact regular directory set under source ``skills``."""
    skills_dir = source_dir / "skills"
    _require_regular_directory(skills_dir, context)
    slugs: list[str] = []
    for path in sorted(skills_dir.iterdir()):
        _validate_source_path(
            path.relative_to(source_dir).as_posix(),
            context,
        )
        _require_regular_directory(path, context)
        slugs.append(path.name)
    return tuple(slugs)


def _validate_source_skill_set(
    source_dir: Path,
    declared: tuple[str, ...],
    context: str,
) -> None:
    """Require source skill directories to equal manifest declarations."""
    source_slugs = _source_skill_slugs(source_dir, context)
    if source_slugs != declared:
        raise _error(
            context,
            (
                f"source skills {source_slugs!r} differ from "
                f"declared skills {declared!r}"
            ),
        )


def _regular_tree_files(
    root: Path,
    source_dir: Path,
    context: str,
) -> list[Path]:
    """Return all regular files below a symlink-free source tree."""
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        _validate_source_path(
            path.relative_to(source_dir).as_posix(),
            context,
        )
        if path.is_symlink():
            raise _error(context, f"source symlink is forbidden: {path}")
        if path.is_file():
            files.append(path)
        elif not path.is_dir():
            raise _error(context, f"source special file is forbidden: {path}")
    return files


def _source_skill_entries(
    source_dir: Path,
    declared: tuple[str, ...],
    context: str,
) -> dict[str, bytes]:
    """Load every declared source skill file using archive-relative names."""
    entries: dict[str, bytes] = {}
    collision_keys: set[str] = set()
    for slug in declared:
        skill_dir = source_dir / "skills" / slug
        for path in _regular_tree_files(skill_dir, source_dir, context):
            name = path.relative_to(source_dir).as_posix()
            key = cowork_path_collision_key(name)
            if key in collision_keys:
                raise _error(context, f"source path case collision: {name}")
            collision_keys.add(key)
            entries[name] = path.read_bytes()
    return entries


def _skill_companion_items(
    entries: dict[str, bytes],
    slug: str,
    origin: str,
) -> tuple[CompanionItem, ...]:
    """Return shared-policy records for one package view of a skill."""
    prefix = f"skills/{slug}/"
    entrypoint = f"{prefix}SKILL.md"
    prefix_parts = len(PurePosixPath("skills", slug).parts)
    return tuple(
        CompanionItem(
            name=f"{origin} companion file {name}",
            size=len(data),
            depth=len(PurePosixPath(name).parts) - prefix_parts - 1,
        )
        for name, data in sorted(entries.items())
        if name.startswith(prefix) and name != entrypoint
    )


def _validate_companion_limits(
    entries: dict[str, bytes],
    declared: tuple[str, ...],
    limits: Limits,
    context: str,
    origin: str,
) -> None:
    """Validate every declared skill with the shared companion policy."""
    policy = companion_policy(limits)
    for slug in declared:
        errors = companion_limit_errors(
            _skill_companion_items(entries, slug, origin),
            policy,
            f"{origin} skill {slug!r}",
        )
        if errors:
            raise _error(context, errors[0])


def _validate_required_skill_files(
    entries: dict[str, bytes],
    declared: tuple[str, ...],
    context: str,
    origin: str,
) -> None:
    """Require each skill's definition, license, and notice."""
    for slug in declared:
        for filename in REQUIRED_SKILL_FILES:
            name = f"skills/{slug}/{filename}"
            data = entries.get(name)
            if not data:
                raise _error(
                    context,
                    f"required {origin} file missing or empty: {name}",
                )


def _canonical_legal_data(
    source_dir: Path,
    context: str,
) -> dict[str, bytes]:
    """Return nonempty package-level canonical legal files."""
    legal_data: dict[str, bytes] = {}
    for filename in CANONICAL_LEGAL_FILES:
        path = source_dir / filename
        _require_regular_file(path, path.as_posix())
        data = path.read_bytes()
        if not data:
            raise _error(context, f"package {filename} must not be empty")
        legal_data[filename] = data
    return legal_data


def _skill_root_legal_filename(
    name: str,
    declared: tuple[str, ...],
) -> str | None:
    """Return a legal-like filename at a declared skill root."""
    parts = PurePosixPath(name).parts
    if (
        len(parts) != SKILL_PATH_PART_COUNT + 1
        or parts[0] != "skills"
        or parts[1] not in declared
    ):
        return None
    filename = parts[2]
    stem, _, _ = filename.partition(".")
    return filename if stem.casefold() in LEGAL_FILE_STEMS else None


def _validate_skill_legal_names(
    names: set[str],
    declared: tuple[str, ...],
    context: str,
    origin: str,
) -> None:
    """Reject legacy, alternate-extension, and mis-cased legal files."""
    for name in sorted(names):
        filename = _skill_root_legal_filename(name, declared)
        if filename is None or filename in REQUIRED_SKILL_FILES:
            continue
        raise _error(
            context,
            _legal_name_error_detail(name, filename, origin),
        )


def _legal_name_error_detail(
    name: str,
    filename: str,
    origin: str,
) -> str:
    """Return the specific error for one unsupported legal filename."""
    _, separator, extension = filename.partition(".")
    if not separator:
        return f"legacy extensionless legal member is forbidden: {name}"
    if extension.casefold() != "txt":
        return f"unsupported legal-file extension in {origin}: {name}"
    return f"legal-file name must use canonical case in {origin}: {name}"


def _validate_distributed_legal_bytes(
    entry_map: dict[str, bytes],
    declared: tuple[str, ...],
    canonical: dict[str, bytes],
    context: str,
) -> None:
    """Require archived legal copies to equal package-root canonical bytes."""
    for slug in declared:
        for distributed_name, canonical_name in DISTRIBUTED_LEGAL_FILES:
            name = f"skills/{slug}/{distributed_name}"
            if entry_map[name] != canonical[canonical_name]:
                raise _error(
                    context,
                    (
                        "archived legal file differs from package-root "
                        f"{canonical_name}: {name}"
                    ),
                )


def _source_icon_data(
    source_dir: Path,
    path: PurePosixPath,
    context: str,
) -> bytes:
    """Read one contained, regular source icon."""
    source_path = source_dir.joinpath(*path.parts)
    try:
        source_path.resolve().relative_to(source_dir.resolve())
    except ValueError as error:
        raise _error(
            context,
            f"source icon escapes package: {path}",
        ) from error
    _require_regular_file(source_path, source_path.as_posix())
    return source_path.read_bytes()


def _validate_icons(
    entry_map: dict[str, bytes],
    source_dir: Path,
    icons: dict[str, PurePosixPath],
    context: str,
) -> None:
    """Validate archived icons and require exact source bytes."""
    for icon_name, path in icons.items():
        archived = entry_map.get(path.as_posix())
        if archived is None:
            raise _error(context, f"declared icon is missing: {path}")
        source = _source_icon_data(source_dir, path, context)
        if archived != source:
            raise _error(context, f"archived icon bytes changed: {path}")
        try:
            validate_png_bytes(
                archived,
                EXPECTED_DIMENSIONS[icon_name],
                f"{context} {path.as_posix()}",
                icon_kind=icon_name,
            )
        except IconValidationError as error:
            raise _error(context, str(error)) from error


def _validate_connector_exclusion(
    manifest: dict[str, object],
    entry_names: set[str],
    context: str,
) -> None:
    """Reject connector declarations and connector draft members."""
    if "agentConnectors" in manifest:
        raise _error(context, "agentConnectors packaging remains deferred")
    if any(
        PurePosixPath(name).name.casefold() == CONNECTOR_DRAFT_NAME
        for name in entry_names
    ):
        raise _error(context, "connector draft must not be packaged")


def _validated_manifest(
    entry_map: dict[str, bytes],
    source_dir: Path,
    context: str,
) -> dict[str, object]:
    """Require semantic equality between archived and source manifests."""
    archived_data = entry_map.get("manifest.json")
    if archived_data is None:
        raise _error(context, "archive is missing manifest.json")
    archived = _load_json_bytes(
        archived_data,
        f"{context} archived manifest",
    )
    source = _load_json_path(source_dir / "manifest.json")
    if archived != source:
        raise _error(
            context,
            "archived manifest differs semantically from source",
        )
    return source


def _expected_archive_names(
    icons: dict[str, PurePosixPath],
    source_entries: dict[str, bytes],
) -> set[str]:
    """Return the complete allowed archive member set."""
    return {
        "manifest.json",
        *(path.as_posix() for path in icons.values()),
        *source_entries,
    }


def _validate_member_set(
    entry_names: set[str],
    expected_names: set[str],
    context: str,
) -> None:
    """Require the archive member set to match source inputs exactly."""
    if entry_names == expected_names:
        return
    missing = sorted(expected_names - entry_names)
    extra = sorted(entry_names - expected_names)
    raise _error(
        context,
        f"archive member set mismatch; missing={missing}, extra={extra}",
    )


def _validate_skill_bytes(
    entry_map: dict[str, bytes],
    source_entries: dict[str, bytes],
    context: str,
) -> None:
    """Require ATK to preserve every declared skill file byte-for-byte."""
    for name, source_data in source_entries.items():
        if entry_map[name] != source_data:
            raise _error(context, f"archived skill bytes changed: {name}")


def _validate_archive_contents(
    entries: list[ArchiveEntry],
    source_dir: Path,
    limits: Limits,
) -> None:
    """Validate package semantics and source-to-archive byte preservation."""
    context = source_dir.name
    entry_map = {entry.name: entry.data for entry in entries}
    source_manifest = _validated_manifest(entry_map, source_dir, context)
    icons = _manifest_icons(source_manifest, context)
    declared = _declared_skills(source_manifest, limits, context)
    _validate_source_skill_set(source_dir, declared, context)
    canonical_legal = _canonical_legal_data(source_dir, context)
    source_entries = _source_skill_entries(source_dir, declared, context)
    _validate_companion_limits(
        source_entries,
        declared,
        limits,
        context,
        "source",
    )
    _validate_skill_legal_names(
        set(source_entries),
        declared,
        context,
        "source",
    )
    _validate_required_skill_files(
        source_entries,
        declared,
        context,
        "source",
    )
    entry_names = set(entry_map)
    _validate_companion_limits(
        entry_map,
        declared,
        limits,
        context,
        "archive",
    )
    _validate_skill_legal_names(
        entry_names,
        declared,
        context,
        "archive",
    )
    _validate_required_skill_files(
        entry_map,
        declared,
        context,
        "archived",
    )
    _validate_distributed_legal_bytes(
        entry_map,
        declared,
        canonical_legal,
        context,
    )
    expected_names = _expected_archive_names(icons, source_entries)
    _validate_connector_exclusion(source_manifest, entry_names, context)
    _validate_member_set(entry_names, expected_names, context)
    _validate_icons(entry_map, source_dir, icons, context)
    _validate_skill_bytes(entry_map, source_entries, context)


def _normalized_info(name: str) -> zipfile.ZipInfo:
    """Create deterministic metadata for one regular ZIP member."""
    info = zipfile.ZipInfo(name, date_time=DOS_EPOCH)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = UNIX_CREATE_SYSTEM
    info.external_attr = FIXED_EXTERNAL_ATTR
    info.extra = b""
    info.comment = b""
    return info


def _write_normalized_archive(
    entries: list[ArchiveEntry],
    output_path: Path,
) -> None:
    """Write sorted member bytes with fixed ZIP metadata."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_name(f".{output_path.name}.part")
    temporary.unlink(missing_ok=True)
    try:
        with zipfile.ZipFile(
            temporary,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            archive.comment = b""
            for entry in sorted(entries):
                archive.writestr(
                    _normalized_info(entry.name),
                    entry.data,
                    compress_type=zipfile.ZIP_DEFLATED,
                    compresslevel=9,
                )
        temporary.replace(output_path)
    except OSError:
        temporary.unlink(missing_ok=True)
        raise


def _validate_normalized_info(
    info: zipfile.ZipInfo,
    context: str,
) -> None:
    """Require the fixed metadata contract on one normalized member."""
    _validate_fixed_encoding(info, context)
    _validate_fixed_permissions(info, context)
    _validate_stripped_metadata(info, context)


def _validate_fixed_encoding(
    info: zipfile.ZipInfo,
    context: str,
) -> None:
    """Require fixed timestamp and compression metadata."""
    if info.date_time != DOS_EPOCH:
        raise _error(context, f"timestamp was not normalized: {info.filename}")
    if info.compress_type != zipfile.ZIP_DEFLATED:
        raise _error(context, f"compression was not fixed: {info.filename}")


def _validate_fixed_permissions(
    info: zipfile.ZipInfo,
    context: str,
) -> None:
    """Require the fixed Unix regular-file permission metadata."""
    if info.create_system != UNIX_CREATE_SYSTEM:
        raise _error(context, f"platform was not fixed: {info.filename}")
    if info.external_attr != FIXED_EXTERNAL_ATTR:
        raise _error(context, f"permissions were not fixed: {info.filename}")


def _validate_stripped_metadata(
    info: zipfile.ZipInfo,
    context: str,
) -> None:
    """Require empty member extras and comments."""
    if info.extra or info.comment:
        raise _error(
            context,
            f"ZIP metadata was not stripped: {info.filename}",
        )


def _verify_archive_handle(
    archive: zipfile.ZipFile,
    expected: dict[str, bytes],
    context: str,
) -> None:
    """Verify normalized ordering, metadata, and member bytes."""
    infos = archive.infolist()
    names = [info.filename for info in infos]
    if names != sorted(expected):
        raise _error(context, "normalized members are not sorted")
    if archive.comment:
        raise _error(context, "normalized ZIP comment is not empty")
    _verify_archive_members(archive, infos, expected, context)


def _verify_archive_members(
    archive: zipfile.ZipFile,
    infos: list[zipfile.ZipInfo],
    expected: dict[str, bytes],
    context: str,
) -> None:
    """Verify fixed metadata and bytes for normalized members."""
    for info in infos:
        _validate_normalized_info(info, context)
        if archive.read(info) != expected[info.filename]:
            raise _error(
                context,
                f"normalized member bytes changed: {info.filename}",
            )


def _verify_normalized_archive(
    output_path: Path,
    entries: list[ArchiveEntry],
) -> None:
    """Reopen the normalized ZIP and verify metadata and member bytes."""
    expected = {entry.name: entry.data for entry in entries}
    context = output_path.as_posix()
    try:
        with zipfile.ZipFile(output_path) as archive:
            _verify_archive_handle(archive, expected, context)
    except zipfile.BadZipFile as error:
        raise _error(context, f"normalized ZIP is invalid: {error}") from error


def normalize_package(
    archive_path: Path,
    output_path: Path,
    source_dir: Path,
) -> str:
    """Validate and deterministically normalize one ATK package.

    Parameters
    ----------
    archive_path:
        Raw package ZIP emitted by Microsoft 365 Agents Toolkit.
    output_path:
        Destination for the normalized ZIP.
    source_dir:
        Canonical source package directory.

    Returns
    -------
    str
        SHA-256 digest of the normalized archive.

    Raises
    ------
    PackageBuildError
        If archive safety or package semantics fail validation.

    Notes
    -----
    Validation keeps general archive security limits separate from Cowork
    companion limits. Every ZIP member remains bounded by 20 MiB and the
    complete expanded archive remains bounded by 100 MiB. Companion files
    additionally use the official 5 MiB per-file and 10 MiB per-skill caps.

    Raw central-directory names are checked before ``zipfile`` can expose a
    NUL-truncated ``filename``. The same explicit ASCII segment policy is
    then applied to source paths and archive members. Manifest folder length
    is measured on the raw value, including the leading ``./``.

    The manifest skill set must exactly equal the source directory set.
    Source and archive companion counts, sizes, totals, and nesting depths
    are evaluated independently. Required legal copies must retain canonical
    names and package-root bytes. Icons, the manifest, every skill byte, and
    the complete member set must match source before deterministic metadata
    is written and verified by reopening the normalized archive.

    """
    if not source_dir.is_dir() or source_dir.is_symlink():
        raise _error(
            source_dir.as_posix(),
            "source must be a regular directory",
        )
    limits = load_limits()
    entries = _read_archive_entries(archive_path)
    _validate_archive_contents(entries, source_dir, limits)
    _write_normalized_archive(entries, output_path)
    _verify_normalized_archive(output_path, entries)
    return hashlib.sha256(output_path.read_bytes()).hexdigest()


def main() -> int:
    """Normalize paths supplied as ``RAW_ZIP OUTPUT_ZIP SOURCE_DIR``."""
    if len(sys.argv) != CLI_ARGUMENT_COUNT:
        sys.stderr.write(
            "usage: normalize_m365_cowork_package.py "
            "RAW_ZIP OUTPUT_ZIP SOURCE_DIR\n",
        )
        return 2
    archive_path, output_path, source_dir = map(Path, sys.argv[1:])
    try:
        digest = normalize_package(archive_path, output_path, source_dir)
    except (OSError, PackageBuildError) as error:
        sys.stderr.write(f"ERROR: {error}\n")
        return 1
    sys.stdout.write(f"{source_dir.name}\t{digest}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
