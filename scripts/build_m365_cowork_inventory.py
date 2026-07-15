#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Build the source inventory for the Japanese Copilot Cowork target."""

from __future__ import annotations

import json
import re
import sys
from itertools import chain
from pathlib import Path
from typing import Final, cast

ROOT: Final = Path(__file__).resolve().parent.parent
TARGET_ROOT: Final = ROOT / "m365-cowork-ja"
OUTPUT_PATH: Final = TARGET_ROOT / "shared" / "source-inventory.json"
STRICT_CHARACTER_LIMIT: Final = 20_000
ALLOWED_FRONTMATTER: Final = frozenset(
    {"name", "description", "license", "metadata", "compatibility"},
)
ADMIN_FLOW_SKILLS: Final = frozenset(
    {
        ("legal-builder-hub", "auto-updater"),
        ("legal-builder-hub", "disable"),
        ("legal-builder-hub", "skill-installer"),
        ("legal-builder-hub", "uninstall"),
    },
)
FRONTMATTER_FIELD_RE: Final = re.compile(
    r"^([A-Za-z][A-Za-z0-9_-]*):",
)
TARGET_ID_RE: Final = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")


def _relative(path: Path) -> str:
    """Return a repository-relative POSIX path.

    Parameters
    ----------
    path:
        Path within the repository.

    Returns
    -------
    str
        Repository-relative path.

    """
    return path.relative_to(ROOT).as_posix()


def _frontmatter_lines(text: str, path: Path) -> tuple[str, ...]:
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
        message = f"{_relative(path)} has no opening frontmatter boundary"
        raise ValueError(message)
    try:
        closing_index = lines.index("---", 1)
    except ValueError as error:
        message = f"{_relative(path)} has no closing frontmatter boundary"
        raise ValueError(message) from error
    return tuple(lines[1:closing_index])


def _frontmatter_fields(lines: tuple[str, ...]) -> tuple[str, ...]:
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


def _frontmatter_value(
    lines: tuple[str, ...],
    field: str,
) -> str | None:
    """Return a scalar frontmatter value when present.

    Parameters
    ----------
    lines:
        Frontmatter lines.
    field:
        Field to locate.

    Returns
    -------
    str | None
        Trimmed scalar value, or ``None`` when absent.

    """
    prefix = f"{field}:"
    for line in lines:
        if line.startswith(prefix):
            value = line.removeprefix(prefix).strip()
            return value.strip("\"'")
    return None


def _is_internal_helper(lines: tuple[str, ...]) -> bool:
    """Return whether source frontmatter hides the skill from users.

    Parameters
    ----------
    lines:
        Frontmatter lines.

    Returns
    -------
    bool
        ``True`` for ``user-invocable: false``.

    """
    value = _frontmatter_value(lines, "user-invocable")
    return value == "false"


def _disposition(
    plugin_id: str,
    skill_id: str,
    *,
    internal_helper: bool,
) -> str:
    """Select the initial target disposition for a source skill.

    Parameters
    ----------
    plugin_id:
        Source plugin identifier.
    skill_id:
        Source skill directory identifier.
    internal_helper:
        Whether the source hides the skill from direct invocation.

    Returns
    -------
    str
        Initial migration disposition.

    """
    if internal_helper:
        return "internal-reference"
    if (plugin_id, skill_id) in ADMIN_FLOW_SKILLS:
        return "admin-approval-flow"
    return "cowork-skill"


def _skill_record(plugin_id: str, skill_path: Path) -> dict[str, object]:
    """Build one skill inventory record.

    Parameters
    ----------
    plugin_id:
        Source plugin identifier.
    skill_path:
        Path to ``SKILL.md``.

    Returns
    -------
    dict[str, object]
        JSON-serializable skill record.

    """
    text = skill_path.read_text(encoding="utf-8")
    frontmatter = _frontmatter_lines(text, skill_path)
    fields = _frontmatter_fields(frontmatter)
    source_id = _frontmatter_value(frontmatter, "name")
    target_id = skill_path.parent.name
    internal_helper = _is_internal_helper(frontmatter)
    unsupported_fields = tuple(
        field for field in fields if field not in ALLOWED_FRONTMATTER
    )
    disposition = _disposition(
        plugin_id,
        target_id,
        internal_helper=internal_helper,
    )
    return {
        "sourceId": source_id or target_id,
        "targetId": target_id,
        "sourcePath": _relative(skill_path),
        "disposition": disposition,
        "registeredInCowork": disposition != "internal-reference",
        "frontmatterFields": fields,
        "unsupportedFrontmatterFields": unsupported_fields,
        "characters": len(text),
        "lines": len(text.splitlines()),
        "overStrictCharacterLimit": len(text) > STRICT_CHARACTER_LIMIT,
        "validTargetId": TARGET_ID_RE.fullmatch(target_id) is not None,
    }


def _agent_record(agent_path: Path) -> dict[str, object]:
    """Build one Markdown agent inventory record.

    Parameters
    ----------
    agent_path:
        Path to an agent Markdown file.

    Returns
    -------
    dict[str, object]
        JSON-serializable agent record.

    """
    text = agent_path.read_text(encoding="utf-8")
    frontmatter = _frontmatter_lines(text, agent_path)
    source_id = _frontmatter_value(frontmatter, "name")
    return {
        "sourceId": source_id or agent_path.stem,
        "sourcePath": _relative(agent_path),
        "disposition": "power-platform-automation",
    }


def _connector_count(plugin_path: Path) -> int:
    """Count MCP server declarations for a plugin.

    Parameters
    ----------
    plugin_path:
        Source plugin directory.

    Returns
    -------
    int
        Number of declared MCP servers.

    """
    manifest_path = plugin_path / ".mcp.json"
    if not manifest_path.is_file():
        return 0
    raw_document: object = json.loads(
        manifest_path.read_text(encoding="utf-8"),
    )
    if not isinstance(raw_document, dict):
        message = f"{_relative(manifest_path)} must contain a JSON object"
        raise TypeError(message)
    document = cast("dict[str, object]", raw_document)
    raw_servers = document.get("mcpServers")
    if not isinstance(raw_servers, dict):
        return 0
    servers = cast("dict[str, object]", raw_servers)
    return len(servers)


def _plugin_manifest_paths(root: Path) -> tuple[Path, ...]:
    """Discover first-party and vendor plugin manifests.

    Parameters
    ----------
    root:
        Repository root.

    Returns
    -------
    tuple[Path, ...]
        Sorted plugin manifest paths.

    """
    paths = chain(
        root.glob("*/.claude-plugin/plugin.json"),
        root.glob("external_plugins/*/.claude-plugin/plugin.json"),
    )
    return tuple(sorted(paths))


def _plugin_record(manifest_path: Path) -> dict[str, object]:
    """Build one plugin inventory record.

    Parameters
    ----------
    manifest_path:
        Path to the Claude plugin manifest.

    Returns
    -------
    dict[str, object]
        JSON-serializable plugin record.

    """
    plugin_path = manifest_path.parent.parent
    plugin_id = plugin_path.name
    skill_paths = tuple(sorted(plugin_path.glob("skills/*/SKILL.md")))
    agent_paths = tuple(sorted(plugin_path.glob("agents/*.md")))
    skills = [_skill_record(plugin_id, path) for path in skill_paths]
    agents = [_agent_record(path) for path in agent_paths]
    registered_count = sum(
        record["registeredInCowork"] is True for record in skills
    )
    source_kind = (
        "vendor"
        if "external_plugins" in plugin_path.parts
        else "first-party"
    )
    return {
        "sourcePlugin": plugin_id,
        "sourceKind": source_kind,
        "sourcePath": _relative(plugin_path),
        "skillCount": len(skills),
        "registeredSkillCount": registered_count,
        "agentCount": len(agents),
        "connectorCount": _connector_count(plugin_path),
        "skills": skills,
        "agents": agents,
    }


def _cookbook_records(root: Path) -> list[dict[str, object]]:
    """Build managed-agent cookbook records.

    Parameters
    ----------
    root:
        Repository root.

    Returns
    -------
    list[dict[str, object]]
        JSON-serializable cookbook records.

    """
    records: list[dict[str, object]] = []
    pattern = "managed-agent-cookbooks/*/agent.yaml"
    for agent_path in sorted(root.glob(pattern)):
        cookbook_path = agent_path.parent
        leaves = tuple(sorted(cookbook_path.glob("subagents/*.yaml")))
        records.append(
            {
                "sourceId": cookbook_path.name,
                "sourcePath": _relative(cookbook_path),
                "leafCount": len(leaves),
                "disposition": "power-platform-solution",
            },
        )
    return records


def build_inventory(root: Path = ROOT) -> dict[str, object]:
    """Build the complete source inventory.

    Parameters
    ----------
    root:
        Repository root.

    Returns
    -------
    dict[str, object]
        JSON-serializable source inventory.

    """
    plugins = [
        _plugin_record(path)
        for path in _plugin_manifest_paths(root)
    ]
    skill_records = [
        cast("dict[str, object]", skill)
        for plugin in plugins
        for skill in cast("list[object]", plugin["skills"])
    ]
    unsupported_skill_count = sum(
        bool(record["unsupportedFrontmatterFields"])
        for record in skill_records
    )
    unsupported_field_count = sum(
        len(cast("tuple[str, ...]", record["unsupportedFrontmatterFields"]))
        for record in skill_records
    )
    oversized_skill_count = sum(
        record["overStrictCharacterLimit"] is True
        for record in skill_records
    )
    agent_count = sum(
        cast("int", plugin["agentCount"]) for plugin in plugins
    )
    connector_count = sum(
        cast("int", plugin["connectorCount"]) for plugin in plugins
    )
    cookbooks = _cookbook_records(root)
    return {
        "schemaVersion": 1,
        "sourceRoot": ".",
        "summary": {
            "pluginCount": len(plugins),
            "firstPartyPluginCount": sum(
                plugin["sourceKind"] == "first-party"
                for plugin in plugins
            ),
            "vendorPluginCount": sum(
                plugin["sourceKind"] == "vendor"
                for plugin in plugins
            ),
            "skillCount": len(skill_records),
            "agentCount": agent_count,
            "cookbookCount": len(cookbooks),
            "connectorDeclarationCount": connector_count,
            "skillsWithUnsupportedFrontmatter": (
                unsupported_skill_count
            ),
            "unsupportedFrontmatterOccurrences": unsupported_field_count,
            "skillsOverStrictCharacterLimit": oversized_skill_count,
        },
        "plugins": plugins,
        "cookbooks": cookbooks,
    }


def write_inventory(output_path: Path = OUTPUT_PATH) -> None:
    """Write the complete source inventory.

    Parameters
    ----------
    output_path:
        Destination JSON path.

    """
    inventory = build_inventory()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    """Write the default inventory and return a process status.

    Returns
    -------
    int
        Zero on success.

    """
    write_inventory()
    sys.stdout.write(f"{_relative(OUTPUT_PATH)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
