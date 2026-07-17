#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Shared strict parsing primitives for reference projection contracts."""

from __future__ import annotations

import re
import unicodedata
from pathlib import PurePosixPath
from typing import Final, cast

from m365_reference_projection_types import (
    ProjectionError,
    ProjectionTransform,
)

IDENTIFIER_RE: Final = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")


def require_object(value: object, context: str) -> dict[str, object]:
    """Require a JSON object."""
    if not isinstance(value, dict):
        message = f"{context} must be an object"
        raise ProjectionError(message)
    return cast("dict[str, object]", value)


def require_list(value: object, context: str) -> list[object]:
    """Require a JSON array."""
    if not isinstance(value, list):
        message = f"{context} must be an array"
        raise ProjectionError(message)
    return cast("list[object]", value)


def require_text(value: object, context: str) -> str:
    """Require a nonempty JSON string."""
    if not isinstance(value, str) or not value:
        message = f"{context} must be a nonempty string"
        raise ProjectionError(message)
    return value


def require_positive_int(value: object, context: str) -> int:
    """Require a positive JSON integer."""
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        message = f"{context} must be a positive integer"
        raise ProjectionError(message)
    return value


def require_exact_fields(
    value: dict[str, object],
    expected: frozenset[str],
    context: str,
) -> None:
    """Require an object's exact field set."""
    actual = frozenset(value)
    if actual == expected:
        return
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    message = f"{context} fields mismatch; missing={missing}, extra={extra}"
    raise ProjectionError(message)


def _has_unsafe_part(path: PurePosixPath) -> bool:
    """Return whether a path contains traversal or drive syntax."""
    return any(
        part in {".", ".."} or ":" in part
        for part in path.parts
    )


def require_relative_path(value: object, context: str) -> PurePosixPath:
    """Require one canonical relative POSIX path."""
    text = require_text(value, context)
    path = PurePosixPath(text)
    checks = (
        "\\" in text,
        path.is_absolute(),
        path.as_posix() != text,
        _has_unsafe_part(path),
        unicodedata.normalize("NFC", text) != text,
    )
    if any(checks):
        message = f"{context} is not a canonical relative path: {text!r}"
        raise ProjectionError(message)
    return path


def require_identifier(value: object, context: str) -> str:
    """Require one canonical package or skill identifier."""
    identifier = require_text(value, context)
    if IDENTIFIER_RE.fullmatch(identifier) is None:
        message = f"{context} is not a canonical identifier: {identifier!r}"
        raise ProjectionError(message)
    return identifier


def parse_byte_transform(
    value: object,
    context: str,
    expected_fields: frozenset[str],
) -> tuple[dict[str, object], ProjectionTransform]:
    """Parse fields shared by jurisdiction and root-common transforms."""
    transform = require_object(value, context)
    require_exact_fields(transform, expected_fields, context)
    fields = ProjectionTransform(
        package=require_identifier(
            transform.get("package"),
            f"{context}.package",
        ),
        path=require_relative_path(
            transform.get("path"),
            f"{context}.path",
        ),
        source=require_text(
            transform.get("from"),
            f"{context}.from",
        ).encode("utf-8"),
        replacement=require_text(
            transform.get("to"),
            f"{context}.to",
        ).encode("utf-8"),
        expected_occurrences=require_positive_int(
            transform.get("expectedOccurrences"),
            f"{context}.expectedOccurrences",
        ),
    )
    return transform, fields
