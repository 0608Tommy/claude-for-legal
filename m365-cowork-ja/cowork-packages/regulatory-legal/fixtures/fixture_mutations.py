"""Apply named fail-closed mutations to known-valid fixtures."""

from __future__ import annotations

from copy import deepcopy
from typing import Final, Literal, NamedTuple

from .fixture_types import (
    FixtureValidationError,
    JsonArray,
    JsonObject,
    JsonValue,
    Validator,
    case_name,
    require_array,
    require_object,
    require_string,
)

type PathPart = str | int
type JsonPath = tuple[PathPart, ...]
type Container = JsonObject | JsonArray


class Edit(NamedTuple):
    """Describe one deterministic JSON mutation."""

    operation: Literal["set", "remove", "copy"]
    path: JsonPath
    value: JsonValue = None
    source: JsonPath = ()


class BaseRef(NamedTuple):
    """Identify a named fixture case and optional nested record."""

    group: str
    name: str
    record_field: str | None


class MutationSpec(NamedTuple):
    """Bind a base fixture, validator, and ordered edits."""

    base: BaseRef
    validator: str
    edits: tuple[Edit, ...]


class MutationOutcome(NamedTuple):
    """Record one direct mutation validator outcome."""

    name: str
    result: bool


_GAP_OPEN: Final = BaseRef(
    "gapCases",
    "open-gap-with-required-scope-coverage",
    "record",
)
_GAP_CLOSED: Final = BaseRef(
    "gapCases",
    "closed-gap-with-regulator-submission",
    "record",
)
_COMMENT_FILED: Final = BaseRef(
    "commentCases",
    "filed-comment-with-exact-external-artifact-and-receipt",
    "record",
)
_PUBLIC_240: Final = BaseRef(
    "publicCommentAuditCases",
    "240000127-exact-egov-form-route",
    None,
)
_SETUP_RESUME: Final = BaseRef(
    "setupSessionCases",
    "user-scoped-resume",
    "record",
)
_SCHEDULED: Final = BaseRef(
    "scopeCases",
    "scheduled-practice",
    None,
)
_CAA: Final = BaseRef(
    "authorityCases",
    "consumer-affairs-agency-structured-authority",
    None,
)
_COMMISSION: Final = BaseRef(
    "authorityCases",
    "consumer-commission-distinct-authority",
    None,
)
_CURSOR: Final = BaseRef(
    "cursorCases",
    "complete-zero-qualifying",
    None,
)
_FIEA: Final = BaseRef(
    "sourceCases",
    "exchange-rule-requires-exact-context",
    "record",
)


def _set(path: JsonPath, value: JsonValue) -> Edit:
    """Create a set edit."""
    return Edit("set", path, value)


def _remove(path: JsonPath) -> Edit:
    """Create a remove edit."""
    return Edit("remove", path)


def _copy(path: JsonPath, source: JsonPath) -> Edit:
    """Create a copy edit."""
    return Edit("copy", path, source=source)


_MUTATION_SPECS: Final[dict[str, MutationSpec]] = {
    "scalar-jurisdiction": MutationSpec(
        _GAP_OPEN,
        "gap",
        (_set(("scope", "jurisdictionCodes"), "JP"),),
    ),
    "blank-jurisdiction": MutationSpec(
        _GAP_OPEN,
        "gap",
        (_set(("scope", "jurisdictionCodes"), ["   "]),),
    ),
    "blank-authority": MutationSpec(
        _GAP_OPEN,
        "gap",
        (_set(("scope", "authorityIds"), ["   "]),),
    ),
    "missing-risk-acceptance": MutationSpec(
        _GAP_OPEN,
        "gap",
        (
            _set(("status",), "risk-accepted"),
            _set(("riskAcceptance",), None),
        ),
    ),
    "identical-closure-artifacts": MutationSpec(
        _GAP_CLOSED,
        "gap",
        (
            _copy(
                ("closureEvidence", "regulatorFacingArtifact"),
                ("closureEvidence", "internalArtifact"),
            ),
            _copy(
                (
                    "closureEvidence",
                    "submissionEvidence",
                    "submittedArtifactItemId",
                ),
                ("closureEvidence", "internalArtifact", "itemId"),
            ),
            _copy(
                (
                    "closureEvidence",
                    "submissionEvidence",
                    "submittedArtifactVersionOrRevisionId",
                ),
                (
                    "closureEvidence",
                    "internalArtifact",
                    "versionOrRevisionId",
                ),
            ),
            _copy(
                (
                    "closureEvidence",
                    "submissionEvidence",
                    "submittedArtifactHash",
                ),
                ("closureEvidence", "internalArtifact", "contentHash"),
            ),
        ),
    ),
    "invalid-comment-decision": MutationSpec(
        _COMMENT_FILED,
        "comment",
        (_set(("decision",), "approved"),),
    ),
    "missing-egov-entry": MutationSpec(
        _COMMENT_FILED,
        "comment",
        (
            _remove(("submissionRoutes", 0, "canonicalCaseEntryUrl")),
            _remove(("submissionEvidence", "canonicalCaseEntryUrl")),
        ),
    ),
    "missing-egov-action": MutationSpec(
        _COMMENT_FILED,
        "comment",
        (
            _remove(("submissionRoutes", 0, "formAction")),
            _remove(("submissionEvidence", "formAction")),
        ),
    ),
    "missing-egov-method": MutationSpec(
        _COMMENT_FILED,
        "comment",
        (
            _remove(("submissionRoutes", 0, "httpMethod")),
            _remove(("submissionEvidence", "httpMethod")),
        ),
    ),
    "missing-egov-class": MutationSpec(
        _COMMENT_FILED,
        "comment",
        (
            _remove(("submissionRoutes", 0, "formClassName")),
            _remove(("submissionEvidence", "formClassName")),
        ),
    ),
    "missing-egov-route-id": MutationSpec(
        _COMMENT_FILED,
        "comment",
        (
            _remove(("submissionRoutes", 0, "routeId")),
            _remove(("submissionEvidence", "routeId")),
        ),
    ),
    "mutate-240-open": MutationSpec(
        _PUBLIC_240,
        "public-comment",
        (_set(("commentOpenAt",), "2026-07-16T00:01:00+09:00"),),
    ),
    "mutate-240-close": MutationSpec(
        _PUBLIC_240,
        "public-comment",
        (_set(("commentCloseAt",), "2026-08-14T23:58:00+09:00"),),
    ),
    "mutate-240-route": MutationSpec(
        _PUBLIC_240,
        "public-comment",
        (_set(("route", "routeId"), "wrong-route"),),
    ),
    "mutate-240-deadline": MutationSpec(
        _PUBLIC_240,
        "public-comment",
        (_set(("route", "deadlineAt"), "2026-08-14T23:58:00+09:00"),),
    ),
    "mutate-240-verified": MutationSpec(
        _PUBLIC_240,
        "public-comment",
        (_set(("route", "verifiedAt"), "2026-07-16T20:20:54+09:00"),),
    ),
    "blank-setup-tenant": MutationSpec(
        _SETUP_RESUME,
        "setup",
        (_set(("tenantId",), ""),),
    ),
    "wrong-setup-practice": MutationSpec(
        _SETUP_RESUME,
        "setup",
        (_set(("payload", "practiceId"), "practice-other"),),
    ),
    "wrong-setup-plugin": MutationSpec(
        _SETUP_RESUME,
        "setup",
        (_set(("payload", "pluginId"), "other-plugin"),),
    ),
    "invalid-setup-status": MutationSpec(
        _SETUP_RESUME,
        "setup",
        (_set(("payload", "setupStatus"), "done"),),
    ),
    "scheduled-user": MutationSpec(
        _SCHEDULED,
        "scope",
        (_set(("userObjectId",), "user-1"),),
    ),
    "scheduled-session": MutationSpec(
        _SCHEDULED,
        "scope",
        (
            _set(
                ("session",),
                {"sessionId": "human-session", "fresh": True},
            ),
        ),
    ),
    "swap-caa-display": MutationSpec(
        _CAA,
        "authority",
        (_set(("displayName",), "消費者委員会"),),
    ),
    "swap-commission-display": MutationSpec(
        _COMMISSION,
        "authority",
        (_set(("displayName",), "消費者庁"),),
    ),
    "cursor-missing-counters": MutationSpec(
        _CURSOR,
        "cursor",
        (
            _remove(("pagesExpected",)),
            _remove(("pagesProcessed",)),
        ),
    ),
    "cursor-failures": MutationSpec(
        _CURSOR,
        "cursor",
        (_set(("failures",), ["failure"]),),
    ),
    "fiea-pseudo-exact-pin": MutationSpec(
        _FIEA,
        "source",
        (
            _set(
                (
                    "marketRuleContext",
                    "approvalBasis",
                    "exactRuleOrExceptionPinned",
                ),
                value=True,
            ),
            _set(
                (
                    "marketRuleContext",
                    "approvalBasis",
                    "sourceVersionOrRevisionId",
                ),
                "current-20260716",
            ),
        ),
    ),
}


def _find_case(document: JsonObject, reference: BaseRef) -> JsonObject:
    """Find and clone a named base fixture."""
    cases = require_array(
        document.get(reference.group),
        reference.group,
    )
    for value in cases:
        case = require_object(value, reference.group)
        if case.get("name") != reference.name:
            continue
        if reference.record_field is None:
            return deepcopy(case)
        record = require_object(
            case.get(reference.record_field),
            f"{reference.group}.{reference.name}.record",
        )
        return deepcopy(record)
    message = f"{reference.group}: missing base case {reference.name}"
    raise FixtureValidationError(message)


def _mapping_child(
    value: JsonObject,
    part: PathPart,
) -> JsonValue | None:
    """Read a mapping child when the key is valid."""
    return value.get(part) if isinstance(part, str) else None


def _sequence_child(
    value: JsonArray,
    part: PathPart,
) -> JsonValue | None:
    """Read a sequence child when the index is valid."""
    if isinstance(part, int) and 0 <= part < len(value):
        return value[part]
    return None


def _child(value: JsonValue, part: PathPart, context: str) -> JsonValue:
    """Read one path component."""
    child = (
        _mapping_child(value, part)
        if isinstance(value, dict)
        else _sequence_child(value, part)
        if isinstance(value, list)
        else None
    )
    if child is not None:
        return child
    message = f"{context}: invalid path component {part!r}"
    raise FixtureValidationError(message)


def _value_at_path(root: JsonObject, path: JsonPath) -> JsonValue:
    """Read a JSON value at a path."""
    current: JsonValue = root
    for part in path:
        current = _child(current, part, "mutation source")
    return current


def _parent_at_path(
    root: JsonObject,
    path: JsonPath,
) -> tuple[Container, PathPart]:
    """Return the parent container and final path component."""
    if not path:
        message = "mutation path must not be empty"
        raise FixtureValidationError(message)
    current: JsonValue = root
    for part in path[:-1]:
        current = _child(current, part, "mutation target")
    if not isinstance(current, dict | list):
        message = "mutation target parent must be an object or array"
        raise FixtureValidationError(message)
    return current, path[-1]


def _set_mapping(
    parent: JsonObject,
    part: PathPart,
    value: JsonValue,
) -> bool:
    """Set one mapping field."""
    if not isinstance(part, str):
        return False
    parent[part] = deepcopy(value)
    return True


def _set_sequence(
    parent: JsonArray,
    part: PathPart,
    value: JsonValue,
) -> bool:
    """Set one sequence element."""
    if isinstance(part, int) and 0 <= part < len(parent):
        parent[part] = deepcopy(value)
        return True
    return False


def _set_value(
    parent: Container,
    part: PathPart,
    value: JsonValue,
) -> None:
    """Set one object field or array element."""
    changed = (
        _set_mapping(parent, part, value)
        if isinstance(parent, dict)
        else _set_sequence(parent, part, value)
    )
    if changed:
        return
    message = f"cannot set mutation path component {part!r}"
    raise FixtureValidationError(message)


def _remove_mapping(parent: JsonObject, part: PathPart) -> bool:
    """Remove one mapping field."""
    if isinstance(part, str) and part in parent:
        del parent[part]
        return True
    return False


def _remove_sequence(parent: JsonArray, part: PathPart) -> bool:
    """Remove one sequence element."""
    if isinstance(part, int) and 0 <= part < len(parent):
        del parent[part]
        return True
    return False


def _remove_value(parent: Container, part: PathPart) -> None:
    """Remove one object field or array element."""
    changed = (
        _remove_mapping(parent, part)
        if isinstance(parent, dict)
        else _remove_sequence(parent, part)
    )
    if changed:
        return
    message = f"cannot remove mutation path component {part!r}"
    raise FixtureValidationError(message)


def _apply_edit(root: JsonObject, edit: Edit) -> None:
    """Apply one deterministic edit."""
    parent, part = _parent_at_path(root, edit.path)
    if edit.operation == "remove":
        _remove_value(parent, part)
        return
    value = edit.value
    if edit.operation == "copy":
        value = _value_at_path(root, edit.source)
    _set_value(parent, part, value)


def run_direct_mutations(
    document: JsonObject,
    validators: dict[str, Validator],
) -> list[MutationOutcome]:
    """Run every named direct mutation.

    Parameters
    ----------
    document
        Complete fixture document.
    validators
        Validator registry.

    Returns
    -------
    list[MutationOutcome]
        Named Boolean outcomes.

    Raises
    ------
    FixtureValidationError
        If a mutation or validator name is unknown.

    """
    outcomes: list[MutationOutcome] = []
    cases = require_array(
        document.get("directMutationCases"),
        "directMutationCases",
    )
    for value in cases:
        case = require_object(value, "directMutationCases")
        name = case_name(case)
        mutation = require_string(
            case.get("mutation"),
            f"{name}.mutation",
        )
        spec = _MUTATION_SPECS.get(mutation)
        if spec is None:
            message = f"{name}: unknown mutation {mutation}"
            raise FixtureValidationError(message)
        validator = validators.get(spec.validator)
        if validator is None:
            message = f"{name}: unknown validator {spec.validator}"
            raise FixtureValidationError(message)
        record = _find_case(document, spec.base)
        for edit in spec.edits:
            _apply_edit(record, edit)
        outcomes.append(MutationOutcome(name, validator(record)))
    return outcomes
