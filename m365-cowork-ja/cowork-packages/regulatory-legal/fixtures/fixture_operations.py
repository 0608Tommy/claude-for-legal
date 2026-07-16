"""Validate setup, write, cursor, and execution-scope operations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from .fixture_common import (
    AUDITED_STAGES,
    SETUP_STATUSES,
    exact_value,
    nonempty_string_list,
    object_field,
    parse_timestamp,
    string_field,
)

if TYPE_CHECKING:
    from .fixture_types import JsonObject, JsonValue

_CANONICAL_KEY_FIELDS: Final = (
    "tenantId",
    "practiceId",
    "scopeType",
    "scopeId",
    "recordType",
    "recordId",
)
_PROFILE_PIN_FIELDS: Final = (
    "profileItemId",
    "profileVersion",
    "profileETag",
)


def _setup_envelope_valid(
    record: JsonObject,
    payload: JsonObject,
) -> bool:
    """Validate setup tenant, practice, plugin, and state identity."""
    setup_id = string_field(payload, "setupSessionId")
    return all(
        (
            exact_value(record.get("tenantId")),
            exact_value(record.get("practiceId")),
            payload.get("tenantId") == record.get("tenantId"),
            payload.get("practiceId") == record.get("practiceId"),
            payload.get("pluginId") == "regulatory-legal",
            payload.get("setupStatus") in SETUP_STATUSES,
            record.get("scopeType") == "user",
            record.get("recordType") == "setup-session",
            record.get("scopeId") == payload.get("userObjectId"),
            exact_value(record.get("scopeId")),
            exact_value(setup_id),
            record.get("recordId") == f"regulatory-legal:{setup_id}",
            exact_value(payload.get("idempotencyKey")),
        ),
    )


def _setup_create_valid(payload: JsonObject) -> bool:
    """Validate setup create fields."""
    return all(
        (
            payload.get("expectedAbsent") is True,
            "itemId" not in payload,
            "eTag" not in payload,
        ),
    )


def _setup_update_valid(payload: JsonObject) -> bool:
    """Validate setup update fields."""
    return all(
        (
            exact_value(payload.get("itemId")),
            exact_value(payload.get("eTag")),
            "expectedAbsent" not in payload,
        ),
    )


def _setup_operation_valid(payload: JsonObject) -> bool:
    """Validate mutually exclusive setup create and update fields."""
    validators = {
        "create": _setup_create_valid,
        "update": _setup_update_valid,
    }
    operation = string_field(payload, "operation")
    validator = validators.get(operation) if operation is not None else None
    return validator(payload) if validator is not None else False


def _completed_setup_valid(payload: JsonObject) -> bool:
    """Validate the terminal completed setup state."""
    if payload.get("setupStatus") != "complete":
        return True
    resume = object_field(payload, "resumeState")
    return (
        resume is not None
        and resume.get("resumable") is False
        and resume.get("pausedAt") is None
        and payload.get("pendingQuestions") == []
    )


def _resume_setup_valid(payload: JsonObject) -> bool:
    """Validate a resume operation."""
    resume = object_field(payload, "resumeState")
    return all(
        (
            payload.get("operation") == "update",
            resume is not None,
            resume is not None and resume.get("resumable") is True,
            resume is not None and exact_value(resume.get("pausedAt")),
            nonempty_string_list(payload.get("pendingQuestions")),
        ),
    )


def _profile_pin_valid(value: JsonValue) -> bool:
    """Validate one aligned profile item, version, and eTag pin."""
    if not isinstance(value, dict):
        return False
    return all(exact_value(value.get(field)) for field in _PROFILE_PIN_FIELDS)


def _redo_setup_valid(payload: JsonObject) -> bool:
    """Validate a new redo setup session."""
    redo = object_field(payload, "redoState")
    if redo is None:
        return False
    base_valid = all(
        (
            payload.get("operation") == "create",
            exact_value(redo.get("parentSetupSessionId")),
            redo.get("parentSetupSessionId")
            != payload.get("setupSessionId"),
            nonempty_string_list(redo.get("targetSections")),
        ),
    )
    if not base_valid:
        return False
    pins = redo.get("baseProfilePins")
    return all(
        (
            isinstance(pins, list),
            bool(pins),
            isinstance(pins, list)
            and all(_profile_pin_valid(pin) for pin in pins),
        ),
    )


def _setup_base_valid(
    record: JsonObject,
    payload: JsonObject,
) -> bool:
    """Validate common setup envelope, operation, and terminal state."""
    return all(
        (
            _setup_envelope_valid(record, payload),
            _setup_operation_valid(payload),
            _completed_setup_valid(payload),
        ),
    )


def validate_setup_session(record: JsonObject) -> bool:
    """Validate a user-scoped setup session.

    Parameters
    ----------
    record
        Setup-session fixture.

    Returns
    -------
    bool
        Whether canonical identity and state transitions are valid.

    """
    payload = object_field(record, "payload")
    if payload is None:
        return False
    if not _setup_base_valid(record, payload):
        return False
    validators = {
        "resume": _resume_setup_valid,
        "redo": _redo_setup_valid,
        "redo-section": _redo_setup_valid,
    }
    state = string_field(payload, "conversationState")
    validator = validators.get(state) if state is not None else None
    if validator is not None:
        return validator(payload)
    return state in {"initial", "quick", "full", "check-integrations"}


def _nonnegative_integer(value: JsonValue) -> bool:
    """Validate a nonnegative integer, excluding Boolean values."""
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value >= 0
    )


def _cursor_metadata_valid(case: JsonObject) -> bool:
    """Validate counters, failures, source health, and stage audit."""
    return all(
        (
            _nonnegative_integer(case.get("pagesExpected")),
            _nonnegative_integer(case.get("pagesProcessed")),
            _nonnegative_integer(case.get("attachmentsExpected")),
            _nonnegative_integer(case.get("attachmentsProcessed")),
            case.get("failures") == [],
            case.get("sourceHealth") == "healthy",
            case.get("auditedStages") == list(AUDITED_STAGES),
        ),
    )


def cursor_should_advance(case: JsonObject) -> bool:
    """Return the deterministic cursor-advance decision.

    Parameters
    ----------
    case
        Scan-result fixture.

    Returns
    -------
    bool
        Whether the cursor may advance.

    """
    if not _cursor_metadata_valid(case):
        return False
    return all(
        (
            case.get("scanStatus") == "succeeded",
            case.get("coverageStatus") == "complete",
            case.get("pagesExpected") == case.get("pagesProcessed"),
            case.get("attachmentsExpected")
            == case.get("attachmentsProcessed"),
        ),
    )


def _write_create_valid(case: JsonObject) -> bool:
    """Validate a conditional create request."""
    return all(
        (
            case.get("expectedAbsent") is True,
            "itemId" not in case,
            "eTag" not in case,
        ),
    )


def _write_update_valid(case: JsonObject) -> bool:
    """Validate an exact conditional update request."""
    return all(
        (
            exact_value(case.get("itemId")),
            exact_value(case.get("eTag")),
            "expectedAbsent" not in case,
        ),
    )


def validate_write(case: JsonObject) -> bool:
    """Validate conditional create or exact update fields.

    Parameters
    ----------
    case
        Write-operation fixture.

    Returns
    -------
    bool
        Whether concurrency fields match the operation.

    """
    canonical_key = object_field(case, "canonicalKey")
    if canonical_key is None:
        return False
    if not _write_base_valid(case, canonical_key):
        return False
    validators = {
        "create": _write_create_valid,
        "update": _write_update_valid,
    }
    operation = string_field(case, "operation")
    validator = validators.get(operation) if operation is not None else None
    return validator(case) if validator is not None else False


def _write_base_valid(
    case: JsonObject,
    canonical_key: JsonObject,
) -> bool:
    """Validate canonical key and idempotency fields."""
    return all(
        (
            all(
                exact_value(canonical_key.get(field))
                for field in _CANONICAL_KEY_FIELDS
            ),
            exact_value(case.get("idempotencyKey")),
        ),
    )


def _common_scope_valid(case: JsonObject) -> bool:
    """Validate common execution-scope identity and access."""
    return all(
        (
            exact_value(case.get("scopeId")),
            case.get("status") == "active",
            case.get("access") == "authorized",
            exact_value(case.get("tenantId")),
            exact_value(case.get("practiceId")),
        ),
    )


def _interactive_matter_valid(case: JsonObject) -> bool:
    """Validate an interactive matter scope."""
    binding = object_field(case, "binding")
    if binding is None:
        return False
    expires = parse_timestamp(binding.get("expiresAt"))
    now = parse_timestamp(case.get("now"))
    if expires is None or now is None:
        return False
    return all(
        (
            case.get("actorType") == "human",
            case.get("scopeType") == "matter",
            binding.get("matterId") == case.get("scopeId"),
            binding.get("status") == "active",
            binding.get("access") == "authorized",
            expires > now,
        ),
    )


def _interactive_practice_valid(case: JsonObject) -> bool:
    """Validate a fresh, verified, unbound practice session."""
    session = object_field(case, "session")
    if session is None:
        return False
    return all(
        (
            case.get("actorType") == "human",
            case.get("scopeType") == "practice",
            case.get("scopeId") == case.get("practiceId"),
            case.get("binding") is None,
            exact_value(session.get("sessionId")),
            session.get("fresh") is True,
            session.get("bindingLookupVerified") is True,
            session.get("status") == "active",
            session.get("access") == "authorized",
        ),
    )


def _practice_profile_key_valid(
    profile: JsonObject,
    case: JsonObject,
) -> bool:
    """Validate the exact scheduled practice-profile key."""
    return all(
        (
            profile.get("tenantId") == case.get("tenantId"),
            profile.get("practiceId") == case.get("practiceId"),
            profile.get("pluginId") == "regulatory-legal",
            profile.get("profileType") == "practice-profile",
        ),
    )


def _scheduled_practice_valid(case: JsonObject) -> bool:
    """Validate a service-identity practice run."""
    profile = object_field(case, "practiceProfileKey")
    return all(
        (
            case.get("actorType") == "service-principal",
            case.get("scopeType") == "practice",
            case.get("scopeId") == case.get("practiceId"),
            case.get("binding") is None,
            "userObjectId" not in case,
            "session" not in case,
            "sessionId" not in case,
            all(
                exact_value(case.get(field))
                for field in (
                    "servicePrincipalObjectId",
                    "automationRunId",
                    "solutionVersion",
                    "connectionReference",
                )
            ),
            nonempty_string_list(case.get("sourceAllowlist")),
            profile is not None,
            profile is not None
            and _practice_profile_key_valid(profile, case),
        ),
    )


def validate_scope(case: JsonObject) -> bool:
    """Validate interactive and scheduled execution scopes.

    Parameters
    ----------
    case
        Execution-scope fixture.

    Returns
    -------
    bool
        Whether the selected mode is valid.

    """
    if not _common_scope_valid(case):
        return False
    validators = {
        "interactive-matter": _interactive_matter_valid,
        "interactive-practice": _interactive_practice_valid,
        "scheduled-practice": _scheduled_practice_valid,
    }
    mode = string_field(case, "mode")
    validator = validators.get(mode) if mode is not None else None
    return validator(case) if validator is not None else False
