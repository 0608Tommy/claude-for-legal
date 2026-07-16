"""Define recursive JSON fixture types and format validation."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import TYPE_CHECKING, TypeGuard, cast

if TYPE_CHECKING:
    from pathlib import Path

type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonArray = list[JsonValue]
type JsonObject = dict[str, JsonValue]
type Validator = Callable[[JsonObject], bool]


class FixtureValidationError(ValueError):
    """Indicate malformed fixtures or an unexpected validation result."""


def _json_array(value: list[object]) -> bool:
    """Validate every member of a JSON array."""
    return all(is_json_value(item) for item in value)


def _json_mapping(value: dict[object, object]) -> bool:
    """Validate every key and value of a JSON object."""
    return all(
        isinstance(key, str) and is_json_value(item)
        for key, item in value.items()
    )


def is_json_value(value: object) -> TypeGuard[JsonValue]:
    """Return whether a value belongs to the recursive JSON value type.

    Parameters
    ----------
    value
        Candidate value.

    Returns
    -------
    bool
        Whether the value is a valid JSON value.

    """
    if value is None or isinstance(value, str | int | float | bool):
        return True
    if isinstance(value, list):
        return _json_array(cast("list[object]", value))
    return (
        isinstance(value, dict)
        and _json_mapping(cast("dict[object, object]", value))
    )


def is_json_object(value: object) -> TypeGuard[JsonObject]:
    """Return whether a value is a string-keyed JSON object.

    Parameters
    ----------
    value
        Candidate value.

    Returns
    -------
    bool
        Whether the value is a JSON object.

    """
    return (
        isinstance(value, dict)
        and _json_mapping(cast("dict[object, object]", value))
    )


def load_json_object(path: Path) -> JsonObject:
    """Load and validate a JSON object from disk.

    Parameters
    ----------
    path
        JSON document path.

    Returns
    -------
    JsonObject
        Validated JSON object.

    Raises
    ------
    FixtureValidationError
        If the document root is not a JSON object.

    """
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    if is_json_object(raw):
        return raw
    message = f"{path.as_posix()}: fixture root must be a JSON object"
    raise FixtureValidationError(message)


def require_object(value: JsonValue, context: str) -> JsonObject:
    """Require a JSON object.

    Parameters
    ----------
    value
        Candidate value.
    context
        Human-readable value location.

    Returns
    -------
    JsonObject
        Validated object.

    Raises
    ------
    FixtureValidationError
        If the value is not an object.

    """
    if isinstance(value, dict):
        return value
    message = f"{context}: expected a JSON object"
    raise FixtureValidationError(message)


def require_array(value: JsonValue, context: str) -> JsonArray:
    """Require a JSON array.

    Parameters
    ----------
    value
        Candidate value.
    context
        Human-readable value location.

    Returns
    -------
    JsonArray
        Validated array.

    Raises
    ------
    FixtureValidationError
        If the value is not an array.

    """
    if isinstance(value, list):
        return value
    message = f"{context}: expected a JSON array"
    raise FixtureValidationError(message)


def require_string(value: JsonValue, context: str) -> str:
    """Require a nonblank string.

    Parameters
    ----------
    value
        Candidate value.
    context
        Human-readable value location.

    Returns
    -------
    str
        Nonblank string.

    Raises
    ------
    FixtureValidationError
        If the value is not a nonblank string.

    """
    if isinstance(value, str) and value.strip():
        return value
    message = f"{context}: expected a nonblank string"
    raise FixtureValidationError(message)


def case_name(case: JsonObject) -> str:
    """Return a validated fixture case name.

    Parameters
    ----------
    case
        Fixture case.

    Returns
    -------
    str
        Case name.

    """
    return require_string(case.get("name"), "fixture case name")


def expected_boolean(case: JsonObject, field: str) -> bool:
    """Return a required expected Boolean.

    Parameters
    ----------
    case
        Fixture case.
    field
        Expected-result field name.

    Returns
    -------
    bool
        Expected Boolean value.

    Raises
    ------
    FixtureValidationError
        If the field is not Boolean.

    """
    value = case.get(field)
    if isinstance(value, bool):
        return value
    message = f"{case_name(case)}: {field} must be Boolean"
    raise FixtureValidationError(message)
