#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MATRIX="$ROOT/m365-cowork-ja/connectors/compatibility-matrix.json"
CATALOG="$ROOT/m365-cowork-ja/shared/package-catalog.json"
PACKAGES="$ROOT/m365-cowork-ja/cowork-packages"
DIST="$ROOT/m365-cowork-ja/dist"

python3 - "$MATRIX" "$CATALOG" "$PACKAGES" "$DIST" <<'PY'
import json
import pathlib
import sys
import urllib.parse
import zipfile

matrix = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
catalog = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
packages_path = pathlib.Path(sys.argv[3])
dist_path = pathlib.Path(sys.argv[4])
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

if by_name["CourtListener"]["disposition"] != "tenant-validation-required":
    raise SystemExit("CourtListener must preserve tenant validation")

if by_name["Trellis"]["disposition"] != (
    "adapter-and-vendor-validation-required"
):
    raise SystemExit("Trellis must require an adapter and vendor validation")

expected_by_plugin = {plugin: {} for plugin in known_plugins}
for connector in connectors:
    for plugin in connector["sourcePlugins"]:
        expected_by_plugin[plugin][connector["sourceName"]] = connector


def manifest_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from manifest_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from manifest_strings(item)


def assert_manifest_excludes_drafts(manifest, label):
    if "agentConnectors" in manifest:
        raise SystemExit(f"{label} must not contain agentConnectors")
    if any(
        "connectors.draft.json" in value
        for value in manifest_strings(manifest)
    ):
        raise SystemExit(f"{label} must not reference connectors.draft.json")


draft_paths = sorted(packages_path.glob("*/connectors.draft.json"))
if not draft_paths:
    raise SystemExit("no package connector drafts found")

for draft_path in draft_paths:
    plugin = draft_path.parent.name
    if plugin not in known_plugins:
        raise SystemExit(f"{draft_path}: unknown package")

    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    draft_connectors = draft["connectors"]
    draft_names = [connector["id"] for connector in draft_connectors]
    if len(draft_names) != len(set(draft_names)):
        raise SystemExit(f"{draft_path}: duplicate connector id")

    expected = expected_by_plugin[plugin]
    if set(draft_names) != set(expected):
        raise SystemExit(
            f"{draft_path}: connector membership differs from matrix\n"
            f"expected={sorted(expected)}\nactual={sorted(draft_names)}"
        )

    uses_source_contract = any(
        "sourceUrl" in connector
        or "sourceTransport" in connector
        or "disposition" in connector
        for connector in draft_connectors
    )
    for connector in draft_connectors:
        name = connector["id"]
        urls = [
            connector[field]
            for field in ("sourceUrl", "url")
            if field in connector
        ]
        if len(urls) != 1:
            raise SystemExit(
                f"{draft_path}: {name} must declare exactly one source URL"
            )
        if urls[0] != expected[name]["url"]:
            raise SystemExit(
                f"{draft_path}: {name} URL differs from matrix\n"
                f"expected={expected[name]['url']}\nactual={urls[0]}"
            )
        if uses_source_contract:
            if "sourceUrl" not in connector or "disposition" not in connector:
                raise SystemExit(
                    f"{draft_path}: {name} has an incomplete source contract"
                )
            if connector["disposition"] != expected[name]["disposition"]:
                raise SystemExit(
                    f"{draft_path}: {name} disposition differs from matrix\n"
                    f"expected={expected[name]['disposition']}\n"
                    f"actual={connector['disposition']}"
                )

for manifest_path in sorted(packages_path.glob("*/manifest.json")):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert_manifest_excludes_drafts(manifest, str(manifest_path))

zip_paths = sorted(packages_path.glob("*/build/*.zip"))
zip_paths.extend(sorted(dist_path.glob("*/*.zip")))
for zip_path in zip_paths:
    with zipfile.ZipFile(zip_path) as archive:
        archive_names = archive.namelist()
        draft_entries = [
            name
            for name in archive_names
            if pathlib.PurePosixPath(name).name == "connectors.draft.json"
        ]
        if draft_entries:
            raise SystemExit(
                f"{zip_path}: connector drafts were packaged: {draft_entries}"
            )
        archived_manifests = [
            name
            for name in archive_names
            if pathlib.PurePosixPath(name).name == "manifest.json"
        ]
        for archived_manifest in archived_manifests:
            manifest = json.loads(archive.read(archived_manifest))
            assert_manifest_excludes_drafts(
                manifest, f"{zip_path}:{archived_manifest}"
            )

print("M365 connector compatibility matrix: OK")
PY
