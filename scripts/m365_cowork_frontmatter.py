#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Parse the restricted frontmatter used by Microsoft 365 Cowork skills."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from pathlib import Path

FRONTMATTER_FIELD_RE: Final = re.compile(
    r"^([A-Za-z][A-Za-z0-9_-]*):",
)
BLOCK_MARKERS: Final = frozenset({">", ">-", ">+", "|", "|-", "|+"})


def extract_frontmatter(text: str, path: Path) -> tuple[str, ...]:
    """Extract frontmatter lines from a Markdown document.

    Parameters
    ----------
    text:
        Full Markdown text.
    path:
        Source path used in error messages.

    Returns
    -------
    tuple[str, ...]
        Lines between the opening and closing frontmatter boundaries.

    Raises
    ------
    ValueError
        If the document does not contain closed frontmatter.

    """
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        message = f"{path.as_posix()} has no opening frontmatter boundary"
        raise ValueError(message)
    try:
        closing_index = lines.index("---", 1)
    except ValueError as error:
        message = f"{path.as_posix()} has no closing frontmatter boundary"
        raise ValueError(message) from error
    return tuple(lines[1:closing_index])


def frontmatter_fields(lines: tuple[str, ...]) -> tuple[str, ...]:
    """Return unique top-level frontmatter field names.

    Parameters
    ----------
    lines:
        Frontmatter lines.

    Returns
    -------
    tuple[str, ...]
        Sorted field names.

    """
    fields = {
        match.group(1)
        for line in lines
        if (match := FRONTMATTER_FIELD_RE.match(line)) is not None
    }
    return tuple(sorted(fields))


def frontmatter_scalar(
    lines: tuple[str, ...],
    field: str,
) -> str | None:
    """Return an inline scalar frontmatter value when present.

    Parameters
    ----------
    lines:
        Frontmatter lines.
    field:
        Field to locate.

    Returns
    -------
    str | None
        Trimmed inline value, or ``None`` when absent or block-valued.

    """
    prefix = f"{field}:"
    for line in lines:
        if not line.startswith(prefix):
            continue
        value = line.removeprefix(prefix).strip()
        if value in BLOCK_MARKERS:
            return None
        return value.strip("\"'")
    return None


def frontmatter_text(
    lines: tuple[str, ...],
    field: str,
) -> str | None:
    """Return an inline or block frontmatter text value.

    Parameters
    ----------
    lines:
        Frontmatter lines.
    field:
        Field to locate.

    Returns
    -------
    str | None
        Normalized text, or ``None`` when absent.

    """
    prefix = f"{field}:"
    for index, line in enumerate(lines):
        if not line.startswith(prefix):
            continue
        value = line.removeprefix(prefix).strip()
        if value not in BLOCK_MARKERS:
            return value.strip("\"'")
        block_lines = _indented_block(lines[index + 1:])
        separator = "\n" if value.startswith("|") else " "
        return separator.join(block_lines).strip()
    return None


def _indented_block(lines: tuple[str, ...]) -> tuple[str, ...]:
    """Return normalized lines from an indented YAML block scalar.

    Parameters
    ----------
    lines:
        Candidate lines after the block marker.

    Returns
    -------
    tuple[str, ...]
        Block content up to the next top-level field.

    """
    content: list[str] = []
    for line in lines:
        if FRONTMATTER_FIELD_RE.match(line) is not None:
            break
        if line and not line[0].isspace():
            break
        content.append(line.strip())
    return tuple(content)
