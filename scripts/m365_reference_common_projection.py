#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Validate flattened package-root common files copied into Cowork skills."""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath
from typing import Final

from m365_reference_contract import (
    parse_byte_transform as _parse_byte_transform,
)
from m365_reference_contract import (
    require_exact_fields as _require_exact_fields,
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
from m365_reference_projection_types import (
    CommonFileTransform,
    CommonProjectionContract,
    CommonProjectionReport,
    FileRecord,
    PackageContract,
    ProjectionError,
)

REQUIRED_CANONICAL_ROOT: Final = PurePosixPath("references")
REQUIRED_LOCAL_ROOT: Final = PurePosixPath("references/common")
REQUIRED_COPY_COUNT: Final = 45
PATH_SOURCE: Final = b"jurisdictions/ja-jp/"
PATH_REPLACEMENT: Final = b"ja-jp/"
CONTRACT_FIELDS: Final = frozenset({
    "canonicalRoot",
    "localRoot",
    "expectedTransformedCopyCount",
    "transforms",
})
TRANSFORM_FIELDS: Final = frozenset({
    "package",
    "path",
    "from",
    "to",
    "expectedOccurrences",
    "expectedCopyCount",
})
REQUIRED_TRANSFORMS: Final = (
    CommonFileTransform(
        "ai-governance-legal",
        PurePosixPath("currency-watch.md"),
        PATH_SOURCE,
        PATH_REPLACEMENT,
        1,
        10,
    ),
    CommonFileTransform(
        "ip-legal",
        PurePosixPath("original-ip-logic.md"),
        PATH_SOURCE,
        PATH_REPLACEMENT,
        1,
        12,
    ),
    CommonFileTransform(
        "product-legal",
        PurePosixPath("source-provenance-and-review.md"),
        PATH_SOURCE,
        PATH_REPLACEMENT,
        1,
        7,
    ),
    CommonFileTransform(
        "regulatory-legal",
        PurePosixPath("global-source-catalog.md"),
        PATH_SOURCE,
        PATH_REPLACEMENT,
        1,
        8,
    ),
    CommonFileTransform(
        "regulatory-legal",
        PurePosixPath("source-provenance-and-review.md"),
        PATH_SOURCE,
        PATH_REPLACEMENT,
        2,
        8,
    ),
)


def _parse_transform(
    value: object,
    index: int,
) -> CommonFileTransform:
    """Parse one flattened common-file transform."""
    context = f"commonFileProjection.transforms[{index}]"
    transform, fields = _parse_byte_transform(
        value,
        context,
        TRANSFORM_FIELDS,
    )
    return CommonFileTransform(
        *fields,
        _require_positive_int(
            transform.get("expectedCopyCount"),
            f"{context}.expectedCopyCount",
        ),
    )


def _parse_transforms(value: object) -> tuple[CommonFileTransform, ...]:
    """Parse and pin the five allowed common-file transforms."""
    items = _require_list(value, "commonFileProjection.transforms")
    transforms = tuple(
        _parse_transform(item, index)
        for index, item in enumerate(items)
    )
    if transforms != REQUIRED_TRANSFORMS:
        message = "commonFileProjection transforms changed"
        raise ProjectionError(message)
    return transforms


def _package_map(
    packages: tuple[PackageContract, ...],
) -> dict[str, PackageContract]:
    """Index package contracts by name."""
    return {package.name: package for package in packages}


def _validate_transform_counts(
    transforms: tuple[CommonFileTransform, ...],
    packages: tuple[PackageContract, ...],
) -> None:
    """Require each copy count to match exact registered skills."""
    by_name = _package_map(packages)
    for transform in transforms:
        package = by_name.get(transform.package)
        if package is None:
            message = (
                "common transform targets undeclared package "
                f"{transform.package}"
            )
            raise ProjectionError(message)
        if transform.expected_copy_count != len(package.registered_skills):
            message = (
                f"{transform.package}/{transform.path}: expectedCopyCount "
                "does not match registered skills"
            )
            raise ProjectionError(message)


def parse_common_projection(
    value: object,
    packages: tuple[PackageContract, ...],
) -> CommonProjectionContract:
    """Parse and strictly pin flattened common-file projection rules."""
    raw = _require_object(value, "commonFileProjection")
    _require_exact_fields(raw, CONTRACT_FIELDS, "commonFileProjection")
    canonical_root = _require_relative_path(
        raw.get("canonicalRoot"),
        "commonFileProjection.canonicalRoot",
    )
    local_root = _require_relative_path(
        raw.get("localRoot"),
        "commonFileProjection.localRoot",
    )
    roots = (canonical_root, local_root)
    required_roots = (REQUIRED_CANONICAL_ROOT, REQUIRED_LOCAL_ROOT)
    if roots != required_roots:
        message = f"common projection roots must remain {required_roots}"
        raise ProjectionError(message)
    expected_copy_count = _require_positive_int(
        raw.get("expectedTransformedCopyCount"),
        "commonFileProjection.expectedTransformedCopyCount",
    )
    if expected_copy_count != REQUIRED_COPY_COUNT:
        message = (
            "common transformed copy count must be "
            f"{REQUIRED_COPY_COUNT}"
        )
        raise ProjectionError(message)
    transforms = _parse_transforms(raw.get("transforms"))
    derived_copy_count = sum(
        transform.expected_copy_count
        for transform in transforms
    )
    if derived_copy_count != expected_copy_count:
        message = "common transform copy counts do not total 45"
        raise ProjectionError(message)
    _validate_transform_counts(transforms, packages)
    return CommonProjectionContract(
        canonical_root=canonical_root,
        local_root=local_root,
        expected_copy_count=expected_copy_count,
        transforms=transforms,
    )


def file_record(data: bytes) -> FileRecord:
    """Fingerprint bytes for independent size, hash, and value checks."""
    return FileRecord(
        data=data,
        size=len(data),
        sha256=hashlib.sha256(data).hexdigest(),
    )


def transformed_bytes(
    record: FileRecord,
    source: bytes,
    replacement: bytes,
    expected_occurrences: int,
    context: str,
) -> bytes:
    """Apply one occurrence-counted byte transform."""
    occurrences = record.data.count(source)
    if occurrences != expected_occurrences:
        message = (
            f"{context}: transform source occurrence count is {occurrences}; "
            f"expected {expected_occurrences}"
        )
        raise ProjectionError(message)
    return record.data.replace(source, replacement)


def compare_file_bytes(
    actual: FileRecord,
    expected_data: bytes,
    context: str,
) -> tuple[str, ...]:
    """Compare file size, SHA-256, and bytes independently."""
    expected = file_record(expected_data)
    errors: list[str] = []
    if actual.size != expected.size:
        errors.append(
            f"{context}: byte count mismatch; "
            f"expected={expected.size}, actual={actual.size}",
        )
    if actual.sha256 != expected.sha256:
        errors.append(
            f"{context}: SHA-256 mismatch; "
            f"expected={expected.sha256}, actual={actual.sha256}",
        )
    if actual.data != expected.data:
        errors.append(f"{context}: projected bytes differ")
    return tuple(errors)


def _is_regular_file(path: Path) -> bool:
    """Return whether a path is a non-symlink regular file."""
    return path.is_file() and not path.is_symlink()


def _canonical_expected(
    package_root: Path,
    contract: CommonProjectionContract,
    transform: CommonFileTransform,
) -> tuple[bytes | None, tuple[str, ...]]:
    """Read and transform one canonical root-common file."""
    path = (
        package_root
        / transform.package
        / Path(*contract.canonical_root.parts)
        / Path(*transform.path.parts)
    )
    if not _is_regular_file(path):
        return None, (f"{path}: canonical common file is missing",)
    record = file_record(path.read_bytes())
    try:
        expected = transformed_bytes(
            record,
            transform.source,
            transform.replacement,
            transform.expected_occurrences,
            path.as_posix(),
        )
    except ProjectionError as error:
        return None, (str(error),)
    return expected, ()


def _local_copy_result(
    path: Path,
    expected: bytes,
    transform: CommonFileTransform,
) -> tuple[tuple[str, ...], int]:
    """Validate one transformed local common-file copy."""
    if not _is_regular_file(path):
        return (f"{path}: common transformed copy is missing",), 0
    record = file_record(path.read_bytes())
    errors: list[str] = []
    if transform.source in record.data:
        errors.append(f"{path}: stale canonical path remains")
    errors.extend(compare_file_bytes(record, expected, path.as_posix()))
    return tuple(errors), 1


def _validate_transform(
    package_root: Path,
    contract: CommonProjectionContract,
    package: PackageContract,
    transform: CommonFileTransform,
) -> CommonProjectionReport:
    """Validate one canonical file and all registered skill copies."""
    expected, canonical_errors = _canonical_expected(
        package_root,
        contract,
        transform,
    )
    if expected is None:
        return CommonProjectionReport(canonical_errors, 0)
    errors = list(canonical_errors)
    observed = 0
    for skill in package.registered_skills:
        path = (
            package_root
            / transform.package
            / "skills"
            / skill
            / Path(*contract.local_root.parts)
            / Path(*transform.path.parts)
        )
        copy_errors, copy_count = _local_copy_result(
            path,
            expected,
            transform,
        )
        errors.extend(copy_errors)
        observed += copy_count
    return CommonProjectionReport(tuple(errors), observed)


def validate_common_projection(
    package_root: Path,
    contract: CommonProjectionContract,
    packages: tuple[PackageContract, ...],
) -> CommonProjectionReport:
    """Validate all 45 transformed root-common file copies."""
    if package_root.is_symlink() or not package_root.is_dir():
        return CommonProjectionReport(
            (f"{package_root}: package root must be a directory",),
            0,
        )
    by_name = _package_map(packages)
    errors: list[str] = []
    observed = 0
    for transform in contract.transforms:
        report = _validate_transform(
            package_root,
            contract,
            by_name[transform.package],
            transform,
        )
        errors.extend(report.errors)
        observed += report.observed_copy_count
    if observed != contract.expected_copy_count:
        errors.append(
            "common transformed copy total mismatch; "
            f"expected={contract.expected_copy_count}, actual={observed}",
        )
    return CommonProjectionReport(tuple(errors), observed)
