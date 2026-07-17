#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Validate Legal Clinic binding fences and matter transitions.

This module keeps the lifecycle state machine separate from the general
fixture runner. It validates atomic binding creation, fenced archive and close
batches, and the permitted matter transitions produced by those batches.
"""

from __future__ import annotations

from typing import Final

type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]
type BindingPartitions = tuple[list[str], list[str], list[str]]

_NON_ACTIVE_MATTER_STATUSES: Final = frozenset(
    {
        "archive-pending",
        "archived",
        "close-pending",
        "closed",
        "reactivation-pending",
    },
)


def _as_object(value: JsonValue) -> JsonObject:
    if not isinstance(value, dict):
        raise TypeError
    return value


def _string_list(value: JsonValue) -> list[str] | None:
    if not isinstance(value, list):
        return None
    strings: list[str] = []
    for item in value:
        if not isinstance(item, str):
            return None
        strings.append(item)
    return strings


def revocation_generation_errors(document: JsonObject) -> list[str]:
    """Validate the atomic fence generation increment."""
    source = document.get("sourceBindingGeneration")
    target = document.get("targetBindingGeneration")
    valid = (
        isinstance(source, int)
        and not isinstance(source, bool)
        and target == source + 1
    )
    if valid:
        return []
    return ["target binding generation must equal source plus one"]


def _revocation_partitions(
    document: JsonObject,
) -> BindingPartitions | None:
    enumerated = _string_list(document.get("enumeratedBindingItemIds"))
    active = _string_list(document.get("bindingItemIds"))
    satisfied = _string_list(
        document.get("alreadyRevokedBindingItemIds"),
    )
    if enumerated is None:
        return None
    if active is None:
        return None
    if satisfied is None:
        return None
    return enumerated, active, satisfied


def revocation_enumeration_errors(document: JsonObject) -> list[str]:
    """Validate the disjoint complete binding enumeration."""
    partitions = _revocation_partitions(document)
    if partitions is None:
        return ["binding enumeration partition is incomplete"]
    enumerated, active, satisfied = partitions
    errors: list[str] = []
    if set(active).intersection(satisfied):
        errors.append(
            "active and already-revoked binding IDs must be disjoint",
        )
    if set(enumerated) != set(active).union(satisfied):
        errors.append(
            "enumerated bindings must equal active plus already-revoked",
        )
    return errors


def _binding_identity_errors(
    document: JsonObject,
    payload: JsonObject,
) -> list[str]:
    errors = [
        f"binding create {field} must match payload"
        for field in ("tenantId", "practiceId")
        if document.get(field) != payload.get(field)
    ]
    expected_scope = (
        f"{payload.get('userObjectId')}:{payload.get('sessionId')}"
    )
    if document.get("scopeId") != expected_scope:
        errors.append("binding create scopeId must match user and session")
    return errors


def _binding_precondition_errors(
    precondition: JsonObject,
) -> list[str]:
    errors: list[str] = []
    if precondition.get("expectedStatus") != "active":
        errors.append("binding create must expect active matter")
    if precondition.get("atomicWithBindingExpectedAbsent") is not True:
        errors.append("binding and matter preconditions must be atomic")
    return errors


def binding_create_errors(document: JsonObject) -> list[str]:
    """Validate one atomic session binding create request."""
    payload = document.get("payload")
    precondition = document.get("matterPrecondition")
    if not isinstance(payload, dict) or not isinstance(precondition, dict):
        return ["binding create payload and matter precondition are required"]
    errors = _binding_identity_errors(document, payload)
    errors.extend(_binding_precondition_errors(precondition))
    return errors


def _active_matter_errors(
    batch_id: JsonValue,
    fresh_binding: JsonValue,
) -> list[str]:
    if batch_id is None and fresh_binding is False:
        return []
    return ["active matter must not retain a revocation batch"]


def _non_active_matter_errors(
    batch_id: JsonValue,
    fresh_binding: JsonValue,
) -> list[str]:
    if isinstance(batch_id, str) and batch_id and fresh_binding is True:
        return []
    return ["non-active matter requires batch ID and fresh binding"]


def clinic_matter_errors(document: JsonObject) -> list[str]:
    """Validate matter status evidence and fresh-binding controls."""
    status = document.get("status")
    batch_id = document.get("lastBindingRevocationBatchId")
    fresh_binding = document.get("freshBindingRequired")
    if status == "active":
        return _active_matter_errors(batch_id, fresh_binding)
    if status in _NON_ACTIVE_MATTER_STATUSES:
        return _non_active_matter_errors(batch_id, fresh_binding)
    return []


def _immutable_matter_errors(
    current: JsonObject,
    updated: JsonObject,
) -> list[str]:
    return [
        f"clinic matter {field} is immutable"
        for field in ("tenantId", "practiceId", "matterId", "itemId")
        if current.get(field) != updated.get(field)
    ]


def _active_transition_errors(
    current_generation: JsonValue,
    updated_status: JsonValue,
    updated_generation: JsonValue,
) -> list[str]:
    errors: list[str] = []
    if updated_status not in {"archive-pending", "close-pending"}:
        errors.append("active matter must transition to a pending fence")
    valid_generation = (
        isinstance(current_generation, int)
        and not isinstance(current_generation, bool)
        and updated_generation == current_generation + 1
    )
    if not valid_generation:
        errors.append("matter fence must increment bindingGeneration")
    return errors


def _pending_transition_errors(
    current_generation: JsonValue,
    updated_status: JsonValue,
    updated_generation: JsonValue,
    *,
    expected_status: str,
    label: str,
) -> list[str]:
    errors: list[str] = []
    if updated_status != expected_status:
        errors.append(f"{label} fence must finalize {expected_status}")
    if updated_generation != current_generation:
        errors.append(f"{label} finalize must preserve generation")
    return errors


def _status_transition_errors(
    current: JsonObject,
    updated: JsonObject,
) -> list[str]:
    current_status = current.get("status")
    updated_status = updated.get("status")
    current_generation = current.get("bindingGeneration")
    updated_generation = updated.get("bindingGeneration")
    if current_status == "active":
        return _active_transition_errors(
            current_generation,
            updated_status,
            updated_generation,
        )
    if current_status == "archive-pending":
        return _pending_transition_errors(
            current_generation,
            updated_status,
            updated_generation,
            expected_status="archived",
            label="archive",
        )
    if current_status == "close-pending":
        return _pending_transition_errors(
            current_generation,
            updated_status,
            updated_generation,
            expected_status="closed",
            label="close",
        )
    return ["clinic matter transition source is invalid"]


def _matter_transition_errors(
    current: JsonObject,
    updated: JsonObject,
) -> list[str]:
    errors = _immutable_matter_errors(current, updated)
    errors.extend(_status_transition_errors(current, updated))
    return errors


def matter_lifecycle_failures(
    examples: dict[str, JsonValue],
) -> list[str]:
    """Validate every positive fenced matter transition pair."""
    pairs = (
        ("clinicMatter", "clinicMatterArchivePending"),
        ("clinicMatterArchivePending", "clinicMatterArchived"),
        ("clinicMatter", "clinicMatterClosePending"),
        ("clinicMatterClosePending", "clinicMatterClosed"),
    )
    failures: list[str] = []
    for current_name, updated_name in pairs:
        current = _as_object(examples[current_name])
        updated = _as_object(examples[updated_name])
        errors = _matter_transition_errors(current, updated)
        if errors:
            failures.append(
                f"matter transition {current_name}->{updated_name}: "
                f"{errors[0]}",
            )
    return failures
