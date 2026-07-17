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

zero_generation_create = copy.deepcopy(generation_binding_create)
zero_generation_create["matterPrecondition"]["bindingGeneration"] = 0
zero_generation_matter = cast(
    MatterSnapshot,
    {
        **matter_snapshot,
        "bindingGeneration": 0,
    },
)
validate("create-request", zero_generation_create)
validate_session_binding_create(
    cast(SessionBindingCreateRequest, zero_generation_create),
    zero_generation_matter,
)

for invalid_generation in (-1, True, ""):
    invalid_generation_create = copy.deepcopy(
        generation_binding_create
    )
    invalid_generation_create["matterPrecondition"][
        "bindingGeneration"
    ] = invalid_generation
    reject_schema(
        "create-request",
        invalid_generation_create,
        f"binding create accepted generation {invalid_generation!r}",
    )
    reject_semantic(
        lambda fixture=cast(
            SessionBindingCreateRequest,
            invalid_generation_create,
        ): validate_session_binding_create(
            fixture,
            matter_snapshot,
        ),
        f"semantic binding create accepted {invalid_generation!r}",
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

packages_root = root.parent / "cowork-packages"


def declared_matter_workflow(package_root):
    matter_workspace = (
        package_root / "skills" / "matter-workspace" / "SKILL.md"
    )
    if matter_workspace.is_file():
        return matter_workspace
    candidates = []
    for skill_path in sorted(
        (package_root / "skills").glob("*/SKILL.md")
    ):
        skill_text = skill_path.read_text(encoding="utf-8")
        if (
            "## Matter closure" in skill_text
            and "matter close" in skill_text
        ):
            candidates.append(skill_path)
    if len(candidates) == 1:
        return candidates[0]
    if candidates:
        raise SystemExit(
            f"{package_root}: multiple equivalent matter workflows"
        )
    return None


matter_workflow_paths = {}
no_close_packages = set()
for package_root_candidate in sorted(packages_root.iterdir()):
    if (
        not package_root_candidate.is_dir()
        or not (package_root_candidate / "manifest.json").is_file()
    ):
        continue
    workflow_path = declared_matter_workflow(
        package_root_candidate
    )
    if workflow_path is not None:
        matter_workflow_paths[package_root_candidate.name] = (
            workflow_path
        )
        continue
    runtime_path_candidate = (
        package_root_candidate
        / "references"
        / "cowork-runtime-contract.md"
    )
    runtime_text_candidate = (
        runtime_path_candidate.read_text(encoding="utf-8")
        if runtime_path_candidate.is_file()
        else ""
    )
    skill_text_candidate = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(
            (package_root_candidate / "skills").glob("*/SKILL.md")
        )
    )
    if (
        "session-matter-binding" in runtime_text_candidate
        or "matter close" in skill_text_candidate
    ):
        raise SystemExit(
            f"{package_root_candidate}: matter close workflow missing"
        )
    no_close_packages.add(package_root_candidate.name)

if not no_close_packages:
    raise SystemExit("expected at least one genuine no-close package")

affected_binding_packages = set(matter_workflow_paths)


def binding_example_kind(document):
    if document.get("recordType") != "session-matter-binding":
        return None
    if "expectedAbsent" in document and "payload" in document:
        return "create"
    if "itemId" in document and "payload" in document:
        return "persist"
    if "itemId" in document and "patch" in document:
        return "revoke"
    return None


def current_matter_for_create(document):
    payload = document["payload"]
    precondition = document["matterPrecondition"]
    return {
        "tenantId": payload["tenantId"],
        "practiceId": payload["practiceId"],
        "matterId": payload["matterId"],
        "itemId": precondition["itemId"],
        "eTag": precondition.get("eTag", "\"synthetic\""),
        "version": precondition.get("version", 1),
        "bindingGeneration": precondition.get(
            "bindingGeneration",
            1,
        ),
        "status": "active",
    }


def require_outer_binding_identity(document, payload, context):
    expected_scope = (
        f"{payload['userObjectId']}:{payload['sessionId']}"
    )
    expected = {
        "tenantId": payload["tenantId"],
        "practiceId": payload["practiceId"],
        "scopeType": "session",
        "scopeId": expected_scope,
        "recordType": "session-matter-binding",
        "recordId": "active-matter",
    }
    for field, value in expected.items():
        if document.get(field) != value:
            raise SystemExit(
                f"{context}: outer {field} does not match payload"
            )


binding_examples = {}
runtime_contracts = sorted(
    packages_root.glob("*/references/cowork-runtime-contract.md")
)
for runtime_contract in runtime_contracts:
    runtime_text_candidate = runtime_contract.read_text(
        encoding="utf-8"
    )
    if (
        "session-matter-binding" in runtime_text_candidate
        and "expiresAt > now" not in runtime_text_candidate
    ):
        raise SystemExit(
            f"{runtime_contract}: binding expiry check is missing"
        )
    package = runtime_contract.parent.parent.name
    package_examples = {}
    for block in re.findall(
        r"```yaml\n(.*?)```",
        runtime_text_candidate,
        flags=re.DOTALL,
    ):
        document = yaml.safe_load(block)
        if not isinstance(document, dict):
            continue
        kind = binding_example_kind(document)
        if kind is None:
            continue
        if kind in package_examples:
            raise SystemExit(
                f"{runtime_contract}: duplicate binding {kind} example"
            )
        package_examples[kind] = document
    if package_examples:
        binding_examples[package] = package_examples


def synthetic_persist_example(create_example):
    return {
        "tenantId": create_example["tenantId"],
        "practiceId": create_example["practiceId"],
        "scopeType": create_example["scopeType"],
        "scopeId": create_example["scopeId"],
        "recordType": create_example["recordType"],
        "recordId": create_example["recordId"],
        "itemId": "synthetic-binding-item",
        "eTag": "\"1\"",
        "version": 1,
        "payload": copy.deepcopy(create_example["payload"]),
        "updatedAt": "2026-07-16T09:00:00+09:00",
    }


def synthetic_revoke_example(create_example):
    return {
        "tenantId": create_example["tenantId"],
        "practiceId": create_example["practiceId"],
        "scopeType": create_example["scopeType"],
        "scopeId": create_example["scopeId"],
        "recordType": create_example["recordType"],
        "recordId": create_example["recordId"],
        "itemId": "synthetic-binding-item",
        "eTag": "\"1\"",
        "idempotencyKey": "synthetic-revoke-0001",
        "patch": {
            "status": "revoked",
            "revokedAt": "2026-07-16T10:00:00+09:00",
            "revokedBy": "synthetic-user",
            "revocationReason": "matter-close",
        },
    }


for package in affected_binding_packages:
    examples = binding_examples.get(package)
    if examples is None or "create" not in examples:
        raise SystemExit(
            f"{package}: binding create example is missing"
        )
    create_example = examples["create"]
    examples.setdefault(
        "persist",
        synthetic_persist_example(create_example),
    )
    examples.setdefault(
        "revoke",
        synthetic_revoke_example(create_example),
    )

for package, examples in binding_examples.items():
    create_example = examples.get("create")
    persist_example = examples.get("persist")
    revoke_example = examples.get("revoke")
    if create_example is not None:
        validate("create-request", create_example)
        create_payload = create_example["payload"]
        validate("session-binding", create_payload)
        require_outer_binding_identity(
            create_example,
            create_payload,
            f"{package} create",
        )
        validate_session_binding_create(
            cast(SessionBindingCreateRequest, create_example),
            cast(
                MatterSnapshot,
                current_matter_for_create(create_example),
            ),
        )
    if persist_example is not None:
        validate("state-envelope", persist_example)
        persist_payload = persist_example["payload"]
        validate("session-binding", persist_payload)
        require_outer_binding_identity(
            persist_example,
            persist_payload,
            f"{package} persist",
        )
        if (
            create_example is not None
            and persist_payload != create_example["payload"]
        ):
            raise SystemExit(
                f"{package}: create and persisted payload differ"
            )
    if revoke_example is not None:
        validate("update-request", revoke_example)
        current_payload = (
            persist_example["payload"]
            if persist_example is not None
            else create_example["payload"]
            if create_example is not None
            else None
        )
        if current_payload is None:
            raise SystemExit(
                f"{package}: revoke example has no active payload"
            )
        require_outer_binding_identity(
            revoke_example,
            current_payload,
            f"{package} revoke",
        )
        revoked_payload = validate_session_binding_update(
            cast(SessionBindingUpdateRequest, revoke_example),
            cast(SessionBinding, current_payload),
        )
        validate("session-binding", revoked_payload)

for package in affected_binding_packages:
    example_kinds = set(binding_examples.get(package, {}))
    if example_kinds != {"create", "persist", "revoke"}:
        raise SystemExit(
            f"{package}: binding example coverage is {example_kinds}"
        )

for package in affected_binding_packages:
    package_root = packages_root / package
    runtime_path = (
        package_root / "references" / "cowork-runtime-contract.md"
    )
    canonical_runtime = runtime_path.read_bytes()
    package_runtime_text = canonical_runtime.decode("utf-8")
    normalized_package_runtime = re.sub(
        r"\s+",
        " ",
        package_runtime_text,
    )
    if (
        "matter `status == active`" not in normalized_package_runtime
        and "matter `status: active`" not in normalized_package_runtime
    ):
        raise SystemExit(
            f"{runtime_path}: active matter access requirement missing"
        )
    for access_fragment in (
        "close-pending",
        "non-active",
        "access",
    ):
        if access_fragment not in normalized_package_runtime:
            raise SystemExit(
                f"{runtime_path}: access coverage missing "
                f"{access_fragment}"
            )
    runtime_variant_groups = (
        (
            "enumeration",
            (
                "fence後に全binding",
                "fence後に対象matterの全binding",
            ),
        ),
        (
            "active-only revoke",
            (
                "activeだけをrevoke",
                "statusが`active`のbindingだけ",
            ),
        ),
        (
            "already-revoked satisfied",
            (
                "already-revokedはsatisfied",
                "既に`revoked`のbindingはsatisfied",
            ),
        ),
        (
            "zero active",
            (
                "zero active",
                "active bindingが0件",
            ),
        ),
        (
            "atomic binding create",
            (
                "binding absenceとatomically",
                "binding `expectedAbsent: true`を同一transactionで評価",
            ),
        ),
    )
    runtime_variant_positions = {}
    for label, variants in runtime_variant_groups:
        positions_for_label = [
            package_runtime_text.index(variant)
            for variant in variants
            if variant in package_runtime_text
        ]
        if not positions_for_label:
            raise SystemExit(
                f"{runtime_path}: runtime binding rule missing {label}"
            )
        runtime_variant_positions[label] = min(positions_for_label)
    for fragment in (
        "finalize",
        "fence前にcommitしたcreate",
        "fence後のcreate",
        "fail closed",
    ):
        if fragment not in package_runtime_text:
            raise SystemExit(
                f"{runtime_path}: runtime binding rule missing {fragment}"
            )
    runtime_start_candidates = (
        "matter closeは最初に",
        "matter closeは、最初の",
        "最初のatomic conditional",
    )
    runtime_start_positions = [
        package_runtime_text.index(fragment)
        for fragment in runtime_start_candidates
        if fragment in package_runtime_text
    ]
    if not runtime_start_positions:
        raise SystemExit(
            f"{runtime_path}: fence-first close start is missing"
        )
    runtime_positions = (
        min(runtime_start_positions),
        runtime_variant_positions["enumeration"],
        runtime_variant_positions["active-only revoke"],
        runtime_variant_positions["zero active"],
        package_runtime_text.index("finalize"),
    )
    if runtime_positions != tuple(sorted(runtime_positions)):
        raise SystemExit(
            f"{runtime_path}: runtime close order is invalid"
        )
    for forbidden in (
        "matter close時は、その`matterId`を参照する全bindingを",
        "全bindingをitemごとに`revoked`へ",
        "matter archived update後、全binding revoke",
    ):
        if forbidden in package_runtime_text:
            raise SystemExit(
                f"{runtime_path}: archive-first/revoke-every runtime rule"
            )
    local_runtime_paths = sorted(
        (package_root / "skills").glob(
            "*/references/common/cowork-runtime-contract.md"
        )
    )
    if not local_runtime_paths:
        raise SystemExit(
            f"{package}: no skill-local runtime contracts found"
        )
    for local_runtime in local_runtime_paths:
        if local_runtime.read_bytes() != canonical_runtime:
            raise SystemExit(
                f"{local_runtime}: runtime contract is not synced"
            )


def simple_matter_fence_errors(current, updated):
    errors = []
    current_generation = current.get("bindingGeneration")
    updated_generation = updated.get("bindingGeneration")
    if (
        not isinstance(current_generation, int)
        or isinstance(current_generation, bool)
        or current_generation < 0
        or not isinstance(updated_generation, int)
        or isinstance(updated_generation, bool)
        or updated_generation < 0
    ):
        errors.append("bindingGeneration must be nonnegative integer")
    current_status = current.get("status")
    updated_status = updated.get("status")
    if current_status == "active":
        if updated_status != "close-pending":
            errors.append("matter must fence before archive")
        if (
            isinstance(current_generation, int)
            and not isinstance(current_generation, bool)
            and updated_generation != current_generation + 1
        ):
            errors.append("fence must increment generation")
    elif current_status == "close-pending":
        if updated_status != "archived":
            errors.append("fenced matter must finalize archived")
        if updated_generation != current_generation:
            errors.append("finalize must preserve generation")
    else:
        errors.append("matter transition source is invalid")
    return errors


def matter_access_allowed(
    binding_status,
    binding_unexpired,
    matter_status,
):
    return (
        binding_status == "active"
        and binding_unexpired is True
        and matter_status == "active"
    )


if not matter_access_allowed("active", True, "active"):
    raise SystemExit("valid active matter access was rejected")
for nonactive_status in ("close-pending", "archived", "closed"):
    if matter_access_allowed("active", True, nonactive_status):
        raise SystemExit(
            "privacy active binding accessed non-active matter "
            f"{nonactive_status}"
        )


for package in affected_binding_packages:
    matter_skill_path = matter_workflow_paths[package]
    package_matter_skill = matter_skill_path.read_text(
        encoding="utf-8"
    )
    if package in {"commercial-legal", "privacy-legal"}:
        runtime_access_text = (
            packages_root
            / package
            / "references"
            / "cowork-runtime-contract.md"
        ).read_text(encoding="utf-8")
        normalized_runtime_access = re.sub(
            r"\s+",
            " ",
            runtime_access_text,
        )
        normalized_skill_access = re.sub(
            r"\s+",
            " ",
            package_matter_skill,
        )
        for path, text in (
            (matter_skill_path, normalized_skill_access),
            (
                packages_root
                / package
                / "references"
                / "cowork-runtime-contract.md",
                normalized_runtime_access,
            ),
        ):
            for fragment in (
                "status == active",
                "active/unexpired",
                "close-pending",
                "archived",
                "closed",
                "non-active",
            ):
                if fragment not in text:
                    raise SystemExit(
                        f"{path}: matter access rule missing {fragment}"
                    )
    close_match = re.search(
        r"^## `close(?: <slug>)?`[^\n]*\n(.*?)(?=^## )",
        package_matter_skill,
        flags=re.DOTALL | re.MULTILINE,
    )
    if close_match is None:
        close_match = re.search(
            r"^## Matter closure\n(.*?)(?=^## )",
            package_matter_skill,
            flags=re.DOTALL | re.MULTILINE,
        )
    if close_match is None:
        raise SystemExit(
            f"{matter_skill_path}: close section is missing"
        )
    close_section_candidate = close_match.group(1)
    for fragment in (
        "最初のatomic conditional operation",
        "fence成功後",
        "conditional finalize",
        "fence前にcommitしたcreate",
        "fence後のcreate",
        "fail closed",
    ):
        if fragment not in close_section_candidate:
            raise SystemExit(
                f"{matter_skill_path}: close rule missing {fragment}"
            )
    close_variant_groups = (
        (
            "active-only revoke",
            (
                "activeだけをrevocation対象",
                "statusが`active`のbindingだけ",
            ),
        ),
        (
            "already-revoked satisfied",
            (
                "already-revokedはsatisfied",
                "既に`revoked`のbindingはsatisfied",
            ),
        ),
        (
            "zero active",
            (
                "zero active",
                "active bindingが0件",
            ),
        ),
    )
    close_variant_positions = {}
    for label, variants in close_variant_groups:
        positions_for_label = [
            close_section_candidate.index(variant)
            for variant in variants
            if variant in close_section_candidate
        ]
        if not positions_for_label:
            raise SystemExit(
                f"{matter_skill_path}: close rule missing {label}"
            )
        close_variant_positions[label] = min(positions_for_label)
    positions = (
        close_section_candidate.index(
            "最初のatomic conditional operation"
        ),
        close_section_candidate.index("fence成功後"),
        close_variant_positions["active-only revoke"],
        close_variant_positions["zero active"],
        close_section_candidate.index("conditional finalize"),
    )
    if positions != tuple(sorted(positions)):
        raise SystemExit(
            f"{matter_skill_path}: close lifecycle order is invalid"
        )
    for forbidden in (
        "matterを`archived`へconditional update",
        "全binding**をitemごとに`revoked`",
        "全bindingを`revoked`へ",
        "matter archived update後、全binding revoke",
        "matterをarchivedへupdateし、全bindingをrevoke",
    ):
        if forbidden in package_matter_skill:
            raise SystemExit(
                f"{matter_skill_path}: archive-first/revoke-every rule"
            )
    matter_records_path = (
        matter_skill_path.parent / "references" / "matter-records.md"
    )
    if matter_records_path.is_file():
        matter_records_text = matter_records_path.read_text(
            encoding="utf-8"
        )
        for fragment in ("close-pending", "bindingGeneration"):
            if fragment not in matter_records_text:
                raise SystemExit(
                    f"{matter_records_path}: matter fence field missing"
                )
        if package in {
            "commercial-legal",
            "employment-legal",
            "ip-legal",
            "privacy-legal",
        }:
            normalized_records = re.sub(
                r"\s+",
                " ",
                matter_records_text,
            )
            for fragment in (
                "bindingGeneration: 0",
                "最初のatomic conditional operation",
                "fence成功後に全bindingをenumerate",
                "active bindingだけをrevoke",
                "already-revokedはsatisfied",
                "zero active",
                "`archived`へfinalize",
                "fence前にcommitしたcreate",
                "fence後のcreate",
            ):
                if fragment not in normalized_records:
                    raise SystemExit(
                        f"{matter_records_path}: close guidance missing "
                        f"{fragment}"
                    )
            for forbidden in (
                "closeは全binding revoke",
                "全session bindingを itemごとにrevoke",
                "matter profileをconditional updateし",
            ):
                if forbidden in normalized_records:
                    raise SystemExit(
                        f"{matter_records_path}: stale revoke-every "
                        "guidance"
                    )
        if package in {"commercial-legal", "privacy-legal"}:
            normalized_access_records = re.sub(
                r"\s+",
                " ",
                matter_records_text,
            )
            for fragment in (
                "active/unexpired",
                "status != active",
                "close-pending",
                "archived",
                "closed",
                "accessを拒否",
            ):
                if fragment not in normalized_access_records:
                    raise SystemExit(
                        f"{matter_records_path}: access rule missing "
                        f"{fragment}"
                    )
        if package in {"commercial-legal", "privacy-legal"}:
            matter_block = re.search(
                r"## Matter\n.*?```yaml\n(.*?)```",
                matter_records_text,
                flags=re.DOTALL,
            )
            if matter_block is None:
                raise SystemExit(
                    f"{matter_records_path}: matter profile missing"
                )
            matter_template = yaml.safe_load(matter_block.group(1))
            if (
                matter_template.get("status")
                != "active | close-pending | archived"
                or matter_template.get("bindingGeneration") != 0
            ):
                raise SystemExit(
                    f"{matter_records_path}: matter lifecycle invalid"
                )
            active_profile = {
                "status": "active",
                "bindingGeneration": 0,
            }
            fenced_profile = {
                "status": "close-pending",
                "bindingGeneration": 1,
            }
            archived_profile = {
                "status": "archived",
                "bindingGeneration": 1,
            }
            if simple_matter_fence_errors(
                active_profile,
                fenced_profile,
            ):
                raise SystemExit(
                    f"{package}: valid matter fence rejected"
                )
            if simple_matter_fence_errors(
                fenced_profile,
                archived_profile,
            ):
                raise SystemExit(
                    f"{package}: valid matter finalize rejected"
                )
            invalid_transitions = (
                (
                    active_profile,
                    {
                        "status": "archived",
                        "bindingGeneration": 0,
                    },
                ),
                (
                    active_profile,
                    {
                        "status": "close-pending",
                        "bindingGeneration": 0,
                    },
                ),
                (
                    fenced_profile,
                    {
                        "status": "archived",
                        "bindingGeneration": 2,
                    },
                ),
            )
            for transition in invalid_transitions:
                if not simple_matter_fence_errors(*transition):
                    raise SystemExit(
                        f"{package}: invalid matter transition accepted"
                    )


def regulatory_matter_errors(document):
    errors = []
    string_fields = (
        "matterId",
        "slug",
        "clientOrBusinessUnit",
        "matterType",
        "confidentiality",
        "retentionClass",
        "legalHoldStatus",
        "openedAt",
    )
    for field in string_fields:
        value = document.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a nonblank string")
    if document.get("status") not in {
        "active",
        "close-pending",
        "archived",
    }:
        errors.append("status must support active/close-pending/archived")
    generation = document.get("bindingGeneration")
    if (
        not isinstance(generation, int)
        or isinstance(generation, bool)
        or generation < 0
    ):
        errors.append("bindingGeneration must be a nonnegative integer")
    for field in ("jurisdictions", "authorities", "authorizedGroups"):
        value = document.get(field)
        if (
            not isinstance(value, list)
            or not all(
                isinstance(item, str) and item.strip()
                for item in value
            )
        ):
            errors.append(f"{field} must be a string array")
    opened_at = document.get("openedAt")
    if (
        isinstance(opened_at, str)
        and not format_checker.conforms(opened_at, "date-time")
    ):
        errors.append("openedAt must be date-time")
    closed_at = document.get("closedAt")
    if closed_at is not None and (
        not isinstance(closed_at, str)
        or not format_checker.conforms(closed_at, "date-time")
    ):
        errors.append("closedAt must be null or date-time")
    return errors


def regulatory_transition_errors(current, updated):
    errors = [
        *regulatory_matter_errors(current),
        *regulatory_matter_errors(updated),
    ]
    for field in (
        "matterId",
        "slug",
        "clientOrBusinessUnit",
        "matterType",
        "openedAt",
    ):
        if current.get(field) != updated.get(field):
            errors.append(f"{field} is immutable")
    current_status = current.get("status")
    current_generation = current.get("bindingGeneration")
    updated_status = updated.get("status")
    updated_generation = updated.get("bindingGeneration")
    if current_status == "active":
        if updated_status != "close-pending":
            errors.append("active matter must fence before archive")
        if (
            isinstance(current_generation, int)
            and not isinstance(current_generation, bool)
            and updated_generation != current_generation + 1
        ):
            errors.append("fence must increment bindingGeneration")
    elif current_status == "close-pending":
        if updated_status != "archived":
            errors.append("fenced matter must finalize archived")
        if updated_generation != current_generation:
            errors.append("finalize must preserve bindingGeneration")
    else:
        errors.append("only active or close-pending may transition")
    return errors


regulatory_root = packages_root / "regulatory-legal"
regulatory_schema_path = (
    regulatory_root / "references" / "regulatory-record-schemas.md"
)
regulatory_schema_text = regulatory_schema_path.read_text(
    encoding="utf-8"
)
matter_section = regulatory_schema_text.split(
    "## Matter profile\n",
    maxsplit=1,
)[1]
matter_match = re.search(
    r"```yaml\n(.*?)```",
    matter_section,
    flags=re.DOTALL,
)
if matter_match is None:
    raise SystemExit(
        "regulatory matter profile example is missing"
    )
regulatory_matter = yaml.safe_load(matter_match.group(1))
matter_errors = regulatory_matter_errors(regulatory_matter)
if matter_errors:
    raise SystemExit(
        f"regulatory matter profile invalid: {matter_errors}"
    )

fenced_regulatory_matter = copy.deepcopy(regulatory_matter)
fenced_regulatory_matter["status"] = "close-pending"
fenced_regulatory_matter["bindingGeneration"] += 1
fence_errors = regulatory_transition_errors(
    regulatory_matter,
    fenced_regulatory_matter,
)
if fence_errors:
    raise SystemExit(
        f"valid regulatory fence rejected: {fence_errors}"
    )

archived_regulatory_matter = copy.deepcopy(
    fenced_regulatory_matter
)
archived_regulatory_matter["status"] = "archived"
archived_regulatory_matter["closedAt"] = (
    "2026-07-16T10:00:00+09:00"
)
finalize_errors = regulatory_transition_errors(
    fenced_regulatory_matter,
    archived_regulatory_matter,
)
if finalize_errors:
    raise SystemExit(
        f"valid regulatory finalize rejected: {finalize_errors}"
    )

negative_profiles = {
    "negative generation": {
        **regulatory_matter,
        "bindingGeneration": -1,
    },
    "Boolean generation": {
        **regulatory_matter,
        "bindingGeneration": True,
    },
    "string generation": {
        **regulatory_matter,
        "bindingGeneration": "1",
    },
    "unsupported status": {
        **regulatory_matter,
        "status": "closed",
    },
}
for name, candidate in negative_profiles.items():
    if not regulatory_matter_errors(candidate):
        raise SystemExit(
            f"invalid regulatory matter accepted: {name}"
        )

negative_transitions = {
    "archive before fence": (
        regulatory_matter,
        {
            **regulatory_matter,
            "status": "archived",
            "closedAt": "2026-07-16T10:00:00+09:00",
        },
    ),
    "fence without generation increment": (
        regulatory_matter,
        {
            **regulatory_matter,
            "status": "close-pending",
        },
    ),
    "finalize with generation change": (
        fenced_regulatory_matter,
        {
            **archived_regulatory_matter,
            "bindingGeneration": (
                fenced_regulatory_matter["bindingGeneration"] + 1
            ),
        },
    ),
}
for name, transition in negative_transitions.items():
    if not regulatory_transition_errors(*transition):
        raise SystemExit(
            f"invalid regulatory transition accepted: {name}"
        )

canonical_regulatory_schema = regulatory_schema_path.read_bytes()
regulatory_schema_copies = sorted(
    (regulatory_root / "skills").glob(
        "*/references/common/regulatory-record-schemas.md"
    )
)
if not regulatory_schema_copies:
    raise SystemExit("regulatory schema common copies are missing")
for schema_copy in regulatory_schema_copies:
    if schema_copy.read_bytes() != canonical_regulatory_schema:
        raise SystemExit(
            f"{schema_copy}: regulatory schema is not synced"
        )


def litigation_matter_errors(document):
    errors = []
    if document.get("status") not in {
        "active",
        "close-pending",
        "archived",
    }:
        errors.append("litigation status lifecycle is invalid")
    generation = document.get("bindingGeneration")
    if (
        not isinstance(generation, int)
        or isinstance(generation, bool)
        or generation < 0
    ):
        errors.append(
            "litigation bindingGeneration must be nonnegative integer"
        )
    matter_id = document.get("id")
    if not isinstance(matter_id, str) or not matter_id.strip():
        errors.append("litigation matter ID must be nonblank")
    return errors


def litigation_transition_errors(current, updated):
    errors = [
        *litigation_matter_errors(current),
        *litigation_matter_errors(updated),
    ]
    if current.get("id") != updated.get("id"):
        errors.append("litigation matter ID is immutable")
    current_status = current.get("status")
    current_generation = current.get("bindingGeneration")
    updated_status = updated.get("status")
    updated_generation = updated.get("bindingGeneration")
    if current_status == "active":
        if updated_status != "close-pending":
            errors.append("litigation matter must fence before archive")
        if (
            isinstance(current_generation, int)
            and not isinstance(current_generation, bool)
            and updated_generation != current_generation + 1
        ):
            errors.append("litigation fence must increment generation")
    elif current_status == "close-pending":
        if updated_status != "archived":
            errors.append("litigation fence must finalize archived")
        if updated_generation != current_generation:
            errors.append("litigation finalize must preserve generation")
    else:
        errors.append("litigation transition source is invalid")
    return errors


litigation_root = packages_root / "litigation-legal"
litigation_schema_path = (
    litigation_root / "references" / "litigation-record-schemas.md"
)
litigation_schema_text = litigation_schema_path.read_text(
    encoding="utf-8"
)
litigation_matter_section = litigation_schema_text.split(
    "## Matter\n",
    maxsplit=1,
)[1]
litigation_matter_match = re.search(
    r"```yaml\n(.*?)```",
    litigation_matter_section,
    flags=re.DOTALL,
)
if litigation_matter_match is None:
    raise SystemExit("litigation matter schema example is missing")
litigation_matter_template = yaml.safe_load(
    litigation_matter_match.group(1)
)
if (
    litigation_matter_template.get("status")
    != "active | close-pending | archived"
    or litigation_matter_template.get("bindingGeneration") != 0
):
    raise SystemExit(
        "litigation matter schema lacks fenced lifecycle fields"
    )

litigation_matter = {
    "id": "matter-1",
    "status": "active",
    "bindingGeneration": 0,
}
if litigation_matter_errors(litigation_matter):
    raise SystemExit("valid litigation matter fixture rejected")
fenced_litigation_matter = {
    **litigation_matter,
    "status": "close-pending",
    "bindingGeneration": 1,
}
if litigation_transition_errors(
    litigation_matter,
    fenced_litigation_matter,
):
    raise SystemExit("valid litigation fence rejected")
archived_litigation_matter = {
    **fenced_litigation_matter,
    "status": "archived",
}
if litigation_transition_errors(
    fenced_litigation_matter,
    archived_litigation_matter,
):
    raise SystemExit("valid litigation finalize rejected")

litigation_negative_profiles = (
    {**litigation_matter, "bindingGeneration": -1},
    {**litigation_matter, "bindingGeneration": True},
    {**litigation_matter, "bindingGeneration": "0"},
    {**litigation_matter, "status": "closed"},
)
for candidate in litigation_negative_profiles:
    if not litigation_matter_errors(candidate):
        raise SystemExit(
            "invalid litigation matter fixture was accepted"
        )

litigation_negative_transitions = (
    (
        litigation_matter,
        {**litigation_matter, "status": "archived"},
    ),
    (
        litigation_matter,
        {**litigation_matter, "status": "close-pending"},
    ),
    (
        fenced_litigation_matter,
        {
            **archived_litigation_matter,
            "bindingGeneration": 2,
        },
    ),
)
for transition in litigation_negative_transitions:
    if not litigation_transition_errors(*transition):
        raise SystemExit(
            "invalid litigation lifecycle transition was accepted"
        )

canonical_litigation_schema = litigation_schema_path.read_bytes()
litigation_schema_copies = sorted(
    (litigation_root / "skills").glob(
        "*/references/common/litigation-record-schemas.md"
    )
)
if not litigation_schema_copies:
    raise SystemExit("litigation schema common copies are missing")
for schema_copy in litigation_schema_copies:
    if schema_copy.read_bytes() != canonical_litigation_schema:
        raise SystemExit(
            f"{schema_copy}: litigation schema is not synced"
        )

matter_close_path = (
    litigation_root / "skills" / "matter-close" / "SKILL.md"
)
matter_close_text = matter_close_path.read_text(encoding="utf-8")
update_sequence = matter_close_text.split(
    "## Update sequence\n",
    maxsplit=1,
)[1].split("## Record", maxsplit=1)[0]
matter_close_fragments = (
    "最初のatomic conditional operation",
    "fence成功後",
    "activeだけをrevocation対象",
    "already-revokedはsatisfied",
    "zero active",
    "`status: archived`へconditional",
    "fence前にcommitしたcreate",
    "fence後のcreate",
    "fenced state",
)
for fragment in matter_close_fragments:
    if fragment not in update_sequence:
        raise SystemExit(
            f"{matter_close_path}: close sequence missing {fragment}"
        )
matter_close_order = (
    "最初のatomic conditional operation",
    "fence成功後",
    "activeだけをrevocation対象",
    "zero active",
    "`status: archived`へconditional",
)
matter_close_positions = tuple(
    update_sequence.index(fragment)
    for fragment in matter_close_order
)
if matter_close_positions != tuple(sorted(matter_close_positions)):
    raise SystemExit("litigation matter-close lifecycle order invalid")
for forbidden in (
    "matterを`status: archived`へconditional update",
    "全bindingをitemごとに`revoked`へconditional update",
    "matter archive後",
):
    if forbidden in matter_close_text:
        raise SystemExit(
            "litigation matter-close contains archive-first guidance"
        )

clinic_root = packages_root / "legal-clinic"
clinic_references = clinic_root / "references"
clinic_schema_path = (
    clinic_references / "clinic-state-payloads.schema.json"
)
clinic_examples_path = (
    clinic_references / "clinic-state-payload-examples.json"
)
clinic_negative_path = (
    clinic_references / "clinic-state-payload-negative-examples.json"
)
clinic_schema = json.loads(
    clinic_schema_path.read_text(encoding="utf-8")
)
clinic_examples = json.loads(
    clinic_examples_path.read_text(encoding="utf-8")
)
clinic_negative = json.loads(
    clinic_negative_path.read_text(encoding="utf-8")
)
jsonschema.Draft202012Validator.check_schema(clinic_schema)
clinic_validator = jsonschema.Draft202012Validator(
    clinic_schema,
    format_checker=format_checker,
)
for example_name in (
    "bindingCreateRequest",
    "sessionMatterBinding",
    "bindingRevocationBatch",
    "clinicMatter",
):
    clinic_validator.validate(clinic_examples[example_name])

clinic_create = clinic_examples["bindingCreateRequest"]
validate("create-request", clinic_create)
validate_session_binding_create(
    cast(SessionBindingCreateRequest, clinic_create),
    cast(MatterSnapshot, current_matter_for_create(clinic_create)),
)

clinic_batch = clinic_examples["bindingRevocationBatch"]
active_ids = set(clinic_batch["bindingItemIds"])
satisfied_ids = set(clinic_batch["alreadyRevokedBindingItemIds"])
enumerated_ids = set(clinic_batch["enumeratedBindingItemIds"])
result_ids = {
    result["bindingItemId"]
    for result in clinic_batch["results"]
}
if active_ids.intersection(satisfied_ids):
    raise SystemExit("clinic active/already-revoked sets overlap")
if enumerated_ids != active_ids.union(satisfied_ids):
    raise SystemExit("clinic binding enumeration partition invalid")
if result_ids != active_ids:
    raise SystemExit("clinic revoke results must match active bindings")
if clinic_batch["postRevocationActiveCount"] != 0:
    raise SystemExit("clinic revocation did not verify zero active")
if (
    clinic_batch["targetBindingGeneration"]
    != clinic_batch["sourceBindingGeneration"] + 1
):
    raise SystemExit("clinic fence generation did not increment")

clinic_active_matter = copy.deepcopy(clinic_examples["clinicMatter"])
clinic_archive_pending = copy.deepcopy(clinic_active_matter)
clinic_archive_pending.update(
    {
        "status": "archive-pending",
        "bindingGeneration": (
            clinic_active_matter["bindingGeneration"] + 1
        ),
        "lastBindingRevocationBatchId": (
            "correlation-archive-0001"
        ),
        "freshBindingRequired": True,
    }
)
clinic_archived = copy.deepcopy(clinic_archive_pending)
clinic_archived["status"] = "archived"
clinic_close_pending = copy.deepcopy(clinic_archive_pending)
clinic_close_pending.update(
    {
        "status": "close-pending",
        "lastBindingRevocationBatchId": "correlation-close-0001",
    }
)
clinic_closed = copy.deepcopy(clinic_close_pending)
clinic_closed["status"] = "closed"
for clinic_matter in (
    clinic_archive_pending,
    clinic_archived,
    clinic_close_pending,
    clinic_closed,
):
    clinic_validator.validate(clinic_matter)
if matter_access_allowed("active", True, "archive-pending"):
    raise SystemExit("clinic archive-pending matter access was allowed")
if matter_access_allowed("active", True, "close-pending"):
    raise SystemExit("clinic close-pending matter access was allowed")
if matter_access_allowed("active", True, "archived"):
    raise SystemExit("clinic archived matter access was allowed")
if matter_access_allowed("active", True, "closed"):
    raise SystemExit("clinic closed matter access was allowed")

negative_ids = {
    fixture["id"]
    for fixture in clinic_negative["fixtures"]
}
required_clinic_negatives = {
    "revocation-generation-not-incremented",
    "revocation-enumeration-missing-satisfied-binding",
    "revocation-active-already-revoked-overlap",
    "revocation-post-active-nonzero",
    "binding-create-missing-matter-precondition",
    "binding-create-negative-generation",
    "binding-create-wrong-matter-status",
    "clinic-matter-direct-archive",
}
if not required_clinic_negatives.issubset(negative_ids):
    raise SystemExit("clinic lifecycle negative fixtures are incomplete")

clinic_common_names = (
    "cowork-runtime-contract.md",
    "clinic-record-schemas.md",
    "clinic-state-payloads.schema.json",
    "clinic-state-payload-examples.json",
    "clinic-state-payload-negative-examples.json",
)
for common_name in clinic_common_names:
    canonical_path = clinic_references / common_name
    canonical_bytes = canonical_path.read_bytes()
    local_paths = sorted(
        (clinic_root / "skills").glob(
            f"*/references/common/{common_name}"
        )
    )
    if not local_paths:
        raise SystemExit(
            f"legal-clinic: no common copies for {common_name}"
        )
    for local_path in local_paths:
        if local_path.read_bytes() != canonical_bytes:
            raise SystemExit(
                f"{local_path}: clinic common copy is not synced"
            )

# Jurisdiction projections are owned by test-m365-reference-projection.sh.
currency_watch_source = b"jurisdictions/ja-jp/"
currency_watch_replacement = b"ja-jp/"
canonical_references = {}
for path in (ai_root / "references").rglob("*"):
    relative = path.relative_to(ai_root / "references")
    if path.is_file() and relative.parts[0] != "jurisdictions":
        data = path.read_bytes()
        if relative == pathlib.Path("currency-watch.md"):
            if data.count(currency_watch_source) != 1:
                raise SystemExit(
                    "AI currency watch transform source count changed"
                )
            data = data.replace(
                currency_watch_source,
                currency_watch_replacement,
            )
        canonical_references[relative] = data
for skill_path in sorted((ai_root / "skills").iterdir()):
    if not skill_path.is_dir():
        continue
    common_root = skill_path / "references" / "common"
    local_references = {}
    for path in common_root.rglob("*"):
        relative = path.relative_to(common_root)
        if (
            path.is_file()
            and relative.parts[0] not in {"jurisdictions", "ja-jp"}
        ):
            local_references[relative] = path.read_bytes()
    if local_references != canonical_references:
        raise SystemExit(
            f"{skill_path}: state references are not byte-for-byte synced"
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
