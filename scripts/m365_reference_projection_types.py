#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Typed models for the Microsoft 365 reference projection contract."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from pathlib import PurePosixPath


class ProjectionError(ValueError):
    """Report an invalid projection contract or filesystem projection."""


class ProjectionTotals(NamedTuple):
    """Hold fleet-wide projection counts."""

    package_count: int
    registered_skill_count: int
    canonical_file_count: int
    projected_file_count: int


class ProjectionTransform(NamedTuple):
    """Describe one explicit canonical-to-local byte transform."""

    package: str
    path: PurePosixPath
    source: bytes
    replacement: bytes
    expected_occurrences: int


class CommonFileTransform(NamedTuple):
    """Describe one root-common canonical-to-local byte transform."""

    package: str
    path: PurePosixPath
    source: bytes
    replacement: bytes
    expected_occurrences: int
    expected_copy_count: int


class CommonProjectionContract(NamedTuple):
    """Hold exact flattened common-file projection rules."""

    canonical_root: PurePosixPath
    local_root: PurePosixPath
    expected_copy_count: int
    transforms: tuple[CommonFileTransform, ...]


class PackageContract(NamedTuple):
    """Describe one package's exact registered projection surface."""

    name: str
    expected_skill_count: int
    expected_files_per_skill: int
    expected_projected_file_count: int
    registered_skills: tuple[str, ...]
    canonical_files: tuple[PurePosixPath, ...]


class ProjectionContract(NamedTuple):
    """Hold the validated machine-readable projection contract."""

    canonical_root: PurePosixPath
    local_root: PurePosixPath
    forbidden_local_root: PurePosixPath
    common_projection: CommonProjectionContract
    expected_totals: ProjectionTotals
    packages: tuple[PackageContract, ...]
    transforms: tuple[ProjectionTransform, ...]


class FileRecord(NamedTuple):
    """Hold bytes and independently computed file fingerprints."""

    data: bytes
    size: int
    sha256: str


class TreeSnapshot(NamedTuple):
    """Hold a checked filesystem tree and structural errors."""

    files: dict[PurePosixPath, FileRecord]
    errors: tuple[str, ...]


class PackageOutcome(NamedTuple):
    """Hold one package's validation result and observed counts."""

    errors: tuple[str, ...]
    registered_skill_count: int
    canonical_file_count: int
    projected_file_count: int


class ValidationReport(NamedTuple):
    """Hold all projection errors and observed fleet counts."""

    errors: tuple[str, ...]
    observed_totals: ProjectionTotals


class CommonProjectionReport(NamedTuple):
    """Hold flattened common-file errors and observed copy count."""

    errors: tuple[str, ...]
    observed_copy_count: int
