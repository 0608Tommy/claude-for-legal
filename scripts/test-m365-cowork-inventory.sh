#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INVENTORY="$ROOT/m365-cowork-ja/shared/source-inventory.json"

python3 "$ROOT/scripts/build_m365_cowork_inventory.py" >/dev/null

python3 - "$INVENTORY" <<'PY'
import json
import pathlib
import sys

inventory_path = pathlib.Path(sys.argv[1])
inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
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

print("m365 Cowork source inventory: OK")
PY
