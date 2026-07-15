#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INVENTORY="$ROOT/m365-cowork-ja/shared/source-inventory.json"
MIGRATION_MAP="$ROOT/m365-cowork-ja/shared/migration-map.json"
PACKAGE_CATALOG="$ROOT/m365-cowork-ja/shared/package-catalog.json"

python3 "$ROOT/scripts/build_m365_cowork_inventory.py" >/dev/null

python3 - "$INVENTORY" "$MIGRATION_MAP" "$PACKAGE_CATALOG" <<'PY'
import json
import pathlib
import sys

inventory_path = pathlib.Path(sys.argv[1])
migration_map_path = pathlib.Path(sys.argv[2])
inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
migration_map = json.loads(
    migration_map_path.read_text(encoding="utf-8")
)
package_catalog = json.loads(
    pathlib.Path(sys.argv[3]).read_text(encoding="utf-8")
)
summary = inventory["summary"]

expected = {
    "pluginCount": 13,
    "firstPartyPluginCount": 12,
    "vendorPluginCount": 1,
    "skillCount": 151,
    "agentCount": 10,
    "cookbookCount": 5,
    "connectorDeclarationCount": 52,
    "skillsWithUnsupportedFrontmatter": 143,
    "unsupportedFrontmatterOccurrences": 144,
    "skillsOverStrictCharacterLimit": 36,
}

if summary != expected:
    raise SystemExit(
        "source inventory changed; review and update the migration contract\n"
        f"expected={expected}\nactual={summary}"
    )

invalid_target_ids = [
    skill["targetId"]
    for plugin in inventory["plugins"]
    for skill in plugin["skills"]
    if not skill["validTargetId"]
]
if invalid_target_ids:
    raise SystemExit(f"invalid target skill IDs: {invalid_target_ids}")

oversized_packages = [
    plugin["sourcePlugin"]
    for plugin in inventory["plugins"]
    if plugin["registeredSkillCount"] > 20
]
if oversized_packages:
    raise SystemExit(
        f"packages exceed the 20-skill limit: {oversized_packages}"
    )

connector_overages = [
    plugin["sourcePlugin"]
    for plugin in inventory["plugins"]
    if plugin["connectorCount"] > 10
]
if connector_overages:
    raise SystemExit(
        f"packages exceed the 10-connector limit: {connector_overages}"
    )

source_skills = {
    f"{plugin['sourcePlugin']}/{skill['targetId']}"
    for plugin in inventory["plugins"]
    for skill in plugin["skills"]
}
mapped_skills = {
    f"{plugin_id}/{skill_id}"
    for plugin_id, dispositions in migration_map["plugins"].items()
    for disposition in (
        "direct",
        "powerPlatform",
        "admin",
        "internalReference",
        "unsupported",
    )
    for skill_id in dispositions[disposition]
}

if source_skills != mapped_skills:
    raise SystemExit(
        "migration map coverage mismatch\n"
        f"missing={sorted(source_skills - mapped_skills)}\n"
        f"unknown={sorted(mapped_skills - source_skills)}"
    )

disposition_counts = {
    disposition: sum(
        len(dispositions[disposition])
        for dispositions in migration_map["plugins"].values()
    )
    for disposition in (
        "direct",
        "powerPlatform",
        "admin",
        "internalReference",
        "unsupported",
    )
}
expected_dispositions = {
    "direct": 71,
    "powerPlatform": 38,
    "admin": 32,
    "internalReference": 9,
    "unsupported": 1,
}
if disposition_counts != expected_dispositions:
    raise SystemExit(
        "migration disposition counts changed\n"
        f"expected={expected_dispositions}\n"
        f"actual={disposition_counts}"
    )

catalog_plugins = set(package_catalog["packages"])
inventory_plugins = {
    plugin["sourcePlugin"] for plugin in inventory["plugins"]
}
if catalog_plugins != inventory_plugins:
    raise SystemExit(
        "package catalog coverage mismatch\n"
        f"missing={sorted(inventory_plugins - catalog_plugins)}\n"
        f"unknown={sorted(catalog_plugins - inventory_plugins)}"
    )

app_ids = [
    package["appId"]
    for package in package_catalog["packages"].values()
]
if len(app_ids) != len(set(app_ids)):
    raise SystemExit("package catalog contains duplicate app IDs")

print("m365 Cowork source inventory: OK")
PY
