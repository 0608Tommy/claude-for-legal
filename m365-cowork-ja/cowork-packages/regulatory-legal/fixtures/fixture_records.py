"""Validate regulatory gap and public-comment records."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .fixture_classification import classification_complete
from .fixture_common import (
    CLOSURE_BASES,
    COMMENT_DECISIONS,
    FINAL_DISPOSITIONS,
    RECORD_KINDS,
    artifact_complete,
    exact_value,
    has_source_identity,
    object_field,
    parse_timestamp,
    string_field,
)
from .fixture_evidence import (
    artifacts_distinct,
    coverage_complete,
    egov_form_identity_complete,
    risk_acceptance_complete,
    route_consistent,
    submission_complete,
)

if TYPE_CHECKING:
    from .fixture_types import JsonObject, JsonValue


def _implementation_evidence_complete(value: JsonValue) -> bool:
    """Validate nonempty implementation evidence."""
    return (
        isinstance(value, list)
        and bool(value)
        and all(artifact_complete(item) for item in value)
    )


def _closure_core(
    record: JsonObject,
) -> tuple[JsonObject, JsonValue] | None:
    """Return validated common closure evidence."""
    closure = object_field(record, "closureEvidence")
    if closure is None:
        return None
    internal = closure.get("internalArtifact")
    complete = all(
        (
            closure.get("closureBasis") in CLOSURE_BASES,
            artifact_complete(internal),
            _implementation_evidence_complete(
                closure.get("implementationEvidence"),
            ),
            exact_value(closure.get("verifiedByObjectId")),
            parse_timestamp(closure.get("verifiedAt")) is not None,
        ),
    )
    return (closure, internal) if complete else None


def _closed_gap_complete(record: JsonObject) -> bool:
    """Validate a closed gap and its conditional evidence."""
    core = _closure_core(record)
    if core is None:
        return False
    closure, internal = core
    if closure.get("closureBasis") != "regulator-submission":
        return True
    return _regulator_submission_closure_complete(closure, internal)


def _regulator_submission_closure_complete(
    closure: JsonObject,
    internal: JsonValue,
) -> bool:
    """Validate regulator-submission artifacts and evidence."""
    evidence = _regulator_evidence(closure)
    if evidence is None:
        return False
    external, submission = evidence
    if not artifacts_distinct(internal, external):
        return False
    return _submitted_artifact_matches(external, submission)


def _regulator_evidence(
    closure: JsonObject,
) -> tuple[JsonObject, JsonObject] | None:
    """Return validated regulator-facing artifact and submission evidence."""
    external = closure.get("regulatorFacingArtifact")
    submission = closure.get("submissionEvidence")
    valid = all(
        (
            artifact_complete(external),
            route_consistent(closure.get("submissionRoute"), submission),
            isinstance(external, dict),
            isinstance(submission, dict),
        ),
    )
    if not valid or not isinstance(external, dict):
        return None
    if not isinstance(submission, dict):
        return None
    return external, submission


def _open_gap_complete(record: JsonObject) -> bool:
    """Validate an open or in-progress gap."""
    return all(
        (
            record.get("closureEvidence") is None,
            record.get("riskAcceptance") is None,
        ),
    )


def _risk_accepted_gap_complete(record: JsonObject) -> bool:
    """Validate a risk-accepted gap."""
    return all(
        (
            record.get("closureEvidence") is None,
            risk_acceptance_complete(record.get("riskAcceptance")),
        ),
    )


def _gap_base_valid(record: JsonObject) -> bool:
    """Validate shared source, classification, and coverage gates."""
    return all(
        (
            has_source_identity(record),
            classification_complete(record),
            coverage_complete(record),
        ),
    )


def validate_gap(record: JsonObject) -> bool:
    """Validate a persisted regulatory gap.

    Parameters
    ----------
    record
        Gap fixture.

    Returns
    -------
    bool
        Whether the gap satisfies classification, coverage, and evidence gates.

    """
    if not _gap_base_valid(record):
        return False
    status = string_field(record, "status")
    validators = {
        "open": _open_gap_complete,
        "in-progress": _open_gap_complete,
        "closed": _closed_gap_complete,
        "risk-accepted": _risk_accepted_gap_complete,
    }
    validator = validators.get(status) if status is not None else None
    return validator(record) if validator is not None else False


def _consultation_shape_valid(record: JsonObject) -> bool:
    """Validate a consultation record shape."""
    return all(
        (
            exact_value(record.get("proposalSnapshotId")),
            record.get("exceptionBasis") is None,
            record.get("noPriorConsultationProven") is False,
        ),
    )


def _exception_notice_shape_valid(record: JsonObject) -> bool:
    """Validate a proven no-prior-consultation notice."""
    if any(
        record.get(field) is not None
        for field in (
            "proposalPublishedAt",
            "commentOpenAt",
            "commentCloseAt",
        )
    ):
        return False
    basis = object_field(record, "exceptionBasis")
    return all(
        (
            basis is not None,
            record.get("noPriorConsultationProven") is True,
            basis is not None and exact_value(basis.get("provision")),
            basis is not None and exact_value(basis.get("reason")),
        ),
    )


def _result_only_shape_valid(record: JsonObject) -> bool:
    """Validate a result-only record shape."""
    return all(
        (
            record.get("exceptionBasis") is None,
            record.get("noPriorConsultationProven") is False,
            exact_value(record.get("resultSnapshotId")),
            parse_timestamp(record.get("resultPublishedAt")) is not None,
        ),
    )


def _record_kind_shape_valid(record: JsonObject) -> bool:
    """Dispatch record-kind-specific shape validation."""
    kind = string_field(record, "recordKind")
    validators = {
        "consultation": _consultation_shape_valid,
        "exception-notice": _exception_notice_shape_valid,
        "result-only": _result_only_shape_valid,
    }
    validator = validators.get(kind) if kind is not None else None
    return validator(record) if validator is not None else False


def _route_for_submission(
    record: JsonObject,
    submission: JsonObject,
) -> JsonObject | None:
    """Find the route named by submission evidence."""
    routes = record.get("submissionRoutes")
    if not isinstance(routes, list):
        return None
    route_id = submission.get("routeId")
    for route in routes:
        if isinstance(route, dict) and route.get("routeId") == route_id:
            return route
    return None


def _filed_artifacts(
    record: JsonObject,
) -> tuple[JsonObject, JsonValue] | None:
    """Return validated artifacts and submission evidence."""
    artifacts = object_field(record, "artifacts")
    submission = object_field(record, "submissionEvidence")
    if artifacts is None or submission is None:
        return None
    external = artifacts.get("regulatorFacing")
    internal = artifacts.get("internalAnalysis")
    complete = all(
        (
            submission_complete(submission),
            artifact_complete(external),
            not isinstance(internal, dict)
            or artifacts_distinct(internal, external),
        ),
    )
    if not complete:
        return None
    return submission, external


def _filed_route(
    record: JsonObject,
    submission: JsonObject,
) -> JsonObject | None:
    """Return a validated filed route."""
    route = _route_for_submission(record, submission)
    if route is None or route.get("method") == "unknown":
        return None
    if not route_consistent(route, submission):
        return None
    if not _egov_identity_valid(record, route, submission):
        return None
    return route


def _submitted_artifact_matches(
    external: JsonObject,
    submission: JsonObject,
) -> bool:
    """Validate the exact artifact named by submission evidence."""
    return all(
        (
            external.get("itemId")
            == submission.get("submittedArtifactItemId"),
            external.get("versionOrRevisionId")
            == submission.get("submittedArtifactVersionOrRevisionId"),
            external.get("contentHash")
            == submission.get("submittedArtifactHash"),
        ),
    )


def _filed_comment_complete(record: JsonObject) -> bool:
    """Validate conditional filed-comment evidence."""
    filed = _filed_artifacts(record)
    if filed is None:
        return False
    submission, external_value = filed
    if not isinstance(external_value, dict):
        return False
    if _filed_route(record, submission) is None:
        return False
    return _submitted_artifact_matches(external_value, submission)


def _egov_identity_valid(
    record: JsonObject,
    route: JsonObject,
    submission: JsonObject,
) -> bool:
    """Validate e-Gov identity only for e-Gov sources."""
    source_system = string_field(record, "sourceSystem")
    if source_system is None or not source_system.startswith("e-gov"):
        return True
    return egov_form_identity_complete(
        route,
        submission,
        record.get("caseId"),
    )


def _comment_base_valid(record: JsonObject) -> bool:
    """Validate common comment identity and enums."""
    decision = string_field(record, "decision")
    disposition = record.get("finalDisposition")
    return all(
        (
            has_source_identity(record),
            decision in COMMENT_DECISIONS,
            record.get("recordKind") in RECORD_KINDS,
            disposition is None or disposition in FINAL_DISPOSITIONS,
        ),
    )


def validate_comment(record: JsonObject) -> bool:
    """Validate a consultation, exception, or result-only record.

    Parameters
    ----------
    record
        Public-comment fixture.

    Returns
    -------
    bool
        Whether the record and conditional filing evidence are valid.

    """
    if not _comment_base_valid(record):
        return False
    decision = string_field(record, "decision")
    if not _record_kind_shape_valid(record):
        return False
    return decision != "filed" or _filed_comment_complete(record)
