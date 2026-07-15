#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CATALOG="$ROOT/m365-cowork-ja/power-platform-solutions/agent-catalog.json"
IDENTITIES="$ROOT/m365-cowork-ja/power-platform-solutions/governance/identity-model.json"
APPROVAL="$ROOT/m365-cowork-ja/power-platform-solutions/governance/approval-policy.json"

python3 - "$CATALOG" "$IDENTITIES" "$APPROVAL" <<'PY'
import json
import pathlib
import sys

catalog = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
identities = json.loads(
    pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
)
approval = json.loads(pathlib.Path(sys.argv[3]).read_text(encoding="utf-8"))

agents = catalog["agents"]
if len(agents) != 10:
    raise SystemExit(f"expected 10 automation contracts, found {len(agents)}")

agent_keys = [agent["agentKey"] for agent in agents]
if len(agent_keys) != len(set(agent_keys)):
    raise SystemExit("duplicate automation agentKey")

solution_names = [agent["solutionUniqueName"] for agent in agents]
if len(solution_names) != len(set(solution_names)):
    raise SystemExit("duplicate Power Platform solution unique name")

if catalog["activationDefault"] is not False:
    raise SystemExit("automation must be disabled by default")

for agent in agents:
    if len(agent["stages"]) < 4:
        raise SystemExit(
            f"{agent['agentKey']} must preserve staged isolation"
        )
    if not agent["sourceAgent"].endswith(".md"):
        raise SystemExit(
            f"{agent['agentKey']} has no canonical source agent"
        )

required_identities = {
    "spn-legal-deployer",
    "spn-legal-runtime",
    "spn-legal-reader",
    "spn-legal-analyzer",
    "spn-legal-writer",
    "spn-legal-delivery",
}
if set(identities["identities"]) != required_identities:
    raise SystemExit("identity model does not contain the required tiers")

if not approval["freshApprovalRequiredFor"]:
    raise SystemExit("approval policy has no consequential actions")

print("Power Platform automation contracts: OK")
PY
