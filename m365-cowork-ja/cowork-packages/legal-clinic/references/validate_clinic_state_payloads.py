#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Validate legal-clinic schemas, examples, and semantic invariants.

The validator applies four independent layers. It checks the authoritative
package schema with format validation, evaluates cross-field semantic rules,
rejects every declared negative fixture, and verifies byte parity across all
skill-local copies.

Tracker and workflow-cursor records receive an additional shared-envelope
validation pass. Cursor records must keep source metadata inside ``payload``,
use lowercase 64-character SHA-256 fingerprints, and repeat the exact
fingerprint as the final colon-delimited component of ``recordId``.

Matter archive and close batches must increment the binding generation and
partition the complete fenced enumeration into disjoint active and
already-revoked sets before finalization.

Lifecycle-specific checks are delegated to a focused companion module so the
fixture runner remains independently auditable while both modules retain
strict type, lint, security, and complexity gates.

Every validation class must contain at least one example so a missing fixture
set cannot produce a vacuous success.
"""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Final, NamedTuple, cast

from clinic_lifecycle_validation import (
    binding_create_errors,
    clinic_matter_errors,
    matter_lifecycle_failures,
    revocation_enumeration_errors,
    revocation_generation_errors,
)
from jsonschema import Draft202012Validator, FormatChecker

type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]
type JsonContainer = list[JsonValue] | JsonObject

_SHA256_PATTERN: Final = re.compile(r"^[0-9a-f]{64}$")
_SHARED_ENVELOPE_RECORD_TYPES: Final = frozenset(
    {"tracker-record", "workflow-cursor"},
)


class EnvelopeCounts(NamedTuple):
    """Hold shared-envelope tracker and cursor validation counts."""

    tracker: int
    cursor: int


ROOT: Final = Path(__file__).resolve().parent
PACKAGE_ROOT: Final = ROOT.parent
SCHEMA_PATH: Final = ROOT / "clinic-state-payloads.schema.json"
EXAMPLES_PATH: Final = ROOT / "clinic-state-payload-examples.json"
NEGATIVE_PATH: Final = (
    ROOT / "clinic-state-payload-negative-examples.json"
)
STATE_ENVELOPE_SCHEMA_PATH: Final = (
    ROOT.parents[2]
    / "state-service"
    / "schemas"
    / "state-envelope.schema.json"
)


def _load_object(path: Path) -> JsonObject:
    value = cast(
        "JsonValue",
        json.loads(path.read_text(encoding="utf-8")),
    )
    if not isinstance(value, dict):
        raise TypeError
    return value


def _as_object(value: JsonValue) -> JsonObject:
    if not isinstance(value, dict):
        raise TypeError
    return value


def _as_object_list(value: JsonValue) -> list[JsonObject]:
    if not isinstance(value, list):
        raise TypeError
    return [_as_object(item) for item in value]


def _required_string(document: JsonObject, key: str) -> str:
    value = document.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError
    return value


def _pointer_parts(pointer: str) -> list[str]:
    parts = [
        part.replace("~1", "/").replace("~0", "~")
        for part in pointer.lstrip("/").split("/")
        if part
    ]
    if not parts:
        raise ValueError
    return parts


def _pointer_parent(
    document: JsonValue,
    pointer: str,
) -> tuple[JsonContainer, str]:
    parts = _pointer_parts(pointer)
    parent = document
    for part in parts[:-1]:
        if isinstance(parent, list):
            parent = parent[int(part)]
        elif isinstance(parent, dict):
            parent = parent[part]
        else:
            raise TypeError
    if not isinstance(parent, (dict, list)):
        raise TypeError
    return parent, parts[-1]


def _write_patch(
    parent: JsonContainer,
    key: str,
    value: JsonValue,
    *,
    insert: bool,
) -> None:
    if isinstance(parent, dict):
        parent[key] = value
    elif insert and key == "-":
        parent.append(value)
    elif insert:
        parent.insert(int(key), value)
    else:
        parent[int(key)] = value


def _remove_patch(parent: JsonContainer, key: str) -> None:
    if isinstance(parent, dict):
        del parent[key]
    else:
        del parent[int(key)]


def _apply_operation(
    document: JsonValue,
    operation: JsonObject,
) -> None:
    action = _required_string(operation, "op")
    path = _required_string(operation, "path")
    parent, key = _pointer_parent(document, path)
    if action in {"add", "replace"}:
        _write_patch(
            parent,
            key,
            operation.get("value"),
            insert=action == "add",
        )
    elif action == "remove":
        _remove_patch(parent, key)
    else:
        raise ValueError


def _apply_patch(
    document: JsonValue,
    operations: list[JsonObject],
) -> JsonValue:
    result = copy.deepcopy(document)
    for operation in operations:
        _apply_operation(result, operation)
    return result


def _template_data(
    value: JsonValue,
) -> tuple[str, list[JsonObject]] | None:
    if not isinstance(value, dict) or "$baseExample" not in value:
        return None
    return (
        _required_string(value, "$baseExample"),
        _as_object_list(value.get("$patch", [])),
    )


def _expand_example(
    name: str,
    raw_examples: JsonObject,
    expanded: dict[str, JsonValue],
    active: set[str],
) -> JsonValue:
    if name in expanded:
        return expanded[name]
    if name in active or name not in raw_examples:
        raise ValueError
    active.add(name)
    value = raw_examples[name]
    template = _template_data(value)
    if template is not None:
        base_name, operations = template
        base = _expand_example(
            base_name,
            raw_examples,
            expanded,
            active,
        )
        value = _apply_patch(base, operations)
    expanded[name] = value
    active.remove(name)
    return value


def _expand_examples(raw_examples: JsonObject) -> dict[str, JsonValue]:
    expanded: dict[str, JsonValue] = {}
    for name in raw_examples:
        _expand_example(name, raw_examples, expanded, set())
    return expanded


def _tracker_scope_errors(document: JsonObject) -> list[str]:
    if document.get("scopeType") == "matter":
        return []
    return ["tracker scopeType must be matter"]


def _tracker_matter_errors(
    document: JsonObject,
    payload: JsonObject,
) -> list[str]:
    matter_id = payload.get("matterId")
    if not isinstance(matter_id, str) or not matter_id:
        return ["tracker payload must contain matterId"]
    if document.get("scopeId") != matter_id:
        return ["tracker scopeId must equal payload matterId"]
    return []


def _tracker_identity_errors(
    document: JsonObject,
    payload: JsonObject,
) -> list[str]:
    return [
        (
            f"tracker payload {field_name} must match outer "
            f"{field_name}"
        )
        for field_name in ("tenantId", "practiceId")
        if field_name in payload
        and payload[field_name] != document.get(field_name)
    ]


def _tracker_errors(document: JsonObject) -> list[str]:
    errors = _tracker_scope_errors(document)
    payload = document.get("payload")
    if not isinstance(payload, dict):
        return [*errors, "tracker payload must be an object"]
    errors.extend(_tracker_matter_errors(document, payload))
    errors.extend(_tracker_identity_errors(document, payload))
    return errors


def _sha256_value_error(value: JsonValue, field: str) -> str | None:
    if (
        not isinstance(value, str)
        or _SHA256_PATTERN.fullmatch(value) is None
    ):
        return f"{field} must match ^[0-9a-f]{{64}}$"
    return None


def _cursor_match_error(
    record_suffix: str,
    query_fingerprint: str,
) -> str | None:
    if record_suffix != query_fingerprint:
        return (
            "cursor recordId final component must equal "
            "payload queryFingerprint"
        )
    return None


def _cursor_record_errors(
    record_id: JsonValue,
    query_fingerprint: str,
) -> list[str]:
    if not isinstance(record_id, str):
        return ["cursor recordId must be a string"]
    record_suffix = record_id.rsplit(":", 1)[-1]
    suffix_error = _sha256_value_error(
        record_suffix,
        "cursor recordId suffix",
    )
    if suffix_error is not None:
        return [suffix_error]
    match_error = _cursor_match_error(
        record_suffix,
        query_fingerprint,
    )
    return [] if match_error is None else [match_error]


def _cursor_errors(document: JsonObject) -> list[str]:
    payload = document.get("payload")
    if not isinstance(payload, dict):
        return ["cursor payload must be an object"]
    query_fingerprint = payload.get("queryFingerprint")
    query_error = _sha256_value_error(
        query_fingerprint,
        "cursor payload queryFingerprint",
    )
    if query_error is not None:
        return [query_error]
    return _cursor_record_errors(
        document.get("recordId"),
        cast("str", query_fingerprint),
    )


def _string_list(value: JsonValue) -> list[str] | None:
    if not isinstance(value, list):
        return None
    if not all(isinstance(item, str) for item in value):
        return None
    return list(cast("list[str]", value))


def _revocation_result_ids(
    value: JsonValue,
) -> tuple[list[str], list[JsonObject]] | None:
    if not isinstance(value, list):
        return None
    results: list[JsonObject] = []
    identifiers: list[str] = []
    for item in value:
        result = _as_object(item)
        identifiers.append(_required_string(result, "bindingItemId"))
        results.append(result)
    return identifiers, results


def _revocation_coverage_errors(
    binding_ids: list[str],
    result_ids: list[str],
) -> list[str]:
    errors: list[str] = []
    if len(result_ids) != len(set(result_ids)):
        errors.append("result binding IDs must be unique")
    if len(binding_ids) != len(result_ids):
        errors.append("binding IDs and results must have identical length")
    if set(binding_ids) != set(result_ids):
        errors.append("binding IDs and result IDs must be an exact set")
    return errors


def _revocation_outcome_errors(
    results: list[JsonObject],
) -> list[str]:
    if all(result.get("outcome") == "revoked" for result in results):
        return []
    return ["every successful batch result must be revoked"]


def _revocation_transition_errors(
    document: JsonObject,
) -> list[str]:
    transition = document.get("transition")
    expected = {
        "archive": ("archive-pending", "archived"),
        "close": ("close-pending", "closed"),
    }.get(transition) if isinstance(transition, str) else None
    actual = (
        document.get("fencedMatterStatus"),
        document.get("targetMatterStatus"),
    )
    if expected == actual:
        return []
    return ["transition, fence status, and target status do not correlate"]


def _revocation_errors(document: JsonObject) -> list[str]:
    binding_ids = _string_list(document.get("bindingItemIds"))
    parsed_results = _revocation_result_ids(document.get("results"))
    if binding_ids is None or parsed_results is None:
        return ["successful batch lacks binding IDs or results"]
    result_ids, results = parsed_results
    errors = _revocation_coverage_errors(binding_ids, result_ids)
    errors.extend(_revocation_outcome_errors(results))
    errors.extend(_revocation_transition_errors(document))
    errors.extend(revocation_generation_errors(document))
    errors.extend(revocation_enumeration_errors(document))
    if document.get("postRevocationActiveCount") != 0:
        errors.append("successful revocation must verify zero active bindings")
    return errors


def _successful_revocation_batch(
    document: JsonObject,
    record_type: JsonValue,
) -> bool:
    return (
        record_type == "binding-revocation-batch"
        and document.get("atomicOutcome") == "succeeded"
    )


def _direct_record_errors(
    document: JsonObject,
    record_type: JsonValue,
) -> list[str] | None:
    if record_type == "tracker-record":
        return _tracker_errors(document)
    if record_type == "workflow-cursor":
        return _cursor_errors(document)
    if record_type == "clinic-matter":
        return clinic_matter_errors(document)
    return None


def _binding_create_request(
    document: JsonObject,
    record_type: JsonValue,
) -> bool:
    return (
        record_type == "session-matter-binding"
        and "expectedAbsent" in document
    )


def _semantic_errors(document: JsonValue) -> list[str]:
    if not isinstance(document, dict):
        return []
    record_type = document.get("recordType")
    direct_errors = _direct_record_errors(document, record_type)
    if direct_errors is not None:
        return direct_errors
    if _binding_create_request(document, record_type):
        return binding_create_errors(document)
    if _successful_revocation_batch(document, record_type):
        return _revocation_errors(document)
    return []


def _schema_errors(
    validator: Draft202012Validator,
    document: JsonValue,
) -> list[str]:
    return [
        error.message
        for error in validator.iter_errors(document)
    ]


def _copy_paths(canonical_path: Path) -> list[Path]:
    return sorted(
        PACKAGE_ROOT.glob(
            f"skills/*/references/common/{canonical_path.name}",
        ),
    )


def _copy_failures(
    canonical_path: Path,
    copy_paths: list[Path],
) -> list[str]:
    canonical_bytes = canonical_path.read_bytes()
    return [
        f"byte parity mismatch: {copy_path}"
        for copy_path in copy_paths
        if copy_path.read_bytes() != canonical_bytes
    ]


def _parity_failures() -> tuple[list[str], list[Path]]:
    failures: list[str] = []
    example_paths = [EXAMPLES_PATH]
    for canonical_path in (SCHEMA_PATH, EXAMPLES_PATH, NEGATIVE_PATH):
        copy_paths = _copy_paths(canonical_path)
        if not copy_paths:
            failures.append(
                f"{canonical_path.name}: no skill-local copies",
            )
        else:
            failures.extend(
                _copy_failures(canonical_path, copy_paths),
            )
        if canonical_path == EXAMPLES_PATH:
            example_paths.extend(copy_paths)
    return failures, example_paths


def _envelope_record_type(document: JsonValue) -> str | None:
    if not isinstance(document, dict):
        return None
    record_type = document.get("recordType")
    if (
        isinstance(record_type, str)
        and record_type in _SHARED_ENVELOPE_RECORD_TYPES
    ):
        return record_type
    return None


def _updated_envelope_counts(
    counts: EnvelopeCounts,
    record_type: str,
) -> EnvelopeCounts:
    if record_type == "tracker-record":
        return EnvelopeCounts(counts.tracker + 1, counts.cursor)
    return EnvelopeCounts(counts.tracker, counts.cursor + 1)


def _missing_envelope_failure(
    example_path: Path,
    counts: EnvelopeCounts,
) -> str | None:
    if counts.tracker + counts.cursor == 0:
        return f"shared envelope {example_path}: no envelope examples"
    return None


def _path_envelope_failures(
    validator: Draft202012Validator,
    example_path: Path,
) -> tuple[list[str], EnvelopeCounts]:
    failures: list[str] = []
    counts = EnvelopeCounts(0, 0)
    examples = _expand_examples(_load_object(example_path))
    for name, document in examples.items():
        record_type = _envelope_record_type(document)
        if record_type is None:
            continue
        counts = _updated_envelope_counts(counts, record_type)
        errors = _schema_errors(validator, document)
        if errors:
            failures.append(
                f"shared envelope {example_path}:{name}: {errors[0]}",
            )
    missing_failure = _missing_envelope_failure(example_path, counts)
    if missing_failure is not None:
        failures.append(missing_failure)
    return failures, counts


def _shared_envelope_failures(
    validator: Draft202012Validator,
    example_paths: list[Path],
) -> tuple[list[str], EnvelopeCounts]:
    failures: list[str] = []
    counts = EnvelopeCounts(0, 0)
    for example_path in example_paths:
        path_failures, path_counts = _path_envelope_failures(
            validator,
            example_path,
        )
        failures.extend(path_failures)
        counts = EnvelopeCounts(
            counts.tracker + path_counts.tracker,
            counts.cursor + path_counts.cursor,
        )
    return failures, counts


def _example_object(
    examples: dict[str, JsonValue],
    name: str,
) -> JsonObject:
    return copy.deepcopy(_as_object(examples[name]))


def _setup_without_profile(
    examples: dict[str, JsonValue],
) -> JsonObject:
    document = _example_object(examples, "setupSession")
    payload = _as_object(document["payload"])
    payload["profileItemId"] = None
    payload["profileVersion"] = None
    payload["profileETag"] = None
    return document


def _close_batch(examples: dict[str, JsonValue]) -> JsonObject:
    document = _example_object(examples, "bindingRevocationBatch")
    document["transition"] = "close"
    document["fencedMatterStatus"] = "close-pending"
    document["targetMatterStatus"] = "closed"
    return document


def _closed_deadline(
    examples: dict[str, JsonValue],
) -> JsonObject:
    document = _example_object(examples, "trackerRecordDeadline")
    payload = _as_object(document["payload"])
    payload["lifecycleStatus"] = "closed"
    payload["closure"] = {
        "reason": "A versioned order superseded the candidate.",
        "authorityApprovalId": "approval-close-1",
        "closedAt": "2026-07-16T16:00:00+09:00",
        "closedByObjectId": "lawyer-object-1",
        "sourceEvidence": [
            {
                "sourceItemId": "court-order-close-1",
                "sourceVersion": "2",
                "authorityType": "matter-document",
                "officialUrl": None,
                "effectiveDate": None,
                "retrievedAt": "2026-07-16T15:30:00+09:00",
                "reviewStatus": "approved",
            },
        ],
    }
    return document


def _review_example(
    examples: dict[str, JsonValue],
    subjects: list[JsonValue],
    role: str,
) -> JsonObject:
    document = _example_object(examples, "trackerRecordReview")
    payload = _as_object(document["payload"])
    payload["reviewSubjectTypes"] = subjects
    payload["requiredReviewerRole"] = role
    payload["legalAndLanguageReview"] = {
        "required": False,
        "status": "not-required",
        "responsibleLawyerObjectId": None,
        "responsibleLawyerReviewedAt": None,
        "languageReviewerObjectId": None,
        "languageReviewerCompetenceRecordId": None,
        "languageReviewedAt": None,
    }
    return document


def _duplicated_identity_tracker(
    examples: dict[str, JsonValue],
) -> JsonObject:
    document = _example_object(
        examples,
        "trackerRecordCommunication",
    )
    payload = _as_object(document["payload"])
    payload["tenantId"] = document["tenantId"]
    payload["practiceId"] = document["practiceId"]
    return document


def _synthetic_examples(
    examples: dict[str, JsonValue],
) -> dict[str, JsonValue]:
    return {
        "setupSessionAllNullProfileReference": (
            _setup_without_profile(examples)
        ),
        "bindingRevocationBatchClose": _close_batch(examples),
        "trackerRecordDeadlineClosed": _closed_deadline(examples),
        "trackerRecordSupervisorAdminReview": _review_example(
            examples,
            ["admin"],
            "supervisor",
        ),
        "trackerRecordMixedReview": _review_example(
            examples,
            ["external-legal-content", "admin"],
            "both",
        ),
        "trackerRecordMatchingDuplicatedIdentity": (
            _duplicated_identity_tracker(examples)
        ),
    }


def _positive_failures(
    validator: Draft202012Validator,
    state_envelope_validator: Draft202012Validator,
    examples: dict[str, JsonValue],
) -> list[str]:
    positives = {**examples, **_synthetic_examples(examples)}
    failures: list[str] = []
    for name, document in positives.items():
        errors = [
            *_schema_errors(validator, document),
            *_semantic_errors(document),
        ]
        if (
            isinstance(document, dict)
            and document.get("recordType")
            in _SHARED_ENVELOPE_RECORD_TYPES
        ):
            errors.extend(
                _schema_errors(state_envelope_validator, document),
            )
        if errors:
            failures.append(f"positive {name}: {errors[0]}")
    return failures


def _negative_failure(
    validator: Draft202012Validator,
    examples: dict[str, JsonValue],
    fixture: JsonObject,
) -> str | None:
    base_name = _required_string(fixture, "baseExample")
    operations = _as_object_list(fixture.get("patch", []))
    document = _apply_patch(examples[base_name], operations)
    schema_errors = _schema_errors(validator, document)
    semantic_errors = _semantic_errors(document)
    layer = _required_string(fixture, "expectedFailure")
    rejected = {
        "schema": bool(schema_errors),
        "semantic": bool(semantic_errors),
    }.get(layer, bool([*schema_errors, *semantic_errors]))
    if rejected:
        return None
    fixture_id = _required_string(fixture, "id")
    return f"negative {fixture_id}: bypass was accepted"


def _negative_failures(
    validator: Draft202012Validator,
    examples: dict[str, JsonValue],
    negative: JsonObject,
) -> tuple[list[str], int]:
    fixtures = _as_object_list(negative.get("fixtures", []))
    failures = [
        failure
        for fixture in fixtures
        if (
            failure := _negative_failure(
                validator,
                examples,
                fixture,
            )
        )
    ]
    return failures, len(fixtures)


def main() -> int:
    """Validate the canonical schema and all fixture classes.

    Returns
    -------
    int
        Zero when positive and bypass-negative validation succeeds.

    """
    schema = _load_object(SCHEMA_PATH)
    state_envelope_schema = _load_object(STATE_ENVELOPE_SCHEMA_PATH)
    examples = _expand_examples(_load_object(EXAMPLES_PATH))
    negative = _load_object(NEGATIVE_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator.check_schema(state_envelope_schema)
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )
    state_envelope_validator = Draft202012Validator(
        state_envelope_schema,
        format_checker=FormatChecker(),
    )
    parity_failures, example_paths = _parity_failures()
    failures = [
        *parity_failures,
        *_positive_failures(
            validator,
            state_envelope_validator,
            examples,
        ),
        *matter_lifecycle_failures(examples),
    ]
    envelope_failures, envelope_counts = _shared_envelope_failures(
        state_envelope_validator,
        example_paths,
    )
    failures.extend(envelope_failures)
    negative_failures, negative_count = _negative_failures(
        validator,
        examples,
        negative,
    )
    failures.extend(negative_failures)
    if failures:
        sys.stderr.write(
            "".join(f"ERROR: {failure}\n" for failure in failures),
        )
        return 1
    positive_count = len(examples) + len(_synthetic_examples(examples))
    sys.stdout.write(
        "clinic state payload validation: "
        f"{positive_count} positive, "
        f"{negative_count} bypass-negative, "
        f"{envelope_counts.tracker} tracker and "
        f"{envelope_counts.cursor} cursor shared-envelope copies OK\n",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
