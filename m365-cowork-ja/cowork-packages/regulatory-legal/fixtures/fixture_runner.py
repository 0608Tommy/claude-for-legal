"""Run all package-local regulatory fixture groups."""

from __future__ import annotations

from copy import deepcopy
from typing import Final, NamedTuple

from .fixture_audits import (
    gazette_approval_required,
    validate_authority,
    validate_gazette_terms,
    validate_jurisdiction_source,
    validate_public_comment_audit,
    validate_source_health,
)
from .fixture_classification import classification_complete, validate_source
from .fixture_common import CLOSURE_BASES, artifact_complete
from .fixture_evidence import coverage_complete, route_consistent
from .fixture_mutations import MutationOutcome, run_direct_mutations
from .fixture_operations import (
    cursor_should_advance,
    validate_scope,
    validate_setup_session,
    validate_write,
)
from .fixture_records import validate_comment, validate_gap
from .fixture_types import (
    FixtureValidationError,
    JsonObject,
    Validator,
    case_name,
    expected_boolean,
    require_array,
    require_object,
)

_GAZETTE_APPROVAL_CASE_COUNT: Final = 2


class GroupSpec(NamedTuple):
    """Describe one ordinary fixture group."""

    key: str
    validator: Validator
    expected_field: str = "expectedValid"


class SuiteResult(NamedTuple):
    """Summarize a completed fixture suite."""

    case_count: int
    direct_outcomes: list[MutationOutcome]


def _closure_probe(case: JsonObject) -> bool:
    """Validate focused closure-basis and implementation evidence probes."""
    evidence = case.get("implementationEvidence")
    return (
        case.get("closureBasis") in CLOSURE_BASES
        and isinstance(evidence, list)
        and bool(evidence)
        and all(artifact_complete(item) for item in evidence)
    )


def _submission_probe(case: JsonObject) -> bool:
    """Validate focused route and submission consistency probes."""
    return route_consistent(case.get("route"), case.get("submission"))


_GROUP_SPECS: Final = (
    GroupSpec("classificationProbeCases", classification_complete),
    GroupSpec("gapCases", validate_gap),
    GroupSpec("commentCases", validate_comment),
    GroupSpec("coverageProbeCases", coverage_complete),
    GroupSpec("closureProbeCases", _closure_probe),
    GroupSpec("submissionProbeCases", _submission_probe),
    GroupSpec("publicCommentAuditCases", validate_public_comment_audit),
    GroupSpec("authorityCases", validate_authority),
    GroupSpec("sourceHealthCases", validate_source_health),
    GroupSpec("jurisdictionSourceCases", validate_jurisdiction_source),
    GroupSpec("setupSessionCases", validate_setup_session),
    GroupSpec("writeCases", validate_write),
    GroupSpec("cursorCases", cursor_should_advance, "expectedAdvance"),
    GroupSpec("scopeCases", validate_scope),
)
_MUTATION_VALIDATORS: Final[dict[str, Validator]] = {
    "gap": validate_gap,
    "comment": validate_comment,
    "public-comment": validate_public_comment_audit,
    "setup": validate_setup_session,
    "scope": validate_scope,
    "authority": validate_authority,
    "cursor": cursor_should_advance,
    "source": validate_source,
}


def _case_payload(case: JsonObject) -> JsonObject:
    """Return a nested record or the case itself."""
    value = case.get("record")
    return value if isinstance(value, dict) else case


def _result_mismatch(
    name: str,
    *,
    expected: bool,
    actual: bool,
) -> FixtureValidationError:
    """Build a result-mismatch exception."""
    message = f"{name}: expected {expected}, got {actual}"
    return FixtureValidationError(message)


def _run_group(document: JsonObject, spec: GroupSpec) -> int:
    """Run one ordinary fixture group."""
    values = require_array(document.get(spec.key), spec.key)
    count = 0
    for value in values:
        case = require_object(value, spec.key)
        actual = spec.validator(_case_payload(case))
        expected = expected_boolean(case, spec.expected_field)
        if actual != expected:
            raise _result_mismatch(
                case_name(case),
                expected=expected,
                actual=actual,
            )
        count += 1
    return count


def _run_source_cases(document: JsonObject) -> int:
    """Run source and embedded setup cases."""
    values = require_array(document.get("sourceCases"), "sourceCases")
    count = 0
    for value in values:
        case = require_object(value, "sourceCases")
        payload = _case_payload(case)
        validator = (
            validate_setup_session
            if payload.get("recordType") == "setup-session"
            else validate_source
        )
        actual = validator(payload)
        expected = expected_boolean(case, "expectedValid")
        if actual != expected:
            raise _result_mismatch(
                case_name(case),
                expected=expected,
                actual=actual,
            )
        count += 1
    return count


def _find_open_gap(document: JsonObject) -> JsonObject:
    """Return the known-valid open gap fixture."""
    values = require_array(document.get("gapCases"), "gapCases")
    for value in values:
        case = require_object(value, "gapCases")
        if case.get("name") == "open-gap-with-required-scope-coverage":
            record = case.get("record")
            return require_object(record, "open gap record")
    message = "gapCases: missing open gap base"
    raise FixtureValidationError(message)


def _run_gap_status_probes(document: JsonObject) -> int:
    """Run status mutations through the full gap validator."""
    base = _find_open_gap(document)
    values = require_array(
        document.get("gapStatusProbeCases"),
        "gapStatusProbeCases",
    )
    count = 0
    for value in values:
        case = require_object(value, "gapStatusProbeCases")
        record = deepcopy(base)
        record["status"] = case.get("status")
        actual = validate_gap(record)
        expected = expected_boolean(case, "expectedValid")
        if actual != expected:
            raise _result_mismatch(
                case_name(case),
                expected=expected,
                actual=actual,
            )
        count += 1
    return count


def _run_gazette_cases(document: JsonObject) -> int:
    """Run Gazette approval and terms cases."""
    values = require_array(document.get("gazetteCases"), "gazetteCases")
    count = 0
    for index, value in enumerate(values):
        case = require_object(value, "gazetteCases")
        validator = (
            gazette_approval_required
            if index < _GAZETTE_APPROVAL_CASE_COUNT
            else validate_gazette_terms
        )
        expected_field = (
            "expectedApprovalRequired"
            if index < _GAZETTE_APPROVAL_CASE_COUNT
            else "expectedValid"
        )
        actual = validator(case)
        expected = expected_boolean(case, expected_field)
        if actual != expected:
            raise _result_mismatch(
                case_name(case),
                expected=expected,
                actual=actual,
            )
        count += 1
    return count


def _validate_direct_outcomes(
    outcomes: list[MutationOutcome],
) -> None:
    """Require every direct mutation to fail closed."""
    for outcome in outcomes:
        if outcome.result is not False:
            message = (
                f"{outcome.name}: direct mutation expected False, "
                f"got {outcome.result}"
            )
            raise FixtureValidationError(message)


def run_fixture_suite(document: JsonObject) -> SuiteResult:
    """Run every contract and direct-mutation fixture.

    Parameters
    ----------
    document
        Complete fixture document.

    Returns
    -------
    SuiteResult
        Case count and named direct outcomes.

    Raises
    ------
    FixtureValidationError
        If any case produces an unexpected result.

    """
    count = _run_source_cases(document)
    for spec in _GROUP_SPECS:
        count += _run_group(document, spec)
    count += _run_gap_status_probes(document)
    count += _run_gazette_cases(document)
    outcomes = run_direct_mutations(document, _MUTATION_VALIDATORS)
    _validate_direct_outcomes(outcomes)
    return SuiteResult(count + len(outcomes), outcomes)
