"""Validate coverage, submission, and risk evidence."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from .fixture_common import (
    SUBMISSION_FIELDS,
    exact_value,
    nonempty_string_list,
    object_field,
    parse_timestamp,
    string_list,
)

if TYPE_CHECKING:
    from .fixture_types import JsonObject, JsonValue

_STRING_SCOPE_FIELDS: Final = (
    "jurisdictionCodes",
    "authorityIds",
    "regulatedEntityIds",
    "businessUnitIds",
    "productsOrServices",
    "activities",
    "provisions",
)
_ROUTE_FIELD_PAIRS: Final = (
    ("routeId", "routeId"),
    ("method", "submissionMethod"),
    ("destinationSystem", "destinationSystem"),
    ("destinationAddressOrEndpoint", "destinationAddressOrEndpoint"),
    ("instructionUrl", "instructionUrl"),
    ("instructionContentHash", "instructionContentHash"),
    ("deadlineAt", "routeDeadlineAt"),
    ("receiptOrPostmark", "receiptOrPostmark"),
    ("verifiedAt", "routeVerifiedAt"),
)
_FORM_FIELD_PAIRS: Final = (
    ("canonicalCaseEntryUrl", "canonicalCaseEntryUrl"),
    ("formAction", "formAction"),
    ("httpMethod", "httpMethod"),
    ("formClassName", "formClassName"),
)


def submission_complete(value: JsonValue) -> bool:
    """Validate exact submission evidence.

    Parameters
    ----------
    value
        Candidate submission object.

    Returns
    -------
    bool
        Whether every submission field is nonblank and valid.

    """
    if not isinstance(value, dict):
        return False
    if not SUBMISSION_FIELDS.issubset(value):
        return False
    if not all(exact_value(value.get(field)) for field in SUBMISSION_FIELDS):
        return False
    return all(
        (
            value.get("submissionMethod")
            in {
                "web-form",
                "email",
                "postal",
                "portal",
                "hand-delivery",
                "other",
            },
            value.get("receiptOrPostmark")
            in {"receipt", "postmark", "not-applicable"},
        ),
    )


def _scope_dimensions_valid(scope: JsonObject) -> bool:
    """Validate all scope dimension arrays."""
    return all(
        string_list(scope.get(field))
        for field in _STRING_SCOPE_FIELDS
    )


def _scope_complete(scope: JsonObject) -> bool:
    """Validate all structured scope dimensions."""
    if not _scope_dimensions_valid(scope):
        return False
    core_present = all(
        (
            bool(scope.get("jurisdictionCodes")),
            bool(scope.get("authorityIds")),
        ),
    )
    if not core_present:
        return False
    excluded = scope.get("excludedScope")
    if not isinstance(excluded, list):
        return False
    return all(_excluded_scope_item(item) for item in excluded)


def _excluded_scope_item(value: JsonValue) -> bool:
    """Validate one excluded-scope entry."""
    if not isinstance(value, dict):
        return False
    return all(
        (
            exact_value(value.get("reason")),
            exact_value(value.get("detail")),
        ),
    )


def _source_coverage_complete(source: JsonObject) -> bool:
    """Validate source attachment coverage."""
    expected = source.get("expectedAttachmentCount")
    reviewed = source.get("reviewedAttachmentCount")
    return all(
        (
            isinstance(expected, int),
            not isinstance(expected, bool),
            isinstance(expected, int) and expected >= 0,
            isinstance(reviewed, int),
            not isinstance(reviewed, bool),
            reviewed == expected,
            source.get("complete") is True,
            source.get("truncated") is False,
            source.get("failures") == [],
        ),
    )


def _policy_coverage_complete(policy: JsonObject) -> bool:
    """Validate policy item and section coverage."""
    policy_items = policy.get("policyItemIds")
    expected_sections = policy.get("sectionsExpected")
    reviewed_sections = policy.get("sectionsReviewed")
    sections_match = (
        isinstance(expected_sections, list)
        and isinstance(reviewed_sections, list)
        and set(expected_sections).issubset(reviewed_sections)
    )
    return all(
        (
            policy.get("complete") is True,
            nonempty_string_list(policy_items),
            nonempty_string_list(expected_sections),
            nonempty_string_list(reviewed_sections),
            sections_match,
        ),
    )


def _time_window_complete(window: JsonObject) -> bool:
    """Validate a bounded, ordered time window."""
    start = parse_timestamp(window.get("from"))
    end = parse_timestamp(window.get("through"))
    return start is not None and end is not None and start <= end


def coverage_complete(record: JsonObject) -> bool:
    """Validate scope, coverage, and time-window completeness.

    Parameters
    ----------
    record
        Gap record or focused coverage probe.

    Returns
    -------
    bool
        Whether coverage is complete and fail-closed.

    """
    scope = object_field(record, "scope")
    coverage = object_field(record, "coverage")
    if scope is None or coverage is None:
        return False
    if not _scope_complete(scope):
        return False
    return _coverage_parts_complete(coverage)


def _coverage_parts_complete(coverage: JsonObject) -> bool:
    """Validate source, policy, and time-window coverage parts."""
    source = object_field(coverage, "source")
    policy = object_field(coverage, "policy")
    window = object_field(coverage, "timeWindow")
    if source is None or policy is None or window is None:
        return False
    return all(
        (
            _source_coverage_complete(source),
            _policy_coverage_complete(policy),
            _time_window_complete(window),
        ),
    )


def _base_route_consistent(
    route: JsonValue,
    submission: JsonValue,
) -> tuple[JsonObject, JsonObject] | None:
    """Return validated route and submission objects."""
    if not isinstance(route, dict) or not isinstance(submission, dict):
        return None
    valid = all(
        (
            submission_complete(submission),
            _fields_match(route, submission, _ROUTE_FIELD_PAIRS),
        ),
    )
    return (route, submission) if valid else None


def _form_identity_present(
    route: JsonObject,
    submission: JsonObject,
) -> bool:
    """Return whether either object contains form identity fields."""
    return any(
        field in route or field in submission
        for pair in _FORM_FIELD_PAIRS
        for field in pair
    )


def _fields_match(
    route: JsonObject,
    submission: JsonObject,
    pairs: tuple[tuple[str, str], ...],
) -> bool:
    """Validate exact paired route and submission fields."""
    return all(
        exact_value(route.get(route_field))
        and route.get(route_field) == submission.get(submission_field)
        for route_field, submission_field in pairs
    )


def route_consistent(route: JsonValue, submission: JsonValue) -> bool:
    """Validate exact route and submission consistency.

    Parameters
    ----------
    route
        Verified submission route.
    submission
        Submission evidence.

    Returns
    -------
    bool
        Whether all shared route fields match.

    """
    validated = _base_route_consistent(route, submission)
    if validated is None:
        return False
    route_object, submission_object = validated
    if not _form_identity_present(route_object, submission_object):
        return True
    return _egov_form_pairs_match(route_object, submission_object)


def _egov_form_pairs_match(
    route: JsonObject,
    submission: JsonObject,
) -> bool:
    """Validate shared e-Gov form identity fields."""
    return all(
        (
            _fields_match(route, submission, _FORM_FIELD_PAIRS),
            route.get("httpMethod") == "POST",
            route.get("formAction")
            == "https://public-comment.e-gov.go.jp/pcm/2010",
            route.get("formClassName") == "PCMIKENINPUT",
            exact_value(route.get("caseId")),
            route.get("caseId") == submission.get("caseId"),
        ),
    )


def _form_identity_fields_complete(
    route: JsonObject,
    submission: JsonObject,
    required: tuple[str, ...],
) -> bool:
    """Validate all required form identity fields in both objects."""
    return all(
        (
            all(exact_value(route.get(field)) for field in required),
            all(exact_value(submission.get(field)) for field in required),
        ),
    )


def egov_form_identity_complete(
    route: JsonValue,
    submission: JsonValue,
    case_id: JsonValue,
) -> bool:
    """Validate every identity field required for an e-Gov filing.

    Parameters
    ----------
    route
        Verified e-Gov route.
    submission
        Filed submission evidence.
    case_id
        Expected case identifier.

    Returns
    -------
    bool
        Whether the e-Gov form identity is exact.

    """
    required = (
        "routeId",
        "canonicalCaseEntryUrl",
        "formAction",
        "httpMethod",
        "formClassName",
        "caseId",
    )
    if not isinstance(route, dict) or not isinstance(submission, dict):
        return False
    return all(
        (
            exact_value(case_id),
            _form_identity_fields_complete(route, submission, required),
            route.get("caseId") == case_id,
            submission.get("caseId") == case_id,
            _egov_form_pairs_match(route, submission),
        ),
    )


def _risk_text_complete(value: JsonObject) -> bool:
    """Validate all risk-acceptance text fields."""
    fields = (
        "acceptedByObjectId",
        "rationale",
        "residualRisk",
        "counselReviewedBy",
        "revisitTrigger",
    )
    return all(exact_value(value.get(field)) for field in fields)


def risk_acceptance_complete(value: JsonValue) -> bool:
    """Validate all evidence required for risk acceptance.

    Parameters
    ----------
    value
        Candidate risk-acceptance object.

    Returns
    -------
    bool
        Whether the evidence is complete.

    """
    if not isinstance(value, dict):
        return False
    if not _risk_text_complete(value):
        return False
    return all(
        (
            nonempty_string_list(value.get("controls")),
            nonempty_string_list(value.get("affectedEntities")),
            parse_timestamp(value.get("expiresAt")) is not None,
        ),
    )


def artifacts_distinct(
    internal: JsonValue,
    external: JsonValue,
) -> bool:
    """Validate distinct internal and regulator-facing artifact identities.

    Parameters
    ----------
    internal
        Internal artifact.
    external
        Regulator-facing artifact.

    Returns
    -------
    bool
        Whether all three identity components differ.

    """
    if not isinstance(internal, dict) or not isinstance(external, dict):
        return False
    return all(
        internal.get(field) != external.get(field)
        for field in ("itemId", "versionOrRevisionId", "contentHash")
    )
