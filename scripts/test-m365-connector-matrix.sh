#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MATRIX="$ROOT/m365-cowork-ja/connectors/compatibility-matrix.json"
CATALOG="$ROOT/m365-cowork-ja/shared/package-catalog.json"

python3 - "$MATRIX" "$CATALOG" <<'PY'
import json
import pathlib
import sys
import urllib.parse

matrix = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
catalog = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
connectors = matrix["connectors"]

if len(connectors) != 20:
    raise SystemExit(f"expected 20 unique connectors, found {len(connectors)}")

names = [connector["sourceName"] for connector in connectors]
if len(names) != len(set(names)):
    raise SystemExit("duplicate connector sourceName")

known_plugins = set(catalog["packages"])
for connector in connectors:
    parsed = urllib.parse.urlparse(connector["url"])
    if parsed.scheme != "https" or not parsed.netloc:
        raise SystemExit(
            f"{connector['sourceName']} does not use a valid HTTPS URL"
        )
    unknown_plugins = set(connector["sourcePlugins"]) - known_plugins
    if unknown_plugins:
        raise SystemExit(
            f"{connector['sourceName']} has unknown plugins: "
            f"{sorted(unknown_plugins)}"
        )

by_name = {connector["sourceName"]: connector for connector in connectors}
for name in ("Asana", "Atlassian"):
    if by_name[name]["disposition"] != "adapter-required":
        raise SystemExit(f"{name} must require a Streamable HTTP adapter")

if by_name["cocounsel-legal"]["disposition"] != (
    "blocked-vendor-approval"
):
    raise SystemExit("CoCounsel must remain blocked")

for name in ("Slack", "Google Drive"):
    if by_name[name]["disposition"] != "m365-replacement-preferred":
        raise SystemExit(f"{name} must prefer a Microsoft 365 replacement")

print("M365 connector compatibility matrix: OK")
PY
