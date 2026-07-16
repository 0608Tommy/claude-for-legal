#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STATE_ROOT="$ROOT/m365-cowork-ja/state-service"
AI_ROOT="$ROOT/m365-cowork-ja/cowork-packages/ai-governance-legal"

PYTHONPATH="$STATE_ROOT${PYTHONPATH:+:$PYTHONPATH}" \
  python3 - "$STATE_ROOT" "$AI_ROOT" <<'PY'
import copy
import json
import pathlib
import re
import sys
from datetime import datetime
from typing import cast

import jsonschema
import yaml
from referencing import Registry, Resource

from contracts import (
    MatterSnapshot,
    SessionBinding,
    SessionBindingCreateRequest,
    SessionBindingTransitionError,
    SessionBindingUpdateRequest,
    validate_session_binding_create,
    validate_session_binding_transition,
    validate_session_binding_update,
)

root = pathlib.Path(sys.argv[1])
ai_root = pathlib.Path(sys.argv[2])

schemas = {
    path.stem.replace(".schema", ""): json.loads(
        path.read_text(encoding="utf-8")
    )
    for path in (root / "schemas").glob("*.schema.json")
}
layout = json.loads(
    (root / "sharepoint-layout.json").read_text(encoding="utf-8")
)
access_model = json.loads(
    (root / "access-model.json").read_text(encoding="utf-8")
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

format_checker = jsonschema.FormatChecker()


@format_checker.checks("date-time", raises=ValueError)
def is_date_time(value):
    if not isinstance(value, str):
        return True
    if "T" not in value.upper():
        return False
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.utcoffset() is not None


registry = Registry().with_resources(
    (
        cast(str, schema["$id"]),
        Resource.from_contents(schema),
    )
    for schema in schemas.values()
)
validators = {
    name: jsonschema.Draft202012Validator(
        schema,
        registry=registry,
        format_checker=format_checker,
    )
    for name, schema in schemas.items()
}


def validate(schema_name, fixture):
    validators[schema_name].validate(fixture)


def reject_schema(schema_name, fixture, message):
    try:
        validate(schema_name, fixture)
    except jsonschema.ValidationError:
        return
    raise SystemExit(message)


def reject_semantic(callback, message):
    try:
        callback()
    except SessionBindingTransitionError:
        return
    raise SystemExit(message)


for name, schema in schemas.items():
    jsonschema.Draft202012Validator.check_schema(schema)
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
validate("create-request", create_fixture)

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
validate("update-request", update_fixture)

binding_key = {
    "tenantId",
    "practiceId",
    "userObjectId",
    "sessionId",
}
binding_required = set(schemas["session-binding"]["required"])
if not binding_key.issubset(binding_required):
    raise SystemExit("session binding key is incomplete")

binding_fixture: SessionBinding = {
    "tenantId": "tenant-1",
    "practiceId": "ai-governance",
    "userObjectId": "user-1",
    "sessionId": "session-1",
    "matterId": "matter-1",
    "status": "active",
    "boundAt": "2026-07-16T09:00:00+09:00",
    "boundBy": "user-1",
    "expiresAt": "2026-07-16T17:00:00+09:00",
    "revokedAt": None,
    "revokedBy": None,
    "revocationReason": None,
}
validate("session-binding", binding_fixture)

matter_snapshot: MatterSnapshot = {
    "tenantId": "tenant-1",
    "practiceId": "ai-governance",
    "matterId": "matter-1",
    "itemId": "matter-item-1",
    "eTag": "\"5\"",
    "version": 5,
    "bindingGeneration": 7,
    "status": "active",
}

revoked_binding = cast(
    SessionBinding,
    {
        **binding_fixture,
        "status": "revoked",
        "revokedAt": "2026-07-16T10:00:00+09:00",
        "revokedBy": "user-1",
        "revocationReason": "matter-switch",
    },
)
validate("session-binding", revoked_binding)
validate_session_binding_transition(binding_fixture, revoked_binding)

for field, value in (
    ("revokedAt", "2026-07-16T10:00:00+09:00"),
    ("revokedBy", "user-1"),
    ("revocationReason", "matter-switch"),
):
    invalid_active = copy.deepcopy(binding_fixture)
    invalid_active[field] = value
    reject_schema(
        "session-binding",
        invalid_active,
        f"active binding accepted non-null {field}",
    )

for field in ("revokedAt", "revokedBy", "revocationReason"):
    invalid_revoked = copy.deepcopy(revoked_binding)
    del invalid_revoked[field]
    reject_schema(
        "session-binding",
        invalid_revoked,
        f"revoked binding accepted missing {field}",
    )

for field, value in (
    ("revokedAt", None),
    ("revokedBy", ""),
    ("revocationReason", ""),
):
    invalid_revoked = copy.deepcopy(revoked_binding)
    invalid_revoked[field] = value
    reject_schema(
        "session-binding",
        invalid_revoked,
        f"revoked binding accepted invalid {field}",
    )

invalid_revoked_time = copy.deepcopy(revoked_binding)
invalid_revoked_time["revokedAt"] = "not-a-date"
reject_schema(
    "session-binding",
    invalid_revoked_time,
    "revoked binding accepted invalid revokedAt format",
)

binding_create_fixture: SessionBindingCreateRequest = {
    "tenantId": "tenant-1",
    "practiceId": "ai-governance",
    "scopeType": "session",
    "scopeId": "user-1:session-1",
    "recordType": "session-matter-binding",
    "recordId": "active-matter",
    "idempotencyKey": "binding-create-0001",
    "expectedAbsent": True,
    "matterPrecondition": {
        "itemId": "matter-item-1",
        "eTag": "\"5\"",
        "version": 5,
        "expectedStatus": "active",
        "atomicWithBindingExpectedAbsent": True,
    },
    "payload": binding_fixture,
}
validate("create-request", binding_create_fixture)
validate_session_binding_create(
    binding_create_fixture,
    matter_snapshot,
)

generation_binding_create = copy.deepcopy(binding_create_fixture)
generation_binding_create["matterPrecondition"] = {
    "itemId": "matter-item-1",
    "bindingGeneration": 7,
    "expectedStatus": "active",
    "atomicWithBindingExpectedAbsent": True,
}
validate("create-request", generation_binding_create)
validate_session_binding_create(
    cast(SessionBindingCreateRequest, generation_binding_create),
    matter_snapshot,
)

missing_matter_precondition = copy.deepcopy(binding_create_fixture)
del missing_matter_precondition["matterPrecondition"]
reject_schema(
    "create-request",
    missing_matter_precondition,
    "binding create accepted no matter precondition",
)

missing_matter_token = copy.deepcopy(binding_create_fixture)
del missing_matter_token["matterPrecondition"]["eTag"]
del missing_matter_token["matterPrecondition"]["version"]
reject_schema(
    "create-request",
    missing_matter_token,
    "binding create accepted no matter concurrency token",
)

for field, value in (
    ("itemId", ""),
    ("expectedStatus", "archived"),
    ("atomicWithBindingExpectedAbsent", False),
):
    invalid_precondition = copy.deepcopy(binding_create_fixture)
    invalid_precondition["matterPrecondition"][field] = value
    reject_schema(
        "create-request",
        invalid_precondition,
        f"binding create accepted invalid matter precondition {field}",
    )

for field, value in (
    ("itemId", "matter-item-other"),
    ("eTag", "\"4\""),
    ("version", 4),
):
    stale_precondition = copy.deepcopy(binding_create_fixture)
    stale_precondition["matterPrecondition"][field] = value
    reject_semantic(
        lambda fixture=cast(
            SessionBindingCreateRequest,
            stale_precondition,
        ): validate_session_binding_create(
            fixture,
            matter_snapshot,
        ),
        f"binding create accepted stale matter precondition {field}",
    )

stale_generation_create = copy.deepcopy(generation_binding_create)
stale_generation_create["matterPrecondition"]["bindingGeneration"] = 6
reject_semantic(
    lambda: validate_session_binding_create(
        cast(SessionBindingCreateRequest, stale_generation_create),
        matter_snapshot,
    ),
    "binding create accepted stale binding generation",
)

fenced_matter = cast(
    MatterSnapshot,
    {
        **matter_snapshot,
        "eTag": "\"6\"",
        "version": 6,
        "bindingGeneration": 8,
        "status": "close-pending",
    },
)
post_fence_create = copy.deepcopy(binding_create_fixture)
post_fence_create["matterPrecondition"] = {
    "itemId": "matter-item-1",
    "eTag": "\"6\"",
    "version": 6,
    "bindingGeneration": 8,
    "expectedStatus": "active",
    "atomicWithBindingExpectedAbsent": True,
}
validate("create-request", post_fence_create)
reject_semantic(
    lambda: validate_session_binding_create(
        cast(SessionBindingCreateRequest, post_fence_create),
        fenced_matter,
    ),
    "binding create succeeded after the close fence",
)

for field, value in (
    ("scopeType", "matter"),
    ("recordId", "matter-1"),
):
    invalid_create = copy.deepcopy(binding_create_fixture)
    invalid_create[field] = value
    reject_schema(
        "create-request",
        invalid_create,
        f"binding create accepted invalid {field}",
    )

revoked_create = copy.deepcopy(binding_create_fixture)
revoked_create["payload"] = revoked_binding
reject_schema(
    "create-request",
    revoked_create,
    "binding create accepted revoked payload",
)

for field, value in (
    ("tenantId", "tenant-other"),
    ("practiceId", "practice-other"),
    ("scopeId", "user-1:session-other"),
):
    mismatched_create = copy.deepcopy(binding_create_fixture)
    mismatched_create[field] = value
    reject_semantic(
        lambda fixture=cast(
            SessionBindingCreateRequest,
            mismatched_create,
        ): validate_session_binding_create(
            fixture,
            matter_snapshot,
        ),
        f"binding create accepted mismatched outer {field}",
    )

for field, value in (
    ("userObjectId", "user-other"),
    ("sessionId", "session-other"),
):
    mismatched_payload_create = copy.deepcopy(binding_create_fixture)
    mismatched_payload_create["payload"][field] = value
    reject_semantic(
        lambda fixture=cast(
            SessionBindingCreateRequest,
            mismatched_payload_create,
        ): validate_session_binding_create(
            fixture,
            matter_snapshot,
        ),
        f"binding create accepted mismatched payload {field}",
    )

binding_update_fixture: SessionBindingUpdateRequest = {
    "tenantId": "tenant-1",
    "practiceId": "ai-governance",
    "scopeType": "session",
    "scopeId": "user-1:session-1",
    "recordType": "session-matter-binding",
    "recordId": "active-matter",
    "itemId": "binding-item-1",
    "eTag": "\"7\"",
    "idempotencyKey": "binding-revoke-0001",
    "patch": {
        "status": "revoked",
        "revokedAt": "2026-07-16T10:00:00+09:00",
        "revokedBy": "user-1",
        "revocationReason": "matter-switch",
    },
}
validate("update-request", binding_update_fixture)
updated_binding = validate_session_binding_update(
    binding_update_fixture,
    binding_fixture,
)
validate("session-binding", updated_binding)

invalid_patch_cases = (
    ("status", "active"),
    ("revokedAt", "not-a-date"),
    ("revokedBy", ""),
    ("revocationReason", ""),
    ("matterId", "matter-2"),
)
for field, value in invalid_patch_cases:
    invalid_update = copy.deepcopy(binding_update_fixture)
    invalid_update["patch"][field] = value
    reject_schema(
        "update-request",
        invalid_update,
        f"binding update accepted invalid patch field {field}",
    )

missing_reason_update = copy.deepcopy(binding_update_fixture)
del missing_reason_update["patch"]["revocationReason"]
reject_schema(
    "update-request",
    missing_reason_update,
    "binding update accepted missing revocationReason",
)

mismatched_update = copy.deepcopy(binding_update_fixture)
mismatched_update["scopeId"] = "user-1:session-other"
reject_semantic(
    lambda: validate_session_binding_update(
        cast(SessionBindingUpdateRequest, mismatched_update),
        binding_fixture,
    ),
    "binding update accepted mismatched outer identity",
)

immutable_mutations = {
    "tenantId": "tenant-other",
    "practiceId": "practice-other",
    "userObjectId": "user-other",
    "sessionId": "session-other",
    "matterId": "matter-other",
    "boundAt": "2026-07-16T09:01:00+09:00",
    "boundBy": "user-other",
    "expiresAt": "2026-07-16T18:00:00+09:00",
}
for field, value in immutable_mutations.items():
    changed_binding = copy.deepcopy(revoked_binding)
    changed_binding[field] = value
    reject_semantic(
        lambda candidate=cast(
            SessionBinding,
            changed_binding,
        ): validate_session_binding_transition(
            binding_fixture,
            candidate,
        ),
        f"binding transition changed immutable {field}",
    )

reject_semantic(
    lambda: validate_session_binding_transition(
        revoked_binding,
        revoked_binding,
    ),
    "revoked binding was accepted as the current transition state",
)
reject_semantic(
    lambda: validate_session_binding_update(
        binding_update_fixture,
        revoked_binding,
    ),
    "already-revoked close binding was accepted for another update",
)
reject_semantic(
    lambda: validate_session_binding_transition(
        binding_fixture,
        binding_fixture,
    ),
    "active-to-active binding update was accepted",
)

ordinary_update = {
    **update_fixture,
    "patch": {
        "status": "cancelled",
        "matterId": "matter-1",
    },
}
validate("update-request", ordinary_update)

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

if not any(
    "active matter precondition and binding expectedAbsent" in rule
    for rule in access_model["rules"]
):
    raise SystemExit(
        "state gateway atomic binding-create rule is missing"
    )

runtime_contracts = [
    root.parent
    / "cowork-packages"
    / plugin
    / "references"
    / "cowork-runtime-contract.md"
    for plugin in (
        "ai-governance-legal",
        "commercial-legal",
        "privacy-legal",
    )
]
for runtime_contract in runtime_contracts:
    text = runtime_contract.read_text(encoding="utf-8")
    if "expiresAt > now" not in text:
        raise SystemExit(
            f"{runtime_contract}: binding expiry check is missing"
        )

canonical_references = {
    path.relative_to(ai_root / "references"): path.read_bytes()
    for path in (ai_root / "references").rglob("*")
    if path.is_file()
}
for skill_path in sorted((ai_root / "skills").iterdir()):
    if not skill_path.is_dir():
        continue
    common_root = skill_path / "references" / "common"
    local_references = {
        path.relative_to(common_root): path.read_bytes()
        for path in common_root.rglob("*")
        if path.is_file()
    }
    if local_references != canonical_references:
        raise SystemExit(
            f"{skill_path}: common references are not byte-for-byte synced"
        )

matter_skill = (
    ai_root / "skills" / "matter-workspace" / "SKILL.md"
).read_text(encoding="utf-8")
required_matter_fragments = (
    "current bindingを`revoked`",
    "現在の会話を停止",
    "fresh session",
    "全bindingをexact query",
    "statusが`active`のbindingだけ",
    "既に`revoked`のbindingはsatisfied",
    "active bindingが0件",
    "最初のatomic conditional operation",
    "fence成功後",
    "zero active確認後だけ",
    "fence前にcommitしたcreate",
    "fence後のcreate",
    "fail closed",
)
for fragment in required_matter_fragments:
    if fragment not in matter_skill:
        raise SystemExit(
            f"AI matter workspace is missing lifecycle rule: {fragment}"
        )
for forbidden in (
    "status: none",
    "status `none`",
    "bindingを`none`へ",
):
    if forbidden in matter_skill:
        raise SystemExit(
            f"AI matter workspace uses forbidden binding state: {forbidden}"
        )
if "全bindingをitemごとに`revoked`へconditional update" in matter_skill:
    raise SystemExit(
        "AI matter close must not update already-revoked bindings"
    )
close_summary = next(
    (
        line
        for line in matter_skill.splitlines()
        if line.startswith("| `close <slug>` |")
    ),
    "",
)
summary_fragments = (
    "fence",
    "active bindingだけをrevoke",
    "already-revokedはsatisfied",
    "zero active",
    "`archived`へfinalize",
)
if not close_summary:
    raise SystemExit("AI matter close summary row is missing")
summary_order = tuple(
    close_summary.index(fragment)
    for fragment in summary_fragments
)
if summary_order != tuple(sorted(summary_order)):
    raise SystemExit(
        "AI matter close summary must fence, revoke active, verify, finalize"
    )
for forbidden_instruction in (
    "`archived`へ更新し、そのmatterの全bindingをrevoke",
    "matterを`status: archived`へconditional update",
    "全bindingをitemごとに`revoked`へconditional update",
    "対象matterの全bindingを`revoked`へ",
    "その`matterId`を参照する全bindingを`revoked`へ",
):
    if forbidden_instruction in matter_skill:
        raise SystemExit(
            "AI matter close contains archive-first or revoke-every guidance"
        )
close_section = matter_skill.split(
    "## `close <slug>`",
    maxsplit=1,
)[1].split("## `none`", maxsplit=1)[0]
active_revoke_index = close_section.index(
    "statusが`active`のbindingだけ",
)
archive_finalize_index = close_section.index(
    "`status: archived`へconditional finalize",
)
if archive_finalize_index < active_revoke_index:
    raise SystemExit(
        "AI matter close must not archive before active revocation"
    )
close_order_fragments = (
    "最初のatomic conditional operation",
    "fence成功後",
    "statusが`active`のbindingだけ",
    "active bindingが0件",
    "zero active確認後だけ",
)
close_order = tuple(
    matter_skill.index(fragment)
    for fragment in close_order_fragments
)
if close_order != tuple(sorted(close_order)):
    raise SystemExit(
        "AI matter close must fence, enumerate, revoke, verify, finalize"
    )

runtime_text = (
    ai_root / "references" / "cowork-runtime-contract.md"
).read_text(encoding="utf-8")
for fragment in (
    "expectedAbsent: true",
    "createへ`itemId` / `eTag`を要求しない",
    "updateへ`expectedAbsent`を含めない",
    "session-matter-binding",
    "atomicWithBindingExpectedAbsent: true",
    "同一transactionで評価",
):
    if fragment not in runtime_text:
        raise SystemExit(
            f"AI runtime contract is missing write rule: {fragment}"
        )
for fragment in (
    "statusが`active`のbindingだけ",
    "既に`revoked`のbindingはsatisfied",
    "active bindingが0件",
    "fence前にcommitしたcreate",
    "fence後のcreate",
):
    if fragment not in runtime_text:
        raise SystemExit(
            f"AI runtime contract is missing close rule: {fragment}"
        )

cold_start_skill = (
    ai_root / "skills" / "cold-start-interview" / "SKILL.md"
).read_text(encoding="utf-8")
for fragment in (
    "first-time company / practice / user profile",
    "`expectedAbsent: true`",
    "create requestへ`itemId` / `eTag`を含めず",
    "exact `itemId`、latest `eTag`",
    "update requestへ`expectedAbsent`",
    "含めない。createとupdateを同じrequest shape",
):
    if fragment not in cold_start_skill:
        raise SystemExit(
            f"AI cold-start is missing create/update rule: {fragment}"
        )

matter_records = (
    ai_root
    / "skills"
    / "matter-workspace"
    / "references"
    / "matter-records.md"
).read_text(encoding="utf-8")
audit_blocks = re.findall(
    r"<!-- audit-event-example -->\s*```yaml\n(.*?)```",
    matter_records,
    flags=re.DOTALL,
)
if len(audit_blocks) != 3:
    raise SystemExit("AI matter records must contain three audit examples")
audit_examples = [yaml.safe_load(block) for block in audit_blocks]
for example in audit_examples:
    validate("audit-event", example)

switch_examples = {
    example["eventType"]: example
    for example in audit_examples
    if example["eventType"] in {
        "session-binding-revoked",
        "session-binding-created",
    }
}
if set(switch_examples) != {
    "session-binding-revoked",
    "session-binding-created",
}:
    raise SystemExit("AI switch audit examples are incomplete")
revoked_event = switch_examples["session-binding-revoked"]
created_event = switch_examples["session-binding-created"]
if revoked_event["correlationId"] != created_event["correlationId"]:
    raise SystemExit("AI switch audit events must share correlationId")
if (
    revoked_event["details"]["sessionId"]
    == created_event["details"]["sessionId"]
):
    raise SystemExit("AI switch audit create must use a fresh session")
required_binding_create_details = {
    "matterItemId",
    "expectedMatterStatus",
    "matterETag",
    "bindingGeneration",
    "atomicWithBindingExpectedAbsent",
}
if not required_binding_create_details.issubset(
    created_event["details"],
):
    raise SystemExit(
        "AI switch audit must record the atomic matter precondition"
    )

classification_reference = (
    ai_root
    / "skills"
    / "ai-inventory"
    / "references"
    / "classification-and-record.md"
).read_text(encoding="utf-8")
classification_blocks = re.findall(
    r"<!-- inventory-audit-event-example -->\s*```yaml\n(.*?)```",
    classification_reference,
    flags=re.DOTALL,
)
if len(classification_blocks) != 1:
    raise SystemExit(
        "AI inventory must contain one classification audit example"
    )
classification_audit = yaml.safe_load(classification_blocks[0])
validate("audit-event", classification_audit)
classification_details = classification_audit["details"]
required_classification_details = {
    "systemId",
    "changedFields",
    "sourceSystem",
    "sourceItemId",
    "sourceVersionOrRevisionId",
    "eTagBefore",
    "eTagAfter",
}
if not required_classification_details.issubset(classification_details):
    raise SystemExit(
        "AI classification audit details are incomplete"
    )
if required_classification_details.intersection(classification_audit):
    raise SystemExit(
        "AI classification package fields must not be top-level"
    )

print("SharePoint state contracts: OK")
PY
