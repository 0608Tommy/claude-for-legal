"""Validate source classification and market-rule context."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from .fixture_common import (
    LIFECYCLE_STATUSES,
    NORMATIVE_FORCES,
    exact_value,
    has_source_identity,
    nonempty_string_list,
    object_field,
    string_field,
    string_list,
)

if TYPE_CHECKING:
    from .fixture_types import JsonObject, JsonValue

_APA_GUIDANCE_PROVISIONS: Final = frozenset(
    {"32", "33", "34", "35", "36", "36-2", "36-3"},
)
_APPLICABILITY_STATUSES: Final = frozenset(
    {"applies", "potentially-applies", "does-not-apply", "unknown"},
)
_MARKET_KINDS: Final = frozenset({"exchange", "non-exchange-sro"})
_FIEA_ID: Final = "323AC0000000025"
_FIEA_REVISION: Final = "323AC0000000025_20260525_506AC0000000052"


def _approval_basis_complete(basis: JsonObject) -> bool:
    """Validate an exact market-rule approval basis."""
    return (
        all(
            exact_value(basis.get(field))
            for field in (
                "sourceSystem",
                "sourceItemId",
                "sourceVersionOrRevisionId",
            )
        )
        and nonempty_string_list(basis.get("provisions"))
        and isinstance(basis.get("exactRuleOrExceptionPinned"), bool)
    )


def _default_exchange_approval(
    context: JsonObject,
    basis: JsonObject,
) -> bool:
    """Validate the unpinned TSE approval default."""
    provisions = basis.get("provisions")
    return all(
        (
            context.get("approvalRequired") == "unknown",
            context.get("approvalAuthority") is None,
            context.get("approvalStatus") == "unknown",
            basis.get("sourceItemId") == _FIEA_ID,
            basis.get("sourceVersionOrRevisionId") == _FIEA_REVISION,
            isinstance(provisions, list),
            isinstance(provisions, list) and "149" in provisions,
        ),
    )


def _required_approval(context: JsonObject) -> bool:
    """Validate an approval-required state."""
    return all(
        (
            context.get("approvalRequired") is True,
            exact_value(context.get("approvalAuthority")),
            context.get("approvalStatus") in {"approved", "pending"},
        ),
    )


def _not_required_approval(context: JsonObject) -> bool:
    """Validate an approval-not-required state."""
    return all(
        (
            context.get("approvalRequired") is False,
            context.get("approvalAuthority") is None,
            context.get("approvalStatus") == "not-required",
        ),
    )


def _unknown_approval(context: JsonObject) -> bool:
    """Validate an unknown approval state."""
    return all(
        (
            context.get("approvalRequired") == "unknown",
            context.get("approvalAuthority") is None,
            context.get("approvalStatus") == "unknown",
        ),
    )


def _pinned_approval_state(context: JsonObject) -> bool:
    """Validate approval state after an exact rule or exception pin."""
    validators = (
        _required_approval,
        _not_required_approval,
        _unknown_approval,
    )
    return any(validator(context) for validator in validators)


def _kind_matches(kind: str, expected_kind: str | None) -> bool:
    """Validate an optional expected market kind."""
    return expected_kind is None or kind == expected_kind


def _market_context(
    value: JsonValue,
    expected_kind: str | None,
) -> tuple[JsonObject, str] | None:
    """Return a validated base market context and kind."""
    if not isinstance(value, dict):
        return None
    kind = string_field(value, "kind")
    valid = all(
        (
            kind in _MARKET_KINDS,
            kind is not None and _kind_matches(kind, expected_kind),
            exact_value(value.get("issuerEntity")),
            nonempty_string_list(value.get("coveredParties")),
        ),
    )
    return (value, kind) if valid and kind is not None else None


def _fiea_version_valid(basis: JsonObject) -> bool:
    """Validate the pinned FIEA revision when applicable."""
    return (
        basis.get("sourceItemId") != _FIEA_ID
        or basis.get("sourceVersionOrRevisionId") == _FIEA_REVISION
    )


def _exchange_approval_valid(
    context: JsonObject,
    basis: JsonObject,
) -> bool:
    """Validate an exchange approval determination."""
    if not _approval_basis_complete(basis):
        return False
    if not _fiea_version_valid(basis):
        return False
    if basis.get("exactRuleOrExceptionPinned") is False:
        return _default_exchange_approval(context, basis)
    return _pinned_approval_state(context)


def _exchange_context_valid(context: JsonObject) -> bool:
    """Validate exchange venue and approval basis."""
    if not exact_value(context.get("venue")):
        return False
    basis = object_field(context, "approvalBasis")
    return (
        basis is not None
        and _exchange_approval_valid(context, basis)
    )


def market_rule_context_valid(
    value: JsonValue,
    expected_kind: str | None = None,
) -> bool:
    """Validate exchange or non-exchange SRO context.

    Parameters
    ----------
    value
        Candidate market-rule context.
    expected_kind
        Required market-rule kind, if known.

    Returns
    -------
    bool
        Whether issuer, venue, approval, and covered parties are valid.

    """
    validated = _market_context(value, expected_kind)
    if validated is None:
        return False
    context, kind = validated
    if kind == "non-exchange-sro":
        return (
            context.get("venue") is None
            and _pinned_approval_state(context)
        )
    return _exchange_context_valid(context)


def _apa_guidance_basis_complete(basis: JsonObject) -> bool:
    """Validate the APA Articles 32 through 36-3 basis."""
    provisions = basis.get("provisions")
    return (
        exact_value(basis.get("statute"))
        and nonempty_string_list(provisions)
        and isinstance(provisions, list)
        and set(provisions).issubset(_APA_GUIDANCE_PROVISIONS)
    )


def _sector_guidance_basis_complete(basis: JsonObject) -> bool:
    """Validate an exact sector-statute guidance basis."""
    return (
        exact_value(basis.get("statute"))
        and nonempty_string_list(basis.get("provisions"))
    )


def _other_guidance_basis_complete(basis: JsonObject) -> bool:
    """Validate an exact other-statutory basis."""
    return exact_value(basis.get("statute"))


def _administrative_guidance_complete(
    record: JsonObject,
    basis: JsonObject,
) -> bool:
    """Validate an affirmative administrative-guidance classification."""
    basis_type = string_field(basis, "basisType")
    if record.get("normativeForce") != "nonbinding":
        return False
    validators = {
        "apa-arts-32-through-36-3": _apa_guidance_basis_complete,
        "sector-statute": _sector_guidance_basis_complete,
        "other": _other_guidance_basis_complete,
    }
    validator = validators.get(basis_type) if basis_type is not None else None
    return validator(basis) if validator is not None else False


def _guidance_complete(record: JsonObject, basis: JsonObject) -> bool:
    """Validate administrative-guidance equivalence and legal basis."""
    is_guidance = record.get("isAdministrativeGuidance")
    class_is_guidance = (
        record.get("instrumentClass") == "administrative-guidance"
    )
    if is_guidance is not class_is_guidance:
        return False
    if is_guidance is True:
        return _administrative_guidance_complete(record, basis)
    return basis.get("basisType") in {"none", "unknown"}


def _base_classification_complete(record: JsonObject) -> bool:
    """Validate independent classification dimensions."""
    applicability = object_field(record, "applicability")
    if applicability is None:
        return False
    return all(
        (
            string_list(record.get("jurisdictions")),
            isinstance(record.get("nexus"), list),
            exact_value(record.get("instrumentClass")),
            record.get("normativeForce") in NORMATIVE_FORCES,
            record.get("lifecycleStatus") in LIFECYCLE_STATUSES,
            applicability.get("status") in _APPLICABILITY_STATUSES,
            isinstance(record.get("displayTags"), list),
            isinstance(record.get("isAdministrativeGuidance"), bool),
        ),
    )


def _market_classification_complete(record: JsonObject) -> bool:
    """Validate optional market-rule classification details."""
    instrument_class = string_field(record, "instrumentClass")
    if instrument_class not in {"exchange-rule", "sro-rule"}:
        return True
    expected_kind = (
        "exchange"
        if instrument_class == "exchange-rule"
        else "non-exchange-sro"
    )
    return all(
        (
            record.get("normativeForce")
            == "binding-on-covered-parties",
            market_rule_context_valid(
                record.get("marketRuleContext"),
                expected_kind,
            ),
        ),
    )


def classification_complete(record: JsonObject) -> bool:
    """Validate independent legal classification fields.

    Parameters
    ----------
    record
        Regulatory source or gap record.

    Returns
    -------
    bool
        Whether classification is complete and internally consistent.

    """
    if not _base_classification_complete(record):
        return False
    basis = object_field(record, "administrativeGuidanceBasis")
    if basis is None or not _guidance_complete(record, basis):
        return False
    return _market_classification_complete(record)


def validate_source(record: JsonObject) -> bool:
    """Validate source identity, classification, and pinned APA text.

    Parameters
    ----------
    record
        Regulatory source fixture.

    Returns
    -------
    bool
        Whether the source fixture is valid.

    """
    if not has_source_identity(record) or not classification_complete(record):
        return False
    is_apa_revision = (
        record.get("sourceItemId") == "405AC0000000088"
        and record.get("sourceVersionOrRevisionId")
        == "405AC0000000088_20260624_508AC0000000046"
    )
    if not is_apa_revision:
        return True
    return record.get("canonicalUrl") == (
        "https://laws.e-gov.go.jp/api/2/law_data/"
        "405AC0000000088_20260624_508AC0000000046"
    )
