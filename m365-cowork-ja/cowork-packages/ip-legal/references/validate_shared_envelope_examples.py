#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Validate canonical and packaged shared-envelope examples."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Final, NamedTuple, TypeGuard, cast

from jsonschema import Draft202012Validator, FormatChecker

type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]
type CursorComponents = tuple[str, str]

_AUDIT_PACKAGE: Final = "legal-builder-hub"
_AUDIT_HEADING: Final = "## Canonical audit event"
_CURSOR_HEADING: Final = "## Scope別cursor"
_CONTRACT_NAME: Final = "cowork-runtime-contract.md"
_JSON_FENCE: Final = "```json\n"
_FENCE_END: Final = "\n```"
_MISMATCH_SUFFIX: Final = "-mismatch"


class EnvelopeValidationError(ValueError):
    """Report an invalid example or inconsistent packaged copy."""


class ValidationSettings(NamedTuple):
    """Hold paths and mode for one package validation run."""

    package_root: Path
    schema_path: Path
    canonical_path: Path
    heading: str
    kind: str
    is_audit: bool


class ValidationResult(NamedTuple):
    """Hold successful positive and negative validation counts."""

    example_count: int
    mismatch_count: int


def _error(context: str, detail: str) -> EnvelopeValidationError:
    """Build a contextual validation error."""
    return EnvelopeValidationError(f"{context}: {detail}")


def _json_array(value: list[object]) -> bool:
    """Return whether every array member is a JSON value."""
    return all(_is_json_value(item) for item in value)


def _json_mapping(value: dict[object, object]) -> bool:
    """Return whether a mapping is a JSON object."""
    return all(
        isinstance(key, str) and _is_json_value(item)
        for key, item in value.items()
    )


def _is_json_value(value: object) -> TypeGuard[JsonValue]:
    """Return whether a value belongs to the recursive JSON type."""
    if value is None or isinstance(value, str | int | float | bool):
        return True
    if isinstance(value, list):
        return _json_array(cast("list[object]", value))
    return (
        isinstance(value, dict)
        and _json_mapping(cast("dict[object, object]", value))
    )


def _is_json_object(value: object) -> TypeGuard[JsonObject]:
    """Return whether a value is a string-keyed JSON object."""
    return (
        isinstance(value, dict)
        and _json_mapping(cast("dict[object, object]", value))
    )


def _read_text(path: Path) -> str:
    """Read one UTF-8 text file with contextual errors."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise _error(
            path.as_posix(),
            f"cannot read UTF-8 text: {error}",
        ) from error


def _read_bytes(path: Path) -> bytes:
    """Read one file as bytes with contextual errors."""
    try:
        return path.read_bytes()
    except OSError as error:
        raise _error(path.as_posix(), f"cannot read bytes: {error}") from error


def _decode_object(text: str, context: str) -> JsonObject:
    """Decode and type-check one JSON object."""
    try:
        raw: object = json.loads(text)
    except json.JSONDecodeError as error:
        raise _error(context, f"invalid JSON: {error}") from error
    if _is_json_object(raw):
        return raw
    raise _error(context, "JSON root must be an object")


def _load_object(path: Path) -> JsonObject:
    """Load one UTF-8 JSON object."""
    return _decode_object(_read_text(path), path.as_posix())


def _after_marker(text: str, marker: str, context: str) -> str:
    """Return text after a required marker."""
    _, separator, remainder = text.partition(marker)
    if separator:
        return remainder
    raise _error(context, f"missing marker {marker!r}")


def _before_marker(text: str, marker: str, context: str) -> str:
    """Return text before a required marker."""
    prefix, separator, _ = text.partition(marker)
    if separator:
        return prefix
    raise _error(context, f"missing marker {marker!r}")


def _settings(entry_path: Path) -> ValidationSettings:
    """Build package-specific paths and validation mode."""
    package_root = entry_path.resolve().parent.parent
    m365_root = package_root.parent.parent
    is_audit = package_root.name == _AUDIT_PACKAGE
    schema_name = (
        "audit-event.schema.json"
        if is_audit
        else "state-envelope.schema.json"
    )
    canonical_path = (
        package_root / "references" / "common" / _CONTRACT_NAME
        if is_audit
        else package_root / "references" / _CONTRACT_NAME
    )
    return ValidationSettings(
        package_root=package_root,
        schema_path=m365_root / "state-service" / "schemas" / schema_name,
        canonical_path=canonical_path,
        heading=_AUDIT_HEADING if is_audit else _CURSOR_HEADING,
        kind="audit" if is_audit else "cursor",
        is_audit=is_audit,
    )


def _local_paths(package_root: Path) -> tuple[Path, ...]:
    """Return every skill-local runtime contract copy."""
    paths = tuple(
        sorted(
            package_root.glob(
                "skills/*/references/common/cowork-runtime-contract.md",
            ),
        ),
    )
    if paths:
        return paths
    raise _error(package_root.name, "no skill-local contract copies")


def _verify_parity(
    canonical_path: Path,
    local_paths: tuple[Path, ...],
) -> None:
    """Require every local copy to equal the canonical bytes."""
    canonical_bytes = _read_bytes(canonical_path)
    for path in local_paths:
        if _read_bytes(path) != canonical_bytes:
            raise _error(path.as_posix(), "byte parity mismatch")


def _extract_example(path: Path, heading: str) -> JsonObject:
    """Extract one fenced JSON example after a required heading."""
    context = path.as_posix()
    section = _after_marker(_read_text(path), f"{heading}\n", context)
    fenced = _after_marker(section, _JSON_FENCE, context)
    block = _before_marker(fenced, _FENCE_END, context)
    return _decode_object(block, context)


def _schema_validator(schema_path: Path) -> Draft202012Validator:
    """Build a format-checking Draft 2020-12 validator."""
    schema = _load_object(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )


def _first_schema_error(
    validator: Draft202012Validator,
    document: JsonObject,
) -> str | None:
    """Return the first deterministic schema error message."""
    errors = sorted(
        validator.iter_errors(document),
        key=lambda error: tuple(str(part) for part in error.path),
    )
    return errors[0].message if errors else None


def _cursor_components(
    document: JsonObject,
) -> CursorComponents | str:
    """Return validated cursor components or a field error."""
    record_id = document.get("recordId")
    if not isinstance(record_id, str):
        return "cursor recordId must be a string"
    payload = document.get("payload")
    if not isinstance(payload, dict):
        return "cursor payload must be an object"
    query_fingerprint = payload.get("queryFingerprint")
    if not isinstance(query_fingerprint, str):
        return "cursor payload.queryFingerprint must be a string"
    if not query_fingerprint:
        return "cursor payload.queryFingerprint must be a non-empty string"
    return record_id, query_fingerprint


def _cursor_invariant_error(document: JsonObject) -> str | None:
    """Return a cursor fingerprint relationship error."""
    components = _cursor_components(document)
    if isinstance(components, str):
        return components
    record_id, query_fingerprint = components
    if ":" in query_fingerprint:
        return "cursor payload.queryFingerprint must not contain ':'"
    if record_id.rsplit(":", 1)[-1] != query_fingerprint:
        return (
            "cursor recordId final component must equal "
            "payload.queryFingerprint"
        )
    return None


def _mismatch_probe(document: JsonObject) -> JsonObject:
    """Create a schema-valid cursor with a mismatched fingerprint."""
    candidate = copy.deepcopy(document)
    payload = candidate.get("payload")
    context = "mismatch probe"
    if not isinstance(payload, dict):
        detail = "cursor payload must be an object"
        raise _error(context, detail)
    query_fingerprint = payload.get("queryFingerprint")
    if not isinstance(query_fingerprint, str):
        detail = "cursor queryFingerprint must be a string"
        raise _error(context, detail)
    payload["queryFingerprint"] = f"{query_fingerprint}{_MISMATCH_SUFFIX}"
    return candidate


def _validate_cursor_negative(
    validator: Draft202012Validator,
    document: JsonObject,
    context: str,
) -> None:
    """Require the fingerprint mismatch probe to fail only the invariant."""
    mismatch = _mismatch_probe(document)
    schema_error = _first_schema_error(validator, mismatch)
    if schema_error is not None:
        raise _error(context, "mismatch probe must remain schema-valid")
    if _cursor_invariant_error(mismatch) is None:
        raise _error(context, "mismatch-negative probe was accepted")


def _validate_example(
    path: Path,
    settings: ValidationSettings,
    validator: Draft202012Validator,
) -> bool:
    """Validate one positive example and its cursor-negative probe."""
    context = path.as_posix()
    document = _extract_example(path, settings.heading)
    schema_error = _first_schema_error(validator, document)
    if schema_error is not None:
        raise _error(context, schema_error)
    if settings.is_audit:
        return False
    invariant_error = _cursor_invariant_error(document)
    if invariant_error is not None:
        raise _error(context, invariant_error)
    _validate_cursor_negative(validator, document, context)
    return True


def _validate_examples(
    paths: tuple[Path, ...],
    settings: ValidationSettings,
    validator: Draft202012Validator,
) -> ValidationResult:
    """Validate every canonical and packaged example."""
    mismatch_count = sum(
        _validate_example(path, settings, validator)
        for path in paths
    )
    return ValidationResult(
        example_count=len(paths),
        mismatch_count=mismatch_count,
    )


def _run(entry_path: Path) -> tuple[ValidationSettings, ValidationResult]:
    """Run parity, schema, format, and fingerprint validation."""
    settings = _settings(entry_path)
    local_paths = _local_paths(settings.package_root)
    _verify_parity(settings.canonical_path, local_paths)
    paths = (settings.canonical_path, *local_paths)
    validator = _schema_validator(settings.schema_path)
    return settings, _validate_examples(paths, settings, validator)


def _success_message(
    settings: ValidationSettings,
    result: ValidationResult,
) -> str:
    """Build the deterministic success message."""
    mismatch = (
        ""
        if settings.is_audit
        else f", {result.mismatch_count} mismatch-negative probes"
    )
    return (
        f"{settings.package_root.name} {settings.kind} "
        f"envelope validation: {result.example_count} examples"
        f"{mismatch} OK\n"
    )


def main() -> int:
    """Validate every byte-identical canonical and skill-local example."""
    try:
        settings, result = _run(Path(__file__))
    except EnvelopeValidationError as error:
        sys.stderr.write(f"ERROR: {error}\n")
        return 1
    sys.stdout.write(_success_message(settings, result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
