#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Add Apache-2.0 change notices to Japanese Cowork Markdown files."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parent.parent
TARGET_ROOT: Final = ROOT / "m365-cowork-ja" / "cowork-packages"
SOURCE_REVISION: Final = "5ceb305b30b4c82653c9b6642499c12e946ec319"
NOTICE_MARKER: Final = "> **変更通知:**"
NOTICE_TEXT: Final = (
    f"{NOTICE_MARKER} `anthropics/claude-for-legal`"
    f" (source revision `{SOURCE_REVISION}`) を日本語化し、"
    "Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。"
)


def _skill_notice(text: str, path: Path) -> str:
    """Insert a notice after strict skill frontmatter.

    Parameters
    ----------
    text:
        Skill Markdown text.
    path:
        Skill path used in error messages.

    Returns
    -------
    str
        Markdown containing the notice.

    Raises
    ------
    ValueError
        If a skill has no closed frontmatter.

    """
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        message = f"{path.as_posix()} has no opening frontmatter"
        raise ValueError(message)
    try:
        closing_index = lines.index("---", 1)
    except ValueError as error:
        message = f"{path.as_posix()} has no closing frontmatter"
        raise ValueError(message) from error
    output = [
        *lines[:closing_index + 1],
        "",
        NOTICE_TEXT,
        "",
        *lines[closing_index + 1:],
    ]
    return "\n".join(output).rstrip() + "\n"


def _markdown_notice(text: str) -> str:
    """Prepend a notice to a non-skill Markdown file.

    Parameters
    ----------
    text:
        Markdown text.

    Returns
    -------
    str
        Markdown containing the notice.

    """
    return f"{NOTICE_TEXT}\n\n{text.lstrip()}".rstrip() + "\n"


def add_notice(path: Path) -> bool:
    """Add a change notice to one Markdown file.

    Parameters
    ----------
    path:
        Markdown file to update.

    Returns
    -------
    bool
        ``True`` when the file changed.

    """
    text = path.read_text(encoding="utf-8")
    if NOTICE_MARKER in text:
        return False
    updated = (
        _skill_notice(text, path)
        if path.name == "SKILL.md"
        else _markdown_notice(text)
    )
    path.write_text(updated, encoding="utf-8")
    return True


def apply_notices(target_root: Path = TARGET_ROOT) -> int:
    """Apply notices to every package Markdown file.

    Parameters
    ----------
    target_root:
        Directory containing Cowork package sources.

    Returns
    -------
    int
        Number of changed files.

    """
    return sum(
        add_notice(path)
        for path in sorted(target_root.rglob("*.md"))
        if "build" not in path.parts
    )


def main() -> int:
    """Apply notices to the default target root.

    Returns
    -------
    int
        Zero on success.

    """
    changed = apply_notices()
    sys.stdout.write(f"Applied Apache change notices to {changed} files.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
