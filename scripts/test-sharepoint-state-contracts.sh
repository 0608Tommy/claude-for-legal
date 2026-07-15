#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STATE_ROOT="$ROOT/m365-cowork-ja/state-service"

python3 - "$STATE_ROOT" <<'PY'
import json
import pathlib
import sys

import jsonschema

root = pathlib.Path(sys.argv[1])
schemas = {
    path.stem.replace(".schema", ""): json.loads(
        path.read_text(encoding="utf-8")
    )
    for path in (root / "schemas").glob("*.schema.json")
}
layout = json.loads(
    (root / "sharepoint-layout.json").read_text(encoding="utf-8")
)

required_schemas = {
    "state-envelope",
    "create-request",
    "update-request",
    "session-binding",
    "audit-event",
}
if set(schemas) != required_schemas:
    raise SystemExit(
        f"state schema coverage mismatch: {sorted(schemas)}"
    )

for name, schema in schemas.items():
    if schema.get("additionalProperties") is not False:
        raise SystemExit(f"{name} must reject additional properties")

create_fixture = {
    "tenantId": "tenant-1",
    "practiceId": "commercial",
    "scopeType": "matter",
    "scopeId": "matter-1",
    "recordType": "renewal",
    "recordId": "ren-001",
    "idempotencyKey": "renewal-create-0001",
    "expectedAbsent": True,
    "payload": {"status": "active"},
}
jsonschema.validate(create_fixture, schemas["create-request"])

update_fixture = {
    "tenantId": "tenant-1",
    "practiceId": "commercial",
    "scopeType": "matter",
    "scopeId": "matter-1",
    "recordType": "renewal",
    "recordId": "ren-001",
    "itemId": "42",
    "eTag": "\"7\"",
    "idempotencyKey": "renewal-update-0001",
    "patch": {"status": "cancelled"},
}
jsonschema.validate(update_fixture, schemas["update-request"])

binding_key = {
    "tenantId",
    "practiceId",
    "userObjectId",
    "sessionId",
}
binding_required = set(schemas["session-binding"]["required"])
if not binding_key.issubset(binding_required):
    raise SystemExit("session binding key is incomplete")

state_key = layout["lists"]["state"]["uniqueKey"]
expected_state_key = [
    "tenantId",
    "practiceId",
    "scopeType",
    "scopeId",
    "recordType",
    "recordId",
]
if state_key != expected_state_key:
    raise SystemExit("SharePoint state unique key changed")

audit = layout["lists"]["audit"]
if audit["appendOnly"] is not True:
    raise SystemExit("audit list must be append-only")
if audit["allowUpdate"] is not False or audit["allowDelete"] is not False:
    raise SystemExit("audit updates and deletes must be disabled")

print("SharePoint state contracts: OK")
PY
