"""Validate fixed-identity session-binding lifecycle transitions."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final, Never, TypeGuard, cast

SESSION_BINDING_SCOPE_TYPE: Final = "session"
SESSION_BINDING_RECORD_TYPE: Final = "session-matter-binding"
SESSION_BINDING_RECORD_ID: Final = "active-matter"
_MISSING: Final = object()

type BindingGeneration = int | str
type SessionBinding = Mapping[str, object]
type MatterSnapshot = Mapping[str, object]
type SessionBindingCreateRequest = Mapping[str, object]
type SessionBindingUpdateRequest = Mapping[str, object]


@dataclass(frozen=True, slots=True)
class _BindingKey:
    """Represent immutable session-binding identity."""

    tenant_id: str
    practice_id: str
    user_object_id: str
    session_id: str
    matter_id: str


@dataclass(frozen=True, slots=True)
class _BindingOrigin:
    """Represent immutable session-binding origin fields."""

    bound_at: str
    bound_by: str
    expires_at: str


@dataclass(frozen=True, slots=True)
class _BindingState:
    """Represent mutable session-binding lifecycle fields."""

    status: str
    revoked_at: str | None
    revoked_by: str | None
    revocation_reason: str | None


@dataclass(frozen=True, slots=True)
class _Binding:
    """Represent a parsed session-binding payload."""

    key: _BindingKey
    origin: _BindingOrigin
    state: _BindingState


@dataclass(frozen=True, slots=True)
class _MatterPrecondition:
    """Represent a parsed atomic matter precondition."""

    item_id: str
    expected_status: str
    atomic_with_binding_expected_absent: bool
    e_tag: str | None
    version: int | None
    binding_generation: BindingGeneration | None


@dataclass(frozen=True, slots=True)
class _MatterIdentity:
    """Represent exact matter identity."""

    tenant_id: str
    practice_id: str
    matter_id: str
    item_id: str


@dataclass(frozen=True, slots=True)
class _MatterConcurrency:
    """Represent current matter concurrency and status fields."""

    e_tag: str
    version: int
    binding_generation: BindingGeneration
    status: str


@dataclass(frozen=True, slots=True)
class _MatterSnapshot:
    """Represent parsed current matter values."""

    identity: _MatterIdentity
    concurrency: _MatterConcurrency


@dataclass(frozen=True, slots=True)
class _OuterIdentity:
    """Represent a generic outer state key."""

    tenant_id: str
    practice_id: str
    scope_type: str
    scope_id: str
    record_type: str
    record_id: str


@dataclass(frozen=True, slots=True)
class _CreateRequest:
    """Represent parsed binding-create semantic fields."""

    outer: _OuterIdentity
    expected_absent: bool
    matter_precondition: _MatterPrecondition
    payload: _Binding


@dataclass(frozen=True, slots=True)
class _RevocationPatch:
    """Represent parsed session-binding revocation fields."""

    status: str
    revoked_at: str
    revoked_by: str
    revocation_reason: str


@dataclass(frozen=True, slots=True)
class _UpdateRequest:
    """Represent parsed binding-update semantic fields."""

    outer: _OuterIdentity
    patch: _RevocationPatch


class SessionBindingTransitionError(ValueError):
    """Indicate a session-binding identity or lifecycle violation."""


type _WriteRequest = _CreateRequest | _UpdateRequest


def _raise_transition_error(message: str) -> Never:
    """Raise a transition error with a caller-supplied explanation.

    Parameters
    ----------
    message
        Human-readable contract violation.

    Raises
    ------
    SessionBindingTransitionError
        Always.

    """
    raise SessionBindingTransitionError(message)


def _mapping_field(
    document: Mapping[str, object],
    field_name: str,
) -> Mapping[str, object]:
    """Return a required mapping field."""
    value = document.get(field_name)
    if isinstance(value, Mapping):
        return cast("Mapping[str, object]", value)
    message = f"{field_name} must be an object"
    _raise_transition_error(message)


def _string_field(
    document: Mapping[str, object],
    field_name: str,
) -> str:
    """Return a required nonblank string field."""
    value = document.get(field_name)
    if isinstance(value, str) and value.strip():
        return value
    message = f"{field_name} must be a nonblank string"
    _raise_transition_error(message)


def _boolean_field(
    document: Mapping[str, object],
    field_name: str,
) -> bool:
    """Return a required Boolean field."""
    value = document.get(field_name)
    if isinstance(value, bool):
        return value
    message = f"{field_name} must be Boolean"
    _raise_transition_error(message)


def _is_positive_integer(value: object) -> TypeGuard[int]:
    """Return whether a value is a positive non-Boolean integer."""
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value > 0
    )


def _integer_value(value: object, field_name: str) -> int:
    """Return a positive integer value."""
    if _is_positive_integer(value):
        return value
    message = f"{field_name} must be a positive integer"
    _raise_transition_error(message)


def _integer_field(
    document: Mapping[str, object],
    field_name: str,
) -> int:
    """Return a required positive integer field."""
    return _integer_value(document.get(field_name), field_name)


def _nullable_string_field(
    document: Mapping[str, object],
    field_name: str,
) -> str | None:
    """Return a required nullable string field."""
    value = document.get(field_name, _MISSING)
    if value is None or isinstance(value, str):
        return value
    message = f"{field_name} must be a string or null"
    _raise_transition_error(message)


def _optional_string_field(
    document: Mapping[str, object],
    field_name: str,
) -> str | None:
    """Return an optional nonblank string field."""
    value = document.get(field_name, _MISSING)
    if value is _MISSING:
        return None
    if isinstance(value, str) and value.strip():
        return value
    message = f"{field_name} must be a nonblank string when supplied"
    _raise_transition_error(message)


def _optional_integer_field(
    document: Mapping[str, object],
    field_name: str,
) -> int | None:
    """Return an optional positive integer field."""
    value = document.get(field_name, _MISSING)
    if value is _MISSING:
        return None
    return _integer_value(value, field_name)


def _generation_value(
    value: object,
    field_name: str,
) -> BindingGeneration:
    """Return a nonblank string or positive integer generation."""
    if _is_positive_integer(value):
        return value
    if isinstance(value, str) and value.strip():
        return value
    message = (
        f"{field_name} must be a positive integer or nonblank string"
    )
    _raise_transition_error(message)


def _generation_field(
    document: Mapping[str, object],
    field_name: str,
) -> BindingGeneration:
    """Return a required binding-generation value."""
    return _generation_value(document.get(field_name), field_name)


def _optional_generation_field(
    document: Mapping[str, object],
    field_name: str,
) -> BindingGeneration | None:
    """Return an optional binding-generation value."""
    value = document.get(field_name, _MISSING)
    if value is _MISSING:
        return None
    return _generation_value(value, field_name)


def _parse_binding(document: SessionBinding) -> _Binding:
    """Parse a session-binding mapping."""
    return _Binding(
        key=_BindingKey(
            tenant_id=_string_field(document, "tenantId"),
            practice_id=_string_field(document, "practiceId"),
            user_object_id=_string_field(document, "userObjectId"),
            session_id=_string_field(document, "sessionId"),
            matter_id=_string_field(document, "matterId"),
        ),
        origin=_BindingOrigin(
            bound_at=_string_field(document, "boundAt"),
            bound_by=_string_field(document, "boundBy"),
            expires_at=_string_field(document, "expiresAt"),
        ),
        state=_BindingState(
            status=_string_field(document, "status"),
            revoked_at=_nullable_string_field(document, "revokedAt"),
            revoked_by=_nullable_string_field(document, "revokedBy"),
            revocation_reason=_nullable_string_field(
                document,
                "revocationReason",
            ),
        ),
    )


def _parse_matter_precondition(
    document: Mapping[str, object],
) -> _MatterPrecondition:
    """Parse a binding-create matter precondition."""
    return _MatterPrecondition(
        item_id=_string_field(document, "itemId"),
        expected_status=_string_field(document, "expectedStatus"),
        atomic_with_binding_expected_absent=_boolean_field(
            document,
            "atomicWithBindingExpectedAbsent",
        ),
        e_tag=_optional_string_field(document, "eTag"),
        version=_optional_integer_field(document, "version"),
        binding_generation=_optional_generation_field(
            document,
            "bindingGeneration",
        ),
    )


def _parse_matter_snapshot(
    document: MatterSnapshot,
) -> _MatterSnapshot:
    """Parse a current matter snapshot."""
    return _MatterSnapshot(
        identity=_MatterIdentity(
            tenant_id=_string_field(document, "tenantId"),
            practice_id=_string_field(document, "practiceId"),
            matter_id=_string_field(document, "matterId"),
            item_id=_string_field(document, "itemId"),
        ),
        concurrency=_MatterConcurrency(
            e_tag=_string_field(document, "eTag"),
            version=_integer_field(document, "version"),
            binding_generation=_generation_field(
                document,
                "bindingGeneration",
            ),
            status=_string_field(document, "status"),
        ),
    )


def _parse_outer_identity(
    document: Mapping[str, object],
) -> _OuterIdentity:
    """Parse a generic outer state key."""
    return _OuterIdentity(
        tenant_id=_string_field(document, "tenantId"),
        practice_id=_string_field(document, "practiceId"),
        scope_type=_string_field(document, "scopeType"),
        scope_id=_string_field(document, "scopeId"),
        record_type=_string_field(document, "recordType"),
        record_id=_string_field(document, "recordId"),
    )


def _parse_create_request(
    document: SessionBindingCreateRequest,
) -> _CreateRequest:
    """Parse binding-create semantic fields."""
    return _CreateRequest(
        outer=_parse_outer_identity(document),
        expected_absent=_boolean_field(document, "expectedAbsent"),
        matter_precondition=_parse_matter_precondition(
            _mapping_field(document, "matterPrecondition"),
        ),
        payload=_parse_binding(_mapping_field(document, "payload")),
    )


def _parse_revocation_patch(
    document: Mapping[str, object],
) -> _RevocationPatch:
    """Parse a session-binding revocation patch."""
    return _RevocationPatch(
        status=_string_field(document, "status"),
        revoked_at=_string_field(document, "revokedAt"),
        revoked_by=_string_field(document, "revokedBy"),
        revocation_reason=_string_field(
            document,
            "revocationReason",
        ),
    )


def _parse_update_request(
    document: SessionBindingUpdateRequest,
) -> _UpdateRequest:
    """Parse binding-update semantic fields."""
    return _UpdateRequest(
        outer=_parse_outer_identity(document),
        patch=_parse_revocation_patch(
            _mapping_field(document, "patch"),
        ),
    )


def _expected_scope_id(binding: _Binding) -> str:
    """Return the fixed outer scope identifier for a binding."""
    return f"{binding.key.user_object_id}:{binding.key.session_id}"


def _require_outer_identity(
    request: _WriteRequest,
    binding: _Binding,
) -> None:
    """Require an outer state key to identify the supplied binding."""
    outer = request.outer
    key = binding.key
    expected_values = (
        ("tenantId", outer.tenant_id, key.tenant_id),
        ("practiceId", outer.practice_id, key.practice_id),
        ("scopeType", outer.scope_type, SESSION_BINDING_SCOPE_TYPE),
        ("scopeId", outer.scope_id, _expected_scope_id(binding)),
        ("recordType", outer.record_type, SESSION_BINDING_RECORD_TYPE),
        ("recordId", outer.record_id, SESSION_BINDING_RECORD_ID),
    )
    for field_name, actual, expected in expected_values:
        if actual != expected:
            message = (
                f"outer {field_name} must match fixed binding identity: "
                f"{actual!r} != {expected!r}"
            )
            _raise_transition_error(message)


def _require_active_metadata(binding: _Binding) -> None:
    """Require active bindings to have no revocation metadata."""
    state = binding.state
    if state.status != "active":
        _raise_transition_error("new and current bindings must be active")
    revocation_values = (
        state.revoked_at,
        state.revoked_by,
        state.revocation_reason,
    )
    if any(value is not None for value in revocation_values):
        _raise_transition_error(
            "active bindings must have null revocation metadata",
        )


def _require_matching_token(
    field_name: str,
    supplied: object,
    current: object,
) -> None:
    """Require one supplied concurrency token to match."""
    if supplied != current:
        message = f"matter {field_name} precondition is stale"
        _raise_transition_error(message)


def _require_current_matter_token(
    precondition: _MatterPrecondition,
    matter: _MatterSnapshot,
) -> None:
    """Require at least one supplied matter token to be current."""
    concurrency = matter.concurrency
    tokens = (
        ("eTag", precondition.e_tag, concurrency.e_tag),
        ("version", precondition.version, concurrency.version),
        (
            "binding-generation",
            precondition.binding_generation,
            concurrency.binding_generation,
        ),
    )
    supplied_tokens = tuple(
        token
        for token in tokens
        if token[1] is not None
    )
    if not supplied_tokens:
        _raise_transition_error(
            "binding create requires a current matter concurrency token",
        )
    for field_name, supplied, current in supplied_tokens:
        _require_matching_token(field_name, supplied, current)


def _require_matter_identity(
    request: _CreateRequest,
    matter: _MatterSnapshot,
) -> None:
    """Require the binding and matter snapshot to identify one matter."""
    binding_key = request.payload.key
    matter_identity = matter.identity
    precondition = request.matter_precondition
    identity_values = (
        ("tenantId", binding_key.tenant_id, matter_identity.tenant_id),
        (
            "practiceId",
            binding_key.practice_id,
            matter_identity.practice_id,
        ),
        ("matterId", binding_key.matter_id, matter_identity.matter_id),
        (
            "matter itemId",
            precondition.item_id,
            matter_identity.item_id,
        ),
    )
    for field_name, expected, actual in identity_values:
        if expected != actual:
            message = f"binding create {field_name} matter identity mismatch"
            _raise_transition_error(message)


def _require_matter_precondition(
    request: _CreateRequest,
    matter: _MatterSnapshot,
) -> None:
    """Require an active exact matter fence for binding creation."""
    precondition = request.matter_precondition
    _require_matter_identity(request, matter)
    if precondition.atomic_with_binding_expected_absent is not True:
        _raise_transition_error(
            "matter and binding preconditions must be evaluated atomically",
        )
    if precondition.expected_status != "active":
        _raise_transition_error(
            "binding create must expect active matter status",
        )
    if matter.concurrency.status != "active":
        _raise_transition_error(
            "binding create requires the current matter to be active",
        )
    _require_current_matter_token(precondition, matter)


def _require_revocation_metadata(binding: _Binding) -> None:
    """Require a revoked binding to contain complete metadata."""
    state = binding.state
    if state.status != "revoked":
        _raise_transition_error("updated binding status must be revoked")
    metadata = (
        ("revokedAt", state.revoked_at),
        ("revokedBy", state.revoked_by),
        ("revocationReason", state.revocation_reason),
    )
    for field_name, value in metadata:
        if not isinstance(value, str) or not value.strip():
            message = f"revoked binding requires nonblank {field_name}"
            _raise_transition_error(message)


def _validate_transition(
    current: _Binding,
    updated: _Binding,
) -> None:
    """Validate the sole permitted active-to-revoked transition."""
    _require_active_metadata(current)
    current_key = current.key
    updated_key = updated.key
    current_origin = current.origin
    updated_origin = updated.origin
    immutable_values = (
        ("tenantId", current_key.tenant_id, updated_key.tenant_id),
        ("practiceId", current_key.practice_id, updated_key.practice_id),
        (
            "userObjectId",
            current_key.user_object_id,
            updated_key.user_object_id,
        ),
        ("sessionId", current_key.session_id, updated_key.session_id),
        ("matterId", current_key.matter_id, updated_key.matter_id),
        ("boundAt", current_origin.bound_at, updated_origin.bound_at),
        ("boundBy", current_origin.bound_by, updated_origin.bound_by),
        (
            "expiresAt",
            current_origin.expires_at,
            updated_origin.expires_at,
        ),
    )
    for field_name, before, after in immutable_values:
        if before != after:
            message = f"session-binding field {field_name} is immutable"
            _raise_transition_error(message)
    _require_revocation_metadata(updated)


def _updated_binding(
    current: _Binding,
    patch: _RevocationPatch,
) -> _Binding:
    """Apply a parsed revocation patch."""
    state = _BindingState(
        status=patch.status,
        revoked_at=patch.revoked_at,
        revoked_by=patch.revoked_by,
        revocation_reason=patch.revocation_reason,
    )
    return _Binding(
        key=current.key,
        origin=current.origin,
        state=state,
    )


def _binding_mapping(binding: _Binding) -> dict[str, object]:
    """Return the external mapping form of a parsed binding."""
    key = binding.key
    origin = binding.origin
    state = binding.state
    return {
        "tenantId": key.tenant_id,
        "practiceId": key.practice_id,
        "userObjectId": key.user_object_id,
        "sessionId": key.session_id,
        "matterId": key.matter_id,
        "status": state.status,
        "boundAt": origin.bound_at,
        "boundBy": origin.bound_by,
        "expiresAt": origin.expires_at,
        "revokedAt": state.revoked_at,
        "revokedBy": state.revoked_by,
        "revocationReason": state.revocation_reason,
    }


def validate_session_binding_create(
    request: SessionBindingCreateRequest,
    matter: MatterSnapshot,
) -> None:
    """Validate binding identity and its atomic active-matter fence.

    Parameters
    ----------
    request
        Candidate conditional create request.
    matter
        Current matter snapshot checked in the same transaction.

    Raises
    ------
    SessionBindingTransitionError
        If create, matter, identity, or atomic preconditions are invalid.

    """
    parsed_request = _parse_create_request(request)
    parsed_matter = _parse_matter_snapshot(matter)
    if parsed_request.expected_absent is not True:
        _raise_transition_error(
            "session-binding create requires expectedAbsent true",
        )
    _require_outer_identity(parsed_request, parsed_request.payload)
    _require_active_metadata(parsed_request.payload)
    _require_matter_precondition(parsed_request, parsed_matter)


def validate_session_binding_transition(
    current: SessionBinding,
    updated: SessionBinding,
) -> None:
    """Validate the sole permitted active-to-revoked transition.

    Parameters
    ----------
    current
        Persisted binding before the update.
    updated
        Full binding payload after applying the requested patch.

    Raises
    ------
    SessionBindingTransitionError
        If current status, next status, metadata, or identity is invalid.

    """
    _validate_transition(
        _parse_binding(current),
        _parse_binding(updated),
    )


def validate_session_binding_update(
    request: SessionBindingUpdateRequest,
    current: SessionBinding,
) -> SessionBinding:
    """Validate an outer update key and active-to-revoked patch.

    Parameters
    ----------
    request
        Candidate conditional update request.
    current
        Persisted binding before the update.

    Returns
    -------
    SessionBinding
        Full validated post-update binding.

    Raises
    ------
    SessionBindingTransitionError
        If outer identity or transition semantics are invalid.

    """
    parsed_request = _parse_update_request(request)
    parsed_current = _parse_binding(current)
    _require_outer_identity(parsed_request, parsed_current)
    updated = _updated_binding(parsed_current, parsed_request.patch)
    _validate_transition(parsed_current, updated)
    return _binding_mapping(updated)
