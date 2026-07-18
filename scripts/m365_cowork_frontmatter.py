#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Parse and validate Microsoft 365 Cowork skill frontmatter."""

from __future__ import annotations

import re
from collections.abc import Hashable, Mapping
from pathlib import Path
from typing import Final, NamedTuple, cast

import yaml

__all__ = (
    "FrontmatterError",
    "FrontmatterPolicy",
    "extract_frontmatter",
    "frontmatter_fields",
    "frontmatter_scalar",
    "frontmatter_validation_errors",
    "has_marketplace_purchase_cta",
    "parse_frontmatter",
    "skill_frontmatter_errors",
    "skill_set_frontmatter_errors",
)

ENGLISH_PURCHASE_CTA_RE: Final = re.compile(
    r"\b(?:buy|purchase)\s+"
    r"(?:a|an|the|this|our|your|subscriptions?|now|here)\b|"
    r"\bsubscribe\s+"
    r"(?:now|here|today|at|on|via|through|from|to|for)\b",
    re.IGNORECASE,
)
JAPANESE_PURCHASE_CTA_RE: Final = re.compile(
    r"(?:購入|購読|申し?込|サブスク(?:リプション)?(?:へ)?登録)"
    r"(?:してください|下さい|するには|はこちら|できます|ください|へ)",
)
EXTERNAL_MARKETPLACE_RE: Final = re.compile(
    r"https?://|www\.|"
    r"\b(?:external\s+)?(?:marketplace|app\s+store)\b|"
    r"(?:外部(?:の)?(?:マーケットプレイス|アプリストア|ストア)|"
    r"マーケットプレイス|アプリストア)",
    re.IGNORECASE,
)
FRONTMATTER_FIELD_RE: Final = re.compile(
    r"^([A-Za-z][A-Za-z0-9_-]*):",
)
BLOCK_MARKERS: Final = frozenset({">", ">-", ">+", "|", "|-", "|+"})


class FrontmatterError(ValueError):
    """Report malformed or structurally invalid YAML frontmatter."""


class FrontmatterPolicy(NamedTuple):
    """Hold machine-contract limits for one skill frontmatter document."""

    allowed_fields: frozenset[str]
    name_minimum: int
    name_maximum: int
    name_pattern: str
    description_minimum: int
    description_maximum: int


class _DuplicateKeyError(ValueError):
    """Report one duplicate YAML mapping key."""


def _construct_unique_mapping(
    loader: yaml.BaseLoader,
    node: yaml.MappingNode,
) -> dict[object, object]:
    """Construct one mapping without silently replacing duplicate keys."""
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if not isinstance(key, Hashable):
            message = "YAML mapping keys must be hashable"
            raise FrontmatterError(message)
        if key in mapping:
            message = f"duplicate YAML key {key!r}"
            raise _DuplicateKeyError(message)
        mapping[key] = loader.construct_object(value_node, deep=True)
    return mapping


StrictBaseLoader: Final = cast(
    "type[yaml.BaseLoader]",
    type("_CoworkBaseLoader", (yaml.BaseLoader,), {}),
)
StrictBaseLoader.add_constructor(
    "tag:yaml.org,2002:map",
    _construct_unique_mapping,
)


def extract_frontmatter(text: str, path: Path) -> tuple[str, ...]:
    """Extract lines between exact Markdown frontmatter boundaries."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        message = f"{path.as_posix()} has no opening frontmatter boundary"
        raise FrontmatterError(message)
    try:
        closing_index = lines.index("---", 1)
    except ValueError as error:
        message = f"{path.as_posix()} has no closing frontmatter boundary"
        raise FrontmatterError(message) from error
    return tuple(lines[1:closing_index])


def frontmatter_fields(lines: tuple[str, ...]) -> tuple[str, ...]:
    """Return unique top-level field names from raw frontmatter lines."""
    fields = {
        match.group(1)
        for line in lines
        if (match := FRONTMATTER_FIELD_RE.match(line)) is not None
    }
    return tuple(sorted(fields))


def frontmatter_scalar(
    lines: tuple[str, ...],
    field: str,
) -> str | None:
    """Return one simple inline scalar from raw frontmatter lines."""
    prefix = f"{field}:"
    for line in lines:
        if not line.startswith(prefix):
            continue
        value = line.removeprefix(prefix).strip()
        if value in BLOCK_MARKERS:
            return None
        return value.strip("\"'")
    return None


def _reject_explicit_yaml_tags(source: str, path: Path) -> None:
    """Reject explicit standard and custom YAML tags before construction."""
    try:
        has_explicit_tag = any(
            isinstance(token, yaml.TagToken)
            for token in yaml.scan(source, Loader=yaml.BaseLoader)
        )
    except (
        yaml.YAMLError,
        LookupError,
        OverflowError,
        RecursionError,
        TypeError,
        ValueError,
    ) as error:
        message = f"{path.as_posix()}: malformed YAML frontmatter: {error}"
        raise FrontmatterError(message) from error
    if has_explicit_tag:
        message = (
            f"{path.as_posix()}: malformed YAML frontmatter: "
            "explicit YAML tags are forbidden"
        )
        raise FrontmatterError(message)


def _load_yaml_document(source: str, path: Path) -> object:
    """Safely load one strict YAML document."""
    _reject_explicit_yaml_tags(source, path)
    try:
        loader = StrictBaseLoader(source)
        try:
            document: object = loader.get_single_data()
        finally:
            loader.dispose()
    except _DuplicateKeyError as error:
        message = f"{path.as_posix()}: {error}"
        raise FrontmatterError(message) from error
    except (
        yaml.YAMLError,
        LookupError,
        OverflowError,
        RecursionError,
        TypeError,
        ValueError,
    ) as error:
        message = f"{path.as_posix()}: malformed YAML frontmatter: {error}"
        raise FrontmatterError(message) from error
    return document


def _require_yaml_mapping(
    document: object,
    path: Path,
) -> dict[str, object]:
    """Require one parsed document to be a string-keyed mapping."""
    if not isinstance(document, dict):
        message = f"{path.as_posix()}: frontmatter must be a YAML mapping"
        raise FrontmatterError(message)
    mapping = cast("dict[object, object]", document)
    if not all(isinstance(key, str) for key in mapping):
        message = f"{path.as_posix()}: frontmatter field names must be strings"
        raise FrontmatterError(message)
    return cast("dict[str, object]", mapping)


def _load_yaml_mapping(source: str, path: Path) -> dict[str, object]:
    """Safely load one strict YAML mapping."""
    return _require_yaml_mapping(_load_yaml_document(source, path), path)


def parse_frontmatter(text: str, path: Path) -> dict[str, object]:
    """Parse one Markdown document's strict safe YAML frontmatter.

    Parameters
    ----------
    text:
        Full Markdown text.
    path:
        Source path used in error messages.

    Returns
    -------
    dict[str, object]
        Parsed top-level YAML mapping.

    Raises
    ------
    FrontmatterError
        If boundaries, YAML syntax, duplicate keys, or the root type are
        invalid.

    """
    source = "\n".join(extract_frontmatter(text, path)) + "\n"
    return _load_yaml_mapping(source, path)


def _string_field(
    document: dict[str, object],
    field: str,
) -> tuple[str | None, tuple[str, ...]]:
    """Return one required nonempty string field and its validation errors."""
    if field not in document:
        return None, (f"{field} is required",)
    value = document[field]
    if not isinstance(value, str):
        return None, (f"{field} must be a string",)
    if not value.strip():
        return None, (f"{field} must be a nonempty string",)
    return value, ()


def _name_errors(
    document: dict[str, object],
    expected_name: str,
    policy: FrontmatterPolicy,
) -> tuple[str, ...]:
    """Return official identifier and folder-match errors."""
    name, errors = _string_field(document, "name")
    if name is None:
        return errors
    details = list(errors)
    if name != expected_name:
        details.append(f"name must match folder {expected_name}")
    if not policy.name_minimum <= len(name) <= policy.name_maximum:
        details.append(
            f"name has {len(name)} characters; expected "
            f"{policy.name_minimum}-{policy.name_maximum}",
        )
    if re.fullmatch(policy.name_pattern, name) is None:
        details.append(f"name does not match {policy.name_pattern!r}")
    return tuple(details)


def has_marketplace_purchase_cta(description: str) -> bool:
    """Detect a conservative external-marketplace purchase call to action."""
    has_purchase_cta = (
        ENGLISH_PURCHASE_CTA_RE.search(description) is not None
        or JAPANESE_PURCHASE_CTA_RE.search(description) is not None
    )
    return (
        has_purchase_cta
        and EXTERNAL_MARKETPLACE_RE.search(description) is not None
    )


def _description_errors(
    document: dict[str, object],
    policy: FrontmatterPolicy,
) -> tuple[str, ...]:
    """Return official description-boundary and conservative CTA errors."""
    description, errors = _string_field(document, "description")
    if description is None:
        return errors
    details = list(errors)
    if not (
        policy.description_minimum
        <= len(description)
        <= policy.description_maximum
    ):
        details.append(
            f"description has {len(description)} characters; expected "
            f"{policy.description_minimum}-{policy.description_maximum}",
        )
    if has_marketplace_purchase_cta(description):
        details.append(
            "description contains an external-marketplace purchase or "
            "subscription call to action",
        )
    return tuple(details)


def frontmatter_validation_errors(
    document: dict[str, object],
    expected_name: str,
    policy: FrontmatterPolicy,
) -> tuple[str, ...]:
    """Return deterministic official Cowork frontmatter errors."""
    unsupported = sorted(set(document) - policy.allowed_fields)
    errors = (
        (f"unexpected frontmatter fields {unsupported}",)
        if unsupported
        else ()
    )
    return (
        *errors,
        *_name_errors(document, expected_name, policy),
        *_description_errors(document, policy),
    )


def skill_frontmatter_errors(
    data: bytes,
    path: Path,
    expected_name: str,
    policy: FrontmatterPolicy,
    maximum_characters: int,
) -> tuple[str, ...]:
    """Return UTF-8, size, YAML, and field errors for one ``SKILL.md``."""
    try:
        text = data.decode("utf-8")
    except UnicodeError:
        return (f"{path.as_posix()}: skill is not UTF-8",)
    if len(text) > maximum_characters:
        return (
            f"{path.as_posix()}: {len(text)} characters exceeds "
            f"{maximum_characters}",
        )
    try:
        document = parse_frontmatter(text, path)
    except FrontmatterError as error:
        return (str(error),)
    return frontmatter_validation_errors(document, expected_name, policy)


def skill_set_frontmatter_errors(
    entries: Mapping[str, bytes],
    slugs: tuple[str, ...],
    policy: FrontmatterPolicy,
    maximum_characters: int,
) -> tuple[str, ...]:
    """Return the first frontmatter failure across declared skill entries."""
    for slug in slugs:
        name = f"skills/{slug}/SKILL.md"
        data = entries.get(name)
        if data is None:
            return (f"required source file missing: {name}",)
        errors = skill_frontmatter_errors(
            data,
            Path(name),
            slug,
            policy,
            maximum_characters,
        )
        if errors:
            return tuple(f"{name}: {error}" for error in errors)
    return ()
