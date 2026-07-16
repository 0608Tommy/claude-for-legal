"""Validate source-audit and authority fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from .fixture_classification import market_rule_context_valid
from .fixture_common import (
    array_field,
    exact_string_tuple,
    exact_value,
    nonempty_string_list,
    object_field,
    string_field,
)

if TYPE_CHECKING:
    from .fixture_types import JsonObject

_AUTHORITY_TYPES: Final = frozenset(
    {
        "ministry",
        "agency",
        "commission",
        "cabinet-office-commission",
        "exchange",
        "non-exchange-sro",
        "court",
        "legislature",
        "cabinet",
        "other",
    },
)
_CAA_REVISION: Final = "421AC0000000048_20240401_505AC0000000036"


def _public_155260508(case: JsonObject) -> bool:
    """Validate the APA Article 40(1) shortened-period case."""
    basis = object_field(case, "shortenedPeriodBasis")
    reason = string_field(basis, "reason") if basis is not None else None
    return all(
        (
            case.get("recordKind") == "consultation",
            basis is not None,
            basis is not None and basis.get("provision") == "40(1)",
            case.get("forbiddenBasis") == "39(4)(1)",
            case.get("commentOpenAt") == "2026-07-16T00:00:00+09:00",
            case.get("commentCloseAt") == "2026-07-29T23:59:00+09:00",
            reason is not None,
            reason is not None
            and "災害に備え可能な限り速やかに施行" in reason,
        ),
    )


def _public_155260717(case: JsonObject) -> bool:
    """Validate the no-prior-consultation result anomaly."""
    basis = object_field(case, "exceptionBasis")
    return all(
        (
            case.get("recordKind") == "exception-notice",
            basis is not None,
            basis is not None and basis.get("provision") == "39(4)(8)",
            case.get("proposalPublishedAt") is None,
            case.get("commentOpenAt") is None,
            case.get("commentCloseAt") is None,
            case.get("sourceControlFinding")
            == "apparent-late-result-publication-contrary-to-43(5)",
            case.get("promulgatedAt") == "2026-05-20T00:00:00+09:00",
            case.get("resultPublishedAt") == "2026-07-16T00:00:00+09:00",
        ),
    )


def _public_240000127(case: JsonObject) -> bool:
    """Validate the exact e-Gov route regression fixture."""
    route = object_field(case, "route")
    if route is None:
        return False
    return all(
        (
            case.get("recordKind") == "consultation",
            route.get("method") == "web-form",
            route.get("destinationSystem") == "e-Gov 意見提出フォーム",
            route.get("destinationAddressOrEndpoint")
            == "https://public-comment.e-gov.go.jp/pcm/2010",
            route.get("canonicalCaseEntryUrl")
            == "https://public-comment.e-gov.go.jp/pcm/detail"
            "?CLASSNAME=PCMMSTDETAIL&id=240000127",
            route.get("formAction")
            == "https://public-comment.e-gov.go.jp/pcm/2010",
            route.get("httpMethod") == "POST",
            route.get("formClassName") == "PCMIKENINPUT",
            route.get("caseId") == "240000127",
            route.get("routeId") == "240000127-egov-form",
            case.get("commentOpenAt") == "2026-07-16T00:00:00+09:00",
            case.get("commentCloseAt") == "2026-08-14T23:59:00+09:00",
            route.get("deadlineAt") == case.get("commentCloseAt"),
            route.get("verifiedAt") == "2026-07-16T20:20:55+09:00",
            route.get("instructionUrl")
            == "https://public-comment.e-gov.go.jp/pcm/download"
            "?seqNo=0000318027",
            route.get("instructionContentHash")
            == "sha256:e7bb3a9145c11b02f31c2b223a91d3c3b0a3f6168e060f"
            "1995fef0dcd93d5035",
            route.get("receiptOrPostmark") == "not-applicable",
        ),
    )


def _public_495260109(case: JsonObject) -> bool:
    """Validate the midnight deadline fixture."""
    return (
        case.get("commentOpenAt") == "2026-07-14T10:20:00+09:00"
        and case.get("commentCloseAt") == "2026-08-14T00:00:00+09:00"
    )


def _public_495260046(case: JsonObject) -> bool:
    """Validate the result and promulgation dates."""
    return (
        case.get("proposalPublishedAt") == "2026-05-01"
        and case.get("commentCloseAt") == "2026-06-01T12:00:00+09:00"
        and case.get("resultPublishedAt") == "2026-07-15"
        and case.get("promulgatedAt") == "2026-07-15"
        and case.get("finalDisposition") == "adopted"
    )


def _public_495250498(case: JsonObject) -> bool:
    """Validate proposal and final artifact version separation."""
    return (
        case.get("proposalTitleVersion") == "6.1"
        and case.get("finalArtifactVersion") == "7.0"
        and case.get("snapshotsSeparate") is True
    )


def validate_public_comment_audit(case: JsonObject) -> bool:
    """Validate one exact Japanese public-comment audit fixture.

    Parameters
    ----------
    case
        Public-comment audit fixture.

    Returns
    -------
    bool
        Whether exact dates, route, and version facts match.

    """
    validators = {
        "155260508": _public_155260508,
        "155260717": _public_155260717,
        "240000127": _public_240000127,
        "495260109": _public_495260109,
        "495260046": _public_495260046,
        "495250498": _public_495250498,
    }
    case_id = string_field(case, "caseId")
    validator = validators.get(case_id) if case_id is not None else None
    return validator(case) if validator is not None else False


def _mandate_complete(case: JsonObject) -> bool:
    """Validate a structured authority mandate."""
    mandate = object_field(case, "mandate")
    if mandate is None:
        return False
    return all(
        (
            case.get("authorityType") in _AUTHORITY_TYPES,
            exact_value(case.get("authorityId")),
            exact_value(case.get("displayName")),
            all(
                exact_value(mandate.get(field))
                for field in (
                    "sourceSystem",
                    "sourceItemId",
                    "sourceVersionOrRevisionId",
                    "description",
                )
            ),
            nonempty_string_list(mandate.get("provisions")),
        ),
    )


def _mandate_matches(
    mandate: JsonObject | None,
    provisions: set[str],
) -> bool:
    """Validate the common pinned establishment-law mandate."""
    if mandate is None:
        return False
    actual = exact_string_tuple(mandate.get("provisions"))
    return all(
        (
            mandate.get("sourceItemId") == "421AC0000000048",
            mandate.get("sourceVersionOrRevisionId") == _CAA_REVISION,
            actual is not None,
            actual is not None and set(actual) == provisions,
        ),
    )


def _caa_authority_valid(case: JsonObject) -> bool:
    """Validate the pinned Consumer Affairs Agency mandate."""
    mandate = object_field(case, "mandate")
    return all(
        (
            case.get("displayName") == "消費者庁",
            case.get("authorityType") == "agency",
            _mandate_matches(mandate, {"2", "3", "4"}),
        ),
    )


def _consumer_commission_valid(case: JsonObject) -> bool:
    """Validate the pinned Consumer Commission mandate."""
    mandate = object_field(case, "mandate")
    return all(
        (
            case.get("displayName") == "消費者委員会",
            case.get("authorityType") == "cabinet-office-commission",
            _mandate_matches(mandate, {"6", "7", "8"}),
        ),
    )


def validate_authority(case: JsonObject) -> bool:
    """Validate authority identity, type, and pinned mandate.

    Parameters
    ----------
    case
        Authority fixture.

    Returns
    -------
    bool
        Whether authority identity and mandate are exact.

    """
    if not _mandate_complete(case):
        return False
    validators = {
        "caa": _caa_authority_valid,
        "consumer-commission": _consumer_commission_valid,
    }
    authority_id = string_field(case, "authorityId")
    if authority_id == "caa-consumer-commission":
        return False
    validator = (
        validators.get(authority_id)
        if authority_id is not None
        else None
    )
    return validator(case) if validator is not None else True


def validate_source_health(case: JsonObject) -> bool:
    """Validate source retrieval and mixed-content metadata.

    Parameters
    ----------
    case
        Source-health fixture.

    Returns
    -------
    bool
        Whether retrieval metadata is safe and complete.

    """
    base_valid = all(
        (
            "authorityClass" not in case,
            case.get("retrievalMode")
            in {"direct", "adapter-required", "manual", "licensed"},
            case.get("encoding") in {"UTF-8", "Shift_JIS", "other"},
            nonempty_string_list(case.get("expectedContentClasses")),
            case.get("itemLevelClassificationRequired") is True,
        ),
    )
    if not base_valid:
        return False
    return _source_specific_health_valid(case)


def _house_health_valid(case: JsonObject) -> bool:
    """Validate the House bill-page encoding."""
    return case.get("encoding") == "Shift_JIS"


def _cyber_health_valid(case: JsonObject) -> bool:
    """Validate current cyber-office identity and historical alias."""
    aliases = array_field(case, "historicalAliases")
    return all(
        (
            case.get("displayNameJa") == "国家サイバー統括室",
            case.get("canonicalUrl") == "https://www.cyber.go.jp/",
            aliases is not None,
            aliases is not None and "NISC" in aliases,
        ),
    )


def _jpx_health_valid(case: JsonObject) -> bool:
    """Validate JPX market-rule context."""
    return market_rule_context_valid(
        case.get("marketRuleContext"),
        "exchange",
    )


def _source_specific_health_valid(case: JsonObject) -> bool:
    """Validate special source-health rules."""
    validators = {
        "house-of-representatives-bills": _house_health_valid,
        "cyber-go-jp": _cyber_health_valid,
        "jpx-rule": _jpx_health_valid,
    }
    source_system = string_field(case, "sourceSystem")
    validator = (
        validators.get(source_system)
        if source_system is not None
        else None
    )
    return validator(case) if validator is not None else True


def gazette_approval_required(case: JsonObject) -> bool:
    """Return the Gazette Act Article 16 approval result.

    Parameters
    ----------
    case
        Gazette database fixture.

    Returns
    -------
    bool
        Whether Article 16 approval is required.

    """
    return (
        case.get("containsAllElectronicGazetteRecords") is True
        and case.get("intendedForOthers") is True
    )


def validate_gazette_terms(case: JsonObject) -> bool:
    """Validate the non-blanket Gazette site-terms interpretation.

    Parameters
    ----------
    case
        Gazette terms fixture.

    Returns
    -------
    bool
        Whether the terms distinction is valid.

    """
    return (
        case.get("burdeningRobotCrawlerProhibited") is True
        and case.get("allAutomationProhibited") is False
    )


def validate_jurisdiction_source(case: JsonObject) -> bool:
    """Validate jurisdiction-specific official-source routing.

    Parameters
    ----------
    case
        Jurisdiction-source fixture.

    Returns
    -------
    bool
        Whether the source belongs to the jurisdiction.

    """
    routes = {
        "federal-register": "US",
        "eur-lex-official-journal": "EU",
    }
    source_system = string_field(case, "sourceSystem")
    return (
        source_system is not None
        and routes.get(source_system) == case.get("jurisdiction")
    )
