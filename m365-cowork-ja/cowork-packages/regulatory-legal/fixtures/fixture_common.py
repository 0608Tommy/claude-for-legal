"""Provide shared constants and scalar fixture validators."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from .fixture_types import JsonObject, JsonValue

NORMATIVE_FORCES: Final = frozenset(
    {
        "binding",
        "nonbinding",
        "binding-on-covered-parties",
        "contractual",
        "internal",
        "unknown",
    },
)
LIFECYCLE_STATUSES: Final = frozenset(
    {
        "proposed",
        "current",
        "future-effective",
        "not-adopted",
        "withdrawn",
        "superseded",
        "repealed",
    },
)
RECORD_KINDS: Final = frozenset(
    {"consultation", "exception-notice", "result-only"},
)
FINAL_DISPOSITIONS: Final = frozenset(
    {"adopted", "not-adopted", "withdrawn"},
)
COMMENT_DECISIONS: Final = frozenset(
    {"undecided", "filing", "not_filing", "filed", "withdrawn"},
)
SETUP_STATUSES: Final = frozenset(
    {"in-progress", "paused", "complete", "abandoned"},
)
CLOSURE_BASES: Final = frozenset(
    {
        "policy-applied",
        "control-implemented",
        "regulator-submission",
        "not-applicable",
        "other",
    },
)
PLACEHOLDERS: Final = frozenset(
    {"source-specific", "tbd", "unknown", "[placeholder]"},
)
SUBMISSION_FIELDS: Final = frozenset(
    {
        "routeId",
        "submissionMethod",
        "destinationSystem",
        "destinationAddressOrEndpoint",
        "instructionUrl",
        "instructionContentHash",
        "routeDeadlineAt",
        "receiptOrPostmark",
        "routeVerifiedAt",
        "caseId",
        "submittedArtifactItemId",
        "submittedArtifactVersionOrRevisionId",
        "submittedArtifactHash",
        "submittedByObjectId",
        "submittedAt",
        "officialDeadlineVerifiedAt",
        "receiptOrReferenceId",
        "receiptArtifactItemId",
        "receiptArtifactVersionOrRevisionId",
        "receiptArtifactHash",
    },
)
AUDITED_STAGES: Final = (
    "official-feed-reader",
    "official-status-verifier",
    "materiality-filter",
    "digest-writer",
)


def object_field(record: JsonObject, field: str) -> JsonObject | None:
    """Return an object field when present.

    Parameters
    ----------
    record
        Source object.
    field
        Field name.

    Returns
    -------
    JsonObject or None
        Object field or ``None``.

    """
    value = record.get(field)
    return value if isinstance(value, dict) else None


def array_field(record: JsonObject, field: str) -> list[JsonValue] | None:
    """Return an array field when present.

    Parameters
    ----------
    record
        Source object.
    field
        Field name.

    Returns
    -------
    list[JsonValue] or None
        Array field or ``None``.

    """
    value = record.get(field)
    return value if isinstance(value, list) else None


def string_field(record: JsonObject, field: str) -> str | None:
    """Return a string field when present.

    Parameters
    ----------
    record
        Source object.
    field
        Field name.

    Returns
    -------
    str or None
        String field or ``None``.

    """
    value = record.get(field)
    return value if isinstance(value, str) else None


def exact_value(value: JsonValue) -> bool:
    """Return whether a value is a nonblank, non-placeholder string.

    Parameters
    ----------
    value
        Candidate JSON value.

    Returns
    -------
    bool
        Whether the value is exact.

    """
    return (
        isinstance(value, str)
        and bool(value.strip())
        and value.strip().lower() not in PLACEHOLDERS
    )


def nonempty_string_list(value: JsonValue) -> bool:
    """Validate a nonempty array of exact strings.

    Parameters
    ----------
    value
        Candidate JSON value.

    Returns
    -------
    bool
        Whether the value is a nonempty exact-string array.

    """
    return (
        isinstance(value, list)
        and bool(value)
        and all(exact_value(item) for item in value)
    )


def string_list(value: JsonValue) -> bool:
    """Validate an array containing only exact strings.

    Parameters
    ----------
    value
        Candidate JSON value.

    Returns
    -------
    bool
        Whether the value is an exact-string array.

    """
    return isinstance(value, list) and all(
        exact_value(item) for item in value
    )


def exact_string_tuple(value: JsonValue) -> tuple[str, ...] | None:
    """Convert an exact-string array to a typed tuple.

    Parameters
    ----------
    value
        Candidate JSON array.

    Returns
    -------
    tuple[str, ...] or None
        Typed strings or ``None`` for an invalid array.

    """
    if not isinstance(value, list):
        return None
    strings: list[str] = []
    for item in value:
        if not exact_value(item) or not isinstance(item, str):
            return None
        strings.append(item)
    return tuple(strings)


def parse_timestamp(value: JsonValue) -> datetime | None:
    """Parse a nonblank ISO-8601 timestamp.

    Parameters
    ----------
    value
        Candidate timestamp.

    Returns
    -------
    datetime or None
        Parsed timestamp or ``None``.

    """
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def has_source_identity(record: JsonObject) -> bool:
    """Validate the generic source identity.

    Parameters
    ----------
    record
        Regulatory source record.

    Returns
    -------
    bool
        Whether all identity fields are exact.

    """
    return all(
        exact_value(record.get(field))
        for field in (
            "sourceSystem",
            "sourceItemId",
            "sourceVersionOrRevisionId",
        )
    )


def artifact_complete(value: JsonValue) -> bool:
    """Validate an exact artifact identity.

    Parameters
    ----------
    value
        Candidate artifact.

    Returns
    -------
    bool
        Whether item, version, and hash are exact.

    """
    if not isinstance(value, dict):
        return False
    return all(
        exact_value(value.get(field))
        for field in ("itemId", "versionOrRevisionId", "contentHash")
    )
