#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Validate Microsoft 365 Cowork manifest PNG icons without dependencies."""

from __future__ import annotations

import json
import struct
import sys
import zlib
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Final, NamedTuple, cast

if TYPE_CHECKING:
    from collections.abc import Iterator

PNG_SIGNATURE: Final = b"\x89PNG\r\n\x1a\n"
IHDR_FORMAT: Final = ">IIBBBBB"
IHDR_LENGTH: Final = 13
RGBA_BYTES_PER_PIXEL: Final = 4
TRANSPARENT_ALPHA: Final = 0
OPAQUE_ALPHA: Final = 255
WHITE_RGB: Final = (255, 255, 255)
PNG_CHUNK_TYPE_LENGTH: Final = 4
PNG_RESERVED_BYTE_INDEX: Final = 2
ASCII_UPPERCASE_START: Final = ord("A")
ASCII_UPPERCASE_END: Final = ord("Z")
PNG_ANCILLARY_BIT: Final = 0x20
MAX_PLTE_LENGTH: Final = 256 * 3
SUPPORTED_CRITICAL_CHUNKS: Final = frozenset(
    {
        b"IHDR",
        b"PLTE",
        b"IDAT",
        b"IEND",
    },
)
FILTER_NONE: Final = 0
FILTER_SUB: Final = 1
FILTER_UP: Final = 2
FILTER_AVERAGE: Final = 3
FILTER_PAETH: Final = 4
PNG_FILTER_TYPES: Final = frozenset(
    {
        FILTER_NONE,
        FILTER_SUB,
        FILTER_UP,
        FILTER_AVERAGE,
        FILTER_PAETH,
    },
)
EXPECTED_PACKAGE_COUNT: Final = 12
EXPECTED_DIMENSIONS: Final = {
    "color": (192, 192),
    "outline": (32, 32),
}
ROOT: Final = Path(__file__).resolve().parent.parent
PACKAGE_ROOT: Final = ROOT / "m365-cowork-ja" / "cowork-packages"


class IconValidationError(ValueError):
    """Report malformed icon data or an invalid manifest icon declaration."""


class PngHeader(NamedTuple):
    """Hold the validated PNG image header."""

    width: int
    height: int


class PngChunk(NamedTuple):
    """Hold one CRC-validated PNG chunk."""

    chunk_type: bytes
    payload: bytes
    next_offset: int


class PngPixelProfile(NamedTuple):
    """Summarize reconstructed RGBA pixels for icon policy checks."""

    has_transparent: bool
    has_visible: bool
    all_opaque: bool
    visible_pixels_white: bool


def _error(context: str, detail: str) -> IconValidationError:
    """Build a consistently contextualized validation error."""
    return IconValidationError(f"{context}: {detail}")


def _validate_chunk_type(chunk_type: bytes, context: str) -> None:
    """Require a four-letter PNG type with an uppercase reserved byte."""
    if (
        len(chunk_type) != PNG_CHUNK_TYPE_LENGTH
        or not chunk_type.isalpha()
    ):
        raise _error(
            context,
            "PNG chunk type must be exactly four ASCII letters",
        )
    reserved_byte = chunk_type[PNG_RESERVED_BYTE_INDEX]
    if not ASCII_UPPERCASE_START <= reserved_byte <= ASCII_UPPERCASE_END:
        raise _error(
            context,
            "PNG chunk type reserved third byte must be uppercase",
        )


def _read_chunk(data: bytes, offset: int, context: str) -> PngChunk:
    """Read and CRC-check one PNG chunk."""
    minimum_chunk_length = 12
    if len(data) - offset < minimum_chunk_length:
        raise _error(context, "truncated PNG chunk")
    payload_length = struct.unpack_from(">I", data, offset)[0]
    payload_start = offset + 8
    payload_end = payload_start + payload_length
    next_offset = payload_end + 4
    if next_offset > len(data):
        raise _error(context, "PNG chunk length exceeds file size")
    chunk_type = data[slice(offset + 4, payload_start)]
    _validate_chunk_type(chunk_type, context)
    payload = data[payload_start:payload_end]
    expected_crc = struct.unpack_from(">I", data, payload_end)[0]
    actual_crc = zlib.crc32(payload, zlib.crc32(chunk_type))
    if actual_crc != expected_crc:
        label = chunk_type.decode("ascii", errors="replace")
        raise _error(context, f"{label} chunk CRC mismatch")
    return PngChunk(chunk_type, payload, next_offset)


def _parse_header(
    payload: bytes,
    expected_dimensions: tuple[int, int],
    context: str,
) -> PngHeader:
    """Validate the exact Microsoft 365 icon IHDR contract."""
    if len(payload) != IHDR_LENGTH:
        raise _error(context, "IHDR must contain exactly 13 bytes")
    width, height, bit_depth, color_type, compression, filtering, interlace = (
        struct.unpack(IHDR_FORMAT, payload)
    )
    if (width, height) != expected_dimensions:
        expected_width, expected_height = expected_dimensions
        raise _error(
            context,
            f"dimensions must be {expected_width}x{expected_height}",
        )
    if (bit_depth, color_type) != (8, 6):
        raise _error(context, "IHDR must declare 8-bit RGBA pixels")
    if (compression, filtering, interlace) != (0, 0, 0):
        raise _error(
            context,
            "IHDR must use standard compression/filtering and no interlace",
        )
    return PngHeader(width, height)


def _inflate_scanlines(
    compressed: bytes,
    expected_length: int,
    context: str,
) -> bytes:
    """Fully decode exactly one bounded zlib stream."""
    decoder = zlib.decompressobj()
    output_limit = expected_length + 1
    try:
        decoded = decoder.decompress(compressed, output_limit)
    except zlib.error as error:
        raise _error(context, f"invalid IDAT zlib stream: {error}") from error
    _validate_output_budget(
        decoded,
        decoder.unconsumed_tail,
        expected_length,
        context,
    )
    _validate_zlib_stream(
        decoder.unused_data,
        context,
        reached_end=decoder.eof,
    )
    return decoded


def _validate_output_budget(
    decoded: bytes,
    unconsumed_tail: bytes,
    expected_length: int,
    context: str,
) -> None:
    """Reject output beyond the exact scanline budget."""
    if len(decoded) > expected_length or unconsumed_tail:
        raise _error(
            context,
            "decoded IDAT data exceeds the output budget",
        )
    if len(decoded) != expected_length:
        raise _error(
            context,
            (
                f"decoded data length must be {expected_length}, "
                f"got {len(decoded)}"
            ),
        )


def _validate_zlib_stream(
    unused_data: bytes,
    context: str,
    *,
    reached_end: bool,
) -> None:
    """Require one complete zlib stream with no trailing stream data."""
    if not reached_end:
        raise _error(context, "IDAT zlib stream is incomplete")
    if unused_data:
        raise _error(context, "IDAT contains trailing compressed data")


def _paeth(left: int, above: int, upper_left: int) -> int:
    """Return the PNG Paeth predictor."""
    prediction = left + above - upper_left
    left_distance = abs(prediction - left)
    above_distance = abs(prediction - above)
    upper_left_distance = abs(prediction - upper_left)
    if (
        left_distance <= above_distance
        and left_distance <= upper_left_distance
    ):
        return left
    if above_distance <= upper_left_distance:
        return above
    return upper_left


def _reconstruct_row(
    filter_type: int,
    filtered: bytearray,
    previous: bytearray,
    context: str,
) -> bytearray:
    """Reconstruct one PNG row for filter types zero through four."""
    if filter_type not in PNG_FILTER_TYPES:
        raise _error(context, f"unsupported PNG filter type {filter_type}")
    for index, value in enumerate(filtered):
        left = (
            filtered[index - RGBA_BYTES_PER_PIXEL]
            if index >= RGBA_BYTES_PER_PIXEL
            else 0
        )
        above = previous[index]
        upper_left = (
            previous[index - RGBA_BYTES_PER_PIXEL]
            if index >= RGBA_BYTES_PER_PIXEL
            else 0
        )
        predictor = _filter_predictor(
            filter_type,
            left,
            above,
            upper_left,
        )
        filtered[index] = (value + predictor) & 0xFF
    return filtered


def _filter_predictor(
    filter_type: int,
    left: int,
    above: int,
    upper_left: int,
) -> int:
    """Return the predictor for a validated PNG filter type."""
    if filter_type == FILTER_NONE:
        return 0
    if filter_type == FILTER_SUB:
        return left
    if filter_type == FILTER_UP:
        return above
    if filter_type == FILTER_AVERAGE:
        return (left + above) // 2
    return _paeth(left, above, upper_left)


def _reconstructed_rows(
    decoded: bytes,
    header: PngHeader,
    context: str,
) -> Iterator[bytearray]:
    """Yield each reconstructed RGBA scanline."""
    row_length = header.width * RGBA_BYTES_PER_PIXEL
    stride = row_length + 1
    previous = bytearray(row_length)
    for row_index in range(header.height):
        offset = row_index * stride
        filter_type = decoded[offset]
        filtered = bytearray(decoded[slice(offset + 1, offset + stride)])
        current = _reconstruct_row(
            filter_type,
            filtered,
            previous,
            context,
        )
        yield current
        previous = current


def _pixel_profile(
    decoded: bytes,
    header: PngHeader,
    context: str,
) -> PngPixelProfile:
    """Reconstruct all scanlines and summarize their icon-policy properties."""
    profile = PngPixelProfile(
        has_transparent=False,
        has_visible=False,
        all_opaque=True,
        visible_pixels_white=True,
    )
    for current in _reconstructed_rows(decoded, header, context):
        row_length = len(current)
        for index in range(0, row_length, RGBA_BYTES_PER_PIXEL):
            pixel = current[index:index + RGBA_BYTES_PER_PIXEL]
            profile = _merge_pixel_profiles(
                profile,
                _profile_pixel(pixel),
            )
    return profile


def _profile_pixel(pixel: bytearray) -> PngPixelProfile:
    """Summarize one reconstructed RGBA pixel."""
    red, green, blue, alpha = pixel
    transparent = alpha == TRANSPARENT_ALPHA
    return PngPixelProfile(
        has_transparent=transparent,
        has_visible=not transparent,
        all_opaque=alpha == OPAQUE_ALPHA,
        visible_pixels_white=(
            transparent or (red, green, blue) == WHITE_RGB
        ),
    )


def _merge_pixel_profiles(
    first: PngPixelProfile,
    second: PngPixelProfile,
) -> PngPixelProfile:
    """Combine two pixel-policy summaries."""
    return PngPixelProfile(
        has_transparent=(
            first.has_transparent or second.has_transparent
        ),
        has_visible=first.has_visible or second.has_visible,
        all_opaque=first.all_opaque and second.all_opaque,
        visible_pixels_white=(
            first.visible_pixels_white and second.visible_pixels_white
        ),
    )


def _validate_color_profile(
    profile: PngPixelProfile,
    context: str,
) -> None:
    """Require a fully opaque Microsoft color icon."""
    if not profile.all_opaque:
        raise _error(
            context,
            "color icon must use alpha 255 for every pixel",
        )


def _validate_outline_profile(
    profile: PngPixelProfile,
    context: str,
) -> None:
    """Require transparent background and white visible outline pixels."""
    if not profile.has_transparent:
        raise _error(
            context,
            "outline icon must contain at least one transparent pixel",
        )
    if not profile.visible_pixels_white:
        raise _error(
            context,
            (
                "every visible outline pixel must be pure white "
                "RGB (255, 255, 255)"
            ),
        )


def _validate_pixel_profile(
    profile: PngPixelProfile,
    icon_kind: str | None,
    context: str,
) -> None:
    """Require generic visibility and Microsoft color/outline pixel policy."""
    if not profile.has_visible:
        raise _error(context, "PNG must contain at least one visible pixel")
    if icon_kind is None:
        return
    if icon_kind not in EXPECTED_DIMENSIONS:
        raise _error(context, "icon kind must be color or outline")
    if icon_kind == "color":
        _validate_color_profile(profile, context)
        return
    _validate_outline_profile(profile, context)


def validate_png_bytes(
    data: bytes,
    expected_dimensions: tuple[int, int],
    context: str,
    *,
    icon_kind: str | None = None,
) -> None:
    """Validate one complete non-interlaced, 8-bit RGBA PNG image.

    Parameters
    ----------
    data
        Complete PNG file bytes.
    expected_dimensions
        Required ``(width, height)`` pair.
    context
        Human-readable source name for errors.
    icon_kind
        Optional ``color`` or ``outline`` Microsoft icon pixel policy.

    Raises
    ------
    IconValidationError
        If the PNG structure, pixels, or dimensions are invalid.

    """
    chunks = _read_chunks(data, context)
    header, compressed = _validate_chunk_structure(
        chunks,
        expected_dimensions,
        context,
    )
    row_length = header.width * RGBA_BYTES_PER_PIXEL + 1
    expected_length = header.height * row_length
    decoded = _inflate_scanlines(
        compressed,
        expected_length,
        context,
    )
    profile = _pixel_profile(decoded, header, context)
    _validate_pixel_profile(profile, icon_kind, context)


def _read_chunks(data: bytes, context: str) -> list[PngChunk]:
    """Read all chunks through IEND and reject trailing file data."""
    if not data.startswith(PNG_SIGNATURE):
        raise _error(context, "invalid PNG signature")
    offset = len(PNG_SIGNATURE)
    chunks: list[PngChunk] = []
    while offset < len(data):
        chunk = _read_chunk(data, offset, context)
        chunks.append(chunk)
        offset = chunk.next_offset
        if chunk.chunk_type == b"IEND":
            break
    _validate_chunk_terminator(chunks, offset, len(data), context)
    return chunks


def _validate_chunk_terminator(
    chunks: list[PngChunk],
    offset: int,
    data_length: int,
    context: str,
) -> None:
    """Require IEND at the physical end of the PNG file."""
    if not chunks:
        raise _error(context, "PNG is missing IEND")
    if chunks[-1].chunk_type != b"IEND":
        raise _error(context, "PNG is missing IEND")
    if offset != data_length:
        raise _error(context, "PNG contains trailing data after IEND")


def _validate_boundary_chunks(
    chunks: list[PngChunk],
    context: str,
) -> list[bytes]:
    """Require exactly one leading IHDR and one empty trailing IEND."""
    chunk_types = [chunk.chunk_type for chunk in chunks]
    if chunk_types[0] != b"IHDR":
        raise _error(context, "IHDR must be the first PNG chunk")
    if chunk_types.count(b"IHDR") != 1:
        raise _error(context, "PNG must contain exactly one IHDR")
    _validate_iend(chunks, chunk_types, context)
    return chunk_types


def _validate_iend(
    chunks: list[PngChunk],
    chunk_types: list[bytes],
    context: str,
) -> None:
    """Require exactly one empty IEND chunk."""
    if chunk_types.count(b"IEND") != 1:
        raise _error(context, "PNG must contain exactly one IEND")
    if chunks[-1].payload:
        raise _error(context, "IEND must be empty")


def _is_critical_chunk(chunk_type: bytes) -> bool:
    """Return whether the PNG chunk's ancillary bit marks it critical."""
    return chunk_type[0] & PNG_ANCILLARY_BIT == 0


def _validate_critical_chunks(
    chunks: list[PngChunk],
    context: str,
) -> None:
    """Reject every critical chunk outside the supported PNG profile."""
    for chunk in chunks:
        if (
            _is_critical_chunk(chunk.chunk_type)
            and chunk.chunk_type not in SUPPORTED_CRITICAL_CHUNKS
        ):
            label = chunk.chunk_type.decode("ascii", errors="replace")
            raise _error(
                context,
                f"unsupported critical PNG chunk {label}",
            )


def _contiguous_idat_indices(
    chunk_types: list[bytes],
    context: str,
) -> list[int]:
    """Return the nonempty contiguous range of IDAT chunk indexes."""
    indices = [
        index
        for index, chunk_type in enumerate(chunk_types)
        if chunk_type == b"IDAT"
    ]
    if not indices:
        raise _error(context, "PNG is missing IDAT")
    expected = list(range(indices[0], indices[-1] + 1))
    if indices != expected:
        raise _error(context, "IDAT chunks must be contiguous")
    return indices


def _validate_plte_payload(chunk: PngChunk, context: str) -> None:
    """Validate the optional truecolor suggested-palette payload."""
    payload_length = len(chunk.payload)
    invalid_lengths = (
        payload_length == 0,
        payload_length % 3 != 0,
        payload_length > MAX_PLTE_LENGTH,
    )
    if any(invalid_lengths):
        raise _error(context, "PLTE must contain 1 to 256 RGB entries")


def _plte_indices(chunks: list[PngChunk]) -> list[int]:
    """Return indexes of optional PLTE chunks."""
    return [
        index
        for index, chunk in enumerate(chunks)
        if chunk.chunk_type == b"PLTE"
    ]


def _validate_plte(
    chunks: list[PngChunk],
    first_idat_index: int,
    context: str,
) -> None:
    """Validate the optional single PLTE chunk before IDAT."""
    indices = _plte_indices(chunks)
    if len(indices) > 1:
        raise _error(context, "PNG must contain at most one PLTE")
    if not indices:
        return
    plte_index = indices[0]
    if plte_index > first_idat_index:
        raise _error(context, "PLTE must precede IDAT")
    _validate_plte_payload(chunks[plte_index], context)


def _validate_chunk_structure(
    chunks: list[PngChunk],
    expected_dimensions: tuple[int, int],
    context: str,
) -> tuple[PngHeader, bytes]:
    """Validate PNG chunk ordering and return its header and IDAT bytes."""
    _validate_critical_chunks(chunks, context)
    chunk_types = _validate_boundary_chunks(chunks, context)
    idat_indices = _contiguous_idat_indices(chunk_types, context)
    _validate_plte(chunks, idat_indices[0], context)
    header = _parse_header(
        chunks[0].payload,
        expected_dimensions,
        context,
    )
    compressed = b"".join(chunks[index].payload for index in idat_indices)
    return header, compressed


def validate_png(
    path: Path,
    expected_dimensions: tuple[int, int],
    *,
    icon_kind: str | None = None,
) -> None:
    """Validate one PNG file from disk.

    Parameters
    ----------
    path
        PNG path.
    expected_dimensions
        Required ``(width, height)`` pair.
    icon_kind
        Optional ``color`` or ``outline`` Microsoft icon pixel policy.

    Raises
    ------
    IconValidationError
        If the file is missing or malformed.

    """
    if not path.is_file() or path.is_symlink():
        raise _error(path.as_posix(), "icon must be a regular file")
    validate_png_bytes(
        path.read_bytes(),
        expected_dimensions,
        path.as_posix(),
        icon_kind=icon_kind,
    )


def _require_object(value: object, context: str) -> dict[str, object]:
    """Require a JSON object."""
    if not isinstance(value, dict):
        raise _error(context, "must be a JSON object")
    return cast("dict[str, object]", value)


def _relative_icon_path(
    package_dir: Path,
    icon_name: str,
    value: object,
) -> PurePosixPath:
    """Validate one package-relative manifest icon path."""
    if not isinstance(value, str):
        raise _error(
            package_dir.as_posix(),
            f"icons.{icon_name} must be a nonempty string",
        )
    if not value:
        raise _error(
            package_dir.as_posix(),
            f"icons.{icon_name} must be a nonempty string",
        )
    relative = PurePosixPath(value)
    if _unsafe_icon_path(relative, value):
        raise _error(
            package_dir.as_posix(),
            f"icons.{icon_name} must be a safe package-relative path",
        )
    return relative


def _unsafe_icon_path(relative: PurePosixPath, value: str) -> bool:
    """Return whether an icon path is absolute, escaping, or non-POSIX."""
    return relative.is_absolute() or ".." in relative.parts or "\\" in value


def _manifest_icon_path(
    package_dir: Path,
    icon_name: str,
    value: object,
) -> Path:
    """Resolve one safe package-local manifest icon path."""
    relative = _relative_icon_path(package_dir, icon_name, value)
    path = package_dir.joinpath(*relative.parts)
    try:
        path.resolve().relative_to(package_dir.resolve())
    except ValueError as error:
        raise _error(
            package_dir.as_posix(),
            f"icons.{icon_name} escapes the package directory",
        ) from error
    return path


def _load_manifest_icons(manifest_path: Path) -> dict[str, object]:
    """Load and validate a manifest's exact icon declaration object."""
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise _error(
            manifest_path.as_posix(),
            "manifest must be a regular file",
        )
    try:
        raw_manifest: object = json.loads(
            manifest_path.read_text(encoding="utf-8"),
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise _error(
            manifest_path.as_posix(),
            f"invalid JSON: {error}",
        ) from error
    manifest = _require_object(raw_manifest, manifest_path.as_posix())
    icons = _require_object(
        manifest.get("icons"),
        f"{manifest_path.as_posix()} icons",
    )
    if set(icons) != set(EXPECTED_DIMENSIONS):
        raise _error(
            manifest_path.as_posix(),
            "icons must declare exactly color and outline",
        )
    return icons


def validate_manifest_icons(package_dir: Path) -> int:
    """Validate both icons declared by one package manifest.

    Parameters
    ----------
    package_dir
        Directory containing ``manifest.json`` and its declared icons.

    Returns
    -------
    int
        Number of validated icons.

    Raises
    ------
    IconValidationError
        If the manifest or either icon is invalid.

    """
    manifest_path = package_dir / "manifest.json"
    icons = _load_manifest_icons(manifest_path)
    paths: set[Path] = set()
    for icon_name, dimensions in EXPECTED_DIMENSIONS.items():
        path = _manifest_icon_path(
            package_dir,
            icon_name,
            icons.get(icon_name),
        )
        if path in paths:
            raise _error(
                manifest_path.as_posix(),
                "color and outline must reference different files",
            )
        validate_png(path, dimensions, icon_kind=icon_name)
        paths.add(path)
    return len(paths)


def validate_icon_fleet(
    package_root: Path = PACKAGE_ROOT,
    expected_package_count: int = EXPECTED_PACKAGE_COUNT,
) -> int:
    """Validate every manifest icon in the exact Cowork source fleet.

    Parameters
    ----------
    package_root
        Root containing package directories.
    expected_package_count
        Exact number of package manifests required.

    Returns
    -------
    int
        Number of validated icons.

    Raises
    ------
    IconValidationError
        If the package count or any manifest icon is invalid.

    """
    package_dirs = sorted(
        path.parent
        for path in package_root.glob("*/manifest.json")
        if path.is_file()
    )
    if len(package_dirs) != expected_package_count:
        raise _error(
            package_root.as_posix(),
            (
                f"expected {expected_package_count} package manifests, "
                f"found {len(package_dirs)}"
            ),
        )
    return sum(validate_manifest_icons(path) for path in package_dirs)


def main() -> int:
    """Validate the repository Cowork icon fleet.

    Returns
    -------
    int
        Zero when all manifest icons are valid.

    """
    try:
        icon_count = validate_icon_fleet()
    except (IconValidationError, OSError) as error:
        sys.stderr.write(f"ERROR: {error}\n")
        return 1
    sys.stdout.write(
        f"Microsoft 365 Cowork icons: OK ({icon_count} manifest icons)\n",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
